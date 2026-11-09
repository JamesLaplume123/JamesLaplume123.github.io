/* Démo « JARVIS App » (dossier User v25) : neuf écrans, quatre entrées de menu, pilotés par la barre latérale
   (ou les onglets du bas). Un écran appartient à une entrée du menu (data-nav) : Ma journée, Mes partages,
   Mes messages et Mes appels sont dans Mon espace, l'Assistant part de l'Accueil. Un sélecteur Personnel |
   Professionnel (data-pp) bascule le contenu des deux espaces, d'un seul état pour tout l'appareil.
   Barre du haut : palette de recherche (Ctrl K), température réelle, Mes appels, Carte, menu du profil (espace,
   mode d'affichage du site). Messages, appels et visio sont simulés. La Carte est vectorielle (caméra en km).
   Vraies données : l'heure locale, la météo de Saint-Hyacinthe (Environnement Canada) et les batteries
   de BouLance (service /live du site). Tout le reste est fictif : rien de réel n'est touché. */
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
      "scale(1.08) translate(2%, 1%)", "scale(1.1) translate(2%, 2%)", "scale(1.14) translate(-1%, 2%)", "scale(1.05) translate(1%, -1%)",
      "scale(1.08) translate(-2%, 1%)"];

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


    /* ---------------------------------------------------------------- Météo réelle (simple indication dans la barre) */
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

    /* ---------------------------------------------------------------- Personnel | Professionnel */
    var pps = $$("[data-pp]");
    function setPP(mode) {
      root.classList.toggle("is-pro", mode === "pro");
      pps.forEach(function (x) {
        var on = x.getAttribute("data-pp") === mode;
        x.classList.toggle("is-on", on);
        x.setAttribute("aria-pressed", on ? "true" : "false");
      });
      if (msgs) msgs.pp();
    }
    pps.forEach(function (b) { b.addEventListener("click", function () { setPP(b.getAttribute("data-pp")); }); });

    /* ---------------------------------------------------------------- Mode d'affichage du site (comme le sélecteur du site) */
    function setSiteMode(m) {
      var btn = document.querySelector('[data-mode-set="' + m + '"]');
      if (btn && !root.contains(btn)) btn.click();
      else {
        document.documentElement.setAttribute("data-mode", m);
        try { localStorage.setItem("jarvis-mode", m); } catch (e) {}
      }
      syncModes();
    }
    function syncModes() {
      var m = document.documentElement.getAttribute("data-mode") || "signature";
      $$("[data-mode-pick]").forEach(function (b) {
        var on = b.getAttribute("data-mode-pick") === m;
        b.classList.toggle("is-on", on);
        if (b.classList.contains("ap-mode")) b.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }
    if ("MutationObserver" in window) new MutationObserver(syncModes).observe(document.documentElement, { attributes: true, attributeFilter: ["data-mode"] });
    syncModes();

    /* ---------------------------------------------------------------- Fenêtres de la barre du haut (recherche, profil) */
    var scrim = $("[data-scrim]"), openPop = null, popFrom = null;
    function closePops(keepFocus) {
      if (!openPop) return;
      var p = $('[data-pop-panel="' + openPop + '"]');
      if (p) p.hidden = true;
      $$("[data-pop-open]").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      if (scrim) scrim.hidden = true;
      root.classList.remove("has-pop");
      openPop = null;
      if (!keepFocus && popFrom && popFrom.focus) popFrom.focus({ preventScroll: true });
      popFrom = null;
    }
    function showPop(name, from) {
      if (openPop === name) { closePops(); return; }
      closePops(true);
      var p = $('[data-pop-panel="' + name + '"]');
      if (!p) return;
      stop();
      openPop = name; popFrom = from || null;
      p.hidden = false;
      root.classList.add("has-pop");
      if (scrim) scrim.hidden = false;
      $$('[data-pop-open="' + name + '"]').forEach(function (b) { b.setAttribute("aria-expanded", "true"); });
      if (name === "cmd") { cmdReset(); var q = $("[data-cmd-q]"); if (q) q.focus({ preventScroll: true }); }
      else {
        p.setAttribute("tabindex", "-1");
        p.focus({ preventScroll: true });
      }
    }
    if (scrim) scrim.addEventListener("click", function () { closePops(); });
    root.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && openPop) { e.preventDefault(); closePops(); }
    });
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K") && visible) {
        var a = document.activeElement;
        if (a && /INPUT|TEXTAREA/.test(a.tagName) && !root.contains(a)) return;
        e.preventDefault();
        showPop("cmd");
      }
    });

    /* Palette de recherche : filtre sans accents, flèches, Entrée */
    var cmdQ = $("[data-cmd-q]"), cmdItems = $$(".ap-cmd-i"), cmdAct = -1, cmdNone = $(".ap-cmd-none"), cmdTerm = $("[data-cmd-term]");
    function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[’']/g, " "); }
    cmdItems.forEach(function (it) { it._k = norm(it.getAttribute("data-k") + " " + it.textContent); });
    function cmdVisible() { return cmdItems.filter(function (it) { return !it.hidden; }); }
    function cmdMark(i) {
      var vis = cmdVisible();
      cmdAct = vis.length ? (i + vis.length) % vis.length : -1;
      cmdItems.forEach(function (it) { it.classList.remove("is-act"); it.setAttribute("aria-selected", "false"); });
      if (cmdAct >= 0) {
        vis[cmdAct].classList.add("is-act");
        vis[cmdAct].setAttribute("aria-selected", "true");
        var box = vis[cmdAct].closest(".ap-cmd-r"), r = vis[cmdAct].getBoundingClientRect(), b = box.getBoundingClientRect();
        if (r.bottom > b.bottom) box.scrollTop += r.bottom - b.bottom + 8; else if (r.top < b.top) box.scrollTop -= b.top - r.top + 8;
      }
    }
    function cmdFilter() {
      var words = norm(cmdQ.value).split(/\s+/).filter(Boolean);
      cmdItems.forEach(function (it) { it.hidden = !words.every(function (w) { return it._k.indexOf(w) >= 0; }); });
      $$(".ap-cmd-grp").forEach(function (g) { g.hidden = !$$(".ap-cmd-i", g).some(function (it) { return !it.hidden; }); });
      var none = !cmdVisible().length;
      if (cmdNone) cmdNone.hidden = !none;
      if (cmdTerm) cmdTerm.textContent = cmdQ.value;
      cmdMark(0);
    }
    function cmdReset() { if (!cmdQ) return; cmdQ.value = ""; cmdFilter(); var r = $(".ap-cmd-r"); if (r) r.scrollTop = 0; }
    if (cmdQ) {
      cmdQ.addEventListener("input", cmdFilter);
      cmdQ.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") { e.preventDefault(); cmdMark(cmdAct + 1); }
        else if (e.key === "ArrowUp") { e.preventDefault(); cmdMark(cmdAct - 1); }
        else if (e.key === "Enter") { e.preventDefault(); var v = cmdVisible()[cmdAct]; if (v) v.click(); }
      });
      cmdItems.forEach(function (it) { it.addEventListener("pointermove", function () { var k = cmdVisible().indexOf(it); if (k !== cmdAct) cmdMark(k); }); });
    }

    /* ---------------------------------------------------------------- Actions communes (tout l'appareil) */
    var flash = $(".ap-flash"), flashT = null;
    function toastMsg(msg) {
      if (!flash) return;
      flash.textContent = msg;
      flash.classList.add("is-on");
      clearTimeout(flashT);
      flashT = setTimeout(function () { flash.classList.remove("is-on"); }, 3600);
    }
    root.addEventListener("click", function (e) {
      var t = e.target.closest("[data-toast]");
      if (t && root.contains(t)) toastMsg(t.getAttribute("data-toast"));
    });
    root.addEventListener("click", function (e) {
      var el = e.target.closest("[data-pop-open],[data-pop-close],[data-go],[data-call-start],[data-mode-pick],[data-pp-set],[data-env-go]");
      if (!el || !root.contains(el)) return;
      if (el.hasAttribute("data-pop-open")) { showPop(el.getAttribute("data-pop-open"), el); return; }
      if (el.hasAttribute("data-pop-close")) { closePops(); return; }
      var inPop = !!el.closest(".ap-pop");
      if (el.hasAttribute("data-mode-pick")) { setSiteMode(el.getAttribute("data-mode-pick")); if (el.classList.contains("ap-cmd-i")) closePops(); return; }
      if (inPop && !el.closest(".ap-menu .ap-pp")) closePops(true);
      if (el.hasAttribute("data-pp-set")) setPP(el.getAttribute("data-pp-set"));
      if (el.hasAttribute("data-call-start")) { e.preventDefault(); stop(); call.start(el.getAttribute("data-call-start"), el.getAttribute("data-call-kind") || "audio"); return; }
      var key = el.getAttribute("data-go");
      if (key) {
        var j = keys.indexOf(key);
        if (j >= 0) go(j, true);
        else {
          var chap = document.getElementById("ecran-" + key);
          if (chap) chap.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
        }
      }
      var conv = el.getAttribute("data-conv"), env = el.getAttribute("data-env-go");
      if (conv && msgs) msgs.open(conv, true);
      if (env && map) {
        if (key) setTimeout(function () { map.focus(env); }, fx ? 380 : 0); else map.focus(env);
      }
    });

    /* ---------------------------------------------------------------- Mes messages */
    var people = {};
    try { people = JSON.parse(($(".ap-people") || {}).textContent || "{}"); } catch (e) {}
    function avatar(k, cls) {
      var p = people[k] || {};
      if (p.img) return '<img class="ap-mono ap-face ' + (cls || "") + '" src="' + p.img + '" alt="" decoding="async" width="96" height="96">';
      return '<span class="ap-mono t-' + (p.tone || "stone") + " " + (cls || "") + '">' + (p.ini || "?") + "</span>";
    }
    function nowHM() { return hm(new Date()); }
    var msgs = (function () {
      var v = $(".ap-v-messages");
      if (!v) return null;
      var list = $$("[data-conv-open]", v), cvs = $$("[data-cv]", v), form = $("[data-compose]", v), input = $(".ap-ms-in", v);
      var attach = $("[data-attach]", v), attachT = $("[data-attach-t]", v), docv = $("[data-docv]", v), cur = null, timers = [];
      var replied = {}, playing = null;
      function later(f, ms) { timers.push(setTimeout(f, ms)); }
      function th(k) { var c = $('[data-cv="' + k + '"]', v); return c && $("[data-thread]", c); }
      function bottom(k) { var t = th(k); if (t) t.scrollTop = t.scrollHeight; }
      function open(k, user) {
        var row = $('[data-conv-open="' + k + '"]', v);
        if (!row) return;
        var scope = row.parentNode.getAttribute("data-pp-only");
        if (scope && (scope === "pro") !== root.classList.contains("is-pro")) setPP(scope);
        cur = k;
        list.forEach(function (b) { var on = b === row; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
        cvs.forEach(function (c) { c.hidden = c.getAttribute("data-cv") !== k; });
        var n = $(".ap-cv-n", row);
        if (n && user) n.remove();
        if (input) input.placeholder = "Écrire à " + ((people[k] || {}).n || "") + "…";
        closeAttach();
        requestAnimationFrame(function () { bottom(k); });
      }
      function pp() {
        var want = root.classList.contains("is-pro") ? "pro" : "perso";
        var row = cur && $('[data-conv-open="' + cur + '"]', v);
        if (row && row.parentNode.getAttribute("data-pp-only") === want) return;
        var first = $('[data-pp-only="' + want + '"] [data-conv-open]', v);
        if (first) open(first.getAttribute("data-conv-open"));
      }
      function receipt(state) {
        var lab = { read: "Lu", dlv: "Distribué", sent: "Envoyé" }[state];
        return '<span class="ap-rcpt is-' + state + '">' + (state === "sent" ? ICON_CHECK : ICON_CHECKS) + "<span>" + lab + "</span></span>";
      }
      var ICON_CHECK = '<svg class="ap-i" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
      var ICON_CHECKS = '<svg class="ap-i" viewBox="0 0 24 24" aria-hidden="true"><path d="m2.75 12.75 4 4L15.5 8"/><path d="m11.25 16.25.5.5L20.5 8"/></svg>';
      function add(k, side, inner, author) {
        var t = th(k);
        if (!t) return null;
        var row = document.createElement("div");
        row.className = "ap-bub-row " + side + (side === "in" ? " has-av" : "") + " is-new";
        row.innerHTML = (side === "in" ? avatar(author || k) : "") + '<div class="ap-bub-c">' + inner +
          '<span class="ap-bub-meta"><time>' + nowHM() + "</time>" + (side === "out" ? receipt("sent") : "") + "</span></div>";
        var typing = $("[data-typing]", t);
        t.insertBefore(row, typing || null);
        bottom(k);
        var prev = $('[data-conv-prev="' + k + '"]', v), txt = row.querySelector(".ap-bubx");
        if (prev && txt) prev.textContent = (side === "out" ? "Vous : " : "") + (txt.classList.contains("is-doc") ? "Document" : txt.classList.contains("is-voice") ? "Message vocal" : txt.classList.contains("is-photo") ? "Photo" : txt.classList.contains("is-pos") ? "Position" : txt.textContent);
        return row;
      }
      function deliver(k, row) {
        var r = $(".ap-rcpt", row);
        later(function () { r.outerHTML = receipt("dlv"); }, 700);
        later(function () { var x = $(".ap-rcpt", row); if (x) x.outerHTML = receipt("read"); }, 1700);
        later(function () { reply(k); }, 2300);
      }
      function reply(k, quick) {
        var c = $('[data-cv="' + k + '"]', v), t = th(k);
        if (!c || !t) return;
        var typing = $("[data-typing]", t), text = replied[k] ? "Bien reçu, merci !" : c.getAttribute("data-reply");
        replied[k] = true;
        if (typing) { typing.hidden = false; t.appendChild(typing); bottom(k); }
        later(function () {
          if (typing) typing.hidden = true;
          add(k, "in", '<div class="ap-bubx">' + esc(text) + "</div>", (people[k] || {}).group ? "camille" : k);
        }, quick ? 1300 : 2100);
      }
      function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
      function closeAttach() { if (attach) { attach.hidden = true; if (attachT) attachT.setAttribute("aria-expanded", "false"); } }
      list.forEach(function (b) { b.addEventListener("click", function () { stop(); open(b.getAttribute("data-conv-open"), true); }); });
      var q = $("[data-conv-q]", v);
      if (q) q.addEventListener("input", function () {
        var w = norm(q.value);
        list.forEach(function (b) { b.parentNode.classList.toggle("is-filtered", !!w && norm(b.textContent).indexOf(w) < 0); });
      });
      if (form) form.addEventListener("submit", function (e) {
        e.preventDefault();
        var s = (input.value || "").trim();
        if (!s || !cur) return;
        input.value = "";
        var row = add(cur, "out", '<div class="ap-bubx">' + esc(s) + "</div>");
        if (row) deliver(cur, row);
      });
      if (attachT) attachT.addEventListener("click", function () {
        var open = attach.hidden;
        attach.hidden = !open;
        attachT.setAttribute("aria-expanded", open ? "true" : "false");
      });
      var DOCS_OUT = { doc: "plan" };
      $$("[data-attach-k]", v).forEach(function (b) {
        b.addEventListener("click", function () {
          var k = b.getAttribute("data-attach-k"), html;
          closeAttach();
          if (k === "doc") {
            var src = $('[data-doc="' + DOCS_OUT.doc + '"]', v);
            html = '<div class="ap-bubx is-doc">' + (src ? src.outerHTML : tplDoc()) + "</div>";
          } else if (k === "photo") {
            html = '<div class="ap-bubx is-photo"><img src="/media/ambiances/heure-doree.webp" alt="" decoding="async" style="object-position:50% 60%"></div>';
          } else {
            html = '<div class="ap-bubx is-pos"><span class="ap-pos-map"><svg viewBox="-16 -11 32 22" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><use href="#' +
              root.getAttribute("data-geo") + '"/></svg><i class="ap-pos-pin"></i></span><span class="ap-pos-t"><b>Hub · Saint-Hyacinthe</b><small>Emplacement de référence, pas votre position</small></span></div>';
          }
          var row = add(cur, "out", html);
          if (row) deliver(cur, row);
          toastMsg("Simulation : rien n’est réellement envoyé.");
        });
      });
      function tplDoc() { var any = $("[data-doc]", v); return any ? any.outerHTML : ""; }
      var rec = $("[data-voice-rec]", v);
      if (rec) rec.addEventListener("click", function () {
        var tpl = $(".ap-voice", v);
        if (!tpl || !cur) return;
        var w = tpl.cloneNode(true);
        w.setAttribute("data-voice", "6");
        w.classList.remove("is-play");
        w.style.removeProperty("--p");
        $("time", w).textContent = "0:06";
        var row = add(cur, "out", '<div class="ap-bubx is-voice">' + w.outerHTML + "</div>");
        if (row) deliver(cur, row);
        toastMsg("Simulation : aucun micro n’est utilisé.");
      });
      /* Vocaux : lecture simulée (aucun son), la forme d'onde se remplit */
      function stopVoice() {
        if (!playing) return;
        cancelAnimationFrame(playing.raf);
        playing.el.classList.remove("is-play");
        playing.el.style.setProperty("--p", "0");
        $("time", playing.el).textContent = playing.label;
        playing = null;
      }
      v.addEventListener("click", function (e) {
        var b = e.target.closest(".ap-voice-b");
        if (b) {
          var el = b.closest(".ap-voice");
          if (playing && playing.el === el) { stopVoice(); return; }
          stopVoice();
          var dur = (+el.getAttribute("data-voice") || 10) * 1000, t0 = performance.now(), label = $("time", el).textContent;
          playing = { el: el, label: label, raf: 0 };
          el.classList.add("is-play");
          (function step(t) {
            var k = Math.min(1, (t - t0) / dur), s = Math.round(k * dur / 1000);
            el.style.setProperty("--p", k.toFixed(4));
            $("time", el).textContent = "0:" + pad(s);
            if (k < 1 && playing && playing.el === el) playing.raf = requestAnimationFrame(step);
            else if (k >= 1) stopVoice();
          })(t0);
          return;
        }
        var d = e.target.closest("[data-doc]");
        if (d && docv) {
          var pg = $(".ap-pdf-page", d), name = $(".ap-doc-f b", d), meta = $(".ap-doc-f small", d);
          $("[data-docv-n]", docv).textContent = name ? name.textContent : "";
          $("[data-docv-m]", docv).textContent = meta ? meta.textContent : "";
          $("[data-docv-b]", docv).innerHTML = pg ? pg.outerHTML : "";
          docv.hidden = false;
          $("[data-docv-x]", docv).focus({ preventScroll: true });
          return;
        }
        if (e.target.closest("[data-docv-x]")) { docv.hidden = true; return; }
        if (attach && !attach.hidden && !e.target.closest("[data-attach],[data-attach-t]")) closeAttach();
      });
      v.addEventListener("keydown", function (e) { if (e.key === "Escape" && docv && !docv.hidden) { e.stopPropagation(); docv.hidden = true; } });
      hooks.messages = {
        enter: function () {
          pp();
          if (!cur) open(root.classList.contains("is-pro") ? "equipe" : "camille");
          bottom(cur);
          // La visite montre la conversation vivante : l'autre écrit, puis répond.
          if (!stopped && fx && !replied[cur]) later(function () { reply(cur, true); }, 1600);
        },
        leave: function () {
          timers.forEach(clearTimeout); timers = [];
          stopVoice();
          closeAttach();
          if (docv) docv.hidden = true;
          $$("[data-typing]", v).forEach(function (t) { t.hidden = true; });
        }
      };
      open("camille");
      return { open: function (k, user) { open(k, user); }, pp: pp };
    })();

    /* ---------------------------------------------------------------- Appel et visio (simulés) */
    var call = (function () {
      var ov = $("[data-callov]"), timer = null, t0 = 0, endT = null, kind = "audio", who = null;
      if (!ov) return { start: function () {} };
      var q = function (s) { return $('[data-co="' + s + '"]', ov); };
      function fmt(ms) { var s = Math.floor(ms / 1000); return pad(Math.floor(s / 60)) + ":" + pad(s % 60); }
      function tile(k, main) {
        var p = people[k] || {};
        var inner = p.hd ? '<img class="ap-co-full" src="' + p.hd + '" alt="" decoding="async">'
          : '<span class="ap-co-av"><i></i>' + avatar(k, "ap-co-img") + "</span>";
        return '<div class="ap-co-tile' + (main ? " is-main" : "") + (p.hd ? " has-hd" : "") + '">' + inner +
          '<span class="ap-co-name">' + (main ? '<i class="ap-co-lvl" aria-hidden="true"><i></i><i></i><i></i></i>' : "") + (p.n || "") + "</span></div>";
      }
      function setKind(k) {
        kind = k;
        ov.classList.toggle("is-video", k === "video");
        var cam = $('[data-co-t="cam"]', ov);
        if (cam) cam.setAttribute("aria-pressed", k === "video" ? "true" : "false");
        ov.classList.remove("cam-off");
        if (k === "video") {
          var p = people[who] || {}, list = p.group || [who];
          q("tiles").innerHTML = list.map(function (x, i) { return tile(x, i === 0); }).join("");
          q("tiles").setAttribute("data-n", list.length);
        }
      }
      function start(k, kd) {
        clearTimeout(endT); clearInterval(timer);
        who = k;
        var p = people[k] || {};
        q("title").textContent = (kd === "video" ? "Visio · " : "Appel · ") + (p.n || "");
        q("name").textContent = p.n || "";
        q("av").innerHTML = avatar(k, "ap-co-img");
        q("state").textContent = p.role ? p.role + " · connexion…" : "Connexion…";
        q("time").textContent = "Appel…";
        ov.classList.remove("is-end", "is-live");
        $$("[data-co-t]", ov).forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        setKind(kd);
        ov.hidden = false;
        // Sur un écran plus haut que la fenêtre (cellulaire), l'appel occupe la partie visible.
        var scr = ov.parentNode, r = scr.getBoundingClientRect(), z = r.height / scr.offsetHeight || 1;
        if (scr.offsetHeight * z > innerHeight + 4) {
          var hh = Math.min(scr.offsetHeight, innerHeight / z), top = Math.max(0, Math.min(scr.offsetHeight - hh, -r.top / z));
          ov.style.top = top + "px"; ov.style.height = hh + "px"; ov.style.bottom = "auto";
        } else { ov.style.top = ""; ov.style.height = ""; ov.style.bottom = ""; }
        root.classList.add("has-call");
        requestAnimationFrame(function () { ov.classList.add("is-on"); });
        ov.setAttribute("tabindex", "-1");
        ov.focus({ preventScroll: true });
        timer = setTimeout(function () {
          ov.classList.add("is-live");
          q("state").textContent = kd === "video" ? "Visio en cours" : "Appel en cours";
          t0 = Date.now();
          q("time").textContent = "00:00";
          timer = setInterval(function () { q("time").textContent = fmt(Date.now() - t0); }, 1000);
        }, 1500);
      }
      function close() {
        ov.classList.remove("is-on");
        root.classList.remove("has-call");
        setTimeout(function () { ov.hidden = true; }, fx ? 300 : 0);
      }
      function end() {
        clearInterval(timer); clearTimeout(timer);
        var d = ov.classList.contains("is-live") ? fmt(Date.now() - t0) : "00:00";
        ov.classList.add("is-end");
        q("state").textContent = "Appel terminé · " + d;
        q("time").textContent = "Terminé";
        endT = setTimeout(function () { close(); toastMsg("Simulation : aucun appel réel n’a été passé."); }, 1100);
      }
      ov.addEventListener("click", function (e) {
        if (e.target.closest("[data-co-end]")) { end(); return; }
        var b = e.target.closest("[data-co-t]");
        if (!b) return;
        var t = b.getAttribute("data-co-t"), on = b.getAttribute("aria-pressed") !== "true";
        if (t === "cam") {
          if (kind === "audio") { setKind("video"); q("title").textContent = "Visio · " + ((people[who] || {}).n || ""); return; }
          b.setAttribute("aria-pressed", on ? "true" : "false");
          ov.classList.toggle("cam-off", !on);
          return;
        }
        b.setAttribute("aria-pressed", on ? "true" : "false");
        if (t === "screen" && on) toastMsg("Simulation : le partage d’écran passerait par votre Hub.");
        if (t === "mute") ov.classList.toggle("is-muted", on);
      });
      ov.addEventListener("keydown", function (e) { if (e.key === "Escape") { e.stopPropagation(); end(); } });
      return { start: start, end: function () { if (!ov.hidden) { clearInterval(timer); clearTimeout(timer); clearTimeout(endT); ov.classList.remove("is-on"); ov.hidden = true; root.classList.remove("has-call"); } } };
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

    /* ---------------------------------------------------------------- Cartes (vectorielles, noires) */
    // Caméra : centre (x, y) et largeur visible w, en kilomètres. Les repères HTML suivent la caméra.
    var maps = $$("[data-map]");
    var BOXV = null;
    function camInit(m) {
      var c = m.getAttribute("data-cam").split(",").map(Number);
      m._home = c;
      m._cam = { x: c[0], y: c[1], w: c[2], h: c[3] };
      m._fit = true;
    }
    maps.forEach(camInit);
    function fitMap(m) {
      var W = m.clientWidth, H = m.clientHeight;
      if (!W || !H) return;
      var a = W / H, c = m._cam;
      if (m._fit) { c.w = Math.max(c.w, c.h * a); m._fit = false; }
      var vw = c.w, vh = vw / a;
      var b = m.getAttribute("data-box");
      if (b) {
        b = b.split(",").map(Number);
        vw = Math.min(vw, b[2]); vh = vw / a;
        if (vh > b[3]) { vh = b[3]; vw = vh * a; }
        c.w = vw;
        c.x = Math.max(b[0] + vw / 2, Math.min(b[0] + b[2] - vw / 2, c.x));
        c.y = Math.max(b[1] + vh / 2, Math.min(b[1] + b[3] - vh / 2, c.y));
      }
      var vx = c.x - vw / 2, vy = c.y - vh / 2;
      $(".ap-map-svg", m).setAttribute("viewBox", vx.toFixed(2) + " " + vy.toFixed(2) + " " + vw.toFixed(2) + " " + vh.toFixed(2));
      m.style.setProperty("--zk", Math.max(0, Math.min(1, (Math.log(700 / vw) / Math.log(700 / 25)))).toFixed(3));
      $$("[data-x]", m).forEach(function (o) {
        var px = (+o.getAttribute("data-x") - vx) / vw * 100, py = (+o.getAttribute("data-y") - vy) / vh * 100;
        var mn = +o.getAttribute("data-minw") || 0, mx = +o.getAttribute("data-maxw") || 1e9;
        var show = vw > mn && vw <= mx && px > -6 && px < 106 && py > -6 && py < 106;
        o.style.left = px.toFixed(2) + "%";
        o.style.top = py.toFixed(2) + "%";
        o.classList.toggle("is-gone", !show);
        if (show && o.classList.contains("ap-city")) {
          var half = o.offsetWidth / 2 / W * 100;
          o.classList.toggle("is-e", px + half > 97);
          o.classList.toggle("is-w", px - half < 3);
        }
      });
      var bar = $("[data-scale-bar]", m), st = $("[data-scale-t]", m);
      if (bar && st) {
        var pxkm = W / vw, steps = [1, 2, 5, 10, 20, 50, 100, 200], d = steps[0];
        steps.forEach(function (s) { if (s * pxkm <= 96) d = s; });
        bar.style.width = Math.round(d * pxkm) + "px";
        st.textContent = d + NB + "km";
      }
    }
    function fitAll() { maps.forEach(fitMap); }
    var big = $(".ap-map-big");
    var map = (function () {
      if (!big) return null;
      var anim = 0, sel = null, cards = $$("[data-envc]", big), envBtns = $$(".ap-env", big), listBtns = $$("[data-env-go]", root);
      function flyTo(x, y, w, ms) {
        cancelAnimationFrame(anim);
        var c = big._cam, x0 = c.x, y0 = c.y, w0 = c.w;
        if (!fx || reduce) { c.x = x; c.y = y; c.w = w; fitMap(big); return; }
        var dist = Math.hypot(x - x0, y - y0), bump = Math.min(1.4, dist / Math.max(w0, w) * .55);
        var dur = ms || Math.min(1500, 650 + dist * 1.6), t0 = performance.now();
        (function step(t) {
          var k = Math.min(1, (t - t0) / dur), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
          c.x = x0 + (x - x0) * e; c.y = y0 + (y - y0) * e;
          c.w = Math.exp(Math.log(w0) + (Math.log(w) - Math.log(w0)) * e) * (1 + bump * Math.sin(Math.PI * e));
          fitMap(big);
          if (k < 1) anim = requestAnimationFrame(step);
        })(t0);
      }
      function home() { var h = big._home; flyTo(h[0], h[1], Math.max(h[2], h[3] * big.clientWidth / Math.max(1, big.clientHeight))); }
      function select(k) {
        sel = k;
        cards.forEach(function (c) { c.hidden = c.getAttribute("data-envc") !== k; });
        envBtns.forEach(function (b) { b.classList.toggle("is-sel", b.getAttribute("data-env") === k); });
        listBtns.forEach(function (b) {
          if (!b.classList.contains("ap-envl")) return;
          var on = b.getAttribute("data-env-go") === k;
          b.classList.toggle("is-on", on);
          b.setAttribute("aria-pressed", on ? "true" : "false");
        });
        big.classList.toggle("has-card", !!k);
        big.classList.toggle("is-route", k === "boulance");
        if (k === "boulance") live();
      }
      function focus(k) {
        var b = $('.ap-env[data-env="' + k + '"]', big);
        if (!b) return;
        select(k);
        // la fiche couvre la gauche de la carte : le lieu se place au centre de ce qui reste visible
        var w = +b.getAttribute("data-w"), shift = big.clientWidth > 620 ? w * .17 : 0;
        flyTo(+b.getAttribute("data-x") - shift, +b.getAttribute("data-y") + (big.clientWidth > 620 ? 0 : w * .18), w);
      }
      big.addEventListener("click", function (e) {
        if (big._dragged) { big._dragged = false; return; }
        var b = e.target.closest(".ap-env");
        if (b) { stop(); focus(b.getAttribute("data-env")); return; }
        var cl = e.target.closest(".ap-cluster");
        if (cl) { stop(); select(null); flyTo(+cl.getAttribute("data-x"), +cl.getAttribute("data-y"), +cl.getAttribute("data-w")); return; }
        if (e.target.closest("[data-envc-x]")) { select(null); return; }
        if (e.target.closest("[data-envc-zoom]") && sel) { focus(sel); return; }
        var rt = e.target.closest("[data-route-t]");
        if (rt) {
          var on = rt.getAttribute("aria-pressed") !== "true";
          rt.setAttribute("aria-pressed", on ? "true" : "false");
          var lt = $('[data-layer-t="trajet"]');
          if (lt && (lt.getAttribute("aria-pressed") === "true") !== on) lt.click();
          if (on) flyTo(24, -162, 390 * big.clientWidth / Math.max(1, big.clientHeight));
          return;
        }
        var z = e.target.closest("[data-zoom]");
        if (z) {
          stop();
          var d = +z.getAttribute("data-zoom"), c = big._cam;
          if (d === 0) { select(null); home(); } else flyTo(c.x, c.y, Math.max(14, Math.min(900, c.w * (d > 0 ? 1 / 1.9 : 1.9))), 520);
        }
      });
      listBtns.forEach(function (b) {
        if (b.hasAttribute("data-go")) return; // depuis l'accueil : géré par l'action commune
        b.addEventListener("click", function (e) { e.stopPropagation(); stop(); focus(b.getAttribute("data-env-go")); });
      });
      // Glisser pour se déplacer (souris), molette pour rapprocher (Ctrl, ou après un clic dans la carte)
      var drag = null;
      big.addEventListener("pointerdown", function (e) {
        if (e.pointerType === "touch" || e.button !== 0 || e.target.closest("button, a, .ap-envc")) return;
        cancelAnimationFrame(anim);
        drag = { x: e.clientX, y: e.clientY, cx: big._cam.x, cy: big._cam.y, moved: false };
        big.classList.add("is-active");
      });
      addEventListener("pointermove", function (e) {
        if (!drag) return;
        var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
        if (!drag.moved && Math.hypot(dx, dy) < 4) return;
        drag.moved = true;
        big.classList.add("is-drag");
        var r = big.getBoundingClientRect(), k = big._cam.w / r.width;
        big._cam.x = drag.cx - dx * k; big._cam.y = drag.cy - dy * k;
        fitMap(big);
      });
      addEventListener("pointerup", function () {
        if (!drag) return;
        big._dragged = drag.moved;
        drag = null;
        big.classList.remove("is-drag");
        setTimeout(function () { big._dragged = false; }, 0);
      });
      big.addEventListener("pointerleave", function () { if (!drag) big.classList.remove("is-active"); });
      big.addEventListener("wheel", function (e) {
        if (!e.ctrlKey && !e.metaKey && !big.classList.contains("is-active")) return;
        e.preventDefault();
        cancelAnimationFrame(anim);
        var r = big.getBoundingClientRect(), c = big._cam, f = Math.exp(Math.max(-1, Math.min(1, e.deltaY * (e.ctrlKey ? .012 : .0025))));
        var nw = Math.max(14, Math.min(900, c.w * f)), mx = (e.clientX - r.left) / r.width - .5, my = (e.clientY - r.top) / r.height - .5;
        c.x += mx * (c.w - nw); c.y += my * (c.w - nw) * r.height / r.width;
        c.w = nw;
        fitMap(big);
      }, { passive: false });
      big.addEventListener("dblclick", function (e) {
        if (e.target.closest("button, a, .ap-envc")) return;
        var r = big.getBoundingClientRect(), c = big._cam;
        flyTo(c.x + ((e.clientX - r.left) / r.width - .5) * c.w, c.y + ((e.clientY - r.top) / r.height - .5) * c.w * r.height / r.width, Math.max(14, c.w / 2), 480);
      });
      /* Couches */
      $$("[data-layer-t]").forEach(function (b) {
        b.addEventListener("click", function () {
          var on = b.getAttribute("aria-pressed") !== "true", k = b.getAttribute("data-layer-t");
          b.setAttribute("aria-pressed", on ? "true" : "false");
          if (k === "personnes") {
            if (on) { say("Personne n’a partagé sa position avec vous."); setTimeout(function () { b.setAttribute("aria-pressed", "false"); }, 1800); }
            return;
          }
          big.classList.toggle("no-" + k, !on);
          $$('[data-layer="' + k + '"]', big).forEach(function (el) { el.classList.toggle("is-off", !on); });
          var rt = $("[data-route-t]", big);
          if (k === "trajet" && rt) rt.setAttribute("aria-pressed", on ? "true" : "false");
        });
      });
      /* Batteries réelles de BouLance (service /live du site); sinon, valeur d'exemple étiquetée */
      var API = (document.documentElement.getAttribute("data-api") || "").replace(/\/$/, ""), liveT = 0;
      function paintSoc(soc, real) {
        $$("[data-live-soc]", root).forEach(function (el) {
          var b = $("b", el), col = soc >= 60 ? "#34d399" : soc >= 30 ? "#fbbf24" : "#f87171";
          b.textContent = Math.round(soc) + NB + "%";
          el.style.setProperty("--soc", col);
          el.classList.add("is-soc");
          el.classList.toggle("is-real", !!real);
          el.title = real ? "Mesure reçue des batteries de BouLance" : "Valeur d’exemple : liaison indisponible";
        });
        var s = $('.ap-env[data-env="boulance"] [data-env-short]', big);
        $$('[data-env-short="boulance"]', root).forEach(function (el) { el.textContent = "Stationné · batteries " + Math.round(soc) + NB + "%"; });
      }
      function live() {
        if (Date.now() - liveT < 60000) return;
        liveT = Date.now();
        // Le service n'accepte que le domaine du site : ailleurs (aperçu local), valeur d'exemple étiquetée.
        if (!API || !window.fetch || !/(^|\.)jameslaplume\.ca$/.test(location.hostname)) { paintSoc(78, false); return; }
        fetch(API + "/live", { cache: "no-store" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
          .then(function (d) {
            var bs = (d && d.ok && d.batteries || []).filter(function (b) { return b.soc >= 0; });
            if (!bs.length) throw new Error("vide");
            var cap = bs.reduce(function (a, b) { return a + (b.cap || 1); }, 0);
            paintSoc(bs.reduce(function (a, b) { return a + b.soc * (b.cap || 1); }, 0) / cap, true);
          }).catch(function () { paintSoc(78, false); });
      }
      var tourT = [];
      return {
        focus: focus, select: select, home: home, live: live,
        tour: function () {
          tourT.forEach(clearTimeout);
          tourT = [setTimeout(function () { if (!stopped) focus("boulance"); }, 1400),
                   setTimeout(function () { if (!stopped) { select(null); var cl = $(".ap-cluster", big); if (cl) flyTo(+cl.getAttribute("data-x"), +cl.getAttribute("data-y"), 26); } }, 5600)];
        },
        reset: function () { tourT.forEach(clearTimeout); tourT = []; cancelAnimationFrame(anim); select(null); camInit(big); fitMap(big); }
      };
    })();
    var toast = $('[data-ap="toast"]'), toastT = null;
    function say(msg) {
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add("is-on");
      clearTimeout(toastT);
      toastT = setTimeout(function () { toast.classList.remove("is-on"); }, 3200);
    }
    hooks.carte = {
      enter: function () { fitAll(); if (map) { map.live(); if (!stopped && fx) map.tour(); } },
      leave: function () { if (map) map.reset(); }
    };
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
          root.classList.toggle("is-away", !visible);
          if (visible) { firstShow(); if (shown) arm(); } else hold();
        });
      }, { threshold: .3 }).observe(stage);
    } else { visible = true; firstShow(); }
  });
})();