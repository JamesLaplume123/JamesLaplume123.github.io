/* L'offre en trois étapes (docs/OFFRE.md) : 1) vos lieux, 2) votre niveau, 3) votre projet.
   L'étape 1 (« Votre écosystème ») est dessinée par assets/js/wow.js, qui tient aussi le forfait (clé
   « jarvis-forfait ») et son tiroir. Ce fichier tient le formulaire :
     - le niveau choisi et les extensions qu'il comprend (cochées d'office, « Incluse »);
     - l'ensemble de départ de chaque lieu (ajouté ou retiré d'un geste; le Boîtier VR suit le niveau);
     - les quantités, les « À prévoir », et ce qui part dans le forfait pour la soumission.
   Le client ne décide que ses lieux et son niveau; tout le reste est proposé, puis ajusté. */
(function () {
  "use strict";
  var form = document.getElementById("ct");
  if (!form) return;
  var $ = function (s, r) { return (r || form).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || form).querySelectorAll(s)); };
  /* Sans prix publics (data-sansprix sur le formulaire) : aucun montant ni total; « une fois » / « par mois » suffisent. */
  var SANS = form.hasAttribute("data-sansprix");
  var fmt = function (n) { return SANS ? "" : String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " $"; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var maj = function (s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : ""; };

  var OFFRE = { niveaux: {}, ensembles: {} }, LIEUX = {};
  try { OFFRE = JSON.parse($("[data-offre]").textContent); } catch (e) {}
  try { LIEUX = JSON.parse(document.querySelector("[data-lieux-data]").textContent); } catch (e) {}
  var RANG = { base: 0, signature: 1, platinum: 2 }, PAR_RANG = ["base", "signature", "platinum"];
  var BOITIER_VR = { base: "vrb", signature: "vrs", platinum: "vrp" };   /* le Boîtier VR suit le niveau */
  var VEHICULES = { vehicules: 1, aerien: 1 };                           /* familles sans appareil à bord */
  function forfait() { return window.JarvisForfait; }

  function qtyOf(el) { var o = el && el.querySelector("output"); return o ? (+o.value || 0) : 0; }
  function setQty(el, v) { var o = el && el.querySelector("output"); if (o) o.value = Math.max(0, v); }
  function titre(el) { var h = el && el.querySelector("h3, b"); return h ? h.textContent.trim() : ""; }
  function piece(id) { return $('.ct-item[data-id="' + id + '"]'); }
  function niveau() { var c = $('input[name="hub"]:checked'); return c ? c.value : ""; }

  var pret = false;
  var ens = {};   /* ensembles de départ ajoutés : lieu → { pièce: quantité }, tels qu'ajoutés */

  /* ---------- L'état du formulaire, gardé dans le forfait pour le retrouver tel quel ---------- */
  var QTES = [["sol:mob", '.ct-sol[data-sol="mob"]'], ["recep", ".ct-ent-recep"], ["mesure", ".ct-ent-mesure"]];
  function etatForm() {
    var c = $$('input[type="checkbox"]:checked:not(:disabled), input[type="radio"]:checked')
      .filter(function (i) { return i.name && ["hub", "sol"].indexOf(i.name) < 0; }).map(function (i) { return i.name + "=" + i.value; });
    var q = {};
    $$(".ct-item[data-id]").forEach(function (it) { var v = qtyOf(it); if (v) q[it.dataset.id] = v; });
    QTES.forEach(function (p) { var v = qtyOf($(p[1])); if (v) q[p[0]] = v; });
    return { c: c, q: q, e: ens, l: listes };
  }
  function poseEtat(e) {
    if (!e || !e.c) return;
    $$('input[type="checkbox"], input[type="radio"]').forEach(function (i) {
      if (!i.name || i.disabled || ["hub", "sol"].indexOf(i.name) >= 0) return;
      i.checked = e.c.indexOf(i.name + "=" + i.value) >= 0;
    });
    if (!$('input[name="install"]:checked')) { var ia = $('input[name="install"][value="auto"]'); if (ia) ia.checked = true; }
    $$(".ct-item[data-id]").forEach(function (it) { setQty(it, (e.q || {})[it.dataset.id] || 0); });
    QTES.forEach(function (p) { setQty($(p[1]), (e.q || {})[p[0]] || 0); });
    ens = e.e && typeof e.e === "object" ? e.e : {};
    listes = e.l && typeof e.l === "object" ? e.l : {};
  }
  function garde(autres, suffixe) {
    var f = forfait(); if (!f || !pret) return;
    var o = f.lire();
    /* Seules les extensions ajoutées en plus du niveau sont des lignes du forfait. */
    o.sols = $$('.ct-sol:not(.is-niveau) input[name="sol"]:checked:not(:disabled)').map(function (c) { return c.getAttribute("data-slug"); }).filter(Boolean);
    o.autres = autres; o.etat = etatForm(); o.suffixe = suffixe;
    f.ecrire(o);
  }

  /* ---------- Le calcul : lignes « une fois » et « par mois », et ce qu'il faut prévoir ---------- */
  function compute() {
    var once = [], month = [], tips = [];
    var hubIn = $('input[name="hub"]:checked'), hubId = hubIn ? hubIn.value : "";
    var hubNom = hubIn ? "Le niveau " + maj(hubId) : "Votre niveau";
    var camMax = hubIn ? +hubIn.dataset.cam : 99, appMax = hubIn ? +hubIn.dataset.app : 1e6, autoMax = hubIn ? +hubIn.dataset.autos : 1e6;
    if (hubIn) once.push({ id: "hub", n: (visData[hubId] || [maj(hubId)])[0], q: 1, p: +hubIn.dataset.prix, fixed: true });

    /* Extensions : celles du niveau sont comprises; les autres sont des lignes par mois */
    var mobLab = $('.ct-sol[data-sol="mob"]'), nVeh = qtyOf(mobLab);
    var hasSecu = false, hasDiag = false, hasMob = false;
    $$('input[name="sol"]:not(:disabled)').forEach(function (s) {
      var lab = s.closest(".ct-sol");
      if (s.value === "mob") {
        if (s.checked && nVeh < 1) { setQty(lab, 1); nVeh = 1; }
        if (!s.checked && nVeh > 0) { setQty(lab, 0); nVeh = 0; }
        if (s.checked) { month.push({ id: "mob", n: "Mobilité", q: nVeh, p: +s.dataset.prix, unit: "véhicule", kind: "sol" }); hasMob = true; }
        return;
      }
      if (!s.checked) return;
      if (s.value === "secu") hasSecu = true;
      if (s.value === "diag") hasDiag = true;
      if (!lab.classList.contains("is-niveau")) month.push({ id: s.value, n: titre(lab), q: 1, p: +s.dataset.prix, kind: "sol" });
    });
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
    if (entActif && !veilleSeule && socle && !socle.checked) socle.checked = true;
    var socleOn = !!(socle && socle.checked);
    if (socleOn) month.unshift({ id: "socle", n: "Socle Entreprise", q: 1, p: +socle.dataset.prix, kind: "ent" });

    /* Le nuage : seulement ce que le client coche */
    $$('input[name="nuage"]:checked').forEach(function (v) {
      month.push({ id: v.value, n: v.closest(".ct-opt").querySelector("b").textContent, q: 1, p: 0, kind: "nuage" });
    });

    /* Équipement et services */
    var nApp = 0, nCam = 0, nCapt = 0, hasBoitierVR = false, hasBoitierMob = false;
    $$(".ct-item").forEach(function (it) {
      var q = qtyOf(it);
      it.classList.toggle("is-on", q > 0);
      if (!q) return;
      once.push({ id: it.dataset.id, n: it.querySelector("b").textContent, q: q, p: +it.dataset.prix });
      if (it.dataset.svc) return;
      nApp += q;
      if (it.dataset.cam) nCam += q;
      if (it.closest(".ct-cat").querySelector("h3").textContent === "Capteurs") nCapt += q;
      if (/^vr[bsp]$/.test(it.dataset.id)) hasBoitierVR = true;
      if (it.dataset.id === "mobb") hasBoitierMob = true;
    });

    /* Installation */
    var inst = $('input[name="install"]:checked');
    if (inst && +inst.dataset.prix > 0) once.push({ id: "install", n: titre(inst.closest(".ct-inst")) + (inst.value === "place" ? " (3 h, estimation)" : ""), q: 1, p: +inst.dataset.prix, fixed: true });

    var totOnce = once.reduce(function (s, l) { return s + l.q * l.p; }, 0);
    var totMonth = month.reduce(function (s, l) { return s + l.q * l.p; }, 0);

    /* À prévoir : ce qui ne tient pas ensemble, dit simplement, avec le geste qui le règle */
    var plusHaut = hubId === "base" ? "signature" : "platinum";
    if (nCam > camMax) tips.push({ t: hubNom + " analyse " + camMax + " caméras; vous en avez " + nCam + ".", up: plusHaut });
    if (nApp > appMax) tips.push({ t: hubNom + " relie " + appMax + " appareils; vous en avez " + nApp + ".", up: plusHaut });
    if (hubId === "base" && (socleOn || entActif)) tips.push({ t: "La réceptionniste et les automatisations d’entreprise demandent le niveau Signature ou Platinum.", up: "signature" });
    else if (nAutos > autoMax) tips.push({ t: hubNom + " fait tourner " + autoMax + " automatisations; vous en avez " + nAutos + ".", up: "platinum" });
    /* Plusieurs lieux : le niveau dit combien se relient entre eux (fiche technique : « Lieux reliés ») */
    var f = forfait(), nLieux = 0;
    if (f) { var cz = f.cerveaux(f.lire()).hub; Object.keys(cz).forEach(function (id) { if (cz[id]) nLieux++; }); }
    if (hubId === "base" && nLieux > 1) tips.push({ t: "Au niveau Base, chaque lieu veille seul. Pour relier vos lieux entre eux, il faut le niveau Signature (jusqu’à trois lieux) ou Platinum.", up: "signature" });
    if (hubId === "signature" && nLieux > 3) tips.push({ t: "Le niveau Signature relie jusqu’à trois lieux; vous en avez " + nLieux + ".", up: "platinum" });
    if (hasSecu && nCam === 0) tips.push({ t: "Sécurité intelligente sans caméra : ajoutez au moins une caméra ou une sonnette." });
    if (hasDiag && nCapt === 0 && !hasBoitierVR) tips.push({ t: "Diagnostic sans capteur : ajoutez au moins un capteur (fuite, température, porte)." });
    if (hasMob && !hasBoitierMob && !hasBoitierVR) tips.push({ t: "Mobilité a besoin d’un Boîtier Mobilité (véhicule) ou d’un Boîtier VR Signature ou Platinum (GPS)." });
    if (hubId === "base" && once.some(function (l) { return l.id === "vrs" || l.id === "vrp"; })) tips.push({ t: "Le Boîtier VR Signature ou Platinum prend tout son sens avec le niveau Signature (IA chez vous, 4G).", up: "signature" });

    affiche(totOnce, totMonth, tips);

    /* Ce qui part dans le forfait : équipement (quantité réglable), services, entreprise, nuage. */
    var autres = [];
    once.forEach(function (l) {
      if (l.id === "hub") return;
      var it = piece(l.id), mat = !!it && !it.hasAttribute("data-svc");
      autres.push({ id: l.id, n: l.n, q: l.q, k: mat ? "mat" : l.fixed ? "fixe" : "autre", s: "Une fois", px: fmt(l.q * l.p), img: it ? it.getAttribute("data-img") || "" : "" });
    });
    month.forEach(function (l) {
      if (l.kind === "sol") return;   /* les extensions ajoutées sont déjà des lignes du forfait (o.sols) */
      autres.push({ id: l.id, n: l.n, q: l.q, k: "autre", px: l.kind === "nuage" ? "" : fmt(l.q * l.p),
        s: l.kind === "nuage" ? "Option, sur votre accord" : (l.q > 1 ? l.q + " " + (l.unit ? l.unit + "s" : "") + " · " : "") + "Par mois" });
    });
    garde(autres, SANS ? "" : " | " + fmt(totOnce) + " une fois, " + fmt(totMonth) + " par mois");
  }

  function affiche(totOnce, totMonth, tips) {
    $$("[data-total-once]", document).forEach(function (e) { e.textContent = fmt(totOnce); });
    $$("[data-total-month]", document).forEach(function (e) { e.textContent = fmt(totMonth); });
    var tb = $("[data-cart-tips]"); if (!tb) return;
    tb.hidden = !tips.length;
    tb.innerHTML = tips.length ? "<h4>À prévoir</h4>" + tips.map(function (t) {
      return "<p>" + esc(t.t) + (t.up ? ' <button type="button" data-up="' + t.up + '">Passer au niveau ' + maj(t.up) + "</button>" : "") + "</p>";
    }).join("") : "";
  }

  /* ---------- Retirer une ligne (demandé par le tiroir du forfait) ---------- */
  function retire(id) {
    var el, f = forfait();
    if (id === "hub") { if (f) { var o = f.lire(); o.manuel = false; o.hub = f.hubDe(o); f.ecrire(o); } poseNiveau(); appliqueNiveau(); return; }
    if (id === "mob") { setQty($('.ct-sol[data-sol="mob"]'), 0); el = $('input[name="sol"][value="mob"]'); if (el) el.checked = false; }
    else if ((el = $('input[name="sol"][value="' + id + '"]'))) { if (!el.closest(".ct-sol").classList.contains("is-niveau")) el.checked = false; }
    else if (id === "toutes") { $('input[name="toutes"]').checked = false; $$('input[name="auto"]').forEach(function (a) { a.checked = false; }); }
    else if (id === "socle") { $('input[name="socle"]').checked = false; $('input[name="toutes"]').checked = false; $$('input[name="auto"]').forEach(function (a) { a.checked = false; }); setQty($(".ct-ent-recep"), 0); setQty($(".ct-ent-mesure"), 0); }
    else if ((el = $('input[name="auto"][value="' + id + '"]'))) el.checked = false;
    else if ((el = $('input[name="veille"][value="' + id + '"]'))) el.checked = false;
    else if ((el = $('input[name="nuage"][value="' + id + '"]'))) el.checked = false;
    else if (id === "recep") setQty($(".ct-ent-recep"), 0);
    else if (id === "mesure" || id === "mesure-m") setQty($(".ct-ent-mesure"), 0);
    else if ((el = piece(id))) setQty(el, 0);
    compute(); dessineEnsembles();
  }

  /* ---------- Étape 2 : le niveau, et les extensions qu'il comprend ---------- */
  function poseNiveau() {
    var f = forfait(), o = f ? f.lire() : {};
    $$('input[name="hub"]').forEach(function (r) { r.checked = r.value === o.hub; });
  }
  function appliqueNiveau() {
    var inclus = OFFRE.niveaux[niveau()] || [];
    $$(".ct-sol[data-sol]").forEach(function (box) {
      var cb = box.querySelector('input[name="sol"]'), dedans = inclus.indexOf(box.getAttribute("data-sol")) >= 0;
      box.classList.toggle("is-niveau", dedans);
      if (cb && !cb.disabled) {
        if (dedans) cb.checked = true;
        else if (box.dataset.niveauAvant === "1") cb.checked = false;   /* comprise avant, plus maintenant */
      }
      box.dataset.niveauAvant = dedans ? "1" : "";
    });
    reapplique();
    compute(); montre(); dessineEnsembles();
  }
  function coche(slug, oui) {
    var cb = $('input[name="sol"][data-slug="' + slug + '"]'); if (!cb || cb.disabled) return;
    cb.checked = oui;
    var box = cb.closest(".ct-sol"); if (box && cb.hasAttribute("data-qty")) setQty(box, oui ? Math.max(1, qtyOf(box)) : 0);
  }

  /* ---------- Étape 3 : l'ensemble de départ de chaque lieu ---------- */
  var listes = {};   /* listes composées par JARVIS : lieu → { pièce: quantité }, « vr* » non résolu */
  function resolu(lieu) {   /* les pièces de l'ensemble; « vr* » devient le Boîtier VR du niveau */
    var mat = listes[lieu] || (OFFRE.ensembles[lieu] || {}).mat, out = {};
    if (!mat) return out;
    var n = niveau() || (LIEUX[lieu] && LIEUX[lieu].hub) || "base";
    Object.keys(mat).forEach(function (id) { out[id === "vr*" ? BOITIER_VR[n] : id] = mat[id]; });
    return out;
  }
  function bouge(pieces, signe) {
    Object.keys(pieces).forEach(function (id) { var it = piece(id); if (it) setQty(it, qtyOf(it) + signe * pieces[id]); });
  }
  function ajouteEnsemble(lieu) {
    if (ens[lieu] || (!OFFRE.ensembles[lieu] && !listes[lieu])) return;
    var p = resolu(lieu), e = OFFRE.ensembles[lieu].ent;
    bouge(p, 1); ens[lieu] = p;
    if (!e) return;
    if (e.socle) $('input[name="socle"]').checked = true;
    if (e.recep) setQty($(".ct-ent-recep"), Math.max(qtyOf($(".ct-ent-recep")), e.recep));
    (e.autos || []).forEach(function (a) { var c = $('input[name="auto"][value="' + a + '"]'); if (c) c.checked = true; });
  }
  function retireEnsemble(lieu) {
    if (!ens[lieu]) return;
    bouge(ens[lieu], -1); delete ens[lieu];
    var e = (OFFRE.ensembles[lieu] || {}).ent;
    if (!e) return;
    if (e.recep) setQty($(".ct-ent-recep"), qtyOf($(".ct-ent-recep")) - e.recep);
    (e.autos || []).forEach(function (a) { var c = $('input[name="auto"][value="' + a + '"]'); if (c) c.checked = false; });
    var reste = $$('input[name="auto"]:checked').length || qtyOf($(".ct-ent-recep")) || qtyOf($(".ct-ent-mesure")) || $$('input[name="veille"]:checked').length;
    if (!reste) { $('input[name="socle"]').checked = false; $('input[name="toutes"]').checked = false; }
  }
  function reapplique() {   /* après un changement de niveau : le Boîtier VR des ensembles ajoutés suit */
    Object.keys(ens).forEach(function (lieu) {
      var neuf = resolu(lieu);
      if (JSON.stringify(neuf) === JSON.stringify(ens[lieu])) return;
      bouge(ens[lieu], -1); bouge(neuf, 1); ens[lieu] = neuf;
    });
  }
  var boiteEns = $("[data-ensembles]"), videEns = boiteEns ? boiteEns.innerHTML : "";
  function dessineEnsembles() {
    if (!boiteEns) return;
    var f = forfait(), o = f ? f.lire() : { lieux: [] };
    var ids = o.lieux.filter(function (id) { return OFFRE.ensembles[id] && LIEUX[id]; });
    if (!ids.length) { boiteEns.innerHTML = videEns; return; }
    boiteEns.innerHTML = ids.map(function (id) {
      var on = !!ens[id], p = on ? ens[id] : resolu(id), e = OFFRE.ensembles[id], ent = e.ent || {};
      var lis = Object.keys(p).map(function (k) { var it = piece(k); return "<li><b>" + p[k] + "×</b> " + esc(it ? it.querySelector("b").textContent : k) + "</li>"; });
      if (ent.recep) lis.push("<li><b>" + ent.recep + "×</b> Réceptionniste IA</li>");
      if (ent.autos && ent.autos.length) lis.push("<li><b>" + ent.autos.length + "×</b> automatisations pour commencer</li>");
      return '<article class="ct-en' + (on ? " is-on" : "") + '">' +
        '<img src="/media/forfait/lieu-' + id + '.webp" alt="" loading="lazy" decoding="async">' +
        '<div class="ct-en-t"><h4>' + esc(LIEUX[id].nom) + "</h4><p>" + esc(e.pourquoi) + "</p><ul>" + lis.join("") + "</ul></div>" +
        '<button type="button" class="ct-en-b" data-ens="' + id + '" aria-pressed="' + (on ? "true" : "false") + '">' + (on ? "Ajouté · retirer" : "Ajouter à mon projet") + "</button></article>";
    }).join("");
  }

  /* ---------- L'appareil du niveau choisi (JARVIS Mini, JARVIS, JARVIS Pro), en grand à gauche ---------- */
  var vis = document.querySelector("[data-ct-vis]"), visData = {};
  if (vis) { try { visData = JSON.parse(vis.querySelector("[data-vis-data]").textContent); } catch (e) {} }
  function montre() {
    if (!vis) return;
    var id = niveau() || "signature";
    $$("[data-v]", vis).forEach(function (im) { im.classList.toggle("is-on", im.getAttribute("data-v") === id); });
    if (visData[id]) { vis.querySelector("[data-vis-nom]").textContent = visData[id][0]; vis.querySelector("[data-vis-ligne]").textContent = visData[id][1]; }
  }

  /* ---------- « Vous hésitez? » : les lieux et trois réponses donnent le niveau conseillé ---------- */
  var guide = $("[data-guide]"), rep = {}, res = guide ? $("[data-guide-res]", guide) : null;
  function conseil() {
    if (!guide) return;
    var f = forfait(), o = f ? f.lire() : { lieux: [] }, r = -1, why = "";
    var rec = f ? f.hubDe(o) : "";
    if (rec && RANG[rec] !== undefined) { r = RANG[rec]; why = o.lieux.length > 1 ? "La bonne taille pour votre lieu principal." : "La bonne taille pour votre lieu."; }
    if (rep.cam !== undefined && rep.cam > r) { r = rep.cam; why = rep.cam === 2 ? "Plus de six caméras à analyser." : "Jusqu’à six caméras analysées par l’IA."; }
    if (rep.ia === 1 && r < 1) { r = 1; why = "L’IA reste chez vous, même sans Internet."; }
    if (rep.coupure === 2 && r < 2) { r = 2; why = "Une coupure serait grave : batterie et Internet de secours."; }
    if (r < 0 && Object.keys(rep).length) { r = 0; why = "L’essentiel, pour un petit lieu."; }
    $$(".ct-hub").forEach(function (h) { h.classList.toggle("is-reco", r >= 0 && h.getAttribute("data-hub") === PAR_RANG[r]); });
    res.hidden = r < 0;
    if (r < 0) return;
    res.dataset.id = PAR_RANG[r];
    $("[data-guide-nom]", res).textContent = "Niveau " + maj(PAR_RANG[r]);
    $("[data-guide-why]", res).textContent = why;
  }
  function choisit(id) {
    var radio = $('input[name="hub"][value="' + id + '"]');
    if (radio && !radio.checked) { radio.checked = true; radio.dispatchEvent(new Event("change", { bubbles: true })); }
  }

  /* ---------- Les gestes ---------- */
  form.addEventListener("change", function (e) {
    var t = e.target;
    if (t.name === "toutes" && t.checked) $('input[name="socle"]').checked = true;
    if (t.name === "hub") {   /* le niveau choisi à la main vaut pour tous les lieux (wow.js redessine l'écosystème) */
      var f = forfait(); if (f) { var o = f.lire(); o.manuel = true; o.hub = t.value; f.ecrire(o); }
      appliqueNiveau(); return;
    }
    compute();
  });
  form.addEventListener("click", function (e) {
    var t = e.target;
    if (t.matches && t.matches('.ct-sol.is-niveau input[name="sol"]')) { e.preventDefault(); return; }   /* comprise dans le niveau : rien à retirer */
    var b = t.closest("[data-q]");
    if (b) {
      var box = b.closest(".ct-item, .ct-ent, .ct-sol"); setQty(box, qtyOf(box) + (+b.dataset.q));
      var cb = box.querySelector('input[name="sol"]'); if (cb) cb.checked = qtyOf(box) > 0;
      compute(); e.preventDefault(); return;
    }
    var up = t.closest("[data-up]");
    if (up) { choisit(up.dataset.up); return; }
    var en = t.closest("[data-ens]");
    if (en) { var lieu = en.dataset.ens; if (ens[lieu]) retireEnsemble(lieu); else ajouteEnsemble(lieu); compute(); dessineEnsembles(); return; }
    var q = t.closest("[data-gq] button[data-v]");
    if (q) {
      var bloc = q.closest("[data-gq]");
      $$("button", bloc).forEach(function (x) { x.setAttribute("aria-pressed", x === q ? "true" : "false"); });
      rep[bloc.getAttribute("data-gq")] = +q.getAttribute("data-v");
      conseil(); return;
    }
    if (t.closest("[data-guide-go]") && res && res.dataset.id) { choisit(res.dataset.id); return; }
    if (t.closest("[data-jv-ouvre]")) { var fab = document.querySelector("#jv-root .jv-fab"); if (fab) fab.click(); }   /* JARVIS, la bulle du site (guide.js) */
  });
  /* Le forfait a changé ailleurs (un lieu ajouté ou retiré à l'étape 1, une ligne retirée dans le tiroir). */
  document.addEventListener("jarvis:forfait", function (e) {
    var d = e.detail || {};
    if (d.lieu) {
      var l = LIEUX[d.lieu], mob = $('.ct-sol[data-sol="mob"]');
      if (l && VEHICULES[l.famille] && mob) {   /* Mobilité suit les véhicules : une par véhicule */
        var n = Math.max(0, qtyOf(mob) + (d.ajoute ? 1 : -1) * ((OFFRE.ensembles[d.lieu] || { mat: {} }).mat.mobb || 1));
        setQty(mob, n); mob.querySelector('input[name="sol"]').checked = n > 0;
      }
      if (!d.ajoute) retireEnsemble(d.lieu);
    }
    if (d.lieu || d.public) poseNiveau();
    if (d.sol) coche(d.sol, !!d.ajoute);
    appliqueNiveau(); conseil();
  });

  function vider() {
    var f = forfait(), o = f ? f.lire() : null;
    ens = {}; rep = {}; form.reset();
    $$('input[name="hub"]').forEach(function (h) { h.checked = false; });
    $$(".ct-item, .ct-ent, .ct-sol").forEach(function (x) { setQty(x, 0); });
    $$("[data-gq] button").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
    if (f) f.ecrire({ lieux: [], sols: [], hub: "", manuel: false, public: o.public, separee: false, autres: [], etat: null });
    appliqueNiveau(); conseil();
  }
  /* Ce que le tiroir du forfait (wow.js) peut demander au formulaire. */
  window.JarvisCatalogue = {
    retire: retire,
    qte: function (id, d) { var it = piece(id); if (it) { setQty(it, qtyOf(it) + d); compute(); } },
    vider: vider
  };

  /* ---------- Arrivée : le forfait bâti en chemin est repris tel quel ---------- */
  (function () {
    var f = forfait(); if (!f) return;
    var o = f.lire();
    poseEtat(o.etat); poseNiveau();
    Object.keys(ens).forEach(function (lieu) { if (o.lieux.indexOf(lieu) < 0) retireEnsemble(lieu); });   /* lieu retiré ailleurs */
    $$('input[name="sol"][data-slug]:not(:disabled)').forEach(function (c) { coche(c.getAttribute("data-slug"), o.sols.indexOf(c.getAttribute("data-slug")) >= 0); });
  })();
  pret = true;
  appliqueNiveau(); conseil();

  /* ---------- Arrivée par un plan tout composé ----------
     JARVIS (la bulle) propose un lien : /offre/?lieux=maison,chalet,auto&niveau=signature&ens=tout#composer
       lieux  : identifiants de src/lieux.py, séparés par des virgules (les inconnus sont ignorés);
       niveau : base, signature ou platinum (absent : le niveau conseillé pour ces lieux);
       ens    : « tout », ou la liste des lieux dont on ajoute l'ensemble de départ;
       <lieu> : la liste sur mesure de ce lieu, « pièce:quantité » séparés par des virgules
                (ex. &maison=fuite:2,camext:2,vanne:1). Elle remplace l'ensemble de départ de ce
                lieu, et se retire ou se réajuste comme lui. Pièces inconnues ignorées, quantité ≤ 99.
     Le plan remplace le forfait en cours; l'adresse est nettoyée pour qu'un rechargement ne le rejoue pas. */
  (function () {
    var q = new URLSearchParams(location.search), f = forfait();
    if (!f || !q.has("lieux")) return;
    var ids = [];
    q.get("lieux").split(",").forEach(function (id) { if (LIEUX[id] && ids.indexOf(id) < 0) ids.push(id); });
    if (!ids.length) return;
    vider();
    var o = f.lire(), n = q.get("niveau");
    var ent = ids.some(function (id) { return LIEUX[id].public === "entreprise"; }), autre = ids.some(function (id) { return LIEUX[id].public !== "entreprise"; });
    o.lieux = ids;
    if (ent) o.public = autre ? "deux" : "entreprise";
    o.manuel = RANG[n] !== undefined;
    o.hub = o.manuel ? n : f.hubDe(o);
    f.ecrire(o); poseNiveau();
    var mob = $('.ct-sol[data-sol="mob"]'), nVeh = 0;   /* Mobilité suit les véhicules */
    ids.forEach(function (id) { if (VEHICULES[LIEUX[id].famille]) nVeh += (OFFRE.ensembles[id] || { mat: {} }).mat.mobb || 1; });
    if (mob) { setQty(mob, nVeh); mob.querySelector('input[name="sol"]').checked = nVeh > 0; }
    appliqueNiveau();
    ids.forEach(function (id) {           /* la liste composée par JARVIS, si elle est là */
      var brut = q.get(id); if (!brut) return;
      var p = {};
      brut.split(",").forEach(function (bout) {
        var m = /^([a-z0-9*_-]{1,16}):(\d{1,2})$/i.exec(bout.trim());
        if (m && +m[2] > 0 && (m[1] === "vr*" || piece(m[1]))) p[m[1]] = Math.min(99, +m[2]);
      });
      if (Object.keys(p).length) listes[id] = p;
    });
    var e = q.get("ens") || "";
    var aAjouter = e === "tout" ? ids : e.split(",");
    ids.forEach(function (id) { if (listes[id] && aAjouter.indexOf(id) < 0) aAjouter.push(id); });
    aAjouter.forEach(function (id) { if (ids.indexOf(id) >= 0) ajouteEnsemble(id); });
    appliqueNiveau(); conseil();
    try { history.replaceState(null, "", location.pathname + location.hash); } catch (x) {}
  })();
})();
