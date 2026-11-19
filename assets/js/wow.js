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
  function fmtInt(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }

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
  /* Journal des visites (service du site) : la page et le domaine d'origine voyagent avec la visite,
     sans témoin. James exclut ses appareils avec localStorage « jarvis-moi » = 1 (bouton sur
     /admin/visites/); les pages /admin/ ne comptent jamais. */
  var local = store("localStorage");
  var silent = /^\/admin\//.test(location.pathname);
  try { silent = silent || (local && local.getItem("jarvis-moi") === "1"); } catch (e) {}
  var alreadyCounted = !!(session && session.getItem("jarvis-visit-counted"));
  function visitInfo() { return JSON.stringify({ path: location.pathname, ref: document.referrer || "" }); }
  if (API && !silent && alreadyCounted) {
    /* Page suivante de la même session : inscrite au journal, le compteur ne bouge pas */
    try { navigator.sendBeacon(API + "/visits/view", visitInfo()); } catch (e) {}
  }
  function loadVisits() {
    var cached = session && session.getItem("jarvis-visits");
    if (cached) {
      try {
        var c = JSON.parse(cached);
        if (Date.now() - c.t < 60000) return Promise.resolve(c.v);
      } catch (e) {}
    }
    var counted = (session && session.getItem("jarvis-visit-counted")) || silent;
    /* Texte brut (JSON) : requête simple, sans requête préalable CORS */
    var req = API
      ? (counted ? fetch(API + "/visits", { cache: "no-store" })
        : fetch(API + "/visits/hit", { method: "POST", cache: "no-store", body: visitInfo() }))
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
  var visitTargets = $$('[data-live="visits"], [data-live="visits-foot"]');
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
      $$('[data-live="visits-foot"]').forEach(function (el) { el.textContent = txt; el.closest(".foot-count").hidden = false; });
    }).catch(function () {
      visitOdos.forEach(function (el) { el.textContent = "—"; });
    });
  }

  /* ---------- Formulaire de contact : envoi sans quitter la page ---------- */
  $$("form[data-contact]").forEach(function (form) {
    var status = $(".form-status", form);
    var btn = $('button[type="submit"]', form);
    var label = btn ? btn.querySelector(".lbl") : null;
    /* Arrivée depuis le catalogue : la configuration préremplit le message. */
    try {
      var cfg = new URLSearchParams(location.search).get("config");
      var msg = $('textarea[name="message"]', form);
      if (cfg && msg && !msg.value) {
        msg.value = "Mon forfait JARVIS :\n" + cfg.split(" + ").join("\n- ").replace(/^/, "- ") + "\n\nMon lieu et mes questions :\n";
        var sujet = $('select[name="sujet"]', form);
        if (sujet) { var o = document.createElement("option"); o.textContent = "Soumission pour mon forfait"; sujet.insertBefore(o, sujet.firstChild); sujet.value = o.textContent; }
        msg.focus();
      }
    } catch (e) {}
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
          if (!ok) {
            var e = new Error((j && j.message) || ("HTTP " + r.status)); e.reply = j;
            /* stored:true = la demande est gardée chez JARVIS même si le courriel n'est pas parti :
               on essaie quand même le service de secours, mais le visiteur verra un succès. */
            if (j && j.stored === true) e.stored = true;
            throw e;
          }
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
      var stored = false;
      var attempt = function (i) {
        if (i >= endpoints.length) return stored ? Promise.resolve({ stored: true }) : Promise.reject(new Error("aucun service"));
        return post(endpoints[i], o).catch(function (err) {
          if (err && err.stored) stored = true;
          if (i + 1 < endpoints.length) return attempt(i + 1);
          if (stored) return { stored: true };
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

  /* ---------- Effets : seulement si le mouvement est permis, puis seulement avec un pointeur fin ----------
     Dans leur propre bloc : sur un téléphone (pointeur tactile) ou avec « réduire les animations », on sort
     de ce bloc seulement. Le forfait, plus bas, doit tourner partout. */
  (function () {
    if (reduce) return;
    doc.classList.add("fx");

    /* Filet de sécurité : tout redevient visible (impression) */
    function defuse() {
      doc.classList.remove("fx");
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

    function frame() {
      var vh = innerHeight;
      var max = Math.max(1, document.documentElement.scrollHeight - vh);
      progress.style.transform = "scaleX(" + c01(scrollY / max).toFixed(4) + ")";
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

  /* ---------- Mon forfait : il se bâtit en chemin, et s'ouvre partout ----------
     Une seule clé (« jarvis-forfait ») : les lieux choisis, le niveau, les solutions, et, écrits par le
     configurateur (/offre/, assets/demos/catalogue.js), le matériel et les services (« autres ») et
     l'état du formulaire (« etat »). Rien ne quitte le navigateur.
     Le forfait se voit dans un tiroir (bouton de la barre) et dans la colonne de /offre/ : même rendu,
     comme un sac d'achats : vignette, nom, quantité, « Retirer », puis le résumé et la soumission.
     Les noms et vignettes viennent du bloc [data-forfait-ref] présent sur chaque page (src/lieux.py). */
  var CLE_F = "jarvis-forfait", RANG = { base: 1, signature: 2, platinum: 3 };
  var REF = { lieux: {}, sols: {}, hubs: {} }, boiteR = $("[data-forfait-ref]");
  if (boiteR) { try { REF = JSON.parse(boiteR.textContent) || REF; } catch (e) {} }
  function lireF() {
    var o = {};
    try { o = JSON.parse(localStorage.getItem(CLE_F) || "{}") || {}; } catch (e) { o = {}; }
    return { lieux: o.lieux || [], sols: o.sols || [], hub: o.hub || "", manuel: !!o.manuel,
      public: o.public === "entreprise" || o.public === "deux" ? o.public : "moi", separee: !!o.separee,
      autres: o.autres || [], etat: o.etat || null, suffixe: o.suffixe || "" };
  }
  function ecrireF(o) { try { localStorage.setItem(CLE_F, JSON.stringify(o)); } catch (e) {} majF(); }
  var LIEUX = null, boiteL = $("[data-lieux-data]");
  if (boiteL) { try { LIEUX = JSON.parse(boiteL.textContent); } catch (e) { LIEUX = null; } }
  function echap(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function hubDe(o) {   /* l'appareil le plus exigeant parmi les lieux choisis */
    var h = "";
    o.lieux.forEach(function (x) { var r = REF.lieux[x] && REF.lieux[x].h; if (r && (RANG[r] || 0) > (RANG[h] || 0)) h = r; });
    return h;
  }
  /* Les règles de l'offre (docs/OFFRE.md) : un seul niveau pour tous les lieux; le lieu principal (celui
     qui demande le plus gros appareil) porte le niveau; aucun autre appareil ne dépasse le niveau.
     Même règle, côté construction : cerveaux() dans src/lieux.py. */
  function cerveaux(o) {
    var N = o.hub || hubDe(o), prin = "", hub = {};
    o.lieux.forEach(function (id) { var r = REF.lieux[id]; if (r && r.h && (!prin || (RANG[r.h] || 0) > (RANG[REF.lieux[prin].h] || 0))) prin = id; });
    o.lieux.forEach(function (id) {
      var r = REF.lieux[id]; if (!r) return;
      hub[id] = !r.h ? "" : id === prin ? (N || r.h) : (N && (RANG[r.h] || 0) > (RANG[N] || 0) ? N : r.h);
    });
    return { niveau: N, principal: prin, hub: hub };
  }
  /* Ce que contient le forfait, prêt à afficher. */
  function lignesF(o) {
    var c = cerveaux(o);
    var L = o.lieux.map(function (id) { var r = REF.lieux[id]; return r ? { id: id, n: r.n, h: c.hub[id], b: r.b, p: r.p, img: r.img } : null; }).filter(Boolean);
    var avec = L.filter(function (l) { return l.h; });
    var hubSeul = o.hub && !avec.length ? o.hub : "";
    var lot = o.autres.filter(function (a) { return a.k === "lot"; })[0] || null;
    var S = lot ? [] : o.sols.map(function (s) { var r = REF.sols[s]; return r ? { slug: s, n: r.n, img: r.img } : null; }).filter(Boolean);
    var A = o.autres.filter(function (a) { return a.k !== "lot"; });
    return { L: L, hubSeul: hubSeul, lot: lot, S: S, A: A, niveau: c.niveau, n: L.length + (hubSeul ? 1 : 0) + (lot ? 1 : 0) + S.length + A.length };
  }
  function nomNiveau(h) { return h ? h.charAt(0).toUpperCase() + h.slice(1) : ""; }
  function quoiLieu(l) { return (l.h && REF.hubs[l.h] ? REF.hubs[l.h].n : "") + (l.b ? (l.h ? " + " : "") + l.b : ""); }
  function lienF(o, x) {   /* le message de soumission : les lieux d'abord, puis chaque ligne */
    function dit(l) { var q = quoiLieu(l); return l.n + (q ? " (" + q + ")" : ""); }
    var chez = x.L.filter(function (l) { return l.p !== "entreprise"; }).map(dit), ent = x.L.filter(function (l) { return l.p === "entreprise"; }).map(dit), t = [];
    if (x.niveau && x.L.length) t.push("Niveau " + nomNiveau(x.niveau));
    if (chez.length) t.push("Chez vous : " + chez.join(", "));
    if (ent.length) t.push("Votre entreprise : " + ent.join(", "));
    if (chez.length && ent.length && o.separee) t.push("Soumission séparée pour l’entreprise, au nom de l’entreprise");
    if (x.hubSeul && REF.hubs[x.hubSeul]) t.push(REF.hubs[x.hubSeul].n);
    if (x.lot) t.push(x.lot.n);
    x.S.forEach(function (s) { t.push(s.n); });
    x.A.forEach(function (a) { t.push((a.q > 1 ? a.q + "× " : "") + a.n); });
    return "/contact/?config=" + encodeURIComponent(t.join(" + ") + (o.suffixe || ""));
  }
  function vig(img, nom) {
    return img ? '<img class="fo-v" src="' + echap(img) + '" alt="" loading="lazy" width="64" height="64">'
      : '<span class="fo-v fo-v0" aria-hidden="true">' + echap(String(nom).charAt(0)) + "</span>";
  }
  function rang(img, nom, sous, droite, prix) {
    return '<li class="fo-l">' + vig(img, nom) + '<div class="fo-t"><b>' + echap(nom) + "</b>" + (sous ? "<span>" + echap(sous) + "</span>" : "") +
      (prix ? "<em>" + echap(prix) + "</em>" : "") + '</div><div class="fo-a">' + droite + "</div></li>";
  }
  function retirer(cle, nom) { return '<button type="button" class="fo-rm" data-fo-rm="' + echap(cle) + '" aria-label="Retirer ' + echap(nom) + '">Retirer</button>'; }
  function groupe(titre, n, lis) { return lis ? '<section class="fo-g"><h3>' + titre + " <i>" + n + "</i></h3><ul>" + lis + "</ul></section>" : ""; }
  function renduF(o) {
    var x = lignesF(o), surOffre = !!window.JarvisCatalogue;
    if (!x.n) {
      return '<div class="fo fo-vide"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 17h24l2 23H10l2-23Z"/><path d="M18 20v-5a6 6 0 0 1 12 0v5"/></svg>' +
        "<b>Votre forfait est vide.</b><p>Choisissez vos lieux : JARVIS propose le cerveau de chacun, puis votre niveau.</p>" +
        '<a class="pill" href="/offre/#composer" data-fo-suite>Commencer par mon lieu</a></div>';
    }
    var lieux = x.L.map(function (l) { return rang(l.img, l.n, quoiLieu(l) || "Un boîtier à bord", retirer("lieu:" + l.id, l.n)); }).join("") +
      (x.hubSeul && REF.hubs[x.hubSeul] ? rang(REF.hubs[x.hubSeul].img, REF.hubs[x.hubSeul].n, "Choisi, sans lieu précis", retirer("hub:", REF.hubs[x.hubSeul].n)) : "");
    var sols = (x.lot ? rang("", x.lot.n, "Par mois", surOffre ? retirer("autre:" + x.lot.id, x.lot.n) : '<a class="fo-mod" href="/offre/#solutions" data-fo-suite>Modifier</a>', x.lot.px) : "") +
      x.S.map(function (s) { return rang(s.img, s.n, "Par mois, annulable", retirer("sol:" + s.slug, s.n)); }).join("");
    var autres = x.A.map(function (a) {
      var droite = a.k === "mat"
        ? '<span class="fo-q"><button type="button" data-fo-q="' + echap(a.id) + ':-1" aria-label="Un de moins">−</button><output>' + a.q + '</output><button type="button" data-fo-q="' + echap(a.id) + ':1" aria-label="Un de plus">+</button></span>' + retirer("mat:" + a.id, a.n)
        : (surOffre ? retirer("autre:" + a.id, a.n) : '<a class="fo-mod" href="/offre/#projet" data-fo-suite>Modifier</a>');
      return rang(a.img, a.n, a.s || (a.q > 1 && a.k !== "mat" ? a.q + " " + (a.u || "") : ""), droite, a.px);
    }).join("");
    var deux = x.L.some(function (l) { return l.p === "entreprise"; }) && x.L.some(function (l) { return l.p !== "entreprise"; });
    function ligne(k, v) { return v ? "<div><dt>" + k + "</dt><dd>" + v + "</dd></div>" : ""; }
    return '<div class="fo">' +
      '<p class="fo-haut"><span>' + x.n + (x.n > 1 ? " éléments" : " élément") + '</span><button type="button" class="fo-rm" data-fo-vider>Tout retirer</button></p>' +
      groupe("Vos lieux", x.L.length + (x.hubSeul ? 1 : 0), lieux) + groupe("Extensions ajoutées", x.S.length + (x.lot ? 1 : 0), sols) + groupe("Matériel et services", x.A.length, autres) +
      '<div class="fo-pied">' +
      (deux ? '<label class="fo-sep"><input type="checkbox" data-fo-sep' + (o.separee ? " checked" : "") + "><span>Une soumission séparée pour l’entreprise, au nom de l’entreprise</span></label>" : "") +
      '<dl class="fo-res">' + ligne("Niveau", x.L.length ? nomNiveau(x.niveau) : "") + ligne("Lieux", x.L.length) + ligne("Extensions ajoutées, par mois", x.S.length + (x.lot ? 1 : 0)) + ligne("Matériel et services, une fois", x.A.length) + "</dl>" +
      '<p class="fo-note">Prix confirmé par écrit dans votre soumission, ligne par ligne. Rien à payer ici.</p>' +
      '<a class="pill fo-go" href="' + lienF(o, x) + '">Recevoir ma soumission</a>' +
      '<a class="fo-suite" href="/offre/#composer" data-fo-suite>Continuer à composer</a></div></div>';
  }

  function majF() {
    var o = lireF(), n = lignesF(o).n;
    $$("[data-forfait-n]").forEach(function (b) { b.hidden = !n; b.textContent = n ? " · " + n : ""; });
    $$("[data-forfait-l]").forEach(function (l) {
      if (!l.getAttribute("data-vide")) l.setAttribute("data-vide", l.textContent);
      l.textContent = n ? l.getAttribute("data-plein") : l.getAttribute("data-vide");
    });
    $$("[data-cart-count]").forEach(function (c) { c.textContent = n ? " · " + n : ""; });
    $$("[data-forfait-add]").forEach(function (b) {
      var on = o.sols.indexOf(b.getAttribute("data-forfait-add")) >= 0;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      var a = $("[data-forfait-off]", b), c = $("[data-forfait-on]", b);
      if (a) a.hidden = on; if (c) c.hidden = !on;
    });
    $$("[data-lieu]").forEach(function (b) { b.setAttribute("aria-pressed", o.lieux.indexOf(b.getAttribute("data-lieu")) >= 0 ? "true" : "false"); });
    /* Pour chez moi / Pour mon entreprise / Les deux : posé sur <html>, lu par la feuille de style */
    doc.setAttribute("data-public", o.public);
    $$("[data-public-set]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-public-set") === o.public ? "true" : "false"); });
    var html = renduF(o);
    $$("[data-forfait-vue]").forEach(function (v) { v.innerHTML = html; });
    if (!LIEUX) return;
    /* Les solutions qui comptent pour les lieux choisis : marquées, sans cacher les autres */
    var utiles = {};
    o.lieux.forEach(function (id) { if (LIEUX[id]) LIEUX[id].sols.forEach(function (x) { utiles[x.slug] = 1; }); });
    $$("[data-sol]").forEach(function (c) { c.classList.toggle("is-lieu", !!utiles[c.getAttribute("data-sol")]); });
    $$("[data-sols]").forEach(function (g) { g.classList.toggle("has-lieu", o.lieux.length > 0); });
    /* Votre écosystème (page L'offre) : les lieux reliés, le principal en premier, un cerveau chacun. */
    $$("[data-lieux-res]").forEach(function (res) {
      var ids = o.lieux.filter(function (id) { return LIEUX[id]; });
      if (!ids.length) { res.hidden = true; res.innerHTML = ""; res.__html = ""; return; }
      res.hidden = false;
      var c = cerveaux(o), prin = c.principal;
      if (prin) ids = [prin].concat(ids.filter(function (id) { return id !== prin; }));
      var nHub = ids.filter(function (id) { return c.hub[id]; }).length;
      function cerveau(id) { var l = LIEUX[id], h = c.hub[id]; return (h && REF.hubs[h] ? REF.hubs[h].n : "") + (l.boitier ? (h ? " + " : "") + l.boitier : ""); }
      var noeuds = ids.map(function (id) {
        var l = LIEUX[id], role;
        if (id === prin) role = "Lieu principal · " + cerveau(id);
        else if (c.hub[id]) role = cerveau(id) + " · relié au principal";
        else role = (l.boitier || "Un petit boîtier") + " · rien d’autre à bord";
        return '<li class="eco-n' + (id === prin ? " is-prin" : "") + '"><button type="button" class="eco-x" data-lieu="' + id + '" aria-label="Retirer ' + echap(l.nom) + '">×</button>' +
          '<img src="/media/forfait/lieu-' + id + '.webp" alt="" loading="lazy" decoding="async"><b>' + echap(l.nom) + "</b><span>" + echap(role) + "</span></li>";
      }).join("");
      var pourquoi = ids.map(function (id) {
        var l = LIEUX[id];
        return '<article class="lx-r"><h3>' + echap(l.nom) + '</h3><p class="lx-r-h"><b>' + echap(cerveau(id)) + "</b> " + echap(l.raison) + "</p><ul>" +
          l.sols.map(function (x) { return '<li><a href="/solutions/' + x.slug + '/">' + echap(x.nom) + "</a><span>" + echap(x.raison) + "</span></li>"; }).join("") +
          '</ul><p class="lx-r-a"><a href="' + l.demo + '">Voir la démonstration <i aria-hidden="true">→</i></a></p></article>';
      }).join("");
      var html = '<div class="eco"><div class="eco-t"><h3>Votre écosystème.</h3><p>' +
        (c.niveau && nHub ? "Niveau " + nomNiveau(c.niveau) + " · " : "") + ids.length + (ids.length > 1 ? " lieux" : " lieu") + " · une seule app</p></div>" +
        '<ol class="eco-l">' + noeuds + '<li class="eco-n eco-plus"><a href="#' + echap((res.closest("[data-lieux]") || {}).id || "") + '"><i aria-hidden="true">+</i><b>Ajouter un lieu</b><span>Chalet, VR, bureau, véhicule…</span></a></li></ol>' +
        '<p class="eco-note">' + (nHub > 1 && c.niveau === "base" ? "Au niveau Base, chaque lieu veille seul. Pour les relier entre eux, choisissez le niveau Signature ou Platinum."
          : nHub > 1 ? "Vos lieux se parlent par un lien privé et chiffré. Les plus petits s’appuient sur l’intelligence du principal. Si le lien tombe, chacun continue seul : règles, alertes, enregistrements."
          : nHub ? "Un cerveau par lieu, choisi par JARVIS selon la taille du lieu et votre niveau." : "Un véhicule ne reçoit qu’un boîtier : il parle à votre application, et à votre JARVIS si vous en avez un.") + "</p>" +
        '<details class="eco-d"><summary>Pourquoi ce cerveau, lieu par lieu</summary><div class="eco-cartes">' + pourquoi + "</div></details></div>";
      if (res.__html !== html) { res.innerHTML = html; res.__html = html; }   /* redessiné seulement s'il a changé : pas de clignotement */
    });
  }

  /* Les gestes : chacun change la clé, prévient la page (événement « jarvis:forfait »), puis tout se redessine. */
  function previent(d) { document.dispatchEvent(new CustomEvent("jarvis:forfait", { detail: d })); }
  function basculeLieu(id) {
    var f = lireF(), j = f.lieux.indexOf(id), r = REF.lieux[id];
    if (j >= 0) f.lieux.splice(j, 1); else f.lieux.push(id);
    /* Un lieu d'entreprise choisi côté particulier (ou l'inverse) : le choix devient « Les deux ». */
    if (j < 0 && r) {
      if (r.p === "entreprise" && f.public === "moi") f.public = f.lieux.length > 1 ? "deux" : "entreprise";
      if (r.p === "particulier" && f.public === "entreprise") f.public = "deux";
    }
    if (!f.manuel) f.hub = hubDe(f);
    ecrireF(f); previent({ lieu: id, ajoute: j < 0 });
  }
  function basculeSol(slug) {
    var o = lireF(), i = o.sols.indexOf(slug);
    if (i >= 0) o.sols.splice(i, 1); else o.sols.push(slug);
    ecrireF(o); previent({ sol: slug, ajoute: i < 0 });
    return i < 0;
  }

  /* Le tiroir « Mon forfait » */
  var tiroir = null, retour = null;
  function ouvreF() {
    if (!tiroir) {
      tiroir = document.createElement("div"); tiroir.className = "fo-tiroir"; tiroir.hidden = true;
      tiroir.innerHTML = '<div class="fo-fond" data-fo-close></div><aside class="fo-panneau" role="dialog" aria-modal="true" aria-label="Mon forfait">' +
        '<header class="fo-tete"><h2>Mon forfait</h2><button type="button" class="fo-x" data-fo-close aria-label="Fermer">×</button></header>' +
        '<div class="fo-corps" data-forfait-vue></div></aside>';
      document.body.appendChild(tiroir); majF();
    }
    retour = document.activeElement; tiroir.hidden = false; doc.classList.add("fo-lock");
    requestAnimationFrame(function () { requestAnimationFrame(function () { tiroir.classList.add("is-on"); }); });
    var x = $(".fo-x", tiroir); if (x) x.focus();
  }
  function fermeF() {
    if (!tiroir || tiroir.hidden) return;
    tiroir.classList.remove("is-on"); doc.classList.remove("fo-lock");
    setTimeout(function () { tiroir.hidden = true; }, 460);
    if (retour && retour.focus) retour.focus();
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") fermeF(); });

  document.addEventListener("click", function (e) {
    var t = e.target; if (!t.closest) return;
    var ouv = t.closest("[data-forfait], [data-cart-open]");
    if (ouv) { if (ouv.hasAttribute("data-cart-open") || lignesF(lireF()).n) { e.preventDefault(); ouvreF(); } return; }
    if (t.closest("[data-fo-close]")) { fermeF(); return; }
    if (t.closest("[data-fo-suite]")) { fermeF(); return; }
    var a = t.closest("[data-forfait-add]");
    if (a) { if (basculeSol(a.getAttribute("data-forfait-add"))) ouvreF(); return; }
    var pb = t.closest("[data-public-set]");
    if (pb) {
      var g = lireF(); g.public = pb.getAttribute("data-public-set");
      /* Côté particulier, les lieux d'entreprise déjà choisis sortent de la sélection (ils restent choisissables). */
      if (g.public === "moi") g.lieux = g.lieux.filter(function (x) { return !REF.lieux[x] || REF.lieux[x].p !== "entreprise"; });
      if (g.public === "entreprise") g.lieux = g.lieux.filter(function (x) { return !REF.lieux[x] || REF.lieux[x].p !== "particulier"; });
      if (!g.manuel) g.hub = hubDe(g);
      ecrireF(g); previent({ public: g.public });
      return;
    }
    var b = t.closest("[data-lieu]");
    if (b) { basculeLieu(b.getAttribute("data-lieu")); return; }
    var C = window.JarvisCatalogue, o;
    var rm = t.closest("[data-fo-rm]");
    if (rm) {
      var k = rm.getAttribute("data-fo-rm").split(":"), id = k.slice(1).join(":");
      if (k[0] === "lieu") basculeLieu(id);
      else if (k[0] === "sol") basculeSol(id);
      else if (k[0] === "hub") { if (C) C.retire("hub"); else { o = lireF(); o.manuel = false; o.hub = hubDe(o); ecrireF(o); } }
      else if (C) C.retire(id);
      else {   /* hors de /offre/ : le matériel se retire ici, et l'état du formulaire suit */
        o = lireF(); o.autres = o.autres.filter(function (x) { return x.id !== id; });
        if (o.etat && o.etat.q) delete o.etat.q[id];
        ecrireF(o);
      }
      return;
    }
    var q = t.closest("[data-fo-q]");
    if (q) {
      var p = q.getAttribute("data-fo-q").split(":"), d = +p[p.length - 1], qid = p.slice(0, -1).join(":");
      if (C) C.qte(qid, d);
      else {
        o = lireF();
        o.autres.forEach(function (x) { if (x.id === qid) x.q = Math.max(0, (x.q || 0) + d); });
        o.autres = o.autres.filter(function (x) { return x.q > 0 || x.k !== "mat"; });
        if (o.etat && o.etat.q) { var v = Math.max(0, (o.etat.q[qid] || 0) + d); if (v) o.etat.q[qid] = v; else delete o.etat.q[qid]; }
        ecrireF(o);
      }
      return;
    }
    if (t.closest("[data-fo-vider]")) {
      if (C) C.vider();
      else { o = lireF(); ecrireF({ lieux: [], sols: [], hub: "", manuel: false, public: o.public, separee: false, autres: [], etat: null }); previent({ vide: true }); }
    }
  });
  document.addEventListener("change", function (e) {
    if (e.target.matches && e.target.matches("[data-fo-sep]")) { var o = lireF(); o.separee = e.target.checked; ecrireF(o); }
  });
  window.JarvisForfait = { lire: lireF, ecrire: ecrireF, maj: majF, ouvre: ouvreF, hubDe: hubDe, cerveaux: cerveaux };
  majF();

  /* ---------- Les cadres de démonstration tiennent dans la fenêtre ----------
     Scènes fixes (page L'appareil) : réduites d'un seul tenant si elles sont plus hautes que la fenêtre moins la barre. */
  var cadres = $$(".hb-frame");
  function tient() {
    if (window.innerWidth <= 900) { cadres.forEach(function (c) { c.style.zoom = ""; }); return; }
    cadres.forEach(function (c) {
      c.style.zoom = "";
      var h = c.offsetHeight, max = window.innerHeight - 96;
      if (h > max) { c.style.zoom = (max / h).toFixed(4); c.style.marginLeft = "auto"; c.style.marginRight = "auto"; }
    });
  }
  if (cadres.length) { tient(); window.addEventListener("resize", tient); window.addEventListener("load", tient); }
})();
