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
