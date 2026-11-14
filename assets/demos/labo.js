/* Laboratoire des cartes : « Édition prestige ». Reflets de lunette et de cadre qui suivent la main,
   légère inclinaison 3D, apparition orchestrée (l'aiguille balaie jusqu'à sa valeur, les graduations
   s'allument à son passage, les chiffres roulent), consigne du thermostat réglable (glisser, boutons,
   flèches du clavier), porte du véhicule. Rien n'est nécessaire à l'affichage : sans script, tout reste
   lisible. Animations en pause hors écran; prefers-reduced-motion respecté. */
(function () {
  "use strict";
  var root = document.querySelector("[data-px-root]");
  if (!root) return;
  var doc = document.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia && matchMedia("(hover: hover) and (pointer: fine)").matches;
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function base() { return doc.getAttribute("data-mode") === "base"; }
  function moving() { return !reduce && doc.classList.contains("fx"); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fmt(n, d) { var s = Math.abs(n).toFixed(d || 0).replace(".", ","); return (n < 0 ? "−" : "") + s; }
  function pol(r, deg) { var a = (deg - 90) * Math.PI / 180; return [120 + r * Math.cos(a), 120 + r * Math.sin(a)]; }
  function arcD(r, a0, a1) {
    if (a1 - a0 < .05) a1 = a0 + .05;
    var p0 = pol(r, a0), p1 = pol(r, a1);
    return "M" + p0[0].toFixed(2) + " " + p0[1].toFixed(2) + "A" + r + " " + r + " 0 " + (a1 - a0 > 180 ? 1 : 0) + " 1 " + p1[0].toFixed(2) + " " + p1[1].toFixed(2);
  }
  function ease(k) { return 1 - Math.pow(1 - k, 3); }

  /* ---------- Chiffres qui roulent ---------- */
  function strip(ch) { var s = ""; for (var n = 0; n < 10; n++) s += "<i>" + n + "</i>"; return '<span class="px-dg" style="--d:' + ch + '"><span>' + s + "</span></span>"; }
  function setNum(el, v, quick) {
    var d = +el.getAttribute("data-d") || 0, txt = fmt(v, d), roll = el.querySelector(".px-roll"), sr = el.querySelector(".px-sr");
    if (sr) sr.textContent = txt;
    var dgs = roll.querySelectorAll(".px-dg"), want = txt.replace(/[^\d]/g, "");
    el.classList.toggle("is-quick", !!quick);
    if (dgs.length !== want.length) {
      var h = "", dec = false;
      for (var i = 0; i < txt.length; i++) {
        var c = txt.charAt(i);
        if (c === ",") { h += '<span class="px-dec">,'; dec = true; } else if (/\d/.test(c)) h += strip(c); else h += '<span class="px-sg">' + c + "</span>";
      }
      roll.innerHTML = h + (dec ? "</span>" : "");
      return;
    }
    for (var j = 0; j < dgs.length; j++) dgs[j].style.setProperty("--d", want.charAt(j));
  }
  /* Place les chiffres d'un coup (sans rouler), pour partir d'une valeur de départ */
  function zeroNum(el) { el.classList.add("is-set"); $$(".px-dg", el).forEach(function (g) { g.style.setProperty("--d", 0); }); void el.offsetWidth; el.classList.remove("is-set"); }

  /* ---------- Cadrans ---------- */
  function Dial(el) {
    this.el = el;
    this.lo = +el.getAttribute("data-lo"); this.hi = +el.getAttribute("data-hi"); this.v = +el.getAttribute("data-v");
    this.arcs = $$("[data-arc]", el); this.knob = el.querySelector("[data-knob]");
    this.ticks = $$("[data-v]", el.querySelector(".px-ticks")).map(function (t) { return [t, +t.getAttribute("data-v")]; });
    this.shown = this.v; this.raf = 0;
  }
  Dial.prototype.ang = function (v) { return -135 + clamp((v - this.lo) / (this.hi - this.lo), 0, 1) * 270; };
  Dial.prototype.paint = function (v) {
    var a = this.ang(v), d = arcD(80, -135, a), k = pol(80, a);
    for (var i = 0; i < this.arcs.length; i++) this.arcs[i].setAttribute("d", d);
    this.knob.setAttribute("transform", "translate(" + k[0].toFixed(2) + " " + k[1].toFixed(2) + ")");
    this.el.style.setProperty("--ka", a.toFixed(2) + "deg");
    for (var j = 0; j < this.ticks.length; j++) {
      var on = this.ticks[j][1] <= v + 1e-6, t = this.ticks[j][0];
      if (t.__on !== on) { t.__on = on; t.classList.toggle("is-on", on); }
    }
    this.shown = v;
  };
  /* L'aiguille glisse jusqu'à sa valeur; les graduations s'allument à son passage */
  Dial.prototype.go = function (to, ms, from) {
    var self = this, f = from != null ? from : this.shown;
    cancelAnimationFrame(this.raf);
    if (!moving() || ms === 0) { this.paint(to); return; }
    var t0 = performance.now();
    (function step(t) {
      var k = clamp((t - t0) / ms, 0, 1);
      self.paint(f + (to - f) * ease(k));
      if (k < 1) self.raf = requestAnimationFrame(step);
    })(t0);
  };

  var dials = {};
  $$("[data-pdial]").forEach(function (el) { dials[el.getAttribute("data-pdial")] = new Dial(el); });

  /* ---------- Apparition orchestrée et pause hors écran ---------- */
  var cards = $$(".px-card, .px-ref");
  function enter(card) {
    if (card.classList.contains("is-in")) return;
    var ds = $$("[data-pdial]", card).map(function (el) { return dials[el.getAttribute("data-pdial")]; });
    var nums = $$(".px-n", card);
    if (moving()) {
      ds.forEach(function (d) { d.paint(d.lo); });
      nums.forEach(zeroNum);
    }
    requestAnimationFrame(function () {
      card.classList.add("is-in");
      var delay = (+getComputedStyle(card).getPropertyValue("--i") || 0) * 110 + 650;
      setTimeout(function () {
        ds.forEach(function (d, i) { setTimeout(function () { d.go(d.v, 1700, d.lo); }, i * 120); });
        nums.forEach(function (n) { setNum(n, +n.getAttribute("data-pn")); });
      }, moving() ? delay : 0);
    });
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) enter(e.target);
        e.target.classList.toggle("is-off", !e.isIntersecting);
      });
    }, { threshold: [0, .18] });
    cards.forEach(function (c) { io.observe(c); });
  } else cards.forEach(enter);

  /* ---------- Reflets et profondeur au survol ---------- */
  function lightAng(cx, cy, x, y) { return Math.atan2(x - cx, -(y - cy)) * 180 / Math.PI - 43; }
  $$(".px-card").forEach(function (card) {
    if (!fine) return;
    var raf = 0, ev = null, ds = $$("[data-pdial]", card);
    card.addEventListener("pointermove", function (e) {
      ev = e;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = card.getBoundingClientRect(), mx = clamp((ev.clientX - r.left) / r.width, 0, 1), my = clamp((ev.clientY - r.top) / r.height, 0, 1);
        card.style.setProperty("--mx", mx.toFixed(3));
        card.style.setProperty("--my", my.toFixed(3));
        if (base() || reduce) return;
        card.style.setProperty("--cang", lightAng(r.left + r.width / 2, r.top + r.height / 2, ev.clientX, ev.clientY).toFixed(1) + "deg");
        card.style.setProperty("--rx", ((.5 - my) * 3.2).toFixed(2) + "deg");
        card.style.setProperty("--ry", ((mx - .5) * 4.2).toFixed(2) + "deg");
        ds.forEach(function (d) {
          var b = d.getBoundingClientRect(), cx = b.left + b.width / 2, cy = b.top + b.height / 2;
          d.style.setProperty("--ang", lightAng(cx, cy, ev.clientX, ev.clientY).toFixed(1) + "deg");
          d.style.setProperty("--gx", clamp((ev.clientX - cx) / b.width, -1, 1).toFixed(2));
          d.style.setProperty("--gy", clamp((ev.clientY - cy) / b.height, -1, 1).toFixed(2));
        });
      });
    });
    card.addEventListener("pointerenter", function () { if (!base()) card.classList.add("is-hover"); });
    card.addEventListener("pointerleave", function () {
      card.classList.remove("is-hover");
      ["--rx", "--ry", "--cang"].forEach(function (p) { card.style.removeProperty(p); });
      ds.forEach(function (d) { ["--ang", "--gx", "--gy"].forEach(function (p) { d.style.removeProperty(p); }); });
    });
  });

  /* ---------- Thermostat : consigne réglable ---------- */
  $$(".px-c-thermo").forEach(function (card) {
    var g = card.querySelector(".px-dial.is-live"), D = dials[g.getAttribute("data-pdial")];
    var inside = 21, step = +g.getAttribute("data-step") || .5, v = D.v, timer = 0, drag = false;
    var big = g.querySelector(".px-n"), md = card.querySelector("[data-tmode]"), sent = card.querySelector("[data-sent]");
    var ICON = { heat: card.querySelector("[data-tmode] svg").innerHTML };
    var SNOW = '<path d="M12 2.75v18.5M3.99 7.38l16.02 9.24M3.99 16.62l16.02-9.24"/><path d="m9.5 4.25 2.5 2 2.5-2M9.5 19.75l2.5-2 2.5 2"/>';
    var CHECK = '<path d="m5 12.5 4.5 4.5L19 7.5"/>';
    function show(nv, quick) {
      v = nv;
      D.v = nv; D.go(nv, quick ? 380 : 0);
      setNum(big, nv, true);
      var m = nv > inside + .25 ? ["heat", ICON.heat, "Chauffage"] : nv < inside - .25 ? ["cool", SNOW, "Refroidissement"] : ["hold", CHECK, "Consigne atteinte"];
      md.className = "px-mode is-" + (m[0] === "hold" ? "ok" : m[0]);
      md.querySelector("svg").innerHTML = m[1]; md.querySelector("span").textContent = m[2];
      g.setAttribute("aria-valuenow", nv); g.setAttribute("aria-valuetext", fmt(nv, 1) + " °C");
    }
    function send() {
      sent.className = "px-sent is-wait"; sent.querySelector("span").textContent = "Envoi de la consigne…";
      clearTimeout(timer);
      timer = setTimeout(function () { sent.className = "px-sent"; sent.querySelector("span").textContent = "Consigne de " + fmt(v, 1) + " °C confirmée par l’appareil"; }, 900);
    }
    function setV(nv) { nv = clamp(Math.round(nv / step) * step, D.lo, D.hi); if (nv !== v) { show(nv, true); return true; } return false; }
    function at(e) {
      var r = g.getBoundingClientRect(), a = Math.atan2(e.clientX - (r.left + r.width / 2), -(e.clientY - (r.top + r.height / 2))) * 180 / Math.PI;
      return D.lo + (clamp(a, -135, 135) + 135) / 270 * (D.hi - D.lo);
    }
    g.addEventListener("pointerdown", function (e) { drag = true; g.classList.add("is-drag"); try { g.setPointerCapture(e.pointerId); } catch (err) {} e.preventDefault(); setV(at(e)); });
    g.addEventListener("pointermove", function (e) { if (drag) setV(at(e)); });
    function end() { if (!drag) return; drag = false; g.classList.remove("is-drag"); send(); }
    g.addEventListener("pointerup", end); g.addEventListener("pointercancel", end);
    g.addEventListener("keydown", function (e) {
      var d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[e.key];
      if (!d) return;
      e.preventDefault();
      if (setV(v + d * step)) send();
    });
    $$("[data-step]", card).forEach(function (b) {
      if (b === g) return;
      b.addEventListener("click", function () { if (setV(v + +b.getAttribute("data-step") * step)) send(); });
    });
  });

  /* ---------- Véhicule : porte de la baie ---------- */
  $$(".px-c-car").forEach(function (card) {
    var btn = card.querySelector("[data-door]"), st = card.querySelector("[data-door-state]"), val = card.querySelector("[data-door-v]"), lab = card.querySelector("[data-door-l]");
    var open = false, busy = false;
    btn.addEventListener("click", function () {
      if (busy) return;
      busy = true; open = !open;
      val.textContent = open ? "Ouverture…" : "Fermeture…";
      setTimeout(function () {
        busy = false;
        val.textContent = open ? "Ouverte" : "Fermée";
        lab.textContent = open ? "Fermer la porte 1" : "Ouvrir la porte 1";
        btn.setAttribute("aria-pressed", open ? "true" : "false");
        st.className = "px-state " + (open ? "is-warn" : "is-ok");
        st.lastChild.textContent = open ? "Porte ouverte" : "Remisé";
      }, reduce ? 0 : 1300);
    });
  });
})();
