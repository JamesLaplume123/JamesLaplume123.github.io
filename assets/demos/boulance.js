/* « BouLance en direct » : lit /live toutes les 5 s et /history toutes les 5 min auprès du
   service du site (html[data-api]). Liquide animé, flux d'énergie, courbe 24 h. Données réelles. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var API = document.documentElement.getAttribute("data-api");

  function fmt(n, d) { return n.toFixed(d).replace(".", ","); }
  function ago(s) {
    if (s < 5) return "à l’instant";
    if (s < 90) return "il y a " + Math.round(s) + " s";
    if (s < 5400) return "il y a " + Math.round(s / 60) + " min";
    return "il y a " + Math.round(s / 3600) + " h";
  }
  function color(soc) { return soc >= 60 ? "#34d399" : soc >= 30 ? "#fbbf24" : "#f87171"; }
  function deep(soc) { return soc >= 60 ? "#0f766e" : soc >= 30 ? "#b45309" : "#991b1b"; }
  /* Change le texte et fait briller la valeur si elle a vraiment changé */
  function put(el, text) {
    if (!el || el.textContent === text) return;
    var first = el.textContent === "—" || el.textContent === "--" || el.textContent === "";
    el.textContent = text;
    if (first || reduce) return;
    el.classList.remove("is-tick"); void el.offsetWidth; el.classList.add("is-tick");
  }

  document.querySelectorAll('[data-demo="boulance"]').forEach(function (root) {
    var $ = function (s, r) { return (r || root).querySelector(s); };
    var bats = [].slice.call(root.querySelectorAll(".bl-bat"));
    var level = [0, 0], target = [0, 0], amps = [0, 0], phase = 0, visible = false, last = null, timer = null;
    var beat = $(".bl-beat");

    var lastT = 0;
    function waves(now) {
      /* Le remplissage dépend du temps écoulé, pas de la vitesse de l'écran : ~1,5 s partout */
      now = now || performance.now();
      var dt = lastT ? Math.min(300, now - lastT) : 16;
      lastT = now;
      phase += .035 * dt / 16;
      var k = 1 - Math.exp(-dt / 320);
      bats.forEach(function (b, i) {
        level[i] += (target[i] - level[i]) * k;
        if (Math.abs(target[i] - level[i]) < .4) level[i] = target[i];
        var y = 400 - (level[i] / 100) * 384, amp = level[i] > 1 && level[i] < 99 ? 7 : 3;
        ["w1", "w2"].forEach(function (w, k) {
          var d = "M0 " + y.toFixed(1);
          for (var x = 0; x <= 200; x += 10) {
            d += " L" + x + " " + (y + Math.sin(x / 26 + phase * (k ? 1.4 : 1) + k * 2) * amp).toFixed(1);
          }
          d += " L200 400 L0 400 Z";
          $(".bl-wave." + w, b).setAttribute("d", d);
        });
        if (last) $('[data-bl="soc"]', b).textContent = Math.round(Math.abs(target[i] - level[i]) < 1.5 ? target[i] : level[i]);
      });
      if (visible && !reduce) requestAnimationFrame(waves); else lastT = 0;
    }

    function setState(ok, text) {
      var s = $('[data-bl="state"]');
      s.classList.toggle("is-off", !ok);
      s.innerHTML = '<i class="dot' + (ok ? "" : " is-off") + '" aria-hidden="true"></i>' + text;
    }

    function paint(d) {
      last = d;
      root.classList.remove("is-waiting");
      d.batteries.forEach(function (b, i) {
        var el = bats[i];
        if (!el) return;
        var soc = b.soc >= 0 ? b.soc : 0;
        target[i] = soc;
        el.style.setProperty("--bl-c", color(soc));
        el.style.setProperty("--bl-c2", deep(soc));
        el.style.setProperty("--soc", soc);
        amps[i] = b.a || 0;
        el.classList.toggle("is-charging", b.a > .4 || !!b.charging);
        el.classList.toggle("is-using", b.a < -.4);
        if (reduce || b.soc < 0) $('[data-bl="soc"]', el).textContent = b.soc >= 0 ? Math.round(b.soc) : "--";
        put($('[data-bl="v"]', el), b.v > 0 ? fmt(b.v, 2) + " V" : "—");
        put($('[data-bl="a"]', el), fmt(b.a, 1) + " A");
        put($('[data-bl="t"]', el), b.t > -90 ? fmt(b.t, 1) + " °C" : "—");
        put($('[data-bl="wh"]', el), b.wh >= 0 ? fmt(b.wh / 1000, 2) + " kWh" : "—");
        put($('[data-bl="cells"]', el), b.hi > 0 ? "Δ " + Math.round((b.hi - b.lo) * 1000) + " mV" : "—");
        $('[data-bl="cells"]', el).title = b.hi > 0 ? "Cellule la plus basse " + fmt(b.lo, 3) + " V, la plus haute " + fmt(b.hi, 3) + " V" : "";
        $('[data-bl="cycles"]', el).textContent = b.cycles >= 0 ? b.cycles : "—";
        $('[data-bl="chg"]', el).classList.toggle("on", !!b.chg);
        $('[data-bl="dsg"]', el).classList.toggle("on", !!b.dsg);
        $('[data-bl="bal"]', el).classList.toggle("on", !!b.balancing);
        var flag = $('[data-bl="flag"]', el);
        if (!b.online) { flag.className = "bl-flag warn"; flag.textContent = "Hors ligne"; }
        else if (!b.chg && soc >= 98) { flag.className = "bl-flag ok"; flag.textContent = "Pleine · charge coupée"; }
        else if (b.problem) { flag.className = "bl-flag warn"; flag.textContent = "Alerte BMS"; }
        else if (b.charging) { flag.className = "bl-flag ok"; flag.textContent = "En charge"; }
        else { flag.className = "bl-flag ok"; flag.textContent = "Normale"; }
      });
      var t = d.total;
      put($('[data-bl="kwh"]'), t.kwh >= 0 ? fmt(t.kwh, 2) : "—");
      put($('[data-bl="ah"]'), t.ah >= 0 ? Math.round(t.ah) + " Ah" : "— Ah");
      put($('[data-bl="w"]'), Math.round(t.w) + " W");
      var flow = t.a > .4 ? "in" : t.a < -.4 ? "out" : "idle";
      root.setAttribute("data-flow", flow);
      $('[data-bl="mode"]').textContent = flow === "in" ? "En charge : " + fmt(t.a, 1) + " A entrent dans les batteries"
        : flow === "out" ? "En utilisation : " + fmt(-t.a, 1) + " A sortent des batteries"
        : "Au repos : aucun courant important";
      var seen = Math.max.apply(null, d.batteries.map(function (b) { return b.seen || 0; }));
      var age = Math.max(0, (d.now || Date.now() / 1000) - seen);
      $('[data-bl="age"]').textContent = "Dernière mesure des batteries " + ago(age);
      setState(true, "En direct");
      if (beat && !reduce) { beat.classList.remove("run"); void beat.offsetWidth; beat.classList.add("run"); }
    }

    /* Bulles dans le liquide : plus le courant est fort, plus elles montent vite et nombreuses */
    function bubble(i) {
      var b = bats[i], box = b && $(".bl-bubbles", b);
      if (!box || !visible || reduce || document.hidden || !last) return;
      var h = box.clientHeight, top = h * (level[i] / 100) - 14;
      if (top < 20) return;
      var a = Math.min(40, Math.abs(amps[i])), size = 3 + Math.random() * (a > .4 ? 6 : 4);
      var el = document.createElement("i");
      el.style.width = el.style.height = size.toFixed(1) + "px";
      el.style.left = (12 + Math.random() * 76).toFixed(1) + "%";
      el.style.setProperty("--top", top.toFixed(0) + "px");
      el.style.setProperty("--sx", ((Math.random() - .5) * 18).toFixed(1) + "px");
      el.style.setProperty("--d", (a > .4 ? 2.4 + Math.random() * 1.4 : 5 + Math.random() * 3).toFixed(2) + "s");
      box.appendChild(el);
      el.addEventListener("animationend", function () { el.remove(); });
    }
    function bubbles() {
      bats.forEach(function (b, i) {
        var a = Math.abs(amps[i]);
        var gap = a > .4 ? Math.max(120, 700 - a * 30) : 1300;
        if (!b._bt || Date.now() - b._bt > gap) { b._bt = Date.now() + Math.random() * 300; bubble(i); }
      });
      if (visible) setTimeout(bubbles, 120); else bubbling = false;
    }
    var bubbling = false;

    function chart(points) {
      if (!points || points.length < 2) return;
      var xs = points.map(function (p) { return p[0]; }), ys = points.map(function (p) { return p[1]; });
      var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
      var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys);
      var pad = Math.max(.05, (hi - lo) * .15);
      lo -= pad; hi += pad;
      var P = points.map(function (p) {
        return [((p[0] - x0) / Math.max(1, x1 - x0) * 300).toFixed(1), (90 - (p[1] - lo) / (hi - lo) * 84 - 3).toFixed(1)];
      });
      var line = "M" + P.map(function (p) { return p.join(" "); }).join(" L");
      $(".bl-line").setAttribute("d", line);
      $(".bl-area").setAttribute("d", line + " L300 90 L0 90 Z");
      var end = P[P.length - 1], now = $(".bl-now");
      if (now) { now.style.left = (end[0] / 300 * 100) + "%"; now.style.top = (end[1] / 90 * 100) + "%"; }
      plotPts = points.map(function (p, k) { return { t: p[0], v: p[1], x: +P[k][0], y: +P[k][1] }; });
      requestAnimationFrame(function () { $(".bl-chart").classList.add("is-drawn"); });
      $('[data-bl="range"]').textContent = fmt(Math.min.apply(null, ys), 2) + " à " + fmt(Math.max.apply(null, ys), 2) + " kWh";
    }

    var plotPts = [], plot = $(".bl-plot");
    if (plot) {
      var tip = $(".bl-tip", plot), cross = $(".bl-cross", plot);
      var hourFmt = new Intl.DateTimeFormat("fr-CA", { hour: "numeric", minute: "2-digit", timeZone: "America/Toronto" });
      plot.addEventListener("pointermove", function (e) {
        if (!plotPts.length) return;
        var r = plot.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * 300, best = plotPts[0];
        plotPts.forEach(function (p) { if (Math.abs(p.x - x) < Math.abs(best.x - x)) best = p; });
        cross.setAttribute("x1", best.x); cross.setAttribute("x2", best.x);
        tip.style.left = (best.x / 300 * 100) + "%";
        tip.textContent = hourFmt.format(new Date(best.t * 1000)) + " · " + fmt(best.v, 2) + " kWh";
        plot.classList.add("is-hover");
      });
      plot.addEventListener("pointerleave", function () { plot.classList.remove("is-hover"); });
    }

    function load() {
      if (!API) {
        root.classList.add("is-waiting");
        setState(false, "Liaison en installation");
        $('[data-bl="age"]').textContent = "Les batteries de l’ambulance apparaîtront ici dès que la liaison sera branchée";
        return;
      }
      fetch(API + "/live", { cache: "no-store" })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (d) { if (!d.ok) throw new Error("ko"); paint(d); })
        .catch(function () {
          setState(false, last ? "Liaison interrompue · dernières valeurs" : "Liaison indisponible");
          if (!last) root.classList.add("is-waiting");
        });
    }
    function loadHistory() {
      if (!API) return;
      fetch(API + "/history").then(function (r) { return r.json(); }).then(function (d) { if (d.ok) chart(d.points); }).catch(function () {});
    }
    function loop() {
      clearInterval(timer);
      timer = setInterval(function () { if (visible && !document.hidden) load(); }, 5000);
    }

    var started = false;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        visible = e.isIntersecting;
        if (visible) {
          if (!started) { started = true; load(); loadHistory(); setInterval(loadHistory, 300000); }
          loop();
          requestAnimationFrame(waves);
          if (!bubbling) { bubbling = true; bubbles(); }
        }
      });
    }, { threshold: .15 }).observe(root);
    if (reduce) waves();
  });
})();
