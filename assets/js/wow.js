/* JARVIS — moteur « WOW » (refonte novembre 2026)
   Règle d'or : rien ne dépend de ce script pour être visible. Les effets ne
   s'activent que sous html.fx, et tout filet de sécurité ramène le contenu.
   Sections : modes · barre · menu · sélecteurs · compteur de visites ·
   console en direct · formulaire · effets de défilement · micro-animations. */
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
      new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" })
        .formatToParts(d).forEach(function (p) { out[p.type] = p.value; });
    } catch (e) {
      out = { hour: String(d.getHours()).padStart(2, "0"), minute: String(d.getMinutes()).padStart(2, "0"), second: String(d.getSeconds()).padStart(2, "0") };
    }
    return out;
  }
  function hm(d) { var p = partsInTz(d); return +p.hour + " h " + p.minute; }
  function hms(d) { var p = partsInTz(d); return p.hour + ":" + p.minute + ":" + p.second; }
  function hourOnly(d) { return +partsInTz(d).hour + " h"; }
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
  if (visitTargets.length) {
    loadVisits().then(function (v) {
      var txt = fmtInt(v);
      $$('[data-live="visits"]').forEach(function (el) { el._odo = txt; if (el._seen) setOdo(el, txt); });
      setText("visits-short", txt + " visites");
      $$('[data-live="visits-foot"]').forEach(function (el) { el.textContent = txt; el.closest(".foot-count").hidden = false; });
    }).catch(function () {
      setText("visits-short", "Visites —");
      $$('[data-live="visits"]').forEach(function (el) { el.textContent = "—"; });
    });
  }

  /* ---------- JARVIS en direct : vraies données, décisions simulées ---------- */
  var liveRoot = $("[data-live-root]");
  var livePill = $("[data-live-pill]");
  if (liveRoot || livePill) {
    var EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/qc-22?f=json&lang=fr";
    var val = function (o) {
      if (o == null) return undefined;
      var v = o.value !== undefined ? o.value : o;
      if (v && typeof v === "object") v = v.fr !== undefined ? v.fr : v.en;
      return v;
    };
    var txt = function (o) {
      if (o == null) return "";
      if (typeof o === "string") return o;
      if (o.fr !== undefined) return o.fr;
      if (o.value !== undefined) return txt(o.value);
      return o.en || "";
    };
    var num = function (o) { var n = parseFloat(val(o)); return isFinite(n) ? n : null; };

    var journalEl = liveRoot && $('[data-live="journal"]', liveRoot);
    var queue = [], typing = false;
    var log = function (text) {
      if (!journalEl) return;
      queue.push(text);
      if (!typing) nextLine();
    };
    var nextLine = function () {
      var text = queue.shift();
      if (!text) { typing = false; return; }
      typing = true;
      var li = document.createElement("li");
      var t = document.createElement("time");
      t.textContent = hms(new Date());
      var s = document.createElement("span");
      li.appendChild(t);
      li.appendChild(s);
      journalEl.appendChild(li);
      while (journalEl.children.length > 5) journalEl.removeChild(journalEl.firstChild);
      if (reduce) { s.textContent = text; nextLine(); return; }
      li.classList.add("typing");
      var i = 0;
      (function type() {
        i += 2;
        s.textContent = text.slice(0, i);
        if (i < text.length) setTimeout(type, 16);
        else { li.classList.remove("typing"); setTimeout(nextLine, 260); }
      })();
    };

    var setState = function (ok, label) {
      $$('[data-live="state"]').forEach(function (el) {
        el.classList.toggle("is-off", !ok);
        el.innerHTML = '<i class="dot' + (ok ? "" : " is-off") + '" aria-hidden="true"></i>' + label;
      });
      if (livePill) $(".dot", livePill).classList.toggle("is-off", !ok);
    };

    /* Horloge de la console */
    if (liveRoot) {
      var tick = function () { setText("clock", hms(new Date()), liveRoot); };
      tick();
      setInterval(tick, 1000);
    }

    /* Arc du soleil (ou de la lune la nuit) */
    var drawSun = function (now, rise, set) {
      if (!liveRoot) return;
      var dot = $('[data-live="sun-dot"]', liveRoot), arc = $('[data-live="sun-arc"]', liveRoot);
      if (!dot || !arc) return;
      var day = now >= rise && now <= set, f, label;
      if (day) {
        f = (now - rise) / (set - rise);
        label = "Jour · " + Math.round(f * 100) + " %";
      } else {
        var start = now > set ? set : new Date(set.getTime() - 864e5);
        var end = now > set ? new Date(rise.getTime() + 864e5) : rise;
        f = (now - start) / (end - start);
        label = "Nuit · lever dans " + Math.max(0, Math.round((end - now) / 36e5 * 10) / 10).toString().replace(".", ",") + " h";
      }
      f = c01(f);
      var x = 150 - 130 * Math.cos(Math.PI * f), y = 105 - 95 * Math.sin(Math.PI * f);
      dot.classList.toggle("is-moon", !day);
      arc.style.stroke = day ? "" : "#aeb8c8";
      var len = arc.getTotalLength ? arc.getTotalLength() : 360;
      arc.style.strokeDasharray = len + " " + len;
      arc.style.strokeDashoffset = len;
      arc.getBoundingClientRect();
      arc.style.transition = reduce ? "none" : "stroke-dashoffset 1.6s cubic-bezier(.16,1,.3,1)";
      arc.style.strokeDashoffset = len * (1 - f);
      dot.setAttribute("cx", x.toFixed(1));
      dot.setAttribute("cy", y.toFixed(1));
      setText("sun-state", label, liveRoot);
    };

    /* Les règles de JARVIS, évaluées sur les vraies conditions */
    var buildRules = function (d) {
      var rules = [];
      var now = d.now, night = d.rise && d.set ? (now < d.rise || now > d.set) : null;
      if (d.rise && d.set) {
        var lightsOn = new Date(d.set.getTime() - 15 * 60000);
        if (night) {
          rules.push({ kind: "auto", cat: "Éclairage", title: "Éclairage extérieur en veilleuse (20 %)",
            why: "Il fait nuit depuis " + hm(d.set) + ". Retour à 0 % au lever du soleil, à " + hm(d.rise) + ".", st: "Automatique" });
        } else if (d.set - now < 90 * 60000) {
          rules.push({ kind: "auto", cat: "Éclairage", title: "Allumer l’éclairage extérieur à " + hm(lightsOn),
            why: "Le soleil se couche à " + hm(d.set) + ". La règle est permise : elle s’applique seule.", st: "Automatique" });
        } else {
          rules.push({ kind: "info", cat: "Éclairage", title: "Éclairage extérieur éteint",
            why: "Lumière du jour jusqu’à " + hm(d.set) + ". Allumage prévu à " + hm(lightsOn) + ".", st: "Rien à faire" });
        }
      }
      if (d.temp !== null) {
        var feel = d.feels !== null ? d.feels : d.temp;
        if (feel <= -5) {
          rules.push({ kind: "ask", cat: "Confort", title: "Préchauffer le véhicule à 7 h 15",
            why: "Ressenti de " + Math.round(feel) + " °C. Départ habituel à 7 h 30 (exemple).", st: "Votre accord" });
        } else if (d.temp >= 26) {
          rules.push({ kind: "ask", cat: "Confort", title: "Fermer les stores côté sud",
            why: "Il fait " + Math.round(d.temp) + " °C dehors. Garder la fraîcheur sans climatiser plus.", st: "Votre accord" });
        } else if (d.temp < 14) {
          rules.push({ kind: "auto", cat: "Confort", title: night ? "Chauffage de nuit : 18 °C dans les chambres" : "Garder 21 °C dans les pièces occupées",
            why: "Extérieur " + Math.round(d.temp) + " °C" + (d.humidity !== null ? ", humidité " + Math.round(d.humidity) + " %" : "") + ".", st: "Automatique" });
        } else {
          rules.push({ kind: "info", cat: "Confort", title: "Chauffage au minimum",
            why: "Extérieur " + Math.round(d.temp) + " °C : aucune correction nécessaire.", st: "Rien à faire" });
        }
      }
      if (night !== null) {
        rules.push(night
          ? { kind: "auto", cat: "Sécurité", title: "Mode nuit : portes verrouillées, caméras en détection",
              why: "Les événements sont regroupés en une chronologie au lieu de dix notifications.", st: "Automatique" }
          : { kind: "info", cat: "Sécurité", title: "Mode jour : notifications pour les inconnus seulement",
              why: "Les passages connus restent au journal, sans vous déranger.", st: "Actif" });
      }
      var wet = null;
      (d.hours || []).forEach(function (h) { if (h.lop !== null && h.lop >= 60 && !wet) wet = h; });
      if (d.warnings.length) {
        rules.push({ kind: "ask", cat: "Météo", title: "Prévenir la famille de l’avertissement en cours",
          why: d.warnings[0], st: "Votre accord" });
      } else if (d.gust !== null && d.gust >= 50) {
        rules.push({ kind: "ask", cat: "Météo", title: "Rentrer l’auvent et le mobilier extérieur",
          why: "Rafales de " + Math.round(d.gust) + " km/h mesurées.", st: "Votre accord" });
      } else if (wet) {
        rules.push({ kind: "ask", cat: "Météo", title: wet.temp !== null && wet.temp <= 1 ? "Déglacer l’entrée avant " + hourOnly(wet.time) : "Rentrer le mobilier extérieur avant " + hourOnly(wet.time),
          why: "Probabilité de précipitations de " + wet.lop + " % vers " + hourOnly(wet.time) + ".", st: "Votre accord" });
      } else {
        rules.push({ kind: "info", cat: "Météo", title: "Aucune action météo nécessaire",
          why: "Pas de précipitations significatives prévues dans les prochaines heures.", st: "Rien à faire" });
      }
      return rules.slice(0, 4);
    };

    var renderRules = function (rules) {
      var ul = liveRoot && $('[data-live="rules"]', liveRoot);
      if (!ul) return;
      ul.innerHTML = "";
      rules.forEach(function (r, i) {
        var li = document.createElement("li");
        li.className = "rule is-" + r.kind;
        li.style.setProperty("--i", i);
        li.innerHTML = '<div class="rule-top"><small></small><span class="st"></span></div><b></b><p></p>';
        $("small", li).textContent = r.cat;
        $(".st", li).textContent = r.st;
        $("b", li).textContent = r.title;
        $("p", li).textContent = r.why;
        if (r.kind === "ask") {
          var acts = document.createElement("div");
          acts.className = "rule-acts";
          acts.innerHTML = '<button type="button" data-act="ok">Approuver</button><button type="button" data-act="no">Ignorer</button>';
          acts.addEventListener("click", function (e) {
            var b = e.target.closest("button");
            if (!b) return;
            var ok = b.getAttribute("data-act") === "ok";
            li.className = "rule " + (ok ? "is-done" : "is-skip");
            $(".st", li).textContent = ok ? "Approuvé · simulé" : "Ignoré";
            acts.remove();
            log((ok ? "Vous avez approuvé : " : "Vous avez ignoré : ") + r.title.toLowerCase() + " — simulation, aucun appareil commandé");
          });
          li.appendChild(acts);
        }
        ul.appendChild(li);
      });
    };

    var renderHours = function (hours) {
      var box = liveRoot && $('[data-live="hours"]', liveRoot);
      if (!box || !hours.length) return;
      var temps = hours.map(function (h) { return h.temp; }).filter(function (t) { return t !== null; });
      var lo = Math.min.apply(null, temps), hi = Math.max.apply(null, temps);
      box.innerHTML = "";
      hours.forEach(function (h) {
        var el = document.createElement("div");
        el.className = "hour";
        var k = hi === lo ? .6 : (h.temp - lo) / (hi - lo);
        el.innerHTML = '<b></b><span class="hbar"></span><span class="t"></span>' + (h.lop >= 30 ? '<span class="rain"></span>' : "");
        $("b", el).textContent = h.temp !== null ? Math.round(h.temp) + "°" : "–";
        $(".t", el).textContent = hourOnly(h.time);
        if (h.lop >= 30) $(".rain", el).textContent = h.lop + " %";
        box.appendChild(el);
        var barEl = $(".hbar", el);
        requestAnimationFrame(function () { requestAnimationFrame(function () { barEl.style.height = Math.round(18 + k * 46) + "px"; }); });
      });
    };

    var shown = false;
    var lastData = null;
    var paint = function (d) {
      lastData = d;
      var tShort = d.temp !== null ? Math.round(d.temp) + " °C" : "—";
      setText("temp-short", tShort);
      setText("temp-hud", d.temp !== null ? Math.round(d.temp) + " °C · " + (d.condition || "").toLowerCase() : "— °C");
      if (!liveRoot) return;
      var tEl = $('[data-live="temp"]', liveRoot);
      if (d.temp !== null) {
        var tv = String(Math.round(d.temp)).replace("-", "−");
        if (tEl._last !== tv) { tEl._last = tv; setOdo(tEl, tv); }
      }
      setText("condition", d.condition || "Conditions actuelles", liveRoot);
      setText("feels", d.feels !== null && Math.round(d.feels) !== Math.round(d.temp)
        ? "Ressenti " + String(Math.round(d.feels)).replace("-", "−") + " °C" : (d.station ? "Observé à : " + d.station : " "), liveRoot);
      setText("wind", d.wind !== null ? Math.round(d.wind) + " km/h " + (d.dir || "") : "—", liveRoot);
      setText("gust", d.gust ? Math.round(d.gust) + " km/h" : "—", liveRoot);
      setText("humidity", d.humidity !== null ? Math.round(d.humidity) + " %" : "—", liveRoot);
      setText("pressure", d.pressure !== null ? String(d.pressure).replace(".", ",") + " kPa" : "—", liveRoot);
      if (d.rise && d.set) {
        setText("sunrise", hm(d.rise), liveRoot);
        setText("sunset", hm(d.set), liveRoot);
        drawSun(d.now, d.rise, d.set);
      }
      renderHours(d.hours);
      var src = $('[data-live="source"]', liveRoot);
      if (src) {
        src.innerHTML = 'Source : Environnement et Changement climatique Canada · <a href="https://meteo.gc.ca/fr/location/index.html?coords=45.63,-72.95" rel="noopener" target="_blank">prévisions de Saint-Hyacinthe</a>' +
          (d.obs ? " · mesure de " + hm(d.obs) : "");
      }
      var rules = buildRules(d);
      renderRules(rules);
      if (!shown) {
        shown = true;
        log("Environnement Canada · " + (d.temp !== null ? Math.round(d.temp) + " °C" : "—") + (d.condition ? ", " + d.condition.toLowerCase() : "") + " · reçu");
        if (d.rise && d.set) log("Soleil · lever " + hm(d.rise) + ", coucher " + hm(d.set));
        var a = rules.filter(function (r) { return r.kind === "auto"; }).length;
        var p = rules.filter(function (r) { return r.kind === "ask"; }).length;
        log(rules.length + " règles évaluées · " + a + " automatique" + (a > 1 ? "s" : "") + ", " + p + " en attente de votre accord");
        log("Démonstration : aucun appareil réel n’est commandé");
      }
    };

    var fail = function () {
      setState(false, "Données indisponibles");
      setText("temp-short", "hors ligne");
      if (!liveRoot) return;
      setText("condition", "Les données en direct ne répondent pas", liveRoot);
      setText("feels", "JARVIS l’affiche honnêtement plutôt que d’inventer.", liveRoot);
      var ul = $('[data-live="rules"]', liveRoot);
      if (ul) ul.innerHTML = '<li class="rule is-info"><div class="rule-top"><small>État</small><span class="st">En attente</span></div><b>Aucune décision sans données fiables</b><p>Les règles reprendront dès que la source répondra.</p></li>';
      if (!shown) log("Source météo injoignable · nouvelle tentative dans 2 minutes");
    };

    var load = function () {
      var cached = session && session.getItem("jarvis-ec");
      var useCache = null;
      if (cached) { try { var c = JSON.parse(cached); if (Date.now() - c.t < 300000) useCache = c.j; } catch (e) {} }
      var got = useCache ? Promise.resolve(useCache) : fetch(EC_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
      return got.then(function (j) {
        if (!useCache && session) { try { session.setItem("jarvis-ec", JSON.stringify({ t: Date.now(), j: j })); } catch (e) {} }
        var p = j.properties || {};
        var cc = p.currentConditions || {};
        var temp = num(cc.temperature);
        /* Ressenti : refroidissement éolien seulement s'il fait froid, humidex s'il fait chaud */
        var wc = num(cc.windChill), hx = num(cc.humidex), feels = null;
        if (temp !== null && wc !== null && temp <= 5 && wc < temp) feels = wc;
        if (temp !== null && hx !== null && temp >= 20 && hx > temp) feels = hx;
        var rs = p.riseSet || {};
        var rise = rs.sunrise ? new Date(txt(rs.sunrise)) : null;
        var set = rs.sunset ? new Date(txt(rs.sunset)) : null;
        var now = new Date();
        var hourly = ((p.hourlyForecastGroup || {}).hourlyForecasts || []).filter(function (h) {
          return new Date(h.timestamp) > now - 3600000;
        }).slice(0, 6).map(function (h) {
          return { time: new Date(h.timestamp), temp: num(h.temperature), lop: num(h.lop) };
        });
        var warnings = (p.warnings || []).map(function (w) {
          return txt(w.description) || txt(w.type) || "Avertissement météo en vigueur.";
        }).filter(Boolean);
        var obs = cc.timestamp ? new Date(txt(cc.timestamp)) : null;
        var d = {
          now: now, temp: temp, feels: feels, condition: txt(cc.condition),
          wind: num((cc.wind || {}).speed), gust: num((cc.wind || {}).gust), dir: val((cc.wind || {}).direction) || "",
          humidity: num(cc.relativeHumidity), pressure: num(cc.pressure),
          station: val(cc.station) || "", rise: rise && !isNaN(rise) ? rise : null, set: set && !isNaN(set) ? set : null,
          hours: hourly, warnings: warnings, obs: obs && !isNaN(obs) ? obs : null
        };
        if (temp === null && !d.condition) throw new Error("vide");
        setState(true, "En direct");
        paint(d);
      }).catch(fail);
    };

    /* Charger au besoin : tout de suite si la console ou la pastille est visible */
    var started = false;
    var start = function () {
      if (started) return;
      started = true;
      load();
      setInterval(function () {
        if (document.hidden) return;
        if (session) session.removeItem("jarvis-ec");
        load();
      }, 600000);
    };
    if (livePill) start();
    if (liveRoot && "IntersectionObserver" in window) {
      var lio = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          start();
          $$('[data-live="visits"]', liveRoot).forEach(function (el) { el._seen = true; if (el._odo) setOdo(el, el._odo); });
          if (lastData && !liveRoot._replayed) {
            liveRoot._replayed = true;
            var tEl = $('[data-live="temp"]', liveRoot);
            if (tEl && tEl._last) setOdo(tEl, tEl._last);
            if (lastData.rise && lastData.set) drawSun(new Date(), lastData.rise, lastData.set);
          }
          lio.unobserve(e.target);
        });
      }, { threshold: .2 });
      lio.observe(liveRoot);
    } else if (liveRoot) {
      start();
      $$('[data-live="visits"]', liveRoot).forEach(function (el) { el._seen = true; });
    }
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

  /* ---------- Vitrine de l'app : onglets automatiques ---------- */
  $$("[data-vitrine]").forEach(function (stage) {
    var root = stage.closest(".vitrine") || document;
    var bar = $(".vit-tabs", root);
    var tabs = $$(".vit-tabs button", root), slides = $$(".vit-slide", stage), caps = $$(".vit-cap", root);
    var sweep = $(".vit-sweep", stage), device = $(".vit-device", stage);
    var n = slides.length, cur = 0, DUR = 7000, timer = null, startedAt = 0, left = DUR, visible = false, hover = false;
    bar.style.setProperty("--dur", DUR + "ms");
    function show(i) {
      if (i === cur) return;
      var prev = slides[cur];
      prev.classList.remove("is-on", "show-hots");
      prev.classList.add("is-out");
      setTimeout(function () { prev.classList.remove("is-out"); }, 1200);
      cur = i;
      slides[i].classList.add("is-on");
      requestAnimationFrame(function () { slides[i].classList.add("show-hots"); });
      tabs.forEach(function (t, k) {
        t.classList.remove("is-on");
        t.setAttribute("aria-selected", k === i ? "true" : "false");
      });
      void tabs[i].offsetWidth;
      tabs[i].classList.add("is-on");
      caps.forEach(function (c, k) { c.classList.toggle("is-on", k === i); });
      if (sweep) { sweep.classList.remove("go"); void sweep.offsetWidth; sweep.classList.add("go"); }
      left = DUR;
      arm();
    }
    function arm() {
      clearTimeout(timer);
      if (reduce || !visible || hover) return;
      startedAt = Date.now();
      timer = setTimeout(function () { show((cur + 1) % n); }, left);
    }
    function pause() {
      if (timer) { clearTimeout(timer); timer = null; left = Math.max(300, left - (Date.now() - startedAt)); }
      bar.classList.add("is-paused");
    }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { show(k); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          var j = (cur + (e.key === "ArrowRight" ? 1 : n - 1)) % n;
          show(j); tabs[j].focus();
        }
      });
    });
    stage.addEventListener("pointerenter", function () { hover = true; pause(); });
    stage.addEventListener("pointerleave", function () {
      hover = false; bar.classList.remove("is-paused"); arm();
      if (device) device.style.transform = "";
    });
    if (finePointer && !reduce && device) {
      stage.addEventListener("pointermove", function (e) {
        var r = stage.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        device.style.transform = "rotateY(" + (x * 4).toFixed(2) + "deg) rotateX(" + (-y * 4).toFixed(2) + "deg)";
      });
    }
    if (reduce) { bar.classList.add("is-manual"); slides[0].classList.add("show-hots"); return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        visible = e.isIntersecting;
        if (visible) {
          stage.classList.add("in");
          if (!slides[cur].classList.contains("show-hots")) setTimeout(function () { slides[cur].classList.add("show-hots"); }, 700);
          bar.classList.remove("is-paused");
          arm();
        } else pause();
      });
    }, { threshold: .35 }).observe(stage);
  });

  if (reduce) return;
  doc.classList.add("fx");

  /* ---------- Héros : lumières et HUD placés sur l'image (object-fit: cover) ---------- */
  var heroBox = $("[data-hero]");
  if (heroBox) {
    var lit = $(".bg img.lit", heroBox), hud = $(".hud", heroBox);
    var LIGHTS = [[58, 47], [74, 50], [35, 78], [27, 63], [88, 50], [55, 12], [50, 55]];
    var map = function (ix, iy) {
      var W = heroBox.clientWidth, H = heroBox.clientHeight, R = 1916 / 821;
      var w = Math.max(W, H * R), h = w / R;
      return [((ix / 100) * w - (w - W) / 2) / W * 100, ((iy / 100) * h - (h - H) / 2) / H * 100];
    };
    var svgNS = "http://www.w3.org/2000/svg";
    var svg = hud ? document.createElementNS(svgNS, "svg") : null;
    var tags = hud ? $$(".hud-tag", hud) : [];
    var marks = [];
    if (svg) {
      svg.setAttribute("viewBox", "0 0 100 100");
      svg.setAttribute("preserveAspectRatio", "none");
      hud.insertBefore(svg, hud.firstChild);
      tags.forEach(function (t, k) {
        var ln = document.createElementNS(svgNS, "line");
        var pt = document.createElement("i");
        pt.className = "hud-pt";
        t.style.setProperty("--k", k);
        ln.style.setProperty("--k", k);
        pt.style.setProperty("--k", k);
        svg.appendChild(ln);
        hud.appendChild(pt);
        marks.push({ tag: t, ln: ln, pt: pt });
      });
    }
    var place = function () {
      if (lit) LIGHTS.forEach(function (l, i) {
        var m = map(l[0], l[1]);
        lit.style.setProperty("--m" + (i + 1), m[0].toFixed(1) + "% " + m[1].toFixed(1) + "%");
      });
      var narrow = heroBox.clientWidth < 880;
      marks.forEach(function (m) {
        var cs = m.tag.style;
        var p = map(parseFloat(cs.getPropertyValue("--px")), parseFloat(cs.getPropertyValue("--py")));
        var tx = parseFloat(cs.getPropertyValue("--x")), ty = parseFloat(cs.getPropertyValue("--y"));
        var off = p[0] < 4 || p[0] > 96 || (narrow && !m.tag.classList.contains("t-out") && !m.tag.classList.contains("t-salon"));
        m.tag.classList.toggle("is-off", off);
        m.pt.style.display = m.ln.style.display = off ? "none" : "";
        m.pt.style.left = p[0] + "%";
        m.pt.style.top = p[1] + "%";
        m.ln.setAttribute("x1", tx); m.ln.setAttribute("y1", ty);
        m.ln.setAttribute("x2", p[0].toFixed(2)); m.ln.setAttribute("y2", p[1].toFixed(2));
      });
    };
    place();
    addEventListener("resize", place);
    if (hud) setTimeout(function () { hud.classList.add("on"); }, 3600);
    /* Salutation selon l'heure à Saint-Hyacinthe */
    var greet = $("[data-greet]", heroBox);
    if (greet) {
      var hr = +partsInTz(new Date()).hour;
      greet.textContent = hr < 5 ? "Bonne nuit · la maison veille" : hr < 12 ? "Bonjour · la maison s’éveille"
        : hr < 18 ? "Bon après-midi · la maison s’adapte" : hr < 22 ? "Bonsoir · la maison s’allume" : "Bonne nuit · la maison veille";
    }
  }

  function prog(el) {
    var r = el.getBoundingClientRect();
    return c01(-r.top / Math.max(1, r.height - innerHeight));
  }

  /* Filet de sécurité : tout redevient visible (impression) */
  function defuse() {
    doc.classList.remove("fx");
    $$(".scene .t1,.scene .t2,.scene .t3,.scene img,.hero .bg,.hero .bg img")
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

  /* Manifeste : chaque mot devient un span qui s'allume */
  var mani = $(".mani");
  var words = [];
  if (mani) {
    var mp = $("p", mani);
    mp.innerHTML = mp.textContent.trim().split(/\s+/).map(function (w) {
      return "<span>" + w + "</span>";
    }).join(" ");
    words = $$("span", mp);
  }

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

  /* Scènes produit (autres pages) : jamais d'image figée à moitié */
  var scenes = $$(".scene").map(function (s) {
    return { el: s, img: $("img", s), t1: $(".t1", s), t2: $(".t2", s), t3: $(".t3", s) };
  });

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
    if (words.length) {
      var mpg = prog(mani), lit = Math.floor(mpg * words.length * 1.3);
      for (var i = 0; i < words.length; i++) words[i].classList.toggle("lit", i < lit);
    }
    scenes.forEach(function (s) {
      if (!s.img) return;
      var r = s.el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      var enter = c01((vh - r.top) / vh), exit = c01(r.bottom / vh), hp = prog(s.el);
      var vis = Math.min(c01((enter - .8) / .18), c01((exit - .8) / .18));
      s.img.style.opacity = vis.toFixed(3);
      s.img.style.transform = "perspective(1400px) rotateX(" + ((1 - easeOut(enter)) * 16).toFixed(2) + "deg) scale(" + (.88 + Math.min(hp, .5) * .24).toFixed(4) + ")";
      var fade = c01((exit - .8) / .18);
      if (s.t1) s.t1.style.opacity = Math.min(c01((hp - .2) * 4), fade);
      if (s.t2) s.t2.style.opacity = Math.min(c01((hp - .35) * 4), fade);
      if (s.t3) s.t3.style.opacity = Math.min(c01((hp - .5) * 4), fade);
    });
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

  /* SMIL du schéma : en pause hors écran pour ménager la batterie */
  $$(".flow-svg").forEach(function (svg) {
    if (!svg.pauseAnimations) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) svg.unpauseAnimations(); else svg.pauseAnimations(); });
    }).observe(svg);
  });

  if (!finePointer) return;

  /* Halo qui suit le pointeur sur les cartes */
  $$(".card, .plan, .stat, .steps li").forEach(function (el) {
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
