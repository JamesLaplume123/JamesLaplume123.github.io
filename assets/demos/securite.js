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

  /* Rendu partagé avec les modules de la plateforme (fin de ce fichier) :
     mêmes silhouettes, même voiture, mêmes icônes. */
  root._sx = { PERSON: PERSON, CAR: CAR, ICON: ICON };

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
    var murP = root.querySelector('[data-sx-panel="mur"]') || root;
    tog(murP, "is-paused", true);
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting && e.intersectionRatio >= .35) begun = true;
        visible = begun && e.isIntersecting;
        tog(murP, "is-paused", !visible);
        play();
      });
    }, { threshold: [0, .35, .6] }).observe(murP);
  } else {
    visible = begun = true;
    play();
  }
})();


/* ==========================================================================
   Plateforme de sécurité — les huit modules autour du mur vidéo.
   Accès, véhicules, personnes, zones et règles, incidents, carte des sites,
   rondes et agents, conformité (Loi 25). Chaque module est construit à sa
   première ouverture (rien n'est rendu d'avance), joue sa propre séquence
   en boucle tant qu'il est affiché et que la démo est à l'écran, puis se
   met en pause. Mouvement réduit ou sans html.fx : état final, aucune
   boucle. Données d'exemple seulement : personnes, plaques, sites et
   numéros sont fictifs.
   ========================================================================== */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="securite"]');
  if (!root || !window.requestAnimationFrame) return;
  var nav = root.querySelector("[data-sx-nav]");
  if (!nav) return;

  var docEl = document.documentElement;
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var ART = root._sx || {};
  var ICON = ART.ICON || {};
  var W = 1672, H = 941, NS = "http://www.w3.org/2000/svg";
  var NB = " ", NN = " ", PC = " %";
  var MS = "/media/solutions/";
  var PH = {};
  try { PH = JSON.parse(root.getAttribute("data-sx-ph") || "{}"); } catch (e) { PH = {}; }

  /* ---------- Outils ---------- */
  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function sv(tag, at, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in at) if (at.hasOwnProperty(k)) n.setAttribute(k, at[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function tog(n, c, on) { if (n && n.classList.contains(c) !== !!on) n.classList.toggle(c, !!on); }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function hms(s) { s = Math.floor(s); s = ((s % 86400) + 86400) % 86400; return pad(Math.floor(s / 3600)) + ":" + pad(Math.floor(s / 60) % 60) + ":" + pad(s % 60); }
  function secs(str) { var p = str.split(":"); return +p[0] * 3600 + +p[1] * 60 + +(p[2] || 0); }
  function num(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, NN); }
  function dec(n, d) { return n.toFixed(d == null ? 1 : d).replace(".", ","); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function lerp(a, b, u) { return a + (b - a) * u; }
  function smooth(u) { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); }
  function pct(v, of) { return (v / of * 100).toFixed(3); }
  function stageCss(v) {
    return "left:" + (-v[0] / v[2] * 100).toFixed(3) + "%;top:" + (-v[1] / v[3] * 100).toFixed(3) +
      "%;width:" + (W / v[2] * 100).toFixed(3) + "%;height:" + (H / v[3] * 100).toFixed(3) + "%";
  }
  function rng(seed) { // générateur reproductible (mêmes données à chaque visite)
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function ico(k) { return ICON[k] || ""; }
  var CHECK = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="m2.5 6.3 2.3 2.2 4.7-5"/></svg>';
  var uid = 0;

  /* Interpolation d'un trajet [t, x, y, (h)] avec départs et arrêts adoucis.
     Rend { x, y, h, mv, left, o, i } ou null hors du trajet. */
  function along(keys, t, fade) {
    var n = keys.length, end = keys[n - 1][0];
    if (t < keys[0][0] || (fade && t > end + fade)) return null;
    var p;
    if (t >= end) {
      var z = keys[n - 1];
      p = { x: z[1], y: z[2], h: z[3], mv: false, i: n - 1 };
    } else {
      var i = 0;
      while (i < n - 2 && t >= keys[i + 1][0]) i++;
      var a = keys[i], b = keys[i + 1], u = (t - a[0]) / Math.max(1, b[0] - a[0]);
      var still = a[1] === b[1] && a[2] === b[2];
      var s0 = i === 0 || (keys[i - 1][1] === a[1] && keys[i - 1][2] === a[2]);
      var s1 = i + 1 === n - 1 || (keys[i + 2][1] === b[1] && keys[i + 2][2] === b[2]);
      var e = s0 && s1 ? .5 - .5 * Math.cos(Math.PI * u) : s0 ? 1 - Math.cos(Math.PI * u / 2) : s1 ? Math.sin(Math.PI * u / 2) : u;
      p = { x: lerp(a[1], b[1], e), y: lerp(a[2], b[2], e), h: a[3] == null ? null : lerp(a[3], b[3], e), mv: !still, left: still ? null : b[1] < a[1], i: i };
    }
    p.o = 1;
    if (fade) p.o = clamp(Math.min((t - keys[0][0]) / fade, 1 - (t - end) / fade), 0, 1);
    return p;
  }

  /* ---------- Briques visuelles partagées ---------- */
  function person(kind) {
    return el("div", "sec-subj k-" + kind, (ART.PERSON || "").replace(/@/g, "x" + (++uid)));
  }
  function placeP(n, p) {
    if (!p) { n.style.opacity = 0; return; }
    var s = n.style;
    s.setProperty("--x", pct(p.x, W)); s.setProperty("--y", pct(p.y, H)); s.setProperty("--h", pct(p.h, H));
    s.opacity = p.o.toFixed(3);
    tog(n, "is-walk", p.mv);
    if (p.left != null) tog(n, "is-left", p.left);
  }
  function box(t) {
    return el("div", "sec-box t-" + t, '<i></i><i></i><i></i><i></i><b><span class="lb-k"></span><span class="lb-c"></span><span class="lb-id"></span></b>');
  }
  function setBox(n, r, k, c, id) {
    var s = n.style, q = n.querySelectorAll("b > span");
    s.setProperty("--x", pct(r[0], W)); s.setProperty("--y", pct(r[1], H));
    s.setProperty("--w", pct(r[2], W)); s.setProperty("--h", pct(r[3], H));
    if (k != null) q[0].textContent = k;
    if (c != null) q[1].textContent = c ? c + PC : "";
    if (id != null) q[2].textContent = id ? "ID " + id : "";
  }
  function boxAround(p, w, pad) { // cadre autour d'une silhouette (pieds en p.y)
    var h = p.h * 1.02, bw = p.h * (w || .42);
    return [p.x - bw / 2, p.y - h - (pad || 4), bw, h + (pad || 4) * 1.6];
  }
  function hud(num, name) {
    return '<figcaption class="sec-hud"><span class="sec-name"><b>' + num + '</b> <span>' + name + "</span></span>" +
      '<span class="sec-tr" aria-hidden="true"><span class="sec-rec">REC</span></span>' +
      '<time class="sec-ts" data-sx-ts></time></figcaption>';
  }
  /* Tuile de caméra : la photo (jamais retouchée) sous le grain, la vignette
     et les incrustations du mur vidéo. Sans photo : panneau « Photo à venir ». */
  function camTile(o) {
    var f = el("figure", "sec-cam sx-cam" + (o.cls ? " " + o.cls : ""));
    if (!o.img) {
      f.classList.add("sx-ph");
      f.innerHTML = '<div class="sx-ph-in"><span class="sx-ph-i" aria-hidden="true">' + ico("cam") + "</span><b>Photo à venir</b><small>" + o.alt + "</small></div>" + hud(o.num, o.name);
    } else {
      f.innerHTML = '<div class="sec-view"><div class="sec-pan"><div class="sec-stage" style="' + stageCss(o.view) + '">' +
        '<img src="' + o.img + '" alt="' + o.alt + '" loading="lazy" decoding="async"></div></div><i class="sec-fx" aria-hidden="true"></i></div>' + hud(o.num, o.name);
    }
    return { el: f, stage: $(".sec-stage", f), ts: $("[data-sx-ts]", f) };
  }
  /* Repère posé dans l'image (coordonnées de la photo) */
  function pin(stage, cls, x, y, html) {
    var n = el("div", "sx-pin " + (cls || ""), html);
    n.style.left = pct(x, W) + "%"; n.style.top = pct(y, H) + "%";
    stage.appendChild(n);
    return n;
  }
  function head(title, sub, kpis) {
    return '<header class="sx-head"><div class="sx-title"><h3>' + title + '</h3><p>' + sub + "</p></div>" +
      '<dl class="sx-kpis">' + kpis.map(function (k) {
        return '<div class="sx-kpi' + (k[2] ? " is-" + k[2] : "") + '"><dt>' + k[0] + '</dt><dd' + (k[3] ? ' data-k="' + k[3] + '"' : "") + ">" + k[1] + "</dd></div>";
      }).join("") + "</dl></header>";
  }
  function card(cls, title, meta, body) {
    return '<section class="sx-card ' + (cls || "") + '"><header class="sx-card-h"><h4>' + title + "</h4>" +
      (meta ? "<span>" + meta + "</span>" : "") + "</header>" + body + "</section>";
  }
  function pill(txt, tone) { return '<span class="sx-pill is-' + (tone || "ok") + '">' + txt + "</span>"; }
  function plate(txt, small) {
    return '<span class="sx-plate' + (small ? " is-s" : "") + '"><small>QUÉBEC</small><b>' + txt + "</b></span>";
  }
  function initials(name) { return name.split(/[\s\-]+/).filter(Boolean).map(function (w) { return w[0]; }).slice(0, 2).join(""); }
  /* Liste vivante : la nouvelle ligne entre en haut, la plus ancienne sort. */
  function push(list, li, max) {
    list.insertBefore(li, list.firstChild);
    li.classList.add("is-new");
    setTimeout(function () { li.classList.remove("is-new"); }, 1600);
    while (list.children.length > (max || 6)) list.removeChild(list.lastChild);
  }
  function setK(scope, key, v) { var n = $('[data-k="' + key + '"]', scope); if (n) n.innerHTML = v; return n; }
  function bump(n) { if (!n) return; n.classList.remove("is-bump"); void n.offsetWidth; n.classList.add("is-bump"); }

  /* ---------- Plan du campus (véhicules, rondes) ----------
     Fond noir, traits fins : clôture, voies, bâtiments, stationnements,
     voie pompiers. 1 unité ≈ 0,5 m. */
  function campusSvg(extra) {
    var g = ++uid;
    var s = '<svg class="sx-plan" viewBox="0 0 1000 600" role="img" aria-label="Plan du campus (exemple)">' +
      '<defs><pattern id="sxG' + g + '" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" class="pl-grid"/></pattern>' +
      '<pattern id="sxH' + g + '" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V8" class="pl-hatch"/></pattern>' +
      '</defs>' +
      '<rect width="1000" height="600" class="pl-bg"/><rect width="1000" height="600" fill="url(#sxG' + g + ')"/>' +
      /* voies */
      '<path class="pl-road" d="M-20 320H930M300 70V540M900 110V540M300 540H900"/>' +
      '<path class="pl-lane" d="M-20 320H930M300 70V540M900 110V540M300 540H900"/>' +
      /* clôture et barrière */
      '<path class="pl-fence" d="M40 300V40H960V560H40V340"/>' +
      '<path class="pl-gatepost" d="M40 296v8M40 336v8"/>' +
      /* stationnement des employés */
      '<rect class="pl-lot" x="70" y="70" width="200" height="210" rx="4"/>' +
      (function () { var p = ""; for (var r = 0; r < 3; r++) for (var c = 0; c < 9; c++) p += '<path class="pl-stall" d="M' + (82 + c * 21) + " " + (82 + r * 66) + "v" + 26 + '"/>'; return p; })() +
      '<text class="pl-t" x="170" y="62" text-anchor="middle">P1 · EMPLOYÉS</text>' +
      /* bâtiment A */
      '<path class="pl-bld" d="M340 80H620V230H560V250H400V230H340Z"/>' +
      '<text class="pl-tb" x="480" y="150" text-anchor="middle">BÂTIMENT A</text><text class="pl-t" x="480" y="168" text-anchor="middle">SIÈGE · BUREAUX</text>' +
      '<rect class="pl-zone-h" x="400" y="252" width="160" height="16" fill="url(#sxH' + g + ')"/>' +
      /* stationnement visiteurs */
      '<rect class="pl-lot" x="660" y="80" width="210" height="150" rx="4"/>' +
      (function () { var p = ""; for (var r = 0; r < 2; r++) for (var c = 0; c < 9; c++) p += '<path class="pl-stall" d="M' + (672 + c * 22) + " " + (92 + r * 70) + "v" + 28 + '"/>'; return p; })() +
      '<text class="pl-t" x="765" y="72" text-anchor="middle">P2 · VISITEURS</text>' +
      /* cour et entrepôt */
      '<rect class="pl-yard" x="580" y="336" width="300" height="34" rx="3"/>' +
      '<rect class="pl-zone-h" x="736" y="340" width="70" height="26" fill="url(#sxH' + g + ')"/>' +
      '<path class="pl-bld" d="M600 372H880V520H600Z"/>' +
      (function () { var p = ""; for (var d = 0; d < 6; d++) p += '<rect class="pl-dock" x="' + (612 + d * 44) + '" y="372" width="30" height="8"/>'; return p; })() +
      '<text class="pl-tb" x="740" y="446" text-anchor="middle">BÂTIMENT B</text><text class="pl-t" x="740" y="464" text-anchor="middle">ENTREPÔT · 6 QUAIS</text>' +
      /* atelier */
      '<path class="pl-bld" d="M70 380H270V520H70Z"/>' +
      '<text class="pl-tb" x="170" y="446" text-anchor="middle">BÂTIMENT C</text><text class="pl-t" x="170" y="464" text-anchor="middle">ATELIER</text>' +
      /* guérite */
      '<rect class="pl-bld is-s" x="54" y="344" width="34" height="22" rx="2"/><text class="pl-t" x="71" y="382" text-anchor="middle">GUÉRITE</text>' +
      '<text class="pl-t is-n" x="958" y="30" text-anchor="end">N ↑ · 1 CASE = 10 M</text>' +
      (extra ? extra(g) : "") + "</svg>";
    return s;
  }
  /* Cônes de caméras sur un plan : [nom, x, y, direction (°), ouverture (°), portée] */
  function coneD(c) {
    var a0 = (c[3] - c[4] / 2) * Math.PI / 180, a1 = (c[3] + c[4] / 2) * Math.PI / 180, r = c[5];
    return "M" + c[1] + " " + c[2] + "L" + (c[1] + r * Math.cos(a0)).toFixed(1) + " " + (c[2] + r * Math.sin(a0)).toFixed(1) +
      "A" + r + " " + r + " 0 0 1 " + (c[1] + r * Math.cos(a1)).toFixed(1) + " " + (c[2] + r * Math.sin(a1)).toFixed(1) + "Z";
  }
  function inCone(c, x, y) {
    var dx = x - c[1], dy = y - c[2], d = Math.sqrt(dx * dx + dy * dy);
    if (d > c[5] || d < 4) return false;
    var a = Math.atan2(dy, dx) * 180 / Math.PI - c[3];
    a = ((a + 540) % 360) - 180;
    return Math.abs(a) <= c[4] / 2;
  }
  function conesSvg(cams, g) {
    return cams.map(function (c, i) {
      var id = "sxK" + g + "-" + i;
      return '<g class="pl-cam" data-cam="' + i + '"><radialGradient id="' + id + '" gradientUnits="userSpaceOnUse" cx="' + c[1] + '" cy="' + c[2] + '" r="' + c[5] + '"><stop offset="0" class="cn0"/><stop offset="1" class="cn1"/></radialGradient>' +
        '<path class="pl-cone" d="' + coneD(c) + '" fill="url(#' + id + ')"/>' +
        '<circle class="pl-cdot" cx="' + c[1] + '" cy="' + c[2] + '" r="5"/>' +
        '<text class="pl-ct" x="' + (c[1] + (c[6] || 0)) + '" y="' + (c[2] + (c[7] || -10)) + '" text-anchor="middle">' + c[0] + "</text></g>";
    }).join("");
  }

  /* ---------- Moteur des modules ----------
     Un module : { site, clock (« hh:mm:ss » simulé), len (boucle, ms),
     build(panneau) une seule fois, reset() à chaque boucle (remplit la
     séquence avec at()), frame(t, dt) à chaque image, leave() }. */
  var MODS = {}, active = "mur", visible = false, raf = 0, last = 0;
  var clockEl = $("[data-sec-clock]"), siteEl = $("[data-sec-site]"), wallSite = "", wallClock = "";
  var cur = null; // module en cours (pour at())

  function motion() { return !reduce && docEl.classList.contains("fx"); }
  function at(ms, fn) { cur.seq.push([ms, fn]); }
  function restart(m) {
    cur = m;
    m.seq = []; m.t = 0; m.q = 0; m.lastS = -1;
    m.reset();
    m.seq.sort(function (a, b) { return a[0] - b[0]; });
  }
  function advance(m, t) { while (m.q < m.seq.length && m.seq[m.q][0] <= t) m.seq[m.q++][1](); }
  function simNow(m) { return secs(m.clock) + m.t / 1000 * (m.rate || 1); }
  function clock(m) {
    var s = Math.floor(simNow(m));
    if (s === m.lastS) return;
    m.lastS = s;
    var txt = hms(s);
    if (clockEl) clockEl.textContent = txt;
    if (m.onSecond) m.onSecond(txt, s);
  }
  function finish(m) { // mouvement réduit : l'état final, calculé d'un coup, sans boucle
    var end = m.final != null ? m.final : (m.len || 0);
    if (m.frame) for (var t = 0; t < end; t += 100) { m.t = t; advance(m, t); m.frame(t, 100); }
    m.t = end;
    advance(m, m.final != null ? end : Infinity);
    if (m.frame) m.frame(end, 0);
    clock(m);
  }
  function tick(now) {
    raf = 0;
    var m = MODS[active];
    if (!m || !visible || !motion()) return;
    var dt = last ? Math.min(80, now - last) : 16;
    last = now;
    m.t += dt;
    advance(m, m.t);
    if (m.frame) m.frame(m.t, dt);
    clock(m);
    if (m.len && m.t >= m.len) restart(m);
    raf = requestAnimationFrame(tick);
  }
  function play() {
    if (raf || active === "mur" || !visible || !motion()) return;
    last = 0;
    raf = requestAnimationFrame(tick);
  }
  /* Petit minuteur lié au module : ne se déclenche que si le module est
     toujours affiché (sert aux réponses des boutons). */
  function soon(ms, fn) {
    var k = active;
    setTimeout(function () { if (active === k) fn(); }, motion() ? ms : 0);
  }

  /* =====================================================================
     ACCÈS — badges, zones, horaires, anti-retour, talonnage, visiteurs QR,
     refus répétés. Scène : porte de service B; une employée badge, une
     seconde personne la suit de près : 2 passages, 1 badge → talonnage.
     ===================================================================== */
  var ACC_FEED = [
    ["ok", "grant", "Accordé", "Émilie Fortin", "Employée · Finances", "Hall · tourniquet 2"],
    ["ok", "grant", "Accordé", "Karim Haddad", "Équipe TI", "Bâtiment A · porte 3"],
    ["gold", "grant", "Visiteur", "Léa Gagnon", "Laissez-passer QR", "Hall · borne d’accueil"],
    ["bad", "access", "Refusé", "Badge E-1187", "Hors horaire", "Toit · accès technique"],
    ["ok", "grant", "Accordé", "Olivier Roy", "Sous-traitant · CVC", "Entrepôt · porte 6"],
    ["warn", "door", "Anti-retour", "Badge E-0733", "Entrée sans sortie", "Stationnement P1 · barrière"],
    ["ok", "grant", "Accordé", "Nadia Bouchard", "Entretien", "Bâtiment C · atelier"],
    ["bad", "access", "Refusé", "Badge E-1187", "Zone non autorisée", "Salle des serveurs · sas"],
    ["ok", "grant", "Accordé", "Thomas Bergeron", "Employé · Logistique", "Entrepôt · quai 2"],
    ["warn", "door", "Porte maintenue", "Porte 14", "Ouverte 42 s", "Bâtiment B · sortie est"],
    ["ok", "lock", "Double validation", "Karim Haddad", "Badge + NIP", "Salle des serveurs · sas"],
    ["ok", "grant", "Accordé", "Camille Lavoie", "Employée · Direction", "Bâtiment A · ascenseur"]
  ];
  var ACC_ZONES = ["Hall", "Bureaux", "Entrepôt", "Serveurs", "Toit"];
  var ACC_GROUPS = [
    ["Employés", ["24 h", "6 h – 20 h", "6 h – 20 h", "—", "—"]],
    ["Équipe TI", ["24 h", "24 h", "6 h – 20 h", "Badge + NIP", "Sur demande"]],
    ["Entretien", ["24 h", "18 h – 23 h", "18 h – 23 h", "Escorte", "—"]],
    ["Sous-traitants", ["7 h – 17 h", "Escorte", "7 h – 17 h", "—", "Permis de travail"]],
    ["Visiteurs", ["QR · 1 jour", "Escorte", "—", "—", "—"]]
  ];

  function qrSvg(seed) { // code QR d'exemple (motif reproductible, trois repères)
    var r = rng(seed), n = 25, s = '<svg viewBox="-2 -2 29 29" class="sx-qr" aria-hidden="true"><rect x="-2" y="-2" width="29" height="29" rx="1.5" class="qr-bg"/>';
    function finder(x, y) {
      return '<path class="qr-m" d="M' + x + " " + y + "h7v7h-7zM" + (x + 1) + " " + (y + 1) + "v5h5v-5z" + '" fill-rule="evenodd"/><rect class="qr-m" x="' + (x + 2) + '" y="' + (y + 2) + '" width="3" height="3"/>';
    }
    var d = "";
    for (var y = 0; y < n; y++) for (var x = 0; x < n; x++) {
      if ((x < 8 && y < 8) || (x > 16 && y < 8) || (x < 8 && y > 16)) continue;
      if (r() < .47) d += "M" + x + " " + y + "h1v1h-1z";
    }
    s += '<path class="qr-m" d="' + d + '"/>' + finder(0, 0) + finder(18, 0) + finder(0, 18) + '<rect class="qr-scan" x="-2" y="-2" width="29" height="2.4"/></svg>';
    return s;
  }

  MODS.acces = {
    site: "Campus Est · contrôle d’accès · 312 portes",
    clock: "08:58:40",
    len: 17000,
    final: 9500,
    build: function (P) {
      var m = this;
      P.innerHTML = head("Contrôle d’accès", "Badges, zones, horaires et visiteurs, reliés aux caméras de chaque porte.", [
        ["Portes en ligne", "312<small>/312</small>", "ok"],
        ["Badges actifs", num(1284)],
        ["Accordés aujourd’hui", num(3912), "", "grant"],
        ["Refus", "37", "", "deny"],
        ["Talonnages", "1", "bad", "tail"]
      ]) +
      '<div class="sx-grid sx-acc">' +
        '<div class="sx-col">' +
          '<div class="sx-doorwrap" data-acc-door></div>' +
          '<div class="sx-camrow" data-acc-row></div>' +
        "</div>" +
        card("sx-feedc", "Événements d’accès", '<i class="sx-live"></i>En direct', '<ol class="sx-feed" data-acc-feed></ol>') +
      "</div>" +
      '<div class="sx-grid sx-g3">' +
        card("sx-matrix", "Zones et horaires", "5 groupes · 5 zones",
          '<div class="sx-mx" data-acc-mx><span></span>' + ACC_ZONES.map(function (z) { return "<b>" + z + "</b>"; }).join("") +
          ACC_GROUPS.map(function (g) {
            return "<em>" + g[0] + "</em>" + g[1].map(function (c, i) {
              var t = c === "—" ? "is-no" : /NIP|Escorte|demande|Permis|QR/.test(c) ? "is-cond" : "is-ok";
              return '<span class="' + t + '" data-z="' + i + '">' + c + "</span>";
            }).join("");
          }).join("") + "</div>") +
        card("sx-pass", "Laissez-passer visiteur", "QR · valide 1 jour",
          '<div class="sx-pass-in"><div class="sx-qrw">' + qrSvg(4217) + '</div><div class="sx-pass-t">' +
          '<b>Léa Gagnon</b><small>Invitée par Marc-André Pelletier · Finances</small>' +
          '<p><span>Valide</span>Aujourd’hui · 9 h à 17 h</p><p><span>Zones</span>Hall · Salle de conférence 2</p>' +
          '<p class="sx-pass-st" data-acc-pass>' + pill("En attente à la borne", "idle") + "</p></div></div>") +
        card("sx-rules", "Règles d’accès", "6 actives",
          '<ul class="sx-rl" data-acc-rules>' + [
            ["tail", "Talonnage · une personne par badge", "1"],
            ["apb", "Anti-retour · entrée sans sortie", "1"],
            ["held", "Porte maintenue ouverte · plus de 30 s", "3"],
            ["rep", "Refus répétés · 3 en 5 min", "0"],
            ["hrs", "Accès hors horaire", "4"],
            ["mfa", "Salle des serveurs · badge + NIP", "Actif"]
          ].map(function (r) { return '<li data-r="' + r[0] + '"><span>' + r[1] + "</span><b>" + r[2] + "</b></li>"; }).join("") + "</ul>" +
          '<div class="sx-rep" data-acc-rep hidden></div>') +
      "</div>";
      m.P = P;
      m.feed = $("[data-acc-feed]", P);
      /* Caméra de la porte : photo du quai de livraison, cadrée sur la porte de service */
      var cam = camTile({ img: MS + "security-enterprise-delivery-v1.webp", view: [980, 110, 692, 432.5], num: "CAM 21", name: "Porte de service B", alt: "Caméra de la porte de service B : porte vitrée ouverte, lecteur de badge et bornes éclairées", cls: "sx-wide" });
      $("[data-acc-door]", P).appendChild(cam.el);
      m.cam = cam;
      var st = cam.stage;
      /* Ligne de comptage et zone de la porte (coordonnées de la photo) */
      var ov = sv("svg", { "class": "sx-ov", viewBox: "0 0 " + W + " " + H, preserveAspectRatio: "none", "aria-hidden": "true" }, st);
      m.line = sv("path", { "class": "sx-trip", d: "M1352 506L1446 498", "vector-effect": "non-scaling-stroke" }, ov);
      sv("path", { "class": "sx-doorz", d: "M1368 212H1434V500H1368Z", "vector-effect": "non-scaling-stroke" }, ov);
      m.reader = pin(st, "sx-reader", 1457, 405, "<i></i>");
      m.rchip = pin(st, "sx-rchip", 1470, 350, "");
      m.count = el("div", "sx-count", '<span><small>Passages</small><b data-c="p">0</b></span><span><small>Badges</small><b data-c="b">0</b></span>');
      cam.el.appendChild(m.count);
      m.banner = el("div", "sx-banner", '<i aria-hidden="true">' + ico("urg") + '</i><span><b>Talonnage détecté</b><small>2 personnes, 1 badge · porte de service B</small></span>');
      cam.el.appendChild(m.banner);
      m.pa = person("dark"); m.pb = person("hood");
      st.appendChild(m.pa); st.appendChild(m.pb);
      m.ba = box("person"); m.bb = box("person");
      st.appendChild(m.ba); st.appendChild(m.bb);
      /* Trois autres portes, plus petites */
      var row = $("[data-acc-row]", P);
      [
        { img: PH.hall, view: [0, 0, W, H], num: "CAM 02", name: "Hall · tourniquets", alt: "Hall d’entrée et tourniquets" },
        { img: PH.sas, view: [0, 0, W, H], num: "CAM 31", name: "Salle des serveurs · sas", alt: "Sas de la salle des serveurs" },
        { img: MS + "security-enterprise-parking-v1.webp", view: [120, 120, 760, 570], num: "CAM 07", name: "Barrière P1", alt: "Barrière du stationnement P1" }
      ].forEach(function (o) { var t = camTile(o); row.appendChild(t.el); });
      m.tsAll = $$("[data-sx-ts]", P);
      /* Approuver la suspension de la carte après les refus répétés */
      P.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("button[data-rep]");
        if (!b) return;
        var rep = $("[data-acc-rep]", P), ok = b.getAttribute("data-rep") === "ok";
        rep.querySelector(".sx-rep-b").innerHTML = ok
          ? '<span class="sx-sent">Commande envoyée au contrôleur…</span>'
          : '<span class="sx-sent">Ignoré · noté au journal</span>';
        if (ok) soon(1200, function () { rep.querySelector(".sx-rep-b").innerHTML = '<span class="sx-okk">' + CHECK + "Confirmé · état relu : carte E-1187 suspendue</span>"; });
      });
      m.fi = 0; m.granted = 3912;
    },
    onSecond: function (txt) { this.tsAll.forEach(function (n) { n.textContent = txt; }); },
    reset: function () {
      var m = this;
      m.A = [[300, 1190, 548, 300], [2900, 1392, 506, 262], [4300, 1392, 506, 262], [5200, 1402, 500, 250]];
      m.B = [[1700, 1140, 560, 312], [4500, 1318, 524, 284], [4900, 1338, 516, 276], [5700, 1404, 500, 252]];
      m.seen = { a: 0, b: 0 };
      [m.ba, m.bb].forEach(function (b, i) { b.style.opacity = 0; b.className = "sec-box t-person" + (i ? "" : " sx-lr"); b.querySelector(".lb-k").textContent = "Personne"; });
      m.count.classList.remove("is-on", "is-bad");
      $('[data-c="p"]', m.count).textContent = "0"; $('[data-c="b"]', m.count).textContent = "0";
      m.banner.classList.remove("is-on");
      m.reader.className = "sx-pin sx-reader"; m.rchip.className = "sx-pin sx-rchip"; m.rchip.innerHTML = "";
      m.line.classList.remove("is-hit");
      at(600, function () { m.count.classList.add("is-on"); });
      at(3000, function () {
        m.reader.classList.add("is-ok");
        m.rchip.innerHTML = "<b>E-0412</b> Accordé · É. Fortin";
        m.rchip.classList.add("is-on");
        $('[data-c="b"]', m.count).textContent = "1";
        m.addRow(["ok", "grant", "Accordé", "Émilie Fortin", "Employée · Finances", "Porte de service B"]);
      });
      at(4300, function () { m.rchip.classList.remove("is-on"); });
      at(4950, function () { m.cross(1); });
      at(5600, function () { m.cross(2); });
      at(6100, function () {
        m.count.classList.add("is-bad");
        m.banner.classList.add("is-on");
        m.bb.classList.remove("t-person"); m.bb.classList.add("t-alert");
        m.bb.querySelector(".lb-k").textContent = "Sans badge";
        m.addRow(["bad", "urg", "Talonnage", "2 passages · 1 badge", "Extrait de 20 s conservé", "Porte de service B"], true);
        bump(setK(m.P, "tail", "2"));
        var r = $('[data-r="tail"] b', m.P); r.textContent = "2"; bump(r.parentNode);
      });
      at(12500, function () { m.banner.classList.remove("is-on"); });
      /* Le reste du campus continue de badger */
      for (var k = 0; k < 9; k++) (function (k) {
        at(900 + k * 1750, function () {
          var r = ACC_FEED[m.fi++ % ACC_FEED.length];
          m.addRow(r);
          if (r[3] === "Badge E-1187" && r[4] === "Zone non autorisée") m.repeated();
        });
      })(k);
      /* Laissez-passer : balayage à la borne, puis validé */
      var pass = $("[data-acc-pass]", m.P);
      pass.innerHTML = pill("En attente à la borne", "idle");
      tog($(".sx-qrw", m.P), "is-scan", false);
      at(7400, function () { tog($(".sx-qrw", m.P), "is-scan", true); pass.innerHTML = pill("Lecture à la borne du hall…", "gold"); });
      at(9200, function () {
        tog($(".sx-qrw", m.P), "is-scan", false); tog($(".sx-qrw", m.P), "is-ok", true);
        pass.innerHTML = pill("Validé · " + hms(simNow(m)).slice(0, 5), "ok") + '<small class="sx-host">Hôte prévenu sur son téléphone</small>';
      });
      /* Matrice : balayage d'une zone, la plus sensible ressort */
      $$("[data-acc-mx] span[data-z]", m.P).forEach(function (s) { s.classList.remove("is-scan"); });
      [0, 1, 2, 3, 4].forEach(function (z) {
        at(2000 + z * 900, function () {
          $$("[data-acc-mx] span[data-z]", m.P).forEach(function (s) { tog(s, "is-scan", +s.getAttribute("data-z") === z); });
        });
      });
      at(6600, function () { $$("[data-acc-mx] span[data-z]", m.P).forEach(function (s) { tog(s, "is-scan", s.getAttribute("data-z") === "3"); }); });
    },
    cross: function (n) {
      var m = this;
      m.line.classList.remove("is-hit"); void m.line.getBoundingClientRect(); m.line.classList.add("is-hit");
      $('[data-c="p"]', m.count).textContent = String(n);
      bump($('[data-c="p"]', m.count));
    },
    repeated: function () {
      var m = this, rep = $("[data-acc-rep]", m.P);
      if (!rep.hidden) return;
      rep.hidden = false;
      rep.innerHTML = '<p><b>Badge E-1187 · 3 refus en 4 min</b><small>Toit, salle des serveurs, toit · hors horaire</small></p>' +
        '<div class="sx-rep-b"><span>Suspendre la carte?</span><button type="button" data-rep="ok">Approuver</button><button type="button" data-rep="no">Ignorer</button></div>';
      var r = $('[data-r="rep"] b', m.P); r.textContent = "1"; bump(r.parentNode);
    },
    addRow: function (r, hot) {
      var m = this, li = el("li", "sx-ev is-" + r[0] + (hot ? " is-hot" : ""),
        '<span class="sx-ev-i">' + ico(r[1]) + "</span>" +
        '<span class="sx-ev-t"><b>' + r[3] + "</b><small>" + r[4] + " · " + r[5] + "</small></span>" +
        '<span class="sx-ev-r">' + pill(r[2], r[0]) + "<time>" + hms(simNow(m)) + "</time></span>");
      push(m.feed, li, 7);
      if (r[2] === "Accordé") { m.granted++; setK(m.P, "grant", num(m.granted)); }
      if (r[2] === "Refusé") { var d = $('[data-k="deny"]', m.P); d.textContent = String(+d.textContent + 1); bump(d); }
    },
    frame: function (t) {
      var m = this;
      var a = along(m.A, t, 500), b = along(m.B, t, 500);
      placeP(m.pa, a); placeP(m.pb, b);
      function bx(n, p, id, c) {
        if (!p || p.o < .3) { n.style.opacity = 0; return; }
        n.style.opacity = Math.min(1, p.o * 1.4).toFixed(2);
        setBox(n, boxAround(p, .44), null, c, id);
      }
      bx(m.ba, a, 31, 96); bx(m.bb, b, 32, 93);
    }
  };

  /* =====================================================================
     VÉHICULES — lecture de plaques (registre), suivi d'un véhicule d'une
     caméra à l'autre sur le plan du site (cônes qui s'allument, heure de
     passage à chaque caméra), vitesse excessive dans la cour, arrêt dans
     la voie pompiers, listes autorisées et surveillées.
     ===================================================================== */
  var VEH_CAMS = [ // nom, x, y, direction, ouverture, portée, décalage de l'étiquette
    ["LPR 01", 86, 300, 180, 54, 120, 0, -12],
    ["CAM 02", 236, 300, 0, 50, 165, 0, -12],
    ["CAM 03", 470, 298, 0, 50, 160, 0, -12],
    ["CAM 05", 872, 300, 180, 48, 200, 0, -12],
    ["CAM 06", 690, 386, -90, 110, 74, 0, 24],
    ["CAM 07", 274, 74, 135, 70, 130, 0, -10],
    ["CAM 08", 876, 84, 150, 64, 150, 0, -10],
    ["CAM 09", 336, 246, 200, 70, 70, -20, 18]
  ];
  var VEH_PATH = [[0, -40, 320], [1500, 20, 320], [3700, 20, 320], [4700, 118, 320], [6000, 330, 320], [7300, 560, 320], [8500, 722, 321], [9500, 768, 342], [10300, 772, 353]];
  var VEH_READS = [
    ["G47 KPL", "Autorisé · employé", "ok", "LPR 01 · entrée"],
    ["V82 3TR", "Livraison prévue · quai 4", "gold", "LPR 01 · entrée"],
    ["M15 9QD", "Autorisé · employé", "ok", "LPR 02 · sortie"],
    ["L03 7XA", "Visiteur attendu · P2", "gold", "LPR 01 · entrée"],
    ["Y29 1HC", "Inconnu · barrière fermée", "bad", "LPR 01 · entrée"],
    ["B71 6WS", "Autorisé · sous-traitant", "ok", "LPR 02 · sortie"],
    ["R58 2ZK", "Autorisé · employé", "ok", "LPR 01 · entrée"]
  ];
  var VEH_PLATE = "T66 4NB";

  MODS.vehicules = {
    site: "Campus Est · 8 caméras de cour · 2 lecteurs de plaques",
    clock: "17:05:58",
    len: 21000,
    final: 16500,
    build: function (P) {
      var m = this;
      P.innerHTML = head("Véhicules", "Lecture de plaques, suivi d’une caméra à l’autre, vitesse et stationnement sur tout le site.", [
        ["Lectures aujourd’hui", num(1942), "", "reads"],
        ["Taux de lecture", "99,1" + PC, "ok"],
        ["Sur le site", "128", "", "onsite"],
        ["Surveillés", "1", "warn"],
        ["Infractions", "2", "bad", "inf"]
      ]) +
      '<div class="sx-grid sx-veh">' +
        card("sx-plancard", "Plan du site · suivi du véhicule", '<span data-veh-trk>En attente</span>',
          '<div class="sx-planw" data-veh-plan></div>' +
          '<ol class="sx-pass" data-veh-pass aria-label="Passages devant les caméras"></ol>') +
        '<div class="sx-col">' +
          card("sx-lpr", "Lecture de plaque", "LPR 01 · barrière d’entrée",
            '<div class="sx-lpr-img" data-veh-img></div>' +
            '<div class="sx-ocr"><span class="sx-plate is-l"><small>QUÉBEC</small><b data-veh-ocr></b></span>' +
            '<dl class="sx-ocr-m"><div><dt>Confiance</dt><dd data-veh-conf>—</dd></div><div><dt>Lecture</dt><dd data-veh-ms>—</dd></div><div><dt>Liste</dt><dd data-veh-list>—</dd></div></dl></div>') +
          card("sx-vcard", "Fiche du véhicule", '<span data-veh-st>—</span>', '<div data-veh-fiche></div>') +
        "</div>" +
      "</div>" +
      '<div class="sx-grid sx-g2">' +
        card("", "Lectures récentes", '<i class="sx-live"></i>2 lecteurs', '<ol class="sx-feed sx-reads" data-veh-reads></ol>') +
        card("sx-lists", "Listes", "Mises à jour en continu",
          '<ul class="sx-lst">' +
          '<li class="is-ok"><b>412</b><span>Autorisés</span><small>Employés et sous-traitants · barrière ouverte</small></li>' +
          '<li class="is-gold"><b>9</b><span>Attendus aujourd’hui</span><small>Visiteurs et livraisons · accès pour la plage prévue</small></li>' +
          '<li class="is-warn"><b>3</b><span>Surveillés</span><small>Accès permis, suivi automatique sur le site</small></li>' +
          '<li class="is-bad"><b>1</b><span>Interdits</span><small>Barrière fermée, agent prévenu</small></li></ul>' +
          '<div class="sx-rules2"><p><span>Vitesse maximale dans la cour</span><b>15 km/h</b></p><p><span>Voie pompiers · arrêt toléré</span><b>2 min</b></p><p><span>Stationnement visiteurs · durée</span><b>4 h</b></p></div>') +
      "</div>";
      m.P = P;
      /* Plan + couches dynamiques */
      var plan = $("[data-veh-plan]", P);
      plan.innerHTML = campusSvg(function (g) {
        return '<g class="pl-cams">' + conesSvg(VEH_CAMS, g) + "</g>" +
          '<path class="pl-barrier" data-veh-bar d="M40 306V334"/>' +
          '<text class="pl-t is-z" x="771" y="333" text-anchor="middle">VOIE POMPIERS</text>' +
          '<path class="pl-trail" data-veh-trail d=""/>' +
          '<g class="pl-veh" data-veh-car><rect x="-11" y="-6" width="22" height="12" rx="3.5"/><path d="M5 -4.2h3.2v8.4H5z"/></g>';
      });
      m.svg = $("svg", plan);
      m.cams = $$(".pl-cam", m.svg);
      m.car = $("[data-veh-car]", m.svg);
      m.trail = $("[data-veh-trail]", m.svg);
      m.bar = $("[data-veh-bar]", m.svg);
      m.tag = el("div", "sx-vtag", "");
      plan.appendChild(m.tag);
      m.speed = el("div", "sx-speed", '<small>Vitesse estimée</small><b data-v>0</b><span>km/h</span><i><em data-vb></em></i><small class="sx-lim">Limite 15 km/h</small>');
      plan.appendChild(m.speed);
      m.stop = el("div", "sx-stop", "");
      plan.appendChild(m.stop);
      /* Photo de la lecture : la berline au stationnement */
      var cam = camTile({ img: MS + "security-enterprise-parking-v1.webp", view: [90, 400, 680, 382.5], num: "LPR 01", name: "Barrière", alt: "Berline noire vue de l’arrière par le lecteur de plaques", cls: "sx-wide sx-lprcam" });
      $("[data-veh-img]", P).appendChild(cam.el);
      m.cam = cam;
      m.bcar = box("vehicle"); m.bpl = box("vehicle");
      m.bpl.classList.add("is-under");
      m.bcar.classList.add("is-in", "is-right");
      cam.stage.appendChild(m.bcar); cam.stage.appendChild(m.bpl);
      setBox(m.bcar, [156, 446, 520, 214], "Véhicule", 97, 58);
      setBox(m.bpl, [166, 546, 48, 38], "Plaque", null, "");
      m.ocr = $("[data-veh-ocr]", P);
      m.reads = $("[data-veh-reads]", P);
      m.ri = 0; m.nreads = 1942;
      m.ts = $$("[data-sx-ts]", P);
    },
    onSecond: function (txt) { this.ts.forEach(function (n) { n.textContent = txt; }); },
    reset: function () {
      var m = this, P = m.P;
      m.cams.forEach(function (c) { c.classList.remove("is-on", "is-seen"); });
      m.seen = {}; m.pts = []; m.trail.setAttribute("d", "");
      m.bar.classList.remove("is-open");
      m.tag.className = "sx-vtag"; m.tag.innerHTML = "";
      m.speed.className = "sx-speed"; m.stop.className = "sx-stop"; m.stop.innerHTML = "";
      m.over = 0; m.stopAt = 0; m.flagged = false;
      $("[data-veh-pass]", P).innerHTML = "";
      $("[data-veh-trk]", P).textContent = "En attente";
      m.bcar.style.opacity = 0; m.bpl.style.opacity = 0;
      m.ocr.textContent = "— — —  — — —"; m.ocr.parentNode.className = "sx-plate is-l";
      $("[data-veh-conf]", P).textContent = "—"; $("[data-veh-ms]", P).textContent = "—"; $("[data-veh-list]", P).textContent = "—";
      $("[data-veh-st]", P).innerHTML = "—";
      $("[data-veh-fiche]", P).innerHTML = '<p class="sx-empty">Aucune lecture en cours. La fiche s’ouvre dès qu’une plaque est lue.</p>';
      at(1300, function () { m.bcar.style.opacity = 1; });
      at(1700, function () { m.bpl.style.opacity = 1; m.reading = 1; });
      at(3000, function () {
        m.reading = 0;
        m.ocr.textContent = VEH_PLATE; m.ocr.parentNode.classList.add("is-done");
        $("[data-veh-conf]", P).textContent = "98,6" + PC; $("[data-veh-ms]", P).textContent = "84 ms";
        $("[data-veh-list]", P).innerHTML = pill("Surveillé", "warn");
        m.bpl.querySelector(".lb-k").textContent = VEH_PLATE;
        m.bpl.querySelector(".lb-c").textContent = "98" + PC;
        $("[data-veh-st]", P).innerHTML = pill("Liste de surveillance", "warn");
        $("[data-veh-fiche]", P).innerHTML =
          '<div class="sx-vf">' + plate(VEH_PLATE) + '<div><b>Berline · noire</b><small>Reconnue par la forme et la couleur, en plus de la plaque</small></div></div>' +
          '<dl class="sx-vf-d"><div><dt>Motif de surveillance</dt><dd>Arrêts répétés dans la voie pompiers (2 et 5 novembre)</dd></div>' +
          "<div><dt>Passages · 30 jours</dt><dd>7</dd></div><div><dt>Dernière visite</dt><dd>5 novembre · 16 h 52</dd></div>" +
          "<div><dt>Décision</dt><dd>Accès permis · suivi automatique activé</dd></div></dl>";
        m.tag.innerHTML = plate(VEH_PLATE, true) + '<span class="sx-vtag-t">Surveillé</span>';
        m.tag.classList.add("is-on");
        $("[data-veh-trk]", P).textContent = "Suivi automatique";
        m.addRead([VEH_PLATE, "Liste de surveillance · suivi", "warn", "LPR 01 · entrée"], true);
      });
      at(3500, function () { m.bar.classList.add("is-open"); });
      at(4300, function () { m.speed.classList.add("is-on"); });
      at(10600, function () { m.speed.classList.remove("is-on"); });
      for (var k = 0; k < 6; k++) (function (k) {
        at(5200 + k * 2600, function () { m.addRead(VEH_READS[m.ri++ % VEH_READS.length]); });
      })(k);
    },
    addRead: function (r, hot) {
      var m = this;
      var li = el("li", "sx-ev is-" + r[2] + (hot ? " is-hot is-warnhot" : ""),
        plate(r[0], true) + '<span class="sx-ev-t"><b>' + r[1] + "</b><small>" + r[3] + "</small></span>" +
        '<span class="sx-ev-r">' + pill(r[2] === "ok" ? "Ouverte" : r[2] === "bad" ? "Fermée" : r[2] === "warn" ? "Suivi" : "Plage prévue", r[2]) + "<time>" + hms(simNow(m)) + "</time></span>");
      push(m.reads, li, 5);
      m.nreads++; setK(m.P, "reads", num(m.nreads));
    },
    frame: function (t, dt) {
      var m = this, P = m.P;
      /* Lecture : les caractères défilent puis se fixent un à un */
      if (m.reading) {
        var u = clamp((t - 1700) / 1300, 0, 1), fixed = Math.floor(u * 7), s = "", A = "ABCDEFGHJKLMNPRSTVWXYZ0123456789";
        for (var i = 0; i < 7; i++) s += i === 3 ? " " : i < fixed ? VEH_PLATE[i] : A[Math.floor(Math.random() * A.length)];
        m.ocr.textContent = s;
      }
      var p = along(VEH_PATH, t);
      if (!p) { m.car.style.opacity = 0; return; }
      m.car.style.opacity = 1;
      /* Cap et vitesse (dérivée sur le trajet) */
      var q = along(VEH_PATH, Math.max(0, t - 120)) || p;
      var dx = p.x - q.x, dy = p.y - q.y, v = Math.sqrt(dx * dx + dy * dy) / .12;
      if (dx * dx + dy * dy > .02) m.head = Math.atan2(dy, dx) * 180 / Math.PI;
      m.car.setAttribute("transform", "translate(" + p.x.toFixed(1) + " " + p.y.toFixed(1) + ") rotate(" + (m.head || 0).toFixed(1) + ")");
      m.tag.style.left = pct(clamp(p.x, 70, 930), 1000) + "%"; m.tag.style.top = pct(p.y, 600) + "%";
      var kmh = Math.round(v * .21);
      m.vs = m.vs == null ? kmh : m.vs + (kmh - m.vs) * Math.min(1, dt / 160);
      var shown = Math.round(m.vs);
      $("[data-v]", m.speed).textContent = shown;
      $("[data-vb]", m.speed).style.width = clamp(shown / 40 * 100, 0, 100) + "%";
      tog(m.speed, "is-bad", shown > 15);
      if (shown > 15 && t > 4700) m.over += dt;
      if (!m.flagged && m.over > 1100) {
        m.flagged = true;
        m.tag.classList.add("is-bad");
        m.tag.querySelector(".sx-vtag-t").textContent = "Vitesse " + shown + " km/h";
        m.addEvent("Vitesse excessive · " + shown + " km/h dans la cour", "bad");
        bump(setK(P, "inf", "3"));
      }
      /* Trace */
      if (!m.pts.length || Math.abs(m.pts[m.pts.length - 1][0] - p.x) + Math.abs(m.pts[m.pts.length - 1][1] - p.y) > 3) {
        if (p.x > 0) m.pts.push([p.x, p.y]);
        if (m.pts.length > 1) m.trail.setAttribute("d", "M" + m.pts.map(function (a) { return a[0].toFixed(1) + " " + a[1].toFixed(1); }).join("L"));
      }
      /* Cônes : allumés tant que le véhicule y est, puis « vus » */
      VEH_CAMS.forEach(function (c, i) {
        var inside = inCone(c, p.x, p.y);
        tog(m.cams[i], "is-on", inside);
        if (inside && !m.seen[i]) {
          m.seen[i] = 1;
          m.cams[i].classList.add("is-seen");
          var li = el("li", "", "<b>" + c[0] + "</b><time>" + hms(simNow(m)) + "</time>");
          var pass = $("[data-veh-pass]", P);
          if (pass.children.length) pass.appendChild(el("li", "sx-pass-a", '<i aria-hidden="true"></i>'));
          pass.appendChild(li);
        }
      });
      /* Arrêt dans la voie pompiers : minuterie accélérée (30 ×) */
      if (t >= 10300) {
        if (!m.stopAt) { m.stopAt = 10300; m.stop.classList.add("is-on"); m.tag.className = "sx-vtag is-on is-warn"; m.tag.querySelector(".sx-vtag-t").textContent = "À l’arrêt"; }
        var el2 = Math.min(300, (t - 10300) / 1000 * 30), mm = Math.floor(el2 / 60), ss = Math.floor(el2 % 60);
        m.stop.style.left = pct(p.x, 1000) + "%"; m.stop.style.top = pct(p.y, 600) + "%";
        m.stop.innerHTML = "<small>Voie pompiers</small><b>" + mm + ":" + pad(ss) + "</b><i><em style=\"width:" + (el2 / 3).toFixed(1) + '%"></em></i>';
        if (el2 >= 120 && !m.stopFlag) {
          m.stopFlag = true; m.stop.classList.add("is-bad");
          m.addEvent("Arrêt interdit · voie pompiers depuis 2 min", "bad");
        }
        if (el2 >= 180 && !m.agent) {
          m.agent = true;
          m.addEvent("Agent de cour prévenu · accusé de réception reçu", "ok");
        }
      } else { m.stopFlag = false; m.agent = false; }
    },
    addEvent: function (txt, tone) {
      var pass = $("[data-veh-pass]", this.P);
      pass.appendChild(el("li", "sx-pass-e is-" + tone, "<span>" + txt + "</span><time>" + hms(simNow(this)) + "</time>"));
    }
  };

  /* =====================================================================
     PERSONNES — recherche par attributs dans les enregistrements
     (« personne en veste rouge entrée après 22 h »), identification des
     personnes INSCRITES avec consentement seulement; une personne non
     inscrite est signalée sans nom; chaque consultation est journalisée.
     ===================================================================== */
  var PER_Q = "Personne en veste rouge entrée après 22 h";
  var PER_TH = [ // photo, cadrage, silhouette (x, y, h), tenue, caméra, lieu, heure, score
    ["delivery", [1130, 220, 416, 260], 1300, 505, 250, "rouge", "CAM 21", "Porte de service B", "22:14:08", 94],
    ["parking", [200, 262, 300, 187.5], 330, 382, 112, "rouge", "CAM 07", "Barrière P1", "22:16:41", 91],
    ["parking", [1104, 244, 288, 180], 1240, 357, 98, "rouge", "CAM 12", "Bâtiment A · entrée", "22:19:55", 88],
    ["delivery", [1000, 246, 480, 300], 1215, 548, 292, "rouge", "CAM 22", "Quai de livraison", "22:31:12", 86],
    ["parking", [560, 430, 448, 280], 790, 650, 230, "bordeaux", "CAM 05", "Stationnement P1", "22:41:30", 72],
    ["delivery", [330, 330, 520, 325], 540, 640, 318, "brique", "CAM 20", "Entrée piétonne", "22:47:03", 61]
  ];
  var PER_FEED = [
    ["Émilie Fortin", "Employée · Finances", "Hall · tourniquet 2", 98, "14 mars 2026"],
    ["Karim Haddad", "Équipe TI", "Salle des serveurs · sas", 99, "9 janvier 2026"],
    [null, "P-2291", "Quai 3 · entrepôt"],
    ["Olivier Roy", "Sous-traitant · CVC", "Toit · accès technique", 96, "2 octobre 2026"],
    ["Nadia Bouchard", "Entretien", "Bâtiment C · atelier", 97, "21 mai 2026"],
    [null, "P-2292", "Hall · accueil"],
    ["Thomas Bergeron", "Employé · Logistique", "Entrepôt · quai 2", 98, "27 février 2026"]
  ];
  function hash4(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(16).slice(0, 4); }

  MODS.personnes = {
    site: "Campus Est · 14 caméras · 252 personnes inscrites",
    clock: "14:02:06",
    len: 22000,
    build: function (P) {
      var m = this;
      P.innerHTML = head("Personnes", "Retrouver une personne par son apparence; identifier seulement celles qui y ont consenti.", [
        ["Inscrites · consentement", "252", "ok"],
        ["Présentes sur le site", "187", "", "here"],
        ["Non inscrites signalées", "4", "warn", "unk"],
        ["Consultations journalisées", "12", "gold", "views"]
      ]) +
      card("sx-searchc", "Recherche dans les enregistrements", "Par attributs · sans reconnaissance faciale",
        '<div class="sx-q"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 3.5 3.5"/></svg><span data-per-q></span><i class="sx-caret" aria-hidden="true"></i>' +
        '<button type="button" class="sx-btn is-main" data-per-go>Rechercher</button></div>' +
        '<div class="sx-chips" data-per-chips></div>' +
        '<div class="sx-scan" data-per-scan><div class="sx-scan-bar"><em data-per-bar></em></div><span data-per-scant></span></div>' +
        '<div class="sx-res" data-per-res></div>' +
        '<div class="sx-trk" data-per-trk></div>') +
      '<div class="sx-grid sx-g2 sx-per2">' +
        card("sx-recog", "Identification · personnes inscrites", '<i class="sx-live"></i>En direct', '<ol class="sx-feed sx-idf" data-per-feed></ol>') +
        card("sx-journal", "Journal des consultations", "Inaltérable · chaîné",
          '<ol class="sx-jr" data-per-jr></ol><p class="sx-note">Chaque ouverture d’une fiche ou d’une image d’identification exige un motif et laisse une trace : qui, quoi, quand, pourquoi.</p>') +
      "</div>";
      m.P = P;
      m.qEl = $("[data-per-q]", P);
      m.feed = $("[data-per-feed]", P);
      m.jr = $("[data-per-jr]", P);
      m.fi = 0; m.views = 12;
      /* Vignettes de résultats (construites une fois, révélées à chaque boucle) */
      var res = $("[data-per-res]", P);
      m.th = PER_TH.map(function (r, i) {
        var f = el("figure", "sx-th", "");
        var v = el("div", "sx-thv", '<div class="sec-stage" style="' + stageCss(r[1]) + '"><img src="' + MS + "security-enterprise-" + r[0] + '-v1.webp" alt="" loading="lazy" decoding="async"></div>');
        var st = $(".sec-stage", v), p = person(r[5]);
        st.appendChild(p);
        placeP(p, { x: r[2], y: r[3], h: r[4], o: 1, mv: false, left: i % 2 === 1 });
        var b = box(r[9] >= 85 ? "person" : "known");
        st.appendChild(b);
        setBox(b, boxAround({ x: r[2], y: r[3], h: r[4] }, .46, r[4] * .03), "", r[9], "");
        b.classList.add("is-in");
        f.appendChild(v);
        f.appendChild(el("figcaption", "", "<b>" + r[6] + "</b><span>" + r[7] + "</span><time>" + r[8] + "</time>"));
        res.appendChild(f);
        return f;
      });
      /* Voir une fiche : motif obligatoire, puis consultation journalisée */
      P.addEventListener("click", function (e) {
        var t = e.target.closest && e.target.closest("button");
        if (!t || !P.contains(t)) return;
        var li = t.closest(".sx-ev");
        if (t.hasAttribute("data-per-view")) {
          $$(".sx-why", P).forEach(function (n) { n.parentNode.removeChild(n); });
          var w = el("div", "sx-why", "<span>Motif de la consultation (obligatoire)</span>" +
            '<button type="button" class="sx-btn" data-per-why="Enquête INC-2026-1108-014">Enquête en cours</button>' +
            '<button type="button" class="sx-btn" data-per-why="Vérification d’accès">Vérification d’accès</button>' +
            '<button type="button" class="sx-btn" data-per-why="">Annuler</button>');
          li.appendChild(w);
        } else if (t.hasAttribute("data-per-why")) {
          var why = t.getAttribute("data-per-why"), wbox = t.parentNode;
          wbox.parentNode.removeChild(wbox);
          if (!why) return;
          li.classList.add("is-open");
          var who = li.getAttribute("data-who");
          m.log("Vous · démo", who, why, true);
        } else if (t.hasAttribute("data-per-go")) {
          restart(m); if (!motion()) finish(m);
        }
      });
      m.ts = [];
    },
    log: function (who, what, why, mine) {
      var m = this, tm = hms(simNow(m)), prev = m.jr.firstChild ? m.jr.firstChild.getAttribute("data-h") : "9f2c";
      var h = hash4(prev + who + what + why + tm);
      var li = el("li", mine ? "is-mine" : "", "<time>" + tm + '</time><span><span class="sx-jr-s"><b>' + who + "</b> a consulté <em>" + what + "</em></span><small>Motif : " + why + "</small></span>" +
        '<code title="Empreinte chaînée">' + prev + " → " + h + "</code>");
      li.setAttribute("data-h", h);
      push(m.jr, li, 5);
      m.views++; bump(setK(m.P, "views", String(m.views)));
    },
    addId: function (r) {
      var m = this, li;
      if (r[0]) {
        li = el("li", "sx-ev is-ok", '<span class="sx-av">' + initials(r[0]) + "</span>" +
          '<span class="sx-ev-t"><b>' + r[0] + "</b><small>" + r[1] + " · " + r[2] + "</small><small class=\"sx-cons\">Consentement signé · " + r[4] + "</small></span>" +
          '<span class="sx-ev-r">' + pill("Inscrite · " + r[3] + PC, "ok") + '<button type="button" class="sx-mini" data-per-view>Voir</button></span>');
        li.setAttribute("data-who", (/^[AEIOUÉÈÊ]/.test(r[0]) ? "la fiche d’" : "la fiche de ") + r[0]);
      } else {
        li = el("li", "sx-ev is-warn", '<span class="sx-av is-unk">?</span>' +
          '<span class="sx-ev-t"><b>Personne non inscrite</b><small>ID temporaire ' + r[1] + " · " + r[2] + "</small><small class=\"sx-cons\">Aucun nom, aucune recherche d’identité · effacé dans 72 h</small></span>" +
          '<span class="sx-ev-r">' + pill("Signalée", "warn") + '<button type="button" class="sx-mini" data-per-view>Voir</button></span>');
        li.setAttribute("data-who", "l’image de " + r[1]);
        var u = $('[data-k="unk"]', m.P); u.textContent = String(+u.textContent + 1); bump(u);
      }
      push(m.feed, li, 5);
    },
    reset: function () {
      var m = this, P = m.P;
      m.qEl.textContent = "";
      $("[data-per-chips]", P).innerHTML = "";
      var scan = $("[data-per-scan]", P); scan.className = "sx-scan";
      $("[data-per-bar]", P).style.width = "0%";
      $("[data-per-scant]", P).textContent = "";
      m.th.forEach(function (f) { f.className = "sx-th"; });
      var trk = $("[data-per-trk]", P); trk.className = "sx-trk"; trk.innerHTML = "";
      m.typing = true;
      at(2300, function () {
        m.typing = false; m.qEl.textContent = PER_Q;
        var chips = $("[data-per-chips]", P);
        ["Haut · rouge", "Vêtement · veste", "Après 22 h · hier", "Bâtiment A et cour", "14 caméras"].forEach(function (c, i) {
          setTimeout(function () { chips.appendChild(el("span", "sx-chip", c)); }, motion() ? i * 110 : 0);
        });
      });
      at(3000, function () { scan.classList.add("is-on"); m.scanning = true; });
      at(6200, function () {
        m.scanning = false;
        $("[data-per-bar]", P).style.width = "100%";
        $("[data-per-scant]", P).innerHTML = "<b>412 h</b> de vidéo · <b>38" + NN + "412</b> personnes détectées · <b>6 correspondances</b> · 2,9 s";
        scan.classList.add("is-done");
      });
      m.th.forEach(function (f, i) { at(6400 + i * 260, function () { f.classList.add("is-on"); }); });
      at(8600, function () {
        m.th.forEach(function (f, i) { tog(f, "is-link", PER_TH[i][9] >= 85); tog(f, "is-low", PER_TH[i][9] < 85); });
        trk.innerHTML = '<p><b>Même personne probable · 4 caméras</b><small>Ressemblance d’apparence (tenue, silhouette, démarche), pas de reconnaissance du visage</small></p>' +
          '<ol>' + PER_TH.slice(0, 4).map(function (r) { return "<li><b>" + r[6] + "</b><span>" + r[7] + "</span><time>" + r[8].slice(0, 5) + "</time></li>"; }).join("") + "</ol>" +
          '<p class="sx-trk-d">Entrée par la barrière P1 à 22 h 16, sortie par le quai de livraison à 22 h 31 · 15 min sur le site</p>';
        trk.classList.add("is-on");
      });
      /* Identification en direct */
      for (var k = 0; k < 6; k++) (function (k) {
        at(500 + k * 3300, function () { m.addId(PER_FEED[m.fi++ % PER_FEED.length]); });
      })(k);
      at(10500, function () { m.log("Sophie Morin · sécurité", "l’image de P-2291", "Vérification d’accès"); });
      if (!m.jr.children.length) {
        m.log("Karim Haddad · TI", "la fiche d’Olivier Roy", "Permis de travail · toit");
        m.views = 12; setK(m.P, "views", "12");
      }
    },
    frame: function (t) {
      var m = this;
      if (m.typing) {
        var n = Math.floor(clamp((t - 200) / 1900, 0, 1) * PER_Q.length);
        if (m.qEl.textContent.length !== n) m.qEl.textContent = PER_Q.slice(0, n);
      }
      if (m.scanning) {
        var u = clamp((t - 3000) / 3200, 0, 1);
        $("[data-per-bar]", m.P).style.width = (u * 100).toFixed(1) + "%";
        var cams = ["CAM 02 · Hall", "CAM 05 · P1", "CAM 07 · Barrière P1", "CAM 12 · Bâtiment A", "CAM 20 · Entrée piétonne", "CAM 21 · Porte B", "CAM 22 · Quai"];
        $("[data-per-scant]", m.P).innerHTML = "Analyse de <b>" + cams[Math.floor(u * 6.99)] + "</b> · " + Math.round(u * 412) + " h sur 412 · " + num(Math.round(u * 38412)) + " personnes";
      }
    }
  };

  /* =====================================================================
     ZONES ET RÈGLES — périmètres virtuels sur le plan de l'entrepôt :
     intrusion, flânage, objet abandonné, foule, chute, porte maintenue
     ouverte, franchissement à contre-sens. Carte de chaleur à la demande.
     ===================================================================== */
  function polyLen(pts) { var L = 0; for (var i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; }
  function loopAt(pts, s) { // position à la distance s sur une boucle fermée
    var L = polyLen(pts); s = ((s % L) + L) % L;
    for (var i = 1; i < pts.length; i++) {
      var a = pts[i - 1], b = pts[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]);
      if (s <= d) return [a[0] + (b[0] - a[0]) * s / d, a[1] + (b[1] - a[1]) * s / d];
      s -= d;
    }
    return pts[pts.length - 1];
  }
  var ZN_RACKS = [0, 1, 2, 3, 4, 5, 6].map(function (i) { return 150 + i * 96; });
  var ZN_LOOPS = [ // circuits de fond (personnes et chariots)
    { pts: [[80, 160], [920, 160], [920, 410], [80, 410], [80, 160]], v: 34, n: 3, k: "p" },
    { pts: [[60, 100], [940, 100], [940, 120], [60, 120], [60, 100]], v: 70, n: 2, k: "f" },
    { pts: [[226, 170], [226, 400], [322, 400], [322, 170], [226, 170]], v: 26, n: 2, k: "p" },
    { pts: [[418, 170], [418, 400], [610, 400], [610, 170], [418, 170]], v: 22, n: 2, k: "p" },
    { pts: [[100, 470], [260, 470], [260, 500], [100, 500], [100, 470]], v: 14, n: 1, k: "p" }
  ];
  var ZN_RULES = [
    ["intr", "Intrusion · salle électrique", "En tout temps", 0],
    ["loit", "Flânage", "Plus de 90 s", 1],
    ["aban", "Objet abandonné", "Plus de 2 min", 0],
    ["crowd", "Foule", "Plus de 12 personnes", 0],
    ["fall", "Chute", "Immobile 20 s", 0],
    ["door", "Porte maintenue ouverte", "Plus de 30 s", 2],
    ["line", "Contre-sens", "Allée 4 · sens unique", 0]
  ];

  MODS.zones = {
    site: "Entrepôt · bâtiment B · 11 caméras · 7 règles",
    clock: "15:41:20",
    len: 26000,
    final: 24000,
    build: function (P) {
      var m = this;
      var racks = ZN_RACKS.map(function (x, i) {
        return '<rect class="zn-rack" x="' + (x - 13) + '" y="180" width="26" height="220" rx="2"/>' +
          '<text class="pl-t" x="' + (x + 48) + '" y="425" text-anchor="middle">' + (i < 6 ? "ALLÉE " + (i + 1) : "") + "</text>";
      }).join("");
      var docks = [0, 1, 2, 3, 4, 5].map(function (i) {
        var x = 120 + i * 140;
        return '<rect class="pl-dock" x="' + (x - 26) + '" y="26" width="52" height="8"/><text class="pl-t" x="' + x + '" y="20" text-anchor="middle">QUAI ' + (i + 1) + "</text>";
      }).join("");
      var svg = '<svg class="sx-plan sx-zplan" viewBox="0 0 1000 560" role="img" aria-label="Plan de l’entrepôt avec zones virtuelles (exemple)">' +
        '<defs><pattern id="znG" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" class="pl-grid"/></pattern></defs>' +
        '<rect width="1000" height="560" class="pl-bg"/><rect width="1000" height="560" fill="url(#znG)"/>' +
        '<path class="zn-wall" d="M30 30H970V286M970 318V530H30V30"/>' + docks + racks +
        '<rect class="pl-bld" x="40" y="440" width="250" height="84"/><text class="pl-t" x="165" y="455" text-anchor="middle">BUREAUX DU QUAI</text>' +
        '<rect class="pl-bld" x="760" y="420" width="204" height="104"/>' +
        /* zones virtuelles */
        '<g class="zn-z is-aban" data-z="aban"><rect x="52" y="44" width="896" height="96" rx="6"/><text x="64" y="134">ZONE DE TRANSIT · OBJET ABANDONNÉ</text></g>' +
        '<g class="zn-z is-crowd" data-z="crowd"><rect x="330" y="46" width="140" height="90" rx="6"/></g>' +
        '<g class="zn-z is-intr" data-z="intr"><rect x="752" y="412" width="212" height="112" rx="4"/><text x="858" y="470" text-anchor="middle">SALLE ÉLECTRIQUE</text><text x="858" y="484" text-anchor="middle" class="zn-sub">ZONE INTERDITE</text></g>' +
        '<g class="zn-z is-loit" data-z="loit"><circle cx="712" cy="420" r="34"/></g>' +
        '<g class="zn-z is-door" data-z="door"><rect x="930" y="270" width="40" height="64" rx="4"/><path class="zn-door" d="M970 286V318"/><text x="922" y="262" text-anchor="end">SORTIE D’URGENCE</text></g>' +
        '<g class="zn-z is-line" data-z="line"><path d="M432 300H500"/><path class="zn-arr" d="M466 286v-12m0 0-5 6m5-6 5 6"/><text x="466" y="318" text-anchor="middle">SENS UNIQUE</text></g>' +
        '<g data-zn-dyn></g>' +
        '<text class="pl-t is-n" x="962" y="550" text-anchor="end">ENTREPÔT · NIVEAU 1</text></svg>';
      P.innerHTML = head("Zones et règles", "Des périmètres virtuels sur le plan, et des règles qui décident quand une situation mérite une alerte.", [
        ["Zones actives", "6", "ok"],
        ["Règles", "7"],
        ["Alertes aujourd’hui", "9", "", "al"],
        ["Fausses alertes · 30 j", "1,8" + PC, "ok"]
      ]) +
      '<div class="sx-grid sx-zn">' +
        '<div class="sx-col">' +
          card("sx-zcard", "Plan de l’entrepôt · détection en direct",
            '<button type="button" class="sx-sw" data-zn-heat aria-pressed="false"><i aria-hidden="true"></i>Carte de chaleur</button>',
            '<div class="sx-planw sx-zw">' + svg + '<canvas class="sx-heat" data-zn-cv width="100" height="56" aria-hidden="true"></canvas><div class="sx-zpins" data-zn-pins></div></div>' +
            '<div class="sx-zleg"><span class="is-p">Personne</span><span class="is-f">Chariot élévateur</span><span class="is-a">Alerte</span><span class="sx-hl">Fréquentation depuis 6 h</span></div>') +
          card("sx-alc", "Alertes", '<i class="sx-live"></i>En direct', '<ol class="sx-feed" data-zn-feed></ol>') +
        "</div>" +
        '<div class="sx-col">' +
          card("sx-rulec", "Règles", "Activez ou coupez",
            '<ul class="sx-rlz">' + ZN_RULES.map(function (r) {
              return '<li data-rule="' + r[0] + '"><button type="button" class="sx-tg" role="switch" aria-checked="true" aria-label="' + r[1] + '"><i></i></button>' +
                "<span><b>" + r[1] + "</b><small>" + r[2] + "</small></span><em>" + r[3] + "</em></li>";
            }).join("") + "</ul>") +
          card("sx-builder", "Créer une règle", "En une phrase",
            '<p class="sx-sent2">Si <span class="sx-tk">une personne</span> entre dans <span class="sx-tk">la salle électrique</span> entre <span class="sx-tk">22 h et 6 h</span>, alors <span class="sx-tk is-a">prévenir l’agent de garde</span>, <span class="sx-tk is-a">allumer le secteur</span> et <span class="sx-tk is-a">garder l’extrait de 30 s</span>.</p>' +
            '<p class="sx-note">Chaque règle se teste d’abord sur les 7 derniers jours d’enregistrements : JARVIS indique combien d’alertes elle aurait produites avant de l’activer.</p>') +
        "</div>" +
      "</div>";
      m.P = P;
      m.dyn = $("[data-zn-dyn]", P);
      m.pins = $("[data-zn-pins]", P);
      m.feed = $("[data-zn-feed]", P);
      m.cv = $("[data-zn-cv]", P);
      m.ctx = m.cv.getContext && m.cv.getContext("2d");
      m.heatOn = false;
      m.grid = new Float32Array(100 * 56);
      m.on = {}; ZN_RULES.forEach(function (r) { m.on[r[0]] = true; });
      /* Base de la carte de chaleur : fréquentation de la journée (circuits) */
      ZN_LOOPS.forEach(function (L) {
        var len = polyLen(L.pts);
        for (var s = 0; s < len; s += 3) { var p = loopAt(L.pts, s); m.heatAdd(p[0], p[1], L.k === "f" ? .5 : 1.2); }
      });
      for (var c = 0; c < 400; c++) m.heatAdd(400 + Math.random() * 30 - 15 + 0, 92 + Math.random() * 30 - 15, 1.4);
      for (var d = 0; d < 260; d++) m.heatAdd(120 + Math.random() * 760, 100 + Math.random() * 30 - 15, .8);
      /* Points de fond */
      m.bg = [];
      ZN_LOOPS.forEach(function (L, li) {
        for (var i = 0; i < L.n; i++) m.bg.push({ L: L, s0: i * polyLen(L.pts) / L.n + li * 37, k: L.k, n: m.dot(L.k) });
      });
      P.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("button");
        if (!b || !P.contains(b)) return;
        if (b.hasAttribute("data-zn-heat")) {
          m.heatOn = !m.heatOn;
          b.setAttribute("aria-pressed", m.heatOn ? "true" : "false");
          tog(P.querySelector(".sx-zw"), "is-heat", m.heatOn);
          m.paint();
        } else if (b.classList.contains("sx-tg")) {
          var li = b.closest("li"), k = li.getAttribute("data-rule"), on = b.getAttribute("aria-checked") !== "true";
          b.setAttribute("aria-checked", on ? "true" : "false");
          m.on[k] = on;
          tog(li, "is-off", !on);
          var z = $('[data-z="' + k + '"]', P); if (z) tog(z, "is-off", !on);
        } else if (b.hasAttribute("data-zn-call")) {
          b.parentNode.innerHTML = '<span class="sx-sent">Appel lancé vers le secouriste du quai…</span>';
          soon(1400, function () { var n = $("[data-zn-callst]", P); if (n) n.innerHTML = '<span class="sx-okk">' + CHECK + "Confirmé · le secouriste se rend à l’allée 6</span>"; });
        }
      });
    },
    dot: function (k, id) {
      var g = sv("g", { "class": "zn-dot is-" + k }, this.dyn);
      if (k === "f") sv("rect", { x: -9, y: -6, width: 18, height: 12, rx: 2.5 }, g);
      else { sv("circle", { r: 12, "class": "zn-halo" }, g); sv("circle", { r: 5.6 }, g); }
      if (id) { var t = sv("text", { x: 9, y: -9, "class": "zn-id" }, g); t.textContent = id; }
      return g;
    },
    heatAdd: function (x, y, w) {
      var gx = Math.round(x / 10), gy = Math.round(y / 10);
      for (var dy = -2; dy <= 2; dy++) for (var dx = -2; dx <= 2; dx++) {
        var X = gx + dx, Y = gy + dy;
        if (X < 0 || Y < 0 || X >= 100 || Y >= 56) continue;
        this.grid[Y * 100 + X] += w * Math.exp(-(dx * dx + dy * dy) / 2.2);
      }
    },
    paint: function () {
      var m = this;
      if (!m.ctx || !m.heatOn) return;
      var g = m.grid, mx = 0, i;
      for (i = 0; i < g.length; i++) if (g[i] > mx) mx = g[i];
      var img = m.ctx.createImageData(100, 56), d = img.data;
      for (i = 0; i < g.length; i++) {
        var u = Math.pow(g[i] / (mx || 1), .4);
        // rampe : bronze sombre → or → blanc chaud
        var r = u < .5 ? 120 + 270 * u : 255, gg = u < .5 ? 70 + 200 * u : 170 + 160 * (u - .5), b = u < .7 ? 30 + 40 * u : 58 + 500 * (u - .7);
        d[i * 4] = Math.min(255, r); d[i * 4 + 1] = Math.min(255, gg); d[i * 4 + 2] = Math.min(255, b);
        d[i * 4 + 3] = u < .05 ? 0 : Math.min(240, 30 + u * 270);
      }
      m.ctx.putImageData(img, 0, 0);
    },
    alert: function (k, title, sub, tone, extra) {
      var m = this;
      if (!m.on[k]) return false;
      var z = $('[data-z="' + k + '"]', m.P);
      if (z) { z.classList.remove("is-fire"); void z.getBoundingClientRect(); z.classList.add("is-fire"); }
      var li = $('[data-rule="' + k + '"]', m.P);
      if (li) { var em = li.querySelector("em"); em.textContent = String(+em.textContent + 1); li.classList.remove("is-hit"); void li.offsetWidth; li.classList.add("is-hit"); }
      var row = el("li", "sx-ev is-" + (tone || "bad") + (tone === "warn" ? " is-warnhot" : tone === "ok" ? "" : " is-hot"),
        '<span class="sx-ev-i">' + ico(tone === "warn" ? "alert" : "urg") + '</span><span class="sx-ev-t"><b>' + title + "</b><small>" + sub + "</small></span>" +
        '<span class="sx-ev-r"><time>' + hms(simNow(m)) + "</time></span>" + (extra || ""));
      push(m.feed, row, 4);
      var a = $('[data-k="al"]', m.P); a.textContent = String(+a.textContent + 1); bump(a);
      return true;
    },
    pin: function (x, y, cls, html) {
      var n = el("div", "sx-zpin " + (cls || ""), html);
      n.style.left = pct(x, 1000) + "%"; n.style.top = pct(y, 560) + "%";
      this.pins.appendChild(n);
      return n;
    },
    reset: function () {
      var m = this;
      $$(".zn-dot.is-s", m.dyn).forEach(function (n) { n.parentNode.removeChild(n); });
      m.pins.innerHTML = "";
      $$(".zn-z", m.P).forEach(function (z) { z.classList.remove("is-fire", "is-open"); });
      /* Acteurs scriptés : [t, x, y] */
      m.S = [
        { id: "47", k: [[0, 300, 160], [1500, 520, 108], [2300, 520, 108], [4000, 760, 160], [5200, 930, 160]] },               // dépose un colis
        { id: "52", k: [[2600, 610, 160], [4200, 712, 380], [5200, 790, 450], [7600, 830, 470], [8800, 712, 400], [10500, 610, 160]] }, // entre en salle électrique
        { id: "38", k: [[1000, 520, 410], [2400, 700, 412], [11800, 718, 424], [13600, 520, 410]] },                          // flâne
        { id: "61", k: [[11500, 650, 170], [12800, 706, 280], [14200, 706, 320], [25600, 706, 320]] },                                           // chute
        { id: "29", k: [[17000, 470, 180], [18800, 466, 330], [19800, 466, 400]] }                                            // contre-sens
      ];
      m.S.forEach(function (a) { a.n = m.dot("p is-s", a.id); a.n.style.opacity = 0; });
      m.crowd = [];
      for (var i = 0; i < 13; i++) {
        var a0 = i / 13 * Math.PI * 2, r0 = 160 + (i % 3) * 40;
        m.crowd.push({ from: [400 + Math.cos(a0) * r0, 250 + Math.sin(a0) * r0 * .6], to: [400 + Math.cos(a0 * 1.7) * (14 + i % 4 * 9), 92 + Math.sin(a0 * 2.3) * (10 + i % 3 * 7)], n: m.dot("p is-s") });
      }
      m.obj = null; m.objT = 0; m.loitT = 0; m.flag = {}; m.doorT = 0;
      m.loitPin = m.fpin = m.doorPin = m.cpin = null;
      at(2300, function () {
        m.obj = m.pin(520, 108, "sx-obj", '<i></i><span class="sx-ring"><svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="15"/><circle class="r" cx="18" cy="18" r="15" pathLength="100"/></svg></span><b>Colis</b>');
        m.objT = 2300;
      });
      at(16200, function () { $('[data-z="door"]', m.P).classList.add("is-open"); m.doorT = 16200; m.doorPin = m.pin(950, 302, "sx-dpin", "<b>0 s</b>"); });
      at(22400, function () { $('[data-z="door"]', m.P).classList.remove("is-open"); if (m.doorPin) m.doorPin.classList.add("is-off"); });
    },
    frame: function (t, dt) {
      var m = this, i;
      /* Fond : circuits */
      m.bg.forEach(function (b) {
        var p = loopAt(b.L.pts, b.s0 + t / 1000 * b.L.v);
        var q = loopAt(b.L.pts, b.s0 + t / 1000 * b.L.v - 2);
        b.n.setAttribute("transform", "translate(" + p[0].toFixed(1) + " " + p[1].toFixed(1) + ")" + (b.k === "f" ? " rotate(" + (Math.atan2(p[1] - q[1], p[0] - q[0]) * 180 / Math.PI).toFixed(0) + ")" : ""));
        if (dt && (t % 400) < dt) m.heatAdd(p[0], p[1], .15);
      });
      /* Acteurs scriptés */
      m.S.forEach(function (a) {
        var p = along(a.k, t, 400);
        if (!p) { a.n.style.opacity = 0; return; }
        a.n.style.opacity = p.o.toFixed(2);
        a.n.setAttribute("transform", "translate(" + p.x.toFixed(1) + " " + p.y.toFixed(1) + ")");
        a.p = p;
      });
      /* Objet abandonné : minuterie accélérée (30 ×) */
      if (m.obj) {
        var el2 = (t - m.objT) / 1000 * 30, ring = $(".r", m.obj);
        ring.style.strokeDashoffset = (100 - clamp(el2 / 120, 0, 1) * 100).toFixed(1);
        m.obj.querySelector("b").textContent = el2 < 120 ? "Colis · " + Math.floor(el2 / 60) + ":" + pad(Math.floor(el2 % 60)) : "Abandonné";
        if (el2 >= 120 && !m.flag.aban) { m.flag.aban = 1; m.obj.classList.add("is-bad"); m.alert("aban", "Objet abandonné · zone de transit", "Colis laissé par ID 47 · 2 min sans surveillance", "bad"); }
        if (t > 21000 && !m.flag.pick) { m.flag.pick = 1; m.obj.classList.add("is-off"); }
      }
      /* Intrusion */
      var a1 = m.S[1].p;
      if (a1 && t > 2600 && a1.x > 752 && a1.y > 412 && !m.flag.intr) {
        m.flag.intr = 1;
        tog(m.S[1].n, "is-alert", true);
        m.alert("intr", "Intrusion · salle électrique", "ID 52 · zone interdite · extrait conservé", "bad");
      }
      /* Flânage : minuterie accélérée (10 ×) */
      var a2 = m.S[2].p;
      if (a2 && Math.hypot(a2.x - 712, a2.y - 420) < 34) {
        m.loitT += dt * 10;
        if (!m.loitPin) m.loitPin = m.pin(712, 420, "sx-lpin", "<b></b>");
        m.loitPin.querySelector("b").textContent = Math.floor(m.loitT / 1000) + " s";
        if (m.loitT >= 90000 && !m.flag.loit) { m.flag.loit = 1; m.loitPin.classList.add("is-bad"); m.alert("loit", "Flânage · près de la salle électrique", "ID 38 · 90 s au même endroit", "warn"); }
      } else if (m.loitPin && t > 12000) { m.loitPin.classList.add("is-off"); }
      /* Foule au quai 3 */
      var cu = smooth((t - 7600) / 2600) * (1 - smooth((t - 14200) / 2400));
      m.crowd.forEach(function (c) {
        c.n.style.opacity = cu > .02 ? Math.min(1, cu * 3).toFixed(2) : 0;
        var x = lerp(c.from[0], c.to[0], cu), y = lerp(c.from[1], c.to[1], cu);
        c.n.setAttribute("transform", "translate(" + x.toFixed(1) + " " + y.toFixed(1) + ")");
        if (cu > .2 && dt && (t % 300) < dt) m.heatAdd(x, y, .4);
      });
      if (cu > .96 && !m.flag.crowd) { m.flag.crowd = 1; m.cpin = m.pin(400, 92, "sx-cpin", "<b>13 personnes</b>"); m.alert("crowd", "Foule · quai 3", "13 personnes · seuil 12 · réception d’un arrivage?", "warn"); }
      if (m.cpin && cu < .5) { m.cpin.classList.add("is-off"); }
      /* Chute */
      if (t > 14200 && !m.flag.fall0) { m.flag.fall0 = 1; m.fpin = m.pin(706, 320, "sx-fpin", "<b>Immobile</b>"); tog(m.S[3].n, "is-alert", true); }
      if (m.fpin && !m.flag.fall) {
        var im = Math.floor((t - 14200) / 1000 * 8);
        m.fpin.querySelector("b").textContent = "Immobile · " + Math.min(20, im) + " s";
        if (im >= 20) {
          m.flag.fall = 1; m.fpin.classList.add("is-bad");
          m.alert("fall", "Chute probable · allée 6", "ID 61 au sol, immobile depuis 20 s", "bad",
            '<span class="sx-ev-x" data-zn-callst><button type="button" class="sx-btn is-main" data-zn-call>Appeler le secouriste</button></span>');
        }
      }
      /* Porte maintenue ouverte : minuterie accélérée (6 ×) */
      if (m.doorT && m.doorPin && !m.doorPin.classList.contains("is-off")) {
        var ds = Math.floor((t - m.doorT) / 1000 * 6);
        m.doorPin.querySelector("b").textContent = Math.min(ds, 36) + " s";
        if (ds >= 30 && !m.flag.door) { m.flag.door = 1; m.doorPin.classList.add("is-bad"); m.alert("door", "Porte maintenue ouverte · sortie d’urgence", "Ouverte depuis 30 s · personne à proximité", "warn"); }
      }
      /* Contre-sens dans l'allée 4 (franchit la ligne vers le bas) */
      var a4 = m.S[4].p;
      if (a4 && a4.y > 300 && t > 17000 && !m.flag.line) { m.flag.line = 1; tog(m.S[4].n, "is-alert", true); m.alert("line", "Contre-sens · allée 4", "ID 29 · allée à sens unique vers le nord", "warn"); }
      if (m.heatOn && dt && (t % 500) < dt) m.paint();
    }
  };

  /* =====================================================================
     INCIDENTS — dossier complet : chronologie, extraits vidéo, plan et
     trajet, actions, puis export pour la police (extraits d'origine,
     personnes non concernées masquées, empreinte, lien qui expire).
     ===================================================================== */
  var INC_Q = [
    ["INC-014", "Porte forcée · quai 3", "Critique", "bad", "En cours", "03:26"],
    ["INC-013", "Talonnage · porte B", "Moyenne", "warn", "À examiner", "08:58"],
    ["INC-012", "Vitesse excessive · cour", "Faible", "idle", "Fermé", "17:06"],
    ["INC-011", "Refus répétés · E-1187", "Moyenne", "warn", "Résolu", "Hier"],
    ["INC-010", "Objet abandonné · transit", "Faible", "idle", "Fermé", "Hier"],
    ["INC-009", "Chute · allée 6", "Élevée", "bad", "Résolu", "2 nov."]
  ];
  var INC_TL = [
    ["03:26:04", "urg", "Porte forcée détectée · quai 3", "Contact de porte + capteur de vibration", "bad"],
    ["03:26:05", "person", "Personne à capuche · ID 47", "CAM 22 · quai de livraison", "warn"],
    ["03:26:09", "siren", "Mode urgence activé", "6 actions exécutées une à une", "bad"],
    ["03:26:12", "lights", "Projecteurs de la cour à 100" + PC, "Confirmé · état relu", "ok"],
    ["03:26:20", "call", "Agente de garde prévenue", "Accusé de réception à 03:26:31", "ok"],
    ["03:27:02", "cam", "Suivi sur 3 caméras", "CAM 22 → CAM 05 → CAM 07", "warn"],
    ["03:29:40", "file", "Police appelée", "Dossier de l’appel 26-118204", "gold"],
    ["03:41:12", "door", "Arrivée de la police", "Accès donné par la guérite", "ok"],
    ["03:58:00", "lock", "Porte sécurisée", "Incident maîtrisé · aucune autre intrusion", "ok"]
  ];
  var INC_EXP = [
    "3 extraits vidéo · 4 min 12 s · format d’origine",
    "Chronologie horodatée à la seconde",
    "Plan du site et trajet reconstitué",
    "Personnes non concernées masquées",
    "Journal des consultations du dossier",
    "Signature numérique · empreinte SHA-256"
  ];

  MODS.incidents = {
    site: "Centre de contrôle · dossiers d’incident",
    clock: "04:02:10",
    len: 20000,
    build: function (P) {
      var m = this;
      var clips = [
        ["delivery", [1100, 200, 520, 325], 1340, 520, 268, "CAM 22", "Quai de livraison", "03:26:05"],
        ["parking", [120, 250, 500, 312.5], 340, 390, 120, "CAM 07", "Barrière P1", "03:27:40"],
        ["delivery", [380, 300, 560, 350], 620, 610, 300, "CAM 05", "Cour · côté est", "03:27:02"]
      ];
      P.innerHTML = head("Incidents", "Chaque incident devient un dossier complet, prêt à remettre à la police ou à l’assureur.", [
        ["Ouverts", "2", "warn"],
        ["Critique", "1", "bad"],
        ["Prise en charge moyenne", "14 s", "ok"],
        ["Dossiers exportés · 30 j", "6", "", "exp"]
      ]) +
      '<div class="sx-grid sx-inc">' +
        card("sx-queue", "File des incidents", "6 derniers",
          '<ol class="sx-iq">' + INC_Q.map(function (q, i) {
            return '<li class="' + (i ? "" : "is-sel") + '"><span class="sx-iq-k">' + q[0] + "<time>" + q[5] + "</time></span><b>" + q[1] + "</b>" +
              '<span class="sx-iq-s">' + pill(q[2], q[3]) + "<small>" + q[4] + "</small></span></li>";
          }).join("") + "</ol>") +
        '<section class="sx-card sx-case">' +
          '<header class="sx-case-h"><div><span class="sx-case-id">INC-2026-1108-014</span><h4>Porte forcée — entrepôt, quai 3</h4>' +
          '<p>Assignée à <b>Sophie Morin</b> · agente de garde · témoin : <b>Julien Côté</b> (guérite)</p></div>' +
          '<div class="sx-case-st">' + pill("Critique", "bad") + pill("En cours", "warn") +
          '<div class="sx-sla"><small>Prise en charge</small><b>11 s</b><i><em></em></i><small>Objectif 60 s</small></div></div></header>' +
          '<div class="sx-case-g">' +
            '<div><p class="sx-k">Chronologie</p><ol class="sx-tl" data-inc-tl>' + INC_TL.map(function (r) {
              return '<li class="is-' + r[4] + '"><time>' + r[0] + '</time><i aria-hidden="true">' + ico(r[1]) + "</i><span><b>" + r[2] + "</b><small>" + r[3] + "</small></span></li>";
            }).join("") + "</ol></div>" +
            '<div class="sx-case-r"><p class="sx-k">Extraits · 3</p><div class="sx-clips" data-inc-clips></div>' +
            '<p class="sx-k">Trajet reconstitué</p><div class="sx-iplan" data-inc-plan></div></div>' +
          "</div>" +
          '<div class="sx-exp" data-inc-exp>' +
            '<div class="sx-exp-h"><p><b>Dossier pour la police</b><small>Extraits d’origine, personnes non concernées masquées, empreinte vérifiable.</small></p>' +
            '<button type="button" class="sx-btn is-main" data-inc-go>Préparer le dossier</button></div>' +
            '<div class="sx-exp-bar"><em data-inc-bar></em></div>' +
            '<ul class="sx-exp-l">' + INC_EXP.map(function (s) { return '<li><i class="sx-chk">' + CHECK + "</i>" + s + "</li>"; }).join("") + "</ul>" +
            '<div class="sx-exp-out" data-inc-out></div>' +
          "</div>" +
        "</section>" +
      "</div>";
      m.P = P;
      var cl = $("[data-inc-clips]", P);
      m.clips = clips.map(function (c) {
        var f = el("figure", "sx-clip", "");
        var v = el("div", "sx-thv", '<div class="sec-stage" style="' + stageCss(c[1]) + '"><img src="' + MS + "security-enterprise-" + c[0] + '-v1.webp" alt="" loading="lazy" decoding="async"></div>');
        var p = person("hood"), st = $(".sec-stage", v);
        st.appendChild(p);
        var b = box("alert"); st.appendChild(b); b.classList.add("is-in");
        f.appendChild(v);
        f.appendChild(el("div", "sx-clip-bar", "<em></em>"));
        f.appendChild(el("figcaption", "", "<b>" + c[5] + "</b><span>" + c[6] + "</span><time>" + c[7] + "</time>"));
        cl.appendChild(f);
        return { def: c, p: p, b: b, bar: $(".sx-clip-bar em", f), f: f };
      });
      $("[data-inc-plan]", P).innerHTML = campusSvg(function (g) {
        return '<g class="pl-cams">' + conesSvg([["CAM 22", 690, 386, -90, 110, 74, 0, 24], ["CAM 05", 872, 300, 180, 48, 200, 0, -12], ["CAM 07", 274, 74, 135, 70, 130, 0, -10]], g) + "</g>" +
          '<path class="pl-path" pathLength="100" d="M960 470H930V378H730V340H560V320H300V200H200V40"/>' +
          '<circle class="pl-pt is-a" cx="930" cy="470" r="7"/><circle class="pl-pt" cx="730" cy="378" r="6"/><circle class="pl-pt" cx="200" cy="44" r="6"/>' +
          '<text class="pl-t is-a" x="944" y="494" text-anchor="end">CLÔTURE · 03:25</text><text class="pl-t is-a" x="730" y="404" text-anchor="middle">QUAI 3 · 03:26</text><text class="pl-t is-a" x="216" y="30">SORTIE · 03:28</text>';
      });
      m.path = $(".pl-path", P);
      $$(".pl-cam", P).forEach(function (c) { c.classList.add("is-seen"); });
      P.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("button");
        if (!b || !P.contains(b)) return;
        if (b.hasAttribute("data-inc-go")) { m.exportGo(motion() ? 0 : -1); }
        else if (b.hasAttribute("data-inc-copy")) { b.textContent = "Lien copié · journalisé"; b.disabled = true; }
      });
      m.nexp = 6;
    },
    exportGo: function (t0) {
      var m = this, exp = $("[data-inc-exp]", m.P);
      exp.className = "sx-exp is-run";
      $("[data-inc-out]", m.P).innerHTML = "";
      $$(".sx-exp-l li", m.P).forEach(function (li) { li.className = ""; });
      m.expT = t0 < 0 ? -1 : m.t;
      if (t0 < 0) m.exportStep(1);
    },
    exportStep: function (u) {
      var m = this, lis = $$(".sx-exp-l li", m.P), n = Math.floor(u * lis.length + .0001);
      $("[data-inc-bar]", m.P).style.width = (u * 100).toFixed(1) + "%";
      lis.forEach(function (li, i) { tog(li, "is-done", i < n); tog(li, "is-cur", i === n); });
      if (u >= 1 && m.expT !== null) {
        m.expT = null;
        $("[data-inc-exp]", m.P).className = "sx-exp is-done";
        $("[data-inc-out]", m.P).innerHTML =
          '<div class="sx-file"><span class="sx-file-i">' + ico("file") + '</span><span><b>INC-2026-1108-014.zip</b><small>486 Mo · 9 fichiers · signé le ' + hms(simNow(m)).slice(0, 5).replace(":", " h ") + "</small></span></div>" +
          '<p class="sx-hash"><small>Empreinte SHA-256</small><code>9f2c 41d7 b08e 6a13 e5c2 77f0 1d9a c4e8 · · · 3b61 e08b</code></p>' +
          '<div class="sx-share"><span>Lien sécurisé pour le service de police · expire dans 7 jours · chaque téléchargement est journalisé</span>' +
          '<button type="button" class="sx-btn" data-inc-copy>Copier le lien</button></div>';
        m.nexp++; bump(setK(m.P, "exp", String(m.nexp)));
      }
    },
    reset: function () {
      var m = this, P = m.P;
      var tl = $$("[data-inc-tl] li", P);
      tl.forEach(function (li) { li.classList.remove("is-on"); });
      tl.forEach(function (li, i) { at(250 + i * 380, function () { li.classList.add("is-on"); }); });
      m.path.style.strokeDashoffset = "100";
      $("[data-inc-exp]", P).className = "sx-exp";
      $("[data-inc-bar]", P).style.width = "0%";
      $("[data-inc-out]", P).innerHTML = "";
      $$(".sx-exp-l li", P).forEach(function (li) { li.className = ""; });
      m.expT = null;
      at(5600, function () { m.exportGo(0); });
    },
    frame: function (t) {
      var m = this;
      m.path.style.strokeDashoffset = (100 - smooth((t - 600) / 3600) * 100).toFixed(2);
      /* Extraits : lecture en boucle, la silhouette avance avec la tête de lecture */
      m.clips.forEach(function (c, i) {
        var u = ((t / 1000 + i * 1.7) % 6) / 6, d = c.def;
        c.bar.style.width = (u * 100).toFixed(1) + "%";
        var p = { x: d[2] + (i === 1 ? 60 : -90) * (u - .5), y: d[3], h: d[4], o: 1, mv: true, left: i === 1 ? false : true };
        placeP(c.p, p);
        setBox(c.b, boxAround(p, .46, d[4] * .03), "ID 47", null, "");
      });
      if (m.expT !== null && m.expT >= 0) m.exportStep(clamp((t - m.expT) / 4200, 0, 1));
    }
  };

  /* =====================================================================
     CARTE DES SITES — plusieurs bâtiments et villes, état de chaque site,
     alertes consolidées vers un seul centre de contrôle. Chaque alerte
     part de son site et voyage jusqu'au centre avant d'entrer au fil.
     ===================================================================== */
  function geo(lon, lat) { return [(lon + 74.05) / 3.25 * 1000, (47.05 - lat) / 2.0 * 560]; }
  var ST_LIST = [
    { id: "mtl", name: "Montréal", role: "Siège social", ll: [-73.57, 45.50], st: "ok", cams: "64/64", doors: 48, arm: "Partiel", ag: 3, dy: 22 },
    { id: "sth", name: "Saint-Hyacinthe", role: "Centre de distribution · centre de contrôle", ll: [-72.96, 45.63], st: "ok", cams: "82/82", doors: 61, arm: "Partiel", ag: 4, soc: true, dy: 24 },
    { id: "dru", name: "Drummondville", role: "Entrepôt", ll: [-72.48, 45.88], st: "warn", cams: "37/38", doors: 22, arm: "Armé", ag: 1, note: "CAM 12 hors ligne depuis 02 h 14 · technicien prévenu", dy: -14 },
    { id: "she", name: "Sherbrooke", role: "Usine", ll: [-71.89, 45.40], st: "ok", cams: "71/71", doors: 54, arm: "Partiel", ag: 2, dy: 22 },
    { id: "trv", name: "Trois-Rivières", role: "Bureau régional", ll: [-72.55, 46.35], st: "bad", cams: "29/29", doors: 14, arm: "Armé", ag: 1, note: "Intrusion · clôture nord · agent en route", dy: -14 },
    { id: "qbc", name: "Québec", role: "Bureau régional", ll: [-71.21, 46.81], st: "ok", cams: "78/78", doors: 113, arm: "Armé à 18 h 04", ag: 0, dy: -14 }
  ];
  var ST_EV = [
    ["trv", "bad", "Intrusion · clôture nord", "Agent en route · arrivée estimée 4 min"],
    ["mtl", "ok", "Livraison prévue reçue · quai 1", "Plaque V82 3TR reconnue"],
    ["dru", "warn", "Caméra hors ligne · CAM 12", "Technicien prévenu · billet 4471"],
    ["she", "gold", "Visiteur attendu · hall", "Laissez-passer QR validé"],
    ["qbc", "ok", "Bâtiment armé", "Dernière sortie à 18 h 02 · ronde confirmée"],
    ["sth", "warn", "Talonnage · porte de service B", "Extrait conservé · INC-013"],
    ["mtl", "warn", "Porte maintenue ouverte · 14", "Fermée après 42 s"],
    ["trv", "ok", "Agent sur place · clôture nord", "Branche tombée sur la clôture · fausse alerte confirmée"]
  ];
  var ST_RIVER = [[-74.3, 45.2], [-73.95, 45.33], [-73.62, 45.45], [-73.47, 45.62], [-73.25, 45.85], [-73.0, 46.04], [-72.75, 46.2], [-72.55, 46.32], [-72.2, 46.45], [-71.8, 46.6], [-71.4, 46.72], [-71.2, 46.8], [-70.95, 46.92], [-70.6, 47.1]];

  MODS.sites = {
    site: "Vue multisite · 6 sites · centre de contrôle Saint-Hyacinthe",
    clock: "19:12:30",
    len: 24000,
    build: function (P) {
      var m = this, soc = geo(-72.96, 45.63);
      var river = ST_RIVER.map(function (p) { var g = geo(p[0], p[1]); return g[0].toFixed(1) + " " + g[1].toFixed(1); }).join("L");
      var grat = "";
      [45, 45.5, 46, 46.5].forEach(function (la) { var y = geo(-74, la)[1]; grat += '<path class="mp-gr" d="M0 ' + y.toFixed(1) + 'H1000"/><text class="mp-gt" x="6" y="' + (y - 4).toFixed(1) + '">' + String(la).replace(".", ",") + "° N</text>"; });
      [-74, -73, -72, -71].forEach(function (lo) { var x = geo(lo, 46)[0]; grat += '<path class="mp-gr" d="M' + x.toFixed(1) + ' 0V560"/><text class="mp-gt" x="' + (x + 4).toFixed(1) + '" y="552">' + Math.abs(lo) + "° O</text>"; });
      var arcs = "", nodes = "";
      ST_LIST.forEach(function (s, i) {
        var p = geo(s.ll[0], s.ll[1]); s.p = p;
        if (!s.soc) {
          var mx = (p[0] + soc[0]) / 2, my = (p[1] + soc[1]) / 2, dx = soc[0] - p[0], dy = soc[1] - p[1], L = Math.hypot(dx, dy);
          var cx = mx - dy / L * L * .22, cy = my + dx / L * L * .22;
          arcs += '<path class="mp-arc" id="sxArc-' + s.id + '" d="M' + p[0].toFixed(1) + " " + p[1].toFixed(1) + "Q" + cx.toFixed(1) + " " + cy.toFixed(1) + " " + soc[0].toFixed(1) + " " + soc[1].toFixed(1) + '"/>';
        }
        nodes += '<g class="mp-site is-' + s.st + (s.soc ? " is-soc" : "") + '" data-site="' + s.id + '" transform="translate(' + p[0].toFixed(1) + " " + p[1].toFixed(1) + ')">' +
          '<circle class="mp-ring" r="16"/><circle class="mp-ring2" r="16"/>' + (s.soc ? '<rect class="mp-socr" x="-11" y="-11" width="22" height="22" rx="4"/>' : "") + '<circle class="mp-dot" r="6.5"/>' +
          '<text class="mp-n" y="' + (s.dy > 0 ? s.dy + 8 : s.dy) + '" text-anchor="middle">' + s.name.toUpperCase() + "</text>" +
          (s.soc ? '<text class="mp-s" y="' + (s.dy + 22) + '" text-anchor="middle">CENTRE DE CONTRÔLE</text>' : "") + "</g>";
      });
      var svg = '<svg class="sx-plan sx-map" viewBox="0 0 1000 560" role="img" aria-label="Carte des sites (exemple)">' +
        '<rect width="1000" height="560" class="pl-bg"/>' + grat +
        '<path class="mp-river" d="M' + river + '"/><path class="mp-river2" d="M' + river + '"/>' +
        '<text class="mp-rt" transform="translate(' + geo(-72.1, 46.56)[0].toFixed(0) + " " + geo(-72.1, 46.56)[1].toFixed(0) + ') rotate(-19)">FLEUVE SAINT-LAURENT</text>' +
        '<g data-st-arcs>' + arcs + "</g>" + nodes + '<g data-st-pulses></g></svg>';
      P.innerHTML = head("Carte des sites", "Tous vos bâtiments sur une seule carte, avec l’état de chacun et un seul fil d’alertes.", [
        ["Sites", "6", "ok"],
        ["Caméras en ligne", "361<small>/362</small>", "warn"],
        ["Portes", "312"],
        ["Alertes ouvertes", "2", "bad", "open"],
        ["Agents en service", "11"]
      ]) +
      '<div class="sx-grid sx-sites">' +
        '<div class="sx-col">' +
          card("sx-mapc", "Réseau des sites", '<i class="sx-live"></i>Liaisons chiffrées · 6 sur 6', '<div class="sx-planw">' + svg + "</div>") +
          card("", "Alertes consolidées", "Tous les sites", '<ol class="sx-feed" data-st-feed></ol>') +
        "</div>" +
        card("sx-slist", "État par site", "Touchez un site",
          '<ul class="sx-sl">' + ST_LIST.map(function (s) {
            return '<li class="is-' + s.st + '" data-site="' + s.id + '"><button type="button">' +
              '<span class="sx-sl-h"><b>' + s.name + "</b>" + pill(s.st === "ok" ? "Normal" : s.st === "warn" ? "Attention" : "Alerte", s.st) + "</span>" +
              "<small>" + s.role + "</small>" +
              '<span class="sx-sl-m"><span><em>' + s.cams + "</em>caméras</span><span><em>" + s.doors + "</em>portes</span><span><em>" + s.ag + "</em>agents</span><span><em>" + s.arm + "</em>alarme</span></span>" +
              (s.note ? '<span class="sx-sl-n">' + s.note + "</span>" : "") + "</button></li>";
          }).join("") + "</ul>") +
      "</div>";
      m.P = P;
      m.feed = $("[data-st-feed]", P);
      m.pulses = $("[data-st-pulses]", P);
      m.ei = 0; m.live = [];
      P.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("[data-site]");
        if (!b || !P.contains(b)) return;
        var id = b.getAttribute("data-site");
        $$("[data-site]", P).forEach(function (n) { tog(n, "is-sel", n.getAttribute("data-site") === id); });
      });
    },
    reset: function () {
      var m = this;
      m.pulses.innerHTML = ""; m.live = [];
      if (!m.feed.children.length) for (var j = 0; j < 3; j++) m.addRow(ST_EV[(m.ei++) % ST_EV.length], true);
      for (var k = 0; k < 8; k++) (function (k) {
        at(800 + k * 2900, function () { m.emit(ST_EV[(m.ei++) % ST_EV.length]); });
      })(k);
    },
    emit: function (ev) {
      var m = this, site = $('.mp-site[data-site="' + ev[0] + '"]', m.P);
      if (site) { site.classList.remove("is-ping"); void site.getBoundingClientRect(); site.classList.add("is-ping"); site.setAttribute("data-tone", ev[1]); }
      var arc = $("#sxArc-" + ev[0], m.P);
      if (!arc || !motion()) { m.addRow(ev); return; }
      var c = sv("circle", { r: 4.5, "class": "mp-pulse is-" + ev[1] }, m.pulses);
      var tail = sv("circle", { r: 9, "class": "mp-pulse2 is-" + ev[1] }, m.pulses);
      arc.classList.add("is-hot");
      m.live.push({ c: c, tail: tail, arc: arc, len: arc.getTotalLength(), t0: m.t, ev: ev });
    },
    addRow: function (ev, quiet) {
      var m = this, s = ST_LIST.filter(function (x) { return x.id === ev[0]; })[0];
      var li = el("li", "sx-ev is-" + ev[1] + (ev[1] === "bad" ? " is-hot" : ""),
        '<span class="sx-ev-i">' + ico("cam") + '</span><span class="sx-ev-t"><b>' + ev[2] + "</b><small>" + s.name + " · " + ev[3] + "</small></span>" +
        '<span class="sx-ev-r">' + pill(s.name, ev[1]) + "<time>" + hms(simNow(m)) + "</time></span>");
      push(m.feed, li, 4);
      if (quiet) li.classList.remove("is-new");
      if (ev[0] === "trv") m.state("trv", ev[1] === "ok" ? "ok" : "bad", ev[1] === "ok" ? "Fausse alerte confirmée par l’agent · branche sur la clôture" : "Intrusion · clôture nord · agent en route");
    },
    state: function (id, st, note) {
      var m = this, n = $('.sx-sl li[data-site="' + id + '"]', m.P);
      if (n) {
        tog(n, "is-ok", st === "ok"); tog(n, "is-bad", st === "bad");
        $(".sx-pill", n).outerHTML = pill(st === "ok" ? "Normal" : "Alerte", st);
        var nt = $(".sx-sl-n", n); if (nt) nt.textContent = note;
      }
      var g = $('.mp-site[data-site="' + id + '"]', m.P);
      if (g) { g.classList.remove("is-ok", "is-bad"); g.classList.add("is-" + st); }
      var o = $('[data-k="open"]', m.P); var v = st === "ok" ? "1" : "2";
      if (o.textContent !== v) { o.textContent = v; bump(o); }
    },
    frame: function (t) {
      var m = this;
      m.live = m.live.filter(function (p) {
        var u = clamp((t - p.t0) / 1300, 0, 1), e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
        var pt = p.arc.getPointAtLength(e * p.len), pt2 = p.arc.getPointAtLength(Math.max(0, e - .06) * p.len);
        p.c.setAttribute("cx", pt.x.toFixed(1)); p.c.setAttribute("cy", pt.y.toFixed(1));
        p.tail.setAttribute("cx", pt2.x.toFixed(1)); p.tail.setAttribute("cy", pt2.y.toFixed(1));
        if (u >= 1) {
          p.c.parentNode.removeChild(p.c); p.tail.parentNode.removeChild(p.tail);
          p.arc.classList.remove("is-hot");
          var soc = $(".mp-site.is-soc", m.P); soc.classList.remove("is-ping"); void soc.getBoundingClientRect(); soc.classList.add("is-ping");
          m.addRow(p.ev);
          return false;
        }
        return true;
      });
    },
    leave: function () {
      var m = this;
      m.live.forEach(function (p) { if (p.c.parentNode) p.c.parentNode.removeChild(p.c); if (p.tail.parentNode) p.tail.parentNode.removeChild(p.tail); });
      m.live = [];
    }
  };

  /* =====================================================================
     RONDES ET AGENTS — ronde de nuit avec 10 points de contrôle (étiquettes
     NFC), agente suivie sur le plan, point en retard, protection du
     travailleur isolé (immobilité → vérification → réponse).
     ===================================================================== */
  var RD_PTS = [ // nom, x, y
    ["Guérite", 71, 372], ["P1 · nord-ouest", 92, 62], ["P1 · est", 290, 180], ["Bâtiment A · ouest", 330, 160],
    ["Bâtiment A · nord", 480, 62], ["P2 · visiteurs", 640, 160], ["Clôture est", 945, 300], ["Quai 6", 862, 352],
    ["Entrepôt · sud", 740, 535], ["Bâtiment C", 275, 450]
  ];
  var RD_ROUTE = [[71, 372, 0], [55, 320], [55, 62], [92, 62, 1], [290, 62], [290, 180, 2], [330, 180], [330, 160, 3], [330, 62], [480, 62, 4], [640, 62], [640, 160, 5],
    [640, 290], [800, 290, "stop"], [945, 290], [945, 300, 6], [890, 300], [890, 352], [862, 352, 7], [890, 352], [890, 535], [740, 535, 8], [300, 535], [300, 450], [275, 450, 9], [300, 450], [300, 372], [90, 372], [71, 372]];

  MODS.rondes = {
    site: "Campus Est · ronde B · 10 points de contrôle",
    clock: "02:00:00",
    rate: 60,
    len: 30000,
    build: function (P) {
      var m = this;
      /* Clés temporelles du trajet : vitesse constante, pause à chaque point */
      var keys = [], t = 0, V = .2; // unités par ms
      m.cpAt = {};
      RD_ROUTE.forEach(function (p, i) {
        if (i) t += Math.hypot(p[0] - RD_ROUTE[i - 1][0], p[1] - RD_ROUTE[i - 1][1]) / V;
        keys.push([Math.round(t), p[0], p[1]]);
        if (typeof p[2] === "number") { m.cpAt[p[2]] = Math.round(t); t += 650; keys.push([Math.round(t), p[0], p[1]]); }
        if (p[2] === "stop") { m.stopAt = Math.round(t); t += 3400; keys.push([Math.round(t), p[0], p[1]]); }
      });
      m.keys = keys; m.walkEnd = Math.round(t); m.len = m.walkEnd + 5500;
      var cps = RD_PTS.map(function (c, i) {
        return '<g class="rd-cp" data-cp="' + i + '" transform="translate(' + c[1] + " " + c[2] + ')"><circle class="rd-cpr" r="18"/><circle class="rd-cpd" r="12.5"/><text y="4.6" text-anchor="middle">' + (i + 1) + "</text></g>";
      }).join("");
      var route = "M" + RD_ROUTE.map(function (p) { return p[0] + " " + p[1]; }).join("L");
      P.innerHTML = head("Rondes et agents", "Des rondes prouvées point par point, et une protection pour l’agent qui travaille seul la nuit.", [
        ["Agents en service", "2", "ok"],
        ["Rondes cette nuit", "4"],
        ["Points vérifiés", "26<small>/40</small>", "", "cp"],
        ["Retards", "0", "", "late"]
      ]) +
      '<div class="sx-grid sx-rd">' +
        card("sx-rdplan", "Ronde B · 02 h 00", '<span data-rd-prog>0 / 10 points</span>',
          '<div class="sx-planw" data-rd-plan>' + campusSvg(function () {
            return '<path class="rd-route" d="' + route + '"/><path class="rd-done" data-rd-done d=""/>' + cps +
              '<g class="rd-ag" data-rd-ag><circle class="rd-agh" r="20"/><circle class="rd-agd" r="8.5"/><text y="-18" text-anchor="middle">SM</text></g>';
          }) + "</div>" + '<ol class="sx-pass" data-rd-pass aria-label="Points vérifiés"></ol>') +
        '<div class="sx-col">' +
          card("sx-agents", "Agents", "2 en service",
            '<div class="sx-agent is-main"><span class="sx-av">SM</span><span class="sx-ag-t"><b>Sophie Morin</b><small>Agente de nuit · ronde B</small></span>' +
            '<span class="sx-ringp"><svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="15"/><circle class="r" data-rd-ring cx="18" cy="18" r="15" pathLength="100"/></svg><b data-rd-n>0</b></span>' +
            '<dl class="sx-ag-d"><div><dt>Radio</dt><dd>' + pill("Liaison OK", "ok") + "</dd></div><div><dt>Batterie</dt><dd><span class=\"sx-batt\"><i style=\"width:82%\"></i></span>82" + PC + "</dd></div>" +
            '<div><dt>Travailleur isolé</dt><dd data-rd-lw>' + pill("Actif · en mouvement", "ok") + "</dd></div></dl></div>" +
            '<div class="sx-agent"><span class="sx-av">JC</span><span class="sx-ag-t"><b>Julien Côté</b><small>Guérite · poste fixe</small></span>' + pill("Au poste", "ok") + "</div>") +
          card("sx-cpc", "Points de contrôle", "Étiquettes NFC",
            '<ol class="sx-cpl">' + RD_PTS.map(function (c, i) { return '<li data-cpl="' + i + '"><span>' + (i + 1) + "</span><b>" + c[0] + "</b><em>À venir</em></li>"; }).join("") + "</ol>") +
        "</div>" +
      "</div>" +
      '<div class="sx-grid sx-g2">' +
        card("", "Horaire de la nuit", "Campus Est",
          '<ol class="sx-sched"><li class="is-ok"><time>22 h 00</time><b>Ronde A · extérieur</b>' + pill("Terminée · 23 min", "ok") + '</li>' +
          '<li class="is-ok"><time>00 h 00</time><b>Ronde B · extérieur et quais</b>' + pill("Terminée · 31 min", "ok") + "</li>" +
          '<li class="is-cur"><time>02 h 00</time><b>Ronde B · extérieur et quais</b>' + pill("En cours", "gold") + "</li>" +
          '<li><time>04 h 00</time><b>Ronde C · intérieur des bâtiments</b>' + pill("À venir", "idle") + "</li></ol>") +
        card("", "Rapport de ronde", "Rédigé par JARVIS", '<p class="sx-rep2" data-rd-rep>La ronde est en cours. Le rapport se rédige à mesure que les points sont vérifiés.</p>') +
      "</div>";
      m.P = P;
      m.ag = $("[data-rd-ag]", P);
      m.done = $("[data-rd-done]", P);
      m.pins = el("div", "sx-zpins", "");
      $("[data-rd-plan]", P).appendChild(m.pins);
    },
    reset: function () {
      var m = this, P = m.P;
      $$(".rd-cp", P).forEach(function (n) { n.setAttribute("class", "rd-cp"); });
      $$("[data-cpl]", P).forEach(function (n) { n.className = ""; n.querySelector("em").textContent = "À venir"; });
      m.pins.innerHTML = ""; m.n = 0; m.trail = [];
      $("[data-rd-pass]", P).innerHTML = "";
      $("[data-rd-n]", P).textContent = "0";
      $("[data-rd-ring]", P).style.strokeDashoffset = "100";
      $("[data-rd-prog]", P).textContent = "0 / 10 points";
      $("[data-rd-lw]", P).innerHTML = pill("Actif · en mouvement", "ok");
      $("[data-rd-rep]", P).textContent = "La ronde est en cours. Le rapport se rédige à mesure que les points sont vérifiés.";
      setK(P, "late", "0"); setK(P, "cp", "26<small>/40</small>");
      Object.keys(m.cpAt).forEach(function (k) {
        at(m.cpAt[k] + 300, function () { m.check(+k); });
      });
      at(m.stopAt + 1300, function () {
        m.lw = m.pin(800, 290, "", "<b>Immobile · 45 s</b>");
        $("[data-rd-lw]", P).innerHTML = pill("Immobile · vérification envoyée", "warn");
        $("[data-rd-pass]", P).appendChild(el("li", "sx-pass-e is-warn", "<span>Travailleur isolé : immobile 45 s · vérification envoyée sur la radio</span><time>" + hms(simNow(m)).slice(0, 5).replace(":", " h ") + "</time>"));
        tog(m.ag, "is-warn", true);
      });
      at(m.stopAt + 2700, function () {
        if (m.lw) m.lw.innerHTML = "<b>Réponse : tout va bien</b>", m.lw.classList.add("is-ok");
        $("[data-rd-lw]", P).innerHTML = pill("Réponse reçue · tout va bien", "ok");
        $("[data-rd-pass]", P).appendChild(el("li", "sx-pass-e is-ok", "<span>Réponse de l’agente : tout va bien · bruit vérifié près de la clôture</span><time>" + hms(simNow(m)).slice(0, 5).replace(":", " h ") + "</time>"));
        tog(m.ag, "is-warn", false);
      });
      at(m.stopAt + 4200, function () { if (m.lw) m.lw.classList.add("is-off"); $("[data-rd-lw]", P).innerHTML = pill("Actif · en mouvement", "ok"); });
      at(m.walkEnd + 600, function () {
        $("[data-rd-rep]", P).innerHTML = "<b>Ronde B terminée en " + Math.round(m.walkEnd / 1000) + " min.</b> 10 points sur 10 vérifiés. " +
          "Un retard de 4 min au point 7 (clôture est) : l’agente s’est arrêtée pour vérifier un bruit près de la clôture, et a répondu à la vérification de travailleur isolé. Aucune anomalie constatée.";
      });
    },
    pin: function (x, y, cls, html) {
      var n = el("div", "sx-zpin " + cls, html);
      n.style.left = pct(x, 1000) + "%"; n.style.top = pct(y, 600) + "%";
      this.pins.appendChild(n);
      return n;
    },
    check: function (i) {
      var m = this, P = m.P, late = i === 6;
      var g = $('.rd-cp[data-cp="' + i + '"]', P); g.setAttribute("class", "rd-cp " + (late ? "is-late" : "is-ok"));
      var li = $('[data-cpl="' + i + '"]', P);
      li.className = late ? "is-late" : "is-ok";
      li.querySelector("em").textContent = hms(simNow(m)).slice(0, 5).replace(":", " h ") + (late ? " · retard 4 min" : "");
      m.n++;
      $("[data-rd-n]", P).textContent = String(m.n);
      $("[data-rd-ring]", P).style.strokeDashoffset = String(100 - m.n * 10);
      $("[data-rd-prog]", P).textContent = m.n + " / 10 points";
      setK(P, "cp", (26 + m.n) + "<small>/40</small>");
      if (late) { bump(setK(P, "late", "1")); }
      var pass = $("[data-rd-pass]", P), tm = hms(simNow(m)).slice(0, 5).replace(":", " h ");
      pass.appendChild(el("li", late ? "is-late" : "", "<b>" + (i + 1) + "</b><time>" + tm + "</time>"));
    },
    frame: function (t) {
      var m = this, p = along(m.keys, Math.min(t, m.walkEnd));
      if (!p) return;
      m.ag.setAttribute("transform", "translate(" + p.x.toFixed(1) + " " + p.y.toFixed(1) + ")");
      var last = m.trail[m.trail.length - 1];
      if (!last || Math.abs(last[0] - p.x) + Math.abs(last[1] - p.y) > 4) {
        m.trail.push([p.x, p.y]);
        if (m.trail.length > 1) m.done.setAttribute("d", "M" + m.trail.map(function (a) { return a[0].toFixed(1) + " " + a[1].toFixed(1); }).join("L"));
      }
    }
  };

  /* =====================================================================
     CONFORMITÉ — Loi 25 comme argument de vente : masquage automatique
     des visages hors incident, registre biométrique déclaré, journal
     d'accès aux images, durées de conservation et purge automatique.
     ===================================================================== */
  var CF_PEOPLE = [[1300, 505, 250, "dark"], [620, 612, 300, "livreur"], [1520, 600, 290, "hood"]];
  var CF_LOG = [
    ["Sophie Morin", "a regardé en direct", "CAM 21 · porte de service B", "Ronde de nuit"],
    ["Karim Haddad", "a exporté", "INC-013 · 1 extrait de 20 s", "Enquête interne"],
    ["Système", "a effacé", "Vidéo du 9 octobre · 1,8 To", "Durée de conservation atteinte"],
    ["Camille Lavoie", "a consulté", "Registre des consentements", "Audit trimestriel"],
    ["Système", "a effacé", "ID temporaire P-2288", "72 h écoulées"],
    ["Sophie Morin", "a consulté", "Fiche d’Olivier Roy", "Permis de travail · toit"]
  ];

  MODS.conformite = {
    site: "Conformité · Loi 25 · registre et journaux",
    clock: "11:47:16",
    len: 24000,
    build: function (P) {
      var m = this;
      P.innerHTML = head("Conformité", "La Loi 25 intégrée au logiciel : ce qui protège les gens protège aussi l’entreprise.", [
        ["Contrôles respectés", "18<small>/18</small>", "ok"],
        ["Consentements valides", "252<small>/252</small>", "ok"],
        ["Consultations · 30 j", "418", "", "views"],
        ["Prochaine purge", "03:12:44", "gold", "purge"]
      ]) +
      '<div class="sx-grid sx-cf">' +
        card("sx-maskc", "Masquage automatique des visages", '<span data-cf-mst>Actif · hors incident</span>',
          '<div data-cf-cam></div>' +
          '<div class="sx-mask-b" data-cf-mb><span>Les visages restent masqués à l’écran et à l’export, sauf pour un incident ouvert, avec un motif.</span>' +
          '<button type="button" class="sx-btn" data-cf-lift>Lever le masquage</button></div>') +
        card("sx-bio", "Registre biométrique", pill("Déclaré à la CAI", "ok"),
          '<p class="sx-bio-l">Déclaration à la Commission d’accès à l’information · 3 février 2026 · mise à jour le 12 octobre</p>' +
          '<div class="sx-bars">' +
          '<p><span>Employés</span><b>214 / 214</b><i><em style="--w:100%"></em></i></p>' +
          '<p><span>Sous-traitants</span><b>38 / 38</b><i><em style="--w:100%"></em></i></p>' +
          '<p><span>Retraits de consentement traités</span><b>3 · délai moyen 4 h</b><i><em style="--w:100%" class="is-g"></em></i></p></div>' +
          '<ul class="sx-facts">' +
          "<li>" + CHECK + "Gabarits chiffrés, gardés sur place; aucune photo de visage conservée pour l’identification</li>" +
          "<li>" + CHECK + "Consentement exprès, séparé, retirable en tout temps</li>" +
          "<li>" + CHECK + "Autre moyen offert sans pénalité : badge seul</li>" +
          "<li>" + CHECK + "Personnes non inscrites jamais identifiées · ID temporaire effacé après 72 h</li></ul>") +
      "</div>" +
      '<div class="sx-grid sx-g3">' +
        card("", "Journal d’accès aux images", '<i class="sx-live"></i>Chaîné', '<ol class="sx-jr" data-cf-jr></ol>') +
        card("sx-ret", "Durées de conservation", "Purge automatique",
          '<ul class="sx-retl">' +
          '<li><span>Vidéo courante</span><b>30 jours</b><i><em style="--w:12%"></em></i></li>' +
          '<li><span>ID temporaires · non inscrits</span><b>72 heures</b><i><em style="--w:3%"></em></i></li>' +
          '<li><span>Extraits d’incident</span><b>2 ans · gel possible</b><i><em style="--w:55%"></em></i></li>' +
          '<li><span>Journal d’accès aux images</span><b>5 ans</b><i><em style="--w:100%"></em></i></li>' +
          '<li><span>Gabarits biométriques</span><b>Jusqu’au retrait</b><i><em style="--w:100%" class="is-g"></em></i></li></ul>' +
          '<div class="sx-purge"><p><small>Prochaine purge</small><b data-cf-purge>03:12:44</b></p><p><small>Dernière purge</small><span>Hier · 3 h · 1,8 To effacés · certificat de destruction no 2291</span></p></div>') +
        card("sx-efvp", "Évaluation et responsabilités", "À jour",
          '<ul class="sx-ck" data-cf-ck>' + [
            "Évaluation des facteurs relatifs à la vie privée (EFVP)",
            "Affichage aux entrées : caméras et finalités",
            "Politique de conservation publiée",
            "Registre des incidents de confidentialité",
            "Accès par rôle · double approbation des exports",
            "Hébergement au Québec · données sur place"
          ].map(function (s) { return '<li><i class="sx-chk">' + CHECK + "</i>" + s + "</li>"; }).join("") + "</ul>" +
          '<p class="sx-resp"><small>Responsable de la protection des renseignements personnels</small><b>Camille Lavoie · direction</b></p>') +
      "</div>";
      m.P = P;
      var cam = camTile({ img: MS + "security-enterprise-delivery-v1.webp", view: [280, 100, 1340, 837.5], num: "CAM 20", name: "Entrée de service", alt: "Entrée de service avec trois personnes dont les visages sont masqués", cls: "sx-wide sx-mcam" });
      $("[data-cf-cam]", P).appendChild(cam.el);
      m.cam = cam;
      m.masks = CF_PEOPLE.map(function (c, i) {
        var p = person(c[3]);
        cam.stage.appendChild(p);
        placeP(p, { x: c[0], y: c[1], h: c[2], o: 1, mv: false, left: i === 2 });
        var w = c[2] * 60 / 170, hx = c[0] + (i === 2 ? -1 : 1) * (32.7 - 30) / 60 * w, hy = c[1] - c[2] * (1 - 14 / 170);
        var mk = pin(cam.stage, "sx-mask", hx, hy, "<b>Masqué</b>");
        mk.style.setProperty("--s", (c[2] * .16 / H * 100).toFixed(3));
        return mk;
      });
      m.scan = el("i", "sx-mscan", ""); cam.el.appendChild(m.scan);
      m.lift = el("div", "sx-lift", ""); cam.el.appendChild(m.lift);
      m.jr = $("[data-cf-jr]", P);
      m.li = 0; m.views = 418;
      m.ts = $$("[data-sx-ts]", P);
      P.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("button");
        if (!b || !P.contains(b)) return;
        var mb = $("[data-cf-mb]", P);
        if (b.hasAttribute("data-cf-lift")) {
          mb.innerHTML = "<span>Motif obligatoire · lié à un incident ouvert</span>" +
            '<button type="button" class="sx-btn is-main" data-cf-why>INC-2026-1108-014 · porte forcée</button><button type="button" class="sx-btn" data-cf-no>Annuler</button>';
        } else if (b.hasAttribute("data-cf-no")) {
          m.barReset();
        } else if (b.hasAttribute("data-cf-why")) {
          m.unmask("Vous · démo");
        }
      });
    },
    barReset: function () {
      $("[data-cf-mb]", this.P).innerHTML = "<span>Les visages restent masqués à l’écran et à l’export, sauf pour un incident ouvert, avec un motif.</span>" +
        '<button type="button" class="sx-btn" data-cf-lift>Lever le masquage</button>';
    },
    unmask: function (who) {
      var m = this;
      m.liftT = m.t; m.lifted = true;
      m.cam.el.classList.add("is-lifted");
      $("[data-cf-mst]", m.P).textContent = "Levé · INC-014";
      $("[data-cf-mb]", m.P).innerHTML = '<span class="sx-okk">' + CHECK + "Masquage levé pour 30 s · consultation inscrite au journal</span>";
      m.log([who, "a levé le masquage", "CAM 20 · 30 s", "INC-2026-1108-014"], true);
      if (!motion()) soon(0, function () { m.lift.className = "sx-lift is-on"; m.lift.innerHTML = "<b>Masquage levé · INC-014</b><span>Retour automatique dans 30 s</span>"; });
    },
    remask: function () {
      var m = this;
      m.lifted = false;
      m.cam.el.classList.remove("is-lifted");
      m.lift.className = "sx-lift";
      $("[data-cf-mst]", m.P).textContent = "Actif · hors incident";
      m.barReset();
    },
    log: function (r, mine) {
      var m = this, tm = hms(simNow(m)), prev = m.jr.firstChild ? m.jr.firstChild.getAttribute("data-h") : "c41a";
      var h = hash4(prev + r.join("") + tm);
      var li = el("li", mine ? "is-mine" : "", "<time>" + tm + '</time><span><span class="sx-jr-s"><b>' + r[0] + "</b> " + r[1] + " <em>" + r[2] + "</em></span><small>Motif : " + r[3] + "</small></span>" +
        "<code>" + prev + " → " + h + "</code>");
      li.setAttribute("data-h", h);
      push(m.jr, li, 4);
      m.views++; bump(setK(m.P, "views", String(m.views)));
    },
    onSecond: function (txt, s) {
      var left = Math.max(0, secs("15:00:00") - s);
      var v = hms(left);
      setK(this.P, "purge", v);
      var n = $("[data-cf-purge]", this.P); if (n) n.textContent = v;
      this.ts.forEach(function (n) { n.textContent = txt; });
    },
    reset: function () {
      var m = this;
      if (m.lifted) m.remask();
      m.masks.forEach(function (k) { k.classList.remove("is-on"); });
      m.scan.className = "sx-mscan";
      $$("[data-cf-ck] li", m.P).forEach(function (li) { li.classList.remove("is-done"); });
      at(300, function () { m.scan.classList.add("is-on"); });
      m.masks.forEach(function (k, i) { at(700 + i * 420, function () { k.classList.add("is-on"); }); });
      $$("[data-cf-ck] li", m.P).forEach(function (li, i) { at(400 + i * 260, function () { li.classList.add("is-done"); }); });
      if (!m.jr.children.length) for (var j = 0; j < 3; j++) m.log(CF_LOG[m.li++ % CF_LOG.length]);
      for (var k = 0; k < 5; k++) (function (k) { at(2600 + k * 3800, function () { m.log(CF_LOG[m.li++ % CF_LOG.length]); }); })(k);
      at(9000, function () { if (!m.lifted) m.unmask("Sophie Morin"); });
    },
    frame: function (t) {
      var m = this;
      if (m.lifted) {
        var left = Math.max(0, 30 - Math.floor((t - m.liftT) / 1000 * 3));
        m.lift.className = "sx-lift is-on";
        m.lift.innerHTML = "<b>Masquage levé · INC-014</b><span>Retour automatique dans " + left + " s</span>";
        if (left <= 0) m.remask();
      }
    }
  };

  /* ---------- Navigation entre les modules ---------- */
  var tabs = $$("[data-sx-mod]", nav);
  var panels = {};
  $$("[data-sx-panel]").forEach(function (p) { panels[p.getAttribute("data-sx-panel")] = p; });

  function select(key) {
    if (key === active || !panels[key]) return;
    var prev = MODS[active];
    if (active === "mur") { wallSite = siteEl ? siteEl.textContent : ""; wallClock = clockEl ? clockEl.textContent : ""; }
    if (prev && prev.leave) prev.leave();
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    active = key;
    tabs.forEach(function (b) {
      var on = b.getAttribute("data-sx-mod") === key;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && b.scrollIntoView && b.parentNode.scrollWidth > b.parentNode.clientWidth) {
        var tl = b.parentNode, x = b.offsetLeft - (tl.clientWidth - b.offsetWidth) / 2;
        tl.scrollTo ? tl.scrollTo({ left: x, behavior: motion() ? "smooth" : "auto" }) : (tl.scrollLeft = x);
      }
    });
    for (var k in panels) if (panels.hasOwnProperty(k)) panels[k].hidden = k !== key;
    root.setAttribute("data-sx-on", key);
    if (key === "mur") {
      if (siteEl && wallSite) siteEl.textContent = wallSite;
      if (clockEl && wallClock) clockEl.textContent = wallClock;
      return;
    }
    var m = MODS[key];
    if (!m.built) { m.build(panels[key]); m.built = true; }
    if (siteEl) siteEl.textContent = m.site;
    restart(m);
    if (!motion()) { finish(m); return; }
    advance(m, 0);
    if (m.frame) m.frame(0, 0);
    clock(m);
    play();
  }
  tabs.forEach(function (b) {
    b.addEventListener("click", function () { select(b.getAttribute("data-sx-mod")); });
  });
  root.classList.add("sx-ready");

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        visible = e.isIntersecting;
        tog(root, "is-paused", !visible);
        if (visible) play();
      });
    }, { threshold: [0, .15] }).observe(root);
  } else {
    visible = true;
  }
})();
