/* JARVIS — démo « Sécurité intelligente » (solution 03).
   « Six notifications deviennent un seul événement compris. »
   Mur de quatre caméras simulées : des silhouettes passent, des cadres de
   détection les suivent, chaque alerte brute file vers la chronologie, puis
   JARVIS relie les alertes et les fusionne en un seul événement expliqué.
   Les actions sensibles attendent « Approuver », puis : envoyé → confirmé
   (une commande n'est réussie qu'une fois l'état relu).
   Six situations : livraison, visiteur de nuit, entrepôt, lecture de
   plaques (registre des plaques tenu à jour), salle des serveurs (carte
   révoquée, caméras du secteur qui s'éveillent, porte qui reste
   verrouillée) et porte forcée, où JARVIS passe en mode urgence : liseré
   rouge sobre, actions exécutées une à une (envoyé → confirmé, l'appel
   sonne pour vrai avant d'être répondu), levée sur confirmation seulement.
   La chronologie se bascule en vue « Incidents » : les alertes brutes
   regroupées par incident, avec gravité, état et caméras concernées.
   Rendu de vrai flux : grain du capteur, dérive lente, exposition qui
   respire, débit qui monte quand ça bouge, bref artefact au mouvement;
   cadres d'analyse qui suivent avec un léger retard, confiance qui varie,
   numéro de piste commun aux caméras, trace au sol; caméra active mise
   en avant. Les photos elles-mêmes ne sont jamais retouchées par ces effets.
   Tout est simulé. Sans JavaScript, le balisage montre l'état final.
   Mouvement réduit : état final directement, aucune boucle.
   Hors écran : tout se met en pause. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="securite"]');
  if (!root || !window.requestAnimationFrame) return;

  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var wide = window.matchMedia ? matchMedia("(min-width: 881px)") : { matches: true };
  var W = 1672, H = 941; // taille des images de caméra
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
    var m = { access: "alert", door: "alert", alert: "alert", plate: "vehicle", grant: "parcel", lock: "parcel", log: "person", file: "move", siren: "alert", cam: "move" };
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
    cam: '<svg viewBox="0 0 16 16"><rect x="2" y="4.5" width="12" height="8.5" rx="1.5"/><circle cx="8" cy="8.7" r="2.3"/><path d="M5.5 4.5 6.5 3h3l1 1.5"/></svg>',
    plate: '<svg viewBox="0 0 16 16"><rect x="1.5" y="5" width="13" height="6.5" rx="1.2"/><path d="M4 8.2h1.6M7.2 8.2h1.6M10.4 8.2h1.6"/></svg>',
    grant: '<svg viewBox="0 0 16 16"><rect x="2.5" y="4" width="11" height="8" rx="1.5"/><path d="M5 7h3.5M5 9.5h2"/><path d="m9.5 9 1.3 1.3L13 8"/></svg>',
    log: '<svg viewBox="0 0 16 16"><path d="M4 2.5h8v11H4z"/><path d="M6 5.5h4M6 8h4M6 10.5h2.5"/></svg>',
    lock: '<svg viewBox="0 0 16 16"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5.2a2.5 2.5 0 0 1 5 0V7"/></svg>',
    urg: '<svg viewBox="0 0 16 16"><path d="M8 2.2 14 13H2Z"/><path d="M8 6.5v3M8 11.3v.2"/></svg>',
    siren: '<svg viewBox="0 0 16 16"><path d="M4.5 13.5V9a3.5 3.5 0 0 1 7 0v4.5"/><path d="M3 13.5h10M8 2v1.6M3.2 4.2l1.1 1.1M12.8 4.2l-1.1 1.1"/></svg>',
    file: '<svg viewBox="0 0 16 16"><path d="M4 2.5h5.5L12.5 5.5V13.5H4Z"/><path d="M9.5 2.5v3h3"/><path d="M6 8.5h4M6 11h4"/></svg>'
  };

  /* Silhouette simulée, vue de trois quarts tournée vers la droite
     (60 × 170, pieds en bas). Membres du fond plus sombres, membres avant
     dégradés (lumière venue d'en haut). Une seule forme pleine : aucun
     contour interne, le liseré de lumière est posé sur le tout en CSS. */
  var LEG = "M28 86H42.4C43 98 41.6 112 40.2 129C39.8 141 39 152 38.8 160.5L45.2 163.6C47.4 164.6 47.4 167.8 45.2 167.8H32.4C31.4 167.8 31 167 31.1 166L31.8 160.5C31.2 150 30.8 141 30.8 129C29.8 113 28.5 99 28 86Z";
  var TORSO = "M15 40C15.5 34 21 31 29.5 31C38 31 44 33.5 45 39L46 55C46.2 63 44.2 70 43 77L43.6 93H16.6L17.2 77C16.2 70 14.6 62 14.4 55Z";
  var ARM = "M34 35C37.5 33.2 42.6 33.8 43.8 37.8C44.8 46 45 54 44.4 62C44.2 70 43.4 78 42.8 87.5C43 91.6 41.8 95.4 39.6 95.6C37.2 95.8 36.2 93 36.6 88.4C36.8 79 37 70 36.6 62C35.6 54 34.4 46 34 35Z";
  var PERSON =
    '<svg viewBox="0 0 60 170" aria-hidden="true" focusable="false">' +
    '<defs><linearGradient id="sgT@" x1="0" y1="0" x2=".18" y2="1"><stop class="g0" offset="0"/><stop class="g1" offset=".3"/><stop class="g2" offset="1"/></linearGradient>' +
    '<linearGradient id="sgL@" x1="0" y1="0" x2="0" y2="1"><stop class="g3" offset="0"/><stop class="g4" offset=".72"/><stop class="g3" offset="1"/></linearGradient>' +
    '<radialGradient id="sgH@" cx=".7" cy=".42" r=".75"><stop class="g5" offset="0"/><stop class="g6" offset="1"/></radialGradient>' +
    '<linearGradient id="sgS@" x1="0" y1="0" x2="1" y2="0"><stop class="s0" offset="0"/><stop class="s1" offset=".6"/></linearGradient></defs>' +
    '<g class="p-body">' +
    '<g transform="translate(-17 1)"><path class="p-armF" d="' + ARM + '"/></g>' +
    '<g transform="translate(-9 0)"><path class="p-legF" d="' + LEG + '"/></g>' +
    '<path class="p-torso" fill="url(#sgT@)" d="' + TORSO + '"/><path class="p-shade" fill="url(#sgS@)" d="' + TORSO + '"/>' +
    '<path class="p-legN" fill="url(#sgL@)" d="' + LEG + '"/>' +
    '<path class="p-neck" d="M28.6 21H35.6L36.2 33H28Z"/>' +
    '<path class="p-head" fill="url(#sgH@)" d="M24.6 14.2C24.6 7 28.6 3.6 32.8 3.6C37.6 3.6 40.8 7.2 40.8 13.8C40.8 18.8 39.4 22.6 36.4 24.4C34.2 25.6 30.4 25.5 28.2 24C25.9 22.4 24.6 18.6 24.6 14.2Z"/>' +
    '<path class="p-hair" d="M24.3 14.4C23.6 6.4 28 3 32.8 3C37.8 3 41.2 6 41 10.8C37 9.4 31.8 9.8 29 12.2C28 15.6 28 18.8 26.6 20.8C25.2 19 24.4 16.8 24.3 14.4Z"/>' +
    '<path class="p-cap" d="M24.1 12.2C23.9 5.4 28.2 2.6 32.8 2.6C37.8 2.6 41.2 5.4 41.4 10.6L48.4 12.4C49.1 13.3 48.2 14.2 46.6 14L24.4 14Z"/>' +
    '<path class="p-hood" fill="url(#sgT@)" d="M22.2 15.6C21.6 5.6 26.8 1.6 33 1.6C39.6 1.6 43 6.6 42.6 13.8C42.4 19.2 40.8 24 37.6 27.4L29.2 31.4C25.2 28.6 22.6 22.2 22.2 15.6Z"/>' +
    '<path class="p-face" d="M34.8 8.8C38.4 8.9 40.4 11.6 40.4 15.4C40.4 19.6 38.8 22.9 36 24C34.6 21.2 34.2 13.6 34.8 8.8Z"/>' +
    '<g class="p-box"><path class="bx-f" d="M36 46H62V69H36Z"/><path class="bx-t" d="M36 46 40 42H66L62 46Z"/><path class="bx-s" d="M62 46 66 42V65L62 69Z"/><path class="bx-tape" d="M49 46V69M47 46 51 42"/></g>' +
    '<path class="p-armN" fill="url(#sgT@)" d="' + ARM + '"/>' +
    '<path class="p-armC" fill="url(#sgT@)" d="M34.5 36C38 33.6 42.8 34 44 38C44.8 46 45 54 44.6 60L55.6 62.2C58.4 62.8 58.6 67.4 55.8 67.8L42.2 68.2C38.8 68.2 37.4 65.6 37.2 61.6C36.8 53 35 45 34.5 36Z"/>' +
    "</g></svg>";
  /* Colis au sol : trois faces ombrées, ruban, étiquette, ombre de contact. */
  /* Couloir éclairé vu par la porte de service ouverte (perspective simple :
     plafond et plafonnier, murs, sol, mur du fond). */
  var CORRIDOR =
    '<svg viewBox="0 0 100 180" preserveAspectRatio="none" aria-hidden="true" focusable="false">' +
    '<defs><linearGradient id="cf@" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#4e3e2e"/><stop offset="1" stop-color="#8a7356"/></linearGradient>' +
    '<linearGradient id="cw@" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a8263"/><stop offset="1" stop-color="#bba27e"/></linearGradient>' +
    '<radialGradient id="cl@" cx=".58" cy=".08" r=".5"><stop offset="0" stop-color="#fff2d6" stop-opacity=".75"/><stop offset="1" stop-color="#fff2d6" stop-opacity="0"/></radialGradient>' +
    '<linearGradient id="cv@" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset=".3" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient></defs>' +
    '<path d="M0 0H100V180H0Z" fill="#a78e6b"/>' +
    '<path d="M0 0 38 46V116L0 180Z" fill="url(#cw@)"/>' +
    '<path d="M100 0 74 46V116L100 180Z" fill="#927a5a"/>' +
    '<path d="M0 0H100L74 46H38Z" fill="#a48b67"/>' +
    '<path d="M38 46H74V116H38Z" fill="#c4ab86"/>' +
    '<path d="M0 180 38 116H74L100 180Z" fill="url(#cf@)"/>' +
    '<path d="M0 0H100V90H0Z" fill="url(#cl@)"/><path d="M0 0H100V180H0Z" fill="url(#cv@)"/></svg>';
  var PARCEL =
    '<svg viewBox="0 0 64 46" aria-hidden="true" focusable="false">' +
    '<defs><linearGradient id="pk@" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a7346"/><stop offset="1" stop-color="#6a4d2c"/></linearGradient></defs>' +
    '<ellipse cx="33" cy="43" rx="31" ry="3.4" fill="#000" opacity=".55"/>' +
    '<path d="M5 18H39V43H5Z" fill="url(#pk@)"/><path d="M39 18 58 9V34L39 43Z" fill="#553d23"/>' +
    '<path d="M5 18 24 9H58L39 18Z" fill="#c09663"/>' +
    '<path d="M14.5 18 33.5 9M22 18V43" stroke="#d9c49c" stroke-opacity=".3" stroke-width="2.2" fill="none"/>' +
    '<path d="M27 25H35V31H27Z" fill="#c8bca6" opacity=".4"/></svg>';
  /* Voiture vue de dos (220 × 140, roues en bas) : carrosserie sombre en
     dégradé, lunette, feux arrière, pare-chocs et plaque lisible (le texte
     est posé par makeSubj). Même famille de rendu que les silhouettes. */
  var CAR =
    '<svg viewBox="0 0 220 140" aria-hidden="true" focusable="false">' +
    '<defs><linearGradient id="cb@" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3d44"/><stop offset=".45" stop-color="#1b1d22"/><stop offset="1" stop-color="#101114"/></linearGradient>' +
    '<linearGradient id="cg@" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3640"/><stop offset="1" stop-color="#11151a"/></linearGradient>' +
    '<linearGradient id="ct@" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a74"/><stop offset=".55" stop-color="#e03a2c"/><stop offset="1" stop-color="#8a1f17"/></linearGradient></defs>' +
    '<path class="c-tire" d="M32 116h32v14a5 5 0 0 1-5 5H37a5 5 0 0 1-5-5Z"/>' +
    '<path class="c-tire" d="M156 116h32v14a5 5 0 0 1-5 5h-22a5 5 0 0 1-5-5Z"/>' +
    '<path fill="url(#cg@)" d="M56 10q4-8 14-8h80q10 0 14 8l16 38H40Z"/>' +
    '<path class="c-glass" d="M66 12h88l13 33H53Z"/>' +
    '<path fill="url(#cb@)" d="M38 44q-16 3-20 18-3 26 0 48 1 12 14 12h156q13 0 14-12 3-22 0-48-4-15-20-18Z"/>' +
    '<path class="c-sh" d="M18 70q92 10 184 0v8q-92 9-184 0Z"/>' +
    '<path fill="url(#ct@)" d="M22 58h54q4 0 4 5v6q0 5-4 5H26q-5 0-5-6Z"/>' +
    '<path fill="url(#ct@)" d="M198 58h-54q-4 0-4 5v6q0 5 4 5h52q5 0 5-6Z"/>' +
    '<path class="c-bmp" d="M18 92h184v14q0 8-9 8H27q-9 0-9-8Z"/>' +
    '<rect class="c-plt" x="82" y="97" width="56" height="20" rx="2.5"/>' +
    '<rect class="c-pltl" x="83.2" y="98.2" width="53.6" height="17.6" rx="1.8"/>' +
    '<text class="c-txt" x="110" y="112.5" text-anchor="middle">———</text></svg>';
  /* Salle des serveurs, image de synthèse « caméra intérieure » (1672 × 941,
     mêmes coordonnées que les photos) : rangée de baies à gauche, porte de
     la salle et lecteur de badge à droite, plafonnier, sol réfléchissant.
     Rendu volontairement sobre : la tuile ajoute grain, vignette et IR. */
  function rackArt(x, y2, w, h, leds) {
    var x2 = x + w, y1 = y2 - h, s = "";
    s += '<path fill="#23272e" stroke="#5a626d" stroke-width="2.5" d="M' + x + " " + y1 + "H" + x2 + "V" + y2 + "H" + x + 'Z"/>';
    for (var i = 1; i < 7; i++) {
      var yy = y1 + h * i / 7;
      s += '<path stroke="#39404b" stroke-width="3" d="M' + (x + w * .06) + " " + yy + "H" + (x2 - w * .2) + '"/>';
    }
    for (var j = 0; j < leds; j++) {
      var ly = y1 + h * (.1 + .8 * j / (leds - 1)), c = j % 3 === 1 ? "#d9dbde" : "#f2f3f5";
      s += '<circle cx="' + (x2 - w * .1) + '" cy="' + ly + '" r="' + (w > 240 ? 4.5 : 3) + '" fill="' + c + '" opacity="' + (j % 2 ? ".95" : ".55") + '"/>';
    }
    return s;
  }
  var SRV =
    '<svg viewBox="0 0 1672 941" preserveAspectRatio="none" aria-hidden="true" focusable="false">' +
    '<defs><linearGradient id="sw@" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6d737c"/><stop offset="1" stop-color="#3c4148"/></linearGradient>' +
    '<linearGradient id="sf@" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4f58"/><stop offset="1" stop-color="#23262b"/></linearGradient>' +
    '<radialGradient id="sl@" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f2f4f6" stop-opacity=".55"/><stop offset="1" stop-color="#f2f4f6" stop-opacity="0"/></radialGradient>' +
    '<radialGradient id="sv@" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></radialGradient></defs>' +
    '<rect width="1672" height="941" fill="url(#sw@)"/>' +
    '<path d="M0 0h1672v150L0 225Z" fill="#30343b"/>' +
    '<ellipse cx="820" cy="140" rx="640" ry="100" fill="url(#sl@)"/>' +
    '<rect x="300" y="96" width="980" height="16" rx="8" fill="#eceef1" opacity=".9" transform="rotate(-2 790 104)"/>' +
    '<path d="M0 941V860l900-140 772 40v181Z" fill="url(#sf@)"/>' +
    '<path d="M240 880 350 760h26L276 884Z" fill="#fff" opacity=".09"/>' +
    '<path d="M700 820 800 735h20l-96 90Z" fill="#fff" opacity=".08"/>' +
    '<path d="M1200 790h260v10h-260Z" fill="#fff" opacity=".07"/>' +
    rackArt(0, 860, 300, 770, 9) + rackArt(330, 800, 230, 640, 8) +
    rackArt(585, 755, 175, 540, 7) + rackArt(783, 722, 118, 465, 6) +
    '<rect x="1148" y="228" width="276" height="514" fill="none" stroke="#6d747e" stroke-width="10"/>' +
    '<rect x="1158" y="238" width="256" height="494" fill="#43484f"/>' +
    '<path d="M1158 238h256v12l-256 16Z" fill="#fff" opacity=".1"/>' +
    '<rect x="1176" y="300" width="90" height="150" fill="#272b31" stroke="#5a626d" stroke-width="3"/>' +
    '<rect x="1384" y="470" width="12" height="42" rx="5" fill="#8a919b"/>' +
    '<rect x="1178" y="170" width="216" height="40" rx="4" fill="#5a626d"/>' +
    '<text x="1286" y="197" text-anchor="middle" font-size="22" letter-spacing="5" fill="#dde1e7" font-family="inherit">SALLE DES SERVEURS</text>' +
    '<rect x="1452" y="428" width="44" height="72" rx="6" fill="#2a2e35" stroke="#767d88" stroke-width="2.5"/>' +
    '<circle cx="1474" cy="450" r="6" fill="#e8eaec" opacity=".95"/>' +
    '<rect x="1462" y="466" width="24" height="22" rx="3" fill="#3c4148"/>' +
    '<rect width="1672" height="941" fill="url(#sv@)"/></svg>';

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
  /* Scènes de synthèse (pas de photo) : la salle des serveurs. */
  var ART = { srv: SRV };
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
    },
    stationnement: {
      label: "Entreprise · stationnement",
      cams: [
        { img: "parking", name: "Voie d’entrée · lecteur", view: [90, 250, 800, 600], alt: "Caméra de la voie d’entrée du stationnement : barrière, lecteur de plaques et berline garée" },
        { img: "parking", name: "Stationnement", view: v43(100), alt: "Caméra du stationnement de l’entreprise, avec un véhicule garé" },
        { img: "parking", name: "Entrée principale", view: [900, 170, 740, 555], alt: "Vue rapprochée de l’entrée principale de l’entreprise" },
        { img: "quai", name: "Quai de livraison", view: v43(330), alt: "Caméra du quai de livraison, avec le camion de l’entreprise" }
      ],
      sensors: [
        { id: "barriere", name: "Barrière · entrée", idle: "Fermée" },
        { id: "lpr", name: "Lecteur de plaques", idle: "En lecture" },
        { id: "bell", name: "Interphone", idle: "Au repos" },
        { id: "alarm", name: "Alarme", idle: "Désarmée" }
      ]
    },
    serveurs: {
      label: "Entreprise · intérieur",
      cams: [
        { img: "parking", name: "Stationnement", view: v43(60), alt: "Caméra du stationnement de l’entreprise, le soir" },
        { img: "quai", name: "Entrée du personnel", view: [1230, 205, 442, 331.5], sleep: true, alt: "Vue rapprochée de l’entrée du personnel, porte vitrée éclairée" },
        { img: "srv", name: "Corridor des serveurs", view: v43(300), ir: true, sleep: true, irlab: "intérieur", alt: "Caméra intérieure infrarouge : corridor des baies, porte de la salle des serveurs et lecteur de badge" },
        { img: "quai", name: "Quai de livraison", view: v43(330), alt: "Caméra du quai de livraison, la nuit" }
      ],
      sensors: [
        { id: "badge", name: "Lecteur · serveurs", idle: "Prêt" },
        { id: "door", name: "Porte des serveurs", idle: "Verrouillée" },
        { id: "motion", name: "Détecteur · corridor", idle: "Calme" },
        { id: "alarm", name: "Alarme", idle: "Armée · partielle" }
      ]
    }
  };

  /* ---------- Situations simulées ----------
     Temps en millisecondes réelles depuis le début. Positions en pixels de
     l'image d'origine (1672 × 941) : [t, x des pieds, y des pieds, hauteur].
     tid : numéro de piste de l'analyse vidéo; il reste le même d'une caméra à
     l'autre quand JARVIS reconnaît la même personne. */
  var P = "Personne · ", PC = NBSP + "%";
  var SC = {
    livraison: {
      site: "maison", start: "21:41:58", rate: 5, mood: "", alarm: "Désarmée",
      walkers: [
        { id: "a", tid: "14", img: "allee", kind: "livreur", carry: true, keys: [[600, 150, 790, 360], [3400, 760, 640, 275], [5000, 1380, 525, 195]] },
        { id: "b", tid: "14", img: "entree", kind: "livreur", carry: [0, 8150], keys: [[4800, 1000, 1010, 560], [6300, 640, 830, 430], [7400, 430, 610, 325], [8000, 255, 508, 288], [8800, 255, 508, 288], [9600, 430, 610, 325], [10300, 760, 860, 450], [10900, 1000, 1010, 560]] },
        { id: "c", tid: "14", img: "allee", kind: "livreur", keys: [[10300, 1380, 525, 195], [12400, 700, 650, 280], [13900, 150, 790, 360]] }
      ],
      props: [
        { img: "entree", kind: "ring", at: 7900, dur: 1700, x: 378, y: 318 },
        { img: "entree", kind: "parcel", at: 8150, x: 350, y: 516 }
      ],
      boxes: [
        { tile: 1, track: "a", from: 900, to: 4900, labels: [[900, "Mouvement", "move"], [1900, P + "94" + PC, "person"]] },
        { tile: 0, track: "b", from: 5300, to: 10700, labels: [[5300, P + "96" + PC, "person"]] },
        { tile: 0, rect: [310, 463, 82, 60], from: 8500, labels: [[8500, "Colis · 91" + PC, "parcel"]] },
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
        { id: "a", tid: "31", img: "allee", kind: "hood", keys: [[400, 150, 800, 370], [2200, 640, 685, 300], [2900, 640, 685, 300], [4300, 1380, 525, 195]] },
        { id: "b", tid: "31", img: "entree", kind: "hood", keys: [[4100, 1000, 1010, 560], [5400, 640, 830, 430], [6300, 470, 640, 335], [8800, 470, 640, 335], [9600, 760, 860, 450], [10300, 1050, 1010, 560]] },
        { id: "c", tid: "31", img: "terrasse", kind: "hood", stay: true, keys: [[9900, 1190, 300, 150], [11300, 1240, 470, 250], [12000, 1255, 590, 305]] }
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
        { id: "a", tid: "07", img: "parking", kind: "dark", keys: [[1900, 690, 650, 215], [3600, 960, 565, 170], [4800, 1190, 470, 122]] },
        { id: "b", tid: "07", img: "quai", kind: "dark", keys: [[4600, 300, 665, 215], [6200, 1000, 700, 235], [7200, 1430, 565, 205], [7700, 1505, 530, 196], [9500, 1505, 530, 196], [10300, 1522, 512, 176]] }
      ],
      props: [
        { img: "parking", kind: "tail", at: 0, until: 2000, x: 238, y: 576 },
        { img: "quai", kind: "door", at: 8600, rect: [1442, 266, 142, 254] }
      ],
      boxes: [
        { tile: 0, tid: "06", rect: [150, 440, 532, 222], from: 600, labels: [[600, "Véhicule · 96" + PC, "vehicle"]] },
        { tile: 0, track: "a", from: 2200, to: 4700, labels: [[2200, P + "92" + PC, "person"]] },
        { tile: 2, rect: [705, 345, 480, 275], from: 300, labels: [[300, "Camion connu · ignoré", "known"]] },
        { tile: 2, track: "b", from: 5000, to: 10100, labels: [[5000, P + "95" + PC, "person"]] },
        { tile: 3, track: "b", from: 6800, to: 10100, labels: [[6800, P + "97" + PC, "person"], [8000, "Aucun badge", "alert"]] }
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
          { fx: "call", ico: "call", label: "Prévenir le responsable de garde", sent: "Message envoyé au responsable de garde", ok: "Confirmé · accusé de réception reçu.", relay: true }
        ]
      }
    },

    /* Lecture de plaques : deux véhicules à la barrière. Le premier est au
       registre (barrière ouverte), le second est consigné comme visiteur
       (photo + plaque), avec notification de courtoisie. Noms et plaques
       fictifs. */
    plaques: {
      site: "stationnement", start: "17:05:46", rate: 8, mood: "", alarm: "Désarmée",
      walkers: [
        { id: "v1", tid: "52", img: "parking", kind: "car", plate: "XKE 204", keys: [[800, 680, 935, 300], [3400, 586, 730, 215], [7600, 586, 730, 215], [9400, 470, 415, 100]] },
        { id: "v2", tid: "53", img: "parking", kind: "car", plate: "H2B 519", keys: [[10600, 685, 940, 300], [13200, 590, 734, 217], [18800, 590, 734, 217], [20400, 474, 418, 100]] }
      ],
      props: [
        { img: "parking", kind: "chip", tile: 0, at: 5600, until: 9000, x: 490, y: 332, tone: "ok", html: "<b>XKE 204 · Québec</b><small>Autorisée · N. Tremblay, employée</small>" },
        { img: "parking", kind: "chip", tile: 0, at: 15400, until: 20200, x: 490, y: 332, tone: "warn", html: "<b>H2B 519 · inconnue</b><small>Consignée · visiteur</small>" }
      ],
      boxes: [
        { tile: 0, track: "v1", shape: "car", from: 1100, to: 9200, labels: [[1100, "Véhicule · 97" + PC, "vehicle"]] },
        { tile: 0, rect: [543, 664, 86, 31], under: true, from: 3900, to: 7400, labels: [[3900, "Plaque · lecture…", "move"], [4700, "XKE 204 · Québec", "plate"]] },
        { tile: 0, track: "v2", shape: "car", from: 10900, to: 20200, labels: [[10900, "Véhicule · 96" + PC, "vehicle"]] },
        { tile: 0, rect: [546, 667, 87, 31], under: true, from: 13700, to: 18500, labels: [[13700, "Plaque · lecture…", "move"], [14500, "H2B 519 · inconnue", "person"]] }
      ],
      events: [
        { t: 1100, k: "vehicle", title: "Véhicule — voie d’entrée", src: "Caméra 01 · 97" + PC, tile: 0 },
        { t: 4700, k: "plate", title: "Plaque lue — XKE 204 · Québec", src: "Lecteur de plaques · voie d’entrée", sensor: "lpr", state: "XKE 204", tile: 0, reg: ["XKE 204", "Autorisée · N. Tremblay", "ok"] },
        { t: 5800, k: "grant", title: "Véhicule autorisé — N. Tremblay, employée", src: "Registre des plaques · entrée permise", sensor: "barriere", state: "Ouverte", reset: 3600, tile: 0 },
        { t: 10900, k: "vehicle", title: "Véhicule — voie d’entrée", src: "Caméra 01 · 96" + PC, tile: 0 },
        { t: 14500, k: "plate", title: "Plaque lue — H2B 519 · inconnue", src: "Lecteur de plaques · aucun dossier", sensor: "lpr", state: "H2B 519", tile: 0 },
        { t: 15600, k: "log", title: "Consignée comme visiteur — photo et plaque au registre", src: "Registre des plaques", sensor: "barriere", state: "Ouverte · visiteur", tile: 0, reg: ["H2B 519", "Visiteur consigné", "warn"] },
        { t: 16900, k: "bell", title: "Notification de courtoisie — sans urgence", src: "Vers votre téléphone", tile: 0 }
      ],
      evidence: [
        { tile: 0, t: 6900, c: [586, 660], w: 620, cap: "XKE 204" },
        { tile: 1, t: 12800, c: [620, 700], w: 900, cap: "Stationnement" },
        { tile: 0, t: 16300, c: [590, 664], w: 620, cap: "H2B 519" }
      ],
      reg: [["16 h 48", "GVR 882", "Autorisée · T. Côté", "ok"], ["16 h 31", "FLM 310", "Visiteur consigné", "warn"], ["16 h 02", "JPS 668", "Autorisée · M. Gagnon", "ok"]],
      inc: {
        lvl: "ok", lvlTxt: "Normal",
        sum: "<b>17" + NBSP + "h" + NBSP + "06 — Entrée du stationnement :</b> XKE 204 (N. Tremblay, employée) reconnue au registre, barrière ouverte. H2B 519, inconnue, consignée comme visiteur : photo et plaque conservées, notification de courtoisie envoyée.",
        why: "2 plaques lues · registre tenu à jour · barrière commandée 2 fois",
        calm: "Aucune action requise. La lecture du visiteur reste au registre 30 jours.",
        acts: []
      }
    },

    /* Salle des serveurs : carte révoquée présentée deux fois. Les caméras
       du secteur s'éveillent, la personne est suivie (même ID), la porte
       reste verrouillée, le gestionnaire reçoit la photo. */
    serveurs: {
      site: "serveurs", start: "22:47:46", rate: 8, mood: "dim", alarm: "Armée · partielle",
      walkers: [
        { id: "a", tid: "23", img: "parking", kind: "dark", keys: [[600, 660, 650, 235], [2600, 1050, 590, 205], [4200, 1330, 470, 160]] },
        { id: "b", tid: "23", img: "quai", kind: "dark", keys: [[4800, 1270, 545, 230], [6000, 1420, 515, 200], [7400, 1452, 505, 192]] },
        { id: "c", tid: "23", img: "srv", kind: "dark", stay: true, keys: [[8200, 260, 905, 430], [10200, 720, 770, 330], [11600, 1120, 700, 290]] }
      ],
      props: [],
      boxes: [
        { tile: 0, track: "a", from: 900, to: 4100, labels: [[900, "Mouvement", "move"], [1700, P + "91" + PC, "person"]] },
        { tile: 1, track: "b", from: 5000, to: 7300, labels: [[5000, P + "95" + PC, "person"]] },
        { tile: 2, track: "c", from: 8400, labels: [[8400, P + "96" + PC, "person"], [12400, "Refus · essai 1", "alert"], [16400, "Refus · essai 2", "alert"]] }
      ],
      events: [
        { t: 900, k: "move", title: "Mouvement — stationnement", src: "Caméra 01 · Stationnement", tile: 0 },
        { t: 1800, k: "person", title: "Personne — stationnement", src: "Caméra 01 · 91" + PC, tile: 0 },
        { t: 5200, k: "person", title: "Personne — entrée du personnel", src: "Caméra 02 · 95" + PC, tile: 1, wake: [1] },
        { t: 12000, k: "access", title: "ID refusé — carte révoquée", src: "Lecteur · salle des serveurs", sensor: "badge", state: "Refusé · révoquée", tile: 2, wake: [2] },
        { t: 13600, k: "cam", title: "Caméras du secteur réveillées", src: "Enregistrement continu · ID 23 suivie", tile: 2 },
        { t: 16400, k: "alert", title: "2e essai — ID refusé", src: "Lecteur · salle des serveurs", sensor: "badge", state: "Refusé · 2e essai", tile: 2 },
        { t: 17800, k: "bell", title: "Gestionnaire prévenu — photo jointe", src: "Notification · M. Bélanger", tile: 2, relay: true },
        { t: 18800, k: "lock", title: "La porte des serveurs reste verrouillée", src: "Aucune ouverture · accès refusé consigné", sensor: "door", state: "Verrouillée · maintenue" }
      ],
      evidence: [
        { tile: 0, t: 2600, c: [900, 560], w: 800, cap: "Stationnement" },
        { tile: 2, t: 12600, c: [1250, 560], w: 760, cap: "Essai 1" },
        { tile: 2, t: 16800, c: [1250, 560], w: 560, cap: "Essai 2 · refusé" }
      ],
      inc: {
        lvl: "crit", lvlTxt: "Prioritaire",
        sum: "<b>22" + NBSP + "h" + NBSP + "48 — Salle des serveurs :</b> une carte révoquée a été présentée deux fois au lecteur. La porte est restée verrouillée, la personne (ID 23) est suivie depuis le stationnement et le gestionnaire a reçu la photo.",
        why: "même personne sur 3 caméras · 2 refus de badge · porte verrouillée",
        acts: [
          { fx: "srv", ico: "lock", label: "Verrouiller tout l’étage technique", sent: "Commande envoyée aux 4 portes de l’étage", ok: "Confirmé · état relu : 4 portes sur 4 verrouillées." },
          { fx: "none", ico: "call", label: "Appeler le gestionnaire de garde", sent: "Appel lancé vers M. Bélanger", ok: "Confirmé · appel répondu, caméras partagées.", relay: true }
        ]
      }
    },

    /* Porte forcée, la nuit : escalade automatique en mode urgence. Les six
       actions s'exécutent une à une (envoyé → confirmé), l'appel sonne pour
       vrai, et la levée du mode demande une confirmation. */
    forcee: {
      site: "entrepot", start: "03:25:48", rate: 6, mood: "ir", alarm: "Armée",
      walkers: [
        { id: "a", tid: "41", img: "quai", kind: "hood", keys: [[500, 250, 690, 230], [2400, 1010, 700, 235], [3400, 1430, 565, 205], [3900, 1505, 530, 196], [5600, 1505, 530, 196], [6300, 1522, 512, 180]] }
      ],
      props: [
        { img: "quai", kind: "door", at: 5200, rect: [1442, 266, 142, 254] }
      ],
      boxes: [
        { tile: 2, track: "a", from: 900, to: 6200, labels: [[900, "Mouvement", "move"], [1700, P + "88" + PC, "person"], [4300, "Personne inconnue", "alert"]] },
        { tile: 3, track: "a", from: 3600, to: 6200, labels: [[3600, P + "96" + PC, "person"], [4400, "Personne inconnue", "alert"]] },
        { tile: 3, rect: [1442, 266, 142, 254], from: 5400, labels: [[5400, "Porte forcée", "urg"]] }
      ],
      events: [
        { t: 1000, k: "move", title: "Mouvement — quai", src: "Caméra 03 · Quai de livraison", tile: 2 },
        { t: 1900, k: "person", title: "Personne — quai de livraison", src: "Caméra 03 · 88" + PC, tile: 2 },
        { t: 4400, k: "alert", title: "Personne inconnue — porte de service", src: "Caméra 04 · aucun badge présenté", tile: 3 },
        { t: 5400, k: "urg", title: "Porte forcée — porte de service", src: "Capteur de choc · pêne forcé", sensor: "door", state: "Forcée", tile: 3 },
        { t: 6600, k: "move", title: "Mouvement — entrepôt · zone armée", src: "Détecteur intérieur", sensor: "motion", state: "Mouvement" },
        { t: 7400, k: "urg", title: "Intrusion confirmée — mode urgence", src: "JARVIS · escalade automatique", sensor: "alarm", state: "Intrusion", urgence: true }
      ],
      evidence: [
        { tile: 2, t: 2600, c: [1000, 560], w: 900, cap: "Quai" },
        { tile: 3, t: 4600, c: [1500, 440], w: 480, cap: "Porte de service" },
        { tile: 3, t: 5900, c: [1500, 420], w: 420, cap: "Porte forcée" }
      ],
      inc: {
        lvl: "urg", lvlTxt: "Urgence",
        sum: "<b>3" + NBSP + "h" + NBSP + "26 — Intrusion :</b> la porte de service a été forcée pendant la nuit et une personne inconnue est entrée dans l’entrepôt. Zone armée, personne attendue : aucune. JARVIS passe en mode urgence.",
        why: "porte forcée · personne inconnue · détecteur intérieur · zone armée",
        acts: [],
        phone: "appel au responsable, dossier envoyé · mode urgence.",
        urg: {
          acts: [
            { ico: "cam", label: "Caméras du secteur en direct", ok: "Confirmé · 4 caméras en direct, enregistrement continu", ms: 1100 },
            { ico: "lights", label: "Éclairage extérieur à 100" + NBSP + "%", ok: "Confirmé · état relu : 12 projecteurs allumés", ms: 1700, fx: "lights" },
            { ico: "lock", label: "Verrouillage des zones sensibles", ok: "Confirmé · 3 zones verrouillées : bureaux, stock, serveurs", ms: 1500 },
            { ico: "siren", label: "Sirène intérieure armée", ok: "Confirmée · déclenchement au prochain mouvement", ms: 1000 },
            { ico: "call", label: "Appel au responsable de garde", call: true, ok: "Répondu à 0:07 · A. Roy en ligne", ms: 7000 },
            { ico: "file", label: "Envoi du dossier — extraits et plan", ok: "Envoyé · reçu par A. Roy", ms: 1900 }
          ],
          end: "Incident consigné · 6 actions confirmées · relayé à A." + NBSP + "Roy"
        }
      }
    }
  };
  var ORDER = ["livraison", "visiteur", "entrepot", "plaques", "serveurs", "forcee"];

  /* Incidents déjà au dossier (fictifs) pour la vue « Incidents ». */
  var HIST = [
    { sev: "crit", when: "Hier · 23 h 07", title: "Entrée après la fermeture — quai", st: "relaye", cams: "CAM 03 · CAM 04", n: 6 },
    { sev: "warn", when: "Hier · 17 h 32", title: "Plaque inconnue récurrente — 3 lectures en 7 jours", st: "consigne", cams: "CAM 01", n: 3 },
    { sev: "crit", when: "Lundi · 22 h 48", title: "Accès refusé répété — salle des serveurs", st: "relaye", cams: "CAM 02 · CAM 03", n: 5 },
    { sev: "ok", when: "Lundi · 10 h 15", title: "Livraison — quai", st: "consigne", cams: "CAM 03", n: 4 }
  ];

  /* ---------- Éléments ---------- */
  var body = $(".demo-body"), wall = $("[data-sec-wall]"), sensorsUl = $("[data-sec-sensors]");
  var feed = $(".sec-feed"), rawList = $("[data-sec-raw]"), empty = $("[data-sec-empty]");
  var inc = $("[data-sec-inc]"), lvl = $("[data-sec-lvl]"), when = $("[data-sec-when]"), sum = $("[data-sec-sum]");
  var why = $("[data-sec-why]"), evBox = $("[data-sec-ev]"), actsWrap = $("[data-sec-acts]"), actList = $("[data-sec-actlist]");
  var calm = $("[data-sec-calm]"), follow = $("[data-sec-follow]"), phaseEl = $("[data-sec-phase]"), nRaw = $("[data-sec-n]"), live = $("[data-sec-live]");
  var clockEl = $("[data-sec-clock]"), siteEl = $("[data-sec-site]"), wires = $("[data-sec-wires]");
  var btns = $$("[data-sec-scen]"), replay = $("[data-sec-replay]");
  var regBox = $("[data-sec-reg]"), regList = $("[data-sec-reglist]");
  var urgBox = $("[data-sec-urg]"), urgList = $("[data-sec-urglist]"), urgEnd = $("[data-sec-urgend]"), urgLift = $("[data-sec-urglift]");
  var lensT = $("[data-sec-lenst]"), lensBtns = $$("[data-sec-lens]"), lensView = $("[data-sec-lensv]");
  var arrowK = $(".sec-arrow small"), phoneB = $(".sec-phone b");
  if (!wall || !feed || !inc || !calm) return;

  var curSite = "maison";
  var tiles = $$(".sec-cam", wall).map(function (fig, i) {
    var br = $("[data-sec-br]", fig);
    return {
      el: fig, view: $(".sec-view", fig), stage: $(".sec-stage", fig), ts: $("[data-sec-ts]", fig),
      st: $("[data-sec-st]", fig), name: $(".sec-name", fig), br: br, cam: SITES.maison.cams[i], k: null,
      busy: false, brV: br ? parseFloat(br.textContent.replace(",", ".")) : 2, h: 0
    };
  });
  /* Hauteur des tuiles, relue seulement quand la fenêtre change de taille */
  function measure() { tiles.forEach(function (t) { t.h = t.el.offsetHeight; }); }
  measure();
  window.addEventListener("resize", measure, { passive: true });
  var today = (function () { var d = new Date(); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); })();

  root.classList.add("is-live");
  if (lensT) lensT.hidden = false;

  /* Minuteries annulables (une nouvelle situation efface les précédentes) */
  var timers = [];
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function clearLater() { timers.forEach(clearTimeout); timers = []; }

  /* ---------- Scènes ---------- */
  function buildStage(img, view, alt) {
    var s = el("div", "sec-stage");
    s.setAttribute("style", stageCss(view));
    if (ART[img]) {
      s.insertAdjacentHTML("afterbegin", ART[img].replace(/@/g, ++uid));
      var sv = s.firstChild;
      sv.setAttribute("class", "sec-scene");
      if (alt) { sv.setAttribute("role", "img"); sv.setAttribute("aria-label", alt); sv.removeAttribute("aria-hidden"); }
      return s;
    }
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
      /* Caméra intérieure IR et caméra en veille, propres à chaque tuile */
      tog(t.el, "is-irc", !!cam.ir);
      var ir = $(".sec-ir", t.el);
      if (ir) ir.innerHTML = "IR<span> · " + (cam.irlab || "nuit") + "</span>";
      if (animate && !reduce) {
        ns.classList.add("is-enter");
        old.parentNode.insertBefore(ns, old.nextSibling);
        var im = ns.querySelector("img");
        var go = function () {
          requestAnimationFrame(function () {
            ns.classList.remove("is-enter");
            old.classList.add("is-leave");
            glitch(t, i * 90); // le nouveau flux « s'accroche » : bref artefact
            setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, 800);
          });
        };
        if (!im) requestAnimationFrame(go);
        else if (im.decode) im.decode().then(go, go); else im.onload = go;
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
  function sensorReset(id) {
    var li = sensorEl(id);
    if (!li || !run) return;
    var def = SITES[run.sc.site].sensors.filter(function (s) { return s.id === id; })[0];
    li.querySelector("b").textContent = def ? (def.id === "alarm" ? run.sc.alarm : def.idle) : "";
    li.classList.remove("is-set", "is-hit");
  }
  function sensorHit(id, state, k) {
    var li = sensorEl(id);
    if (!li) return;
    li.style.setProperty("--c", cvar(k));
    li.querySelector("b").textContent = state;
    li.classList.add("is-set");
    li.classList.remove("is-hit"); void li.offsetWidth; li.classList.add("is-hit");
    if (id === "bell") later(function () { sensorReset(id); }, 3400);
  }
  /* Une caméra en veille s'éveille : le flux s'accroche, REC remplace VEILLE */
  function wake(i) {
    var tile = tiles[i];
    if (!tile.el.classList.contains("is-sleep")) return;
    tile.el.classList.remove("is-sleep");
    glitch(tile);
    flashTile(tile, true);
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
  function makeSubj(w) {
    uid++;
    if (w.kind === "car") {
      var n = el("div", "sec-subj k-car", CAR.replace(/@/g, uid));
      n.querySelector(".c-txt").textContent = w.plate || "";
      return n;
    }
    return el("div", "sec-subj k-" + w.kind, PERSON.replace(/@/g, uid));
  }
  function placeSubj(n, p, w, t) {
    var s = n.style;
    s.setProperty("--x", pct(p.x, W));
    s.setProperty("--y", pct(p.y, H));
    s.setProperty("--h", pct(p.h, H)); // vraie hauteur (pas d'agrandissement flou d'une image)
    s.opacity = p.o.toFixed(3);
    if (w.kind === "car") return; // une voiture ne marche pas et ne se retourne pas
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
    var art = p.kind === "parcel" ? PARCEL : p.kind === "door" ? CORRIDOR : null;
    var n = el("div", "sec-prop p-" + p.kind, art && art.replace(/@/g, ++uid));
    if (p.kind === "chip") {
      n.innerHTML = p.html;
      n.classList.add("is-" + (p.tone || "ok"));
    }
    var r = p.rect || (p.kind === "parcel" ? [p.x - 32, p.y - 45, 64, 46] : [p.x, p.y, 0, 0]);
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
      tiles.forEach(function (tile, ti) {
        if (tile.cam.img !== p.img || (p.tile != null && p.tile !== ti)) return;
        var n = makeProp(p);
        tile.stage.appendChild(n);
        rec.push(n);
      });
    } else if (!on && rec && rec.length) {
      rec.forEach(kill); // s'éteint en douceur (feux arrière, sonnette)
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
    if (b.shape === "car") {
      var cw = p.h * 1.5;
      return [p.x - cw / 2, p.y - p.h * 1.02, cw, p.h * 1.05];
    }
    return [p.x - p.h * .2, p.y - p.h * 1.03, p.h * .4, p.h * 1.06];
  }
  function makeBox() {
    return el("div", "sec-box", '<i></i><i></i><i></i><i></i><b><span class="lb-k"></span><span class="lb-c"></span><span class="lb-id"></span></b>');
  }
  /* Étiquette « Personne · 94 % » → classe, confiance, numéro de piste.
     Rend la confiance nominale (0 si l'étiquette n'en a pas). */
  function setLabel(n, L, tid) {
    var m = /^(.*) · (\d+)\s%$/.exec(L[1]), q = n.querySelectorAll("b > span");
    q[0].textContent = m ? m[1] : L[1];
    q[1].textContent = m ? m[2] + PC : "";
    q[2].textContent = tid ? "ID " + tid : "";
    n.className = n.className.replace(/\bt-\w+/g, "").trim() + " t-" + L[2];
    return m ? +m[2] : 0;
  }
  /* thr : hauteur (part de la vue) sous laquelle l'étiquette passe dans le
     cadre, pour ne pas chevaucher le nom de la caméra en haut de la tuile. */
  function posBox(n, r, v, thr) {
    var s = n.style;
    s.setProperty("--x", pct(r[0], W)); s.setProperty("--y", pct(r[1], H));
    s.setProperty("--w", pct(r[2], W)); s.setProperty("--h", pct(r[3], H));
    tog(n, "is-in", (r[1] - v[1]) / v[3] < (thr || .22));
    tog(n, "is-right", (r[0] + r[2] / 2 - v[0]) / v[2] > .6);
  }

  /* Trace au sol : la position des pieds sur les ~1,3 dernières secondes,
     qui s'estompe vers l'arrière (dessinée dans les coordonnées de l'image). */
  var NS = "http://www.w3.org/2000/svg", TRAIL = 12, TSTEP = 110;
  function makeTrail(k) {
    uid++;
    var s = document.createElementNS(NS, "svg");
    s.setAttribute("viewBox", "0 0 " + W + " " + H);
    s.setAttribute("preserveAspectRatio", "none");
    s.setAttribute("aria-hidden", "true");
    s.setAttribute("class", "sec-trail t-" + k);
    s.innerHTML = '<defs><linearGradient id="st' + uid + '" gradientUnits="userSpaceOnUse"><stop offset="0"/><stop offset="1"/></linearGradient></defs>' +
      '<path class="tr-line" stroke="url(#st' + uid + ')"/><path class="tr-dot"/>';
    return s;
  }
  function drawTrail(s, w, t) {
    var a = [], k, p;
    for (k = TRAIL; k >= 0; k--) { p = walkerAt(w, t - k * TSTEP); if (p && p.o > .2) a.push(p); }
    if (!a.length) return;
    var g = s.firstChild.firstChild, f = a[0], l = a[a.length - 1];
    s.childNodes[1].setAttribute("d", "M" + a.map(function (q) { return q.x.toFixed(1) + " " + q.y.toFixed(1); }).join("L"));
    g.setAttribute("x1", f.x.toFixed(1)); g.setAttribute("y1", f.y.toFixed(1));
    g.setAttribute("x2", l.x.toFixed(1)); g.setAttribute("y2", l.y.toFixed(1));
    s.childNodes[2].setAttribute("d", "M" + l.x.toFixed(1) + " " + l.y.toFixed(1) + "h.01");
  }

  /* Comme une vraie analyse vidéo : le cadre suit la personne avec un léger
     retard et respire un peu; la confiance varie pendant la marche et se
     stabilise à l'arrêt. */
  function wob(t, s, f) { return Math.sin(t / f + s) * Math.sin(t / (f * 1.7) + s * 2.3); }
  function drawBox(rb, t, dt) {
    var b = rb.def, raw = boxOn(b, t) && boxRect(b, t), tile = tiles[b.tile], w = b.track && run.wmap[b.track];
    if (!raw) {
      if (rb.node) { kill(rb.node); kill(rb.trail); rb.node = rb.trail = rb.r = null; rb.lab = -1; }
      return;
    }
    if (!rb.node || rb.node.parentNode !== tile.stage) {
      rb.node = makeBox(); tile.stage.appendChild(rb.node); rb.lab = -1; rb.r = null;
      tog(rb.node, "is-under", !!b.under);
      if (w) { rb.trail = makeTrail(b.labels[0][2]); tile.stage.appendChild(rb.trail); }
    }
    var j = boxLabel(b, t);
    if (j !== rb.lab) {
      rb.nom = rb.cv = setLabel(rb.node, b.labels[j], w ? w.tid : b.tid);
      if (rb.trail) rb.trail.setAttribute("class", "sec-trail t-" + b.labels[j][2]);
      if (rb.lab >= 0) { rb.node.classList.remove("is-swap"); void rb.node.offsetWidth; rb.node.classList.add("is-swap"); }
      rb.lab = j;
    }
    var r = raw;
    if (w) {
      if (!rb.r || !(dt > 0) || dt > 250) rb.r = raw.slice();
      else for (var i = 0, a = 1 - Math.exp(-dt / 85); i < 4; i++) rb.r[i] += (raw[i] - rb.r[i]) * a;
      var ew = rb.r[2] * .035 * wob(t, rb.seed, 230), eh = rb.r[3] * .018 * wob(t, rb.seed + 1, 310);
      r = [rb.r[0] - ew / 2, rb.r[1] - eh, rb.r[2] + ew, rb.r[3] + eh];
      drawTrail(rb.trail, w, t);
      var p = walkerAt(w, t);
      var c = rb.nom && p && p.mv ? Math.min(99, rb.nom + Math.round(2.4 * Math.sin(Math.floor(t / 280) * 2.1 + rb.seed))) : rb.nom;
      if (c !== rb.cv) { rb.cv = c; rb.node.querySelector(".lb-c").textContent = c + PC; }
    }
    posBox(rb.node, r, tile.cam.view, tile.h ? clamp(46 / tile.h, .2, .36) : .22);
  }

  /* État de chaque tuile, et caméra « active » mise en avant : celle de la
     dernière alerte tant qu'une personne y est suivie (ou pendant 2,6 s),
     sinon toute autre caméra qui suit quelqu'un. */
  var ST = { move: "Mouvement", person: "Personne", vehicle: "Véhicule", parcel: "Colis", alert: "Alerte", known: "Connu", plate: "Plaque", access: "Accès", urg: "Urgence" };
  function tileStatus(t) {
    var best = [null, null, null, null], seen = [false, false, false, false];
    run.boxes.forEach(function (rb) {
      if (!rb.node || rb.lab < 0) return;
      var k = rb.def.labels[rb.lab][2], i = rb.def.tile;
      if (k !== "known" || !best[i]) best[i] = k;
      if (rb.def.track) seen[i] = true;
    });
    var L = run.lastTile, act = L != null && (seen[L] || t - run.lastT < 2600) ? L : seen.indexOf(true);
    tiles.forEach(function (tile, i) {
      var k = best[i] || "calm";
      tile.busy = seen[i];
      tog(tile.el, "is-act", i === act);
      if (tile.k === k) return;
      tile.k = k;
      if (k !== "calm") tile.el.style.setProperty("--a", cvar(k));
      tile.st.textContent = k === "calm" ? "Calme" : ST[k];
      tile.st.className = "sec-st t-" + k;
    });
  }

  /* Débit du flux, relu chaque seconde : il monte quand quelque chose bouge
     dans l'image (l'encodeur a plus à transmettre), redescend au calme. */
  function bitrate(dt) {
    run.brT += dt;
    if (run.brT < 1000) return;
    run.brT = 0;
    tiles.forEach(function (tile) {
      if (!tile.br) return;
      tile.brV = clamp(tile.brV + ((tile.busy ? 4.4 : 1.8) - tile.brV) * .45 + (Math.random() - .5) * .4, .9, 6.4);
      tile.br.textContent = tile.brV.toFixed(1).replace(".", ",") + " Mb/s";
    });
  }

  /* ---------- Effets visuels ---------- */
  /* Relance une classe d'animation sur la tuile, puis la retire */
  function pulse(tile, cls, ms) {
    tile.el.classList.remove(cls); void tile.el.offsetWidth; tile.el.classList.add(cls);
    later(function () { tile.el.classList.remove(cls); }, ms);
  }
  /* Alerte : liseré lumineux de la couleur de la détection */
  function hit(tile, k) {
    tile.el.style.setProperty("--c", cvar(k));
    pulse(tile, "is-hit", 1500);
  }
  /* Bref artefact de compression (le flux se réajuste au mouvement) */
  function glitch(tile, delay) {
    if (reduce) return;
    later(function () { pulse(tile, "is-glitch", 380); }, delay || 0);
  }
  /* Éclair : fort à l'allumage des lumières, discret (obturateur) pour une capture */
  function flashTile(tile, soft) {
    if (reduce) return;
    pulse(tile, soft ? "is-shot" : "is-flash", 800);
  }
  function snap(e) {
    if (reduce) return;
    var tile = tiles[e.tile], chip = el("span", "sec-snap", ICON.cam + "<span>Preuve </span>capturée");
    chip.setAttribute("aria-hidden", "true");
    tile.el.appendChild(chip);
    flashTile(tile, true);
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
    count(run.n);
    phase(run.n + (run.n > 1 ? " alertes reçues" : " alerte reçue"), "idle");
    if (ev.tile != null) {
      run.lastTile = ev.tile; run.lastT = ev.t;
      hit(tiles[ev.tile], ev.k);
      if (/^(move|person|vehicle)$/.test(ev.k)) glitch(tiles[ev.tile]);
    }
    if (ev.sensor) {
      sensorHit(ev.sensor, ev.state, ev.k);
      if (ev.reset) later(function () { sensorReset(ev.sensor); }, ev.reset);
    }
    if (ev.wake) ev.wake.forEach(wake);
    if (ev.reg) addReg(hmin(simAt(ev.t)), ev.reg[0], ev.reg[1], ev.reg[2], true);
    if (ev.relay) run.relayed = true;
    if (ev.urgence) urgOn();
    if (feed.classList.contains("is-lens")) buildLens();
    comet(ev.sensor ? sensorEl(ev.sensor) : tiles[ev.tile].view, li, ev.k);
  }
  /* « 17 h 06 » pour le registre des plaques */
  function hmin(s) {
    s = Math.floor(s) % 86400;
    return Math.floor(s / 3600) + NBSP + "h" + NBSP + pad(Math.floor(s / 60) % 60);
  }
  function addReg(when, plate, st, cls, fresh) {
    if (!regList) return;
    var li = el("li", "r-" + cls + (fresh ? " is-new" : ""),
      "<time>" + when + "</time><b>" + plate + "</b><span>" + st + "</span>");
    regList.insertBefore(li, regList.firstChild);
    while (regList.children.length > 5) regList.removeChild(regList.lastChild);
  }
  /* Compteur à rouleau : l'ancien chiffre monte et sort, le nouveau entre
     (sans html.fx, seul le nouveau chiffre est visible). */
  function count(n) {
    nRaw.innerHTML = '<span class="n-out" aria-hidden="true">' + (n - 1) + '</span><span class="n-in">' + n + "</span>";
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
    if (run.urg) phase("Mode urgence", "urg");
    else phase("1 événement compris", "ok");
    live.textContent = sum.textContent;
    if (run.sc.inc.urg) urgRun();
    if (feed.classList.contains("is-lens")) buildLens();
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
    /* Compte de la situation : flèche, téléphone, registre, mode urgence */
    if (arrowK) arrowK.textContent = "1 notification au lieu de " + sc.events.length;
    if (phoneB) phoneB.textContent = I.phone || "1 notification au lieu de " + sc.events.length + ".";
    if (regBox) {
      regBox.hidden = !sc.reg;
      regList.innerHTML = "";
      (sc.reg || []).slice().reverse().forEach(function (r) { addReg(r[0], r[1], r[2], r[3]); });
    }
    if (urgBox) {
      urgBox.hidden = !I.urg;
      urgList.innerHTML = "";
      urgEnd.hidden = true;
      urgEnd.textContent = "";
      urgLift.hidden = true;
      urgLift.innerHTML = "";
    }
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
      var fig = el("figure", "sec-th"), view = el("div", "sec-th-view" + (sc.mood === "ir" || cam.ir ? " is-ir" : ""));
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
        var r = boxRect(b, e.t), w = b.track && run.wmap[b.track];
        if (!r) return;
        var n = makeBox(), L = b.labels[boxLabel(b, e.t)];
        setLabel(n, L, w ? w.tid : b.tid);
        posBox(n, r, v);
        if (w) { var tr = makeTrail(L[2]); drawTrail(tr, w, e.t); s.appendChild(tr); }
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
      if (a.relay && run) { run.relayed = true; if (feed.classList.contains("is-lens")) buildLens(); }
      confirmed(a.fx);
    }, reduce ? 700 : 2500);
  }
  function lightTiles(idx) {
    idx.forEach(function (i) { var t = tiles[i]; t.el.classList.add("is-lit"); flashTile(t); });
  }
  function effect(fx) {
    if (fx === "lights") lightTiles([0, 1, 2, 3]);
    if (fx === "dock") lightTiles([2, 3]);
    if (fx === "srv") { sensorHit("door", "Verrouillée · étage", "lock"); flashTile(tiles[2], true); }
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

  /* ---------- Mode urgence ----------
     Escalade automatique, sobre : liseré rouge fin sur le mur, incrustation
     « MODE URGENCE », actions exécutées une à une (chacune confirmée avant
     la suivante, l'appel sonne pour vrai). La levée demande confirmation. */
  function urgOn() {
    if (!run || run.urg) return;
    run.urg = true;
    root.classList.add("is-urgence");
    phase("Mode urgence", "urg");
    tiles.forEach(function (t) {
      var c = el("span", "sec-urgosd", "Mode urgence");
      c.setAttribute("aria-hidden", "true");
      t.el.appendChild(c);
    });
    live.textContent = "JARVIS passe en mode urgence.";
  }
  function urgOff() {
    if (run) run.urg = false;
    root.classList.remove("is-urgence");
    $$(".sec-urgosd").forEach(function (n) { n.parentNode.removeChild(n); });
    phase("1 événement compris", "ok");
  }
  function urgRun() {
    var U = run.sc.inc.urg;
    urgList.innerHTML = U.acts.map(function (a, i) {
      return '<li data-state="wait"><span class="sec-act-ico" aria-hidden="true">' + ICON[a.ico] +
        "</span><b>" + a.label + '</b><span class="sec-urg-st" role="status"></span></li>';
    }).join("");
    var rows = $$("li", urgList);
    if (reduce) {
      rows.forEach(function (li, i) {
        li.setAttribute("data-state", "done");
        $(".sec-urg-st", li).textContent = U.acts[i].ok;
      });
      urgDone();
      return;
    }
    var i = 0;
    function next() {
      if (!run || run.sc.inc.urg !== U) return; // la situation a changé
      if (i >= rows.length) { urgDone(); return; }
      var a = U.acts[i], li = rows[i], st = $(".sec-urg-st", li), iv = 0;
      li.setAttribute("data-state", "go");
      if (a.call) {
        var sec = 0;
        st.textContent = "Sonnerie · 0:00…";
        iv = setInterval(function () {
          sec++;
          if (sec * 1000 < a.ms) st.textContent = "Sonnerie · 0:" + pad(sec) + "…";
        }, 1000);
        timers.push(iv); // clearTimeout efface aussi un intervalle (même liste)
      } else {
        st.textContent = "Envoi de la commande…";
      }
      if (a.fx) effect(a.fx);
      later(function () {
        if (iv) clearInterval(iv);
        li.setAttribute("data-state", "done");
        st.textContent = a.ok;
        i++;
        later(next, 380);
      }, a.ms);
    }
    next();
  }
  function urgDone() {
    run.relayed = true;
    urgEnd.textContent = run.sc.inc.urg.end;
    urgEnd.hidden = false;
    urgLift.innerHTML = '<button type="button" data-urg="lift">Lever le mode urgence</button>';
    urgLift.hidden = false;
    live.textContent = urgEnd.textContent;
    if (feed.classList.contains("is-lens")) buildLens();
  }
  if (urgLift) urgLift.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("button[data-urg]");
    if (!b || !run) return;
    var k = b.getAttribute("data-urg");
    if (k === "lift") {
      urgLift.innerHTML = '<span class="sec-urg-q">Confirmer la levée du mode urgence?</span>' +
        '<span class="sec-urg-btns"><button type="button" data-urg="yes">Lever</button>' +
        '<button type="button" data-urg="no">Garder</button></span>';
    } else if (k === "no") {
      urgLift.innerHTML = '<button type="button" data-urg="lift">Lever le mode urgence</button>';
    } else if (k === "yes") {
      urgOff();
      urgLift.hidden = true;
      urgLift.innerHTML = "";
      addFollow(hms(simAt(run.t)) + " — mode urgence levé par vous · les caméras du secteur restent en direct.");
    }
  });

  /* ---------- Vue « Incidents » ----------
     Les alertes brutes, regroupées par incident : gravité, état (ouvert,
     consigné, relayé) et caméras concernées. La situation en cours s'ajoute
     au-dessus des incidents déjà au dossier. */
  var LENS_TITLE = {
    livraison: "Livraison — entrée avant",
    visiteur: "Visiteur inconnu la nuit — terrasse",
    entrepot: "Entrée après la fermeture — quai",
    plaques: "Plaque inconnue consignée — entrée",
    serveurs: "Accès refusé répété — salle des serveurs",
    forcee: "Intrusion — porte forcée · mode urgence"
  };
  var LENS_ST = { ouvert: "Ouvert", consigne: "Consigné", relaye: "Relayé" };
  function lensRow(it) {
    return '<li class="sec-i sv-' + it.sev + (it.cur ? " is-cur" : "") + '"><i class="sec-i-dot" aria-hidden="true"></i>' +
      "<div><b>" + it.title + "</b><small>" + it.when + " · " + it.n + " alertes · " + it.cams + "</small></div>" +
      '<span class="sec-i-st st-' + it.st + '">' + LENS_ST[it.st] + "</span></li>";
  }
  function buildLens() {
    if (!lensView) return;
    var sc = run.sc, seen = {}, cams = [];
    sc.events.forEach(function (e) {
      if (e.tile == null || seen[e.tile]) return;
      seen[e.tile] = 1;
      cams.push("CAM 0" + (e.tile + 1));
    });
    var cur = {
      sev: sc.inc.lvl === "ok" ? "ok" : sc.inc.lvl === "warn" ? "warn" : "crit",
      when: "En cours · " + hmin(secs(sc.start)),
      title: LENS_TITLE[run.key] || "Situation en cours",
      st: run.phase >= 3 ? (run.relayed ? "relaye" : "consigne") : "ouvert",
      cams: cams.sort().join(" · "), n: Math.max(run.n, 1), cur: true
    };
    lensView.innerHTML = [cur].concat(HIST).map(lensRow).join("");
  }
  function setLens(mode) {
    var on = mode === "incidents";
    lensBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", String((b.getAttribute("data-sec-lens") === "incidents") === on));
    });
    tog(feed, "is-lens", on);
    lensView.hidden = !on;
    if (on) buildLens();
  }
  lensBtns.forEach(function (b) {
    b.addEventListener("click", function () { setLens(b.getAttribute("data-sec-lens")); });
  });

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
    var sc = run.sc, T = run.T, dt = t - run.lt;
    run.lt = t;
    sc.walkers.forEach(function (w) { drawWalker(w, t); });
    sc.props.forEach(function (p, i) { drawProp(p, i, t); });
    run.boxes.forEach(function (rb) { drawBox(rb, t, dt); });
    tileStatus(t);
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
    bitrate(dt);
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
    root.classList.remove("is-urgence");
    $$(".sec-urgosd").forEach(function (n) { n.parentNode.removeChild(n); });
    tiles.forEach(function (tile, i) {
      tile.cam = SITES[sc.site].cams[i];
      $$(".sec-subj, .sec-box, .sec-trail, .sec-prop, .sec-say, .sec-snap", tile.el).forEach(function (n) { n.parentNode.removeChild(n); });
      tile.el.classList.remove("is-lit", "is-hit", "is-flash", "is-shot", "is-glitch", "is-act");
      tog(tile.el, "is-sleep", !!tile.cam.sleep);
      tile.k = null;
      tile.busy = false;
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
      key: key, sc: sc, t: 0, lt: 0, ev: 0, shot: 0, phase: 0, n: 0, lastS: -1, lastTile: null, lastT: -1e9, brT: 0,
      urg: false, relayed: false,
      wn: {}, pn: {}, dir: {}, wmap: {},
      boxes: sc.boxes.map(function (b, i) { return { def: b, node: null, trail: null, r: null, lab: -1, seed: i * 1.7 + .4 }; }),
      T: { link: end + 700, collapse: end + 2000, reveal: end + 2800, done: end + 4000 }
    };
    sc.walkers.forEach(function (w) { run.wmap[w.id] = w; });
    renderInc(sc);
    setLens("alertes");
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
