/* Démo « Automatisation d'entreprise » : une demande traverse cinq étapes
   (reçue → lue → règle → votre approbation → exécutée), avec particules entre
   les étapes, narration, journal horodaté et compteur avant / après. JARVIS
   s'arrête à l'étape 4 : rien ne part sans votre clic. Démarre à l'entrée dans
   la fenêtre, se met en pause hors écran. Sans JavaScript, l'état statique
   (demande d'achat approuvée) reste lisible. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="automatisation"]');
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
  var stage = $("[data-stage]"), lead = $("[data-lead]"), say = $("[data-say]");
  var stepEl = $("[data-step]"), sayText = $("[data-say-text]"), journal = $("[data-journal]");
  var statsEl = $("[data-stats]"), tabs = $$(".au-tab"), tpls = $$("template[data-au-sc]");
  var cur = 0, started = false, pending = null;
  var DECIDED_ICON = $(".au-role svg") ? $(".au-role svg").outerHTML : "";

  function pad(n) { return ("0" + n).slice(-2); }
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
  function flow(st) {
    st.classList.add("is-flow", "is-linked");
    return wait(820).then(function () { st.classList.remove("is-flow"); });
  }

  function auto(st, k, n) {
    activate(st, k, n);
    var kind = st.getAttribute("data-k");
    if (kind === "fields") {
      st.classList.add("is-scan");
      return wait(300).then(function () { return reveal(st, 400); })
        .then(function () { return wait(350); })
        .then(function () { finish(st, st.getAttribute("data-log")); });
    }
    if (kind === "rule") {
      return wait(200).then(function () { return reveal(st, 560); })
        .then(function () { return wait(650); })
        .then(function () { finish(st, st.getAttribute("data-log")); });
    }
    return wait(200).then(function () { return reveal(st, 300); })
      .then(function () { return wait(850); })
      .then(function () { finish(st, st.getAttribute("data-log")); });
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

  function result(st, k, n) {
    activate(st, k, n);
    var steps = $$(".au-track li", st), res = $(".au-res", st);
    return wait(200).then(function () { return reveal(st, 300); }).then(function () {
      steps[0].classList.add("on");
      return wait(750);
    }).then(function () {
      steps[1].classList.add("on");
      res.textContent = res.getAttribute("data-sent") + "…";
      log(res.getAttribute("data-sent"));
      return wait(1200);
    }).then(function () {
      steps[2].classList.add("on");
      st.classList.add("is-conf");
      res.textContent = res.getAttribute("data-conf") + ".";
      finish(st, res.getAttribute("data-conf"), "is-ok");
      narrate(0, n, "Une approbation de votre part. Tout le reste s’est fait seul, avec une trace complète.");
      statsEl.classList.add("is-win");
    });
  }

  /* ---------- Un scénario complet ---------- */
  function play(i) {
    run++;
    timers = []; tweens = [];
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

    var chain = wait(600);
    [0, 1, 2].forEach(function (k) {
      chain = chain.then(function () { return auto(sts[k], k, n); }).then(function () { return flow(sts[k]); });
    });
    return chain.then(function () { return ask(sts[3], 3, n); }).then(function (what) {
      var st = sts[3], btns = $(".au-btns", st), dec = $(".au-decided", st);
      var text = btns.getAttribute(what === "ok" ? "data-ok-log" : "data-no-log");
      if (pending && pending.line) pending.line.classList.remove("is-wait");
      pending = null;
      st.classList.add("is-decided");
      dec.className = "au-decided is-" + what;
      dec.innerHTML = DECIDED_ICON;
      dec.appendChild(document.createTextNode(text));
      $(".au-sum", st).textContent = text;
      finish(st, text, what === "ok" ? "is-ok" : "");
      if (what !== "ok") {
        var r = sts[4], res = $(".au-res", r);
        r.classList.add("is-skip");
        res.textContent = res.getAttribute("data-skip");
        $(".au-sum", r).textContent = "Aucune action";
        $$(".au-x", r).forEach(function (x) { x.classList.add("on"); });
        narrate(0, n, "Rien n’a été exécuté : vous avez dit non. Votre décision est inscrite au journal.");
        return;
      }
      return flow(st).then(function () { return result(sts[4], 4, n); });
    });
  }

  root.addEventListener("click", function (e) {
    var tab = e.target.closest(".au-tab");
    if (tab) { play(+tab.getAttribute("data-sc")); return; }
    if (e.target.closest("[data-replay]")) { play(cur); return; }
    var b = e.target.closest("[data-do]");
    if (b && pending && pending.st.contains(b)) {
      var p = pending;
      b.blur();
      p.res(b.getAttribute("data-do"));
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
