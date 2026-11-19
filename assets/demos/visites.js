/* Page privée « Visites du site » (/admin/visites/).
   Lit GET /visits/log du service du site avec le jeton collé par James (Authorization: Bearer).
   Le journal arrive par tranches de 200 (« Charger plus » suit le curseur du service). Les chiffres
   viennent des compteurs par jour du service, pas des visites chargées. Le relevé d'avant la mise en
   service (« archives ») vient aussi du service : il n'est jamais dans le dépôt.
   Le jeton reste dans sessionStorage (cet onglet seulement) et ne part que vers le service du site.
   Toutes les valeurs venant des visiteurs sont écrites en texte (textContent), jamais en HTML. */
(function () {
  "use strict";
  var root = document.querySelector("[data-av-root]");
  if (!root) return;
  var API = (document.documentElement.getAttribute("data-api") || "").replace(/\/$/, "");
  var KEY = "jarvis-visites-jeton";
  var TZ = "America/Toronto";
  var DAY = 86400000;
  var SVG = "http://www.w3.org/2000/svg";
  var all = [];          // visites chargées, les plus récentes d'abord
  var cursor = null;     // suite du journal, donnée par le service (null : tout est chargé)
  var stats = null;      // { jours: [{jour, visites, pages}], totaux: {visites, pages} }
  var keep = "";         // durée de conservation annoncée par le service
  var busy = false;
  var LIMIT = 200;
  var chats = [];        // échanges avec JARVIS (GET /chats), les plus récents d'abord
  var cCursor = null, cBusy = false, cState = "";
  var tab = "visiteurs";
  /* Robots : ceux que le service a reconnus, et les centres de données (pas des gens chez eux). */
  var HOSTS = /anthropic|amazon|aws|google cloud|google llc|microsoft|azure|digitalocean|ovh|hetzner|linode|akamai|gthost|datacamp|m247|leaseweb|vultr|contabo|oracle|alibaba|tencent|scaleway|cloudflare/i;
  function isBot(v) { return v.robot === true || v.appareil === "Robot" || HOSTS.test(v.fournisseur || ""); }

  function $(k) { return root.querySelector('[data-av="' + k + '"]'); }
  function store(kind) { try { return window[kind]; } catch (e) { return null; } }
  var session = store("sessionStorage"), local = store("localStorage");
  function get(s, k) { try { return s ? s.getItem(k) : null; } catch (e) { return null; } }
  function set(s, k, v) { try { if (!s) return; if (v == null) s.removeItem(k); else s.setItem(k, v); } catch (e) {} }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function plural(n, one, many) { return fmt(n) + " " + (n > 1 ? many : one); }

  var regionName = null;
  try { regionName = new Intl.DisplayNames(["fr-CA"], { type: "region" }); } catch (e) {}
  function countryName(cc) {
    if (!cc || cc === "XX" || cc === "T1") return "Pays inconnu";
    try { return (regionName && regionName.of(cc)) || cc; } catch (e) { return cc; }
  }
  function flag(cc) {
    if (!/^[A-Z]{2}$/.test(cc || "") || cc === "XX" || cc === "T1") return "🌐";
    return String.fromCodePoint(127397 + cc.charCodeAt(0), 127397 + cc.charCodeAt(1));
  }
  var timeFmt = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
  var dayFmt = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" });

  /* ---------- Message d'état ---------- */
  function status(text, tone) {
    var el = $("status");
    el.textContent = text;
    el.className = "av-status" + (tone ? " is-" + tone : "");
  }

  /* ---------- « Ne pas compter mes visites » (localStorage jarvis-moi) ---------- */
  var meBtn = $("me");
  function paintMe() {
    var on = get(local, "jarvis-moi") === "1";
    meBtn.classList.toggle("is-on", on);
    meBtn.setAttribute("aria-pressed", on ? "true" : "false");
    meBtn.textContent = on ? "Cet appareil n’est pas compté · le recompter" : "Ne pas compter mes visites sur cet appareil";
  }
  meBtn.addEventListener("click", function () {
    var on = get(local, "jarvis-moi") === "1";
    set(local, "jarvis-moi", on ? null : "1");
    paintMe();
    status(on ? "Cet appareil est de nouveau compté dans les visites." : "C’est noté : vos visites sur cet appareil et ce navigateur ne seront plus comptées.", "ok");
  });
  paintMe();

  /* ---------- Chargement du journal ---------- */
  function token() { return get(session, KEY) || ""; }
  function clock() { return new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, hour: "2-digit", minute: "2-digit" }).format(new Date()); }
  function load(more) {
    if (!API) { status("Le service du site n’est pas configuré (adresse « api » vide dans src/config.py).", "bad"); return; }
    var t = token();
    if (!t) { status("Collez le jeton pour afficher le journal.", ""); return; }
    if (busy || (more && !cursor)) return;
    busy = true;
    $("more").disabled = true;
    status(more ? "Chargement de la suite du journal…" : "Chargement du journal…", "");
    fetch(API + "/visits/log?limit=" + LIMIT + (more ? "&cursor=" + encodeURIComponent(cursor) : ""), { headers: { Authorization: "Bearer " + t }, cache: "no-store" })
      .then(function (r) {
        if (r.status === 401) throw { msg: "Jeton refusé par le service. Vérifiez que c’est bien le jeton LEADS_TOKEN.", tone: "bad", forget: true };
        if (!r.ok) throw { msg: "Le service répond avec une erreur (" + r.status + "). Réessayez dans un moment.", tone: "bad" };
        return r.json();
      })
      .then(function (j) {
        if (!j || !Array.isArray(j.visits)) throw { msg: "Le service répond, mais ne connaît pas encore le journal des visites : le nouveau Worker n’est pas encore déployé sur Cloudflare.", tone: "warn" };
        var got = j.visits.filter(function (v) { return v && v.t; });
        all = more ? all.concat(got) : got;
        all.sort(function (a, b) { return a.t < b.t ? 1 : -1; });
        cursor = typeof j.cursor === "string" && j.cursor ? j.cursor : null;
        if (!more) {
          stats = Array.isArray(j.jours) ? { jours: j.jours, totaux: j.totaux || {} } : null;
          keep = j.conservation_jours ? (j.conservation_jours % 365 === 0 ? (j.conservation_jours / 365 * 12) + " mois" : j.conservation_jours + " jours") : "";
          archive(Array.isArray(j.archives) ? j.archives : []);
        }
        root.classList.add("is-ouvert");
        fillFilters();
        render();
        status("Journal à jour à " + clock() + " · " + plural(all.length, "entrée chargée", "entrées chargées") +
          (cursor ? " · il en reste, « Charger plus » en bas du journal" : " · tout le journal est chargé") +
          (keep ? " · conservation " + keep : "") +
          (stats ? "" : " · le service n’envoie pas encore les compteurs par jour (Worker à mettre à jour) : chiffres tirés des visites chargées") + ".", stats ? "ok" : "warn");
      })
      .catch(function (e) {
        if (e && e.forget) set(session, KEY, null);
        status(e && e.msg ? e.msg : "Le service ne répond pas, ou il n’est pas encore à jour sur Cloudflare (le nouveau Worker doit être déployé).", (e && e.tone) || "bad");
      })
      .then(function () { busy = false; $("more").disabled = false; });
  }

  /* ---------- Conversations avec JARVIS (GET /chats, même jeton) ---------- */
  function loadChats(more) {
    var t = token();
    if (!API || !t || cBusy || (more && !cCursor)) return;
    cBusy = true;
    fetch(API + "/chats?limit=300" + (more ? "&cursor=" + encodeURIComponent(cCursor) : ""), { headers: { Authorization: "Bearer " + t }, cache: "no-store" })
      .then(function (r) {
        if (r.status === 404) throw new Error("Le service ne connaît pas encore les conversations.");
        if (!r.ok) throw new Error("Le service ne répond pas (" + r.status + ").");
        return r.json();
      })
      .then(function (d) {
        if (!d || !Array.isArray(d.echanges)) throw new Error("Le service ne connaît pas encore les conversations.");
        chats = (more ? chats.concat(d.echanges) : d.echanges).filter(function (x) { return x && x.t && x.q; });
        chats.sort(function (a, b) { return a.t < b.t ? 1 : -1; });
        cCursor = typeof d.cursor === "string" && d.cursor ? d.cursor : null;
        cState = "";
      })
      .catch(function (e) { cState = e.message || "Les conversations ne se chargent pas."; })
      .then(function () { cBusy = false; render(); });
  }

  $("form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var input = root.querySelector("#av-jeton");
    var t = input.value.trim();
    input.value = "";
    if (!t) { status("Le champ est vide : collez le jeton.", "warn"); return; }
    set(session, KEY, t);
    load(false); loadChats(false);
  });
  $("refresh").addEventListener("click", function () { load(false); loadChats(false); });
  $("forget").addEventListener("click", function () {
    set(session, KEY, null);
    root.classList.remove("is-ouvert");
    all = []; cursor = null; stats = null; chats = []; cCursor = null; archive([]); fillFilters(); fermeFiche(); render();
    status("Jeton oublié dans cet onglet.", "");
  });
  $("f-pays").addEventListener("change", render);
  $("f-page").addEventListener("change", render);
  $("f-bots").addEventListener("change", render);
  $("f-parle").addEventListener("change", render);
  $("q").addEventListener("input", render);
  $("more").addEventListener("click", function () { load(true); });
  $("c-more").addEventListener("click", function () { loadChats(true); });
  Array.prototype.forEach.call(root.querySelectorAll(".av-tab"), function (b) {
    b.addEventListener("click", function () { montre(b.getAttribute("data-tab")); });
  });
  function montre(t) {
    tab = t;
    Array.prototype.forEach.call(root.querySelectorAll(".av-tab"), function (b) {
      var on = b.getAttribute("data-tab") === t;
      b.classList.toggle("is-on", on); b.setAttribute("aria-selected", on ? "true" : "false");
    });
    Array.prototype.forEach.call(root.querySelectorAll("[data-pane]"), function (p) { p.hidden = p.getAttribute("data-pane") !== t; });
    root.classList.toggle("is-journal", t === "journal");
  }

  /* ---------- Export CSV de ce qui est chargé (fabriqué dans le navigateur, rien n'est envoyé) ---------- */
  function csvCell(v) {
    var s = v == null ? "" : String(v);
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; // jamais lu comme une formule par un tableur
    return '"' + s.replace(/"/g, '""') + '"';
  }
  $("csv").addEventListener("click", function () {
    if (!all.length) { status("Rien à exporter : chargez d’abord le journal.", "warn"); return; }
    var cols = ["t", "type", "pays", "region", "ville", "fuseau", "fournisseur", "asn", "ip", "page", "appareil", "systeme", "navigateur", "ref"];
    var head = ["heure", "type", "pays", "region", "ville", "fuseau", "fournisseur", "asn", "adresse_ip", "page", "appareil", "systeme", "navigateur", "provenance", "robot"];
    var lines = [head.map(csvCell).join(";")];
    all.forEach(function (v) {
      lines.push(cols.map(function (c) { return csvCell(v[c]); }).concat(csvCell(isBot(v) ? "oui" : "non")).join(";"));
    });
    var url = URL.createObjectURL(new Blob(["\ufeff" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" }));
    var a = document.createElement("a");
    a.href = url; a.download = "visites-" + dayFmt.format(new Date()) + ".csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
    status(plural(all.length, "visite exportée", "visites exportées") + " en CSV (ce qui est chargé" + (cursor ? "; le reste du journal ne l’est pas encore" : "") + ").", "ok");
  });

  /* ---------- Filtres ---------- */
  function options(sel, values, label) {
    var keep = sel.value;
    while (sel.options.length > 1) sel.remove(1);
    values.forEach(function (v) {
      var o = document.createElement("option");
      o.value = v[0]; o.textContent = label(v[0]) + " · " + fmt(v[1]);
      sel.appendChild(o);
    });
    sel.value = values.some(function (v) { return v[0] === keep; }) ? keep : "";
  }
  function tally(key) {
    var m = {};
    all.forEach(function (v) { var k = v[key] || ""; m[k] = (m[k] || 0) + 1; });
    return Object.keys(m).map(function (k) { return [k, m[k]]; }).sort(function (a, b) { return b[1] - a[1]; });
  }
  function fillFilters() {
    options($("f-pays"), tally("pays"), function (cc) { return flag(cc) + " " + countryName(cc); });
    options($("f-page"), tally("page"), function (p) { return p || "(page inconnue)"; });
  }

  /* ---------- Chiffres : compteurs par jour du service (heure de Toronto) ---------- */
  function dayKey(ms) { return dayFmt.format(new Date(ms)); }
  function kpis() {
    // Par jour : le compteur du service, ou les visites chargées si elles en montrent plus
    // (jours d'avant les compteurs, ou service pas encore à jour).
    var days = {};
    all.forEach(function (v) {
      if (isBot(v)) return;
      var d = days[dayKey(Date.parse(v.t))] || (days[dayKey(Date.parse(v.t))] = [0, 0]);
      d[1]++; if (v.type !== "page") d[0]++;
    });
    var first = "";
    ((stats && stats.jours) || []).forEach(function (j) {
      if (!j || !/^\d{4}-\d\d-\d\d$/.test(j.jour)) return;
      var d = days[j.jour] || (days[j.jour] = [0, 0]);
      d[0] = Math.max(d[0], +j.visites || 0); d[1] = Math.max(d[1], +j.pages || 0);
      if (!first || j.jour < first) first = j.jour;
    });
    var has = all.length > 0 || Boolean(stats && stats.jours.length), now = Date.now();
    function span(n) {
      var b = [0, 0];
      for (var i = 0; i < n; i++) { var d = days[dayKey(now - i * DAY)]; if (d) { b[0] += d[0]; b[1] += d[1]; } }
      return b;
    }
    function put(k, b, tail) { $(k).textContent = has ? fmt(b[0]) : "—"; $(k + "-p").textContent = has ? plural(b[1], "page vue", "pages vues") + (tail || "") : "pages vues —"; }
    put("k-day", span(1)); put("k-7", span(7)); put("k-30", span(30));
    var tot = stats && stats.totaux, sum = [0, 0];
    Object.keys(days).forEach(function (k) { sum[0] += days[k][0]; sum[1] += days[k][1]; });
    var since = first ? " depuis le " + new Intl.DateTimeFormat("fr-CA", { timeZone: "UTC", day: "numeric", month: "short", year: "numeric" }).format(new Date(first + "T12:00:00Z")) : "";
    put("k-all", tot && tot.visites >= 0 ? [Math.max(+tot.visites || 0, sum[0]), Math.max(+tot.pages || 0, sum[1])] : sum, tot ? since : " (chargées)");
  }

  /* ---------- Cartes : un point par visite ---------- */
  var P = JSON.parse(root.querySelector("[data-proj]").getAttribute("data-proj"));
  function world(lat, lon) {
    var g = P.world, l = ((lon - g.lon0) % 360 + 360) % 360;
    return [l / g.step * g.u + g.u / 2, (g.lat0 - lat) / g.step * g.u + g.u / 2];
  }
  function qc(lat, lon) {
    var q = P.qc, x = (lon - q.lon0) * q.kx, y = (q.lat0 - lat) * q.ky, b = q.box;
    return x >= b[0] && x <= b[0] + b[2] && y >= b[1] && y <= b[1] + b[3] ? [x, y] : null;
  }
  function dot(g, xy, r, fresh, title) {
    var halo = document.createElementNS(SVG, "circle");
    halo.setAttribute("class", "av-pt-halo"); halo.setAttribute("cx", xy[0].toFixed(1)); halo.setAttribute("cy", xy[1].toFixed(1)); halo.setAttribute("r", (r * 2.6).toFixed(1));
    var c = document.createElementNS(SVG, "circle");
    c.setAttribute("class", "av-pt" + (fresh ? " is-new" : "")); c.setAttribute("cx", xy[0].toFixed(1)); c.setAttribute("cy", xy[1].toFixed(1)); c.setAttribute("r", r.toFixed(1));
    var t = document.createElementNS(SVG, "title"); t.textContent = title; c.appendChild(t);
    g.appendChild(halo); g.appendChild(c);
  }
  function maps(list) {
    var gw = root.querySelector('[data-av="world"]'), gq = root.querySelector('[data-av="qc"]');
    gw.textContent = ""; gq.textContent = "";
    // Un point par lieu, grossi selon le nombre de visites; les plus récents par-dessus.
    var places = {}, order = [];
    list.forEach(function (v) {
      if (v.lat == null || v.lon == null) return;
      var k = (+v.lat).toFixed(2) + "," + (+v.lon).toFixed(2);
      if (!places[k]) { places[k] = { lat: +v.lat, lon: +v.lon, n: 0, t: v.t, label: place(v) }; order.push(k); }
      places[k].n++;
    });
    var nw = 0, nq = 0, now = Date.now();
    order.reverse().forEach(function (k) {
      var p = places[k], fresh = now - Date.parse(p.t) < 3600000, title = p.label + " — " + plural(p.n, "visite", "visites");
      dot(gw, world(p.lat, p.lon), Math.min(7, 2.6 + Math.sqrt(p.n) * .9), fresh, title); nw += p.n;
      var xy = qc(p.lat, p.lon);
      if (xy) { dot(gq, xy, Math.min(14, 5 + Math.sqrt(p.n) * 1.8), fresh, title); nq += p.n; }
    });
    $("world-n").textContent = plural(nw, "visite", "visites");
    $("qc-n").textContent = plural(nq, "visite", "visites");
  }

  /* ---------- Tableau ---------- */
  function cell(row, main, sub, cls) {
    var s = document.createElement("span");
    s.setAttribute("role", "cell");
    if (cls) s.className = cls;
    if (main instanceof Node) s.appendChild(main); else s.textContent = main;
    if (sub) { var sm = document.createElement("small"); sm.textContent = sub; s.appendChild(sm); }
    row.appendChild(s);
    return s;
  }
  function place(v) { return [v.ville, v.region, countryName(v.pays)].filter(Boolean).join(" · "); }
  function where(v) {
    var w = document.createElement("span");
    var fl = document.createElement("span"); fl.className = "av-flag"; fl.setAttribute("aria-hidden", "true"); fl.textContent = flag(v.pays);
    w.appendChild(fl);
    w.appendChild(document.createTextNode(place(v) || "Lieu inconnu"));
    return w;
  }
  function cherche() { return ($("q").value || "").trim().toLowerCase(); }
  function trouve(q, champs) { return !q || champs.join(" ").toLowerCase().indexOf(q) >= 0; }
  function lienIp(ip) {
    if (!ip) return "—";
    var b = document.createElement("button");
    b.type = "button"; b.className = "av-ip"; b.textContent = ip; b.setAttribute("data-ip", ip);
    b.title = "Ouvrir la fiche de ce visiteur";
    return b;
  }
  function render() {
    var fp = $("f-pays").value, fg = $("f-page").value, hide = $("f-bots").checked, bots = 0, q = cherche();
    var list = all.filter(function (v) {
      if (!((!fp || (v.pays || "") === fp) && (!fg || (v.page || "") === fg))) return false;
      if (!trouve(q, [v.ip, v.ville, v.region, countryName(v.pays), v.fournisseur, v.page, v.ref])) return false;
      if (isBot(v)) { bots++; return !hide; }
      return true;
    });
    kpis();
    maps(list);
    var box = $("rows");
    box.textContent = "";
    var frag = document.createDocumentFragment(), ips = {}, pays = {};
    list.forEach(function (v) {
      if (v.ip) ips[v.ip] = 1;
      if (v.pays) pays[v.pays] = 1;
      var bot = isBot(v);
      var row = document.createElement("div");
      row.className = "av-row" + (bot ? " is-bot" : ""); row.setAttribute("role", "row");
      cell(row, timeFmt.format(new Date(v.t)), v.type === "page" ? "page suivante" : "arrivée", "av-mono");
      cell(row, where(v), v.fuseau || "");
      cell(row, v.fournisseur || "Fournisseur inconnu", v.asn ? "AS" + v.asn : "");
      cell(row, lienIp(v.ip), "", "av-mono");
      cell(row, v.page || "—", "", "av-mono");
      var dev = document.createElement("span");
      var tag = document.createElement("span"); tag.className = "av-tag" + (bot ? " is-bot" : ""); tag.textContent = bot && v.appareil !== "Robot" ? "Centre de données" : v.appareil || "—";
      dev.appendChild(tag);
      cell(row, dev, [v.systeme, v.navigateur].filter(Boolean).join(" · "));
      cell(row, v.ref || "Accès direct", "");
      frag.appendChild(row);
    });
    box.appendChild(frag);
    $("count").textContent = plural(list.length, "visite", "visites") +
      (list.length ? " · " + plural(Object.keys(ips).length, "adresse IP", "adresses IP") + " · " + fmt(Object.keys(pays).length) + " pays" : "") +
      (hide && bots ? " · " + plural(bots, "robot masqué", "robots masqués") : "");
    $("more").hidden = !cursor;
    $("empty").hidden = list.length > 0;
    $("empty").textContent = all.length && !list.length ? "Aucune visite ne correspond aux filtres." : "Aucune visite à afficher.";
    $("n-journal").textContent = fmt(list.length);
    var vs = visiteurs();
    renderVisiteurs(vs);
    renderConversations();
    if (ficheIp) remplisFiche(ficheIp);
  }

  /* ---------- Visiteurs : une ligne par adresse IP (visites et conversations réunies) ---------- */
  function visiteurs() {
    var par = {}, liste = [];
    function fiche(ip, x) {
      if (!par[ip]) { par[ip] = { ip: ip, visites: 0, pages: 0, questions: 0, premier: x.t, dernier: x.t, info: x, vus: [], chats: [] }; liste.push(par[ip]); }
      var f = par[ip];
      if (x.t < f.premier) f.premier = x.t;
      if (x.t > f.dernier) { f.dernier = x.t; }
      if (x.lat != null || !f.info.ville) f.info = Object.assign({}, f.info, x);
      return f;
    }
    all.forEach(function (v) {
      if (!v.ip) return;
      var f = fiche(v.ip, v);
      f.pages++; if (v.type !== "page") f.visites++;
      f.vus.push(v);
      if (isBot(v)) f.bot = true;
    });
    chats.forEach(function (c) {
      if (!c.ip) return;
      var f = fiche(c.ip, c);
      f.questions++; f.chats.push(c);
    });
    liste.forEach(function (f) { if (!f.visites && f.pages) f.visites = 1; });
    liste.sort(function (a, b) { return a.dernier < b.dernier ? 1 : -1; });
    return liste;
  }
  var depuis = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
  function ilYa(t) {
    var m = Math.round((Date.now() - Date.parse(t)) / 60000);
    if (m < 1) return "à l’instant";
    if (m < 60) return "il y a " + m + " min";
    if (m < 1440) return "il y a " + Math.round(m / 60) + " h";
    return depuis.format(new Date(t));
  }
  function renderVisiteurs(vs) {
    var hide = $("f-bots").checked, parle = $("f-parle").checked, q = cherche();
    var liste = vs.filter(function (f) {
      if (hide && f.bot) return false;
      if (parle && !f.questions) return false;
      return trouve(q, [f.ip, f.info.ville, f.info.region, countryName(f.info.pays), f.info.fournisseur,
        f.vus.map(function (v) { return v.page; }).join(" "), f.chats.map(function (c) { return c.q + " " + c.r; }).join(" ")]);
    });
    var box = $("v-rows"); box.textContent = "";
    var frag = document.createDocumentFragment();
    liste.forEach(function (f) {
      var row = document.createElement("div");
      row.className = "av-row av-vrow" + (f.bot ? " is-bot" : "") + (f.questions ? " a-parle" : "");
      row.setAttribute("role", "row"); row.setAttribute("data-ip", f.ip); row.tabIndex = 0;
      cell(row, where(f.info), f.info.fournisseur || "Fournisseur inconnu", "av-qui");
      cell(row, f.ip, "", "av-mono");
      var dev = document.createElement("span");
      var tag = document.createElement("span"); tag.className = "av-tag" + (f.bot ? " is-bot" : ""); tag.textContent = f.bot && f.info.appareil !== "Robot" ? "Centre de données" : f.info.appareil || "—";
      dev.appendChild(tag);
      cell(row, dev, [f.info.systeme, f.info.navigateur].filter(Boolean).join(" · "));
      cell(row, fmt(f.visites), "", "av-mono");
      cell(row, fmt(f.pages), "", "av-mono");
      var j = document.createElement("span");
      if (f.questions) { j.className = "av-jarvis"; j.textContent = plural(f.questions, "question", "questions"); }
      else { j.className = "av-jarvis is-vide"; j.textContent = "—"; }
      cell(row, j, "");
      cell(row, ilYa(f.dernier), "", "av-mono");
      frag.appendChild(row);
    });
    box.appendChild(frag);
    var humains = vs.filter(function (f) { return !f.bot; }).length;
    $("n-visiteurs").textContent = fmt(liste.length);
    $("v-count").textContent = plural(liste.length, "visiteur", "visiteurs") + " · " +
      plural(vs.filter(function (f) { return f.questions; }).length, "a parlé à JARVIS", "ont parlé à JARVIS") +
      (hide && vs.length > humains ? " · " + plural(vs.length - humains, "robot masqué", "robots masqués") : "");
    $("v-empty").hidden = liste.length > 0;
    $("v-empty").textContent = vs.length ? "Aucun visiteur ne correspond." : (token() ? "Aucun visiteur pour l’instant." : "Collez le jeton en haut pour voir les visiteurs.");
  }

  /* ---------- Conversations : un fil par conversation (un onglet de visiteur) ---------- */
  function groupes(liste) {
    var par = {}, ordre = [];
    liste.forEach(function (x) { var k = x.s || x.t; if (!par[k]) { par[k] = []; ordre.push(k); } par[k].push(x); });
    return ordre.map(function (k) { return par[k].slice().sort(function (a, b) { return a.t < b.t ? -1 : 1; }); });
  }
  function el(tag, cls, txt) { var n = document.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }
  function bulles(box, x) {
    box.appendChild(el("p", "cv-q", x.q));
    if (x.r) box.appendChild(el("p", "cv-r" + (/^\(aucune réponse/.test(x.r) ? " is-rate" : ""), x.r));
    else box.appendChild(el("p", "cv-r is-attente", "En attente de la réponse de JARVIS…"));
  }
  function renderConversations() {
    var q = cherche();
    var convs = groupes(chats).filter(function (c) {
      return c.some(function (x) { return trouve(q, [x.q, x.r, x.page, x.ville, x.region, x.ip, x.fournisseur]); });
    });
    var box = $("c-rows"); box.textContent = "";
    $("n-conversations").textContent = fmt(convs.length);
    $("c-count").textContent = plural(convs.length, "conversation", "conversations") + " · " + plural(chats.length, "question", "questions");
    $("c-state").textContent = cState || (token() ? (chats.length ? "" : "Aucune conversation pour l’instant. Chaque question posée à JARVIS sur le site apparaîtra ici, même s’il ne répond pas.") : "Collez le jeton en haut pour voir les conversations.");
    $("c-state").hidden = !$("c-state").textContent;
    $("c-more").hidden = !cCursor;
    convs.forEach(function (c, n) {
      var d = el("details", "cv-c");
      var s = el("summary");
      var premier = c[0], dernier = c[c.length - 1];
      var tete = el("div", "cv-tete");
      tete.appendChild(el("b", "", premier.q.length > 110 ? premier.q.slice(0, 110) + "…" : premier.q));
      tete.appendChild(el("span", "cv-quand", ilYa(dernier.t)));
      s.appendChild(tete);
      var meta = el("div", "cv-meta");
      meta.appendChild(where(premier));
      meta.appendChild(el("span", "", plural(c.length, "question", "questions") + " · " + (premier.appareil || "Appareil inconnu") + " · " + (premier.page || "/")));
      if (premier.ip) meta.appendChild(lienIp(premier.ip));
      s.appendChild(meta);
      d.appendChild(s);
      c.forEach(function (x) {
        var m = el("div", "cv-m");
        bulles(m, x);
        m.appendChild(el("small", "", timeFmt.format(new Date(x.t)) + " · " + (x.page || "/") + (x.lang === "en" ? " · anglais" : "")));
        d.appendChild(m);
      });
      if (n === 0 && convs.length < 4) d.open = true;
      box.appendChild(d);
    });
  }

  /* ---------- Fiche d'un visiteur : son parcours et ses questions, dans un seul fil ---------- */
  var ficheIp = "";
  function remplisFiche(ip) {
    var f = visiteurs().filter(function (x) { return x.ip === ip; })[0];
    var corps = $("fiche-corps"); corps.textContent = "";
    if (!f) { corps.appendChild(el("p", "av-hint", "Ce visiteur n’est plus dans ce qui est chargé.")); return; }
    var tete = el("div", "av-f-tete");
    var lieu = el("h3", "", ""); lieu.appendChild(where(f.info)); tete.appendChild(lieu);
    var ipl = el("p", "av-f-ip");
    ipl.appendChild(el("span", "", f.ip));
    var copie = el("button", "av-copie", "Copier");
    copie.type = "button";
    copie.addEventListener("click", function () {
      try { navigator.clipboard.writeText(f.ip).then(function () { copie.textContent = "Copié"; }, function () {}); } catch (e) {}
    });
    ipl.appendChild(copie);
    tete.appendChild(ipl);
    tete.appendChild(el("p", "av-f-sous", [f.info.fournisseur, f.info.appareil, [f.info.systeme, f.info.navigateur].filter(Boolean).join(" · ")].filter(Boolean).join(" · ")));
    corps.appendChild(tete);
    var ch = el("div", "av-f-chiffres");
    [[f.visites, f.visites > 1 ? "visites" : "visite"], [f.pages, f.pages > 1 ? "pages vues" : "page vue"], [f.questions, f.questions > 1 ? "questions à JARVIS" : "question à JARVIS"]].forEach(function (k) {
      var b = el("div"); b.appendChild(el("b", "", fmt(k[0]))); b.appendChild(el("span", "", k[1])); ch.appendChild(b);
    });
    corps.appendChild(ch);
    corps.appendChild(el("p", "av-f-sous", "Première visite " + depuis.format(new Date(f.premier)) + " · dernière " + ilYa(f.dernier)));
    corps.appendChild(el("h4", "", "Son parcours"));
    var fil = el("ol", "av-fil");
    var evts = f.vus.map(function (v) { return { t: v.t, v: v }; }).concat(f.chats.map(function (c) { return { t: c.t, c: c }; }));
    evts.sort(function (a, b) { return a.t < b.t ? -1 : 1; });
    var jour = "";
    var jf = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, weekday: "long", day: "numeric", month: "long" });
    var hf = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, hour: "2-digit", minute: "2-digit" });
    evts.forEach(function (e) {
      var j = jf.format(new Date(e.t));
      if (j !== jour) { jour = j; fil.appendChild(el("li", "av-fil-jour", j)); }
      var li = el("li", e.c ? "av-fil-q" : "av-fil-p");
      li.appendChild(el("time", "", hf.format(new Date(e.t))));
      var c = el("div");
      if (e.c) { bulles(c, e.c); }
      else {
        c.appendChild(el("span", "av-fil-page", e.v.page || "/"));
        if (e.v.type !== "page") c.appendChild(el("small", "", "Arrivée" + (e.v.ref ? " depuis " + e.v.ref : " directe")));
      }
      li.appendChild(c);
      fil.appendChild(li);
    });
    corps.appendChild(fil);
  }
  function ouvreFiche(ip) {
    ficheIp = ip; remplisFiche(ip);
    $("fiche").hidden = false; $("voile").hidden = false;
    document.documentElement.classList.add("av-fiche-ouverte");
    $("fiche").scrollTop = 0; $("fermer").focus();
  }
  function fermeFiche() {
    ficheIp = ""; $("fiche").hidden = true; $("voile").hidden = true;
    document.documentElement.classList.remove("av-fiche-ouverte");
  }
  $("fermer").addEventListener("click", fermeFiche);
  $("voile").addEventListener("click", fermeFiche);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && ficheIp) fermeFiche(); });
  root.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-ip]");
    if (t && root.contains(t) && !e.target.closest(".av-fiche")) { e.preventDefault(); ouvreFiche(t.getAttribute("data-ip")); }
  });
  root.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target.classList && e.target.classList.contains("av-vrow")) ouvreFiche(e.target.getAttribute("data-ip"));
  });

  /* ---------- Relevé d'avant la mise en service (clés « archive:… » du service) ---------- */
  function archive(items) {
    var card = $("archive"), box = $("a-rows");
    box.textContent = "";
    var lines = [], notes = [], heads = [];
    items.forEach(function (a) {
      var c = a && a.contenu;
      if (!c || !Array.isArray(c.lignes)) return;
      lines = lines.concat(c.lignes.filter(function (l) { return l && typeof l === "object"; }));
      if (c.note) notes.push(String(c.note));
      heads.push([c.periode ? "Relevé " + c.periode : "", c.source ? "Source : " + c.source : ""].filter(Boolean).join(". "));
    });
    card.hidden = !lines.length;
    if (!lines.length) return;
    lines.sort(function (a, b) { return (+b.appels || 0) - (+a.appels || 0); });
    var frag = document.createDocumentFragment(), total = 0;
    lines.forEach(function (l) {
      var bot = isBot(l);
      total += +l.appels || 0;
      var row = document.createElement("div");
      row.className = "av-row av-arow" + (bot ? " is-bot" : ""); row.setAttribute("role", "row");
      cell(row, where(l), "");
      cell(row, l.fournisseur || "Fournisseur inconnu", bot ? "robot" : "");
      cell(row, l.ip || "—", "", "av-mono");
      cell(row, fmt(+l.appels || 0), "", "av-mono");
      frag.appendChild(row);
    });
    box.appendChild(frag);
    $("a-count").textContent = plural(lines.length, "adresse", "adresses") + " · " + plural(total, "appel", "appels");
    $("a-lead").textContent = heads.filter(Boolean).join(" · ") + (heads.filter(Boolean).length ? "." : "");
    $("a-note").textContent = notes.join(" ");
  }

  render();
  load(false);
  loadChats(false);
})();
