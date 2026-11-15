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

  $("form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var input = root.querySelector("#av-jeton");
    var t = input.value.trim();
    input.value = "";
    if (!t) { status("Le champ est vide : collez le jeton.", "warn"); return; }
    set(session, KEY, t);
    load(false);
  });
  $("refresh").addEventListener("click", function () { load(false); });
  $("forget").addEventListener("click", function () {
    set(session, KEY, null);
    all = []; cursor = null; stats = null; archive([]); fillFilters(); render();
    status("Jeton oublié dans cet onglet.", "");
  });
  $("f-pays").addEventListener("change", render);
  $("f-page").addEventListener("change", render);
  $("f-bots").addEventListener("change", render);
  $("more").addEventListener("click", function () { load(true); });

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
  function render() {
    var fp = $("f-pays").value, fg = $("f-page").value, hide = $("f-bots").checked, bots = 0;
    var list = all.filter(function (v) {
      if (!((!fp || (v.pays || "") === fp) && (!fg || (v.page || "") === fg))) return false;
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
      cell(row, v.ip || "—", "", "av-mono");
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
  }

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
})();
