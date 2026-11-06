/* Démo « Automatisation d'entreprise » : une demande traverse cinq étapes
   (reçue → lue → règle → votre approbation → exécutée), avec narration,
   journal horodaté et compteur avant / après. JARVIS s'arrête à l'étape 4 :
   rien ne part sans votre clic. Sous html.fx, le travail se voit : le message
   arrive, un paquet voyage sur chaque liaison, JARVIS surligne ce qu'il lit et
   les valeurs volent jusqu'aux champs, la règle compte, le bouton s'enfonce, le
   document s'imprime et se signe. Démarre à l'entrée dans la fenêtre, se met
   en pause hors écran. Sans JavaScript, l'état statique (demande d'achat
   approuvée) reste lisible. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="automatisation"]');
  if (!root || !window.requestAnimationFrame || !window.Promise) return;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var S = reduce ? 0.12 : 1;
  var fx = false; // effets fins : décidé au lancement de chaque scénario (html.fx)

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
  var stage = $("[data-stage]"), lead = $("[data-lead]"), say = $("[data-say]");
  var stepEl = $("[data-step]"), sayText = $("[data-say-text]"), journal = $("[data-journal]");
  var statsEl = $("[data-stats]"), tabs = $$(".au-tab"), tpls = $$("template[data-au-sc]");
  var cur = 0, started = false, pending = null;
  var DECIDED_ICON = $(".au-role svg") ? $(".au-role svg").outerHTML : "";

  function pad(n) { return ("0" + n).slice(-2); }
  function ease(k) { return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }
  function out(k) { return 1 - Math.pow(1 - k, 3); }

  /* ---------- Valeurs : montants comptés, textes tapés ---------- */
  var NB = "\u00a0";
  function money(t) {
    var m = /^([\d\u00a0 ]+)(?:,(\d+))?\u00a0\$$/.exec(t);
    return m ? { v: +(m[1].replace(/\D/g, "") + "." + (m[2] || "0")), d: m[2] ? m[2].length : 0 } : null;
  }
  function fmt(v, d) {
    var p = v.toFixed(d).split(".");
    return p[0].replace(/\B(?=(\d{3})+(?!\d))/g, NB) + (d ? "," + p[1] : "") + NB + "$";
  }
  /* Écrit la valeur dans el : compte si c'est un montant, sinon tape les lettres */
  function write(el, text, ms, onStep) {
    if (!fx) { el.textContent = text; return Promise.resolve(); }
    var m = money(text);
    el.classList.add("is-typing");
    return tween(ms || (m ? 900 : Math.min(700, 120 + text.length * 32)), function (k) {
      if (m) {
        var v = m.v * out(k);
        el.textContent = fmt(v, m.d);
        if (onStep) onStep(v);
      } else el.textContent = text.slice(0, Math.round(text.length * k));
    }).then(function () { el.textContent = text; el.classList.remove("is-typing"); });
  }
  /* Une copie de la valeur vole du passage lu jusqu'au champ (coordonnées de la scène) */
  function fly(from, to, text) {
    var a = from && from.getBoundingClientRect(), b = to.getBoundingClientRect(), o = stage.getBoundingClientRect();
    if (!fx || !a || !a.width || !b.width) return Promise.resolve();
    var g = document.createElement("span");
    g.className = "au-ghost";
    g.setAttribute("aria-hidden", "true");
    g.textContent = text;
    stage.appendChild(g);
    var x0 = a.left - o.left, y0 = a.top - o.top + (a.height - g.offsetHeight) / 2;
    var x1 = b.left - o.left - 8, y1 = b.top - o.top + (b.height - g.offsetHeight) / 2;
    return tween(620, function (k) {
      var e = ease(k), arc = Math.sin(Math.PI * e) * -26;
      g.style.transform = "translate(" + (x0 + (x1 - x0) * e).toFixed(1) + "px," + (y0 + (y1 - y0) * e + arc).toFixed(1) + "px) scale(" + (0.92 + 0.08 * e).toFixed(3) + ")";
      g.style.opacity = k < .15 ? k / .15 : k > .85 ? (1 - k) / .15 : 1;
    }).then(function () { g.remove(); });
  }
  function stamp() { var d = new Date(); return d.getHours() + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds()); }

  function log(text, cls) {
    var li = document.createElement("li"), t = document.createElement("time"), s = document.createElement("span");
    li.className = "is-new" + (cls ? " " + cls : "");
    t.textContent = stamp();
    s.textContent = text;
    li.appendChild(t); li.appendChild(s);
    journal.appendChild(li);
    while (journal.children.length > 9) journal.removeChild(journal.firstChild);
    return li;
  }

  function narrate(step, total, text) {
    stepEl.textContent = step ? "Étape " + step + " sur " + total : (total ? "Terminé" : "Scénario");
    sayText.textContent = text;
    say.classList.remove("is-new");
    void say.offsetWidth;
    say.classList.add("is-new");
  }

  function setTab(i) {
    tabs.forEach(function (t, k) {
      t.classList.toggle("is-on", k === i);
      t.setAttribute("aria-pressed", k === i ? "true" : "false");
    });
  }

  function countUp() {
    var nums = $$("[data-count]", statsEl);
    statsEl.classList.remove("is-struck", "is-win");
    statsEl.classList.add("is-count");
    nums.forEach(function (b) { b.textContent = "0"; });
    return tween(1400, function (k) {
      var e = 1 - Math.pow(1 - k, 3);
      nums.forEach(function (b) { b.textContent = Math.round(+b.getAttribute("data-count") * e); });
    }).then(function () { return wait(250); }).then(function () { statsEl.classList.add("is-struck"); });
  }

  /* ---------- Étapes ---------- */
  function reveal(st, gap) {
    var xs = $$(".au-x", st), i = 0;
    function next() {
      if (i >= xs.length) return Promise.resolve();
      xs[i++].classList.add("on");
      return wait(gap).then(next);
    }
    return next();
  }
  function activate(st, k, n) {
    st.classList.add("is-on");
    narrate(k + 1, n, st.getAttribute("data-say"));
  }
  function finish(st, text, cls) {
    st.classList.remove("is-on", "is-scan");
    st.classList.add("is-done");
    $$(".au-x", st).forEach(function (x) { x.classList.add("on"); });
    if (text) log(text, cls);
  }
  /* Un paquet lumineux (l'icône de l'étape) suit la liaison, qui se remplit derrière lui.
     L'étape reste ouverte pendant le trajet : elle passe le relais, puis se termine. */
  function pass(st, text, cls) {
    return flow(st).then(function () { finish(st, text === undefined ? st.getAttribute("data-log") : text, cls); });
  }
  function flow(st) {
    var link = $(".au-link", st), next = st.nextElementSibling;
    if (!fx || !link) { st.classList.add("is-linked"); return wait(300); }
    var fill = $("i", link), horiz = link.clientWidth >= link.clientHeight;
    var len = horiz ? link.clientWidth : link.clientHeight;
    var pk = document.createElement("span");
    pk.className = "au-packet";
    pk.innerHTML = $(".au-node svg", st).outerHTML;
    link.appendChild(pk);
    fill.style.transition = "none";
    return tween(Math.max(520, Math.min(950, 360 + len * 3)), function (k) {
      var e = ease(k);
      pk.style.transform = horiz ? "translateX(" + (e * len).toFixed(1) + "px)" : "translateY(" + (e * len).toFixed(1) + "px)";
      pk.style.opacity = k < .12 ? k / .12 : k > .9 ? (1 - k) / .1 : 1;
      fill.style.transform = (horiz ? "scaleX(" : "scaleY(") + e.toFixed(3) + ")";
    }).then(function () {
      st.classList.add("is-linked");
      fill.style.transform = ""; fill.style.transition = "";
      pk.remove();
      if (next) { next.classList.add("is-recv"); wait(700).then(function () { next.classList.remove("is-recv"); }); }
    });
  }

  /* Étape 1 : le message arrive (pastille « 1 », non lu) */
  function arrive(st, k, n) {
    activate(st, k, n);
    var msg = $(".au-mail, .au-form", st);
    if (fx) {
      var badge = document.createElement("b");
      badge.className = "au-badge";
      badge.setAttribute("aria-hidden", "true");
      badge.textContent = "1";
      $(".au-node", st).appendChild(badge);
      st.classList.add("is-arrive");
      msg.classList.add("is-unread");
    }
    return wait(250).then(function () { return reveal(st, 300); })
      .then(function () { return wait(fx ? 1100 : 850); })
      .then(function () {
        var badge = $(".au-badge", st);
        if (badge) { badge.classList.add("is-gone"); wait(450).then(function () { badge.remove(); }); }
        st.classList.remove("is-arrive");
      });
  }

  /* Étape 2 : JARVIS lit le message (balayage, surlignage), les valeurs volent jusqu'aux champs */
  function extract(st, k, n, src) {
    activate(st, k, n);
    var rows = $$(".au-f", st), note = $(".au-note", st);
    var srcCard = $(".au-card", src), seen = fx && srcCard.getBoundingClientRect().height > 0;
    var msg = $(".au-mail, .au-form", src);
    if (msg) msg.classList.remove("is-unread");
    if (fx) {
      rows.forEach(function (li) { var t = $(".au-t", li); t.setAttribute("data-v", t.textContent); t.textContent = ""; });
      src.classList.add(seen ? "is-reading" : "is-none");
      if (!seen) st.classList.add("is-scan");
    }
    var chain = wait(fx ? 450 : 200);
    rows.forEach(function (li, i) {
      chain = chain.then(function () {
        var t = $(".au-t", li), text = t.getAttribute("data-v") || t.textContent;
        var mark = li.hasAttribute("data-src") ? $('.au-m[data-m="' + li.getAttribute("data-src") + '"]', src) : null;
        if (mark && fx) mark.classList.add("is-hl");
        li.classList.add("on");
        if (!fx) return wait(400);
        /* La valeur voyage pendant que le passage suivant se surligne */
        var done = wait(seen ? 260 : 0).then(function () { return fly(seen && mark, t.parentNode, text); })
          .then(function () { return write(t, text); })
          .then(function () { li.classList.add("is-set"); });
        return i < rows.length - 1 && seen ? wait(700) : done;
      });
    });
    return chain.then(function () {
      src.classList.remove("is-reading", "is-none");
      note.classList.add("on");
      return wait(fx ? 600 : 350);
    });
  }

  /* Étape 3 : la règle s'évalue sous vos yeux (le montant défile et dépasse le seuil) */
  function rule(st, k, n) {
    activate(st, k, n);
    var ev = $(".au-eval", st), sp = $$("span", ev), op = $("i", ev);
    var L = money(sp[0].textContent), R = money(sp[1].textContent);
    return wait(200).then(function () {
      $(".au-rule", st).classList.add("on");
      return wait(fx ? 520 : 560);
    }).then(function () {
      ev.classList.add("on");
      if (!fx) return wait(560);
      var tl = sp[0].textContent, tr = sp[1].textContent;
      sp.forEach(function (s) { s.style.minWidth = s.offsetWidth + "px"; });
      ev.classList.add("is-eval");
      if (L && R) {
        return write(sp[0], tl, 1300, function (v) {
          if (v > R.v && !op.classList.contains("is-lit")) { op.classList.add("is-lit"); sp[1].classList.add("is-past"); }
        });
      }
      sp[1].textContent = "";
      sp[1].classList.add("is-search");
      return wait(R ? 200 : 750).then(function () {
        sp[1].classList.remove("is-search");
        return write(sp[1], tr, R ? 900 : 260);
      }).then(function () { op.classList.add("is-lit"); sp[1].classList.add("is-past"); });
    }).then(function () { return wait(fx ? 380 : 0); }).then(function () {
      $(".au-verdict", st).classList.add("on");
      return wait(fx ? 900 : 650);
    });
  }

  /* L'approbation : le bouton répond dès qu'il apparaît, puis JARVIS attend */
  function ask(st, k, n) {
    activate(st, k, n);
    var timer = $("[data-timer]", st), t0 = Date.now();
    var answer = new Promise(function (res) { pending = { st: st, res: res, line: null }; });
    reveal(st, 200).then(function () {
      if (!pending || pending.st !== st) return;
      pending.line = log(st.getAttribute("data-log"), "is-wait");
      (function tick() {
        wait(1000).then(function () {
          if (!pending || pending.st !== st) return;
          var sec = Math.round((Date.now() - t0) / 1000);
          timer.textContent = Math.floor(sec / 60) + ":" + pad(sec % 60);
          tick();
        });
      })();
    });
    return answer;
  }

  /* Étape 5 : le document s'imprime, se signe, part, puis reçoit le tampon « Confirmé » */
  function result(st, k, n) {
    activate(st, k, n);
    var steps = $$(".au-track li", st), track = $(".au-track", st), res = $(".au-res", st), doc = $(".au-doc", st);
    return wait(200).then(function () {
      if (fx) st.classList.add("is-printing");
      doc.classList.add("on");
      return wait(fx ? 1150 : 300);
    }).then(function () {
      st.classList.remove("is-printing");
      if (!fx || !$(".au-sign", doc)) return;
      doc.classList.add("is-signed");
      return wait(1000);
    }).then(function () {
      track.classList.add("on");
      return wait(300);
    }).then(function () {
      steps[0].classList.add("on");
      return wait(750);
    }).then(function () {
      steps[1].classList.add("on");
      track.style.setProperty("--tk", ".5");
      res.textContent = res.getAttribute("data-sent") + "…";
      log(res.getAttribute("data-sent"));
      return wait(1200);
    }).then(function () {
      steps[2].classList.add("on");
      track.style.setProperty("--tk", "1");
      st.classList.add("is-conf");
      res.textContent = res.getAttribute("data-conf") + ".";
      finish(st, res.getAttribute("data-conf"), "is-ok");
      narrate(0, n, "Une approbation de votre part. Tout le reste s’est fait seul, avec une trace complète.");
      statsEl.classList.add("is-win");
    });
  }

  /* Le bouton s'enfonce, une onde part du doigt, la coche se trace, puis la décision s'affiche */
  function press(b, e) {
    if (!fx) return;
    var r = b.getBoundingClientRect(), rip = document.createElement("span"), dot = document.createElement("i");
    var x = e.clientX || e.clientY ? e.clientX - r.left : r.width / 2, y = e.clientX || e.clientY ? e.clientY - r.top : r.height / 2;
    rip.className = "au-rip";
    dot.style.left = x + "px"; dot.style.top = y + "px";
    rip.appendChild(dot);
    b.appendChild(rip);
    b.insertAdjacentHTML("afterbegin", '<svg class="au-tick" viewBox="0 0 24 24" aria-hidden="true"><path pathLength="1" d="m5 12.5 4.5 4.5L19 7.5"/></svg>');
    b.classList.add("is-press");
    b.parentNode.classList.add("is-chosen");
  }

  /* ---------- Un scénario complet ---------- */
  function play(i) {
    run++;
    timers = []; tweens = [];
    fx = !reduce && document.documentElement.classList.contains("fx");
    cur = i; started = true; pending = null;
    setTab(i);
    var tpl = tpls[i];
    if (!tpl) return;
    var frag = tpl.content.cloneNode(true);
    lead.textContent = frag.querySelector('[data-part="lead"]').textContent;
    stage.innerHTML = "";
    stage.appendChild(frag.querySelector('[data-part="pipe"] .au-pipe'));
    var statsPart = frag.querySelector('[data-part="stats"]');
    statsEl.innerHTML = "";
    while (statsPart.firstChild) statsEl.appendChild(statsPart.firstChild);
    journal.innerHTML = "";
    log("Démonstration lancée · données simulées");
    var sts = $$(".au-st", stage), n = sts.length;
    narrate(0, 0, "La demande arrive. Regardez-la circuler.");
    countUp();

    return wait(600).then(function () { return arrive(sts[0], 0, n); })
      .then(function () { return pass(sts[0]); })
      .then(function () { return extract(sts[1], 1, n, sts[0]); })
      .then(function () { return pass(sts[1]); })
      .then(function () { return rule(sts[2], 2, n); })
      .then(function () { return pass(sts[2]); })
      .then(function () { return ask(sts[3], 3, n); }).then(function (what) {
      var st = sts[3], btns = $(".au-btns", st), dec = $(".au-decided", st);
      var text = btns.getAttribute(what === "ok" ? "data-ok-log" : "data-no-log");
      if (pending && pending.line) pending.line.classList.remove("is-wait");
      pending = null;
      st.classList.add("is-decided");
      dec.className = "au-decided is-" + what;
      dec.innerHTML = DECIDED_ICON;
      dec.appendChild(document.createTextNode(text));
      $(".au-sum", st).textContent = text;
      if (what !== "ok") {
        finish(st, text);
        var r = sts[4], res = $(".au-res", r);
        r.classList.add("is-skip");
        res.textContent = res.getAttribute("data-skip");
        $(".au-sum", r).textContent = "Aucune action";
        $$(".au-x", r).forEach(function (x) { x.classList.add("on"); });
        narrate(0, n, "Rien n’a été exécuté : vous avez dit non. Votre décision est inscrite au journal.");
        return;
      }
      log(text, "is-ok");
      return pass(st, "").then(function () { return result(sts[4], 4, n); });
    });
  }

  root.addEventListener("click", function (e) {
    var tab = e.target.closest(".au-tab");
    if (tab) { play(+tab.getAttribute("data-sc")); return; }
    if (e.target.closest("[data-replay]")) { play(cur); return; }
    var b = e.target.closest("[data-do]");
    if (b && pending && pending.st.contains(b) && !pending.lock) {
      var p = pending;
      p.lock = true;
      b.blur();
      press(b, e);
      wait(fx ? 720 : 0).then(function () { p.res(b.getAttribute("data-do")); });
    }
  });

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
        if (visible && !started && e.intersectionRatio >= 0.2) {
          started = true;
          var rid = run;
          wait(400).then(function () { if (rid === run) play(0); });
        }
      });
    }, { threshold: [0, 0.2] }).observe(root);
  } else {
    visible = true;
    sync();
  }
  document.addEventListener("visibilitychange", sync);
})();
