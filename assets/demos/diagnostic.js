/* Démo « Diagnostic & continuité » : enquête guidée en cinq étapes (données simulées).
   Les chiffres viennent de la simulation de src/demos/diagnostic.py (bloc JSON).
   Lecture automatique jusqu'à l'étape 5, qui attend « Approuver l'intervention ».
   Sous html.fx, la mesure vit : la valeur du capteur bouge un peu, le point
   « Maintenant » respire, la courbe se trace avec sa tête de lecture, chaque
   cause écartée est biffée avec sa raison, le dossier s'assemble page par page
   et, après l'accord, le graphique se rapproche des dernières heures pour
   montrer le retour dans la plage normale en temps réel.
   Sans JavaScript, les cinq étapes du premier cas restent lisibles. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="diagnostic"]');
  if (!root || !window.SVGElement) return;
  var DATA;
  try { DATA = JSON.parse(root.querySelector(".dg-data").textContent); } catch (e) { return; }
  var NS = "http://www.w3.org/2000/svg";
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs[k] !== undefined) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function fr(v, d) { return v.toFixed(d === undefined ? 1 : d).replace(".", ","); }
  function hm(m) {
    var t = (Math.round(m) + 720) % 1440, h = Math.floor(t / 60), mn = t % 60;
    return h + " h" + (mn ? " " + (mn < 10 ? "0" : "") + mn : "");
  }
  function ease(k) { return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }
  root.classList.add("is-live");

  var svg = $(".dg-svg"), chart = $(".dg-chart"), tip = $(".dg-tip"), sweep = $(".dg-sweep"), stage = $(".dg-stage");
  var rail = $(".dg-rail"), railLis = $$(".dg-rail li");
  var playBtn = $('[data-nav="play"]'), prevBtn = $('[data-nav="prev"]'), nextBtn = $('[data-nav="next"]');
  var DUR = [0, 6, 8.5, 9.5, 8, 0];
  var S = { cas: "froid", step: 1, playing: !reduce, approved: false, auto: 0, hover: false, fx: false, zoom: 0, live: 0 };
  var D = DATA.froid, G = {};

  /* ---------- Horloge (s'arrête hors écran) ---------- */
  var clock = 0, events = [], tweens = [], running = false, raf = 0, last = 0, visible = false;
  function later(sec, fn) { events.push({ t: clock + (reduce ? Math.min(sec, .05) : sec), fn: fn }); }
  function tween(dur, fn, done) {
    if (reduce || dur <= 0) { fn(1); if (done) done(); return; }
    tweens.push({ t0: clock, d: dur, fn: fn, done: done });
  }
  function tick(now) {
    raf = 0;
    var dt = Math.min(.05, Math.max(0, (now - last) / 1000));
    last = now; clock += dt;
    if (tweens.length) {
      var fin = [];
      tweens.slice().forEach(function (tw) {
        var k = Math.min(1, (clock - tw.t0) / tw.d);
        tw.fn(k);
        if (k >= 1) { tw.fin = true; fin.push(tw); }
      });
      tweens = tweens.filter(function (tw) { return !tw.fin; });
      fin.forEach(function (tw) { if (tw.done) tw.done(); });
    }
    if (events.length) {
      var due = [], rest = [];
      events.forEach(function (e) { (e.t <= clock ? due : rest).push(e); });
      if (due.length) { events = rest; due.forEach(function (e) { e.fn(); }); }
    }
    var dur = DUR[S.step];
    if (S.playing && !S.hover && dur) {
      S.auto += dt;
      var on = railLis[S.step - 1];
      if (on) $("button", on).style.setProperty("--p", Math.min(1, S.auto / dur).toFixed(3));
      if (S.auto >= dur) go(S.step + 1, true);
    }
    if (running) raf = requestAnimationFrame(tick);
  }
  function sync() {
    var want = visible && !document.hidden;
    if (want && !running) { running = true; last = performance.now(); raf = requestAnimationFrame(tick); }
    else if (!want && running) { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }
  }

  /* ---------- Graphique : tracé à la taille réelle (texte net sur téléphone) ---------- */
  function valAt(arr, m) {
    var f = m / D.step, i = Math.max(0, Math.min(arr.length - 2, Math.floor(f))), k = Math.min(1, Math.max(0, f - i));
    return arr[i] + (arr[i + 1] - arr[i]) * k;
  }
  function pathOf(arr, fx, fy, m0, m1) {
    var i0 = Math.max(0, Math.floor(m0 / D.step)), i1 = Math.min(arr.length - 1, Math.ceil(m1 / D.step)), d = "";
    for (var i = i0; i <= i1; i++) d += (i === i0 ? "M" : "L") + fx(i * D.step).toFixed(1) + " " + fy(arr[i]).toFixed(1);
    return d;
  }
  /* Début de la fenêtre affichée : zoom 0 = les 27 h; zoom 1 = cinq heures avant « Maintenant » */
  function dom0() { return Math.max(0, D.now - 300) * S.zoom; }
  function tickLabel(m, small) {
    if (m === 0) return small ? "12 h" : "Hier 12 h";
    if (m === 720) return small ? "0 h" : "Minuit";
    return hm(m);
  }
  function build() {
    D = DATA[S.cas];
    var kp = G.past || 0, kf = G.fut || D.now;
    var W = Math.max(260, Math.round(chart.clientWidth)), small = W < 520;
    var H = small ? 280 : 410, L = small ? 31 : 34, R = 8, T = 30, B = 20, secH = small ? 38 : 46;
    var mainB = H - T - B - 25 - 18 - secH + T, compY = mainB + 17, secT = compY + 8 + 18, secB = H - B;
    G = { W: W, H: H, L: L, R: R, T: T, mainB: mainB, compY: compY, secT: secT, secB: secB, small: small };
    var pw = W - L - R, m0 = dom0(), span = D.end - m0;
    var x = G.x = function (m) { return L + (m - m0) / span * pw; };
    G.m0 = m0; G.span = span;
    sweep.style.cssText = "left:" + L + "px;top:" + T + "px;width:" + pw + "px;height:" + (secB - T) + "px";
    var y = G.y = function (v) { return T + (mainB - T) * (1 - (v - D.y[0]) / (D.y[1] - D.y[0])); };
    var sy = function (v) { return secT + (secB - secT) * (1 - (v - D.sy[0]) / (D.sy[1] - D.sy[0])); };
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("height", H);
    svg.classList.toggle("is-small", small);
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    var defs = el("defs", {}, svg);
    var a0 = (x(D.anom[0]) - L) / pw, fx0 = x(D.now), fx1 = x(D.verify);
    var g1 = el("linearGradient", { id: "dg-grad", gradientUnits: "userSpaceOnUse", x1: L, x2: W - R, y1: 0, y2: 0 }, defs);
    [[0, "var(--gold-soft)"], [a0 - .012, "var(--gold-soft)"], [a0 + .012, "var(--dg-bad)"], [1, "var(--dg-bad)"]].forEach(function (s) {
      el("stop", { offset: Math.max(0, Math.min(1, s[0])), style: "stop-color:" + s[1] }, g1);
    });
    var g2 = el("linearGradient", { id: "dg-grad2", gradientUnits: "userSpaceOnUse", x1: fx0, x2: fx1, y1: 0, y2: 0 }, defs);
    el("stop", { offset: 0, style: "stop-color:var(--dg-bad)" }, g2);
    el("stop", { offset: 1, style: "stop-color:var(--dg-ok)" }, g2);
    var ga = el("linearGradient", { id: "dg-area", x1: 0, x2: 0, y1: 0, y2: 1 }, defs);
    el("stop", { offset: 0, style: "stop-color:var(--gold-soft);stop-opacity:.2" }, ga);
    el("stop", { offset: 1, style: "stop-color:var(--gold-soft);stop-opacity:0" }, ga);
    var gp = el("linearGradient", { id: "dg-peng", x1: 0, x2: 1, y1: 0, y2: 0 }, defs);
    el("stop", { offset: 0, style: "stop-color:var(--gold-soft);stop-opacity:0" }, gp);
    el("stop", { offset: 1, style: "stop-color:var(--gold-soft);stop-opacity:.22" }, gp);
    var pat = el("pattern", { id: "dg-hatch", width: 6, height: 6, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" }, defs);
    el("line", { x1: 0, y1: 0, x2: 0, y2: 6, stroke: "#ffffff", "stroke-opacity": ".06", "stroke-width": 2 }, pat);
    var cp = el("clipPath", { id: "dg-cp" }, defs), cf = el("clipPath", { id: "dg-cf" }, defs);
    G.clipP = el("rect", { x: L - 3, y: 0, width: 0, height: H }, cp);
    G.clipF = el("rect", { x: x(D.now), y: 0, width: 0, height: H }, cf);

    // Grille, axes, plage normale, consigne, avenir hachuré
    var grid = el("g", {}, svg);
    for (var v = D.y[0] + 2; v < D.y[1]; v += 2) {
      el("line", { class: "dg-gl", x1: L, x2: W - R, y1: y(v), y2: y(v) }, grid);
      el("text", { x: L - 6, y: y(v) + 3.5, "text-anchor": "end" }, grid).textContent = v + "°";
    }
    // Graduations : aux 6 h sur la journée, plus serrées quand le graphique se rapproche
    var every = span > 900 ? 360 : span > 560 ? 120 : (small ? 120 : 60), last = 0;
    for (var tk = Math.ceil(m0 / every) * every; tk <= D.end; tk += every) {
      var tx = x(tk), edge = tx > W - R - 12;
      el("line", { class: "dg-gl", x1: tx, x2: tx, y1: T, y2: secB }, grid);
      el("text", { x: tx + (tk === m0 ? 1 : 0), y: H - 5, "text-anchor": tk === m0 ? "start" : edge ? "end" : "middle" }, grid).textContent = tickLabel(tk, small);
      last = tk;
    }
    if (!small && D.end - last > every * .4) el("text", { x: W - R, y: H - 5, "text-anchor": "end" }, grid).textContent = hm(D.end);
    el("rect", { class: "dg-fut", x: x(D.now), y: T, width: x(D.end) - x(D.now), height: secB - T }, svg);
    el("rect", { class: "dg-band", x: L, width: pw, y: y(D.band[1]), height: y(D.band[0]) - y(D.band[1]) }, svg);
    el("line", { class: "dg-bandl", x1: L, x2: W - R, y1: y(D.band[1]), y2: y(D.band[1]) }, svg);
    el("line", { class: "dg-bandl", x1: L, x2: W - R, y1: y(D.band[0]), y2: y(D.band[0]) }, svg);
    var setG = el("g", { "data-k": "set" }, svg);
    el("line", { class: "dg-set", x1: L, x2: x(D.now), y1: y(D.set), y2: y(D.set) }, setG);
    // Fenêtre d'anomalie
    var ax = Math.max(L, x(D.anom[0]));
    el("rect", { class: "dg-anom", x: ax, y: T, width: x(D.anom[1]) - ax, height: mainB - T, rx: 4 }, svg);
    var at = el("text", { class: "dg-anomt halo", x: x(D.anom[1]) - 6, y: mainB - 16, "text-anchor": "end" }, svg);
    at.textContent = D.lab.anom;
    try { if (x(D.anom[1]) - 6 - at.getComputedTextLength() < L) { at.setAttribute("x", L + 4); at.setAttribute("text-anchor", "start"); } } catch (e) { /* mesure indisponible */ }
    // Libellés des voies
    el("text", { class: "dg-lane halo", x: L, y: compY - 5 }, svg).textContent = D.lab.comp.toUpperCase();
    el("text", { class: "dg-lane halo", x: L, y: secT - 6 }, svg).textContent = D.lab.sec.toUpperCase();

    // Passé (révélé de gauche à droite) et suite après l'accord
    function layer(clip, future) {
      var g = el("g", { "clip-path": "url(#" + clip + ")" }, svg);
      var comp = el("g", { class: "dg-comp", "data-k": "comp" }, g);
      D.comp.forEach(function (c) {
        var cls = c[0] >= D.anom[0] && c[0] < D.fix ? "is-anom" : (c[0] >= D.fix ? "is-fix" : "");
        el("rect", { class: cls, x: x(c[0]), y: compY, width: Math.max(1.4, x(c[1]) - x(c[0])), height: 8, rx: 2 }, comp);
      });
      if (D.sthr !== null) {
        el("line", { class: "dg-thr", x1: L, x2: W - R, y1: sy(D.sthr), y2: sy(D.sthr) }, g);
      }
      var from = Math.max(0, m0 - D.step);
      el("path", { class: future ? "dg-secp2" : "dg-secp", "data-k": "sec", d: pathOf(D.s, x, sy, future ? D.now : from, D.end) }, g);
      if (!future) {
        el("path", { class: "dg-area", "data-k": "line", d: pathOf(D.t, x, y, from, D.now) + "L" + x(D.now).toFixed(1) + " " + mainB + "L" + L + " " + mainB + "Z" }, g);
        el("path", { class: "dg-line", "data-k": "line", d: pathOf(D.t, x, y, from, D.now) }, g);
        var marks = el("g", { class: "dg-marks" }, g), dg = el("g", { "data-k": "doors" }, marks);
        D.doors.forEach(function (m) {
          if (m > D.now) return;
          el("circle", { class: "dg-door", cx: x(m), cy: mainB - 5, r: 2.6 }, dg);
        });
        D.cuts.forEach(function (m) {
          el("path", { class: "dg-cut", "data-k": "sec", d: "M" + x(m).toFixed(1) + " " + (compY - 1) + "l-4 -7h8z" }, marks);
        });
      } else {
        el("path", { class: "dg-line2", "data-k": "line", d: pathOf(D.t, x, y, D.now, D.end) }, g);
      }
    }
    layer("dg-cp", false);
    layer("dg-cf", true);
    if (D.sthr !== null) {
      el("text", { class: "dg-thrt halo", x: L + 2, y: sy(D.sthr) - 4 }, svg).textContent = D.lab.thr;
    }

    // Repère « Maintenant », drapeau de vérification, tête lumineuse, curseur
    G.now = el("g", { class: "dg-now" }, svg);
    el("line", { class: "dg-nowl", x1: 0, x2: 0, y1: T - 6, y2: secB }, G.now);
    var pill = G.pill = el("g", { class: "dg-nowp" }, G.now);
    G.pillR = el("rect", { x: -48, y: T - 26, width: 96, height: 18, rx: 9 }, pill);
    G.nowT = el("text", { x: 0, y: T - 13.5 }, pill);
    var fl = G.flag = el("g", { class: "dg-flag", transform: "translate(" + x(D.verify).toFixed(1) + " " + y(valAt(D.t, D.verify)).toFixed(1) + ")" }, svg);
    el("line", { x1: 0, x2: 0, y1: 0, y2: -34 }, fl);
    el("circle", { r: 4 }, fl);
    var fr_ = el("rect", { y: -54, height: 20, rx: 10 }, fl), ft = el("text", { y: -40 }, fl);
    ft.textContent = D.lab.verify;
    var fw = 124;
    try { fw = ft.getComputedTextLength() + 20; } catch (e) { fw = 124; }
    var fxp = Math.min(0, (W - R) - x(D.verify) - fw / 2);
    fr_.setAttribute("x", (-fw / 2 + fxp).toFixed(1)); fr_.setAttribute("width", fw.toFixed(1)); ft.setAttribute("x", fxp.toFixed(1));
    // Tête de lecture (tracé et vérification), point « Maintenant » qui respire, valeur en direct
    G.pen = el("g", { class: "dg-pen" }, svg);
    el("rect", { x: -18, y: T, width: 18, height: secB - T }, G.pen);
    el("line", { x1: 0, x2: 0, y1: T, y2: secB }, G.pen);
    G.live = el("g", { class: "dg-live" }, svg);
    el("circle", { class: "r", r: 5 }, G.live); el("circle", { class: "c", r: 3.6 }, G.live);
    G.liveT = el("text", { class: "halo", x: 9, y: 4 }, G.live);
    G.head = el("g", { class: "dg-headdot" }, svg);
    el("circle", { class: "h", r: 9 }, G.head); el("circle", { class: "c", r: 3.4 }, G.head);
    G.headT = el("text", { class: "halo", y: -14 }, G.head);
    G.cur = el("g", { class: "dg-cur" }, svg);
    G.curL = el("line", { y1: T, y2: secB }, G.cur);
    G.curD = el("circle", { r: 4.5 }, G.cur);
    G.hit = el("rect", { class: "dg-hit", x: L, y: 0, width: pw, height: H }, svg);
    G.hit.addEventListener("pointermove", hover);
    G.hit.addEventListener("pointerdown", hover);
    G.hit.addEventListener("pointerleave", unhover);
    G.past = kp; G.fut = kf;
    setPast(G.past); setFut(G.fut);
    setLive(S.live || valAt(D.t, D.now));
  }
  function setLive(v) {
    S.live = v;
    G.live.setAttribute("transform", "translate(" + G.x(D.now).toFixed(1) + " " + G.y(v).toFixed(1) + ")");
    G.liveT.textContent = fr(v) + "°";
  }
  function setHead(m, show) {
    G.head.style.display = show ? "" : "none";
    if (show) G.head.setAttribute("transform", "translate(" + G.x(m).toFixed(1) + " " + G.y(valAt(D.t, m)).toFixed(1) + ")");
  }
  function setNow(m) {
    G.nowT.textContent = D.lab.now + " · " + hm(m);
    var tw = 0;
    try { tw = G.nowT.getComputedTextLength(); } catch (e) { tw = 0; }
    var half = Math.max(30, tw / 2 + 9), px = G.x(m), cx = Math.max(G.L + half - 6, Math.min(G.W - G.R - half + 4, px));
    G.pillR.setAttribute("x", (-half).toFixed(1)); G.pillR.setAttribute("width", (2 * half).toFixed(1));
    G.now.setAttribute("transform", "translate(" + px.toFixed(1) + " 0)");
    G.pill.setAttribute("transform", "translate(" + (cx - px).toFixed(1) + " 0)");
  }
  function setPast(m) {
    G.past = m;
    G.clipP.setAttribute("width", Math.max(0, G.x(m) - G.L + 3).toFixed(1));
    setHead(m, m > 0 && m < D.now - .5);
    G.pen.setAttribute("transform", "translate(" + G.x(m).toFixed(1) + " 0)");
    G.now.style.display = m >= D.now - .5 ? "" : "none";
    G.live.style.display = m >= D.now - .5 && G.fut <= D.now + .5 ? "" : "none";
    G.headT.style.display = "none";
    if (G.fut <= D.now) setNow(D.now);
  }
  function setFut(m) {
    G.fut = m;
    G.clipF.setAttribute("width", Math.max(0, G.x(m) - G.x(D.now)).toFixed(1));
    if (m > D.now) {
      var v = valAt(D.t, m), inb = v >= D.band[0] && v <= D.band[1];
      setNow(m); setHead(m, m < D.end - .5);
      G.live.style.display = "none";
      G.pen.setAttribute("transform", "translate(" + G.x(m).toFixed(1) + " 0)");
      G.headT.style.display = "";
      G.headT.setAttribute("x", Math.min(0, G.W - G.R - G.x(m) - 26).toFixed(1));
      G.headT.textContent = fr(v) + " °C";
      G.headT.setAttribute("class", "halo" + (inb ? " is-ok" : ""));
      svg.classList.toggle("is-inband", inb && m < D.end - .5);
    }
  }

  /* Survol de la courbe : heure, température, compresseur, deuxième mesure */
  function hover(e) {
    if (S.step < 2) return;
    var r = svg.getBoundingClientRect(), px = e.clientX - r.left;
    var m = Math.max(G.m0, Math.min(D.end, G.m0 + (px - G.L) / (G.W - G.L - G.R) * G.span));
    var lim = G.fut > D.now ? G.fut : G.past;
    if (m > lim) { unhover(); return; }
    var tv = valAt(D.t, m), sv = valAt(D.s, m), on = D.comp.some(function (c) { return c[0] <= m && m < c[1]; });
    var X = G.x(m), Y = G.y(tv);
    G.curL.setAttribute("x1", X); G.curL.setAttribute("x2", X);
    G.curD.setAttribute("cx", X); G.curD.setAttribute("cy", Y);
    G.cur.classList.add("is-on");
    tip.innerHTML = "";
    var b = document.createElement("b"); b.textContent = (m < 720 ? "Hier " : "Aujourd’hui ") + hm(m); tip.appendChild(b);
    var st = document.createElement("strong"); st.textContent = fr(tv) + " °C"; tip.appendChild(st);
    var s1 = document.createElement("span"); s1.textContent = D.lab.comp + " : " + (on ? D.lab.on : D.lab.off); tip.appendChild(s1);
    var s2 = document.createElement("span"); s2.textContent = D.sname + " : " + fr(sv, D.sdec === 2 ? 2 : 1) + " " + D.sunit; tip.appendChild(s2);
    tip.hidden = false;
    var tw = tip.offsetWidth, th = tip.offsetHeight;
    var lx = X + 14 + tw > G.W ? X - 14 - tw : X + 14, ly = Math.max(0, Math.min(G.H - th, Y - th / 2));
    tip.style.transform = "translate(" + Math.round(lx) + "px," + Math.round(ly) + "px)";
    tip.classList.add("is-on");
  }
  function unhover() { if (G.cur) G.cur.classList.remove("is-on"); tip.classList.remove("is-on"); }

  /* ---------- Étapes ---------- */
  function panel(n) { return $('.dg-step[data-case="' + S.cas + '"][data-step="' + (n || S.step) + '"]'); }
  function resetPanel(p) {
    p.classList.remove("is-concl", "is-verified");
    $$(".dg-checks li", p).forEach(function (li) { li.className = ""; });
    $$(".dg-sheet .is-in", p).forEach(function (n) { n.classList.remove("is-in"); });
    var sh = $(".dg-sheet", p); if (sh) { sh.classList.remove("is-ready", "is-laid"); sh.style.removeProperty("--pg"); }
    var pr = $(".dg-prop", p);
    if (pr) { pr.className = "dg-prop"; $$(".dg-flow li", pr).forEach(function (li) { li.className = ""; }); }
  }
  function flow(p, k, cls) { var li = $('.dg-flow li[data-k="' + k + '"]', p); if (li) li.className = cls; }

  function go(n, auto) {
    n = Math.max(1, Math.min(5, n));
    S.step = n; S.auto = 0; events = []; tweens = [];
    S.fx = !reduce && document.documentElement.classList.contains("fx");
    $$(".dg-fly", stage).forEach(function (g) { g.remove(); });
    svg.classList.remove("is-drawing", "is-inband");
    if (S.zoom && !(n === 5 && S.approved)) { S.zoom = 0; build(); }
    root.setAttribute("data-step", n);
    root.classList.remove("is-end");
    railLis.forEach(function (li, i) {
      li.classList.toggle("is-on", i + 1 === n);
      li.classList.toggle("is-done", i + 1 < n);
      li.classList.remove("is-ok");
      var b = $("button", li); b.style.setProperty("--p", "0");
      if (i + 1 === n) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
    });
    rail.style.setProperty("--done", ((n - 1) / 4).toFixed(3));
    prevBtn.disabled = n === 1; nextBtn.disabled = n === 5;
    $$(".dg-step").forEach(function (p) { p.classList.remove("is-on"); });
    var p = panel(n);
    resetPanel(p);
    p.classList.add("is-on");
    svg.removeAttribute("data-hl");
    svg.classList.remove("is-verified");
    unhover();
    enter[n](p);
    if (S.fx) later(n === 1 ? 2.2 : 1.4, liveTick);
  }

  /* ---------- Capteur en direct : petite dérive et bruit de mesure ---------- */
  var ticks = 0;
  function liveTick() {
    if (G.fut > D.now + .5) return;
    var base = valAt(D.t, D.now), v = base + Math.min(.05, ticks++ * .012) + (Math.random() - .5) * .1;
    setLive(v);
    if (S.step === 1) {
      var h = $('.dg-hero[data-case="' + S.cas + '"]'), b = $(".dg-big b", h), gauge = $(".dg-gauge", h);
      var to = +b.getAttribute("data-to"), per = parseFloat(gauge.style.getPropertyValue("--v")) / to, txt = fr(v);
      gauge.style.setProperty("--vk", (v * per).toFixed(2) + "%");
      if (b.textContent !== txt) {
        b.textContent = txt;
        if (b.animate) b.animate([{ opacity: .5, transform: "translateY(4px)" }, { opacity: 1, transform: "none" }], { duration: 420, easing: "cubic-bezier(.16,1,.3,1)" });
      }
      var hk = $(".dg-hk", h);
      hk.classList.remove("is-tick"); void hk.offsetWidth; hk.classList.add("is-tick");
    }
    later(1.5 + Math.random() * .9, liveTick);
  }

  /* Faisceau qui parcourt le graphique (lecture des preuves à l'étape 3) */
  function scan() {
    if (!S.fx) return;
    sweep.classList.remove("is-on"); void sweep.offsetWidth; sweep.classList.add("is-on");
  }

  /* Une pièce jointe quitte sa voie du graphique et rejoint le dossier */
  function fly(chip) {
    var lane = chip.getAttribute("data-from"), r = svg.getBoundingClientRect(), o = stage.getBoundingClientRect();
    var mx = (Math.max(G.m0, D.anom[0]) + D.now) / 2;
    var sy = lane === "comp" ? G.compY + 4 : lane === "sec" ? (G.secT + G.secB) / 2 : G.y(valAt(D.t, mx));
    var ax = r.left + G.x(mx), ay = r.top + sy, b = chip.getBoundingClientRect();
    if (!S.fx || ay < 0 || ay > innerHeight || !b.width) return false;
    var g = document.createElement("span");
    g.className = "dg-fly";
    g.setAttribute("aria-hidden", "true");
    g.textContent = chip.textContent;
    stage.appendChild(g);
    var x0 = ax - o.left - g.offsetWidth / 2, y0 = ay - o.top - g.offsetHeight / 2, x1 = b.left - o.left, y1 = b.top - o.top;
    tween(.75, function (k) {
      var e = ease(k), arc = Math.sin(Math.PI * e) * -40;
      g.style.transform = "translate(" + (x0 + (x1 - x0) * e).toFixed(1) + "px," + (y0 + (y1 - y0) * e + arc).toFixed(1) + "px) scale(" + (.85 + .15 * e).toFixed(3) + ")";
      g.style.opacity = k < .12 ? k / .12 : k > .9 ? (1 - k) / .1 : 1;
    }, function () { g.remove(); });
    return true;
  }

  var enter = {
    1: function () {
      setFut(D.now); setPast(0);
      svg.classList.remove("is-marked", "is-anom");
      var h = $('.dg-hero[data-case="' + S.cas + '"]'), b = $(".dg-big b", h), gauge = $(".dg-gauge", h);
      var from = +b.getAttribute("data-from"), to = +b.getAttribute("data-to");
      var v0 = parseFloat(gauge.style.getPropertyValue("--v0")), v1 = parseFloat(gauge.style.getPropertyValue("--v"));
      b.textContent = fr(from);
      tween(1.6, function (k) {
        var e = ease(k);
        b.textContent = fr(from + (to - from) * e);
        gauge.style.setProperty("--vk", (v0 + (v1 - v0) * e).toFixed(2) + "%");
      });
    },
    2: function () {
      setFut(D.now);
      svg.classList.remove("is-marked", "is-anom");
      setPast(0);
      if (S.fx) svg.classList.add("is-drawing");
      tween(2.8, function (k) { setPast(D.now * ease(k)); }, function () {
        svg.classList.remove("is-drawing");
        svg.classList.add("is-marked");
        later(.5, function () { svg.classList.add("is-anom"); });
      });
    },
    3: function (p) {
      full();
      var lis = $$(".dg-checks li", p);
      lis.forEach(function (li, i) {
        var t0 = .5 + i * 1.2;
        later(t0, function () { li.className = "is-run"; svg.setAttribute("data-hl", li.getAttribute("data-hl")); scan(); });
        later(t0 + .85, function () { li.className = "is-done"; });
      });
      later(.5 + lis.length * 1.2 + .1, function () { p.classList.add("is-concl"); svg.setAttribute("data-hl", "sec"); });
    },
    4: function (p) {
      full();
      var sh = $(".dg-sheet", p), chips = $$(".dg-att", p), gap = S.fx ? .3 : .22;
      var rows = [$(".dg-sheet header", p)].concat($$(".dg-sheet dl div", p), [$(".dg-sheet footer", p)]);
      later(.05, function () { sh.classList.add("is-laid"); });
      rows.forEach(function (r, i) { later(.3 + i * gap, function () { r.classList.add("is-in"); }); });
      // Chaque pièce jointe arrive du graphique et ajoute une page sous le dossier
      var t = .3 + rows.length * gap;
      chips.forEach(function (c, i) {
        later(t + i * .5, function () {
          var flew = fly(c);
          later(flew ? .7 : 0, function () { c.classList.add("is-in"); sh.style.setProperty("--pg", i + 1); });
        });
      });
      t += S.fx ? chips.length * .5 + .5 : .2;
      later(t, function () { sh.classList.add("is-ready"); });
      later(t + .6, function () { p.classList.add("is-concl"); });
    },
    5: function (p) {
      full();
      var pr = $(".dg-prop", p);
      if (S.approved) { finish(p, false); return; }
      pr.classList.add("is-wait");
    }
  };
  function full() {
    setFut(D.now); setPast(D.now);
    svg.classList.add("is-marked", "is-anom");
  }
  function approve(p) {
    var pr = $(".dg-prop", p);
    if (S.approved || pr.classList.contains("is-sent")) return;
    S.approved = true; S.playing = false; syncPlay();
    pr.classList.remove("is-wait"); pr.classList.add("is-sent");
    flow(p, "sent", "is-on is-done");
    var worked = false, read = false, ok = false;
    later(.5, function () { if (!worked) flow(p, "work", "is-on is-run"); });
    if (S.fx) {
      tween(1.1, function (k) { S.zoom = ease(k); build(); }, verify);
    } else verify();
    function verify() {
    if (S.fx) svg.classList.add("is-drawing");
    tween(S.fx ? 7 : 6.5, function (k) {
      var m = D.now + (D.end - D.now) * k;
      setFut(m);
      if (!worked && m >= D.fix + 4) { worked = true; flow(p, "work", "is-on is-done"); flow(p, "read", "is-on is-run"); }
      if (!read && m >= D.verify) {
        read = true; flow(p, "read", "is-on is-done"); flow(p, "ok", "is-on is-done");
        svg.classList.add("is-verified");
      }
      if (!ok && m >= D.verify + 8) { ok = true; p.classList.add("is-verified"); railLis[4].classList.add("is-ok"); }
    }, function () { finish(p, true); });
    }
  }
  function finish(p, animated) {
    var pr = $(".dg-prop", p);
    pr.classList.remove("is-wait"); pr.classList.add("is-sent");
    ["sent", "work", "read", "ok"].forEach(function (k) { flow(p, k, "is-on is-done"); });
    svg.classList.remove("is-drawing", "is-inband");
    if (S.fx && S.zoom !== 1) { S.zoom = 1; build(); }
    setFut(D.end);
    svg.classList.add("is-verified");
    p.classList.add("is-verified");
    railLis[4].classList.add("is-ok");
    railLis[4].classList.add("is-done");
    rail.style.setProperty("--done", "1");
    root.classList.add("is-end");
    if (!animated) setHead(D.end, false);
  }

  /* ---------- Commandes ---------- */
  function syncPlay() { playBtn.setAttribute("aria-pressed", S.playing ? "true" : "false"); }
  function setCase(k) {
    S.cas = k; S.approved = false; S.zoom = 0; S.live = 0;
    $$(".dg-cases button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-case") === k ? "true" : "false"); });
    $$(".dg-step, .dg-hero, .dg-legend").forEach(function (n) { n.hidden = n.getAttribute("data-case") !== k; });
    G.past = 0; G.fut = DATA[k].now;
    build();
  }
  root.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("button") : null;
    if (!b || !root.contains(b)) return;
    if (b.hasAttribute("data-case")) { setCase(b.getAttribute("data-case")); S.playing = !reduce; syncPlay(); go(1, true); return; }
    if (b.hasAttribute("data-go")) { S.playing = false; syncPlay(); go(+b.getAttribute("data-go")); return; }
    var nav = b.getAttribute("data-nav");
    if (nav === "prev") { S.playing = false; syncPlay(); go(S.step - 1); }
    else if (nav === "next") { S.playing = false; syncPlay(); go(S.step + 1); }
    else if (nav === "play") {
      S.playing = !S.playing; syncPlay();
      if (S.playing && S.step === 5 && S.approved) { S.approved = false; go(1, true); }
    }
    else if (nav === "replay") { S.approved = false; S.playing = !reduce; syncPlay(); go(1, true); }
    else if (b.getAttribute("data-act") === "approve") approve(b.closest(".dg-step"));
  });

  stage.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") S.hover = true; });
  stage.addEventListener("pointerleave", function () { S.hover = false; });
  root.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest(".dg-rail, .dg-ctrl")) {
      if (e.key === "ArrowRight") { S.playing = false; syncPlay(); go(S.step + 1); }
      else if (e.key === "ArrowLeft") { S.playing = false; syncPlay(); go(S.step - 1); }
    }
  });

  /* ---------- Démarrage ---------- */
  setCase("froid");
  syncPlay();
  go(1, true);
  var lastW = chart.clientWidth;
  if (window.ResizeObserver) {
    var rt = 0;
    new ResizeObserver(function () {
      if (Math.abs(chart.clientWidth - lastW) < 2) return;
      clearTimeout(rt);
      rt = setTimeout(function () { lastW = chart.clientWidth; build(); }, 120);
    }).observe(chart);
  }
  var started = false;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { visible = e.isIntersecting; });
      if (visible && !started) { started = true; go(1, true); }
      sync();
    }, { threshold: .25 }).observe(root);
  } else { visible = true; sync(); }
  document.addEventListener("visibilitychange", sync);
})();
