/* Page Vision : horizons (onglets), une journée avec JARVIS (client + moments).
   Sans JavaScript, le premier état de chaque bloc reste affiché, complet. */
(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var press = function (list, on) {
    list.forEach(function (b) {
      var is = b === on;
      b.classList.toggle("is-on", is);
      if (b.hasAttribute("aria-selected")) b.setAttribute("aria-selected", is ? "true" : "false");
      if (b.hasAttribute("aria-pressed")) b.setAttribute("aria-pressed", is ? "true" : "false");
    });
  };

  /* ---------- Horizons ---------- */
  $$('[data-vn="horizons"]').forEach(function (root) {
    var tabs = $$(".vn-hz-tab", root), panels = $$(".vn-hz-panel", root), line = root.querySelector(".vn-hz-line");
    var show = function (i, focus) {
      press(tabs, tabs[i]);
      panels.forEach(function (p, k) {
        p.hidden = k !== i;
        p.classList.toggle("is-on", k === i);
        $$(".vn-hz-j li", p).forEach(function (li, n) { li.style.setProperty("--n", n); });
      });
      if (line) line.style.setProperty("--p", tabs.length > 1 ? i / (tabs.length - 1) : 0);
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(i); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        show((i + d + tabs.length) % tabs.length, true);
      });
      if (i) t.tabIndex = -1;
    });
    tabs.forEach(function (t) { t.addEventListener("focus", function () { tabs.forEach(function (o) { o.tabIndex = o === t ? 0 : -1; }); }); });
    show(0);
  });

  /* ---------- Une journée avec JARVIS ---------- */
  $$('[data-vn="journee"]').forEach(function (root) {
    var segs = $$(".vn-seg-b", root), days = $$(".vn-day", root), cur = 0;
    var moments = function () { return $$(".vn-tl-b", days[cur]); };
    var showMo = function (i) {
      var bs = moments(), mos = $$(".vn-mo", days[cur]);
      i = (i + bs.length) % bs.length;
      press(bs, bs[i]);
      mos.forEach(function (m, k) { m.hidden = k !== i; m.classList.toggle("is-on", k === i); });
      var line = days[cur].querySelector(".vn-tl-line");
      if (line) line.style.setProperty("--p", (i + 1) / bs.length);
      var row = bs[i].parentNode;
      if (row.scrollWidth > row.clientWidth) row.scrollTo({ left: bs[i].offsetLeft - row.clientWidth / 2 + bs[i].offsetWidth / 2, behavior: "smooth" });
    };
    var current = function () {
      var bs = moments();
      for (var k = 0; k < bs.length; k++) if (bs[k].classList.contains("is-on")) return k;
      return 0;
    };
    segs.forEach(function (s, d) {
      s.addEventListener("click", function () {
        cur = d;
        press(segs, s);
        days.forEach(function (el, k) { el.hidden = k !== d; el.classList.toggle("is-on", k === d); });
        showMo(0);
      });
    });
    days.forEach(function (day) {
      $$(".vn-tl-b", day).forEach(function (b, i) { b.addEventListener("click", function () { showMo(i); }); });
    });
    $$("[data-step]", root).forEach(function (b) {
      b.addEventListener("click", function () { showMo(current() + parseInt(b.getAttribute("data-step"), 10)); });
    });
    showMo(0);
  });
})();
