/* « Météo en direct » : le ciel de Saint-Hyacinthe, 100 % réel.
   Données : Environnement et Changement climatique Canada (API GeoMet) — page météo de
   Saint-Hyacinthe (qc-22) et mesures SWOB de la station de Granby (SMC). La lune est calculée
   localement (formules astronomiques). Rien n'est inventé : sans données, on le dit.
   Le ciel (canevas) suit l'heure réelle, le lever et le coucher, les nuages, la pluie ou la neige
   et le vent réels. Il ne s'anime que visible, et reste fixe si le mouvement est réduit.
   Les décisions de JARVIS sont simulées : aucun appareil n'est commandé. */
(function () {
  "use strict";
  var roots = [].slice.call(document.querySelectorAll('[data-demo="meteo"]'));
  if (!roots.length) return;

  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var TZ = "America/Toronto";
  var HOME = { lat: 45.63, lon: -72.95 };
  var STN = { name: "Granby", lat: 45.372631, lon: -72.774189 };
  var NB = " ", MINUS = "−";
  var EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/qc-22?f=json&lang=fr";
  var SWOB_URL = "https://api.weather.gc.ca/collections/swob-realtime/items?f=json&msc_id-value=7022802&limit=4&sortby=-date_tm-value" +
    "&properties=date_tm-value,air_temp,rel_hum,mslp,pres_tend_char_pst3hrs,pres_tend_amt_pst3hrs,pcpn_amt_pst1hr,pcpn_amt_pst24hrs";
  var EC_PAGE = "https://meteo.gc.ca/fr/location/index.html?coords=45.63,-72.95";
  var LICENCE = "https://ouvert.canada.ca/fr/licence-du-gouvernement-ouvert-canada";
  var FRESH = 300000, REFRESH = 600000, RETRY = 120000;

  /* ---------- Lecture des valeurs d'EC (souvent { value: { fr, en } }) ---------- */
  function val(o) {
    if (o == null) return undefined;
    var v = o.value !== undefined ? o.value : o;
    if (v && typeof v === "object") v = v.fr !== undefined ? v.fr : v.en;
    return v;
  }
  function txt(o) {
    if (o == null) return "";
    if (typeof o === "string" || typeof o === "number") return String(o);
    if (o.fr !== undefined) return String(o.fr);
    if (o.value !== undefined) return txt(o.value);
    return o.en !== undefined ? String(o.en) : "";
  }
  function num(o) { var n = parseFloat(val(o)); return isFinite(n) ? n : null; }
  /* Texte d'EC pour l'affichage : apostrophes typographiques */
  function say(o) { return txt(o).replace(/'/g, "’"); }
  function when(s) { var d = s ? new Date(s) : null; return d && !isNaN(d) ? d : null; }
  function c01(v) { return Math.max(0, Math.min(1, v)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------- Formats (français du Québec) ---------- */
  var fmtParts = (function () {
    try {
      var f = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, hour: "numeric", minute: "2-digit", hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit" });
      return function (d) { var o = {}; f.formatToParts(d).forEach(function (p) { o[p.type] = p.value; }); return o; };
    } catch (e) {
      return function (d) { return { hour: String(d.getHours()), minute: String(d.getMinutes()).padStart(2, "0"), year: d.getFullYear(), month: d.getMonth() + 1, day: d.getDate() }; };
    }
  })();
  function hm(d) { var p = fmtParts(d); return (+p.hour) + NB + "h" + NB + p.minute; }
  function hh(d) { return (+fmtParts(d).hour) + NB + "h"; }
  function dayKey(d) { var p = fmtParts(d); return p.year + "-" + p.month + "-" + p.day; }
  var WEEKDAY = (function () {
    try { var f = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, weekday: "long" }); return function (d) { return f.format(d); }; }
    catch (e) { return function (d) { return ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"][d.getDay()]; }; }
  })();
  /* « 16 h », « 3 h demain » ou « 3 h samedi » (minutes en option) */
  function at(d, now, withMin) {
    var k = dayKey(d), t = withMin ? hm(d) : hh(d);
    if (k === dayKey(now)) return t;
    if (k === dayKey(new Date(now.getTime() + 864e5))) return t + " demain";
    return t + " " + WEEKDAY(d);
  }
  function sgn(s) { return String(s).replace("-", MINUS); }
  function int(n) { return sgn(Math.round(n) === 0 ? 0 : Math.round(n)); }
  function dec1(n) { return sgn((Math.round(n * 10) / 10).toFixed(1).replace(".", ",")).replace(MINUS + "0,0", "0,0"); }
  function cap(s) { s = String(s || ""); return s.charAt(0).toUpperCase() + s.slice(1); }
  function dur(ms) { var m = Math.round(ms / 60000); return Math.floor(m / 60) + NB + "h" + NB + String(m % 60).padStart(2, "0"); }
  function within(ms) {
    var m = Math.round(Math.abs(ms) / 60000);
    if (m < 60) return m + NB + "min";
    return Math.floor(m / 60) + NB + "h" + (m % 60 ? NB + String(m % 60).padStart(2, "0") : "");
  }
  function km(a, b) {
    var R = 6371, r = Math.PI / 180, dLa = (b.lat - a.lat) * r, dLo = (b.lon - a.lon) * r;
    var h = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLo / 2) * Math.sin(dLo / 2);
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  /* « 45.52N » / « 73.42O » → degrés signés */
  function coord(s) {
    var m = /(-?[\d.]+)\s*([NSEWO])?/i.exec(s || "");
    if (!m) return null;
    var v = parseFloat(m[1]);
    return /[SWO]/i.test(m[2] || "") ? -v : v;
  }
  function sentence(s) {
    s = String(s || "").toLowerCase().replace(/'/g, "’").replace(/\s+-\s+/g, " – ");
    return cap(s);
  }

  /* ---------- Vent : abréviations d'EC en français ---------- */
  var DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"];
  var DIR_NAMES = {
    N: "nord", NNE: "nord-nord-est", NE: "nord-est", ENE: "est-nord-est", E: "est", ESE: "est-sud-est", SE: "sud-est",
    SSE: "sud-sud-est", S: "sud", SSO: "sud-sud-ouest", SO: "sud-ouest", OSO: "ouest-sud-ouest", O: "ouest",
    ONO: "ouest-nord-ouest", NO: "nord-ouest", NNO: "nord-nord-ouest"
  };
  function dirPhrase(abbr) {
    var n = DIR_NAMES[abbr];
    if (!n) return abbr === "VR" ? "Vent variable" : "";
    return "Vent " + (/^[eo]/.test(n) ? "de l’" : "du ") + n;
  }
  function dirBearing(abbr) { var i = DIRS.indexOf(abbr); return i < 0 ? null : i * 22.5; }

  /* ---------- Astronomie : lune réelle et lever du lendemain ---------- */
  var RAD = Math.PI / 180, DAY = 864e5, J1970 = 2440588, J2000 = 2451545, OBL = RAD * 23.4397, J0 = .0009;
  function toDays(d) { return d.valueOf() / DAY - .5 + J1970 - J2000; }
  function rAsc(l, b) { return Math.atan2(Math.sin(l) * Math.cos(OBL) - Math.tan(b) * Math.sin(OBL), Math.cos(l)); }
  function decl(l, b) { return Math.asin(Math.sin(b) * Math.cos(OBL) + Math.cos(b) * Math.sin(OBL) * Math.sin(l)); }
  function meanAnom(d) { return RAD * (357.5291 + .98560028 * d); }
  function eclLon(M) { return M + RAD * (1.9148 * Math.sin(M) + .02 * Math.sin(2 * M) + .0003 * Math.sin(3 * M)) + RAD * 102.9372 + Math.PI; }
  function sunC(d) { var L = eclLon(meanAnom(d)); return { dec: decl(L, 0), ra: rAsc(L, 0) }; }
  function moonC(d) {
    var L = RAD * (218.316 + 13.176396 * d), M = RAD * (134.963 + 13.064993 * d), F = RAD * (93.272 + 13.22935 * d);
    var l = L + RAD * 6.289 * Math.sin(M), b = RAD * 5.128 * Math.sin(F);
    return { ra: rAsc(l, b), dec: decl(l, b), dist: 385001 - 20905 * Math.cos(M) };
  }
  /* Position (azimut depuis le sud, positif vers l'ouest ; hauteur) */
  function skyPos(date, c) {
    var lw = RAD * -HOME.lon, phi = RAD * HOME.lat, d = toDays(date);
    var H = RAD * (280.16 + 360.9856235 * d) - lw - c.ra;
    return {
      az: Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(phi) - Math.tan(c.dec) * Math.cos(phi)),
      alt: Math.asin(Math.sin(phi) * Math.sin(c.dec) + Math.cos(phi) * Math.cos(c.dec) * Math.cos(H))
    };
  }
  function moonPos(date) { return skyPos(date, moonC(toDays(date))); }
  function sunPos(date) { return skyPos(date, sunC(toDays(date))); }
  function moonIllum(date) {
    var d = toDays(date), s = sunC(d), m = moonC(d), sd = 149598000;
    var phi = Math.acos(Math.sin(s.dec) * Math.sin(m.dec) + Math.cos(s.dec) * Math.cos(m.dec) * Math.cos(s.ra - m.ra));
    var inc = Math.atan2(sd * Math.sin(phi), m.dist - sd * Math.cos(phi));
    var ang = Math.atan2(Math.cos(s.dec) * Math.sin(s.ra - m.ra), Math.sin(s.dec) * Math.cos(m.dec) - Math.cos(s.dec) * Math.sin(m.dec) * Math.cos(s.ra - m.ra));
    return { fraction: (1 + Math.cos(inc)) / 2, phase: .5 + .5 * inc * (ang < 0 ? -1 : 1) / Math.PI };
  }
  function moonName(p) {
    var names = ["Nouvelle lune", "Premier croissant", "Premier quartier", "Gibbeuse croissante", "Pleine lune",
      "Gibbeuse décroissante", "Dernier quartier", "Dernier croissant"];
    return names[Math.round(p * 8) % 8];
  }
  /* Lever et coucher calculés (±2 min) : servent seulement à ombrer la nuit de demain */
  function sunTimes(date) {
    var lw = RAD * -HOME.lon, phi = RAD * HOME.lat, d = toDays(date), n = Math.round(d - J0 - lw / (2 * Math.PI));
    var ds = J0 + lw / (2 * Math.PI) + n, M = meanAnom(ds), L = eclLon(M), de = decl(L, 0);
    var Jnoon = J2000 + ds + .0053 * Math.sin(M) - .0069 * Math.sin(2 * L);
    var w = Math.acos((Math.sin(-.833 * RAD) - Math.sin(phi) * Math.sin(de)) / (Math.cos(phi) * Math.cos(de)));
    var a = J0 + (w + lw) / (2 * Math.PI) + n, Jset = J2000 + a + .0053 * Math.sin(M) - .0069 * Math.sin(2 * L);
    var f = function (j) { return new Date((j + .5 - J1970) * DAY); };
    return { rise: f(Jnoon - (Jset - Jnoon)), set: f(Jset), noon: f(Jnoon) };
  }

  /* ---------- Codes d'icônes d'EC → ciel et pictogramme ----------
     c : couverture nuageuse (0 à 1) ; p : précipitation ; i : intensité ; k : pictogramme */
  var SKY = {};
  function def(codes, o) { codes.forEach(function (c) { SKY[c] = o; }); }
  def([0, 30], { c: 0, k: "clear" });
  def([1, 31], { c: .18, k: "few" });
  def([2, 4, 5, 22, 32, 34, 35], { c: .42, k: "partly" });
  def([3, 33], { c: .72, k: "mostly" });
  def([10, 29], { c: .96, k: "cloud" });
  def([6, 36], { c: .62, p: "rain", i: .35, k: "showers" });
  def([7, 37], { c: .66, p: "mix", i: .35, k: "showers-mix" });
  def([8, 38], { c: .66, p: "snow", i: .35, k: "flurries" });
  def([9, 39], { c: .8, p: "rain", i: .55, t: 1, k: "storm-sun" });
  def([11, 12], { c: .95, p: "rain", i: .55, k: "rain" });
  def([13], { c: 1, p: "rain", i: .9, k: "rain-heavy" });
  def([14], { c: 1, p: "rain", i: .6, k: "freezing" });
  def([15], { c: 1, p: "mix", i: .6, k: "mix" });
  def([16, 26], { c: .92, p: "snow", i: .5, k: "snow" });
  def([17, 25], { c: 1, p: "snow", i: .75, k: "snow" });
  def([18, 40], { c: 1, p: "snow", i: 1, k: "snow-heavy" });
  def([19, 41, 42, 46, 47, 48], { c: 1, p: "rain", i: .8, t: 1, k: "storm" });
  def([27], { c: 1, p: "pellets", i: .6, k: "pellets" });
  def([28], { c: .95, p: "drizzle", i: .5, k: "drizzle" });
  def([20, 21, 24], { c: .9, f: 1, k: "fog" });
  def([23, 44, 45], { c: .25, f: .5, k: "haze" });
  def([43], { c: .3, k: "wind" });
  function sky(code) { return SKY[code] || { c: .5, k: "cloud" }; }
  function wetKind(code) {
    var s = sky(code);
    if (s.p === "snow") return "snow";
    if (s.k === "freezing" || s.p === "pellets") return "ice";
    return s.p ? "rain" : null;
  }

  /* ---------- Pictogrammes au trait (24 × 24) ---------- */
  var CLOUD = "M7.5 18.5h9.75a3.75 3.75 0 0 0 .4-7.48a5.25 5.25 0 0 0-10.1-.9A4.2 4.2 0 0 0 7.5 18.5z";
  function rays(cx, cy, r1, r2) {
    var s = "";
    for (var i = 0; i < 8; i++) {
      var a = i * Math.PI / 4;
      s += "M" + (cx + r1 * Math.cos(a)).toFixed(2) + " " + (cy + r1 * Math.sin(a)).toFixed(2) +
        "L" + (cx + r2 * Math.cos(a)).toFixed(2) + " " + (cy + r2 * Math.sin(a)).toFixed(2);
    }
    return s;
  }
  function sunG(cx, cy, r) { return '<g class="i-sun"><circle cx="' + cx + '" cy="' + cy + '" r="' + r + '"/><path d="' + rays(cx, cy, r + 2.1, r + 3.9) + '"/></g>'; }
  function moonG(cx, cy, r) {
    /* Croissant : disque moins un disque décalé */
    var x1 = cx + r * .62, y1 = cy - r * .78, x2 = cx + r * .72, y2 = cy + r * .7;
    return '<path class="i-moon" d="M' + x1.toFixed(2) + " " + y1.toFixed(2) + "A" + r + " " + r + " 0 1 0 " + x2.toFixed(2) + " " + y2.toFixed(2) +
      "A" + (r * .78).toFixed(2) + " " + (r * .78).toFixed(2) + " 0 0 1 " + x1.toFixed(2) + " " + y1.toFixed(2) + 'z"/>';
  }
  function cloudG(tf) { return '<path class="i-cloud" d="' + CLOUD + '"' + (tf ? ' transform="' + tf + '"' : "") + "/>"; }
  function drops(n, short) {
    var xs = n === 4 ? [6.5, 10.5, 14.5, 18.5] : [8, 12, 16], s = "";
    xs.forEach(function (x) { s += "M" + (x + .6) + " " + 17.6 + "l-" + (short ? .5 : 1.1) + " " + (short ? 1.5 : 3.4); });
    return '<path class="i-wet" d="' + s + '"/>';
  }
  function flakes(n) {
    var pts = n > 5 ? [[7, 18.4], [11, 18.4], [15, 18.4], [19, 18.4], [9, 21.4], [13, 21.4], [17, 21.4]] : [[8, 18.4], [12, 18.4], [16, 18.4], [10, 21.4], [14, 21.4]];
    return '<g class="i-snow">' + pts.map(function (p) { return '<circle cx="' + p[0] + '" cy="' + p[1] + '" r=".95"/>'; }).join("") + "</g>";
  }
  var ICONS = {
    clear: function (n) { return n ? moonG(12, 12, 6.2) : sunG(12, 12, 4.2); },
    few: function (n) { return (n ? moonG(10.5, 10, 5.4) : sunG(10.5, 10.5, 3.6)) + cloudG("translate(9.6 10.4) scale(.6)"); },
    partly: function (n) { return (n ? moonG(9, 8.6, 4.4) : sunG(8.6, 8.6, 3)) + cloudG("translate(1.4 1.4)"); },
    mostly: function (n) { return (n ? moonG(7.4, 6.8, 3.2) : sunG(7.2, 7.2, 2.3)) + cloudG("translate(.8 .8)"); },
    cloud: function () { return cloudG(); },
    showers: function (n) { return (n ? moonG(8, 6.4, 3.4) : sunG(7.4, 6.6, 2.4)) + cloudG("translate(1 -3)") + drops(3); },
    "showers-mix": function (n) { return (n ? moonG(8, 6.4, 3.4) : sunG(7.4, 6.6, 2.4)) + ICONS.mix().replace(CLOUD + '" transform="translate(0 -3.4)', CLOUD + '" transform="translate(1 -3)'); },
    flurries: function (n) { return (n ? moonG(8, 6.4, 3.4) : sunG(7.4, 6.6, 2.4)) + cloudG("translate(1 -3)") + flakes(5); },
    rain: function () { return cloudG("translate(0 -3.4)") + drops(3); },
    "rain-heavy": function () { return cloudG("translate(0 -3.4)") + drops(4); },
    drizzle: function () { return cloudG("translate(0 -3.4)") + drops(4, 1); },
    freezing: function () { return cloudG("translate(0 -3.4)") + drops(3, 1) + '<path class="i-wet" d="M6 22.2h12"/>'; },
    mix: function () { return cloudG("translate(0 -3.4)") + '<path class="i-wet" d="M8.6 17.6l-1.1 3.4M16.6 17.6l-1.1 3.4"/><g class="i-snow"><circle cx="12" cy="18.4" r=".95"/><circle cx="12" cy="21.6" r=".95"/></g>'; },
    pellets: function () { return cloudG("translate(0 -3.4)") + '<g class="i-wet"><circle cx="8" cy="19" r="1.1"/><circle cx="12" cy="21" r="1.1"/><circle cx="16" cy="19" r="1.1"/></g>'; },
    snow: function () { return cloudG("translate(0 -3.4)") + flakes(5); },
    "snow-heavy": function () { return cloudG("translate(0 -3.4)") + flakes(7); },
    "storm-sun": function (n) { return (n ? moonG(8, 6.4, 3.4) : sunG(7.4, 6.6, 2.4)) + cloudG("translate(1 -3)") + '<path class="i-bolt" d="M13 15.4l-2.6 3.6h3l-1.8 3.6"/>'; },
    storm: function () { return cloudG("translate(0 -3.4)") + '<path class="i-bolt" d="M12.8 15.2l-2.6 3.8h3l-1.8 3.6"/>' + '<path class="i-wet" d="M7.6 17.6l-.9 2.8M17.6 17.6l-.9 2.8"/>'; },
    fog: function () { return '<path class="i-fog" d="M4 8.5h16M2.5 12.5h19M5 16.5h14M8 20.5h8"/>'; },
    haze: function (n) { return (n ? moonG(12, 8, 3.6) : sunG(12, 8.4, 2.8)) + '<path class="i-fog" d="M3 16h18M6 19.5h12"/>'; },
    wind: function () { return '<path class="i-fog" d="M3 9h10.5a2.5 2.5 0 1 0-2.5-2.5M3 13h15.5a2.5 2.5 0 1 1-2.5 2.5M3 17h8"/>'; }
  };
  function nightCode(code, t, m) {
    if (code >= 30 && code <= 39) return true;
    if (code >= 0 && code <= 9) return false;
    return isNightAt(t, m);
  }
  function iconSvg(code, night, cls) {
    var k = sky(code).k, f = ICONS[k] || ICONS.cloud;
    return '<svg class="mt-ico ' + (cls || "") + '" viewBox="0 0 24 24" aria-hidden="true">' + f(night) + "</svg>";
  }

  /* ---------- Jour ou nuit, à partir des vraies heures du soleil ---------- */
  function sunEvents(m) {
    /* Lever et coucher d'aujourd'hui (EC), puis veille et lendemain (calculés) */
    var ev = [];
    if (!m.rise || !m.set) return ev;
    [-1, 0, 1, 2].forEach(function (k) {
      if (k === 0) { ev.push({ t: m.rise, up: true, ec: true }, { t: m.set, up: false, ec: true }); return; }
      var s = sunTimes(new Date(m.rise.getTime() + k * DAY + 5 * 36e5));
      ev.push({ t: s.rise, up: true }, { t: s.set, up: false });
    });
    return ev.sort(function (a, b) { return a.t - b.t; });
  }
  function isNightAt(t, m) {
    var ev = sunEvents(m), last = null;
    ev.forEach(function (e) { if (e.t <= t) last = e; });
    if (!last) return false;
    return !last.up;
  }
  /* Élévation fictive de -1 (nuit noire) à 1 (plein jour), en minutes du lever ou du coucher */
  function elevation(m, now) {
    if (!m.rise || !m.set) return -.7;
    var ev = sunEvents(m), prev = null, next = null;
    ev.forEach(function (e) { if (e.t <= now) prev = e; else if (!next) next = e; });
    if (!prev || !next) return -.7;
    var since = (now - prev.t) / 60000, until = (next.t - now) / 60000;
    if (prev.up) return Math.min(1, since / 120, until / 120);
    return -Math.min(1, since / 80, until / 80);
  }

  /* ---------- Modèle à partir du JSON d'EC ---------- */
  function parse(j) {
    var p = j.properties || {}, cc = p.currentConditions || {}, now = new Date();
    var temp = num(cc.temperature);
    var wc = num(cc.windChill), hx = num(cc.humidex), feels = null, feelsKind = "";
    /* Ressenti : refroidissement éolien seulement s'il fait froid, humidex seulement s'il fait chaud */
    if (temp !== null && wc !== null && temp <= 5 && wc < temp) { feels = wc; feelsKind = "refroidissement éolien"; }
    if (temp !== null && hx !== null && temp >= 20 && hx > temp) { feels = hx; feelsKind = "humidex"; }
    var w = cc.wind || {}, st = cc.station || {}, rs = p.riseSet || {}, pr = cc.pressure || {};
    var dir = String(val(w.direction) || "").toUpperCase();
    var bearing = num(w.bearing);
    if (bearing === null) bearing = dirBearing(dir);
    var slat = coord(txt(st.lat)), slon = coord(txt(st.lon));
    var m = {
      now: now, updated: when(txt(p.lastUpdated)), obs: when(txt(cc.timestamp)),
      temp: temp, feels: feels, feelsKind: feelsKind, cond: say(cc.condition), code: num(cc.iconCode),
      wind: num(w.speed), gust: num(w.gust), dir: dir, bearing: bearing,
      hum: num(cc.relativeHumidity), dew: num(cc.dewpoint), pres: num(pr),
      presTend: txt(pr.tendency), presChange: num(pr.change),
      station: String(val(st) || ""), stationKm: slat !== null && slon !== null ? km(HOME, { lat: slat, lon: slon }) : null,
      rise: when(txt(rs.sunrise)), set: when(txt(rs.sunset)),
      url: txt(p.url) || EC_PAGE
    };
    m.hours = (((p.hourlyForecastGroup || {}).hourlyForecasts) || []).map(function (h) {
      var hw = h.wind || {};
      return { t: when(txt(h.timestamp)), temp: num(h.temperature), code: num(h.iconCode), lop: num(h.lop), cond: say(h.condition),
        wind: num(hw.speed), gust: num(hw.gust) };
    }).filter(function (h) { return h.t && h.t > now - 36e5 && h.temp !== null; }).slice(0, 24);
    if (m.code === null && m.hours.length) m.code = m.hours[0].code;

    /* Sept jours : chaque jour (maximum) avec la nuit qui le suit (minimum), comme meteo.gc.ca */
    var days = [], cur = null;
    (((p.forecastGroup || {}).forecasts) || []).forEach(function (f) {
      var list = (f.temperatures || {}).temperature;
      list = Array.isArray(list) ? list : list ? [list] : [];
      var hi = null, lo = null;
      list.forEach(function (t) { var c = txt(t.class), v = num(t); if (c === "high") hi = v; if (c === "low") lo = v; });
      var ab = f.abbreviatedForecast || {}, cp = txt(f.cloudPrecip);
      var popM = /(\d+)\s*pour cent/.exec(cp);
      var part = {
        name: say((f.period || {}).textForecastName), day: txt(f.period), code: num(ab.icon), cond: say(ab.textSummary),
        text: say(f.textSummary), pop: num(ab.pop) !== null ? num(ab.pop) : popM ? +popM[1] : null,
        uv: f.uv ? num(f.uv.index) : null, uvCat: f.uv ? txt(f.uv.category) : ""
      };
      var night = hi === null && lo !== null;
      if (!night) {
        cur = { label: days.length ? cap(part.day) : "Aujourd’hui", short: days.length ? cap(part.day).slice(0, 3) + "." : "Auj.",
          hi: hi, lo: null, d: part, n: null, today: !days.length };
        days.push(cur);
      } else if (cur && !cur.n) {
        cur.lo = lo; cur.n = part;
      } else {
        cur = { label: "Ce soir", short: "Ce soir", hi: null, lo: lo, d: null, n: part, today: true };
        days.push(cur);
      }
    });
    days.forEach(function (d) {
      var a = d.d || d.n;
      d.code = a.code; d.cond = a.cond;
      d.night = !d.d;
      var pops = [d.d && d.d.pop, d.n && d.n.pop].filter(function (x) { return x !== null && x !== undefined; });
      d.pop = pops.length ? Math.max.apply(null, pops) : null;
    });
    m.days = days.slice(0, 7);
    /* UV : maximum prévu du prochain jour qui en a un */
    m.uv = null;
    for (var i = 0; i < days.length; i++) {
      if (days[i].d && days[i].d.uv !== null) { m.uv = { v: days[i].d.uv, cat: days[i].d.uvCat, when: i === 0 ? "aujourd’hui" : WEEKDAY_FROM(days[i]) }; break; }
    }
    var rn = ((p.forecastGroup || {}).regionalNormals || {}).temperature || [];
    m.normals = {};
    (Array.isArray(rn) ? rn : [rn]).forEach(function (t) { var c = txt(t.class); if (c === "high" || c === "low") m.normals[c] = num(t); });
    m.warnings = (p.warnings || []).map(function (w) {
      return { title: sentence(txt(w.description)), type: txt(w.type), level: txt(w.alertColourLevel), url: txt(w.url), until: when(txt(w.expiryTime)) };
    }).filter(function (w) { return w.title && w.type !== "ended" && (!w.until || w.until > now); });
    return m;
  }
  function WEEKDAY_FROM(day) { return (day.d && day.d.day) || day.label.toLowerCase(); }

  /* Granby (SMC) : dernière mesure horaire */
  function parseSwob(j) {
    var f = (j.features || [])[0];
    if (!f) return null;
    var p = f.properties || {};
    var n = function (k) { var v = parseFloat(p[k]); return isFinite(v) ? v : null; };
    var s = {
      t: when(p["date_tm-value"]), temp: n("air_temp"), mslp: n("mslp"),
      tch: n("pres_tend_char_pst3hrs"), tamt: n("pres_tend_amt_pst3hrs"), r1: n("pcpn_amt_pst1hr"), r24: n("pcpn_amt_pst24hrs")
    };
    if (!s.t || s.temp === null) return null;
    /* Tendance sur 3 h, sinon à partir des mesures précédentes */
    if (s.tch === null || s.tamt === null) {
      var old = (j.features || [])[3];
      var o = old && parseFloat(old.properties.mslp);
      if (isFinite(o) && s.mslp !== null) { s.tamt = Math.abs(s.mslp - o); s.tch = s.mslp - o > .1 ? 2 : s.mslp - o < -.1 ? 7 : 4; }
    }
    return s;
  }

  /* ---------- Couleurs ---------- */
  function mix(a, b, k) { return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]; }
  function rgb(c, a) { return "rgba(" + (c[0] | 0) + "," + (c[1] | 0) + "," + (c[2] | 0) + "," + (a === undefined ? 1 : a) + ")"; }
  /* Températures en tons d'or : bronze profond (froid) → champagne (chaud) */
  var TSCALE = [[-25, [92, 66, 30]], [-10, [138, 99, 38]], [0, [176, 133, 66]], [10, [217, 184, 119]],
    [20, [233, 201, 140]], [30, [246, 224, 176]]];
  function tcol(t) {
    if (t <= TSCALE[0][0]) return TSCALE[0][1];
    for (var i = 1; i < TSCALE.length; i++) {
      if (t <= TSCALE[i][0]) return mix(TSCALE[i - 1][1], TSCALE[i][1], (t - TSCALE[i - 1][0]) / (TSCALE[i][0] - TSCALE[i - 1][0]));
    }
    return TSCALE[TSCALE.length - 1][1];
  }
  /* Ciel noir et or selon l'élévation : [e, haut, milieu, horizon] */
  var PAL = [
    [-1, [4, 3, 2], [8, 6, 4], [19, 14, 9]],
    [-.55, [5, 4, 3], [12, 9, 6], [36, 26, 15]],
    [-.2, [8, 6, 5], [24, 17, 11], [88, 60, 30]],
    [0, [12, 9, 6], [46, 32, 18], [170, 114, 52]],
    [.35, [16, 12, 8], [60, 43, 24], [192, 140, 72]],
    [1, [28, 22, 14], [80, 62, 38], [172, 138, 88]]
  ];
  function palette(e, cover, wet) {
    var a = PAL[0], b = PAL[PAL.length - 1];
    for (var i = 1; i < PAL.length; i++) { if (e <= PAL[i][0]) { a = PAL[i - 1]; b = PAL[i]; break; } }
    var k = b[0] === a[0] ? 0 : c01((e - a[0]) / (b[0] - a[0]));
    var dim = 1 - cover * .16 - (wet ? .16 : 0);
    return [1, 2, 3].map(function (n) {
      var c = mix(a[n], b[n], k), g = .3 * c[0] + .59 * c[1] + .11 * c[2];
      c = mix(c, [g * 1.05, g, g * .9], cover * .7);
      return [c[0] * dim, c[1] * dim, c[2] * dim];
    });
  }

  /* ==========================================================================
     Le ciel animé (canevas)
     ========================================================================== */
  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function Sky(cv, host) {
    this.cv = cv; this.host = host; this.ctx = cv.getContext("2d");
    this.m = null; this.s = { c: .5 }; this.t = 0; this.run = false; this.flash = 0; this.nextFlash = 6;
    this.clouds = []; this.parts = []; this.stars = []; this.sprites = []; this.tinted = []; this.tintKey = "";
    var self = this;
    this.tick = function (ts) { self.loop(ts); };
    var r = rng(11);
    for (var i = 0; i < 7; i++) this.sprites.push(this.sprite(r, 300 + r() * 160));
  }
  /* Un nuage : une base plate de boules serrées, quelques dômes au-dessus, bords nets mais doux */
  Sky.prototype.sprite = function (r, w) {
    var h = Math.round(w * .5), c = document.createElement("canvas");
    c.width = w; c.height = h;
    var x = c.getContext("2d"), puffs = [], i;
    var nb = 10 + Math.floor(r() * 5), base = h * .66;
    for (i = 0; i < nb; i++) {
      var t = (i + .5) / nb, px = w * (.1 + .8 * t) + (r() - .5) * w * .03, edge = 1 - Math.pow(Math.abs(t - .5) * 2, 2) * .6;
      puffs.push([px, base - h * .05 * r(), h * (.1 + .06 * r()) * edge]);
    }
    var nt = 4 + Math.floor(r() * 4);
    for (i = 0; i < nt; i++) {
      var tx = w * (.26 + .48 * r()), lift = 1 - Math.abs(tx / w - .5) * 1.5;
      puffs.push([tx, base - h * (.1 + .16 * r()) * lift, h * (.12 + .09 * r()) * (.6 + .4 * lift)]);
    }
    if ("filter" in x) x.filter = "blur(" + Math.round(h * .04) + "px)";
    puffs.forEach(function (p) {
      var g = x.createRadialGradient(p[0], p[1] - p[2] * .25, p[2] * .1, p[0], p[1], p[2]);
      g.addColorStop(0, "rgba(255,255,255,.9)"); g.addColorStop(.72, "rgba(255,255,255,.62)"); g.addColorStop(1, "rgba(255,255,255,0)");
      x.fillStyle = g;
      x.beginPath(); x.arc(p[0], p[1], p[2], 0, Math.PI * 2); x.fill();
    });
    /* Base aplatie : on efface sous la ligne de base */
    x.filter = "none";
    x.globalCompositeOperation = "destination-out";
    var cut = x.createLinearGradient(0, base + h * .04, 0, base + h * .2);
    cut.addColorStop(0, "rgba(0,0,0,0)"); cut.addColorStop(1, "rgba(0,0,0,1)");
    x.fillStyle = cut; x.fillRect(0, base, w, h - base);
    return c;
  };
  /* Teinte des nuages : éclairés par-dessus, plus sombres dessous */
  Sky.prototype.tint = function (top, bottom) {
    var key = top.map(Math.round).join() + bottom.map(Math.round).join();
    if (key === this.tintKey) return;
    this.tintKey = key;
    this.tinted = this.sprites.map(function (sp) {
      var c = document.createElement("canvas");
      c.width = sp.width; c.height = sp.height;
      var x = c.getContext("2d");
      x.drawImage(sp, 0, 0);
      x.globalCompositeOperation = "source-in";
      var g = x.createLinearGradient(0, 0, 0, sp.height);
      g.addColorStop(0, rgb(top)); g.addColorStop(1, rgb(bottom));
      x.fillStyle = g; x.fillRect(0, 0, sp.width, sp.height);
      return c;
    });
  };
  Sky.prototype.size = function () {
    var r = this.host.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var W = Math.max(1, Math.round(r.width)), H = Math.max(1, Math.round(r.height));
    if (W === this.W && H === this.H) return false;
    this.W = W; this.H = H; this.dpr = dpr;
    this.cv.width = Math.round(W * dpr); this.cv.height = Math.round(H * dpr);
    var mob = W < 700;
    this.hy = Math.round(H * (mob ? .82 : .8));
    this.x0 = mob ? W * .1 : W * .5; this.x1 = mob ? W * .9 : W * .93;
    this.cx = (this.x0 + this.x1) / 2; this.rx = (this.x1 - this.x0) / 2;
    this.ry = mob ? Math.min(H * .34, this.hy - H * .46) : H * .56;
    this.host.style.setProperty("--x0", this.x0.toFixed(0) + "px");
    this.host.style.setProperty("--x1", this.x1.toFixed(0) + "px");
    this.host.style.setProperty("--hy", this.hy + "px");
    this.hills();
    var rs = rng(5), n = Math.min(320, Math.round(W * this.hy / 2600));
    this.stars = [];
    for (var i = 0; i < n; i++) {
      var big = rs() < .06;
      this.stars.push({ x: rs() * W, y: Math.pow(rs(), 1.25) * this.hy * .9, r: big ? 1.1 + rs() * .6 : .45 + rs() * rs() * 1, a: big ? .9 : .3 + rs() * .6, w: .6 + rs() * 1.6, p: rs() * 6.3, big: big });
    }
    this.layout();
    return true;
  };
  Sky.prototype.hills = function () {
    var W = this.W, hy = this.hy, k = Math.min(1.2, this.H / 460) * (.62 + .38 * Math.min(1, W / 1000));
    /* Les collines montérégiennes à l'horizon : Yamaska, Rougemont, Saint-Hilaire */
    var bumps = [[.24, 17, .05], [.47, 13, .045], [.66, 21, .04], [.86, 9, .06]];
    var far = new Path2D(), near = new Path2D();
    far.moveTo(0, this.H); near.moveTo(0, this.H);
    for (var x = 0; x <= W + 6; x += 6) {
      var y = hy - 3 - 2.2 * Math.sin(x / 83) - 1.2 * Math.sin(x / 31);
      bumps.forEach(function (b) { var d = (x - b[0] * W) / Math.max(b[2] * W, 44); y -= b[1] * k * Math.exp(-d * d); });
      far.lineTo(x, y);
      near.lineTo(x, hy + 7 - 1.6 * Math.sin(x / 11) - 1.1 * Math.sin(x / 4.3) - 2.4 * Math.sin(x / 57));
    }
    far.lineTo(W, this.H); near.lineTo(W, this.H);
    far.closePath(); near.closePath();
    this.farP = far; this.nearP = near;
  };
  Sky.prototype.setModel = function (m) {
    this.m = m;
    this.s = m ? sky(m.code) : { c: .8 };
    this.layout();
    this.draw();
  };
  Sky.prototype.layout = function () {
    if (!this.W) return;
    var s = this.s, W = this.W, r = rng(23);
    var n = s.c < .06 ? 0 : Math.round(1 + s.c * 12);
    this.clouds = [];
    for (var i = 0; i < n; i++) {
      var depth = r(), sp = Math.floor(r() * this.sprites.length);
      this.clouds.push({ sp: sp, x: r() * (W + 400) - 200, y: this.H * (.03 + .5 * Math.pow(r(), 1.3)) * (s.c > .85 ? .8 : 1),
        sc: (.5 + depth * .75) * Math.min(1.25, W / 1100 + .25), d: depth, a: .45 + depth * .5 });
    }
    this.clouds.sort(function (a, b) { return a.d - b.d; });
    /* Précipitations : quantité selon l'intensité réelle et la surface */
    var area = W * this.H / (1200 * 460), pr = rng(41);
    this.parts = [];
    var add = function (kind, count) {
      for (var j = 0; j < count; j++) {
        this.parts.push({ k: kind, x: pr() * W, y: pr() * this.H, z: .45 + pr() * .55, p: pr() * 6.3 });
      }
    }.bind(this);
    var I = s.i || 0;
    if (s.p === "rain") add("r", Math.round(230 * I * area));
    if (s.p === "drizzle") add("d", Math.round(300 * I * area));
    if (s.p === "snow") add("s", Math.round(190 * I * area));
    if (s.p === "pellets") add("i", Math.round(160 * I * area));
    if (s.p === "mix") { add("r", Math.round(120 * I * area)); add("s", Math.round(110 * I * area)); }
  };
  Sky.prototype.windX = function () {
    var m = this.m, sp = m && m.wind !== null ? m.wind : 6;
    /* Vue vers le sud : l'est à gauche, l'ouest à droite. Un vent du sud-ouest pousse vers la gauche. */
    var dir = m && m.bearing !== null ? Math.sin(m.bearing * RAD) : -.6;
    if (Math.abs(dir) < .25) dir = dir < 0 ? -.25 : .25;
    return { v: (4 + Math.min(sp, 90) * .5) * dir, slant: dir * Math.min(.55, sp / 70) };
  };
  Sky.prototype.step = function (dt) {
    var W = this.W, H = this.H, w = this.windX();
    this.clouds.forEach(function (c) {
      var spr = this.sprites[c.sp];
      c.x += w.v * (.35 + c.d * .65) * dt;
      var cw = spr.width * c.sc;
      if (w.v < 0 && c.x + cw < -40) c.x = W + 40;
      if (w.v > 0 && c.x > W + 40) c.x = -cw - 40;
    }, this);
    var t = this.t;
    this.parts.forEach(function (p) {
      if (p.k === "s") {
        p.y += (22 + 40 * p.z) * dt; p.x += (w.v * .6 + Math.sin(t * .9 + p.p) * 14 * p.z) * dt;
      } else {
        var v = p.k === "r" ? 640 + 320 * p.z : p.k === "d" ? 380 + 160 * p.z : 420 + 220 * p.z;
        p.y += v * dt; p.x += v * w.slant * dt;
      }
      if (p.y > H + 20) { p.y = -24; p.x = Math.random() * W; }
      if (p.x < -30) p.x += W + 60; else if (p.x > W + 30) p.x -= W + 60;
    });
    if (this.s.t) {
      this.flash = Math.max(0, this.flash - dt * 3.2);
      this.nextFlash -= dt;
      if (this.nextFlash <= 0) { this.flash = 1; this.nextFlash = 5 + Math.random() * 9; }
    }
  };
  Sky.prototype.draw = function () {
    if (!this.W) return;
    var x = this.ctx, W = this.W, H = this.H, hy = this.hy, m = this.m, s = this.s, now = new Date();
    x.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    var e = m ? elevation(m, now) : -.35, cover = s.c, wet = !!s.p;
    var pal = palette(e, cover, wet), top = pal[0], mid = pal[1], bot = pal[2];
    var g = x.createLinearGradient(0, 0, 0, hy);
    g.addColorStop(0, rgb(top)); g.addColorStop(.58, rgb(mid)); g.addColorStop(1, rgb(bot));
    x.fillStyle = g; x.fillRect(0, 0, W, H);

    /* Étoiles : seulement la nuit, et seulement si le ciel est assez dégagé */
    var starA = c01(-e * 1.5 - .25) * Math.pow(1 - cover, 2);
    if (starA > .01) {
      var t = this.t;
      this.stars.forEach(function (st) {
        var a = st.a * starA * (.7 + .3 * Math.sin(t * st.w + st.p));
        if (st.big) {
          var sg = x.createRadialGradient(st.x, st.y, 0, st.x, st.y, st.r * 5);
          sg.addColorStop(0, "rgba(255,226,170," + (a * .5).toFixed(3) + ")"); sg.addColorStop(1, "rgba(255,226,170,0)");
          x.fillStyle = sg; x.fillRect(st.x - st.r * 5, st.y - st.r * 5, st.r * 10, st.r * 10);
        }
        x.fillStyle = "rgba(255,234,196," + a.toFixed(3) + ")";
        x.beginPath(); x.arc(st.x, st.y, st.r, 0, Math.PI * 2); x.fill();
      });
    }
    /* Lueur de la ville la nuit, lueur chaude du soleil près de l'horizon */
    if (e < 0) {
      var cg = x.createLinearGradient(0, hy - 90, 0, hy);
      cg.addColorStop(0, "rgba(233,180,110,0)"); cg.addColorStop(1, "rgba(233,180,110," + (.11 * (1 - cover * .3)).toFixed(3) + ")");
      x.fillStyle = cg; x.fillRect(0, hy - 90, W, 90);
    }
    var sunUp = m && m.rise && m.set && now >= m.rise && now <= m.set;
    var f = sunUp ? (now - m.rise) / (m.set - m.rise) : null;
    var horizonGlow = 1 - Math.min(1, Math.abs(e) / .55);
    if (horizonGlow > 0 && m && m.rise) {
      var gx = sunUp ? this.cx - this.rx * Math.cos(Math.PI * f) : (now < m.rise ? this.x0 : this.x1);
      x.save();
      x.translate(gx, hy); x.scale(1, .32);
      var hg = x.createRadialGradient(0, 0, 0, 0, 0, W * .55);
      hg.addColorStop(0, "rgba(232,170,90," + (.42 * horizonGlow * (1 - cover * .55)).toFixed(3) + ")");
      hg.addColorStop(1, "rgba(232,170,90,0)");
      x.fillStyle = hg; x.fillRect(-W, -H * 3, W * 2, H * 6);
      x.restore();
    }

    /* Trajectoire du soleil : arc pointillé, partie parcourue en or */
    x.save();
    x.lineWidth = 1; x.setLineDash([2, 6]); x.strokeStyle = "rgba(233,201,140,.26)";
    x.beginPath(); x.ellipse(this.cx, hy, this.rx, this.ry, 0, Math.PI, Math.PI * 2); x.stroke();
    x.setLineDash([]);
    if (sunUp) {
      x.strokeStyle = "rgba(233,201,140,.75)"; x.lineWidth = 1.5;
      x.beginPath(); x.ellipse(this.cx, hy, this.rx, this.ry, 0, Math.PI, Math.PI + Math.PI * f); x.stroke();
    }
    x.strokeStyle = "rgba(233,201,140,.2)"; x.lineWidth = 1;
    x.beginPath(); x.moveTo(this.x0 - 24, hy + .5); x.lineTo(this.x1 + 24, hy + .5); x.stroke();
    x.fillStyle = "rgba(233,201,140,.75)";
    [this.x0, this.x1].forEach(function (px) { x.beginPath(); x.arc(px, hy, 2.4, 0, Math.PI * 2); x.fill(); });
    x.restore();

    /* La lune, à sa vraie place et dans sa vraie phase */
    if (m) {
      var mp = moonPos(now);
      if (mp.alt > 0) {
        var noonAlt = this.noonAlt || (this.noonAlt = Math.max(.2, sunPos(sunTimes(now).noon).alt));
        var azR = this.azR || (this.azR = Math.max(.6, Math.abs(sunPos(m.rise || now).az)));
        var mx = Math.max(14, Math.min(W - 14, this.cx + Math.max(-1.3, Math.min(1.3, mp.az / azR)) * this.rx));
        var my = Math.max(18, hy - this.ry * Math.min(1.2, mp.alt / noonAlt));
        var il = moonIllum(now), ma = (e < 0 ? 1 : .4) * (1 - cover * .85);
        if (ma > .03) this.moon(mx, my, W < 700 ? 7.5 : 9, il, ma);
      }
    }
    /* Le soleil, sur l'arc réel entre le lever et le coucher */
    if (sunUp) {
      var sx = this.cx - this.rx * Math.cos(Math.PI * f), sy = hy - this.ry * Math.sin(Math.PI * f);
      var clear = 1 - cover, halo = x.createRadialGradient(sx, sy, 0, sx, sy, 150);
      halo.addColorStop(0, "rgba(240,206,146," + (.34 * (.35 + clear * .65)).toFixed(3) + ")");
      halo.addColorStop(1, "rgba(240,206,146,0)");
      x.fillStyle = halo; x.fillRect(sx - 150, sy - 150, 300, 300);
      var da = Math.pow(clear, 1.3) * .95 + .05;
      var disk = x.createRadialGradient(sx, sy, 0, sx, sy, 15);
      disk.addColorStop(0, "rgba(255,247,226," + da.toFixed(3) + ")"); disk.addColorStop(.55, "rgba(255,236,196," + (da * .95).toFixed(3) + ")");
      disk.addColorStop(1, "rgba(255,228,180,0)");
      x.fillStyle = disk; x.beginPath(); x.arc(sx, sy, 15, 0, Math.PI * 2); x.fill();
    }

    /* Nuages, éclairés selon le moment de la journée */
    var cTop, cBot;
    if (e > .3) { cTop = [216, 202, 178]; cBot = [108, 94, 76]; }
    else if (e > -.3) {
      var gk = c01((e + .3) / .6);
      cTop = mix(mix([56, 47, 38], [222, 172, 112], c01((e + .3) / .3)), [216, 202, 178], c01(e / .3));
      cBot = mix([24, 20, 16], [108, 94, 76], gk);
    }
    else { cTop = [54, 46, 38]; cBot = [20, 17, 14]; }
    if (cover > .85) { cTop = mix(cTop, [150, 142, 130], .35); cBot = mix(cBot, [66, 60, 52], .35); }
    if (wet) { cTop = mix(cTop, cBot, .35); }
    this.tint(cTop, cBot);
    if (cover > .85) {
      var deck = x.createLinearGradient(0, 0, 0, hy * .8);
      deck.addColorStop(0, rgb(cBot, .5)); deck.addColorStop(1, rgb(cBot, 0));
      x.fillStyle = deck; x.fillRect(0, 0, W, hy);
    }
    var tinted = this.tinted;
    this.clouds.forEach(function (c) {
      var sp = tinted[c.sp];
      x.globalAlpha = Math.min(.92, c.a * (.5 + cover * .45));
      x.drawImage(sp, c.x, c.y, sp.width * c.sc, sp.height * c.sc);
    });
    x.globalAlpha = 1;

    /* Brouillard ou brume */
    if (s.f) {
      var fg = x.createLinearGradient(0, hy - 120, 0, hy + 30);
      fg.addColorStop(0, "rgba(204,192,170,0)"); fg.addColorStop(1, "rgba(204,192,170," + (.3 * s.f).toFixed(3) + ")");
      x.fillStyle = fg; x.fillRect(0, hy - 120, W, 150);
    }

    /* Horizon : collines au loin, puis la plaine */
    var hc = mix(bot, [0, 0, 0], .74);
    x.fillStyle = rgb(hc); x.fill(this.farP);
    var ng = x.createLinearGradient(0, hy, 0, H);
    ng.addColorStop(0, "rgb(10,8,6)"); ng.addColorStop(1, "rgb(6,5,4)");
    x.fillStyle = ng; x.fill(this.nearP);

    /* Pluie, bruine, neige, grésil */
    if (this.parts.length) {
      var sl = this.windX().slant;
      x.lineCap = "round";
      [["r", 15, 1, "rgba(236,220,188,.32)"], ["d", 6, .9, "rgba(236,220,188,.24)"]].forEach(function (k) {
        x.strokeStyle = k[3]; x.lineWidth = k[2]; x.beginPath();
        this.parts.forEach(function (p) {
          if (p.k !== k[0]) return;
          var L = k[1] * (.6 + p.z * .7);
          x.moveTo(p.x, p.y); x.lineTo(p.x + sl * L, p.y + L);
        });
        x.stroke();
      }, this);
      x.fillStyle = "rgba(252,246,234,.82)"; x.beginPath();
      this.parts.forEach(function (p) {
        if (p.k !== "s" && p.k !== "i") return;
        var r = p.k === "s" ? .7 + p.z * 1.6 : .9 + p.z * .6;
        x.moveTo(p.x + r, p.y); x.arc(p.x, p.y, r, 0, Math.PI * 2);
      });
      x.fill();
    }
    if (this.flash > 0) {
      var fl = this.flash > .6 ? (this.flash - .6) * 2.5 : this.flash < .3 ? this.flash : .3;
      x.fillStyle = "rgba(255,240,214," + (fl * .22).toFixed(3) + ")"; x.fillRect(0, 0, W, H);
    }
  };
  Sky.prototype.moon = function (cx, cy, r, il, a) {
    var x = this.ctx;
    var halo = x.createRadialGradient(cx, cy, 0, cx, cy, r * 5);
    halo.addColorStop(0, "rgba(240,214,160," + (.18 * a * (.3 + il.fraction)).toFixed(3) + ")");
    halo.addColorStop(1, "rgba(240,214,160,0)");
    x.fillStyle = halo; x.fillRect(cx - r * 5, cy - r * 5, r * 10, r * 10);
    x.fillStyle = "rgba(232,210,166," + (.1 * a).toFixed(3) + ")";
    x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill();
    /* Partie éclairée : un demi-disque et une demi-ellipse (le terminateur) */
    var p = il.phase, k = Math.cos(2 * Math.PI * p), waxing = p < .5;
    x.fillStyle = "rgba(246,228,190," + (.94 * a).toFixed(3) + ")";
    x.beginPath();
    if (waxing) {
      x.arc(cx, cy, r, -Math.PI / 2, Math.PI / 2, false);
      x.ellipse(cx, cy, r * Math.abs(k), r, 0, Math.PI / 2, -Math.PI / 2, k > 0);
    } else {
      x.arc(cx, cy, r, Math.PI / 2, Math.PI * 1.5, false);
      x.ellipse(cx, cy, r * Math.abs(k), r, 0, Math.PI * 1.5, Math.PI / 2, k > 0);
    }
    x.fill();
  };
  Sky.prototype.loop = function (ts) {
    if (!this.run) return;
    var dt = this.last ? Math.min(.05, (ts - this.last) / 1000) : 0;
    this.last = ts; this.t += dt;
    this.step(dt); this.draw();
    this.raf = requestAnimationFrame(this.tick);
  };
  Sky.prototype.start = function () {
    if (reduce) { this.draw(); return; }
    if (this.run) return;
    this.run = true; this.last = 0;
    this.raf = requestAnimationFrame(this.tick);
  };
  Sky.prototype.stop = function () { this.run = false; cancelAnimationFrame(this.raf); };

  /* ==========================================================================
     Chaque démo de la page
     ========================================================================== */
  roots.forEach(function (root) {
    var $ = function (s) { return root.querySelector('[data-mt="' + s + '"]'); };
    var hero = $("hero"), cv = $("sky");
    var skyR = cv && cv.getContext ? new Sky(cv, hero) : null;
    var model = null, stn = null, lastOk = 0, visible = false, heroVisible = false, shownTemp = null, timer = null;
    var cards = [].slice.call(root.querySelectorAll(".mt-card, .mt-tiles, .mt-rules"));

    function set(k, v) { var el = $(k); if (el) el.textContent = v; }
    function html(k, v) { var el = $(k); if (el) el.innerHTML = v; }

    /* ---------- Chargement (cache de session partagé avec wow.js : « jarvis-ec ») ---------- */
    function cached(key) {
      try { var c = JSON.parse(sessionStorage.getItem(key)); if (c && Date.now() - c.t < FRESH) return c.j; } catch (e) {}
      return null;
    }
    function getJSON(url, key) {
      var c = cached(key);
      if (c) return Promise.resolve(c);
      return fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (j) {
        try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), j: j })); } catch (e) {}
        return j;
      });
    }
    function load() {
      clearTimeout(timer);
      getJSON(EC_URL, "jarvis-ec").then(function (j) {
        var m = parse(j);
        if (m.temp === null && !m.cond) throw new Error("vide");
        lastOk = Date.now();
        model = m;
        root.removeAttribute("data-state");
        root.setAttribute("data-ready", "");
        paint();
        getJSON(SWOB_URL, "jarvis-swob").then(function (sj) { stn = parseSwob(sj); paintStation(); paintTiles(); }).catch(function () { stn = null; paintStation(); });
      }).catch(function () {
        if (!model) fail();
        timer = setTimeout(function () { if (visible && !document.hidden) load(); }, RETRY);
      });
    }

    /* ---------- État indisponible : honnête, jamais de chiffres inventés ---------- */
    function fail() {
      root.setAttribute("data-state", "off");
      state(false, "Données indisponibles");
      set("temp", "—"); set("dec", ""); set("daypart", "");
      $("temp-box").setAttribute("aria-label", "Température indisponible");
      set("cond", "Données météo indisponibles");
      set("hilo", "Environnement Canada ne répond pas pour l’instant.");
      set("feels", "JARVIS préfère le dire plutôt que d’inventer. Nouvel essai dans 2" + NB + "minutes.");
      set("obs", ""); set("arc-rise", ""); set("arc-set", "");
      $("noalert").hidden = true;
      html("hours", '<p class="mt-wait">Les prévisions horaires s’afficheront dès que la source répondra.</p>');
      html("days", '<li class="mt-wait">Les prévisions de la semaine s’afficheront dès que la source répondra.</li>');
      html("rules", '<li class="mt-rule is-info"><p class="mt-rule-k">État</p><b>Aucune décision sans données fiables</b><p>Les règles reprendront dès que la météo réelle sera de retour.</p></li>');
      if (skyR) skyR.setModel(null);
    }
    /* Pastille d'état ; le préfixe se cache sur cellulaire pour garder une seule ligne */
    function state(ok, label, prefix) {
      var el = $("state");
      el.classList.toggle("is-off", !ok);
      el.innerHTML = '<i class="dot' + (ok ? "" : " is-off") + '" aria-hidden="true"></i><span><span class="mt-st-p"></span><span></span></span>';
      el.querySelector(".mt-st-p").textContent = prefix || "";
      el.querySelector(".mt-st-p + span").textContent = label;
      el.setAttribute("title", (prefix || "") + label);
    }

    /* ---------- Rendu complet ---------- */
    function paint() {
      var m = model;
      m.now = new Date();
      var old = m.updated && Date.now() - m.updated > 3 * 36e5;
      if (m.updated) state(!old, hm(m.updated), old ? "Données de " : "Mis à jour à ");
      else state(true, "En direct");
      paintAlerts(); paintNow(); paintHours(); paintDays(); paintTiles(); paintRules(); paintSource();
      if (skyR) { skyR.size(); skyR.setModel(m); }
    }

    function paintAlerts() {
      var box = $("alerts"), w = model.warnings;
      $("noalert").hidden = !!w.length;
      if (!w.length) { box.hidden = true; box.innerHTML = ""; return; }
      box.hidden = false;
      box.innerHTML = w.slice(0, 3).map(function (a) {
        var lvl = /^(yellow|orange|red)$/.test(a.level) ? a.level : "info";
        return '<p class="mt-alert is-' + lvl + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5 21.5 20h-19z"/><path d="M12 10v4.5M12 17.2v.1"/></svg>' +
          "<b>" + esc(a.title) + "</b>" + (a.until ? "<span>Jusqu’à " + at(a.until, model.now, true) + "</span>" : "") +
          (a.url ? '<a href="' + esc(a.url) + '" target="_blank" rel="noopener">Détails<span class="sr"> de l’alerte sur meteo.gc.ca</span> ↗</a>' : "") + "</p>";
      }).join("");
    }

    function paintNow() {
      var m = model, now = m.now;
      var e = elevation(m, now), part = "";
      if (m.rise && m.set) {
        if (now < m.rise) part = m.rise - now < 45 * 6e4 ? "Aube" : "Nuit";
        else if (now <= m.set) part = now - m.rise < 60 * 6e4 ? "Lever du jour" : m.set - now < 60 * 6e4 ? "Heure dorée" : "Jour";
        else part = now - m.set < 45 * 6e4 ? "Crépuscule" : "Nuit";
      }
      set("daypart", part ? " · " + part : "");
      root.style.setProperty("--mt-e", e.toFixed(2));
      if (m.temp !== null) {
        $("temp-box").setAttribute("aria-label", dec1(m.temp) + " degrés Celsius");
        if (heroVisible) countTemp();
        else if (shownTemp === null) { set("temp", "—"); set("dec", ""); }
      }
      set("cond", m.cond || "Conditions actuelles");
      var d0 = m.days[0], hl = [];
      if (d0) {
        if (d0.hi !== null) hl.push("Max " + int(d0.hi) + "°");
        if (d0.lo !== null) hl.push((d0.hi === null ? "Min " + int(d0.lo) + "° cette nuit" : "Min " + int(d0.lo) + "°"));
      }
      set("hilo", hl.join("  ·  "));
      set("feels", m.feels !== null ? "Ressenti " + int(m.feels) + NB + "°C · " + m.feelsKind : "");
      var obs = [];
      if (m.obs) obs.push("Mesure de " + hm(m.obs));
      if (m.station) obs.push(m.station + (m.stationKm !== null ? ", à " + Math.round(m.stationKm) + NB + "km" : ""));
      set("obs", obs.join(" · "));
      set("arc-rise", m.rise ? "Lever " + hm(m.rise) : "");
      set("arc-set", m.set ? "Coucher " + hm(m.set) : "");
    }
    function countTemp() {
      var to = model.temp, from = shownTemp === null ? (to < 0 ? 0 : Math.max(0, to - 14)) : shownTemp;
      shownTemp = to;
      var el = $("temp"), dc = $("dec");
      var show = function (v) {
        var r = Math.round(v * 10) / 10, a = Math.abs(r), i = Math.floor(a + 1e-9), d = Math.round((a - i) * 10);
        if (d === 10) { i++; d = 0; }
        el.textContent = (r < 0 && (i || d) ? MINUS : "") + i;
        dc.textContent = "," + d;
      };
      if (reduce || from === to) { show(to); return; }
      var t0 = performance.now();
      (function f(t) {
        var k = Math.min(1, (t - t0) / 1400), ease = 1 - Math.pow(1 - k, 4);
        show(from + (to - from) * ease);
        if (k < 1) requestAnimationFrame(f);
      })(t0);
    }

    /* ---------- 24 heures : courbe, pictogrammes, probabilité de précipitations ---------- */
    var hoursW = 0;
    function paintHours() {
      var box = $("hours"), m = model, hs = m.hours;
      if (!hs.length) { box.innerHTML = '<p class="mt-wait">Aucune prévision horaire reçue.</p>'; set("h24-sum", ""); return; }
      var avail = box.clientWidth || 900, n = hs.length;
      hoursW = avail;
      var step = Math.max(46, avail / n), W = Math.round(step * n), H = 204;
      var cT = 96, cB = 150, pB = 180, pMax = 22;
      var temps = hs.map(function (h) { return h.temp; });
      var lo = Math.min.apply(null, temps), hi = Math.max.apply(null, temps);
      if (hi - lo < 4) { var pad = (4 - (hi - lo)) / 2; lo -= pad; hi += pad; }
      var X = function (i) { return step * (i + .5); };
      var Y = function (t) { return cB - (t - lo) / (hi - lo) * (cB - cT); };
      var t0 = hs[0].t.getTime();
      var XT = function (t) { return X(0) + (t - t0) / 36e5 * step; };
      var pts = hs.map(function (h, i) { return [X(i), Y(h.temp)]; });
      var line = monotone(pts);
      var s = '<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc(sum24(m)) + '">';
      s += "<defs>" + gradH("mtg", hs) + '<linearGradient id="mtf" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>';
      /* Bandes de jour (soleil levé) et repères de lever / coucher */
      var ev = sunEvents(m), tEnd = t0 + (n - 1) * 36e5, x0 = 0, x1 = W;
      for (var k = 0; k < ev.length; k++) {
        if (!ev[k].up) continue;
        var setE = ev[k + 1];
        if (!setE) break;
        var a = Math.max(x0, XT(ev[k].t)), b = Math.min(x1, XT(setE.t));
        if (b > a) s += '<rect class="c-day" x="' + a.toFixed(1) + '" y="58" width="' + (b - a).toFixed(1) + '" height="125" rx="6"/>';
      }
      ev.forEach(function (e) {
        var ex = XT(e.t);
        if (e.t < t0 - 18e5 || e.t > tEnd + 18e5 || ex < 6 || ex > W - 6) return;
        var label = (e.up ? "Lever" : "Coucher") + (e.ec ? " " + hm(e.t) : "");
        var right = ex > W - 120;
        s += '<line class="c-ev" x1="' + ex.toFixed(1) + '" x2="' + ex.toFixed(1) + '" y1="58" y2="183"/>' +
          '<text class="c-evt" x="' + (ex + (right ? -6 : 6)).toFixed(1) + '" y="72"' + (right ? ' text-anchor="end"' : "") + ">" + label + "</text>";
      });
      s += '<path class="c-area" d="' + line + "L" + pts[n - 1][0].toFixed(1) + " " + (cB + 18) + "L" + pts[0][0].toFixed(1) + " " + (cB + 18) + 'Z" fill="url(#mtf)"/>';
      s += '<line class="c-base" x1="' + (step * .2).toFixed(1) + '" x2="' + (W - step * .2).toFixed(1) + '" y1="' + (pB + .5) + '" y2="' + (pB + .5) + '"/>';
      s += '<path class="c-line" d="' + line + '" pathLength="1" stroke="url(#mtg)"/>';
      hs.forEach(function (h, i) {
        var x = X(i), isMid = +fmtParts(h.t).hour === 0;
        var lab = isMid ? cap(WEEKDAY(h.t)).slice(0, 3) + "." : hh(h.t);
        s += '<g class="c-col" style="--i:' + i + '">';
        s += '<text class="c-h' + (isMid ? " is-day" : "") + '" x="' + x.toFixed(1) + '" y="17">' + lab + "</text>";
        s += '<g transform="translate(' + (x - 11).toFixed(1) + ' 27) scale(.9167)">' + iconInner(h.code, nightCode(h.code, h.t, m)) + "</g>";
        s += '<text class="c-t" x="' + x.toFixed(1) + '" y="' + (pts[i][1] - 10).toFixed(1) + '">' + int(h.temp) + "°</text>";
        var lop = h.lop || 0, bh = Math.max(3, lop / 100 * pMax);
        if (lop) s += '<rect class="c-pop" x="' + (x - step * .19).toFixed(1) + '" y="' + (pB - bh).toFixed(1) + '" width="' + (step * .38).toFixed(1) + '" height="' + bh.toFixed(1) + '" rx="2" style="--o:' + (.45 + lop / 100 * .5).toFixed(2) + '"/>';
        if (lop) s += '<text class="c-p" x="' + x.toFixed(1) + '" y="198">' + lop + NB + "%</text>";
        s += "<title>" + esc(hh(h.t) + " : " + int(h.temp) + " °C, " + (h.cond || "").toLowerCase() + ", précipitations " + lop + " %") + "</title></g>";
      });
      /* Maintenant : point sur la courbe */
      var nx = XT(m.now.getTime());
      if (nx >= 6 && nx <= W - 6) {
        var i0 = Math.max(0, Math.min(n - 2, Math.floor((m.now - t0) / 36e5))), fr = c01((m.now - hs[i0].t) / 36e5);
        var ny = Y(hs[i0].temp + (hs[i0 + 1].temp - hs[i0].temp) * fr);
        s += '<circle class="c-now" cx="' + nx.toFixed(1) + '" cy="' + ny.toFixed(1) + '" r="4"/>';
      }
      s += "</svg>";
      box.innerHTML = s;
      set("h24-sum", sum24(m));
    }
    function iconInner(code, night) { var f = ICONS[sky(code).k] || ICONS.cloud; return '<g class="mt-ico">' + f(night) + "</g>"; }
    function gradH(id, hs) {
      var n = hs.length;
      return '<linearGradient id="' + id + '" x1="0" x2="1" y1="0" y2="0">' + hs.map(function (h, i) {
        return '<stop offset="' + (n > 1 ? i / (n - 1) : 0).toFixed(3) + '" stop-color="' + rgb(tcol(h.temp)) + '"/>';
      }).join("") + "</linearGradient>";
    }
    /* Courbe monotone (Fritsch-Carlson) : pas de bosses inventées entre deux heures égales */
    function monotone(p) {
      var n = p.length, d = [], ms = [];
      if (n < 2) return "M" + p[0][0] + " " + p[0][1];
      for (var i = 0; i < n - 1; i++) d.push((p[i + 1][1] - p[i][1]) / (p[i + 1][0] - p[i][0]));
      ms[0] = d[0]; ms[n - 1] = d[n - 2];
      for (i = 1; i < n - 1; i++) ms[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
      for (i = 0; i < n - 1; i++) {
        if (d[i] === 0) { ms[i] = 0; ms[i + 1] = 0; continue; }
        var a = ms[i] / d[i], b = ms[i + 1] / d[i], q = a * a + b * b;
        if (q > 9) { var tq = 3 / Math.sqrt(q); ms[i] = tq * a * d[i]; ms[i + 1] = tq * b * d[i]; }
      }
      var s = "M" + p[0][0].toFixed(1) + " " + p[0][1].toFixed(1);
      for (i = 0; i < n - 1; i++) {
        var h = (p[i + 1][0] - p[i][0]) / 3;
        s += "C" + (p[i][0] + h).toFixed(1) + " " + (p[i][1] + ms[i] * h).toFixed(1) + " " + (p[i + 1][0] - h).toFixed(1) + " " +
          (p[i + 1][1] - ms[i + 1] * h).toFixed(1) + " " + p[i + 1][0].toFixed(1) + " " + p[i + 1][1].toFixed(1);
      }
      return s;
    }
    /* Résumé des 24 h tiré des vraies prévisions horaires */
    function sum24(m) {
      var hs = m.hours, hi = hs[0], lo = hs[0], wet = null;
      hs.forEach(function (h) { if (h.temp > hi.temp) hi = h; if (h.temp < lo.temp) lo = h; if (!wet && h.lop >= 30) wet = h; });
      var out = "Maximum " + int(hi.temp) + NB + "°C vers " + at(hi.t, m.now) + ", minimum " + int(lo.temp) + NB + "°C vers " + at(lo.t, m.now);
      if (wet) {
        var kind = wetKind(wet.code), word = kind === "snow" ? "neige" : kind === "ice" ? "verglas" : "précipitations";
        out += " · " + word + " possibles dès " + at(wet.t, m.now) + " (" + wet.lop + NB + "%)";
      } else out += " · pas de précipitations prévues";
      return out + ".";
    }

    /* ---------- 7 jours : barres min-max, à la manière d'Apple ---------- */
    function paintDays() {
      var m = model, ds = m.days, box = $("days");
      if (!ds.length) { box.innerHTML = '<li class="mt-wait">Aucune prévision reçue.</li>'; return; }
      var all = [];
      ds.forEach(function (d) { if (d.hi !== null) all.push(d.hi); if (d.lo !== null) all.push(d.lo); });
      if (m.temp !== null) all.push(m.temp);
      var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), span = Math.max(1, hi - lo);
      var P = function (t) { return ((t - lo) / span * 100).toFixed(1); };
      box.innerHTML = ds.map(function (d, i) {
        var a = d.lo !== null ? d.lo : d.hi, b = d.hi !== null ? d.hi : d.lo;
        if (d.today && m.temp !== null) { a = Math.min(a, m.temp); b = Math.max(b, m.temp); }
        var bar = '<i style="left:' + P(a) + "%;right:" + (100 - P(b)) + "%;background:linear-gradient(90deg," + rgb(tcol(a)) + "," + rgb(tcol(b)) + ')"></i>';
        if (d.today && m.temp !== null) bar += '<em style="left:' + P(m.temp) + '%" title="Maintenant"></em>';
        var txts = [];
        if (d.d && d.d.text) txts.push("<p><b>" + esc(d.d.name || d.label) + "</b> " + esc(d.d.text) + "</p>");
        if (d.n && d.n.text) txts.push("<p><b>" + esc(d.n.name) + "</b> " + esc(d.n.text) + "</p>");
        return '<li style="--i:' + i + '"><details><summary>' +
          '<span class="d-name"><span class="d-long">' + esc(d.label) + '</span><span class="d-short" aria-hidden="true">' + esc(d.short) + "</span></span>" +
          '<span class="d-ico" title="' + esc(d.cond) + '">' + iconSvg(d.code, d.night) + '<span class="sr">' + esc(d.cond) + "</span></span>" +
          '<span class="d-pop">' + (d.pop ? d.pop + NB + "%" : "") + "</span>" +
          '<span class="d-lo"><span class="sr">Minimum </span>' + (d.lo !== null ? int(d.lo) + "°" : "—") + "</span>" +
          '<span class="d-bar" aria-hidden="true">' + bar + "</span>" +
          '<span class="d-hi"><span class="sr">Maximum </span>' + (d.hi !== null ? int(d.hi) + "°" : "—") + "</span>" +
          '<span class="d-more" aria-hidden="true"></span>' +
          '</summary><div class="d-txt">' + txts.join("") + "</div></details></li>";
      }).join("");
      var nm = m.normals;
      set("normals", nm.high !== undefined && nm.low !== undefined ? "Normales de saison : " + int(nm.high) + "° / " + int(nm.low) + "°" : "");
    }

    /* ---------- Tuiles de détail ---------- */
    function paintTiles() {
      var m = model;
      if (!m) return;
      /* Vent : l'aiguille pointe là où va le vent */
      set("wind", m.wind !== null ? Math.round(m.wind) : "—");
      var wt = [];
      if (m.wind === 0) wt.push("Calme");
      else if (m.dir) wt.push(dirPhrase(m.dir));
      if (m.gust) wt.push("rafales " + Math.round(m.gust) + NB + "km/h");
      set("wind-txt", wt.join(" · ") || "Direction non mesurée");
      var nd = $("needle");
      if (nd) {
        nd.style.setProperty("--b", ((m.bearing !== null ? m.bearing : 0) + 180) + "deg");
        nd.classList.toggle("is-calm", m.bearing === null || m.wind === 0);
        nd.style.setProperty("--g", m.gust && m.wind ? Math.min(6, (m.gust - m.wind) / 6).toFixed(1) + "deg" : "1deg");
      }
      /* Humidité et point de rosée */
      set("hum", m.hum !== null ? Math.round(m.hum) : "—");
      $("hum-bar").style.setProperty("--v", m.hum !== null ? (m.hum / 100).toFixed(3) : 0);
      set("dew", m.dew !== null ? "Point de rosée " + dec1(m.dew) + NB + "°C" : "Point de rosée non mesuré");
      /* Pression, avec tendance (EC si fournie, sinon station de Granby) */
      set("pres", m.pres !== null ? dec1(m.pres) : "—");
      $("pres-mark").style.setProperty("--p", m.pres !== null ? c01((m.pres - 97) / 8).toFixed(3) : .5);
      var pt = "";
      if (m.presTend) pt = cap(m.presTend) + (m.presChange !== null ? " · " + dec1(m.presChange) + NB + "kPa" : "");
      else if (stn && stn.tch !== null) {
        var up = stn.tch <= 3, flat = stn.tch === 4 || (stn.tamt !== null && stn.tamt < .3);
        pt = (flat ? "Stable" : up ? "En hausse" : "En baisse") + (stn.tamt !== null && !flat ? " de " + dec2(stn.tamt / 10) + NB + "kPa" : "") + " en 3" + NB + "h (Granby)";
      } else pt = "Au niveau de la mer";
      set("pres-txt", pt);
      $("pres-mark").parentNode.classList.toggle("is-up", /hausse/i.test(pt));
      /* Indice UV : maximum prévu par EC */
      if (m.uv) {
        set("uv", Math.round(m.uv.v)); set("uv-cat", NB + cap(m.uv.cat));
        $("uv-mark").style.setProperty("--p", c01(m.uv.v / 11).toFixed(3));
        set("uv-txt", "Maximum prévu " + m.uv.when);
      } else { set("uv", "—"); set("uv-cat", ""); set("uv-txt", "Aucune prévision d’UV"); }
      /* Soleil et lune */
      var now = new Date();
      if (m.rise && m.set) {
        var dayLen = m.set - m.rise, k, big, note, bar;
        if (now < m.rise) { k = "Lever du soleil"; big = hm(m.rise); note = "Dans " + within(m.rise - now); bar = 0; }
        else if (now <= m.set) { k = "Coucher du soleil"; big = hm(m.set); note = "Dans " + within(m.set - now) + " · levé à " + hm(m.rise); bar = (now - m.rise) / dayLen; }
        else {
          k = "Coucher du soleil"; big = hm(m.set);
          note = "Il y a " + within(now - m.set) + " · lever demain vers " + hm(sunTimes(new Date(m.rise.getTime() + DAY + 5 * 36e5)).rise);
          bar = 1;
        }
        set("sun-k", k); set("sun-next", big);
        set("sun-txt", note + " · jour de " + dur(dayLen));
        $("sun-bar").style.setProperty("--v", c01(bar).toFixed(3));
      }
      var il = moonIllum(now);
      set("moon-txt", "Lune : " + moonName(il.phase).toLowerCase() + ", éclairée à " + Math.round(il.fraction * 100) + NB + "%");
    }
    function dec2(n) { return (Math.round(n * 100) / 100).toFixed(2).replace(".", ","); }
    function paintStation() {
      if (!stn) {
        set("stn-temp", "—"); set("stn-rain", "Mesures indisponibles pour l’instant");
        set("stn-txt", STN.name + " · à " + Math.round(km(HOME, STN)) + NB + "km");
        return;
      }
      set("stn-temp", dec1(stn.temp));
      var r = [];
      if (stn.r1 !== null) r.push(dec1(stn.r1) + NB + "mm en 1" + NB + "h");
      if (stn.r24 !== null) r.push(dec1(stn.r24) + NB + "mm en 24" + NB + "h");
      set("stn-rain", r.length ? "Précipitations : " + r.join(" · ") : "Précipitations non mesurées");
      var age = Date.now() - stn.t;
      set("stn-txt", STN.name + " · à " + Math.round(km(HOME, STN)) + NB + "km · " + (age > 3 * 36e5 ? "dernière mesure à " : "mesure de ") + hm(stn.t));
    }

    /* ---------- Ce que JARVIS ferait (évalué sur les vraies données) ---------- */
    function buildRules(m) {
      var out = [], now = m.now, s = sky(m.code), night = m.rise && m.set ? (now < m.rise || now > m.set) : null;
      var tonight = null;
      m.days.forEach(function (d) { if (tonight === null && d.lo !== null) tonight = d.lo; });
      if (m.rise && m.set) {
        var on = new Date(m.set.getTime() - (s.c >= .85 ? 30 : 15) * 6e4);
        if (night && now < m.rise) {
          out.push(m.rise - now < 75 * 6e4
            ? { kind: "auto", cat: "Éclairage", title: "Éteindre l’extérieur au lever du soleil, à " + hm(m.rise), why: "Il fait encore nuit : veilleuse à 20" + NB + "% jusqu’au lever, dans " + within(m.rise - now) + ".", st: "Automatique" }
            : { kind: "auto", cat: "Éclairage", title: "Éclairage extérieur en veilleuse (20" + NB + "%)", why: "Il fait nuit jusqu’au lever du soleil, à " + hm(m.rise) + ". Retour à 0" + NB + "% à ce moment.", st: "Automatique" });
        } else if (night) {
          out.push({ kind: "auto", cat: "Éclairage", title: "Éclairage extérieur en veilleuse (20" + NB + "%)", why: "Nuit depuis le coucher du soleil, à " + hm(m.set) + ". Passage à 0" + NB + "% au lever.", st: "Automatique" });
        } else if (m.set - now < 90 * 6e4) {
          out.push({ kind: "auto", cat: "Éclairage", title: "Allumer l’extérieur à " + hm(on), why: "Coucher du soleil à " + hm(m.set) + (s.c >= .85 ? ", ciel couvert : 30 min plus tôt." : ". La règle est permise : elle s’applique seule."), st: "Automatique" });
        } else if (s.c >= .85) {
          out.push({ kind: "auto", cat: "Éclairage", title: "Lumière d’appoint à 40" + NB + "% dans les pièces occupées", why: "Ciel « " + (m.cond || "couvert").toLowerCase() + " » en plein jour. Retour à 0" + NB + "% s’il s’éclaircit.", st: "Automatique" });
        } else {
          out.push({ kind: "info", cat: "Éclairage", title: "Éclairage extérieur éteint", why: "Lumière du jour jusqu’à " + hm(m.set) + ". Allumage prévu à " + hm(on) + ".", st: "Rien à faire" });
        }
      }
      if (m.temp !== null) {
        var feel = m.feels !== null ? m.feels : m.temp;
        if (feel <= -5) {
          out.push({ kind: "ask", cat: "Confort", title: "Préchauffer le véhicule à 7" + NB + "h" + NB + "15", why: "Ressenti de " + int(feel) + NB + "°C. Départ habituel à 7" + NB + "h" + NB + "30 (exemple).", st: "Votre accord" });
        } else if (m.temp >= 26) {
          out.push({ kind: "ask", cat: "Confort", title: "Fermer les stores côté sud", why: "Il fait " + int(m.temp) + NB + "°C dehors" + (m.feelsKind === "humidex" ? " (humidex " + int(m.feels) + ")" : "") + ". Garder la fraîcheur sans climatiser plus.", st: "Votre accord" });
        } else if (m.temp < 14 || (tonight !== null && tonight < 10)) {
          out.push({ kind: "auto", cat: "Confort", title: night ? "Chauffage de nuit : 18" + NB + "°C dans les chambres" : "Garder 21" + NB + "°C dans les pièces occupées",
            why: "Dehors " + dec1(m.temp) + NB + "°C" + (tonight !== null ? ", minimum prévu " + int(tonight) + NB + "°C" : "") + (m.hum !== null ? ", humidité " + Math.round(m.hum) + NB + "%" : "") + ".", st: "Automatique" });
        } else {
          out.push({ kind: "info", cat: "Confort", title: "Chauffage au minimum", why: "Dehors " + dec1(m.temp) + NB + "°C : aucune correction nécessaire.", st: "Rien à faire" });
        }
      }
      var horizon = now.getTime() + 18 * 36e5, wet = null, gusty = null;
      m.hours.forEach(function (h) {
        if (h.t > horizon) return;
        if (!wet && h.lop !== null && h.lop >= 40) wet = h;
        if (!gusty && h.gust !== null && h.gust >= 50) gusty = h;
      });
      if (m.warnings.length) {
        var w0 = m.warnings[0];
        out.push({ kind: "ask", cat: "Alerte", title: "Prévenir la famille : " + w0.title.toLowerCase(), why: "Alerte d’Environnement Canada" + (w0.until ? " en vigueur jusqu’à " + at(w0.until, now, true) : " en vigueur") + ".", st: "Votre accord" });
      } else if ((m.gust !== null && m.gust >= 50) || gusty) {
        out.push({ kind: "ask", cat: "Météo", title: "Rentrer l’auvent et le mobilier extérieur", why: m.gust >= 50 ? "Rafales de " + Math.round(m.gust) + NB + "km/h mesurées." : "Rafales de " + Math.round(gusty.gust) + NB + "km/h prévues vers " + at(gusty.t, now) + ".", st: "Votre accord" });
      } else if (wet) {
        var kind = wetKind(wet.code) || (wet.temp <= 1 ? "ice" : "rain");
        var titles = { snow: "Prévoir le déneigement de l’entrée", ice: "Déglacer l’entrée avant " + at(wet.t, now), rain: "Rentrer les coussins avant " + at(wet.t, now) };
        var words = { snow: "Neige", ice: "Verglas possible", rain: "Précipitations" };
        out.push({ kind: "ask", cat: "Météo", title: titles[kind], why: words[kind] + " à " + wet.lop + NB + "% vers " + at(wet.t, now) + " (" + (wet.cond || "prévision horaire").toLowerCase() + ").", st: "Votre accord" });
      } else {
        out.push({ kind: "info", cat: "Météo", title: "Aucune action météo nécessaire", why: "Pas de précipitations significatives prévues d’ici 18" + NB + "heures.", st: "Rien à faire" });
      }
      if (night) {
        out.push({ kind: "auto", cat: "Sécurité", title: "Mode nuit : portes verrouillées, caméras en détection", why: "Les événements sont regroupés en une chronologie au lieu de dix notifications.", st: "Automatique" });
      } else if (s.c <= .45 && !s.p) {
        out.push({ kind: "ask", cat: "Énergie", title: "Lancer le lave-vaisselle vers midi", why: "Ciel « " + (m.cond || "dégagé").toLowerCase() + " » : la production solaire couvre la charge" + (m.uv ? ", UV " + Math.round(m.uv.v) + " prévu" : "") + ".", st: "Votre accord" });
      } else {
        out.push({ kind: "auto", cat: "Énergie", title: "Batteries : garder 30" + NB + "% en réserve", why: "Ciel « " + (m.cond || "nuageux").toLowerCase() + " » : peu de production solaire attendue.", st: "Automatique" });
      }
      return out.slice(0, 4);
    }
    function paintRules() {
      var ul = $("rules"), rules = buildRules(model);
      ul.innerHTML = "";
      rules.forEach(function (r, i) {
        var li = document.createElement("li");
        li.className = "mt-rule is-" + r.kind;
        li.style.setProperty("--i", i);
        li.innerHTML = '<div class="mt-rule-top"><p class="mt-rule-k"></p><span class="mt-st"></span></div><b></b><p class="mt-why"></p>';
        li.querySelector(".mt-rule-k").textContent = r.cat;
        li.querySelector(".mt-st").textContent = r.st;
        li.querySelector("b").textContent = r.title;
        li.querySelector(".mt-why").textContent = r.why;
        if (r.kind === "ask") {
          var acts = document.createElement("div");
          acts.className = "mt-acts";
          acts.innerHTML = '<button type="button" data-act="ok">Approuver</button><button type="button" data-act="no">Ignorer</button>';
          acts.addEventListener("click", function (e) {
            var b = e.target.closest("button");
            if (!b) return;
            var ok = b.getAttribute("data-act") === "ok";
            li.className = "mt-rule " + (ok ? "is-done" : "is-skip");
            li.querySelector(".mt-st").textContent = ok ? "Approuvé · simulé" : "Ignoré";
            acts.remove();
          });
          li.appendChild(acts);
        }
        ul.appendChild(li);
      });
    }
    function paintSource() {
      var m = model;
      $("src").innerHTML = 'Source : Environnement et Changement climatique Canada · <a href="' + esc(m.url) + '" target="_blank" rel="noopener">prévisions de Saint-Hyacinthe</a>' +
        " · mesures : " + esc(m.station || "station d’EC") + " et station de Granby (SMC) · lune : calcul astronomique · " +
        '<a href="' + LICENCE + '" target="_blank" rel="noopener">Licence du gouvernement ouvert – Canada</a>';
    }

    /* ---------- Visibilité : animer et rafraîchir seulement à l'écran ---------- */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          visible = e.isIntersecting;
          if (visible && (!lastOk || Date.now() - lastOk > REFRESH)) load();
        });
      }, { rootMargin: "300px 0px" }).observe(root);
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          heroVisible = e.isIntersecting;
          if (!skyR) return;
          if (heroVisible && !document.hidden) { skyR.size(); skyR.start(); if (model && model.temp !== null && shownTemp !== model.temp) countTemp(); }
          else skyR.stop();
        });
      }, { threshold: .05 }).observe(hero);
      var cio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); cio.unobserve(e.target); } });
      }, { threshold: .25 });
      cards.forEach(function (c) { cio.observe(c); });
    } else {
      visible = heroVisible = true;
      cards.forEach(function (c) { c.classList.add("is-in"); });
      load();
      if (skyR) { skyR.size(); skyR.start(); }
    }
    document.addEventListener("visibilitychange", function () {
      if (!skyR) return;
      if (document.hidden) skyR.stop();
      else if (heroVisible) skyR.start();
    });
    /* Rafraîchir toutes les 10 minutes (visible seulement) ; l'heure du ciel avance chaque minute */
    setInterval(function () {
      if (!visible || document.hidden) return;
      if (Date.now() - lastOk > REFRESH) load();
      else if (model) { model.now = new Date(); paintNow(); paintTiles(); if (reduce && skyR) skyR.draw(); }
    }, 60000);
    var rz = null;
    var onResize = function () {
      clearTimeout(rz);
      rz = setTimeout(function () {
        if (skyR && skyR.size()) { skyR.layout(); skyR.draw(); }
        var box = $("hours");
        if (model && box && Math.abs(box.clientWidth - hoursW) > 8) paintHours();
      }, 120);
    };
    if ("ResizeObserver" in window) new ResizeObserver(onResize).observe(root);
    else addEventListener("resize", onResize);
  });
})();
