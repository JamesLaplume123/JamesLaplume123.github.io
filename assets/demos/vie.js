/* Démo « Personal Intelligence » : la journée d'Alex défile d'un réveil à l'autre.
   Chaque source a sa propre permission; retirée, son flux est coupé et JARVIS ne
   relie plus ce qui en dépend. Les liens arrivent avec leur raison; au réveil,
   un échange d'habitude attend l'accord, puis l'essai de 14 jours s'anime.
   Démonstration seulement : données fictives, aucun appareil ni compte réel. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NB = " ";
  var DAY_MS = 22000;   /* durée d'une journée en lecture automatique */
  var GATE = 5600;      /* sans réponse au réveil, Alex approuve après ce délai (démo) */
  var START = 6 * 60 + 30;
  var EASE = "cubic-bezier(.16, 1, .3, 1)";

  function fx() { return !reduce && document.documentElement.classList.contains("fx"); }
  function q(s) { return "«" + NB + s + NB + "»"; }
  function num(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, NB); }
  function dur(m) {
    m = Math.round(m);
    return m < 60 ? m + NB + "min" : Math.floor(m / 60) + NB + "h" + NB + ("0" + m % 60).slice(-2);
  }
  function hm(p) {
    var m = (Math.round(p) + START) % 1440;
    return Math.floor(m / 60) + NB + "h" + NB + ("0" + m % 60).slice(-2);
  }

  document.querySelectorAll('[data-demo="vie"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var pi = function (k) { return $('[data-pi="' + k + '"]'); };
    var data;
    try { data = JSON.parse(pi("data").textContent); } catch (e) { return; }
    root.classList.add("is-live");

    var DAY = data.day, INS = data.ins;
    var el = {
      clock: pi("clock"), time: pi("time"), date: pi("date"), tl: pi("tl"), sky: pi("sky"), count: pi("count"),
      play: pi("play"), replay: pi("replay"), links: pi("links"), feed: pi("feed"), empty: $(".pi-feed-empty"),
      swap: pi("swap"), old: pi("old"), nw: pi("new"), sugg: pi("sugg"), why: pi("why"), uses: pi("uses"), plan: pi("plan"),
      yes: pi("yes"), no: pi("no"), again: pi("again"), okWho: pi("ok-who"), need: pi("need"),
      week: pi("week"), delta: pi("delta"), metric: pi("metric"), goal: pi("goal"), axT: pi("ax-t"), axB: pi("ax-b"),
      base: pi("base"), baseL: pi("base-l"), bars: pi("bars"), avg: pi("avg"), avgL: pi("avg-l"), end: pi("end"), streak: pi("streak"),
      erase: pi("erase"), erased: pi("erased"), restart: pi("restart"), live: pi("live")
    };
    var sun = $(".pi-sun");
    var rows = {};
    $$(".pi-row[data-src]").forEach(function (r) {
      rows[r.getAttribute("data-src")] = { el: r, sw: r.querySelector(".pi-sw"), v: r.querySelector("[data-pi-v]"), last: "" };
    });
    var cards = {}, hls = {}, marks = {};
    $$(".pi-ins").forEach(function (c) { cards[c.getAttribute("data-ins")] = c; });
    $$(".pi-hl").forEach(function (h) { (hls[h.getAttribute("data-ins")] = hls[h.getAttribute("data-ins")] || []).push(h); });
    $$(".pi-mark").forEach(function (m) { marks[m.getAttribute("data-ins")] = m; });
    var habitBtns = $$(".pi-tabs button");

    var perm = { montre: true, tel: true, agenda: true, maison: true };
    var p = 0, shown = [], lastClock = "";
    var playing = false, auto = !reduce, visible = false, started = false, raf = 0, prev = 0, gateT = 0;
    var H = 0, approved = false, declined = false, byDemo = false, erased = false;

    function say(t) { el.live.textContent = t; }
    function restartCls(n, cls) { n.classList.remove(cls); void n.offsetWidth; n.classList.add(cls); }
    function habit() { return data.habits[H]; }

    /* ---------- Valeurs en direct de chaque source ---------- */
    function steps(t) {
      var s = 0;
      data.steps.forEach(function (v, i) { s += v * Math.max(0, Math.min(1, (t - i * 30) / 30)); });
      return s;
    }
    function screen(t) {
      var s = 0;
      data.screen.forEach(function (x) { s += Math.max(0, Math.min(t, x[1]) - x[0]); });
      return s;
    }
    function inRange(list, t) {
      for (var i = 0; i < list.length; i++) if (t >= list[i][0] && t < list[i][1]) return list[i];
      return null;
    }
    function temp(t) {
      var T = data.temp;
      for (var i = 1; i < T.length; i++) {
        if (t <= T[i][0]) {
          var k = (t - T[i - 1][0]) / (T[i][0] - T[i - 1][0]);
          return T[i - 1][1] + (T[i][1] - T[i - 1][1]) * k;
        }
      }
      return T[T.length - 1][1];
    }
    function value(k, t) {
      if (!perm[k]) return "Aucune donnée";
      if (k === "montre") {
        if (t >= data.asleep) return "Sommeil · " + dur(t - data.asleep);
        if (t >= data.inBed) return "Au lit · " + num(steps(t)) + NB + "pas";
        return num(steps(t)) + NB + "pas";
      }
      if (k === "tel") return dur(screen(t)) + " d’écran";
      if (k === "agenda") { var m = inRange(data.meet, t); return m ? m[2] : "Libre"; }
      var l = inRange(data.light, t);
      return temp(t).toFixed(1).replace(".", ",") + NB + "°C · " + (l ? l[2] : "Éteinte");
    }
    function paintValues() {
      Object.keys(rows).forEach(function (k) {
        var v = erased ? "—" : value(k, p), r = rows[k];
        if (v !== r.last) { r.last = v; r.v.textContent = v; }
      });
    }

    /* ---------- L'instant présent ---------- */
    function paintSun() {
      var rise = data.sun[0], set = data.sun[1], day = p > rise && p < set;
      var e = day ? Math.sin(Math.PI * (p - rise) / (set - rise)) : 0;
      sun.classList.toggle("is-night", !day);
      sun.style.setProperty("--sy", day ? (70 - e * 60).toFixed(2) : "22");
    }
    function setP(v, quiet) {
      p = Math.max(0, Math.min(DAY, v));
      el.tl.style.setProperty("--p", (p / DAY * 100).toFixed(3));
      paintSun();
      var c = hm(p), tomorrow = p + START >= 1440;
      if (c + tomorrow !== lastClock) {
        lastClock = c + tomorrow;
        el.time.textContent = c;
        el.date.textContent = tomorrow ? "Mardi 3" + NB + "novembre" : "Lundi 2" + NB + "novembre";
        el.clock.textContent = (tomorrow ? "Mardi · " : "Lundi · ") + c;
        el.sky.setAttribute("aria-valuenow", String(Math.round(p)));
        el.sky.setAttribute("aria-valuetext", (tomorrow ? "Mardi, " : "Lundi, ") + c);
        paintValues();
      }
      arrivals(quiet);
      paintSwap();
    }

    /* ---------- Les liens de JARVIS ---------- */
    function insOff(i) { return INS[i].src.some(function (k) { return !perm[k]; }); }
    function showCard(i, animate) {
      var c = cards[i], vis = [];
      if (animate && fx() && c.animate) {
        Object.keys(cards).forEach(function (k) { if (cards[k].classList.contains("is-in")) vis.push(cards[k]); });
      }
      var before = vis.map(function (x) { return x.getBoundingClientRect().top; });
      c.classList.add("is-in");
      if (!vis.length && !(animate && fx() && c.animate)) return;
      vis.forEach(function (x, j) {
        var d = before[j] - x.getBoundingClientRect().top;
        if (d) x.animate([{ transform: "translateY(" + d + "px)" }, { transform: "none" }], { duration: 650, easing: EASE });
      });
      if (c.animate && animate && fx()) {
        c.animate([{ opacity: 0, transform: "translateY(-12px) scale(.97)" }, { opacity: 1, transform: "none" }], { duration: 750, easing: EASE });
      }
    }
    function arrivals(quiet) {
      var n = 0;
      INS.forEach(function (ins, i) {
        var on = !erased && p >= ins.t, was = shown[i];
        if (on) n++;
        if (on === was) return;
        shown[i] = on;
        if (on) {
          showCard(i, !quiet);
          (hls[i] || []).forEach(function (h) {
            h.classList.add("is-on");
            if (!quiet) restartCls(h, "is-flash");
          });
          if (!quiet) say("Lien " + (i + 1) + " : " + cards[i].querySelector(".pi-ins-h b").textContent);
        } else {
          cards[i].classList.remove("is-in");
          (hls[i] || []).forEach(function (h) { h.classList.remove("is-on", "is-flash"); });
        }
        marks[i].classList.toggle("is-on", on);
      });
      el.empty.hidden = n > 0;
      el.links.textContent = n + (n > 1 ? " liens" : " lien");
      INS.forEach(function (ins, i) { cards[i].classList.toggle("is-old", shown[i] && i < n - 2); });
    }
    function paintLinks() {
      var key = habit().links;
      INS.forEach(function (ins, i) {
        var off = insOff(i), isKey = key.indexOf(i) >= 0;
        cards[i].classList.toggle("is-off", off);
        cards[i].classList.toggle("is-key", isKey && !off);
        (hls[i] || []).forEach(function (h) { h.classList.toggle("is-dim", off); h.classList.toggle("is-key", isKey); });
      });
    }

    /* Survoler un lien éclaire ses preuves dans la journée */
    Object.keys(cards).forEach(function (k) {
      var on = function (v) { return function () { (hls[k] || []).forEach(function (h) { h.classList.toggle("is-hot", v); }); }; };
      cards[k].addEventListener("mouseenter", on(true));
      cards[k].addEventListener("mouseleave", on(false));
      cards[k].addEventListener("focusin", on(true));
      cards[k].addEventListener("focusout", on(false));
    });

    /* ---------- Permissions ---------- */
    function setPerm(k, on) {
      perm[k] = on;
      var r = rows[k];
      r.sw.setAttribute("aria-checked", on ? "true" : "false");
      r.el.classList.toggle("is-off", !on);
      $$('.pi-chips [data-src="' + k + '"]').forEach(function (s) { s.classList.toggle("is-off", !on); });
      var n = Object.keys(perm).filter(function (x) { return perm[x]; }).length;
      el.count.textContent = n + " sur 4";
      r.last = "";
      paintValues(); paintLinks(); paintSwap(); paintWeek();
      say(on ? "Permission rétablie : " + data.names[k] + ". Les données reprennent."
        : "Permission retirée : " + data.names[k] + ". Plus rien n’est reçu de cette source.");
    }

    /* ---------- La proposition du matin ---------- */
    function missing() { return habit().uses.filter(function (k) { return !perm[k]; }); }
    function swapState() {
      if (p < DAY) return "wait";
      if (approved) return "ok";
      if (declined) return "no";
      return missing().length ? "blocked" : "ready";
    }
    function paintSwap() {
      var s = swapState();
      if (el.swap.getAttribute("data-state") !== s) {
        el.swap.setAttribute("data-state", s);
        if (s === "ready") say("Proposition du matin : " + habit().old + " remplacé par " + habit().new + ". En attente de votre accord.");
      }
      el.need.textContent = missing().map(function (k) { return data.names[k]; }).join(" · ");
      el.yes.classList.toggle("is-wait", s === "ready" && auto);
      if (s !== "ready") gateT = 0;
    }
    function fillHabit() {
      var h = habit();
      el.old.textContent = q(h.old);
      el.nw.textContent = q(h.new);
      el.sugg.textContent = h.sugg;
      el.why.textContent = h.why;
      el.uses.innerHTML = h.uses.map(function (k) {
        return '<span data-src="' + k + '"' + (perm[k] ? "" : ' class="is-off"') + ">" + data.names[k] + "</span>";
      }).join("");
      $$('[data-pi="plan"] li').forEach(function (li, i) { li.textContent = h.plan[i]; });
      el.metric.textContent = h.metric;
      el.goal.textContent = h.goal;
      el.axT.textContent = h.top;
      el.axB.textContent = h.bottom;
      el.base.style.setProperty("--y", h.base);
      el.bars.style.setProperty("--b", h.base);
      el.baseL.textContent = h.baseL;
      $$('[data-pi="bars"] i').forEach(function (b, i) { b.style.setProperty("--v", h.vals[i]); });
      el.avg.style.setProperty("--y", h.avg);
      el.avgL.textContent = h.avgL;
      el.end.textContent = h.end;
      el.end.style.setProperty("--e", (h.vals[h.vals.length - 1] * 100).toFixed(2));
      el.delta.textContent = h.delta;
      $$('[data-pi="streak"] i').forEach(function (d, i) { d.classList.toggle("is-ok", h.streak[i] === "1"); });
      $$(".pi-kpi").forEach(function (k, i) {
        var d = h.kpis[i];
        k.querySelector('[data-pi="kpi-l"]').textContent = d.l;
        k.querySelector('[data-pi="kpi-u"]').textContent = d.u;
        k.querySelector('[data-pi="kpi-c"]').textContent = d.c;
      });
      paintLinks();
    }

    /* ---------- La progression ---------- */
    function countUp(span, txt) {
      var m = /^([+−-]?)([\d  ]+)$/.exec(txt);
      if (!m || !fx()) { span.textContent = txt; return; }
      var sign = m[1], to = parseInt(m[2].replace(/\D/g, ""), 10), t0 = performance.now();
      (function step(t) {
        var k = Math.min(1, (t - t0) / 1300), e = 1 - Math.pow(1 - k, 3);
        span.textContent = sign + num(to * e);
        if (k < 1) requestAnimationFrame(step); else span.textContent = txt;
      })(t0);
    }
    function paintWeek(anim) {
      var on = approved && !erased;
      el.week.setAttribute("data-state", on ? "on" : "ghost");
      el.week.classList.toggle("is-paused", on && missing().length > 0);
      $$(".pi-kpi").forEach(function (k, i) {
        var span = k.querySelector('[data-pi="kpi-v"]');
        if (!on) { span.textContent = "—"; return; }
        if (anim) countUp(span, habit().kpis[i].v); else span.textContent = habit().kpis[i].v;
      });
      if (anim && on) restartCls(el.week, "is-anim");
      if (!on) el.week.classList.remove("is-anim");
    }
    function approve(demo) {
      if (swapState() !== "ready") return;
      approved = true; byDemo = demo;
      el.okWho.textContent = demo ? "Approuvé par Alex" : "Approuvé par vous";
      paintSwap();
      paintWeek(true);
      say(el.okWho.textContent + ". L’essai de 14 jours commence; révocable en un geste.");
    }

    function chooseHabit(i) {
      H = i;
      habitBtns.forEach(function (b, j) { b.setAttribute("aria-pressed", j === i ? "true" : "false"); });
      approved = false; declined = false; gateT = 0;
      fillHabit();
      restartCls(el.swap, "is-new");
      paintSwap();
      paintWeek(false);
      kick();
    }

    /* ---------- Lecture : avance seulement quand la démo est visible ---------- */
    function paintPlay() {
      root.toggleAttribute("data-paused", !playing);
      el.play.setAttribute("aria-label", playing ? "Mettre en pause" : "Lire la journée");
    }
    function tick(t) {
      raf = 0;
      if (!visible || erased) { prev = 0; return; }
      var dt = prev ? Math.min(100, t - prev) : 0;
      prev = t;
      if (playing) {
        setP(p + dt * DAY / DAY_MS);
        if (p >= DAY) { playing = false; paintPlay(); }
      } else if (auto && swapState() === "ready") {
        gateT += dt;
        if (gateT >= GATE) approve(true);
      }
      if (playing || (auto && swapState() === "ready")) raf = requestAnimationFrame(tick);
      else prev = 0;
    }
    function kick() { if (!raf && visible && !erased && (playing || (auto && swapState() === "ready"))) { prev = 0; raf = requestAnimationFrame(tick); } }

    function resetDay() {
      approved = false; declined = false; gateT = 0;
      shown = [];
      Object.keys(cards).forEach(function (k) { cards[k].classList.remove("is-in"); });
      Object.keys(hls).forEach(function (k) { hls[k].forEach(function (h) { h.classList.remove("is-on", "is-flash"); }); });
      setP(0, true);
      paintWeek(false);
    }
    function playFromStart() {
      auto = !reduce;
      resetDay();
      playing = !reduce;
      if (reduce) setP(DAY, true);
      paintPlay();
      kick();
    }

    /* ---------- Interactions ---------- */
    Object.keys(rows).forEach(function (k) {
      rows[k].sw.addEventListener("click", function () { if (!erased) setPerm(k, !perm[k]); });
    });
    el.play.addEventListener("click", function () {
      if (erased) return;
      if (!playing && p >= DAY) { playFromStart(); return; }
      playing = !playing;
      if (!playing) auto = false;
      paintPlay();
      kick();
    });
    el.replay.addEventListener("click", function () { if (!erased) playFromStart(); });
    habitBtns.forEach(function (b, i) { b.addEventListener("click", function () { if (!erased) chooseHabit(i); }); });
    el.yes.addEventListener("click", function () { approve(false); });
    el.no.addEventListener("click", function () {
      declined = true; auto = false;
      paintSwap();
      say("Proposition refusée. Rien n’a changé.");
    });
    el.again.addEventListener("click", function () { declined = false; paintSwap(); });

    /* Glisser la journée : le ciel et chaque voie servent de curseur */
    var drag = null;
    function scrubAt(target, x) {
      var r = target.getBoundingClientRect();
      setP((x - r.left) / r.width * DAY, true);
    }
    function grab(e) {
      if (erased || e.button > 0) return;
      var target = e.currentTarget;
      drag = target;
      playing = false; auto = false; paintPlay();
      scrubAt(target, e.clientX);
      if (target.setPointerCapture) target.setPointerCapture(e.pointerId);
    }
    [el.sky].concat($$(".pi-lane")).forEach(function (t) {
      t.addEventListener("pointerdown", grab);
      t.addEventListener("pointermove", function (e) { if (drag === t) scrubAt(t, e.clientX); });
      t.addEventListener("pointerup", function () { drag = null; });
      t.addEventListener("pointercancel", function () { drag = null; });
    });
    el.sky.addEventListener("keydown", function (e) {
      var steps = { ArrowRight: 30, ArrowUp: 30, ArrowLeft: -30, ArrowDown: -30, PageUp: 180, PageDown: -180 };
      var v = null;
      if (e.key in steps) v = p + steps[e.key];
      else if (e.key === "Home") v = 0;
      else if (e.key === "End") v = DAY;
      if (v === null || erased) return;
      e.preventDefault();
      playing = false; auto = false; paintPlay();
      setP(v, true);
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
      playing = false; auto = false; paintPlay();
      erased = true;
      el.erased.hidden = false;
      paintValues(); paintWeek(false);
      el.clock.textContent = "Données effacées";
      el.restart.focus({ preventScroll: true });
      say("Données de la démo effacées.");
    });
    el.restart.addEventListener("click", function () {
      erased = false;
      el.erased.hidden = true;
      Object.keys(perm).forEach(function (k) { if (!perm[k]) setPerm(k, true); });
      lastClock = "";
      chooseHabit(0);
      playFromStart();
    });

    /* ---------- Départ : seulement quand la démo est à l'écran ---------- */
    fillHabit();
    resetDay();
    if (reduce) setP(DAY, true);
    paintPlay();
    function onVisible(v) {
      visible = v;
      root.classList.toggle("is-vis", v);
      if (v && !started) { started = true; playFromStart(); }
      kick();
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { onVisible(e.isIntersecting); }); }, { threshold: .12 }).observe(root);
    } else onVisible(true);
  });
})();
