/* Démo « Réseau et cybersécurité » : carte vivante du réseau (données simulées).
   Les paquets circulent en continu; trois situations se jouent sur demande.
   Rien n'est appliqué sans « Approuver » : envoyé, état relu, puis confirmé.
   Sans JavaScript, le HTML montre l'état normal (voir src/demos/reseau.py). */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="reseau"]');
  if (!root || !window.SVGElement || !root.querySelector(".rz-svg")) return;
  var NS = "http://www.w3.org/2000/svg";
  var svg = root.querySelector(".rz-svg");
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var tallMQ = window.matchMedia ? matchMedia("(max-width: 640px)") : null;
  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }
  function reflow(el) { return el.getBoundingClientRect(); }
  function restart(el, cls) { el.classList.remove(cls); reflow(el); el.classList.add(cls); }
  root.classList.add("is-live");

  var layer = $(".rz-pk", svg), trace = $(".rz-trace", svg), call = $(".rz-call", svg),
      cut = $(".rz-cut", svg), blocked = $(".rz-blocked", svg), tip = $(".rz-tip"), wrap = $(".rz-wrap"),
      card = $(".rz-card"), jump = $(".rz-jump"), replay = $(".rz-replay");

  /* ---------- Inventaire tiré du HTML ---------- */
  var nodes = {}, firstState = {}, devs = {}, devIds = [];
  $$(".rz-n", svg).forEach(function (n) {
    var id = n.getAttribute("data-id");
    nodes[id] = n; firstState[id] = n.getAttribute("data-state");
    if (n.classList.contains("rz-dev")) {
      devs[id] = { id: id, zone: n.getAttribute("data-zone"), kind: n.getAttribute("data-kind"),
                   w: +n.getAttribute("data-w8"), acc: Math.random() };
      devIds.push(id);
    }
  });
  var linkEls = {};
  $$("[data-link]", svg).forEach(function (p) { linkEls[p.getAttribute("data-link")] = p; });
  var visLinks = $$(".rz-link", svg), buses = $$(".rz-bus", svg);
  var gates = {}, zones = {};
  $$(".rz-gate", svg).forEach(function (g) { gates[g.getAttribute("data-zone")] = g; });
  $$(".rz-zone", svg).forEach(function (g) { zones[g.getAttribute("data-zone")] = g; });
  var arts = {};
  $$(".rz-scn").forEach(function (a) { arts[a.getAttribute("data-scn")] = a; });
  var btns = $$(".rz-bar button");

  /* ---------- Géométrie : disposition large (w) ou haute (t) ---------- */
  var layout = "", geo = {}, routes = {};
  function setGeo(el, v) {
    var tag = el.tagName.toLowerCase();
    if (tag === "path") { el.setAttribute("d", v); return; }
    var p = v.split(",");
    if (tag === "rect") {
      el.setAttribute("x", p[0]); el.setAttribute("y", p[1]);
      el.setAttribute("width", p[2]); el.setAttribute("height", p[3]);
      return;
    }
    el.setAttribute("transform", "translate(" + p[0] + " " + p[1] + ")");
    if (p[2]) el.style.textAnchor = p[2];
  }
  function sample(path) {
    var len = path.getTotalLength(), n = Math.max(2, Math.ceil(len / 5)), pts = [], cum = [0], i, q;
    for (i = 0; i <= n; i++) { q = path.getPointAtLength(len * i / n); pts.push(q.x, q.y); }
    for (i = 1; i <= n; i++) cum.push(cum[i - 1] + Math.hypot(pts[2 * i] - pts[2 * i - 2], pts[2 * i + 1] - pts[2 * i - 1]));
    return { pts: pts, cum: cum, len: cum[n] };
  }
  function seg(id, rev) {
    var pts = geo[id].pts;
    if (!rev) return pts.slice();
    var r = [];
    for (var i = pts.length - 2; i >= 0; i -= 2) r.push(pts[i], pts[i + 1]);
    return r;
  }
  function build(list) {
    var pts = [];
    list.forEach(function (s) { var p = seg(s[0], s[1]); pts = pts.concat(pts.length ? p.slice(2) : p); });
    var cum = [0];
    for (var i = 2; i < pts.length; i += 2) cum.push(cum[cum.length - 1] + Math.hypot(pts[i] - pts[i - 2], pts[i + 1] - pts[i - 1]));
    return { pts: pts, cum: cum, len: cum[cum.length - 1] };
  }
  function routeFor(d, up) {
    var key = d.id + (up ? "^" : "v") + state.wan;
    if (routes[key]) return routes[key];
    var list = d.kind === "net"
      ? [["internet>" + state.wan, false], [state.wan + ">routeur", false], ["routeur>switch", false],
         ["switch>gate:" + d.zone, false], ["gate:" + d.zone + ">" + d.id, false]]
      : [["switch>jarvis", true], ["switch>gate:" + d.zone, false], ["gate:" + d.zone + ">" + d.id, false]];
    if (up) list = list.slice().reverse().map(function (s) { return [s[0], !s[1]]; });
    return (routes[key] = build(list));
  }
  function applyLayout() {
    var key = tallMQ && tallMQ.matches ? "t" : "w";
    if (key === layout) return;
    layout = key;
    svg.setAttribute("viewBox", svg.getAttribute("data-v" + key));
    svg.classList.toggle("is-tall", key === "t");
    $$("[data-gw]", svg).forEach(function (el) { setGeo(el, el.getAttribute("data-g" + key)); });
    geo = {}; routes = {};
    Object.keys(linkEls).forEach(function (id) { geo[id] = sample(linkEls[id]); });
    var g = geo["internet>fibre"], m = Math.floor(g.pts.length / 4) * 2;
    cut.setAttribute("transform", "translate(" + g.pts[m].toFixed(1) + " " + g.pts[m + 1].toFixed(1) + ")");
    clearPackets();
    hideTip();
    if (!state) return;
    if (traceSegs) drawTrace(traceSegs, false);
    prefill();
    if (state.inflight) { state.inflight = false; attempt(arts.iot, false); }
  }

  /* ---------- Paquets lumineux ---------- */
  var packets = [], pool = [];
  function pkEl(cls) {
    var g = pool.pop();
    if (!g) {
      g = document.createElementNS(NS, "g");
      var h = document.createElementNS(NS, "circle"), c = document.createElementNS(NS, "circle");
      h.setAttribute("class", "h"); c.setAttribute("class", "c");
      g.appendChild(h); g.appendChild(c); layer.appendChild(g);
    }
    g.firstChild.setAttribute("r", "7.5"); g.lastChild.setAttribute("r", "2.4");
    g.setAttribute("class", cls); g.style.display = ""; g.style.opacity = "0";
    return g;
  }
  function launch(r, cls, v, opts) {
    var p = { r: r, s: 0, i: 0, v: v, el: pkEl(cls), fade: 1, dying: false };
    if (opts) for (var k in opts) p[k] = opts[k];
    if (p.big) { p.el.firstChild.setAttribute("r", "11"); p.el.lastChild.setAttribute("r", "3.8"); }
    packets.push(p);
    place(p);
    return p;
  }
  function recycle(p) { p.el.style.display = "none"; pool.push(p.el); }
  function clearPackets() { packets.forEach(recycle); packets = []; }
  function kill(test) { packets.forEach(function (p) { if (test(p)) p.dying = true; }); }
  function place(p) {
    var cum = p.r.cum, pts = p.r.pts, last = cum.length - 1;
    while (p.i < last - 1 && cum[p.i + 1] < p.s) p.i++;
    var a = cum[p.i], b = cum[Math.min(p.i + 1, last)], k = b > a ? Math.min(1, (p.s - a) / (b - a)) : 0, j = 2 * p.i;
    var x = pts[j] + ((pts[j + 2] !== undefined ? pts[j + 2] : pts[j]) - pts[j]) * k;
    var y = pts[j + 1] + ((pts[j + 3] !== undefined ? pts[j + 3] : pts[j + 1]) - pts[j + 1]) * k;
    p.el.setAttribute("transform", "translate(" + x.toFixed(1) + " " + y.toFixed(1) + ")");
    var o = Math.min(1, p.s / 14, p.noEndFade ? 1 : (p.r.len - p.s) / 14);
    p.el.style.opacity = (Math.max(0, o) * p.fade).toFixed(2);
  }
  function move(dt) {
    var keep = [];
    for (var n = 0; n < packets.length; n++) {
      var p = packets[n];
      if (p.dying) { p.fade -= dt * 3; if (p.fade <= 0) { recycle(p); continue; } }
      else p.s += p.v * dt;
      if (p.s >= p.r.len) {
        p.s = p.r.len; place(p);
        var cb = p.onEnd; p.onEnd = null;
        if (cb) cb(p);
        recycle(p); continue;
      }
      place(p); keep.push(p);
    }
    packets = keep;
  }
  function canSpawn(d) {
    if (state.down[d.id]) return false;
    if (d.kind === "net" && !state.wan) return false;
    return true;
  }
  function spawnTick(dt) {
    for (var n = 0; n < devIds.length; n++) {
      var d = devs[devIds[n]];
      if (!canSpawn(d)) continue;
      d.acc += d.w * 1.35 * dt;
      while (d.acc >= 1) {
        d.acc -= 1;
        var up = d.zone === "cameras" ? Math.random() < .85 : d.kind === "net" ? Math.random() < .3 : Math.random() < .5;
        launch(routeFor(d, up), "z-" + d.zone, 115 + Math.random() * 75, { dev: d.id, net: d.kind === "net" });
      }
    }
  }
  function prefill() {
    if (reduce) return;
    for (var k = 0; k < 36; k++) { spawnTick(.1); move(.1); }
  }

  /* Épaisseur des liens : proportionnelle au trafic qui y passe */
  function widths() {
    var load = {};
    function add(id, w) { load[id] = (load[id] || 0) + w; }
    devIds.forEach(function (id) {
      var d = devs[id];
      if (!canSpawn(d)) return;
      add("switch>gate:" + d.zone, d.w);
      if (d.kind === "net") {
        add("routeur>switch", d.w); add(state.wan + ">routeur", d.w); add("internet>" + state.wan, d.w);
      } else add("switch>jarvis", d.w);
    });
    function px(v) { return (1.5 + 4.4 * Math.sqrt(v / 4)).toFixed(2); }
    visLinks.forEach(function (el) { el.style.strokeWidth = px(load[el.getAttribute("data-link")] || 0); });
    buses.forEach(function (el) {
      var v = 0;
      el.getAttribute("data-devs").split(" ").forEach(function (id) { if (canSpawn(devs[id])) v += devs[id].w; });
      el.style.strokeWidth = px(v);
    });
  }

  /* ---------- Horloge commune (s'arrête hors écran) ---------- */
  var clock = 0, events = [], running = false, raf = 0, last = 0, visible = false;
  function later(sec, fn) { events.push({ t: clock + sec, fn: fn }); }
  function tick(now) {
    raf = 0;
    var dt = Math.min(.05, Math.max(0, (now - last) / 1000));
    last = now; clock += dt;
    if (events.length) {
      var due = [], rest = [];
      events.forEach(function (e) { (e.t <= clock ? due : rest).push(e); });
      if (due.length) {
        events = rest;
        due.sort(function (a, b) { return a.t - b.t; }).forEach(function (e) { e.fn(); });
      }
    }
    if (!reduce) { spawnTick(dt); move(dt); }
    if (running) raf = requestAnimationFrame(tick);
  }
  function sync() {
    var go = visible && !document.hidden;
    if (go && !running) { running = true; last = performance.now(); raf = requestAnimationFrame(tick); }
    else if (!go && running) { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }
  }

  /* ---------- États visibles ---------- */
  var NODE_CLS = ["is-down", "is-boot", "is-back", "is-warn", "is-iso", "is-hit", "is-standby", "is-active", "is-local"];
  var tipFor = null, tipTimer = 0;
  function setNode(id, cls, label) {
    var n = nodes[id];
    NODE_CLS.forEach(function (c) { n.classList.remove(c); });
    if (cls) cls.split(" ").forEach(function (c) { n.classList.add(c); });
    if (label) n.setAttribute("data-state", label);
    var dev = n.classList.contains("rz-dev");
    n.setAttribute("aria-label", n.getAttribute("data-name") + ", " +
      (dev ? "zone " + n.getAttribute("data-zname") + ", " : "") + n.getAttribute("data-state").toLowerCase());
    if (tipFor === n) fillTip(n);
  }
  function setSub(id, text) { var s = $(".rz-sub", nodes[id]); if (s) s.textContent = text; }
  var hud = { net: $('[data-hud="net"]'), dev: $('[data-hud="dev"]'), alert: $('[data-hud="alert"]') };
  function setHud(key, text, cls) {
    var el = hud[key], span = $("dd span", el);
    if (span.textContent !== text) { span.textContent = text; restart(span, "is-flash"); }
    el.classList.remove("is-bad", "is-warn");
    if (cls) el.classList.add(cls);
  }
  function refreshHud() {
    var down = Object.keys(state.down).length;
    setHud("dev", (devIds.length - down) + " / " + devIds.length, down ? "is-bad" : "");
    setHud("alert", String(state.alerts), state.alerts ? "is-bad" : "");
    if (state.wan === "fibre") setHud("net", "Fibre · 9 ms", "");
    else if (state.wan === "starlink") setHud("net", "Starlink · 38 ms", "is-warn");
    else setHud("net", "Coupure", "is-bad");
  }
  function callText(ok) {
    var k = $(".rz-call-k", call), v = $(".rz-call-v", call);
    if (!call.hasAttribute("data-k1")) { call.setAttribute("data-k1", k.textContent); call.setAttribute("data-v1", v.textContent); }
    k.textContent = call.getAttribute(ok ? "data-k2" : "data-k1");
    v.textContent = call.getAttribute(ok ? "data-v2" : "data-v1");
    call.classList.toggle("is-ok", ok);
  }

  /* Tracé du chemin de dépendance (de l'appareil vers sa cause) */
  var traceSegs = null;
  function drawTrace(segs, animate) {
    traceSegs = segs;
    var r = build(segs), d = "M" + r.pts[0].toFixed(1) + " " + r.pts[1].toFixed(1);
    for (var i = 2; i < r.pts.length; i += 2) d += "L" + r.pts[i].toFixed(1) + " " + r.pts[i + 1].toFixed(1);
    trace.setAttribute("d", d);
    trace.classList.remove("is-off"); trace.classList.add("is-on");
    trace.style.transition = "none";
    trace.style.strokeDasharray = r.len.toFixed(1);
    if (animate && !reduce) {
      trace.style.strokeDashoffset = r.len.toFixed(1);
      reflow(trace);
      trace.style.transition = "stroke-dashoffset 1.4s linear";
      trace.style.strokeDashoffset = "0";
      launch(r, "is-head", r.len / 1.4, { scripted: true, big: true, noEndFade: true });
    } else trace.style.strokeDashoffset = "0";
  }
  function hideTrace() { traceSegs = null; trace.style.transition = "none"; trace.classList.remove("is-on", "is-off"); }
  function fadeTrace() { traceSegs = null; trace.style.transition = "opacity 1.2s"; trace.classList.remove("is-on"); trace.classList.add("is-off"); }

  /* ---------- Panneau de JARVIS ---------- */
  function stepCls(a, i, cls) { var li = $$(".rz-steps li", a)[i]; if (li) li.className = cls; }
  function flow(prop, k, cls) { var li = $('.rz-flow li[data-k="' + k + '"]', prop); if (li) li.className = cls; }
  var cardIn = $(".rz-card-in");
  function toEnd() {
    if (cardIn.scrollHeight > cardIn.clientHeight + 4 && getComputedStyle(cardIn).overflowY === "auto") {
      cardIn.scrollTo({ top: cardIn.scrollHeight, behavior: reduce ? "auto" : "smooth" });
    }
  }
  function ask(a) { a.classList.add("is-ask"); $(".rz-prop", a).classList.add("is-wait"); jumpCheck(); toEnd(); }
  function resetArt(a) {
    a.classList.remove("is-cause", "is-ask", "is-starlink", "is-fibre");
    $$(".rz-steps li", a).forEach(function (li) { li.className = ""; });
    var p = $(".rz-prop", a);
    if (p) { p.className = "rz-prop"; $$(".rz-flow li", p).forEach(function (li) { li.className = ""; }); }
  }

  /* ---------- Situations ---------- */
  var state = null;
  function baseline() {
    events = [];
    state = { scn: "normal", wan: "fibre", down: {}, alerts: 0, iso: false, inflight: false };
    Object.keys(nodes).forEach(function (id) { setNode(id, "", firstState[id]); });
    setNode("starlink", "is-standby", firstState.starlink);
    setSub("starlink", "secours"); setSub("fibre", "9 ms");
    ["internet>fibre", "fibre>routeur"].forEach(function (id) { linkEls[id].classList.remove("is-down"); });
    ["internet>starlink", "starlink>routeur"].forEach(function (id) { linkEls[id].classList.add("is-standby"); });
    cut.classList.remove("is-on"); call.classList.remove("is-on"); blocked.classList.remove("is-on");
    callText(false);
    svg.classList.remove("is-offline");
    Object.keys(gates).forEach(function (z) { gates[z].classList.remove("is-block"); });
    Object.keys(zones).forEach(function (z) { zones[z].classList.remove("is-hit"); });
    hideTrace();
    kill(function (p) { return p.scripted; });
  }

  function scnCamera(a) {
    state.down.camg = true; state.alerts = 1;
    setNode("camg", "is-down", "Hors ligne depuis 17 h 42");
    kill(function (p) { return p.dev === "camg"; });
    stepCls(a, 0, "is-run");
    later(.9, function () {
      stepCls(a, 0, "is-done"); stepCls(a, 1, "is-run");
      drawTrace([["gate:cameras>camg", true], ["switch>gate:cameras", true]], true);
    });
    later(1.25, function () { restart(gates.cameras, "is-block"); });
    later(2.3, function () {
      stepCls(a, 1, "is-done"); stepCls(a, 2, "is-run");
      setNode("switch", "is-hit"); call.classList.add("is-on");
    });
    later(3.1, function () { stepCls(a, 2, "is-done is-cause"); a.classList.add("is-cause"); });
    later(3.7, function () { ask(a); });
  }

  function scnIot(a) {
    setNode("bulb", "is-warn", "Comportement inhabituel");
    attempt(a, true);
  }
  function attempt(a, first) {
    if (state.scn !== "iot" || state.iso) return;
    var hit = function () { state.inflight = false; blockHit(a, first); };
    if (reduce) { later(1.2, hit); return; }
    state.inflight = true;
    var r = build([["gate:objets>bulb", true], ["switch>gate:objets", true], ["switch>gate:famille", false]]);
    launch(r, "is-bad", first ? 190 : 210, { scripted: true, big: true, noEndFade: true, onEnd: hit });
  }
  function blockHit(a, first) {
    if (state.scn !== "iot") return;
    gates.famille.classList.remove("is-block"); reflow(gates.famille); gates.famille.classList.add("is-block");
    restart(zones.famille, "is-hit");
    blocked.classList.add("is-on");
    sparks(gates.famille);
    later(1.8, function () { blocked.classList.remove("is-on"); });
    if (first) {
      state.alerts = 1; refreshHud();
      later(.4, function () { a.classList.add("is-cause"); });
      later(1.3, function () { ask(a); });
    }
    later(3.6, function () { attempt(a, false); });
  }

  /* Éclats du paquet arrêté par le mur */
  function sparks(g) {
    if (reduce) return;
    var m = /translate\(([-\d.]+)[ ,]([-\d.]+)/.exec(g.getAttribute("transform") || "");
    if (!m) return;
    var x = +m[1], y = +m[2];
    for (var k = 0; k < 7; k++) {
      var ang = Math.PI * (.55 + k / 6 * .9) + (Math.random() - .5) * .3, d = 22 + Math.random() * 14;
      var x2 = x + Math.cos(ang) * d, y2 = y + Math.sin(ang) * d;
      var p = launch({ pts: [x, y, x2, y2], cum: [0, d], len: d }, "is-spark", d / (.45 + Math.random() * .25), { scripted: true });
      p.el.firstChild.setAttribute("r", "4"); p.el.lastChild.setAttribute("r", "1.5");
    }
  }

  function scnInternet(a) {
    state.wan = ""; state.alerts = 1;
    ["internet>fibre", "fibre>routeur"].forEach(function (id) { linkEls[id].classList.add("is-down"); });
    cut.classList.add("is-on");
    setNode("fibre", "is-down", "Coupée depuis 18 h 03"); setSub("fibre", "coupée");
    svg.classList.add("is-offline");
    setNode("jarvis", "is-local", "Actif · la maison continue en local");
    kill(function (p) { return p.net; });
    stepCls(a, 0, "is-run");
    later(.5, function () { stepCls(a, 0, "is-done"); stepCls(a, 1, "is-run"); });
    later(1.5, function () { stepCls(a, 1, "is-done"); stepCls(a, 2, "is-run"); });
    later(3, function () {
      state.wan = "starlink";
      ["internet>starlink", "starlink>routeur"].forEach(function (id) {
        linkEls[id].classList.remove("is-standby"); restart(linkEls[id], "is-wake");
      });
      setNode("starlink", "is-active", "Active · 38 ms"); setSub("starlink", "38 ms");
      svg.classList.remove("is-offline");
      setNode("jarvis", "", firstState.jarvis);
      stepCls(a, 2, "is-done"); a.classList.add("is-starlink");
      refreshHud(); widths();
    });
    later(3.7, function () { ask(a); });
  }
  function fibreBack(a) {
    if (state.scn !== "internet" || state.wan !== "starlink") return;
    state.wan = "fibre"; state.alerts = 0;
    ["internet>fibre", "fibre>routeur"].forEach(function (id) {
      linkEls[id].classList.remove("is-down"); restart(linkEls[id], "is-wake");
    });
    ["internet>starlink", "starlink>routeur"].forEach(function (id) { linkEls[id].classList.add("is-standby"); });
    cut.classList.remove("is-on");
    setNode("fibre", "is-back", firstState.fibre); setSub("fibre", "9 ms");
    setNode("starlink", "is-standby", firstState.starlink); setSub("starlink", "secours");
    a.classList.add("is-fibre");
    refreshHud(); widths();
  }

  /* Accord donné : envoyé, relecture de l'état, puis confirmé */
  var approvals = {
    camera: function (a, prop) {
      setNode("camg", "is-boot", "Redémarrage du port 7…");
      later(2.4, function () {
        flow(prop, "read", "is-on is-done"); flow(prop, "ok", "is-on is-done"); prop.classList.add("is-done"); toEnd();
        delete state.down.camg; state.alerts = 0;
        setNode("camg", "is-back", "En ligne · image reçue à 17 h 46");
        setNode("switch", "", firstState["switch"]);
        callText(true); fadeTrace(); refreshHud(); widths();
        later(3, function () { call.classList.remove("is-on"); });
      });
    },
    iot: function (a, prop) {
      later(1.8, function () {
        flow(prop, "read", "is-on is-done"); flow(prop, "ok", "is-on is-done"); prop.classList.add("is-done"); toEnd();
        state.iso = true; state.alerts = 0;
        setNode("bulb", "is-iso", "Isolées · répondent seulement à JARVIS");
        refreshHud();
      });
    },
    internet: function (a, prop) {
      later(1.6, function () {
        flow(prop, "read", "is-on is-done"); flow(prop, "ok", "is-on is-done"); prop.classList.add("is-done"); toEnd();
      });
    }
  };

  function play(name) {
    baseline();
    state.scn = name;
    btns.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-scn") === name ? "true" : "false"); });
    Object.keys(arts).forEach(function (k) {
      var a = arts[k];
      resetArt(a);
      a.hidden = k !== name;
      a.classList.remove("is-on");
    });
    reflow(arts[name]);
    arts[name].classList.add("is-on");
    replay.hidden = name === "normal";
    cardIn.scrollTop = 0;
    if (name === "camera") scnCamera(arts[name]);
    else if (name === "iot") scnIot(arts[name]);
    else if (name === "internet") scnInternet(arts[name]);
    refreshHud(); widths(); jumpCheck();
  }

  root.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-act], .rz-bar button") : null;
    if (!b || !root.contains(b)) return;
    if (b.hasAttribute("data-scn")) { root.classList.remove("is-invite"); play(b.getAttribute("data-scn")); return; }
    var act = b.getAttribute("data-act"), a = b.closest(".rz-scn"), prop = b.closest(".rz-prop");
    if (act === "ok" && prop && !prop.classList.contains("is-sent")) {
      prop.classList.remove("is-wait"); prop.classList.add("is-sent");
      flow(prop, "sent", "is-on is-done"); flow(prop, "read", "is-on is-run");
      approvals[state.scn](a, prop);
      toEnd();
    } else if (act === "no" && prop) {
      prop.classList.remove("is-wait"); prop.classList.add("is-later");
    } else if (act === "fibre") fibreBack(a);
    else if (act === "replay") play(state.scn);
    else if (act === "jump") card.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  });

  /* ---------- Infobulle des appareils ---------- */
  function fillTip(n) {
    $("b", tip).textContent = n.getAttribute("data-name");
    $(".rz-tz", tip).textContent = n.classList.contains("rz-dev") ? "Zone " + n.getAttribute("data-zname") : "Infrastructure";
    var st = $(".rz-ts", tip);
    st.textContent = n.getAttribute("data-state");
    st.className = "rz-ts" + (n.classList.contains("is-down") ? " is-bad"
      : (n.classList.contains("is-boot") || n.classList.contains("is-warn") || n.classList.contains("is-standby") || n.classList.contains("is-iso")) ? " is-warn" : "");
    $(".rz-ti", tip).textContent = n.getAttribute("data-info");
  }
  function showTip(n) {
    tipFor = n; fillTip(n); tip.hidden = false;
    var r = $(".rz-disc", n).getBoundingClientRect(), w = wrap.getBoundingClientRect();
    var tw = tip.offsetWidth, th = tip.offsetHeight;
    var x = r.left + r.width / 2 - w.left - tw / 2, y = r.top - w.top - th - 10;
    if (y < -40) y = r.bottom - w.top + 10;
    x = Math.max(4, Math.min(w.width - tw - 4, x));
    tip.style.transform = "translate(" + Math.round(x) + "px," + Math.round(y) + "px)";
    tip.classList.add("is-on");
  }
  function hideTip() { tipFor = null; tip.classList.remove("is-on"); }
  Object.keys(nodes).forEach(function (id) {
    var n = nodes[id];
    n.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") showTip(n); });
    n.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") hideTip(); });
    n.addEventListener("focus", function () { showTip(n); });
    n.addEventListener("blur", hideTip);
    n.addEventListener("click", function () {
      showTip(n); clearTimeout(tipTimer); tipTimer = setTimeout(function () { if (tipFor === n) hideTip(); }, 3500);
    });
  });

  /* ---------- Raccourci vers le panneau (téléphone) ---------- */
  var cardSeen = true;
  function jumpCheck() {
    if (!jump) return;
    var single = card.offsetTop > wrap.offsetTop + 40;
    jump.hidden = !(single && state && state.scn !== "normal" && !cardSeen);
  }

  /* ---------- Démarrage ---------- */
  applyLayout();
  baseline();
  prefill();
  widths(); refreshHud();
  if (tallMQ) {
    var onMQ = function () { applyLayout(); widths(); jumpCheck(); };
    if (tallMQ.addEventListener) tallMQ.addEventListener("change", onMQ); else if (tallMQ.addListener) tallMQ.addListener(onMQ);
  }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { visible = e.isIntersecting; });
      sync();
      if (visible && !root.classList.contains("was-seen")) { root.classList.add("was-seen", "is-invite"); }
    }, { threshold: 0.04 }).observe(root);
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { cardSeen = e.isIntersecting; });
      jumpCheck();
    }, { threshold: 0.25 }).observe(card);
  } else { visible = true; sync(); }
  document.addEventListener("visibilitychange", sync);
})();
