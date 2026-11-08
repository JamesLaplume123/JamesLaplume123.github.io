/* Démo « Réseau et cybersécurité » : console réseau de JARVIS, douze modules (données d'exemple).
   La lumière qui circule sur la carte est en CSS (sous html.fx); ce script tient l'horloge,
   les chiffres en direct, les situations (rien n'est appliqué sans « Approuver »), la carte de
   chaleur Wi-Fi, le graphique du trafic, la carte des menaces et les petites commandes.
   Tout s'arrête quand la démo sort de l'écran. Sans JavaScript, la topologie reste lisible
   (voir src/demos/reseau.py). */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="reseau"]');
  if (!root) return;
  var NS = "http://www.w3.org/2000/svg";
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }
  function svgEl(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function fr(n, d) { return n.toFixed(d || 0).replace(".", ","); }
  function thousands(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function setAll(key, txt) { $$('[data-live="' + key + '"]').forEach(function (e) { e.textContent = txt; }); }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function hms(d) { return pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds()); }
  /* Heure de la démo : 17 h 52 au chargement, puis le temps réel s'écoule (cohérent avec le journal). */
  var T0 = Date.now(), D0 = new Date(); D0.setHours(17, 52, 4, 0);
  function now() { return new Date(D0.getTime() + (Date.now() - T0)); }
  root.classList.add("is-live");

  /* ---------- Visibilité : tout s'arrête hors écran ---------- */
  var visible = true;
  if ("IntersectionObserver" in window) {
    visible = false;
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      root.classList.toggle("is-vis", visible);
    }, { rootMargin: "80px" }).observe(root);
  } else root.classList.add("is-vis");

  /* ---------- État partagé ---------- */
  var S = { down: 312, up: 41, blocked: 1284, wan: "fibre", alerts: 0, t: 0 };
  var WAN = { fibre: "Fibre · 9 ms", g5: "5G · 31 ms" };

  /* ---------- Accord avant d'agir (générique) ---------- */
  var timers = [];
  function later(fn, ms) { var t = setTimeout(fn, reduce ? Math.min(ms, 250) : ms); timers.push(t); return t; }
  function runFlow(list, onDone, step) {
    list.forEach(function (li) { li.classList.remove("is-run", "is-done"); });
    var i = 0;
    (function next() {
      if (i > 0) { list[i - 1].classList.remove("is-run"); list[i - 1].classList.add("is-done"); }
      if (i >= list.length) { if (onDone) onDone(); return; }
      list[i].classList.add("is-run");
      i++;
      later(next, step || 950);
    })();
  }
  function resetProp(p) {
    p.classList.remove("is-ok", "is-no");
    $$(".rs-flowl li", p).forEach(function (li) { li.classList.remove("is-run", "is-done"); });
  }
  var propDone = {};
  root.addEventListener("click", function (e) {
    var b = e.target.closest(".rs-prop [data-act]");
    if (!b) return;
    var p = b.closest(".rs-prop");
    if (b.getAttribute("data-act") === "no") { p.classList.add("is-no"); return; }
    p.classList.add("is-ok");
    runFlow($$(".rs-flowl li", p), function () {
      var host = p.closest("[data-scn], [data-new], .rs-crit");
      var fn = host && propDone[host.getAttribute("data-scn") || (host.hasAttribute("data-new") ? "new" : "crit")];
      if (fn) fn(p);
    });
  });

  /* ---------- Horloge ---------- */
  var clock = $("[data-clock]");
  function tickClock() { if (clock) clock.textContent = hms(now()); }
  tickClock();

  /* ---------- Modules ---------- */
  var tabs = $$(".rs-tab"), panels = {}, inited = {}, current = "topo";
  $$(".rs-mod").forEach(function (p) { panels[p.getAttribute("data-panel")] = p; });
  var INIT = {}, SHOW = {};
  function openMod(k) {
    if (!panels[k]) return;
    current = k;
    tabs.forEach(function (t) { t.setAttribute("aria-pressed", t.getAttribute("data-mod") === k ? "true" : "false"); });
    for (var m in panels) {
      var on = m === k;
      panels[m].hidden = !on;
      panels[m].classList.toggle("is-in", on);
    }
    if (!inited[k] && INIT[k]) { inited[k] = true; INIT[k](); }
    if (SHOW[k]) SHOW[k]();
  }
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      openMod(t.getAttribute("data-mod"));
      if (t.scrollIntoView && t.parentNode.scrollWidth > t.parentNode.clientWidth) {
        var bar = t.parentNode;
        bar.scrollTo({ left: t.offsetLeft - (bar.clientWidth - t.offsetWidth) / 2, behavior: reduce ? "auto" : "smooth" });
      }
    });
  });
  function setState(k, txt, warn) {
    var e = $('[data-mstate="' + k + '"]');
    if (e) e.textContent = txt;
    var t = $('.rs-tab[data-mod="' + k + '"]');
    if (t && warn !== undefined) t.classList.toggle("is-warn", !!warn);
  }

  /* ---------- Topologie : situations ---------- */
  var wrap = $(".rs-topo-wrap"), scns = {}, sbtn = $$(".rs-sbar button");
  $$(".rs-scn").forEach(function (a) { scns[a.getAttribute("data-scn")] = a; });
  function meta(id, txt) { var e = $('[data-meta="' + id + '"]'); if (e) e.textContent = txt; }
  function setWan(w) {
    S.wan = w;
    setAll("wan", WAN[w]);
    meta("g5", w === "g5" ? "Actif · 31\u00a0ms" : "En veille · 31\u00a0ms");
    setState("continuite", w === "fibre" ? "Fibre · 9 ms" : "5G · secours", w !== "fibre");
  }
  function situation(k) {
    timers.forEach(clearTimeout); timers = [];
    sbtn.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-scn") === k ? "true" : "false"); });
    for (var s in scns) {
      var on = s === k;
      scns[s].hidden = !on;
      scns[s].classList.toggle("is-on", on);
      $$(".rs-prop", scns[s]).forEach(resetProp);
    }
    wrap.setAttribute("data-s", k);
    wrap.classList.remove("is-fixed", "is-back");
    meta("poe", "6 caméras alimentées");
    var c = $('[data-count="cameras"]'); if (c) c.textContent = "6 appareils";
    if (S.wan !== "fibre" && !failing) setWan("fibre");
    S.alerts = k === "normal" ? 0 : 1;
    if (k === "camera") { meta("poe", "Port 7 coupé · 186 W demandés"); if (c) c.textContent = "5 / 6 en ligne"; }
    if (k === "panne") setWan("g5");
    setAll("alerts", String(S.alerts));
  }
  sbtn.forEach(function (b) { b.addEventListener("click", function () { situation(b.getAttribute("data-scn")); }); });
  propDone.camera = function () {
    wrap.classList.add("is-fixed"); meta("poe", "6 caméras · réserve de 12 W");
    var c = $('[data-count="cameras"]'); if (c) c.textContent = "6 appareils";
    setAll("alerts", "0");
  };
  propDone.iot = function () { wrap.classList.add("is-fixed"); setAll("alerts", "0"); };
  propDone.panne = function () { setAll("alerts", "0"); };

  /* ---------- Chiffres en direct (une fois par seconde) ---------- */
  var VB = {};
  $$("[data-band]").forEach(function (b) {
    var n = $(".rs-b-n", b); VB[b.getAttribute("data-band")] = { el: n, base: parseFloat(n.textContent) };
  });
  var cpu = 18;
  function liveTick() {
    S.t++;
    S.down = Math.max(180, Math.min(520, S.down + rnd(-26, 26) + (312 - S.down) * .12));
    S.up = Math.max(18, Math.min(90, S.up + rnd(-5, 5) + (41 - S.up) * .15));
    if (Math.random() < .35) S.blocked += Math.random() < .7 ? 1 : 2;
    cpu = Math.max(9, Math.min(31, cpu + rnd(-2, 2)));
    setAll("down", String(Math.round(S.down)));
    setAll("up", String(Math.round(S.up)));
    setAll("blocked", thousands(S.blocked));
    setAll("pct", String(Math.round(S.down / 10)));
    setAll("lat", S.wan === "fibre" ? String(Math.round(rnd(8, 11))) : String(Math.round(rnd(28, 36))));
    setAll("wan-fibre", S.wan === "fibre" ? "↓ " + Math.round(S.down) + " · ↑ " + Math.round(S.up) + " Mb/s" : "Aucune réponse");
    setAll("wan-g5", S.wan === "g5" ? "↓ " + Math.round(S.down * .8) + " · ↑ " + Math.round(S.up) + " Mb/s" : "−84 dBm · 4 barres");
    setAll("gw", "CPU " + Math.round(cpu) + " % · " + thousands(S.blocked) + " blocages");
    setState("trafic", Math.round(S.down) + " Mb/s");
    setState("menaces", thousands(S.blocked) + " bloquées");
    for (var k in VB) VB[k].el.textContent = fr(VB[k].base * rnd(.82, 1.18) * (S.down / 312), VB[k].base < 30 ? 1 : 0) + " Mb/s";
    if (SHOW_TICK[current]) SHOW_TICK[current]();
  }
  var SHOW_TICK = {};

  /* ---------- Appareils ---------- */
  INIT.appareils = function () {
    var rows = $$(".rs-inv tbody tr"), chips = $$(".rs-chip"), q = $("[data-dev-q]"), vf = "all";
    function apply() {
      var t = (q.value || "").trim().toLowerCase();
      rows.forEach(function (r) {
        r.hidden = !((vf === "all" || r.getAttribute("data-vlan") === vf) && (!t || r.getAttribute("data-q").indexOf(t) >= 0));
      });
    }
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        vf = c.getAttribute("data-vf");
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
        apply();
      });
    });
    q.addEventListener("input", apply);
    propDone["new"] = function () {
      var box = $("[data-new]");
      box.classList.add("is-done");
      $(".rs-kick", box).innerHTML = '<i class="rs-dot is-ok"></i>Appareil accepté · rangé dans le VLAN 30';
      var tb = $(".rs-inv tbody"), tr = document.createElement("tr");
      tr.setAttribute("data-vlan", "objets");
      tr.setAttribute("data-q", "prise connectée 10.0.30.88");
      tr.className = "is-added";
      tr.innerHTML = '<td><span class="rs-dv"><svg class="rs-ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M5.6 1.8v3M10.4 1.8v3M3.6 4.8h8.8v2.6a4.4 4.4 0 0 1-8.8 0z"/><path d="M8 11.8v2.4"/></svg><span><b>Prise connectée · terrasse</b><small>Prise intelligente · nouvelle</small></span></span></td>' +
        '<td><span class="rs-conf" style="--v:91%"><i></i>91 %</span></td><td><span class="rs-vtag z-objets">VLAN 30</span></td>' +
        '<td class="rs-mono">10.0.30.88</td><td class="rs-dim">Wi-Fi 2,4 GHz · Extérieur</td><td class="rs-mono rs-r">&lt; 0,1</td>' +
        '<td><span class="rs-pill is-ok">En ligne</span></td>';
      tb.insertBefore(tr, tb.firstChild);
      rows.unshift(tr);
      setState("appareils", "45 · à jour", false);
    };
  };
  SHOW_TICK.appareils = function () {
    $$("[data-dev-mbps]").forEach(function (td) {
      var b = parseFloat(td.getAttribute("data-dev-mbps"));
      if (b < .1) return;
      td.textContent = fr(b * rnd(.75, 1.25), 1);
    });
  };

  /* ---------- Wi-Fi : carte de chaleur ---------- */
  INIT.wifi = function () {
    var plan = $(".rs-plan"), cv = $(".rs-heat", plan);
    var D = JSON.parse(plan.getAttribute("data-wifi"));
    var M = 20 / 640; // mètres par unité
    function roomOf(x, y) {
      for (var i = 0; i < D.rooms.length; i++) {
        var r = D.rooms[i];
        if (x >= r[1] && x < r[1] + r[3] && y >= r[2] && y < r[2] + r[4]) return i;
      }
      return -1;
    }
    function walls(ax, ay, bx, by) {
      var n = 0;
      D.rooms.forEach(function (r) {
        var ia = ax >= r[1] && ax < r[1] + r[3] && ay >= r[2] && ay < r[2] + r[4];
        var ib = bx >= r[1] && bx < r[1] + r[3] && by >= r[2] && by < r[2] + r[4];
        if (ia !== ib) n++;
      });
      return Math.ceil(n / 2);
    }
    function raw(x, y) {
      var best = -120;
      D.aps.forEach(function (a) {
        var d = Math.max(1, Math.hypot(x - a[0], y - a[1]) * M);
        best = Math.max(best, -36 - 20 * Math.log10(d) - 6 * walls(a[0], a[1], x, y));
      });
      return best;
    }
    var off = D.rooms.map(function (r) { return r[5] - raw(r[1] + r[3] / 2, r[2] + r[4] / 2); });
    function rssi(x, y) { var i = roomOf(x, y); return i < 0 ? null : raw(x, y) + off[i]; }
    var STOPS = [[-44, [45, 226, 160]], [-52, [120, 230, 150]], [-60, [236, 224, 92]], [-67, [255, 170, 60]], [-75, [255, 96, 96]]];
    function col(v) {
      if (v >= STOPS[0][0]) return STOPS[0][1];
      for (var i = 1; i < STOPS.length; i++) {
        if (v >= STOPS[i][0]) {
          var t = (STOPS[i - 1][0] - v) / (STOPS[i - 1][0] - STOPS[i][0]), a = STOPS[i - 1][1], b = STOPS[i][1];
          return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
        }
      }
      return STOPS[STOPS.length - 1][1];
    }
    var gw = 160, gh = 90, small = document.createElement("canvas");
    small.width = gw; small.height = gh;
    var sc = small.getContext("2d"), img = sc.createImageData(gw, gh);
    for (var j = 0; j < gh; j++) {
      for (var i = 0; i < gw; i++) {
        var x = (i + .5) * 4, y = (j + .5) * 4, v = rssi(x, y), k = (j * gw + i) * 4;
        if (v === null) { img.data[k + 3] = 0; continue; }
        var c = col(v);
        img.data[k] = c[0]; img.data[k + 1] = c[1]; img.data[k + 2] = c[2];
        img.data[k + 3] = Math.round(255 * (.66 + Math.max(0, Math.min(1, (v + 80) / 40)) * .18));
      }
    }
    sc.putImageData(img, 0, 0);
    var ctx = cv.getContext("2d");
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
    ctx.drawImage(small, 0, 0, 640, 360);
    D.rooms.forEach(function (r) {
      var t = $('[data-room="' + r[0] + '"]', plan);
      if (t) t.textContent = r[5] + " dBm";
    });
  };

  /* ---------- Trafic : graphique en direct ---------- */
  var hist = { d: [], u: [] };
  for (var h = 0; h < 60; h++) { hist.d.push(312 + Math.sin(h / 5) * 40 + rnd(-30, 30)); hist.u.push(41 + rnd(-8, 8)); }
  var tc, tctx, tW = 0, tH = 0, gold = "#e7c888";
  function sizeChart() {
    if (!tc) return;
    var r = tc.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
    tW = r.width; tH = r.height;
    tc.width = Math.round(tW * dpr); tc.height = Math.round(tH * dpr);
    tctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    gold = getComputedStyle(root).getPropertyValue("--gold-soft").trim() || gold;
  }
  function drawChart() {
    if (!tc || !tW) return;
    var c = tctx, max = 600, padL = 34, padB = 4, w = tW - padL, hgt = tH - padB;
    c.clearRect(0, 0, tW, tH);
    c.font = "500 10px " + (getComputedStyle(root).getPropertyValue("--mono") || "monospace");
    c.textAlign = "right";
    [0, 200, 400, 600].forEach(function (v) {
      var y = hgt - v / max * (hgt - 14);
      c.strokeStyle = "rgba(255,255,255,.06)"; c.lineWidth = 1;
      c.beginPath(); c.moveTo(padL, y + .5); c.lineTo(tW, y + .5); c.stroke();
      c.fillStyle = "rgba(255,255,255,.38)"; c.fillText(String(v), padL - 6, y + 3);
    });
    function line(arr, stroke, fill) {
      var n = arr.length, step = w / (n - 1);
      c.beginPath();
      arr.forEach(function (v, i) {
        var x = padL + i * step, y = hgt - v / max * (hgt - 14);
        if (!i) c.moveTo(x, y); else c.lineTo(x, y);
      });
      if (fill) {
        c.save(); c.lineTo(padL + w, hgt); c.lineTo(padL, hgt); c.closePath();
        var g = c.createLinearGradient(0, 0, 0, hgt);
        g.addColorStop(0, fill); g.addColorStop(1, "rgba(0,0,0,0)");
        c.fillStyle = g; c.globalAlpha = .38; c.fill(); c.restore();
        c.beginPath();
        arr.forEach(function (v, i) { var x = padL + i * step, y = hgt - v / max * (hgt - 14); if (!i) c.moveTo(x, y); else c.lineTo(x, y); });
      }
      c.strokeStyle = stroke; c.lineWidth = 1.6; c.lineJoin = "round"; c.stroke();
      var lx = padL + w, ly = hgt - arr[n - 1] / max * (hgt - 14);
      c.beginPath(); c.arc(lx - 1, ly, 3, 0, 7); c.fillStyle = stroke; c.fill();
    }
    line(hist.d, gold, gold);
    line(hist.u, "rgba(255,255,255,.85)", null);
  }
  var tdev, tapp;
  INIT.trafic = function () {
    tc = $(".rs-tc"); tctx = tc.getContext("2d");
    tdev = $$("[data-tdev]").map(function (li) { var v = $("[data-v]", li); return { li: li, v: v, base: parseFloat(v.textContent.replace(",", ".")) }; });
    tapp = $$("[data-tapp]").map(function (li) { var v = $("[data-v]", li); return { li: li, v: v, base: parseFloat(v.textContent) }; });
    window.addEventListener("resize", function () { if (current === "trafic") { sizeChart(); drawChart(); } });
  };
  function bars(list, dec) {
    var vals = list.map(function (o) { return o.base * rnd(.78, 1.22) * (S.down / 312); });
    var mx = Math.max.apply(null, vals);
    list.forEach(function (o, i) {
      o.v.textContent = fr(vals[i], dec);
      $(".rs-bar i", o.li).style.setProperty("--v", (vals[i] / mx * 100).toFixed(1) + "%");
    });
  }
  SHOW.trafic = function () { sizeChart(); drawChart(); bars(tdev, 1); bars(tapp, 0); };
  SHOW_TICK.trafic = function () { drawChart(); bars(tdev, 1); bars(tapp, 0); };
  function pushHist() {
    hist.d.push(S.down); hist.u.push(S.up);
    if (hist.d.length > 60) { hist.d.shift(); hist.u.shift(); }
  }

  /* ---------- Menaces : carte du monde et arcs ---------- */
  var G, gArcs, gHome, home, evI = 6, feed;
  function proj(lat, lon) {
    var l = ((lon - G.lon0) % 360 + 360) % 360;
    return [l / G.step * G.u + G.u / 2, (G.lat0 - lat) / G.step * G.u + G.u / 2];
  }
  function arcPath(a, b) {
    var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, d = Math.hypot(b[0] - a[0], b[1] - a[1]);
    return "M" + a[0].toFixed(1) + " " + a[1].toFixed(1) + "Q" + mx.toFixed(1) + " " + (my - d * .32).toFixed(1) + " " + b[0].toFixed(1) + " " + b[1].toFixed(1);
  }
  INIT.menaces = function () {
    var box = $(".rs-geo");
    G = JSON.parse(box.getAttribute("data-geo"));
    var d = [], rows = G.rows.split(",");
    rows.forEach(function (r, j) {
      for (var c = 0; c < r.length; c++) {
        var v = parseInt(r[c], 16);
        for (var b = 0; b < 4; b++) if (v & (8 >> b)) {
          var i = c * 4 + b;
          if (i < G.cols) d.push("M" + (i * G.u + G.u / 2) + " " + (j * G.u + G.u / 2) + "h0");
        }
      }
    });
    $(".rs-geo-dots").setAttribute("d", d.join(""));
    gArcs = $(".rs-geo-arcs"); gHome = $(".rs-geo-home"); feed = $(".rs-feed");
    home = proj(G.home[0], G.home[1]);
    // Historique discret : chaque source des dernières heures
    G.ev.forEach(function (e) {
      var s = proj(e[5], e[6]);
      svgEl("path", { "class": "rs-arc is-" + e[7], d: arcPath(s, home), opacity: ".16" }, gArcs);
      svgEl("circle", { "class": "rs-arc-dot is-" + e[7], cx: s[0], cy: s[1], r: 2, opacity: ".5" }, gArcs);
    });
    svgEl("circle", { "class": "rs-home-s", cx: home[0], cy: home[1], r: 6 }, gHome);
    svgEl("circle", { "class": "rs-home-r", cx: home[0], cy: home[1], r: 7 }, gHome);
    svgEl("circle", { "class": "rs-home-c", cx: home[0], cy: home[1], r: 3.2 }, gHome);
    var t = svgEl("text", { "class": "rs-home-l", x: home[0] + 10, y: home[1] - 8 }, gHome);
    t.textContent = "MAISON · SAINT-HYACINTHE";
  };
  function strike() {
    if (!G) return;
    var e = G.ev[evI++ % G.ev.length], s = proj(e[5], e[6]), tone = e[7];
    var p = svgEl("path", { "class": "rs-arc is-" + tone, d: arcPath(s, home) }, gArcs);
    var src = svgEl("circle", { "class": "rs-arc-src is-" + tone, cx: s[0], cy: s[1], r: 3 }, gArcs);
    var lab = svgEl("text", { "class": "rs-arc-lab", x: s[0] + 7, y: s[1] - 6 }, gArcs);
    lab.textContent = e[4].toUpperCase();
    var len = p.getTotalLength();
    if (p.animate && !reduce) {
      p.animate([{ strokeDasharray: "0 " + len }, { strokeDasharray: len + " " + len, offset: .55 }, { strokeDasharray: len + " " + len, opacity: 0 }],
        { duration: 2600, easing: "cubic-bezier(.3,.6,.3,1)", fill: "forwards" });
      src.animate([{ r: 2, opacity: 1 }, { r: 14, opacity: 0 }], { duration: 1400, easing: "ease-out", fill: "forwards" });
      lab.animate([{ opacity: 0 }, { opacity: 1, offset: .15 }, { opacity: 1, offset: .7 }, { opacity: 0 }], { duration: 2600, fill: "forwards" });
      var ring = $(".rs-home-s", gHome);
      setTimeout(function () {
        if (ring.animate) ring.animate([{ r: 6, opacity: .9 }, { r: 26, opacity: 0 }], { duration: 1100, easing: "ease-out" });
      }, 1300);
    }
    setTimeout(function () { [p, src, lab].forEach(function (n) { if (n.parentNode) n.parentNode.removeChild(n); }); }, 2800);
    // Journal
    var li = document.createElement("li");
    li.className = "is-" + tone + " is-new";
    li.innerHTML = "<time>" + hms(now()) + "</time><span><b></b><small></small><em></em></span><span class=\"rs-pill is-ok\">Bloqué</span>";
    li.querySelector("b").textContent = e[1];
    li.querySelector("small").textContent = e[2];
    li.querySelector("em").textContent = e[3] + " · " + e[4];
    feed.insertBefore(li, feed.firstChild);
    while (feed.children.length > 6) feed.removeChild(feed.lastChild);
    S.blocked += 1;
  }
  SHOW.menaces = function () { strike(); };
  var strikeEvery = 0;
  SHOW_TICK.menaces = function () { if (++strikeEvery % 3 === 0) strike(); };

  /* ---------- VPN : durées des sessions ---------- */
  var since = $$("[data-since]").map(function (e) { return { e: e, s: +e.getAttribute("data-since") }; });
  function dur(s) { var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60); return h ? h + " h " + pad(m) : m + " min " + pad(s % 60); }
  function tickSince() { since.forEach(function (o) { o.s++; o.e.textContent = dur(o.s); }); }
  tickSince();

  /* ---------- Contrôles ---------- */
  $$("[data-pause]").forEach(function (b) {
    b.addEventListener("click", function () {
      var on = b.getAttribute("aria-checked") !== "true";
      b.setAttribute("aria-checked", on ? "true" : "false");
      $("span", b).textContent = on ? "Internet en pause" : "Mettre Internet en pause";
      b.closest(".rs-prof").classList.toggle("is-paused", on);
    });
  });
  var gsw = $("[data-guest]");
  if (gsw) gsw.addEventListener("click", function () {
    var on = gsw.getAttribute("aria-checked") !== "true";
    gsw.setAttribute("aria-checked", on ? "true" : "false");
    $(".rs-guest").classList.toggle("is-off", !on);
    $("[data-gcount]").textContent = on ? "3 appareils" : "Réseau coupé";
    $$("[data-gk]").forEach(function (e) { e.textContent = on ? "3" : "0"; });
  });
  var WORDS = ["soleil", "érable", "rivière", "aurore", "galet", "boréal", "cèdre", "orage", "lynx", "nordet"];
  var gnew = $("[data-gnew]");
  if (gnew) gnew.addEventListener("click", function () {
    var a = WORDS[Math.floor(Math.random() * WORDS.length)], b = WORDS[Math.floor(Math.random() * WORDS.length)];
    if (a === b) b = "lac";
    $("[data-gpass]").textContent = a + "-" + b + "-" + Math.floor(rnd(10, 99));
  });

  /* ---------- Continuité ---------- */
  var spark = {};
  $$("[data-wan]").forEach(function (w) {
    var k = w.getAttribute("data-wan"), base = k === "fibre" ? 9 : k === "g5" ? 31 : 38, arr = [];
    for (var i = 0; i < 40; i++) arr.push(base + rnd(-1.5, 1.5) * (base / 9));
    spark[k] = { el: w, base: base, arr: arr, l: $(".rs-spark-l", w), a: $(".rs-spark-a", w), t: $("[data-lat]", w) };
  });
  function drawSpark(o) {
    var mx = 60, n = o.arr.length, pts = o.arr.map(function (v, i) {
      return (i / (n - 1) * 200).toFixed(1) + " " + (38 - Math.min(v, mx) / mx * 34).toFixed(1);
    });
    o.l.setAttribute("d", "M" + pts.join("L"));
    o.a.setAttribute("d", "M" + pts.join("L") + "L200 40L0 40Z");
  }
  function tickSpark() {
    for (var k in spark) {
      var o = spark[k], down = o.el.classList.contains("is-down");
      o.arr.push(down ? 60 : o.base + rnd(-1.5, 1.5) * (o.base / 9));
      o.arr.shift();
      o.t.textContent = down ? "—" : Math.round(o.arr[o.arr.length - 1]) + " ms";
      drawSpark(o);
    }
  }
  for (var sk in spark) drawSpark(spark[sk]);
  var failing = false, fbtn = $("[data-failover]");
  function pillTo(w, txt, tone) {
    var p = $(".rs-wan-h .rs-pill", w);
    p.className = "rs-pill" + (tone ? " is-" + tone : ""); p.textContent = txt;
  }
  if (fbtn) fbtn.addEventListener("click", function () {
    if (failing) return;
    failing = true; fbtn.disabled = true;
    var card = $(".rs-c-tl"), items = $$(".rs-tl li", card), f = spark.fibre.el, g = spark.g5.el;
    card.classList.add("is-sim");
    $(".rs-ch h5", card).textContent = "Simulation en cours";
    items.forEach(function (li) { li.classList.remove("is-done"); });
    var t0 = now();
    function stamp(i, ms) { var d = new Date(t0.getTime() + ms); $("time", items[i]).textContent = hms(d) + "." + Math.floor(ms % 1000 / 100); }
    var seq = [
      [0, function () { f.classList.add("is-down"); f.classList.remove("is-on"); pillTo(f, "Coupée", "bad"); }],
      [1400, function () {}],
      [2100, function () { g.classList.add("is-on"); pillTo(g, "Actif", "ok"); setWan("g5"); }],
      [3000, function () {}],
      [9000, function () { f.classList.remove("is-down"); f.classList.add("is-on"); g.classList.remove("is-on"); pillTo(f, "Actif", "ok"); pillTo(g, "En veille", ""); setWan("fibre"); }],
    ];
    seq.forEach(function (s, i) {
      stamp(i, s[0]);
      setTimeout(function () {
        s[1](); items[i].classList.add("is-done");
        if (i === seq.length - 1) {
          failing = false; fbtn.disabled = false;
          $(".rs-ch h5", card).textContent = "Simulation · terminée";
        }
      }, reduce ? i * 300 : s[0] + 400);
    });
  });

  /* ---------- Sauvegardes : test de restauration ---------- */
  var rbtn = $("[data-restore]");
  if (rbtn) rbtn.addEventListener("click", function () {
    var box = rbtn.closest(".rs-restore");
    box.classList.add("is-run");
    runFlow($$(".rs-flowl li", box), function () {
      $(".rs-kick", box).innerHTML = '<i class="rs-dot is-ok"></i>Test de restauration · aujourd’hui ' + hms(now()).slice(0, 5);
    }, 1100);
  });

  /* ---------- Mises à jour ---------- */
  propDone.crit = function () {
    var box = $(".rs-crit");
    box.classList.add("is-done");
    $(".rs-kick", box).innerHTML = '<i class="rs-dot is-ok"></i>Correctif approuvé · installation cette nuit à 3 h 00';
    var st = $('.rs-table tr.is-crit [data-pstate]');
    if (st) st.innerHTML = '<span class="rs-pill is-gold">Approuvée · cette nuit 3 h</span>';
    $$("[data-crit]").forEach(function (e) { e.textContent = "0"; });
    setState("maj", "Planifiées · 3 h", false);
  };

  /* ---------- Segmentation ---------- */
  var segBtns = $$(".rs-matrix button"), sd = $(".rs-segd");
  var VLAB = { ok: "Permis", lim: "Limité", vpn: "VPN seulement", no: "Bloqué" };
  function pickSeg(b) {
    segBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    $("[data-sd-t]", sd).textContent = b.getAttribute("data-seg");
    var v = $("[data-sd-v]", sd), k = b.getAttribute("data-v");
    v.className = "rs-segd-v is-" + k; v.textContent = VLAB[k];
    $("[data-sd-w]", sd).textContent = b.getAttribute("data-why");
    var h = +b.getAttribute("data-hits");
    $("[data-sd-h]", sd).textContent = h ? thousands(h) + " tentatives bloquées · 24 h" : "Aucune tentative refusée · 24 h";
  }
  segBtns.forEach(function (b) {
    b.setAttribute("aria-pressed", "false");
    b.addEventListener("click", function () { pickSeg(b); });
  });
  var first = segBtns.filter(function (b) { return b.getAttribute("data-seg").indexOf("Objets → Personnel") === 0; })[0];
  if (first) pickSeg(first);

  /* ---------- Boucle (une seconde) ---------- */
  setInterval(function () {
    if (!visible || document.hidden) return;
    tickClock();
    pushHist();
    liveTick();
    tickSince();
    if (current === "continuite") tickSpark();
  }, 1000);

  situation("normal");
})();
