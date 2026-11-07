/* Module « Éclairage » des Environnements intelligents — dossier « JARVIS accueil lumières » (13 pages).
   Huit environnements (VR, maison, chalet, entreprise, garage, ferme, bateau, avion), un seul moteur.
   Le contrat « Conserver sans perdre » (page 13) est appliqué ici, et le site sert de cahier des charges :
     01 un style n'est pas une configuration;          05 chaque lumière confirme son propre résultat;
     02 un aperçu ou un brouillon n'envoie rien;       06 le retour se fait dans le bon périmètre, avec avertissement;
     03 le précédent est protégé AVANT la 1re commande; 07 une sauvegarde durable est toujours explicite;
     04 un seul précédent par environnement;           08 on enregistre les valeurs confirmées, jamais un brouillon.
   Les photos ne sont jamais retouchées : la lumière est une couche posée dessus.
   Démonstration : aucun appareil réel n'est commandé; la latence et la panne de la page 12 sont simulées.

   API (pour le cadre Environnements) :
     JarvisLumieres.mount(el, envKey, api)      section complète, navigation interne
     JarvisLumieres.unmount(el)                 nettoyage (minuteries, écouteurs)
     JarvisLumieres.mini(el, envKey, api)       carte compacte de la Vue d'ensemble
     JarvisLumieres.applyAmbiance(envKey, k)    Promise → { confirmed, failed }
   api = { toast(text), go(sectionKey) }.  Événement : document « lum:change » { env, on, total }. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NB = " ", PC = " %";

  /* ---------------------------------------------------------------- outils */
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function pct(v, t) { return (v / t * 100).toFixed(3) + "%"; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }
  function norm(s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function words(n) { return ["aucune", "une", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze"][n] || String(n); }
  function plural(n, one, many) { return n + NB + (n > 1 ? many : one); }
  function off(g) { return { m: "éteint", f: "éteinte", mp: "éteints", fp: "éteintes" }[g] || "éteint"; }
  function resta(g) { return { m: "est resté", f: "est restée", mp: "sont restés", fp: "sont restées" }[g] || "est resté"; }
  function au(the) { return /^le /.test(the) ? "au " + the.slice(3) : /^les /.test(the) ? "aux " + the.slice(4) : "à " + the; }
  function list(a) { return a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " et " + a[a.length - 1]; }
  function hex(r, g, b) { return "#" + [r, g, b].map(function (v) { v = clamp(Math.round(v), 0, 255); return (v < 16 ? "0" : "") + v.toString(16); }).join(""); }
  function rgb(h) { h = h.replace("#", ""); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function mix(a, b, t) { var x = rgb(a), y = rgb(b); return hex(x[0] + (y[0] - x[0]) * t, x[1] + (y[1] - x[1]) * t, x[2] + (y[2] - x[2]) * t); }
  function rgba(h, a) { var c = rgb(h); return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
  /* Température de couleur → teinte (approximation de Tanner Helland) */
  function kelvin(k) {
    var t = k / 100, r, g, b;
    if (t <= 66) { r = 255; g = 99.47 * Math.log(t) - 161.12; b = t <= 19 ? 0 : 138.52 * Math.log(t - 10) - 305.04; }
    else { r = 329.7 * Math.pow(t - 60, -0.1332); g = 288.12 * Math.pow(t - 60, -0.0755); b = 255; }
    return hex(r, g, b);
  }
  function whiteName(k) { return k >= 5000 ? "blanc froid" : k >= 3300 ? "blanc neutre" : "blanc chaud"; }
  function lat() { return 150 + Math.random() * 250; } /* latence d'un appareil : 150 à 400 ms */

  function circ(x, y, r) { return "M" + (x - r) + " " + y + "a" + r + " " + r + " 0 1 0 " + 2 * r + " 0a" + r + " " + r + " 0 1 0 " + -2 * r + " 0"; }
  var ICONS = {
    sun: circ(12, 12, 3.6) + "M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6 7 7M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4",
    plus: "M12 5v14M5 12h14", check: "m5.5 12.5 4 4 9-9", x: "M6.5 6.5l11 11M17.5 6.5l-11 11",
    heart: "M12 19.5s-7-4.3-7-9.6A3.9 3.9 0 0 1 12 7.6a3.9 3.9 0 0 1 7 2.3c0 5.3-7 9.6-7 9.6Z",
    arrow: "M5 12h14M13.5 6.5 19 12l-5.5 5.5", left: "m14.5 6-6 6 6 6", right: "m9.5 6 6 6-6 6",
    search: circ(11, 11, 6.2) + "M20 20l-4.4-4.4", grid: "M4.5 4.5h6v6h-6zM13.5 4.5h6v6h-6zM4.5 13.5h6v6h-6zM13.5 13.5h6v6h-6z",
    map: "M9 4.5 3.5 6.5v13L9 17.5l6 2 5.5-2v-13L15 6.5zM9 4.5v13M15 6.5v13",
    lock: "M6 10.5h12v9.5H6zM8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5", warn: "M12 4.2 21 19.5H3zM12 10v4.4M12 17.1v.2",
    bands: "M4 9h16M4 15h16", retry: "M19.5 12a7.5 7.5 0 1 1-2.2-5.3M19.5 4.5v3.7h-3.7", shield: "M12 3.5 19 6v5.5c0 4.4-2.9 7.6-7 9-4.1-1.4-7-4.6-7-9V6z",
    strip: "M4 7.5h16M4 16.5h16M7.5 12h.01M12 12h.01M16.5 12h.01", cook: "M7 3.5v7a2 2 0 0 0 2 2v8M5 3.5v5M9 3.5v5M16.5 20.5v-17c-2 1.5-3 4-3 7h3",
    bed: "M3.5 18.5v-9M3.5 14h17v4.5M20.5 14v-2a3 3 0 0 0-3-3h-7v5M5.5 11.5h3", out: "M12 20.5v-4M12 3.5l-5.5 8h3l-3 5h11l-3-5h3z",
    sofa: "M5 11V8.5A2.5 2.5 0 0 1 7.5 6h9A2.5 2.5 0 0 1 19 8.5V11M3.5 17.5v-5a1.5 1.5 0 0 1 3 0V14h11v-1.5a1.5 1.5 0 0 1 3 0v5zM6 17.5v2M18 17.5v2",
    desk: "M3.5 9.5h17M5.5 9.5v10M18.5 9.5v10M9 9.5V5.5h6v4", bath: "M4 12.5h16v2a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM6.5 12.5V6a2 2 0 0 1 3.7-1",
    door: "M6 20.5V4.5a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v16M4 20.5h16M14.5 12.5h.01", car: "M5 16.5h14M4.5 16.5v-4l2-5h11l2 5v4M7.5 16.5v2M16.5 16.5v2M7.5 13.5h.01M16.5 13.5h.01",
    pool: "M3.5 16c2 1.4 3.5 1.4 5.5 0s3.5-1.4 5.5 0 3.5 1.4 5.5 0M3.5 19.5c2 1.4 3.5 1.4 5.5 0s3.5-1.4 5.5 0 3.5 1.4 5.5 0M8 13V5.5a2 2 0 0 1 4 0M16 13V5.5",
    fire: "M12 20.5c3.5 0 6-2.4 6-5.6 0-3.8-3.4-5.6-4.2-9.4-1.8 1.4-2.6 3.4-2.5 5.2-1.4-.6-2.3-1.9-2.5-3.2C7.3 9.2 6 11.5 6 14.9c0 3.2 2.5 5.6 6 5.6Z",
    spa: "M4 13.5h16a8 8 0 0 1-16 0ZM9 4c-1 1.2 1 2.3 0 3.5S9 9.8 9 10M14.5 4c-1 1.2 1 2.3 0 3.5s0 2.3 0 2.5",
    meet: "M5 9.5h14v5H5zM7.5 6.5h.01M12 6.5h.01M16.5 6.5h.01M7.5 17.5h.01M12 17.5h.01M16.5 17.5h.01",
    box: "M3.5 8 12 3.5 20.5 8v8.5L12 21l-8.5-4.5zM3.5 8 12 12.5 20.5 8M12 12.5V21", park: "M4.5 4.5h15v15h-15zM10 16.5v-9h3a2.5 2.5 0 0 1 0 5h-3",
    tool: "M14.7 4.6a4.2 4.2 0 0 0 4.7 5.3l-8.9 8.9a2.1 2.1 0 0 1-3-3l8.9-8.9a4.2 4.2 0 0 0-1.7-2.3Z",
    barn: "M3.5 20.5V10l8.5-6 8.5 6v10.5zM9 20.5v-6h6v6M9 14.5l6 6M15 14.5l-6 6",
    plant: "M12 20.5v-8M12 12.5c0-3.5 2.5-6 6.5-6 0 4-2.5 6-6.5 6ZM12 15c0-3-2-5-5.5-5 0 3.4 2 5 5.5 5ZM7.5 20.5h9",
    boat: "M3.5 15.5h17l-2.5 4h-12zM12 3.5v12M12 4.5l6 9h-6", wheel: circ(12, 12, 7.5) + circ(12, 12, 2) + "M12 4.5V10M12 14v5.5M4.5 12H10M14 12h5.5",
    plane: "M21 12.5 13.5 10V5a1.5 1.5 0 0 0-3 0v5L3 12.5v2l7.5-1.5v4l-2 1.5v1.5L12 19l3.5 1v-1.5l-2-1.5v-4l7.5 1.5z",
    nav: circ(12, 12, 3) + "M12 3.5v3M12 17.5v3M3.5 12h3M17.5 12h3M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2"
  };
  function ic(n, cls) { return '<svg class="lu-i' + (cls ? " " + cls : "") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + (ICONS[n] || ICONS.sun) + '"/></svg>'; }

  /* ---------------------------------------------------------------- données */
  var D = null, AMB = {}, ENV = {};
  function data() {
    if (D) return D;
    var el = document.getElementById("lum-data");
    if (!el) throw new Error("JarvisLumieres : le bloc de données #lum-data est absent de la page.");
    D = JSON.parse(el.textContent);
    D.ambiances.forEach(function (a) { AMB[a.k] = a; });
    Object.keys(D.envs).forEach(function (k) {
      var e = D.envs[k];
      e.key = k; e.L = {}; e.Z = {}; e.zl = {};
      e.zones.forEach(function (z) { e.Z[z.k] = z; e.zl[z.k] = []; });
      e.lights.forEach(function (l) { e.L[l.k] = l; e.zl[l.zone].push(l); });
      e.ctrl = e.lights.filter(function (l) { return l.kind !== "regl"; });
      ENV[k] = e;
    });
    return D;
  }
  function env(k) {
    data();
    if (!ENV[k]) throw new Error("JarvisLumieres : environnement inconnu « " + k + " ».");
    return ENV[k];
  }
  function ambs() { return data().ambiances; }
  function photo(name, size) {
    /* name : « amb-ocean » ou « vr-cuisine »; size : s (480 px), m (960 px), l (original) */
    if (size === "l") return name.indexOf("amb-") === 0 ? "/media/ambiances/" + name.slice(4) + ".webp" : "/media/vr/" + name.slice(3) + ".webp";
    return "/media/env/lum-" + name + "-" + (size === "s" ? 480 : 960) + ".webp";
  }
  function ambPhoto(a, size) { return photo("amb-" + (data().photos[a] || "heure-doree"), size); }

  /* ---------------------------------------------------------------- mémoire (session) */
  var KEY = "jarvis-lumieres-v1", STORE = null, saveT = 0;
  function store() {
    if (STORE) return STORE;
    try { STORE = JSON.parse(sessionStorage.getItem(KEY) || "null"); } catch (e) { STORE = null; }
    if (!STORE || STORE.v !== 1) STORE = { v: 1, envs: {}, favs: { "heure-doree": true, ocean: true } };
    /* Une commande interrompue par un rechargement n'est jamais présumée réussie */
    Object.keys(STORE.envs).forEach(function (k) {
      var s = STORE.envs[k];
      s.busy = false;
      Object.keys(s.lights).forEach(function (lk) { if (s.lights[lk].conf === "pending") s.lights[lk].conf = "unknown"; });
      if (s.tx && !s.tx.done) {
        s.tx.done = true;
        Object.keys(s.tx.res).forEach(function (lk) { if (s.tx.res[lk] !== "ok") s.tx.res[lk] = "fail"; });
      }
    });
    return STORE;
  }
  function persist(now) {
    clearTimeout(saveT);
    var go = function () { try { sessionStorage.setItem(KEY, JSON.stringify(STORE)); return true; } catch (e) { return false; } };
    if (now) return go();
    saveT = setTimeout(go, 250);
    return true;
  }
  function S(k) {
    var st = store(), s = st.envs[k];
    if (!s || !env(k).lights.every(function (l) { return s.lights[l.k]; })) s = st.envs[k] = fresh(k);
    return s;
  }
  function lv(a) { return { on: !!a[0], amb: a[1], lvl: a[2] }; }
  function fresh(k) {
    var e = env(k), s = { lights: {}, prev: null, origin: null, mod: false, configs: [], expect: null, tx: null, failDone: false, busy: false, seq: 1 };
    e.lights.forEach(function (l) {
      var v = lv(e.state[l.k] || [0, "lecture", 60]);
      v.last = v.lvl || 60; v.conf = "ok";
      s.lights[l.k] = v;
    });
    s.configs = e.configs.map(function (c) {
      var m = {};
      Object.keys(c.lights).forEach(function (lk) { m[lk] = lv(c.lights[lk]); });
      return { k: c.k, name: c.name, fav: !!c.fav, v: 1, lights: m, inc: [] };
    });
    return s;
  }
  function favs() { return store().favs; }
  function cfgOf(s, ck) { for (var i = 0; i < s.configs.length; i++) if (s.configs[i].k === ck) return s.configs[i]; return null; }

  /* ---------------------------------------------------------------- logique des lumières */
  function family(amb) { return amb === "ocean" ? "bleu" : amb === "cinema" ? "violet" : amb === "aurore" ? "aurore" : "ambre"; }
  function colorful(a) { return AMB[a] && AMB[a].cats.indexOf("colorees") >= 0; }
  function same(a, b) { return !!a.on === !!b.on && (!a.on || (a.amb === b.amb && a.lvl === b.lvl)); }
  /* Ce qu'une ambiance fait à une lumière : niveau (plafonné au besoin) et note d'adaptation */
  function adapt(l, a) {
    var A = AMB[a], lvl = A.lvl, notes = [];
    if (l.kind === "regl") return { skip: true, why: l.fixed };
    if (l.cap && lvl > l.cap[0]) { lvl = l.cap[0]; notes.push("plafonnée à " + lvl + PC); }
    if (l.kind === "fixe") notes.push("blanc fixe : intensité seulement");
    else if (l.kind === "blanc" && colorful(a)) notes.push("en " + whiteName(A.kv));
    return { lvl: lvl, note: notes.join(" · ") };
  }
  /* Couleurs réelles d'une lumière dans un état donné */
  function tints(l, v) {
    if (l.kind === "regl") return null;
    var A = AMB[v.amb] || AMB.lecture;
    if (l.kind === "fixe") return [kelvin(l.kv || 4000)];
    if (l.kind === "blanc") return [kelvin(A.kv)];
    return A.c2 ? [A.c, A.c2] : [A.c];
  }
  function dot(l, v) { var t = tints(l, v); return t ? t[0] : (l.fx && l.fx[0][3]) || "#ffffff"; }
  function ambName(l, a) { if (l && l.kind === "regl") return l.mode; return AMB[a] ? AMB[a].name : "Personnalisé"; }
  function vText(l, v, unknown) {
    if (unknown) return "État non confirmé";
    if (!v.on) return "Éteint";
    return ambName(l, v.amb) + " · " + v.lvl + PC;
  }
  function vLong(l, v) { return v.on ? ambName(l, v.amb) + " · On · " + v.lvl + PC : "Off · " + (v.lvl || v.last || 60) + PC + " au rallumage"; }
  function stateLabel(k) {
    var s = S(k);
    if (s.busy) return "Application en cours";
    if (s.origin && s.origin.t === "cfg") { var c = cfgOf(s, s.origin.k); if (c) return s.mod ? c.name + " · modifiée" : c.name; }
    if (s.origin && s.origin.t === "amb" && !s.mod) return AMB[s.origin.k].name;
    return "Personnalisé · non enregistré";
  }
  function snap(k) {
    var s = S(k), out = {};
    env(k).ctrl.forEach(function (l) { var v = s.lights[l.k]; out[l.k] = { on: v.on, amb: v.amb, lvl: v.lvl }; });
    return out;
  }
  function unknownLights(k) { var s = S(k); return env(k).ctrl.filter(function (l) { return s.lights[l.k].conf === "unknown"; }); }
  function onCount(k, src) { var s = src || S(k).lights, n = 0; env(k).ctrl.forEach(function (l) { if (s[l.k] && s[l.k].on) n++; }); return n; }
  /* Texte d'ambiance d'une zone : « Heure dorée », « Océan · Lecture », « Éteint » */
  function zoneAmb(e, z, V) {
    var ls = e.zl[z.k], fixed = ls.filter(function (l) { return l.kind === "regl"; });
    if (fixed.length === ls.length) return fixed[0].mode;
    var on = ls.filter(function (l) { return l.kind !== "regl" && V[l.k].on; }), names = [];
    on.forEach(function (l) { var n = ambName(l, V[l.k].amb); if (names.indexOf(n) < 0) names.push(n); });
    return names.length ? names.join(" · ") : (z.out ? z.tag : "Éteint");
  }
  function zoneOn(e, z, V) { return e.zl[z.k].some(function (l) { return l.kind !== "regl" && V[l.k].on; }); }
  function zoneLvl(e, z, V) {
    var on = e.zl[z.k].filter(function (l) { return l.kind !== "regl" && V[l.k].on; });
    if (!on.length) return 0;
    return Math.round(on.reduce(function (t, l) { return t + V[l.k].lvl; }, 0) / on.length);
  }
  function zoneDot(e, z, V) {
    var ls = e.zl[z.k];
    for (var i = 0; i < ls.length; i++) if (V[ls[i].k].on || ls[i].kind === "regl") return dot(ls[i], V[ls[i].k]);
    return "";
  }

  /* ---------------------------------------------------------------- plans d'application (rien n'est envoyé ici) */
  function change(s, l, to) { var v = s.lights[l.k]; return { k: l.k, to: to, from: { on: v.on, amb: v.amb, lvl: v.lvl } }; }
  /* Ambiance sur tout l'environnement : les lumières éteintes le restent, sauf allumage explicite (02) */
  function ambPlan(k, a, extra) {
    var s = S(k), e = env(k), ch = [], keep = [], notes = [];
    e.ctrl.forEach(function (l) {
      var v = s.lights[l.k], r = adapt(l, a);
      if (!v.on && !(extra && extra[l.k])) { keep.push(l.k); return; }
      var to = { on: true, amb: a, lvl: r.lvl };
      if (r.note) notes.push({ l: l, note: r.note });
      if (v.conf === "ok" && same(v, to)) keep.push(l.k); else ch.push(change(s, l, to));
    });
    return { changes: ch, keep: keep, notes: notes };
  }
  /* Ambiance d'une seule zone : une zone éteinte s'allume (c'est elle qu'on vise), sinon ses OFF restent */
  function zonePlan(k, z, a) {
    var s = S(k), e = env(k), ls = e.zl[z].filter(function (l) { return l.kind !== "regl"; }), ch = [], keep = [];
    var anyOn = ls.some(function (l) { return s.lights[l.k].on; });
    ls.forEach(function (l) {
      var v = s.lights[l.k];
      if (anyOn && !v.on) { keep.push(l.k); return; }
      var to = { on: true, amb: a, lvl: adapt(l, a).lvl };
      if (v.conf === "ok" && same(v, to)) keep.push(l.k); else ch.push(change(s, l, to));
    });
    return { changes: ch, keep: keep, wake: !anyOn };
  }
  function draftPlan(k, draft) {
    var s = S(k), ch = [];
    env(k).ctrl.forEach(function (l) {
      var d = draft[l.k], v = s.lights[l.k];
      if (d && (v.conf !== "ok" || !same(v, d))) ch.push(change(s, l, { on: d.on, amb: d.amb, lvl: d.lvl }));
    });
    return { changes: ch };
  }
  function restorePlan(k) {
    var s = S(k), e = env(k), drift = [], ch = [];
    if (!s.prev) return null;
    e.ctrl.forEach(function (l) {
      var v = s.lights[l.k], ex = s.expect && s.expect[l.k], p = s.prev.snap[l.k];
      if (v.conf === "unknown") drift.push({ l: l, unknown: true });
      else if (ex && !same(v, ex)) drift.push({ l: l, was: ex, now: v });
      if (p && (v.conf !== "ok" || !same(v, p))) ch.push(change(s, l, { on: p.on, amb: p.amb, lvl: p.lvl }));
    });
    return { changes: ch, drift: drift };
  }

  /* ---------------------------------------------------------------- abonnés et événements */
  var SUBS = [];
  function emit(k) {
    SUBS.forEach(function (u) { if (u.k === k) u.queue(); });
    var e = env(k);
    document.dispatchEvent(new CustomEvent("lum:change", { detail: { env: k, on: onCount(k), total: e.ctrl.length } }));
    persist();
  }

  /* État initial annoncé au cadre (compte « x / y allumées »), sans rien envoyer */
  function announce(k) {
    document.dispatchEvent(new CustomEvent("lum:change", { detail: { env: k, on: onCount(k), total: env(k).ctrl.length } }));
  }

  /* ---------------------------------------------------------------- transactions (03, 04, 05) */
  function txRun(k, p) {
    /* p = { kind: amb|zone|compose|config|restore, title, amb, zone, cfg, changes, origin, prevLabel } */
    var s = S(k), e = env(k);
    if (s.busy) return Promise.resolve({ confirmed: 0, failed: 0, busy: true });
    var tx = { id: s.seq++, kind: p.kind, title: p.title || "", amb: p.amb || null, zone: p.zone || null, cfg: p.cfg || null,
      changes: p.changes, keep: p.keep || [], res: {}, done: false, origin: p.origin || null, prevLabel: p.prevLabel || "" };
    if (p.kind !== "restore") {
      /* 03 : capture complète des états requis, ou zéro commande */
      var unk = unknownLights(k);
      if (unk.length) {
        tx.aborted = unk.map(function (l) { return l.k; });
        tx.prevTx = s.tx && s.tx.aborted ? s.tx.prevTx : s.tx;
        tx.done = true;
        s.tx = tx;
        emit(k);
        return Promise.resolve({ confirmed: 0, failed: 0, aborted: true });
      }
      /* 03-04 : le précédent est écrit d'un bloc AVANT la première commande; il remplace l'ancien */
      s.prev = { snap: snap(k), label: p.prevLabel || stateLabel(k), origin: s.origin, mod: s.mod, before: p.title || "", at: Date.now() };
      persist(true);
    }
    p.changes.forEach(function (c) { tx.res[c.k] = "wait"; });
    s.tx = tx;
    s.busy = true;
    emit(k);
    return send(k, tx, p.changes.map(function (c) { return c.k; })).then(function () { return finish(k, tx); });
  }
  /* Envoi lumière par lumière; chaque résultat est confirmé (ou non) séparément (05) */
  function send(k, tx, keys) {
    var s = S(k), e = env(k);
    return new Promise(function (resolve) {
      var i = 0;
      (function next() {
        if (i >= keys.length) return resolve();
        var lk = keys[i++], c = tx.changes.filter(function (x) { return x.k === lk; })[0], v = s.lights[lk];
        tx.res[lk] = "send";
        v.conf = "pending";
        emit(k);
        setTimeout(function () {
          var f = e.failOnce;
          var fail = f && !s.failDone && tx.kind === "amb" && tx.amb === f.amb && lk === f.light && !tx.retry;
          if (fail) {
            s.failDone = true;
            v.conf = "unknown";
            tx.res[lk] = "fail";
          } else {
            v.on = c.to.on; v.amb = c.to.amb; v.lvl = c.to.lvl;
            if (v.lvl > 0) v.last = v.lvl;
            v.conf = "ok";
            tx.res[lk] = "ok";
          }
          emit(k);
          next();
        }, lat());
      })();
    });
  }
  function counts(tx) {
    var ok = 0, ko = 0;
    Object.keys(tx.res).forEach(function (lk) { if (tx.res[lk] === "ok" || tx.res[lk] === "manual") ok++; else if (tx.res[lk] === "fail") ko++; });
    return { confirmed: ok, failed: ko };
  }
  function finish(k, tx) {
    var s = S(k);
    tx.done = true;
    s.busy = false;
    /* État attendu après cette application (sert à détecter tout changement avant un retour, 06) */
    var ex = snap(k);
    tx.changes.forEach(function (c) { ex[c.k] = { on: c.to.on, amb: c.to.amb, lvl: c.to.lvl }; });
    s.expect = ex;
    if (tx.kind === "restore") { s.origin = s.prev ? s.prev.origin : null; s.mod = s.prev ? s.prev.mod : false; }
    else if (tx.origin) { s.origin = tx.origin; s.mod = false; }
    emit(k);
    return counts(tx);
  }
  /* Réessayer : même transaction, même précédent, aucune nouvelle capture (04) */
  function txRetry(k) {
    var s = S(k), tx = s.tx;
    if (!tx || s.busy) return Promise.resolve({ confirmed: 0, failed: 0 });
    var keys = Object.keys(tx.res).filter(function (lk) { return tx.res[lk] === "fail"; });
    if (!keys.length) return Promise.resolve(counts(tx));
    tx.retry = (tx.retry || 0) + 1;
    tx.done = false;
    s.busy = true;
    keys.forEach(function (lk) { tx.res[lk] = "wait"; });
    emit(k);
    return send(k, tx, keys).then(function () { return finish(k, tx); });
  }
  /* Redemander l'état d'une lumière muette (lecture seule : aucune commande) */
  function requery(k, keys) {
    var s = S(k);
    keys.forEach(function (lk) { s.lights[lk].conf = "pending"; });
    emit(k);
    setTimeout(function () { keys.forEach(function (lk) { s.lights[lk].conf = "ok"; }); emit(k); }, lat());
  }
  /* Gestes directs : changent l'actuel seulement (07), sans toucher au précédent */
  var ACK = {};
  function direct(k, keys, patch, quiet) {
    var s = S(k), e = env(k);
    keys.forEach(function (lk) {
      var l = e.L[lk], v = s.lights[lk];
      if (!l || l.kind === "regl") return;
      if ("on" in patch) { v.on = patch.on; if (v.on && !(v.lvl > 0)) v.lvl = v.last || 60; }
      if ("lvl" in patch) { v.lvl = clamp(Math.round(patch.lvl), 1, l.cap ? l.cap[0] : 100); v.last = v.lvl; v.on = true; }
      if (quiet) return;
      v.conf = "pending";
      clearTimeout(ACK[k + lk]);
      ACK[k + lk] = setTimeout(function () {
        v.conf = "ok";
        if (s.tx && s.tx.res[lk] === "fail") s.tx.res[lk] = "manual";
        emit(k);
      }, lat());
    });
    s.mod = true;
    emit(k);
  }

  /* ---------------------------------------------------------------- configurations (07, 08) */
  function uniqueName(s, n) {
    var base = n, i = 2;
    while (s.configs.some(function (c) { return norm(c.name) === norm(n); })) n = base + " " + i++;
    return n;
  }
  function slug(n) { return norm(n).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "config"; }
  /* Enregistrer l'actuel : valeurs confirmées seulement; une lumière non confirmée rend la capture incomplète */
  function confirmedSnap(k) {
    var s = S(k), out = {}, inc = [];
    env(k).ctrl.forEach(function (l) {
      var v = s.lights[l.k];
      if (v.conf === "ok") out[l.k] = { on: v.on, amb: v.amb, lvl: v.lvl };
      else inc.push(l.k);
    });
    return { lights: out, inc: inc };
  }
  function saveNew(k, name, from) {
    var s = S(k);
    name = String(name || "").trim();
    if (!name) return { error: "Donnez un nom à cette configuration." };
    var clash = s.configs.filter(function (c) { return norm(c.name) === norm(name); })[0];
    if (clash) return { conflict: clash };
    var cap = from || confirmedSnap(k);
    var c = { k: slug(name) + "-" + s.seq++, name: name, fav: false, v: 1, lights: cap.lights, inc: cap.inc || [] };
    s.configs.unshift(c);
    if (!from) { s.origin = { t: "cfg", k: c.k, v: 1 }; s.mod = false; }
    emit(k);
    return { ok: c };
  }
  /* Mettre à jour : on vérifie la version avant d'écrire; un conflit n'écrase jamais en silence */
  function updateCfg(k, ck, seenV) {
    var s = S(k), c = cfgOf(s, ck);
    if (!c) return { error: "Configuration introuvable." };
    if (seenV != null && seenV !== c.v) return { conflict: c, stale: true };
    var cap = confirmedSnap(k);
    c.lights = cap.lights; c.inc = cap.inc; c.v++;
    s.origin = { t: "cfg", k: c.k, v: c.v }; s.mod = false;
    emit(k);
    return { ok: c };
  }
  function copyCfg(k, ck) {
    var s = S(k), c = cfgOf(s, ck);
    return saveNew(k, uniqueName(s, (c ? c.name : "Configuration") + " · copie"));
  }

  /* ---------------------------------------------------------------- filtres SVG partagés (flou des halos) */
  function defs() {
    if (document.getElementById("lu-defs")) return;
    var d = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    d.id = "lu-defs";
    d.setAttribute("aria-hidden", "true");
    d.setAttribute("style", "position:absolute;width:0;height:0;overflow:hidden");
    d.innerHTML = [["lu-b1", 2], ["lu-b2", 7], ["lu-b3", 16], ["lu-b4", 30], ["lu-b5", 56]].map(function (f) {
      return '<filter id="' + f[0] + '" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2800" height="2200" color-interpolation-filters="sRGB">' +
        '<feGaussianBlur stdDeviation="' + f[1] + '"/></filter>';
    }).join("");
    document.body.appendChild(d);
  }
  function blurFor(r) { return r > 110 ? "lu-b5" : r > 60 ? "lu-b4" : r > 30 ? "lu-b3" : "lu-b2"; }

  /* ---------------------------------------------------------------- plan (photo ou dessin) + couches de lumière */
  var UID = 0;
  function polyPts(poly) { return poly.map(function (p) { return p[0] + "," + p[1]; }).join(" "); }
  function polyPct(poly, W, H) { return "polygon(" + poly.map(function (p) { return pct(p[0], W) + " " + pct(p[1], H); }).join(",") + ")"; }
  function planHTML(e, src, o) {
    o = o || {};
    var p = e.plan, id = "lu" + (++UID), vb = "0 0 " + p.w + " " + p.h, vr = p.type === "vr";
    var view = p.view, ar = (view[2] / view[3]).toFixed(4);
    var h = '<div class="lu-plan lu-plan-' + p.type + (o.cls ? " " + o.cls : "") + '" data-src="' + esc(src) + '" data-crop="' + (o.crop || "view") + '"' +
      (o.labels ? ' data-lab="' + o.labels + '"' : "") + (o.fill ? "" : ' style="aspect-ratio:' + ar + '"') + '><div class="lu-pi">';
    if (vr) {
      Object.keys(p.imgs).forEach(function (pk) {
        h += '<img class="lu-pb" data-pk="' + pk + '" src="' + p.imgs[pk] + '" alt="" width="' + p.w + '" height="' + p.h + '" decoding="async" draggable="false">';
      });
      h += '<svg class="lu-dk" viewBox="' + vb + '" preserveAspectRatio="none" aria-hidden="true">' + e.lights.map(function (l) {
        return l.dk ? '<g data-l="' + l.k + '" filter="url(#lu-b4)">' + l.dk.map(function (d) {
          return '<ellipse cx="' + d[0] + '" cy="' + d[1] + '" rx="' + d[2] + '" ry="' + d[3] + '"/>';
        }).join("") + "</g>" : "";
      }).join("") + "</svg>";
    } else if (p.type === "photo") {
      h += '<img class="lu-pb is-on" src="' + p.img + '" alt="" width="' + p.w + '" height="' + p.h + '" decoding="async" draggable="false">';
      h += '<div class="lu-night" aria-hidden="true"><i></i><i></i></div>';
      h += e.lights.map(function (l) {
        return '<i class="lu-rev" data-l="' + l.k + '" style="background-image:url(&quot;' + p.img + '&quot;);clip-path:' + polyPct(e.Z[l.zone].poly, p.w, p.h) + '"></i>';
      }).join("");
    } else {
      h += p.svg;
    }
    /* Halos : un groupe par lumière, fondu en « écran » sur le plan */
    var gd = "", gl = "";
    e.lights.forEach(function (l) {
      /* Les murs arrêtent la lumière : à l'intérieur, chaque halo est découpé sur sa pièce */
      var inside = !vr && l.kind !== "regl" && !e.Z[l.zone].out;
      if (inside) gd += '<clipPath id="' + id + "c" + l.k + '"><polygon points="' + polyPts(e.Z[l.zone].poly) + '"/></clipPath>';
      var g = '<g class="lu-g' + (l.strobe ? " is-strobe" : "") + '" data-l="' + l.k + '"' + (inside ? ' clip-path="url(#' + id + "c" + l.k + ')"' : "") + ">";
      if (inside) g += '<polygon class="lu-fw" points="' + polyPts(e.Z[l.zone].poly) + '"/>';
      if (l.fl) g += '<g filter="url(#lu-b4)">' + l.fl.map(function (f) { return '<ellipse class="lu-fe" cx="' + f[0] + '" cy="' + f[1] + '" rx="' + f[2] + '" ry="' + f[3] + '"/>'; }).join("") + "</g>";
      if (l.st) {
        l.st.forEach(function (s, j) {
          gd += '<linearGradient id="' + id + l.k + j + '" gradientUnits="userSpaceOnUse" x1="' + s[0] + '" y1="' + s[1] + '" x2="' + s[2] + '" y2="' + s[3] + '"><stop offset="0"/><stop offset="1"/></linearGradient>';
        });
        var line = function (w, j, s) { return '<line x1="' + s[0] + '" y1="' + s[1] + '" x2="' + s[2] + '" y2="' + s[3] + '" stroke-width="' + w + '" stroke-linecap="round" stroke="url(#' + id + l.k + j + ')"/>'; };
        g += '<g filter="url(#' + (vr ? "lu-b4" : "lu-b3") + ')" class="lu-sh">' + l.st.map(function (s, j) { return line(vr ? 34 : 22, j, s); }).join("") + "</g>";
        g += '<g filter="url(#lu-b1)" class="lu-sc">' + l.st.map(function (s, j) { return line(vr ? 6 : 4, j, s); }).join("") + "</g>";
      }
      if (l.fx) {
        var avg = l.fx.reduce(function (t, f) { return t + f[2]; }, 0) / l.fx.length;
        g += '<g filter="url(#' + blurFor(avg) + ')">' + l.fx.map(function (f, i) { return '<circle class="lu-h" data-i="' + i + '" cx="' + f[0] + '" cy="' + f[1] + '" r="' + (f[2] * (inside ? .72 : .6)).toFixed(1) + '"/>'; }).join("") + "</g>";
        g += '<g filter="url(#lu-b1)">' + l.fx.map(function (f, i) { return '<circle class="lu-c" data-i="' + i + '" cx="' + f[0] + '" cy="' + f[1] + '" r="' + Math.max(3, f[2] * .09).toFixed(1) + '"/>'; }).join("") + "</g>";
      }
      gl += g + "</g>";
    });
    h += '<svg class="lu-gl' + (e.lights.some(function (l) { return l.strobe; }) ? " has-strobe" : "") + '" viewBox="' + vb + '" preserveAspectRatio="none" aria-hidden="true"><defs>' + gd + "</defs>" + gl + "</svg>";
    if (o.crop && o.crop.indexOf("zone:") === 0) {
      h += '<svg class="lu-zl" viewBox="' + vb + '" preserveAspectRatio="none" aria-hidden="true"><polygon points="' + polyPts(e.Z[o.crop.slice(5)].poly) + '"/></svg>';
    }
    if (o.labels) {
      var btn = !!o.click;
      h += e.zones.map(function (z) {
        var tag = btn ? 'button type="button" data-a="zone" data-v="' + z.k + '"' : "span";
        return "<" + tag + ' class="lu-tag" data-z="' + z.k + '" style="left:' + pct(z.lab[0], p.w) + ";top:" + pct(z.lab[1], p.h) + '"><i></i><b>' + esc(z.name) + "</b><em></em></" + (btn ? "button" : "span") + ">";
      }).join("");
    }
    return h + "</div></div>";
  }
  function lvlOp(v) { return v.on ? .32 + .68 * Math.pow(v.lvl / 100, .8) : 0; }
  function setOp(el, v) { if (el) el.style.opacity = (+v).toFixed(3); }
  function paintPlan(el, e, V) {
    var p = e.plan, vr = p.type === "vr";
    var baked = null;
    if (vr) {
      var cg = V["couloir-g"], cd = V["couloir-d"], ch = V.chambre;
      var pk = ((cg.on && cg.amb === "ocean") || (cd.on && cd.amb === "ocean")) ? "ocean" : (ch.on && ch.amb === "cinema") ? "chaleur" : "signature";
      [].forEach.call(el.querySelectorAll(".lu-pb"), function (img) { img.classList.toggle("is-on", img.getAttribute("data-pk") === pk); });
      baked = p.baked[pk];
    }
    e.lights.forEach(function (l) {
      var v = V[l.k], fixed = l.kind === "regl", g = el.querySelector('.lu-gl [data-l="' + l.k + '"]');
      var cols = tints(l, v) || [];
      var op = fixed ? 1 : lvlOp(v), dark = 0;
      if (vr && baked && baked[l.k]) {
        var b = baked[l.k], fam = family(v.amb);
        if (!v.on) { dark = .9; op = 0; }
        else if (fam !== b) { dark = .82; }
        else { dark = (1 - v.lvl / 100) * .6; op = v.amb === "lecture" ? .3 : 0; }
        setOp(el.querySelector('.lu-dk [data-l="' + l.k + '"]'), dark);
      }
      if (p.type === "photo") {
        var rv = el.querySelector('.lu-rev[data-l="' + l.k + '"]');
        setOp(rv, v.on ? Math.pow(v.lvl / 100, .7) : 0);
      }
      if (!g) return;
      setOp(g, op);
      var c0 = cols[0] || "#ffffff", c1 = cols[1] || c0;
      [].forEach.call(g.querySelectorAll(".lu-h"), function (c) {
        var i = +c.getAttribute("data-i"), f = l.fx[i], col = f[3] || (i % 2 ? c1 : c0);
        c.style.fill = col;
      });
      [].forEach.call(g.querySelectorAll(".lu-c"), function (c) {
        var i = +c.getAttribute("data-i"), f = l.fx[i], col = f[3] || (i % 2 ? c1 : c0);
        c.style.fill = mix(col, "#ffffff", .55);
      });
      [].forEach.call(g.querySelectorAll(".lu-fe"), function (f) { f.style.fill = c0; f.style.opacity = (.22 + .3 * v.lvl / 100).toFixed(3); });
      [].forEach.call(g.querySelectorAll(".lu-fw"), function (f) { f.style.fill = c0; f.style.opacity = (.05 + .1 * v.lvl / 100).toFixed(3); });
      if (l.st) {
        l.st.forEach(function (s, j) {
          var gr = el.querySelector("#" + CSS.escape(gradId(el, l.k, j)));
          if (!gr) return;
          gr.children[0].style.stopColor = c0;
          gr.children[1].style.stopColor = c1;
        });
        [].forEach.call(g.querySelectorAll(".lu-sc line"), function (ln) { ln.style.opacity = .95; });
      }
    });
    /* Étiquettes */
    var mode = el.getAttribute("data-lab");
    if (mode) {
      [].forEach.call(el.querySelectorAll(".lu-tag"), function (t) {
        var z = e.Z[t.getAttribute("data-z")], on = zoneOn(e, z, V), d = zoneDot(e, z, V), multi = z.group ? " · " + z.group.short : "";
        var lit = on || e.zl[z.k].every(function (l) { return l.kind === "regl"; });
        t.querySelector("b").textContent = mode === "amb" ? (lit ? zoneAmb(e, z, V) : "Éteint") : z.short || z.name;
        t.querySelector("em").textContent = mode === "amb" && !lit ? "" : multi;
        t.querySelector("i").style.background = d || "transparent";
        t.classList.toggle("is-off", !d);
      });
    }
  }
  /* Le premier dégradé du plan porte un identifiant unique : on le retrouve par son préfixe */
  function gradId(el, lk, j) {
    var any = el.querySelector(".lu-gl linearGradient");
    if (!any) return "";
    var pre = el._pre || (el._pre = any.id.match(/^lu\d+/)[0]);
    return pre + lk + j;
  }
  /* Cadrage : la vue entière ou une zone, en « couvrir », selon la taille réelle du cadre */
  function fit(el, e) {
    var crop = el.getAttribute("data-crop"), p = e.plan, w = el.clientWidth, hgt = el.clientHeight;
    if (!w || !hgt) return;
    var bx, by, bw, bh;
    if (crop.indexOf("zone:") === 0) {
      var z = e.Z[crop.slice(5)], xs = z.poly.map(function (q) { return q[0]; }), ys = z.poly.map(function (q) { return q[1]; });
      bx = Math.min.apply(0, xs); by = Math.min.apply(0, ys); bw = Math.max.apply(0, xs) - bx; bh = Math.max.apply(0, ys) - by;
      var pad = Math.max(bw, bh) * .16;
      bx -= pad; by -= pad; bw += 2 * pad; bh += 2 * pad;
      var minW = p.w * .3;
      if (bw < minW) { bx -= (minW - bw) / 2; bw = minW; }
    } else { bx = p.view[0]; by = p.view[1]; bw = p.view[2]; bh = p.view[3]; }
    var a = w / hgt;
    if (bw / bh < a) { var nw = bh * a; bx -= (nw - bw) / 2; bw = nw; } else { var nh = bw / a; by -= (nh - bh) / 2; bh = nh; }
    bx = bw <= p.w ? clamp(bx, 0, p.w - bw) : (p.w - bw) / 2;
    by = bh <= p.h ? clamp(by, 0, p.h - bh) : (p.h - bh) / 2;
    var pi = el.firstChild.style;
    pi.width = (p.w / bw * 100).toFixed(3) + "%"; pi.height = (p.h / bh * 100).toFixed(3) + "%";
    pi.left = (-bx / bw * 100).toFixed(3) + "%"; pi.top = (-by / bh * 100).toFixed(3) + "%";
  }

  /* ---------------------------------------------------------------- photos de zone (BouLance) */
  function zonePhoto(e, z, V, size) {
    if (z.photo === "amb") {
      var ls = e.zl[z.k], lead = ls.filter(function (l) { return V[l.k].on; })[0] || ls[0];
      return ambPhoto(V[lead.k].amb, size);
    }
    return photo("vr-" + z.photo, size);
  }
  function phHTML(e, z, V, size) {
    var src = zonePhoto(e, z, V, size);
    var h = '<div class="lu-ph" data-z="' + z.k + '" data-size="' + size + '"><img class="lu-phi is-on" src="' + src + '" alt="" decoding="async" draggable="false">' +
      '<img class="lu-phi" alt="" decoding="async" draggable="false"><i class="lu-phd"></i>';
    (z.ov || []).forEach(function (r, i) {
      h += '<i class="lu-phg" data-i="' + i + '" style="left:' + r[0] + "%;top:" + r[1] + "%;width:" + (r[2] - r[0]) + "%;height:" + (r[3] - r[1]) + '%"></i>';
    });
    if (z.photo === "amb") h += '<i class="lu-phg lu-phg-r"></i>';
    return h + "</div>";
  }
  function paintPhoto(el, e, V) {
    var z = e.Z[el.getAttribute("data-z")], size = el.getAttribute("data-size"), ls = e.zl[z.k];
    var want = zonePhoto(e, z, V, size), imgs = el.querySelectorAll(".lu-phi"), cur = el.querySelector(".lu-phi.is-on");
    if (cur && cur.getAttribute("src") !== want && el._want !== want) {
      el._want = want;
      var nxt = cur === imgs[0] ? imgs[1] : imgs[0];
      var swap = function () { if (el._want !== want) return; nxt.classList.add("is-on"); cur.classList.remove("is-on"); };
      nxt.onload = swap;
      nxt.setAttribute("src", want);
      if (nxt.complete && nxt.naturalWidth) swap();
    }
    var veil = el.querySelector(".lu-phd"), gls = el.querySelectorAll(".lu-phg");
    if (z.photo === "amb") {
      var a = V[ls[0].k], b = V[ls[1] ? ls[1].k : ls[0].k];
      var dv = function (v) { return v.on ? (1 - v.lvl / 100) * .42 : .8; };
      veil.style.background = "linear-gradient(90deg, rgba(4,3,2," + dv(a).toFixed(3) + ") 18%, rgba(4,3,2," + dv(b).toFixed(3) + ") 82%)";
      veil.style.opacity = 1;
      var r = el.querySelector(".lu-phg-r");
      if (r) {
        var diff = a.on && b.on && family(a.amb) !== family(b.amb);
        r.style.background = diff ? "radial-gradient(closest-side, " + rgba(dot(ls[1], b), .9) + ", transparent)" : "none";
        setOp(r, diff ? lvlOp(b) : 0);
      }
      return;
    }
    var l = ls[0], v = V[l.k], fam = family(v.amb), col = dot(l, v);
    if (z.baked === "off") {
      veil.style.background = "#040302"; setOp(veil, 0);
      [].forEach.call(gls, function (g) { g.style.background = "radial-gradient(closest-side, " + rgba(mix(col, "#ffffff", .15), .95) + ", transparent)"; setOp(g, lvlOp(v)); });
      return;
    }
    veil.style.background = "#040302";
    var mismatch = v.on && fam !== z.baked;
    setOp(veil, !v.on ? .74 : mismatch ? .42 : (1 - v.lvl / 100) * .45);
    [].forEach.call(gls, function (g) { g.style.background = "radial-gradient(closest-side, " + rgba(col, .95) + ", transparent)"; setOp(g, mismatch ? lvlOp(v) : 0); });
  }

  /* Vignette d'ambiance : photo du dossier (BouLance) ou composition lumineuse sur le contour du plan */
  function glowTile(e, V, zoneKey) {
    var p = e.plan, layers = [], zs = zoneKey ? [e.Z[zoneKey]] : e.zones;
    var bx = 0, by = 0, bw = p.w, bh = p.h;
    if (zoneKey) {
      var z = zs[0], xs = z.poly.map(function (q) { return q[0]; }), ys = z.poly.map(function (q) { return q[1]; });
      bx = Math.min.apply(0, xs); by = Math.min.apply(0, ys); bw = Math.max.apply(0, xs) - bx || 1; bh = Math.max.apply(0, ys) - by || 1;
      var pad = Math.max(bw, bh) * .25; bx -= pad; by -= pad; bw += 2 * pad; bh += 2 * pad;
    }
    e.lights.forEach(function (l) {
      if (zoneKey && l.zone !== zoneKey) return;
      var v = V[l.k], cols = tints(l, v) || [], op = l.kind === "regl" ? .9 : lvlOp(v);
      if (!op) return;
      var pts = (l.fx || []).map(function (f) { return [f[0], f[1], f[2], f[3]]; });
      (l.st || []).forEach(function (s) { pts.push([(s[0] + s[2]) / 2, (s[1] + s[3]) / 2, Math.max(Math.abs(s[2] - s[0]), Math.abs(s[3] - s[1])) * .5]); });
      pts.forEach(function (f, i) {
        var col = f[3] || cols[i % (cols.length || 1)] || "#ffffff";
        var rx = Math.max(6, f[2] / bw * 100 * 1.4), ry = Math.max(6, f[2] / bh * 100 * 1.4);
        layers.push("radial-gradient(" + rx.toFixed(1) + "% " + ry.toFixed(1) + "% at " + ((f[0] - bx) / bw * 100).toFixed(1) + "% " + ((f[1] - by) / bh * 100).toFixed(1) + "%, " + rgba(col, (.85 * op).toFixed(2)) + ", " + rgba(col, (.25 * op).toFixed(2)) + " 35%, transparent 72%)");
      });
    });
    var outline = '<svg viewBox="' + bx.toFixed(0) + " " + by.toFixed(0) + " " + bw.toFixed(0) + " " + bh.toFixed(0) + '" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' +
      e.zones.map(function (z) { return '<polygon points="' + polyPts(z.poly) + '"/>'; }).join("") + "</svg>";
    return '<span class="lu-gt" style="background:' + (layers.join(",") || "none") + '">' + outline + "</span>";
  }
  function ambThumb(e, a, size) {
    if (e.key === "boulance") return '<img src="' + ambPhoto(a, size || "s") + '" alt="" loading="lazy" decoding="async" draggable="false">';
    var V = {};
    e.lights.forEach(function (l) { V[l.k] = l.kind === "regl" ? { on: true, amb: "", lvl: 100 } : { on: true, amb: a, lvl: adapt(l, a).lvl }; });
    return glowTile(e, V);
  }
  /* Vignette d'une lumière (rangées du compositeur, résultats) */
  function lightThumb(e, l, v) {
    if (e.key === "boulance") {
      if (l.zone === "exterieur") return '<img src="' + photo("vr-exterieur", "s") + '" alt="" loading="lazy" decoding="async">';
      return '<img src="' + ambPhoto(v.amb, "s") + '" alt="" loading="lazy" decoding="async"' + (v.on ? "" : ' class="is-off"') + ">";
    }
    var V = {};
    e.lights.forEach(function (x) { V[x.k] = x.k === l.k ? v : { on: false, amb: v.amb, lvl: 0 }; });
    return glowTile(e, V, l.zone);
  }

  /* ---------------------------------------------------------------- petits composants */
  function sw(on, a, v, label, dis, pend) {
    return '<span class="lu-swl" aria-hidden="true">' + (on ? "On" : "Off") + '</span><button type="button" class="lu-sw' + (pend ? " is-pend" : "") + '" role="switch" aria-checked="' + !!on +
      '" aria-label="' + esc(label) + '" data-a="' + a + '" data-v="' + esc(v) + '"' + (dis ? " disabled" : "") + "><i></i></button>";
  }
  function heart(a) {
    var on = !!favs()[a];
    return '<button type="button" class="lu-heart' + (on ? " is-on" : "") + '" data-a="fav" data-v="' + a + '" aria-pressed="' + on + '" aria-label="' + (on ? "Retirer des favoris" : "Ajouter aux favoris") + " : " + esc(AMB[a].name) + '">' + ic("heart") + "</button>";
  }
  function ambDot(a) { var A = AMB[a]; return '<i class="lu-dot" style="background:' + (A.c2 ? "linear-gradient(135deg," + A.c + "," + A.c2 + ")" : A.c) + '"></i>'; }
  function filterAmbs(q, favOnly, cat, withStyle) {
    return ambs().filter(function (a) {
      if (a.style && !withStyle) return false;
      if (q && norm(a.name + " " + a.desc).indexOf(norm(q)) < 0) return false;
      if (favOnly && !favs()[a.k]) return false;
      if (cat && a.cats.indexOf(cat) < 0) return false;
      return true;
    });
  }
  function greet() {
    var h = new Date().getHours();
    if (h >= 5 && h < 17) return ["Bonjour", "La journée commence en douceur."];
    if (h >= 17 && h < 22) return ["Bonsoir", "Installez-vous. La soirée est à vous."];
    return ["Bonne nuit", "Tout se calme. Le passage reste doux."];
  }

  /* ================================================================ SECTION COMPLÈTE */
  var INST = [];
  /* Le module vit dans son propre élément, sans toucher aux styles du conteneur fourni */
  function rootIn(host, cls) {
    var r = document.createElement("div");
    r.className = cls;
    host.appendChild(r);
    return r;
  }
  function mountFull(host, k, api) {
    data(); defs();
    unmount(host);
    var e = env(k), el = rootIn(host, "lu");
    var I = { host: host, el: el, k: k, e: e, api: api || {}, scr: { n: "home" }, hist: [], view: "pieces", filter: "", q: "", favOnly: false, parts: {}, dlg: null, saveOpen: true, timers: [] };
    el.setAttribute("data-lu-env", k);
    I.queue = function () {
      if (I.raf) return;
      I.raf = requestAnimationFrame(function () { I.raf = 0; update(I); });
    };
    I.on = function (type, fn, opts) { el.addEventListener(type, fn, opts); I.timers.push(function () { el.removeEventListener(type, fn, opts); }); };
    bindFull(I);
    I.ro = "ResizeObserver" in window ? new ResizeObserver(function () { fitAll(I); }) : null;
    if (I.ro) I.ro.observe(el);
    live(I);
    SUBS.push(I);
    INST.push(I);
    render(I);
    announce(k);
    return I;
  }
  function live(I) {
    if (!("IntersectionObserver" in window)) { I.el.classList.add("is-live"); return; }
    I.io = new IntersectionObserver(function (es) { es.forEach(function (x) { I.el.classList.toggle("is-live", x.isIntersecting); }); });
    I.io.observe(I.el);
  }
  function unmount(host) {
    INST.slice().forEach(function (I) {
      if (I.host !== host) return;
      if (I.raf) cancelAnimationFrame(I.raf);
      I.timers.forEach(function (f) { f(); });
      if (I.ro) I.ro.disconnect();
      if (I.io) I.io.disconnect();
      SUBS.splice(SUBS.indexOf(I), 1);
      INST.splice(INST.indexOf(I), 1);
      if (I.el.parentNode === host) host.removeChild(I.el);
    });
  }
  function fitAll(I) { [].forEach.call(I.el.querySelectorAll(".lu-plan"), function (p) { fit(p, I.e); }); }
  function V(I, src) {
    var s = S(I.k), e = I.e, out = {};
    e.lights.forEach(function (l) { out[l.k] = s.lights[l.k]; });
    if (src === "cur") return out;
    if (src === "draft" && I.scr.draft) Object.keys(I.scr.draft).forEach(function (lk) { out[lk] = I.scr.draft[lk]; });
    else if (src === "prev" && s.prev) Object.keys(s.prev.snap).forEach(function (lk) { out[lk] = s.prev.snap[lk]; });
    else if (src.indexOf("amb:") === 0) e.ctrl.forEach(function (l) { var a = src.slice(4); out[l.k] = { on: true, amb: a, lvl: adapt(l, a).lvl }; });
    else if (src.indexOf("ambp:") === 0) ambPlan(I.k, src.slice(5), I.scr.extra).changes.forEach(function (c) { out[c.k] = c.to; });
    else if (src.indexOf("cfg:") === 0) {
      var c = cfgOf(s, src.slice(4));
      if (c) Object.keys(c.lights).forEach(function (lk) { out[lk] = c.lights[lk]; });
    } else if (src === "zprev" && I.scr.pa) zonePlan(I.k, I.scr.z, I.scr.pa).changes.forEach(function (c) { out[c.k] = c.to; });
    return out;
  }
  function paintAll(I) {
    [].forEach.call(I.el.querySelectorAll(".lu-plan"), function (p) { paintPlan(p, I.e, V(I, p.getAttribute("data-src"))); });
    [].forEach.call(I.el.querySelectorAll(".lu-ph"), function (p) { var h = p.closest("[data-src]"); paintPhoto(p, I.e, V(I, h ? h.getAttribute("data-src") : "cur")); });
  }

  /* Navigation interne */
  function go(I, scr, noHist) {
    if (!noHist) I.hist.push(I.scr);
    if (I.hist.length > 30) I.hist.shift();
    I.scr = scr;
    I.dlg = null;
    render(I, true);
    var top = I.el.getBoundingClientRect().top;
    if (top < 0) I.el.scrollIntoView({ block: "start", behavior: reduce ? "auto" : "smooth" });
  }
  function back(I) { var p = I.hist.pop(); go(I, p || { n: "home" }, true); }

  /* Rendu : squelette de l'écran + parties dynamiques (data-part), puis peinture des couches de lumière */
  function render(I, enter) {
    var r = SCREENS[I.scr.n] || SCREENS.home;
    I.parts = {};
    var body = r(I);
    I.el.innerHTML = '<div class="lu-in">' + topBar(I) + '<div class="lu-scr' + (enter ? " is-enter" : "") + '" data-scr="' + I.scr.n + '">' + body + "</div>" + part(I, "dlg", function () { return dialog(I); }) + "</div>";
    [].forEach.call(I.el.querySelectorAll("[data-part]"), function (p) { p._h = p.innerHTML; });
    I.el.classList.add("lu-still");
    fitAll(I);
    paintAll(I);
    requestAnimationFrame(function () { requestAnimationFrame(function () { I.el.classList.remove("lu-still"); }); });
  }
  function part(I, name, fn, tag, cls) {
    I.parts[name] = fn;
    tag = tag || "div";
    return "<" + tag + ' data-part="' + name + '"' + (cls ? ' class="' + cls + '"' : "") + ">" + fn() + "</" + tag + ">";
  }
  function update(I) {
    if (!I.el.isConnected) return;
    var act = document.activeElement, stills = [];
    [].forEach.call(I.el.querySelectorAll("[data-part]"), function (p) {
      var fn = I.parts[p.getAttribute("data-part")];
      if (!fn) return;
      var h = fn();
      if (h === p._h) return;
      /* On ne remplace jamais une partie où l'on est en train de glisser ou d'écrire */
      var inside = act && p.contains(act);
      if (inside && ((act.type === "range" && DRAG.on) || ((act.tagName === "INPUT" && act.type !== "range" && act.type !== "checkbox") || act.tagName === "TEXTAREA"))) { syncInputs(I, p); return; }
      var key = inside ? fkey(act) : null;
      /* Les éléments recréés prennent leur état tout de suite, sans fondu depuis zéro */
      p.classList.add("lu-still");
      stills.push(p);
      p.innerHTML = h;
      p._h = p.innerHTML;
      if (key) {
        var b = [].filter.call(p.querySelectorAll("button, input"), function (x) { return fkey(x) === key; })[0];
        if (b) b.focus({ preventScroll: true });
      }
    });
    fitAll(I);
    paintAll(I);
    /* Un dialogue ouvert reçoit le focus (clavier et lecteurs d'écran) */
    var dlg = I.el.querySelector(".lu-dlg");
    if (dlg && !dlg.contains(document.activeElement)) { var fb = dlg.querySelector(".lu-btn-pri") || dlg.querySelector("button"); if (fb) fb.focus({ preventScroll: true }); }
    if (stills.length) requestAnimationFrame(function () { requestAnimationFrame(function () { stills.forEach(function (p) { p.classList.remove("lu-still"); }); }); });
  }
  function fkey(x) { return ["data-a", "data-r", "data-q", "data-n", "data-x", "data-v"].map(function (n) { return x.getAttribute(n) || ""; }).join("|"); }
  /* Glissement en cours sur un curseur (souris ou doigt) : le rendu attend qu'on relâche */
  var DRAG = { on: false };
  document.addEventListener("pointerdown", function (ev) { if (ev.target && ev.target.type === "range" && ev.target.closest(".lu")) DRAG.on = true; }, true);
  ["pointerup", "pointercancel"].forEach(function (t) { document.addEventListener(t, function () { if (DRAG.on) { DRAG.on = false; SUBS.forEach(function (u) { u.queue(); }); } }, true); });
  function syncInputs(I, p) {
    /* Pendant un glissement, seules les valeurs affichées suivent (pas de nouveau rendu) */
    [].forEach.call(p.querySelectorAll("[data-out]"), function (o) {
      var f = OUT[o.getAttribute("data-out")];
      if (f) o.textContent = f(I, o.getAttribute("data-v"));
    });
  }
  var OUT = {
    zlvl: function (I) { var z = I.e.Z[I.scr.z]; return zoneLvl(I.e, z, V(I, "cur")) + PC; },
    llvl: function (I, lk) { return S(I.k).lights[lk].lvl + PC; }
  };

  /* ---------------------------------------------------------------- barre du module */
  function topBar(I) {
    var n = I.scr.n, lib = n === "lib";
    var tab = function (a, label, on) { return '<button type="button" class="lu-tab' + (on ? " is-on" : "") + '" data-a="' + a + '"' + (on ? ' aria-current="page"' : "") + ">" + label + "</button>"; };
    return '<div class="lu-bar"><nav class="lu-tabs" aria-label="Éclairage">' +
      tab("home", "Lumières", n === "home" || n === "zone") + tab("lib-amb", "Bibliothèque", lib && I.scr.tab !== "cfg") + tab("lib-cfg", "Mes configurations", lib && I.scr.tab === "cfg") +
      "</nav>" + part(I, "chip", function () { return chip(I); }, "div", "lu-bar-r") + "</div>";
  }
  function chip(I) {
    var s = S(I.k), unk = unknownLights(I.k), lab = stateLabel(I.k);
    var cls = s.busy ? "is-busy" : unk.length ? "is-warn" : s.mod || !s.origin || s.origin.t === "perso" ? "is-perso" : "is-ok";
    var h = '<span class="lu-state ' + cls + '" role="status"><i></i>' + esc(unk.length && !s.busy ? "À vérifier · " + unk.length + NB + (unk.length > 1 ? "lumières" : "lumière") : lab) + "</span>";
    if (s.prev) h += '<button type="button" class="lu-prevchip" data-a="restore" title="Revenir à votre éclairage précédent">' + ic("shield") + "<span>Précédent gardé</span></button>";
    return h;
  }

  /* ---------------------------------------------------------------- écrans */
  var SCREENS = {};

  /* 01-02 : Accueil lumières (Pièces / Vue du dessus) */
  SCREENS.home = function (I) {
    var e = I.e, g = greet();
    var h = '<header class="lu-head"><div><h2 class="lu-h1">' + g[0] + ", " + esc(data().user) + '.</h2><p class="lu-sub">' + g[1] + "</p></div>" +
      '<div class="lu-acts"><button type="button" class="lu-btn" data-a="all-on">Tout allumer</button><button type="button" class="lu-btn" data-a="all-off">Tout éteindre</button>' +
      '<button type="button" class="lu-btn lu-btn-wide" data-a="compose">' + ic("plus") + "<span>Choisir des lumières</span></button></div></header>";
    h += part(I, "alert", function () { return alertBar(I); });
    h += '<div class="lu-row lu-filters"><div class="lu-chips" role="group" aria-label="Filtrer par zone">' +
      '<button type="button" class="lu-chip' + (!I.filter ? " is-on" : "") + '" data-a="filter" data-v="" aria-pressed="' + !I.filter + '">Tous</button>' +
      e.zones.map(function (z) { var on = I.filter === z.k; return '<button type="button" class="lu-chip' + (on ? " is-on" : "") + '" data-a="filter" data-v="' + z.k + '" aria-pressed="' + on + '">' + esc(z.short || z.name) + "</button>"; }).join("") +
      '</div><div class="lu-seg" role="group" aria-label="Affichage"><button type="button" data-a="view" data-v="pieces" class="' + (I.view === "pieces" ? "is-on" : "") + '" aria-pressed="' + (I.view === "pieces") + '">' + ic("grid") + "<span>Pièces</span></button>" +
      '<button type="button" data-a="view" data-v="plan" class="' + (I.view === "plan" ? "is-on" : "") + '" aria-pressed="' + (I.view === "plan") + '">' + ic("map") + "<span>Vue du dessus</span></button></div></div>";
    h += I.view === "plan" ? planView(I) : rooms(I);
    h += ambStrip(I, { mode: "preview", title: "Les ambiances" });
    return h;
  };
  function alertBar(I) {
    var s = S(I.k), unk = unknownLights(I.k);
    if (s.busy && s.tx) {
      var c = counts(s.tx), tot = s.tx.changes.length;
      return '<div class="lu-alert is-busy"><span class="lu-spin"></span><p><b>Application en cours</b> · ' + c.confirmed + " sur " + tot + ' confirmées</p><button type="button" class="lu-link" data-a="res">Suivre</button></div>';
    }
    if (unk.length) {
      return '<div class="lu-alert is-warn">' + ic("warn") + "<p><b>" + (unk.length > 1 ? words(unk.length) + " lumières restent à vérifier." : "Une lumière reste à vérifier.") + "</b> " +
        esc(cap(list(unk.map(function (l) { return l.the; })))) + (unk.length > 1 ? " ne répondent pas." : " ne répond pas.") + '</p><button type="button" class="lu-btn lu-btn-sm" data-a="res">Voir le détail</button></div>';
    }
    return "";
  }
  function rooms(I) {
    var e = I.e, cur = V(I, "cur"), main = e.Z[e.main];
    var zs = I.filter ? [e.Z[I.filter]] : e.zones;
    var inside = zs.filter(function (z) { return !z.out && z.k !== e.main; }), outs = zs.filter(function (z) { return z.out; });
    var showMain = !I.filter || I.filter === e.main;
    var bigZone = showMain ? main : (!I.filter ? null : e.Z[I.filter]);
    if (I.filter && I.filter !== e.main) { bigZone = e.Z[I.filter]; inside = []; outs = []; }
    var side = inside.slice(0, 4), more = inside.slice(4);
    var sideOuts = side.length <= 2 ? outs.slice(0, 2) : [], restOuts = outs.slice(sideOuts.length);
    var h = '<div class="lu-rooms' + (I.filter ? " is-one" : "") + '">';
    if (bigZone) h += roomCard(I, bigZone, cur, true);
    if (side.length || sideOuts.length) {
      h += '<div class="lu-side">' + (side.length ? '<div class="lu-cards n' + side.length + '">' + side.map(function (z, i) { return roomCard(I, z, cur, false, side.length % 2 && i === side.length - 1); }).join("") + "</div>" : "") +
        sideOuts.map(function (z) { return outRow(I, z, cur); }).join("") + "</div>";
    }
    h += "</div>";
    if (more.length) h += '<div class="lu-more">' + more.map(function (z) { return roomCard(I, z, cur); }).join("") + "</div>";
    if (restOuts.length) h += '<div class="lu-outs">' + restOuts.map(function (z) { return outRow(I, z, cur); }).join("") + "</div>";
    return h;
  }
  function zoneVisual(I, z, V0, size, cls) {
    if (I.e.key === "boulance") return phHTML(I.e, z, V0, size);
    return planHTML(I.e, "cur", { crop: "zone:" + z.k, fill: true, cls: cls });
  }
  function roomCard(I, z, cur, big, wide) {
    var e = I.e;
    return '<article class="lu-card' + (big ? " is-big" : "") + (wide ? " is-wide" : "") + '" data-src="cur">' +
      '<button type="button" class="lu-card-hit" data-a="zone" data-v="' + z.k + '" aria-label="Ouvrir ' + esc(z.name) + '"></button>' +
      zoneVisual(I, z, cur, big ? "l" : "m") + '<i class="lu-card-shade" aria-hidden="true"></i>' +
      part(I, "card-" + z.k, function () { return cardInfo(I, z, big); }, "div", "lu-card-info") + "</article>";
  }
  function cardInfo(I, z, big) {
    var e = I.e, s = S(I.k), cur = V(I, "cur"), on = zoneOn(e, z, cur), ls = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; });
    var pend = ls.some(function (l) { return s.lights[l.k].conf === "pending"; }), unk = ls.some(function (l) { return s.lights[l.k].conf === "unknown"; });
    var d = zoneDot(e, z, cur);
    var h = '<div class="lu-card-top">' + (ls.length ? sw(on, "zone-sw", z.k, (on ? "Éteindre " : "Allumer ") + z.the, false, pend) : '<span class="lu-lockchip">' + ic("lock") + "Réglementaire</span>") + "</div>";
    h += '<div class="lu-card-txt"><h3>' + esc(z.name) + '</h3><p class="lu-ambt">' + (d ? '<i class="lu-dot" style="background:' + d + '"></i>' : "") + esc(zoneAmb(e, z, cur)) +
      (unk ? ' <em class="lu-warnt">· à vérifier</em>' : "") + "</p></div>";
    h += '<span class="lu-card-go" aria-hidden="true">' + ic(big ? "arrow" : "right") + "</span>";
    return h;
  }
  function outRow(I, z, cur) {
    var e = I.e;
    return '<article class="lu-out" data-src="cur"><button type="button" class="lu-card-hit" data-a="zone" data-v="' + z.k + '" aria-label="Ouvrir ' + esc(z.name) + '"></button>' +
      '<div class="lu-out-pic">' + (e.key === "boulance" ? phHTML(e, z, cur, "s") : planHTML(e, "cur", { crop: "zone:" + z.k, fill: true })) + "</div>" +
      part(I, "out-" + z.k, function () {
        var c = V(I, "cur"), ls = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; }), on = zoneOn(e, z, c), s = S(I.k);
        var pend = ls.some(function (l) { return s.lights[l.k].conf === "pending"; });
        return '<div class="lu-out-txt"><h3>' + esc(z.name) + "</h3><p>" + esc(zoneAmb(e, z, c)) + "</p></div>" +
          (ls.length ? '<div class="lu-out-sw">' + sw(on, "zone-sw", z.k, (on ? "Éteindre " : "Allumer ") + z.the, false, pend) + "</div>" : '<span class="lu-lockchip">' + ic("lock") + "Réglementaire</span>");
      }, "div", "lu-out-info") + "</article>";
  }
  function planView(I) {
    var e = I.e;
    return '<div class="lu-planview' + (e.zones.length > 6 ? " is-wide" : "") + '"><div class="lu-stage lu-rim">' + planHTML(e, "cur", { labels: "zone", click: true }) + "</div>" +
      '<aside class="lu-panel lu-yours"><h3 class="lu-h3">Vos lumières</h3>' + part(I, "yours", function () {
        var cur = V(I, "cur"), s = S(I.k);
        return '<ul class="lu-list">' + e.zones.filter(function (z) { return !I.filter || I.filter === z.k; }).map(function (z) {
          var ls = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; }), on = zoneOn(e, z, cur), d = zoneDot(e, z, cur);
          var pend = ls.some(function (l) { return s.lights[l.k].conf === "pending"; });
          return '<li><button type="button" class="lu-li-main" data-a="zone" data-v="' + z.k + '"><i class="lu-dot" style="background:' + (d || "#5a5650") + '"></i><span><b>' + esc(z.name) + "</b><small>" + esc(zoneAmb(e, z, cur)) + "</small></span></button>" +
            (ls.length ? '<span class="lu-li-sw">' + sw(on, "zone-sw", z.k, (on ? "Éteindre " : "Allumer ") + z.the, false, pend) + "</span>" : '<span class="lu-lockchip">' + ic("lock") + "Fixe</span>") + "</li>";
        }).join("") + "</ul>";
      }) + "</aside></div>";
  }

  /* Bande d'ambiances (accueil, zone, compositeur) */
  function ambStrip(I, o) {
    var e = I.e;
    var h = '<section class="lu-strip"><div class="lu-strip-head"><h3 class="lu-h2">' + (o.title || "Les ambiances") + "</h3>" +
      (o.sub ? part(I, "strip-sub", function () { return esc(o.sub()); }, "p", "lu-for") : "") +
      '<div class="lu-strip-tools"><label class="lu-search">' + ic("search") + '<input type="search" placeholder="Rechercher une ambiance" aria-label="Rechercher une ambiance" data-q="strip" value="' + esc(I.q) + '"></label>' +
      '<button type="button" class="lu-fav' + (I.favOnly ? " is-on" : "") + '" data-a="fav-only" aria-pressed="' + I.favOnly + '">' + ic("heart") + "<span>Favoris</span></button>" +
      '<button type="button" class="lu-link" data-a="lib-amb">Tout voir ' + ic("arrow") + "</button></div></div>";
    h += part(I, "strip", function () {
      var list0 = filterAmbs(I.q, I.favOnly, null, o.mode === "preview" && !!I.q);
      if (!list0.length) return '<p class="lu-empty">' + (I.favOnly && !I.q ? "Aucun favori pour l’instant. Touchez " + ic("heart", "lu-i-in") + " sur une ambiance." : "Aucune ambiance ne correspond à « " + esc(I.q) + " ».") + "</p>";
      var sel = o.sel ? o.sel() : null;
      return '<div class="lu-amb-row" role="list">' + list0.map(function (a) {
        var on = sel === a.k;
        return '<button type="button" role="listitem" class="lu-amb' + (on ? " is-sel" : "") + '" data-a="' + o.mode + '" data-v="' + a.k + '"' + (on ? ' aria-current="true"' : "") + ">" +
          '<span class="lu-amb-pic">' + ambThumb(e, a.k, "s") + (on ? '<i class="lu-amb-ck">' + ic("check") + "</i>" : "") + "</span>" +
          '<span class="lu-amb-name">' + ambDot(a.k) + esc(a.name) + "</span></button>";
      }).join("") + "</div>";
    });
    return h + "</section>";
  }

  /* 03-04 : Détail d'une zone */
  SCREENS.zone = function (I) {
    var e = I.e, z = e.Z[I.scr.z], ctrl = e.zl[z.k].some(function (l) { return l.kind !== "regl"; });
    if (I.scr.apart == null) I.scr.apart = false;
    var h = '<button type="button" class="lu-back" data-a="back">' + ic("left") + "<span>Toutes les lumières</span></button>";
    h += '<header class="lu-head lu-head-z"><div class="lu-titlez"><h2 class="lu-h1">' + esc(z.name) + "</h2>" + part(I, "ztag", function () {
      return '<p class="lu-sub">' + esc(I.scr.apart && z.tagApart ? z.tagApart : z.tag) + "</p>";
    }) + "</div>" + (ctrl ? '<div class="lu-acts"><button type="button" class="lu-btn" data-a="compose" data-v="' + z.k + '">Choisir des lumières</button></div>' : "") + "</header>";
    h += '<div class="lu-zgrid"><div class="lu-hero lu-rim" data-src="zprev">' + (e.key === "boulance" ? phHTML(e, z, V(I, "zprev"), "l") : planHTML(e, "zprev", { crop: "zone:" + z.k, fill: true })) +
      '<i class="lu-hero-shade" aria-hidden="true"></i>' + part(I, "zcap", function () { return heroCap(I, z); }, "div", "lu-hero-cap") + "</div>" +
      '<aside class="lu-panel lu-now">' + part(I, "znow", function () { return nowPanel(I, z); }) + "</aside></div>";
    if (ctrl) {
      h += ambStrip(I, { mode: "zprev", sel: function () { return I.scr.pa || zoneMainAmb(I, z); } });
      h += part(I, "zbar", function () { return zoneBar(I, z); }, "div", "lu-dock-wrap");
    }
    return h;
  };
  function zoneMainAmb(I, z) {
    var cur = V(I, "cur"), ls = I.e.zl[z.k].filter(function (l) { return l.kind !== "regl"; });
    var on = ls.filter(function (l) { return cur[l.k].on; })[0];
    return on ? cur[on.k].amb : null;
  }
  function heroCap(I, z) {
    var e = I.e, a = I.scr.pa || zoneMainAmb(I, z), on = zoneOn(e, z, V(I, "cur")), A = AMB[a];
    var chipTxt = I.scr.pa && I.scr.pa !== zoneMainAmb(I, z) ? "Aperçu · " + AMB[I.scr.pa].name : on ? "En place · " + (A ? A.name : "") : "Éteint";
    var fixedOnly = e.zl[z.k].every(function (l) { return l.kind === "regl"; });
    if (fixedOnly) chipTxt = "Réglementaire";
    var t1 = A ? A.title : "Éteint pour l’instant.", t2 = A ? A.cap : "Touchez « On » ou choisissez une ambiance.";
    if (I.scr.apart && z.titleApart) { t1 = z.titleApart; t2 = z.capApart; }
    if (fixedOnly) { var l0 = e.zl[z.k][0]; t1 = l0.name; t2 = l0.mode + " · jamais modifiés par une ambiance."; }
    if (!on && !I.scr.pa && !fixedOnly) { t1 = "Éteint pour l’instant."; t2 = "Touchez « On » ou choisissez une ambiance ci-dessous."; }
    return '<span class="lu-pill' + (I.scr.pa ? " is-prev" : "") + '"><i></i>' + esc(chipTxt) + "</span><div><p class=\"lu-hero-t\">" + esc(t1) + '</p><p class="lu-hero-s">' + esc(t2) + "</p></div>";
  }
  function nowPanel(I, z) {
    var e = I.e, s = S(I.k), ls = e.zl[z.k], ctrl = ls.filter(function (l) { return l.kind !== "regl"; }), fixed = ls.filter(function (l) { return l.kind === "regl"; });
    var cur = V(I, "cur"), on = zoneOn(e, z, cur), pend = ctrl.some(function (l) { return s.lights[l.k].conf === "pending"; });
    var h = '<div class="lu-now-head"><h3 class="lu-h3">Lumière actuelle</h3>' + (ctrl.length && !(I.scr.apart && ctrl.length > 1) ? '<span class="lu-swbox">' + sw(on, "zone-sw", z.k, (on ? "Éteindre " : "Allumer ") + z.the, false, pend) + "</span>" : "") + "</div>";
    var slider = function (val, r, v, label, max) {
      return '<input type="range" min="1" max="' + (max || 100) + '" step="1" value="' + val + '" data-r="' + r + '" data-v="' + v + '" aria-label="' + esc(label) + '" style="--p:' + (val / (max || 100) * 100).toFixed(1) + '%">' +
        '<div class="lu-range-l"><span>Douce</span><span>Vive</span></div>';
    };
    if (ctrl.length > 1 && I.scr.apart) {
      ctrl.forEach(function (l) {
        var v = s.lights[l.k];
        h += '<div class="lu-now-row"><div class="lu-now-l">' + ic("sun") + "<b>" + esc(l.short || l.name) + '</b><span class="lu-val" data-out="llvl" data-v="' + l.k + '">' + (v.on ? v.lvl + PC : "Éteint") + "</span>" +
          '<span class="lu-swbox">' + sw(v.on, "light-sw", l.k, (v.on ? "Éteindre " : "Allumer ") + l.the, false, v.conf === "pending") + "</span></div>" +
          slider(v.lvl, "light", l.k, "Luminosité : " + (l.short || l.name), l.cap && l.cap[0]) + (l.cap ? '<p class="lu-note">' + ic("lock") + esc(l.cap[1]) + "</p>" : "") + "</div>";
      });
      h += '<div class="lu-now-row lu-now-grp"><p class="lu-note">' + esc(z.group.apart) + '</p><button type="button" class="lu-link" data-a="apart" data-v="0">Régler ensemble</button></div>';
    } else if (ctrl.length) {
      var lvl = zoneLvl(e, z, cur) || Math.round(ctrl.reduce(function (t, l) { return t + (s.lights[l.k].last || 60); }, 0) / ctrl.length);
      var capL = ctrl.filter(function (l) { return l.cap; })[0];
      h += '<div class="lu-now-row"><div class="lu-now-l">' + ic("sun") + '<b>Luminosité</b><span class="lu-val" data-out="zlvl">' + (on ? lvl + PC : "Éteint") + "</span></div>" + slider(lvl, "zone", z.k, "Luminosité : " + z.name, capL && capL.cap[0]) +
        (capL ? '<p class="lu-note">' + ic("lock") + esc(capL.cap[1]) + "</p>" : "") + "</div>";
      if (ctrl.length > 1) {
        var lv0 = ctrl.map(function (l) { return s.lights[l.k]; });
        var differ = lv0.some(function (v) { return v.on !== lv0[0].on || (v.on && (v.lvl !== lv0[0].lvl || v.amb !== lv0[0].amb)); });
        h += '<div class="lu-now-row lu-now-grp"><div class="lu-now-l">' + ic("bands") + "<b>" + esc(z.group.together) + '</b></div><p class="lu-note">' + esc(z.group.same) +
          (differ ? " Actuellement : " + ctrl.map(function (l) { return (l.short || l.name).toLowerCase() + " " + (s.lights[l.k].on ? s.lights[l.k].lvl + PC : "éteinte"); }).join(", ") + "." : "") +
          '</p><button type="button" class="lu-link" data-a="apart" data-v="1">Régler séparément</button></div>';
      }
    }
    fixed.forEach(function (l) {
      h += '<div class="lu-now-row lu-fixed"><div class="lu-now-l">' + ic("lock") + "<b>" + esc(l.name) + '</b><span class="lu-val">' + esc(l.mode) + '</span></div><p class="lu-note">' + esc(l.fixed) + "</p></div>";
    });
    var a = I.scr.pa || zoneMainAmb(I, z);
    if (a && ctrl.length) {
      var A = AMB[a], adapted = ctrl.map(function (l) { return adapt(l, a).note; }).filter(Boolean);
      h += '<div class="lu-now-amb"><i class="lu-swatch" style="background:' + (A.c2 ? "linear-gradient(135deg," + A.c + "," + A.c2 + ")" : A.c) + '"></i><div><b>' + esc(A.name) + "</b><small>" +
        (I.scr.pa && I.scr.pa !== zoneMainAmb(I, z) ? "L’ambiance en aperçu · rien n’est envoyé" : "L’ambiance actuelle") + (adapted.length ? " · " + esc(adapted[0]) : "") + "</small></div>" + heart(a) + "</div>";
    }
    return h;
  }
  function zoneBar(I, z) {
    var e = I.e, ctrl = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; });
    if (!ctrl.length) return "";
    var pa = I.scr.pa, pl = pa ? zonePlan(I.k, z.k, pa) : null, n = pl ? pl.changes.length : 0, s = S(I.k);
    var note = !pa ? "Choisissez une ambiance ci-dessous : l’aperçu n’envoie rien." : !n ? AMB[pa].name + " est déjà en place " + z.in + "." :
      pl.wake ? cap(z.the) + " s’allumera en " + AMB[pa].name + ". Les autres lumières restent comme elles sont." :
        pl.keep.length ? "Les autres lumières restent comme elles sont. " + cap(list(pl.keep.map(function (k) { return e.L[k].the; }))) +
          (pl.keep.length > 1 ? " restent " + off("fp") + "." : " reste " + off(e.L[pl.keep[0]].g) + ".") : "Les autres lumières restent comme elles sont.";
    return '<div class="lu-dock"><div class="lu-dock-t"><b>' + esc(z.name) + " seulement</b><p>" + esc(note) + "</p></div>" +
      '<div class="lu-dock-a"><button type="button" class="lu-btn lu-btn-pri" data-a="zone-apply"' + (n && !s.busy ? "" : " disabled") + ">Appliquer " + esc(au(z.the)) + "</button></div></div>";
  }

  /* 05, 09 : Bibliothèque */
  SCREENS.lib = function (I) {
    var cfg = I.scr.tab === "cfg";
    var h = '<header class="lu-head"><div><h2 class="lu-h1">Bibliothèque</h2><p class="lu-sub">' +
      (cfg ? "Une configuration garde les " + words(I.e.ctrl.length) + " lumières, pas seulement un style." : "Des styles à explorer. Vos éclairages à retrouver.") + "</p></div>" +
      (cfg ? '<div class="lu-acts"><button type="button" class="lu-btn" data-a="save-open">Enregistrer l’éclairage actuel</button></div>' :
        '<label class="lu-search lu-search-big">' + ic("search") + '<input type="search" placeholder="Rechercher une ambiance" aria-label="Rechercher une ambiance" data-q="lib" value="' + esc(I.scr.q || "") + '"></label>') + "</header>";
    h += '<div class="lu-row"><div class="lu-seg lu-seg-tabs" role="group" aria-label="Bibliothèque"><button type="button" data-a="lib-amb" class="' + (!cfg ? "is-on" : "") + '" aria-pressed="' + !cfg + '">Ambiances</button>' +
      '<button type="button" data-a="lib-cfg" class="' + (cfg ? "is-on" : "") + '" aria-pressed="' + cfg + '">Mes configurations</button></div>';
    if (!cfg) {
      h += '<div class="lu-chips" role="group" aria-label="Filtres">' + [["fav", "Favoris"], ["chaleureuses", "Chaleureuses"], ["colorees", "Colorées"], ["douces", "Douces"]].map(function (f) {
        var on = I.scr.f === f[0];
        return '<button type="button" class="lu-chip' + (on ? " is-on" : "") + '" data-a="lib-f" data-v="' + f[0] + '" aria-pressed="' + on + '">' + (f[0] === "fav" ? ic("heart", "lu-i-in") : "") + f[1] + "</button>";
      }).join("") + "</div>";
    }
    h += "</div>";
    if (!cfg) {
      h += part(I, "libgrid", function () { return libGrid(I); });
      h += '<button type="button" class="lu-discover" data-a="preview" data-v="signature"><b>Découvrir Signature</b><span>Un style pour ' + esc(I.e.all) + ", sans perdre votre éclairage.</span>" + ic("arrow") + "</button>";
    } else {
      h += '<div class="lu-cfggrid"><div class="lu-cfglist">' + part(I, "cfglist", function () { return cfgList(I); }) + "</div>" +
        '<aside class="lu-panel lu-cfgside">' + part(I, "cfgside", function () { return cfgSide(I); }) + "</aside></div>";
    }
    return h;
  };
  function libGrid(I) {
    var e = I.e, f = I.scr.f, items = filterAmbs(I.scr.q || "", f === "fav", f && f !== "fav" ? f : null, !!I.scr.q);
    if (!items.length) return '<p class="lu-empty">' + (f === "fav" ? "Aucun favori pour l’instant. Touchez " + ic("heart", "lu-i-in") + " sur une ambiance." : "Aucune ambiance ne correspond. Essayez un autre mot.") + "</p>";
    return '<div class="lu-libgrid">' + items.map(function (a) {
      var vis = e.key === "boulance" ? '<img src="' + ambPhoto(a.k, "m") + '" alt="" loading="lazy" decoding="async" draggable="false">' : planHTML(e, "amb:" + a.k, { fill: true });
      return '<article class="lu-libcard"><button type="button" class="lu-card-hit" data-a="preview" data-v="' + a.k + '" aria-label="Aperçu : ' + esc(a.name) + '"></button>' +
        '<div class="lu-libpic">' + vis + "</div>" + heart(a.k) +
        '<div class="lu-libtxt"><h3>' + ambDot(a.k) + esc(a.name) + "</h3><p>" + esc(a.desc) + "</p></div>" + '<span class="lu-card-go" aria-hidden="true">' + ic("arrow") + "</span></article>";
    }).join("") + "</div>";
  }
  function cfgThumb(e, c) {
    if (e.key === "boulance") {
      var lead = c.lights["couloir-g"] || c.lights["couloir-d"];
      return '<img src="' + ambPhoto(lead ? lead.amb : "heure-doree", "s") + '" alt="" loading="lazy" decoding="async">';
    }
    return planHTML(e, "cfg:" + c.k, { fill: true });
  }
  function cfgList(I) {
    var e = I.e, s = S(I.k), h = "", o = s.origin;
    if (o && o.t === "cfg" && s.mod) {
      var oc = cfgOf(s, o.k);
      if (oc) h += '<div class="lu-modcard"><h3>' + esc(oc.name) + ' · modifiée</h3><p class="lu-gold">Personnalisé · non enregistré</p><small>La version enregistrée n’a pas changé.</small></div>';
    }
    if (!s.configs.length) h += '<p class="lu-empty">Aucune configuration pour l’instant.</p>';
    h += s.configs.map(function (c) {
      var n = Object.keys(c.lights).length, rec = o && o.t === "cfg" && o.k === c.k;
      return '<article class="lu-cfg"><div class="lu-cfgpic">' + cfgThumb(e, c) + '</div><div class="lu-cfgtxt"><h3>' + esc(c.name) + "</h3><p>" + plural(n, "lumière", "lumières") +
        (c.inc && c.inc.length ? ' · <em class="lu-warnt">incomplète</em>' : "") + " · " + (rec ? "configuration rappelée" : "enregistrée") + (c.v > 1 ? " · version " + c.v : "") + "</p>" +
        '<button type="button" class="lu-btn lu-btn-sm" data-a="recall" data-v="' + c.k + '"' + (s.busy ? " disabled" : "") + ">Rappeler</button></div>" +
        '<button type="button" class="lu-heart' + (c.fav ? " is-on" : "") + '" data-a="cfg-fav" data-v="' + c.k + '" aria-pressed="' + !!c.fav + '" aria-label="Favori : ' + esc(c.name) + '">' + ic("heart") + "</button></article>";
    }).join("");
    return h;
  }
  function cfgSide(I) {
    var e = I.e, s = S(I.k), o = s.origin;
    if (I.saveOpenCfg) return savePanel(I, "cfg");
    if (o && o.t === "cfg" && s.mod) {
      var c = cfgOf(s, o.k);
      if (c) {
        var diffs = e.ctrl.filter(function (l) { return c.lights[l.k] && !same(c.lights[l.k], s.lights[l.k]); });
        var others = e.ctrl.length - diffs.length;
        return '<h3 class="lu-h2">Garder vos ajustements ?</h3><p class="lu-sub2">Configuration rappelée : ' + esc(c.name) + "</p>" +
          '<div class="lu-mini-plan">' + planHTML(e, "cur") + "</div>" +
          diffs.map(function (l) {
            return '<div class="lu-diff"><b>' + esc(l.name) + '</b><p><span>Enregistré : ' + esc(vText(l, c.lights[l.k])) + "</span>" + ic("arrow") + '<span class="lu-gold">Actuel : ' + esc(vText(l, s.lights[l.k])) + "</span></p></div>";
          }).join("") +
          (others ? '<p class="lu-note">' + (others > 1 ? "Les " + words(others) + " autres lumières sont inchangées." : "L’autre lumière est inchangée.") + "</p>" : "") +
          '<p class="lu-ask">Choisissez comment enregistrer cette version.</p>' +
          '<div class="lu-stack"><button type="button" class="lu-btn" data-a="cfg-update" data-v="' + c.k + '">Mettre à jour ' + esc(c.name) + '</button><button type="button" class="lu-btn lu-btn-pri" data-a="cfg-copy" data-v="' + c.k + '">Enregistrer une copie</button></div>';
      }
    }
    return '<h3 class="lu-h2">Comment ça fonctionne</h3><ul class="lu-rules">' +
      "<li><b>Une ambiance est un style.</b> Une configuration garde chaque lumière : allumée ou non, intensité, couleur.</li>" +
      "<li><b>Rappeler montre d’abord ce qui change.</b> Ce qui s’allume, ce qui s’éteint. Rien n’est envoyé avant votre accord.</li>" +
      "<li><b>Votre éclairage est protégé.</b> Avant toute application, l’éclairage actuel est gardé comme précédent.</li>" +
      "<li><b>Rien ne change en silence.</b> Une configuration enregistrée ne bouge que si vous la mettez à jour.</li></ul>" +
      prevBox(I);
  }
  function prevBox(I) {
    var s = S(I.k);
    if (!s.prev) return '<p class="lu-note">Aucun éclairage précédent pour l’instant : il sera gardé à la prochaine application.</p>';
    return '<div class="lu-prevbox">' + ic("shield") + "<div><b>Votre éclairage précédent est gardé.</b><small>" + esc(s.prev.label) + (s.prev.before ? " · avant " + esc(s.prev.before) : "") + '</small></div><button type="button" class="lu-btn lu-btn-sm" data-a="restore">Revenir</button></div>';
  }
  function suggestName(I) {
    var e = I.e, s = S(I.k), ws = [];
    e.ctrl.forEach(function (l) { var v = s.lights[l.k]; if (v.on) { var w = AMB[v.amb].word; if (ws.indexOf(w) < 0) ws.push(w); } });
    var n = ws.length >= 2 ? cap(ws[0]) + " et " + ws[1].toLowerCase() : ws.length ? cap(ws[0]) + " · " + e.name : "Tout éteint";
    return uniqueName(s, n);
  }
  function savePanel(I, where) {
    var e = I.e, s = S(I.k), snapC = confirmedSnap(I.k);
    var name = I.saveName != null ? I.saveName : suggestName(I);
    return '<div class="lu-save-head"><h3 class="lu-h2">Enregistrer l’éclairage actuel</h3><span class="lu-k">Facultatif</span></div>' +
      '<label class="lu-field"><span>Nom de la configuration</span><input type="text" maxlength="40" data-n="save" value="' + esc(name) + '" autocomplete="off"></label>' +
      '<p class="lu-k2">Les ' + words(e.ctrl.length) + " lumières mémorisées</p>" +
      '<ul class="lu-mem">' + e.ctrl.map(function (l) {
        var v = s.lights[l.k], unk = v.conf !== "ok";
        return '<li><span class="lu-thumb">' + lightThumb(e, l, v) + "</span><span><b>" + esc(l.name) + '</b><small style="color:' + (unk ? "var(--lu-warn)" : v.on ? mix(dot(l, v), "#ffffff", .35) : "var(--lu-muted)") + '">' +
          esc(unk ? "Non confirmée · ne sera pas mémorisée" : vLong(l, v)) + "</small></span></li>";
      }).join("") + "</ul>" +
      (snapC.inc.length ? '<p class="lu-note lu-warnt">' + ic("warn") + "Capture incomplète : " + esc(list(snapC.inc.map(function (k) { return e.L[k].the; }))) + " n’a pas confirmé son état. La configuration ne pourra pas tout restaurer.</p>" :
        '<p class="lu-note">Couleurs, effets et paramètres disponibles inclus. Seules les valeurs confirmées sont enregistrées.</p>') +
      (I.saveErr ? '<p class="lu-note lu-warnt">' + esc(I.saveErr) + "</p>" : "") +
      '<div class="lu-row-end"><button type="button" class="lu-btn" data-a="save-close" data-v="' + where + '">Pas maintenant</button><button type="button" class="lu-btn lu-btn-pri" data-a="save" data-v="' + where + '">Enregistrer</button></div>';
  }

  /* 06-07 : Composer puis vérifier (brouillon : rien n'est envoyé) */
  SCREENS.compose = function (I) {
    var e = I.e, sc = I.scr;
    var h = part(I, "chead", function () {
      var pl = draftPlan(I.k, sc.draft), n = pl.changes.length;
      var title = sc.cfg ? "Rappeler « " + cfgOf(S(I.k), sc.cfg).name + " »" : sc.verify ? "Vérifiez votre éclairage" : "Composez votre éclairage";
      var sub = sc.verify || sc.cfg ? summary(I, pl) : stateLabel(I.k);
      return '<header class="lu-head"><div><h2 class="lu-h1">' + esc(title) + '</h2><p class="lu-sub">' + esc(sub) + "</p></div>" +
        '<div class="lu-same"><button type="button" class="lu-btn lu-btn-wide" data-a="same-all">Même ambiance partout</button><small>Préparer pour les ' + e.ctrl.length + NB + "lumières<br>Les lumières éteintes le restent.</small></div></header>";
    });
    h += '<div class="lu-cgrid"><section class="lu-csel">' + part(I, "csel-h", function () {
      return '<div class="lu-row-sb"><h3 class="lu-h2"><span class="lu-n">1</span>Choisissez les lumières</h3>' + (sc.verify ? '<button type="button" class="lu-link" data-a="draft-edit">Modifier</button>' : "") + "</div>";
    }) + part(I, "crows", function () { return composeRows(I); }) + "</section>" +
      '<section class="lu-crep"><div class="lu-crep-head"><h3 class="lu-h2">Votre répartition</h3><span class="lu-pill is-draft"><i></i>Brouillon</span></div>' +
      '<div class="lu-stage lu-rim">' + planHTML(e, "draft", { labels: "amb" }) + "</div>" +
      part(I, "cnote", function () { return '<p class="lu-cnote' + (sc.verify ? " is-safe" : "") + '">' + (sc.verify ? ic("shield") + "Votre éclairage actuel sera protégé avant toute commande." : esc(draftSentence(I))) + "</p>"; }) +
      ambStrip(I, {
        mode: "draft", title: '<span class="lu-n">2</span>Choisissez une ambiance', sub: function () { return selFor(I); },
        sel: function () { var k0 = sc.sel[0]; return k0 && sc.draft[k0] ? sc.draft[k0].amb : null; }
      }) + "</section></div>";
    h += part(I, "cbar", function () {
      var pl = draftPlan(I.k, sc.draft), n = pl.changes.length, same0 = e.ctrl.filter(function (l) { return !pl.changes.some(function (c) { return c.k === l.k; }); });
      var s = S(I.k), unk = unknownLights(I.k);
      return '<div class="lu-dock"><div class="lu-dock-t"><b>' + (n ? plural(n, "changement préparé", "changements préparés") : "Aucun changement préparé") + "</b><p>" +
        (unk.length ? "Une lumière n’a pas confirmé son état : réessayez-la avant d’appliquer." : same0.length ? esc(cap(list(same0.map(function (l) { return l.name.toLowerCase(); })))) + (same0.length > 1 ? " inchangés." : same0[0].g === "f" ? " inchangée." : " inchangé.") : "Toutes les lumières changent.") + "</p></div>" +
        '<div class="lu-dock-a"><button type="button" class="lu-btn" data-a="draft-cancel">Annuler le brouillon</button>' +
        (sc.verify || sc.cfg ? '<button type="button" class="lu-btn lu-btn-pri" data-a="draft-apply"' + (n && !s.busy && !unk.length ? "" : " disabled") + ">Appliquer les changements</button>" :
          '<button type="button" class="lu-btn lu-btn-pri" data-a="draft-verify"' + (n ? "" : " disabled") + ">Vérifier mon éclairage</button>") + "</div></div>";
    }, "div", "lu-dock-wrap");
    return h;
  };
  function selFor(I) {
    var e = I.e, sel = I.scr.sel;
    if (I.scr.verify) return "Touchez « Modifier » pour changer une ambiance";
    if (!sel.length) return "Touchez une lumière à gauche";
    if (sel.length === e.ctrl.length) return "Pour les " + sel.length + NB + "lumières";
    return "Pour " + list(sel.map(function (k) { return e.L[k].short || e.L[k].name; }));
  }
  function composeRows(I) {
    var e = I.e, s = S(I.k), sc = I.scr, verify = sc.verify || sc.cfg;
    return '<ul class="lu-crow-list">' + e.lights.map(function (l) {
      var cur = s.lights[l.k], d = sc.draft[l.k] || cur, fixed = l.kind === "regl", sel = sc.sel.indexOf(l.k) >= 0;
      var changed = !fixed && (cur.conf !== "ok" || !same(cur, d)), col = d.on ? mix(dot(l, d), "#ffffff", .3) : "var(--lu-muted)";
      var status, tag = "";
      if (fixed) status = "Réglementaire · jamais modifié";
      else if (verify) {
        tag = changed ? "À changer" : "Inchangé";
        status = changed ? '<span>' + esc(vText(l, cur, cur.conf === "unknown")) + "</span>" + ic("arrow") + '<span style="color:' + col + '">' + esc(vText(l, d)) + "</span>" :
          cur.on ? esc(vText(l, cur)) + " · inchangée" : "Restera " + off(l.g);
      } else if (changed) status = !cur.on && d.on ? "Préparé · s’allumera" : !d.on ? "Préparé · s’éteindra" : "Préparé · reste allumé";
      else if (sel) status = d.on ? "Choisie · " + esc(ambName(l, d.amb)) + " déjà en place" : "Choisie · éteinte";
      else status = d.on ? "Conserve son ambiance" : "Restera éteint";
      if (!fixed && !verify && sel && !d.on && sc.touched && sc.touched[l.k]) status = "Préparé · restera éteint";
      var note = !fixed && d.on && changed ? adapt(l, d.amb).note : "";
      return '<li class="lu-crow' + (sel && !verify ? " is-sel" : "") + (verify && changed ? " is-chg" : "") + (fixed ? " is-fixed" : "") + '">' +
        (fixed || verify ? "" : '<button type="button" class="lu-card-hit" data-a="draft-sel" data-v="' + l.k + '" aria-pressed="' + sel + '" aria-label="Choisir ' + esc(l.name) + '"></button>') +
        '<span class="lu-thumb">' + lightThumb(e, l, d) + "</span>" +
        '<div class="lu-crow-t"><b>' + esc(l.name) + '</b><span class="lu-crow-a" style="color:' + col + '">' + esc(fixed ? l.mode : d.on ? ambName(l, d.amb) : "Éteint") + "</span><small>" + status + (note ? " · " + esc(note) : "") + "</small></div>" +
        '<div class="lu-crow-r">' + (tag ? '<span class="lu-k' + (changed ? " lu-gold" : "") + '">' + tag + "</span>" : sel && !verify ? '<i class="lu-ck">' + ic("check") + "</i>" : "") +
        '<span class="lu-pct">' + (fixed ? ic("lock") : d.on ? d.lvl + PC : "Off") + "</span>" +
        (!fixed && !verify && sel && !d.on ? '<button type="button" class="lu-link lu-link-sm" data-a="draft-on" data-v="' + l.k + '">Allumer</button>' : "") +
        (!fixed && !verify && sel && d.on && changed && !cur.on ? '<button type="button" class="lu-link lu-link-sm" data-a="draft-offk" data-v="' + l.k + '">Laisser éteinte</button>' : "") + "</div></li>";
    }).join("") + "</ul>";
  }
  function draftSentence(I) {
    var e = I.e, sc = I.scr, s = S(I.k), bits = [];
    e.zones.forEach(function (z) {
      var ls = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; });
      if (!ls.length) return;
      var ch = ls.filter(function (l) { return !same(s.lights[l.k], sc.draft[l.k] || s.lights[l.k]); });
      var on = ls.filter(function (l) { return (sc.draft[l.k] || s.lights[l.k]).on; });
      if (!on.length) return;
      var a = ambName(on[0], (sc.draft[on[0].k] || s.lights[on[0].k]).amb);
      if (ch.length) bits.push(a + " " + z.in + ".");
      else if (ls.length > 1 && on.length > 1) bits.push(cap(z.group ? z.group.together.replace(/ ensemble$/, "") : z.the) + " gardent " + a + ".");
      else bits.push(a + " reste " + z.in + ".");
    });
    return bits.slice(0, 3).join(" ") || "Tout est éteint dans ce brouillon.";
  }
  function summary(I, pl) {
    var e = I.e, n = pl.changes.length, s = S(I.k);
    if (!n) return "Aucun changement : tout est déjà en place.";
    var on = pl.changes.filter(function (c) { return c.to.on && !s.lights[c.k].on; }).length, offc = pl.changes.filter(function (c) { return !c.to.on && s.lights[c.k].on; }).length;
    var zones = [];
    pl.changes.forEach(function (c) { var z = e.Z[e.L[c.k].zone]; if (zones.indexOf(z) < 0) zones.push(z); });
    var t = zones.length === 1 && pl.changes[0].to.on ? cap(zones[0].the) + " en " + ambName(e.L[pl.changes[0].k], pl.changes[0].to.amb) + (zones.length < e.zones.length ? ", les autres lumières inchangées." : ".") :
      plural(n, "lumière change", "lumières changent") + ".";
    if (on || offc) t += " " + (on ? plural(on, "s’allume", "s’allument") : "") + (on && offc ? ", " : "") + (offc ? plural(offc, "s’éteint", "s’éteignent") : "") + ".";
    return t;
  }

  /* 10 : Aperçu d'une ambiance (Signature ou autre) : rien n'est envoyé */
  SCREENS.preview = function (I) {
    var e = I.e, a = I.scr.a, A = AMB[a];
    if (!I.scr.extra) I.scr.extra = {};
    var h = '<button type="button" class="lu-back" data-a="back">' + ic("left") + "<span>Retour</span></button>";
    h += '<header class="lu-head"><div><h2 class="lu-h1">Ambiance ' + esc(A.name) + '</h2><p class="lu-sub">' + (A.style ? "Un style pour " + esc(e.all) + "." : esc(A.desc)) + ' Votre éclairage reste à vous.</p></div><span class="lu-pill is-prev"><i></i>Aperçu · aucun changement</span></header>';
    h += '<div class="lu-pgrid"><div class="lu-hero lu-rim">' + (e.key === "boulance" ? '<img class="lu-hero-img" src="' + ambPhoto(a, "l") + '" alt="Le couloir de BouLance en ambiance ' + esc(A.name) + '" decoding="async">' : planHTML(e, "ambp:" + a, { fill: true, labels: "amb" })) +
      '<i class="lu-hero-shade" aria-hidden="true"></i><div class="lu-hero-cap"><div><p class="lu-hero-t">' + esc(A.style ? A.name : A.title) + '</p><p class="lu-hero-s">' + esc(A.style ? A.desc : A.cap) + "</p></div></div></div>" +
      '<aside class="lu-panel lu-before"><h3 class="lu-h2">Avant d’appliquer</h3><p class="lu-sub2">Votre éclairage actuel</p><div class="lu-mini-plan">' + planHTML(e, "cur") + "</div>" +
      part(I, "pside", function () { return previewSide(I); }) + "</aside></div>";
    h += part(I, "pbar", function () {
      var pl = ambPlan(I.k, a, I.scr.extra), s = S(I.k), unk = unknownLights(I.k);
      var blocked = unk.length > 0;
      return '<div class="lu-dock' + (blocked ? " is-warn" : "") + '"><div class="lu-dock-t"><b>' + (blocked ? "Votre éclairage ne peut pas être protégé en entier." : "Votre éclairage précédent restera disponible.") + "</b><p>" +
        (blocked ? esc(cap(list(unk.map(function (l) { return l.the; })))) + " n’a pas confirmé son état : aucune commande ne sera envoyée. Réessayez-la d’abord." : "Même si vous fermez puis rouvrez JARVIS.") + "</p></div>" +
        '<div class="lu-dock-a"><button type="button" class="lu-btn" data-a="back">Fermer l’aperçu</button>' +
        (blocked ? '<button type="button" class="lu-btn lu-btn-pri" data-a="res">Voir la lumière à vérifier</button>' :
          '<button type="button" class="lu-btn lu-btn-pri" data-a="amb-apply"' + (pl.changes.length && !s.busy ? "" : " disabled") + ">" + (pl.changes.length ? "Appliquer " + esc(A.name) : "Rien à changer") + "</button>") + "</div></div>";
    }, "div", "lu-dock-wrap");
    return h;
  };
  function previewSide(I) {
    var e = I.e, a = I.scr.a, A = AMB[a], s = S(I.k), pl = ambPlan(I.k, a, I.scr.extra);
    var lit = e.ctrl.filter(function (l) { return s.lights[l.k].on || I.scr.extra[l.k]; });
    var h = '<p class="lu-state-n">' + esc(stateLabel(I.k)) + '</p><p class="lu-note">Cet éclairage sera gardé avant le changement. Vous pourrez y revenir.</p><hr>';
    h += '<p class="lu-gold lu-big">' + (lit.length ? plural(lit.length, "lumière allumée", "lumières allumées") + " · " + esc(A.tone || A.name) + " · " + A.lvl + PC : "Aucune lumière allumée") + "</p>";
    pl.notes.forEach(function (n) { h += '<p class="lu-note">' + esc(n.l.name) + " : " + esc(n.note) + "</p>"; });
    e.ctrl.forEach(function (l) {
      if (s.lights[l.k].on) return;
      var on = !!I.scr.extra[l.k];
      h += '<p class="lu-note">' + esc(l.name) + " : " + (on ? "s’allumera en " + esc(A.name) : "reste " + off(l.g)) + '</p><label class="lu-check"><input type="checkbox" data-x="' + l.k + '"' + (on ? " checked" : "") + "><span></span>Allumer aussi " + esc(l.the) + "</label>";
    });
    e.lights.forEach(function (l) { if (l.kind === "regl") h += '<p class="lu-note lu-fixednote">' + ic("lock") + esc(l.name) + " : réglementaires, jamais modifiés par une ambiance.</p>"; });
    return h;
  }

  /* 08, 11, 12 : Suivi d'une application, puis résultat confirmé lumière par lumière */
  SCREENS.res = function (I) {
    return part(I, "res", function () { return resBody(I); }, "div", "lu-stackp") + part(I, "resdock", function () { return resDock(I); }, "div", "lu-dock-wrap");
  };
  function resStatus(tx) {
    var c = counts(tx), fails = Object.keys(tx.res).filter(function (k) { return tx.res[k] === "fail"; });
    return { c: c, fails: fails, partial: tx.done && fails.length > 0, ok: tx.done && !fails.length && !tx.aborted };
  }
  function resBody(I) {
    var e = I.e, s = S(I.k), tx = s.tx;
    if (!tx) return '<header class="lu-head"><div><h2 class="lu-h1">Aucune application récente.</h2><p class="lu-sub">Choisissez une ambiance ou composez votre éclairage.</p></div></header>';
    var st = resStatus(tx), A = tx.amb ? AMB[tx.amb] : null, tot = tx.changes.length;
    var name = tx.kind === "amb" ? A.name : tx.kind === "config" ? tx.title : tx.kind === "zone" ? (A ? A.name + " " + e.Z[tx.zone].in : "") : "";
    var title, sub, badge, bcls;
    if (tx.aborted) {
      title = "Aucune commande envoyée.";
      sub = cap(list(tx.aborted.map(function (k) { return e.L[k].the; }))) + " n’a pas confirmé son état : votre éclairage ne peut pas être protégé en entier.";
      badge = "Rien n’a changé"; bcls = "is-warn";
    } else if (!tx.done) {
      title = tx.kind === "restore" ? "Retour à votre éclairage précédent…" : "Application en cours…";
      sub = (tx.kind === "restore" ? "" : "Votre éclairage précédent est protégé. ") + "Les lumières confirment une à une : " + st.c.confirmed + " sur " + tot + ".";
      badge = "En cours"; bcls = "is-busy";
    } else if (st.partial) {
      title = (tx.kind === "amb" ? A.name + " est partiellement appliquée." : tx.kind === "restore" ? "Votre éclairage précédent est revenu en partie." : "Votre éclairage est partiellement en place.");
      sub = plural(st.c.confirmed, "réglage confirmé", "réglages confirmés") + " sur " + tot + ". " + cap(list(st.fails.map(function (k) { return e.L[k].the; }))) + (st.fails.length > 1 ? " ne répondent pas." : " ne répond pas.");
      badge = "À vérifier"; bcls = "is-warn";
    } else if (tx.kind === "amb") {
      title = A.name + " est en place.";
      var kept = tx.keep.filter(function (k) { return !S(I.k).lights[k].on; });
      sub = plural(st.c.confirmed, "réglage confirmé", "réglages confirmés") + "." + (kept.length === 1 ? " " + cap(e.L[kept[0]].the) + " " + resta(e.L[kept[0]].g) + " " + off(e.L[kept[0]].g) + "." : kept.length > 1 ? " Les lumières éteintes le sont restées." : "");
      badge = "Application confirmée"; bcls = "is-ok";
    } else if (tx.kind === "restore") {
      title = "Votre éclairage précédent est revenu.";
      sub = plural(st.c.confirmed, "réglage confirmé", "réglages confirmés") + ". Le précédent reste gardé jusqu’à la prochaine application.";
      badge = "Retour confirmé"; bcls = "is-ok";
    } else {
      title = tx.kind === "config" ? tx.title + " est en place." : "Votre éclairage est en place.";
      sub = zoneSentences(I, tx);
      badge = "Changements appliqués"; bcls = "is-ok";
    }
    var h = '<header class="lu-head"><div><h2 class="lu-h1">' + esc(title) + '</h2><p class="lu-sub' + (st.partial || tx.aborted ? " lu-gold" : "") + '">' + esc(sub) + "</p>" +
      (st.partial ? '<p class="lu-k3">Cas de connexion interrompue</p>' : "") + '</div><span class="lu-pill ' + bcls + '"><i></i>' + badge + "</span></header>";
    if (!tx.done) h += '<div class="lu-progress" role="progressbar" aria-valuemin="0" aria-valuemax="' + tot + '" aria-valuenow="' + st.c.confirmed + '"><i style="width:' + (tot ? st.c.confirmed / tot * 100 : 100).toFixed(1) + '%"></i></div>';
    if (!tx.done || st.partial || tx.aborted) {
      h += '<div class="lu-rgrid"><section class="lu-panel lu-perlight"><h3 class="lu-h2">État confirmé, lumière par lumière</h3>' + perLight(I, tx) + "</section>" +
        '<aside class="lu-panel lu-prot">' + (s.prev ? '<h3 class="lu-h2">Votre précédent est protégé.</h3><div class="lu-mini-plan">' + planHTML(e, "prev") + '</div><p class="lu-state-n">' + esc(tx.kind === "amb" ? "Avant " + A.name : s.prev.label) + "</p>" +
          '<p class="lu-note">' + (tx.done ? "Les confirmations reçues sont conservées. Une lumière indisponible n’est jamais annoncée comme réglée." : "Il a été gardé avant la première commande.") + "</p>" +
          (st.partial ? '<p class="lu-gold">Réessayer garde le même éclairage précédent protégé.</p>' : "") +
          (tx.done ? '<button type="button" class="lu-btn" data-a="restore">Revenir à mon éclairage précédent</button>' : "") : '<h3 class="lu-h2">Aucun précédent.</h3>') + "</aside></div>";
      return h;
    }
    if (tx.kind === "amb") {
      h += '<div class="lu-rgrid2"><section class="lu-panel"><h3 class="lu-h2">Éclairage actuel · ' + esc(A.name) + '</h3><div class="lu-mini-plan">' + planHTML(e, "cur") + "</div>" +
        '<p class="lu-gold lu-big">' + plural(onCount(I.k), "lumière", "lumières") + " " + esc(A.tone || A.name) + " à " + A.lvl + PC + "</p>" +
        tx.keep.filter(function (k) { return !s.lights[k].on; }).map(function (k) { return '<p class="lu-note">' + esc(e.L[k].name) + " OFF · confirmé</p>"; }).join("") + "</section>" +
        '<section class="lu-panel lu-hl"><div class="lu-row-sb"><h3 class="lu-h2">Votre éclairage précédent</h3><span class="lu-pill is-draft"><i></i>Temporaire</span></div><div class="lu-mini-plan">' + planHTML(e, "prev") + "</div>" +
        '<p class="lu-state-n">' + esc((s.prev ? s.prev.label.replace(" · non enregistré", "") : "") + " · avant " + A.name) + '</p><p class="lu-note">' + esc(prevSummary(I)) + "</p></section>" +
        '<section class="lu-panel"><h3 class="lu-h2">Reprendre votre éclairage</h3><button type="button" class="lu-btn lu-btn-pri lu-btn-full" data-a="restore">Revenir à mon éclairage précédent</button>' +
        '<p class="lu-note">Disponible après fermeture et réouverture de JARVIS.</p><p class="lu-note lu-faint">Remplacé à la prochaine application d’ambiance ou de configuration.</p></section>' +
        '<section class="lu-panel">' + part(I, "keepprev", function () { return keepPrev(I, A); }) + "</section></div>";
      return h;
    }
    h += '<div class="lu-rgrid2"><div class="lu-col"><section class="lu-panel"><h3 class="lu-h2">L’éclairage actuel</h3><div class="lu-mini-plan">' + planHTML(e, "cur") + "</div>" +
      '<p class="lu-big">' + esc(changeSentence(I, tx)) + '</p><p class="lu-note">' + esc(keptSentence(I, tx)) + "</p></section>";
    if (tx.kind !== "restore") {
      h += '<section class="lu-panel"><h3 class="lu-h2">Votre éclairage précédent est gardé.</h3><p class="lu-note">Il reste disponible, même après fermeture de JARVIS.</p>' +
        '<button type="button" class="lu-btn lu-btn-full" data-a="restore">Revenir à mon éclairage précédent</button>' +
        (tx.kind !== "config" ? '<p class="lu-note lu-gold">La configuration à droite gardera l’éclairage actuel.</p>' : "") + "</section>";
    }
    h += "</div>";
    if (tx.kind === "config") h += '<section class="lu-panel"><h3 class="lu-h2">Rien à enregistrer</h3><p class="lu-note">Votre éclairage correspond à « ' + esc(tx.title) + " ». La configuration reste telle qu’enregistrée : un rappel ne la modifie jamais.</p></section>";
    else h += '<section class="lu-panel lu-hl lu-savebox">' + part(I, "saveres", function () { return I.saveOpen ? savePanel(I, "res") : savedNote(I); }) + "</section>";
    h += "</div>";
    return h;
  }
  function savedNote(I) {
    if (I.savedAs) return '<h3 class="lu-h2">Enregistré.</h3><p class="lu-note">« ' + esc(I.savedAs) + " » est dans Mes configurations, avec les valeurs confirmées.</p>" +
      '<button type="button" class="lu-btn" data-a="lib-cfg">Voir Mes configurations</button>';
    return '<h3 class="lu-h2">Non enregistré.</h3><p class="lu-note">Vous pourrez l’enregistrer plus tard depuis Mes configurations.</p><button type="button" class="lu-btn" data-a="save-reopen">Enregistrer quand même</button>';
  }
  function keepPrev(I, A) {
    var s = S(I.k);
    if (I.prevSaved) return '<h3 class="lu-h2">Précédent enregistré.</h3><p class="lu-note">« ' + esc(I.prevSaved) + " » est une copie durable de votre éclairage d’avant " + esc(A.name) + ".</p>";
    var nm = I.prevName != null ? I.prevName : uniqueName(s, "Mon éclairage avant " + A.name);
    return '<h3 class="lu-h2">Garder ce précédent pour plus tard</h3><label class="lu-field"><span class="lu-vh">Nom</span><input type="text" maxlength="40" data-n="prev" value="' + esc(nm) + '" autocomplete="off"></label>' +
      '<button type="button" class="lu-btn lu-btn-full" data-a="save-prev">Enregistrer ce précédent dans Mes configurations</button>' +
      (I.prevErr ? '<p class="lu-note lu-warnt">' + esc(I.prevErr) + "</p>" : "") + '<p class="lu-note">Copie durable du précédent, pas de ' + esc(A.name) + ".</p>";
  }
  function perLight(I, tx) {
    var e = I.e, s = S(I.k);
    return '<ul class="lu-pl">' + e.lights.map(function (l) {
      var r = tx.res[l.k], v = s.lights[l.k], c = tx.changes.filter(function (x) { return x.k === l.k; })[0], fixed = l.kind === "regl";
      var lab, cls = "", det;
      if (fixed) { lab = "Réglementaire"; det = l.mode + " · jamais modifié"; }
      else if (tx.aborted && tx.aborted.indexOf(l.k) >= 0) { lab = "Indisponible"; cls = "is-warn"; det = "État non confirmé"; }
      else if (tx.aborted) { lab = "Rien envoyé"; det = vLong(l, v).replace(" au rallumage", ""); }
      else if (!r) { lab = "Confirmé"; det = vText(l, v) === "Éteint" ? "Off · inchangé" : vText(l, v) + " · inchangé"; }
      else if (r === "wait") { lab = "En attente"; cls = "is-wait"; det = vText(l, c.from) + " → " + vText(l, c.to); }
      else if (r === "send") { lab = "Envoi…"; cls = "is-send"; det = vText(l, c.from) + " → " + vText(l, c.to); }
      else if (r === "ok") { lab = "Confirmé"; cls = "is-ok"; det = vLong(l, v).replace(" au rallumage", ""); }
      else if (r === "manual") { lab = "Réglée à la main"; cls = "is-ok"; det = vText(l, v); }
      else { lab = "Indisponible"; cls = "is-warn"; det = "Avant tentative : " + vText(l, c.from); }
      return '<li class="' + cls + '"><span class="lu-thumb">' + lightThumb(e, l, r === "fail" ? c.from : v) + '</span><div><b>' + esc(l.name) + "</b><small>" + esc(det) + '</small></div><div class="lu-pl-r"><span class="lu-k ' + cls + '">' +
        (r === "send" ? '<span class="lu-spin"></span>' : "") + lab + "</span>" + (r === "fail" ? '<small class="lu-warnt">Actuel non confirmé</small>' : "") + "</div></li>";
    }).join("") + "</ul>";
  }
  function resDock(I) {
    var e = I.e, s = S(I.k), tx = s.tx;
    if (!tx || !tx.done) return "";
    var st = resStatus(tx);
    if (tx.aborted) {
      return '<div class="lu-dock is-warn"><div class="lu-dock-t"><b>Rien n’a été envoyé.</b><p>Votre éclairage est resté tel quel.</p></div><div class="lu-dock-a"><button type="button" class="lu-btn" data-a="home">Retour aux lumières</button>' +
        (s.tx && Object.keys(s.tx.res).length ? "" : "") + '<button type="button" class="lu-btn lu-btn-pri" data-a="retry-unknown">Réessayer ' + esc(list(tx.aborted.map(function (k) { return e.L[k].the; }))) + "</button></div></div>";
    }
    if (st.partial) {
      var offs = e.ctrl.filter(function (l) { return !s.lights[l.k].on && s.lights[l.k].conf === "ok"; });
      return '<div class="lu-dock is-warn"><div class="lu-dock-t"><b>' + (st.fails.length > 1 ? cap(words(st.fails.length)) + " lumières restent à vérifier." : "Une lumière reste à vérifier.") + "</b><p>" +
        (offs.length ? esc(cap(list(offs.map(function (l) { return l.the; })))) + " toujours " + off(offs.length > 1 ? "mp" : offs[0].g) + ". " : "") + "Aucun succès global annoncé.</p></div>" +
        '<div class="lu-dock-a"><button type="button" class="lu-btn lu-btn-pri" data-a="retry"' + (s.busy ? " disabled" : "") + ">" + ic("retry") + "Réessayer " + esc(list(st.fails.map(function (k) { return e.L[k].the; }))) + "</button></div></div>";
    }
    return '<div class="lu-dock is-done"><div class="lu-dock-t"><b>Tout est confirmé.</b><p>Chaque lumière a répondu.</p></div><div class="lu-dock-a"><button type="button" class="lu-btn" data-a="home">Retour aux lumières</button></div></div>';
  }
  function zoneSentences(I, tx) {
    var e = I.e, cur = V(I, "cur"), bits = [];
    var moved = tx ? tx.changes.map(function (c) { return e.L[c.k].zone; }) : [];
    e.zones.slice().sort(function (a, b) { return (moved.indexOf(b.k) >= 0) - (moved.indexOf(a.k) >= 0); }).forEach(function (z) {
      if (!zoneOn(e, z, cur) || e.zl[z.k].every(function (l) { return l.kind === "regl"; })) return;
      bits.push(zoneAmb(e, z, cur).replace(" · ", " et ") + " " + z.in + ".");
    });
    return bits.slice(0, 4).join(" ") || "Tout est éteint.";
  }
  function changeSentence(I, tx) {
    var e = I.e, zones = [];
    tx.changes.forEach(function (c) { var z = e.Z[e.L[c.k].zone]; if (zones.indexOf(z) < 0) zones.push(z); });
    if (zones.length === 1) {
      var z = zones[0], ls = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; }), c0 = tx.changes[0];
      if (!c0.to.on) return cap(z.the) + " est maintenant " + off(z.g) + ".";
      if (ls.length > 1 && tx.changes.length === ls.length) return "Les deux " + (z.group ? z.group.short.replace(/^2 /, "") : "lumières") + " " + z.the.replace(/^l[ea] |^l’/, function (m) { return m === "le " ? "du " : m === "la " ? "de la " : "de l’"; }) + " sont en " + ambName(e.L[c0.k], c0.to.amb) + ".";
      return cap(z.the) + " en " + ambName(e.L[c0.k], c0.to.amb) + ".";
    }
    return plural(tx.changes.length, "lumière a changé", "lumières ont changé") + " : " + list(zones.map(function (z) { return z.the; })) + ".";
  }
  function keptSentence(I, tx) {
    var e = I.e, s = S(I.k), moved = tx.changes.map(function (c) { return e.L[c.k].zone; }), keptOn = [], keptOff = [];
    e.zones.forEach(function (z) {
      if (moved.indexOf(z.k) >= 0 || e.zl[z.k].every(function (l) { return l.kind === "regl"; })) return;
      (zoneOn(e, z, V(I, "cur")) ? keptOn : keptOff).push(z);
    });
    var t = "";
    var allF = keptOn.every(function (z) { return z.g.charAt(0) === "f"; });
    if (keptOn.length) t += cap(list(keptOn.map(function (z) { return z.name.toLowerCase(); }))) + (keptOn.length > 1 ? (allF ? " conservées." : " conservés.") : " conservé" + (allF ? "e" : "") + (/p$/.test(keptOn[0].g) ? "s" : "") + ".");
    if (keptOff.length) t += (t ? " " : "") + cap(list(keptOff.map(function (z) { return z.the; }))) + " toujours " + off(keptOff.length > 1 ? "mp" : keptOff[0].g) + ".";
    return t;
  }
  function prevSummary(I) {
    var e = I.e, s = S(I.k);
    if (!s.prev) return "";
    var parts = [], seen = {};
    e.ctrl.forEach(function (l) {
      var v = s.prev.snap[l.k];
      if (!v) return;
      var t = v.on ? ambName(l, v.amb) + " " + v.lvl + PC : l.name.toLowerCase() + " OFF";
      if (!seen[t]) { seen[t] = 1; parts.push(t); }
    });
    return parts.join(" · ");
  }

  /* ---------------------------------------------------------------- dialogues (retour avec avertissement, conflits) */
  function dialog(I) {
    var d = I.dlg, e = I.e;
    if (!d) return "";
    var body = "";
    if (d.t === "restore") {
      body = '<h3 class="lu-h2">Des lumières ont changé depuis la dernière application.</h3><ul class="lu-drift">' + d.drift.map(function (x) {
        return "<li><b>" + esc(x.l.name) + "</b><span>" + (x.unknown ? "État non confirmé" : "Attendu : " + esc(vText(x.l, x.was)) + " · maintenant : " + esc(vText(x.l, x.now))) + "</span></li>";
      }).join("") + '</ul><p class="lu-note">Revenir à votre éclairage précédent remplacera aussi ces changements, dans cet environnement seulement.</p>' +
        '<div class="lu-row-end"><button type="button" class="lu-btn" data-a="dlg-close">Annuler</button><button type="button" class="lu-btn lu-btn-pri" data-a="restore-force">Revenir quand même</button></div>';
    } else if (d.t === "name") {
      body = '<h3 class="lu-h2">Une configuration s’appelle déjà « ' + esc(d.c.name) + " ».</h3><p class=\"lu-note\">Rien n’a été écrasé. Voulez-vous la mettre à jour avec l’éclairage actuel, ou choisir un autre nom ?</p>" +
        '<div class="lu-row-end"><button type="button" class="lu-btn" data-a="dlg-close">Choisir un autre nom</button><button type="button" class="lu-btn lu-btn-pri" data-a="cfg-update-name" data-v="' + d.c.k + '">Mettre à jour ' + esc(d.c.name) + "</button></div>";
    } else if (d.t === "stale") {
      body = '<h3 class="lu-h2">« ' + esc(d.c.name) + " » a changé depuis votre rappel.</h3><p class=\"lu-note\">Une autre version a été enregistrée entre-temps (version " + d.c.v + "). Rien n’a été écrasé.</p>" +
        '<div class="lu-row-end"><button type="button" class="lu-btn" data-a="dlg-close">Annuler</button><button type="button" class="lu-btn lu-btn-pri" data-a="cfg-copy" data-v="' + d.c.k + '">Enregistrer une copie</button></div>';
    } else if (d.t === "none") {
      body = '<h3 class="lu-h2">Rien à restaurer.</h3><p class="lu-note">' + esc(d.msg) + '</p><div class="lu-row-end"><button type="button" class="lu-btn lu-btn-pri" data-a="dlg-close">D’accord</button></div>';
    }
    return '<div class="lu-dlg" role="dialog" aria-modal="true" aria-label="Confirmation"><div class="lu-dlg-box">' + body + "</div></div>";
  }

  /* ---------------------------------------------------------------- actions */
  function toast(I, t) { if (I.api && typeof I.api.toast === "function") I.api.toast(t); }
  function startRestore(I, force) {
    var pl = restorePlan(I.k);
    if (!pl) { I.dlg = { t: "none", msg: "Aucun éclairage précédent n’est gardé pour l’instant." }; I.queue(); return; }
    if (!pl.changes.length) { I.dlg = { t: "none", msg: "Votre éclairage est déjà celui d’avant." }; I.queue(); return; }
    if (pl.drift.length && !force) { I.dlg = { t: "restore", drift: pl.drift }; I.queue(); return; }
    I.dlg = null;
    var p = txRun(I.k, { kind: "restore", title: "Retour", changes: pl.changes });
    if (I.scr.n !== "res") go(I, { n: "res" }); else I.queue();
    return p;
  }
  function openCompose(I, zone, cfgKey) {
    var e = I.e, s = S(I.k), draft = {}, sel = [];
    e.ctrl.forEach(function (l) { var v = s.lights[l.k]; draft[l.k] = { on: v.on, amb: v.amb, lvl: v.lvl }; });
    if (cfgKey) {
      var c = cfgOf(s, cfgKey);
      Object.keys(c.lights).forEach(function (lk) { var v = c.lights[lk]; draft[lk] = { on: v.on, amb: v.amb, lvl: v.lvl }; });
    }
    if (zone) sel = e.zl[zone].filter(function (l) { return l.kind !== "regl"; }).map(function (l) { return l.k; });
    go(I, { n: "compose", draft: draft, sel: sel, verify: false, cfg: cfgKey || null, touched: {} });
  }
  function bindFull(I) {
    I.on("click", function (ev) {
      var b = ev.target.closest("[data-a]");
      if (!b || !I.el.contains(b) || b.disabled) return;
      var a = b.getAttribute("data-a"), v = b.getAttribute("data-v"), e = I.e, s = S(I.k), sc = I.scr;
      switch (a) {
        case "home": I.hist = []; go(I, { n: "home" }, true); break;
        case "back": back(I); break;
        case "lib-amb": go(I, { n: "lib", tab: "amb", q: "", f: null }); break;
        case "lib-cfg": I.saveOpenCfg = false; go(I, { n: "lib", tab: "cfg" }); break;
        case "zone": go(I, { n: "zone", z: v, pa: null, apart: false }); break;
        case "filter": I.filter = v; render(I); break;
        case "lib-f": sc.f = sc.f === v ? null : v; render(I); break;
        case "view": I.view = v; render(I); break;
        case "all-on": case "all-off":
          direct(I.k, e.ctrl.map(function (l) { return l.k; }), { on: a === "all-on" });
          toast(I, a === "all-on" ? "Toutes les lumières s’allument." : "Toutes les lumières s’éteignent." + (e.lights.some(function (l) { return l.kind === "regl"; }) ? " Les feux réglementaires restent comme ils sont." : ""));
          break;
        case "zone-sw": {
          var ls = e.zl[v].filter(function (l) { return l.kind !== "regl"; }), on = ls.some(function (l) { return s.lights[l.k].on; });
          direct(I.k, ls.map(function (l) { return l.k; }), { on: !on });
          break;
        }
        case "light-sw": direct(I.k, [v], { on: !s.lights[v].on }); break;
        case "apart": sc.apart = v === "1"; I.queue(); break;
        case "fav": favs()[v] = !favs()[v]; persist(); I.queue(); SUBS.forEach(function (u) { if (u !== I) u.queue(); }); break;
        case "fav-only": I.favOnly = !I.favOnly; I.queue(); b.classList.toggle("is-on", I.favOnly); b.setAttribute("aria-pressed", I.favOnly); break;
        case "preview": go(I, { n: "preview", a: v, extra: {} }); break;
        case "zprev": sc.pa = v; I.queue(); break;
        case "zone-apply": {
          var pl = zonePlan(I.k, sc.z, sc.pa), z = e.Z[sc.z];
          if (!pl.changes.length) break;
          txRun(I.k, { kind: "zone", title: AMB[sc.pa].name + " " + z.in, amb: sc.pa, zone: sc.z, changes: pl.changes, keep: pl.keep, origin: { t: "perso" } });
          freshResult(I);
          go(I, { n: "res" });
          break;
        }
        case "amb-apply": {
          var pl2 = ambPlan(I.k, sc.a, sc.extra);
          if (!pl2.changes.length) break;
          txRun(I.k, { kind: "amb", title: AMB[sc.a].name, amb: sc.a, changes: pl2.changes, keep: pl2.keep, origin: { t: "amb", k: sc.a } });
          freshResult(I);
          go(I, { n: "res" });
          break;
        }
        case "compose": openCompose(I, v || null); break;
        case "same-all": sc.sel = e.ctrl.map(function (l) { return l.k; }); sc.verify = false; I.queue(); break;
        case "draft-sel": {
          var i = sc.sel.indexOf(v);
          if (i >= 0) sc.sel.splice(i, 1); else sc.sel.push(v);
          I.queue();
          break;
        }
        case "draft":
          if (sc.verify) { sc.verify = false; I.queue(); toast(I, "Brouillon rouvert : choisissez les lumières à changer."); break; }
          if (!sc.sel.length) { toast(I, "Touchez d’abord une lumière à gauche."); break; }
          sc.sel.forEach(function (lk) {
            var l = e.L[lk], d = sc.draft[lk];
            d.amb = v; d.lvl = adapt(l, v).lvl;
            sc.touched[lk] = true;
          });
          sc.verify = false;
          I.queue();
          break;
        case "draft-on": sc.draft[v].on = true; if (!sc.draft[v].lvl) sc.draft[v].lvl = adapt(e.L[v], sc.draft[v].amb).lvl; I.queue(); break;
        case "draft-offk": sc.draft[v].on = false; I.queue(); break;
        case "draft-verify": sc.verify = true; render(I); break;
        case "draft-edit": sc.verify = false; I.queue(); break;
        case "draft-cancel": toast(I, "Brouillon annulé. Rien n’a été envoyé."); back(I); break;
        case "draft-apply": {
          var pl3 = draftPlan(I.k, sc.draft);
          if (!pl3.changes.length) break;
          if (sc.cfg) {
            var c = cfgOf(s, sc.cfg);
            txRun(I.k, { kind: "config", title: c.name, cfg: c.k, changes: pl3.changes, origin: { t: "cfg", k: c.k, v: c.v } });
          } else txRun(I.k, { kind: "compose", title: "Composition", changes: pl3.changes, origin: { t: "perso" } });
          freshResult(I);
          go(I, { n: "res" });
          break;
        }
        case "recall": openCompose(I, null, v); I.scr.verify = true; render(I); break;
        case "cfg-fav": { var cf = cfgOf(s, v); cf.fav = !cf.fav; emit(I.k); break; }
        case "cfg-update": {
          var r = updateCfg(I.k, v, s.origin && s.origin.k === v ? s.origin.v : null);
          if (r.conflict) I.dlg = { t: "stale", c: r.conflict }; else toast(I, "« " + r.ok.name + " » est mise à jour (version " + r.ok.v + ").");
          I.queue();
          break;
        }
        case "cfg-update-name": { var r2 = updateCfg(I.k, v, null); I.dlg = null; if (r2.ok) { toast(I, "« " + r2.ok.name + " » est mise à jour."); afterSave(I, r2.ok.name); } break; }
        case "cfg-copy": { var r3 = copyCfg(I.k, v); I.dlg = null; if (r3.ok) toast(I, "Copie enregistrée : « " + r3.ok.name + " »."); I.queue(); break; }
        case "save-open": I.saveOpenCfg = true; I.saveName = null; I.saveErr = null; I.queue(); break;
        case "save-close": if (v === "cfg") I.saveOpenCfg = false; else I.saveOpen = false; I.saveErr = null; I.queue(); break;
        case "save-reopen": I.saveOpen = true; I.queue(); break;
        case "save": {
          var inp = I.el.querySelector('[data-n="save"]'), nm = inp ? inp.value : I.saveName;
          var r4 = saveNew(I.k, nm);
          if (r4.error) { I.saveErr = r4.error; I.queue(); break; }
          if (r4.conflict) { I.dlg = { t: "name", c: r4.conflict }; I.queue(); break; }
          toast(I, "« " + r4.ok.name + " » enregistrée dans Mes configurations.");
          afterSave(I, r4.ok.name);
          break;
        }
        case "save-prev": {
          var inp2 = I.el.querySelector('[data-n="prev"]'), nm2 = String(inp2 ? inp2.value : "").trim();
          if (!s.prev) break;
          var r5 = saveNew(I.k, nm2, { lights: JSON.parse(JSON.stringify(s.prev.snap)), inc: [] });
          if (r5.error || r5.conflict) { I.prevErr = r5.error || "Ce nom existe déjà : choisissez-en un autre. Rien n’a été écrasé."; I.queue(); break; }
          I.prevSaved = r5.ok.name; I.prevErr = null;
          toast(I, "Précédent enregistré : « " + r5.ok.name + " ».");
          I.queue();
          break;
        }
        case "restore": startRestore(I, false); break;
        case "restore-force": startRestore(I, true); break;
        case "dlg-close": I.dlg = null; I.queue(); break;
        case "res": go(I, { n: "res" }); break;
        case "retry": txRetry(I.k); break;
        case "retry-unknown": {
          /* La lumière muette vient d'une application précédente : on reprend cette même transaction
             (même précédent); sinon on redemande simplement son état à l'appareil. */
          var base = s.tx && s.tx.aborted ? s.tx.prevTx : s.tx;
          if (base && Object.keys(base.res).some(function (lk) { return base.res[lk] === "fail"; })) { s.tx = base; txRetry(I.k); }
          else requery(I.k, unknownLights(I.k).map(function (l) { return l.k; }));
          break;
        }
      }
    });
    I.on("input", function (ev) {
      var t = ev.target;
      if (t.hasAttribute("data-r")) {
        var r = t.getAttribute("data-r"), v = t.getAttribute("data-v"), val = +t.value, e = I.e;
        t.style.setProperty("--p", (val / (+t.max || 100) * 100).toFixed(1) + "%");
        var keys = r === "zone" ? e.zl[v].filter(function (l) { return l.kind !== "regl"; }).map(function (l) { return l.k; }) : [v];
        direct(I.k, keys, { lvl: val }, true);
        if (I.scr.n === "zone") I.scr.pa = null;
      } else if (t.hasAttribute("data-q")) {
        var q = t.getAttribute("data-q");
        if (q === "lib") I.scr.q = t.value; else I.q = t.value;
        I.queue();
      } else if (t.getAttribute("data-n") === "save") { I.saveName = t.value; }
      else if (t.getAttribute("data-n") === "prev") { I.prevName = t.value; }
    });
    I.on("change", function (ev) {
      var t = ev.target;
      if (t.hasAttribute("data-r")) {
        var r = t.getAttribute("data-r"), v = t.getAttribute("data-v"), e = I.e;
        var keys = r === "zone" ? e.zl[v].filter(function (l) { return l.kind !== "regl"; }).map(function (l) { return l.k; }) : [v];
        direct(I.k, keys, { lvl: +t.value });
      } else if (t.hasAttribute("data-x")) {
        I.scr.extra[t.getAttribute("data-x")] = t.checked;
        I.queue();
      }
    });
    I.on("keydown", function (ev) {
      if (ev.key === "Escape" && I.dlg) { I.dlg = null; I.queue(); }
      if (ev.key === "Enter" && ev.target.getAttribute && ev.target.getAttribute("data-n")) {
        var b = I.el.querySelector(ev.target.getAttribute("data-n") === "prev" ? '[data-a="save-prev"]' : '[data-a="save"]');
        if (b) b.click();
      }
    });
  }
  function freshResult(I) { I.saveOpen = true; I.savedAs = null; I.saveName = null; I.saveErr = null; I.prevSaved = null; I.prevName = null; I.prevErr = null; }
  function afterSave(I, name) {
    I.savedAs = name; I.saveOpen = false; I.saveOpenCfg = false; I.saveName = null; I.saveErr = null;
    emit(I.k);
  }

  /* ================================================================ CARTE COMPACTE (Vue d'ensemble) */
  var QUICK = [["lecture", "Lecture"], ["heure-doree", "Soirée"], ["nuit-douce", "Nuit"]];
  function mountMini(host, k, api) {
    data(); defs();
    unmount(host);
    var e = env(k), el = rootIn(host, "lu lu-mini-host");
    var M = { host: host, el: el, k: k, e: e, api: api || {}, timers: [], parts: {}, mini: true };
    M.queue = function () { if (M.raf) return; M.raf = requestAnimationFrame(function () { M.raf = 0; miniUpdate(M); }); };
    M.on = function (type, fn) { el.addEventListener(type, fn); M.timers.push(function () { el.removeEventListener(type, fn); }); };
    var zs = [e.Z[e.main]].concat(e.zones.filter(function (z) { return z.k !== e.main && !z.out && e.zl[z.k].some(function (l) { return l.kind !== "regl"; }); })).slice(0, 3);
    M.zs = zs;
    /* Corps seulement : le cadre fournit déjà la carte, le titre, le compte et le lien « Ouvrir » */
    el.innerHTML = '<div class="lu-mini"><div class="lu-mini-q" data-mp="quick" role="group" aria-label="Ambiances rapides"></div>' +
      '<ul class="lu-mini-rows" data-mp="rows"></ul><p class="lu-mini-st" data-mp="state" role="status"></p></div>';
    M.on("click", function (ev) {
      var b = ev.target.closest("[data-a]");
      if (!b || b.disabled) return;
      var a = b.getAttribute("data-a"), v = b.getAttribute("data-v"), s = S(k);
      if (a === "quick") {
        var name = QUICK.filter(function (q) { return q[0] === v; })[0][1];
        applyAmb(k, v).then(function (r) {
          if (!M.api.toast) return;
          if (r.aborted) M.api.toast("Rien n’a été envoyé : une lumière n’a pas confirmé son état.");
          else if (r.busy) M.api.toast("Une application est déjà en cours.");
          else if (r.unchanged) M.api.toast(onCount(k) ? name + " est déjà en place." : "Tout est éteint : une ambiance garde les lumières éteintes.");
          else if (r.failed) M.api.toast(name + " partiellement appliquée : " + r.confirmed + " sur " + (r.confirmed + r.failed) + " confirmées.");
          else M.api.toast(name + " en place · " + plural(r.confirmed, "réglage confirmé", "réglages confirmés") + ".");
        });
      } else if (a === "zone-sw") {
        var ls = e.zl[v].filter(function (l) { return l.kind !== "regl"; }), on = ls.some(function (l) { return s.lights[l.k].on; });
        direct(k, ls.map(function (l) { return l.k; }), { on: !on });
      }
    });
    M.on("input", function (ev) {
      var t = ev.target;
      if (!t.hasAttribute("data-r")) return;
      t.style.setProperty("--p", (+t.value / (+t.max || 100) * 100).toFixed(1) + "%");
      var keys = e.zl[t.getAttribute("data-v")].filter(function (l) { return l.kind !== "regl"; }).map(function (l) { return l.k; });
      direct(k, keys, { lvl: +t.value }, true);
    });
    M.on("change", function (ev) {
      var t = ev.target;
      if (!t.hasAttribute("data-r")) return;
      var keys = e.zl[t.getAttribute("data-v")].filter(function (l) { return l.kind !== "regl"; }).map(function (l) { return l.k; });
      direct(k, keys, { lvl: +t.value });
    });
    SUBS.push(M);
    INST.push(M);
    miniUpdate(M);
    announce(k);
    return M;
  }
  function miniUpdate(M) {
    if (!M.el.isConnected) return;
    var e = M.e, s = S(M.k), cur = s.lights, k = M.k;
    var act = document.activeElement, dragging = act && act.type === "range" && M.el.contains(act);
    var on = e.ctrl.filter(function (l) { return cur[l.k].on; });
    var activeAmb = on.length && on.every(function (l) { return cur[l.k].amb === cur[on[0].k].amb; }) ? cur[on[0].k].amb : null;
    var q = M.el.querySelector('[data-mp="quick"]');
    q.innerHTML = QUICK.map(function (x) {
      var isOn = activeAmb === x[0];
      return '<button type="button" data-a="quick" data-v="' + x[0] + '" class="' + (isOn ? "is-on" : "") + '" aria-pressed="' + isOn + '"' + (s.busy ? " disabled" : "") + ">" + x[1] + "</button>";
    }).join("");
    if (!dragging) {
      M.el.querySelector('[data-mp="rows"]').innerHTML = M.zs.map(function (z) {
        var V0 = {}; e.lights.forEach(function (l) { V0[l.k] = cur[l.k]; });
        var zon = zoneOn(e, z, V0), lvl = zoneLvl(e, z, V0), ls = e.zl[z.k].filter(function (l) { return l.kind !== "regl"; });
        var shown = lvl || Math.round(ls.reduce(function (t, l) { return t + (cur[l.k].last || 60); }, 0) / ls.length);
        var capL = ls.filter(function (l) { return l.cap; })[0], max = capL ? capL.cap[0] : 100;
        var pend = ls.some(function (l) { return cur[l.k].conf === "pending"; }), unk = ls.some(function (l) { return cur[l.k].conf === "unknown"; });
        return '<li class="' + (zon ? "is-on" : "") + '"><span class="lu-mini-zi">' + ic(z.ic) + "</span><b>" + esc(z.short || z.name) + (unk ? ' <em class="lu-warnt">!</em>' : "") + '</b><span class="lu-val">' + (zon ? lvl + PC : "Éteint") + "</span>" +
          '<input type="range" min="1" max="' + max + '" value="' + shown + '" data-r="zone" data-v="' + z.k + '" aria-label="Luminosité : ' + esc(z.name) + '" style="--p:' + (shown / max * 100).toFixed(1) + '%">' +
          '<span class="lu-mini-sw">' + sw(zon, "zone-sw", z.k, (zon ? "Éteindre " : "Allumer ") + z.the, false, pend).replace(/<span class="lu-swl"[^>]*>[^<]*<\/span>/, "") + "</span></li>";
      }).join("");
    } else {
      [].forEach.call(M.el.querySelectorAll('[data-mp="rows"] li'), function (li, i) {
        var z = M.zs[i], V0 = {}; e.lights.forEach(function (l) { V0[l.k] = cur[l.k]; });
        li.querySelector(".lu-val").textContent = zoneOn(e, z, V0) ? zoneLvl(e, z, V0) + PC : "Éteint";
      });
    }
    /* Ligne d'état : seulement pendant une application ou quand une lumière reste à vérifier */
    var st = M.el.querySelector('[data-mp="state"]'), unk = unknownLights(k);
    if (s.busy && s.tx) { var c = counts(s.tx); st.innerHTML = '<span class="lu-spin"></span>Application en cours · ' + c.confirmed + " sur " + s.tx.changes.length + " confirmées"; st.className = "lu-mini-st is-busy"; }
    else if (unk.length) { st.innerHTML = ic("warn") + esc(cap(list(unk.map(function (l) { return l.the; })))) + (unk.length > 1 ? " ne répondent pas." : " ne répond pas.") + " Ouvrez l’éclairage pour réessayer."; st.className = "lu-mini-st is-warn"; }
    else { st.textContent = ""; st.className = "lu-mini-st"; }
  }

  /* ================================================================ API publique */
  function applyAmb(k, a) {
    env(k);
    if (!AMB[a]) return Promise.reject(new Error("JarvisLumieres : ambiance inconnue « " + a + " »."));
    var pl = ambPlan(k, a, {});
    if (!pl.changes.length) return Promise.resolve({ confirmed: 0, failed: 0, unchanged: true });
    /* Rien n'est envoyé (application déjà en cours, ou précédent impossible à protéger) :
       chaque lumière visée compte comme « à vérifier », jamais comme un succès */
    return txRun(k, { kind: "amb", title: AMB[a].name, amb: a, changes: pl.changes, keep: pl.keep, origin: { t: "amb", k: a } }).then(function (r) {
      if (r.aborted || r.busy) r.failed = pl.changes.length;
      return r;
    });
  }
  window.JarvisLumieres = {
    mount: function (el, envKey, api) { mountFull(el, envKey, api); },
    unmount: function (el) { unmount(el); },
    mini: function (el, envKey, api) { mountMini(el, envKey, api); },
    applyAmbiance: function (envKey, ambianceKey) { return applyAmb(envKey, ambianceKey); },
    /* Lecture seule, pour le cadre : nombre de lumières allumées et libellé d'état */
    status: function (envKey) { var e = env(envKey); return { on: onCount(envKey), total: e.ctrl.length, label: stateLabel(envKey) }; }
  };
  document.dispatchEvent(new CustomEvent("lum:ready"));
  /* Comptes de départ de chaque environnement, dès que les données sont dans la page */
  function announceAll() { try { Object.keys(data().envs).forEach(announce); } catch (err) { /* page sans module Éclairage */ } }
  if (document.getElementById("lum-data")) announceAll();
  else document.addEventListener("DOMContentLoaded", announceAll, { once: true });
})();
