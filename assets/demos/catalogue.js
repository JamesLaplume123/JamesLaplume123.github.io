/* Catalogue : panier détaillé (une fois / par mois), quantités, kits, conseils de Hub, lien de soumission prérempli. */
(function () {
  var form = document.getElementById("ct");
  if (!form) return;
  var $ = function (s, r) { return (r || form).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || form).querySelectorAll(s)); };
  /* Sans prix publics (data-sansprix sur le formulaire) : aucun montant ni total; « une fois » / « par mois » suffisent. */
  var SANS = form.hasAttribute("data-sansprix");
  var fmt = function (n) { return SANS ? "" : String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " $"; };
  var txt = function (el, s) { if (el) el.textContent = s; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  var kit = null; /* kit appliqué : son rabais tient tant que ses pièces et son Hub sont là */
  function qtyOf(el) { var o = el && el.querySelector("output"); return o ? (+o.value || 0) : 0; }
  function setQty(el, v) { var o = el && el.querySelector("output"); if (o) o.value = Math.max(0, v); }
  function h3(el) { var h = el && el.querySelector("h3, b"); return h ? h.textContent.trim() : ""; }

  var pret = false;
  function garde(hubId, n) {
    var F = window.JarvisForfait; if (!F || !pret) return;
    var o = F.lire();
    o.sols = $$('input[name="sol"]:checked:not(:disabled)').map(function (c) { return c.getAttribute("data-slug"); }).filter(Boolean);
    if (o.hub !== hubId) { o.manuel = o.manuel || !!o.hub; o.hub = hubId; }
    o.n = n; F.ecrire(o);
  }
  function compute() {
    var once = [], month = [], tips = [];
    var hubIn = $('input[name="hub"]:checked');
    var hub = hubIn ? hubIn.closest(".ct-hub") : null;
    var hubNom = hub ? h3(hub) : "Hub";
    var hubId = hubIn ? hubIn.value : "";
    var camMax = hubIn ? +hubIn.dataset.cam : 99, appMax = hubIn ? +hubIn.dataset.app : 1e6, autoMax = hubIn ? +hubIn.dataset.autos : 1e6;
    if (hubIn) once.push({ id: "hub", n: hubNom, q: 1, p: +hubIn.dataset.prix, fixed: true });

    /* Solutions */
    var complet = $('input[name="complet"]');
    var sols = $$('input[name="sol"]:not(:disabled)');
    var mobLab = $('.ct-sol[data-sol="mob"]');
    var nVeh = qtyOf(mobLab);
    var hasSecu = false, hasDiag = false, hasMob = false;
    if (complet && complet.checked) {
      month.push({ id: "complet", n: "JARVIS Complet (5 solutions)", q: 1, p: +complet.dataset.prix, kind: "sol" });
      sols.forEach(function (s) { s.checked = true; s.closest(".ct-sol").classList.add("is-locked"); });
      if (mobLab && nVeh < 1) { setQty(mobLab, 1); nVeh = 1; }
      if (nVeh > 1) month.push({ id: "mob", n: "Mobilité, véhicules supplémentaires", q: nVeh - 1, p: +mobLab.querySelector('input[name="sol"]').dataset.prix, kind: "sol" });
      hasSecu = hasDiag = hasMob = true;
    } else {
      sols.forEach(function (s) {
        var lab = s.closest(".ct-sol");
        lab.classList.remove("is-locked");
        if (s.value === "mob") {
          if (s.checked && nVeh < 1) { setQty(lab, 1); nVeh = 1; }
          if (!s.checked && nVeh > 0) { setQty(lab, 0); nVeh = 0; }
          if (s.checked) { month.push({ id: "mob", n: "Mobilité", q: nVeh, p: +s.dataset.prix, unit: "véhicule", kind: "sol" }); hasMob = true; }
          return;
        }
        if (s.checked) {
          month.push({ id: s.value, n: h3(lab), q: 1, p: +s.dataset.prix, kind: "sol" });
          if (s.value === "secu") hasSecu = true;
          if (s.value === "diag") hasDiag = true;
        }
      });
    }
    if (mobLab) mobLab.classList.toggle("is-on", nVeh > 0);

    /* Entreprise */
    var socle = $('input[name="socle"]');
    var recep = $(".ct-ent-recep"), nRecep = qtyOf(recep);
    var toutes = $('input[name="toutes"]');
    var autos = $$('input[name="auto"]');
    var mesure = $(".ct-ent-mesure"), nMesure = qtyOf(mesure);
    var nAutos = 0, entActif = false;
    if (toutes && toutes.checked) {
      autos.forEach(function (a) { a.checked = true; a.closest(".ct-auto").classList.add("is-locked"); });
      month.push({ id: "toutes", n: "Toutes les automatisations (" + autos.length + ")", q: 1, p: +toutes.dataset.prix, kind: "ent" });
      nAutos = autos.length; entActif = true;
    } else {
      autos.forEach(function (a) {
        a.closest(".ct-auto").classList.remove("is-locked");
        if (a.checked) { nAutos++; entActif = true; month.push({ id: a.value, n: a.closest(".ct-auto").querySelector("b").textContent, q: 1, p: +a.dataset.prix, kind: "ent" }); }
      });
    }
    if (nRecep > 0) { entActif = true; month.push({ id: "recep", n: "Réceptionniste IA", q: nRecep, p: +recep.dataset.prix, unit: "ligne", kind: "ent" }); }
    if (nMesure > 0) {
      entActif = true;
      once.push({ id: "mesure", n: "Automatisation sur mesure (construction)", q: nMesure, p: +mesure.dataset.prix });
      month.push({ id: "mesure-m", n: "Automatisation sur mesure", q: nMesure, p: +mesure.dataset.mois, kind: "ent" });
    }
    $$('input[name="veille"]').forEach(function (v) {
      if (v.checked) { entActif = true; month.push({ id: v.value, n: v.closest(".ct-ent").querySelector("h3").textContent, q: 1, p: +v.dataset.prix, kind: "ent" }); }
    });
    if (recep) recep.classList.toggle("is-on", nRecep > 0);
    if (mesure) mesure.classList.toggle("is-on", nMesure > 0);
    var veilleSeule = entActif && nAutos === 0 && nRecep === 0 && nMesure === 0;
    if (entActif && !veilleSeule && socle && !socle.checked) { socle.checked = true; }
    if (socle && socle.checked) month.unshift({ id: "socle", n: "Socle Entreprise", q: 1, p: +socle.dataset.prix, kind: "ent" });
    var socleOn = socle && socle.checked;

    /* Matériel */
    var nApp = 0, nCam = 0, nCapt = 0, hasBoitierVR = false, hasBoitierMob = false;
    $$(".ct-item").forEach(function (it) {
      var q = qtyOf(it);
      it.classList.toggle("is-on", q > 0);
      if (q > 0) {
        once.push({ id: it.dataset.id, n: it.querySelector("b").textContent, q: q, p: +it.dataset.prix });
        if (it.dataset.svc) return;
        nApp += q;
        if (it.dataset.cam) nCam += q;
        if (it.closest(".ct-cat").querySelector("h3").textContent === "Capteurs") nCapt += q;
        if (/^vr[bsp]$/.test(it.dataset.id)) hasBoitierVR = true;
        if (it.dataset.id === "mobb") hasBoitierMob = true;
      }
    });

    /* Rabais du kit */
    if (kit) {
      var ok = hubId === kit.hub && Object.keys(kit.mat).every(function (id) { return qtyOf($('.ct-item[data-id="' + id + '"]')) >= kit.mat[id]; });
      if (ok) once.push({ id: "kit", n: "Rabais " + kit.nom + " (−8 %)", q: 1, p: -kit.rabais, fixed: true });
      else kit = null;
    }

    /* Installation */
    var inst = $('input[name="install"]:checked');
    if (inst && +inst.dataset.prix > 0) once.push({ id: "install", n: h3(inst.closest(".ct-inst")) + (inst.value === "place" ? " (3 h, estimation)" : ""), q: 1, p: +inst.dataset.prix, fixed: true });

    /* Deuxième lieu */
    var rang = $('select[name="rang"]');
    var rabais = rang && rang.value === "2" ? 0.3 : 0;
    var monthBrut = month.reduce(function (s, l) { return s + l.q * l.p; }, 0);
    var monthRab = 0;
    if (rabais) {
      monthRab = month.filter(function (l) { return l.kind === "sol"; }).reduce(function (s, l) { return s + l.q * l.p; }, 0) * rabais;
    }
    var totOnce = once.reduce(function (s, l) { return s + l.q * l.p; }, 0);
    var totMonth = monthBrut - monthRab;

    /* Conseils */
    if (nCam > camMax) tips.push({ t: hubNom + " analyse " + camMax + " caméras; vous en avez " + nCam + ".", up: hubId === "base" ? "signature" : "platinum" });
    if (nApp > appMax) tips.push({ t: hubNom + " relie " + appMax + " appareils; vous en avez " + nApp + ".", up: hubId === "base" ? "signature" : "platinum" });
    if (hubId === "base" && (socleOn || entActif)) tips.push({ t: "Les automatisations d’entreprise et la réceptionniste demandent un Hub Signature ou Platinum.", up: "signature" });
    else if (nAutos > autoMax) tips.push({ t: hubNom + " fait tourner " + autoMax + " automatisations; vous en avez " + nAutos + ".", up: "platinum" });
    if (hasSecu && nCam === 0) tips.push({ t: "Sécurité intelligente sans caméra : ajoutez au moins une caméra ou une sonnette." });
    if (hasDiag && nCapt === 0 && !hasBoitierVR) tips.push({ t: "Diagnostic sans capteur : ajoutez au moins un capteur (fuite, température, porte)." });
    if (hasMob && !hasBoitierMob && !hasBoitierVR) tips.push({ t: complet && complet.checked
      ? "JARVIS Complet comprend Mobilité pour un véhicule : ajoutez un Boîtier Mobilité pour en profiter."
      : "Mobilité a besoin d’un Boîtier Mobilité (voiture) ou d’un Boîtier VR Signature ou Platinum (GPS)." });
    if (hubId === "base" && once.some(function (l) { return l.id === "vrs" || l.id === "vrp"; })) tips.push({ t: "Le Boîtier VR Signature ou Platinum donne tout son sens avec un Hub Signature (IA locale, 4G).", up: "signature" });

    render(once, month, monthRab, totOnce, totMonth, hubNom, tips, rabais);
    garde(hubId, once.length + month.length);
  }

  function line(l) {
    var sub = fmt(l.q * l.p);
    var q = l.q > 1 || l.unit ? '<i>' + l.q + "× " + (l.unit ? l.unit + (l.q > 1 ? "s" : "") + (SANS ? "" : " · ") : "") + fmt(l.p) + "</i>" : "";
    var rm = l.fixed ? "" : '<button type="button" data-rm="' + esc(l.id) + '" aria-label="Retirer">×</button>';
    return '<li class="' + (l.p < 0 ? "is-rab" : "") + '"><span><b>' + esc(l.n) + "</b>" + q + "</span><em>" + sub + "</em>" + rm + "</li>";
  }

  function render(once, month, monthRab, totOnce, totMonth, hubNom, tips, rabais) {
    txt($("[data-cart-nom]"), hubNom);
    var lo = $("[data-cart-once]"), lm = $("[data-cart-month]");
    lo.innerHTML = once.map(line).join("");
    lm.innerHTML = month.length ? month.map(line).join("") + (monthRab ? '<li class="is-rab"><span><b>Deuxième lieu : −30 % sur les solutions</b></span><em>' + (SANS ? "" : "−" + fmt(monthRab)) + "</em></li>" : "")
      : '<li class="is-vide">Aucune solution payante. JARVIS fonctionne chez vous; ajoutez une solution pour l’accès de partout et les alertes.</li>';
    txt($("[data-cart-once-sub]"), fmt(totOnce));
    txt($("[data-cart-month-sub]"), fmt(totMonth));
    $$("[data-total-once]", document).forEach(function (e) { e.textContent = fmt(totOnce); });
    $$("[data-total-month]", document).forEach(function (e) { e.textContent = fmt(totMonth); });
    txt($("[data-total-year]"), fmt(totOnce + 12 * totMonth));
    var n = once.length + month.length;
    txt($("[data-cart-count]"), n ? " · " + n : "");

    var tb = $("[data-cart-tips]");
    if (tips.length) {
      tb.hidden = false;
      tb.innerHTML = "<h4>Conseils</h4>" + tips.map(function (t) {
        return "<p>" + esc(t.t) + (t.up ? ' <button type="button" data-up="' + t.up + '">Passer au Hub ' + t.up.charAt(0).toUpperCase() + t.up.slice(1) + "</button>" : "") + "</p>";
      }).join("");
    } else { tb.hidden = true; tb.innerHTML = ""; }

    var lines = once.concat(month).map(function (l) { return (l.q > 1 ? l.q + "× " : "") + l.n; });
    /* Les lieux choisis ouvrent le récapitulatif envoyé avec la demande de soumission. */
    try {
      var Fo = window.JarvisForfait && window.JarvisForfait.lire(), Ld = JSON.parse(document.querySelector("[data-lieux-data]").textContent);
      var noms = (Fo ? Fo.lieux : []).map(function (id) { return Ld[id] && Ld[id].nom; }).filter(Boolean);
      if (noms.length) lines.unshift("Lieu : " + noms.join(", "));
    } catch (x) {}
    var link = $("[data-total-link]");
    if (link) link.href = "/contact/?config=" + encodeURIComponent(lines.join(" + ") + (rabais ? " | 2e lieu" : "") + (SANS ? "" : " | " + fmt(totOnce) + " une fois, " + fmt(totMonth) + " par mois"));
  }

  /* Retirer une ligne du panier */
  function remove(id) {
    var el;
    if (id === "complet") { $('input[name="complet"]').checked = false; $$('input[name="sol"]:not(:disabled)').forEach(function (s) { s.checked = false; }); setQty($('.ct-sol[data-sol="mob"]'), 0); }
    else if (id === "mob") { setQty($('.ct-sol[data-sol="mob"]'), 0); el = $('input[name="sol"][value="mob"]'); if (el) el.checked = false; }
    else if ((el = $('input[name="sol"][value="' + id + '"]'))) el.checked = false;
    else if (id === "toutes") { $('input[name="toutes"]').checked = false; $$('input[name="auto"]').forEach(function (a) { a.checked = false; }); }
    else if (id === "socle") { $('input[name="socle"]').checked = false; $('input[name="toutes"]').checked = false; $$('input[name="auto"]').forEach(function (a) { a.checked = false; }); setQty($(".ct-ent-recep"), 0); setQty($(".ct-ent-mesure"), 0); }
    else if ((el = $('input[name="auto"][value="' + id + '"]'))) el.checked = false;
    else if ((el = $('input[name="veille"][value="' + id + '"]'))) el.checked = false;
    else if (id === "recep") setQty($(".ct-ent-recep"), 0);
    else if (id === "mesure" || id === "mesure-m") setQty($(".ct-ent-mesure"), 0);
    else if ((el = $('.ct-item[data-id="' + id + '"]'))) setQty(el, 0);
    compute();
  }

  function applyKit(cfg) {
    kit = cfg;
    var hub = $('input[name="hub"][value="' + cfg.hub + '"]'); if (hub) hub.checked = true;
    $$(".ct-item").forEach(function (it) { setQty(it, 0); });
    Object.keys(cfg.mat || {}).forEach(function (id) { var it = $('.ct-item[data-id="' + id + '"]'); if (it) setQty(it, cfg.mat[id]); });
    var complet = $('input[name="complet"]'); if (complet) complet.checked = (cfg.sol || []).indexOf("complet") >= 0;
    $$('input[name="sol"]:not(:disabled)').forEach(function (s) { s.checked = (cfg.sol || []).indexOf(s.value) >= 0; });
    setQty($('.ct-sol[data-sol="mob"]'), (cfg.sol || []).indexOf("mob") >= 0 || complet.checked ? 1 : 0);
    var e = cfg.ent || {};
    $('input[name="socle"]').checked = !!e.socle;
    $('input[name="toutes"]').checked = !!e.toutes;
    setQty($(".ct-ent-recep"), e.recep || 0);
    setQty($(".ct-ent-mesure"), 0);
    $$('input[name="auto"]').forEach(function (a) { a.checked = (e.autos || []).indexOf(a.value) >= 0; });
    $$('input[name="veille"]').forEach(function (v) { v.checked = (e.veille || []).indexOf(v.value) >= 0; });
    $('input[name="install"][value="auto"]').checked = true;
    compute();
    var cart = $(".ct-cart");
    if (cart) { cart.classList.add("is-flash"); setTimeout(function () { cart.classList.remove("is-flash"); }, 900); }
    if (window.matchMedia("(max-width: 960px)").matches) { form.classList.add("is-cart"); document.body.classList.add("ct-lock"); }
  }

  form.addEventListener("change", function (e) {
    if (e.target.name === "toutes" && e.target.checked) $('input[name="socle"]').checked = true;
    compute();
  });
  form.addEventListener("click", function (e) {
    var b = e.target.closest("[data-q]");
    if (b) {
      var box = b.closest(".ct-item, .ct-ent, .ct-sol"); setQty(box, qtyOf(box) + (+b.dataset.q));
      var cb = box.querySelector('input[name="sol"]'); if (cb) cb.checked = qtyOf(box) > 0;
      compute(); e.preventDefault(); return;
    }
    var rm = e.target.closest("[data-rm]");
    if (rm) { remove(rm.dataset.rm); return; }
    var up = e.target.closest("[data-up]");
    if (up) { var h = $('input[name="hub"][value="' + up.dataset.up + '"]'); if (h) { h.checked = true; compute(); } return; }
    var kg = e.target.closest("[data-kit-go]");
    if (kg) { var kb2 = $$("[data-kit]")[+kg.dataset.kitGo - 1]; if (kb2) { applyKit(JSON.parse(kb2.dataset.kit)); kb2.closest(".ct-kit").scrollIntoView({ behavior: "smooth", block: "center" }); } return; }
    var k = e.target.closest("[data-kit]");
    if (k) { e.preventDefault(); applyKit(JSON.parse(k.dataset.kit)); return; }
    if (e.target.closest("[data-cart-open]")) { form.classList.add("is-cart"); document.body.classList.add("ct-lock"); return; }
    if (e.target.closest("[data-cart-close]")) { form.classList.remove("is-cart"); document.body.classList.remove("ct-lock"); return; }
  });
  /* Arrivée avec ?kit=N (depuis L'offre) : le kit est appliqué et la page s'ouvre dessus. */
  var kq = +(new URLSearchParams(location.search).get("kit") || 0);
  var kb = kq ? $$("[data-kit]")[kq - 1] : null;
  if (kb) { applyKit(JSON.parse(kb.dataset.kit)); form.classList.remove("is-cart"); document.body.classList.remove("ct-lock"); setTimeout(function () { kb.closest(".ct-kit").scrollIntoView({ block: "center" }); }, 60); }
  else { depuisForfait(); compute(); }
  pret = true; compute();

  /* Le forfait bâti en chemin (clé « jarvis-forfait », assets/js/wow.js) : le Hub conseillé pour le lieu et
     les solutions ajoutées sont déjà cochés à l'arrivée; chaque changement ici est gardé de la même façon. */
  function depuisForfait() {
    var F = window.JarvisForfait; if (!F) return;
    var o = F.lire();
    if (o.hub) { var h = $('input[name="hub"][value="' + o.hub + '"]'); if (h) h.checked = true; }
    o.sols.forEach(function (slug) { coche(slug, true); });
  }
  function coche(slug, oui) {
    var cb = $('input[name="sol"][data-slug="' + slug + '"]'); if (!cb || cb.disabled) return;
    cb.checked = oui;
    var box = cb.closest(".ct-sol"); if (box && cb.hasAttribute("data-qty")) setQty(box, oui ? Math.max(1, qtyOf(box)) : 0);
  }
  document.addEventListener("jarvis:forfait", function (e) {
    var F = window.JarvisForfait, d = e.detail || {}; if (!F) return;
    if (d.lieu) {
      var o = F.lire(), data = document.querySelector("[data-lieux-data]"), L = {};
      try { L = JSON.parse(data.textContent); } catch (x) {}
      if (o.hub) { var h = $('input[name="hub"][value="' + o.hub + '"]'); if (h) h.checked = true; }
      if (d.ajoute && L[d.lieu]) L[d.lieu].sols.forEach(function (x) { coche(x.slug, true); });
    }
    compute();
  });
})();
