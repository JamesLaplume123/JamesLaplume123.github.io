/* Page Vision : horizons (onglets).
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
})();
