/* « Écrit en Rust » : compteurs, puis deux demandes de l'IA devant la porte du noyau. */
(function () {
  "use strict";
  var root = document.querySelector('[data-demo="rust"]');
  if (!root) return;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Compteurs : montent jusqu'à leur valeur quand ils apparaissent */
  var counters = [].slice.call(root.querySelectorAll("[data-rs-count]"));
  function count(el) {
    var end = parseFloat(el.getAttribute("data-rs-count")), t0 = null;
    if (reduce) { el.textContent = end; return; }
    el.textContent = "0";
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(end * e);
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* Porte du noyau : une demande permise, une demande refusée */
  var lanes = [].slice.call(root.querySelectorAll(".rs-lane"));
  var timers = [];
  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
  function centerX(lane, el) {
    var a = lane.getBoundingClientRect(), b = el.getBoundingClientRect();
    return b.left - a.left + b.width / 2;
  }
  function leftX(lane, el) { return el.getBoundingClientRect().left - lane.getBoundingClientRect().left; }
  function run(lane, start) {
    var ok = lane.getAttribute("data-lane") === "ok";
    var dot = lane.querySelector(".rs-dot"), core = lane.querySelector(".rs-core");
    var from = lane.querySelector(".rs-from"), to = lane.querySelector(".rs-to");
    later(function () {
      lane.classList.remove("is-pass", "is-block", "is-done");
      var x0 = centerX(lane, from), x2 = centerX(lane, to), stop = leftX(lane, core) - 10, after = leftX(lane, core) + core.offsetWidth + 10;
      if (reduce || !dot.animate) { lane.classList.add(ok ? "is-pass" : "is-block", "is-done"); return; }
      var a = dot.animate([
        { transform: "translateX(" + (x0 - 35) + "px)", opacity: 0 },
        { transform: "translateX(" + (x0 - 35) + "px)", opacity: 1, offset: .08 },
        { transform: "translateX(" + (stop - 35) + "px)", opacity: 1 }
      ], { duration: 1300, easing: "cubic-bezier(.4,0,.2,1)", fill: "forwards" });
      a.onfinish = function () {
        lane.classList.add(ok ? "is-pass" : "is-block");
        if (!ok) {
          dot.animate([{ transform: "translateX(" + (stop - 35) + "px)", opacity: 1 },
                       { transform: "translateX(" + (stop - 60) + "px) scale(.4)", opacity: 0 }],
                      { duration: 520, easing: "ease-out", fill: "forwards" });
          later(function () { lane.classList.add("is-done"); }, 380);
          return;
        }
        var b = dot.animate([{ transform: "translateX(" + (after - 35) + "px)", opacity: 1 },
                             { transform: "translateX(" + (x2 - 35) + "px)", opacity: 1 },
                             { transform: "translateX(" + (x2 - 35) + "px)", opacity: 0 }],
                            { duration: 1300, easing: "cubic-bezier(.4,0,.2,1)", fill: "forwards" });
        b.onfinish = function () { lane.classList.add("is-done"); };
      };
    }, start);
  }
  function cycle() {
    timers.forEach(clearTimeout); timers = [];
    run(lanes[0], 200);
    if (lanes[1]) run(lanes[1], 1700);
  }

  var seen = false, loop = null;
  new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.target === root.querySelector(".rs-stats") && e.isIntersecting && !seen) {
        seen = true;
        counters.forEach(count);
      }
    });
  }, { threshold: .35 }).observe(root.querySelector(".rs-stats"));
  var gateIo = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      clearInterval(loop);
      if (e.isIntersecting) { cycle(); if (!reduce) loop = setInterval(cycle, 7000); }
    });
  }, { threshold: .35 });
  gateIo.observe(root.querySelector(".rs-gate"));
})();
