/* Démo « Studio lumière » : aperçu (rien n'est envoyé) → appliquer → envoyé → confirmé → revenir. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var GLOW = { "heure-doree": "#ffcf8a", aurore: "#7cf0dc", lecture: "#fff1d6", ocean: "#7fd0ff", cinema: "#c39bff", "nuit-douce": "#c79a5a" };

  document.querySelectorAll('[data-demo="ambiances"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var imgs = [].slice.call(root.querySelectorAll(".am-img"));
    var chips = [].slice.call(root.querySelectorAll(".am-chips button"));
    var front = $(".am-front"), nameEl = $('[data-am="name"]'), state = $('[data-am="state"]');
    var apply = $('[data-am="apply"]'), back = $('[data-am="back"]'), dim = $('[data-am="dim"]');
    var shown = imgs[0].getAttribute("data-k"), applied = shown, previous = null, manual = false, timer = null, visible = false;

    function img(k) { return imgs.filter(function (i) { return i.getAttribute("data-k") === k; })[0]; }
    function chip(k) { return chips.filter(function (c) { return c.getAttribute("data-k") === k; })[0]; }
    function setState(cls, text) {
      state.className = "am-state" + (cls ? " " + cls : "");
      state.querySelector("span").textContent = text;
    }
    function show(k) {
      if (k === shown) return;
      var next = img(k), cur = img(shown);
      shown = k;
      nameEl.textContent = chip(k).getAttribute("data-name");
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip(k)); });
      if (reduce) { cur.classList.remove("is-on"); next.classList.add("is-on"); return; }
      imgs.forEach(function (i) { i.classList.remove("is-enter"); });
      next.classList.add("is-enter");
      root.style.setProperty("--glow", GLOW[k] || "#ffd9a0");
      front.style.setProperty("--glow", GLOW[k] || "#ffd9a0");
      front.classList.remove("go"); void front.offsetWidth; front.classList.add("go");
      setTimeout(function () {
        if (shown !== k) return;
        imgs.forEach(function (i) { i.classList.toggle("is-on", i === next); });
        next.classList.remove("is-enter");
      }, 1550);
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
    dim.addEventListener("input", function () {
      imgs.forEach(function (i) { i.style.setProperty("--dim", (dim.value / 100).toFixed(2)); });
    });

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
