/* Galeries photo : le lent mouvement des photos (CSS, seulement sous html.fx) ne tourne que
   lorsque la carte est à l'écran; hors écran, il s'arrête (IntersectionObserver). */
(function () {
  "use strict";
  var figs = document.querySelectorAll(".gl-fig");
  if (!figs.length || !("IntersectionObserver" in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { e.target.classList.toggle("is-vis", e.isIntersecting); });
  }, { rootMargin: "80px 0px" });
  figs.forEach(function (f) { if (f.querySelector("img")) io.observe(f); });
})();
