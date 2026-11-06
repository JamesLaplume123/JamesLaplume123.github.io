/* Démo « Une vie entière, un seul système » : les domaines de la vie envoient leurs
   signaux autorisés au Hub privé; le coach d'habitudes propose, explique, attend
   l'accord, puis montre 14 jours et le rapport du matin.
   Démonstration seulement : données fictives, aucun appareil ni compte réel. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NB = " ";
  var STEPS = ["Signaux", "Suggestion", "14 jours", "Rapport du matin"];
  var PLAN = [5600, 7400, 8200, 9500];   /* durée de chaque étape en lecture automatique (ms) */
  var GATE = 5200;                        /* sans réponse, Alex approuve après ce délai (démo) */

  function q(s) { return "«" + NB + s + NB + "»"; }

  document.querySelectorAll('[data-demo="vie"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var vi = function (k) { return $('[data-vi="' + k + '"]'); };
    var vis = function (k) { return $$('[data-vi="' + k + '"]'); };
    var data;
    try { data = JSON.parse(vi("data").textContent); } catch (e) { return; }
    root.classList.add("is-live");

    var nodes = {};
    $$(".vi-node").forEach(function (n) { nodes[n.getAttribute("data-node")] = { el: n, v: n.querySelector("[data-vi-v]") }; });
    var spokes = {};
    $$(".vi-spokes g").forEach(function (g) { spokes[g.getAttribute("data-node")] = g; });
    var habitBtns = $$(".vi-habits button"), stepBtns = $$(".vi-steps button"), views = $$(".vi-view");
    var el = {
      clock: vi("clock"), old: vi("old"), nw: vi("new"), when: vi("when"), sugg: vi("sugg"), why: vi("why"),
      ask: vi("ask"), yes: vi("yes"), no: vi("no"), ok: vi("ok"), okWho: vi("ok-who"),
      declined: vi("declined"), again: vi("again"), chartL: vi("chart-l"), line: vi("line"), area: vi("area"),
      base: vi("base"), baseL: vi("base-l"), end: vi("end"), endL: vi("end-l"), axT: vi("ax-t"), axB: vi("ax-b"),
      dots: vi("dots"), streakL: vi("streak-l"), tip: vi("tip"), tipWhy: vi("tipwhy"), tipAdd: vi("tip-add"),
      erase: vi("erase"), erased: vi("erased"), restart: vi("restart"), live: vi("live")
    };

    var H = 0, step = 0, approved = false, declined = false, erased = false;
    var auto = !reduce, visible = false, started = false, elapsed = 0, raf = 0, prev = 0;

    function habit() { return data.habits[H]; }
    function say(t) { el.live.textContent = t; }
    function restartAnim(n, cls) { n.classList.remove(cls); void n.offsetWidth; n.classList.add(cls); }

    /* ---------- Remplir le panneau avec l'habitude choisie ---------- */
    function fill() {
      var h = habit(), c = h.chart;
      el.old.textContent = q(h.old);
      el.nw.textContent = q(h.new);
      restartAnim(el.old, "is-new"); restartAnim(el.nw, "is-new");
      $$(".vi-sig").forEach(function (li, i) {
        var s = h.signals[i];
        li.querySelector('[data-vi="sig-ic"]').innerHTML = s.ic;
        li.querySelector('[data-vi="sig-t"]').textContent = s.t;
        li.querySelector('[data-vi="sig-src"]').textContent = s.src;
        li.querySelector('[data-vi="sig-v"]').textContent = s.v;
        li.querySelector('[data-vi="sig-sp"]').setAttribute("d", s.sp);
      });
      el.when.textContent = h.when;
      el.sugg.textContent = h.sugg;
      el.why.textContent = h.why;
      $$('[data-vi="plan"] li').forEach(function (li, i) { li.textContent = h.plan[i]; });
      el.chartL.textContent = c.label;
      el.line.setAttribute("d", c.line);
      el.area.setAttribute("d", c.area);
      el.base.style.setProperty("--y", c.baseY + "%");
      el.baseL.textContent = c.baseL;
      el.end.style.setProperty("--x", c.endX + "%");
      el.end.style.setProperty("--y", c.endY + "%");
      el.endL.textContent = c.endL;
      el.axT.textContent = c.top;
      el.axB.textContent = c.bottom;
      el.streakL.textContent = h.streakL;
      el.dots.innerHTML = h.streak.split("").map(function (b, i) {
        return '<i class="' + (b === "1" ? "is-ok" : "") + '" style="--i:' + i + '"></i>';
      }).join("");
      $$(".vi-kpi").forEach(function (k, i) {
        var d = h.kpis[i];
        k.querySelector('[data-vi="kpi-l"]').textContent = d.l;
        k.querySelector('[data-vi="kpi-v"]').textContent = d.v;
        k.querySelector('[data-vi="kpi-u"]').textContent = d.u;
        k.querySelector('[data-vi="kpi-c"]').textContent = d.c;
      });
      $$(".vi-rep li").forEach(function (li, i) {
        var r = h.report[i];
        li.querySelector('[data-vi="rep-ic"]').innerHTML = r.ic;
        li.querySelector('[data-vi="rep-l"]').textContent = r.l;
        li.querySelector('[data-vi="rep-v"]').textContent = r.v;
      });
      el.tip.textContent = h.tip;
      el.tipWhy.textContent = h.tipwhy;
      el.tipAdd.textContent = "Ajouter à l’agenda";
      el.tipAdd.setAttribute("aria-pressed", "false");
      approved = false; declined = false;
      paintAsk();
    }

    function paintAsk() {
      el.ask.hidden = approved || declined;
      el.ok.hidden = !approved;
      el.declined.hidden = !declined;
      el.yes.classList.toggle("is-wait", step === 1 && auto && !approved && !declined);
      stepBtns.forEach(function (b, i) {
        if (i >= 2) b.setAttribute("aria-disabled", declined ? "true" : "false");
      });
    }

    /* ---------- L'orbite suit l'histoire ---------- */
    function setValue(k, v) {
      var n = nodes[k];
      if (!n || n.v.textContent === v) return;
      n.v.textContent = v;
      restartAnim(n.v, "is-new");
    }
    function paintOrbit() {
      var h = habit();
      root.setAttribute("data-step", String(step));
      root.toggleAttribute("data-focus", !erased);
      Object.keys(nodes).forEach(function (k) {
        var use = h.uses.indexOf(k) >= 0, act = h.acts.indexOf(k) >= 0;
        nodes[k].el.classList.toggle("is-use", use && !erased);
        if (spokes[k]) {
          spokes[k].classList.toggle("is-use", use && !erased);
          spokes[k].classList.toggle("is-act", act && step === 2 && approved);
        }
        var v = data.nodes[k];
        if (use) v = (step >= 2 && approved ? h.after[k] : h.sig[k]) || v;
        setValue(k, erased ? "—" : v);
      });
    }

    /* ---------- Compteurs ---------- */
    function countUp(span) {
      var txt = span.textContent, m = /^([+−-]?)([\d ]+)$/.exec(txt);
      if (!m || reduce) return;
      var sign = m[1], to = parseInt(m[2].replace(/ /g, ""), 10), t0 = performance.now();
      (function tick(t) {
        var k = Math.min(1, (t - t0) / 1300), e = 1 - Math.pow(1 - k, 3);
        span.textContent = sign + Math.round(to * e).toLocaleString("fr-CA").replace(/\s/g, NB);
        if (k < 1) requestAnimationFrame(tick); else span.textContent = txt;
      })(t0);
    }

    /* ---------- Étapes ---------- */
    function setStep(i) {
      step = i;
      views.forEach(function (v, j) {
        if (j === i) restartAnim(v, "is-on"); else v.classList.remove("is-on");
      });
      stepBtns.forEach(function (b, j) {
        if (j === i) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
        b.classList.toggle("is-done", j < i);
        b.classList.toggle("is-auto", j === i && auto);
        b.querySelector(".vi-bar").style.transform = "";
      });
      el.clock.textContent = i === 1 ? habit().when : data.clock[i];
      if (i === 2) setTimeout(function () { $$('[data-vi="kpi-v"]').forEach(countUp); }, reduce ? 0 : 900);
      elapsed = 0;
      paintAsk();
      paintOrbit();
      say("Étape " + (i + 1) + " sur 4 : " + STEPS[i]);
    }

    function approve(byDemo) {
      if (approved || declined) return;
      approved = true;
      el.okWho.textContent = byDemo ? "Approuvé par Alex" : "Approuvé par vous";
      if (step === 1) elapsed = Math.max(elapsed, GATE);
      paintAsk();
      paintOrbit();
      say(el.okWho.textContent + ". Révocable en un geste.");
    }

    /* ---------- Lecture automatique (avance seulement quand la démo est visible) ---------- */
    function tick(t) {
      raf = 0;
      if (!auto || !visible || erased) { prev = 0; return; }
      if (prev) elapsed += Math.min(100, t - prev);
      prev = t;
      if (step === 1 && !approved && !declined && elapsed >= GATE) approve(true);
      var p = Math.min(1, elapsed / PLAN[step]);
      stepBtns[step].querySelector(".vi-bar").style.transform = "scaleX(" + p.toFixed(4) + ")";
      if (p >= 1) {
        if (step < 3) setStep(step + 1);
        else { stop(); return; }
      }
      raf = requestAnimationFrame(tick);
    }
    function kick() { if (!raf && auto && visible && !erased) { prev = 0; raf = requestAnimationFrame(tick); } }
    function stop() {
      auto = false;
      stepBtns.forEach(function (b) { b.classList.remove("is-auto"); b.querySelector(".vi-bar").style.transform = ""; });
      el.yes.classList.remove("is-wait");
    }

    function chooseHabit(i) {
      H = i;
      habitBtns.forEach(function (b, j) { b.setAttribute("aria-pressed", j === i ? "true" : "false"); });
      fill();
      auto = !reduce;
      setStep(0);
      kick();
    }

    /* ---------- Interactions ---------- */
    habitBtns.forEach(function (b, i) { b.addEventListener("click", function () { if (!erased) chooseHabit(i); }); });
    stepBtns.forEach(function (b, i) {
      b.addEventListener("click", function () {
        if (erased || b.getAttribute("aria-disabled") === "true") return;
        stop();
        setStep(i);
      });
    });
    el.yes.addEventListener("click", function () { approve(false); kick(); });
    el.no.addEventListener("click", function () {
      declined = true;
      stop();
      paintAsk(); paintOrbit();
      say("Suggestion refusée. Rien n’a changé.");
    });
    el.again.addEventListener("click", function () { declined = false; paintAsk(); });
    el.tipAdd.addEventListener("click", function () {
      var on = el.tipAdd.getAttribute("aria-pressed") !== "true";
      el.tipAdd.setAttribute("aria-pressed", on ? "true" : "false");
      el.tipAdd.textContent = on ? "Ajouté à l’agenda ✓" : "Ajouter à l’agenda";
    });

    var confirmTimer = 0;
    el.erase.addEventListener("click", function () {
      var label = el.erase.querySelector("span");
      if (!el.erase.classList.contains("is-confirm")) {
        el.erase.classList.add("is-confirm");
        label.textContent = "Confirmer l’effacement";
        clearTimeout(confirmTimer);
        confirmTimer = setTimeout(function () { el.erase.classList.remove("is-confirm"); label.textContent = "Effacer les données"; }, 4000);
        return;
      }
      clearTimeout(confirmTimer);
      el.erase.classList.remove("is-confirm");
      label.textContent = "Effacer les données";
      stop();
      erased = true;
      root.classList.remove("is-erased"); void root.offsetWidth; root.classList.add("is-erased");
      el.erased.hidden = false;
      paintOrbit();
      el.clock.textContent = "Données effacées";
      el.restart.focus({ preventScroll: true });
      say("Données de la démo effacées.");
    });
    el.restart.addEventListener("click", function () {
      erased = false;
      root.classList.remove("is-erased");
      el.erased.hidden = true;
      chooseHabit(0);
    });

    /* ---------- Départ : seulement quand la démo est à l'écran ---------- */
    fill();
    setStep(0);
    function onVisible(v) {
      visible = v;
      root.classList.toggle("is-vis", v);
      if (v && !started) { started = true; elapsed = 0; setStep(0); }
      kick();
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { onVisible(e.isIntersecting); }); }, { threshold: .3 }).observe(root);
    } else onVisible(true);
  });
})();
