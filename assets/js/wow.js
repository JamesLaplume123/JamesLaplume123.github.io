/* JARVIS — moteur « WOW » (chantier 2026)
   Règle d'or : rien ne dépend de ce script pour être visible. Les effets ne
   s'activent que sous html.fx, et tout filet de sécurité ramène le contenu. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Barre : fond plein après défilement */
  var bar = document.querySelector("[data-bar]");
  if (bar) {
    var solid = function () { bar.classList.toggle("is-solid", scrollY > 24); };
    addEventListener("scroll", solid, { passive: true });
    solid();
  }

  /* Menu mobile */
  var menuBtn = document.querySelector("[data-menu]");
  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".sheet a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-open");
        menuBtn.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Sélecteurs de contenu (ex. : moments de la journée) */
  document.querySelectorAll("[data-swap-group]").forEach(function (group) {
    var dataEl = document.getElementById(group.getAttribute("data-swap-group"));
    if (!dataEl) return;
    var data;
    try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var btns = [].slice.call(group.querySelectorAll("button[data-swap]"));
    var scope = document.querySelector(group.getAttribute("data-swap-scope")) || document;
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) {
          var on = x === b;
          x.classList.toggle("is-on", on);
          x.setAttribute("aria-pressed", on ? "true" : "false");
        });
        var d = data[b.getAttribute("data-swap")] || {};
        Object.keys(d).forEach(function (k) {
          var el = scope.querySelector('[data-swap-field="' + k + '"]');
          if (el) el.textContent = d[k];
        });
      });
    });
  });

  if (reduce) return;
  doc.classList.add("fx");

  function c01(v) { return Math.max(0, Math.min(1, v)); }
  function prog(el) {
    var r = el.getBoundingClientRect();
    return c01(-r.top / Math.max(1, r.height - innerHeight));
  }

  /* Filet de sécurité : tout redevient visible (impression, onglet caché) */
  function defuse() {
    doc.classList.remove("fx");
    document.querySelectorAll(".scene .t1,.scene .t2,.scene .t3,.scene img,.hero .bg img")
      .forEach(function (el) { el.style.opacity = ""; el.style.transform = ""; el.style.filter = ""; });
  }
  addEventListener("beforeprint", defuse);

  /* Manifeste : chaque mot devient un span qui s'allume */
  var mani = document.querySelector(".mani");
  var words = [];
  if (mani) {
    var mp = mani.querySelector("p");
    mp.innerHTML = mp.textContent.trim().split(/\s+/).map(function (w) {
      return "<span>" + w + "</span>";
    }).join(" ");
    words = [].slice.call(mp.querySelectorAll("span"));
  }

  /* Héros : zoom et assombrissement liés au défilement */
  var heroImg = document.querySelector(".hero .bg img");

  /* Scènes produit : image qui grossit, textes qui apparaissent */
  var scenes = [].slice.call(document.querySelectorAll(".scene")).map(function (s) {
    return { el: s, img: s.querySelector("img"), t1: s.querySelector(".t1"),
             t2: s.querySelector(".t2"), t3: s.querySelector(".t3") };
  });

  function frame() {
    if (heroImg) {
      var p = c01(scrollY / Math.max(innerHeight, 1));
      heroImg.style.transform = "scale(" + (1 + p * .14) + ")";
      heroImg.style.filter = "brightness(" + (1 - p * .55) + ")";
    }
    if (words.length) {
      var mpg = prog(mani), lit = Math.floor(mpg * words.length * 1.3);
      for (var i = 0; i < words.length; i++) words[i].classList.toggle("lit", i < lit);
    }
    scenes.forEach(function (s) {
      if (!s.img) return;
      var hp = prog(s.el);
      s.img.style.transform = "scale(" + (.8 + Math.min(hp, .55) * .4) + ")";
      if (s.t1) s.t1.style.opacity = c01((hp - .25) * 4);
      if (s.t2) s.t2.style.opacity = c01((hp - .42) * 4);
      if (s.t3) s.t3.style.opacity = c01((hp - .58) * 4);
    });
  }
  var queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; frame(); });
  }
  addEventListener("scroll", schedule, { passive: true });
  addEventListener("resize", schedule);
  schedule();

  /* Révélations à l'entrée dans la fenêtre */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: .18 });
  document.querySelectorAll("[data-rev]").forEach(function (el) { io.observe(el); });

  /* Patrouille : aucun élément dans la fenêtre ne reste caché */
  setInterval(function () {
    document.querySelectorAll("[data-rev]:not(.in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < innerHeight * 1.05 && r.bottom > 0) el.classList.add("in");
    });
  }, 800);

  /* Compteurs animés */
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var b = e.target, end = +b.getAttribute("data-n"), t0 = performance.now();
      (function tick(t) {
        var k = c01((t - t0) / 1400), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
        b.textContent = v;
        if (k < 1) requestAnimationFrame(tick);
      })(t0);
    });
  }, { threshold: .5 });
  document.querySelectorAll("[data-n]").forEach(function (el) { cio.observe(el); });
})();
