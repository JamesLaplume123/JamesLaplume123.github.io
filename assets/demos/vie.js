/* Démo « Personal Intelligence » : treize sources alimentent le modèle d'Alex
   sur le Hub JARVIS; chaque permission se retire séparément. Les habitudes
   détectées mènent à deux avenirs projetés (estimations étiquetées), à une
   automatisation à approuver ou refuser (conséquence honnête dans les deux cas)
   et au coach de vie (conseils, principes de livres, citations du domaine
   public, engagements choisis). Données d'exemple, aucun appareil réel. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NB = "\u00a0";
  var PRIMARY = { ecran: "sommeil", cafe: "sommeil", achats: "argent", course: "objectif", repas: "energie" };
  var MLABEL = { sommeil: "Sommeil par nuit", energie: "Énergie, sur 100", argent: "Épargne cumulée", objectif: "Progression de l’objectif" };

  function fx() { return !reduce && document.documentElement.classList.contains("fx"); }
  function grp(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, NB); }

  function fmt(m, v) {
    if (m === "sommeil") { var mi = Math.round(v * 60); return Math.floor(mi / 60) + NB + "h" + NB + ("0" + mi % 60).slice(-2); }
    if (m === "argent") return grp(Math.round(v / 10) * 10) + NB + "$";
    if (m === "objectif") return Math.round(v) + NB + "%";
    return String(Math.round(v));
  }
  function delta(m, d) {
    var s = d >= 0 ? "+" : "−", a = Math.abs(d);
    if (m === "sommeil") return s + Math.round(a * 60) + NB + "min par nuit";
    if (m === "argent") return s + grp(Math.round(a / 10) * 10) + NB + "$";
    return s + Math.round(a) + NB + "points";
  }

  document.querySelectorAll('[data-demo="vie"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var pi = function (k) { return $('[data-pi="' + k + '"]'); };
    var data;
    try { data = JSON.parse(pi("data").textContent); } catch (e) { return; }
    root.classList.add("is-live");
    var WILL = data.will;

    /* ---------- Projections (même formule que vie.py : project) ---------- */
    function lvl(s, end, tau, t) { return s + (end - s) * (1 - Math.exp(-t / tau)); }
    function project(sp, k, t) {
      if (sp.rc !== undefined) {
        var r = k === "c" ? sp.rc : k === "n" ? sp.rn : sp.rc + WILL * (sp.rn - sp.rc);
        return sp.s + r * t;
      }
      if (k === "c") return lvl(sp.s, sp.c, sp.tc, t);
      if (k === "n") return lvl(sp.s, sp.n, sp.tn, t);
      return lvl(sp.s, sp.c + WILL * (sp.n - sp.c), sp.tn * 1.6, t);
    }
    function cap(m, v) { return m === "objectif" || m === "energie" ? Math.min(v, 100) : v; }
    function val(h, m, k, t) { return cap(m, project(h.m[m], k, t)); }
    function metricGoal(m) { for (var i = 0; i < data.metrics.length; i++) if (data.metrics[i].k === m) return data.metrics[i]; return {}; }
    function nice(lo, hi, m) {
      var raw = (hi - lo) / 3, mag = Math.pow(10, Math.floor(Math.log10(raw > 0 ? raw : 1))), step = mag;
      [1, 2, 2.5, 5, 10].some(function (s) { step = s * mag; return step >= raw; });
      if (m === "sommeil") step = Math.max(.25, Math.round(step * 4) / 4);
      return [Math.floor(lo / step) * step, Math.ceil(hi / step) * step, step];
    }

    /* ---------- État ---------- */
    var perm = {}, sig = {};
    data.sources.forEach(function (s) { perm[s.k] = true; sig[s.k] = s; });
    var H = 0, M = "sommeil", HOR = 90, dec = {}, tone = "doux", visible = false, pingT = 0, signals = 0;
    var el = {
      count: pi("count"), signals: pi("signals"), fut: pi("fut"), mlabel: pi("mlabel"), yax: pi("yax"), plot: pi("plot"),
      lc: pi("lc"), ln: pi("ln"), lw: pi("lw"), band: pi("band"), goal: pi("goal"), en: pi("en"), ec: pi("ec"), ew: pi("ew"),
      cross: pi("cross"), tip: pi("tip"), xmid: pi("xmid"), xend: pi("xend"), nl: pi("nl"), basis: pi("basis"),
      evidence: pi("evidence"), chips: pi("chips"), auto: pi("auto"), aname: pi("aname"), steps: pi("steps"), touch: pi("touch"),
      abook: pi("abook"), aauth: pi("aauth"), aprin: pi("aprin"), yesT: pi("yes-t"), noT: pi("no-t"), need: pi("need"),
      adapt: pi("adapt"), pacts: pi("pacts"), live: pi("live"), core: pi("core")
    };
    signals = parseInt(el.signals.textContent.replace(/\D/g, ""), 10) || 0;
    function say(t) { el.live.textContent = t; }
    function restart(n, cls) { if (!n) return; n.classList.remove(cls); void n.getBoundingClientRect(); n.classList.add(cls); }
    function habit() { return data.habits[H]; }
    function missing(srcs) { return srcs.filter(function (k) { return !perm[k]; }); }
    function names(list) { return list.map(function (k) { return sig[k].name; }).join(", "); }

    /* ---------- Sources ---------- */
    var rows = {};
    $$(".pi-src").forEach(function (r) {
      var k = r.getAttribute("data-src"), s = sig[k];
      var svg = $(".pi-flows-" + (s.side ? "r" : "l"));
      rows[k] = { el: r, sw: r.querySelector(".pi-sw"),
        fl: svg && svg.querySelector('.pi-fl[data-i="' + s.i + '"]'), fd: svg && svg.querySelector('.pi-fd[data-i="' + s.i + '"]') };
      rows[k].sw.addEventListener("click", function () {
        perm[k] = !perm[k];
        say((perm[k] ? "Permission accordée : " : "Permission retirée : ") + s.name + (perm[k] ? "." : ". Ce qui en venait est effacé de la démo."));
        syncPerm();
      });
    });
    function syncPerm() {
      var on = 0, perDay = 0;
      Object.keys(rows).forEach(function (k) {
        var r = rows[k], p = perm[k];
        if (p) { on++; perDay += sig[k].sig; }
        r.el.classList.toggle("is-off", !p);
        r.sw.setAttribute("aria-checked", p ? "true" : "false");
        if (r.fl) r.fl.classList.toggle("is-off", !p);
        if (r.fd) r.fd.classList.toggle("is-off", !p);
      });
      el.count.textContent = on;
      signals = perDay * 7;
      el.signals.textContent = grp(signals);
      $$(".pi-hab").forEach(function (b, i) {
        var miss = missing(data.habits[i].srcs);
        b.classList.toggle("is-blocked", miss.length > 0);
        var n = b.querySelector("[data-pi-need]"); if (n) n.textContent = names(miss);
      });
      $$(".pi-chips span[data-src]").forEach(function (c) { c.classList.toggle("is-off", !perm[c.getAttribute("data-src")]); });
      $$(".pi-adv").forEach(function (a, i) {
        var miss = missing(data.advice[i].srcs);
        if (miss.length) { a.setAttribute("data-state", "off"); a.querySelector("[data-pi-need]").textContent = names(miss); }
        else a.setAttribute("data-state", a.getAttribute("data-done") ? "done" : "ask");
      });
      syncAuto();
      draw(false);
    }

    /* Pouls des signaux : une source à la fois, seulement visible et sous .fx */
    function ping() {
      var ks = Object.keys(perm).filter(function (k) { return perm[k]; });
      if (!ks.length) return;
      var k = ks[Math.floor(Math.random() * ks.length)], r = rows[k];
      r.el.classList.add("is-ping"); if (r.fl) r.fl.classList.add("is-ping"); el.core.classList.add("is-ping");
      signals += 1 + Math.floor(Math.random() * 3);
      el.signals.textContent = grp(signals);
      setTimeout(function () { r.el.classList.remove("is-ping"); if (r.fl) r.fl.classList.remove("is-ping"); el.core.classList.remove("is-ping"); }, 900);
    }
    function loop() {
      clearInterval(pingT); pingT = 0;
      if (visible && fx()) pingT = setInterval(ping, 1500);
    }

    /* ---------- Deux avenirs ---------- */
    var model = null;
    function draw(anim) {
      var h = habit(), blocked = missing(h.srcs).length > 0;
      if (!h.m[M]) M = PRIMARY[h.k];
      $$(".pi-kpi").forEach(function (b) {
        var m = b.getAttribute("data-metric"), ok = !!h.m[m], v = b.querySelector("[data-pi-kv]");
        b.disabled = !ok;
        b.setAttribute("aria-pressed", m === M ? "true" : "false");
        v.textContent = ok ? delta(m, val(h, m, "n", HOR) - val(h, m, "c", HOR)) : "Aucun effet estimé";
      });
      $$("[data-hor]").forEach(function (b) { b.setAttribute("aria-pressed", +b.getAttribute("data-hor") === HOR ? "true" : "false"); });
      el.mlabel.textContent = MLABEL[M];
      var N = 60, ts = [], ser = { c: [], n: [], w: [] }, all = [];
      for (var i = 0; i <= N; i++) {
        var t = HOR * i / N; ts.push(t);
        ["c", "n", "w"].forEach(function (k) { var v = val(h, M, k, t); ser[k].push(v); all.push(v); });
      }
      var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), g = metricGoal(M);
      var showGoal = g.goal !== null && g.goal !== undefined && g.goal <= hi * 1.25 && g.goal >= lo;
      if (showGoal) hi = Math.max(hi, g.goal);
      var pad = (hi - lo) * .12 || 1, nk = nice(lo - pad, hi + pad, M), a = nk[0], b = nk[1], step = nk[2];
      if (M === "objectif" || M === "energie") b = Math.min(b, 100);
      model = { h: h, a: a, b: b, ts: ts };
      function Y(v) { return 400 - (v - a) / (b - a) * 400; }
      function pct(v) { return ((v - a) / (b - a) * 100).toFixed(2); }
      function path(arr) { return "M" + arr.map(function (v, i) { return (ts[i] / HOR * 1000).toFixed(1) + " " + Y(v).toFixed(1); }).join(" L"); }
      el.lc.setAttribute("d", path(ser.c));
      el.ln.setAttribute("d", path(ser.n));
      el.lw.setAttribute("d", path(ser.w));
      var up = [], dn = [];
      ts.forEach(function (t, i) { var d = Math.abs(ser.n[i] - ser.c[i]) * .15, x = (t / HOR * 1000).toFixed(1); up.push(x + " " + Y(ser.n[i] + d).toFixed(1)); dn.unshift(x + " " + Y(ser.n[i] - d).toFixed(1)); });
      el.band.setAttribute("d", "M" + up.concat(dn).join(" L") + " Z");
      var ticks = "";
      for (var v = a; v <= b + 1e-9; v += step) ticks += '<span style="--y:' + pct(v) + '">' + fmt(M, v) + "</span>";
      el.yax.innerHTML = ticks;
      el.goal.hidden = !showGoal;
      if (showGoal) { el.goal.style.setProperty("--y", pct(g.goal)); el.goal.firstChild.textContent = g.goalL; el.goal.classList.toggle("is-top", +pct(g.goal) > 86); }
      /* Étiquettes de fin, écartées si elles se chevauchent */
      var ends = [["c", el.ec, ser.c[N]], ["n", el.en, ser.n[N]]];
      if (dec[H] === "no") ends.push(["w", el.ew, ser.w[N]]);
      el.ew.querySelector("b").textContent = fmt(M, ser.w[N]);
      ends.forEach(function (x) { x[3] = +pct(x[2]); x[1].querySelector("b").textContent = fmt(M, x[2]); });
      ends.sort(function (p, q) { return p[3] - q[3]; });
      for (var j = 1; j < ends.length; j++) if (ends[j][3] - ends[j - 1][3] < 17) ends[j][3] = ends[j - 1][3] + 17;
      var over = ends[ends.length - 1][3] - 92;
      if (over > 0) ends.forEach(function (x) { x[3] -= over; });
      if (ends[0][3] < 8) { var under = 8 - ends[0][3]; ends.forEach(function (x) { x[3] += under; }); }
      ends.forEach(function (x) { x[1].style.setProperty("--y", x[3].toFixed(2)); });
      el.xmid.textContent = "Jour " + Math.round(HOR / 2);
      el.xend.textContent = "Jour " + HOR;
      el.fut.setAttribute("data-dec", blocked ? "blocked" : (dec[H] || "ask"));
      el.nl.textContent = dec[H] === "yes" ? "Avec l’automatisation approuvée" : "Si vous changez";
      el.en.querySelector("span").textContent = dec[H] === "yes" ? "Avec l’automatisation" : "Si vous changez";
      el.plot.setAttribute("aria-label", "Estimation à " + HOR + " jours, " + MLABEL[M] + " : si vous continuez " + fmt(M, ser.c[N]) +
        ", si vous changez " + fmt(M, ser.n[N]) + (dec[H] === "no" ? ", par vous-même " + fmt(M, ser.w[N]) : "") + ".");
      if (anim && fx()) { [el.lc, el.ln, el.lw, el.band].forEach(function (n) { restart(n, "is-draw"); }); }
      syncTexts();
    }

    /* Survol : réticule et valeurs du jour */
    function hover(clientX) {
      if (!model) return;
      var r = el.plot.getBoundingClientRect(), f = Math.max(0, Math.min(1, (clientX - r.left) / r.width)), t = f * HOR, h = model.h;
      var a = model.a, b = model.b;
      function pct(v) { return ((v - a) / (b - a) * 100).toFixed(2); }
      var vc = val(h, M, "c", t), vn = val(h, M, "n", t), vw = val(h, M, "w", t);
      el.plot.style.setProperty("--x", (f * 100).toFixed(2));
      el.cross.querySelector(".c").style.setProperty("--y", pct(vc));
      el.cross.querySelector(".n").style.setProperty("--y", pct(vn));
      el.cross.querySelector(".w").style.setProperty("--y", pct(vw));
      el.cross.style.setProperty("--x", (f * 100).toFixed(2));
      el.tip.style.setProperty("--x", (f * 100).toFixed(2));
      el.tip.style.setProperty("--tx", f > .55 ? "calc(-100% - 12px)" : "12px");
      el.tip.innerHTML = "<p>Jour " + Math.round(t) + " · estimation</p>" +
        "<p><span>Si vous continuez</span><b>" + fmt(M, vc) + "</b></p>" +
        "<p><span>" + (dec[H] === "yes" ? "Avec l’automatisation" : "Si vous changez") + "</span><b>" + fmt(M, vn) + "</b></p>" +
        (dec[H] === "no" ? "<p><span>Par vous-même</span><b>" + fmt(M, vw) + "</b></p>" : "");
    }
    el.plot.addEventListener("pointermove", function (ev) { el.plot.classList.add("is-hover"); hover(ev.clientX); });
    el.plot.addEventListener("pointerdown", function (ev) { el.plot.classList.add("is-hover"); hover(ev.clientX); });
    el.plot.addEventListener("pointerleave", function () { el.plot.classList.remove("is-hover"); });

    $$(".pi-kpi").forEach(function (b) {
      b.addEventListener("click", function () { if (b.disabled) return; M = b.getAttribute("data-metric"); draw(true); say("Projection : " + MLABEL[M] + "."); });
    });
    $$("[data-hor]").forEach(function (b) {
      b.addEventListener("click", function () { HOR = +b.getAttribute("data-hor"); draw(true); say("Horizon : " + HOR + " jours."); });
    });

    /* ---------- Automatisation et décision ---------- */
    function fillTpl(tpl) {
      var h = habit(), m = PRIMARY[h.k];
      var c = val(h, m, "c", HOR), n = val(h, m, "n", HOR), lost;
      if (m === "sommeil") {
        var sum = 0; for (var t = 1; t <= HOR; t++) sum += val(h, m, "n", t) - val(h, m, "c", t);
        lost = "environ " + Math.round(sum) + NB + "h";
      } else lost = fmt(m, Math.abs(n - c)).replace(/^\+/, "");
      var d = m === "sommeil" ? Math.round((n - c) * 60) + NB + "min" : m === "argent" ? grp(Math.round((n - c) / 10) * 10) + NB + "$" : fmt(m, n);
      return tpl.replace("{d}", d).replace(/\{h\}/g, HOR).replace("{c}", fmt(m, c)).replace("{n}", fmt(m, n)).replace("{lost}", lost);
    }
    function syncTexts() {
      var a = habit().auto;
      el.yesT.textContent = fillTpl(a.yes);
      el.noT.textContent = fillTpl(a.no);
    }
    function syncAuto() {
      var h = habit(), miss = missing(h.srcs);
      el.auto.setAttribute("data-state", miss.length ? "blocked" : (dec[H] || "ask"));
      el.need.textContent = names(miss);
    }
    function renderHabit() {
      var h = habit(), a = h.auto;
      el.evidence.textContent = h.evidence;
      el.chips.innerHTML = h.chips;
      el.basis.textContent = h.basis;
      el.aname.textContent = a.name;
      el.touch.innerHTML = a.touch.map(function (t) { return "<span>" + t + "</span>"; }).join("");
      el.steps.innerHTML = a.steps.map(function (s, i) { return '<li style="--i:' + i + '"><time>' + s[0] + "</time><span>" + s[1] + "</span></li>"; }).join("");
      restart(el.steps, "is-in");
      el.abook.textContent = a.book; el.aauth.textContent = a.author; el.aprin.textContent = a.principle;
      $$(".pi-hab").forEach(function (b, i) { b.setAttribute("aria-pressed", i === H ? "true" : "false"); });
      M = PRIMARY[h.k];
      syncPerm();
      draw(true);
    }
    $$(".pi-hab").forEach(function (b, i) {
      b.addEventListener("click", function () { H = i; renderHabit(); say("Habitude : " + b.querySelector("b").textContent + "."); });
    });
    function decide(v) {
      dec[H] = v; syncAuto(); draw(v !== undefined);
      if (v === "yes") say("Approuvé. " + el.yesT.textContent);
      else if (v === "no") say("Refusé. " + el.noT.textContent);
      else say("Décision retirée. Rien n’est actif pour cette habitude.");
    }
    pi("yes").addEventListener("click", function () { decide("yes"); });
    pi("no").addEventListener("click", function () { decide("no"); });
    pi("undo").addEventListener("click", function () { decide(undefined); });
    pi("undo2").addEventListener("click", function () { decide(undefined); });

    /* ---------- Coach : style, conseils, engagements ---------- */
    $$("[data-tone]").forEach(function (b) {
      b.addEventListener("click", function () {
        tone = b.getAttribute("data-tone");
        $$("[data-tone]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        $$(".pi-say").forEach(function (p, i) {
          var txt = data.advice[i].t[tone];
          if (!fx()) { p.textContent = txt; return; }
          p.classList.add("is-swap");
          setTimeout(function () { p.textContent = txt; p.classList.remove("is-swap"); }, 260);
        });
        say("Style du coach : " + b.textContent + ".");
      });
    });
    var ADAPT = [
      "Plan ajusté : dès mardi prochain, course à 6 h 45 les jours de réunion tardive. Réveil à 6 h 20, météo sèche prévue.",
      "Plan ajusté : chaque soir à 22 h 45, rappel de charger le téléphone dans la cuisine.",
      "Plan ajusté : panier d’attente de 24 h actif de 21 h à 23 h. L’automatisation « Panier qui dort » est approuvée.",
      "Plan ajusté : coucher cible à 23 h, à 30 minutes près, sept soirs sur sept."
    ];
    $$(".pi-adv").forEach(function (card, i) {
      card.querySelector("[data-pi-apply]").addEventListener("click", function () {
        card.setAttribute("data-done", "1"); card.setAttribute("data-state", "done");
        el.adapt.querySelector("span").textContent = ADAPT[i].replace(/(\d) h (\d)/g, "$1" + NB + "h" + NB + "$2").replace(/ :/g, NB + ":");
        restart(el.adapt, "is-new");
        if (i === 0) {
          data.move.forEach(function (d) {
            var cell = $('.pi-lane[data-lane="course"] .pi-cell:nth-child(' + (d + 2) + ")");
            if (cell && !cell.querySelector(".is-move")) {
              var s = document.createElement("span");
              s.className = "pi-it is-move"; s.title = "Prochaine fois : 6 h 45";
              s.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8.6"/><path d="M12 7.4V12l3 1.8"/></svg><em>Prochaine : 6' + NB + "h" + NB + "45</em>";
              cell.appendChild(s);
            }
          });
        }
        if (i === 2) {
          for (var k = 0; k < data.habits.length; k++) if (data.habits[k].k === "achats") dec[k] = "yes";
          syncAuto(); draw(false);
        }
        say(el.adapt.textContent);
      });
    });
    $$(".pi-pact").forEach(function (p) {
      var sw = p.querySelector(".pi-sw");
      sw.addEventListener("click", function () {
        var on = sw.getAttribute("aria-checked") !== "true";
        sw.setAttribute("aria-checked", on ? "true" : "false");
        p.classList.toggle("is-on", on);
        var n = $$(".pi-pact.is-on").length;
        el.pacts.textContent = n;
        el.pacts.parentNode.lastChild.textContent = (n > 1 ? " actifs" : " actif") + " sur 4";
        say((on ? "Engagement choisi : " : "Engagement retiré : ") + p.querySelector("b").textContent + ".");
      });
    });

    /* ---------- Visibilité ---------- */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        root.classList.toggle("is-vis", visible);
        if (visible) root.classList.add("is-seen");
        loop();
      }, { threshold: 0.05 }).observe(root);
      var cs = $(".pi-csec");
      if (cs) new IntersectionObserver(function (es) { if (es[0].isIntersecting) root.classList.add("is-seen-c"); }, { threshold: 0.2 }).observe(cs);
      var fut = el.fut, drawn = false;
      new IntersectionObserver(function (es) { if (es[0].isIntersecting && !drawn) { drawn = true; draw(true); } }, { threshold: 0.3 }).observe(fut);
    } else { visible = true; root.classList.add("is-vis", "is-seen", "is-seen-c"); }
    document.addEventListener("visibilitychange", function () { if (document.hidden) { clearInterval(pingT); pingT = 0; } else loop(); });

    renderHabit();
  });
})();
