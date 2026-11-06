/* Démo « Ma maison » : chaque pièce s'allume comme derrière un vrai gradateur.
   La photo du plan n'est jamais retouchée : la nuit est un voile posé dessus, et une
   pièce allumée révèle la photo à travers son masque (murs nets, débord doux par les
   portes), puis ajoute le halo de ses luminaires, teinté selon la couleur choisie.
   Les ambiances se déroulent pièce par pièce, comme une vraie scène.
   Démonstration seulement : aucun appareil réel n'est commandé. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  /* Couleur de la lumière : c = halo des luminaires, t = voile coloré sur la pièce éclairée.
     Chaude ≈ 2700 K (ambre), Neutre ≈ 4000 K, Froide ≈ 5500 K (pointe de bleu). */
  var TONES = {
    chaude: { c: "#ffb35c", t: "rgba(255, 150, 60, .2)" },
    neutre: { c: "#ffe7cc", t: "rgba(130, 165, 255, .3)" },
    froide: { c: "#d2e1ff", t: "rgba(80, 135, 255, .68)" },
    cinema: { c: "#6585ff", t: "rgba(45, 80, 255, .75)" },
    eau: { c: "#5edcff", t: "rgba(40, 200, 255, .22)" }
  };
  var CLOCK = { matin: "Matin · 6 h 58", soiree: "Soirée · 19 h 42", cinema: "Cinéma · 21 h 05", nuit: "Nuit · 23 h 30", absent: "Absent · 14 h 10" };

  var EDGE = 4, SPILL = 22; /* flou des murs et du débord par les ouvertures, en pixels de l'image */

  /* Cadre d'une pièce : son polygone et ses ouvertures, plus la marge du flou.
     Les couches de lumière n'occupent que ce cadre (moins de surface à peindre). */
  function frame(r, W, H) {
    var xs = [], ys = [];
    r.poly.forEach(function (p) { xs.push(p[0] - 3 * EDGE, p[0] + 3 * EDGE); ys.push(p[1] - 3 * EDGE, p[1] + 3 * EDGE); });
    r.d.forEach(function (d) { xs.push(d[0] - d[2] - 3 * SPILL, d[0] + d[2] + 3 * SPILL); ys.push(d[1] - d[3] - 3 * SPILL, d[1] + d[3] + 3 * SPILL); });
    var x0 = Math.max(0, Math.floor(Math.min.apply(0, xs))), y0 = Math.max(0, Math.floor(Math.min.apply(0, ys)));
    var x1 = Math.min(W, Math.ceil(Math.max.apply(0, xs))), y1 = Math.min(H, Math.ceil(Math.max.apply(0, ys)));
    return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
  }

  /* Masque d'une pièce, dessiné une seule fois en image : la pièce (murs adoucis, plus claire
     près des luminaires) et ses ouvertures, où la lumière déborde à moitié. Le flou passe par
     l'ombre portée du canevas, reconnue par tous les navigateurs. */
  function mask(r, box) {
    var S = .6, w = Math.ceil(box.w * S), h = Math.ceil(box.h * S);
    function layer(sigma, alpha, paint) {
      var c = document.createElement("canvas"), g = c.getContext("2d"), off = w + 8 * sigma * S + 40;
      c.width = w; c.height = h;
      g.shadowColor = "rgba(255, 255, 255, " + alpha + ")"; g.shadowBlur = 2 * sigma * S; g.shadowOffsetX = off;
      g.translate(-off, 0); g.scale(S, S); g.translate(-box.x, -box.y);
      g.fillStyle = "#fff"; g.beginPath(); paint(g); g.fill();
      return c;
    }
    var room = layer(EDGE, 1, function (g) { r.poly.forEach(function (p, i) { g[i ? "lineTo" : "moveTo"](p[0], p[1]); }); g.closePath(); });
    var near = layer(SPILL, 1, function (g) { r.f.forEach(function (f) { g.moveTo(f[0] + f[2] * .7, f[1]); g.arc(f[0], f[1], f[2] * .7, 0, 7); }); });
    var ng = near.getContext("2d");
    ng.globalCompositeOperation = "destination-in"; ng.drawImage(room, 0, 0);
    var out = document.createElement("canvas"), o = out.getContext("2d");
    out.width = w; out.height = h;
    o.globalAlpha = .7; o.drawImage(room, 0, 0);
    o.globalAlpha = 1; o.drawImage(near, 0, 0);
    if (r.d.length) {
      o.globalAlpha = .55;
      o.drawImage(layer(SPILL, 1, function (g) { r.d.forEach(function (d) { g.moveTo(d[0] + d[2], d[1]); g.ellipse(d[0], d[1], d[2], d[3], 0, 0, 7); }); }), 0, 0);
    }
    return 'url("' + out.toDataURL() + '")';
  }

  /* Halo : un dégradé radial par luminaire, positions en % du cadre. Sa couleur vient de
     --mz-<couche><sorte> (sorte 1 = principal, 2 = d'appoint, 3 = écran, 0 = lumière diffuse).
     La mi-teinte placée tôt (28 %) donne une chute rapide puis une longue traîne, comme la vraie lumière. */
  function glow(list, scale, layer, box) {
    return list.map(function (f) {
      var r = f[2] * scale;
      return "radial-gradient(" + pc(r, box.w) + " " + pc(r, box.h) + " at " + pc(f[0] - box.x, box.w) + " " + pc(f[1] - box.y, box.h) +
        ",var(--mz-" + layer + f[3] + "),28%,transparent)";
    }).join(",");
  }
  function pc(v, total) { return (v / total * 100).toFixed(2) + "%"; }

  document.querySelectorAll('[data-demo="maison"]').forEach(function (root) {
    var $ = function (s) { return root.querySelector(s); };
    var $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var data;
    try { data = JSON.parse($('[data-mz="data"]').textContent); } catch (e) { return; }
    var W = data.size[0], H = data.size[1];
    var lights = $('[data-mz="lights"]');
    var rooms = {}, order = [];
    data.rooms.forEach(function (r) {
      /* Lumière de la pièce, dans son cadre et sous un seul masque : la photo révélée, puis le halo (cœur et étendue) */
      var box = frame(r, W, H);
      var xs = r.poly.map(function (p) { return p[0]; }), ys = r.poly.map(function (p) { return p[1]; });
      var cx = (Math.min.apply(0, xs) + Math.max.apply(0, xs)) / 2, cy = (Math.min.apply(0, ys) + Math.max.apply(0, ys)) / 2;
      var reach = Math.hypot(Math.max.apply(0, xs) - Math.min.apply(0, xs), Math.max.apply(0, ys) - Math.min.apply(0, ys)) * .45;
      var l = document.createElement("div");
      l.className = "mz-l is-off";
      l.setAttribute("data-room", r.k);
      l.style.cssText = "left:" + pc(box.x, W) + ";top:" + pc(box.y, H) + ";width:" + pc(box.w, W) + ";height:" + pc(box.h, H);
      var lit = document.createElement("i"), core = document.createElement("i"), spread = document.createElement("i");
      lit.className = "mz-lit"; core.className = "mz-core"; spread.className = "mz-spread";
      /* La photo entière, placée pour que le cadre en montre exactement la bonne partie */
      lit.style.backgroundSize = "100% 100%, " + pc(W, box.w) + " " + pc(H, box.h);
      lit.style.backgroundPosition = "0 0, " + (box.w < W ? pc(box.x, W - box.w) : "0") + " " + (box.h < H ? pc(box.y, H - box.h) : "0");
      core.style.backgroundImage = glow(r.f, .6, "k", box);
      spread.style.backgroundImage = glow(r.f.concat([[cx, cy, reach, 0]]), 1.35, "p", box);
      l.appendChild(lit); l.appendChild(core); l.appendChild(spread);
      lights.appendChild(l);
      rooms[r.k] = {
        def: r, lvl: 0, on: false, tone: "chaude", temp: r.temp, lock: !!r.lock, door: false, store: false,
        fire: false, water: r.water, l: l, box: box, tag: $('.mz-tag[data-room="' + r.k + '"]'),
        poly: $('.mz-hit polygon[data-room="' + r.k + '"]')
      };
      order.push(r.k);
    });
    var sel = "salon", sceneKey = null, watts = 0, wattsShown = 0;
    var el = {
      name: $('[data-mz="room-name"]'), sw: $('[data-mz="switch"]'), lvl: $('[data-mz="lvl"]'), lvlV: $('[data-mz="lvl-v"]'),
      ack: $('[data-mz="ack"]'), extra: $('[data-mz="extra"]'), watts: $('[data-mz="watts"]'), locks: $('[data-mz="locks"]'),
      state: $('[data-mz="state"]'), tones: $$(".mz-temps button"), scenes: $$(".mz-scenes button")
    };

    /* how = "drag" pendant qu'on glisse l'intensité : la lumière suit le doigt sans traîner */
    function paintRoom(k, how) {
      var r = rooms[k], v = r.on ? r.lvl : 0, s = r.l.style, t = TONES[r.tone] || TONES.chaude;
      r.l.classList.toggle("is-off", !(v > 0));
      r.l.classList.toggle("is-drag", how === "drag");
      r.l.setAttribute("data-tone", r.tone);
      /* Courbes d'un gradateur : le cœur des luminaires paraît avant que la pièce soit pleine */
      /* En Cinéma, la pièce reste sombre et l'écran l'éclaire quel que soit le gradateur des plafonniers */
      var screen = v > 0 && r.tone === "cinema";
      s.setProperty("--mz-fill", (v > 0 ? Math.pow(v, screen ? 1 : .75) : 0).toFixed(3));
      s.setProperty("--mz-core", (v > 0 ? Math.max(Math.pow(v, .5), screen ? .85 : 0) : 0).toFixed(3));
      s.setProperty("--mz-spread", (v > 0 ? Math.max(Math.pow(v, .9), screen ? .7 : 0) : 0).toFixed(3));
      s.setProperty("--mz-c", t.c);
      s.setProperty("--mz-tint", t.t);
      if (r.def.water) {
        root.style.setProperty("--mz-water", (v > 0 ? Math.pow(v, .75) : 0).toFixed(3));
        root.classList.toggle("is-swim", v > 0);
      }
      if (r.def.fire) root.classList.toggle("is-fire", r.fire);
      r.tag.classList.toggle("is-on", v > 0);
      var bits = [];
      bits.push(v > 0 ? Math.round(v * 100) + " %" : "Éteint");
      if (r.def.lock) bits.push(r.lock ? "verrouillée" : "déverrouillée");
      if (r.def.door) bits.push(r.door ? "porte ouverte" : "porte fermée");
      if (r.def.temp && !r.def.lock) bits.push(r.temp.toString().replace(".", ",") + " °C");
      r.tag.querySelector(".mz-tag-v").textContent = bits.join(" · ");
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
    var tweenRaf = 0;
    function tween() {
      cancelAnimationFrame(tweenRaf);
      if (reduce) { wattsShown = watts; el.watts.textContent = Math.round(watts).toLocaleString("fr-CA") + " W"; return; }
      var from = wattsShown, to = watts, t0 = performance.now();
      (function step(t) {
        var k = Math.min(1, (t - t0) / 900), e = 1 - Math.pow(1 - k, 3);
        wattsShown = from + (to - from) * e;
        el.watts.textContent = Math.round(wattsShown).toLocaleString("fr-CA") + " W";
        if (k < 1) tweenRaf = requestAnimationFrame(step);
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

    function setRoom(k, lvl, tone, how) {
      var r = rooms[k];
      r.lvl = lvl;
      r.on = lvl > 0;
      if (tone) r.tone = tone;
      paintRoom(k, how);
    }

    /* Étapes d'une scène en cours : annulées par la scène suivante, jouées tout de suite
       si le visiteur reprend la main sur une pièce. */
    var steps = [];
    function later(fn, ms) {
      if (reduce || !ms) { fn(); return; }
      var s = { fn: fn };
      s.id = setTimeout(function () { steps.splice(steps.indexOf(s), 1); fn(); }, ms);
      steps.push(s);
    }
    function cancel() { steps.forEach(function (s) { clearTimeout(s.id); }); steps = []; }
    function flush() { var pending = steps; cancel(); pending.forEach(function (s) { s.fn(); }); }

    function scene(key) {
      var s = data.scenes[key];
      if (!s) return;
      cancel();
      sceneKey = key;
      el.scenes.forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-scene") === key); });
      el.state.textContent = CLOCK[key] || "";
      if (s.away) root.setAttribute("data-away", ""); else root.removeAttribute("data-away");
      /* Portes, foyer et stores suivent la scène tout de suite; seule la lumière se déroule */
      order.forEach(function (k) {
        var r = rooms[k];
        if (r.def.lock) r.lock = !!s.lock || key === "nuit" || key === "absent";
        if (r.def.door) r.door = false;
        if (r.def.fire) r.fire = key === "soiree";
        if (r.def.store) r.store = key === "cinema" || key === "nuit";
        paintRoom(k);
      });
      /* Chorégraphie : les pièces à éteindre s'éteignent en vague rapide, puis les pièces
         de la scène s'allument une à une dans l'ordre de la scène (≈ 1,2 s en tout). */
      var offs = order.filter(function (k) { return !s.rooms[k] && rooms[k].on; });
      var ons = Object.keys(s.rooms);
      var step = Math.min(220, 1100 / Math.max(1, ons.length)), t0 = offs.length ? 160 : 0;
      offs.forEach(function (k, i) {
        later(function () {
          setRoom(k, 0);
          if (k === sel) syncPanel();
          totals();
        }, i * 70);
      });
      ons.forEach(function (k, i) {
        later(function () {
          setRoom(k, s.rooms[k][0], s.rooms[k][1]);
          if (k === sel) syncPanel();
          totals();
        }, t0 + i * step);
      });
      syncPanel();
      totals();
    }

    /* Interactions */
    $$(".mz-hit polygon, .mz-tag").forEach(function (n) {
      n.addEventListener("click", function () { select(n.getAttribute("data-room")); });
    });
    el.scenes.forEach(function (b) { b.addEventListener("click", function () { scene(b.getAttribute("data-scene")); }); });
    el.sw.addEventListener("click", function () {
      flush();
      var r = rooms[sel];
      if (r.on && r.lvl > 0) r.on = false;
      else { if (!(r.lvl > 0)) r.lvl = .7; r.on = true; }
      paintRoom(sel);
      syncPanel(); totals(); ack(sel); clearScene();
    });
    el.lvl.addEventListener("input", function () {
      flush();
      var v = +el.lvl.value / 100;
      setRoom(sel, v, null, "drag");
      el.lvl.style.setProperty("--p", el.lvl.value + "%");
      el.lvlV.textContent = el.lvl.value + " %";
      el.sw.setAttribute("aria-checked", v > 0 ? "true" : "false");
      totals();
    });
    el.lvl.addEventListener("change", function () { paintRoom(sel); ack(sel); clearScene(); });
    el.tones.forEach(function (b) {
      b.addEventListener("click", function () {
        flush();
        var r = rooms[sel];
        r.tone = b.getAttribute("data-tone");
        if (!r.on || r.lvl === 0) setRoom(sel, .7);
        paintRoom(sel); syncPanel(); totals(); ack(sel); clearScene();
      });
    });
    el.extra.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      flush();
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

    /* Départ : tout est éteint, puis la soirée s'allume pièce par pièce.
       Les masques et la photo des couches de lumière ne sont préparés qu'à l'approche de la démo,
       et les animations continues (eau, foyer, écran) ne tournent que lorsqu'elle est à l'écran. */
    order.forEach(function (k) { paintRoom(k); });
    select("salon");
    totals();
    var started = false, fed = false;
    function feed() {
      if (fed) return;
      fed = true;
      order.forEach(function (k) { rooms[k].l.style.setProperty("--m", mask(rooms[k].def, rooms[k].box)); });
      root.style.setProperty("--mz-img", 'url("' + $(".mz-base").getAttribute("src") + '")');
    }
    function start() {
      if (started) return;
      started = true;
      feed();
      setTimeout(function () { scene("soiree"); }, reduce ? 0 : 900);
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          root.classList.toggle("is-live", e.isIntersecting);
          if (e.isIntersecting) feed();
          if (e.intersectionRatio >= .35) start();
        });
      }, { threshold: [0, .35] }).observe(root);
    } else { root.classList.add("is-live"); start(); }
  });
})();
