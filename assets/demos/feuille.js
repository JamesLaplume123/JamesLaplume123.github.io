/* Feuille de route : la piste se remplit une fois à l'arrivée; le point « en cours »
   ne respire que lorsque la section est à l'écran. */
(function () {
  "use strict";
  document.querySelectorAll('[data-demo="feuille"]').forEach(function (root) {
    if (!("IntersectionObserver" in window)) { root.classList.add("is-in", "is-vis"); return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) root.classList.add("is-in");
        root.classList.toggle("is-vis", e.isIntersecting);
      });
    }, { threshold: .35 }).observe(root);
  });
})();

/* Tableau des jalons : un filtre par solution, des interrupteurs par état; les compteurs
   suivent la solution choisie. Sans JavaScript, tous les jalons restent affichés. */
(function () {
  "use strict";
  document.querySelectorAll('[data-demo="feuille"] .fr-board').forEach(function (board) {
    var q = function (s) { return Array.prototype.slice.call(board.querySelectorAll(s)); };
    var fs = q(".fr-f"), ss = q(".fr-s"), cards = q(".fr-c");
    var count = board.querySelector(".fr-count b"), empty = board.querySelector(".fr-empty");
    var sol = "all", on = { existe: true, construit: true, avenir: true };
    var apply = function () {
      var shown = 0, per = { existe: 0, construit: 0, avenir: 0 };
      cards.forEach(function (c) {
        var okSol = sol === "all" || c.getAttribute("data-sol") === sol, st = c.getAttribute("data-st");
        if (okSol) per[st]++;
        var vis = okSol && on[st];
        if (vis && c.hidden) { c.classList.remove("is-new"); void c.offsetWidth; c.classList.add("is-new"); }
        c.hidden = !vis;
        if (vis) shown++;
      });
      ss.forEach(function (b) { b.querySelector("em").textContent = per[b.getAttribute("data-st")]; });
      count.textContent = shown;
      empty.hidden = shown > 0;
    };
    fs.forEach(function (b) {
      b.addEventListener("click", function () {
        sol = b.getAttribute("data-sol");
        fs.forEach(function (o) { o.classList.toggle("is-on", o === b); o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
        apply();
      });
    });
    ss.forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-st");
        on[k] = !on[k];
        b.classList.toggle("is-on", on[k]);
        b.setAttribute("aria-pressed", on[k] ? "true" : "false");
        apply();
      });
    });
  });
})();
