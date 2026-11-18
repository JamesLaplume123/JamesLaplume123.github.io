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
  /* Le formulaire écrit dans le forfait (clé « jarvis-forfait », assets/js/wow.js) : le Hub, les solutions,
     les lignes de matériel et de services (« autres ») et son propre état (« etat »), pour le retrouver tel
     quel au retour. L'affichage du forfait (colonne et tiroir) est fait par wow.js, le même partout. */
  function etatForm() {
    var c = $$('input[type="checkbox"]:checked:not(:disabled), input[type="radio"]:checked')
      .filter(function (i) { return i.name && ["hub", "sol"].indexOf(i.name) < 0; }).map(function (i) { return i.name + "=" + i.value; });
    var q = {};
    $$(".ct-item[data-id]").forEach(function (it) { var v = qtyOf(it); if (v) q[it.dataset.id] = v; });
    QTES.forEach(function (p) { var v = qtyOf($(p[1])); if (v) q[p[0]] = v; });
    return { c: c, q: q };
  }
  var QTES = [["sol:mob", '.ct-sol[data-sol="mob"]'], ["recep", ".ct-ent-recep"], ["mesure", ".ct-ent-mesure"]];
  function poseEtat(e) {
    if (!e || !e.c) return;
    $$('input[type="checkbox"], input[type="radio"]').forEach(function (i) {
      if (!i.name || i.disabled || ["hub", "sol"].indexOf(i.name) >= 0) return;
      i.checked = e.c.indexOf(i.name + "=" + i.value) >= 0;
    });
    if (!$('input[name="install"]:checked')) { var ia = $('input[name="install"][value="auto"]'); if (ia) ia.checked = true; }
    $$(".ct-item[data-id]").forEach(function (it) { setQty(it, (e.q || {})[it.dataset.id] || 0); });
    QTES.forEach(function (p) { setQty($(p[1]), (e.q || {})[p[0]] || 0); });
  }
  function garde(hubId, autres, suffixe) {
    var F = window.JarvisForfait; if (!F || !pret) return;
    var o = F.lire();
    o.sols = $$('input[name="sol"]:checked:not(:disabled)').map(function (c) { return c.getAttribute("data-slug"); }).filter(Boolean);
    o.hub = hubId; o.autres = autres; o.etat = etatForm(); o.suffixe = suffixe;
    F.ecrire(o);
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

    render(month, monthRab, totOnce, totMonth, tips);
    /* Les lignes hors lieux et hors solutions à l'unité : matériel (quantité réglable), services, entreprise. */
    var autres = [];
    once.forEach(function (l) {
      if (l.id === "hub" || (SANS && l.p < 0)) return;
      var it = $('.ct-item[data-id="' + l.id + '"]'), mat = !!it && !it.hasAttribute("data-svc");
      autres.push({ id: l.id, n: l.n, q: l.q, k: mat ? "mat" : l.fixed ? "fixe" : "autre", s: "Une fois", px: fmt(l.q * l.p), img: it ? it.getAttribute("data-img") || "" : "" });
    });
    month.forEach(function (l) {
      if (l.kind === "sol") { if (l.id === "complet") autres.push({ id: "complet", n: l.n, q: 1, k: "lot", px: fmt(l.p) }); return; }
      autres.push({ id: l.id, n: l.n, q: l.q, k: "autre", s: (l.q > 1 ? l.q + " " + (l.unit ? l.unit + "s" : "") + " · " : "") + "Par mois", px: fmt(l.q * l.p) });
    });
    garde(hubId, autres, (rabais ? " | 2e lieu" : "") + (SANS ? "" : " | " + fmt(totOnce) + " une fois, " + fmt(totMonth) + " par mois"));
  }

  /* Sur la page : les totaux (quand les prix sont publics), les « À prévoir », et les solutions utiles aux
     lieux choisis, signalées sans jamais être cochées d'office. La liste du forfait, elle, est dessinée par wow.js. */
  function render(month, monthRab, totOnce, totMonth, tips) {
    var Fo = window.JarvisForfait && window.JarvisForfait.lire(), Ld = {};
    try { Ld = JSON.parse(document.querySelector("[data-lieux-data]").textContent); } catch (x) {}
    var utiles = {};
    (Fo ? Fo.lieux : []).forEach(function (id) { if (Ld[id]) Ld[id].sols.forEach(function (x) { utiles[x.slug] = 1; }); });
    $$('input[name="sol"][data-slug]').forEach(function (c) { var bx = c.closest(".ct-sol"); if (bx) bx.classList.toggle("is-conseil", !!utiles[c.getAttribute("data-slug")] && !c.disabled); });
    $$("[data-total-once]", document).forEach(function (e) { e.textContent = fmt(totOnce); });
    $$("[data-total-month]", document).forEach(function (e) { e.textContent = fmt(totMonth); });
    txt($("[data-total-year]"), fmt(totOnce + 12 * totMonth));
    var tb = $("[data-cart-tips]");
    if (tips.length) {
      tb.hidden = false;
      tb.innerHTML = "<h4>À prévoir</h4>" + tips.map(function (t) {
        return "<p>" + esc(t.t) + (t.up ? ' <button type="button" data-up="' + t.up + '">Passer au Hub ' + t.up.charAt(0).toUpperCase() + t.up.slice(1) + "</button>" : "") + "</p>";
      }).join("");
    } else { tb.hidden = true; tb.innerHTML = ""; }
  }

  /* Retirer une ligne du panier */
  function remove(id) {
    var el;
    if (id === "hub") { $$('input[name="hub"]').forEach(function (h) { h.checked = false; }); var Fh = window.JarvisForfait; if (Fh) { var oh = Fh.lire(); oh.manuel = false; oh.hub = ""; Fh.ecrire(oh); } }
    else if (id === "complet") { $('input[name="complet"]').checked = false; $$('input[name="sol"]:not(:disabled)').forEach(function (s) { s.checked = false; }); setQty($('.ct-sol[data-sol="mob"]'), 0); }
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
    if (window.JarvisForfait && window.matchMedia("(max-width: 960px)").matches) window.JarvisForfait.ouvre();
  }

  form.addEventListener("change", function (e) {
    if (e.target.name === "toutes" && e.target.checked) $('input[name="socle"]').checked = true;
    if (e.target.name === "hub") { var Fm = window.JarvisForfait; if (Fm) { var om = Fm.lire(); om.manuel = true; om.hub = e.target.value; Fm.ecrire(om); } }
    compute();
  });
  form.addEventListener("click", function (e) {
    var b = e.target.closest("[data-q]");
    if (b) {
      var box = b.closest(".ct-item, .ct-ent, .ct-sol"); setQty(box, qtyOf(box) + (+b.dataset.q));
      var cb = box.querySelector('input[name="sol"]'); if (cb) cb.checked = qtyOf(box) > 0;
      compute(); e.preventDefault(); return;
    }
    var up = e.target.closest("[data-up]");
    if (up) { var h = $('input[name="hub"][value="' + up.dataset.up + '"]'); if (h) { h.checked = true; compute(); } return; }
    var kg = e.target.closest("[data-kit-go]");
    if (kg) { var kb2 = $$("[data-kit]")[+kg.dataset.kitGo - 1]; if (kb2) { applyKit(JSON.parse(kb2.dataset.kit)); kb2.closest(".ct-kit").scrollIntoView({ behavior: "smooth", block: "center" }); } return; }
    var k = e.target.closest("[data-kit]");
    if (k) { e.preventDefault(); applyKit(JSON.parse(k.dataset.kit)); return; }
  });
  /* Arrivée avec ?kit=N (depuis L'offre) : le kit est appliqué et la page s'ouvre dessus. */
  var kq = +(new URLSearchParams(location.search).get("kit") || 0);
  var kb = kq ? $$("[data-kit]")[kq - 1] : null;
  if (kb) { applyKit(JSON.parse(kb.dataset.kit)); setTimeout(function () { kb.closest(".ct-kit").scrollIntoView({ block: "center" }); }, 60); }
  else { depuisForfait(); compute(); }
  function vider() {
    var F = window.JarvisForfait, o = F ? F.lire() : null;
    kit = null; form.reset();
    $$('input[name="hub"]').forEach(function (h) { h.checked = false; });
    $$(".ct-item, .ct-ent, .ct-sol").forEach(function (x) { setQty(x, 0); });
    if (F) F.ecrire({ lieux: [], sols: [], hub: "", manuel: false, public: o.public, separee: false, autres: [], etat: null });
    compute();
  }
  /* Ce que le tiroir du forfait (wow.js) peut demander au formulaire. */
  window.JarvisCatalogue = {
    retire: remove,
    qte: function (id, d) { var it = $('.ct-item[data-id="' + id + '"]'); if (it) { setQty(it, qtyOf(it) + d); compute(); } },
    vider: vider
  };
  pret = true; compute();

  /* Le forfait bâti en chemin (clé « jarvis-forfait », assets/js/wow.js) : le Hub conseillé pour le lieu et
     les solutions ajoutées sont déjà cochés à l'arrivée; chaque changement ici est gardé de la même façon. */
  function depuisForfait() {
    var F = window.JarvisForfait; if (!F) return;
    var o = F.lire();
    poseEtat(o.etat);
    $$('input[name="hub"]').forEach(function (r) { r.checked = r.value === o.hub; });
    /* Les solutions du forfait font foi (elles peuvent avoir changé ailleurs sur le site). */
    if (!$('input[name="complet"]:checked')) $$('input[name="sol"][data-slug]:not(:disabled)').forEach(function (c) { coche(c.getAttribute("data-slug"), o.sols.indexOf(c.getAttribute("data-slug")) >= 0); });
  }
  function coche(slug, oui) {
    var cb = $('input[name="sol"][data-slug="' + slug + '"]'); if (!cb || cb.disabled) return;
    cb.checked = oui;
    var box = cb.closest(".ct-sol"); if (box && cb.hasAttribute("data-qty")) setQty(box, oui ? Math.max(1, qtyOf(box)) : 0);
  }
  document.addEventListener("jarvis:forfait", function (e) {
    var F = window.JarvisForfait, d = e.detail || {}; if (!F) return;
    var o = F.lire();
    if (d.lieu || d.public) $$('input[name="hub"]').forEach(function (r) { r.checked = r.value === o.hub; });
    if (d.sol) coche(d.sol, !!d.ajoute);
    compute();
  });

  /* Le Hub choisi, en grand à gauche : suit le choix (clic, lieu choisi, kit, forfait rechargé). */
  var vis = document.querySelector("[data-ct-vis]");
  if (vis) {
    var visData = {};
    try { visData = JSON.parse(vis.querySelector("[data-vis-data]").textContent); } catch (e) {}
    var montre = function () {
      var c = document.querySelector('input[name="hub"]:checked');
      var id = c ? c.value : "signature";
      vis.querySelectorAll("[data-v]").forEach(function (im) { im.classList.toggle("is-on", im.getAttribute("data-v") === id); });
      if (visData[id]) {
        vis.querySelector("[data-vis-nom]").textContent = visData[id][0];
        vis.querySelector("[data-vis-ligne]").textContent = visData[id][1];
      }
    };
    document.addEventListener("change", function (e) { if (e.target && e.target.name === "hub") montre(); });
    document.addEventListener("jarvis:forfait", function () { setTimeout(montre, 0); });
    document.addEventListener("click", function () { setTimeout(montre, 60); });
    montre();
  }
})();
