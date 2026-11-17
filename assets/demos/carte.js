/* Vraie carte JARVIS : une seule fabrique pour l'écran « Carte » et « Mes lieux » de JARVIS App
   (assets/demos/app.js) et pour le copilote de Mobilité (assets/demos/mobilite.js).
   - MapLibre GL JS, hébergé sur le site (assets/vendor/maplibre/) : aucun réseau de diffusion externe.
   - Tuiles vectorielles OpenFreeMap (données OpenStreetMap, schéma OpenMapTiles) et relief public
     (Terrain Tiles) : sans clé, sans compte. Ce sont les deux seuls tiers contactés, et seulement
     quand une carte s'ouvre (voir /confidentialite/).
   - Style écrit ici, noir et or, décliné pour les trois modes (Base, Signature, Platinum).
   - RÈGLE « aucun lieu » : le style ne contient AUCUNE couche de texte. La géographie est réelle,
     mais aucun nom de ville, de région, de pays ni numéro de route n'est écrit.
   Ce fichier n'est chargé qu'à l'ouverture d'une carte. Si WebGL, la bibliothèque ou les tuiles
   manquent, ouvre() échoue et la page garde sa carte dessinée. */
(function () {
  "use strict";
  if (window.JarvisCarte) return;
  var LIB = "/assets/vendor/maplibre/maplibre-gl";
  var TUILES = "https://tiles.openfreemap.org/planet";
  var RELIEF = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png";

  /* ---------------------------------------------------------------- Teintes des trois modes */
  var TONS = {
    signature: {
      terre: "#100f0e", eau: "#000000", rive: "#e2c27a", bord: "#4d4230", riveOp: .5, bois: "#0f100c", ville: "#151514", glace: "#1b1a18",
      rue: "#2c271d", route: "#55472d", grande: "#8a7242", auto: "#e2c27a", rail: "#2a2620", frontiere: "#6b5a3a",
      bati0: "#0c0c0c", bati1: "#1b1a17", bati2: "#4a4028", batiOp: .94,
      ombre: "#000000", clair: "#e2c27a", clairOp: .16, trajet: "#f4d892", halo: "#e2c27a",
      ciel: "#000000", horizon: "#3b2c10", brume: "#0b0a09", lumiere: "#ffe3a6", atmo: .55
    },
    platinum: {
      terre: "#10151c", eau: "#01040a", rive: "#bfe0ff", bord: "#4a6078", riveOp: .7, bois: "#0e141a", ville: "#151c25", glace: "#26313d",
      rue: "#2c3743", route: "#4f6377", grande: "#8fa9c2", auto: "#d9ecff", rail: "#27303a", frontiere: "#6f879e",
      bati0: "#111922", bati1: "#2b3b4c", bati2: "#6f8fae", batiOp: .82,
      ombre: "#00040a", clair: "#bfe0ff", clairOp: .26, trajet: "#f2f9ff", halo: "#9fd0ff",
      ciel: "#01050b", horizon: "#234a70", brume: "#0c1016", lumiere: "#dff0ff", atmo: 1
    },
    base: {
      terre: "#0f0f0f", eau: "#000000", rive: "#ffffff", bord: "#3c3c3c", riveOp: .28, bois: "#0e0e0e", ville: "#141414", glace: "#1c1c1c",
      rue: "#262626", route: "#444444", grande: "#6e6e6e", auto: "#a8a8a8", rail: "#242424", frontiere: "#5a5a5a",
      bati0: "#0d0d0d", bati1: "#1e1e1e", bati2: "#444444", batiOp: .92,
      ombre: "#000000", clair: "#ffffff", clairOp: .1, trajet: "#ffffff", halo: "#ffffff",
      ciel: "#000000", horizon: "#1c1c1c", brume: "#0b0b0b", lumiere: "#ffffff", atmo: .3
    }
  };
  function ton() { return TONS[document.documentElement.getAttribute("data-mode")] || TONS.signature; }

  /* ---------------------------------------------------------------- Style (aucune couche de texte) */
  function larg(k) { return ["interpolate", ["exponential", 1.6], ["zoom"], 4, .35 * k, 9, 1.1 * k, 13, 2.6 * k, 16, 9 * k, 18, 22 * k]; }
  function cls(noms) { return ["match", ["get", "class"], noms, true, false]; }
  var ROND = { "line-cap": "round", "line-join": "round" };
  function couches(t) {
    function ligne(id, couche, filtre, paint, min, layout) {
      var l = { id: id, type: "line", source: "omt", "source-layer": couche, layout: layout || ROND, paint: paint };
      if (filtre) l.filter = filtre;
      if (min) l.minzoom = min;
      return l;
    }
    return [
      { id: "fond", type: "background", paint: { "background-color": t.terre } },
      { id: "glace", type: "fill", source: "omt", "source-layer": "landcover", filter: cls(["ice"]), paint: { "fill-color": t.glace, "fill-antialias": false } },
      { id: "bois", type: "fill", source: "omt", "source-layer": "landcover", filter: cls(["wood", "forest"]), paint: { "fill-color": t.bois, "fill-antialias": false, "fill-opacity": .8 } },
      { id: "ville", type: "fill", source: "omt", "source-layer": "landuse", filter: cls(["residential", "commercial", "industrial", "retail"]), paint: { "fill-color": t.ville, "fill-antialias": false, "fill-opacity": ["interpolate", ["linear"], ["zoom"], 6, .9, 13, .45] } },
      { id: "relief", type: "hillshade", source: "relief", maxzoom: 15, paint: { "hillshade-shadow-color": t.ombre, "hillshade-highlight-color": t.clair, "hillshade-accent-color": t.ombre, "hillshade-exaggeration": ["interpolate", ["linear"], ["zoom"], 3, t.clairOp * 1.2, 9, t.clairOp * 2.4, 14, t.clairOp * 1.4], "hillshade-illumination-direction": 315 } },
      { id: "eau", type: "fill", source: "omt", "source-layer": "water", paint: { "fill-color": t.eau, "fill-antialias": true, "fill-outline-color": t.bord } },
      ligne("rive", "water", null, { "line-color": t.rive, "line-opacity": ["interpolate", ["linear"], ["zoom"], 0, Math.min(1, t.riveOp * 1.9), 4, Math.min(1, t.riveOp * 1.6), 6.5, t.riveOp * .3, 16, t.riveOp * .22], "line-blur": ["interpolate", ["linear"], ["zoom"], 0, .3, 4, .6, 6, 2.5], "line-width": ["interpolate", ["linear"], ["zoom"], 0, 1.1, 4, 1.4, 6, 2.2, 12, 3] }),
      ligne("riviere", "waterway", null, { "line-color": t.rive, "line-opacity": t.riveOp * .3, "line-width": ["interpolate", ["linear"], ["zoom"], 6, .4, 12, 1.2, 16, 3] }, 7),
      ligne("frontiere", "boundary", ["all", ["<=", ["get", "admin_level"], 4], ["!=", ["get", "maritime"], 1]],
        { "line-color": t.frontiere, "line-opacity": ["interpolate", ["linear"], ["zoom"], 0, .55, 6, .4, 10, .2], "line-width": ["case", ["<=", ["get", "admin_level"], 2], 1, .5], "line-dasharray": [3, 2.5] }, 0, { "line-join": "round" }),
      ligne("piste", "aeroway", cls(["runway", "taxiway"]), { "line-color": t.route, "line-width": ["interpolate", ["exponential", 1.6], ["zoom"], 10, 1, 15, 14] }, 10, { "line-cap": "butt", "line-join": "round" }),
      ligne("route-rue", "transportation", cls(["minor", "service", "track"]), { "line-color": t.rue, "line-width": larg(.8) }, 12),
      ligne("route-locale", "transportation", cls(["tertiary", "secondary"]), { "line-color": t.route, "line-width": larg(1) }, 8),
      ligne("route-grande", "transportation", cls(["primary", "trunk"]), { "line-color": t.grande, "line-width": larg(1.25) }, 5),
      ligne("route-auto-halo", "transportation", cls(["motorway"]), { "line-color": t.auto, "line-opacity": .22, "line-blur": 6, "line-width": larg(5) }, 4),
      ligne("route-auto", "transportation", cls(["motorway"]), { "line-color": t.auto, "line-opacity": .9, "line-width": larg(1.5) }, 4),
      ligne("rail", "transportation", cls(["rail"]), { "line-color": t.rail, "line-width": larg(.6), "line-dasharray": [4, 3] }, 10, { "line-join": "round" }),
      { id: "bati", type: "fill-extrusion", source: "omt", "source-layer": "building", minzoom: 13,
        paint: {
          "fill-extrusion-color": ["interpolate", ["linear"], ["coalesce", ["get", "render_height"], 6], 0, t.bati0, 30, t.bati1, 160, t.bati2],
          "fill-extrusion-height": ["interpolate", ["linear"], ["zoom"], 13, 0, 14.2, ["*", 1.25, ["coalesce", ["get", "render_height"], 6]]],
          "fill-extrusion-base": ["interpolate", ["linear"], ["zoom"], 13, 0, 14.2, ["coalesce", ["get", "render_min_height"], 0]],
          "fill-extrusion-opacity": t.batiOp, "fill-extrusion-vertical-gradient": true
        } }
    ];
  }
  function ciel(t) {
    return { "sky-color": t.ciel, "sky-horizon-blend": .7, "horizon-color": t.horizon, "horizon-fog-blend": .8, "fog-color": t.brume, "fog-ground-blend": .6,
      "atmosphere-blend": ["interpolate", ["linear"], ["zoom"], 0, t.atmo, 4, t.atmo, 6.5, 0] };
  }
  function lumiere(t) { return { anchor: "viewport", color: t.lumiere, intensity: .4, position: [1.4, 215, 38] }; }
  function style(t, opt) {
    var s = {
      version: 8,
      projection: { type: opt.globe ? "globe" : "mercator" },
      sources: {
        omt: { type: "vector", url: TUILES },
        relief: { type: "raster-dem", tiles: [RELIEF], tileSize: 512, maxzoom: 11, encoding: "terrarium" }
      },
      layers: couches(t), sky: ciel(t), light: lumiere(t)
    };
    if (opt.relief3d) {
      s.sources.sol = { type: "raster-dem", tiles: [RELIEF], tileSize: 512, maxzoom: 11, encoding: "terrarium" };
      s.terrain = { source: "sol", exaggeration: opt.relief3d };
    }
    return s;
  }

  /* ---------------------------------------------------------------- Chargement de la bibliothèque (une fois) */
  var lib = null;
  function bibliotheque() {
    if (lib) return lib;
    lib = new Promise(function (ok, non) {
      if (window.maplibregl) return ok();
      var css = document.createElement("link"); css.rel = "stylesheet"; css.href = LIB + ".css"; document.head.appendChild(css);
      var js = document.createElement("script"); js.src = LIB + ".js"; js.onload = function () { window.maplibregl ? ok() : non(new Error("bibliothèque")); };
      js.onerror = function () { non(new Error("bibliothèque")); };
      document.head.appendChild(js);
    });
    return lib;
  }

  /* ---------------------------------------------------------------- Ouvrir une carte */
  var cartes = [];
  function repeint(carte) {
    var t = ton();
    couches(t).forEach(function (l) {
      Object.keys(l.paint).forEach(function (k) { try { carte.setPaintProperty(l.id, k, l.paint[k]); } catch (e) {} });
    });
    try { carte.setSky(ciel(t)); carte.setLight(lumiere(t)); } catch (e) {}
    (carte._jvTrajets || []).forEach(function (tr) { tr.teinte(); });
  }
  /* hote : élément vide qui reçoit la carte. opt : centre [lon, lat], zoom, pitch, bearing, globe (vrai ou faux),
     relief3d (exagération du relief en 3D, 0 = à plat), interactive. Rend une promesse de carte prête. */
  function ouvre(hote, opt) {
    opt = opt || {};
    return bibliotheque().then(function () {
      return new Promise(function (ok, non) {
        var carte, fini = false;
        function rate(e) {
          if (fini) return;
          fini = true; clearTimeout(garde);
          try { if (carte) carte.remove(); } catch (x) {}
          non(e instanceof Error ? e : new Error("carte"));
        }
        var garde = setTimeout(function () { rate(new Error("délai")); }, opt.delai || 60000);
        try {
          carte = new window.maplibregl.Map({
            container: hote, style: style(ton(), opt), center: opt.center || [-72.9, 46.4], zoom: opt.zoom == null ? 6 : opt.zoom,
            pitch: opt.pitch || 0, bearing: opt.bearing || 0, minZoom: .6, maxZoom: 16.8, maxPitch: 72,
            interactive: opt.interactive !== false, attributionControl: false, fadeDuration: 0, renderWorldCopies: true,
            dragRotate: true, pitchWithRotate: true, keyboard: false, canvasContextAttributes: { antialias: true }
          });
        } catch (e) { return rate(e); }
        /* Avant d'être prête : une erreur du style ou des tuiles de base annule tout; le relief seul n'est pas essentiel */
        carte.on("error", function (e) { if (!fini && !(e && e.sourceId && e.sourceId !== "omt")) rate(e && e.error); });
        carte.on("load", function () {
          if (fini) return;
          fini = true; clearTimeout(garde);
          cartes.push(carte);
          carte.on("remove", function () { cartes = cartes.filter(function (c) { return c !== carte; }); });
          ok(carte);
        });
      });
    });
  }
  /* Le mode (Base, Signature, Platinum) change : toutes les cartes ouvertes reprennent leurs teintes */
  new MutationObserver(function () { cartes.forEach(repeint); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ["data-mode"] });

  /* ---------------------------------------------------------------- Trajet lumineux qui se dessine
     points : [[lon, lat], …]; km (facultatif) : distance cumulée de chaque point. Rend
     { avance(f) → { lon, lat, cap } pour f de 0 à 1, visible(oui), bornes } */
  function trajet(carte, id, points, km) {
    var n = points.length, cum = km;
    if (!cum) {
      cum = [0];
      for (var i = 1; i < n; i++) {
        var a = points[i - 1], b = points[i], k = Math.cos((a[1] + b[1]) / 2 * Math.PI / 180);
        cum.push(cum[i - 1] + Math.hypot((b[0] - a[0]) * 111.32 * k, (b[1] - a[1]) * 111.13));
      }
    }
    var total = cum[n - 1], vide = { type: "Feature", geometry: { type: "LineString", coordinates: [points[0], points[0]] } };
    carte.addSource(id + "-tout", { type: "geojson", data: { type: "Feature", geometry: { type: "LineString", coordinates: points } } });
    carte.addSource(id + "-fait", { type: "geojson", data: vide });
    carte.addSource(id + "-tete", { type: "geojson", data: { type: "Feature", geometry: { type: "Point", coordinates: points[0] } } });
    carte.addLayer({ id: id + "-tout", type: "line", source: id + "-tout", layout: ROND, paint: { "line-width": 2.2, "line-opacity": .5, "line-dasharray": [.2, 2.4] } });
    carte.addLayer({ id: id + "-halo", type: "line", source: id + "-fait", layout: ROND, paint: { "line-width": ["interpolate", ["linear"], ["zoom"], 4, 9, 12, 20], "line-opacity": .34, "line-blur": 9 } });
    carte.addLayer({ id: id + "-fait", type: "line", source: id + "-fait", layout: ROND, paint: { "line-width": ["interpolate", ["linear"], ["zoom"], 4, 2.6, 12, 4.6] } });
    carte.addLayer({ id: id + "-lueur", type: "circle", source: id + "-tete", paint: { "circle-radius": 17, "circle-blur": 1, "circle-opacity": .55, "circle-pitch-alignment": "map" } });
    carte.addLayer({ id: id + "-tete", type: "circle", source: id + "-tete", paint: { "circle-radius": 5.5, "circle-stroke-width": 2.5, "circle-stroke-color": "#000000" } });
    var ids = ["-tout", "-halo", "-fait", "-lueur", "-tete"].map(function (s) { return id + s; }), tete = true, voit = true;
    function teinte() {
      var t = ton();
      try {
        carte.setPaintProperty(id + "-tout", "line-color", t.trajet);
        carte.setPaintProperty(id + "-halo", "line-color", t.halo);
        carte.setPaintProperty(id + "-fait", "line-color", t.trajet);
        carte.setPaintProperty(id + "-lueur", "circle-color", t.halo);
        carte.setPaintProperty(id + "-tete", "circle-color", t.trajet);
      } catch (e) {}
    }
    teinte();
    (carte._jvTrajets = carte._jvTrajets || []).push({ teinte: teinte });
    function applique() {
      ids.forEach(function (l) {
        var on = voit && (tete || !/-(lueur|tete)$/.test(l));
        try { carte.setLayoutProperty(l, "visibility", on ? "visible" : "none"); } catch (e) {}
      });
    }
    var w = points[0][0], e = w, s = points[0][1], nn = s;
    points.forEach(function (p) { w = Math.min(w, p[0]); e = Math.max(e, p[0]); s = Math.min(s, p[1]); nn = Math.max(nn, p[1]); });
    return {
      total: total, bornes: [[w, s], [e, nn]],
      /* f de 0 à 1 (ou kilomètres si enKm) : la partie parcourue s'allume, la tête avance */
      avance: function (f, enKm) {
        var d = Math.max(0, Math.min(total, enKm ? f : f * total)), lo = 0, hi = n - 1;
        while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (cum[mid] < d) lo = mid; else hi = mid; }
        var a = points[lo], b = points[hi], r = Math.min(1, Math.max(0, (d - cum[lo]) / ((cum[hi] - cum[lo]) || 1)));
        var p = [a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r];
        var fait = points.slice(0, lo + 1); fait.push(p);
        if (fait.length < 2) fait.push(p);
        carte.getSource(id + "-fait").setData({ type: "Feature", geometry: { type: "LineString", coordinates: fait } });
        carte.getSource(id + "-tete").setData({ type: "Feature", geometry: { type: "Point", coordinates: p } });
        var kx = Math.cos(p[1] * Math.PI / 180);
        return { lon: p[0], lat: p[1], cap: Math.atan2((b[0] - a[0]) * kx, b[1] - a[1]) * 180 / Math.PI };
      },
      visible: function (on) { voit = !!on; applique(); },
      tete: function (on) { tete = !!on; applique(); }
    };
  }

  /* Largeur visible au centre de la carte, en kilomètres (pour l'échelle et le regroupement des repères) */
  function largeurKm(carte) {
    var c = carte.getCenter(), el = carte.getContainer();
    return 78271.517 * Math.cos(c.lat * Math.PI / 180) / Math.pow(2, carte.getZoom()) * el.clientWidth / 1000;
  }
  function zoomPour(km, lat, px) { return Math.log(78271.517 * Math.cos(lat * Math.PI / 180) * px / (km * 1000)) / Math.LN2; }

  window.JarvisCarte = { ouvre: ouvre, trajet: trajet, ton: ton, largeurKm: largeurKm, zoomPour: zoomPour };
})();
