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

  /* ---------- Mon forfait : il se bâtit en chemin ----------
     Une seule clé (« jarvis-forfait ») partagée avec le configurateur (/catalogue/) : les lieux choisis,
     le Hub conseillé, les solutions ajoutées et le nombre de lignes. Rien ne quitte le navigateur. */
  var CLE_F = "jarvis-forfait", RANG = { base: 1, signature: 2, platinum: 3 };
  function lireF() {
    var o = {};
    try { o = JSON.parse(localStorage.getItem(CLE_F) || "{}") || {}; } catch (e) { o = {}; }
    return { lieux: o.lieux || [], sols: o.sols || [], hub: o.hub || "", manuel: !!o.manuel, n: o.n || 0 };
  }
  function ecrireF(o) { try { localStorage.setItem(CLE_F, JSON.stringify(o)); } catch (e) {} majF(); }
  function compteF(o) { return o.n || (o.sols.length + (o.hub ? 1 : 0)); }
  var LIEUX = null, boiteL = $("[data-lieux-data]");
  if (boiteL) { try { LIEUX = JSON.parse(boiteL.textContent); } catch (e) { LIEUX = null; } }
  function echap(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function majF() {
    var o = lireF(), n = compteF(o);
    $$("[data-forfait-n]").forEach(function (b) { b.hidden = !n; b.textContent = n ? " · " + n : ""; });
    $$("[data-forfait-l]").forEach(function (l) {
      if (!l.getAttribute("data-vide")) l.setAttribute("data-vide", l.textContent);
      l.textContent = n ? l.getAttribute("data-plein") : l.getAttribute("data-vide");
    });
    $$("[data-forfait-add]").forEach(function (b) {
      var on = o.sols.indexOf(b.getAttribute("data-forfait-add")) >= 0;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      var a = $("[data-forfait-off]", b), c = $("[data-forfait-on]", b);
      if (a) a.hidden = on; if (c) c.hidden = !on;
    });
    $$("[data-lieu]").forEach(function (b) { b.setAttribute("aria-pressed", o.lieux.indexOf(b.getAttribute("data-lieu")) >= 0 ? "true" : "false"); });
    if (!LIEUX) return;
    /* Les solutions qui comptent pour les lieux choisis : mises en avant, sans cacher les autres */
    var utiles = {};
    o.lieux.forEach(function (id) { if (LIEUX[id]) LIEUX[id].sols.forEach(function (x) { utiles[x.slug] = 1; }); });
    $$("[data-sol]").forEach(function (c) { c.classList.toggle("is-lieu", !!utiles[c.getAttribute("data-sol")]); });
    $$("[data-sols]").forEach(function (g) { g.classList.toggle("has-lieu", o.lieux.length > 0); });
    $$("[data-lieux-res]").forEach(function (res) {
      if (!o.lieux.length) { res.hidden = true; res.innerHTML = ""; return; }
      res.hidden = false;
      res.innerHTML = o.lieux.filter(function (id) { return LIEUX[id]; }).map(function (id) {
        var l = LIEUX[id];
        var quoi = (l.hubNom ? l.hubNom : "") + (l.boitier ? (l.hubNom ? " + " : "") + l.boitier : "");
        return '<article class="lx-r"><h3>' + echap(l.nom) + '</h3><p class="lx-r-h"><b>' + echap(quoi) + "</b> " + echap(l.raison) + "</p><ul>" +
          l.sols.map(function (x) { return '<li><a href="/solutions/' + x.slug + '/">' + echap(x.nom) + "</a><span>" + echap(x.raison) + "</span></li>"; }).join("") +
          '</ul><p class="lx-r-a"><a href="' + l.demo + '">Voir la démonstration <i aria-hidden="true">→</i></a></p></article>';
      }).join("") + (/^\/catalogue\//.test(location.pathname) ? "" : '<p class="lx-go"><a class="pill" href="/catalogue/">Composer mon forfait</a></p>');
    });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-forfait-add]");
    if (a) {
      var o = lireF(), s = a.getAttribute("data-forfait-add"), i = o.sols.indexOf(s);
      if (i >= 0) o.sols.splice(i, 1); else o.sols.push(s);
      o.n = 0; ecrireF(o);
      document.dispatchEvent(new CustomEvent("jarvis:forfait", { detail: { sol: s, ajoute: i < 0 } }));
      return;
    }
    var b = e.target.closest && e.target.closest("[data-lieu]");
    if (b && LIEUX) {
      var f = lireF(), id = b.getAttribute("data-lieu"), j = f.lieux.indexOf(id);
      if (j >= 0) f.lieux.splice(j, 1); else f.lieux.push(id);
      if (!f.manuel) {
        f.hub = "";
        f.lieux.forEach(function (x) { var h = LIEUX[x] && LIEUX[x].hub; if (h && (RANG[h] || 0) > (RANG[f.hub] || 0)) f.hub = h; });
      }
      f.n = 0; ecrireF(f);
      document.dispatchEvent(new CustomEvent("jarvis:forfait", { detail: { lieu: id, ajoute: j < 0 } }));
    }
  });
  window.JarvisForfait = { lire: lireF, ecrire: ecrireF, maj: majF };
  majF();

  /* ---------- Les cadres de démonstration tiennent dans la fenêtre ----------
     Scènes fixes (Hub) : réduites d'un seul tenant si elles sont plus hautes que la fenêtre moins la barre. */
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
