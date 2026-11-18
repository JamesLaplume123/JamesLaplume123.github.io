/* Coquille « logiciel » des pages de solution : météo réelle dans l'en-tête
   avec le même cache de session que la démo de l'app. */
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

  /* ---------- Le cadre tient dans la fenêtre ----------
     Hauteur disponible : la fenêtre moins la barre du site (et le menu de sections s'il y en a un). Le cadre est
     presque jamais réduit (94 % au plus petit, pour rester lisible); ce qui dépasse défile à l'intérieur. */
  var coques = Array.prototype.slice.call(document.querySelectorAll("[data-xs]"));
  function tient() {
    var toc = document.querySelector(".toc");
    /* Sous la barre du site et la barre des sections, avec de l'air en haut et en bas. */
    var dispo = window.innerHeight - 66 - (toc ? toc.offsetHeight : 0) - 52;
    coques.forEach(function (xs) {
      var ecran = xs.querySelector(".xs-screen"), main = xs.querySelector(".xs-main"), cote = xs.querySelector(".xs-side");
      if (!ecran || !main) return;
      [ecran, main, cote].forEach(function (e) { if (e) e.style.maxHeight = ""; });
      xs.style.zoom = "";
      if (window.innerWidth <= 900) return;
      var nat = Math.max(main.scrollHeight, cote ? cote.scrollHeight : 0);
      /* Taille réelle (ou presque) : le contenu défile à l'intérieur plutôt que d'être rapetissé. */
      var z = Math.max(.94, Math.min(1, dispo / nat));
      if (z < 1) xs.style.zoom = z.toFixed(4);
      var max = Math.floor(dispo / z) + "px";
      [ecran, main, cote].forEach(function (e) { if (e) e.style.maxHeight = max; });
    });
  }
  /* Arrivée propre sur la démo (« Essayer », #jarvis) : le cadre se pose juste sous les barres, en entier. */
  function pose(xs, doux) {
    var toc = document.querySelector(".toc"), bar = document.querySelector(".bar");
    var haut = (bar ? bar.offsetHeight : 66) + (toc ? toc.offsetHeight : 0) + 16;
    var y = xs.getBoundingClientRect().top + window.scrollY - haut;
    window.scrollTo({ top: Math.max(0, y), behavior: doux ? "smooth" : "auto" });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var cible = document.getElementById(a.getAttribute("href").slice(1));
    if (!cible || !cible.hasAttribute("data-xs")) return;
    e.preventDefault();
    tient();
    var doux = !(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
    pose(cible, doux);
    setTimeout(function () { pose(cible, false); }, doux ? 700 : 50);   /* rattrape un réajustement de la page */
    if (history.replaceState) history.replaceState(null, "", "#" + cible.id);
  });
  if (coques.length) {
    tient();
    window.addEventListener("resize", tient);
    window.addEventListener("load", function () {
      tient();
      var c = location.hash && document.getElementById(location.hash.slice(1));
      if (c && c.hasAttribute("data-xs")) pose(c, false);
    });
  }
})();
