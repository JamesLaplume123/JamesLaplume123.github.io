/* Démo « JARVIS App » (dossier User v25) : huit écrans, quatre entrées de menu, pilotés par la barre latérale
   (ou les onglets du bas). Un écran appartient à une entrée du menu (data-nav) : Ma journée, Mes partages et
   Mes appels sont dans Mon espace, l'Assistant part de l'Accueil. Un sélecteur Personnel | Professionnel
   (data-pp) bascule le contenu des deux espaces, d'un seul état pour tout l'appareil.
   Vraies données : l'heure locale et la météo de Saint-Hyacinthe (Environnement Canada).
   Tout le reste est fictif : aucun rappel, partage ou appareil réel n'est touché. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia && matchMedia("(hover: hover) and (pointer: fine)").matches;
  var NB = " ";
  var EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/qc-22?f=json&lang=fr";
  var JOURS = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];
  var MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  var MOIS_C = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function hm(d) { return d.getHours() + NB + "h" + NB + pad(d.getMinutes()); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function num(n) { return n < 0 ? "−" + Math.abs(n) : String(n); }
  function store() { try { return window.sessionStorage; } catch (e) { return null; } }

  /* Lecture du JSON d'Environnement Canada (même logique que la console en direct) */
  function val(o) {
    if (o == null) return undefined;
    var v = o.value !== undefined ? o.value : o;
    if (v && typeof v === "object") v = v.fr !== undefined ? v.fr : v.en;
    return v;
  }
  function txt(o) {
    if (o == null) return "";
    if (typeof o === "string") return o;
    if (o.fr !== undefined) return o.fr;
    if (o.value !== undefined) return txt(o.value);
    return o.en || "";
  }
  function nval(o) { var n = parseFloat(val(o)); return isFinite(n) ? n : null; }

  /* Une seule requête météo pour toute la page, même si plusieurs appareils sont affichés. */
  var wxShared = null;
  function wxFetch(fresh) {
    if (wxShared && !fresh) return wxShared;
    var ss = store(), cached = null;
    try { var c = ss && JSON.parse(ss.getItem("jarvis-ec") || "null"); if (c && Date.now() - c.t < 300000) cached = c.j; } catch (e) {}
    wxShared = cached ? Promise.resolve(cached) : fetch(EC_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) { try { ss && ss.setItem("jarvis-ec", JSON.stringify({ t: Date.now(), j: j })); } catch (e) {} return j; });
    wxShared.catch(function () { wxShared = null; });
    return wxShared;
  }

  /* Rail de la séquence : la pastille suit le chapitre à l'écran. */
  (function () {
    var rail = document.querySelector(".apx-rail");
    if (!rail || !("IntersectionObserver" in window)) return;
    var links = [].slice.call(rail.querySelectorAll("a"));
    var chapters = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    function mark(el) {
      links.forEach(function (a, i) {
        var on = chapters[i] === el;
        a.classList.toggle("is-on", on);
        if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
    }
    var seen = [];
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var i = chapters.indexOf(e.target);
        if (i < 0) return;
        seen[i] = e.isIntersecting ? e.intersectionRatio : 0;
      });
      var best = -1, score = 0;
      seen.forEach(function (v, i) { if (v > score) { score = v; best = i; } });
      mark(best >= 0 ? chapters[best] : null);
    }, { threshold: [0, .15, .4, .7], rootMargin: "-25% 0px -45% 0px" });
    chapters.forEach(function (c) { if (c) io.observe(c); });
    mark(chapters[0]);
  })();

  document.querySelectorAll('[data-demo="app"]').forEach(function (root) {
    var $ = function (s, r) { return (r || root).querySelector(s); };
    var $$ = function (s, r) { return [].slice.call((r || root).querySelectorAll(s)); };
    var fx = document.documentElement.classList.contains("fx");
    var stage = $(".ap-stage"), tilt = $(".ap-tilt"), banner = $(".ap-banner");
    var tabs = $$('.ap-nav [role="tab"]'), views = $$(".ap-view"), caps = $$(".ap-cap");
    var keys = views.map(function (v) { return v.getAttribute("data-view"); });
    var navs = tabs.map(function (t) { return t.getAttribute("data-nav"); });
    function tabOf(i) { return Math.max(0, navs.indexOf(views[i].getAttribute("data-nav"))); }
    var ind = $(".ap-ind"), prog = $(".ap-prog");
    var stepEl = $('[data-ap="step"]'), playBtn = $('[data-ap="play"]');
    var n = views.length, cur = 0;
    var BANNER = ["scale(1.02)", "scale(1.1) translate(-3%, 2%)", "scale(1.06) translate(3%, 1%)", "scale(1.12) translate(-2%, 3%)",
      "scale(1.08) translate(2%, 1%)", "scale(1.14) translate(-1%, 2%)", "scale(1.05) translate(1%, -1%)"];

    /* ---------------------------------------------------------------- Compteurs */
    function countUp(el, to) {
      var end = to !== undefined ? to : parseFloat(el.getAttribute("data-ap-n"));
      if (!isFinite(end)) return;
      var from = el._v !== undefined ? el._v : 0;
      el._v = end;
      if (!fx || from === end) { el.textContent = num(end); return; }
      var t0 = performance.now(), d = 900;
      (function step(t) {
        var k = Math.min(1, (t - t0) / d), e = 1 - Math.pow(1 - k, 3);
        el.textContent = num(Math.round(from + (end - from) * e));
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    }

    /* ---------------------------------------------------------------- Heure, salutation, date */
    var nowLine = $('[data-ap="nowline"]');
    function tickClock() {
      var d = new Date(), h = d.getHours();
      $$('[data-ap="clock"]').forEach(function (el) { el.textContent = hm(d); });
      $$('[data-ap="greet"]').forEach(function (el) { el.textContent = h < 5 || h >= 18 ? "Bonsoir" : h < 12 ? "Bonjour" : "Bon après-midi"; });
      $$('[data-ap="date"]').forEach(function (el) { el.textContent = cap(JOURS[d.getDay()]) + " " + d.getDate() + " " + MOIS[d.getMonth()]; });
      $$('[data-ap="now"]').forEach(function (el) { el.textContent = hm(d); });
      if (nowLine) {
        var f = (h + d.getMinutes() / 60 - 8) / 14;
        nowLine.hidden = !(f >= 0 && f <= 1);
        nowLine.style.top = (f * 100).toFixed(2) + "%";
      }
      // Ma journée : vrais jours à partir d'aujourd'hui
      var first = null, last = null;
      for (var i = 0; i < 3; i++) {
        var di = new Date(d.getFullYear(), d.getMonth(), d.getDate() + i);
        if (!i) first = di; last = di;
        var b = $('[data-ap="dname' + i + '"]'), s = $('[data-ap="dnum' + i + '"]');
        if (b) b.textContent = i ? cap(JOURS[di.getDay()]) : "Aujourd’hui";
        if (s) s.textContent = (i ? "" : cap(JOURS[di.getDay()]).slice(0, 3) + ". ") + di.getDate() + " " + MOIS_C[di.getMonth()];
      }
      var r = $('[data-ap="range"]');
      if (r && first) {
        r.textContent = first.getMonth() === last.getMonth()
          ? first.getDate() + NB + "–" + NB + last.getDate() + " " + MOIS[first.getMonth()] + " " + first.getFullYear()
          : first.getDate() + " " + MOIS_C[first.getMonth()] + NB + "–" + NB + last.getDate() + " " + MOIS_C[last.getMonth()] + " " + last.getFullYear();
      }
    }
    tickClock();
    setTimeout(function () { tickClock(); setInterval(tickClock, 60000); }, (60 - new Date().getSeconds()) * 1000 + 50);

    /* ---------------------------------------------------------------- Météo réelle */
    var wxStarted = false;
    function wxFail() {
      root.setAttribute("data-wx-state", "off");
      $$('[data-ap="temp"]').forEach(function (el) { el.textContent = "—"; });
    }
    function wxPaint(j) {
      var p = j.properties || {}, cc = p.currentConditions || {};
      var t = nval(cc.temperature), cond = txt(cc.condition), code = nval(cc.iconCode);
      if (t === null) { wxFail(); return; }
      var night = code !== null && code >= 30 && code <= 39;
      var c = (cond || "").toLowerCase(), kind = "cloud";
      if (/neige|flocon|poudrerie|gr[eé]sil/.test(c)) kind = "snow";
      else if (/pluie|averse|bruine|orage/.test(c)) kind = "rain";
      else if (/brouillard|brume/.test(c)) kind = "fog";
      else if (/d[eé]gag|ensoleill|soleil/.test(c)) kind = night ? "moon" : "sun";
      root.setAttribute("data-wx", kind);
      root.setAttribute("data-wx-state", "on");
      $$('[data-ap="temp"]').forEach(function (el) { countUp(el, Math.round(t)); });
      var chip = $(".ap-wx");
      if (chip) chip.title = "Saint-Hyacinthe : " + (cond ? cond.toLowerCase() + ", " : "") + num(Math.round(t)) + NB + "°C · Environnement Canada, en direct";
      var rs = p.riseSet || {}, set = rs.sunset ? new Date(txt(rs.sunset)) : null, reco = $('[data-ap="reco"]');
      if (reco && set && !isNaN(set)) {
        var pre = new Date(set.getTime() - 15 * 60000);
        reco.textContent = "Coucher du soleil à " + hm(set) + " (réel) : JARVIS propose " + hm(pre) + ", si vous l’acceptez.";
      }
    }
    function wxLoad(fresh) { wxFetch(fresh).then(wxPaint).catch(wxFail); }
    function wxStart() {
      if (wxStarted) return;
      wxStarted = true;
      wxLoad();
      setInterval(function () { if (!document.hidden && visible) wxLoad(true); }, 600000);
    }

    /* ---------------------------------------------------------------- Écrans et visite automatique */
    var timer = null, left = 0, startedAt = 0, visible = false, hover = false, focusIn = false;
    var single = root.hasAttribute("data-single");
    var stopped = reduce || !fx || single;
    var hooks = {};
    function dur(i) { return +views[i].getAttribute("data-dur") || 7000; }
    function running() { return visible && !hover && !focusIn && !stopped; }
    function syncPlay() {
      root.classList.toggle("is-auto", !stopped);
      root.classList.toggle("is-stopped", stopped);
      root.classList.toggle("is-paused", !running());
      if (playBtn) {
        playBtn.lastChild.textContent = stopped ? "Lecture" : "Pause";
        playBtn.setAttribute("aria-label", stopped ? "Reprendre la visite automatique" : "Mettre la visite en pause");
      }
    }
    function arm() {
      clearTimeout(timer); timer = null;
      syncPlay();
      if (!running()) return;
      startedAt = Date.now();
      timer = setTimeout(function () { go((cur + 1) % n); }, left);
    }
    function hold() {
      if (timer) { clearTimeout(timer); timer = null; left = Math.max(400, left - (Date.now() - startedAt)); }
      syncPlay();
    }
    function stop() { if (stopped) return; stopped = true; hold(); }
    function restartProg() {
      if (!prog) return;
      var np = prog.cloneNode(true);
      prog.parentNode.replaceChild(np, prog);
      prog = np;
    }
    function moveInd() {
      var b = tabs[tabOf(cur)];
      if (ind && b) ind.style.transform = "translate(" + b.offsetLeft + "px," + b.offsetTop + "px)";
    }
    function enter(v, i) {
      v.inert = false;
      v.removeAttribute("inert");
      v.classList.remove("is-out");
      v.classList.add("is-on");
      var show = function () {
        v.classList.add("is-shown");
        $$("[data-ap-n]", v).forEach(function (el) { el._v = 0; countUp(el); });
      };
      if (fx) requestAnimationFrame(function () { requestAnimationFrame(show); }); else show();
      if (hooks[keys[i]] && hooks[keys[i]].enter) hooks[keys[i]].enter();
    }
    function leave(v, i) {
      v.classList.remove("is-shown");
      v.inert = true;
      v.setAttribute("inert", "");
      if (!fx) { v.classList.remove("is-on"); if (hooks[keys[i]] && hooks[keys[i]].leave) hooks[keys[i]].leave(); return; }
      v.classList.add("is-out");
      clearTimeout(v._t);
      v._t = setTimeout(function () {
        if (views[cur] === v) return;
        v.classList.remove("is-on", "is-out");
        if (hooks[keys[i]] && hooks[keys[i]].leave) hooks[keys[i]].leave();
      }, 320);
    }
    function go(i, user) {
      if (user) stop();
      if (i === cur) return;
      var prev = cur;
      cur = i;
      leave(views[prev], prev);
      var ti = tabOf(i);
      var wn = $('[data-ap="winname"]');
      if (wn && views[i]) wn.textContent = views[i].getAttribute("data-title") || views[i].getAttribute("aria-label") || "";
      tabs.forEach(function (t, k) {
        var on = k === ti;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        t.classList.toggle("is-on", on);
      });
      moveInd();
      caps.forEach(function (c, k) { c.classList.toggle("is-on", k === i); });
      if (stepEl) stepEl.textContent = pad(i + 1);
      if (banner) banner.style.transform = BANNER[i] || "";
      enter(views[i], i);
      left = dur(i);
      root.style.setProperty("--dur", left + "ms");
      restartProg();
      arm();
    }

    function viewOf(t) { return Math.max(0, keys.indexOf(navs[t])); }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { go(viewOf(k), true); });
    });
    var nav = $(".ap-nav"), nt = tabs.length;
    if (nav && nt) nav.addEventListener("keydown", function (e) {
      var k = e.key, j = null, c = tabOf(cur);
      if (k === "ArrowDown" || k === "ArrowRight") j = (c + 1) % nt;
      else if (k === "ArrowUp" || k === "ArrowLeft") j = (c + nt - 1) % nt;
      else if (k === "Home") j = 0;
      else if (k === "End") j = nt - 1;
      if (j === null) return;
      e.preventDefault();
      go(viewOf(j), true);
      tabs[j].focus();
    });
    /* Petit message dans l'app (Administration, éléments présentés ailleurs) */
    var flash = $(".ap-flash"), flashT = null;
    root.addEventListener("click", function (e) {
      var t = e.target.closest("[data-toast]");
      if (!t || !root.contains(t) || !flash) return;
      flash.textContent = t.getAttribute("data-toast");
      flash.classList.add("is-on");
      clearTimeout(flashT);
      flashT = setTimeout(function () { flash.classList.remove("is-on"); }, 3600);
    });
    root.addEventListener("click", function (e) {
      var g = e.target.closest("[data-go]");
      if (!g || !root.contains(g)) return;
      var key = g.getAttribute("data-go"), j = keys.indexOf(key);
      if (j >= 0) { go(j, true); return; }
      var chap = document.getElementById("ecran-" + key);
      if (chap) chap.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    });
    // Toute interaction dans l'app arrête la visite automatique (le bouton Lecture la relance).
    $(".ap-screen").addEventListener("pointerdown", stop);
    $(".ap-screen").addEventListener("keydown", function (e) { if (e.key !== "Tab" && e.key !== "Shift") stop(); });
    if (playBtn) playBtn.addEventListener("click", function () {
      if (stopped) {
        stopped = false;
        if (reduce) stopped = true;
        left = dur(cur);
        restartProg();
        arm();
      } else stop();
    });
    stage.addEventListener("pointerenter", function () { hover = true; hold(); });
    stage.addEventListener("pointerleave", function () { hover = false; arm(); });
    root.addEventListener("focusin", function () { focusIn = true; hold(); });
    root.addEventListener("focusout", function (e) { if (!root.contains(e.relatedTarget)) { focusIn = false; arm(); } });

    /* ---------------------------------------------------------------- Accueil */
    $$("[data-seg]").forEach(function (b) {
      b.addEventListener("click", function () {
        var card = b.closest(".ap-card");
        $$("[data-seg]", card).forEach(function (x) { var on = x === b; x.classList.toggle("is-on", on); x.setAttribute("aria-pressed", on ? "true" : "false"); });
        $$("[data-seg-panel]", card).forEach(function (p) { p.hidden = p.getAttribute("data-seg-panel") !== b.getAttribute("data-seg"); });
      });
    });

    /* ---------------------------------------------------------------- Mes outils : l'extension s'ouvre sur place */
    (function () {
      var v = $(".ap-v-outils");
      if (!v) return;
      var grid = $(".ap-exts", v), pile = $(".ap-extp", v), head = $(".ap-head", v);
      var panels = $$(".ap-extd", v);
      var wn = $('[data-ap="winname"]'), winBase = wn ? wn.textContent : "";
      function show(slug) {
        panels.forEach(function (d) { d.hidden = d.getAttribute("data-extd") !== slug; });
        var t = $('[data-extd="' + slug + '"] .ap-extd-t b', v);
        if (wn && t) {
          winBase = wn.textContent.split(" / ")[0];
          wn.textContent = (window.matchMedia("(max-width: 680px)").matches ? "" : winBase + " / ") + t.textContent;
        }
        v.classList.add("is-ext");
        if (head) head.hidden = true;
        grid.hidden = true;
        pile.hidden = false;
        var back = $(".ap-back", pile.querySelector('[data-extd="' + slug + '"]'));
        if (back) back.focus({ preventScroll: true });
      }
      function back() {
        if (wn && winBase) wn.textContent = winBase;
        v.classList.remove("is-ext");
        panels.forEach(function (d) { d.hidden = true; });
        pile.hidden = true;
        grid.hidden = false;
        if (head) head.hidden = false;
      }
      v.addEventListener("click", function (e) {
        var card = e.target.closest("[data-ext]");
        if (card && v.contains(card)) {
          /* Le visiteur reste dans le logiciel : l'extension s'ouvre ici, la page ne bouge pas. */
          e.preventDefault();
          stop();
          show(card.getAttribute("data-ext"));
          return;
        }
        if (e.target.closest("[data-ext-close]")) { e.preventDefault(); stop(); back(); }
      });
      v.addEventListener("keydown", function (e) { if (e.key === "Escape" && v.classList.contains("is-ext")) back(); });
      hooks.outils = { leave: back };
      pile.hidden = true;
    })();

    /* ---------------------------------------------------------------- Mon espace : notifications */
    (function () {
      var v = $(".ap-v-espace");
      if (!v) return;
      var list = $(".ap-nl", v), count = $('[data-ap="unread"]', v), mark = $('[data-ap="markread"]', v);
      var unread = $$(".is-unread", list), LABEL = mark.lastChild.textContent;
      $$("[data-nf]", v).forEach(function (b) {
        b.addEventListener("click", function () {
          $$("[data-nf]", v).forEach(function (x) { var on = x === b; x.classList.toggle("is-on", on); x.setAttribute("aria-pressed", on ? "true" : "false"); });
          list.classList.toggle("only-unread", b.getAttribute("data-nf") === "unread");
        });
      });
      mark.addEventListener("click", function () {
        unread.forEach(function (li) { li.classList.remove("is-unread"); });
        countUp(count, 0);
        mark.disabled = true;
        mark.classList.add("is-done");
        mark.lastChild.textContent = "Tout est lu";
      });
      hooks.espace = {
        leave: function () {
          unread.forEach(function (li) { li.classList.add("is-unread"); });
          count._v = 2; count.textContent = "2";
          mark.disabled = false; mark.classList.remove("is-done"); mark.lastChild.textContent = LABEL;
          list.classList.remove("only-unread");
          $$("[data-nf]", v).forEach(function (x, k) { x.classList.toggle("is-on", !k); x.setAttribute("aria-pressed", k ? "false" : "true"); });
        }
      };
    })();

    /* ---------------------------------------------------------------- Personnel | Professionnel */
    var pps = $$("[data-pp]");
    pps.forEach(function (b) {
      b.addEventListener("click", function () {
        var mode = b.getAttribute("data-pp");
        root.classList.toggle("is-pro", mode === "pro");
        pps.forEach(function (x) {
          var on = x.getAttribute("data-pp") === mode;
          x.classList.toggle("is-on", on);
          x.setAttribute("aria-pressed", on ? "true" : "false");
        });
      });
    });

    /* ---------------------------------------------------------------- Mes appels */
    (function () {
      var v = $(".ap-v-appels");
      if (!v) return;
      var openT = null;
      function close(row) {
        row.classList.remove("is-open");
        var b = $("[data-call]", row);
        if (b) b.setAttribute("aria-expanded", "false");
      }
      function open(row) {
        $$(".ap-call.is-open", v).forEach(close);
        row.classList.add("is-open");
        var b = $("[data-call]", row);
        if (b) b.setAttribute("aria-expanded", "true");
      }
      $$("[data-call]", v).forEach(function (b) {
        b.addEventListener("click", function () {
          var row = b.closest(".ap-call");
          if (row.classList.contains("is-open")) close(row); else open(row);
        });
      });
      hooks.appels = {
        // La visite montre l'appel répondu par JARVIS : la ligne clé s'ouvre d'elle-même.
        enter: function () {
          clearTimeout(openT);
          var sel = root.classList.contains("is-pro") ? '[data-pp-only="pro"]' : '[data-pp-only="perso"]';
          var row = $(".ap-call.is-jv" + sel, v);
          if (!row) return;
          if (!fx) { open(row); return; }
          openT = setTimeout(function () { open(row); }, 1600);
        },
        leave: function () {
          clearTimeout(openT);
          $$(".ap-call.is-open", v).forEach(close);
        }
      };
    })();

    /* ---------------------------------------------------------------- Assistant */
    (function () {
      var v = $(".ap-v-assistant");
      if (!v) return;
      var thread = $('[data-ap="thread"]', v), steps = $$("[data-step]", thread);
      var action = $('[data-ap="action"]', v), state = $('[data-ap="state"]', v), fine = $('[data-ap="fine"]', v);
      var verify = $('[data-ap="verify"]', v), approve = $('[data-ap="approve"]', v), fields = $$(".ap-fields li", v);
      var timers = [], FINE = fine.textContent, STATE = state.lastChild.textContent;
      function later(f, ms) { timers.push(setTimeout(f, ms)); }
      function typeInto(span, done) {
        var full = span._full || (span._full = span.textContent), words = full.split(" "), k = 0;
        span.innerHTML = '<span class="ap-tw-t"></span><span class="ap-tw-u"></span>';
        var t = span.firstChild, u = span.lastChild;
        u.textContent = full;
        (function next() {
          k++;
          t.textContent = words.slice(0, k).join(" ");
          u.textContent = k < words.length ? " " + words.slice(k).join(" ") : "";
          if (k < words.length) later(next, 42 + Math.random() * 46); else if (done) done();
        })();
      }
      function show(i) { steps[i].classList.add("is-in"); }
      function jv(i, next) {
        show(i);
        var bub = $(".ap-bub", steps[i]), span = $("[data-type]", steps[i]);
        bub.classList.add("is-typing");
        span.style.visibility = "hidden";
        later(function () {
          bub.classList.remove("is-typing");
          span.style.visibility = "";
          typeInto(span, function () { steps[i].classList.add("is-done"); later(next, 520); });
        }, 1000);
      }
      function resetAction() {
        action.classList.remove("is-ready");
        state.className = "ap-state"; state.lastChild.textContent = STATE;
        fine.textContent = FINE; fine.parentNode.classList.remove("is-ok");
        verify.disabled = approve.disabled = false;
        verify.textContent = "Vérifier"; approve.textContent = "Approuver"; approve.classList.remove("is-done");
        fields.forEach(function (f) { f.classList.remove("is-ok"); });
      }
      function reset() {
        timers.forEach(clearTimeout); timers = [];
        steps.forEach(function (s) {
          s.classList.remove("is-in", "is-done");
          var span = $("[data-type]", s);
          if (span && span._full) span.textContent = span._full;
          if (span) span.style.visibility = "";
          var bub = $(".ap-bub", s); if (bub) bub.classList.remove("is-typing");
        });
        resetAction();
      }
      function play() {
        reset();
        if (!fx) { steps.forEach(function (s) { s.classList.add("is-in", "is-done"); }); action.classList.add("is-ready"); return; }
        thread.classList.add("is-scripted");
        var seq = [
          function (next) { later(function () { show(0); later(next, 700); }, 380); },
          function (next) { jv(1, next); },
          function (next) { show(2); later(next, 700); },
          function (next) { jv(3, next); },
          function () { show(4); steps[4].classList.add("is-done"); action.classList.add("is-ready"); }
        ];
        var k = 0;
        (function run() { var f = seq[k++]; if (f) f(run); })();
      }
      if (fx) thread.classList.add("is-scripted");
      hooks.assistant = { enter: play, leave: reset };
      verify.addEventListener("click", function () {
        verify.disabled = true;
        fields.forEach(function (f, i) { later(function () { f.classList.add("is-ok"); }, fx ? i * 200 : 0); });
        later(function () { verify.textContent = "Vérifié"; fine.textContent = "Détails vérifiés. Rien n’est créé sans votre accord."; }, fx ? 850 : 0);
      });
      approve.addEventListener("click", function () {
        action.classList.remove("is-ready");
        verify.disabled = approve.disabled = true;
        state.className = "ap-state is-sent"; state.lastChild.textContent = "Envoyé";
        fine.textContent = "Envoi au Hub…";
        later(function () {
          state.className = "ap-state is-ok"; state.lastChild.textContent = "Confirmé";
          approve.textContent = "Approuvé";
          approve.classList.add("is-done");
          fine.textContent = "Prêt pour demain, 14" + NB + "h" + NB + "00 · démo, rien n’est créé.";
          fine.parentNode.classList.add("is-ok");
        }, fx ? 1100 : 0);
      });
    })();

    /* ---------------------------------------------------------------- Ma journée */
    $$("[data-cal]").forEach(function (b) {
      b.addEventListener("click", function () {
        var on = b.getAttribute("aria-pressed") !== "true", k = b.getAttribute("data-cal");
        b.setAttribute("aria-pressed", on ? "true" : "false");
        $$('.ap-ev[data-src="' + k + '"]').forEach(function (e) { e.classList.toggle("is-hidden", !on); });
      });
    });
    var doneEl = $('[data-ap="done"]');
    $$(".ap-tasks button.ap-box").forEach(function (b) {
      b.addEventListener("click", function () {
        var li = b.closest("li"), on = !li.classList.contains("is-done");
        li.classList.toggle("is-done", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
        if (doneEl) countUp(doneEl, $$(".ap-tasks li.is-done").length);
      });
    });
    if (doneEl) doneEl._v = 1;

    /* ---------------------------------------------------------------- Cartes */
    var maps = $$("[data-map]");
    function fitMap(m) {
      var f = m.getAttribute("data-focus").split(",").map(Number), z = m._z || 1;
      var W = m.clientWidth, H = m.clientHeight;
      if (!W || !H) return;
      var a = W / H, w = f[2] / z, h = f[3] / z;
      var cx = (f[0] + f[2] / 2) * (1 / z), cy = (f[1] + f[3] / 2) * (1 / z); // glisse vers le Hub (0, 0)
      var vx, vy, vw, vh;
      if (w / h < a) { vh = h; vw = h * a; } else { vw = w; vh = w / a; }
      vx = cx - vw / 2; vy = cy - vh / 2;
      $(".ap-map-svg", m).setAttribute("viewBox", vx.toFixed(2) + " " + vy.toFixed(2) + " " + vw.toFixed(2) + " " + vh.toFixed(2));
      $$("[data-x]", m).forEach(function (o) {
        var px = (+o.getAttribute("data-x") - vx) / vw * 100, py = (+o.getAttribute("data-y") - vy) / vh * 100;
        o.style.left = px.toFixed(2) + "%";
        o.style.top = py.toFixed(2) + "%";
        o.style.visibility = px < -4 || px > 104 || py < -4 || py > 104 ? "hidden" : "";
        if (o.classList.contains("ap-city")) {
          var half = o.offsetWidth / 2 / W * 100;
          o.classList.toggle("is-e", px + half > 97);
          o.classList.toggle("is-w", px - half < 3);
          o.classList.toggle("is-s", py + 30 / H * 100 > 97);
        }
      });
    }
    function fitAll() { maps.forEach(fitMap); }
    var big = $(".ap-map-big");
    function zoomTo(z) {
      if (!big) return;
      var from = big._z || 1, t0 = performance.now();
      if (!fx) { big._z = z; fitMap(big); return; }
      (function step(t) {
        var k = Math.min(1, (t - t0) / 520), e = 1 - Math.pow(1 - k, 3);
        big._z = from + (z - from) * e;
        fitMap(big);
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    }
    var LEVELS = [1, 1.7, 2.8];
    $$("[data-zoom]").forEach(function (b) {
      b.addEventListener("click", function () {
        var d = +b.getAttribute("data-zoom"), z = big._z || 1, i = 0;
        LEVELS.forEach(function (l, k) { if (Math.abs(l - z) < Math.abs(LEVELS[i] - z)) i = k; });
        if (d === 0) zoomTo(2.2);
        else zoomTo(LEVELS[Math.max(0, Math.min(LEVELS.length - 1, i + d))]);
      });
    });
    var toast = $('[data-ap="toast"]'), toastT = null;
    function say(msg) {
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add("is-on");
      clearTimeout(toastT);
      toastT = setTimeout(function () { toast.classList.remove("is-on"); }, 3200);
    }
    $$("[data-layer-t]").forEach(function (b) {
      b.addEventListener("click", function () {
        var on = b.getAttribute("aria-pressed") !== "true", k = b.getAttribute("data-layer-t");
        b.setAttribute("aria-pressed", on ? "true" : "false");
        if (k === "appareils" || k === "personnes") {
          if (on) say(k === "appareils" ? "Aucun appareil n’a autorisé sa position." : "Personne n’a partagé sa position avec vous.");
          return;
        }
        $$('[data-layer="' + k + '"]', big).forEach(function (el) { el.classList.toggle("is-off", !on); });
      });
    });
    var askPos = $('[data-ap="askpos"]'), posNote = $('[data-ap="posnote"]');
    if (askPos && posNote) askPos.addEventListener("click", function () { posNote.hidden = false; });
    hooks.carte = { enter: function () { fitAll(); }, leave: function () { if (big) { big._z = 1; fitMap(big); } } };
    hooks.accueil = { enter: fitAll };

    /* ---------------------------------------------------------------- Partage */
    (function () {
      var v = $(".ap-v-partage");
      if (!v) return;
      var active = $('[data-ap="active"]', v), log = $('[data-ap="log"]', v), firstNew = $(".ap-log-new", v);
      var timers = [];
      function later(f, ms) { timers.push(setTimeout(f, ms)); }
      $$(".ap-acc", v).forEach(function (row) {
        var revoke = $('[data-ap="revoke"]', row), confirm = $(".ap-confirm", row), prop = $(".ap-prop", row);
        var name = $(".ap-acc-who b", row).textContent;
        revoke.addEventListener("click", function () {
          row.classList.add("is-asking");
          revoke.hidden = true; confirm.hidden = false;
          $('[data-ap="keep"]', row).focus();
        });
        $('[data-ap="keep"]', row).addEventListener("click", function () {
          row.classList.remove("is-asking");
          confirm.hidden = true; revoke.hidden = false; revoke.focus();
        });
        $('[data-ap="sure"]', row).addEventListener("click", function () {
          row.classList.remove("is-asking");
          confirm.hidden = true;
          row.classList.add("is-going");
          var items = $$("li", prop), gap = fx ? 380 : 0;
          items.forEach(function (li, i) { later(function () { li.classList.add("is-ok"); }, 200 + i * gap); });
          later(function () {
            row.classList.remove("is-going");
            row.classList.add("is-gone");
            prop.setAttribute("data-gone", name + " · " + $(".ap-acc-what b", row).textContent + " · " + hm(new Date()));
            countUp(active, Math.max(0, (active._v || 5) - 1));
            var li = firstNew.hidden ? firstNew : firstNew.cloneNode(true);
            li.hidden = false;
            li.classList.add("ap-log-new");
            $("time", li).textContent = "À l’instant";
            $("span", li).textContent = "Accès de " + name + " retiré partout";
            if (li !== firstNew) log.insertBefore(li, log.firstChild);
          }, 300 + items.length * gap + 250);
        });
      });
      hooks.partage = {
        leave: function () {
          timers.forEach(clearTimeout); timers = [];
          $$(".ap-acc", v).forEach(function (row) {
            row.classList.remove("is-asking", "is-going", "is-gone");
            $('[data-ap="revoke"]', row).hidden = false;
            $(".ap-confirm", row).hidden = true;
            $$(".ap-prop li", row).forEach(function (li) { li.classList.remove("is-ok"); });
          });
          $$(".ap-log-new", v).forEach(function (li) { if (li === firstNew) li.hidden = true; else li.remove(); });
          active._v = 5;
        }
      };
    })();

    /* ---------------------------------------------------------------- Inclinaison 3D (bureau seulement) */
    if (finePointer && !reduce && tilt) {
      var raf = 0, px = 0, py = 0;
      stage.addEventListener("pointermove", function (e) {
        if (stage.clientWidth < 900) return;
        var r = tilt.getBoundingClientRect();
        px = (e.clientX - r.left) / r.width - .5; py = (e.clientY - r.top) / r.height - .5;
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          tilt.style.transform = "perspective(2400px) rotateX(" + (-py * 4).toFixed(2) + "deg) rotateY(" + (px * 4).toFixed(2) + "deg)";
        });
      });
      stage.addEventListener("pointerleave", function () { cancelAnimationFrame(raf); raf = 0; tilt.style.transform = ""; });
    }

    /* ---------------------------------------------------------------- L'appareil tient dans l'écran */
    // Sur ordinateur, l'appareil entier doit être visible d'un coup : réduction douce, jamais sous 72 %.
    var device = $(".ap-device"), zoomT = 0;
    function fitZoom() {
      tilt.style.removeProperty("--ap-zoom");
      if (innerWidth < 700) return;
      var rail = document.querySelector(".apx-rail"), railH = 0;
      if (rail && root.closest(".apx") && getComputedStyle(rail).position === "sticky") railH = rail.offsetHeight + 18;
      var avail = innerHeight - 66 - railH - 30, h = device.offsetHeight + 16;
      var z = Math.max(.72, Math.min(1, avail / h));
      if (z < .995) tilt.style.setProperty("--ap-zoom", z.toFixed(3));
    }
    addEventListener("resize", function () { clearTimeout(zoomT); zoomT = setTimeout(fitZoom, 120); });
    addEventListener("load", fitZoom);
    fitZoom();

    /* ---------------------------------------------------------------- Mise en page vivante */
    if ("ResizeObserver" in window) new ResizeObserver(function () { moveInd(); fitAll(); }).observe(stage);
    else addEventListener("resize", function () { moveInd(); fitAll(); });
    moveInd();
    fitAll();
    if (banner) banner.style.transform = BANNER[0];
    left = dur(0);
    root.style.setProperty("--dur", left + "ms");
    syncPlay();

    /* ---------------------------------------------------------------- Entrée en scène */
    var shown = false;
    function firstShow() {
      if (shown) return;
      shown = true;
      root.classList.add("in");
      wxStart();
      setTimeout(function () { enter(views[0], 0); restartProg(); arm(); }, fx ? 380 : 0);
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          visible = e.isIntersecting;
          if (visible) { firstShow(); if (shown) arm(); } else hold();
        });
      }, { threshold: .3 }).observe(stage);
    } else { visible = true; firstShow(); }
  });
})();
