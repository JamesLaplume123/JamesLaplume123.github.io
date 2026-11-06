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

  document.querySelectorAll('[data-demo="boulance"]').forEach(function (root) {
    var $ = function (s, r) { return (r || root).querySelector(s); };
    var bats = [].slice.call(root.querySelectorAll(".bl-bat"));
    var level = [0, 0], target = [0, 0], phase = 0, visible = false, last = null, timer = null;

    function waves() {
      phase += .035;
      bats.forEach(function (b, i) {
        level[i] += (target[i] - level[i]) * .06;
        var y = 400 - (level[i] / 100) * 384, amp = level[i] > 1 && level[i] < 99 ? 7 : 3;
        ["w1", "w2"].forEach(function (w, k) {
          var d = "M0 " + y.toFixed(1);
          for (var x = 0; x <= 200; x += 10) {
            d += " L" + x + " " + (y + Math.sin(x / 26 + phase * (k ? 1.4 : 1) + k * 2) * amp).toFixed(1);
          }
          d += " L200 400 L0 400 Z";
          $(".bl-wave." + w, b).setAttribute("d", d);
        });
      });
      if (visible && !reduce) requestAnimationFrame(waves);
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
        el.style.setProperty("--soc", soc);
        $('[data-bl="soc"]', el).textContent = b.soc >= 0 ? Math.round(b.soc) : "--";
        $('[data-bl="v"]', el).textContent = b.v > 0 ? fmt(b.v, 2) + " V" : "—";
        $('[data-bl="a"]', el).textContent = fmt(b.a, 1) + " A";
        $('[data-bl="t"]', el).textContent = b.t > -90 ? fmt(b.t, 1) + " °C" : "—";
        $('[data-bl="wh"]', el).textContent = b.wh >= 0 ? fmt(b.wh / 1000, 2) + " kWh" : "—";
        $('[data-bl="cells"]', el).textContent = b.hi > 0 ? "Δ " + Math.round((b.hi - b.lo) * 1000) + " mV" : "—";
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
      $('[data-bl="kwh"]').textContent = t.kwh >= 0 ? fmt(t.kwh, 2) : "—";
      $('[data-bl="ah"]').textContent = t.ah >= 0 ? Math.round(t.ah) + " Ah" : "— Ah";
      $('[data-bl="w"]').textContent = Math.round(t.w) + " W";
      var flow = t.a > .4 ? "in" : t.a < -.4 ? "out" : "idle";
      root.setAttribute("data-flow", flow);
      $('[data-bl="mode"]').textContent = flow === "in" ? "En charge : " + fmt(t.a, 1) + " A entrent dans les batteries"
        : flow === "out" ? "En utilisation : " + fmt(-t.a, 1) + " A sortent des batteries"
        : "Au repos : aucun courant important";
      var seen = Math.max.apply(null, d.batteries.map(function (b) { return b.seen || 0; }));
      var age = Math.max(0, (d.now || Date.now() / 1000) - seen);
      $('[data-bl="age"]').textContent = "Dernière mesure des batteries " + ago(age);
      setState(true, "En direct");
    }

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
      $('[data-bl="range"]').textContent = fmt(Math.min.apply(null, ys), 2) + " à " + fmt(Math.max.apply(null, ys), 2) + " kWh";
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
        }
      });
    }, { threshold: .15 }).observe(root);
    if (reduce) waves();
  });
})();
