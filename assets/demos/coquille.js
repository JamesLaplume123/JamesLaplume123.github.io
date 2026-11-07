/* Coquille « logiciel » des pages de solution : météo réelle de Saint-Hyacinthe dans l'en-tête
   (Environnement Canada), avec le même cache de session que la démo de l'app. */
(function () {
  "use strict";
  var root = document.querySelector("[data-xs]");
  if (!root) return;
  // Arrivée par un lien d'extension (#jarvis) : la page s'ouvre dans JARVIS, et le reste
  // même si des images plus haut finissent de se charger après le saut.
  if (location.hash === "#jarvis") {
    var moved = false, stop = function () { moved = true; };
    ["wheel", "touchstart", "keydown"].forEach(function (e) { addEventListener(e, stop, { once: true, passive: true }); });
    var land = function () {
      if (moved) return;
      var y = root.getBoundingClientRect().top - 72;
      if (Math.abs(y) > 2) scrollTo({ top: scrollY + y, behavior: "instant" });
    };
    land();
    addEventListener("load", function () { land(); setTimeout(land, 350); }, { once: true });
  }
  var EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/qc-22?f=json&lang=fr";
  function txt(o) {
    if (o == null) return "";
    if (typeof o === "string") return o;
    if (o.fr !== undefined) return o.fr;
    if (o.value !== undefined) return txt(o.value);
    return o.en || "";
  }
  function num(o) { var n = parseFloat(txt(o)); return isFinite(n) ? n : null; }
  function paint(j) {
    var cc = (j.properties || {}).currentConditions || {};
    var t = num(cc.temperature), cond = txt(cc.condition).toLowerCase(), code = num(cc.iconCode);
    if (t === null) throw new Error("température absente");
    var night = code !== null && code >= 30 && code <= 39, kind = "cloud";
    if (/neige|flocon|poudrerie|gr[eé]sil/.test(cond)) kind = "snow";
    else if (/pluie|averse|bruine|orage/.test(cond)) kind = "rain";
    else if (/brouillard|brume/.test(cond)) kind = "fog";
    else if (/d[eé]gag|ensoleill|soleil/.test(cond)) kind = night ? "moon" : "sun";
    root.setAttribute("data-wx", kind);
    root.setAttribute("data-wx-state", "on");
    var r = Math.round(t), el = root.querySelector('[data-xs="temp"]');
    if (el) el.textContent = r < 0 ? "−" + Math.abs(r) : String(r);
  }
  var ss = null, cached = null;
  try { ss = window.sessionStorage; var c = JSON.parse(ss.getItem("jarvis-ec") || "null"); if (c && Date.now() - c.t < 300000) cached = c.j; } catch (e) {}
  (cached ? Promise.resolve(cached) : fetch(EC_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (j) { try { ss && ss.setItem("jarvis-ec", JSON.stringify({ t: Date.now(), j: j })); } catch (e) {} return j; }))
    .then(paint)
    .catch(function () { root.setAttribute("data-wx-state", "off"); });
})();
