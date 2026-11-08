/* Démo « Mobilité » — copilote de route, journal de voyage, garage connecté.
   Données (trajet, points d'intérêt, voyages, modes) : JSON #mb-data produit par src/demos/mobilite.py.
   Le copilote calcule ses suggestions à chaque instant selon : la distance restante, les heures
   d'ouverture à l'heure d'arrivée, le soleil (coucher 16 h 42) et l'état du VR (eau, propane, Webasto).
   Le véhicule n'avance que sous html.fx, quand la démo est visible et que l'onglet Copilote est ouvert. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="mobilite"]');
  if (!root) return;
  var D;
  try { D = JSON.parse(document.getElementById("mb-data").textContent); } catch (e) { return; }
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var NB = " ";
  function $(s, el) { return (el || root).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || root).querySelectorAll(s)); }
  function fx() { return document.documentElement.classList.contains("fx") && !reduce; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function ico(n) { return '<svg class="mb-i" viewBox="0 0 24 24" aria-hidden="true">' + (D.icons[n] || "") + "</svg>"; }
  function hm(min, full) { min = Math.round(min); var h = Math.floor(min / 60) % 24, m = min % 60; return h + NB + "h" + (m || full ? NB + (m < 10 ? "0" : "") + m : ""); }
  function dur(min) { min = Math.max(0, Math.round(min)); if (min < 60) return min + NB + "min"; var h = Math.floor(min / 60), m = min % 60; return h + NB + "h" + (m ? NB + (m < 10 ? "0" : "") + m : ""); }
  function kmf(k) { return k < 10 ? String(Math.round(k * 10) / 10).replace(".", ",") : String(Math.round(k)); }
  function pct(x, y, vb) { return { l: (x - vb[0]) / vb[2] * 100, t: (y - vb[1]) / vb[3] * 100 }; }

  /* ---------------- Onglets ---------------- */
  var tab = "copilote";
  $$(".mb-tab").forEach(function (b) {
    b.addEventListener("click", function () {
      tab = b.getAttribute("data-tab");
      $$(".mb-tab").forEach(function (o) { var on = o === b; o.classList.toggle("is-on", on); o.setAttribute("aria-pressed", on ? "true" : "false"); });
      $$(".mb-pane").forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== tab; });
      if (tab === "journal") renderJournal();
      sync();
    });
  });

  /* ================================================================
     COPILOTE
     ================================================================ */
  var START = 9 * 60 + 5, SPEED = 80, KM0 = 150, SUNRISE = 6 * 60 + 48, SUNSET = 16 * 60 + 42, GOLDEN = SUNSET - 22;
  var PRODUITS = { orleans: 1, bleuets: 1 };
  var HORIZON = { decouverte: 240, efficace: 120, nature: 320, gourmand: 240, famille: 200, horsreseau: 300 };
  var NEEDS = { eau: 1, propane: 1, webasto: 1, meca: 1 };
  var MEALS = [[11 * 60 + 15, 13 * 60 + 45, "dîner"], [17 * 60 + 15, 20 * 60, "souper"]];
  var LVL0 = { eau: 24, propane: 31, carb: 56, batt: 76 };
  var pois = D.pois, byId = {};
  pois.forEach(function (p) { byId[p.id] = p; p.det = Math.max(1, Math.round(p.off * 2 / 45 * 60)); });
  var S;
  function reset(km) {
    S = { km: km, mode: S ? S.mode : "decouverte", acc: {}, ign: {}, done: {}, shots: {}, ended: false, speed: 92 };
  }
  reset(KM0);
  var mapCo = $('[data-mb-map="co"]'), car = $("[data-mb-car]"), cards = $("[data-mb-cards]");
  var doneEls = $$("[data-mb-done]"), detG = $("[data-mb-detours]");
  var pinEls = {};
  $$(".mb-poi").forEach(function (b) { pinEls[b.getAttribute("data-poi")] = b; });

  function extraBefore(km) {
    var t = 0;
    pois.forEach(function (p) { if (S.acc[p.id] && p.km < km) t += p.stop + p.det; });
    return t;
  }
  function clockAt(km) { return START + km / SPEED * 60 + extraBefore(km); }
  function lastFill(cat, km) {
    var best = null;
    pois.forEach(function (p) { if (p.cat === cat && S.acc[p.id] && p.km <= km && (!best || p.km > best.km)) best = p; });
    return best;
  }
  function levels(km) {
    var e = lastFill("eau", km), pr = lastFill("propane", km);
    return {
      eau: Math.max(4, e ? 100 - (km - e.km) * 0.012 : LVL0.eau - km * 0.012),
      propane: Math.max(4, pr ? 100 - (km - pr.km) * 0.006 : LVL0.propane - km * 0.006),
      carb: Math.max(8, LVL0.carb - km * 0.045),
      batt: Math.min(98, LVL0.batt + km * 0.02),
      webasto: !!lastFill("webasto", km)
    };
  }
  function nextOpen(cat, fromKm) {
    for (var i = 0; i < pois.length; i++) {
      var p = pois[i];
      if (p.cat === cat && p.km > fromKm + 1) { var a = clockAt(p.km); if (a >= p.h[0] && a <= p.h[1] - 15) return p; }
    }
    return null;
  }
  function meal(t) { for (var i = 0; i < MEALS.length; i++) if (t >= MEALS[i][0] && t <= MEALS[i][1]) return MEALS[i][2]; return null; }

  /* Une suggestion : pourquoi, combien de détour, quand. null = rien d'utile à proposer. */
  function build(p, lv, w) {
    var dist = p.km - S.km, now = clockAt(S.km), arr = clockAt(p.km) + p.det / 2, wt = w[p.cat] || 0;
    if (!wt) return null;
    var open = arr >= p.h[0] && arr <= p.h[1] - 15, allDay = p.h[0] === 0 && p.h[1] >= 1440;
    if (!open) return null;
    var inMin = arr - now, s = { p: p, urg: 0, title: "", why: p.why, meta: [], act: "Accepter" };
    var e = Math.round(lv.eau), pr = Math.round(lv.propane);
    switch (p.cat) {
      case "eau":
        if (lv.eau > 45) return null;
        s.urg = (45 - lv.eau) / 9;
        s.title = "Eau propre " + e + NB + "% : " + (p.id === "eau1" ? "remplissage gratuit" : "eau et vidange") + " à " + kmf(dist) + NB + "km";
        break;
      case "propane":
        if (lv.propane > 42) return null;
        var nx = nextOpen("propane", p.km), gap = nx ? nx.km - p.km : D.len - p.km;
        s.urg = (42 - lv.propane) / 8 + (gap > 120 ? 1.5 : 0);
        s.title = "Propane " + pr + NB + "% : " + (gap > 120 ? "dernier poste ouvert avant " + Math.round(gap / 10) * 10 + NB + "km" : "poste ouvert à " + kmf(dist) + NB + "km");
        break;
      case "repas":
        var m = meal(arr), prod = PRODUITS[p.id];
        if (m && !prod) { s.urg = 2; s.meal = true; s.title = "Arrêt " + m + " dans " + dur(inMin) + " — ouvert jusqu’à " + hm(p.h[1]); }
        else if (wt >= 2) { s.urg = wt >= 3 ? 1.2 : .5; s.title = "Pause gourmande dans " + dur(inMin) + " : " + p.nom.charAt(0).toLowerCase() + p.nom.slice(1); }
        else return null;
        s.sub = p.nom;
        break;
      case "webasto":
        if (lv.webasto) return null;
        s.urg = 1.1; s.title = "Webasto : entretien saisonnier dû (" + p.val + ")"; s.sub = p.nom;
        break;
      case "meca":
        s.urg = .9; s.title = "Entretien mécanique : " + p.nom.charAt(0).toLowerCase() + p.nom.slice(1);
        break;
      case "soleil":
        var slack = GOLDEN - arr;
        if (slack < -10 || p !== bestSun()) return null;
        if (slack <= 60) { s.urg = 3; s.title = "Coucher de soleil " + hm(SUNSET) + " : roulez maintenant pour arriver avant " + hm(GOLDEN); s.why = "Arrivée prévue à " + hm(arr) + " · " + p.why; }
        else { s.urg = 1.4; s.title = "Coucher de soleil " + hm(SUNSET) + " : arrivez au belvédère avant " + hm(GOLDEN); s.why = "Au rythme actuel, vous y serez à " + hm(arr) + " : " + dur(slack) + " de marge pour d’autres arrêts. " + p.why; }
        s.sub = p.nom;
        break;
      case "histoire":
        s.urg = 1; s.title = "Site historique à " + kmf(p.off) + NB + "km de votre route : " + p.nom;
        break;
      case "nature":
        s.urg = .8; s.title = p.nom + " dans " + dur(inMin);
        break;
      case "famille":
        s.urg = 1; s.title = "Pause famille dans " + dur(inMin) + " : " + p.nom.charAt(0).toLowerCase() + p.nom.slice(1);
        break;
      case "nuit":
        if (arr < 15 * 60 + 30 && wt < 3) return null;
        s.urg = arr > 15 * 60 + 30 ? 1.8 : .5; s.title = "Nuit gratuite au bord du fjord : arrivée vers " + hm(arr);
        s.sub = p.nom;
        break;
      case "signal":
        s.urg = 1.2; s.title = "Zone sans réseau dans " + kmf(dist) + NB + "km : tout est téléchargé"; s.act = "Compris";
        break;
      case "traversier":
        var dep = Math.ceil(arr / 20) * 20;
        s.urg = 1.3; s.title = "Traversier : prochain départ " + hm(dep) + ", attente " + Math.round(dep - arr) + NB + "min";
        s.why = "Gratuit, départ aux 20 minutes. Arrivée au quai prévue à " + hm(arr) + ".";
        s.act = "Compris";
        break;
    }
    if (NEEDS[p.cat]) s.tag = "need"; else if (wt >= 3) s.tag = "mode";
    if (p.cat !== "signal" && p.cat !== "traversier") s.meta.push("Détour +" + (p.det + (p.stop && p.cat !== "nuit" ? 0 : 0)) + NB + "min");
    if (p.stop && p.cat !== "signal" && p.cat !== "traversier" && p.cat !== "nuit") s.meta.push("Arrêt " + dur(p.stop));
    s.meta.push(allDay ? "Ouvert 24" + NB + "h" : "Ouvert jusqu’à " + hm(p.h[1]));
    if (p.off >= 1) s.meta.push("À " + kmf(p.off) + NB + "km de la route");
    s.when = dist < 1 ? "maintenant" : "dans " + dur(inMin) + " · " + kmf(dist) + NB + "km";
    s.score = wt * (1 + s.urg) - dist / 140;
    return s;
  }
  function bestSun() {
    var best = null, bs = 1e9;
    pois.forEach(function (p) {
      if (p.cat !== "soleil" || p.km < S.km || S.ign[p.id]) return;
      var sl = GOLDEN - (clockAt(p.km) + p.det / 2);
      if (sl >= -10 && sl < bs) { bs = sl; best = p; }
    });
    return best;
  }
  function suggestions() {
    var lv = levels(S.km), w = D.modes[S.mode].w, horizon = HORIZON[S.mode], out = [], acc = [];
    pois.forEach(function (p) {
      if (S.ign[p.id] || S.done[p.id]) return;
      if (p.km < S.km - .3 || p.km - S.km > horizon) return;
      if (S.acc[p.id]) { acc.push(p); return; }
      var s = build(p, lv, w);
      if (s) out.push(s);
    });
    out.sort(function (a, b) { return b.score - a.score; });
    var mealSeen = false;
    out = out.filter(function (x) { if (!x.meal) return true; if (mealSeen) return false; mealSeen = true; return true; });
    out = out.slice(0, Math.max(2, 5 - acc.length));
    acc.forEach(function (p) {
      out.push({ p: p, accepted: true, title: p.nom, why: p.why, when: "Arrivée " + hm(clockAt(p.km) + p.det / 2) + " · dans " + kmf(p.km - S.km) + NB + "km", meta: [] });
    });
    out.sort(function (a, b) { return a.p.km - b.p.km; });
    return out;
  }

  var cardEls = {}, lastKeys = "";
  function cardHTML(s) {
    var p = s.p, k = D.cats[p.cat];
    var head = '<div class="mb-card-k">' + ico(p.cat) + esc(k) + "<span>" + esc(s.when) + "</span></div>";
    if (s.accepted) {
      return head + "<h4>" + esc(s.title) + "</h4>" +
        '<div class="mb-card-a"><span class="mb-done">' + ico("check") + "Ajouté à l’itinéraire<button type=\"button\" data-undo>Retirer</button></span></div>";
    }
    var meta = (s.tag === "mode" ? '<span class="is-mode">' + ico("etoile") + "Choisi pour le mode " + esc(D.modes[S.mode].nom) + "</span>" : s.tag === "need" ? '<span class="is-need">Besoin du véhicule</span>' : "") +
      s.meta.map(function (m) { return "<span>" + esc(m) + "</span>"; }).join("");
    return head + "<h4>" + esc(s.title) + "</h4>" + (s.sub && s.title.indexOf(s.sub) < 0 ? '<p class="mb-sub"><b>' + esc(s.sub) + "</b></p>" : "") +
      "<p>" + esc(s.why) + "</p>" + (meta ? '<div class="mb-card-m">' + meta + "</div>" : "") +
      '<div class="mb-card-a"><button type="button" class="mb-acc" data-acc>' + ico("check") + esc(s.act) + '</button><button type="button" class="mb-ign" data-ign>Ignorer</button></div>';
  }
  var booted = false;
  function renderFeed(replan) {
    var list = suggestions(), keys = list.map(function (s) { return s.p.id + (s.accepted ? "+" : ""); }).join(",");
    var seen = {};
    if (replan) { cards.innerHTML = ""; cardEls = {}; }
    list.forEach(function (s, i) {
      var id = s.p.id + (s.accepted ? "+" : ""), el = cardEls[id], html = cardHTML(s);
      seen[id] = 1;
      if (!el) {
        el = document.createElement("li");
        el.className = "mb-card is-new";
        el.setAttribute("data-card", s.p.id);
        el.style.setProperty("--d", (replan ? i * 0.08 : 0) + "s");
        cardEls[id] = el;
        el._h = "";
      }
      if (el._h !== html) { el.innerHTML = html; el._h = html; }
      el.classList.toggle("is-acc", !!s.accepted);
      el.classList.toggle("is-urgent", !s.accepted && s.urg >= 2.4);
      if (cards.children[i] !== el) cards.insertBefore(el, cards.children[i] || null);
    });
    Object.keys(cardEls).forEach(function (id) {
      if (!seen[id]) { var el = cardEls[id]; delete cardEls[id]; el.remove(); }
    });
    if (!list.length) cards.innerHTML = '<li class="mb-empty">Rien d’utile à proposer pour l’instant. JARVIS vous préviendra au bon moment.</li>';
    else { var em = $(".mb-empty", cards); if (em) em.remove(); }
    var set = {};
    list.forEach(function (s) { set[s.p.id] = 1; });
    pois.forEach(function (p) {
      var b = pinEls[p.id]; if (!b) return;
      b.classList.toggle("is-sugg", !!set[p.id] && !S.acc[p.id]);
      b.classList.toggle("is-acc", !!S.acc[p.id]);
      b.classList.toggle("is-ign", !!S.ign[p.id]);
      b.classList.toggle("is-past", p.km < S.km - .3 && !S.acc[p.id]);
      b.tabIndex = set[p.id] ? 0 : -1;
    });
    if (keys !== lastKeys || replan) {
      lastKeys = keys;
      var m = D.modes[S.mode], open = list.filter(function (s) { return !s.accepted; });
      var nm = open.filter(function (s) { return s.tag === "mode"; }).length, nn = open.filter(function (s) { return s.tag === "need"; }).length;
      var extra = open.reduce(function (t, s) { return t + (s.p.cat === "signal" || s.p.cat === "traversier" ? 0 : s.p.stop + s.p.det); }, 0);
      $("[data-mb-plan]").textContent = (replan && booted ? "Itinéraire replanifié · " : "") + open.length + " suggestion" + (open.length > 1 ? "s" : "") +
        " sur les " + HORIZON[S.mode] + NB + "prochains km" + (nm ? " · " + nm + " choisie" + (nm > 1 ? "s" : "") + " pour le mode " + m.nom : "") +
        (nn ? " · " + nn + " besoin" + (nn > 1 ? "s" : "") + " du véhicule" : "") + (extra ? " · +" + dur(extra) + " si tout est accepté." : ".");
    }
    drawDetours();
  }
  function drawDetours() {
    var html = "";
    pois.forEach(function (p) {
      if (!S.acc[p.id] || p.off < .3) return;
      var a = posAt(p.km);
      html += '<path class="mb-detour" d="M' + a.x.toFixed(1) + " " + a.y.toFixed(1) + "L" + p.x + " " + p.y + '"/>';
    });
    if (detG._h !== html) { detG.innerHTML = html; detG._h = html; }
  }

  cards.addEventListener("click", function (e) {
    var li = e.target.closest("[data-card]"); if (!li) return;
    var id = li.getAttribute("data-card"), p = byId[id];
    if (e.target.closest("[data-acc]")) {
      if (p.cat === "signal" || p.cat === "traversier") { S.done[id] = 1; toast(ico("check") + "<span><b>Noté.</b> " + esc(p.cat === "signal" ? "Cartes et musique sont prêtes hors ligne." : "JARVIS vous rappellera 10 minutes avant le quai.") + "</span>"); }
      else { S.acc[id] = 1; toast(ico("check") + "<span><b>Ajouté à l’itinéraire</b> · " + esc(p.nom) + ", arrivée " + hm(clockAt(p.km) + p.det / 2) + "</span>"); }
      renderFeed(); paint();
    } else if (e.target.closest("[data-ign]")) {
      S.ign[id] = 1;
      if (fx()) { li.classList.add("is-out"); setTimeout(function () { renderFeed(); }, 320); } else renderFeed();
      pinEls[id] && pinEls[id].classList.add("is-ign");
    } else if (e.target.closest("[data-undo]")) {
      delete S.acc[id]; renderFeed(); paint();
    }
  });
  Object.keys(pinEls).forEach(function (id) {
    pinEls[id].addEventListener("click", function () {
      var c = cards.querySelector('[data-card="' + id + '"]'), p = byId[id];
      if (c) {
        $$(".mb-card.is-hot", cards).forEach(function (o) { o.classList.remove("is-hot"); });
        c.classList.add("is-hot");
        cards.scrollTo({ top: c.offsetTop - cards.offsetTop - 8, behavior: fx() ? "smooth" : "auto" });
        setTimeout(function () { c.classList.remove("is-hot"); }, 2200);
      } else toast(ico(p.cat) + "<span><b>" + esc(p.nom) + "</b> · " + esc(p.why) + "</span>");
    });
  });

  /* Modes */
  $$(".mb-mode").forEach(function (b) {
    b.addEventListener("click", function () {
      S.mode = b.getAttribute("data-mode");
      $$(".mb-mode").forEach(function (o) { var on = o === b; o.classList.toggle("is-on", on); o.setAttribute("aria-pressed", on ? "true" : "false"); });
      var m = D.modes[S.mode];
      $("[data-mb-modeline]").textContent = "Mode " + m.nom + " · " + m.desc.charAt(0).toLowerCase() + m.desc.slice(1).replace(/\.$/, "");
      renderFeed(true);
    });
  });

  /* Position sur le trajet */
  var R = D.route, RK = D.km, vb = D.vbco;
  function posAt(km) {
    var lo = 0, hi = RK.length - 1;
    while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (RK[mid] < km) lo = mid; else hi = mid; }
    var t = Math.min(1, Math.max(0, (km - RK[lo]) / ((RK[hi] - RK[lo]) || 1)));
    var a = R[lo], b = R[hi];
    return { x: a[0] + (b[0] - a[0]) * t, y: a[1] + (b[1] - a[1]) * t, ang: Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI };
  }
  var hud = {
    clock: $("[data-mb-clock]"), speed: $("[data-mb-speed]"), next: $("[data-mb-next]"), nexteta: $("[data-mb-nexteta]"),
    prog: $("[data-mb-prog]"), done: $("[data-mb-kmdone]"), left: $("[data-mb-kmleft]"), sun: $("[data-mb-sun]"), webasto: $("[data-mb-webasto]")
  };
  var lastGauge = "";
  function paint() {
    var km = S.km, p = posAt(km), c = pct(p.x, p.y, vb), now = clockAt(km);
    car.style.left = c.l + "%"; car.style.top = c.t + "%";
    car.firstElementChild.nextElementSibling.style.setProperty("--a", p.ang + "deg");
    doneEls.forEach(function (el) { el.style.strokeDasharray = km.toFixed(1) + " " + (D.len + 10); });
    hud.clock.textContent = hm(now, true);
    hud.speed.textContent = S.speed;
    var nx = null;
    for (var i = 0; i < D.stops.length; i++) if (D.stops[i].km > km + .5) { nx = D.stops[i]; break; }
    hud.next.textContent = nx ? nx.nom : "Arrivée";
    hud.nexteta.textContent = nx ? "dans " + dur(clockAt(nx.km) - now) + " · " + kmf(nx.km - km) + NB + "km" : "Roberval";
    hud.prog.style.width = (km / D.len * 100).toFixed(1) + "%";
    hud.done.textContent = Math.round(km); hud.left.textContent = Math.round(D.len - km);
    var f = Math.min(1, Math.max(0, (now - SUNRISE) / (SUNSET - SUNRISE))), ang = Math.PI * (1 - f);
    hud.sun.setAttribute("cx", (40 + Math.cos(ang) * 36).toFixed(1)); hud.sun.setAttribute("cy", (27 - Math.sin(ang) * 22).toFixed(1));
    var lv = levels(km), g = [Math.round(lv.eau), Math.round(lv.propane), Math.round(lv.carb), Math.round(lv.batt), lv.webasto].join();
    if (g !== lastGauge) {
      lastGauge = g;
      ["eau", "propane", "carb", "batt"].forEach(function (k) {
        var v = Math.round(lv[k]), li = $('[data-g="' + k + '"]');
        $('[data-gv="' + k + '"]').textContent = v; $('[data-gb="' + k + '"]').style.width = v + "%";
        li.classList.toggle("is-low", v < 25); li.classList.toggle("is-mid", v >= 25 && v < 50);
      });
      hud.webasto.textContent = lv.webasto ? "À jour" : "Dû · 450" + NB + "h";
      hud.webasto.parentNode.parentNode.classList.toggle("is-ok", lv.webasto);
    }
  }

  /* Toast */
  var toastEl = $("[data-mb-toast]"), toastT;
  function toast(html) {
    toastEl.innerHTML = html; toastEl.classList.add("is-on");
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("is-on"); }, 3600);
  }

  /* Passages : arrêts faits, photos automatiques */
  var quiet = false;
  function passages(prev, km) {
    pois.forEach(function (p) {
      if (S.acc[p.id] && !S.done[p.id] && p.km > prev && p.km <= km) {
        S.done[p.id] = 1;
        var msg = p.cat === "eau" ? "Eau propre à 100" + NB + "%" : p.cat === "propane" ? "Propane à 100" + NB + "%" : p.cat === "webasto" ? "Webasto entretenu" : "Arrêt enregistré au journal";
        addLive({ lieu: p.nom, x: p.x, y: p.y, km: p.km, quand: hm(clockAt(p.km)), note: msg, src: p.src, stop: true });
        if (!quiet) toast((p.src ? '<img src="' + p.src + '" alt="">' : ico(p.cat)) + "<span><b>" + esc(msg) + "</b> · " + esc(p.nom) + "</span>");
      }
    });
    D.auto.forEach(function (a, i) {
      if (!S.shots[i] && a.km > prev && a.km <= km) {
        S.shots[i] = 1;
        addLive({ lieu: a.lieu, x: a.x, y: a.y, km: a.km, quand: hm(clockAt(a.km)), note: a.note, src: a.src });
        if (!quiet) toast((a.src ? '<img src="' + a.src + '" alt="">' : ico("photo")) + "<span><b>Photo enregistrée</b> · " + esc(a.lieu) + ", placée sur la carte du voyage</span>");
      }
    });
  }

  /* Boucle */
  var playing = true, visible = false, raf = 0, last = 0, KMPS = 3.2, feedT = 0, endT = 0;
  function loop(t) {
    raf = 0;
    if (!running()) { last = 0; return; }
    var dt = last ? Math.min(.1, (t - last) / 1000) : 0; last = t;
    var prev = S.km;
    S.km = Math.min(D.len, S.km + dt * KMPS);
    S.speed = Math.round(92 + Math.sin(t / 2300) * 5 + Math.sin(t / 900) * 2);
    passages(prev, S.km);
    paint();
    if (t - feedT > 450) { feedT = t; renderFeed(); }
    if (S.km >= D.len && !S.ended) {
      S.ended = true;
      toast(ico("check") + "<span><b>Arrivée à Roberval.</b> Le voyage est enregistré dans votre journal.</span>");
      endT = setTimeout(function () { restart(0); }, 6500);
    }
    if (!S.ended) raf = requestAnimationFrame(loop);
  }
  function running() { return playing && visible && tab === "copilote" && fx() && !S.ended; }
  function sync() {
    root.classList.toggle("is-run", running());
    root.classList.toggle("is-paused", !playing);
    if (running() && !raf) { last = 0; raf = requestAnimationFrame(loop); }
  }
  function restart(km) {
    clearTimeout(endT);
    var mode = S.mode; reset(km); S.mode = mode;
    live = [];
    quiet = true; passages(-1, km); quiet = false;
    paint(); renderFeed(true); sync();
  }
  var playBtn = $("[data-mb-play]");
  playBtn.addEventListener("click", function () {
    playing = !playing; playBtn.setAttribute("aria-label", playing ? "Pause" : "Lecture"); sync();
  });
  $("[data-mb-restart]").addEventListener("click", function () { restart(0); });

  /* ================================================================
     JOURNAL
     ================================================================ */
  var live = [], jtrip = null, jsel = -1, vbj = D.vbjo, replayT = [];
  var trips = {};
  D.trips.forEach(function (t) { trips[t.id] = t; });
  function addLive(e) {
    live.push(e);
    var lt = entries(trips.encours).length, tn = $('[data-tripn="encours"]');
    if (tn) tn.textContent = trips.encours.km + NB + "km · " + lt + NB + "souvenir" + (lt > 1 ? "s" : "");
    if (tab === "journal" && jtrip === "encours") renderJournal(true);
  }
  function entries(t) {
    if (!t.live) return t.entries;
    return t.entries.concat(live.slice().sort(function (a, b) { return a.km - b.km; }));
  }
  var jpins = $("[data-mb-jpins]"), viewer = { ph: $("[data-mb-vph]"), lieu: $("[data-mb-vlieu]"), note: $("[data-mb-vnote]"), geo: $("[data-mb-vgeo]") };
  function photoBox(src, alt) {
    return src ? '<img src="' + src + '" alt="' + esc(alt) + '" loading="lazy" decoding="async">'
      : '<span class="mb-noph" role="img" aria-label="' + esc(alt) + ' · photo à venir">' + ico("photo") + "<small>Photo à venir</small></span>";
  }
  function geoOf(e) {
    if (e.geo) return e.geo;
    var lat = 48.95 - e.y / 111.13, lon = -73.9 + e.x / (111.32 * Math.cos(47.05 * Math.PI / 180));
    return lat.toFixed(2).replace(".", ",") + "° N · " + (-lon).toFixed(2).replace(".", ",") + "° O";
  }
  function select(i, scroll) {
    var t = trips[jtrip], es = entries(t), e = es[i];
    if (!e) return;
    jsel = i;
    viewer.ph.innerHTML = photoBox(e.src, e.lieu);
    viewer.lieu.textContent = e.lieu; viewer.note.textContent = e.note;
    viewer.geo.textContent = e.quand + " · " + geoOf(e) + (e.src ? " · photo géolocalisée" : " · point enregistré");
    $$(".mb-jpin", jpins).forEach(function (b, k) { b.classList.toggle("is-sel", k === i); });
    $$(".mb-tl button").forEach(function (b, k) { b.classList.toggle("is-sel", k === i); });
    if (scroll) { var b = $$(".mb-tl button")[i]; if (b) { var tl = $("[data-mb-tl]"); tl.scrollTo({ top: b.parentNode.offsetTop - tl.offsetTop - 40, behavior: fx() ? "smooth" : "auto" }); } }
  }
  function renderJournal(keepSel) {
    replayT.forEach(clearTimeout); replayT = [];
    if (!jtrip) jtrip = entries(trips.encours).some(function (e) { return e.src; }) ? "encours" : "mauricie";
    var t = trips[jtrip], es = entries(t);
    var lt = entries(trips.encours).length, tn = $('[data-tripn="encours"]');
    if (tn) tn.textContent = trips.encours.km + NB + "km · " + lt + NB + "souvenir" + (lt > 1 ? "s" : "");
    $$(".mb-trip").forEach(function (p) {
      var on = p.getAttribute("data-trip") === jtrip;
      p.classList.toggle("is-on", on);
      p.style.strokeDasharray = ""; p.style.strokeDashoffset = ""; p.style.transition = "";
      if (on) p.parentNode.appendChild(p);
    });
    $$(".mb-tripc").forEach(function (b) { var on = b.getAttribute("data-trip") === jtrip; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
    $("[data-mb-jtitle]").textContent = t.nom;
    jpins.innerHTML = es.map(function (e, i) {
      var c = pct(e.x, e.y, vbj);
      return '<button type="button" class="mb-jpin" style="left:' + c.l.toFixed(2) + "%;top:" + c.t.toFixed(2) + '%" data-i="' + i + '" aria-label="' + esc(e.lieu) + '">' +
        (e.src ? '<img src="' + e.src + '" alt="" loading="lazy" decoding="async">' : ico(e.stop ? "check" : "pin")) + "</button>";
    }).join("");
    var tl = $("[data-mb-tl]"), n0 = tl.children.length;
    tl.innerHTML = es.map(function (e, i) {
      return '<li' + (keepSel && i >= n0 ? ' class="is-new"' : "") + '><button type="button" data-i="' + i + '"><span class="mb-tl-ph' + (e.src ? "" : " is-pt") + '">' +
        (e.src ? '<img src="' + e.src + '" alt="" loading="lazy" decoding="async">' : ico(e.stop ? "check" : "pin")) + "</span><span><small>" + esc(e.quand) + "</small><b>" + esc(e.lieu) +
        '</b><span class="mb-tl-n">' + esc(e.note) + "</span></span></button></li>";
    }).join("");
    var photos = es.filter(function (e) { return e.src; }).length;
    var kmDone = t.live ? Math.round(S.km) + NB + "/" + NB + t.km : t.km;
    $("[data-mb-jstats]").innerHTML =
      "<div><dt>Kilomètres</dt><dd>" + kmDone + "</dd></div><div><dt>Jours</dt><dd>" + t.jours + "</dd></div>" +
      "<div><dt>Souvenirs</dt><dd>" + es.length + "</dd></div><div><dt>Photos</dt><dd>" + photos + "</dd></div>";
    var sel = keepSel ? es.length - 1 : Math.max(0, es.map(function (e) { return !!e.src; }).lastIndexOf(true));
    select(sel);
  }
  jpins.addEventListener("click", function (e) { var b = e.target.closest(".mb-jpin"); if (b) select(+b.getAttribute("data-i"), true); });
  $("[data-mb-tl]").addEventListener("click", function (e) { var b = e.target.closest("button[data-i]"); if (b) select(+b.getAttribute("data-i")); });
  function pickTrip(id) { jtrip = id; renderJournal(); }
  $$(".mb-tripc").forEach(function (b) { b.addEventListener("click", function () { pickTrip(b.getAttribute("data-trip")); }); });
  $$(".mb-trip-hit").forEach(function (p) { p.addEventListener("click", function () { pickTrip(p.getAttribute("data-trip-hit")); }); });
  $("[data-mb-replay]").addEventListener("click", function () {
    renderJournal();
    var t = trips[jtrip], es = entries(t), path = $('.mb-trip[data-trip="' + jtrip + '"]');
    if (!fx()) { select(0); return; }
    var L = path.getTotalLength(), T = 900 + es.length * 1100;
    path.style.transition = "none"; path.style.strokeDasharray = L + " " + L; path.style.strokeDashoffset = L;
    path.getBoundingClientRect();
    path.style.transition = "stroke-dashoffset " + T + "ms cubic-bezier(.45,0,.25,1)"; path.style.strokeDashoffset = "0";
    var pins = $$(".mb-jpin", jpins);
    pins.forEach(function (b) { b.classList.add("is-hide"); });
    es.forEach(function (e, i) {
      replayT.push(setTimeout(function () { pins[i] && pins[i].classList.remove("is-hide"); select(i, true); }, 500 + i * 1100));
    });
  });

  /* ================================================================
     VÉHICULES
     ================================================================ */
  $$(".mb-vtab").forEach(function (b) {
    b.addEventListener("click", function () {
      var id = b.getAttribute("data-veh");
      $$(".mb-vtab").forEach(function (o) { var on = o === b; o.classList.toggle("is-on", on); o.setAttribute("aria-pressed", on ? "true" : "false"); });
      $$(".mb-veh").forEach(function (v) { var on = v.getAttribute("data-veh") === id; v.hidden = !on; v.classList.toggle("is-new", on); });
    });
  });
  $$(".mb-veh").forEach(function (v) {
    var fig = $(".mb-veh-ph", v), img = fig && $("img", fig);
    if (img && fig.classList.contains("is-zoom")) fig.style.setProperty("--o", img.style.objectPosition || "50% 50%");
    var box = $("[data-mb-confirm]", v), q = $("[data-mb-cq]", v), res = $("[data-mb-cres]", v), pending = null;
    $$(".mb-cmd", v).forEach(function (b) {
      b.addEventListener("click", function () {
        pending = b; q.textContent = b.getAttribute("data-q"); box.hidden = false; res.textContent = ""; res.className = "mb-cres";
        $("[data-mb-yes]", v).focus({ preventScroll: true });
      });
    });
    $("[data-mb-no]", v).addEventListener("click", function () { box.hidden = true; if (pending) pending.focus({ preventScroll: true }); res.textContent = "Annulé · rien n’a été envoyé."; pending = null; });
    $("[data-mb-yes]", v).addEventListener("click", function () {
      var b = pending; if (!b) return;
      box.hidden = true; pending = null;
      b.classList.add("is-wait"); res.className = "mb-cres"; res.innerHTML = '<span class="mb-spin" aria-hidden="true"></span>Commande envoyée au véhicule…';
      setTimeout(function () {
        b.classList.remove("is-wait"); b.classList.add("is-done");
        res.className = "mb-cres is-ok"; res.textContent = b.getAttribute("data-ok");
      }, reduce ? 300 : 1300);
    });
  });

  /* ---------------- Démarrage ---------------- */
  quiet = true; passages(-1, S.km); quiet = false;
  paint();
  renderFeed(true);
  booted = true;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; sync(); }, { threshold: 0.15 }).observe(mapCo);
  } else { visible = true; sync(); }
  // html.fx est posé par wow.js : relancer une fois qu'il est en place.
  setTimeout(sync, 400);
})();
