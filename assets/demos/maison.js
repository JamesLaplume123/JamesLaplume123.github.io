/* Démo « Ma maison » : les pièces s'allument, se règlent et confirment chaque commande.
   Démonstration seulement : aucun appareil réel n'est commandé. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var TONES = {
    chaude: "none",
    neutre: "saturate(.7) brightness(1.06)",
    froide: "saturate(.3) brightness(1.16) hue-rotate(-12deg)",
    cinema: "hue-rotate(245deg) saturate(1.7) brightness(.92)",
    eau: "saturate(1.15) brightness(1.05)"
  };
  var CLOCK = { matin: "Matin · 6 h 58", soiree: "Soirée · 19 h 42", cinema: "Cinéma · 21 h 05", nuit: "Nuit · 23 h 30", absent: "Absent · 14 h 10" };

  document.querySelectorAll('[data-demo="maison"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var data;
    try { data = JSON.parse($('[data-mz="data"]').textContent); } catch (e) { return; }
    var rooms = {}, order = [];
    data.rooms.forEach(function (r) {
      rooms[r.k] = {
        def: r, lvl: 0, on: false, tone: "chaude", temp: r.temp, lock: !!r.lock, door: false, store: false,
        fire: false, water: r.water, img: $('.mz-lit[data-room="' + r.k + '"]'), tag: $('.mz-tag[data-room="' + r.k + '"]'),
        poly: $('.mz-hit polygon[data-room="' + r.k + '"]'), bloom: $('.mz-bloom[data-room="' + r.k + '"]')
      };
      order.push(r.k);
    });
    var sel = "salon", sceneKey = null, watts = 0, wattsShown = 0;
    var el = {
      name: $('[data-mz="room-name"]'), sw: $('[data-mz="switch"]'), lvl: $('[data-mz="lvl"]'), lvlV: $('[data-mz="lvl-v"]'),
      ack: $('[data-mz="ack"]'), extra: $('[data-mz="extra"]'), watts: $('[data-mz="watts"]'), locks: $('[data-mz="locks"]'),
      state: $('[data-mz="state"]'), tones: $$(".mz-temps button"), scenes: $$(".mz-scenes button")
    };

    function paintRoom(k, bloom) {
      var r = rooms[k];
      var v = r.on ? r.lvl : 0;
      r.img.style.setProperty("--lvl", v.toFixed(2));
      r.img.style.setProperty("--tone", TONES[r.tone] || "none");
      r.tag.classList.toggle("is-on", r.on && v > 0);
      var bits = [];
      bits.push(r.on && v > 0 ? Math.round(v * 100) + " %" : "Éteint");
      if (r.def.lock) bits.push(r.lock ? "verrouillée" : "déverrouillée");
      if (r.def.door) bits.push(r.door ? "porte ouverte" : "porte fermée");
      if (r.def.temp && !r.def.lock) bits.push(r.temp.toString().replace(".", ",") + " °C");
      r.tag.querySelector(".mz-tag-v").textContent = bits.join(" · ");
      if (bloom && !reduce && r.bloom) { r.bloom.classList.remove("go"); void r.bloom.offsetWidth; r.bloom.classList.add("go"); }
    }

    function totals() {
      watts = 260;
      order.forEach(function (k) {
        var r = rooms[k];
        if (r.on) watts += r.lvl * r.def.w;
        if (k === "piscine" && r.on) watts += 650;
        if (k === "terrasse" && r.fire) watts += 40;
      });
      if (root.hasAttribute("data-away")) watts -= 120;
      tween();
      var open = order.filter(function (k) { var r = rooms[k]; return (r.def.lock && !r.lock) || (r.def.door && r.door); }).length;
      el.locks.textContent = open ? open + " ouverte" + (open > 1 ? "s" : "") : "Verrouillées";
      el.locks.style.color = open ? "#fcd34d" : "#9fe8bc";
    }
    function tween() {
      if (reduce) { wattsShown = watts; el.watts.textContent = Math.round(watts) + " W"; return; }
      var from = wattsShown, to = watts, t0 = performance.now();
      (function step(t) {
        var k = Math.min(1, (t - t0) / 900), e = 1 - Math.pow(1 - k, 3);
        wattsShown = from + (to - from) * e;
        el.watts.textContent = Math.round(wattsShown).toLocaleString("fr-CA") + " W";
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    }

    var ackTimer = null;
    function ack(k) {
      var r = rooms[k];
      r.tag.classList.add("is-pending");
      if (k === sel) { el.ack.className = "mz-ack is-sent"; el.ack.textContent = "Envoyé"; }
      clearTimeout(ackTimer);
      setTimeout(function () {
        r.tag.classList.remove("is-pending");
        if (k !== sel) return;
        el.ack.className = "mz-ack is-ok"; el.ack.textContent = "Confirmé";
        ackTimer = setTimeout(function () { el.ack.className = "mz-ack"; }, 1600);
      }, reduce ? 0 : 650);
    }

    function extraButtons(r) {
      var h = "";
      if (r.def.temp && !r.def.lock) {
        h += '<div class="mz-thermo"><span><small>Chauffage</small><br><b>' + r.temp.toString().replace(".", ",") +
          ' °C</b></span><span><button type="button" data-x="cold" aria-label="Baisser">−</button> ' +
          '<button type="button" data-x="hot" aria-label="Monter">+</button></span></div>';
      }
      if (r.def.store) h += '<button type="button" class="mz-wide" data-x="store">' + (r.store ? "Ouvrir les stores" : "Fermer les stores") + "</button>";
      if (r.def.lock) h += '<button type="button" class="mz-wide' + (r.lock ? " is-locked" : "") + '" data-x="lock">' + (r.lock ? "Verrouillée · déverrouiller" : "Ouverte · verrouiller") + "</button>";
      if (r.def.door) h += '<button type="button" class="mz-wide" data-x="door">' + (r.door ? "Fermer la porte de garage" : "Ouvrir la porte de garage") + "</button>";
      if (r.def.fire) h += '<button type="button" class="mz-wide" data-x="fire">' + (r.fire ? "Éteindre le foyer" : "Allumer le foyer") + "</button>";
      if (r.def.water) h += '<div class="mz-thermo"><span><small>Eau de la piscine</small><br><b>' + r.water + ' °C</b></span><span><button type="button" data-x="wcold" aria-label="Baisser">−</button> <button type="button" data-x="whot" aria-label="Monter">+</button></span></div>';
      return h;
    }

    function select(k) {
      sel = k;
      var r = rooms[k];
      order.forEach(function (x) {
        rooms[x].poly.classList.toggle("is-sel", x === k);
        rooms[x].tag.classList.toggle("is-sel", x === k);
      });
      el.name.textContent = r.def.name;
      el.ack.className = "mz-ack";
      syncPanel();
    }
    function syncPanel() {
      var r = rooms[sel], v = Math.round((r.on ? r.lvl : 0) * 100);
      el.sw.setAttribute("aria-checked", r.on && v > 0 ? "true" : "false");
      el.lvl.value = v;
      el.lvl.style.setProperty("--p", v + "%");
      el.lvlV.textContent = v + " %";
      el.tones.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-tone") === r.tone); });
      el.extra.innerHTML = extraButtons(r);
    }

    function setRoom(k, lvl, tone, bloom) {
      var r = rooms[k], was = r.on && r.lvl > 0;
      r.lvl = lvl;
      r.on = lvl > 0;
      if (tone) r.tone = tone;
      paintRoom(k, bloom && !was && r.on);
    }

    function scene(key) {
      var s = data.scenes[key];
      if (!s) return;
      sceneKey = key;
      el.scenes.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-scene") === key); });
      el.state.textContent = CLOCK[key] || "";
      if (s.away) root.setAttribute("data-away", ""); else root.removeAttribute("data-away");
      order.forEach(function (k, i) {
        var t = s.rooms[k];
        setTimeout(function () {
          setRoom(k, t ? t[0] : 0, t ? t[1] : null, true);
          var r = rooms[k];
          if (r.def.lock) r.lock = !!s.lock || key === "nuit" || key === "absent";
          if (r.def.door) r.door = false;
          if (r.def.fire) r.fire = key === "soiree";
          if (r.def.store) r.store = key === "cinema" || key === "nuit";
          paintRoom(k, false);
          if (k === sel) syncPanel();
          totals();
        }, reduce ? 0 : i * 110);
      });
    }

    /* Interactions */
    $$(".mz-hit polygon, .mz-tag").forEach(function (n) {
      n.addEventListener("click", function () { select(n.getAttribute("data-room")); });
    });
    el.scenes.forEach(function (b) { b.addEventListener("click", function () { scene(b.getAttribute("data-scene")); }); });
    el.sw.addEventListener("click", function () {
      var r = rooms[sel], isOn = r.on && r.lvl > 0;
      if (isOn) { r.on = false; paintRoom(sel); }
      else { if (!(r.lvl > 0)) r.lvl = .7; r.on = true; paintRoom(sel, true); }
      syncPanel(); totals(); ack(sel); clearScene();
    });
    el.lvl.addEventListener("input", function () {
      var v = +el.lvl.value / 100;
      setRoom(sel, v, null, true);
      el.lvl.style.setProperty("--p", el.lvl.value + "%");
      el.lvlV.textContent = el.lvl.value + " %";
      el.sw.setAttribute("aria-checked", v > 0 ? "true" : "false");
      totals();
    });
    el.lvl.addEventListener("change", function () { ack(sel); clearScene(); });
    el.tones.forEach(function (b) {
      b.addEventListener("click", function () {
        var r = rooms[sel];
        r.tone = b.getAttribute("data-tone");
        if (!r.on || r.lvl === 0) setRoom(sel, .7, null, true);
        paintRoom(sel); syncPanel(); totals(); ack(sel); clearScene();
      });
    });
    el.extra.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      var r = rooms[sel], x = b.getAttribute("data-x");
      /* Action sensible : on demande une confirmation explicite avant d'envoyer */
      var sensitive = (x === "lock" && r.lock) || (x === "door" && !r.door);
      if (sensitive && !b.hasAttribute("data-confirm")) {
        b.setAttribute("data-confirm", "");
        b.textContent = x === "lock" ? "Confirmer le déverrouillage" : "Confirmer l’ouverture";
        b.style.borderColor = "#fcd34d";
        return;
      }
      if (x === "hot") r.temp = Math.min(26, r.temp + .5);
      if (x === "cold") r.temp = Math.max(15, r.temp - .5);
      if (x === "whot") r.water = Math.min(32, r.water + 1);
      if (x === "wcold") r.water = Math.max(20, r.water - 1);
      if (x === "store") r.store = !r.store;
      if (x === "lock") r.lock = !r.lock;
      if (x === "door") r.door = !r.door;
      if (x === "fire") r.fire = !r.fire;
      paintRoom(sel); syncPanel(); totals(); ack(sel); clearScene();
    });
    function clearScene() {
      if (!sceneKey) return;
      sceneKey = null;
      el.scenes.forEach(function (b) { b.classList.remove("is-on"); });
      el.state.textContent = "Personnalisé";
    }

    /* Départ : tout est éteint, puis la soirée s'allume pièce par pièce */
    order.forEach(function (k) { paintRoom(k); });
    select("salon");
    totals();
    var started = false;
    function start() {
      if (started) return;
      started = true;
      setTimeout(function () { scene("soiree"); }, reduce ? 0 : 900);
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es, obs) {
        es.forEach(function (e) { if (e.isIntersecting) { start(); obs.disconnect(); } });
      }, { threshold: .35 }).observe(root);
    } else start();
  });
})();
