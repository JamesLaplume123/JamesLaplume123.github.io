/* Démo « Hub + extensions » (page JARVIS). Données d'exemple.
   Trois blocs [data-demo="hub"] : cœur (le boîtier et ses fils de lumière; un Hub par lieu), IA (une conversation qui
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
     1. Le Hub, cœur de JARVIS : la lumière part du boîtier vers les choses
        de la vie; puis un Hub par lieu, relié à une seule application.
     ====================================================================== */
  (function () {
    var root = $('[data-hb="coeur"]');
    if (!root) return;
    var D = data(root); if (!D) return;
    var scene = $(".hb-scene", root);

    /* Internet optionnel : rien ne change sur place. */
    var btn = $(".hb-net-btn", root), off = $(".hb-offline", root);
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var cut = btn.getAttribute("aria-pressed") !== "true";
      btn.setAttribute("aria-pressed", cut ? "true" : "false");
      $("span", btn).textContent = cut ? "Rétablir Internet" : "Couper Internet";
      off.hidden = !cut;
    });

    /* Les fils de lumière et les phrases qui changent doucement */
    var vies = $$(".hb-vie", scene).map(function (li) {
      var k = li.getAttribute("data-vie");
      return { k: k, li: li, b: $(".hb-vie-tx b", li), fil: $('[data-fil="' + k + '"]', scene), ph: D.vie[k] || [], n: 0 };
    });
    function swap(v) {
      if (v.ph.length < 2) return;
      v.n = (v.n + 1) % v.ph.length;
      v.b.classList.add("is-out");
      setTimeout(function () { v.b.textContent = v.ph[v.n]; v.b.classList.remove("is-out"); }, 360);
    }
    if (fx) {
      var clock = Clock(scene), i = 0;
      (function beat() {
        var v = vies[i % vies.length]; i++;
        if (v.fil) restart(v.fil, "is-go");
        clock.later(function () {
          v.li.classList.add("is-lit"); if (v.fil) v.fil.classList.add("is-lit");
          swap(v);
        }, 1500);
        clock.later(function () {
          v.li.classList.remove("is-lit"); if (v.fil) v.fil.classList.remove("is-lit", "is-go");
        }, 4600);
        clock.later(beat, 2300);
      })();
    }

    /* Un Hub par lieu : fils entre chaque petit Hub et sa ligne dans l'application */
    var box = $(".hb-lieux", root);
    if (!box || !window.SVGElement) return;
    var body = $(".hb-lx-body", box), svg = $(".hb-lx-fils", box), tel = $(".hb-lx-tel", box);
    var tiles = $$(".hb-lx-t", box), rows = {};
    $$("[data-rang]", box).forEach(function (r) { rows[r.getAttribute("data-rang")] = r; });
    var wide = window.matchMedia ? matchMedia("(min-width: 901px)") : { matches: true };
    var wires = {};
    function draw() {
      svg.textContent = ""; wires = {};
      if (!wide.matches) return;
      var o = body.getBoundingClientRect(), t = tel.getBoundingClientRect();
      tiles.forEach(function (tile) {
        var k = tile.getAttribute("data-lieu"), led = $(".hb-lx-hub i", tile), row = rows[k];
        if (!led || !row) return;
        var a = led.getBoundingClientRect(), r = row.getBoundingClientRect();
        var left = tile.classList.contains("is-g");
        var x0 = a.left + a.width / 2 - o.left, y0 = a.top + a.height / 2 - o.top;
        var x1 = (left ? t.left + 3 : t.right - 3) - o.left, y1 = r.top + r.height / 2 - o.top;
        var dx = x1 - x0;
        var d = "M" + x0.toFixed(1) + " " + y0.toFixed(1) + "C" + (x0 + dx * .55).toFixed(1) + " " + y0.toFixed(1) + " " +
          (x1 - dx * .45).toFixed(1) + " " + y1.toFixed(1) + " " + x1.toFixed(1) + " " + y1.toFixed(1);
        var g = document.createElementNS(NS, "g");
        g.setAttribute("class", "hb-fil");
        ["hb-fil-base", "hb-fil-halo", "hb-fil-lum"].forEach(function (c) {
          var p = document.createElementNS(NS, "path");
          p.setAttribute("class", c); p.setAttribute("d", d);
          if (c !== "hb-fil-base") p.setAttribute("pathLength", "1000");
          g.appendChild(p);
        });
        svg.appendChild(g); wires[k] = g;
      });
    }
    draw();
    if ("ResizeObserver" in window) new ResizeObserver(draw).observe(body);
    else addEventListener("resize", draw);
    if (wide.addEventListener) wide.addEventListener("change", draw);
    $$("img", box).forEach(function (im) { if (!im.complete) im.addEventListener("load", draw); });

    if (!fx) return;
    var lc = Clock(box), j = 0;
    (function beat() {
      var tile = tiles[j % tiles.length]; j++;
      var k = tile.getAttribute("data-lieu"), w = wires[k], row = rows[k];
      tile.classList.add("is-lit");
      if (w) restart(w, "is-go");
      lc.later(function () { if (row) row.classList.add("is-lit"); if (w) w.classList.add("is-lit"); }, w ? 1500 : 500);
      lc.later(function () {
        tile.classList.remove("is-lit"); if (row) row.classList.remove("is-lit");
        if (w) w.classList.remove("is-lit", "is-go");
      }, 4200);
      lc.later(beat, 2100);
    })();
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
