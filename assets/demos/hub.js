/* Démo « Hub + extensions » (page JARVIS). Données d'exemple.
   Trois blocs [data-demo="hub"] : cœur (événements sur le bus), IA (une conversation qui
   comprend, vérifie, propose, demande, explique), ensemble (trois chaînes de bout en bout);
   (l'offre vit sur /offre/). Le mouvement vit seulement sous html.fx et s'arrête hors écran.
   Sans JavaScript, le HTML montre déjà un état complet (voir src/demos/hub.py). */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var fx = !reduce && doc.classList.contains("fx");
  var NS = "http://www.w3.org/2000/svg";
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function data(root) { try { return JSON.parse($(".hb-data", root).textContent); } catch (e) { return null; } }
  function restart(el, cls) { el.classList.remove(cls); void el.getBoundingClientRect(); el.classList.add(cls); }
  function watch(el, cb) {
    if (!("IntersectionObserver" in window)) { cb(true); return; }
    new IntersectionObserver(function (es) { cb(es[0].isIntersecting); }, { threshold: 0.18 }).observe(el);
  }
  /* Minuterie qui attend que le bloc soit visible, et qu'on peut annuler. */
  function Clock(root) {
    var self = { vis: false, token: 0 };
    watch(root, function (v) { self.vis = v; root.classList.toggle("is-run", v); });
    self.later = function (fn, ms) {
      var t = self.token;
      setTimeout(function wait() {
        if (t !== self.token) return;
        if (!self.vis || document.hidden) { setTimeout(wait, 400); return; }
        fn();
      }, ms);
    };
    self.cancel = function () { self.token++; };
    return self;
  }

  /* ======================================================================
     1. Le Hub, cœur de JARVIS
     ====================================================================== */
  (function () {
    var root = $('[data-hb="coeur"]');
    if (!root || !window.SVGElement) return;
    var D = data(root); if (!D) return;
    var svg = $(".hb-svg", root), layer = $(".hb-pk", svg), ticker = $(".hb-tk-txt", root);
    var nodes = {}, spokes = {}, segs = {}, hosts = {};
    $$(".hb-node", svg).forEach(function (n) { nodes[n.getAttribute("data-node")] = n; });
    $$(".hb-spoke", svg).forEach(function (p) {
      var a = p.getAttribute("data-a").split(",").map(Number), b = p.getAttribute("data-b").split(",").map(Number);
      spokes[p.getAttribute("data-spoke")] = { el: p, a: a, b: b, c: getComputedStyle(p).getPropertyValue("--x").trim() };
    });
    $$(".hb-seg", svg).forEach(function (g) { segs[g.getAttribute("data-seg")] = g; });
    $$(".hb-hosted li", root).forEach(function (li) { hosts[li.getAttribute("data-host")] = li; });
    var pulse = $(".hb-core-pulse", svg);

    function hotHost(k, on) { if (segs[k]) segs[k].classList.toggle("is-hot", on); if (hosts[k]) hosts[k].classList.toggle("is-hot", on); }
    Object.keys(hosts).forEach(function (k) {
      hosts[k].addEventListener("mouseenter", function () { hotHost(k, true); });
      hosts[k].addEventListener("mouseleave", function () { hotHost(k, false); });
      if (segs[k]) {
        segs[k].addEventListener("mouseenter", function () { hotHost(k, true); });
        segs[k].addEventListener("mouseleave", function () { hotHost(k, false); });
      }
    });

    /* Internet optionnel */
    var btn = $(".hb-net-btn", root), net = $("[data-net]", svg), off = $(".hb-offline", root);
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var cut = btn.getAttribute("aria-pressed") !== "true";
      btn.setAttribute("aria-pressed", cut ? "true" : "false");
      $("span", btn).textContent = cut ? "Rétablir Internet" : "Couper Internet";
      net.classList.toggle("is-off", cut);
      off.hidden = !cut;
    });

    if (!fx) return;
    var clock = Clock(root);

    function travel(from, to, color, ms, done) {
      var c = document.createElementNS(NS, "circle");
      c.setAttribute("r", "4.6"); c.setAttribute("fill", color);
      layer.appendChild(c);
      var t0 = performance.now();
      (function step(now) {
        var k = Math.min(1, (now - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        c.setAttribute("cx", from[0] + (to[0] - from[0]) * e);
        c.setAttribute("cy", from[1] + (to[1] - from[1]) * e);
        if (k < 1) requestAnimationFrame(step); else { c.remove(); if (done) done(); }
      })(t0);
    }
    function nm(k) { return "<b>" + D.names[k] + "</b>"; }
    var i = 0;
    function play() {
      var ev = D.events[i % D.events.length]; i++;
      var s = spokes[ev.src];
      nodes[ev.src].classList.add("is-hot"); s.el.classList.add("is-hot");
      ticker.innerHTML = nm(ev.src) + " publie « " + ev.txt + " »…";
      restart(ticker, "is-in");
      travel(s.b, s.a, s.c, 950, function () {
        hotHost("bus", true); restart(pulse, "is-ping");
        setTimeout(function () { hotHost("comptes", true); if (ev.ia) hotHost("iacore", true); }, 260);
        setTimeout(function () { hotHost("journal", true); }, 520);
        setTimeout(function () {
          ev.to.forEach(function (k) {
            var t = spokes[k]; t.el.classList.add("is-hot");
            travel(t.a, t.b, t.c, 950, function () { nodes[k].classList.add("is-hot"); });
          });
          ticker.innerHTML = nm(ev.src) + " publie « " + ev.txt + " » · droits vérifiés" +
            (ev.ia ? " · l’IA en tient compte" : "") + " · consigné au journal · reçu par " + ev.to.map(nm).join(" et ");
        }, 700);
      });
      clock.later(function () {
        $$(".is-hot", root).forEach(function (el) { el.classList.remove("is-hot"); });
      }, 3500);
      clock.later(play, 4300);
    }
    clock.later(play, 900);
  })();

  /* ======================================================================
     2. L'IA au cœur
     ====================================================================== */
  (function () {
    var root = $('[data-hb="ia"]');
    if (!root) return;
    var D = data(root); if (!D) return;
    var body = $(".hb-con-body", root), tabsBox = $(".hb-con-tabs", root), tabs = $$("[data-scene]", root);
    var traits = {}; $$("[data-trait]", root).forEach(function (li) { traits[li.getAttribute("data-trait")] = li; });
    var zero = $(".hb-con-zero", root);
    var order = tabs.map(function (b) { return b.getAttribute("data-scene"); });
    var clock = Clock(root), cur = 0;
    root.classList.add("is-live"); tabsBox.hidden = false;

    function trait(k) {
      var seen = true;
      Object.keys(traits).forEach(function (t) {
        var li = traits[t];
        li.classList.toggle("is-on", t === k);
        li.classList.toggle("is-done", seen && t !== k);
        if (t === k) seen = false;
      });
    }
    function down() { body.scrollTop = body.scrollHeight; }
    function show(el) { el.classList.add("is-in"); down(); }
    /* « JARVIS réfléchit » : trois points, puis la réponse. */
    function think(el, cb) {
      var d = document.createElement("div");
      d.className = "hb-think is-in"; d.setAttribute("aria-hidden", "true");
      d.innerHTML = "<i></i><i></i><i></i>";
      body.appendChild(d); down();
      clock.later(function () { d.remove(); show(el); if (cb) cb(); }, 750);
    }

    function load(n, auto) {
      clock.cancel(); cur = n;
      tabs.forEach(function (b, j) { b.setAttribute("aria-selected", j === n ? "true" : "false"); });
      body.innerHTML = D.scenes[order[n]];
      zero.classList.remove("is-hot");
      var parts = [].slice.call(body.children);
      if (!fx) {
        parts.forEach(function (p) { p.classList.add("is-in"); });
        $$(".hb-checks li", body).forEach(function (li) { li.classList.add("is-in"); });
        Object.keys(traits).forEach(function (t) { traits[t].classList.remove("is-on"); traits[t].classList.add("is-done"); });
        return;
      }
      Object.keys(traits).forEach(function (t) { traits[t].classList.remove("is-on", "is-done"); });
      var me = parts[0], ask = $(".hb-ask", me), text = ask.textContent, k = 0;
      var later = clock.later;
      ask.textContent = ""; ask.classList.add("is-typing");
      later(function () {
        show(me); trait("comprend");
        (function type() {
          k++; ask.textContent = text.slice(0, k);
          if (k < text.length) later(type, 24 + Math.random() * 30);
          else {
            ask.classList.remove("is-typing");
            later(function () { think(parts[1]); }, 250);
            later(function () {
              think(parts[2], function () {
                trait("raisonne");
                $$(".hb-checks li", parts[2]).forEach(function (li, j) {
                  later(function () { li.classList.add("is-in"); down(); }, 380 + j * 520);
                });
              });
              var after = 750 + 380 + $$(".hb-checks li", parts[2]).length * 520 + 300;
              later(function () {
                think(parts[3], function () { trait("propose"); });
                var ok = $(".hb-ok", parts[3]), why = $(".hb-why-b", parts[3]);
                later(function () { trait("confirme"); ok.classList.add("is-press"); }, 2500);
                later(function () { ok.classList.remove("is-press"); ok.classList.add("is-done"); ok.textContent = "Confirmé"; }, 3100);
                later(function () { why.classList.add("is-press"); }, 3800);
                later(function () { think(parts[4], function () { trait("explique"); }); }, 4100);
                later(function () { show(parts[5]); trait("apprend"); }, 7400);
                later(function () { trait("local"); zero.classList.add("is-hot"); }, 8800);
                later(function () { load((cur + 1) % order.length, true); }, 14500);
              }, after);
            }, 1300);
          }
        })();
      }, auto ? 300 : 150);
    }
    tabs.forEach(function (b, j) { b.addEventListener("click", function () { load(j, false); }); });
    load(0, true);
  })();

  /* ======================================================================
     3. Comment les extensions travaillent ensemble
     ====================================================================== */
  (function () {
    var root = $('[data-hb="ensemble"]');
    if (!root) return;
    var D = data(root); if (!D) return;
    var box = $(".hb-chain", root), rail = $(".hb-ch-rail", root), detail = $(".hb-ch-detail", root),
        log = $(".hb-ch-log ol", root), lieu = $(".hb-ch-lieu b", root), bus = $(".hb-ch-bus", root),
        dot = $(".hb-ch-pulse", root), ctl = $(".hb-ch-ctl", root), playB = $(".hb-ch-play", root),
        tabs = $$("[data-chain]", root);
    var order = tabs.map(function (b) { return b.getAttribute("data-chain"); });
    var clock = Clock(box), ci = 0, i = 0, playing = fx;
    box.classList.add("is-live"); ctl.hidden = false;

    function setPlay(p) {
      playing = p; playB.classList.toggle("is-paused", !p);
      playB.setAttribute("aria-label", p ? "Pause" : "Lecture");
    }
    function C() { return D[order[ci]]; }
    function bind() {
      $$("li", rail).forEach(function (li, j) {
        var b = $("button", li); b.tabIndex = 0;
        b.setAttribute("aria-label", "Étape " + (j + 1));
        b.addEventListener("click", function () { setPlay(false); show(j); });
      });
    }
    function place() {
      var li = $$("li", rail)[i]; if (!li) return;
      var r = rail.getBoundingClientRect(), b = $(".hb-r-dot", li).getBoundingClientRect(), w = bus.getBoundingClientRect();
      var x = (b.left + b.width / 2 - w.left) / w.width * 100;
      dot.style.setProperty("--p", Math.max(2, Math.min(98, x)) + "%");
      dot.style.setProperty("--pc", C().steps[i].c);
      void r;
    }
    function show(n) {
      i = n;
      var c = C();
      $$("li", rail).forEach(function (li, j) { li.classList.toggle("is-on", j === n); li.classList.toggle("is-done", j < n); });
      detail.innerHTML = c.details[n];
      restart(detail.firstElementChild, "is-in");
      place();
      var html = "";
      for (var j = n; j >= 0; j--) {
        var s = c.steps[j];
        html += '<li style="--x:' + s.c + '"><time>' + s.t + '</time><b>' + s.n + ' publie « ' + s.ev + ' »</b>' +
          '<span>✓ droit vérifié · consigné</span></li>';
      }
      log.innerHTML = html;
      clock.cancel();
      if (playing) clock.later(next, 5600);
    }
    function next() {
      if (i + 1 < C().steps.length) show(i + 1);
      else { clock.cancel(); clock.later(function () { load((ci + 1) % order.length); }, 1400); }
    }
    function load(n) {
      ci = n;
      tabs.forEach(function (b, j) { b.setAttribute("aria-selected", j === n ? "true" : "false"); });
      var c = C();
      lieu.textContent = c.lieu;
      rail.style.setProperty("--n", c.steps.length);
      rail.innerHTML = c.rail;
      bind(); show(0);
    }
    tabs.forEach(function (b, j) { b.addEventListener("click", function () { load(j); }); });
    $(".hb-ch-prev", root).addEventListener("click", function () { setPlay(false); show(Math.max(0, i - 1)); });
    $(".hb-ch-next", root).addEventListener("click", function () { setPlay(false); show(Math.min(C().steps.length - 1, i + 1)); });
    playB.addEventListener("click", function () {
      setPlay(!playing);
      if (playing) { if (i + 1 >= C().steps.length) load((ci + 1) % order.length); else { clock.cancel(); clock.later(next, 1200); } }
      else clock.cancel();
    });
    addEventListener("resize", place);
    setPlay(playing);
    load(0);
  })();
})();
