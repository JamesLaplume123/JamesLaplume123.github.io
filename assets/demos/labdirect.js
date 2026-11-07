/* Accueil : batteries de l'ambulance en direct dans la section du laboratoire mobile.
   Lit la même source que le tableau complet (Worker → Home Assistant, lecture seule),
   seulement quand la section est à l'écran, toutes les 10 secondes. */
(function () {
  "use strict";
  var root = document.querySelector("[data-labdirect]");
  var API = document.documentElement.getAttribute("data-api");
  if (!root) return;
  function $(k) { return document.querySelector('[data-ld="' + k + '"]'); }
  function color(soc) { return soc >= 60 ? "#34d399" : soc >= 30 ? "#fbbf24" : "#f87171"; }
  var bats = root.querySelectorAll(".ld-bat"), timer = 0, visible = false, last = null;
  function fmt(n, d) { return n.toFixed(d).replace(".", ","); }
  function off(text) {
    root.classList.add("is-off");
    $("state").textContent = text;
  }
  function paint(d) {
    last = d;
    root.classList.remove("is-off");
    ["a", "b"].forEach(function (k, i) {
      var b = d.batteries[i];
      if (!b || b.soc < 0) { $(k).textContent = "--"; return; }
      $(k).textContent = Math.round(b.soc);
      bats[i].style.setProperty("--ld-c", color(b.soc));
    });
    if (d.total && d.total.kwh > 0) {
      $("kwh").textContent = fmt(d.total.kwh, 1);
      $("unit").textContent = "kWh";
      $("kwh-l").textContent = "En réserve";
    }
    var w = d.total ? d.total.w : 0, charging = d.batteries.some(function (b) { return b.charging; });
    $("state").textContent = "Mesuré à l’instant · " + (charging ? "en charge" : Math.abs(w) > 5 ? fmt(Math.abs(w), 0) + " W consommés" : "au repos") + " · Home Assistant de l’ambulance";
  }
  function load() {
    if (!API) { off("Liaison en installation"); return; }
    fetch(API + "/live", { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { if (!d.ok || !d.batteries) throw new Error("ko"); paint(d); })
      .catch(function () { off(last ? "Liaison interrompue · dernières valeurs" : "Liaison momentanément indisponible"); });
  }
  if (!("IntersectionObserver" in window)) { load(); return; }
  new IntersectionObserver(function (es) {
    visible = es[0].isIntersecting;
    if (visible) { load(); if (!timer) timer = setInterval(function () { if (visible && !document.hidden) load(); }, 10000); }
  }, { rootMargin: "200px 0px" }).observe(root);
})();
