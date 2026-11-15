/* Page privée « Visites du site » (/admin/visites/).
   Lit GET /visits/log du service du site avec le jeton collé par James (Authorization: Bearer).
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
  var all = [];
  var PAGE_SIZE = 50, shown = PAGE_SIZE; // le tableau s'allonge par tranches de 50

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
  function load() {
    if (!API) { status("Le service du site n’est pas configuré (adresse « api » vide dans src/config.py).", "bad"); return; }
    var t = token();
    if (!t) { status("Collez le jeton pour afficher le journal.", ""); return; }
    status("Chargement du journal…", "");
    fetch(API + "/visits/log?limit=1000", { headers: { Authorization: "Bearer " + t }, cache: "no-store" })
      .then(function (r) {
        if (r.status === 401) throw { msg: "Jeton refusé par le service. Vérifiez que c’est bien le jeton LEADS_TOKEN.", tone: "bad", forget: true };
        if (!r.ok) throw { msg: "Le service répond avec une erreur (" + r.status + "). Réessayez dans un moment.", tone: "bad" };
        return r.json();
      })
      .then(function (j) {
        if (!j || !Array.isArray(j.visits)) throw { msg: "Le service répond, mais ne connaît pas encore le journal des visites : le nouveau Worker n’est pas encore déployé sur Cloudflare.", tone: "warn" };
        all = j.visits.filter(function (v) { return v && v.t; });
        all.sort(function (a, b) { return a.t < b.t ? 1 : -1; });
        shown = PAGE_SIZE;
        fillFilters();
        render();
        var when = new Intl.DateTimeFormat("fr-CA", { timeZone: TZ, hour: "2-digit", minute: "2-digit" }).format(new Date());
        status("Journal à jour à " + when + " · " + plural(all.length, "entrée", "entrées") + " · conservation 30 jours" +
          (all.length >= 1000 ? " · seules les 1 000 plus récentes sont affichées" : "") + ".", "ok");
      })
      .catch(function (e) {
        if (e && e.forget) set(session, KEY, null);
        status(e && e.msg ? e.msg : "Le service ne répond pas, ou il n’est pas encore à jour sur Cloudflare (le nouveau Worker doit être déployé).", (e && e.tone) || "bad");
      });
  }

  $("form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var input = root.querySelector("#av-jeton");
    var t = input.value.trim();
    input.value = "";
    if (!t) { status("Le champ est vide : collez le jeton.", "warn"); return; }
    set(session, KEY, t);
    load();
  });
  $("refresh").addEventListener("click", load);
  $("forget").addEventListener("click", function () {
    set(session, KEY, null);
    all = []; fillFilters(); render();
    status("Jeton oublié dans cet onglet.", "");
  });
  function refilter() { shown = PAGE_SIZE; render(); }
  $("f-pays").addEventListener("change", refilter);
  $("f-page").addEventListener("change", refilter);
  $("more").addEventListener("click", function () { shown += PAGE_SIZE; render(); });

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

  /* ---------- Chiffres ---------- */
  function kpis() {
    var now = Date.now(), today = dayFmt.format(new Date());
    var w = { day: [0, 0], d7: [0, 0], d30: [0, 0] }, ips = {}, pays = {};
    all.forEach(function (v) {
      var t = Date.parse(v.t), age = now - t, arrive = v.type !== "page";
      function add(b) { b[1]++; if (arrive) b[0]++; }
      if (dayFmt.format(new Date(t)) === today) add(w.day);
      if (age <= 7 * DAY) add(w.d7);
      if (age <= 30 * DAY) { add(w.d30); if (v.ip) ips[v.ip] = 1; if (v.pays) pays[v.pays] = 1; }
    });
    var has = all.length > 0;
    function put(k, b) { $(k).textContent = has ? fmt(b[0]) : "—"; $(k + "-p").textContent = has ? plural(b[1], "page vue", "pages vues") : "pages vues —"; }
    put("k-day", w.day); put("k-7", w.d7); put("k-30", w.d30);
    $("k-ip").textContent = has ? fmt(Object.keys(ips).length) : "—";
    $("k-pays").textContent = has ? plural(Object.keys(pays).length, "pays", "pays") : "pays —";
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
      if (!places[k]) { places[k] = { lat: +v.lat, lon: +v.lon, n: 0, t: v.t, label: [v.ville, v.region, countryName(v.pays)].filter(Boolean).join(" · ") }; order.push(k); }
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
  function render() {
    var fp = $("f-pays").value, fg = $("f-page").value;
    var list = all.filter(function (v) { return (!fp || (v.pays || "") === fp) && (!fg || (v.page || "") === fg); });
    kpis();
    maps(list);
    var box = $("rows");
    box.textContent = "";
    var frag = document.createDocumentFragment();
    list.slice(0, shown).forEach(function (v) {
      var row = document.createElement("div");
      row.className = "av-row"; row.setAttribute("role", "row");
      cell(row, timeFmt.format(new Date(v.t)), v.type === "page" ? "page suivante" : "arrivée", "av-mono");
      var where = document.createElement("span");
      var fl = document.createElement("span"); fl.className = "av-flag"; fl.setAttribute("aria-hidden", "true"); fl.textContent = flag(v.pays);
      where.appendChild(fl);
      where.appendChild(document.createTextNode([v.ville, v.region, countryName(v.pays)].filter(Boolean).join(" · ")));
      cell(row, where, v.fuseau || "");
      cell(row, v.fournisseur || "Fournisseur inconnu", v.asn ? "AS" + v.asn : "");
      cell(row, v.ip || "—", "", "av-mono");
      cell(row, v.page || "—", "", "av-mono");
      var dev = document.createElement("span");
      var tag = document.createElement("span"); tag.className = "av-tag" + (v.appareil === "Robot" ? " is-bot" : ""); tag.textContent = v.appareil || "—";
      dev.appendChild(tag);
      cell(row, dev, [v.systeme, v.navigateur].filter(Boolean).join(" · "));
      cell(row, v.ref || "Accès direct", "");
      frag.appendChild(row);
    });
    box.appendChild(frag);
    $("count").textContent = plural(list.length, "visite", "visites") + (list.length > shown ? " · " + fmt(shown) + " affichées" : "");
    $("more").hidden = list.length <= shown;
    $("empty").hidden = list.length > 0;
  }

  render();
  load();
})();
