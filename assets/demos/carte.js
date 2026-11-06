/* « Radar en direct » : MapLibre (hébergé sur le site) + radar WMS d'Environnement Canada.
   La bibliothèque n'est chargée qu'à l'approche de la carte. Boucle sur la dernière heure
   (12 images aux 6 minutes, comme le radar). Toutes les minutes, tant que la carte est visible,
   le site redemande la dernière image publiée : dès qu'elle paraît, elle s'ajoute au bout. */
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
  var STEP = 6 * 60000, N = 12;
  /* Dernière image publiée par Environnement Canada (null si le service ne répond pas) */
  function latest() {
    return fetch(CAPS + "&_=" + Math.floor(Date.now() / 60000), { cache: "no-store" }).then(function (r) { return r.text(); }).then(function (x) {
      var m = x.match(/<Dimension name="time"[^>]*>([^<]+)<\/Dimension>/);
      var end = m ? new Date(m[1].split("/")[1]) : null;
      return end && !isNaN(end) ? end : null;
    }).catch(function () { return null; });
  }
  function frames() {
    return latest().then(function (end) {
      if (!end) {
        end = new Date(Date.now() - 12 * 60000);
        end.setUTCMinutes(Math.floor(end.getUTCMinutes() / 6) * 6, 0, 0);
      }
      var out = [];
      for (var i = N - 1; i >= 0; i--) out.push(new Date(end.getTime() - i * STEP));
      return out;
    });
  }
  function ago(d) {
    var m = Math.max(0, Math.round((Date.now() - d.getTime()) / 60000));
    return m < 1 ? "à l’instant" : "il y a " + m + " min";
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
        var cur = times.length - 1, playing = !reduce, timer = null, ready = false, visible = true;
        var track = $('[data-ct="track"]'), play = $('[data-ct="play"]'), stamp = $('[data-ct="time"]');
        function key(t) { return String(t.getTime()); }
        function addLayer(t) {
          var iso = t.toISOString().replace(".000", "");
          [["r", "RADAR_1KM_RRAI"], ["s", "RADAR_1KM_RSNO"]].forEach(function (L) {
            var id = L[0] + key(t);
            if (map.getLayer(id)) return;
            map.addSource(id, { type: "raster", tileSize: 256, tiles: [WMS + "&LAYERS=" + L[1] + "&TIME=" + iso] });
            map.addLayer({ id: id, type: "raster", source: id, paint: { "raster-opacity": 0, "raster-fade-duration": 0 } });
          });
        }
        function dropLayer(t) {
          ["r", "s"].forEach(function (L) {
            var id = L + key(t);
            if (map.getLayer(id)) map.removeLayer(id);
            if (map.getSource(id)) map.removeSource(id);
          });
        }
        function buttons() {
          track.innerHTML = "";
          times.forEach(function (t, i) {
            var b = document.createElement("button");
            var last = i === times.length - 1;
            b.type = "button"; b.textContent = last ? "Maintenant" : hm(t);
            b.setAttribute("aria-label", "Radar de " + hm(t));
            if (last) b.className = "is-live";
            b.addEventListener("click", function () { playing = false; clearTimeout(timer); play.textContent = "▶"; play.setAttribute("aria-label", "Lancer l’animation"); show(i); });
            track.appendChild(b);
          });
        }
        function label() {
          var t = times[cur], last = cur === times.length - 1;
          stamp.textContent = "Radar · " + hm(t) + " · " + ago(t);
          root.classList.toggle("is-live", last && Date.now() - times[times.length - 1].getTime() < 20 * 60000);
        }
        function show(i) {
          cur = i;
          times.forEach(function (t, k) {
            ["r", "s"].forEach(function (L) {
              var id = L + key(t);
              if (map.getLayer(id)) map.setPaintProperty(id, "raster-opacity", k === i ? .78 : 0);
            });
          });
          [].forEach.call(track.children, function (b, k) { b.classList.toggle("is-on", k === i); });
          label();
        }
        function loop() {
          clearTimeout(timer);
          if (!playing) return;
          timer = setTimeout(function () { show((cur + 1) % times.length); loop(); }, cur === times.length - 1 ? 2400 : 520);
        }
        /* Toutes les minutes : y a-t-il une image plus récente ? Si oui, elle s'ajoute au bout. */
        function refresh() {
          if (!ready || !visible || document.hidden) return;
          latest().then(function (end) {
            if (!end) return;
            var lastT = times[times.length - 1], added = false;
            for (var t = lastT.getTime() + STEP; t <= end.getTime(); t += STEP) {
              var d = new Date(t);
              times.push(d); addLayer(d); added = true;
              while (times.length > N) { dropLayer(times.shift()); cur = Math.max(0, cur - 1); }
            }
            if (!added) return;
            buttons();
            if (!playing) show(times.length - 1); else show(Math.min(cur, times.length - 1));
          });
        }
        buttons();
        play.addEventListener("click", function () {
          playing = !playing;
          play.textContent = playing ? "❚❚" : "▶";
          play.setAttribute("aria-label", playing ? "Mettre en pause l’animation" : "Lancer l’animation");
          loop();
        });
        map.on("load", function () {
          var w = $('[data-ct="wait"]'); if (w) w.remove();
          times.forEach(addLayer);
          ready = true;
          show(cur);
          setTimeout(loop, 1200);
        });
        setInterval(refresh, 60000);
        setInterval(function () { if (ready) label(); }, 30000);
        document.addEventListener("visibilitychange", function () { if (!document.hidden) refresh(); });
        if ("IntersectionObserver" in window) {
          new IntersectionObserver(function (es) {
            es.forEach(function (e) { visible = e.isIntersecting; if (visible) refresh(); });
          }).observe(root);
        }
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
