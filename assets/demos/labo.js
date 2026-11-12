/* Laboratoire des cartes : reflets qui suivent la souris, inclinaison 3D (B), consignes réglables
   (glisser, boutons, flèches du clavier), flux qui respirent, caméras, portes, lecture de l'historique,
   apparition orchestrée. Rien n'est nécessaire à l'affichage : sans script, tout reste lisible. */
(function () {
  "use strict";
  var root = document.querySelector("[data-lx]");
  if (!root) return;
  var doc = document.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia && matchMedia("(hover: hover) and (pointer: fine)").matches;
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function base() { return doc.getAttribute("data-mode") === "base"; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fmt(n, d) { var s = Math.abs(n).toFixed(d || 0).replace(".", ","); return (n < 0 ? "−" : "") + s; }
  function pol(cx, cy, r, deg) { var a = (deg - 90) * Math.PI / 180; return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; }
  function arcD(cx, cy, r, a0, a1) {
    var p0 = pol(cx, cy, r, a0), p1 = pol(cx, cy, r, a1);
    return "M" + p0[0].toFixed(2) + " " + p0[1].toFixed(2) + "A" + r + " " + r + " 0 " + ((a1 - a0) % 360 > 180 ? 1 : 0) + " 1 " + p1[0].toFixed(2) + " " + p1[1].toFixed(2);
  }

  /* ---------- Tween des nombres ---------- */
  function tween(el, to, d, ms) {
    var from = parseFloat((el.textContent || "0").replace("−", "-").replace(",", ".")) || 0;
    if (reduce || ms === 0) { el.textContent = fmt(to, d); return; }
    var t0 = performance.now();
    (function step(t) {
      var k = clamp((t - t0) / ms, 0, 1), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(from + (to - from) * e, d);
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  /* ---------- Reflets et inclinaison ---------- */
  $$("[data-lx-tilt]").forEach(function (card) {
    if (!fine) return;
    var is3d = card.getAttribute("data-lx-tilt") === "3d", raf = 0, ev = null;
    card.addEventListener("pointermove", function (e) {
      ev = e;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = card.getBoundingClientRect(), mx = clamp((ev.clientX - r.left) / r.width, 0, 1), my = clamp((ev.clientY - r.top) / r.height, 0, 1);
        card.style.setProperty("--mx", mx.toFixed(3));
        card.style.setProperty("--my", my.toFixed(3));
        if (base() || reduce) return;
        var ang = Math.atan2(my - .5, mx - .5) * 180 / Math.PI + 90;
        card.style.setProperty("--ang", ang.toFixed(1) + "deg");
        if (is3d) {
          card.classList.add("is-hover");
          card.style.setProperty("--rx", ((.5 - my) * 5).toFixed(2) + "deg");
          card.style.setProperty("--ry", ((mx - .5) * 7).toFixed(2) + "deg");
        }
      });
    });
    card.addEventListener("pointerenter", function () { if (!base()) card.classList.add("is-hover"); });
    card.addEventListener("pointerleave", function () {
      card.classList.remove("is-hover");
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    });
  });

  /* ---------- Thermostats ---------- */
  var SCENE_MIN = 14 * 60 + 20;
  function hhmm(min) { var h = Math.floor(min / 60) % 24, m = Math.round(min % 60); return h + " h " + (m < 10 ? "0" : "") + m; }
  $$("[data-thermo]").forEach(function (card) {
    var kind = card.getAttribute("data-thermo");
    var lo = +card.getAttribute("data-min"), hi = +card.getAttribute("data-max");
    var inside = +card.getAttribute("data-in"), v = +card.getAttribute("data-set");
    var dial = card.querySelector("[data-dial]");
    var outs = function (k) { return $$('[data-out="' + k + '"]', card); };
    function texts() {
      var diff = v - inside, eta = SCENE_MIN + Math.max(10, diff * 60);
      var heat = diff > .2, cool = diff < -.2;
      var st = heat ? "Chauffe en douceur · " + fmt(v, 1) + "° vers " + hhmm(eta) : cool ? "Au repos · la pièce redescend vers " + fmt(v, 1) + "°" : "Température atteinte · " + fmt(v, 1) + "° maintenus";
      if (kind === "b") st = heat ? "Chauffe · cible atteinte vers " + hhmm(eta) : cool ? "Au repos · descente vers " + fmt(v, 1) + " °C" : "Cible atteinte · maintien";
      if (kind === "c") {
        st = heat ? "La pièce atteindra " + fmt(v, 1) + "° vers " + hhmm(eta) + ". La thermopompe travaille " + (diff > 2 ? "à pleine puissance." : "au tiers de sa puissance.")
          : cool ? "Le chauffage se repose. La pièce redescendra doucement vers " + fmt(v, 1) + "°." : "La pièce est à la bonne température. JARVIS la maintient sans bruit.";
        outs("state").forEach(function (o) { o.textContent = heat ? "Chauffe en douceur" : cool ? "Au repos" : "Stable"; });
        card.classList.toggle("is-warm", heat);
        card.style.setProperty("--al-i", clamp(.35 + diff / 3, .35, 1).toFixed(2));
      }
      outs("status").forEach(function (o) { o.textContent = st; });
    }
    function render(animate) {
      var t = (v - lo) / (hi - lo);
      outs("set").forEach(function (o) { o.textContent = fmt(v, 1) + (kind === "a" ? "°" : ""); });
      if (kind === "a") {
        var a = -135 + 270 * t, ai = -135 + 270 * (inside - lo) / (hi - lo);
        var h = card.querySelector("[data-hand]"); if (h) h.style.setProperty("--a", a.toFixed(2) + "deg");
        var dem = card.querySelector("[data-demand]");
        if (dem) dem.setAttribute("d", Math.abs(a - ai) < .5 ? "M0 0" : arcD(160, 160, 124, Math.min(a, ai), Math.max(a, ai)));
      } else if (kind === "b") {
        var k = card.querySelector("[data-knob]"); if (k) k.style.setProperty("--a", (-100 + 200 * t).toFixed(2) + "deg");
        $$("[data-arcval]", card).forEach(function (p) { p.style.strokeDasharray = (t * 100).toFixed(2) + " 100"; });
      } else {
        card.style.setProperty("--t", t.toFixed(4));
      }
      if (dial) { dial.setAttribute("aria-valuenow", v); dial.setAttribute("aria-valuetext", fmt(v, 1) + " degrés"); }
      texts();
    }
    function set(nv) { nv = clamp(Math.round(nv * 2) / 2, lo, hi); if (nv === v) return; v = nv; card.classList.add("is-live"); render(true); }
    $$("[data-step]", card).forEach(function (b) { b.addEventListener("click", function () { set(v + parseFloat(b.getAttribute("data-step"))); }); });
    if (dial) {
      dial.setAttribute("role", "slider"); dial.setAttribute("tabindex", "0");
      dial.setAttribute("aria-label", "Consigne de température"); dial.setAttribute("aria-valuemin", lo); dial.setAttribute("aria-valuemax", hi);
      dial.addEventListener("keydown", function (e) {
        var d = { ArrowUp: .5, ArrowRight: .5, ArrowDown: -.5, ArrowLeft: -.5 }[e.key];
        if (d) { e.preventDefault(); set(v + d); }
      });
      var drag = false;
      var fromPoint = function (e) {
        var r = dial.getBoundingClientRect();
        if (kind === "c") { var rail = dial.querySelector(".al-rail").getBoundingClientRect(); return lo + (hi - lo) * clamp((e.clientX - rail.left) / rail.width, 0, 1); }
        var cx = r.left + r.width / 2, cy = kind === "a" ? r.top + r.height / 2 : r.top + r.width * 196 / 400;
        var ang = Math.atan2(e.clientX - cx, cy - e.clientY) * 180 / Math.PI;
        var span = kind === "a" ? 135 : 100;
        return lo + (hi - lo) * (clamp(ang, -span, span) + span) / (2 * span);
      };
      dial.addEventListener("pointerdown", function (e) {
        if (e.target.closest("button")) return;
        drag = true; dial.setPointerCapture(e.pointerId); set(fromPoint(e));
      });
      dial.addEventListener("pointermove", function (e) { if (drag) set(fromPoint(e)); });
      dial.addEventListener("pointerup", function () { drag = false; });
      dial.addEventListener("pointercancel", function () { drag = false; });
    }
    render(false);
  });

  /* ---------- Flux d'énergie : la production respire, les compteurs suivent ---------- */
  var MAX = { solaire: 14.4, maison: 10, batteries: 10, reseau: 10 };
  function flowTick(card, first) {
    var s = 4.4 + (Math.random() - .5) * .34, m = 2.8 + (Math.random() - .5) * .2, b = 1.2 + (Math.random() - .5) * .1;
    if (first) { s = 4.4; m = 2.8; b = 1.2; }
    var vals = { solaire: s, maison: m, batteries: b, reseau: Math.max(0, s - m - b) };
    Object.keys(vals).forEach(function (k) {
      $$('[data-num="' + k + '"]', card).forEach(function (el) { tween(el, Math.round(vals[k] * 10) / 10, 1, 700); });
      var a = -140 + 280 * clamp(vals[k] / MAX[k], 0, 1);
      var hand = card.querySelector('[data-hand-of="' + k + '"]'); if (hand) hand.style.setProperty("--a", a.toFixed(2) + "deg");
      var arc = card.querySelector('[data-arc="' + k + '"]');
      if (arc) arc.setAttribute("d", arcD(+arc.dataset.cx, +arc.dataset.cy, +arc.dataset.r, -140, Math.max(a, -139)));
    });
  }
  var flows = $$("[data-flow]");

  /* ---------- Compteurs à l'arrivée ---------- */
  function countUp(card) {
    $$("[data-count]", card).forEach(function (el) {
      var to = parseFloat(el.getAttribute("data-count")), d = +(el.getAttribute("data-d") || 0);
      if (reduce) { el.textContent = fmt(to, d); return; }
      el.textContent = fmt(0, d); tween(el, to, d, 1500);
    });
  }

  /* ---------- Horloge de la scène (14:20:00 au chargement) ---------- */
  var t0 = Date.now();
  function tick() {
    var s = 14 * 3600 + 20 * 60 + Math.floor((Date.now() - t0) / 1000);
    var txt = [Math.floor(s / 3600) % 24, Math.floor(s / 60) % 60, s % 60].map(function (n) { return (n < 10 ? "0" : "") + n; }).join(":");
    $$("[data-clock]").forEach(function (el) { el.textContent = txt; });
  }
  tick(); setInterval(tick, 1000);

  /* ---------- Caméras ---------- */
  $$("[data-cams]").forEach(function (card) {
    var img = card.querySelector("[data-cam-img]");
    function show(btn) {
      $$("[data-cam]", card).forEach(function (b) { var on = b === btn; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
      var src = btn.getAttribute("data-src"), name = btn.getAttribute("data-name");
      $$("[data-cam-name]", card).forEach(function (n) { n.textContent = name; });
      if (!img || img.getAttribute("src") === src) return;
      img.classList.add("is-swap");
      setTimeout(function () {
        img.onload = function () { img.classList.remove("is-swap"); };
        img.src = src; img.alt = "Vue de la caméra " + name;
        if (img.complete) img.classList.remove("is-swap");
      }, reduce ? 0 : 260);
    }
    $$("[data-cam]", card).forEach(function (b) { b.addEventListener("click", function () { show(b); }); });
    var arm = card.querySelector("[data-arm]");
    if (arm) arm.addEventListener("click", function () {
      var on = !arm.classList.contains("is-on");
      arm.classList.toggle("is-on", on); arm.setAttribute("aria-pressed", on ? "true" : "false");
      $$("[data-arm-l]", card).forEach(function (l) { l.textContent = on ? "Système armé" : "Système désarmé"; });
      $$("[data-arm-s]", card).forEach(function (l) { l.textContent = on ? "Périmètre et mouvement" : "Caméras en enregistrement seulement"; });
      $$("[data-armed-l]", card).forEach(function (l) {
        l.classList.toggle("is-off", !on);
        var long = l.classList.contains("ck-armed");
        var dot = l.querySelector("i");
        l.textContent = on ? (long ? "Armé · mode nuit 23 h" : "Armé") : "Désarmé";
        if (dot) l.insertBefore(dot, l.firstChild);
      });
    });
    var sim = card.querySelector("[data-simulate]"), timer = 0;
    if (sim) sim.addEventListener("click", function () {
      var title = card.querySelector("[data-alert-title]"), text = card.querySelector("[data-alert-text]");
      var allee = card.querySelector('[data-cam="allee"]'); if (allee) show(allee);
      card.classList.add("is-alert");
      title.textContent = "Mouvement dans l’allée.";
      text.textContent = "Une silhouette près de la porte du garage, à l’instant. Les lumières extérieures sont allumées et la vidéo est gardée.";
      sim.textContent = "Revenir au calme";
      clearTimeout(timer);
      var calm = function () {
        card.classList.remove("is-alert");
        title.textContent = "Tout est calme.";
        text.textContent = "Trois caméras veillent. Le mode nuit armera aussi les fenêtres à 23 h.";
        sim.textContent = "Simuler un mouvement";
      };
      if (sim.dataset.alert === "1") { sim.dataset.alert = ""; calm(); return; }
      sim.dataset.alert = "1";
      timer = setTimeout(function () { sim.dataset.alert = ""; calm(); }, 9000);
    });
  });

  /* ---------- Porte du garage ---------- */
  $$("[data-car]").forEach(function (card) {
    var btn = card.querySelector("[data-door]");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-pressed") !== "true";
      btn.setAttribute("aria-pressed", open ? "true" : "false");
      card.classList.toggle("is-alert", open);
      $$("[data-door-l]", card).forEach(function (l) { l.textContent = open ? "Fermer la porte 1" : "Ouvrir la porte 1"; });
      $$("[data-door-v]", card).forEach(function (l) { l.textContent = open ? "Ouverte" : "Fermée"; });
      $$("[data-door-state]", card).forEach(function (l) { l.textContent = open ? "Porte 1 ouverte" : "Remisée"; l.classList.toggle("is-ok", !open); });
      var tri = card.querySelector('[data-tri="porte"]');
      if (tri) {
        tri.querySelector("[data-tri-hand]").style.setProperty("--a", open ? "-120deg" : "120deg");
        tri.querySelector("[data-tri-v]").textContent = open ? "Ouverte" : "Fermée";
      }
      var co = card.querySelector('[data-co="porte"]');
      if (co) { co.classList.toggle("is-alert", open); co.querySelector("[data-co-v]").textContent = open ? "Ouverte" : "Fermée"; }
    });
  });

  /* ---------- Historique : lecture heure par heure ---------- */
  $$(".ck-chart[data-hist], .al-chart[data-hist]").forEach(function (box) {
    var data = JSON.parse(box.getAttribute("data-hist")), cross = box.querySelector("[data-cross]");
    function at(e) {
      var r = box.getBoundingClientRect(), x = clamp((e.clientX - r.left) / r.width, 0, 1), h = Math.round(x * 23);
      cross.hidden = false;
      cross.style.left = (100 * h / 23) + "%";
      cross.classList.toggle("is-flip", h > 15);
      cross.querySelector("[data-tip-h]").textContent = h + " h";
      cross.querySelector("[data-tip-p]").textContent = fmt(data[h][1], 1);
      cross.querySelector("[data-tip-c]").textContent = fmt(data[h][0], 1);
    }
    box.addEventListener("pointermove", at);
    box.addEventListener("pointerdown", at);
    box.addEventListener("pointerleave", function () { cross.hidden = true; });
  });
  $$(".ha-hist[data-hist]").forEach(function (card) {
    var data = JSON.parse(card.getAttribute("data-hist")), gmt = card.querySelector(".ha-gmt");
    var hEl = card.querySelector("[data-hist-h]"), vEl = card.querySelector("[data-hist-v]");
    function show(h) {
      gmt.classList.toggle("is-hl", h != null);
      $$("[data-hs]", card).forEach(function (p) { p.classList.toggle("is-hl", +p.getAttribute("data-hs") === h); });
      if (h == null) h = 14;
      hEl.textContent = h + " h";
      vEl.textContent = fmt(data[h][1], 1) + " · " + fmt(data[h][0], 1);
    }
    $$("[data-h]", card).forEach(function (p) {
      p.addEventListener("pointerenter", function () { show(+p.getAttribute("data-h")); });
      p.addEventListener("pointerdown", function () { show(+p.getAttribute("data-h")); });
    });
    gmt.addEventListener("pointerleave", function () { show(null); });
  });

  /* ---------- Arrivée orchestrée et pause hors écran ---------- */
  $$(".lx-grid").forEach(function (g) { $$(".lx-card", g).forEach(function (c, i) { c.style.setProperty("--i", i); }); });
  $$(".ck-cells").forEach(function (cells) { $$("i", cells).forEach(function (c, i) { c.style.setProperty("--k", i); }); });
  var cards = $$(".lx-card");
  function svgs(card, run) { $$("svg", card).forEach(function (s) { if (s.pauseAnimations) { if (run && !reduce && !base()) s.unpauseAnimations(); else s.pauseAnimations(); } }); }
  function arrive(card) {
    if (card.classList.contains("is-in")) return;
    card.classList.add("is-in");
    countUp(card);
    if (card.hasAttribute("data-flow")) flowTick(card, true);
    var feed = card.querySelector(".ck-feed"); if (feed) card.style.setProperty("--scan-h", feed.offsetHeight + "px");
  }
  if ("IntersectionObserver" in window) {
    var seen = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { arrive(e.target); seen.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -12% 0px", threshold: .12 });
    var vis = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle("is-paused", !e.isIntersecting); e.target._vis = e.isIntersecting; svgs(e.target, e.isIntersecting); });
    }, { rootMargin: "80px" });
    cards.forEach(function (c) { seen.observe(c); vis.observe(c); });
  } else {
    cards.forEach(arrive);
  }
  if (!reduce) setInterval(function () {
    if (document.hidden) return;
    flows.forEach(function (c) { if (c._vis && c.classList.contains("is-in")) flowTick(c, false); });
  }, 2600);
  new MutationObserver(function () { cards.forEach(function (c) { svgs(c, c._vis); }); }).observe(doc, { attributes: true, attributeFilter: ["data-mode"] });
  addEventListener("resize", function () { $$(".ck-feed").forEach(function (f) { f.closest(".lx-card").style.setProperty("--scan-h", f.offsetHeight + "px"); }); }, { passive: true });
})();
