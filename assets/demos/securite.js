/* JARVIS — démo « Sécurité intelligente » (solution 03).
   « Six notifications deviennent un seul événement compris. »
   Mur de quatre caméras simulées : des silhouettes passent, des cadres de
   détection les suivent, chaque alerte brute file vers la chronologie, puis
   JARVIS relie les alertes et les fusionne en un seul événement expliqué.
   Les actions sensibles attendent « Approuver », puis : envoyé → confirmé
   (une commande n'est réussie qu'une fois l'état relu).
   Tout est simulé. Sans JavaScript, le balisage montre l'état final.
   Mouvement réduit : état final directement, aucune boucle.
   Hors écran : tout se met en pause. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="securite"]');
  if (!root || !window.requestAnimationFrame) return;

  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var wide = window.matchMedia ? matchMedia("(min-width: 881px)") : { matches: true };
  var W = 1672, H = 941, BASE = H * 0.3; // taille des images · hauteur de référence d'une silhouette
  var NBSP = " ";

  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function tog(n, c, on) { if (n.classList.contains(c) !== !!on) n.classList.toggle(c, !!on); }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function hms(s) { s = Math.floor(s) % 86400; return pad(Math.floor(s / 3600)) + ":" + pad(Math.floor(s / 60) % 60) + ":" + pad(s % 60); }
  function secs(str) { var p = str.split(":"); return +p[0] * 3600 + +p[1] * 60 + +(p[2] || 0); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function pct(v, of) { return (v / of * 100).toFixed(3); }
  function v43(vx) { return [vx, 0, H * 4 / 3, H]; }
  function stageCss(v) {
    return "left:" + (-v[0] / v[2] * 100).toFixed(3) + "%;top:" + (-v[1] / v[3] * 100).toFixed(3) +
      "%;width:" + (W / v[2] * 100).toFixed(3) + "%;height:" + (H / v[3] * 100).toFixed(3) + "%";
  }
  function cvar(k) {
    var m = { access: "alert", door: "alert", alert: "alert" };
    return "var(--sx-" + (m[k] || k) + ")";
  }

  /* ---------- Icônes ---------- */
  var ICON = {
    move: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="1.6"/><path d="M4.6 4.6a4.8 4.8 0 0 0 0 6.8M11.4 4.6a4.8 4.8 0 0 1 0 6.8M2.6 2.6a7.6 7.6 0 0 0 0 10.8M13.4 2.6a7.6 7.6 0 0 1 0 10.8"/></svg>',
    person: '<svg viewBox="0 0 16 16"><circle cx="8" cy="5" r="2.6"/><path d="M3 14c.6-3 2.6-4.6 5-4.6s4.4 1.6 5 4.6"/></svg>',
    vehicle: '<svg viewBox="0 0 16 16"><path d="M2.5 11V9l1.3-3.3A1.5 1.5 0 0 1 5.2 4.8h5.6a1.5 1.5 0 0 1 1.4.9L13.5 9v2z"/><circle cx="5" cy="11.5" r="1.2"/><circle cx="11" cy="11.5" r="1.2"/></svg>',
    parcel: '<svg viewBox="0 0 16 16"><path d="M2.5 5 8 2.5 13.5 5v6L8 13.5 2.5 11z"/><path d="M2.5 5 8 7.5 13.5 5M8 7.5v6"/></svg>',
    bell: '<svg viewBox="0 0 16 16"><path d="M4 11V7.5a4 4 0 0 1 8 0V11l1 1.5H3z"/><path d="M6.5 14a1.6 1.6 0 0 0 3 0"/></svg>',
    alert: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="5.6"/><path d="M8 5v3.2l2 1.3"/></svg>',
    access: '<svg viewBox="0 0 16 16"><rect x="2.5" y="4" width="11" height="8" rx="1.5"/><path d="M5 7h6M5 9.5h3"/><path d="m11 9 2 2m0-2-2 2"/></svg>',
    door: '<svg viewBox="0 0 16 16"><path d="M4 14V2.5h8V14M2.5 14h11"/><circle cx="10" cy="8.5" r=".7"/></svg>',
    lights: '<svg viewBox="0 0 16 16"><path d="M6 13.5h4M6.3 11.3h3.4c0-1.7 2.1-2.5 2.1-5.1a3.8 3.8 0 0 0-7.6 0c0 2.6 2.1 3.4 2.1 5.1z"/></svg>',
    talk: '<svg viewBox="0 0 16 16"><path d="M2.5 6.3h2.6L8.6 3.5v9L5.1 9.7H2.5z"/><path d="M10.8 6a2.8 2.8 0 0 1 0 4M12.6 4.3a5.2 5.2 0 0 1 0 7.4"/></svg>',
    call: '<svg viewBox="0 0 16 16"><path d="M2.5 3.5h11v7.5h-6l-3 2.4V11h-2z"/><path d="M5.5 6.5h5M5.5 8.5h3"/></svg>',
    cam: '<svg viewBox="0 0 16 16"><rect x="2" y="4.5" width="12" height="8.5" rx="1.5"/><circle cx="8" cy="8.7" r="2.3"/><path d="M5.5 4.5 6.5 3h3l1 1.5"/></svg>'
  };

  /* Silhouette simulée (60 × 160, pieds en bas au centre). */
  var PERSON =
    '<svg viewBox="0 0 60 160" aria-hidden="true" focusable="false">' +
    '<defs><linearGradient id="sgT@" x1="0" y1="0" x2=".25" y2="1"><stop class="g0" offset="0"/><stop class="g1" offset=".4"/><stop class="g2" offset="1"/></linearGradient>' +
    '<linearGradient id="sgL@" x1="0" y1="0" x2="0" y2="1"><stop class="g3" offset="0"/><stop class="g4" offset="1"/></linearGradient></defs>' +
    '<ellipse class="p-shadow" cx="30" cy="157" rx="17" ry="3"/>' +
    '<g class="p-body">' +
    '<path class="p-leg p-rim p-legL" fill="url(#sgL@)" d="M16.5 86H30l-1.5 36-1 30c0 3-1.5 4.5-4.5 4.5h-5c-1.5 0-1.5-2.5.5-3.5l1-31z"/>' +
    '<path class="p-leg p-rim p-legR" fill="url(#sgL@)" d="M30 86h13.5l-3 36 1 31c2 1 2 3.5.5 3.5h-5c-3 0-4.5-1.5-4.5-4.5l-1-30z"/>' +
    '<path class="p-top p-rim" fill="url(#sgT@)" d="M26 23h8l1 5c7 1 12 3.5 13 9l-2 25-2 26H16l-2-26-2-25c1-5.5 6-8 13-9z"/>' +
    '<path class="p-strip" d="M13.6 57h32.8l-.2 3H13.8zM13.9 65h32.2l-.2 3H14.1z"/>' +
    '<path class="p-top p-rim p-armL" fill="url(#sgT@)" d="M12.5 35c-3 13-3.5 27-2.5 43 .3 4.5 5 4.5 5.2 0 .4-14 1.4-28 3.3-40z"/>' +
    '<path class="p-top p-rim p-armR" fill="url(#sgT@)" d="M47.5 35c3 13 3.5 27 2.5 43-.3 4.5-5 4.5-5.2 0-.4-14-1.4-28-3.3-40z"/>' +
    '<ellipse class="p-skin p-rim" cx="30" cy="15" rx="8" ry="9.5"/>' +
    '<path class="p-hood p-top p-rim" d="M19.5 18c-1-11 4.5-15.5 10.5-15.5S41.5 7 40.5 18c-.3 6-3.5 10-6.5 11h-8c-3-1-6.2-5-6.5-11z"/>' +
    '<path class="p-cap p-top" d="M21.5 11c.5-6 4.5-6.5 8.5-6.5s8 .5 8.5 6.5l4.5 1.5c0 1-2 1.5-4.5 1L21.5 13z"/>' +
    '<g class="p-box"><path d="M13 49h34v26H13z" fill="#93724a"/><path d="m13 49 4-5h26l4 5z" fill="#b48f60"/><path d="M30 49v26" stroke="#e6d3ab" stroke-opacity=".55" stroke-width="2"/></g>' +
    "</g></svg>";
  var PARCEL =
    '<svg viewBox="0 0 74 52" aria-hidden="true" focusable="false">' +
    '<path d="M4 17h40v33H4z" fill="#8a6a43"/><path d="M44 17 70 6v33L44 50z" fill="#6b5133"/>' +
    '<path d="M4 17 30 6h40L44 17z" fill="#b08b5d"/><path d="M15 17 41 6M24 17v33" stroke="#e3cfa6" stroke-opacity=".55" stroke-width="2.4"/></svg>';

  /* ---------- Sites et caméras ---------- */
  var M = "/media/solutions/";
  var IMG = {
    entree: M + "camera-front-entry-v1.webp",
    allee: M + "camera-driveway-garage-v1.webp",
    terrasse: M + "camera-rear-terrace-v1.webp",
    piscine: M + "camera-pool-spa-v1.webp",
    parking: M + "security-enterprise-parking-v1.webp",
    quai: M + "security-enterprise-delivery-v1.webp"
  };
  var SITES = {
    maison: {
      label: "Résidence · 4 caméras",
      cams: [
        { img: "entree", name: "Entrée avant", view: v43(60), alt: "Caméra de l’entrée avant : porte, marches et allée éclairées le soir" },
        { img: "allee", name: "Allée et garage", view: v43(220), alt: "Caméra de l’allée : porte de garage et entrée de cour" },
        { img: "terrasse", name: "Terrasse arrière", view: v43(400), alt: "Caméra de la terrasse arrière : salon extérieur, table et piscine" },
        { img: "piscine", name: "Piscine et spa", view: v43(210), alt: "Caméra de la piscine et du spa" }
      ],
      sensors: [
        { id: "bell", name: "Sonnette", idle: "Au repos" },
        { id: "door", name: "Porte d’entrée", idle: "Verrouillée" },
        { id: "terrace", name: "Détecteur · terrasse", idle: "Calme" },
        { id: "alarm", name: "Alarme", idle: "Désarmée" }
      ]
    },
    entrepot: {
      label: "Entrepôt · 4 caméras",
      cams: [
        { img: "parking", name: "Stationnement", view: v43(100), alt: "Caméra du stationnement de l’entreprise, avec un véhicule garé" },
        { img: "parking", name: "Portail", view: [100, 215, 520, 390], alt: "Vue rapprochée du portail du stationnement" },
        { img: "quai", name: "Quai de livraison", view: v43(330), alt: "Caméra du quai de livraison, avec le camion de l’entreprise" },
        { img: "quai", name: "Porte de service", view: [1230, 205, 442, 331.5], alt: "Vue rapprochée de la porte de service du quai" }
      ],
      sensors: [
        { id: "door", name: "Porte de service", idle: "Fermée" },
        { id: "badge", name: "Contrôle d’accès", idle: "Prêt" },
        { id: "motion", name: "Détecteur · entrepôt", idle: "Calme" },
        { id: "alarm", name: "Alarme", idle: "Armée" }
      ]
    }
  };

  /* ---------- Situations simulées ----------
     Temps en millisecondes réelles depuis le début. Positions en pixels de
     l'image d'origine (1672 × 941) : [t, x des pieds, y des pieds, hauteur]. */
  var P = "Personne · ", PC = NBSP + "%";
  var SC = {
    livraison: {
      site: "maison", start: "21:41:58", rate: 5, mood: "", alarm: "Désarmée",
      walkers: [
        { id: "a", img: "allee", kind: "livreur", carry: true, keys: [[600, 150, 790, 360], [3400, 760, 640, 275], [5000, 1380, 525, 195]] },
        { id: "b", img: "entree", kind: "livreur", carry: [0, 8150], keys: [[4800, 1000, 1010, 560], [6300, 640, 830, 430], [7400, 430, 610, 325], [8000, 255, 508, 288], [8800, 255, 508, 288], [9600, 430, 610, 325], [10300, 760, 860, 450], [10900, 1000, 1010, 560]] },
        { id: "c", img: "allee", kind: "livreur", keys: [[10300, 1380, 525, 195], [12400, 700, 650, 280], [13900, 150, 790, 360]] }
      ],
      props: [
        { img: "entree", kind: "ring", at: 7900, dur: 1700, x: 378, y: 318 },
        { img: "entree", kind: "parcel", at: 8150, x: 350, y: 516 }
      ],
      boxes: [
        { tile: 1, track: "a", from: 900, to: 4900, labels: [[900, "Mouvement", "move"], [1900, P + "94" + PC, "person"]] },
        { tile: 0, track: "b", from: 5300, to: 10700, labels: [[5300, P + "96" + PC, "person"]] },
        { tile: 0, rect: [303, 455, 94, 70], from: 8500, labels: [[8500, "Colis · 91" + PC, "parcel"]] },
        { tile: 1, track: "c", from: 10600, to: 13800, labels: [[10600, P + "93" + PC, "person"]] }
      ],
      events: [
        { t: 1000, k: "move", title: "Mouvement — allée", src: "Caméra 02 · Allée et garage", tile: 1 },
        { t: 2000, k: "person", title: "Personne — allée", src: "Caméra 02 · 94" + PC, tile: 1 },
        { t: 5500, k: "person", title: "Personne — entrée avant", src: "Caméra 01 · 96" + PC, tile: 0 },
        { t: 7900, k: "bell", title: "Sonnette — entrée avant", src: "Sonnette de la porte", sensor: "bell", state: "Appel", tile: 0 },
        { t: 8700, k: "parcel", title: "Colis déposé — entrée", src: "Caméra 01 · 91" + PC, tile: 0 },
        { t: 10900, k: "person", title: "Départ — allée", src: "Caméra 02 · 93" + PC, tile: 1 }
      ],
      evidence: [
        { tile: 1, t: 2600, c: [700, 520], w: 760, cap: "Allée" },
        { tile: 0, t: 8000, c: [330, 380], w: 640, cap: "Sonnette" },
        { tile: 0, t: 10400, c: [340, 470], w: 480, cap: "Colis" }
      ],
      inc: {
        lvl: "ok", lvlTxt: "Normal",
        sum: "<b>21" + NBSP + "h" + NBSP + "42 — Livraison :</b> un livreur a déposé un colis à l’entrée puis est reparti. Rien d’anormal.",
        why: "même personne suivie sur 2 caméras · sonnette · colis",
        calm: "Aucune action requise. Le colis reste sous l’œil de la caméra 01.",
        acts: []
      }
    },

    visiteur: {
      site: "maison", start: "02:12:50", rate: 16, mood: "ir", alarm: "Armée · nuit",
      walkers: [
        { id: "a", img: "allee", kind: "hood", keys: [[400, 150, 800, 370], [2200, 640, 685, 300], [2900, 640, 685, 300], [4300, 1380, 525, 195]] },
        { id: "b", img: "entree", kind: "hood", keys: [[4100, 1000, 1010, 560], [5400, 640, 830, 430], [6300, 470, 640, 335], [8800, 470, 640, 335], [9600, 760, 860, 450], [10300, 1050, 1010, 560]] },
        { id: "c", img: "terrasse", kind: "hood", stay: true, keys: [[9900, 1190, 300, 150], [11300, 1240, 470, 250], [12000, 1255, 590, 305]] }
      ],
      props: [],
      boxes: [
        { tile: 1, track: "a", from: 700, to: 4200, labels: [[700, "Mouvement", "move"], [1500, P + "92" + PC, "person"]] },
        { tile: 0, track: "b", from: 4500, to: 10200, labels: [[4500, P + "95" + PC, "person"], [8800, "Présence · 40" + NBSP + "s", "alert"]] },
        { tile: 2, track: "c", from: 10300, labels: [[10300, P + "93" + PC, "person"]] }
      ],
      events: [
        { t: 700, k: "move", title: "Mouvement — allée", src: "Caméra 02 · Allée et garage", tile: 1 },
        { t: 1500, k: "person", title: "Personne non reconnue — allée", src: "Caméra 02 · 92" + PC, tile: 1 },
        { t: 4600, k: "person", title: "Personne — entrée avant", src: "Caméra 01 · 95" + PC, tile: 0 },
        { t: 8800, k: "alert", title: "Présence prolongée — entrée", src: "Caméra 01 · 40" + NBSP + "s devant la porte", tile: 0 },
        { t: 10400, k: "person", title: "Personne — terrasse arrière", src: "Caméra 03 · 93" + PC, tile: 2 },
        { t: 11600, k: "move", title: "Mouvement — terrasse", src: "Détecteur extérieur", sensor: "terrace", state: "Mouvement" }
      ],
      evidence: [
        { tile: 1, t: 2500, c: [640, 560], w: 760, cap: "Allée" },
        { tile: 0, t: 7500, c: [470, 480], w: 700, cap: "Entrée" },
        { tile: 2, t: 12300, c: [1210, 450], w: 760, cap: "Terrasse" }
      ],
      inc: {
        lvl: "warn", lvlTxt: "À vérifier",
        sum: "<b>2" + NBSP + "h" + NBSP + "13 — Visiteur inconnu :</b> une personne non reconnue a remonté l’allée, est restée 40 secondes devant la porte, puis a contourné la maison jusqu’à la terrasse. Personne n’est attendu cette nuit.",
        why: "même silhouette sur 3 caméras · détecteur de la terrasse",
        acts: [
          { fx: "lights", ico: "lights", label: "Allumer l’éclairage extérieur", sent: "Commande envoyée aux 8 lumières extérieures", ok: "Confirmé · état relu : 8 lumières sur 8 allumées." },
          { fx: "talk", ico: "talk", label: "Parler par l’interphone", sent: "Message diffusé sur la terrasse", ok: "Confirmé · état relu : message diffusé en entier." }
        ]
      }
    },

    entrepot: {
      site: "entrepot", start: "23:06:40", rate: 6, mood: "dim", alarm: "Armée",
      walkers: [
        { id: "a", img: "parking", kind: "dark", keys: [[1900, 690, 650, 215], [3600, 960, 565, 170], [4800, 1190, 470, 122]] },
        { id: "b", img: "quai", kind: "dark", keys: [[4600, 300, 665, 215], [6200, 1000, 700, 235], [7200, 1430, 565, 205], [7700, 1505, 530, 196], [9000, 1505, 530, 196], [9400, 1515, 522, 190]] }
      ],
      props: [
        { img: "parking", kind: "tail", at: 0, until: 2000, x: 238, y: 576 },
        { img: "quai", kind: "door", at: 8600, rect: [1442, 266, 142, 254] }
      ],
      boxes: [
        { tile: 0, rect: [150, 440, 532, 222], from: 600, labels: [[600, "Véhicule · 96" + PC, "vehicle"]] },
        { tile: 0, track: "a", from: 2200, to: 4700, labels: [[2200, P + "92" + PC, "person"]] },
        { tile: 2, rect: [705, 345, 480, 275], from: 300, labels: [[300, "Camion connu · ignoré", "known"]] },
        { tile: 2, track: "b", from: 5000, to: 9300, labels: [[5000, P + "95" + PC, "person"]] },
        { tile: 3, track: "b", from: 6800, to: 9300, labels: [[6800, P + "97" + PC, "person"], [8000, "Aucun badge", "alert"]] }
      ],
      events: [
        { t: 700, k: "vehicle", title: "Véhicule — stationnement", src: "Caméra 01 · 96" + PC, tile: 0 },
        { t: 2400, k: "person", title: "Personne — stationnement", src: "Caméra 01 · 92" + PC, tile: 0 },
        { t: 5200, k: "person", title: "Personne — quai de livraison", src: "Caméra 03 · 95" + PC, tile: 2 },
        { t: 8000, k: "access", title: "Aucun badge présenté", src: "Contrôle d’accès · porte de service", sensor: "badge", state: "Refusé", tile: 3 },
        { t: 8600, k: "door", title: "Porte de service ouverte", src: "Capteur de porte", sensor: "door", state: "Ouverte" },
        { t: 10200, k: "move", title: "Mouvement — entrepôt", src: "Détecteur intérieur · zone armée", sensor: "motion", state: "Mouvement" }
      ],
      evidence: [
        { tile: 0, t: 2600, c: [560, 560], w: 820, cap: "Arrivée" },
        { tile: 2, t: 6000, c: [900, 540], w: 900, cap: "Quai" },
        { tile: 3, t: 8800, c: [1480, 420], w: 400, cap: "Porte" }
      ],
      inc: {
        lvl: "crit", lvlTxt: "Prioritaire",
        sum: "<b>23" + NBSP + "h" + NBSP + "07 — Entrée après la fermeture :</b> une personne arrivée en voiture a ouvert la porte de service du quai sans présenter de badge. L’entrepôt est fermé depuis 18" + NBSP + "h.",
        why: "même personne sur 3 caméras · badge · porte · détecteur",
        acts: [
          { fx: "dock", ico: "lights", label: "Allumer l’éclairage du quai", sent: "Commande envoyée aux projecteurs du quai", ok: "Confirmé · état relu : quai éclairé." },
          { fx: "call", ico: "call", label: "Prévenir le responsable de garde", sent: "Message envoyé au responsable de garde", ok: "Confirmé · accusé de réception reçu." }
        ]
      }
    }
  };
  var ORDER = ["livraison", "visiteur", "entrepot"];

  /* ---------- Éléments ---------- */
  var body = $(".demo-body"), wall = $("[data-sec-wall]"), sensorsUl = $("[data-sec-sensors]");
  var feed = $(".sec-feed"), rawList = $("[data-sec-raw]"), empty = $("[data-sec-empty]");
  var inc = $("[data-sec-inc]"), lvl = $("[data-sec-lvl]"), when = $("[data-sec-when]"), sum = $("[data-sec-sum]");
  var why = $("[data-sec-why]"), evBox = $("[data-sec-ev]"), actsWrap = $("[data-sec-acts]"), actList = $("[data-sec-actlist]");
  var calm = $("[data-sec-calm]"), follow = $("[data-sec-follow]"), phaseEl = $("[data-sec-phase]"), nRaw = $("[data-sec-n]"), live = $("[data-sec-live]");
  var clockEl = $("[data-sec-clock]"), siteEl = $("[data-sec-site]"), wires = $("[data-sec-wires]");
  var btns = $$("[data-sec-scen]"), replay = $("[data-sec-replay]");
  if (!wall || !feed || !inc || !calm) return;

  var curSite = "maison";
  var tiles = $$(".sec-cam", wall).map(function (fig, i) {
    return {
      el: fig, view: $(".sec-view", fig), stage: $(".sec-stage", fig), ts: $("[data-sec-ts]", fig),
      st: $("[data-sec-st]", fig), name: $(".sec-name", fig), cam: SITES.maison.cams[i], k: null
    };
  });
  var today = (function () { var d = new Date(); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); })();

  root.classList.add("is-live");

  /* Minuteries annulables (une nouvelle situation efface les précédentes) */
  var timers = [];
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function clearLater() { timers.forEach(clearTimeout); timers = []; }

  /* ---------- Scènes ---------- */
  function buildStage(img, view, alt) {
    var s = el("div", "sec-stage");
    s.setAttribute("style", stageCss(view));
    var im = document.createElement("img");
    im.decoding = "async";
    im.alt = alt || "";
    im.src = IMG[img];
    s.appendChild(im);
    return s;
  }

  function setSite(key, animate) {
    if (curSite === key) return;
    curSite = key;
    var site = SITES[key];
    if (siteEl) siteEl.textContent = site.label;
    tiles.forEach(function (t, i) {
      var cam = site.cams[i], old = t.stage, ns = buildStage(cam.img, cam.view, cam.alt);
      t.cam = cam;
      t.name.innerHTML = "<b>CAM 0" + (i + 1) + "</b> <span>" + cam.name + "</span>";
      if (animate && !reduce) {
        ns.classList.add("is-enter");
        old.parentNode.insertBefore(ns, old.nextSibling);
        var im = ns.querySelector("img");
        var go = function () {
          requestAnimationFrame(function () {
            ns.classList.remove("is-enter");
            old.classList.add("is-leave");
            setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, 800);
          });
        };
        if (im.decode) im.decode().then(go, go); else im.onload = go;
      } else {
        old.parentNode.replaceChild(ns, old);
      }
      t.stage = ns;
    });
  }

  function setSensors(sc) {
    sensorsUl.innerHTML = SITES[sc.site].sensors.map(function (s) {
      var idle = s.id === "alarm" ? sc.alarm : s.idle;
      var armed = s.id === "alarm" && /^Armée/.test(idle);
      return '<li class="sec-sen' + (armed ? " is-armed" : "") + '" data-sensor="' + s.id + '"><i aria-hidden="true"></i><span>' +
        s.name + "</span><b>" + idle + "</b></li>";
    }).join("");
  }
  function sensorEl(id) { return sensorsUl.querySelector('[data-sensor="' + id + '"]'); }
  function sensorHit(id, state, k) {
    var li = sensorEl(id);
    if (!li) return;
    li.style.setProperty("--c", cvar(k));
    li.querySelector("b").textContent = state;
    li.classList.add("is-set");
    li.classList.remove("is-hit"); void li.offsetWidth; li.classList.add("is-hit");
    if (id === "bell") {
      later(function () {
        li.querySelector("b").textContent = "Au repos";
        li.classList.remove("is-set", "is-hit");
      }, 3400);
    }
  }

  /* ---------- Silhouettes ---------- */
  function same(a, b) { return a[1] === b[1] && a[2] === b[2] && a[3] === b[3]; }
  function walkerAt(w, t) {
    var k = w.keys, n = k.length, end = k[n - 1][0];
    if (t < k[0][0] || (t > end && !w.stay)) return null;
    var p;
    if (t >= end) {
      p = { x: k[n - 1][1], y: k[n - 1][2], h: k[n - 1][3], mv: false };
    } else {
      var i = 0;
      while (i < n - 2 && t >= k[i + 1][0]) i++;
      var a = k[i], b = k[i + 1], u = (t - a[0]) / Math.max(1, b[0] - a[0]);
      var still = same(a, b);
      var s0 = i === 0 || same(k[i - 1], a), s1 = i + 1 === n - 1 || same(b, k[i + 2]);
      var e = s0 && s1 ? .5 - .5 * Math.cos(Math.PI * u) : s0 ? 1 - Math.cos(Math.PI * u / 2) : s1 ? Math.sin(Math.PI * u / 2) : u;
      p = { x: a[1] + (b[1] - a[1]) * e, y: a[2] + (b[2] - a[2]) * e, h: a[3] + (b[3] - a[3]) * e, mv: !still, left: still ? null : b[1] < a[1] };
    }
    var o = Math.min(1, (t - k[0][0]) / 280);
    if (!w.stay) o = Math.min(o, (end - t) / 280);
    p.o = clamp(o, 0, 1);
    return p;
  }
  function carrying(w, t) { return w.carry === true || (w.carry && t >= w.carry[0] && t < w.carry[1]); }
  var uid = 0;
  function makeSubj(w) { uid++; return el("div", "sec-subj k-" + w.kind, PERSON.replace(/@/g, uid)); }
  function placeSubj(n, p, w, t) {
    var s = n.style;
    s.setProperty("--x", pct(p.x, W));
    s.setProperty("--y", pct(p.y, H));
    s.setProperty("--k", (p.h / BASE).toFixed(4));
    s.opacity = p.o.toFixed(3);
    tog(n, "is-walk", p.mv);
    if (p.left != null) tog(n, "is-left", p.left);
    tog(n, "is-carry", carrying(w, t));
  }
  function drawWalker(w, t) {
    var p = walkerAt(w, t), list = run.wn[w.id] || (run.wn[w.id] = {});
    if (p && p.left == null && run.dir[w.id] != null) p.left = run.dir[w.id];
    if (p && p.left != null) run.dir[w.id] = p.left;
    tiles.forEach(function (tile, ti) {
      if (tile.cam.img !== w.img) return;
      var n = list[ti];
      if (!p) { if (n) n.style.opacity = 0; return; }
      if (!n || n.parentNode !== tile.stage) { n = list[ti] = makeSubj(w); tile.stage.appendChild(n); }
      placeSubj(n, p, w, t);
    });
  }

  /* ---------- Objets de scène ---------- */
  function propOn(p, t) { return t >= p.at && (p.until == null || t < p.until) && (p.dur == null || t < p.at + p.dur); }
  function makeProp(p) {
    var n = el("div", "sec-prop p-" + p.kind, p.kind === "parcel" ? PARCEL : null);
    var r = p.rect || (p.kind === "parcel" ? [p.x - 37, p.y - 52, 74, 52] : [p.x, p.y, 0, 0]);
    n.style.setProperty("--x", pct(r[0], W)); n.style.setProperty("--y", pct(r[1], H));
    n.style.setProperty("--w", pct(r[2], W)); n.style.setProperty("--h", pct(r[3], H));
    return n;
  }
  function kill(n) {
    if (!n) return;
    n.classList.add("is-off");
    setTimeout(function () { if (n.parentNode) n.parentNode.removeChild(n); }, 380);
  }
  function drawProp(p, i, t) {
    var on = propOn(p, t), rec = run.pn[i];
    if (on && !rec) {
      rec = run.pn[i] = [];
      tiles.forEach(function (tile) {
        if (tile.cam.img !== p.img) return;
        var n = makeProp(p);
        tile.stage.appendChild(n);
        rec.push(n);
      });
    } else if (!on && rec && rec.length) {
      rec.forEach(function (n) { if (n.parentNode) n.parentNode.removeChild(n); });
      run.pn[i] = [];
    }
  }

  /* ---------- Cadres de détection ---------- */
  function boxOn(b, t) { return t >= b.from && (b.to == null || t < b.to); }
  function boxLabel(b, t) { var j = 0; for (var i = 0; i < b.labels.length; i++) if (b.labels[i][0] <= t) j = i; return j; }
  function boxRect(b, t) {
    if (b.rect) return b.rect;
    var p = walkerAt(run.wmap[b.track], t);
    if (!p || p.o < .25) return null;
    return [p.x - p.h * .24, p.y - p.h * 1.01, p.h * .48, p.h * 1.05];
  }
  function makeBox() { return el("div", "sec-box", "<i></i><i></i><i></i><i></i><b></b>"); }
  function setLabel(n, L) {
    n.querySelector("b").textContent = L[1];
    n.className = n.className.replace(/\bt-\w+/g, "").trim() + " t-" + L[2];
  }
  function posBox(n, r, v) {
    var s = n.style;
    s.setProperty("--x", pct(r[0], W)); s.setProperty("--y", pct(r[1], H));
    s.setProperty("--w", pct(r[2], W)); s.setProperty("--h", pct(r[3], H));
    tog(n, "is-in", (r[1] - v[1]) / v[3] < .22);
    tog(n, "is-right", (r[0] + r[2] / 2 - v[0]) / v[2] > .6);
  }
  function drawBox(rb, t) {
    var b = rb.def, r = boxOn(b, t) && boxRect(b, t), tile = tiles[b.tile];
    if (!r) { if (rb.node) { kill(rb.node); rb.node = null; rb.lab = -1; } return; }
    if (!rb.node || rb.node.parentNode !== tile.stage) { rb.node = makeBox(); tile.stage.appendChild(rb.node); rb.lab = -1; }
    var j = boxLabel(b, t);
    if (j !== rb.lab) {
      setLabel(rb.node, b.labels[j]);
      if (rb.lab >= 0) { rb.node.classList.remove("is-swap"); void rb.node.offsetWidth; rb.node.classList.add("is-swap"); }
      rb.lab = j;
    }
    posBox(rb.node, r, tile.cam.view);
  }
  var ST = { move: "Mouvement", person: "Personne", vehicle: "Véhicule", parcel: "Colis", alert: "Alerte", known: "Connu" };
  function tileStatus() {
    var best = [null, null, null, null];
    run.boxes.forEach(function (rb) {
      if (!rb.node || rb.lab < 0) return;
      var k = rb.def.labels[rb.lab][2];
      if (k !== "known" || !best[rb.def.tile]) best[rb.def.tile] = k;
    });
    tiles.forEach(function (tile, i) {
      var k = best[i] || "calm";
      if (tile.k === k) return;
      tile.k = k;
      tile.st.textContent = k === "calm" ? "Calme" : ST[k];
      tile.st.className = "sec-st t-" + k;
    });
  }

  /* ---------- Effets visuels ---------- */
  function hit(tile, k) {
    tile.el.style.setProperty("--c", cvar(k));
    tile.el.classList.remove("is-hit"); void tile.el.offsetWidth; tile.el.classList.add("is-hit");
    later(function () { tile.el.classList.remove("is-hit"); }, 1300);
  }
  function flashTile(tile) {
    if (reduce) return;
    tile.el.classList.remove("is-flash"); void tile.el.offsetWidth; tile.el.classList.add("is-flash");
    later(function () { tile.el.classList.remove("is-flash"); }, 800);
  }
  function snap(e) {
    if (reduce) return;
    var tile = tiles[e.tile], chip = el("span", "sec-snap", ICON.cam + "Preuve capturée");
    chip.setAttribute("aria-hidden", "true");
    tile.el.appendChild(chip);
    flashTile(tile);
    later(function () { if (chip.parentNode) chip.parentNode.removeChild(chip); }, 1450);
  }
  function comet(fromEl, li, k) {
    if (reduce || !wide.matches || !fromEl || !wires || !wires.animate) return;
    var ico = li.querySelector(".sec-r-ico");
    var box = body.getBoundingClientRect(), a = fromEl.getBoundingClientRect(), b = ico.getBoundingClientRect();
    var sx = a.left + a.width / 2 - box.left, sy = a.top + a.height / 2 - box.top;
    var ex = b.left + b.width / 2 - box.left, ey = b.top + b.height / 2 - box.top;
    var dx = Math.max(80, (ex - sx) * .5);
    var d = "M" + sx.toFixed(1) + " " + sy.toFixed(1) + "C" + (sx + dx).toFixed(1) + " " + sy.toFixed(1) + " " +
      (ex - dx).toFixed(1) + " " + ey.toFixed(1) + " " + ex.toFixed(1) + " " + ey.toFixed(1);
    var NS = "http://www.w3.org/2000/svg";
    var g = document.createElementNS(NS, "g"), base = document.createElementNS(NS, "path"), dash = document.createElementNS(NS, "path");
    g.setAttribute("class", "sec-wire");
    g.style.setProperty("--c", cvar(k));
    base.setAttribute("d", d); base.setAttribute("class", "w-base");
    dash.setAttribute("d", d); dash.setAttribute("class", "w-dash");
    g.appendChild(base); g.appendChild(dash); wires.appendChild(g);
    var L = dash.getTotalLength(), seg = Math.min(130, L * .35);
    dash.style.strokeDasharray = seg + " " + (L + seg);
    dash.style.strokeDashoffset = seg;
    dash.animate([{ strokeDashoffset: seg }, { strokeDashoffset: -L }], { duration: 780, easing: "cubic-bezier(.55,0,.25,1)", fill: "forwards" });
    base.animate([{ opacity: 0 }, { opacity: .4, offset: .35 }, { opacity: 0 }], { duration: 1000, fill: "forwards" });
    later(function () { if (g.parentNode) g.parentNode.removeChild(g); }, 1100);
  }

  /* ---------- Chronologie ---------- */
  function phase(txt, kind) {
    phaseEl.textContent = txt;
    phaseEl.className = "sec-phase" + (kind ? " is-" + kind : "");
  }
  function fire(ev) {
    run.n++;
    empty.hidden = true;
    var li = el("li", "sec-r t-" + ev.k);
    li.style.setProperty("--i", run.n - 1);
    li.innerHTML = '<span class="sec-r-ico" aria-hidden="true">' + (ICON[ev.k] || ICON.move) + '</span><span class="sec-r-txt"><b>' +
      ev.title + "</b><small>" + ev.src + "</small></span><time>" + hms(simAt(ev.t)) + "</time>";
    rawList.appendChild(li);
    nRaw.textContent = run.n;
    if (!reduce) { nRaw.classList.remove("sec-n-raw-bump"); void nRaw.offsetWidth; nRaw.classList.add("sec-n-raw-bump"); }
    phase(run.n + (run.n > 1 ? " alertes reçues" : " alerte reçue"), "idle");
    if (ev.tile != null) hit(tiles[ev.tile], ev.k);
    if (ev.sensor) sensorHit(ev.sensor, ev.state, ev.k);
    comet(ev.sensor ? sensorEl(ev.sensor) : tiles[ev.tile].view, li, ev.k);
  }
  function linkPhase() {
    feed.classList.add("is-linking");
    phase("JARVIS relie les alertes…", "busy");
  }
  function collapsePhase() {
    var lis = $$(".sec-r", rawList);
    if (!lis.length) return;
    var top = lis[0].offsetTop;
    lis.forEach(function (li, j) {
      li.style.setProperty("--dy", (top - li.offsetTop + Math.min(j, 4) * 5) + "px");
      li.style.setProperty("--j", j);
    });
    feed.classList.add("is-collapsing");
    phase("Regroupement en 1 événement…", "busy");
  }
  function revealPhase() {
    buildThumbs();
    feed.classList.add("is-merged");
    inc.classList.add("is-on");
    phase("1 événement compris", "ok");
    live.textContent = sum.textContent;
  }
  function donePhase() {
    root.classList.add("is-done");
    var next = btns.filter(function (b) { return b.getAttribute("data-sec-scen") === ORDER[(ORDER.indexOf(run.key) + 1) % ORDER.length]; })[0];
    if (next && !reduce) next.classList.add("is-next");
  }

  /* ---------- Événement compris ---------- */
  function dur(sc) {
    var s = (sc.events[sc.events.length - 1].t - sc.events[0].t) / 1000 * sc.rate;
    return s < 60 ? Math.round(s / 5) * 5 + NBSP + "s" : Math.round(s / 60) + NBSP + "min";
  }
  function renderInc(sc) {
    var I = sc.inc;
    inc.classList.remove("is-on");
    lvl.className = "sec-lvl is-" + I.lvl;
    lvl.textContent = I.lvlTxt;
    when.textContent = "Durée · " + dur(sc);
    sum.innerHTML = I.sum;
    why.innerHTML = '<span class="sec-icos" aria-hidden="true">' + sc.events.map(function (e, i) {
      return '<i class="t-' + e.k + '" style="--i:' + i + '">' + (ICON[e.k] || ICON.move) + "</i>";
    }).join("") + "</span><span>" + sc.events.length + " alertes regroupées · " + I.why + "</span>";
    evBox.innerHTML = "";
    follow.innerHTML = "";
    actsWrap.hidden = !I.acts.length;
    calm.hidden = !I.calm;
    calm.lastChild.textContent = I.calm || "";
    actList.innerHTML = I.acts.map(function (a, i) {
      return '<li class="sec-act" data-i="' + i + '" data-state="ask"><div class="sec-act-main"><span class="sec-act-ico" aria-hidden="true">' +
        ICON[a.ico] + "</span><b>" + a.label + '</b><span class="sec-act-btns"><button type="button" data-act="ok">Approuver</button>' +
        '<button type="button" data-act="no">Ignorer</button></span><span class="sec-act-ok"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="m2.5 6.3 2.3 2.2 4.7-5"/></svg>Confirmé</span></div>' +
        '<ol class="sec-flow" aria-hidden="true"><li>Approuvé</li><li>Envoyé</li><li>Confirmé</li></ol>' +
        '<p class="sec-act-st" role="status"></p></li>';
    }).join("");
  }
  function buildThumbs() {
    var sc = run.sc;
    evBox.innerHTML = "";
    sc.evidence.forEach(function (e, i) {
      var tile = tiles[e.tile], cam = tile.cam, vw = e.w, vh = vw / 1.6;
      var v = [clamp(e.c[0] - vw / 2, 0, W - vw), clamp(e.c[1] - vh / 2, 0, H - vh), vw, vh];
      var fig = el("figure", "sec-th"), view = el("div", "sec-th-view" + (sc.mood === "ir" ? " is-ir" : ""));
      var s = buildStage(cam.img, v, "Preuve : " + (e.cap || cam.name));
      fig.style.setProperty("--i", i);
      sc.walkers.forEach(function (w) {
        if (w.img !== cam.img) return;
        var p = walkerAt(w, e.t);
        if (!p || p.o < .3) return;
        var n = makeSubj(w);
        placeSubj(n, p, w, e.t);
        s.appendChild(n);
      });
      sc.props.forEach(function (pr) { if (pr.img === cam.img && propOn(pr, e.t)) s.appendChild(makeProp(pr)); });
      run.boxes.forEach(function (rb) {
        var b = rb.def;
        if (b.tile !== e.tile || !boxOn(b, e.t)) return;
        var r = boxRect(b, e.t);
        if (!r) return;
        var n = makeBox();
        setLabel(n, b.labels[boxLabel(b, e.t)]);
        posBox(n, r, v);
        s.appendChild(n);
      });
      view.appendChild(s);
      fig.appendChild(view);
      fig.appendChild(el("figcaption", "", (e.cap || cam.name) + "<span> · " + hms(simAt(e.t)) + "</span>"));
      evBox.appendChild(fig);
    });
  }
  function addFollow(txt) {
    var p = el("p", "", "<b>Suivi</b>" + txt);
    follow.appendChild(p);
  }

  /* Approuver → envoyé → confirmé (l'état est relu avant de parler de réussite) */
  function act(li, a, ok) {
    if (li.getAttribute("data-state") !== "ask") return;
    var st = li.querySelector(".sec-act-st"), flow = [].slice.call(li.querySelectorAll(".sec-flow li"));
    if (!ok) {
      li.setAttribute("data-state", "skip");
      st.textContent = "Ignoré · aucune commande envoyée.";
      return;
    }
    li.setAttribute("data-state", "go");
    flow[0].classList.add("is-done");
    flow[1].classList.add("is-cur");
    st.textContent = "Approuvé par vous · envoi de la commande…";
    later(function () {
      flow[1].classList.remove("is-cur"); flow[1].classList.add("is-done"); flow[2].classList.add("is-cur");
      st.textContent = a.sent + " · relecture de l’état…";
      effect(a.fx);
    }, reduce ? 300 : 900);
    later(function () {
      flow[2].classList.remove("is-cur"); flow[2].classList.add("is-done");
      li.setAttribute("data-state", "done");
      st.textContent = a.ok;
      confirmed(a.fx);
    }, reduce ? 700 : 2500);
  }
  function lightTiles(idx) {
    idx.forEach(function (i) { var t = tiles[i]; t.el.classList.add("is-lit"); flashTile(t); });
  }
  function effect(fx) {
    if (fx === "lights") lightTiles([0, 1, 2, 3]);
    if (fx === "dock") lightTiles([2, 3]);
    if (fx === "talk") {
      var t = tiles[2], say = el("div", "sec-say", ICON.talk.replace("<svg", '<svg aria-hidden="true"') +
        "<span>« Bonjour. Cette propriété est sous surveillance. Puis-je vous aider? »</span>");
      t.el.appendChild(say);
      later(function () { if (say.parentNode) say.parentNode.removeChild(say); }, 4700);
    }
  }
  function confirmed(fx) {
    if (fx !== "talk") return;
    var w = run.wmap.c;
    if (!w) return;
    var t = run.t, last = w.keys[w.keys.length - 1];
    w.keys.push([t + 400, last[1], last[2], last[3]], [t + 2000, 1240, 470, 250], [t + 3100, 1190, 300, 150]);
    w.stay = false;
    var leaveAt = t + 3100;
    if (reduce) { run.t = leaveAt + 50; step(run.t); }
    later(function () {
      addFollow(hms(simAt(leaveAt)) + " — la personne quitte la terrasse après le message.");
    }, reduce ? 0 : 3100);
  }

  /* ---------- Horloge simulée ---------- */
  function simAt(t) {
    var sc = run.sc, s0 = secs(sc.start), done = run.T.done;
    return t <= done ? s0 + t / 1000 * sc.rate : s0 + done / 1000 * sc.rate + (t - done) / 1000;
  }
  function clock(t) {
    var s = Math.floor(simAt(t));
    if (s === run.lastS) return;
    run.lastS = s;
    var txt = hms(s);
    if (clockEl) clockEl.textContent = txt;
    tiles.forEach(function (tile) { tile.ts.innerHTML = "<span>" + today + " </span>" + txt; });
  }

  /* ---------- Moteur ---------- */
  var run = null, visible = false, raf = 0, last = 0;

  function step(t) {
    var sc = run.sc, T = run.T;
    sc.walkers.forEach(function (w) { drawWalker(w, t); });
    sc.props.forEach(function (p, i) { drawProp(p, i, t); });
    run.boxes.forEach(function (rb) { drawBox(rb, t); });
    tileStatus();
    while (run.ev < sc.events.length && sc.events[run.ev].t <= t) fire(sc.events[run.ev++]);
    while (run.shot < sc.evidence.length && sc.evidence[run.shot].t <= t) snap(sc.evidence[run.shot++]);
    if (run.phase < 1 && t >= T.link) { run.phase = 1; linkPhase(); }
    if (run.phase < 2 && t >= T.collapse) { run.phase = 2; collapsePhase(); }
    if (run.phase < 3 && t >= T.reveal) { run.phase = 3; revealPhase(); }
    if (run.phase < 4 && t >= T.done) { run.phase = 4; donePhase(); }
    clock(t);
  }
  function loop(now) {
    raf = 0;
    if (!run || !visible) return;
    var dt = last ? Math.min(100, now - last) : 16;
    last = now;
    run.t += dt;
    step(run.t);
    raf = requestAnimationFrame(loop);
  }
  function play() {
    if (raf || !run || !visible || reduce) return;
    last = 0;
    raf = requestAnimationFrame(loop);
  }

  function start(key) {
    clearLater();
    var sc = JSON.parse(JSON.stringify(SC[key]));
    setSite(sc.site, !!run);
    tiles.forEach(function (tile, i) {
      tile.cam = SITES[sc.site].cams[i];
      $$(".sec-subj, .sec-box, .sec-prop, .sec-say, .sec-snap", tile.el).forEach(function (n) { n.parentNode.removeChild(n); });
      tile.el.classList.remove("is-lit", "is-hit", "is-flash");
      tile.k = null;
    });
    if (wires) wires.innerHTML = "";
    tog(wall, "is-ir", sc.mood === "ir");
    tog(wall, "is-dim", sc.mood === "dim");
    setSensors(sc);
    rawList.innerHTML = "";
    empty.hidden = false;
    feed.className = "sec-feed";
    nRaw.textContent = "0";
    live.textContent = "";
    root.classList.remove("is-done");
    btns.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-sec-scen") === key ? "true" : "false");
      b.classList.remove("is-next");
    });
    var end = sc.events[sc.events.length - 1].t;
    run = {
      key: key, sc: sc, t: 0, ev: 0, shot: 0, phase: 0, n: 0, lastS: -1,
      wn: {}, pn: {}, dir: {}, wmap: {},
      boxes: sc.boxes.map(function (b) { return { def: b, node: null, lab: -1 }; }),
      T: { link: end + 700, collapse: end + 2000, reveal: end + 2800, done: end + 4000 }
    };
    sc.walkers.forEach(function (w) { run.wmap[w.id] = w; });
    renderInc(sc);
    phase("En écoute", "idle");
    if (reduce) {
      run.t = run.T.done;
      step(run.t);
      return;
    }
    step(0);
    play();
  }

  /* ---------- Commandes ---------- */
  btns.forEach(function (b) {
    b.addEventListener("click", function () { start(b.getAttribute("data-sec-scen")); });
  });
  if (replay) replay.addEventListener("click", function () { start(run ? run.key : "livraison"); });
  inc.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("button[data-act]");
    if (!b || !run) return;
    var li = b.closest(".sec-act");
    act(li, run.sc.inc.acts[+li.getAttribute("data-i")], b.getAttribute("data-act") === "ok");
  });

  /* Préparée tout de suite (état « En écoute »), lancée à l'entrée dans la
     fenêtre, en pause hors écran. */
  var begun = false;
  start("livraison");
  if ("IntersectionObserver" in window) {
    tog(root, "is-paused", true);
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting && e.intersectionRatio >= .35) begun = true;
        visible = begun && e.isIntersecting;
        tog(root, "is-paused", !visible);
        play();
      });
    }, { threshold: [0, .35, .6] }).observe(root);
  } else {
    visible = begun = true;
    play();
  }
})();
