/* Environnements intelligents : un seul modèle de logiciel pour tous les lieux (BouLance, maison, chalet,
   entreprise, atelier, ferme, bateau, hangar avec turbopropulseur et jet). Les données viennent de src/demos/env.py (bloc JSON #env-data);
   chaque section est dessinée seulement quand elle s'ouvre. Batteries de BouLance réelles (service /live du
   site, toutes les 10 s, seulement quand la démo est visible); soleil et lune calculés pour la vraie date.
   Le module Éclairage est fourni par window.JarvisLumieres (assets/demos/lumieres.js), s'il est présent. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="env"]');
  var dataEl = document.getElementById("env-data");
  if (!root || !dataEl) return;
  var app = root.querySelector("[data-ev-app]");
  var dlg = root.querySelector("[data-ev-dlg]");
  var toastEl = root.querySelector("[data-ev-toast]");
  var D = JSON.parse(dataEl.textContent);
  var API = (document.documentElement.getAttribute("data-api") || "").replace(/\/$/, "");
  var mq = window.matchMedia ? matchMedia("(prefers-reduced-motion: reduce)") : null;
  function reduce() { return !!(mq && mq.matches); }
  var NB = " ";
  var E = {};
  D.envs.forEach(function (e) { E[e.key] = e; });

  /* ======================================================================================
     Outils : nombres, texte, temps local (America/Toronto), hasard reproductible, courbes
     ====================================================================================== */
  function nf(v, d) {
    var s = (d ? Number(v).toFixed(d) : String(Math.round(v))).replace(".", ",");
    if (s === "-0" || s === "-0,0") s = s.slice(1);
    return s.charAt(0) === "-" ? "−" + s.slice(1) : s;
  }
  function deg(v, d) { return nf(v, d) + NB + "°C"; }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function rng(seed) {
    var a = (seed >>> 0) || 1;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  var uidN = 0;
  function uid() { return "ev" + (++uidN); }
  function fmtW(w) { var a = Math.abs(w); return a >= 1000 ? nf(w / 1000, a >= 10000 ? 0 : 1) + NB + "kW" : nf(w) + NB + "W"; }

  var TZ = "America/Toronto";
  var DTF = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, hourCycle: "h23", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric" });
  function NOW() { return Date.now(); }
  function lp(t) {
    var o = {};
    DTF.formatToParts(new Date(t)).forEach(function (p) { o[p.type] = p.value; });
    return { y: +o.year, m: +o.month, d: +o.day, h: (+o.hour) % 24, mi: +o.minute };
  }
  function tzo(t) { var p = lp(t); return (Date.UTC(p.y, p.m - 1, p.d, p.h, p.mi) - Math.floor(t / 60000) * 60000) / 60000; }
  function midnight(t) { var p = lp(t), base = Date.UTC(p.y, p.m - 1, p.d); return base - tzo(base - tzo(t) * 60000) * 60000; }
  function dayAt(d, hmS) {
    var m = midnight(midnight(NOW()) + d * 864e5 + 5 * 3600e3), x = String(hmS || "00:00").split(":");
    return m + (+x[0]) * 3600e3 + (+(x[1] || 0)) * 60e3;
  }
  var JOURS = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];
  var JC = ["Dim.", "Lun.", "Mar.", "Mer.", "Jeu.", "Ven.", "Sam."];
  var MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  function wd(t) { var p = lp(t); return new Date(Date.UTC(p.y, p.m - 1, p.d)).getUTCDay(); }
  function hm(t) { var p = lp(t); return p.h + NB + "h" + NB + pad(p.mi); }
  function hh(h) { return h + NB + "h"; }
  function dnum(p) { return p.d + (p.d === 1 ? "er" : ""); }
  function dateLong(t) { var p = lp(t); return JOURS[wd(t)] + " " + dnum(p) + " " + MOIS[p.m - 1]; }
  function dateShort(t) { var p = lp(t); return dnum(p) + " " + MOIS[p.m - 1]; }
  function dayDiff(t) { return Math.round((midnight(t) - midnight(NOW())) / 864e5); }
  function rel(t) {
    var d = dayDiff(t);
    return d === 0 ? "aujourd’hui" : d === 1 ? "demain" : d === -1 ? "hier" : d > 1 && d < 7 ? JOURS[wd(t)] : dateLong(t);
  }
  function relAt(t) { return cap(rel(t)) + " · " + hm(t); }
  function lc1(s) { return s.charAt(0).toLowerCase() + s.slice(1); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function dur(ms) {
    var m = Math.max(0, Math.round(ms / 60000)), d = Math.floor(m / 1440), h = Math.floor((m % 1440) / 60), mi = m % 60;
    if (d) return d + NB + "j" + NB + h + NB + "h";
    if (h) return h + NB + "h" + NB + pad(mi);
    return mi + NB + "min";
  }
  function ago(min) {
    min = Math.max(0, min);
    if (min < 1) return "à l’instant";
    if (min < 60) return "il y a " + Math.round(min) + NB + "min";
    if (min < 1440) return "il y a " + Math.floor(min / 60) + NB + "h";
    return "il y a " + Math.round(min / 1440) + NB + "j";
  }
  function stamp(minAgo) {
    var t = NOW() - minAgo * 60000, d = dayDiff(t);
    return (d === 0 ? "Aujourd’hui" : d === -1 ? "Hier" : cap(dateShort(t))) + " · " + hm(t);
  }

  function f2(p) { return p[0].toFixed(1) + " " + p[1].toFixed(1); }
  /* Courbe lisse passant par les points (Catmull-Rom) */
  function sp(pts, closed, k) {
    k = k == null ? 1 : k;
    var n = pts.length;
    if (n < 2) return "";
    var P = function (i) { return closed ? pts[(i + n) % n] : pts[clamp(i, 0, n - 1)]; };
    var d = "M" + f2(pts[0]), last = closed ? n : n - 1;
    for (var i = 0; i < last; i++) {
      var p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
      d += " C" + f2([p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k]) + " " +
        f2([p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k]) + " " + f2(p2);
    }
    return d + (closed ? " Z" : "");
  }
  function pol(cx, cy, r, a) { var t = (a - 90) * Math.PI / 180; return [cx + r * Math.cos(t), cy + r * Math.sin(t)]; }
  function arcD(cx, cy, r, a0, a1) {
    var p0 = pol(cx, cy, r, a0), p1 = pol(cx, cy, r, a1);
    return "M" + f2(p0) + " A" + r + " " + r + " 0 " + (a1 - a0 > 180 ? 1 : 0) + " 1 " + f2(p1);
  }

  /* ======================================================================================
     Icônes (grille 24, trait 1,5) et pictogrammes météo en couleur
     ====================================================================================== */
  var I = {
    grid: '<rect x="4" y="4" width="6.75" height="6.75" rx="1.75"/><rect x="13.25" y="4" width="6.75" height="6.75" rx="1.75"/><rect x="4" y="13.25" width="6.75" height="6.75" rx="1.75"/><rect x="13.25" y="13.25" width="6.75" height="6.75" rx="1.75"/>',
    bulb: '<path d="M9.5 18h5M10.5 21h3"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.1v.1h5v-.1c0-.8.4-1.5 1.1-2.1A6 6 0 0 0 12 3Z"/>',
    thermo: '<path d="M10 14.3V5.2a2 2 0 0 1 4 0v9.1a4 4 0 1 1-4 0Z"/><path d="M12 9.5v7"/>',
    bolt: '<path d="M13 2.75 5.5 13.25H12l-1 8 7.5-10.5H12z"/>',
    drop: '<path d="M12 3.5s-6 6.4-6 10.9a6 6 0 0 0 12 0C18 9.9 12 3.5 12 3.5Z"/>',
    shield: '<path d="M12 3.5 19 6v5.5c0 4.4-2.9 7.6-7 9-4.1-1.4-7-4.6-7-9V6z"/><path d="m9 12 2.2 2.2L15.2 10"/>',
    wifi: '<path d="M3 9.25a13 13 0 0 1 18 0M6 12.75a8.5 8.5 0 0 1 12 0M9 16.25a4 4 0 0 1 6 0"/><path d="M12 19.75v.1"/>',
    cube: '<path d="M12 3 4.25 7.5v9L12 21l7.75-4.5v-9z"/><path d="M4.25 7.5 12 12l7.75-4.5M12 12v9"/>',
    wrench: '<path d="M14.6 6.4a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.4-3.4a5.75 5.75 0 0 1-7.6 7.6l-6.6 6.6a2.1 2.1 0 0 1-3-3l6.6-6.6a5.75 5.75 0 0 1 7.6-7.6z"/>',
    sparkle: '<path d="M11 3.5c.6 4 2.5 5.9 6.5 6.5-4 .6-5.9 2.5-6.5 6.5-.6-4-2.5-5.9-6.5-6.5 4-.6 5.9-2.5 6.5-6.5Z"/><path d="M18 14.5c.3 1.7 1 2.4 2.7 2.7-1.7.3-2.4 1-2.7 2.7-.3-1.7-1-2.4-2.7-2.7 1.7-.3 2.4-1 2.7-2.7Z"/>',
    map: '<path d="M9 4.75 3.75 6.5v12.75L9 17.5l6 1.75 5.25-1.75V4.75L15 6.5z"/><path d="M9 4.75V17.5M15 6.5v12.75"/>',
    pin: '<path d="M12 20.5s-6.25-5.4-6.25-10.6a6.25 6.25 0 0 1 12.5 0c0 5.2-6.25 10.6-6.25 10.6Z"/><circle cx="12" cy="9.9" r="2.3"/>',
    battery: '<rect x="3" y="7" width="16" height="10" rx="2.25"/><path d="M21.25 10.5v3"/><path d="M6.5 10.25v3.5M9.5 10.25v3.5M12.5 10.25v3.5"/>',
    sun: '<circle cx="12" cy="12" r="3.75"/><path d="M12 2.75v2M12 19.25v2M2.75 12h2M19.25 12h2M5.45 5.45l1.4 1.4M17.15 17.15l1.4 1.4M5.45 18.55l1.4-1.4M17.15 6.85l1.4-1.4"/>',
    moon: '<path d="M19 14.6A7.5 7.5 0 0 1 9.4 5a7.5 7.5 0 1 0 9.6 9.6Z"/>',
    cloud: '<path d="M7.25 18.5h9.5a4 4 0 0 0 .55-7.95 5.5 5.5 0 0 0-10.6 1.35 3.3 3.3 0 0 0 .55 6.6Z"/>',
    cloudsun: '<path d="M10 2.75v1.5M4.2 5.2l1.05 1.05M15.8 5.2l-1.05 1.05M2.75 11h1.5"/><path d="M6.6 10.3a3.75 3.75 0 0 1 6.9-2"/><path d="M9 20h8.25a3.4 3.4 0 0 0 .45-6.77 4.6 4.6 0 0 0-8.85 1.13A2.85 2.85 0 0 0 9 20Z"/>',
    snowflake: '<path d="M12 2.75v18.5M3.99 7.38l16.02 9.24M3.99 16.62l16.02-9.24"/><path d="m9.5 4.25 2.5 2 2.5-2M9.5 19.75l2.5-2 2.5 2"/>',
    wind: '<path d="M3 8.5h11a2.5 2.5 0 1 0-2.5-2.5M3 12.5h15a2.5 2.5 0 1 1-2.5 2.5M3 16.5h8"/>',
    home: '<path d="M4.5 10.2 12 4l7.5 6.2V19a1 1 0 0 1-1 1h-4v-5.5h-5V20h-4a1 1 0 0 1-1-1z"/>',
    fan: '<circle cx="12" cy="12" r="1.6"/><path d="M12 10.4c-1-3.4.3-6.4 2.6-6.4 2.4 0 2.6 3.4-.9 6.6M13.6 12c3.4-1 6.4.3 6.4 2.6 0 2.4-3.4 2.6-6.6-.9M12 13.6c1 3.4-.3 6.4-2.6 6.4-2.4 0-2.6-3.4.9-6.6M10.4 12c-3.4 1-6.4-.3-6.4-2.6 0-2.4 3.4-2.6 6.6.9"/>',
    leaf: '<path d="M5.5 19C5 11 9.5 5.5 19.5 4.5 19 14 14 19 6 19.5"/><path d="m5.5 19 8-8"/>',
    fridge: '<rect x="6" y="2.75" width="12" height="18.5" rx="2"/><path d="M6 10h12M9 6v1.75M9 12.75v3"/>',
    plug: '<path d="M9 3v5M15 3v5M6.5 8h11v3.5a5.5 5.5 0 0 1-11 0zM12 17v4"/>',
    alt: '<circle cx="12" cy="12" r="6.25"/><circle cx="12" cy="12" r="2.25"/><path d="M12 2.75v3M12 18.25v3M2.75 12h3M18.25 12h3"/>',
    chart: '<path d="M5 20v-7M10 20V6M15 20v-9M20 20v-4"/>',
    clock: '<circle cx="12" cy="12" r="8.25"/><path d="M12 7.5V12l3 2"/>',
    calendar: '<rect x="3.75" y="5" width="16.5" height="15" rx="2.5"/><path d="M3.75 9.75h16.5M8 3v4M16 3v4"/>',
    lock: '<rect x="5" y="10.5" width="14" height="10" rx="2.25"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    unlock: '<rect x="5" y="10.5" width="14" height="10" rx="2.25"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 6.8-1.2"/>',
    check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    x: '<path d="m6.5 6.5 11 11M17.5 6.5l-11 11"/>',
    right: '<path d="m9.5 6 6 6-6 6"/>',
    left: '<path d="m14.5 6-6 6 6 6"/>',
    up: '<path d="m6 14.5 6-6 6 6"/>',
    down: '<path d="m6 9.5 6 6 6-6"/>',
    back: '<path d="M19.5 12h-15M10.5 6l-6 6 6 6"/>',
    edit: '<path d="M4.5 19.5h4l10-10a2.8 2.8 0 0 0-4-4l-10 10z"/><path d="m13.5 6.5 4 4"/>',
    bell: '<path d="M6.5 16.5v-5a5.5 5.5 0 0 1 11 0v5l1.5 1.75H5z"/><path d="M10 20.75a2.3 2.3 0 0 0 4 0"/>',
    camera: '<rect x="3.5" y="7" width="12.5" height="10" rx="2.25"/><path d="m16 10.5 4.5-2.5v8L16 13.5"/>',
    door: '<path d="M6 21V4.5a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1V21M4 21h16"/><path d="M14.5 12.5v.1"/>',
    warn: '<path d="M12 4 2.75 19.75h18.5z"/><path d="M12 10v4.5M12 17.25v.1"/>',
    info: '<circle cx="12" cy="12" r="8.25"/><path d="M12 11v5"/><path d="M12 7.9v.1"/>',
    fire: '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.2 0-3.6 2.7-5.4 3.7-8.8 1.9 1.4 2.4 3.3 2.4 4.6 1-.6 1.7-1.8 1.8-3 2.4 1.9 5.1 4.5 5.1 7.4 0 3.4-2.6 6-6.5 6Z"/>',
    flame: '<path d="M12 21a5 5 0 0 1-5-5c0-3 2.2-4.4 3-7.5 1.6 1.1 2 2.6 2 3.6.8-.5 1.4-1.4 1.5-2.4 2 1.6 3.5 3.6 3.5 6.3a5 5 0 0 1-5 5Z"/><path d="M12 21a2 2 0 0 1-2-2c0-1.2.9-1.8 2-3.2 1.1 1.4 2 2 2 3.2a2 2 0 0 1-2 2Z"/>',
    tank: '<rect x="6.5" y="6" width="11" height="15" rx="4"/><path d="M9.5 6V3.5h5V6M6.5 11h11"/>',
    tap: '<path d="M4 9.5h9a3 3 0 0 1 3 3V14M4 13h6"/><path d="M8 9.5V6.5M5.5 6.5h5"/><path d="M16 17.5s-1.5 1.7-1.5 2.6a1.5 1.5 0 0 0 3 0c0-.9-1.5-2.6-1.5-2.6Z"/>',
    shower: '<path d="M5 21V8a4 4 0 0 1 7.5-2"/><path d="M10.5 7.5a4.5 4.5 0 0 1 8 0z"/><path d="M12 11v.1M15 11.5v.1M18 11v.1M13 14v.1M16.5 14.5v.1"/>',
    pump: '<circle cx="10" cy="13" r="6.25"/><path d="M16.25 13h4.25M10 6.75V3.5h4"/><path d="M10 10s-2 2.2-2 3.4a2 2 0 0 0 4 0C12 12.2 10 10 10 10Z"/>',
    antenna: '<path d="M12 11v10M9 21h6"/><circle cx="12" cy="9" r="1.6"/><path d="M8.3 5.3a5.25 5.25 0 0 0 0 7.4M15.7 5.3a5.25 5.25 0 0 1 0 7.4M5.6 2.6a9 9 0 0 0 0 12.8M18.4 2.6a9 9 0 0 1 0 12.8"/>',
    satellite: '<path d="M4 10.5a9.5 9.5 0 0 0 9.5 9.5"/><path d="M5.25 8.25a10.5 10.5 0 0 0 10.5 10.5z"/><path d="m10.5 13.5 4.25-4.25M17 4a3 3 0 0 1 3 3M16.5 1.75A5.75 5.75 0 0 1 22.25 7.5"/>',
    router: '<rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 16.5h.1M10.5 16.5h.1M8.5 9.5a5 5 0 0 1 7 0M6 7a8.5 8.5 0 0 1 12 0"/>',
    phone: '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 17.75h2"/>',
    laptop: '<rect x="5" y="5" width="14" height="10" rx="1.5"/><path d="M3 19h18"/>',
    tv: '<rect x="3" y="4.5" width="18" height="12" rx="1.5"/><path d="M8 20.5h8M12 16.5v4"/>',
    cpu: '<rect x="6.5" y="6.5" width="11" height="11" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx=".5"/><path d="M9.5 3v3.5M14.5 3v3.5M9.5 17.5V21M14.5 17.5V21M3 9.5h3.5M3 14.5h3.5M17.5 9.5H21M17.5 14.5H21"/>',
    mem: '<rect x="3" y="7" width="18" height="10" rx="1.5"/><path d="M7 10.5v3M11 10.5v3M15 10.5v3M6.5 17v2.25M17.5 17v2.25"/>',
    disk: '<rect x="5" y="3.5" width="14" height="17" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M8.5 17h7"/>',
    db: '<ellipse cx="12" cy="6" rx="7" ry="2.75"/><path d="M5 6v12c0 1.5 3.1 2.75 7 2.75s7-1.25 7-2.75V6M5 12c0 1.5 3.1 2.75 7 2.75S19 13.5 19 12"/>',
    refresh: '<path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/><path d="M19.5 4.5v4h-4"/>',
    list: '<path d="M9 7h11M9 12h11M9 17h11M4.5 7h.1M4.5 12h.1M4.5 17h.1"/>',
    clip: '<rect x="5.5" y="4.5" width="13" height="16.5" rx="2"/><path d="M9 4.5V3.25h6V4.5M9 10.5h6M9 14h6M9 17.5h3.5"/>',
    cart: '<path d="M3 4h2.5l2.2 11h10.6l2-8H6.5"/><circle cx="9" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/>',
    tent: '<path d="M2.75 19.75 12 6.25l9.25 13.5z"/><path d="M12 6.25 9 19.75M12 6.25l3 13.5"/><path d="M12 6.25V3.25l3 1.3-3 1.2"/>',
    road: '<path d="M7.5 20.5 10 3.5M16.5 20.5 14 3.5M12 6v1.75M12 11v1.75M12 16v1.75"/>',
    route: '<circle cx="6" cy="18" r="2.25"/><circle cx="18" cy="6" r="2.25"/><path d="M8.25 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.75"/>',
    car: '<path d="M5 16.5h14v-4l-2-5H7l-2 5z"/><path d="M5 12.5h14M6.5 16.5v2M17.5 16.5v2"/>',
    rv: '<rect x="2.5" y="6" width="19" height="10.5" rx="2"/><path d="M2.5 10.75h19M7.5 6v4.75M12.5 6v4.75M17.5 6v4.75"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    boat: '<path d="M12 3v13M12 4.25l6 9.75h-6M12 7l-4.5 7H12"/><path d="M3.5 17h17l-2.5 3.5H6z"/>',
    plane: '<path d="M12 3c.9 0 1.5.9 1.5 2v4.5l7 4v2l-7-2v4l2 1.5v1.5l-3.5-1-3.5 1V19.5l2-1.5v-4l-7 2v-2l7-4V5c0-1.1.6-2 1.5-2Z"/>',
    barn: '<path d="M3.5 21V10L12 4l8.5 6v11z"/><path d="M8.5 21v-6.5h7V21M8.5 14.5l7 6.5M15.5 14.5 8.5 21M10 9.5h4"/>',
    anchor: '<circle cx="12" cy="5" r="2"/><path d="M12 7v14M8 11h8M4.5 13.5A7.5 7.5 0 0 0 12 21a7.5 7.5 0 0 0 7.5-7.5"/>',
    step: '<path d="M3 20h5v-5h5v-5h5V5h3"/>',
    awning: '<path d="M3 5.5h18v3H3zM4 8.5l1.5 4h13L20 8.5"/><path d="M6 12.5V20M18 12.5V20"/>',
    jacks: '<path d="M3 8h18M6 8v9M18 8v9M4.5 17h3M16.5 17h3"/><path d="M9 8V5h6v3"/>',
    compress: '<rect x="3.5" y="9" width="12" height="9" rx="4.5"/><path d="M15.5 13.5H20M18 11v5"/><circle cx="7" cy="20" r="1"/><circle cx="12" cy="20" r="1"/><path d="M9.5 9V6h3"/>',
    evcharge: '<rect x="4" y="3.5" width="9" height="17" rx="1.5"/><path d="M9.25 7.5 7.25 11h3l-2 3.5M13 9h2.5a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V8l-2-2"/>',
    garage: '<path d="M3 21V9l9-5 9 5v12"/><path d="M6.5 21v-9h11v9M6.5 15h11M6.5 18h11"/>',
    fireplace: '<path d="M3 4h18v3H3zM5 7v14h14V7"/><path d="M12 19c-2 0-3-1.2-3-2.6 0-1.6 1.4-2.3 2-4 1.4 1 3.9 2.4 3.9 4 0 1.5-1 2.6-2.9 2.6Z"/>',
    spa: '<path d="M3 12h18v5a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3z"/><path d="M8 9c-1-1.5 1-2.5 0-4M12 9c-1-1.5 1-2.5 0-4M16 9c-1-1.5 1-2.5 0-4"/>',
    pool: '<path d="M3 17c1.5 0 1.5 1 3 1s1.5-1 3-1 1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1M3 13.5c1.5 0 1.5 1 3 1s1.5-1 3-1 1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1"/><path d="M8 13V5.5a2 2 0 0 1 4 0M14 13V5.5a2 2 0 0 1 4 0M8 8.5h6"/>',
    eye: '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/>',
    play: '<path d="M8.5 5.75v12.5L18.5 12z"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    minus: '<path d="M5 12h14"/>',
    star: '<path d="m12 4 2.4 5 5.35.65-3.95 3.7 1.05 5.35L12 16.05 7.15 18.7l1.05-5.35-3.95-3.7L9.6 9z"/>',
    fuel: '<path d="M4.5 21V5a1.5 1.5 0 0 1 1.5-1.5h6A1.5 1.5 0 0 1 13.5 5v16M3 21h12M4.5 10h9"/><path d="M13.5 8h2a2 2 0 0 1 2 2v6a1.5 1.5 0 0 0 3 0V8.5L18 6"/>',
    dump: '<rect x="4" y="3.5" width="16" height="9" rx="2"/><path d="M12 12.5v7.5M8.75 17l3.25 3 3.25-3"/>',
    waves: '<path d="M3 8c2 0 2-1.5 4.5-1.5S9.5 8 12 8s2.5-1.5 4.5-1.5S19 8 21 8M3 13c2 0 2-1.5 4.5-1.5S9.5 13 12 13s2.5-1.5 4.5-1.5S19 13 21 13M3 18c2 0 2-1.5 4.5-1.5S9.5 18 12 18s2.5-1.5 4.5-1.5S19 18 21 18"/>',
    sliders: '<path d="M4 7h9M17 7h3M4 12h3M11 12h9M4 17h11M19 17h1"/><path d="M15 5v4M9 10v4M17 15v4"/>',
    users: '<circle cx="9" cy="8.75" r="3.25"/><path d="M3 19.5c.7-3.1 3-4.75 6-4.75s5.3 1.65 6 4.75"/><path d="M15.5 5.75a3.25 3.25 0 0 1 0 6M17.5 14.9c1.9.5 3.1 2 3.5 4.6"/>',
    key: '<circle cx="8" cy="15" r="3.75"/><path d="m10.7 12.3 8.3-8.3M16 7l2.5 2.5M14 9l1.75 1.75"/>',
    power: '<path d="M12 3v8.5"/><path d="M7 6.2a7.5 7.5 0 1 0 10 0"/>',
    co: '<rect x="3.5" y="5" width="17" height="14" rx="3"/><path d="M10.75 10.1a2.1 2.1 0 1 0 0 3.8M15 9.9a2.1 2.1 0 1 1 0 4.2 2.1 2.1 0 0 1 0-4.2Z"/>',
    smoke: '<path d="M7 17.5h10a3.5 3.5 0 0 0 .4-7A5 5 0 0 0 7.8 11.6 3 3 0 0 0 7 17.5Z"/><path d="M8.5 21h7"/>',
    radar: '<circle cx="12" cy="12" r="2"/><path d="M7.75 7.75a6 6 0 0 0 0 8.5M16.25 7.75a6 6 0 0 1 0 8.5M5 5a10 10 0 0 0 0 14M19 5a10 10 0 0 1 0 14"/>',
    hydro: '<path d="M12 3 7 21M12 3l5 18M8.4 15.5h7.2M9.6 11h4.8M5 7h14M7.5 7 12 11l4.5-4"/>',
    solar: '<path d="M5 5h14l2 10H3z"/><path d="M4 10h16M10 5l-1 10M14 5l1 10M12 15v5M8 20h8"/>',
    gen: '<rect x="3" y="7" width="18" height="11" rx="2"/><path d="M12.5 9.5 10 13h3.5L11 16.5M6 7V5h4v2M6 18v2M18 18v2"/>',
    inverter: '<rect x="4" y="4" width="16" height="16" rx="2.5"/><path d="M7 12c1.2-2.7 2.8-2.7 4 0s2.8 2.7 4 0M15.5 8h2M6.5 16h2"/>',
    sunrise: '<path d="M3 18.5h18M7.5 18.5a4.5 4.5 0 0 1 9 0M12 3.5v5.5M9.5 6l2.5-2.5L14.5 6M4.5 12l1.4 1M19.5 12l-1.4 1"/>',
    sunset: '<path d="M3 18.5h18M7.5 18.5a4.5 4.5 0 0 1 9 0M12 3.5v5.5M9.5 6.5 12 9l2.5-2.5M4.5 12l1.4 1M19.5 12l-1.4 1"/>',
    gauge: '<path d="M4.5 17a8 8 0 1 1 15 0"/><path d="m12 13.5 3.75-4"/><circle cx="12" cy="13.5" r="1.4"/>',
    arrdown: '<path d="M12 4.5v15M6.5 14l5.5 5.5 5.5-5.5"/>',
    arrup: '<path d="M12 19.5v-15M6.5 10 12 4.5l5.5 5.5"/>',
    bed: '<path d="M3 19V6.5M3 15h18v4M21 15v-2.5A2.5 2.5 0 0 0 18.5 10H11v5"/><circle cx="7" cy="11.5" r="1.9"/>',
    compass: '<circle cx="12" cy="12" r="8.25"/><path d="m15.5 8.5-2.2 4.8-4.8 2.2 2.2-4.8z"/>',
    nav: '<path d="M4 11.2 20 4l-7.2 16-1.9-6.9z"/>',
    percent: '<path d="M18 6 6 18"/><circle cx="7.5" cy="7.5" r="2.25"/><circle cx="16.5" cy="16.5" r="2.25"/>',
    silo: '<path d="M6 21V8a6 4 0 0 1 12 0v13M4 21h16M6 12h12M6 16h12"/>',
    fence: '<path d="M5 21V6l2-2 2 2v15M15 21V6l2-2 2 2v15M3 10h18M3 16h18"/>',
    window: '<rect x="4.5" y="3.5" width="15" height="17" rx="1.5"/><path d="M12 3.5v17M4.5 12h15"/>',
    heater: '<rect x="6" y="3" width="12" height="17" rx="3"/><path d="M9 20v1.5M15 20v1.5M10 9.5c.9-1 .9-2 0-3M14 9.5c.9-1 .9-2 0-3M9 14h6"/>',
    valve: '<path d="M3 15h4l3-3h4l3 3h4M3 11v8M21 11v8M12 12V6M8.5 6h7"/>',
    engine: '<path d="M3.5 10v6M3.5 13h2.5M6 9h3V7h5v2h2l2 2h2.5v6H18l-2 2H9l-3-3z"/>',
    prop: '<circle cx="12" cy="12" r="1.8"/><path d="M12 10.2C11 6 11.2 3 12 3s1 3 0 7.2M12 13.8c1 4.2.8 7.2 0 7.2s-1-3 0-7.2"/>',
    hangar: '<path d="M2.5 20v-8a9.5 7 0 0 1 19 0v8z"/><path d="M7 20v-6.5h10V20M2.5 20h19"/>',
    wheel: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3"/><path d="M12 3.5V9M12 15v5.5M3.5 12H9M15 12h5.5"/>',
    box: '<path d="M3.5 8 12 4l8.5 4v8L12 20l-8.5-4z"/><path d="M3.5 8 12 12l8.5-4M12 12v8"/>',
    height: '<path d="M12 3.5v17M8.5 7 12 3.5 15.5 7M8.5 17l3.5 3.5 3.5-3.5M5 3.5h14M5 20.5h14"/>',
    cone: '<path d="M10 4h4l4.5 15h-13z"/><path d="M8.5 9.5h7M7 14.5h10M3.5 19h17"/>',
    dots: '<path d="M6 12h.1M12 12h.1M18 12h.1"/>',
    doc: '<path d="M7 3.5h6.5L18 8v12.5H7z"/><path d="M13.5 3.5V8H18M9.75 12.5h5.5M9.75 16h5.5"/>',
    gear: '<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.2M12 18.3v2.2M3.5 12h2.2M18.3 12h2.2M6 6l1.55 1.55M16.45 16.45 18 18M6 18l1.55-1.55M16.45 7.55 18 6"/>',
    link: '<path d="M10.5 13.5a3.75 3.75 0 0 0 5.3 0l3-3a3.75 3.75 0 0 0-5.3-5.3l-1 1"/><path d="M13.5 10.5a3.75 3.75 0 0 0-5.3 0l-3 3a3.75 3.75 0 0 0 5.3 5.3l1-1"/>',
    swap: '<path d="M4 8h14.5M15 4.5 18.5 8 15 11.5M20 16H5.5M9 12.5 5.5 16 9 19.5"/>',
    users2: '<circle cx="12" cy="8.5" r="3.75"/><path d="M4.75 20c.9-3.6 3.75-5.5 7.25-5.5s6.35 1.9 7.25 5.5"/>',
    trough: '<path d="M3 9h18l-2 8.5H5z"/><path d="M6 13h12M7 17.5V21M17 17.5V21"/>',
    milk: '<path d="M8.5 3h7M9.5 3v3L7.5 9v12h9V9l-2-3V3M7.5 13.5h9"/>',
    tree: '<path d="M12 3 6.5 10.5h3l-4 6h13l-4-6h3zM12 16.5V21"/>',
    parking: '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M10 16.5v-9h3a2.75 2.75 0 0 1 0 5.5h-3"/>',
    truck: '<path d="M3 6h11v10H3zM14 9.5h4l3 3.5V16h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    city: '<path d="M3.5 20.5h17M5.5 20.5V9.5l6-3.5v14.5M11.5 10l7 2.75v7.75"/><path d="M8.25 10.5v.1M8.25 13.5v.1M8.25 16.5v.1M15 14.75v.1M15 17.5v.1"/>',
    brief: '<rect x="3.5" y="7.5" width="17" height="12" rx="2.25"/><path d="M9 7.5V6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 6v1.5M3.5 12.5h17"/>',
    blinds: '<path d="M4 4h16M5 4v13M19 4v13M5 7.5h14M5 11h14M5 14.5h14M12 17v3"/>',
    speaker: '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>'
  };
  function ic(n, c) { return '<svg class="ev-i' + (c ? " " + c : "") + '" viewBox="0 0 24 24" aria-hidden="true">' + (I[n] || I.info) + "</svg>"; }

  /* Pictogrammes météo en couleur (48 × 48) : d dégagé, p partiel, c couvert, r pluie, w neige, f brouillard.
     Dégradés communs (soleil, nuage, lune, cadran du thermostat) déclarés une seule fois dans le document. */
  var DEFS = '<svg class="ev-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' +
    '<radialGradient id="evw-sun" cx="40%" cy="36%" r="70%"><stop offset="0" stop-color="#fff6d2"/><stop offset=".45" stop-color="#ffd25c"/><stop offset="1" stop-color="#f59a1f"/></radialGradient>' +
    '<radialGradient id="evw-halo" cx="50%" cy="50%" r="50%"><stop offset=".35" stop-color="#ffc24a" stop-opacity=".55"/><stop offset="1" stop-color="#ffc24a" stop-opacity="0"/></radialGradient>' +
    '<linearGradient id="evw-cloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#dfe5ec"/><stop offset="1" stop-color="#a9b4c1"/></linearGradient>' +
    '<linearGradient id="evw-cloud2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9d1dc"/><stop offset="1" stop-color="#6f7c8c"/></linearGradient>' +
    '<radialGradient id="evw-moon" cx="38%" cy="34%" r="72%"><stop offset="0" stop-color="#fffaf0"/><stop offset=".7" stop-color="#e3dac4"/><stop offset="1" stop-color="#a99f88"/></radialGradient>' +
    '<linearGradient id="evw-drop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd0ff"/><stop offset="1" stop-color="#3d8ff0"/></linearGradient>' +
    '<linearGradient id="evd-bezel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a4a4a"/><stop offset=".22" stop-color="#1b1b1b"/><stop offset=".55" stop-color="#0a0a0a"/><stop offset=".8" stop-color="#2b2b2b"/><stop offset="1" stop-color="#101010"/></linearGradient>' +
    '<radialGradient id="evd-face" cx="50%" cy="38%" r="70%"><stop offset="0" stop-color="#1a1918"/><stop offset=".7" stop-color="#070707"/><stop offset="1" stop-color="#000"/></radialGradient>' +
    '<linearGradient id="evd-glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>' +
    '<linearGradient id="evd-heat" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ffb347"/><stop offset=".6" stop-color="#ff8a3d"/><stop offset="1" stop-color="#ff5f3d"/></linearGradient>' +
    '<linearGradient id="evd-cool" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#7cc4ff"/><stop offset="1" stop-color="#3d8ff0"/></linearGradient>' +
    '<linearGradient id="evd-hold" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#6ee7b7"/><stop offset="1" stop-color="#34d399"/></linearGradient>' +
    "</defs></svg>";
  root.insertAdjacentHTML("afterbegin", DEFS);
  var WXC = {
    halo: '<circle cx="24" cy="24" r="17" fill="url(#evw-halo)" class="w-halo"/>',
    sun: '<g class="w-rays"><path class="w-ray" d="M24 6.5v4M24 37.5v4M6.5 24h4M37.5 24h4M11.6 11.6l2.8 2.8M33.6 33.6l2.8 2.8M11.6 36.4l2.8-2.8M33.6 14.4l2.8-2.8"/></g><circle cx="24" cy="24" r="8.6" fill="url(#evw-sun)" class="w-sun"/>',
    moon: '<path class="w-moon" fill="url(#evw-moon)" d="M31 30.5A12 12 0 0 1 19.5 13.5a12 12 0 1 0 11.5 17Z"/>',
    cloud: '<path class="w-cloud" fill="url(#evw-cloud)" d="M15 37h19a7.5 7.5 0 0 0 1.1-14.9 10.5 10.5 0 0 0-20.1 2.4A6.3 6.3 0 0 0 15 37Z"/>',
    cloudd: '<path class="w-cloud" fill="url(#evw-cloud2)" d="M15 33h19a7.5 7.5 0 0 0 1.1-14.9 10.5 10.5 0 0 0-20.1 2.4A6.3 6.3 0 0 0 15 33Z"/>',
    sunsmall: '<g class="w-rays"><path class="w-ray" d="M18 5v3.5M5 18h3.5M8.8 8.8l2.4 2.4M27.2 8.8l-2.4 2.4"/></g><circle cx="18" cy="18" r="7" fill="url(#evw-sun)" class="w-sun"/>',
    moonsmall: '<path class="w-moon" fill="url(#evw-moon)" d="M25 22A9 9 0 0 1 16.5 9.5a9 9 0 1 0 8.5 12.5Z"/>',
    cloudlow: '<path class="w-cloud w-drift" fill="url(#evw-cloud)" d="M17 40h17a7 7 0 0 0 1-13.9 9.5 9.5 0 0 0-18.2 2.2A5.8 5.8 0 0 0 17 40Z"/>',
    rain: '<path class="w-rain" d="M18 38l-2 4.5M25 38l-2 4.5M32 38l-2 4.5"/>',
    snow: '<g class="w-snow"><circle cx="17" cy="40" r="1.7"/><circle cx="24" cy="43" r="1.7"/><circle cx="31" cy="40" r="1.7"/></g>',
    fog: '<path class="w-fog" d="M10 30h28M13 35h22M10 40h28"/>'
  };
  function wxi(code, night, cls) {
    var b = "";
    if (code === "d") b = night ? WXC.moon : WXC.halo + WXC.sun;
    else if (code === "p") b = (night ? WXC.moonsmall : WXC.sunsmall) + WXC.cloudlow;
    else if (code === "c") b = WXC.cloud;
    else if (code === "r") b = WXC.cloudd + WXC.rain;
    else if (code === "w") b = WXC.cloudd + WXC.snow;
    else if (code === "f") b = WXC.cloud.replace("37h", "26h") + WXC.fog;
    return '<svg class="ev-wx' + (cls ? " " + cls : "") + '" viewBox="0 0 48 48" aria-hidden="true">' + b + "</svg>";
  }
  var WXN = { d: "Dégagé", p: "Ciel variable", c: "Nuageux", r: "Pluie", w: "Neige", f: "Brouillard" };
  var ICON2CODE = { sun: "d", cloudsun: "p", cloud: "c", rain: "r", snow: "w", fog: "f", moon: "d" };

  /* ======================================================================================
     Astronomie : position du soleil, lever, coucher, crépuscules et phase de la lune
     ====================================================================================== */
  var RAD = Math.PI / 180;
  function sunAt(t, lat, lon) {
    var d = t / 864e5 + 2440587.5 - 2451545.0;
    var g = (357.529 + 0.98560028 * d) * RAD;
    var q = 280.459 + 0.98564736 * d;
    var L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * RAD;
    var eps = (23.439 - 0.00000036 * d) * RAD;
    var ra = Math.atan2(Math.cos(eps) * Math.sin(L), Math.cos(L));
    var dec = Math.asin(Math.sin(eps) * Math.sin(L));
    var gmst = (18.697374558 + 24.06570982441908 * d) % 24;
    var ha = ((gmst * 15 + lon) * RAD - ra);
    var la = lat * RAD;
    var el = Math.asin(Math.sin(la) * Math.sin(dec) + Math.cos(la) * Math.cos(dec) * Math.cos(ha));
    var az = Math.atan2(-Math.sin(ha), Math.tan(dec) * Math.cos(la) - Math.sin(la) * Math.cos(ha));
    return { el: el / RAD, az: (az / RAD + 360) % 360 };
  }
  var sunCache = {};
  function sunDay(e, dayOffset) {
    var m0 = midnight(midnight(NOW()) + (dayOffset || 0) * 864e5 + 5 * 3600e3), k = e.key + m0;
    if (sunCache[k]) return sunCache[k];
    var lat = e.geo.lat, lon = e.geo.lon, step = 120000, prev = sunAt(m0, lat, lon).el, r = { m0: m0, noon: m0, max: -90 };
    function cross(name, lvl, t, a, b) { var x = t - step + step * (lvl - a) / (b - a); r[name] = x; }
    for (var t = m0 + step; t <= m0 + 864e5; t += step) {
      var el = sunAt(t, lat, lon).el;
      if (prev < -0.833 && el >= -0.833) cross("rise", -0.833, t, prev, el);
      if (prev >= -0.833 && el < -0.833) cross("set", -0.833, t, prev, el);
      if (prev < -6 && el >= -6) cross("dawn", -6, t, prev, el);
      if (prev >= -6 && el < -6) cross("dusk", -6, t, prev, el);
      if (el > r.max) { r.max = el; r.noon = t; }
      prev = el;
    }
    return (sunCache[k] = r);
  }
  function moonInfo(t) {
    var syn = 29.530588853, ref = Date.UTC(2000, 0, 6, 18, 14);
    var age = ((t - ref) / 864e5) % syn;
    if (age < 0) age += syn;
    var ph = 2 * Math.PI * age / syn, ill = (1 - Math.cos(ph)) / 2;
    var names = [[1.0, "Nouvelle lune"], [6.4, "Premier croissant"], [8.4, "Premier quartier"], [13.8, "Lune gibbeuse croissante"],
      [15.8, "Pleine lune"], [21.1, "Lune gibbeuse décroissante"], [23.1, "Dernier quartier"], [28.5, "Dernier croissant"], [30, "Nouvelle lune"]];
    var name = names.filter(function (n) { return age < n[0]; })[0][1];
    var toFull = (14.765 - age + syn) % syn, toNew = syn - age;
    return { age: age, ill: ill, ph: ph, name: name, full: t + toFull * 864e5, nw: t + toNew * 864e5, waxing: age < syn / 2 };
  }
  function moonSVG(m, cls) {
    var r = 40, cx = 50, cy = 50, k = Math.cos(m.ph), rx = Math.abs(k) * r;
    var lit;
    if (m.waxing) lit = "M50 10 A40 40 0 0 1 50 90 A" + rx.toFixed(2) + " 40 0 0 " + (k > 0 ? 0 : 1) + " 50 10Z";
    else lit = "M50 10 A40 40 0 0 0 50 90 A" + rx.toFixed(2) + " 40 0 0 " + (k > 0 ? 1 : 0) + " 50 10Z";
    var id = uid();
    return '<svg class="ev-moon ' + (cls || "") + '" viewBox="0 0 100 100" aria-hidden="true"><defs><radialGradient id="' + id + '" cx="40%" cy="38%" r="70%">' +
      '<stop offset="0" style="stop-color:#fbf3dc"/><stop offset=".7" style="stop-color:#d8ccad"/><stop offset="1" style="stop-color:#8f8670"/></radialGradient></defs>' +
      '<circle cx="50" cy="50" r="40" class="m-dark"/><path d="' + lit + '" fill="url(#' + id + ')"/>' +
      '<g class="m-crater"><circle cx="38" cy="36" r="6"/><circle cx="60" cy="58" r="8"/><circle cx="44" cy="66" r="4"/><circle cx="64" cy="32" r="3.5"/></g></svg>';
  }

  /* ======================================================================================
     Modèles d'exemple : température de l'heure, production solaire, consommation
     ====================================================================================== */
  function tempAt(e, t) {
    var p = lp(t), a = e.wx.t24[p.h], b = e.wx.t24[(p.h + 1) % 24];
    return a + (b - a) * p.mi / 60;
  }
  function isNight(e, t) { return sunAt(t, e.geo.lat, e.geo.lon).el < -0.833; }
  function skyAt(e, t) { return e.wx.sky.charAt(lp(t).h) || "p"; }
  function popAt(e, t) { return (+e.wx.p24.charAt(lp(t).h) || 0) * 10; }
  function chill(T, V) {
    if (T > 10 || V < 5) return T;
    var v = Math.pow(V, 0.16);
    return 13.12 + 0.6215 * T - 11.37 * v + 0.3965 * T * v;
  }
  function wxNow(e) {
    var t = NOW(), T = tempAt(e, t), code = skyAt(e, t), night = isNight(e, t);
    var lo = Math.min.apply(null, e.wx.t24), hi = Math.max.apply(null, e.wx.t24);
    return { t: T, code: code, night: night, cond: night && code === "d" ? "Nuit dégagée" : WXN[code], feels: chill(T, e.wx.wind), hi: hi, lo: lo, pop: popAt(e, t) };
  }
  /* Production solaire du jour, au quart d'heure, selon la vraie hauteur du soleil */
  var solCache = {};
  function solarDay(e) {
    var s = e.energy && e.energy.solar;
    if (!s) return null;
    var m0 = midnight(NOW()), k = e.key + m0;
    if (!solCache[k]) {
      var R = rng(hash(e.key) + m0 / 864e5), vals = [], meas = [];
      for (var q = 0; q < 96; q++) {
        var t = m0 + q * 9e5, el = sunAt(t + 4.5e5, e.geo.lat, e.geo.lon).el;
        var inc = Math.sin(clamp(el + (s.tilt || 0), 0, 90) * RAD), atm = el > 0 ? clamp(el / 6, 0, 1) : 0;
        var w = s.peak * inc * atm * (1 - (s.cloud || 0) * 0.7);
        vals.push(Math.max(0, w));
        meas.push(Math.max(0, w * (0.82 + R() * 0.3)));
      }
      solCache[k] = { m0: m0, f: vals, m: meas };
    }
    var c = solCache[k], nowQ = clamp(Math.floor((NOW() - c.m0) / 9e5), 0, 95), total = 0, sofar = 0, i;
    for (i = 0; i < 96; i++) { var v = i <= nowQ ? c.m[i] : c.f[i]; total += v / 4; if (i <= nowQ) sofar += c.m[i] / 4; }
    return { f: c.f, m: c.m, q: nowQ, total: total, sofar: sofar, now: c.m[nowQ] };
  }
  /* Consommation horaire d'exemple : base, matin, journée (bureaux), soirée */
  var loadCache = {};
  function loadCurve(e) {
    if (loadCache[e.key]) return loadCache[e.key];
    var s = e.energy.solar || {}, R = rng(hash(e.key + "c")), out = [], base = s.base || e.energy.load * 0.8;
    for (var h = 0; h < 24; h++) {
      var v = base;
      if (s.day && h >= 8 && h <= 17) v = s.day;
      if (h >= 17 && h <= 22) v = Math.max(v, s.eve || base * 1.4);
      if (h >= 6 && h <= 9) v += base * (s.morn != null ? s.morn : 0.3);
      out.push(v + (R() - 0.5) * base * 0.3);
    }
    return (loadCache[e.key] = out);
  }
  function loadNow(e) { var c = loadCurve(e), p = lp(NOW()); return Math.max(0, c[p.h] + (c[(p.h + 1) % 24] - c[p.h]) * p.mi / 60); }

  /* ======================================================================================
     Batteries réelles de BouLance (service /live du site)
     ====================================================================================== */
  var LIVE = { d: null, ok: null, hist: null, histT: 0, timer: null, busy: false };
  function batColor(soc) { return soc >= 60 ? "#34d399" : soc >= 30 ? "#fbbf24" : "#f87171"; }
  function bat(e) {
    var en = e.energy, capT = en.cap, isLive = !!(en.live && LIVE.ok && LIVE.d);
    if (isLive) {
      var d = LIVE.d, bs = d.batteries.filter(function (b) { return b.soc >= 0; });
      var socAvg = bs.length ? bs.reduce(function (a, b) { return a + b.soc * (b.cap || 1); }, 0) / bs.reduce(function (a, b) { return a + (b.cap || 1); }, 0) : en.soc;
      var tot = d.total || {}, soc = tot.ah > 0 ? clamp(tot.ah / capT * 100, 0, 100) : socAvg;
      var v = bs.length ? bs.reduce(function (a, b) { return a + b.v; }, 0) / bs.length : 0;
      var w = tot.w || 0, a = tot.a || 0, flow = a > 0.4 ? "in" : a < -0.4 ? "out" : "idle";
      var availWh = (tot.kwh > 0 ? tot.kwh * 1000 : soc / 100 * capT * 12.8), auton;
      if (tot.hours > 0) auton = "Autonomie estimée : " + nf(tot.hours, tot.hours < 10 ? 1 : 0) + NB + "h";
      else if (flow === "out" && w) auton = "Autonomie estimée : " + nf(availWh / Math.abs(w), 0) + NB + "h";
      else if (flow === "in") auton = "En charge · " + nf(Math.abs(a), 1) + NB + "A entrent";
      else auton = soc >= 97 ? "Pleines · au repos" : "Au repos · aucun courant important";
      var seen = Math.max.apply(null, d.batteries.map(function (b) { return b.seen || 0; }));
      return { live: true, soc: soc, v: v, w: w, a: a, flow: flow, autonomy: auton, availWh: availWh, ah: tot.ah,
        packs: d.batteries.map(function (b, i) {
          return { name: (en.packs[i] || {}).name || "Batterie " + (i + 1), cap: b.cap || (en.packs[i] || {}).cap, soc: b.soc, v: b.v, a: b.a, t: b.t,
            cycles: b.cycles, hi: b.hi, lo: b.lo, chg: b.chg, dsg: b.dsg, bal: b.balancing, online: b.online, problem: b.problem, charging: b.charging };
        }), seen: seen, now: d.now || NOW() / 1000, alarm: !!tot.alarm };
    }
    var so = solarDay(e), solarW = so ? so.now : 0, flowEx = exampleFlow(e);
    var socE = en.soc, availE = socE / 100 * capT, wh = en.unit === "Ah" ? availE * 12.8 : availE * 1000;
    var autoE = flowEx.batt < -5 ? "Autonomie estimée : " + nf(wh * (1 - en.reserve / socE) / Math.abs(flowEx.batt), 0) + NB + "h"
      : flowEx.batt > 5 ? "En charge · " + fmtW(flowEx.batt) : "Au repos";
    if (en.autonomy) autoE = en.autonomy;
    return { live: false, failed: !!(en.live && LIVE.ok === false), soc: socE, w: flowEx.batt, flow: flowEx.batt > 5 ? "in" : flowEx.batt < -5 ? "out" : "idle",
      autonomy: autoE, packs: en.packs || [], solarW: solarW };
  }
  function exampleFlow(e) {
    var en = e.energy, so = solarDay(e), load = en.solar ? loadNow(e) : en.load, srcs = [], known = 0, grid = null;
    en.sources.forEach(function (s) {
      var w = s[3] === "solar" ? (so ? so.now : 0) : s[3] === "grid" ? null : +s[3] || 0;
      var o = { k: s[0], label: s[1], icon: s[2], w: w, note: s[4] || "" };
      if (w === null) grid = o; else known += w;
      srcs.push(o);
    });
    var batt;
    if (grid) { batt = en.battW || 0; grid.w = Math.max(0, load + batt - known); }
    else batt = known - load;
    return { srcs: srcs, load: load, batt: batt };
  }
  function liveWanted() {
    return visible && !document.hidden && API && (S.view === "home" || (S.env === "boulance" && (S.sec === "apercu" || S.sec === "energie" || S.sec === "internet")));
  }
  function liveTick(force) {
    if (!API) { if (LIVE.ok === null) { LIVE.ok = false; paintLive(); } return; }
    if ((!liveWanted() && !force) || LIVE.busy) return;
    LIVE.busy = true;
    fetch(API + "/live", { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { if (!d || !d.ok || !d.batteries) throw new Error("ko"); LIVE.d = d; LIVE.ok = true; })
      .catch(function () { LIVE.ok = false; })
      .then(function () { LIVE.busy = false; paintLive(); });
    if (S.sec === "energie" && NOW() - LIVE.histT > 300000) {
      LIVE.histT = NOW();
      fetch(API + "/history").then(function (r) { return r.json(); })
        .then(function (d) { if (d && d.ok && d.points && d.points.length > 1) { LIVE.hist = d.points; paintLive(); } }).catch(function () {});
    }
  }
  function liveLoop() {
    clearInterval(LIVE.timer);
    LIVE.timer = null;
    if (!liveWanted()) return;
    liveTick();
    LIVE.timer = setInterval(function () { if (liveWanted()) liveTick(); else { clearInterval(LIVE.timer); LIVE.timer = null; } }, 10000);
  }
  /* Redessine seulement les cartes liées aux mesures réelles */
  function paintLive() {
    app.querySelectorAll("[data-live]").forEach(function (el) {
      var i = +el.getAttribute("data-c"), c = CUR[i];
      if (c && K[c.type]) { el.innerHTML = K[c.type](c, cur(), i, true); el.classList.remove("is-new"); if (HOOK[c.type]) HOOK[c.type](el, c, cur(), i); }
    });
    app.querySelectorAll("[data-live-pick]").forEach(function (el) { el.innerHTML = pickStatus(E[el.getAttribute("data-live-pick")]); });
    app.querySelectorAll("[data-live-cell]").forEach(function (el) { var x = siteOf(E[el.getAttribute("data-live-cell")]); el.innerHTML = enCell(x, batColor(x.soc)); });
  }
  function liveTag(b) {
    if (b.live) return '<span class="ev-tag is-live" title="Mesure reçue des batteries de BouLance">réel</span>';
    if (b.failed) return '<span class="ev-tag" title="Liaison des batteries indisponible : valeurs d’exemple">exemple · liaison indisponible</span>';
    return "";
  }

  /* ======================================================================================
     Briques visuelles : en-tête de carte, courbes, jauges, anneau, interrupteur
     ====================================================================================== */
  function head(icon, title, sub, right, cls) {
    return '<header class="ev-ch' + (cls ? " " + cls : "") + '">' + (icon ? '<span class="ev-ci">' + ic(icon) + "</span>" : "") +
      '<div class="ev-ct"><h5>' + esc(title) + "</h5>" + (sub ? "<p>" + sub + "</p>" : "") + "</div>" + (right ? '<div class="ev-cr">' + right + "</div>" : "") + "</header>";
  }
  function dot(t) { return '<i class="ev-dot t-' + (t || "ok") + '" aria-hidden="true"></i>'; }
  function sw(on, a, v, label) {
    return '<button type="button" class="ev-sw' + (on ? " is-on" : "") + '" role="switch" aria-checked="' + (on ? "true" : "false") + '" data-a="' + a + '" data-v="' + esc(v) + '" aria-label="' + esc(label) + '"><i></i></button>';
  }
  function bar(pct, cls, style) {
    return '<span class="ev-bar ' + (cls || "") + '"><i style="width:' + clamp(pct, 0, 100).toFixed(1) + "%" + (style || "") + '"></i></span>';
  }
  var COL = { gold: "var(--e-acc)", blue: "var(--e-water)", white: "var(--e-text)", green: "var(--e-ok)", warn: "var(--e-warn)" };
  /* Courbe : tracé en SVG étiré, étiquettes en HTML (nettes à toutes les tailles). Grille fine, aire en dégradé,
     trait doublé d'un halo statique. o.tip = { l: libellé de chaque index, f: format d'une valeur, names: [...] }
     ajoute un curseur au survol avec infobulle (données préparées ici, aucune requête). */
  function plot(o) {
    var n = o.n, lo = o.min, hi = o.max, H = 300;
    function X(i) { return i / (n - 1) * 1000; }
    function Y(v) { return H - (v - lo) / (hi - lo) * H * 0.9 - H * 0.05; }
    var defs = "", paths = "";
    (o.series || []).forEach(function (s) {
      var from = s.from || 0, pts = s.v.map(function (v, i) { return [X(i + from), Y(v)]; });
      if (pts.length < 2) return;
      var line = s.straight ? "M" + pts.map(f2).join(" L") : sp(pts, false, 0.85), col = COL[s.c] || COL.gold;
      if (s.area) {
        var id = uid();
        defs += '<linearGradient id="' + id + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:' + col + ';stop-opacity:' + (s.op || 0.3) + '"/><stop offset=".7" style="stop-color:' + col + ';stop-opacity:' + ((s.op || 0.3) * 0.22).toFixed(3) + '"/><stop offset="1" style="stop-color:' + col + ';stop-opacity:0"/></linearGradient>';
        paths += '<path class="ev-pa-fill" d="' + line + " L" + f2([pts[pts.length - 1][0], H]) + " L" + f2([pts[0][0], H]) + ' Z" fill="url(#' + id + ')"/>';
      }
      if (!s.dash) paths += '<path class="ev-pa-glow" d="' + line + '" style="stroke:' + col + '" vector-effect="non-scaling-stroke"/>';
      paths += '<path class="ev-pa-line' + (s.dash ? " is-dash" : "") + '" d="' + line + '" style="stroke:' + col + '" pathLength="1000" vector-effect="non-scaling-stroke"/>';
    });
    var bg = {};
    (o.bars || []).forEach(function (b) {
      var col = COL[b[2]] || COL.blue;
      if (!bg[col]) { bg[col] = uid(); defs += '<linearGradient id="' + bg[col] + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:' + col + ';stop-opacity:.95"/><stop offset="1" style="stop-color:' + col + ';stop-opacity:.16"/></linearGradient>'; }
      var bw = 1000 / n * 0.42, x = X(b[0]) - bw / 2, y = Y(b[1]);
      paths += '<rect class="ev-pa-bar" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + Math.max(0, H - H * 0.05 - y).toFixed(1) + '" fill="url(#' + bg[col] + ')"/>';
    });
    var grid = (o.y || []).map(function (v) { return '<line x1="0" x2="1000" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" vector-effect="non-scaling-stroke"/>'; }).join("");
    if (o.vgrid) grid += o.vgrid.map(function (i) { return '<line class="is-v" y1="0" y2="300" x1="' + X(i).toFixed(1) + '" x2="' + X(i).toFixed(1) + '" vector-effect="non-scaling-stroke"/>'; }).join("");
    var now = o.now != null ? '<line class="ev-pa-now" y1="0" y2="300" x1="' + X(o.now).toFixed(1) + '" x2="' + X(o.now).toFixed(1) + '" vector-effect="non-scaling-stroke"/>' : "";
    var html = (o.y || []).map(function (v) { return '<span class="ev-yl" style="top:' + (Y(v) / 3).toFixed(2) + '%">' + (o.yf ? o.yf(v) : nf(v)) + "</span>"; }).join("");
    html += (o.x || []).map(function (x) { return '<span class="ev-xl' + (x[2] ? " is-b" : X(x[0]) >= 985 ? " is-end" : "") + '" style="left:' + (X(x[0]) / 10).toFixed(2) + '%">' + x[1] + "</span>"; }).join("");
    html += (o.dots || []).map(function (d) {
      return '<span class="ev-pd' + (d[3] ? " c-" + d[3] : "") + '" style="left:' + (X(d[0]) / 10).toFixed(2) + "%;top:" + (Y(d[1]) / 3).toFixed(2) + '%">' + (d[2] ? "<b>" + d[2] + "</b>" : "") + "</span>";
    }).join("");
    var tip = "";
    if (o.tip) {
      var rows = [];
      for (var i = 0; i < n; i++) {
        var r = [o.tip.l(i), []];
        (o.series || []).forEach(function (s, k) {
          var j = i - (s.from || 0);
          if (j >= 0 && j < s.v.length && (!o.tip.skip || !o.tip.skip(k, j))) r[1].push([s.c || "gold", (o.tip.names || [])[k] || "", o.tip.f(s.v[j]), +(Y(s.v[j]) / 3).toFixed(1)]);
        });
        (o.bars || []).forEach(function (b) { if (b[0] === i) r[1].push([b[2] || "blue", (o.tip.names || [])[0] || "", o.tip.f(b[1]), +(Y(b[1]) / 3).toFixed(1)]); });
        rows.push(r);
      }
      tip = " data-tip='" + JSON.stringify(rows).replace(/'/g, "&#39;") + "'";
    }
    return '<div class="ev-plot' + (o.cls ? " " + o.cls : "") + (o.y && o.y.length ? " has-y" : "") + '" style="--h:' + (o.h || 140) + 'px"><div class="ev-pa"' + tip + ">" +
      '<svg viewBox="0 0 1000 300" preserveAspectRatio="none" aria-hidden="true"><defs>' + defs + '</defs><g class="ev-grid">' + grid + "</g>" + now + paths + "</svg>" + html + "</div></div>";
  }
  /* Curseur des courbes : ligne verticale, points sur chaque série et infobulle (au survol ou au toucher) */
  function plotTip(pa, ev) {
    var rows = pa.__tip || (pa.__tip = JSON.parse(pa.getAttribute("data-tip"))), r = pa.getBoundingClientRect();
    var i = clamp(Math.round((ev.clientX - r.left) / r.width * (rows.length - 1)), 0, rows.length - 1), row = rows[i], x = i / (rows.length - 1) * 100;
    var cur = pa.querySelector(".ev-pc");
    if (!cur) { pa.insertAdjacentHTML("beforeend", '<span class="ev-pc" aria-hidden="true"><i class="ev-pc-l"></i><span class="ev-pc-d"></span><span class="ev-pc-t"></span></span>'); cur = pa.querySelector(".ev-pc"); }
    if (!row[1].length) { cur.hidden = true; return; }
    cur.hidden = false;
    cur.style.left = x + "%";
    cur.querySelector(".ev-pc-d").innerHTML = row[1].map(function (s) { return '<i class="c-' + s[0] + '" style="top:' + s[3] + '%"></i>'; }).join("");
    var t = cur.querySelector(".ev-pc-t");
    t.innerHTML = "<small>" + row[0] + "</small>" + row[1].map(function (s) { return '<span><i class="c-' + s[0] + '"></i>' + (s[1] ? "<em>" + s[1] + "</em>" : "") + "<b>" + s[2] + "</b></span>"; }).join("");
    t.classList.toggle("is-l", x > 60);
  }
  /* Graduations fines autour d'un arc (mêmes règles que le cadran) : majeures tous les 10 pas, allumées jusqu'à la valeur */
  function ticks(a0, a1, n, p, r0, r1, r2) {
    var out = "", on = a0 + (a1 - a0) * p / 100;
    for (var i = 0; i <= n - (a1 - a0 >= 360 ? 1 : 0); i++) {
      var a = a0 + (a1 - a0) * i / n, maj = i % 10 === 0, q0 = pol(50, 50, maj ? r0 : r1, a), q1 = pol(50, 50, r2, a);
      out += '<line class="g-tk' + (maj ? " is-maj" : "") + (p > 0 && a <= on + 0.01 ? " is-on" : "") + '" x1="' + q0[0].toFixed(2) + '" y1="' + q0[1].toFixed(2) + '" x2="' + q1[0].toFixed(2) + '" y2="' + q1[1].toFixed(2) + '"/>';
    }
    return '<g class="g-tks">' + out + "</g>";
  }
  /* Jauge en arc : balayage 270° (cadran : verre noir au centre) ou 180° (demi-cercle) */
  function gauge(pct, o) {
    o = o || {};
    var sw2 = o.sweep || 270, a0 = -sw2 / 2, a1 = sw2 / 2, r = 40, id = uid();
    var track = arcD(50, 50, r, a0, a1), p = clamp(pct, 0, 100);
    var grad = o.grad ? '<defs><linearGradient id="' + id + '" gradientUnits="userSpaceOnUse" x1="0" y1="100" x2="100" y2="0">' + o.grad.map(function (g, i) {
      return '<stop offset="' + (i / (o.grad.length - 1)) + '" style="stop-color:' + g + '"/>';
    }).join("") + "</linearGradient></defs>" : "";
    var stroke = o.grad ? "url(#" + id + ")" : (o.color || "var(--e-acc)"), glow = o.grad ? o.grad[o.grad.length - 1] : (o.color || "var(--e-acc)");
    var face = sw2 > 180 ? '<circle class="g-face" cx="50" cy="50" r="33" fill="url(#evd-face)"/>' : "";
    return '<svg class="ev-gauge' + (o.cls ? " " + o.cls : "") + '" viewBox="0 0 100 ' + (sw2 <= 180 ? 58 : 100) + '" style="--gs:' + stroke + ";--gc:" + glow + '" aria-hidden="true">' + grad + face +
      ticks(a0, a1, sw2 <= 180 ? 36 : 60, p, 45.5, 46.8, 49.5) +
      '<path class="g-track" d="' + track + '"/><path class="g-val" d="' + track + '" pathLength="100" style="stroke-dasharray:' + p.toFixed(1) + ' 100"/></svg>';
  }
  /* Anneau : même finition que le cadran (graduations sur 360°, verre noir au centre) */
  function ring(pct, color) {
    var p = clamp(pct, 0, 100);
    return '<svg class="ev-ring" viewBox="0 0 100 100" style="--gs:' + color + ";--gc:" + color + '" aria-hidden="true"><circle class="g-face" cx="50" cy="50" r="34" fill="url(#evd-face)"/>' + ticks(0, 360, 60, p, 45.5, 46.8, 49.5) +
      '<circle class="g-track" cx="50" cy="50" r="40.5"/><circle class="g-val" cx="50" cy="50" r="40.5" pathLength="100" transform="rotate(-90 50 50)" style="stroke-dasharray:' + p.toFixed(1) + ' 100"/></svg>';
  }
  /* Valeur typographiée : chiffres tabulaires légers, unité plus petite et atténuée. Le nombre « monte » jusqu'à
     sa valeur au premier affichage (countUp, seulement sous html.fx et hors mouvement réduit). */
  function unitize(s) {
    s = String(s);
    var m = /^([+−-]?)(\d+(?:,\d+)?)([  ]?)([^\d]*)$/.exec(s);
    if (!m) return esc(s);
    var neg = m[1] === "−" || m[1] === "-", dec = (m[2].split(",")[1] || "").length;
    return '<span class="ev-num" data-n="' + (neg ? "-" : "") + m[2].replace(",", ".") + '" data-d="' + dec + '"' + (m[1] === "+" ? ' data-p="+"' : "") + ">" + esc(m[1] + m[2]) + "</span>" +
      (m[4] ? '<small class="ev-u">' + esc(m[4]) + "</small>" : "");
  }
  function countUp(scope) {
    if (reduce() || !document.documentElement.classList.contains("fx")) return;
    var items = [].map.call(scope.querySelectorAll(".ev-card.is-new [data-n]"), function (el) {
      return { el: el, to: +el.getAttribute("data-n"), d: +el.getAttribute("data-d") || 0, p: el.getAttribute("data-p") || "" };
    }), t0 = null;
    if (!items.length) return;
    function step(ts) {
      t0 = t0 || ts;
      var k = clamp((ts - t0) / 1100, 0, 1), ea = 1 - Math.pow(1 - k, 3);
      items.forEach(function (it) { if (it.el.isConnected) it.el.textContent = it.p + nf(it.to * ea, it.d); });
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function kv(label, value, cls) { return '<div class="ev-kv' + (cls ? " " + cls : "") + '"><span>' + label + "</span><b>" + value + "</b></div>"; }

  /* ======================================================================================
     Cartes stylisées (aucune tuile : géographie dessinée, illustrative)
     ====================================================================================== */
  function mapView(e, o) {
    var M = e.maps[o.map];
    if (!M) return "";
    var v = o.view || [0, 0, 400, 240], sx = 400 / v[2], sy = 240 / v[3];
    function P(p) { return [(p[0] - v[0]) * sx, (p[1] - v[1]) * sy]; }
    function at(p) { var q = P(p); return "left:" + (q[0] / 4).toFixed(2) + "%;top:" + (q[1] / 2.4).toFixed(2) + "%"; }
    function inside(p) { var q = P(p); return q[0] > 6 && q[0] < 394 && q[1] > 6 && q[1] < 234; }
    /* Fond noir : quadrillage très fin, eau en noir bleuté avec rive lumineuse, routes en filets dorés */
    var id = uid(), svg = '<defs><pattern id="' + id + '" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16"/></pattern></defs>' +
      '<rect class="m-land" width="400" height="240"/><rect class="m-tex" width="400" height="240" fill="url(#' + id + ')"/>';
    (M.fields || []).forEach(function (f) { svg += '<path class="m-field" d="M' + f.map(function (p) { return f2(P(p)); }).join(" L") + 'Z"/>'; });
    (M.water || []).forEach(function (w) { var d = sp(w.map(P), true); svg += '<path class="m-shore" d="' + d + '"/><path class="m-water" d="' + d + '"/>'; });
    (M.rivers || []).forEach(function (r) { svg += '<path class="m-river" d="' + sp(r.map(P), false) + '"/>'; });
    (M.roads || []).forEach(function (r) { svg += '<path class="m-road' + (r.minor ? " is-minor" : "") + (r.rail ? " is-rail" : "") + '" d="' + (r.straight ? "M" + r.pts.map(function (p) { return f2(P(p)); }).join(" L") : sp(r.pts.map(P), false)) + '"/>'; });
    (M.blocks || []).forEach(function (b) { var a = P([b[0], b[1]]), c = P([b[0] + b[2], b[1] + b[3]]); svg += '<rect class="m-block' + (b[4] ? " is-" + b[4] : "") + '" x="' + a[0].toFixed(1) + '" y="' + a[1].toFixed(1) + '" width="' + (c[0] - a[0]).toFixed(1) + '" height="' + (c[1] - a[1]).toFixed(1) + '" rx="1.5"/>'; });
    (M.strips || []).forEach(function (r) { svg += '<path class="m-strip" d="M' + f2(P(r[0])) + " L" + f2(P(r[1])) + '" style="stroke-width:' + (r[2] || 8) * sx + '"/><path class="m-strip-c" d="M' + f2(P(r[0])) + " L" + f2(P(r[1])) + '"/>'; });
    var R = o.route;
    if (R) {
      if (R.later && R.later.length > 1) svg += '<path class="m-rt is-later" d="' + sp(R.later.map(P), false) + '"/>';
      if (R.done && R.done.length > 1) svg += '<path class="m-rt is-done" d="' + sp(R.done.map(P), false) + '"/>';
      if (R.next && R.next.length > 1) svg += '<path class="m-rt is-next" d="' + sp(R.next.map(P), false) + '"/>';
    }
    if (o.ring) { var c = P(M.me), rr = o.ring * M.km * sx; svg += '<circle class="m-ring" cx="' + c[0].toFixed(1) + '" cy="' + c[1].toFixed(1) + '" r="' + rr.toFixed(1) + '"/>'; }
    var html = "";
    if (M.lake && inside(M.lake)) { var lq = P(M.lake); html += '<span class="m-lake" style="left:' + clamp(lq[0] / 4, 18, 82).toFixed(2) + "%;top:" + (lq[1] / 2.4).toFixed(2) + '%">' + esc(M.lake[2]) + "</span>"; }
    (M.towns || []).forEach(function (t) { if (inside(t)) html += '<span class="m-town' + (t[3] ? " is-" + t[3] : P(t)[0] > 320 ? " is-l" : "") + '" style="' + at(t) + '"><i></i>' + esc(t[2]) + "</span>"; });
    (M.roads || []).forEach(function (r) { if (r.n && r.at && inside(r.at)) html += '<span class="m-shield" style="' + at(r.at) + '">' + r.n + "</span>"; });
    (M.labels || []).forEach(function (t) { if (inside(t)) html += '<span class="m-lbl' + (t[3] ? " is-" + t[3] : "") + (P(t)[0] > 330 ? " is-r" : "") + '" style="' + at(t) + '">' + esc(t[2]) + "</span>"; });
    (o.pins || []).forEach(function (p) {
      if (!inside([p.x, p.y])) return;
      html += '<span class="m-pin t-' + (p.tone || "gold") + (p.dim ? " is-dim" : "") + '" style="' + at([p.x, p.y]) + '"' + (p.title ? ' title="' + esc(p.title) + '"' : "") + ">" + (p.n ? "<b>" + p.n + "</b>" : ic(p.icon || "pin")) + "</span>";
    });
    if (M.me && inside(M.me)) html += '<span class="m-me" style="' + at(M.me) + '">' + ic(o.meIcon || e.meIcon || "rv") + "</span>";
    if (R && R.next && R.next.length > 1) html += '<span class="m-dest" style="' + at(R.next[R.next.length - 1]) + '">' + ic("pin") + "</span>";
    // Échelle : longueur ronde proche de 22 % de la largeur
    var kmW = v[2] / M.km, target = kmW * 0.22, steps = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500], L = steps.filter(function (s) { return s <= target; }).pop() || steps[0];
    html += '<span class="m-scale" style="--w:' + (L / kmW * 100).toFixed(2) + '%"><i></i>' + nf(L, L < 1 ? 1 : 0) + NB + "km</span>";
    if (o.ring) html += '<span class="m-ringl" style="' + at([M.me[0], M.me[1] + o.ring * M.km * 0.98]) + '">' + o.ring + NB + "km</span>";
    return '<div class="ev-map' + (o.cls ? " " + o.cls : "") + '"><svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' + svg + '</svg><span class="m-vig" aria-hidden="true"></span>' + html +
      '<span class="m-note">' + (M.note || "Carte illustrative") + "</span></div>";
  }

  /* ======================================================================================
     Cartes : chaque sorte reçoit (carte, environnement, index) et rend son contenu
     ====================================================================================== */
  var K = {};
  var CUR = [];
  function cur() { return E[S.env]; }

  K.kpi = function (c, e) {
    var v = c.value, sub = c.sub, b = null, pct = c.bar, color = null, tag = "";
    if (c.live === "soc") { b = bat(e); v = nf(b.soc) + NB + "%"; pct = b.soc; sub = b.autonomy; color = batColor(b.soc); tag = liveTag(b); }
    else if (c.tone === "bat") color = batColor(pct);
    else if (c.tone === "heat") color = "#ff9f5a";
    if (v === "solar:today" || v === "solar:sofar") { var so = solarDay(e); v = so ? nf((v === "solar:today" ? so.total : so.sofar) / 1000, 1) + NB + "kWh" : "—"; }
    var inner = '<span class="ev-ki t-' + (c.tone || "gold") + '"' + (color ? ' style="--tc:' + color + '"' : "") + ">" + ic(c.icon) + "</span>" +
      '<span class="ev-kb"><span class="ev-kl">' + esc(c.label) + tag + "</span>" +
      '<b class="ev-kn">' + (/[<]/.test(v) ? v : "<span>" + unitize(v) + "</span>") + (c.dot ? dot(c.dot) : "") + "</b>" +
      (pct != null ? bar(pct, "t-" + (c.tone || "gold"), color ? ";--bc:" + color : "") : "") +
      (sub ? '<span class="ev-ks">' + (c.subicon ? ic(c.subicon) : "") + sub + "</span>" : "") + "</span>" +
      (c.go ? '<span class="ev-kgo">' + ic("right") + "</span>" : "");
    return c.go ? '<button type="button" class="ev-kpi" data-a="go" data-v="' + c.go + '">' + inner + "</button>" : '<div class="ev-kpi">' + inner + "</div>";
  };

  K.conditions = function (c, e) {
    var w = e.wx, n = wxNow(e), sd = sunDay(e), now = NOW(), h0 = lp(now).h, temps = [], xs = [], dots = [];
    for (var i = 0; i <= 14; i++) {
      var t = e.wx.t24[(h0 + i) % 24];
      temps.push(i === 0 ? n.t : t);
      if (i % 2 === 0) { xs.push([i, hh((h0 + i) % 24)]); dots.push([i, i === 0 ? n.t : t, nf(i === 0 ? n.t : t) + "°"]); }
    }
    var lo = Math.floor(Math.min.apply(null, temps)) - 2, hi = Math.ceil(Math.max.apply(null, temps)) + 3;
    var right = '<span class="ev-upd">Mise à jour : ' + hm(now - w.upd * 60000) + "<br>Source : " + esc(w.src) + "</span>";
    return head("cloudsun", c.title || "Conditions extérieures", ic("pin", "is-sm") + esc(e.geo.place), right) +
      '<div class="ev-cond">' +
      '<div class="ev-cond-now">' + wxi(n.code, n.night, "is-lg") + "<div><b>" + deg(n.t) + "</b><span>" + n.cond + "</span></div></div>" +
      '<div class="ev-cond-i">' + ic("wind") + "<div><small>Vent</small><b>" + w.wind + NB + "km/h</b><small>" + esc(w.dir) + "</small></div></div>" +
      '<div class="ev-cond-i">' + ic("sunset") + "<div><small>Coucher du soleil</small><b>" + (sd.set ? hm(sd.set) : "—") + "</b></div></div>" +
      '<div class="ev-cond-i">' + ic("sunrise") + "<div><small>Lever du soleil</small><b>" + (sd.rise ? hm(sd.rise + (sd.rise < now ? 864e5 : 0)) : "—") + "</b>" + (sd.rise < now ? "<small>demain</small>" : "") + "</div></div>" +
      '<div class="ev-cond-chips"><span>' + ic("sun") + "UV <b>" + w.uv + '</b></span><span title="Cote air santé">' + ic("leaf") + "CAS <b>" + w.cas + "</b></span></div></div>" +
      plot({ n: temps.length, min: lo, max: hi, h: 112, series: [{ v: temps, c: "gold", area: true }], x: xs, dots: dots, cls: "is-cond",
        tip: { l: function (k) { return k ? hh((h0 + k) % 24) : "Maintenant"; }, f: function (v) { return deg(v); }, names: ["Température"] } });
  };

  K.lumieres = function (c, e) {
    var st = rt(e).lights, cnt = st ? '<span class="ev-count"><b>' + st.on + "</b> / " + st.total + " allumées</span>" : "";
    return head("bulb", "Éclairage", "", cnt + '<button type="button" class="ev-link" data-a="go" data-v="eclairage">Ouvrir' + ic("right") + "</button>") +
      '<div class="ev-lum-mini" data-lum-mini></div>' + lumFoot(e);
  };
  /* Pied de la carte Éclairage : prochaine bascule de l'éclairage extérieur, calculée selon le vrai soleil */
  function lumFoot(e) {
    var sd = sunDay(e), now = NOW(), on = sd.set && now < sd.set, t = on ? sd.set : sunDay(e, 1).rise;
    return '<div class="ev-lumf"><span class="ev-ri">' + ic(on ? "sunset" : "sunrise") + "</span><span><small>Éclairage extérieur</small><b>" + (on ? "S’allume au coucher du soleil" : "S’éteint au lever du soleil") + "</b></span>" +
      '<b class="ev-lumf-t">' + (t ? hm(t) : "—") + "</b></div>";
  }

  function pointsOf(e) { return e.points || []; }
  K.around = function (c, e) {
    var pins = c.pins === "points" ? pointsOf(e).map(function (p) { return { x: p.x, y: p.y, icon: KIND[p.kind].icon, tone: KIND[p.kind].tone, title: p.name }; }) : (c.pinsList || []);
    return head("map", c.title, c.sub || "", "") + '<div class="ev-around">' + mapView(e, { map: c.map, view: c.view, pins: pins }) +
      '<div class="ev-around-l"><p class="ev-k">' + esc(c.listTitle || "Points de service à confirmer") + "</p>" +
      c.list.map(function (r) { return '<div class="ev-row"><span class="ev-ri t-' + r[1] + '">' + ic(r[0]) + "</span><span><b>" + esc(r[2]) + "</b><small>" + esc(r[3]) + "</small></span></div>"; }).join("") +
      (c.btn ? '<button type="button" class="ev-btn" data-a="go" data-v="' + c.btn[1] + '">' + ic("map") + esc(c.btn[0]) + ic("right") + "</button>" : "") + "</div></div>";
  };
  var KIND = { eau: { icon: "drop", tone: "water", label: "Remplissage" }, vidange: { icon: "dump", tone: "ok", label: "Vidange" },
    carburant: { icon: "fuel", tone: "muted", label: "Carburant" }, service: { icon: "wrench", tone: "gold", label: "Service" } };

  function checks(e, id, items) {
    var r = rt(e);
    if (!r.checks[id]) r.checks[id] = items.map(function (x) { return !!x[1]; });
    return r.checks[id];
  }
  /* Sources : d'où vient chaque élément d'une liste ou d'un entretien */
  var SRC = { fab: ["doc", "Manuel du fabricant", "Intervalle ou consigne tirés du manuel du fabricant."],
    compteur: ["gauge", "Compteur", "Calculé à partir du compteur : kilomètres, heures moteur, cycles ou volume."],
    capteur: ["radar", "Capteur", "Vérifié automatiquement par un capteur relié à JARVIS."],
    saison: ["cloudsun", "Saison et météo", "Ajouté selon la saison et la météo prévue sur le lieu."],
    vous: ["users2", "Ajouté par vous", "Ajouté par vous ou par un membre de votre équipe."],
    jarvis: ["sparkle", "Recommandé par JARVIS", "Recommandé par JARVIS selon l’usage réel du lieu."],
    regle: ["shield", "Règlement", "Exigé par un règlement en vigueur."] };
  function srcChip(s, full) {
    if (!s) return "";
    var d = SRC[s.k] || SRC.jarvis, t = s.t || s.ref || "";
    return '<span class="ev-src s-' + esc(s.k) + '"' + (t && !full ? ' title="' + esc(t) + '"' : "") + ">" + ic(d[0]) + "<b>" + d[1] + "</b>" + (full && t ? "<em>" + esc(t) + "</em>" : "") + "</span>";
  }
  K.checklist = function (c, e) {
    var st = checks(e, c.id, c.items), done = st.filter(Boolean).length, pct = done / st.length * 100;
    return head(c.icon || "clip", c.title, "Chaque élément indique d’où il vient", '<span class="ev-count"><b>' + done + "</b> / " + st.length + " terminées</span>" + bar(pct, "t-ok is-sm")) +
      '<ul class="ev-checks">' + c.items.map(function (it, i) {
        return '<li><button type="button" class="ev-check' + (st[i] ? " is-on" : "") + '" data-a="chk" data-v="' + c.id + ":" + i + '" aria-pressed="' + st[i] + '"><span class="ev-box">' + ic("check") + "</span>" +
          '<span class="ev-chk-t"><span>' + esc(it[0]) + "</span>" + srcChip(it[2], true) + "</span></button></li>";
      }).join("") + "</ul>";
  };

  /* Prochaines 48 heures : ce qui compte bientôt, réuni d'une seule lecture (rappel du lieu, soleil, agenda, entretien) */
  K.upcoming = function (c, e) {
    var now = NOW(), items = [], sd = sunDay(e), sd1 = sunDay(e, 1), ag = findCard(e, "agenda"), mt = findCard(e, "maint");
    if (c.note) items.push({ t: now - 1, pin: true, icon: c.icon || "info", tone: "water", title: c.note, text: c.text || "", go: c.go, when: "À retenir" });
    if (sd.set && sd.set > now) items.push({ t: sd.set, icon: "sunset", tone: "gold", title: "Coucher du soleil", text: "Éclairage extérieur selon votre règle", go: "eclairage" });
    if (sd1.rise) items.push({ t: sd1.rise, icon: "sunrise", tone: "gold", title: "Lever du soleil", text: "Durée du jour : " + dur(sd1.set - sd1.rise), go: "confort:soleil" });
    if (ag) ag.events.forEach(function (ev) {
      var t = dayAt(ev[0], ev[1]);
      if (t > now && t < now + 48 * 3600e3 && ev[4] !== "stay") items.push({ t: t, icon: ev[4] === "maint" ? "wrench" : ev[4] === "flight" ? "plane" : ev[4] === "peak" ? "bolt" : "calendar", tone: ev[4] === "maint" ? "water" : "gold", title: ev[3], text: "À l’agenda", go: "voyage:agenda" });
    });
    if (mt) mt.rows.forEach(function (m) {
      var due = m[5] ? dueOf(m[5]) : m[3];
      if (due <= 2) items.push({ t: due < 0 ? now - 2 : dayAt(due, "09:00"), icon: m[0], tone: due < 0 ? "err" : "warn", title: m[1], text: "Source : " + (m[5] ? lc1((SRC[m[5].k] || SRC.jarvis)[1]) : m[2]), go: "voyage:entretien",
        when: due < 0 ? "En retard de " + (-due) + NB + "j" : null });
    });
    items.sort(function (a, b) { return (b.pin ? 1 : 0) - (a.pin ? 1 : 0) || (b.tone === "err" ? 1 : 0) - (a.tone === "err" ? 1 : 0) || a.t - b.t; });
    return head("clock", c.title || "Prochaines 48 heures", "Ce qui compte bientôt, au même endroit", "") + '<ol class="ev-up">' + items.slice(0, 5).map(function (it) {
      return '<li><button type="button" class="ev-upi t-' + it.tone + (it.pin ? " is-pin" : "") + '" data-a="go" data-v="' + esc(it.go || "apercu") + '"><span class="ev-ri">' + ic(it.icon) + "</span>" +
        '<span class="ev-upi-b"><em>' + (it.when || cap(rel(it.t)) + " · " + hm(it.t)) + "</em><b>" + esc(it.title) + "</b><small>" + esc(it.text) + "</small></span>" + ic("right", "ev-chev") + "</button></li>";
    }).join("") + "</ol>";
  };

  /* Sécurité en un regard : système armé, ouvertures, détection, caméras */
  function armedOf(e) { var r = rt(e); return r.armed != null ? r.armed : !!(e.site && e.site.armed); }
  K.secsum = function (c, e) {
    var armed = armedOf(e), op = findCard(e, "openings"), det = null, cams = findCard(e, "cams");
    tabsOf(e, "securite").forEach(function (t) { t[2].forEach(function (x) { if (!det && x.type === "list" && (x.icon === "radar" || x.icon === "bell")) det = x; }); });
    var ops = op ? opsOf(e, op) : [], openI = [], detBad = det ? det.rows.filter(function (r) { return r[3] && r[3] !== "ok" && r[3] !== "muted"; }).length : 0;
    ops.forEach(function (o, j) { if (o.tone === "warn") openI.push(j); });
    var rows = [
      ["lock", "Ouvertures", op ? (ops.length - openI.length) + " / " + ops.length + " fermées" : "—", openI.length ? "warn" : "ok", openI.length ? op.points[openI[0]].label + " · " + ops[openI[0]].state.toLowerCase() : "Toutes fermées"],
      ["radar", "Détection", det ? (detBad ? detBad + " à vérifier" : "Normale") : "—", detBad ? "warn" : "ok", det ? det.rows.length + " capteurs surveillés" : ""],
      ["camera", "Caméras", cams && cams.items.length ? cams.items.length + " reliées" : "Aucune reliée", cams && cams.items.length ? "ok" : "muted", cams && cams.items.length ? "Accès : propriétaire uniquement" : "Aucune image n’est simulée"]
    ];
    return head("shield", "Sécurité", esc((e.site && e.site.arm) || ""), "") +
      '<div class="ev-sec-st' + (armed ? " is-armed" : "") + '"><span class="ev-sec-ring">' + ic("shield") + "</span><span><b>" + (armed ? "Système armé" : "Système désarmé") + "</b><small>" +
      (armed ? "Toute ouverture déclenche une alerte" : "Intrusion en pause · fumée et CO toujours surveillés") + "</small></span>" +
      '<button type="button" class="ev-btn is-sm' + (armed ? "" : " is-primary") + '" data-a="arm" data-v="' + e.key + '">' + ic(armed ? "unlock" : "lock") + (armed ? "Désarmer" : "Armer") + "</button></div>" +
      rows.map(function (r) { return '<div class="ev-row"><span class="ev-ri t-' + (r[3] === "muted" ? "gold" : r[3]) + '">' + ic(r[0]) + "</span><span><b>" + r[1] + "</b><small>" + esc(r[4]) + "</small></span><b class=\"t-" + r[3] + '">' + (r[3] !== "muted" ? dot(r[3]) : "") + esc(r[2]) + "</b></div>"; }).join("") +
      '<button type="button" class="ev-btn is-wide" data-a="go" data-v="securite">' + ic("shield") + "Ouvrir la sécurité" + ic("right") + "</button>";
  };

  K.trip = function (c, e) {
    if (!c.big && c.stages) {
      var n = c.stages.length, dots = c.stages.map(function (st, i) {
        return '<li class="' + (i < c.at ? "is-done" : i === c.at ? "is-here" : i === c.at + 1 ? "is-next" : "") + '" style="--x:' + (i / (n - 1) * 100).toFixed(2) + '%"><i></i><span>' + esc(st) + "</span></li>";
      }).join("");
      return head("route", c.title, esc(c.name), '<button type="button" class="ev-btn is-sm" data-a="go" data-v="' + c.go + '">' + ic("map") + "Ouvrir le voyage" + ic("right") + "</button>") +
        '<div class="ev-stg"><ol style="--p:' + (c.at / (n - 1) * 100).toFixed(2) + '%">' + dots + "</ol></div>" +
        '<div class="ev-stg-f"><span>' + ic("check") + "<small>Parcouru</small><b>" + esc(c.done) + "</b></span><span>" + ic("route") + "<small>" + esc(c.next) + "</small><b>" + esc(c.left) + " restants</b></span><span>" + ic("clock") + "<small>Prochain départ</small><b>" + esc(c.eta) + "</b></span></div>";
    }
    if (!c.big) {
      return head("route", c.title, "", "") + '<div class="ev-trip-s"><span><b>' + esc(c.name) + "</b><small>" + esc(c.next) + "</small></span>" +
        '<button type="button" class="ev-btn" data-a="go" data-v="' + c.go + '">' + ic("map") + "Ouvrir le voyage" + ic("right") + "</button></div>";
    }
    return '<div class="ev-trip"><div class="ev-trip-t">' + head("map", c.title, "", "") + '<p class="ev-trip-n">' + esc(c.name) + "</p><p class=\"ev-trip-x\">" + esc(c.next) + "</p>" +
      '<p class="ev-trip-d">' + ic(e.meIcon || "rv") + "<b>" + esc(c.dist) + "</b> · durée estimée : " + esc(c.dur) + "</p>" +
      '<button type="button" class="ev-btn is-primary" data-a="toast" data-v="L’extension Mobilité et voyage ouvrira l’itinéraire complet, une fois reliée.">Ouvrir Mobilité et voyage' + ic("right") + "</button>" +
      '<small class="ev-fine">Estimation d’exemple · actualisation automatique prévue.</small></div>' +
      mapView(e, { map: c.map, view: c.view, route: c.route, cls: "is-trip" }) + "</div>";
  };

  /* ---------- Confort ---------- */
  /* Cadran de thermostat : lunette métallique, verre noir, graduations, arc de chauffe entre la température
     actuelle et la consigne. Se règle au toucher (glisser), aux boutons ou aux flèches du clavier. */
  function dialAng(c, v) { return -135 + clamp((v - c.min) / (c.max - c.min), 0, 1) * 270; }
  function dialNow(c) { return c.now != null ? c.now : c.inside != null ? c.inside : c.set; }
  function dialSVG(c, v, key) {
    var now = dialNow(c), aV = dialAng(c, v), aN = dialAng(c, now), mode = v > now + 0.25 ? "heat" : v < now - 0.25 ? (key === "hot" ? "hold" : "cool") : "hold";
    var lo = Math.min(aV, aN), hi = Math.max(aV, aN), ticks = "";
    for (var i = 0; i <= 60; i++) {
      var a = -135 + i * 4.5, maj = i % 10 === 0, p0 = pol(100, 100, maj ? 70 : 73, a), p1 = pol(100, 100, 79, a);
      ticks += '<line class="d-tk' + (maj ? " is-maj" : "") + (a >= lo - 0.1 && a <= hi + 0.1 && hi - lo > 0.5 ? " is-on" : "") + '" x1="' + p0[0].toFixed(1) + '" y1="' + p0[1].toFixed(1) + '" x2="' + p1[0].toFixed(1) + '" y2="' + p1[1].toFixed(1) + '"/>';
    }
    var kn = pol(100, 100, 62, aV), cn = pol(100, 100, 86, aN), cn2 = pol(100, 100, 92, aN);
    var arc = hi - lo > 0.5 ? '<path class="d-val is-' + mode + '" d="' + arcD(100, 100, 62, lo, hi) + '"/>' : "";
    return '<svg class="ev-dsvg is-' + mode + '" viewBox="0 0 200 200" aria-hidden="true">' +
      '<circle cx="100" cy="100" r="98" fill="url(#evd-bezel)" class="d-bezel"/><circle cx="100" cy="100" r="90" class="d-bezel-in"/>' +
      '<circle cx="100" cy="100" r="88" fill="url(#evd-face)"/>' + ticks +
      '<path class="d-track" d="' + arcD(100, 100, 62, -135, 135) + '"/>' + arc +
      '<line class="d-now" x1="' + cn[0].toFixed(1) + '" y1="' + cn[1].toFixed(1) + '" x2="' + cn2[0].toFixed(1) + '" y2="' + cn2[1].toFixed(1) + '"/>' +
      '<circle class="d-knob is-' + mode + '" cx="' + kn[0].toFixed(1) + '" cy="' + kn[1].toFixed(1) + '" r="6.5"/>' +
      '<ellipse cx="100" cy="58" rx="66" ry="40" fill="url(#evd-glass)" class="d-glass"/></svg>';
  }
  function dialMode(c, v, key) {
    var now = dialNow(c);
    if (v > now + 0.25) return ["heat", "fire", key === "hot" ? "Chauffe" : "Chauffage"];
    if (v < now - 0.25) return key === "hot" ? ["hold", "leaf", "Refroidit lentement"] : ["cool", "snowflake", "Refroidissement"];
    return ["hold", "check", "Consigne atteinte"];
  }
  function dialCard(c, e, key, title, sub, icon, unit) {
    var r = rt(e), v = r.vals[key] != null ? r.vals[key] : c.set, st = r.pend[key], md = dialMode(c, v, key);
    var status = st === "send" ? '<span class="ev-sent is-wait">' + ic("refresh") + "Envoi de la consigne…</span>"
      : st === "ok" ? '<span class="ev-sent">' + ic("check") + "Consigne confirmée par l’appareil</span>" : '<span class="ev-sent is-idle">' + ic("info") + "Glissez sur le cadran ou utilisez + et −</span>";
    return head(icon, title, sub, "") + '<div class="ev-dialw"><div class="ev-dial">' +
      '<button type="button" class="ev-round" data-a="step" data-v="' + key + ':-1" aria-label="Baisser la consigne">' + ic("minus") + "</button>" +
      '<div class="ev-dial-g" data-dial="' + key + '" role="slider" tabindex="0" aria-label="Consigne · ' + esc(title) + '" aria-valuemin="' + c.min + '" aria-valuemax="' + c.max + '" aria-valuenow="' + v + '" aria-valuetext="' + nf(v, v % 1 ? 1 : 0) + " " + unit + '">' +
      dialSVG(c, v, key) + '<div class="ev-dial-v"><span class="ev-dial-m is-' + md[0] + '" data-dm>' + ic(md[1]) + md[2] + "</span><b data-dv>" + nf(v, v % 1 ? 1 : 0) + "<sup>" + unit + "</sup></b>" +
      "<small>Actuelle " + deg(dialNow(c)) + "</small></div></div>" +
      '<button type="button" class="ev-round" data-a="step" data-v="' + key + ':1" aria-label="Monter la consigne">' + ic("plus") + "</button></div>" + status + "</div>";
  }
  K.thermostat = function (c, e) {
    return '<div class="ev-thermo">' + '<div>' + dialCard(c, e, "thermo", c.title, c.sub, "thermo", "°C") + "</div>" +
      '<div class="ev-thermo-r">' + c.rows.map(function (r) { return '<div class="ev-row is-lg"><span class="ev-ri t-gold">' + ic(r[0]) + "</span><span><small>" + esc(r[1]) + "</small><b>" + esc(r[2]) + "</b></span>" + ic("right", "ev-chev") + "</div>"; }).join("") + "</div></div>";
  };
  K.trends = function (c, e) {
    return '<div class="ev-trends" data-fill>' + c.items.map(function (t) {
      var xs = [[0, "−3 h"], [4, "−2 h"], [8, "−1 h"], [11, "maint.", 1]];
      var unit = String(t.value).replace(/^[−\d,\s ]+/, "");
      return '<div class="ev-trend" data-fill>' + head(t.icon, t.title, "", "") + '<p class="ev-big">' + unitize(t.value) + ' <span class="ev-state">' + dot(t.tone) + esc(t.state) + "</span></p>" +
        plot({ n: t.pts.length, min: t.min, max: t.max, h: 96, y: [t.min, (t.min + t.max) / 2, t.max], series: [{ v: t.pts, c: t.c, area: true }], x: xs, dots: [[t.pts.length - 1, t.pts[t.pts.length - 1], "", t.c]],
          tip: { l: function (k) { var m = Math.round((t.pts.length - 1 - k) * 180 / (t.pts.length - 1)); return m ? "Il y a " + (m >= 60 ? Math.floor(m / 60) + NB + "h" + (m % 60 ? NB + pad(m % 60) : "") : m + NB + "min") : "Maintenant"; }, f: function (v) { return nf(v, 1) + (unit ? NB + unit.trim() : ""); }, names: [t.title] } }) + "</div>";
    }).join("") + "</div>";
  };
  K.ventilation = function (c, e) {
    var r = rt(e), s = r.vals.vent != null ? r.vals.vent : c.speed, st = r.pend.vent;
    var dots = "";
    for (var i = 1; i <= c.max; i++) dots += '<button type="button" class="ev-vd' + (i <= s ? " is-on" : "") + '" data-a="vent" data-v="' + i + '" aria-label="Vitesse ' + i + '"></button>';
    return head("fan", "Ventilation", "Renouvellement de l’air intérieur", "") +
      '<div class="ev-vent"><div class="ev-vent-h"><span>Vitesse</span><b>' + s + " / " + c.max + "</b></div>" +
      '<div class="ev-vdots" style="--p:' + ((s - 1) / (c.max - 1) * 100) + '%">' + dots + "</div>" +
      (st === "send" ? '<span class="ev-sent is-wait">' + ic("refresh") + "Envoi…</span>" : st === "ok" ? '<span class="ev-sent">' + ic("check") + "Confirmée</span>" : "") + "</div>" +
      c.rows.map(function (r2) { return '<div class="ev-row"><span class="ev-ri t-gold">' + ic(r2[0]) + "</span><span><small>" + esc(r2[1]) + "</small><b>" + esc(r2[2]) + "</b></span>" + ic("right", "ev-chev") + "</div>"; }).join("");
  };
  K.air = function (c, e) {
    var p = clamp((c.co2 - 400) / 1600 * 100, 0, 100), tone = c.co2 < 800 ? "ok" : c.co2 < 1200 ? "warn" : "err";
    return head("wind", c.title || "Qualité de l’air", c.sub || "Air intérieur", "") +
      '<div class="ev-semi">' + gauge(p, { sweep: 180, grad: ["#34d399", "#a3e07a", "#f3c969", "#e88a82"], cls: "is-semi" }) +
      '<div class="ev-semi-v"><small>CO₂</small><b>' + c.co2 + NB + "ppm</b><span>" + dot(tone) + esc(c.quality) + "</span></div></div>" +
      '<div class="ev-trio">' + c.rows.map(function (r) { return "<span>" + ic(r[0]) + "<small>" + esc(r[1]) + "</small><b>" + esc(r[2]) + "</b></span>"; }).join("") + "</div>";
  };
  K.outside = function (c, e) {
    var n = wxNow(e), w = e.wx;
    return head("sun", c.title || "Conditions extérieures", "Données locales · exemple", "") +
      '<div class="ev-out">' + wxi(n.code, n.night, "is-md") + "<div><b>" + deg(n.t) + "</b><span>" + n.cond + "</span></div></div>" +
      '<div class="ev-row">' + '<span class="ev-ri t-gold">' + ic("wind") + "</span><span><small>Vent</small><b>" + w.wind + NB + "km/h</b></span><em>" + esc(w.dir) + "</em></div>" +
      '<div class="ev-row"><span class="ev-ri t-gold">' + ic("thermo") + "</span><span><small>Ressenti</small><b>" + deg(n.feels) + "</b></span></div>";
  };
  /* Températures : une rangée par point, valeur et réglette de température (froid bleu → chaud orangé) */
  function tnum(v) { var m = /(−|-)?(\d+(?:,\d+)?)/.exec(String(v)); return m ? (m[1] ? -1 : 1) * parseFloat(m[2].replace(",", ".")) : null; }
  K.cold = function (c, e) {
    return head(c.icon || "fridge", c.title, c.sub, "") + '<div class="ev-temps">' + c.rows.map(function (r) {
      var T = tnum(r[2]), x = T == null ? null : clamp((T + 30) / 90 * 100, 0, 100);
      return '<div class="ev-temp"><span class="ev-ri t-water"' + (T != null ? ' style="--tc:' + tcol(T) + '"' : "") + ">" + ic(r[0]) + "</span><span><small>" + esc(r[1]) + "</small><b>" + unitize(r[2]) + "</b></span>" +
        (x != null ? '<span class="ev-tscale" aria-hidden="true"><i style="left:' + x.toFixed(1) + "%;--tc:" + tcol(T) + '"></i></span>' : "") + "</div>";
    }).join("") + "</div>";
  };
  var DIRS = { "Nord": 0, "Nord-est": 45, "Est": 90, "Sud-est": 135, "Sud": 180, "Sud-ouest": 225, "Ouest": 270, "Nord-ouest": 315 };
  /* Couleur d'une température (froid bleu → doux vert → chaud orangé), pour les plages des prévisions */
  var TSTOPS = [[-25, [79, 108, 255]], [-8, [102, 178, 255]], [3, [127, 224, 192]], [14, [255, 210, 92]], [24, [255, 138, 61]], [34, [255, 95, 61]]];
  function tcol(T) {
    for (var i = 1; i < TSTOPS.length; i++) {
      if (T <= TSTOPS[i][0] || i === TSTOPS.length - 1) {
        var a = TSTOPS[i - 1], b = TSTOPS[i], f = clamp((T - a[0]) / (b[0] - a[0]), 0, 1);
        return "rgb(" + a[1].map(function (v, k) { return Math.round(v + (b[1][k] - v) * f); }).join(" ") + ")";
      }
    }
    return "rgb(255 138 61)";
  }
  K.wxnow = function (c, e) {
    var n = wxNow(e), w = e.wx, sky = n.night ? (n.code === "d" || n.code === "p" ? "n" : n.code + " is-night") : n.code, from = DIRS[w.dir] != null ? DIRS[w.dir] : 270;
    var tiles = [
      ["Vent · " + esc(w.dir), w.wind + NB + "km/h", "Rafales " + w.gust + NB + "km/h", '<span class="ev-compass" style="--a:' + (from + 180) + 'deg">' + ic("nav") + "</span>"],
      ["Humidité", w.hum + NB + "%", "Point de rosée " + deg(w.dew), ic("drop")],
      ["Précipitations", n.pop + NB + "%", "Probabilité dans l’heure", ic("cloud")],
      ["Pression", w.hpa + NB + "hPa", cap(w.trend.toLowerCase()), ic("gauge")],
      ["Visibilité", w.vis + NB + "km", w.vis >= 20 ? "Excellente" : w.vis >= 8 ? "Bonne" : "Réduite", ic("eye")],
      ["Indice UV", String(w.uv), w.uv <= 2 ? "Faible" : w.uv <= 5 ? "Modéré" : "Élevé", ic("sun")]
    ].map(function (t) { return '<div class="ev-wxt"><span class="ev-wxt-i">' + t[3] + "</span><small>" + t[0] + "</small><b>" + t[1] + "</b><em>" + t[2] + "</em></div>"; }).join("");
    return '<div class="ev-wxhero sky-' + sky + '"><div class="ev-wxh-m">' + wxi(n.code, n.night, "is-xl") +
      '<div class="ev-wxh-t"><small>' + ic("pin", "is-sm") + esc(e.geo.place) + "</small><b>" + deg(n.t) + "</b><span>" + n.cond + "</span>" +
      "<em>Ressenti " + deg(n.feels) + '<i aria-hidden="true">·</i>Max. ' + deg(n.hi) + '<i aria-hidden="true">·</i>Min. ' + deg(n.lo) + "</em></div></div>" +
      '<div class="ev-wxh-s">' + tiles + "</div>" +
      '<p class="ev-wxh-f">' + ic("clock", "is-sm") + "Mise à jour à " + hm(NOW() - w.upd * 60000) + " · " + esc(w.src) + "</p></div>";
  };
  /* Prévisions horaires : 12 heures, courbe de température au-dessus des pictogrammes, lever et coucher marqués */
  K.hourly = function (c, e) {
    var now = NOW(), h0 = lp(now).h, N = c.n || 12, temps = [], cols = "", sd = sunDay(e), sd1 = sunDay(e, 1);
    var marks = [[sd.rise, "sunrise", "Lever"], [sd.set, "sunset", "Coucher"], [sd1.rise, "sunrise", "Lever"]];
    for (var i = 0; i < N; i++) {
      var t = now + i * 3600e3, hr = (h0 + i) % 24, T = i === 0 ? wxNow(e).t : e.wx.t24[hr], pop = popAt(e, t);
      temps.push(T);
      var mk = marks.filter(function (m) { return m[0] && m[0] > t - (i === 0 ? 0 : 1800e3) && m[0] <= t + 1800e3 && m[0] > now; })[0];
      cols += '<div class="' + (i === 0 ? "is-now" : "") + '"><small>' + (i === 0 ? "Maint." : hh(hr)) + "</small>" + wxi(skyAt(e, t), isNight(e, t)) +
        '<span class="ev-hp" title="Probabilité de précipitations"><i style="height:' + Math.max(4, pop) + '%"></i></span><em>' + pop + NB + "%</em>" +
        (mk ? '<span class="ev-hsun">' + ic(mk[1]) + hm(mk[0]) + "</span>" : "") + "</div>";
    }
    var lo = Math.min.apply(null, temps), hi = Math.max.apply(null, temps), rg = Math.max(1, hi - lo);
    var pts = temps.map(function (T, i) { return [(i + 0.5) / N * 1000, 14 + (1 - (T - lo) / rg) * 44]; }), id = uid();
    var lbl = temps.map(function (T, i) { return '<span style="left:' + ((i + 0.5) / N * 100).toFixed(2) + "%;top:" + (pts[i][1] - 4).toFixed(1) + 'px">' + nf(T) + "°</span>"; }).join("");
    var svg = '<svg class="ev-hrs-c" viewBox="0 0 1000 72" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="' + id + '" x1="0" y1="0" x2="1" y2="0">' +
      temps.map(function (T, i) { return '<stop offset="' + ((i + 0.5) / N).toFixed(3) + '" stop-color="' + tcol(T) + '"/>'; }).join("") + "</linearGradient></defs>" +
      '<path class="ev-hrs-a" d="' + sp(pts, false, 0.9) + " L1000 72 L0 72Z" + '" fill="url(#' + id + ')"/><path class="ev-hrs-l" d="' + sp(pts, false, 0.9) + '" stroke="url(#' + id + ')" vector-effect="non-scaling-stroke"/></svg>';
    return head("clock", "Prévisions horaires", "Les 12 prochaines heures · température, ciel et précipitations", "") +
      '<div class="ev-hrs"><div class="ev-hrs-in" style="--n:' + N + '"><div class="ev-hrs-cw">' + svg + '<div class="ev-hrs-lb">' + lbl + "</div></div>" +
      '<div class="ev-hrs-g">' + cols + "</div></div></div>";
  };
  /* Prévisions sur 5 jours : plage minimum-maximum colorée selon la température, position actuelle aujourd'hui */
  K.days = function (c, e) {
    var n = wxNow(e), rows = e.wx.days.map(function (d, i) { return { d: d, lo: i === 0 ? n.lo : d[2], hi: i === 0 ? n.hi : d[1] }; });
    var L = Math.min.apply(null, rows.map(function (r) { return r.lo; })), H = Math.max.apply(null, rows.map(function (r) { return r.hi; })), rg = Math.max(1, H - L);
    var html = rows.map(function (r, i) {
      var t = NOW() + i * 864e5, name = i === 0 ? "Aujourd’hui" : i === 1 ? "Demain" : cap(JOURS[wd(t)]);
      var a = (r.lo - L) / rg * 100, w = Math.max(6, (r.hi - r.lo) / rg * 100);
      var now = i === 0 ? '<em style="left:' + clamp((n.t - L) / rg * 100, 0, 100).toFixed(1) + '%" title="Maintenant : ' + deg(n.t) + '"></em>' : "";
      return '<div class="ev-dr' + (i === 0 ? " is-on" : "") + '"><b>' + name + "</b>" + wxi(ICON2CODE[r.d[0]] || "p", false) +
        '<span class="ev-dpop' + (r.d[3] >= 50 ? " is-hi" : "") + '">' + ic("drop") + r.d[3] + NB + "%</span>" +
        '<span class="ev-dt is-lo">' + nf(r.lo) + "°</span>" +
        '<span class="ev-drg"><i style="left:' + a.toFixed(1) + "%;width:" + w.toFixed(1) + "%;background:linear-gradient(90deg," + tcol(r.lo) + "," + tcol(r.hi) + ')"></i>' + now + "</span>" +
        '<span class="ev-dt">' + nf(r.hi) + "°</span></div>";
    }).join("");
    return head("calendar", "Prévisions sur 5 jours", "Minimum, maximum et risque de précipitations", "") + '<div class="ev-days">' + html + "</div>";
  };

  /* ---------- Soleil et lune (calculés pour la vraie date) ---------- */
  K.sun = function (c, e) {
    var sd = sunDay(e), now = NOW(), day = sd.rise && sd.set, len = day ? sd.set - sd.rise : 0;
    var p = day ? clamp((now - sd.rise) / len, -0.08, 1.08) : 0, isDay = now > sd.rise && now < sd.set;
    var next = now < sd.rise ? ["Avant le lever", sd.rise] : now < sd.set ? ["Avant le coucher", sd.set] : ["Avant le lever", sunDay(e, 1).rise];
    var x0 = 90, x1 = 910, base = 214, top = 46;
    function pt(q) { var x = x0 + (x1 - x0) * q, y = base - Math.sin(Math.PI * clamp(q, 0, 1)) * (base - top); return [x, y]; }
    var arcPts = [], passed = [];
    for (var i = 0; i <= 40; i++) { var q = i / 40; arcPts.push(pt(q)); if (q <= p) passed.push(pt(q)); }
    var sp2 = pt(clamp(p, 0, 1));
    var svg = '<svg class="ev-sunarc" viewBox="0 0 1000 260" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
      '<defs><linearGradient id="evsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="s-sky0"/><stop offset=".78" class="s-sky1"/><stop offset="1" class="s-sky2"/></linearGradient>' +
      '<radialGradient id="evglow" cx="50%" cy="100%" r="60%"><stop offset="0" class="s-glow0"/><stop offset="1" class="s-glow1"/></radialGradient>' +
      '<linearGradient id="evsea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="s-sea0"/><stop offset="1" class="s-sea1"/></linearGradient></defs>' +
      '<rect width="1000" height="260" fill="url(#evsky)"/><ellipse cx="' + (isDay ? sp2[0] : 500).toFixed(0) + '" cy="216" rx="420" ry="120" fill="url(#evglow)" class="s-gl' + (isDay ? "" : " is-night") + '"/>' +
      '<path class="s-water" d="M0 216H1000V260H0Z" fill="url(#evsea)"/>' + (isDay ? '<path class="s-refl" d="M' + (sp2[0] - 40).toFixed(0) + " 224h80M" + (sp2[0] - 26).toFixed(0) + " 234h52M" + (sp2[0] - 14).toFixed(0) + ' 244h28"/>' : "") +
      '<path class="s-arc" d="' + sp(arcPts, false) + '"/>' + (passed.length > 1 ? '<path class="s-arc is-done" d="' + sp(passed, false) + '"/>' : "") +
      '<line class="s-hz" x1="0" x2="1000" y1="216" y2="216"/>' +
      (isDay ? '<line class="s-drop" x1="' + sp2[0].toFixed(0) + '" x2="' + sp2[0].toFixed(0) + '" y1="' + sp2[1].toFixed(0) + '" y2="216"/>' : "") +
      '<circle class="s-end" cx="' + x0 + '" cy="' + base + '" r="7"/><circle class="s-end" cx="' + x1 + '" cy="' + base + '" r="7"/>' + "</svg>";
    var marker = isDay ? '<span class="ev-sundot" style="left:' + (sp2[0] / 10) + "%;top:" + (sp2[1] / 2.6) + '%"><b>' + hm(now) + "</b></span>" : "";
    return head("sun", "Cycle du soleil", cap(dateLong(now)) + " · " + esc(e.geo.place) + " · calculé", '<span class="ev-sunnext"><small>' + next[0] + "</small><b>" + dur(next[1] - now) + "</b></span>") +
      '<div class="ev-sunwrap">' + svg + marker + "</div>" +
      '<div class="ev-sunfoot"><span><b>' + (sd.rise ? hm(sd.rise) : "—") + "</b><small>Lever</small></span><span class=\"is-mid\"><b>" + dur(len) + "</b><small>Durée du jour</small></span><span><b>" + (sd.set ? hm(sd.set) : "—") + "</b><small>Coucher</small></span></div>" +
      (day ? '<div class="ev-sunbar"><small>' + (isDay ? "Jour écoulé" : now < sd.rise ? "Avant le lever" : "Jour terminé") + "</small>" + bar(clamp(p, 0, 1) * 100, "t-gold") + "<b>" + unitize(nf(clamp(p, 0, 1) * 100) + NB + "%") + "</b></div>" : "");
  };
  K.moments = function (c, e) {
    var sd = sunDay(e);
    var rows = [["sunrise", "Aube civile", sd.dawn, "t-water"], ["sun", "Lever du soleil", sd.rise, "t-gold"], ["sun", "Midi solaire", sd.noon, "t-gold"],
      ["sunset", "Coucher du soleil", sd.set, "t-gold"], ["moon", "Crépuscule civil", sd.dusk, "t-water"]];
    return head("clock", "Moments clés", "Heures locales · calculées", "") + rows.map(function (r) {
      return '<div class="ev-row"><span class="ev-ri ' + r[3] + '">' + ic(r[0]) + "</span><span><small>" + r[1] + "</small></span><b class=\"ev-mono\">" + (r[2] ? hm(r[2]) : "—") + "</b></div>";
    }).join("");
  };
  K.sunpos = function (c, e) {
    var s = sunAt(NOW(), e.geo.lat, e.geo.lon), card = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"][Math.round(s.az / 45) % 8];
    // Dôme : ellipse au sol (azimut), hauteur selon l'élévation
    var a = (s.az - 180) * RAD, gx = 200 + Math.sin(a) * 150, gy = 170 - Math.cos(a) * -38, el = Math.max(s.el, -4);
    var sx = gx, sy = gy - Math.sin(clamp(el, 0, 90) * RAD) * 120 * Math.cos(clamp(el, 0, 90) * RAD * 0.2);
    var up = s.el > -0.833;
    var svg = '<svg class="ev-dome" viewBox="0 0 400 210" aria-hidden="true"><path class="d-sky" d="M50 170 A150 140 0 0 1 350 170Z"/><ellipse class="d-ground" cx="200" cy="170" rx="150" ry="38"/>' +
      '<path class="d-mer" d="M200 30 V170 M50 170 A150 38 0 0 0 350 170"/><path class="d-mer is-f" d="M50 170 A150 140 0 0 1 350 170"/>' +
      '<line class="d-ray" x1="200" y1="170" x2="' + sx.toFixed(1) + '" y2="' + sy.toFixed(1) + '"/>' +
      '<circle class="d-foot" cx="' + gx.toFixed(1) + '" cy="' + gy.toFixed(1) + '" r="3"/><line class="d-drop" x1="' + gx.toFixed(1) + '" y1="' + gy.toFixed(1) + '" x2="' + sx.toFixed(1) + '" y2="' + sy.toFixed(1) + '"/>' +
      '<circle class="d-sun' + (up ? "" : " is-down") + '" cx="' + sx.toFixed(1) + '" cy="' + sy.toFixed(1) + '" r="9"/>' +
      '<text x="38" y="176">E</text><text x="356" y="176">O</text><text x="196" y="222" class="d-s">S</text><text x="196" y="124">N</text></svg>';
    return head("compass", "Position du soleil", up ? "Position actuelle · calculée" : "Sous l’horizon · position calculée", "") +
      '<div class="ev-sunpos"><div><div class="ev-row is-lg"><span class="ev-ri t-gold">' + ic("compass") + "</span><span><small>Azimut</small><b>" + nf(s.az) + "° " + card + "</b></span></div>" +
      '<div class="ev-row is-lg"><span class="ev-ri t-gold">' + ic("sliders") + "</span><span><small>Élévation</small><b>" + nf(s.el) + "°</b></span></div></div>" + svg + "</div>";
  };
  K.moon = function (c, e) {
    var m = moonInfo(NOW());
    return head("moon", "Lune", "Phase du jour · calculée", "") + '<div class="ev-moonw">' + moonSVG(m) +
      '<div><div class="ev-kv2"><small>Phase</small><b>' + m.name + "</b></div>" +
      '<div class="ev-kv2"><small>Illumination</small><b>' + nf(m.ill * 100) + NB + "%</b></div>" +
      '<div class="ev-kv2"><small>Prochaine pleine lune</small><b>' + cap(dateShort(m.full)) + "</b></div></div></div>";
  };

  /* ---------- Énergie ---------- */
  /* Flux d'énergie : scène en croix (production en haut, réseau à gauche, consommation à droite, stockage en bas)
     autour d'un nœud central. Les conduits sont tracés après affichage (HOOK.flow) à partir de la position réelle
     des nœuds; leur épaisseur suit la puissance et des particules lumineuses coulent dans le sens réel. */
  function flowModel(e) {
    var b = bat(e), en = e.energy, live = b.live, nodes = [], ex = exampleFlow(e), gridN = null, maxW = 1;
    ex.srcs.forEach(function (s, k) {
      var isGrid = en.sources[k][3] === "grid";
      var n = { k: s.k, label: s.label, icon: s.icon, w: live ? null : s.w, pos: isGrid ? "left" : "top", tone: isGrid ? "grid" : "prod" };
      if (live) { n.dir = "none"; n.state = "Capteur à relier"; }
      else if (isGrid) { gridN = n; }
      else { n.dir = s.w > 1 ? "in" : "none"; n.state = s.w > 1 ? "Production" : (s.note ? cap(s.note) : "En veille"); }
      nodes.push(n);
    });
    var known = ex.srcs.reduce(function (a, s, k) { return a + (en.sources[k][3] === "grid" ? 0 : s.w); }, 0);
    var bw = live ? b.w : ex.batt, load = live ? (b.flow === "out" ? Math.abs(b.w) : null) : ex.load;
    if (gridN && !live) {
      var exp = Math.max(0, known - ex.load - Math.max(0, bw));
      if (gridN.w > 1) { gridN.dir = "in"; gridN.state = "Importation"; }
      else if (exp > 1) { gridN.w = exp; gridN.dir = "out"; gridN.state = "Exportation"; }
      else { gridN.dir = "none"; gridN.state = "Au repos"; }
    }
    nodes.push({ k: "load", label: en.loads || "Charges", icon: e.icon === "rv" || !e.icon ? "home" : e.icon, w: load, pos: "right", tone: "load",
      dir: load == null ? "none" : load > 1 ? "out" : "none", state: load == null ? "Mesure à relier" : "Consommation" });
    var inB = live ? b.flow === "in" : bw > 5, outB = live ? b.flow === "out" : bw < -5;
    nodes.push({ k: "bat", label: en.store || "Batterie", icon: "battery", w: Math.abs(bw), pos: "bottom", tone: "bat", soc: b.soc,
      dir: inB ? "out" : outB ? "in" : "none", state: inB ? "En charge" : outB ? "En décharge" : "Au repos" });
    nodes.forEach(function (n) { if (n.w != null && n.dir !== "none") maxW = Math.max(maxW, n.w); });
    return { b: b, live: live, nodes: nodes, maxW: maxW, prod: known, load: load, bw: bw };
  }
  function flowNode(n, maxW) {
    var val = n.w == null ? '<b class="ev-fn-v is-na">—</b>' : '<b class="ev-fn-v">' + unitize(fmtW(n.w)) + "</b>";
    var disc = n.tone === "bat"
      ? '<span class="ev-fn-ic is-bat" style="--bc:' + batColor(n.soc) + '">' + ring(n.soc, batColor(n.soc)) + '<span class="ev-fn-soc">' + unitize(nf(n.soc) + NB + "%") + "</span></span>"
      : '<span class="ev-fn-ic">' + ic(n.icon) + "</span>";
    return '<div class="ev-fn is-' + n.pos + " t-" + n.tone + (n.dir !== "none" ? " is-on" : "") + '" data-fn="' + n.pos + '" data-dir="' + n.dir + '" data-tone="' + n.tone + '" data-pw="' + (n.w == null || n.dir === "none" ? 0 : (n.w / maxW).toFixed(3)) + '">' +
      disc + '<span class="ev-fn-t"><small>' + esc(n.label) + "</small>" + val + '<em class="ev-fn-s">' + (n.dir !== "none" ? dot(n.tone === "bat" ? (n.dir === "out" ? "ok" : "warn") : n.tone === "grid" && n.dir === "out" ? "ok" : "gold") : "") + esc(n.state) + "</em></span></div>";
  }
  K.flow = function (c, e) {
    var M = flowModel(e), en = e.energy, img = (e.banner || {}).img;
    var top = M.nodes.filter(function (n) { return n.pos === "top"; }), side = function (p) { return M.nodes.filter(function (n) { return n.pos === p; }).map(function (n) { return flowNode(n, M.maxW); }).join(""); };
    var net = M.live ? (M.bw > 0 ? "+" : "") + fmtW(M.bw) : fmtW(M.prod);
    var foot = M.live ? [["battery", "Batteries", (M.bw > 0 ? "+" : "") + fmtW(M.bw)], ["radar", "Sources et charges", "Capteurs à relier"]]
      : [["sun", "Production", fmtW(M.prod)], ["home", "Consommation", fmtW(M.load)], [M.bw >= 0 ? "battery" : "battery", M.bw > 5 ? "Stockage" : M.bw < -5 ? "Puisé des batteries" : "Batteries", (M.bw > 5 ? "+" : "") + fmtW(M.bw)]];
    if (!M.live && M.load > 0) foot.push(["leaf", "Autonomie du moment", nf(clamp(M.prod / M.load * 100, 0, 100)) + NB + "%"]);
    return head("bolt", "Flux d’énergie", M.live ? "Batteries mesurées · sources et charges à relier" : "Production, stockage et consommation en ce moment", liveTag(M.b)) +
      '<div class="ev-flow' + (M.live ? " is-live" : "") + (img ? " has-bg" : "") + '" data-flow style="--nt:' + top.length + '">' +
      (img ? '<span class="ev-flow-bg" aria-hidden="true"><img src="' + img + '" alt="" loading="lazy" decoding="async" style="object-position:' + ((e.banner || {}).pos || "50% 50%") + '"></span>' : "") +
      '<svg class="ev-flow-svg" data-flow-svg aria-hidden="true"></svg>' +
      '<div class="ev-flow-top">' + top.map(function (n) { return flowNode(n, M.maxW); }).join("") + "</div>" +
      '<div class="ev-flow-l">' + side("left") + "</div>" +
      '<div class="ev-flow-core" data-fn-core><span>' + ic("bolt") + "</span></div>" +
      '<div class="ev-flow-r">' + side("right") + "</div>" +
      '<div class="ev-flow-b">' + side("bottom") + "</div></div>" +
      '<div class="ev-flow-f">' + foot.map(function (f) { return "<span>" + ic(f[0], "is-sm") + "<small>" + f[1] + "</small><b>" + unitize(f[2]) + "</b></span>"; }).join("") + "</div>";
  };
  K.ring = function (c, e) {
    var b = bat(e), en = e.energy, color = batColor(b.soc), unit = en.unit, capT = en.cap;
    var avail = b.soc / 100 * capT, rows;
    rows = kv("Capacité nominale", nf(capT, capT < 30 && capT % 1 ? 1 : 0) + NB + unit) + kv("Tension", b.live && b.v ? nf(b.v, 2) + NB + "V" : en.v || en.nominal) +
      '<hr class="ev-hr">' + kv("Disponible", nf(avail, avail < 30 ? 1 : 0) + NB + unit) + kv("Réserve", en.reserve + NB + "%");
    return head("battery", en.ringTitle || "Batterie", "État de charge et informations", liveTag(b)) +
      '<div class="ev-ringw"><div class="ev-ringg">' + ring(b.soc, color) + '<div class="ev-ringv"><b style="color:' + color + '">' + nf(b.soc) + NB + "%</b><small>" + esc(en.chem) + "</small></div></div>" +
      '<div class="ev-ringr">' + rows + '<div class="ev-auton"><small>' + (b.flow === "in" ? "État" : "Autonomie") + "</small><b>" + esc(b.autonomy.replace("Autonomie estimée : ", "≈ ")) + "</b>" +
      (!b.live && b.flow === "out" ? "<small>à " + fmtW(exampleFlow(e).load) + " en ce moment</small>" : "") + "</div></div></div>";
  };
  /* Légende de courbe : pastille, nom et valeur repère (sous l'en-tête, jamais tassée à côté du titre) */
  function legend(items) {
    return '<div class="ev-lg">' + items.map(function (it) {
      return '<span class="ev-lg-i"><i class="c-' + it[0] + (it[3] ? " is-dash" : "") + '"></i><span><small>' + it[1] + "</small>" + (it[2] ? "<b>" + it[2] + "</b>" : "") + "</span></span>";
    }).join("") + "</div>";
  }
  K.history = function (c, e) {
    var b = bat(e);
    if (b.live && LIVE.hist) {
      var pts = LIVE.hist, vs = pts.map(function (p) { return p[1]; }), lo = Math.min.apply(null, vs), hi = Math.max.apply(null, vs), pad2 = Math.max(0.05, (hi - lo) * 0.2);
      var t0 = pts[0][0], t1 = pts[pts.length - 1][0], n = 48, res = [];
      for (var k = 0; k < n; k++) {
        var tt = t0 + (t1 - t0) * k / (n - 1), j = 0;
        while (j < pts.length - 2 && pts[j + 1][0] < tt) j++;
        var a = pts[j], bb = pts[j + 1], f = clamp((tt - a[0]) / Math.max(1, bb[0] - a[0]), 0, 1);
        res.push(a[1] + (bb[1] - a[1]) * f);
      }
      var xs = [0, 16, 32, 47].map(function (k2) { return [k2, hh(lp((t0 + (t1 - t0) * k2 / (n - 1)) * 1000).h)]; });
      var d24 = LIVE.d && LIVE.d.total && LIVE.d.total.delta24 != null ? (LIVE.d.total.delta24 >= 0 ? "+" : "") + nf(LIVE.d.total.delta24, 2) + NB + "kWh" : "—";
      return head("chart", "Énergie stockée · 24 h", "Mesures des batteries, en kWh", liveTag(b)) +
        legend([["green", "Maintenant", nf(res[n - 1], 2) + NB + "kWh"], ["green", "Plus haut", nf(hi, 2) + NB + "kWh"], ["green", "Plus bas", nf(lo, 2) + NB + "kWh"], ["gold", "Variation sur 24 h", d24]]) +
        plot({ n: n, min: lo - pad2, max: hi + pad2, h: 150, y: [lo, (lo + hi) / 2, hi], yf: function (v) { return nf(v, 1); }, series: [{ v: res, c: "green", area: true }], x: xs, vgrid: [16, 32],
          dots: [[n - 1, res[n - 1], "", "green"]], tip: { l: function (k3) { return hm((t0 + (t1 - t0) * k3 / (n - 1)) * 1000); }, f: function (v) { return nf(v, 2) + NB + "kWh"; }, names: ["Stockée"] } });
    }
    var so = solarDay(e), cons = loadCurve(e), prod = [];
    for (var h = 0; h < 24; h++) { var s4 = so ? (so.m[h * 4] + so.m[h * 4 + 1] + so.m[h * 4 + 2] + so.m[h * 4 + 3]) / 4 : 0; prod.push(s4); }
    var mx = Math.max.apply(null, prod.concat(cons)), top = Math.ceil(mx / 100) * 100 || 100;
    var sumP = prod.reduce(function (x, y) { return x + y; }, 0) / 1000, sumC = cons.reduce(function (x, y) { return x + y; }, 0) / 1000;
    var leg = [["gold", "Production solaire", nf(sumP, sumP < 10 ? 1 : 0) + NB + "kWh"], ["blue", "Consommation", nf(sumC, sumC < 10 ? 1 : 0) + NB + "kWh"]];
    if (sumC > 0) leg.push(["green", "Couverte par le solaire", nf(clamp(prod.reduce(function (x, y, k4) { return x + Math.min(y, cons[k4]); }, 0) / 1000 / sumC * 100, 0, 100)) + NB + "%"]);
    return head("chart", "Historique · veille", "Production et consommation, heure par heure · exemple", "") + legend(leg) +
      plot({ n: 24, min: 0, max: top * 1.08, h: 150, y: [0, top / 2, top], yf: function (v) { return fmtW(v).replace(NB + "W", "").replace(NB + "kW", NB + "k"); },
        series: [{ v: cons, c: "blue", area: true, op: 0.22 }, { v: prod, c: "gold", area: true }], x: [[0, "0 h"], [6, "6 h"], [12, "12 h"], [18, "18 h"], [23, "23 h"]], vgrid: [6, 12, 18],
        tip: { l: function (k5) { return hh(k5) + " – " + hh(k5 + 1); }, f: fmtW, names: ["Consommation", "Production"] } });
  };
  /* Consommateurs : pastille par appareil, part du total, barre fine graduée (or vers blanc), valeur à droite */
  K.bars = function (c, e) {
    var mx = Math.max.apply(null, c.rows.map(function (r) { return r[2]; })) || 1, tot = c.rows.reduce(function (a, r) { return a + r[2]; }, 0) || 1;
    return head(c.icon || "home", c.title, c.sub, '<span class="ev-tot"><small>Total</small><b>' + unitize(fmtW(tot)) + "</b></span>") +
      '<div class="ev-cons">' + c.rows.map(function (r) {
        var off = r[2] <= 0;
        return '<div class="ev-con' + (off ? " is-off" : "") + '"><span class="ev-ri' + (off ? " t-muted" : "") + '">' + ic(r[0]) + "</span>" +
          '<span class="ev-con-n"><b>' + esc(r[1]) + "</b><small>" + (off ? "À l’arrêt" : nf(r[2] / tot * 100) + NB + "% du total") + "</small></span>" +
          '<b class="ev-con-v">' + unitize(fmtW(r[2])) + "</b>" + bar(r[2] / mx * 100, "t-gold") + "</div>";
      }).join("") + "</div>";
  };
  K.chips = function (c, e) {
    var b = bat(e);
    return '<div class="ev-chips">' + c.items.map(function (it) {
      var v = it[2], t = it[3];
      if (t === "live") { v = b.flow === "in" ? "En cours" : b.flow === "out" ? "Décharge" : "Au repos"; t = b.flow === "in" ? "ok" : b.flow === "out" ? "warn" : "muted"; }
      if (v === "src") {
        if (b.live) { v = "Capteurs à relier"; t = "muted"; }
        else { var fl = exampleFlow(e).srcs.filter(function (s) { return s.w > 1; }).sort(function (a, b2) { return b2.w - a.w; }); v = fl.length ? fl.map(function (s) { return s.label; }).slice(0, 2).join(" + ") : "Aucune · batteries"; t = fl.length ? "gold" : "muted"; }
      }
      return '<div class="ev-chip"><span class="ev-ri t-gold">' + ic(it[0]) + "</span><span><small>" + esc(it[1]) + "</small><b>" + dot(t) + esc(v) + "</b></span></div>";
    }).join("") + "</div>";
  };
  /* Batteries : anneau gradué par batterie (vert, ambre, corail selon la charge), état, puis mesures en grille */
  K.packs = function (c, e) {
    var b = bat(e), u = e.energy.unit;
    return head("battery", e.energy.packsTitle || "Batteries", b.live ? "Mesures reçues " + ago((NOW() / 1000 - b.seen) / 60) : "Valeurs d’exemple", liveTag(b)) +
      '<div class="ev-packs">' + b.packs.map(function (p) {
        var col = batColor(p.soc), flag = p.online === false ? ["warn", "Hors ligne"] : p.problem ? ["warn", "Alerte BMS"] : p.a > 0.4 || p.charging ? ["ok", "En charge"] : p.a < -0.4 ? ["gold", "En utilisation"] : ["ok", p.soc >= 97 ? "Pleine · au repos" : "Au repos"];
        var spread = p.hi > 0 ? (p.hi - p.lo) * 1000 : null;
        var stats = [["Tension", nf(p.v, 2) + NB + "V"], ["Courant", (p.a > 0 ? "+" : "") + nf(p.a, 1) + NB + "A"], ["Température", p.t > -90 ? deg(p.t, 1) : "—"],
          ["Écart des cellules", spread != null ? nf(spread) + NB + "mV" : "—"], ["Cycles", p.cycles >= 0 ? String(p.cycles) : "—"], ["Capacité", p.cap ? nf(p.cap, p.cap % 1 ? 1 : 0) + NB + u : "—"]];
        return '<div class="ev-pack" style="--bc:' + col + '"><div class="ev-pack-h"><div class="ev-pack-g">' + ring(p.soc, col) + '<b class="ev-pack-v"><span>' + unitize(nf(p.soc) + NB + "%") + "</span></b></div>" +
          '<div class="ev-pack-t"><h6>' + esc(p.name) + '</h6><span class="ev-flag t-' + flag[0] + '">' + dot(flag[0]) + flag[1] + "</span>" +
          (spread != null ? '<small class="ev-pack-c">Cellules ' + nf(p.lo, 3) + " – " + nf(p.hi, 3) + NB + "V</small>" : "") + "</div></div>" +
          '<div class="ev-pack-s">' + stats.map(function (x) { return "<span><small>" + x[0] + "</small><b>" + unitize(x[1]) + "</b></span>"; }).join("") + "</div></div>";
      }).join("") + "</div>";
  };
  K.list = function (c, e) {
    var b = c.live ? bat(e) : null, rows = c.rows.map(function (r) {
      var v = r[2], t = r[3], extra = "";
      if (v === "live:link") { v = LIVE.ok ? "En ligne" : LIVE.ok === false ? "Indisponible" : "Connexion…"; t = LIVE.ok ? "ok" : "warn"; }
      if (v === "live:seen") { v = LIVE.ok && LIVE.d ? "Dernière lecture : " + ago((NOW() / 1000 - Math.max.apply(null, LIVE.d.batteries.map(function (x) { return x.seen || 0; }))) / 60) : "Liaison indisponible"; t = LIVE.ok ? "ok" : "warn"; }
      if (typeof v === "string" && v.indexOf("d:") === 0) { var x = v.slice(2).split(" "); v = relAt(dayAt(+x[0], x[1])); }
      if (c.live === "bms" && b && b.live && b.packs.length) {
        var all = function (k) { return b.packs.every(function (p) { return p[k]; }); };
        if (r[1] === "Charge autorisée") { v = all("chg") ? "Oui" : "Coupée"; t = all("chg") ? "ok" : "warn"; }
        if (r[1] === "Décharge autorisée") { v = all("dsg") ? "Oui" : "Coupée"; t = all("dsg") ? "ok" : "warn"; }
        if (r[1] === "Équilibrage des cellules") { v = b.packs.some(function (p) { return p.bal; }) ? "En cours" : "Au repos"; t = "muted"; }
        if (r[1] === "Alarme") { v = b.alarm || b.packs.some(function (p) { return p.problem; }) ? "À vérifier" : "Aucune"; t = v === "Aucune" ? "ok" : "warn"; }
      }
      if (r[4]) extra = ic("right", "ev-chev");
      return '<div class="ev-row' + (c.big ? " is-lg" : "") + '">' + (r[0] ? '<span class="ev-ri t-' + (c.tone || "gold") + '">' + ic(r[0]) + "</span>" : "") + "<span><small>" + esc(r[1]) + "</small></span>" +
        (v !== "" && v != null ? "<b" + (t ? ' class="t-' + t + '"' : "") + ">" + (t && t !== "muted" ? dot(t) : "") + esc(v) + "</b>" : "") + extra + "</div>";
    }).join("");
    return head(c.icon, c.title, c.sub || "", b ? liveTag(b) : "") + rows + (c.note ? '<p class="ev-fine">' + esc(c.note) + "</p>" : "");
  };
  K.solar = function (c, e) {
    var so = solarDay(e);
    if (!so) return "";
    var meas = so.m.slice(0, so.q + 1), fc = so.f.slice(so.q), mx = Math.max.apply(null, so.f.concat(so.m)), top = Math.max(50, Math.ceil(mx / 50) * 50);
    var sd = sunDay(e), first = Math.max(0, Math.floor((sd.rise - sd.m0) / 9e5) - 2), last = Math.min(95, Math.ceil((sd.set - sd.m0) / 9e5) + 2);
    var n = last - first + 1, m2 = so.m.slice(first, Math.min(so.q, last) + 1), f2b = so.q < last ? so.f.slice(Math.max(so.q, first), last + 1) : [];
    var xs = [];
    for (var h = Math.ceil(first / 4); h * 4 <= last; h += 2) xs.push([h * 4 - first, hh(h)]);
    var nowI = so.q >= first && so.q <= last ? so.q - first : null;
    var ser = [];
    if (m2.length > 1) ser.push({ v: m2, c: "gold", area: true });
    if (f2b.length > 1) ser.push({ v: f2b, c: "gold", dash: true, from: Math.max(so.q, first) - first });
    return head("sun", "Production solaire · aujourd’hui", "Mesure d’exemple jusqu’à maintenant, puis prévision",
      '<span class="ev-legend"><i class="c-gold"></i>Mesure<i class="c-gold is-dash"></i>Prévision</span>') +
      plot({ n: n, min: 0, max: top * 1.05, h: 190, y: [0, top / 2, top], yf: function (v) { return fmtW(v); }, series: ser, x: xs, now: nowI,
        tip: { l: function (k) { var q = first + k; return hh(Math.floor(q / 4)).replace(NB + "h", NB + "h" + NB + pad(q % 4 * 15)); }, f: fmtW, names: ["Mesure", "Prévision"], skip: function (si, j) { return ser.length > 1 && si === 1 && j === 0; } },
        dots: nowI != null ? [[nowI, so.m[so.q], nf(so.sofar / 1000, 2) + NB + "kWh à " + hm(NOW()), "gold"]] : [] }) +
      '<p class="ev-fine">' + ic("info") + "Lever " + hm(sd.rise) + " · coucher " + hm(sd.set) + " · courbe calculée selon la vraie hauteur du soleil. Une prévision n’est pas une mesure.</p>";
  };
  K.fwx = function (c, e) {
    return head("cloudsun", "Météo prévue", "Conditions d’ensoleillement pour aujourd’hui", "") +
      '<div class="ev-fwx"><div>' + wxi("p", false, "is-md") + "<span><small>Conditions</small><b>" + esc(c.cond) + "</b></span></div>" +
      "<div><small>Couverture nuageuse</small><b>" + c.cloud + NB + "%</b>" + bar(c.cloud, "t-gold") + "</div>" +
      '<div><small>Qualité de la prévision</small><b>' + ["Faible", "Moyenne", "Bonne", "Très bonne"][c.quality - 1] + '</b>' + bar(c.quality / 4 * 100, "t-gold") + "</div>" +
      "<div>" + ic("doc") + "<span><small>Source</small><b>" + esc(c.src) + "</b><small>" + cap(dateShort(NOW())) + "</small></span></div></div>";
  };

  /* ---------- Eau ---------- */
  var TANK = { clean: ["#5aa9ff", "#8fc8ff"], grey: ["#9aa3ad", "#c6ccd3"], black: ["#b07a4f", "#d39a68"], hot: ["#f0b45b", "#ffd28a"],
    fuel: ["#d9a24a", "#f3c969"], oil: ["#c99a5b", "#e6bd7f"], feed: ["#a3c27a", "#c7df9f"] };
  K.tanks = function (c, e) {
    return head("drop", c.title || "Niveaux des réservoirs", c.sub || "Niveaux actuels et volumes estimés", '<span class="ev-hint">' + ic("info") + "Volumes estimés</span>") +
      '<div class="ev-tanks">' + c.items.map(function (t) {
        var col = TANK[t[3]] || TANK.clean;
        return '<div class="ev-tank"><p>' + ic(t[3] === "clean" ? "waves" : t[3] === "fuel" ? "fuel" : "waves") + esc(t[0]) + "</p>" +
          '<div class="ev-gw">' + gauge(t[1], { grad: [col[0], col[1]] }) + "<b><span>" + unitize(t[1] + NB + "%") + "</span></b></div><small>" + nf(t[1] / 100 * t[2]) + " / " + t[2] + NB + (t[4] || "L") + "</small>" + bar(t[1], "", ";--bc:" + col[0]) + "</div>";
      }).join("") + "</div>";
  };
  K.levels = function (c, e) {
    return '<div class="ev-levels">' + c.items.map(function (t) {
      var col = TANK[t[3]] || TANK.clean;
      return '<div class="ev-level"><span class="ev-ri" style="--tc:' + col[0] + '">' + ic("drop") + "</span><div><p><b>" + esc(t[0]) + "</b><span>" + nf(t[1] / 100 * t[2]) + " / " + t[2] + NB + (t[4] || "L") + "</span></p>" +
        "<strong>" + t[1] + NB + "%</strong>" + bar(t[1], "", ";--bc:" + col[0]) + "</div></div>";
    }).join("") + "</div>";
  };
  K.hotwater = function (c, e) {
    return '<div class="ev-hot">' + dialCard(c, e, "hot", c.title || "Eau chaude", c.sub || "Température et mode", "heater", "°C") +
      '<div class="ev-row is-lg"><span class="ev-ri t-ok">' + ic("leaf") + "</span><span><small>Mode</small><b>" + esc(c.mode) + "</b></span>" + ic("right", "ev-chev") + "</div></div>";
  };
  K.pump = function (c, e) {
    return head(c.icon || "pump", c.title || "Pompe à eau", c.sub || "État et pression", '<span class="ev-flag t-' + (c.tone || "ok") + '">' + dot(c.tone || "ok") + esc(c.state) + "</span>") +
      '<div class="ev-inst">' + [["wind", c.l1 || "Débit actuel", c.flow], ["gauge", c.l2 || "Pression", c.pressure]].map(function (x) {
        return '<span class="ev-inst-i"><span class="ev-ri">' + ic(x[0]) + "</span><small>" + esc(x[1]) + "</small><b>" + unitize(x[2]) + "</b></span>";
      }).join("") + "</div>";
  };
  K.leaks = function (c, e) {
    return head("shield", c.title || "Prévention des fuites", "Surveillance en temps réel", "") +
      '<p class="ev-okline">' + ic("check") + (c.text || "Aucune fuite détectée") + "</p>" +
      '<div class="ev-sensors">' + c.sensors.map(function (s) { return "<span>" + ic(s[0]) + "<small>" + esc(s[1]) + "</small><b>" + dot(s[3] || "ok") + esc(s[2]) + "</b></span>"; }).join("") + "</div>";
  };
  K.gauge = function (c, e) {
    var col = c.pct >= 40 ? ["#34d399", "#7ee2b0"] : c.pct >= 20 ? ["#f3c969", "#f3c969"] : ["#e88a82", "#f0a59f"];
    return head(c.icon, c.title, c.sub, "") + '<div class="ev-gaugew"><div class="ev-semi">' + gauge(c.pct, { sweep: 180, grad: col, cls: "is-semi" }) +
      '<div class="ev-semi-v"><b>' + c.pct + NB + "%</b><small>" + esc(c.value) + "</small></div></div>" +
      '<div class="ev-est"><small>Estimation</small><b>' + esc(c.est) + "</b><small>" + esc(c.estsub || "") + "</small></div></div>";
  };
  K.usage = function (c, e) {
    var R = rng(hash(e.key + "use" + (c.seed || 0))), h0 = lp(NOW()).h, vals = [], mx = 0, sum = 0, xs = [];
    for (var i = 0; i < 24; i++) {
      var h = (h0 + 1 + i) % 24;
      var v = (h >= 6 && h <= 9) || (h >= 17 && h <= 21) ? 3 + R() * 6 : h >= 23 || h <= 5 ? R() * 0.6 : 0.5 + R() * 2.5;
      vals.push(v); sum += v;
      if (i % 6 === 0) xs.push([i, hh(h)]);
    }
    xs.push([23, "maint.", 1]);
    var k = c.total / sum, bars2 = vals.map(function (v, i) { mx = Math.max(mx, v * k); return [i, v * k, "blue"]; });
    var top = Math.ceil(mx);
    return head("chart", c.title || "Eau utilisée · 24 dernières heures", "Consommation totale · exemple", "") +
      '<div class="ev-usage" data-fill>' + legend([["blue", "Total · 24 h", nf(c.total) + NB + c.unit], ["blue", "Heure la plus forte", nf(mx, mx < 10 ? 1 : 0) + NB + c.unit]]) +
      plot({ n: 24, min: 0, max: top * 1.05, h: 96, y: [0, top / 2, top], yf: function (v) { return nf(v) + NB + c.unit; }, bars: bars2, x: xs,
        tip: { l: function (k) { return hh((h0 + 1 + k) % 24); }, f: function (v) { return nf(v, v < 10 ? 1 : 0) + NB + c.unit; }, names: ["Eau"] } }) + "</div>";
  };
  K.fill = function (c, e) {
    var p = pointsOf(e).filter(function (x) { return x.n === c.point; })[0];
    if (!p) return "";
    var M = e.maps[c.map], me = M.me;
    var route = { next: [me, [(me[0] + p.x) / 2 + 4, (me[1] + p.y) / 2 - 6], [p.x, p.y]] };
    var vw = 70, view = [(me[0] + p.x) / 2 - vw / 2, (me[1] + p.y) / 2 - vw * 0.3, vw, vw * 0.6];
    return '<div class="ev-fill"><div>' + head("pin", c.title || "Point de remplissage", "Aire de service la plus proche", "") +
      '<p class="ev-big">' + esc(p.dist) + '</p><p class="ev-fine">Destination d’exemple<br><b>' + esc(p.name) + "</b></p>" +
      '<button type="button" class="ev-btn" data-a="toast" data-v="Itinéraire d’exemple vers ' + esc(p.name) + ' : ' + esc(p.dist) + '. L’ouverture dans votre application de navigation viendra avec la liaison.">' + ic("nav") + "Itinéraire</button></div>" +
      mapView(e, { map: c.map, view: view, route: route, cls: "is-mini" }) + "</div>";
  };
  K.points = function (c, e) {
    var r = rt(e), flt = r.vals.pflt || "tous", added = r.vals.padd || {};
    var pts = pointsOf(e), sel = pts.filter(function (p) { return flt === "tous" || p.kind === flt || (flt === "vidange" && /vidange/i.test(p.what)) || (flt === "eau" && /eau|remplissage/i.test(p.what)); });
    var pins = pts.map(function (p) { return { x: p.x, y: p.y, n: p.n, tone: KIND[p.kind].tone, dim: sel.indexOf(p) < 0, title: p.name }; });
    var kinds = c.filters || [["tous", "Tous"], ["eau", "Remplissage"], ["vidange", "Vidange"], ["carburant", "Carburant"]];
    return '<div class="ev-pts">' + '<div class="ev-pts-m">' + head("pin", c.title || "Points de service", c.sub || "Aires de remplissage, vidange et services à proximité", "") +
      mapView(e, { map: c.map, view: c.view, pins: pins }) + "</div>" +
      '<div class="ev-pts-l"><div class="ev-seg" role="group" aria-label="Filtrer">' + kinds.map(function (k) {
        return '<button type="button" class="' + (flt === k[0] ? "is-on" : "") + '" data-a="pflt" data-v="' + k[0] + '" aria-pressed="' + (flt === k[0]) + '">' + k[1] + "</button>";
      }).join("") + "</div>" + sel.map(function (p) {
        var on = !!added[p.n];
        return '<article class="ev-pt"><span class="ev-ptn t-' + KIND[p.kind].tone + '">' + p.n + "</span><div><h6>" + esc(p.name) + " · " + esc(p.what) + "</h6><p>" + esc(p.dist) + " à vol d’oiseau</p><small>" + esc(p.info) + "</small></div>" +
          '<div class="ev-pt-a"><button type="button" class="ev-btn is-sm is-primary" data-a="toast" data-v="Fiche d’exemple : ' + esc(p.name) + '. Les fiches réelles viendront d’une source publique, avec leur date.">' + ic("doc") + "Voir la fiche</button>" +
          '<button type="button" class="ev-btn is-sm" data-a="toast" data-v="Itinéraire d’exemple vers ' + esc(p.name) + '.">' + ic("nav") + "Itinéraire</button>" +
          '<button type="button" class="ev-link' + (on ? " is-done" : "") + '" data-a="padd" data-v="' + p.n + '">' + ic(on ? "check" : "map") + (on ? "Ajouté au voyage" : "Ajouter au voyage") + "</button></div></article>";
      }).join("") + (sel.length ? "" : '<p class="ev-fine">Aucun point pour ce filtre dans le secteur.</p>') + "</div></div>";
  };
  K.note = function (c) { return '<p class="ev-note">' + ic(c.icon || "info") + "<span>" + esc(c.text) + "</span></p>"; };

  /* ---------- Sécurité ---------- */
  /* Ouvertures : une fiche par porte, fenêtre ou trappe, regroupées par zone; état clair, dernière ouverture,
     verrou à un geste (déverrouiller demande toujours confirmation), photo du lieu dès qu'elle est fournie. */
  function opsOf(e, c) {
    var r = rt(e);
    if (!r.ops) r.ops = c.points.map(function (o) { return { state: o.state, tone: o.tone, ago: o.ago, who: o.who, locked: /verrouill|cadenas/i.test(o.state) }; });
    return r.ops;
  }
  function findCard(e, type) {
    var out = null;
    Object.keys(e.s).forEach(function (k) {
      tabsOf(e, k).forEach(function (t) { t[2].forEach(function (c) { if (!out && c.type === type) out = c; }); });
    });
    return out;
  }
  K.openings = function (c, e) {
    var ops = opsOf(e, c), open = [], zones = [], byZ = {}, lockable = 0;
    c.points.forEach(function (o, j) {
      var st = ops[j];
      if (st.tone === "warn") open.push(j);
      if (o.lock && !st.locked) lockable++;
      if (!byZ[o.zone]) { byZ[o.zone] = []; zones.push(o.zone); }
      byZ[o.zone].push(j);
    });
    var closed = c.points.length - open.length;
    var banner = open.length ? '<div class="ev-opb t-warn"><span class="ev-opb-i">' + ic("warn") + "</span><span><b>" + open.map(function (j) { return esc(c.points[j].label); }).join(", ") +
        (open.length > 1 ? " restent ouvertes" : " " + (/e$/.test(ops[open[0]].state.split(" ")[0]) ? "restée " : "resté ") + esc(ops[open[0]].state.toLowerCase().split(" ")[0])) + "</b><small>Depuis " + dur(ops[open[0]].ago * 60000) +
        (ops[open[0]].who ? " · " + esc(ops[open[0]].who) : "") + "</small></span>" +
        '<button type="button" class="ev-btn is-sm" data-a="toast" data-v="Rappel prévu dans 30 minutes si l’ouverture est encore détectée.">' + ic("bell") + "Me le rappeler</button></div>"
      : '<div class="ev-opb t-ok"><span class="ev-opb-i">' + ic("check") + "</span><span><b>Tout est fermé" + (c.points.some(function (o) { return o.lock; }) ? " et verrouillé" : "") + "</b><small>Dernière vérification à " + hm(NOW() - 120000) + "</small></span></div>";
    var body = zones.map(function (z) {
      return '<div class="ev-opz"><p class="ev-opz-h">' + esc(z) + "<span>" + byZ[z].length + "</span></p><div class=\"ev-ots\">" + byZ[z].map(function (j) {
        var o = c.points[j], st = ops[j], ph = o.photo ? '<img src="' + o.photo + '" alt="' + esc(o.label) + '" loading="lazy" decoding="async">'
          : '<span class="ev-ot-pha">' + ic(o.icon || "door") + "<small>Photo à venir</small></span>";
        var since = st.tone === "warn" ? "Depuis " + dur(st.ago * 60000) : cap(ago(st.ago));
        var btn = o.lock ? '<button type="button" class="ev-ot-lk' + (st.locked ? " is-on" : "") + '" data-a="oplock" data-v="' + j + '" aria-label="' + (st.locked ? "Déverrouiller " : "Verrouiller ") + esc(o.label) + '"' + (st.busy ? " disabled" : "") + ">" +
          (st.busy ? ic("refresh", "is-spin") + "<span>Envoi…</span>" : ic(st.locked ? "lock" : "unlock") + "<span>" + (st.locked ? "Verrouillée" : "Verrouiller") + "</span>") + "</button>" : "";
        return '<article class="ev-ot t-' + st.tone + (st.locked ? " is-locked" : "") + '"><figure class="ev-ot-ph">' + ph + "</figure>" +
          '<div class="ev-ot-b"><b>' + esc(o.label) + '</b><span class="ev-ot-st">' + dot(st.tone) + esc(st.state) + "</span><small>" + since + (st.who ? " · " + esc(st.who) : "") + "</small></div>" + btn + "</article>";
      }).join("") + "</div></div>";
    }).join("");
    return head("lock", c.title, c.sub, '<span class="ev-opc"><b>' + closed + "</b> / " + c.points.length + " fermées</span>") + banner + body +
      (lockable ? '<button type="button" class="ev-btn is-wide" data-a="oplockall">' + ic("lock") + "Tout verrouiller (" + lockable + ")</button>" : "");
  };
  K.cams = function (c, e) {
    if (!c.items || !c.items.length) {
      return head("camera", c.title || "Caméras autorisées", "Accès caméra : propriétaire uniquement", "") +
        '<div class="ev-empty">' + ic("camera") + "<b>" + esc(c.empty) + "</b><small>" + esc(c.emptysub || "") + "</small></div>";
    }
    return head("camera", c.title || "Caméras autorisées", "Accès caméra : propriétaire uniquement", '<span class="ev-tag">aperçus d’exemple</span>') +
      '<div class="ev-cams">' + c.items.map(function (it) {
        return '<figure><img src="' + it[0] + '" alt="' + esc(it[2] || it[1]) + '" decoding="async"><figcaption><b>' + esc(it[1]) + "</b>" + (it[3] ? "<span>" + esc(it[3]) + "</span>" : "") + "</figcaption></figure>";
      }).join("") + "</div>";
  };
  K.events = function (c, e) {
    var log = rt(e).log.filter(function (l) { return l.sec; }).map(function (l) { return [(NOW() - l.t) / 60000, l.what, l.sub, l.tone]; });
    var items = log.concat(c.items);
    return head("clock", c.title || "Événements", "Activité récente", "") + '<ol class="ev-tl">' + items.slice(0, 5).map(function (it) {
      return '<li class="t-' + (it[3] || "ok") + '"><time>' + hm(NOW() - it[0] * 60000) + "</time><span><b>" + esc(it[1]) + "</b><small>" + esc(it[2]) + "</small></span></li>";
    }).join("") + "</ol>";
  };
  K.toggle = function (c, e) {
    var r = rt(e), on = r.tog[c.key] != null ? r.tog[c.key] : c.on;
    return '<div class="ev-tog">' + head(c.icon, c.title, on ? c.sub : (c.offsub || "Désactivée · aucune alerte ne sera envoyée"), sw(on, "tog", c.key, c.title)) + "</div>";
  };
  K.ec = function (c, e) {
    var n = wxNow(e), labels = [["warn", "Avertissements", "err"], ["bell", "Veilles", "warn"], ["info", "Avis", "water"], ["doc", "Bulletins", "muted"], ["check", "Fin d’alerte", "ok"]];
    var counts = '<div class="ev-ecc">' + labels.map(function (l, i) {
      return '<div class="' + (c.counts[i] ? "is-on" : "") + '"><span class="ev-ri t-' + l[2] + '">' + ic(l[0]) + "</span><span><small>" + l[1] + "</small><b>" + c.counts[i] + "</b></span></div>";
    }).join("") + "</div>";
    var a = c.alert, act = c.counts[0] + c.counts[1] + c.counts[2] + c.counts[3];
    var box = a ? '<div class="ev-alert t-' + (a.tone || "warn") + '"><span class="ev-alert-i">' + ic(a.icon || "info") + "</span><div><h6><em>" + esc(a.level) + "</em> · " + esc(a.title) + "</h6><p>" + esc(a.text) + "</p>" +
      "<small>Source : " + esc(a.src) + "<br>Calcul : " + cap(dateShort(NOW() - a.ago * 60000)) + ", " + hm(NOW() - a.ago * 60000) + " · mise à jour " + ago(a.ago) + "</small></div></div>" : "";
    return head("cloudsun", c.title, esc(c.sub || "Scénario d’exemple"), '<span class="ev-ecw">' + ic("pin", "is-sm") + esc(e.geo.place) + "<b>" + deg(n.t) + "</b>" + wxi(n.code, n.night) + "</span>") +
      counts + '<p class="ev-fine">' + act + " " + (act > 1 ? "alertes actives" : "alerte active") + " · fins d’alerte exclues</p>" + box;
  };
  K.danger = function (c, e) {
    var lv = ["Bas", "Modéré", "Élevé", "Très élevé", "Extrême"], cols = ["#34d399", "#f3c969", "#f0a24a", "#e8735f", "#c2413b"];
    var segs = "", a = -90;
    for (var i = 0; i < 5; i++) { segs += '<path d="' + arcD(50, 52, 40, a + 2, a + 34) + '" style="stroke:' + cols[i] + '" class="dg-s' + (i === c.level - 1 ? " is-on" : "") + '"/>'; a += 36; }
    var ang = -90 + (c.level - 0.5) * 36, tip = pol(50, 52, 33, ang);
    var svg = '<svg class="ev-danger" viewBox="0 0 100 60" aria-hidden="true">' + segs + '<line x1="50" y1="52" x2="' + tip[0].toFixed(1) + '" y2="' + tip[1].toFixed(1) + '" class="dg-n"/><circle cx="50" cy="52" r="3.5" class="dg-c"/></svg>';
    return head("fire", c.title, "Scénario d’exemple", "") + '<div class="ev-dgw">' + svg + '<div><small>Niveau de danger</small><b style="color:' + cols[c.level - 1] + '">' + lv[c.level - 1] + "</b>" +
      "<p>" + ic("tree") + esc(c.fires) + "</p>" + (c.note ? "<small>" + esc(c.note) + "</small>" : "") + "</div></div>" +
      '<button type="button" class="ev-btn is-wide" data-a="toast" data-v="Les règles locales (feux à ciel ouvert, restrictions) viendront de la SOPFEU et de la municipalité, avec leur date.">' + ic("link") + "Vérifier les règles locales" + ic("right") + "</button>" +
      '<p class="ev-fine">Source : ' + esc(c.src) + " · mise à jour " + ago(c.ago) + "</p>";
  };
  K.zone = function (c, e) {
    var M = e.maps[c.map], me = M.me, vw = c.radius * M.km * 2.9, view = [me[0] - vw / 2, me[1] - vw * 0.3, vw, vw * 0.6];
    return head("pin", c.title, "Autour de la position actuelle", "") + mapView(e, { map: c.map, view: view, ring: c.radius, cls: "is-zone" });
  };

  K.metar = function (c, e) {
    var rows = c.rows.map(function (r) { return '<div class="ev-row"><span class="ev-ri t-gold">' + ic(r[0]) + "</span><span><small>" + esc(r[1]) + "</small></span><b>" + esc(r[2]) + "</b></div>"; }).join("");
    return head("plane", c.title || "Météo aéronautique", esc(c.sub || ""), '<span class="ev-flag t-ok">' + esc(c.cat) + "</span>") +
      '<p class="ev-raw"><small>METAR · ' + esc(c.station) + "</small><code>" + esc(c.raw) + "</code></p>" + '<div class="ev-metar">' + rows + "</div>" +
      (c.taf ? '<p class="ev-raw"><small>Prévision (TAF) · exemple</small><code>' + esc(c.taf) + "</code></p>" : "") + '<p class="ev-fine">' + ic("info") + esc(c.note || "Exemple · consulter les sources officielles avant chaque vol.") + "</p>";
  };

  /* ---------- Internet ---------- */
  var NET = {};
  function netSeries(e, c) {
    var k = e.key;
    if (!NET[k]) {
      var R = rng(hash(k + "net")), dn = [], up = [];
      for (var i = 0; i < 30; i++) { dn.push(c.down * (0.7 + R() * 0.6) + (i > 12 && i < 17 ? c.down * 0.4 : 0)); up.push(c.up * (0.6 + R() * 0.8)); }
      NET[k] = { dn: dn, up: up, R: R };
    }
    return NET[k];
  }
  /* Courbes du réseau et du processeur : mêmes réglages au premier affichage et à chaque actualisation */
  function minAgo(k) { return k === 29 ? "Maintenant" : "Il y a " + Math.round((29 - k) / 2) + NB + "min"; }
  function netPlot(s) {
    var top = Math.max(1, Math.ceil(Math.max.apply(null, s.dn) * 1.15 / 5) * 5);
    return plot({ n: 30, min: 0, max: top, h: 110, y: [0, top / 2, top], yf: function (v) { return nf(v); }, series: [{ v: s.dn, c: "gold", area: true }, { v: s.up, c: "white" }],
      x: [[0, "15 min"], [10, "10 min"], [20, "5 min"], [29, "maint."]], cls: "is-net", tip: { l: minAgo, f: function (x) { return nf(x, x < 10 ? 1 : 0) + NB + "Mbit/s"; }, names: ["Téléchargement", "Téléversement"] } });
  }
  function sysPlot(c, v) {
    return plot({ n: 30, min: 0, max: 100, h: 70, y: [0, 50, 100], yf: function (x) { return x + NB + "%"; }, series: [{ v: v, c: "gold", area: true }], x: [[0, "15 min"], [29, "maint."]], cls: "is-sys",
      tip: { l: minAgo, f: function (x) { return nf(x) + NB + "%"; }, names: [c.title] } });
  }
  K.link = function (c, e) {
    var s = netSeries(e, c), dn = s.dn[s.dn.length - 1], up = s.up[s.up.length - 1], r = rt(e), test = r.vals.speed;
    var bars2 = "";
    for (var i = 1; i <= 4; i++) bars2 += "<i" + (i <= c.bars ? ' class="is-on"' : "") + ' style="height:' + (i * 25) + '%"></i>';
    var res = test === "run" ? '<span class="ev-sent is-wait">' + ic("refresh") + "Test en cours…</span>" : test ? '<span class="ev-sent">' + ic("check") + "Test d’exemple : " + nf(test[0], 1) + NB + "Mbit/s ↓ · " + nf(test[1], 1) + NB + "Mbit/s ↑ · " + test[2] + NB + "ms</span>" : "";
    return head(c.icon || "antenna", "Connexion active", esc(c.kind) + " · " + dot("ok") + '<span class="t-ok">Connecté</span>', '<span class="ev-sig"><small>Signal<br>' + (c.dbm ? nf(c.dbm) + NB + "dBm" : esc(c.sig || "")) + '</small><span class="ev-sigb">' + bars2 + "</span></span>") +
      '<div class="ev-thr"><div><small>Débit utilisé maintenant</small><p><span class="t-gold">' + ic("arrdown") + '<b data-net="dn">' + nf(dn, dn < 10 ? 1 : 0) + "</b>" + NB + "Mbit/s</span>" +
      '<span>' + ic("arrup") + '<b data-net="up">' + nf(up, up < 10 ? 1 : 0) + "</b>" + NB + "Mbit/s</span></p></div>" +
      '<button type="button" class="ev-btn is-primary" data-a="speed"' + (test === "run" ? " disabled" : "") + ">" + ic("gauge") + "Tester la vitesse</button></div>" + res +
      '<div data-net="plot" data-fill>' + netPlot(s) + "</div>" +
      '<span class="ev-legend is-below"><i class="c-gold"></i>Téléchargement<i class="c-white"></i>Téléversement</span>' +
      '<div class="ev-duo is-foot"><span>' + ic("clock") + "<small>Latence · 15 dernières minutes</small><b>" + c.ping + NB + "ms</b></span><span>" + ic("percent") + "<small>Pertes · 15 dernières minutes</small><b>" + esc(c.loss) + "</b></span></div>";
  };
  /* Compteur : jauge d'instrument (270°) à gauche, valeur utilisée sur le total à droite */
  K.meter = function (c, e) {
    var pct = c.used / c.total * 100, tone = pct >= 90 ? "#ef8d85" : pct >= 75 ? "#f3c969" : null;
    return head(c.icon, c.title, "", "") + '<div class="ev-meter"><div class="ev-meter-g">' + gauge(pct, tone ? { color: tone } : {}) + '<b class="ev-meter-p"><span>' + unitize(nf(pct) + NB + "%") + "</span></b></div>" +
      '<div class="ev-meter-v"><small>Utilisé</small><p class="ev-big">' + unitize(nf(c.used, c.used % 1 ? 1 : 0) + NB + c.unit) + '</p><small>sur ' + nf(c.total) + NB + c.unit + "</small></div></div>" +
      (c.note ? '<p class="ev-fine">' + esc(c.note) + "</p>" : "");
  };
  K.devices = function (c, e) {
    var n = c.groups.length;
    return head("router", "Appareils connectés", c.total + " appareils sur le réseau", "") + '<div class="ev-devs" style="--n:' + n + '"><span class="ev-dev-r">' + ic("router") + "<small>Routeur</small></span>" +
      '<span class="ev-dev-t" aria-hidden="true"></span><div class="ev-dev-g">' + c.groups.map(function (g) {
        return "<span>" + ic(g[0]) + "<em>" + g[1] + "</em><small>" + g[1] + " " + esc(g[2]) + "</small></span>";
      }).join("") + "</div></div>";
  };
  K.prio = function (c, e) {
    var r = rt(e);
    if (!r.prio) r.prio = c.items.map(function (x, i) { return i; });
    var auto = r.tog.autoswitch != null ? r.tog.autoswitch : true;
    return head("swap", "Priorités de connexion", auto ? "Bascule automatique en cas de perte de connexion" : "Bascule automatique désactivée", sw(auto, "tog", "autoswitch", "Bascule automatique")) +
      '<ol class="ev-prio">' + r.prio.map(function (k, i) {
        var it = c.items[k];
        return '<li data-k="' + k + '"><span class="ev-pn">' + (i + 1) + "</span>" + ic(it[0]) + "<b>" + esc(it[1]) + "</b>" +
          '<button type="button" class="ev-iconb" data-a="prio" data-v="' + i + ':-1" aria-label="Monter ' + esc(it[1]) + '"' + (i === 0 ? " disabled" : "") + ">" + ic("up") + "</button>" +
          '<button type="button" class="ev-iconb" data-a="prio" data-v="' + i + ':1" aria-label="Descendre ' + esc(it[1]) + '"' + (i === r.prio.length - 1 ? " disabled" : "") + ">" + ic("down") + "</button></li>";
      }).join("") + "</ol>";
  };
  var SYS = {};
  K.sys = function (c, e) {
    var k = e.key + c.icon;
    if (!SYS[k]) { var R = rng(hash(k)), a = []; for (var i = 0; i < 30; i++) a.push(clamp(c.value + (R() - 0.5) * 18 + Math.sin(i / 3) * 6, 3, 96)); SYS[k] = { v: a, R: R }; }
    var v = SYS[k].v;
    return head(c.icon, c.title, "", "") + '<p class="ev-big"><b data-sys="v">' + nf(v[v.length - 1]) + "</b>" + NB + '%</p><p class="ev-fine">' + esc(c.sub) + "</p>" +
      '<div data-sys="plot" data-fill>' + sysPlot(c, v) + "</div>";
  };
  K.actions = function (c, e) {
    var r = rt(e), st = r.vals.diag;
    return '<div class="ev-acts"><button type="button" class="ev-btn is-primary" data-a="diag"' + (st === "run" ? " disabled" : "") + ">" + ic("refresh") + (st === "run" ? "Actualisation…" : "Actualiser les diagnostics") + "</button>" +
      '<button type="button" class="ev-btn" data-a="toast" data-v="Les journaux du Hub s’ouvrent dans l’Administration, réservée à l’administrateur de votre système.">' + ic("doc") + "Consulter les journaux</button>" +
      '<button type="button" class="ev-btn" data-a="diag2">' + ic("link") + "Tester les connexions</button>" +
      (st && st !== "run" ? '<span class="ev-sent">' + ic("check") + "Diagnostics actualisés " + hm(st) + " · exemple</span>" : "") + "</div>";
  };

  /* ---------- Équipements ---------- */
  K.status = function (c, e) {
    var r = rt(e), mv = !!r.moving;
    return '<div class="ev-status' + (mv ? " is-moving" : "") + '"><span>' + dot(mv ? "warn" : "ok") + "<b>" + esc(mv ? (c.moveLabel || "Véhicule en mouvement") : c.still) + "</b><em>· " + esc(mv ? "Commandes verrouillées" : c.ok) + "</em></span>" +
      (c.moving ? '<label class="ev-sim">Simuler le mouvement ' + sw(mv, "move", "1", "Simuler le mouvement") + "</label>" : "") +
      '<span class="ev-lockn">' + ic("lock") + esc(c.lock) + "</span></div>";
  };
  K.equip = function (c, e, i) {
    var r = rt(e), st = r.eq[i] || {}, state = st.state || c.state, tone = st.tone || c.tone, busy = st.busy, a = c.act, mv = !!r.moving;
    var rows = (c.rows || []).map(function (x) { return kv(esc(x[0]), esc(x[1])); }).join("");
    var viz = c.spark ? plot({ n: c.spark.length, min: 0, max: 8, h: 54, y: [0, 4, 8], yf: function (v) { return v + NB + "°"; }, series: [{ v: c.spark, c: "gold" }], cls: "is-spark" }) : "";
    var action = "";
    if (a) {
      var locked = a.moving && mv, lab = st.flip ? (a.back || a.label) : a.label;
      action = '<button type="button" class="ev-btn is-wide' + (a.preview ? "" : "") + '" data-a="eq" data-v="' + i + '"' + (busy || locked ? " disabled" : "") + ">" + (busy ? ic("refresh", "is-spin") + "Commande envoyée…" : locked ? ic("lock") + "Verrouillé en mouvement" : ic(a.icon || "play") + esc(lab)) + "</button>";
    }
    if (c.toggle) {
      var on = !!st.on;
      action = '<div class="ev-eqt">' + ic("power") + "<span>" + esc(c.toggle.label) + "</span>" + sw(on, "eqt", String(i), c.toggle.label) + "</div>";
      state = on ? c.toggle.on : c.toggle.off; tone = on ? "ok" : "muted";
    }
    var ph = c.photo ? '<img src="' + c.photo + '" alt="' + esc(c.title) + '" loading="lazy" decoding="async">' : '<span class="ev-eq-pha">' + ic(c.icon) + "<small>Photo à venir</small></span>";
    return head(c.icon, c.title, c.sub, "") + '<div class="ev-eq"><figure class="ev-eq-ph' + (c.photo ? " has-img" : "") + '">' + ph + "</figure><div class=\"ev-eq-s\"><small>État</small><b class=\"t-" + tone + '">' + dot(tone) + esc(state) + "</b>" + rows + "</div></div>" + viz +
      action + (c.note ? '<p class="ev-fine is-c">' + ic("info") + esc(c.note) + "</p>" : "");
  };
  /* ---------- Hangar à plusieurs appareils : l'abri commun et chaque appareil d'un regard ---------- */
  function fleetOf(e) { return e.hangar ? e.hangar.fleet.filter(function (k) { return E[k]; }) : [e.key]; }
  function urgentOf(k) { return siteOf(E[k]).alerts.filter(function (a) { return a.tone === "err" || a.tone === "warn"; }); }
  K.hangar = function (c, e) {
    var H0 = e.hangar, ks = fleetOf(e);
    var rows = '<div class="ev-hg-r">' + H0.rows.map(function (r) {
      return "<span>" + ic(r[0]) + "<small>" + esc(r[1]) + "</small><b>" + dot(r[3] || "ok") + esc(r[2]) + "</b></span>";
    }).join("") + "</div>";
    var planes = ks.map(function (k) {
      var p = E[k], P0 = p.plane || {}, me = k === e.key, u = urgentOf(k).length, st = P0.state || ["", "ok"];
      var inner = '<figure class="ev-hg-ph' + (P0.photo ? " has-img" : "") + '">' + bph(P0.photo, p.name, p.icon) +
        '<span class="ev-hg-spot">' + esc(P0.spot || "") + "</span>" +
        (u ? '<span class="ev-hg-al">' + ic("bell", "is-sm") + u + " alerte" + (u > 1 ? "s" : "") + "</span>" : "") + "</figure>" +
        '<span class="ev-hg-b"><span class="ev-hg-k">' + ic(p.icon) + esc(p.kind) + "</span><b class=\"ev-hg-n\">" + esc(p.name) + "</b>" +
        '<span class="ev-hg-st t-' + st[1] + '">' + dot(st[1]) + esc(st[0]) + "</span>" +
        '<span class="ev-hg-kp">' + (P0.kpis || []).map(function (x) { return "<span>" + ic(x[0], "is-sm") + "<small>" + esc(x[1]) + "</small><b>" + esc(x[2]) + "</b></span>"; }).join("") + "</span>" +
        '<span class="ev-hg-go">' + (me ? ic("check", "is-sm") + "Tableau ouvert" : "Ouvrir ce tableau" + ic("right", "is-sm")) + "</span></span>";
      return me ? '<div class="ev-hg-p is-cur" aria-current="true">' + inner + "</div>"
        : '<button type="button" class="ev-hg-p" data-a="plane" data-v="' + k + '">' + inner + "</button>";
    }).join("");
    return head("hangar", "Le hangar · " + ks.length + " appareils", esc(H0.name) + " · " + esc(H0.sub), '<span class="ev-tag">exemple</span>') + rows + '<div class="ev-hg">' + planes + "</div>";
  };

  /* ---------- Ferme : vue d'ensemble des bâtiments et en-tête du détail d'un bâtiment ---------- */
  function bph(src, alt, icon, label) {
    return src ? '<img src="' + src + '" alt="' + esc(alt) + '" loading="lazy" decoding="async">'
      : '<span class="ev-bph-a" role="img" aria-label="' + esc(alt) + ' · photo à venir">' + ic(icon) + "<small>" + esc(label || "Photo à venir") + "</small></span>";
  }
  var BTONE = { ok: "Normal", gold: "Surveillé", warn: "À vérifier", muted: "En veille" };
  K.batiments = function (c, e) {
    var n = c.items.length, warn = c.items.filter(function (b) { return b.tone === "warn"; }).length;
    var right = '<span class="ev-count"><b>' + (n - warn) + "</b> / " + n + " normaux</span>" + (warn ? '<span class="ev-tag t-warn">' + warn + " à vérifier</span>" : "");
    return head("barn", c.title, esc(c.sub || ""), right) + '<div class="ev-bats">' + c.items.map(function (b) {
      return '<button type="button" class="ev-bat" data-tone="' + b.tone + '" data-a="go" data-v="' + esc(b.go) + '">' +
        '<figure class="ev-bat-ph' + (b.photo ? " has-img" : "") + '">' + bph(b.photo, b.name, b.icon) +
        '<span class="ev-bat-st">' + dot(b.tone) + esc(b.state || BTONE[b.tone] || "") + "</span></figure>" +
        '<span class="ev-bat-b"><span class="ev-bat-n">' + ic(b.icon) + "<b>" + esc(b.name) + "</b></span>" +
        '<span class="ev-bat-k">' + b.kpis.map(function (k) { return "<span><small>" + esc(k[0]) + "</small><b>" + esc(k[1]) + "</b></span>"; }).join("") + "</span>" +
        '<span class="ev-bat-a">' + ic(b.tone === "warn" ? "warn" : "info") + "<span>" + esc(b.alert) + "</span>" + ic("right", "ev-chev") + "</span></span></button>";
    }).join("") + "</div>";
  };
  K.batiment = function (c, e) {
    var chips = (c.chips || []).map(function (x) { return '<span class="ev-bh-c" data-tone="' + (x[3] || "ok") + '">' + ic(x[0]) + "<small>" + esc(x[1]) + "</small><b>" + dot(x[3] || "ok") + esc(x[2]) + "</b></span>"; }).join("");
    var src = (c.sources || []).map(function (s) { return "<span>" + ic("radar") + esc(s) + "</span>"; }).join("");
    return '<div class="ev-bh"><div class="ev-bh-ph">' +
      '<figure class="ev-bat-ph' + (c.photoExt ? " has-img" : "") + '">' + bph(c.photoExt, "Extérieur · " + c.name, c.icon) + "<figcaption>Extérieur</figcaption></figure>" +
      '<figure class="ev-bat-ph' + (c.photoInt ? " has-img" : "") + '">' + bph(c.photoInt, "Intérieur · " + c.name, c.icon) + "<figcaption>Intérieur</figcaption></figure></div>" +
      '<div class="ev-bh-b">' + head(c.icon, c.name, esc(c.sub || ""), '<span class="ev-tag">données d’exemple</span>') +
      '<div class="ev-bh-cs">' + chips + "</div>" +
      (src ? '<p class="ev-k">Sources de données</p><div class="ev-bh-src">' + src + "</div>" : "") + "</div></div>";
  };
  K.inspection = function (c, e) {
    var t = dayAt(c.d, c.h || "14:00");
    return '<div class="ev-insp"><span class="ev-ci">' + ic("calendar") + "</span><span><b>" + esc(c.title) + "</b><small>" + esc(c.sub) + "</small></span>" +
      '<span class="ev-insp-d">' + ic("calendar") + cap(dateLong(t)) + "</span>" +
      '<button type="button" class="ev-btn" data-a="go" data-v="' + c.go + '">Voir l’entretien' + ic("right") + "</button></div>";
  };

  /* ---------- Voyage, agenda, listes, entretien ---------- */
  /* À l'arrivée : conditions sur place, heure d'arrivée estimée (d'après le voyage lié) et lumière du jour */
  K.arrival = function (c, e) {
    var tr = findCard(e, "trip"), sd = sunDay(e), now = NOW(), m = tr && /(\d+)\s*h(?:\s*(\d+))?|(\d+)\s*min/.exec(tr.dur || ""), mins = m ? (m[3] ? +m[3] : +m[1] * 60 + (+m[2] || 0)) : null;
    var eta = mins != null ? now + mins * 60000 : null, rows = [["wind", "Vent", c.wind.replace(/^Vent\s*/, "")]];
    if (eta) rows.unshift(["clock", "Arrivée estimée", hm(eta) + (tr.dist ? " · " + tr.dist : "")]);
    if (sd.set) rows.push([now < sd.set ? "sunset" : "sunrise", now < sd.set ? "Coucher du soleil" : "Lever du soleil", now < sd.set ? hm(sd.set) + (eta && eta > sd.set ? " · arrivée de nuit" : " · arrivée de jour") : hm(sunDay(e, 1).rise)]);
    return head("pin", "À l’arrivée", esc(c.place), '<span class="ev-tag">exemple</span>') +
      '<div class="ev-arr"><div class="ev-out is-arr">' + wxi(ICON2CODE[c.icon] || "c", false, "is-lg") + "<div><b>" + unitize(deg(c.temp)) + "</b><span>" + esc(c.cond) + "</span></div></div>" +
      rows.map(function (r) { return '<div class="ev-row"><span class="ev-ri t-gold">' + ic(r[0]) + "</span><span><small>" + r[1] + "</small><b>" + esc(r[2]) + "</b></span></div>"; }).join("") + "</div>" +
      '<p class="ev-fine">' + ic("info") + "Conditions d’exemple · heure estimée selon le voyage lié.</p>";
  };
  K.agenda = function (c, e) {
    var r = rt(e), wk = r.vals.week || 0, today = midnight(NOW()), dow = (wd(NOW()) + 6) % 7;
    var monday = midnight(today - dow * 864e5 + wk * 7 * 864e5 + 5 * 3600e3), h0 = 8, h1 = 18;
    var days = "", cols = "", evs = "";
    for (var d = 0; d < 7; d++) {
      var t = midnight(monday + d * 864e5 + 5 * 3600e3), isT = t === today, p = lp(t);
      days += '<div class="' + (isT ? "is-today" : "") + '"><small>' + JC[(d + 1) % 7] + "</small><b>" + p.d + "</b></div>";
      cols += '<div class="' + (isT ? "is-today" : "") + '"></div>';
    }
    c.events.forEach(function (ev) {
      var t0 = dayAt(ev[0], ev[1]), di = Math.round((midnight(t0) - monday) / 864e5), span = ev[5] || 1;
      if (di + span - 1 < 0 || di > 6) return;
      var a = Math.max(0, di), b2 = Math.min(6, di + span - 1);
      var x = ev[1].split(":"), y0 = (+x[0] + x[1] / 60 - h0) / (h1 - h0) * 100;
      var y1 = ev[2] ? ((+ev[2].split(":")[0] + ev[2].split(":")[1] / 60 - h0) / (h1 - h0) * 100) : y0 + 7;
      evs += '<div class="ev-ag-e is-' + ev[4] + '" title="' + esc(ev[3]) + '" style="--c0:' + a + ";--c1:" + (b2 + 1) + ";top:" + clamp(y0, 0, 96).toFixed(1) + "%;height:" + Math.max(6, y1 - y0).toFixed(1) + '%">' +
        ic(ev[4] === "maint" ? "wrench" : ev[4] === "peak" ? "bolt" : ev[4] === "flight" ? "plane" : ev[4] === "event" ? "calendar" : "bed") + "<span><b>" + esc(ev[3]) + "</b>" + (ev[4] !== "stay" ? "<small>" + ev[1].replace(":", NB + "h" + NB) + (ev[2] ? " – " + ev[2].replace(":", NB + "h" + NB) : "") + "</small>" : "") + "</span></div>";
    });
    var last = midnight(monday + 6 * 864e5 + 5 * 3600e3), pm = lp(monday), pl = lp(last);
    var title = pm.m === pl.m ? pm.d + " – " + pl.d + " " + MOIS[pl.m - 1] + " " + pl.y : pm.d + " " + MOIS[pm.m - 1] + " – " + pl.d + " " + MOIS[pl.m - 1] + " " + pl.y;
    var hrs = "";
    for (var h = h0; h <= h1; h += 2) hrs += '<span style="top:' + ((h - h0) / (h1 - h0) * 100) + '%">' + hh(h) + "</span>";
    return head("calendar", title, "", '<div class="ev-agn"><button type="button" class="ev-iconb" data-a="week" data-v="-1" aria-label="Semaine précédente">' + ic("left") + "</button>" +
      '<button type="button" class="ev-btn is-sm" data-a="week" data-v="0">Aujourd’hui</button><button type="button" class="ev-iconb" data-a="week" data-v="1" aria-label="Semaine suivante">' + ic("right") + "</button></div>") +
      '<div class="ev-ag"><div class="ev-ag-d">' + days + '</div><div class="ev-ag-b"><div class="ev-ag-h">' + hrs + '</div><div class="ev-ag-c">' + cols + evs + "</div></div></div>" +
      '<p class="ev-legend is-below"><i class="c-gold"></i>' + esc(c.l1 || "Réservations (campings, étapes)") + '<i class="c-blue"></i>' + esc(c.l2 || "Entretien (rendez-vous, inspections)") + "</p>";
  };
  K.next = function (c, e) {
    var t = c.d != null ? dayAt(c.d, c.h) : null;
    return '<div class="ev-next"><span class="ev-ci">' + ic(c.icon) + "</span><div><small>" + esc(c.kick) + "</small><b>" + esc(c.title) + "</b>" +
      (t ? "<p>" + cap(dateLong(t)) + " · " + hm(t) + "</p>" : "") + (c.countdown && t ? '<strong>Dans ' + dur(t - NOW()) + "</strong>" : "") + (c.text ? "<p>" + esc(c.text) + "</p>" : "") + "</div></div>";
  };
  K.lists = function (c, e) {
    var r = rt(e), cur2 = r.vals.list || c.lists[0].k, L = c.lists.filter(function (l) { return l.k === cur2; })[0] || c.lists[0];
    var st = checks(e, "list:" + L.k, L.items.map(function (x) { return [x[0], x[2]]; })), done = st.filter(Boolean).length;
    var selI = r.vals["lsel:" + L.k];
    if (selI == null) selI = st.indexOf(false);
    var tabs = '<div class="ev-seg is-lists" role="group" aria-label="Listes">' + c.lists.map(function (l) { return '<button type="button" class="' + (l.k === L.k ? "is-on" : "") + '" data-a="list" data-v="' + l.k + '" aria-pressed="' + (l.k === L.k) + '">' + esc(l.l) + "</button>"; }).join("") + "</div>";
    var items = L.items.map(function (it, i) {
      return '<li class="' + (i === selI ? "is-sel" : "") + '"><button type="button" class="ev-check' + (st[i] ? " is-on" : "") + '" data-a="chk" data-v="list:' + L.k + ":" + i + '" aria-pressed="' + st[i] + '" aria-label="' + esc(it[0]) + '"><span class="ev-box">' + ic("check") + "</span></button>" +
        '<button type="button" class="ev-li" data-a="lsel" data-v="' + L.k + ":" + i + '"><span><span>' + esc(it[0]) + "</span>" + srcChip(it[3]) + "</span><small>" + (st[i] ? "Fait" : "À valider") + "</small>" + ic("right", "ev-chev") + "</button></li>";
    }).join("");
    var sel = selI >= 0 ? L.items[selI] : null;
    var detail = sel ? '<div class="ev-ld">' + head("box", sel[0], "", "") + '<span class="ev-flag t-' + (st[selI] ? "ok" : "warn") + '">' + (st[selI] ? "Terminé" : "À faire") + "</span>" +
      (sel[1] ? '<p class="ev-ld-n">' + esc(sel[1]) + "</p>" : "") +
      '<div class="ev-why"><p class="ev-k">D’où vient cet élément?</p>' + srcChip(sel[3], true) + "<small>" + (SRC[(sel[3] || {}).k] || SRC.jarvis)[2] + "</small>" +
      '<p class="ev-why-v">' + ic(sel[3] && sel[3].k === "capteur" ? "radar" : "users2") + (sel[3] && sel[3].k === "capteur" ? "Validation automatique par le capteur, confirmable à la main" : "Validation manuelle") + "</p></div>" +
      '<button type="button" class="ev-btn is-primary is-wide" data-a="chk" data-v="list:' + L.k + ":" + selI + '">' + ic("check") + (st[selI] ? "Marquer comme à faire" : "Marquer comme terminé") + "</button></div>"
      : '<div class="ev-ld is-done">' + ic("check") + "<b>Liste terminée.</b><small>Tout est prêt.</small></div>";
    var others = c.lists.filter(function (l) { return l.k !== L.k; }).map(function (l) {
      var s2 = checks(e, "list:" + l.k, l.items.map(function (x) { return [x[0], x[2]]; })), d2 = s2.filter(Boolean).length;
      return '<button type="button" class="ev-lsum" data-a="list" data-v="' + l.k + '"><span class="ev-ci">' + ic(l.icon || "list") + "</span><span><b>" + esc(l.l) + "</b><small>" + esc(l.sub) + "</small></span><em>" + d2 + " / " + s2.length + "<small>" + nf(d2 / s2.length * 100) + NB + "%</small></em>" + bar(d2 / s2.length * 100, "t-gold") + "</button>";
    }).join("");
    return '<div class="ev-lists-h"><div><h5>' + esc(c.title || "Listes de bord") + "</h5><p>" + esc(c.sub || "Des listes simples et complètes pour voyager l’esprit tranquille.") + "</p></div>" + tabs + "</div>" +
      '<div class="ev-lists"><div class="ev-lmain">' + head(L.icon || "list", L.l, esc(L.sub), '<span class="ev-count"><b>' + done + "</b> / " + st.length + " terminés · " + nf(done / st.length * 100) + NB + "%</span>" + bar(done / st.length * 100, "t-gold is-sm")) +
      '<ul class="ev-litems">' + items + "</ul></div>" + detail + "</div>" + '<div class="ev-lsums">' + others + "</div>";
  };
  /* Échéance d'un entretien selon sa source (les règlements à date fixe sont calculés pour la vraie date) */
  function dueOf(s) {
    if (s.basis !== "date-fixe") return s.due;
    var p = lp(NOW()), x = s.mmdd.split("-"), today = Date.UTC(p.y, p.m - 1, p.d), target = Date.UTC(p.y, +x[0] - 1, +x[1]);
    if (target < today) target = Date.UTC(p.y + 1, +x[0] - 1, +x[1]);
    return Math.round((target - today) / 864e5);
  }
  function fmtN(v) { return nf(v, v % 1 ? 1 : 0); }
  K.maint = function (c, e) {
    var r = rt(e), plan = r.vals.mplan || {}, kinds = {};
    var rows = c.rows.map(function (m, i) {
      var s = m[5], due = s ? dueOf(s) : m[3], tone = due < 0 ? "err" : due <= 14 ? "warn" : "ok", lab = due < 0 ? "En retard" : due <= 14 ? "Bientôt" : "À jour";
      var t = dayAt(due, "09:00"), when = due < 0 ? "En retard de " + (-due) + NB + "j" : due === 0 ? "Aujourd’hui" : "Dans " + due + NB + "j · " + dateShort(t);
      var prog = null, calc = "";
      if (s) {
        kinds[s.k] = (kinds[s.k] || 0) + 1;
        if (s.basis === "date") { prog = -s.last / s.n; calc = "Fait il y a " + (-s.last) + NB + "j · à refaire " + s.every; }
        else if (s.basis === "count") { prog = s.now / s.at; calc = fmtN(s.now) + NB + s.unit + " depuis le dernier entretien, sur " + fmtN(s.at) + NB + s.unit + " · rythme ≈ " + fmtN(s.rate) + NB + s.unit + " par jour"; }
        else if (s.basis === "date-fixe") calc = "Date limite : " + dateLong(t);
        else calc = s.why || "";
      }
      return '<div class="ev-mrow t-' + tone + '"><span class="ev-ri t-' + tone + '">' + ic(m[0]) + '</span><div class="ev-mb"><p class="ev-mt"><b>' + esc(m[1]) + "</b><small>" + esc(m[2]) + "</small></p>" +
        (s ? '<p class="ev-msrc">' + srcChip(s) + "<span>" + esc(s.ref) + "</span></p>" : "") +
        (prog != null ? '<span class="ev-mprog" title="' + nf(clamp(prog, 0, 1.5) * 100) + ' % de l’intervalle"><i style="width:' + clamp(prog * 100, 2, 100).toFixed(1) + '%"></i></span>' : "") +
        (calc ? '<p class="ev-mcalc">' + ic("info") + "<span>" + esc(calc) + " → <b>" + (due < 0 ? "en retard de " + (-due) + NB + "j" : due === 0 ? "échéance aujourd’hui" : "échéance dans " + due + NB + "j") + "</b></span></p>" : "") + "</div>" +
        '<div class="ev-mside"><span class="ev-flag t-' + tone + '">' + lab + '</span><span class="ev-mwhen">' + when + "</span>" +
        '<button type="button" class="ev-btn is-sm' + (plan[i] ? " is-done" : "") + '" data-a="mplan" data-v="' + i + '">' + (plan[i] ? ic("check") + "Planifié" : "Planifier") + "</button></div></div>";
    }).join("");
    var legend = Object.keys(SRC).filter(function (k) { return kinds[k]; }).map(function (k) { return '<span class="ev-src s-' + k + '">' + ic(SRC[k][0]) + "<b>" + SRC[k][1] + "</b><em>" + kinds[k] + "</em></span>"; }).join("");
    return head("wrench", c.title || "Entretien à venir", "Chaque échéance est calculée à partir de sa source", "") +
      (legend ? '<div class="ev-mleg">' + legend + "</div>" : "") + '<div class="ev-maint">' + rows + "</div>";
  };

  /* ---------- Modes et activité ---------- */
  K.modes = function (c, e) {
    var r = rt(e), active = r.mode || c.current, selK = r.vals.msel || active, M = c.items.filter(function (m) { return m.k === selK; })[0] || c.items[0];
    var grid = '<div class="ev-modes" style="--n:' + c.items.length + '">' + c.items.map(function (m) {
      return '<button type="button" class="ev-mode' + (m.k === selK ? " is-sel" : "") + (m.k === active ? " is-act" : "") + '" data-a="msel" data-v="' + m.k + '" aria-pressed="' + (m.k === selK) + '">' + ic(m.icon) +
        "<span><b>" + esc(m.label) + "</b><small>" + esc(m.sub) + "</small>" + (m.k === active ? '<em>Mode actif</em>' : "") + "</span></button>";
    }).join("") + "</div>";
    var fx = M.fx.map(function (f) {
      return '<div class="ev-row is-lg"><span class="ev-ri t-gold">' + ic(f[0]) + "</span><span><b>" + esc(f[1]) + "</b><small>" + esc(f[2]) + (/crit/.test(f[4] || "") ? ' · <em class="t-warn">confirmation requise</em>' : "") + "</small></span><strong>" + esc(f[3]) + "</strong></div>";
    }).join("");
    var autos = (M.autos || []).map(function (a) {
      return '<div class="ev-row"><span class="ev-ri t-gold">' + ic(a[0]) + "</span><span><b>" + esc(a[1]) + "</b><small>" + esc(a[2]) + "</small></span><em class=\"t-ok\">Prévue</em></div>";
    }).join("");
    var scen = (c.scenarios || []).map(function (s) { return '<div class="ev-scen"><b>' + esc(s[0]) + "</b><span>" + esc(s[1]) + "</span></div>"; }).join("");
    var res = r.vals.mres && r.vals.mres.k === M.k ? '<div class="ev-mres">' + r.vals.mres.html + "</div>" : "";
    return grid + '<div class="ev-mgrid"><section class="ev-card ev-subcard">' + head(M.icon, "Aperçu du mode " + M.label, "Vérifiez les effets avant d’appliquer. Un aperçu n’envoie rien.", "") + fx +
      '<div class="ev-mapply"><button type="button" class="ev-btn is-primary" data-a="mapply" data-v="' + M.k + '"' + (r.vals.mrun ? " disabled" : "") + ">" + ic("play") + (M.k === active ? "Réappliquer" : "Examiner et appliquer") + "</button>" +
      '<span class="ev-fine">' + ic("info") + "Actions critiques : confirmation obligatoire.</span></div>" + res + "</section>" +
      '<section class="ev-card ev-subcard">' + head("gear", "Automatisations prévues", "Elles seront actives avec ce mode.", "") + (autos || '<p class="ev-fine">Aucune automatisation propre à ce mode.</p>') +
      (scen ? '<p class="ev-k">Scénarios d’exemple</p>' + scen : "") + "</section></div>";
  };
  K.autos = function (c, e) {
    var r = rt(e);
    return head("gear", "Automatisations", "Règles approuvées par vous · chacune peut être suspendue", "") + c.rows.map(function (a, i) {
      var on = r.tog["auto" + i] != null ? r.tog["auto" + i] : a[4];
      return '<div class="ev-auto"><span class="ev-ri t-gold">' + ic(a[0]) + "</span><span><b>" + esc(a[1]) + "</b><small>" + esc(a[2]) + "</small></span>" +
        '<span class="ev-trig">' + ic("clock") + "<small>Déclencheur</small><b>" + esc(a[3]) + "</b></span><em class=\"t-" + (on ? "ok" : "muted") + '">' + (on ? "Active" : "En pause") + "</em>" + sw(on, "tog", "auto" + i, a[1]) + "</div>";
    }).join("");
  };
  K.activity = function (c, e) {
    var log = rt(e).log.map(function (l) { return [(NOW() - l.t) / 60000, l.who || "Vous", l.what + (l.sub ? " · " + l.sub : "")]; });
    var rows = log.concat(c.rows);
    return head("clock", "Activité", "Dernières actions liées aux modes, commandes et automatisations", "") + '<ol class="ev-act">' + rows.map(function (a) {
      return "<li><time>" + stamp(a[0]) + "</time><b>" + esc(a[1]) + "</b><span>" + esc(a[2]) + "</span></li>";
    }).join("") + "</ol>";
  };

  /* ======================================================================================
     État d'exécution (en mémoire seulement : rien n'est envoyé nulle part)
     ====================================================================================== */
  var R = {};
  function rt(e) { var k = e.key || e; return R[k] || (R[k] = { checks: {}, vals: {}, pend: {}, tog: {}, eq: {}, prio: null, mode: null, log: [], lights: null, moving: false }); }
  function log(e, what, sub, tone, sec) { rt(e).log.unshift({ t: NOW(), who: "Vous", what: what, sub: sub || "", tone: tone || "ok", sec: !!sec }); }

  /* ======================================================================================
     Vues : sélecteur d'environnements, page d'un environnement, navigation, onglets
     ====================================================================================== */
  var SECS = [["apercu", "Vue d’ensemble", "grid"], ["eclairage", "Éclairage", "bulb"], ["confort", "Confort", "thermo"], ["energie", "Énergie", "bolt"],
    ["eau", "Eau", "drop"], ["securite", "Sécurité", "shield"], ["internet", "Internet", "wifi"], ["equipements", "Équipements", "cube"],
    ["voyage", "Voyage et entretien", "wrench"], ["modes", "Modes et activité", "sparkle"]];
  var SUBS = { apercu: "L’essentiel du lieu en un regard.", eclairage: "Des ambiances adaptées à chaque moment.", confort: "Chaleur, air et météo.",
    energie: "Sources, stockage et consommation.", eau: "Réservoirs, eau chaude et prévention.", securite: "Ouvertures, détection et alertes.",
    internet: "Connexions et réseau.", equipements: "Les équipements en un regard.", voyage: "Agenda, listes et entretien.", modes: "Des routines claires et des effets visibles." };
  function secTitle(e, k) { var s = SECS.filter(function (x) { return x[0] === k; })[0]; return (e.titles && e.titles[k]) || s[1]; }
  function secSub(e, k) { return (e.subs && e.subs[k]) || SUBS[k]; }
  function tabsOf(e, k) {
    var s = e.s[k];
    if (!s) return [];
    if (s.length && !Array.isArray(s[0])) return [["", "", s]];
    return s;
  }
  var S = { view: "home", env: D.order[0], sec: "apercu", tab: {} };

  function banner(e, cls) {
    var b = e.banner || {};
    if (b.img) return '<figure class="ev-ban ' + (cls || "") + '"><img src="' + b.img + '" alt="' + esc(b.alt || e.name) + '" style="object-position:' + (b.pos || "50% 50%") + '" decoding="async"></figure>';
    /* Panneau d'attente premium : verre noir, filet doré, nom et mesures — jamais de dessin. */
    var chips = (e.status || []).slice(0, 3).map(function (s) {
      return '<span class="ev-ph-c">' + ic(s[0], "is-sm") + '<b class="t-' + (s[3] || "gold") + '">' + esc(String(s[2])) + "</b></span>";
    }).join("");
    return '<figure class="ev-ban is-ph ' + (cls || "") + '" role="img" aria-label="' + esc(b.alt || e.name) + '">' +
      '<span class="ev-ph-frame" aria-hidden="true"></span>' +
      '<span class="ev-ph-b"><span class="ev-ph-n">' + esc(e.name) + '</span><span class="ev-ph-chips">' + chips + "</span></span>" +
      "<figcaption>Photo à venir</figcaption></figure>";
  }
  function pickStatus(e) {
    return e.status.map(function (s) {
      var v = s[2], t = s[3];
      if (v === "live") { var b = bat(e); v = nf(b.soc) + NB + "%"; t = b.live ? "ok" : "gold"; }
      if (s[1] === "Lumières" || s[0] === "bulb") { var l = rt(e).lights; if (l) v = l.on + " / " + l.total + " allumées"; }
      return '<span class="ev-ps">' + ic(s[0]) + "<small>" + esc(s[1]) + "</small><b class=\"t-" + t + '">' + esc(v) + "</b></span>";
    }).join("");
  }
  /* ======================================================================================
     Accueil multisite : tous les lieux d'un regard, alertes réunies, comparaison,
     mode appliqué à plusieurs lieux (avec confirmation) et journal consolidé.
     ====================================================================================== */
  function siteOf(e) {
    var site = e.site || {}, al = [], mt = findCard(e, "maint"), op = findCard(e, "openings"), next = null;
    (site.alerts || []).forEach(function (a) { al.push({ tone: a[0], title: a[1], text: a[2], go: a[3], env: e.key }); });
    if (op) opsOf(e, op).forEach(function (o, j) { if (o.tone === "warn") al.push({ tone: "warn", title: op.points[j].label + " · " + o.state.toLowerCase(), text: "Depuis " + dur(o.ago * 60000) + (o.who ? " · " + o.who : ""), go: "securite", env: e.key }); });
    if (mt) mt.rows.forEach(function (m, i) {
      var due = m[5] ? dueOf(m[5]) : m[3];
      if (due < 0 && !((rt(e).vals.mplan || {})[i])) al.push({ tone: "err", title: m[1] + " · en retard de " + (-due) + NB + "j", text: m[5] ? "Source : " + lc1((SRC[m[5].k] || SRC.jarvis)[1]) : m[2], go: "voyage:entretien", env: e.key });
      if (due >= 0 && (!next || due < next.due)) next = { due: due, title: m[1] };
    });
    var b = bat(e), load = e.energy ? (b.live ? Math.abs(b.w || 0) : exampleFlow(e).load) : 0;
    return { site: site, alerts: al, armed: armedOf(e), soc: b.soc, live: b.live, load: load, wx: wxNow(e), next: next, n: site.n || 0 };
  }
  function alertsAll() {
    var all = [];
    D.order.forEach(function (k) { all = all.concat(siteOf(E[k]).alerts); });
    var rank = { err: 0, warn: 1, water: 2, gold: 3 };
    return all.sort(function (a, b) { return (a.tone in rank ? rank[a.tone] : 3) - (b.tone in rank ? rank[b.tone] : 3); });
  }
  function greet() { var h = lp(NOW()).h; return h < 5 ? "Bonne nuit" : h < 12 ? "Bonjour" : h < 18 ? "Bon après-midi" : "Bonsoir"; }
  function whenTxt(d) { return d === 0 ? "aujourd’hui" : d === 1 ? "demain" : "dans " + d + NB + "j"; }

  var H = { cmp: "load", af: "urgent", alAll: false, tl: "all", tlAll: false, mm: "absence", sel: null, res: "", run: false, anim: true };
  function mmLocal(e, k) { var m = e.site && e.site.multi ? e.site.multi[k] : null, mc = findCard(e, "modes"); return m && mc ? mc.items.filter(function (x) { return x.k === m; })[0] || null : null; }
  function mmSel() {
    if (!H.sel) { H.sel = {}; D.order.forEach(function (k) { H.sel[k] = !!mmLocal(E[k], H.mm) && !(E[k].site || {}).n; }); }
    return H.sel;
  }

  var HP = {};
  function nPlaces() { return D.order.filter(function (k) { return fleetOf(E[k])[0] === k; }).length; }
  HP.sum = function () {
    var S2 = D.order.map(function (k) { return siteOf(E[k]); }), al = alertsAll(), urgent = al.filter(function (a) { return a.tone === "err" || a.tone === "warn"; });
    var armed = S2.filter(function (x) { return x.armed; }).length, off = D.order.filter(function (k, i) { return !S2[i].armed; }).map(function (k) { return E[k].name; });
    var ppl = S2.reduce(function (a, x) { return a + x.n; }, 0), occ = S2.filter(function (x) { return x.n > 0; }).length, load = S2.reduce(function (a, x) { return a + x.load; }, 0);
    var nx = null;
    D.order.forEach(function (k, i) { var n = S2[i].next; if (n && (!nx || n.due < nx.due)) nx = { due: n.due, title: n.title, env: E[k] }; });
    var t = [
      ["grid", "Lieux", nPlaces() + " / " + nPlaces(), "en ligne · " + D.order.length + " tableaux · synchronisés il y a 12 s", "ok", ""],
      ["bell", "Alertes", String(urgent.length), urgent.length ? al.filter(function (a) { return a.tone === "err"; }).length + " en retard · " + al.filter(function (a) { return a.tone === "warn"; }).length + " à vérifier" : "Rien à signaler", urgent.length ? "warn" : "ok", "alerts"],
      ["shield", "Sécurité", armed + " / " + D.order.length + " armés", off.length ? "Désarmés : " + off.join(", ") : "Tous les lieux sont armés", armed === D.order.length ? "ok" : "gold", ""],
      ["users", "Présence", ppl + " personne" + (ppl > 1 ? "s" : ""), occ + " lieu" + (occ > 1 ? "x" : "") + " occupé" + (occ > 1 ? "s" : "") + " · " + (D.order.length - occ) + " vides", "gold", ""],
      ["bolt", "Énergie", fmtW(load), "Puissance appelée, tous les lieux", "gold", "cmp"],
      ["wrench", "Prochain entretien", nx ? cap(whenTxt(nx.due)) : "—", nx ? nx.title + " · " + nx.env.name : "", "water", ""]
    ];
    return t.map(function (x, i) {
      var inner = '<span class="ev-hs-i t-' + x[4] + '">' + ic(x[0]) + '</span><span class="ev-hs-b"><small>' + x[1] + "</small><b>" + esc(x[2]) + "</b><em>" + esc(x[3]) + "</em></span>";
      return x[5] ? '<button type="button" class="ev-hs" data-a="hjump" data-v="' + x[5] + '" style="--i:' + i + '">' + inner + "</button>" : '<div class="ev-hs" style="--i:' + i + '">' + inner + "</div>";
    }).join("");
  };
  HP.board = function () {
    var rows = D.order.map(function (k) {
      var e = E[k], x = siteOf(e), urgent = x.alerts.filter(function (a) { return a.tone === "err" || a.tone === "warn"; }).length;
      var col = batColor(x.soc);
      return '<button type="button" class="ev-brow" data-a="env" data-v="' + k + '">' +
        '<span class="ev-b-site"><span class="ev-b-ic">' + ic(e.icon || "home") + '</span><span><b>' + esc(e.name) + "</b><small>" + esc(e.place) + "</small></span></span>" +
        '<span class="ev-b-c" data-l="Sécurité"><span class="ev-b-arm' + (x.armed ? " is-on" : "") + '">' + ic(x.armed ? "shield" : "unlock") + (x.armed ? "Armé" : "Désarmé") + "</span></span>" +
        '<span class="ev-b-c" data-l="Intérieur"><b>' + (x.site.inside != null ? deg(x.site.inside, x.site.inside % 1 ? 1 : 0) : "—") + "</b></span>" +
        '<span class="ev-b-c is-wx" data-l="Extérieur">' + wxi(x.wx.code, x.wx.night) + "<b>" + deg(x.wx.t) + "</b></span>" +
        '<span class="ev-b-c is-en" data-l="Énergie"' + (k === "boulance" ? ' data-live-cell="boulance"' : "") + ">" + enCell(x, col) + "</span>" +
        '<span class="ev-b-c" data-l="Présence"><small class="ev-b-who">' + ic(x.n ? "users2" : "home", "is-sm") + esc(x.site.who || "—") + "</small></span>" +
        '<span class="ev-b-c" data-l="Entretien"><small>' + (x.next ? esc(x.next.title) + "<em>" + cap(whenTxt(x.next.due)) + "</em>" : "—") + "</small></span>" +
        '<span class="ev-b-c" data-l="Alertes">' + (urgent ? '<span class="ev-b-al t-' + (x.alerts.some(function (a) { return a.tone === "err"; }) ? "err" : "warn") + '">' + urgent + "</span>" : '<span class="ev-b-al t-ok">' + ic("check") + "</span>") + "</span>" +
        ic("right", "ev-chev") + "</button>";
    }).join("");
    return head("grid", "Tous vos lieux, en direct", "Sécurité, températures, énergie, présence et entretien · cliquez pour ouvrir un tableau", '<span class="ev-tag is-live">en direct</span>') +
      '<div class="ev-board" role="list"><div class="ev-brow is-h" aria-hidden="true"><span>Lieu</span><span>Sécurité</span><span>Intérieur</span><span>Extérieur</span><span>Énergie</span><span>Présence</span><span>Prochain entretien</span><span>Alertes</span><span></span></div>' + rows + "</div>";
  };
  function enCell(x, col) {
    return '<span class="ev-b-en"><span class="ev-bar is-xs"><i style="width:' + clamp(x.soc, 2, 100).toFixed(0) + "%;background:" + col + '"></i></span><b>' + nf(x.soc) + NB + "%</b></span><small>" + (x.live ? "réel · " : "") + fmtW(x.load) + "</small>";
  }
  HP.alerts = function () {
    var al = alertsAll(), list = H.af === "urgent" ? al.filter(function (a) { return a.tone === "err" || a.tone === "warn"; }) : al;
    var seg = '<div class="ev-seg is-sm" role="group" aria-label="Filtrer les alertes">' + [["all", "Toutes · " + al.length], ["urgent", "À traiter"]].map(function (f) {
      return '<button type="button" class="' + (H.af === f[0] ? "is-on" : "") + '" aria-pressed="' + (H.af === f[0]) + '" data-a="haf" data-v="' + f[0] + '">' + f[1] + "</button>";
    }).join("") + "</div>";
    var ICO = { err: "warn", warn: "bell", water: "snowflake", gold: "info" };
    return head("bell", "Alertes de tous les lieux", "Retards d’entretien, ouvertures et avis, triés par urgence", seg) +
      '<ul class="ev-hal">' + (H.alAll ? list : list.slice(0, 6)).map(function (a) {
        var e = E[a.env];
        return '<li><button type="button" class="ev-hali t-' + a.tone + '" data-a="hgo" data-v="' + a.env + "|" + esc(a.go) + '"><span class="ev-ri t-' + a.tone + '">' + ic(ICO[a.tone] || "info") + "</span>" +
          '<span class="ev-hali-b"><b>' + esc(a.title) + "</b><small>" + esc(a.text) + '</small></span><span class="ev-sitec">' + ic(e.icon || "home", "is-sm") + esc(e.name) + "</span>" + ic("right", "ev-chev") + "</button></li>";
      }).join("") + "</ul>" + (list.length ? "" : '<p class="ev-fine">' + ic("check") + "Aucune alerte à traiter.</p>") +
      (list.length > 6 ? '<button type="button" class="ev-link ev-more" data-a="halall">' + (H.alAll ? "Afficher moins" : "Afficher les " + list.length + " alertes") + ic(H.alAll ? "up" : "down") + "</button>" : "");
  };
  HP.multi = function () {
    var sel = mmSel(), M0 = D.multi.filter(function (m) { return m.k === H.mm; })[0], n = 0;
    var modes = '<div class="ev-mm">' + D.multi.map(function (m) {
      return '<button type="button" class="ev-mm-b' + (m.k === H.mm ? " is-on" : "") + '" aria-pressed="' + (m.k === H.mm) + '" data-a="hmm" data-v="' + m.k + '">' + ic(m.icon) + "<span><b>" + esc(m.label) + "</b><small>" + esc(m.sub) + "</small></span></button>";
    }).join("") + "</div>";
    var sites = D.order.map(function (k) {
      var e = E[k], L = mmLocal(e, H.mm), on = !!(L && sel[k]);
      if (on) n++;
      if (!L) return '<li class="is-na"><span class="ev-box"></span>' + ic(e.icon || "home") + "<span><b>" + esc(e.name) + "</b><small>Aucun mode équivalent · non modifié</small></span></li>";
      var crit = L.fx.filter(function (f) { return /crit/.test(f[4] || ""); }).length, act = (rt(e).mode || findCard(e, "modes").current) === L.k;
      return '<li><button type="button" class="ev-mm-s' + (on ? " is-on" : "") + '" aria-pressed="' + on + '" data-a="hmms" data-v="' + k + '"><span class="ev-box">' + ic("check") + "</span>" + ic(e.icon || "home") +
        "<span><b>" + esc(e.name) + "</b><small>Mode " + esc(L.label) + " · " + L.fx.length + " effets" + (crit ? " dont " + crit + " critique" + (crit > 1 ? "s" : "") : "") + "</small></span>" +
        (act ? '<em class="ev-flag t-ok">Déjà actif</em>' : (e.site || {}).n ? '<em class="ev-flag t-gold">Occupé</em>' : "") + "</button></li>";
    }).join("");
    return head("sparkle", "Un mode sur plusieurs lieux", "Chaque lieu reçoit son propre mode · tout est confirmé avant l’envoi", "") + modes +
      '<ul class="ev-mm-l">' + sites + "</ul>" +
      '<div class="ev-mapply"><button type="button" class="ev-btn is-primary" data-a="hmmapply"' + (n && !H.run ? "" : " disabled") + ">" + ic("play") + "Examiner et appliquer · " + n + " lieu" + (n > 1 ? "x" : "") + "</button>" +
      '<span class="ev-fine">' + ic("info") + "Vous confirmez la liste des lieux et leurs effets critiques.</span></div>" + (H.res ? '<div class="ev-mres">' + H.res + "</div>" : "");
  };
  function timeline() {
    var out = [];
    D.order.forEach(function (k) {
      var e = E[k], ac = findCard(e, "activity"), ev = findCard(e, "events");
      rt(e).log.forEach(function (l) { out.push({ m: (NOW() - l.t) / 60000, env: k, who: l.who || "Vous", text: l.what, sub: l.sub, tone: l.tone, cat: l.sec ? "securite" : /^Mode /.test(l.what) ? "modes" : "commandes" }); });
      if (ev) ev.items.forEach(function (x) { out.push({ m: x[0], env: k, who: "", text: x[1], sub: x[2], tone: x[3] || "ok", cat: "securite" }); });
      if (ac) ac.rows.forEach(function (x) { out.push({ m: x[0], env: k, who: x[1], text: x[2], sub: "", tone: "gold", cat: /^Mode |mode /i.test(x[2]) ? "modes" : "commandes" }); });
    });
    out.sort(function (a, b) { return a.m - b.m; });
    var seen = {};
    return out.filter(function (x) { var k = x.env + "|" + x.text.toLowerCase() + "|" + Math.round(x.m / 15); if (seen[k]) return false; seen[k] = 1; return true; });
  }
  function stampS(m) { var t = NOW() - m * 60000, d = dayDiff(t); return d === 0 ? hm(t) : (d === -1 ? "Hier " : cap(dateShort(t)) + " ") + hm(t); }
  HP.tl = function () {
    var all = timeline(), list = H.tl === "all" ? all : all.filter(function (x) { return x.cat === H.tl; }), shown = H.tlAll ? list : list.slice(0, 7);
    var seg = '<div class="ev-seg is-sm" role="group" aria-label="Filtrer le journal">' + [["all", "Tout"], ["securite", "Sécurité"], ["modes", "Modes"], ["commandes", "Commandes"]].map(function (f) {
      return '<button type="button" class="' + (H.tl === f[0] ? "is-on" : "") + '" aria-pressed="' + (H.tl === f[0]) + '" data-a="htl" data-v="' + f[0] + '">' + f[1] + "</button>";
    }).join("") + "</div>";
    return head("clock", "Journal de tous les lieux", "Une seule chronologie : sécurité, modes et commandes", "") + seg +
      '<ol class="ev-htl">' + shown.map(function (x) {
        var e = E[x.env];
        return '<li class="t-' + x.tone + '"><time>' + stampS(x.m) + '</time><span class="ev-sitec">' + ic(e.icon || "home", "is-sm") + esc(e.name) + "</span><span><b>" + esc(x.text) + "</b>" +
          ((x.who || x.sub) ? "<small>" + esc([x.who, x.sub].filter(Boolean).join(" · ")) + "</small>" : "") + "</span></li>";
      }).join("") + "</ol>" +
      (list.length > 7 ? '<button type="button" class="ev-link" data-a="htlall">' + (H.tlAll ? "Afficher moins" : "Afficher tout · " + list.length + " événements") + ic(H.tlAll ? "up" : "down") + "</button>" : "");
  };
  var CMP = [["load", "Énergie", "Puissance appelée maintenant"], ["soc", "Batteries", "Charge des batteries"], ["in", "Intérieur", "Température intérieure"], ["out", "Extérieur", "Température extérieure"], ["al", "Alertes", "Alertes à traiter"]];
  HP.cmp = function () {
    var m = CMP.filter(function (x) { return x[0] === H.cmp; })[0];
    var vals = D.order.map(function (k) {
      var x = siteOf(E[k]), v = m[0] === "load" ? x.load : m[0] === "soc" ? x.soc : m[0] === "in" ? x.site.inside : m[0] === "out" ? x.wx.t : x.alerts.filter(function (a) { return a.tone === "err" || a.tone === "warn"; }).length;
      return { k: k, v: v, x: x };
    }).sort(function (a, b) { return b.v - a.v; });
    var lo = Math.min(0, Math.min.apply(null, vals.map(function (v) { return v.v; }))), hi = Math.max.apply(null, vals.map(function (v) { return v.v; })), rg = Math.max(1e-6, hi - lo);
    function fv(v) { return m[0] === "load" ? fmtW(v) : m[0] === "soc" ? nf(v) + NB + "%" : m[0] === "al" ? String(v) : deg(v, v % 1 ? 1 : 0); }
    function colr(o) { return m[0] === "soc" ? batColor(o.v) : m[0] === "in" || m[0] === "out" ? tcol(o.v) : m[0] === "al" ? (o.v ? "var(--e-warn)" : "var(--e-ok)") : "var(--mode-action)"; }
    var seg = '<div class="ev-seg is-sm" role="group" aria-label="Comparer selon">' + CMP.map(function (c) {
      return '<button type="button" class="' + (H.cmp === c[0] ? "is-on" : "") + '" aria-pressed="' + (H.cmp === c[0]) + '" data-a="hcmp" data-v="' + c[0] + '">' + c[1] + "</button>";
    }).join("") + "</div>";
    return head("chart", "Comparer vos lieux", esc(m[2]) + " · du plus élevé au plus bas", "") + seg + '<div class="ev-cmp">' + vals.map(function (o, i) {
      var e = E[o.k], z = (0 - lo) / rg * 100, a = (Math.min(0, o.v) - lo) / rg * 100, w = Math.abs(o.v) / rg * 100;
      return '<button type="button" class="ev-cmpr' + (i === 0 ? " is-top" : "") + '" data-a="env" data-v="' + o.k + '" style="--i:' + i + '">' + ic(e.icon || "home") + "<span>" + esc(e.name) + "</span>" +
        '<span class="ev-cmpb">' + (lo < 0 ? '<i class="ev-cmpz" style="left:' + z.toFixed(1) + '%"></i>' : "") + '<i style="left:' + a.toFixed(1) + "%;width:" + Math.max(1.5, w).toFixed(1) + "%;background:" + colr(o) + '"></i></span><b>' + fv(o.v) + "</b></button>";
    }).join("") + "</div>";
  };
  function homeCards() {
    return D.order.map(function (k) {
      var e = E[k], x = siteOf(e), urgent = x.alerts.filter(function (a) { return a.tone === "err" || a.tone === "warn"; }).length;
      return '<button type="button" class="ev-pick' + (k === S.env ? " is-cur" : "") + '" data-a="env" data-v="' + k + '">' + banner(e, "is-pick") +
        (urgent ? '<span class="ev-pick-al">' + ic("bell", "is-sm") + urgent + " alerte" + (urgent > 1 ? "s" : "") + "</span>" : "") +
        '<span class="ev-pick-b"><span class="ev-pick-k">' + ic(e.icon || "home") + esc(e.kind) + "</span><b>" + esc(e.name) + "</b><small>" + ic("pin", "is-sm") + esc(e.place) + "</small>" +
        '<span class="ev-pick-s"' + (k === "boulance" ? ' data-live-pick="boulance"' : "") + ">" + pickStatus(e) + "</span>" +
        '<span class="ev-pick-f"><span class="ev-b-arm' + (x.armed ? " is-on" : "") + '">' + ic(x.armed ? "shield" : "unlock") + (x.armed ? "Armé" : "Désarmé") + "</span>" +
        '<span class="ev-pick-go">Ouvrir le tableau' + ic("right") + "</span></span></span></button>";
    }).join("") + '<button type="button" class="ev-pick is-add" data-a="admin">' + ic("plus") + "<b>Ajouter un environnement</b><small>" + ic("lock", "is-sm") + "Réservé à l’administrateur</small></button>";
  }
  function home() {
    var now = NOW(), anim = H.anim;
    H.anim = false;
    function part(name, cls) { return '<section class="ev-card ' + cls + (anim ? " is-new" : "") + '" data-h="' + name + '">' + HP[name]() + "</section>"; }
    return '<div class="ev-home"><div class="ev-bar0"><div><p class="ev-env">JARVIS · Environnements intelligents</p><h4 class="ev-h">Vos environnements</h4>' +
      '<p class="ev-sub">' + greet() + ", James. " + cap(dateLong(now)) + " · " + hm(now) + ". Tous vos lieux sur un seul écran.</p></div>" +
      '<span class="ev-badge">' + ic("info") + "Données d’exemple · batteries de BouLance réelles</span>" +
      '<p class="ev-pop" data-ev-pop role="status" hidden>' + ic("lock") + "Réservé à l’administrateur de votre système.</p></div>" +
      '<div class="ev-hsum' + (anim ? " is-new" : "") + '" data-h="sum">' + HP.sum() + "</div>" +
      '<div class="ev-grid ev-hgrid">' + part("board", "w12 ev-t-board") + part("alerts", "w7 ev-t-halerts") + part("multi", "w5 ev-t-multi") +
      part("cmp", "w5 ev-t-cmp") + part("tl", "w7 ev-t-tl") + "</div>" +
      '<div class="ev-hsec"><h5>Ouvrir un tableau</h5><p>Le même modèle pour chaque lieu · seules les données changent.</p></div>' +
      '<div class="ev-picks">' + homeCards() + "</div></div>";
  }
  function homeRefresh(names) {
    (names || ["sum", "board", "alerts", "multi", "cmp", "tl"]).forEach(function (n) { var el = app.querySelector('[data-h="' + n + '"]'); if (el) el.innerHTML = HP[n](); });
  }
  /* Bande des lieux, dans chaque tableau : passer d'un lieu à l'autre sans revenir à l'accueil */
  function siteStrip() {
    return '<nav class="ev-sites" aria-label="Changer de lieu">' + D.order.map(function (k) {
      var e = E[k], fl = fleetOf(e);
      if (fl[0] !== k) return "";  /* un hangar à plusieurs appareils compte pour un seul lieu */
      var here = fl.indexOf(S.env) >= 0, urgent = [];
      fl.forEach(function (f) { urgent = urgent.concat(urgentOf(f)); });
      return '<button type="button" class="ev-site' + (here ? " is-on" : "") + '" data-a="env" data-v="' + (here ? S.env : k) + '"' + (here ? ' aria-current="page"' : "") + ">" + ic(e.hangar ? "hangar" : e.icon || "home") + "<span>" + esc(e.hangar ? "Hangar" : e.name) + "</span>" +
        (urgent.length ? '<i class="ev-site-d t-' + (urgent.some(function (a) { return a.tone === "err"; }) ? "err" : "warn") + '" title="' + urgent.length + ' alerte(s)"></i>' : "") + "</button>";
    }).join("") + "</nav>";
  }
  /* Choix de l'appareil dans un hangar à plusieurs appareils : on garde la section ouverte */
  function fleetBar(e) {
    if (!e.hangar) return "";
    var ks = fleetOf(e);
    return '<nav class="ev-fleet" aria-label="Appareils du hangar"><span class="ev-fleet-h">' + ic("hangar") + "<span><b>" + esc(e.hangar.name) + "</b><small>" + ks.length + " appareils · choisissez un tableau</small></span></span>" +
      '<span class="ev-fleet-l">' + ks.map(function (k) {
        var p = E[k], P0 = p.plane || {}, on = k === S.env, u = urgentOf(k).length, st = P0.state || ["", "ok"];
        return '<button type="button" class="ev-fleet-b' + (on ? " is-on" : "") + '" data-a="plane" data-v="' + k + '" aria-pressed="' + on + '">' +
          '<span class="ev-fleet-ph">' + (P0.photo ? '<img src="' + P0.photo + '" alt="" loading="lazy" decoding="async" style="object-position:' + (P0.pos || "50% 50%") + '">' : ic(p.icon)) + "</span>" +
          "<span class=\"ev-fleet-t\"><b>" + esc(p.name) + "</b><small class=\"t-" + st[1] + '">' + dot(st[1]) + esc(st[0]) + "</small></span>" +
          (u ? '<i class="ev-site-d t-warn" title="' + u + ' alerte(s)"></i>' : "") + "</button>";
      }).join("") + "</span></nav>";
  }
  function heroChips(e) {
    var x = siteOf(e), urgent = x.alerts.filter(function (a) { return a.tone === "err" || a.tone === "warn"; }).length;
    return '<p class="ev-hero-s"><span>' + wxi(x.wx.code, x.wx.night) + "<b>" + deg(x.wx.t) + "</b>" + esc(x.wx.cond) + "</span>" +
      '<span class="' + (x.armed ? "t-ok" : "t-gold") + '">' + ic(x.armed ? "shield" : "unlock", "is-sm") + (x.armed ? "Armé" : "Désarmé") + "</span>" +
      "<span>" + ic(x.n ? "users2" : "home", "is-sm") + esc((x.site.who || "").split(" · ")[0]) + "</span>" +
      (urgent ? '<span class="t-warn">' + ic("bell", "is-sm") + urgent + " alerte" + (urgent > 1 ? "s" : "") + "</span>" : '<span class="t-ok">' + ic("check", "is-sm") + "Aucune alerte</span>") + "</p>";
  }
  function envView() {
    var e = cur();
    var nav = SECS.map(function (s) {
      if (!e.s[s[0]] && s[0] !== "eclairage") return "";
      return '<button type="button" class="ev-nav-i' + (s[0] === S.sec ? " is-on" : "") + '" data-a="sec" data-v="' + s[0] + '"' + (s[0] === S.sec ? ' aria-current="page"' : "") + ">" + ic(s[0] === "voyage" && e.voyageIcon ? e.voyageIcon : s[2]) +
        "<span>" + esc(secTitle(e, s[0])) + "</span>" + (s[0] === "eclairage" ? '<em class="ev-lcount" data-lcount></em>' : "") + "</button>";
    }).join("");
    return '<div class="ev-bar0"><button type="button" class="ev-back" data-a="pick">' + ic("back") + "<span>Tous les lieux</span></button>" +
      '<span class="ev-badge">' + ic("info") + "Données d’exemple" + (e.energy && e.energy.live ? " · batteries réelles" : "") + "</span>" +
      '<span class="ev-adms"><button type="button" class="ev-adm is-cfg" data-a="admin" aria-label="Configurer · réservé à l’administrateur">' + ic("edit") + "<span>Configurer</span>" + ic("lock", "ev-lk") + "</button>" +
      '<button type="button" class="ev-adm" data-a="admin" aria-label="Accès et publication · réservé à l’administrateur">' + ic("shield") + "<span>Accès et publication</span>" + ic("lock", "ev-lk") + "</button></span>" +
      '<p class="ev-pop" data-ev-pop role="status" hidden>' + ic("lock") + "Réservé à l’administrateur de votre système.</p></div>" + siteStrip() + fleetBar(e) +
      '<header class="ev-hero"><div class="ev-hero-t"><p class="ev-env">' + esc(e.name) + '</p><h4 class="ev-h" data-ev-h>' + esc(secTitle(e, S.sec)) + "</h4>" +
      '<p class="ev-sub" data-ev-sub>' + esc(secSub(e, S.sec)) + '</p><p class="ev-meta">' + ic(e.icon || "home", "is-sm") + esc(e.kind) + " · " + esc(e.place) + "</p>" + heroChips(e) + "</div>" + banner(e) + "</header>" +
      '<div class="ev-main"><nav class="ev-nav" aria-label="Sections de ' + esc(e.name) + '"><p class="ev-nav-h">' + esc(e.name) + '</p><div class="ev-nav-l">' + nav + "</div></nav>" +
      '<div class="ev-sec" data-ev-sec></div></div>' +
      '<p class="ev-foot">JARVIS / ' + esc(e.name.toUpperCase()) + " / DONNÉES D’EXEMPLE" + (e.energy && e.energy.live ? " · BATTERIES RÉELLES" : "") + "</p>";
  }
  function renderSection(anim) {
    var e = cur(), host = app.querySelector("[data-ev-sec]");
    if (!host) return;
    teardownSection();
    var h = app.querySelector("[data-ev-h]"), sub = app.querySelector("[data-ev-sub]");
    if (h) h.textContent = secTitle(e, S.sec);
    if (sub) sub.textContent = secSub(e, S.sec);
    app.querySelectorAll(".ev-nav-i").forEach(function (b) {
      var on = b.getAttribute("data-v") === S.sec;
      b.classList.toggle("is-on", on);
      if (on) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
    if (S.sec === "eclairage") {
      host.innerHTML = '<div class="ev-lum" data-lum-full></div>';
      mountLights(host.firstChild, e, false);
    } else {
      var tabs = tabsOf(e, S.sec), tk = S.tab[e.key + S.sec] || tabs[0][0], T = tabs.filter(function (t) { return t[0] === tk; })[0] || tabs[0];
      var bar2 = tabs.length > 1 ? '<div class="ev-tabs" role="tablist" aria-label="' + esc(secTitle(e, S.sec)) + '">' + tabs.map(function (t) {
        return '<button type="button" role="tab" class="ev-tab' + (t[0] === T[0] ? " is-on" : "") + '" aria-selected="' + (t[0] === T[0]) + '" data-a="tab" data-v="' + t[0] + '">' + esc(t[1]) + "</button>";
      }).join("") + "</div>" : "";
      CUR = T[2];
      host.innerHTML = bar2 + '<div class="ev-grid" role="' + (tabs.length > 1 ? "tabpanel" : "region") + '">' + layout(CUR).map(function (x) { return cardHTML(CUR[x.i], e, x.i, anim, x.w); }).join("") + "</div>";
      CUR.forEach(function (c, i) { if (HOOK[c.type]) HOOK[c.type](host.querySelector('[data-c="' + i + '"]'), c, e, i); });
      if (anim) countUp(host);
    }
    liveLoop();
    startTimers();
  }
  /* Mise en page d'un onglet : chaque rangée se remplit sans vide. Une note partage rarement bien une rangée :
     elle passe sous ses voisines, qui se partagent la largeur. Des cartes « prochain événement » placées à côté
     d'une grande carte (entretien) passent au-dessus d'elle, côte à côte. Les données ne changent pas. */
  function layout(cards) {
    var items = cards.map(function (c, i) { return { i: i, w: c.w || 12, t: c.type }; }), out = [], k = 0;
    while (k < items.length) {
      var lead = items[k], side = [];
      for (var j = k + 1; j < items.length && items[j].t === "next" && items[j].w === 12 - lead.w; j++) side.push(items[j]);
      if (lead.w < 12 && lead.t !== "next" && side.length >= 2 && 12 % side.length === 0) {
        side.forEach(function (x) { out.push({ i: x.i, w: 12 / side.length }); });
        out.push({ i: lead.i, w: 12 });
        k = j; continue;
      }
      var row = [], sum = 0;
      while (k < items.length && sum + items[k].w <= 12) { row.push(items[k]); sum += items[k].w; k++; }
      if (!row.length) { row.push(items[k]); k++; }
      var notes = row.filter(function (x) { return x.t === "note"; }), rest = row.filter(function (x) { return x.t !== "note"; });
      if (notes.length && rest.length && sum === 12) {
        var W = rest.reduce(function (a, x) { return a + x.w; }, 0), acc = 0;
        rest.forEach(function (x, n) { var w = n === rest.length - 1 ? 12 - acc : Math.round(x.w * 12 / W); acc += w; out.push({ i: x.i, w: w }); });
        notes.forEach(function (x) { out.push({ i: x.i, w: 12 }); });
      } else row.forEach(function (x) { out.push({ i: x.i, w: x.w }); });
    }
    return out;
  }
  function cardHTML(c, e, i, anim, w) {
    var liveCard = e.energy && e.energy.live && (c.live || c.type === "flow" || c.type === "ring" || c.type === "packs" || c.type === "history" || c.type === "chips" || (c.type === "list" && c.rows && c.rows.some(function (r) { return String(r[2]).indexOf("live:") === 0; })));
    return '<section class="ev-card ev-t-' + c.type + " w" + (w || c.w || 12) + (c.h ? " h" + c.h : "") + (anim ? " is-new" : "") + '" data-c="' + i + '"' + (liveCard ? " data-live" : "") + ' style="--i:' + i + '">' + K[c.type](c, e, i) + "</section>";
  }
  function rerender(i) {
    var el = app.querySelector('[data-c="' + i + '"]');
    if (!el) return;
    el.innerHTML = K[CUR[i].type](CUR[i], cur(), i);
    el.classList.remove("is-new");
    if (HOOK[CUR[i].type]) HOOK[CUR[i].type](el, CUR[i], cur(), i);
  }
  function render() {
    teardownSection();
    if (S.view === "home") { app.innerHTML = home(); liveLoop(); stopTimers(); return; }
    app.innerHTML = envView();
    renderSection(true);
    lightCount();
  }
  function goSec(v, scroll) {
    var parts = String(v).split(":");
    if (parts[0] === S.sec && !parts[1]) return;
    S.sec = parts[0];
    if (parts[1]) S.tab[S.env + S.sec] = parts[1];
    renderSection(true);
    if (scroll !== false) intoView();
  }
  function intoView() {
    var top = app.querySelector(".ev-hero") || app;
    var r = top.getBoundingClientRect();
    if (r.top < 60 || r.top > innerHeight * 0.5) scrollTo({ top: scrollY + r.top - 84, behavior: reduce() ? "auto" : "smooth" });
  }

  /* ---------- Après affichage : éclairage, horloges ---------- */
  var HOOK = {};
  /* Conduits : du nœud vers le centre (ou l'inverse), courbes douces, particules selon la puissance */
  var FLOWC = { prod: "var(--e-acc)", grid: "#e9edf3", load: "#f6efe2", bat: "#34d399" };
  HOOK.flow = function (el) {
    var box = el && el.querySelector("[data-flow]"), svg = box && box.querySelector("[data-flow-svg]"), core = box && box.querySelector("[data-fn-core]");
    if (!svg || !core) return;
    function draw() {
      if (!svg.isConnected) { if (box.__ro) box.__ro.disconnect(); return; }
      var B = box.getBoundingClientRect(), C = core.getBoundingClientRect(), cx = C.left - B.left + C.width / 2, cy = C.top - B.top + C.height / 2, cr = C.width / 2;
      if (!B.width) return;
      var out = "";
      box.querySelectorAll("[data-fn]").forEach(function (n) {
        var d = n.querySelector(".ev-fn-ic").getBoundingClientRect(), x = d.left - B.left + d.width / 2, y = d.top - B.top + d.height / 2, r = d.width / 2;
        var pos = n.getAttribute("data-fn"), dir = n.getAttribute("data-dir"), tone = n.getAttribute("data-tone"), pw = +n.getAttribute("data-pw") || 0, p;
        if (pos === "top") p = [x, y + r + 4, x, (y + cy) / 2, cx + (x - cx) * 0.18, (y + cy) / 2, cx + (x - cx) * 0.12, cy - cr - 2];
        else if (pos === "bottom") p = [x, y - r - 4, x, (y + cy) / 2, cx, (y + cy) / 2, cx, cy + cr + 2];
        else { var sx = pos === "left" ? 1 : -1; p = [x + sx * (r + 4), y, (x + cx) / 2, y, (x + cx) / 2, cy, cx - sx * (cr + 2), cy]; }
        if (dir === "out") p = [p[6], p[7], p[4], p[5], p[2], p[3], p[0], p[1]];
        var dd = "M" + p[0].toFixed(1) + " " + p[1].toFixed(1) + " C" + p.slice(2).map(function (v) { return v.toFixed(1); }).join(" ");
        var col = tone === "grid" && dir === "out" ? FLOWC.prod : FLOWC[tone] || FLOWC.prod, on = dir !== "none";
        out += '<path class="ev-fc" d="' + dd + '"/>';
        if (on) {
          var wdt = (2.5 + 7 * Math.sqrt(pw)).toFixed(1), sp = clamp(2.8 - pw * 1.8, 0.9, 2.8).toFixed(2);
          out += '<path class="ev-fg" d="' + dd + '" style="stroke:' + col + ";stroke-width:" + wdt + '"/><path class="ev-fl" d="' + dd + '" style="stroke:' + col + '"/>' +
            '<path class="ev-fp" d="' + dd + '" style="stroke:' + col + ";--sp:" + sp + 's"/>';
        }
      });
      svg.setAttribute("viewBox", "0 0 " + B.width.toFixed(0) + " " + B.height.toFixed(0));
      svg.innerHTML = out;
    }
    draw();
    if ("ResizeObserver" in window) { if (box.__ro) box.__ro.disconnect(); box.__ro = new ResizeObserver(function () { requestAnimationFrame(draw); }); box.__ro.observe(box); }
  };
  HOOK.lumieres = function (el, c, e) { var box = el && el.querySelector("[data-lum-mini]"); if (box) mountLights(box, e, true); };
  var mounted = [];
  function lumApi(e) {
    return {
      toast: function (t) { toast(t); },
      go: function (k) { if (S.env === e.key) goSec(k); }
    };
  }
  function mountLights(el, e, mini) {
    var L = window.JarvisLumieres;
    if (!L || typeof L.mount !== "function") {
      el.innerHTML = '<div class="ev-lumph">' + ic("bulb") + "<b>Module d’éclairage en cours de branchement</b><small>Les zones et les ambiances de " + esc(e.name) + " apparaîtront ici.</small></div>";
      if (!lumWait) { lumWait = true; addEventListener("load", function () { if (window.JarvisLumieres) renderSection(false); }, { once: true }); }
      return;
    }
    try {
      if (mini) { if (typeof L.mini === "function") L.mini(el, e.key, lumApi(e)); }
      else L.mount(el, e.key, lumApi(e));
      mounted.push(el);
    } catch (err) {
      el.innerHTML = '<div class="ev-lumph">' + ic("warn") + "<b>Le module d’éclairage ne répond pas.</b><small>Aucune commande n’a été envoyée.</small></div>";
    }
  }
  var lumWait = false;
  function teardownSection() {
    var L = window.JarvisLumieres;
    mounted.forEach(function (el) { try { if (L && typeof L.unmount === "function") L.unmount(el); } catch (err) {} });
    mounted = [];
  }
  document.addEventListener("lum:change", function (ev) {
    var d = ev.detail || {};
    if (!d.env || !E[d.env]) return;
    rt(E[d.env]).lights = { on: d.on, total: d.total };
    lightCount();
  });
  function lightCount() {
    var l = rt(cur()).lights, el = app.querySelector("[data-lcount]");
    if (el) el.textContent = l ? l.on + "/" + l.total : "";
    var c2 = app.querySelector(".ev-t-lumieres .ev-cr");
    if (c2 && l) {
      var cnt = c2.querySelector(".ev-count");
      var html = '<b>' + l.on + "</b> / " + l.total + " allumées";
      if (cnt) cnt.innerHTML = html; else c2.insertAdjacentHTML("afterbegin", '<span class="ev-count">' + html + "</span>");
    }
  }

  /* Débits et processeur qui évoluent (seulement visibles, jamais en mouvement réduit) */
  var tick = null;
  function startTimers() {
    stopTimers();
    if (reduce()) return;
    if (!app.querySelector('[data-net="plot"],[data-sys="plot"]')) return;
    tick = setInterval(function () {
      if (!visible || document.hidden) return;
      var e = cur();
      CUR.forEach(function (c, i) {
        var el = app.querySelector('[data-c="' + i + '"]');
        if (!el) return;
        if (c.type === "link") {
          var s = netSeries(e, c), R2 = s.R;
          s.dn.shift(); s.up.shift();
          var last = s.dn[s.dn.length - 1];
          s.dn.push(clamp(last + (R2() - 0.5) * c.down * 0.5 + (c.down - last) * 0.25, c.down * 0.25, c.down * 1.9));
          s.up.push(c.up * (0.6 + R2() * 0.8));
          el.querySelector('[data-net="plot"]').innerHTML = netPlot(s);
          var dn = s.dn[29], up = s.up[29];
          el.querySelector('[data-net="dn"]').textContent = nf(dn, dn < 10 ? 1 : 0);
          el.querySelector('[data-net="up"]').textContent = nf(up, up < 10 ? 1 : 0);
        }
        if (c.type === "sys") {
          var k = e.key + c.icon, v = SYS[k].v;
          v.shift(); v.push(clamp(v[v.length - 1] + (SYS[k].R() - 0.5) * 14 + (c.value - v[v.length - 1]) * 0.3, 3, 96));
          el.querySelector('[data-sys="plot"]').innerHTML = sysPlot(c, v);
          el.querySelector('[data-sys="v"]').textContent = nf(v[29]);
        }
      });
    }, 2000);
  }
  function stopTimers() { clearInterval(tick); tick = null; }

  /* ======================================================================================
     Fenêtre de confirmation, messages, administrateur
     ====================================================================================== */
  var dlgResolve = null;
  function ask(o) {
    return new Promise(function (res) {
      if (!dlg || typeof dlg.showModal !== "function") { res(window.confirm(o.title + "\n" + (o.text || "")) ? (o.items ? o.items.map(function () { return true; }) : true) : false); return; }
      var items = o.items ? '<ul class="ev-dlg-l">' + o.items.map(function (it, i) {
        return '<li><label><input type="checkbox" checked data-i="' + i + '"><span class="ev-box">' + ic("check") + "</span>" + ic(it.icon) + "<span><b>" + esc(it.label) + "</b><small>" + esc(it.sub) + (it.crit ? ' · <em class="t-warn">action critique</em>' : "") + "</small></span><strong>" + esc(it.value) + "</strong></label></li>";
      }).join("") + "</ul>" : "";
      dlg.innerHTML = '<form method="dialog" class="ev-dlg-f"><header>' + '<span class="ev-ci' + (o.danger ? " is-warn" : "") + '">' + ic(o.icon || "shield") + '</span><div><h5 id="ev-dlg-t">' + esc(o.title) + "</h5>" + (o.text ? "<p>" + esc(o.text) + "</p>" : "") + "</div></header>" + items +
        '<footer><button type="button" class="ev-btn" value="no" data-x="no">Annuler</button><button type="button" class="ev-btn is-primary" data-x="ok">' + ic("check") + esc(o.ok || "Confirmer") + "</button></footer></form>";
      dlgResolve = function (ok) {
        var sel = o.items ? [].map.call(dlg.querySelectorAll("input[data-i]"), function (x) { return x.checked; }) : true;
        dlgResolve = null;
        dlg.close();
        res(ok ? sel : false);
      };
      dlg.showModal();
      var okB = dlg.querySelector('[data-x="ok"]');
      if (okB) okB.focus();
    });
  }
  if (dlg) {
    dlg.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-x]");
      if (b && dlgResolve) dlgResolve(b.getAttribute("data-x") === "ok");
      else if (ev.target === dlg && dlgResolve) dlgResolve(false);
    });
    dlg.addEventListener("cancel", function (ev) { ev.preventDefault(); if (dlgResolve) dlgResolve(false); });
  }
  var toastT = null;
  function toast(t) {
    if (!toastEl) return;
    toastEl.textContent = t;
    toastEl.classList.add("is-on");
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove("is-on"); }, 4200);
  }
  var popT = null;
  function admin(btn) {
    var p = app.querySelector("[data-ev-pop]");
    if (!p) { toast("Réservé à l’administrateur de votre système."); return; }
    p.hidden = false;
    p.classList.remove("is-on"); void p.offsetWidth; p.classList.add("is-on");
    clearTimeout(popT);
    popT = setTimeout(function () { p.hidden = true; }, 3200);
  }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, reduce() ? Math.min(ms, 150) : ms); }); }

  /* ======================================================================================
     Actions (délégation d'événements)
     ====================================================================================== */
  app.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-a]");
    if (!b || !app.contains(b) || b.disabled) return;
    var a = b.getAttribute("data-a"), v = b.getAttribute("data-v") || "", e = cur(), r = rt(e), i, x;
    switch (a) {
      case "pick": S.view = "home"; H.anim = true; render(); intoView(); break;
      case "env": S.view = "env"; S.env = v; S.sec = "apercu"; render(); intoView(); break;
      case "plane": if (v === S.env) break; S.env = v; if (!E[v].s[S.sec] && S.sec !== "eclairage") S.sec = "apercu"; render(); break;
      case "sec": goSec(v); break;
      case "go": goSec(v); break;
      case "tab": S.tab[S.env + S.sec] = v; renderSection(true); break;
      case "admin": admin(b); break;
      case "hjump": { var tg = app.querySelector('[data-h="' + v + '"]'); if (tg) { tg.scrollIntoView({ behavior: reduce() ? "auto" : "smooth", block: "center" }); tg.classList.remove("is-flash"); void tg.offsetWidth; tg.classList.add("is-flash"); } break; }
      case "haf": H.af = v; H.alAll = false; homeRefresh(["alerts"]); break;
      case "halall": H.alAll = !H.alAll; homeRefresh(["alerts"]); break;
      case "htl": H.tl = v; H.tlAll = false; homeRefresh(["tl"]); break;
      case "htlall": H.tlAll = !H.tlAll; homeRefresh(["tl"]); break;
      case "hcmp": H.cmp = v; homeRefresh(["cmp"]); break;
      case "hmm": H.mm = v; H.sel = null; H.res = ""; homeRefresh(["multi"]); break;
      case "hmms": mmSel()[v] = !mmSel()[v]; homeRefresh(["multi"]); break;
      case "hmmapply": multiApply(); break;
      case "hgo": { x = v.split("|"); var g2 = (x[1] || "apercu").split(":"); S.view = "env"; S.env = x[0]; S.sec = g2[0]; if (g2[1]) S.tab[x[0] + g2[0]] = g2[1]; render(); intoView(); break; }
      case "oplock": opLock(e, +b.closest("[data-c]").getAttribute("data-c"), [+v]); break;
      case "oplockall": {
        var ci7 = +b.closest("[data-c]").getAttribute("data-c"), c7 = CUR[ci7], o7 = opsOf(e, c7), js = [];
        c7.points.forEach(function (o, j) { if (o.lock && !o7[j].locked) js.push(j); });
        opLock(e, ci7, js);
        break;
      }
      case "arm": {
        var on = armedOf(e);
        var doArm = function () { r.armed = !on; log(e, r.armed ? "Système armé" : "Système désarmé", "Par vous · confirmé", r.armed ? "ok" : "warn", true); rerender(+b.closest("[data-c]").getAttribute("data-c")); toast(r.armed ? e.name + " : système armé." : e.name + " : système désarmé. Fumée et CO restent surveillés."); };
        if (on) ask({ title: "Désarmer " + e.name + "?", text: "Les alertes d’intrusion seront en pause. La fumée, le monoxyde de carbone et les fuites restent surveillés.", ok: "Désarmer", icon: "unlock", danger: true }).then(function (ok) { if (ok) doArm(); });
        else doArm();
        break;
      }
      case "toast": toast(v); break;
      case "chk": {
        x = v.split(":"); var idx = +x.pop(), id = x.join(":");
        if (r.checks[id]) r.checks[id][idx] = !r.checks[id][idx];
        rerender(+b.closest("[data-c]").getAttribute("data-c"));
        break;
      }
      case "step": {
        x = v.split(":"); var ci = +b.closest("[data-c]").getAttribute("data-c"), c = CUR[ci], key = x[0];
        var base = r.vals[key] != null ? r.vals[key] : c.set;
        setDial(e, ci, x[0], base + (+x[1]) * dialStep(c, key));
        break;
      }
      case "vent": {
        var ci2 = +b.closest("[data-c]").getAttribute("data-c");
        r.vals.vent = +v; r.pend.vent = "send"; rerender(ci2);
        setTimeout(function () { r.pend.vent = "ok"; if (S.env === e.key) rerender(ci2); }, 800);
        break;
      }
      case "tog": {
        var ci3 = +b.closest("[data-c]").getAttribute("data-c"), c3 = CUR[ci3], curOn = r.tog[v] != null ? r.tog[v] : (c3 && c3.key === v ? c3.on : v === "autoswitch" ? true : c3 && c3.rows && /^auto\d+$/.test(v) ? c3.rows[+v.slice(4)][4] : true);
        var doIt = function () {
          r.tog[v] = !curOn;
          rerender(ci3);
          if (c3 && c3.type === "toggle") log(e, c3.title + (r.tog[v] ? " activée" : " désactivée"), "Par vous", r.tog[v] ? "ok" : "warn", true);
        };
        if (c3 && c3.critical && curOn) {
          ask({ title: "Désactiver « " + c3.title + " »?", text: "Plus aucune alerte d’ouverture ne sera envoyée tant que la surveillance restera coupée.", ok: "Désactiver", icon: "warn", danger: true })
            .then(function (ok) { if (ok) doIt(); });
        } else doIt();
        break;
      }
      case "prio": {
        x = v.split(":"); i = +x[0]; var j = i + (+x[1]), ci4 = +b.closest("[data-c]").getAttribute("data-c");
        if (j < 0 || j >= r.prio.length) break;
        var el = b.closest("[data-c]"), before = {};
        el.querySelectorAll(".ev-prio li").forEach(function (li) { before[li.getAttribute("data-k")] = li.getBoundingClientRect().top; });
        var tmp = r.prio[i]; r.prio[i] = r.prio[j]; r.prio[j] = tmp;
        rerender(ci4);
        if (!reduce()) {
          app.querySelectorAll('[data-c="' + ci4 + '"] .ev-prio li').forEach(function (li) {
            var d = before[li.getAttribute("data-k")] - li.getBoundingClientRect().top;
            if (d) li.animate([{ transform: "translateY(" + d + "px)" }, { transform: "none" }], { duration: 320, easing: "cubic-bezier(.16,1,.3,1)" });
          });
        }
        var nb = app.querySelector('[data-c="' + ci4 + '"] [data-a="prio"][data-v="' + j + ":" + x[1] + '"]') || app.querySelector('[data-c="' + ci4 + '"] [data-a="prio"][data-v="' + j + ":" + (-x[1]) + '"]');
        if (nb && !nb.disabled) nb.focus();
        log(e, "Priorité réseau modifiée", CUR[ci4].items[r.prio[0]][1] + " en premier");
        break;
      }
      case "speed": {
        var ci5 = +b.closest("[data-c]").getAttribute("data-c"), c5 = CUR[ci5];
        r.vals.speed = "run"; rerender(ci5);
        setTimeout(function () { var R3 = rng(Date.now()); r.vals.speed = [c5.down * (2.2 + R3() * 1.4), c5.up * (2 + R3() * 1.5), Math.round(c5.ping * (0.85 + R3() * 0.3))]; if (S.env === e.key && CUR[ci5] === c5) rerender(ci5); }, reduce() ? 300 : 2400);
        break;
      }
      case "diag": {
        var ci6 = +b.closest("[data-c]").getAttribute("data-c");
        r.vals.diag = "run"; rerender(ci6);
        setTimeout(function () { r.vals.diag = NOW(); if (S.env === e.key) rerender(ci6); toast("Diagnostics actualisés · données d’exemple."); }, reduce() ? 200 : 1600);
        break;
      }
      case "diag2": toast("Test des connexions : passerelle, DNS et services du Hub répondent (exemple)."); break;
      case "pflt": r.vals.pflt = v; rerender(+b.closest("[data-c]").getAttribute("data-c")); break;
      case "padd": {
        var pa = r.vals.padd || (r.vals.padd = {});
        pa[v] = !pa[v];
        rerender(+b.closest("[data-c]").getAttribute("data-c"));
        toast(pa[v] ? "Ajouté au voyage d’exemple." : "Retiré du voyage.");
        break;
      }
      case "move": {
        r.moving = !r.moving;
        var grid = app.querySelector(".ev-grid");
        CUR.forEach(function (c, k) { if (c.type === "status" || c.type === "equip") rerender(k); });
        if (grid) grid.classList.toggle("is-moving", r.moving);
        toast(r.moving ? "Simulation : véhicule en mouvement. Les commandes extérieures sont verrouillées." : "Simulation : véhicule à l’arrêt. Commandes disponibles.");
        break;
      }
      case "eq": equipAction(e, +v); break;
      case "eqt": {
        var st = r.eq[+v] || (r.eq[+v] = {});
        st.on = !st.on; rerender(+v);
        log(e, CUR[+v].title + (st.on ? " allumé" : " en veille"), "Confirmé");
        break;
      }
      case "week": r.vals.week = v === "0" ? 0 : (r.vals.week || 0) + (+v); rerender(+b.closest("[data-c]").getAttribute("data-c")); break;
      case "list": r.vals.list = v; rerender(+b.closest("[data-c]").getAttribute("data-c")); break;
      case "lsel": x = v.split(":"); r.vals["lsel:" + x[0]] = +x[1]; rerender(+b.closest("[data-c]").getAttribute("data-c")); break;
      case "mplan": {
        var mp = r.vals.mplan || (r.vals.mplan = {});
        mp[v] = !mp[v]; rerender(+b.closest("[data-c]").getAttribute("data-c"));
        if (mp[v]) toast("Rappel d’entretien planifié (exemple).");
        break;
      }
      case "msel": r.vals.msel = v; r.vals.mres = null; rerender(+b.closest("[data-c]").getAttribute("data-c")); break;
      case "mapply": applyMode(e, v, +b.closest("[data-c]").getAttribute("data-c")); break;
    }
  });

  function equipAction(e, i) {
    var c = CUR[i], a = c.act, r = rt(e), st = r.eq[i] || (r.eq[i] = {});
    if (a.preview) { ask({ title: a.label, text: a.text, ok: "Compris", icon: c.icon }); return; }
    var lab = st.flip ? (a.back || a.label) : a.label;
    ask({ title: lab + " · " + c.title, text: st.flip ? "Confirmer la commande « " + lab + " »?" : a.confirm, ok: lab, icon: c.icon }).then(function (ok) {
      if (!ok) return;
      st.busy = true; rerender(i);
      wait(1400).then(function () {
        st.busy = false;
        if (a.fail) { st.tone = "warn"; st.state = "À vérifier · aucune confirmation"; log(e, c.title + " : " + lab, "Aucune confirmation de l’appareil", "warn"); toast(c.title + " : l’appareil n’a pas confirmé. État affiché : à vérifier."); }
        else {
          st.flip = !st.flip; st.state = st.flip ? a.done : c.state; st.tone = "ok";
          log(e, c.title + " : " + (st.flip ? a.done : c.state).toLowerCase(), "Confirmé par l’appareil", "ok");
        }
        if (S.env === e.key && CUR[i] === c) rerender(i);
      });
    });
  }

  /* Consigne d'un cadran : envoyée, puis confirmée par l'appareil */
  function dialStep(c, key) { return c.step || (key === "hot" ? 1 : 0.5); }
  function setDial(e, ci, key, nv, quiet) {
    var r = rt(e), c = CUR[ci];
    nv = clamp(Math.round(nv / dialStep(c, key)) * dialStep(c, key), c.min, c.max);
    r.vals[key] = nv; r.pend[key] = "send";
    if (!quiet) rerender(ci);
    clearTimeout(r["t" + key]);
    r["t" + key] = setTimeout(function () { r.pend[key] = "ok"; if (S.env === e.key && CUR[ci] === c) rerender(ci); log(e, (key === "hot" ? "Consigne d’eau chaude" : "Consigne de " + c.title.toLowerCase()) + " : " + nf(nv, nv % 1 ? 1 : 0) + NB + "°C", "Confirmée par l’appareil"); }, 900);
  }
  /* Glisser sur le cadran : la valeur suit le doigt; l'envoi part au relâchement */
  var drag = null;
  function dialAt(ev, g, c) {
    var rc = g.getBoundingClientRect(), dx = ev.clientX - (rc.left + rc.width / 2), dy = ev.clientY - (rc.top + rc.height / 2);
    var a = Math.atan2(dx, -dy) / RAD;
    if (a > 135 || a < -135) a = a > 0 ? 135 : -135;
    return c.min + (a + 135) / 270 * (c.max - c.min);
  }
  function dialPaint(g, c, key, v) {
    var sv = g.querySelector("svg"), md = dialMode(c, v, key);
    if (sv) sv.outerHTML = dialSVG(c, v, key);
    var dv = g.querySelector("[data-dv]"), dm = g.querySelector("[data-dm]");
    if (dv) dv.innerHTML = nf(v, v % 1 ? 1 : 0) + "<sup>°C</sup>";
    if (dm) { dm.className = "ev-dial-m is-" + md[0]; dm.innerHTML = ic(md[1]) + md[2]; }
    g.setAttribute("aria-valuenow", v);
  }
  app.addEventListener("pointerdown", function (ev) {
    var g = ev.target.closest("[data-dial]");
    if (!g || S.view !== "env") return;
    var ci = +g.closest("[data-c]").getAttribute("data-c"), c = CUR[ci], key = g.getAttribute("data-dial");
    drag = { g: g, ci: ci, c: c, key: key, v: null };
    try { g.setPointerCapture(ev.pointerId); } catch (err) {}
    g.classList.add("is-drag");
    ev.preventDefault();
    var v0 = clamp(Math.round(dialAt(ev, g, c) / dialStep(c, key)) * dialStep(c, key), c.min, c.max);
    drag.v = v0; dialPaint(g, c, key, v0);
  });
  app.addEventListener("pointermove", function (ev) {
    var pa = ev.target.closest && ev.target.closest(".ev-pa[data-tip]");
    if (pa) plotTip(pa, ev);
  });
  app.addEventListener("pointerout", function (ev) {
    var pa = ev.target.closest && ev.target.closest(".ev-pa[data-tip]");
    if (pa && !pa.contains(ev.relatedTarget)) { var c = pa.querySelector(".ev-pc"); if (c) c.hidden = true; }
  });
  app.addEventListener("pointermove", function (ev) {
    if (!drag) return;
    var v1 = clamp(Math.round(dialAt(ev, drag.g, drag.c) / dialStep(drag.c, drag.key)) * dialStep(drag.c, drag.key), drag.c.min, drag.c.max);
    if (v1 !== drag.v) { drag.v = v1; dialPaint(drag.g, drag.c, drag.key, v1); }
  });
  function dialEnd() { if (!drag) return; var d = drag; drag = null; d.g.classList.remove("is-drag"); setDial(cur(), d.ci, d.key, d.v); }
  app.addEventListener("pointerup", dialEnd);
  app.addEventListener("pointercancel", dialEnd);
  app.addEventListener("keydown", function (ev) {
    var g = ev.target.closest && ev.target.closest("[data-dial]");
    if (!g) return;
    var d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[ev.key];
    if (!d) return;
    ev.preventDefault();
    var ci = +g.closest("[data-c]").getAttribute("data-c"), c = CUR[ci], key = g.getAttribute("data-dial"), r = rt(cur());
    setDial(cur(), ci, key, (r.vals[key] != null ? r.vals[key] : c.set) + d * dialStep(c, key));
    var ng = app.querySelector('[data-c="' + ci + '"] [data-dial]');
    if (ng) ng.focus();
  });

  /* Verrous des ouvertures : verrouiller est direct; déverrouiller demande toujours confirmation */
  function opLock(e, ci, js) {
    var c = CUR[ci], ops = opsOf(e, c);
    if (!js.length) return;
    var unlock = js.length === 1 && ops[js[0]].locked;
    var go = function () {
      js.forEach(function (j) { ops[j].busy = true; });
      rerender(ci);
      wait(900).then(function () {
        js.forEach(function (j) {
          var o = ops[j];
          o.busy = false; o.locked = !unlock; o.state = unlock ? "Déverrouillée" : "Verrouillée"; o.tone = unlock ? "gold" : "ok";
          if (unlock) { o.ago = 0; o.who = "Vous"; }
          log(e, c.points[j].label + (unlock ? " déverrouillée" : " verrouillée"), "Confirmé par la serrure", unlock ? "warn" : "ok", true);
        });
        if (S.env === e.key && CUR[ci] === c) rerender(ci);
        toast(js.length > 1 ? js.length + " serrures verrouillées · confirmées." : c.points[js[0]].label + (unlock ? " déverrouillée." : " verrouillée · confirmée par la serrure."));
      });
    };
    if (unlock) ask({ title: "Déverrouiller « " + c.points[js[0]].label + " »?", text: "La porte restera déverrouillée jusqu’à votre prochaine commande ou au mode Nuit.", ok: "Déverrouiller", icon: "unlock", danger: true }).then(function (ok) { if (ok) go(); });
    else if (js.length > 1) ask({ title: "Verrouiller " + js.length + " accès?", text: js.map(function (j) { return c.points[j].label; }).join(", ") + ".", ok: "Tout verrouiller", icon: "lock" }).then(function (ok) { if (ok) go(); });
    else go();
  }

  /* Mode sur plusieurs lieux : une confirmation pour la liste, puis chaque lieu et chaque effet confirmés */
  function multiApply() {
    var M0 = D.multi.filter(function (m) { return m.k === H.mm; })[0], sel = mmSel(), keys = D.order.filter(function (k) { return sel[k] && mmLocal(E[k], H.mm); });
    if (!keys.length || H.run) return;
    var items = keys.map(function (k) {
      var e = E[k], L = mmLocal(e, H.mm), crit = L.fx.filter(function (f) { return /crit/.test(f[4] || ""); });
      return { icon: e.icon || "home", label: e.name, sub: "Mode " + L.label + " · " + L.fx.map(function (f) { return f[1].toLowerCase(); }).join(", "), value: L.label, crit: crit.length > 0 };
    });
    ask({ title: "Appliquer « " + M0.label + " » à " + keys.length + " lieu" + (keys.length > 1 ? "x" : "") + "?", text: "Chaque lieu reçoit son propre mode. Décochez un lieu pour l’exclure. Chaque effet est envoyé, puis confirmé séparément.", items: items, ok: "Appliquer", icon: M0.icon })
      .then(function (ok) {
        if (!ok) return;
        var todo = keys.filter(function (k, i) { return ok[i]; });
        if (!todo.length) return;
        H.run = true;
        var lines = {}, seq = Promise.resolve();
        function paint(done) {
          H.res = '<p class="ev-k">' + (done ? "Résultat" : "Application en cours…") + "</p>" + todo.map(function (k) { return lines[k] || '<div class="ev-mline">' + ic("clock") + "<span>" + esc(E[k].name) + "</span><em>En attente</em></div>"; }).join("");
          if (S.view === "home") homeRefresh(["multi"]);
        }
        paint(false);
        todo.forEach(function (k) {
          seq = seq.then(function () {
            var e = E[k], L = mmLocal(e, H.mm), okN = 0, p2 = Promise.resolve();
            lines[k] = '<div class="ev-mline is-wait">' + ic("refresh", "is-spin") + "<span>" + esc(e.name) + " · " + esc(L.label) + "</span><em>Envoi…</em></div>";
            paint(false);
            L.fx.forEach(function (f) {
              p2 = p2.then(function () {
                if (/light/.test(f[4] || "") && f[5]) {
                  var LM = window.JarvisLumieres;
                  return LM && typeof LM.applyAmbiance === "function" ? Promise.resolve(LM.applyAmbiance(k, f[5])).then(function (res) { if (!(res && res.failed)) okN++; }, function () {}) : wait(250);
                }
                return wait(260).then(function () { if (!/fail/.test(f[4] || "")) okN++; });
              });
            });
            return p2.then(function () {
              var all = okN === L.fx.length;
              rt(e).mode = L.k;
              if (H.mm !== "froid") rt(e).armed = true;
              log(e, "Mode " + L.label + " appliqué depuis l’accueil", okN + " / " + L.fx.length + " effets confirmés", all ? "ok" : "warn", false);
              lines[k] = '<div class="ev-mline ' + (all ? "is-ok" : "is-warn") + '">' + ic(all ? "check" : "warn") + "<span>" + esc(e.name) + " · " + esc(L.label) + "</span><em>" + okN + " / " + L.fx.length + " confirmés" + (all ? "" : " · à vérifier") + "</em></div>";
              paint(false);
            });
          });
        });
        seq.then(function () {
          H.run = false; H.sel = null;
          paint(true);
          if (S.view === "home") homeRefresh(["sum", "board", "alerts", "tl", "multi"]);
          toast("« " + M0.label + " » appliqué à " + todo.length + " lieu" + (todo.length > 1 ? "x" : "") + ". Le détail est au journal.");
        });
      });
  }

  function applyMode(e, k, ci) {
    var c = CUR[ci], M = c.items.filter(function (m) { return m.k === k; })[0], r = rt(e);
    var items = M.fx.map(function (f) { return { icon: f[0], label: f[1], sub: f[2], value: f[3], crit: /crit/.test(f[4] || "") }; });
    ask({ title: "Appliquer le mode " + M.label + "?", text: "Choisissez les effets à appliquer. Chacun est envoyé, puis confirmé séparément.", items: items, ok: "Appliquer", icon: M.icon }).then(function (sel) {
      if (!sel) return;
      r.vals.mrun = true;
      var lines = [], okN = 0, total = 0;
      function paint(done) {
        r.vals.mres = { k: k, html: '<p class="ev-k">' + (done ? "Résultat" : "Application en cours…") + "</p>" + lines.join("") };
        if (S.env === e.key && CUR[ci] === c) rerender(ci);
      }
      var seq = Promise.resolve();
      M.fx.forEach(function (f, idx) {
        if (!sel[idx]) return;
        total++;
        seq = seq.then(function () {
          var li = lines.length;
          lines.push('<div class="ev-mline is-wait">' + ic("refresh", "is-spin") + "<span>" + esc(f[1]) + " · " + esc(f[3]) + "</span><em>Envoi…</em></div>");
          paint(false);
          var p;
          if (/light/.test(f[4] || "") && f[5]) {
            var L = window.JarvisLumieres;
            p = L && typeof L.applyAmbiance === "function" ? Promise.resolve(L.applyAmbiance(e.key, f[5])).then(function (res) {
              var cf = res && res.confirmed != null ? res.confirmed : 0, fl = res && res.failed != null ? res.failed : 0;
              return fl ? { ok: cf > 0, partial: true, note: cf + " confirmée" + (cf > 1 ? "s" : "") + ", " + fl + " à vérifier" } : { ok: true, note: cf ? cf + " lumière" + (cf > 1 ? "s" : "") + " confirmée" + (cf > 1 ? "s" : "") : "Confirmé" };
            }, function () { return { ok: false, note: "Le module d’éclairage n’a pas répondu" }; })
              : wait(700).then(function () { return { ok: false, note: "Module d’éclairage non branché : rien n’a été envoyé" }; });
          } else p = wait(650).then(function () { return /fail/.test(f[4] || "") ? { ok: false, note: "Aucune réponse de l’appareil · à vérifier" } : { ok: true, note: "Confirmé par l’appareil" }; });
          return p.then(function (res) {
            if (res.ok && !res.partial) okN++;
            lines[li] = '<div class="ev-mline ' + (res.ok && !res.partial ? "is-ok" : "is-warn") + '">' + ic(res.ok && !res.partial ? "check" : "warn") + "<span>" + esc(f[1]) + " · " + esc(f[3]) + "</span><em>" + esc(res.note) + "</em></div>";
            paint(false);
          });
        });
      });
      seq.then(function () {
        r.vals.mrun = false;
        r.mode = k;
        lines.push('<p class="ev-msum ' + (okN === total ? "t-ok" : "t-warn") + '">' + (okN === total ? ic("check") + "Mode " + M.label + " appliqué : " + okN + " / " + total + " effets confirmés."
          : ic("warn") + "Mode " + M.label + " appliqué en partie : " + okN + " / " + total + " effets confirmés. Les autres restent à vérifier.") + "</p>");
        paint(true);
        log(e, "Mode " + M.label + " appliqué", okN + " / " + total + " effets confirmés", okN === total ? "ok" : "warn", true);
      });
    });
  }

  /* ======================================================================================
     Visibilité : mesures et animations seulement quand la démo est à l'écran
     ====================================================================================== */
  var visible = false;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        visible = en.isIntersecting;
        root.classList.toggle("is-off", !visible);
        if (visible) liveLoop(); else { clearInterval(LIVE.timer); LIVE.timer = null; }
      });
    }, { rootMargin: "120px 0px" }).observe(root);
  } else visible = true;
  document.addEventListener("visibilitychange", function () { if (!document.hidden) liveLoop(); });

  render();
})();
