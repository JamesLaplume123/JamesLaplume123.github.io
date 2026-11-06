/* Démo « Studio lumière » : aperçu (rien n'est envoyé) → appliquer → envoyé → confirmé → revenir. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  /* Circuits de la pièce (zones des photos), dans l'ordre où ils changent : plafond, couloir, cuisine, salon */
  var ZONES = [
    "radial-gradient(62% 36% at 50% 12%, #000 30%, transparent 78%)",
    "radial-gradient(17% 27% at 48% 52%, #000 25%, transparent 78%)",
    "radial-gradient(34% 56% at 16% 64%, #000 30%, transparent 78%)",
    "radial-gradient(40% 52% at 80% 66%, #000 30%, transparent 78%)"
  ];

  document.querySelectorAll('[data-demo="ambiances"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var imgs = [].slice.call(root.querySelectorAll(".am-img"));
    var chips = [].slice.call(root.querySelectorAll(".am-chips button"));
    var veil = $(".am-veil"), nameEl = $('[data-am="name"]'), state = $('[data-am="state"]');
    var apply = $('[data-am="apply"]'), back = $('[data-am="back"]'), dim = $('[data-am="dim"]');
    var shown = imgs[0].getAttribute("data-k"), applied = shown, previous = null, manual = false, timer = null, visible = false;
    var zones = [], settle = null, arriving = null;

    function img(k) { return imgs.filter(function (i) { return i.getAttribute("data-k") === k; })[0]; }
    function chip(k) { return chips.filter(function (c) { return c.getAttribute("data-k") === k; })[0]; }
    function setState(cls, text) {
      state.className = "am-state" + (cls ? " " + cls : "");
      state.querySelector("span").textContent = text;
    }
    /* Change d'ambiance comme une vraie scène : chaque circuit passe à la nouvelle lumière
       l'un après l'autre (≈ 160 ms d'écart), puis la pièce entière se pose (≈ 1,4 s en tout). */
    function land() {
      clearTimeout(settle);
      if (arriving) imgs.forEach(function (i) { i.classList.toggle("is-on", i === arriving); });
      imgs.forEach(function (i) { i.classList.remove("is-enter"); });
      zones.forEach(function (z) { z.remove(); });
      zones = []; arriving = null;
    }
    function show(k) {
      if (k === shown) return;
      var next = img(k);
      shown = k;
      nameEl.textContent = chip(k).getAttribute("data-name");
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip(k)); });
      land(); /* un changement encore en cours se termine d'abord */
      arriving = next;
      if (reduce) { land(); return; }
      var src = next.currentSrc || next.src;
      zones = ZONES.map(function (z, i) {
        var e = document.createElement("img");
        e.className = "am-zone"; e.src = src; e.alt = ""; e.setAttribute("aria-hidden", "true");
        e.style.setProperty("--z", z);
        e.style.transitionDelay = (i * .16) + "s";
        next.parentNode.insertBefore(e, veil);
        return e;
      });
      next.classList.add("is-enter");
      void next.offsetWidth;
      zones.forEach(function (e) { e.classList.add("go"); });
      settle = setTimeout(land, 1500);
    }
    function markApplied(k) {
      chips.forEach(function (c) { c.classList.toggle("is-applied", c.getAttribute("data-k") === k); });
    }

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        manual = true;
        root.classList.add("is-manual");
        clearTimeout(timer);
        var k = c.getAttribute("data-k");
        show(k);
        if (k === applied) { setState("", "Appliquée"); apply.disabled = true; }
        else { setState("is-preview", "Aperçu · rien n’est envoyé"); apply.disabled = false; }
      });
    });
    apply.addEventListener("click", function () {
      if (apply.disabled) return;
      apply.disabled = true;
      previous = applied;
      setState("is-sent", "Envoyé aux lumières…");
      setTimeout(function () {
        applied = shown;
        markApplied(applied);
        setState("", "Confirmé · lumières relues");
        back.hidden = false;
        back.textContent = "Revenir à " + chip(previous).getAttribute("data-name");
      }, reduce ? 0 : 900);
    });
    back.addEventListener("click", function () {
      if (!previous) return;
      var k = previous;
      previous = null;
      back.hidden = true;
      show(k);
      setState("is-sent", "Retour à l’éclairage précédent…");
      setTimeout(function () { applied = k; markApplied(k); setState("", "Confirmé · éclairage précédent rétabli"); apply.disabled = true; }, reduce ? 0 : 900);
    });
    dim.addEventListener("input", function () { veil.style.setProperty("--am-dim", (dim.value / 100).toFixed(2)); });

    /* Démonstration automatique tant que le visiteur n'a rien touché */
    function auto() {
      clearTimeout(timer);
      if (manual || reduce || !visible) return;
      timer = setTimeout(function () {
        var i = chips.indexOf(chip(shown));
        var k = chips[(i + 1) % chips.length].getAttribute("data-k");
        show(k); applied = k; markApplied(k); setState("", "Appliquée");
        auto();
      }, 3800);
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { visible = e.isIntersecting; if (visible) auto(); else clearTimeout(timer); });
      }, { threshold: .4 }).observe(root);
    }
  });
})();
