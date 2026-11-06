/* Démo « IA privée et connaissances » : la question se tape, JARVIS fouille les
   documents (balayage, compteur de passages), répond mot à mot avec ses
   citations, montre le passage exact, puis propose une action qui attend
   « Approuver ». Démarre à l'entrée dans la fenêtre, se met en pause hors écran.
   Sans JavaScript, l'état statique (première question répondue) reste lisible. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="ia"]');
  if (!root || !window.requestAnimationFrame || !window.Promise) return;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var S = reduce ? 0.12 : 1;

  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }

  /* ---------- Horloge interne : n'avance que si la démo est visible ---------- */
  var clock = 0, last = 0, running = false, raf = 0, timers = [], tweens = [], run = 0;
  function loop(t) {
    raf = 0;
    if (!running) return;
    clock += Math.min(64, t - last);
    last = t;
    tweens.slice().forEach(function (tw) {
      var k = Math.min(1, (clock - tw.t0) / tw.d);
      tw.fn(k);
      if (k >= 1) { tweens.splice(tweens.indexOf(tw), 1); tw.done(); }
    });
    var due = timers.filter(function (x) { return x.at <= clock; });
    timers = timers.filter(function (x) { return x.at > clock; });
    due.forEach(function (x) { x.fn(); });
    if (timers.length || tweens.length) raf = requestAnimationFrame(loop);
  }
  function kick() { if (running && !raf) { last = performance.now(); raf = requestAnimationFrame(loop); } }
  function wait(ms) {
    var rid = run;
    return new Promise(function (res) {
      timers.push({ at: clock + ms * S, fn: function () { if (rid === run) res(); } });
      kick();
    });
  }
  function tween(ms, fn) {
    var rid = run;
    return new Promise(function (res) {
      tweens.push({ t0: clock, d: Math.max(1, ms * S), fn: fn, done: function () { if (rid === run) res(); } });
      kick();
    });
  }
  function setRunning(on) { running = on; if (on) kick(); }

  /* ---------- Éléments ---------- */
  var log = $("[data-log]"), typed = $("[data-typed]"), send = $(".ia-send"), count = $("[data-count]");
  var tabsEl = $("[data-tabs]"), stack = $("[data-stack]"), sr = $("[data-sr]");
  var docs = $$(".ia-doc"), chips = $$(".ia-chip"), tpls = $$("template[data-ia-sc]");
  var total = docs.reduce(function (a, d) { return a + (+d.getAttribute("data-pass") || 0); }, 0);
  var cur = 0, curCite = "", started = false, quoteLive = true;

  function fmt(n) { return Math.round(n).toLocaleString("fr-CA"); }
  function hhmm() { var d = new Date(); return d.getHours() + " h " + ("0" + d.getMinutes()).slice(-2); }
  function moveKids(from, to) { to.innerHTML = ""; while (from && from.firstChild) to.appendChild(from.firstChild); }
  /* Sur grand écran, la conversation défile d'elle-même vers le dernier message */
  function follow(smooth) {
    var max = log.scrollHeight - log.clientHeight;
    if (max <= 0) return;
    if (smooth && log.scrollTo && !reduce) log.scrollTo({ top: max, behavior: "smooth" });
    else log.scrollTop = max;
  }

  function setChip(i) {
    chips.forEach(function (c, k) {
      c.classList.toggle("is-on", k === i);
      c.setAttribute("aria-pressed", k === i ? "true" : "false");
    });
  }

  function resetDocs() {
    docs.forEach(function (d) {
      d.classList.remove("is-scan", "is-hit", "is-miss", "is-focus");
      $(".ia-hit", d).textContent = "";
    });
  }

  function parseHits(str) {
    var out = {};
    (str || "").split("|").forEach(function (p) {
      if (!p) return;
      var kv = p.split(":");
      out[kv[0]] = kv[1].split(",");
    });
    return out;
  }

  /* ---------- Citation → passage exact ---------- */
  function focusCite(n, force) {
    n = String(n);
    if (n === curCite && !force) return;
    var page = $('.ia-page[data-c="' + n + '"]', stack);
    if (!page) return;
    curCite = n;
    $$(".ia-page", stack).forEach(function (p) {
      p.classList.toggle("is-on", p === page);
      var ps = $(".ia-pass", p);
      if (ps) ps.classList.remove("is-on");
    });
    var pass = $(".ia-pass", page);
    requestAnimationFrame(function () { requestAnimationFrame(function () { if (pass) pass.classList.add("is-on"); }); });
    $$(".ia-tab", tabsEl).forEach(function (t) { t.classList.toggle("is-on", t.getAttribute("data-c") === n); });
    $$(".ia-cite", log).forEach(function (c) { c.classList.toggle("is-on", c.getAttribute("data-c") === n); });
    var doc = page.getAttribute("data-doc");
    docs.forEach(function (d) { d.classList.toggle("is-focus", d.getAttribute("data-doc") === doc); });
    var quote = $(".ia-quote", log);
    if (quoteLive && quote && pass) {
      quote.innerHTML = "";
      var b = document.createElement("b");
      b.textContent = "Source " + n + " · " + $("header b", page).textContent + " · " + $("header small", page).textContent;
      quote.appendChild(b);
      quote.appendChild(document.createTextNode(pass.textContent.trim()));
      quote.hidden = false;
    }
  }

  root.addEventListener("click", function (e) {
    var c = e.target.closest(".ia-cite, .ia-tab");
    if (c) { focusCite(c.getAttribute("data-c")); return; }
    var chip = e.target.closest(".ia-chip");
    if (chip) { play(+chip.getAttribute("data-sc")); return; }
    if (e.target.closest("[data-replay]")) { play(cur); return; }
    var btn = e.target.closest("[data-do]");
    if (btn) decide(btn.closest(".ia-act"), btn.getAttribute("data-do"));
  });
  root.addEventListener("pointerover", function (e) {
    if (e.pointerType !== "mouse") return;
    var c = e.target.closest(".ia-cite, .ia-tab");
    if (c) focusCite(c.getAttribute("data-c"));
  });

  /* ---------- Approuver / Ignorer ---------- */
  function decide(act, what) {
    if (!act || act.getAttribute("data-state")) return;
    var done = $(".ia-act-done", act);
    act.setAttribute("data-state", what);
    if (what !== "ok") {
      done.textContent = "Ignoré. Rien n’a été fait, rien n’est parti.";
      sr.textContent = done.textContent;
      follow(true);
      return;
    }
    var steps = $$(".ia-track li", act), rid = run;
    steps[0].classList.add("on");
    follow(true);
    wait(700).then(function () {
      steps[1].classList.add("on");
      return wait(950);
    }).then(function () {
      if (rid !== run) return;
      steps[2].classList.add("on");
      act.classList.add("is-conf");
      done.textContent = done.getAttribute("data-done") + " Confirmé à " + hhmm() + ".";
      sr.textContent = "Action confirmée. " + done.textContent;
      follow(true);
    });
  }

  /* ---------- Réponse mot à mot ---------- */
  function splitWords(el) {
    var toks = [];
    (function walk(node) {
      [].slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/([ \t\n\r]+)/).forEach(function (p) {
            if (!p) return;
            if (/^[ \t\n\r]+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var s = document.createElement("span");
            s.className = "ia-w";
            s.textContent = p;
            frag.appendChild(s);
            toks.push(s);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1) {
          if (n.classList.contains("ia-cite")) toks.push(n);
          else if (n.namespaceURI === "http://www.w3.org/1999/xhtml") walk(n);
        }
      });
    })(el);
    return toks;
  }

  function stream(ans, onCite) {
    var toks = splitWords(ans);
    ans.classList.add("is-stream");
    function show(t) {
      t.classList.add("on");
      for (var a = t.parentNode; a && a !== ans; a = a.parentNode) a.classList.add("on");
      if (t.classList.contains("ia-cite")) onCite(t.getAttribute("data-c"));
    }
    if (reduce) {
      toks.forEach(show);
      follow(false);
      return Promise.resolve();
    }
    var i = 0;
    function next() {
      if (i > 0) toks[i - 1].classList.remove("cur");
      if (i >= toks.length) return Promise.resolve();
      var t = toks[i++];
      show(t);
      t.classList.add("cur");
      follow(false);
      var w = t.textContent;
      var d = t.classList.contains("ia-cite") ? 190 : /[.:;!?]$/.test(w) ? 170 : /,$/.test(w) ? 100 : 36 + Math.random() * 30;
      return wait(d).then(next);
    }
    return next();
  }

  /* ---------- Recherche dans les documents ---------- */
  function search(bot, hits) {
    var bar = $(".ia-think-bar", bot), read = $("[data-read]", bot), step = 240;
    docs.forEach(function (d, k) {
      wait(k * step).then(function () { d.classList.add("is-scan"); });
    });
    return tween(docs.length * step + 650, function (k) {
      var v = fmt(total * (1 - Math.pow(1 - k, 2)));
      count.textContent = v;
      read.textContent = v;
      bar.style.setProperty("--p", k.toFixed(3));
    }).then(function () {
      docs.forEach(function (d) {
        var h = hits[d.getAttribute("data-doc")];
        d.classList.remove("is-scan");
        if (h) { d.classList.add("is-hit"); $(".ia-hit", d).textContent = h.join(" "); }
        else d.classList.add("is-miss");
      });
      return wait(520);
    });
  }

  /* ---------- Un scénario complet ---------- */
  function play(i) {
    run++;
    timers = []; tweens = [];
    cur = i; started = true; curCite = ""; quoteLive = false;
    setChip(i);
    var tpl = tpls[i];
    if (!tpl) return;
    var frag = tpl.content.cloneNode(true);
    var chat = frag.querySelector('[data-part="chat"]');
    var me = $(".is-me", chat), bot = $(".is-bot", chat), act = $(".ia-act", chat);
    var think = $(".ia-think", bot), ans = $(".ia-ans", bot), meta = $(".ia-meta", bot);
    var q = tpl.getAttribute("data-q"), hits = parseHits(tpl.getAttribute("data-hits"));

    $$(".ia-log > :not([data-keep])").forEach(function (el) { el.parentNode.removeChild(el); });
    log.scrollTop = 0;
    stack.innerHTML = ""; tabsEl.innerHTML = ""; sr.textContent = "";
    resetDocs();
    count.textContent = "0";
    ans.hidden = true; meta.hidden = true;
    typed.textContent = "";
    typed.classList.add("is-typing");

    var typing = reduce
      ? Promise.resolve(typed.textContent = q)
      : tween(Math.min(1700, q.length * 27), function (k) { typed.textContent = q.slice(0, Math.round(k * q.length)); });

    return typing.then(function () { return wait(320); }).then(function () {
      send.classList.add("is-press");
      return wait(200);
    }).then(function () {
      send.classList.remove("is-press");
      typed.classList.remove("is-typing");
      typed.textContent = "";
      log.appendChild(me); me.classList.add("ia-in");
      follow(true);
      return wait(420);
    }).then(function () {
      log.appendChild(bot); bot.classList.add("ia-in", "is-thinking");
      follow(true);
      return search(bot, hits);
    }).then(function () {
      think.hidden = true;
      bot.classList.remove("is-thinking");
      ans.hidden = false;
      /* La preuve suit la réponse : chaque citation écrite affiche son passage */
      var proofs = false;
      function proof() {
        if (proofs) return;
        proofs = true;
        moveKids(frag.querySelector('[data-part="pages"]'), stack);
        moveKids(frag.querySelector('[data-part="tabs"]'), tabsEl);
      }
      return stream(ans, function (n) { proof(); focusCite(n); }).then(function () {
        proof();
        quoteLive = true;
        if (curCite) focusCite(curCite, true);
        var none = $(".ia-page.is-none", stack);
        if (none) none.classList.add("is-on");
      });
    }).then(function () {
      meta.hidden = false; meta.classList.add("ia-in");
      follow(true);
      sr.textContent = "Réponse de JARVIS : " + ans.textContent.replace(/\s+/g, " ").trim();
      return wait(900);
    }).then(function () {
      log.appendChild(act); act.classList.add("ia-in");
      follow(true);
    });
  }

  /* ---------- Visibilité : démarrage et pause ---------- */
  var visible = false;
  function sync() {
    setRunning(visible && !document.hidden);
    root.classList.toggle("is-paused", !visible);
  }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        visible = e.isIntersecting;
        sync();
        if (visible && !started && e.intersectionRatio >= 0.25) {
          started = true;
          var rid = run;
          wait(450).then(function () { if (rid === run) play(0); });
        }
      });
    }, { threshold: [0, 0.25] }).observe(root);
  } else {
    visible = true;
    sync();
  }
  document.addEventListener("visibilitychange", sync);
})();
