/* « Radar en direct » : MapLibre (hébergé sur le site) + radar WMS d'Environnement Canada.
   La bibliothèque n'est chargée qu'à l'approche de la carte. Boucle sur ~1 h 30 (8 images). */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var HOME = [-72.956, 45.631]; // Saint-Hyacinthe, lieu de base fixe (aucun GPS en direct)
  var WMS = "https://geo.weather.gc.ca/geomet?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=TRUE" +
    "&CRS=EPSG:3857&WIDTH=256&HEIGHT=256&BBOX={bbox-epsg-3857}";
  var CAPS = "https://geo.weather.gc.ca/geomet?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities&LAYER=RADAR_1KM_RRAI";
  var EC = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/qc-22?f=json&lang=fr";
  var V = (document.querySelector('script[src*="carte.js"]') || {}).src || "";
  var ver = (V.split("?v=")[1] || "1");

  function loadLib() {
    if (window.maplibregl) return Promise.resolve();
    return new Promise(function (res, rej) {
      var css = document.createElement("link");
      css.rel = "stylesheet"; css.href = "/assets/vendor/maplibre-gl.css?v=" + ver;
      document.head.appendChild(css);
      var s = document.createElement("script");
      s.src = "/assets/vendor/maplibre-gl.js?v=" + ver; s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
    });
  }
  function hm(d) {
    try {
      return new Intl.DateTimeFormat("fr-CA", { timeZone: "America/Toronto", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
        .format(d).replace(":", " h ");
    } catch (e) { return d.getHours() + " h " + String(d.getMinutes()).padStart(2, "0"); }
  }
  function frames() {
    return fetch(CAPS).then(function (r) { return r.text(); }).then(function (x) {
      var m = x.match(/<Dimension name="time"[^>]*>([^<]+)<\/Dimension>/);
      var end = m ? new Date(m[1].split("/")[1]) : null;
      if (!end || isNaN(end)) throw new Error("temps");
      return end;
    }).catch(function () {
      var d = new Date(Date.now() - 12 * 60000);
      d.setUTCMinutes(Math.floor(d.getUTCMinutes() / 6) * 6, 0, 0);
      return d;
    }).then(function (end) {
      var out = [];
      for (var i = 7; i >= 0; i--) out.push(new Date(end.getTime() - i * 12 * 60000));
      return out;
    });
  }

  document.querySelectorAll('[data-demo="carte"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var started = false;

    function weather() {
      var c = null;
      try { c = JSON.parse(sessionStorage.getItem("jarvis-ec")); } catch (e) {}
      var p = c && Date.now() - c.t < 300000 ? Promise.resolve(c.j) : fetch(EC).then(function (r) { return r.json(); });
      p.then(function (j) {
        var cc = (j.properties || {}).currentConditions || {};
        var t = cc.temperature && cc.temperature.value ? parseFloat(cc.temperature.value.fr != null ? cc.temperature.value.fr : cc.temperature.value.en) : NaN;
        if (isFinite(t)) $('[data-ct="temp"]').textContent = String(Math.round(t)).replace("-", "−") + " °C";
        var cond = cc.condition ? (cc.condition.fr || cc.condition.en) : "";
        if (cond) $('[data-ct="cond"]').textContent = cond;
      }).catch(function () {});
    }

    function start() {
      if (started) return;
      started = true;
      weather();
      Promise.all([loadLib(), frames()]).then(function (res) {
        var times = res[1];
        var map = new maplibregl.Map({
          container: $('[data-ct="map"]'), style: "https://tiles.openfreemap.org/styles/dark",
          center: HOME, zoom: 6.4, minZoom: 4, maxZoom: 10, attributionControl: false,
          cooperativeGestures: true, pitch: 0, dragRotate: false
        });
        map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
        var el = document.createElement("div");
        el.className = "ct-marker";
        el.innerHTML = "<i></i><b>BouLance · Saint-Hyacinthe</b>";
        new maplibregl.Marker({ element: el, anchor: "left", offset: [-9, 0] }).setLngLat(HOME).addTo(map);
        var cur = times.length - 1, playing = !reduce, timer = null;
        var track = $('[data-ct="track"]'), play = $('[data-ct="play"]');
        times.forEach(function (t, i) {
          var b = document.createElement("button");
          b.type = "button"; b.textContent = hm(t); b.setAttribute("aria-label", "Radar de " + hm(t));
          b.addEventListener("click", function () { playing = false; play.textContent = "▶"; show(i); });
          track.appendChild(b);
        });
        function show(i) {
          cur = i;
          times.forEach(function (_t, k) {
            ["r", "s"].forEach(function (L) {
              if (map.getLayer(L + k)) map.setPaintProperty(L + k, "raster-opacity", k === i ? .78 : 0);
            });
          });
          [].forEach.call(track.children, function (b, k) { b.classList.toggle("is-on", k === i); });
          $('[data-ct="time"]').textContent = "Radar · " + hm(times[i]);
        }
        function loop() {
          clearTimeout(timer);
          if (!playing) return;
          timer = setTimeout(function () { show((cur + 1) % times.length); loop(); }, cur === times.length - 1 ? 1800 : 650);
        }
        play.addEventListener("click", function () {
          playing = !playing;
          play.textContent = playing ? "❚❚" : "▶";
          play.setAttribute("aria-label", playing ? "Mettre en pause l’animation" : "Lancer l’animation");
          loop();
        });
        map.on("load", function () {
          var w = $('[data-ct="wait"]'); if (w) w.remove();
          times.forEach(function (t, k) {
            var iso = t.toISOString().replace(".000", "");
            [["r", "RADAR_1KM_RRAI"], ["s", "RADAR_1KM_RSNO"]].forEach(function (L) {
              map.addSource(L[0] + k, { type: "raster", tileSize: 256, tiles: [WMS + "&LAYERS=" + L[1] + "&TIME=" + iso] });
              map.addLayer({ id: L[0] + k, type: "raster", source: L[0] + k, paint: { "raster-opacity": 0, "raster-fade-duration": 0 } });
            });
          });
          show(cur);
          setTimeout(loop, 1200);
        });
      }).catch(function () {
        var w = $('[data-ct="wait"]');
        if (w) w.textContent = "La carte ne répond pas pour le moment.";
      });
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es, o) {
        es.forEach(function (e) { if (e.isIntersecting) { start(); o.disconnect(); } });
      }, { rootMargin: "300px" }).observe(root);
    } else start();
  });
})();
