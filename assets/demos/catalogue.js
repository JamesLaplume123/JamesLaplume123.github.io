/* Catalogue : total en direct (une fois / par mois), quantités, kits, lien de soumission prérempli. */
(function () {
  var form = document.getElementById("ct");
  if (!form) return;
  var $ = function (s, r) { return (r || form).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || form).querySelectorAll(s)); };
  var fmt = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " $"; };

  function hubName() {
    var r = $('input[name="hub"]:checked');
    var lab = r && r.closest(".ct-hub");
    return lab ? lab.querySelector("h3").textContent : "Hub";
  }

  function compute() {
    var once = 0, month = 0, nSol = 0, nMat = 0, lines = [];
    var hub = $('input[name="hub"]:checked');
    if (hub) { once += +hub.dataset.prix; lines.push(hubName()); }

    var complet = $('input[name="complet"]');
    var sols = $$('input[name="sol"]:not(:disabled)');
    if (complet && complet.checked) {
      month += +complet.dataset.prix; nSol = sols.length; lines.push("JARVIS Complet");
      sols.forEach(function (s) { s.checked = true; s.closest(".ct-sol").classList.add("is-locked"); });
    } else {
      sols.forEach(function (s) {
        s.closest(".ct-sol").classList.remove("is-locked");
        if (s.checked) { month += +s.dataset.prix; nSol++; lines.push(s.closest(".ct-sol").querySelector("h3").textContent); }
      });
    }
    var ent = $('input[name="ent"]:checked');
    if (ent && ent.value) { month += +ent.dataset.prix; lines.push(ent.closest(".ct-ent").querySelector("h3").textContent); }

    var rang = $('select[name="rang"]');
    if (rang && rang.value === "2") month = month * 0.7;

    $$(".ct-item").forEach(function (it) {
      var q = +it.querySelector("output").value || 0;
      it.classList.toggle("is-on", q > 0);
      if (q > 0) { once += q * +it.dataset.prix; nMat += q; lines.push(q + "× " + it.querySelector("b").textContent); }
    });

    $("[data-total-nom]").textContent = hubName();
    $("[data-total-detail]").textContent = nSol + (nSol > 1 ? " solutions" : " solution") + " · " + nMat + (nMat > 1 ? " appareils" : " appareil") + (rang && rang.value === "2" ? " · 2e lieu −30 %" : "");
    $("[data-total-once]").textContent = fmt(once);
    $("[data-total-month]").textContent = fmt(month);
    var link = $("[data-total-link]");
    if (link) link.href = "/contact/?config=" + encodeURIComponent(lines.join(" + ") + " | " + fmt(once) + " une fois, " + fmt(month) + "/mois");
  }

  form.addEventListener("change", compute);
  form.addEventListener("click", function (e) {
    var b = e.target.closest("[data-q]");
    if (b) {
      var out = b.parentNode.querySelector("output");
      out.value = Math.max(0, (+out.value || 0) + (+b.dataset.q));
      compute();
      return;
    }
    var k = e.target.closest("[data-kit]");
    if (k) {
      e.preventDefault();
      var cfg = JSON.parse(k.dataset.kit);
      var hub = $('input[name="hub"][value="' + cfg.hub + '"]'); if (hub) hub.checked = true;
      $$(".ct-item output").forEach(function (o) { o.value = 0; });
      Object.keys(cfg.mat || {}).forEach(function (id) {
        var it = $('.ct-item[data-id="' + id + '"]'); if (it) it.querySelector("output").value = cfg.mat[id];
      });
      var complet = $('input[name="complet"]'); if (complet) complet.checked = (cfg.sol || []).indexOf("complet") >= 0;
      $$('input[name="sol"]:not(:disabled)').forEach(function (s) { s.checked = (cfg.sol || []).indexOf(s.value) >= 0; });
      var ent = $('input[name="ent"][value="' + (cfg.ent || "") + '"]'); if (ent) ent.checked = true;
      compute();
      var hubSec = document.getElementById("hub");
      if (hubSec) hubSec.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
  compute();
})();
