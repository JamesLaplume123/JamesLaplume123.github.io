/* L'offre : le mini-guide « Vous hésitez? ». Trois questions, la carte conseillée est mise en évidence avec sa
   raison (src/lieux.py, HESITE). Platinum si le lieu doit tourner pendant une panne ou s'il y a plus de trois
   lieux; Signature si l'IA doit fonctionner sans Internet ou s'il y a deux ou trois lieux; sinon Base. */
(function () {
  "use strict";
  Array.prototype.slice.call(document.querySelectorAll("[data-of-choix]")).forEach(function (bloc) {
    var rep = {}, raisons = {};
    try { raisons = JSON.parse(bloc.querySelector("[data-of-raisons]").textContent); } catch (e) {}
    var out = bloc.querySelector("[data-of-raison]");
    function maj() {
      var n = Object.keys(rep).length, hub = "";
      if (n) {
        if (rep.panne === "oui" || rep.lieux === "9") hub = "platinum";
        else if (rep.ia === "oui" || rep.lieux === "3") hub = "signature";
        else hub = "base";
      }
      Array.prototype.slice.call(bloc.querySelectorAll("[data-hub]")).forEach(function (c) {
        c.classList.toggle("is-conseil", c.getAttribute("data-hub") === hub);
        c.classList.toggle("is-autre", !!hub && c.getAttribute("data-hub") !== hub);
      });
      if (out) { out.hidden = !hub; out.textContent = hub ? raisons[hub] || "" : ""; }
    }
    bloc.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-r]"); if (!b) return;
      var q = b.closest("[data-q]"), k = q.getAttribute("data-q"), v = b.getAttribute("data-r");
      if (rep[k] === v) delete rep[k]; else rep[k] = v;
      Array.prototype.slice.call(q.querySelectorAll("[data-r]")).forEach(function (x) {
        x.setAttribute("aria-pressed", rep[k] === x.getAttribute("data-r") ? "true" : "false");
      });
      maj();
    });
  });
})();
