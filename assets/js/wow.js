/* JARVIS — moteur « WOW » (refonte novembre 2026)
   Règle d'or : rien ne dépend de ce script pour être visible. Les effets ne
   s'activent que sous html.fx, et tout filet de sécurité ramène le contenu.
   Sections : modes · barre · menu · sélecteurs · compteur de visites ·
   météo du héros · formulaire · effets de défilement · micro-animations. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia && matchMedia("(hover: hover) and (pointer: fine)").matches;
  doc.classList.add("js");

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); }
  function c01(v) { return Math.max(0, Math.min(1, v)); }
  function easeOut(k) { return 1 - Math.pow(1 - k, 3); }
  function store(kind) { try { return window[kind]; } catch (e) { return null; } }
  var session = store("sessionStorage");

  /* ---------- Modes Base, Signature et Platinum ---------- */
  var modeButtons = $$("[data-mode-set]");
  function applyMode(mode, remember) {
    doc.setAttribute("data-mode", mode);
    modeButtons.forEach(function (b) {
      var on = b.getAttribute("data-mode-set") === mode;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    if (remember) { try { localStorage.setItem("jarvis-mode", mode); } catch (e) {} }
  }
  applyMode(doc.getAttribute("data-mode") || "signature", false);
  modeButtons.forEach(function (b) {
    b.addEventListener("click", function () { applyMode(b.getAttribute("data-mode-set"), true); });
  });

  /* ---------- Barre : fond plein après défilement ---------- */
  var bar = $("[data-bar]");
  if (bar) {
    var solid = function () { bar.classList.toggle("is-solid", scrollY > 24); };
    addEventListener("scroll", solid, { passive: true });
    solid();
  }

  /* ---------- Menu mobile ---------- */
  var menuBtn = $("[data-menu]");
  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$(".sheet a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-open");
        menuBtn.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---------- Menu des extensions (déroulant de « Solutions ») ---------- */
  $$("[data-mega]").forEach(function (dd) {
    var t = $("[data-mega-t]", dd);
    var set = function (open) {
      dd.classList.toggle("is-open", open);
      t.setAttribute("aria-expanded", open ? "true" : "false");
    };
    t.addEventListener("click", function (e) {
      e.stopPropagation();
      set(!dd.classList.contains("is-open"));
    });
    dd.addEventListener("focusout", function (e) {
      if (!dd.contains(e.relatedTarget)) set(false);
    });
    document.addEventListener("click", function (e) { if (!dd.contains(e.target)) set(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && dd.classList.contains("is-open")) { set(false); t.focus(); }
    });
  });

  /* ---------- Menu de sections collant : section en cours surlignée ---------- */
  var toc = $("[data-toc-nav]");
  if (toc && "IntersectionObserver" in window) {
    var tocLinks = $$(".toc-in a", toc);
    var tocRow = $(".toc-in", toc);
    var fade = function () { tocRow.classList.toggle("is-scroll", tocRow.scrollWidth - tocRow.scrollLeft > tocRow.clientWidth + 4); };
    tocRow.addEventListener("scroll", fade, { passive: true });
    addEventListener("resize", fade);
    fade();
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var mark = function (id) {
      tocLinks.forEach(function (a) { a.classList.toggle("is-on", a === byId[id]); });
      var a = byId[id], row = a && a.parentNode;
      if (a && row.scrollWidth > row.clientWidth) {
        row.scrollTo({ left: a.offsetLeft - row.clientWidth / 2 + a.offsetWidth / 2, behavior: "smooth" });
      }
    };
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) mark(en.target.id); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) tio.observe(el);
    });
  }

  /* ---------- Sélecteurs de contenu (ex. : moments de la journée) ---------- */
  $$("[data-swap-group]").forEach(function (group) {
    var dataEl = document.getElementById(group.getAttribute("data-swap-group"));
    if (!dataEl) return;
    var data;
    try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var btns = $$("button[data-swap]", group);
    var scope = document.querySelector(group.getAttribute("data-swap-scope")) || document;
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) {
          var on = x === b;
          x.classList.toggle("is-on", on);
          x.setAttribute("aria-pressed", on ? "true" : "false");
        });
        var d = data[b.getAttribute("data-swap")] || {};
        Object.keys(d).forEach(function (k) {
          var el = scope.querySelector('[data-swap-field="' + k + '"]');
          if (el) el.textContent = d[k];
        });
      });
    });
  });

  /* ---------- Outils d'affichage ---------- */
  var TZ = "America/Toronto";
  function partsInTz(d) {
    var out = {};
    try {
      new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
        .formatToParts(d).forEach(function (p) { out[p.type] = p.value; });
    } catch (e) {
      out = { hour: String(d.getHours()).padStart(2, "0"), minute: String(d.getMinutes()).padStart(2, "0") };
    }
    return out;
  }
  function hm(d) { var p = partsInTz(d); return +p.hour + " h " + p.minute; }
  function fmtInt(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function setText(key, value, root) {
    $$('[data-live="' + key + '"]', root).forEach(function (el) { el.textContent = value; });
  }

  /* Compteur à rouleaux : chaque chiffre glisse vers sa valeur */
  function setOdo(el, text) {
    if (!el) return;
    el.setAttribute("aria-label", text);
    if (reduce) { el.textContent = text; return; }
    var chars = String(text).split("");
    el.textContent = "";
    var cols = [];
    chars.forEach(function (ch) {
      if (!/\d/.test(ch)) {
        var s = document.createElement("span");
        s.textContent = ch;
        s.setAttribute("aria-hidden", "true");
        el.appendChild(s);
        return;
      }
      var dg = document.createElement("span");
      dg.className = "dg";
      dg.setAttribute("aria-hidden", "true");
      var col = document.createElement("span");
      for (var i = 0; i <= 9; i++) {
        var n = document.createElement("span");
        n.textContent = i;
        col.appendChild(n);
      }
      dg.appendChild(col);
      el.appendChild(dg);
      cols.push({ col: col, d: +ch });
    });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        cols.forEach(function (c, k) {
          c.col.style.transitionDelay = (k * 90) + "ms";
          c.col.style.transform = "translateY(-" + c.d + "em)";
        });
      });
    });
  }

  /* ---------- Compteur de visites (une visite par session) ---------- */
  /* Service du site (Worker Cloudflare) si configuré, sinon compteur Abacus */
  var API = doc.getAttribute("data-api");
  var COUNTER = "https://abacus.jasoncameron.dev";
  var COUNTER_KEY = "/jameslaplume-ca/visites";
  function loadVisits() {
    var cached = session && session.getItem("jarvis-visits");
    if (cached) {
      try {
        var c = JSON.parse(cached);
        if (Date.now() - c.t < 60000) return Promise.resolve(c.v);
      } catch (e) {}
    }
    var counted = session && session.getItem("jarvis-visit-counted");
    var req = API
      ? fetch(API + (counted ? "/visits" : "/visits/hit"), { method: counted ? "GET" : "POST", cache: "no-store" })
      : fetch(COUNTER + (counted ? "/get" : "/hit") + COUNTER_KEY, { cache: "no-store" });
    return req
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) {
        var v = +j.value;
        if (!(v >= 0)) throw new Error("valeur");
        if (session) {
          session.setItem("jarvis-visit-counted", "1");
          session.setItem("jarvis-visits", JSON.stringify({ v: v, t: Date.now() }));
        }
        return v;
      });
  }
  var visitTargets = $$('[data-live="visits"], [data-live="visits-short"], [data-live="visits-foot"]');
  /* Le grand compteur ne roule qu'une fois à l'écran */
  var visitOdos = $$('[data-live="visits"]');
  if (visitOdos.length && "IntersectionObserver" in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target._seen = true;
        if (e.target._odo) setOdo(e.target, e.target._odo);
        vio.unobserve(e.target);
      });
    }, { threshold: .5 });
    visitOdos.forEach(function (el) { vio.observe(el); });
  } else visitOdos.forEach(function (el) { el._seen = true; });
  if (visitTargets.length) {
    loadVisits().then(function (v) {
      var txt = fmtInt(v);
      visitOdos.forEach(function (el) { el._odo = txt; if (el._seen) setOdo(el, txt); });
      setText("visits-short", txt + " visites");
      $$('[data-live="visits-foot"]').forEach(function (el) { el.textContent = txt; el.closest(".foot-count").hidden = false; });
    }).catch(function () {
      setText("visits-short", "Visites —");
      visitOdos.forEach(function (el) { el.textContent = "—"; });
    });
  }

  /* ---------- Météo réelle pour le héros (pastille et panneau) ----------
     JARVIS App (assets/demos/app.js) lit la même source; ce cache de session s'appelle « jarvis-ec ». */
  var livePill = $("[data-live-pill]");
  if (livePill || $("[data-hero-panel]")) {
    var EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/qc-22?f=json&lang=fr";
    var ecText = function (o) {
      if (o == null) return "";
      if (typeof o !== "object") return String(o);
      if (o.fr !== undefined) return String(o.fr);
      return o.value !== undefined ? ecText(o.value) : "";
    };
    var ecDate = function (o) { var d = o ? new Date(ecText(o)) : null; return d && !isNaN(d) ? d : null; };
    var pillDot = function (ok) { var dot = livePill && $(".dot", livePill); if (dot) dot.classList.toggle("is-off", !ok); };
    var heroLoad = function () {
      var cached = null;
      try { var c = JSON.parse(session.getItem("jarvis-ec")); if (Date.now() - c.t < 300000) cached = c.j; } catch (e) {}
      var got = cached ? Promise.resolve(cached) : fetch(EC_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
      got.then(function (j) {
        if (!cached && session) { try { session.setItem("jarvis-ec", JSON.stringify({ t: Date.now(), j: j })); } catch (e) {} }
        var p = j.properties || {}, cc = p.currentConditions || {}, rs = p.riseSet || {};
        var t = parseFloat(ecText(cc.temperature)), temp = isFinite(t) ? t : null, cond = ecText(cc.condition);
        if (temp === null && !cond) throw new Error("vide");
        pillDot(true);
        setText("temp-short", temp !== null ? String(Math.round(temp) || 0).replace("-", "\u2212") + "\u00a0°C" : "—");
        setText("cond", cond || "Conditions actuelles");
        try {
          document.dispatchEvent(new CustomEvent("jv:weather", { detail: {
            now: new Date(), temp: temp, condition: cond, rise: ecDate(rs.sunrise), set: ecDate(rs.sunset)
          } }));
        } catch (e) {}
      }).catch(function () {
        pillDot(false);
        setText("temp-short", "hors ligne");
        setText("cond", "Météo indisponible pour l’instant");
      });
    };
    heroLoad();
    setInterval(function () { if (!document.hidden) heroLoad(); }, 600000);
  }

  /* ---------- Formulaire de contact : envoi sans quitter la page ---------- */
  $$("form[data-contact]").forEach(function (form) {
    var status = $(".form-status", form);
    var btn = $('button[type="submit"]', form);
    var label = btn ? btn.querySelector(".lbl") : null;
    function show(kind, html) {
      status.className = "form-status is-show is-" + kind;
      status.innerHTML = html;
      status.setAttribute("role", kind === "err" ? "alert" : "status");
    }
    function payload() {
      var o = {};
      new FormData(form).forEach(function (v, k) { o[k] = typeof v === "string" ? v.trim() : v; });
      return o;
    }
    function mailtoFor(o) {
      var body = [
        "Nom : " + (o.nom || ""), "Courriel : " + (o.email || ""),
        "Environnement : " + (o.environnement || ""), "Organisation : " + (o.organisation || ""),
        "Région : " + (o.region || ""), "Profil : " + (o.profil || ""), "Sujet : " + (o.sujet || ""),
        "", o.message || ""
      ].join("\n");
      return "mailto:laplumejames@gmail.com?subject=" + encodeURIComponent("Demande — " + (o.sujet || "JARVIS")) +
        "&body=" + encodeURIComponent(body);
    }
    function withTimeout(p, ms) {
      return new Promise(function (res, rej) {
        var t = setTimeout(function () { rej(new Error("délai")); }, ms);
        p.then(function (v) { clearTimeout(t); res(v); }, function (e) { clearTimeout(t); rej(e); });
      });
    }
    function post(url, o) {
      return withTimeout(fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(o)
      }), 15000).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          var ok = r.ok && j && (j.success === true || j.success === "true" || j.ok === true);
          if (!ok) { var e = new Error((j && j.message) || ("HTTP " + r.status)); e.reply = j; throw e; }
          return j;
        });
      });
    }
    form.addEventListener("submit", function (e) {
      if (!window.fetch || !window.Promise) return; // envoi classique
      e.preventDefault();
      if (!form.reportValidity()) return;
      var o = payload();
      if (o._honey) return;
      delete o._honey;
      delete o._next;
      o.page = location.pathname;
      var endpoints = [form.getAttribute("data-endpoint"), form.getAttribute("data-fallback")].filter(Boolean);
      form.classList.add("is-sending");
      btn.disabled = true;
      if (label) label.textContent = "Envoi en cours…";
      status.className = "form-status";
      var attempt = function (i) {
        if (i >= endpoints.length) return Promise.reject(new Error("aucun service"));
        return post(endpoints[i], o).catch(function (err) {
          if (i + 1 < endpoints.length) return attempt(i + 1);
          throw err;
        });
      };
      attempt(0).then(function () {
        form.classList.remove("is-sending");
        var first = (o.nom || "").split(" ")[0];
        form.innerHTML = '<div class="form-done" role="status"><div class="check" aria-hidden="true">✓</div>' +
          "<h3>Merci" + (first ? ", " + first.replace(/[<>&"]/g, "") : "") + ".</h3>" +
          "<p>Votre message est transmis à James. Il vous répondra personnellement.</p></div>";
      }).catch(function (err) {
        form.classList.remove("is-sending");
        btn.disabled = false;
        if (label) label.textContent = "Réessayer l’envoi";
        var msg = (err && err.message) || "";
        var needsActivation = /activat/i.test(msg);
        show("err",
          (needsActivation
            ? "<b>Le service d’envoi est en cours d’activation.</b> "
            : "<b>Le service d’envoi ne répond pas pour le moment.</b> ") +
          "Votre message n’est pas perdu : " +
          '<a href="' + mailtoFor(o).replace(/"/g, "&quot;") + '">ouvrez-le dans votre courriel</a>, il est déjà rédigé. ' +
          "Ou écrivez directement à laplumejames@gmail.com.");
      });
    });
  });

  /* ---------- Panneau JARVIS du héros : propositions approuvées, pièces qui suivent ---------- */
  var hp = $("[data-hero-panel]");
  if (hp) {
    var hpAsk = $("[data-hp-ask]", hp), hpText = $("[data-hp-text]", hp), hpState = $(".hp-state", hp);
    var hpClock = $("[data-hp-clock]", hp);
    var clockTick = function () { if (hpClock) hpClock.textContent = hm(new Date()); };
    clockTick();
    setInterval(clockTick, 30000);
    var room = function (k) { return $('[data-room="' + k + '"]', hp); };
    var setRoom = function (k, txt, v) {
      var li = room(k); if (!li) return;
      var b = $("b", li); b.textContent = txt; b.classList.add("is-new");
      setTimeout(function () { b.classList.remove("is-new"); }, 1600);
      var bar = $("i", li); if (bar && v !== undefined) bar.style.setProperty("--v", v);
    };
    $$(".hp-rooms li", hp).forEach(function (li, k) { li.style.setProperty("--k", k); });
    /* Propositions : la première suit la vraie météo dès qu'elle arrive */
    var asks = [
      { t: "Passer la maison en mode nuit à 23 h ? Portes verrouillées, caméras en détection.",
        done: "Confirmé · mode nuit prévu à 23 h", apply: function () { setRoom("entree", "Verrouillée"); setRoom("salon", "Veilleuse · 10 %", .1); setRoom("energie", "0,6 kW", .15); } },
      { t: "La porte du garage est ouverte depuis 20 minutes. La fermer ?",
        done: "Confirmé · porte du garage fermée", apply: function () { setRoom("energie", "0,7 kW", .18); } },
      { t: "Plus personne à la maison. Passer en mode Absent ? Lumières éteintes, chauffage à 17 °C.",
        done: "Confirmé · mode Absent actif", apply: function () { setRoom("salon", "Éteint", 0); setRoom("chambre", "17 °C", .2); setRoom("entree", "Verrouillée"); setRoom("energie", "0,3 kW", .08); } }
    ];
    var initial = { salon: ["Soirée · 60 %", .6], chambre: ["19 °C", .42], entree: ["Déverrouillée"], energie: ["1,2 kW", .3] };
    document.addEventListener("jv:weather", function (e) {
      var d = e.detail;
      if (d.temp === null) return;
      var night = d.rise && d.set ? (d.now < d.rise || d.now > d.set) : true;
      if (d.temp <= 8) {
        asks[0] = { t: "Il fait " + String(Math.round(d.temp)).replace("-", "−") + " °C dehors. Monter les chambres à 20 °C pour 6 h 30 ?",
          done: "Confirmé · chambres à 20 °C pour 6 h 30", apply: function () { setRoom("chambre", "20 °C à 6 h 30", .55); setRoom("energie", "1,6 kW", .42); } };
      } else if (!night && d.set) {
        var on = new Date(d.set.getTime() - 15 * 60000);
        asks[0] = { t: "Le soleil se couche à " + hm(d.set) + ". Allumer l’extérieur à " + hm(on) + " ?",
          done: "Confirmé · extérieur à " + hm(on), apply: function () { setRoom("energie", "1,3 kW", .34); } };
      }
      if (cur === 0 && !hpAsk.classList.contains("is-sent")) hpText.textContent = asks[0].t;
    });
    var cur = 0, busy = false, touched = false, timer = null;
    var show = function (i) {
      cur = i % asks.length;
      hpAsk.classList.remove("is-sent", "is-ok");
      hpText.textContent = asks[cur].t;
      busy = false;
    };
    var answer = function (ok) {
      if (busy) return;
      busy = true;
      var btn = $('[data-hp="' + (ok ? "ok" : "no") + '"]', hp);
      btn.classList.add("is-press");
      setTimeout(function () {
        btn.classList.remove("is-press");
        hpAsk.classList.add("is-sent");
        if (!ok) { hpState.textContent = "Reporté · JARVIS reproposera plus tard"; return; }
        hpState.textContent = "Envoyé…";
        setTimeout(function () {
          hpAsk.classList.add("is-ok");
          hpState.textContent = asks[cur].done;
          asks[cur].apply();
        }, 900);
      }, 220);
    };
    hp.addEventListener("click", function (e) {
      var b = e.target.closest("[data-hp]");
      if (!b) return;
      touched = true;
      clearTimeout(timer);
      answer(b.getAttribute("data-hp") === "ok");
      timer = setTimeout(function () { show(cur + 1); }, 6000);
    });
    /* Lecture automatique tant que le visiteur n'a pas touché */
    var cycle = function () {
      if (touched || document.hidden) return;
      answer(true);
      timer = setTimeout(function () {
        if (touched) return;
        Object.keys(initial).forEach(function (k) { setRoom(k, initial[k][0], initial[k][1]); });
        show(cur + 1);
        timer = setTimeout(cycle, 4200);
      }, 5200);
    };
    var hpSeen = false;
    var hpGo = function () {
      if (hpSeen) return;
      hpSeen = true;
      hp.classList.add("is-in");
      if (!reduce) timer = setTimeout(cycle, 4200);
    };
    setTimeout(hpGo, reduce ? 0 : 1900);
  }

  if (reduce) return;
  doc.classList.add("fx");

  /* Filet de sécurité : tout redevient visible (impression) */
  function defuse() {
    doc.classList.remove("fx");
    $$(".hero .bg,.hero .bg img")
      .forEach(function (el) { el.style.opacity = ""; el.style.transform = ""; el.style.filter = ""; });
  }
  addEventListener("beforeprint", defuse);

  /* Barre de progression de lecture */
  var progress = document.createElement("div");
  progress.className = "progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.appendChild(progress);

  /* Titres découpés en mots (dévoilement en cascade) */
  $$("[data-split]").forEach(function (h) {
    var i = 0;
    (function walk(node) {
      [].slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/);
          var frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var s = document.createElement("span");
            s.className = "w";
            s.style.setProperty("--i", i++);
            s.textContent = p;
            frag.appendChild(s);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") {
          walk(n);
        }
      });
    })(h);
  });

  /* Héros : zoom, assombrissement et parallaxe à la souris */
  var hero = $("[data-hero]") || $(".hero");
  var heroImg = hero ? $(".bg", hero) : null;
  var mx = 0, my = 0, tmx = 0, tmy = 0;
  if (hero && finePointer) {
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      tmx = (e.clientX - r.left) / r.width - .5;
      tmy = (e.clientY - r.top) / r.height - .5;
      schedule();
    });
    hero.addEventListener("pointerleave", function () { tmx = 0; tmy = 0; schedule(); });
  }

  function frame() {
    var vh = innerHeight;
    var max = Math.max(1, document.documentElement.scrollHeight - vh);
    progress.style.transform = "scaleX(" + c01(scrollY / max).toFixed(4) + ")";

    mx += (tmx - mx) * .12;
    my += (tmy - my) * .12;
    if (heroImg) {
      var p = c01(scrollY / Math.max(vh, 1));
      heroImg.style.transform = "translate3d(" + (-mx * 22).toFixed(2) + "px," + (-my * 14).toFixed(2) + "px,0) scale(" + (1.04 + p * .14) + ")";
      heroImg.style.filter = "brightness(" + (1 - p * .55) + ")";
      if (Math.abs(tmx - mx) > .002 || Math.abs(tmy - my) > .002) schedule();
    }
  }
  var queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; frame(); });
  }
  addEventListener("scroll", schedule, { passive: true });
  addEventListener("resize", schedule);
  schedule();

  /* Révélations à l'entrée dans la fenêtre */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: .18 });
  $$("[data-rev]").forEach(function (el) { io.observe(el); });

  /* Patrouille : aucun élément dans la fenêtre ne reste caché */
  setInterval(function () {
    $$("[data-rev]:not(.in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < innerHeight * 1.05 && r.bottom > 0) el.classList.add("in");
    });
  }, 800);

  /* Compteurs animés */
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var b = e.target, end = +b.getAttribute("data-n"), t0 = performance.now();
      (function tickN(t) {
        var k = c01((t - t0) / 1400), v = Math.round(end * easeOut(k));
        b.textContent = v;
        if (k < 1) requestAnimationFrame(tickN);
      })(t0);
    });
  }, { threshold: .5 });
  $$("[data-n]").forEach(function (el) { cio.observe(el); });

  if (!finePointer) return;

  /* Halo qui suit le pointeur sur les cartes */
  $$(".card, .plan, .stat").forEach(function (el) {
    el.classList.add("spot");
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty("--px", (e.clientX - r.left) + "px");
      el.style.setProperty("--py", (e.clientY - r.top) + "px");
      el.style.setProperty("--spot", "1");
    });
    el.addEventListener("pointerleave", function () { el.style.setProperty("--spot", "0"); });
  });

  /* Inclinaison 3D des tuiles */
  $$("[data-tilt]").forEach(function (el) {
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.classList.add("is-tilting");
      el.style.transform = "perspective(900px) rotateY(" + (x * 7).toFixed(2) + "deg) rotateX(" + (-y * 7).toFixed(2) + "deg) translateZ(0)";
    });
    el.addEventListener("pointerleave", function () {
      el.classList.remove("is-tilting");
      el.style.transform = "";
    });
  });

  /* Boutons magnétiques */
  $$("[data-magnet]").forEach(function (el) {
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      var x = e.clientX - (r.left + r.width / 2), y = e.clientY - (r.top + r.height / 2);
      el.style.transform = "translate(" + (x * .18).toFixed(1) + "px," + (y * .28).toFixed(1) + "px)";
    });
    el.addEventListener("pointerleave", function () { el.style.transform = ""; });
  });
})();
