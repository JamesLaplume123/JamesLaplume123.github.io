/* Section « Conversations avec JARVIS » de la page privée des visites (/admin/visites/).
   Lit GET /chats du service du site avec le jeton collé par James (Authorization: Bearer), regroupe
   les échanges par conversation (un onglet de visiteur) et les affiche comme un fil de messages.
   Même jeton que le journal (collé en haut de la page) : il reste dans sessionStorage (cet onglet
   seulement) et ne part que vers le service du site.
   Tout ce qui vient des visiteurs est écrit en texte (textContent), jamais en HTML. */
(function () {
  "use strict";
  var root = document.querySelector("[data-cv-root]");
  if (!root) return;
  var API = (document.documentElement.getAttribute("data-api") || "").replace(/\/$/, "");
  var KEY = "jarvis-visites-jeton";   /* même jeton que le journal des visites */
  var tous = [], curseur = null, occupe = false;
  function $(k) { return root.querySelector('[data-cv="' + k + '"]'); }
  function jeton(v) { try { if (v === undefined) return sessionStorage.getItem(KEY) || ""; if (v) sessionStorage.setItem(KEY, v); else sessionStorage.removeItem(KEY); } catch (e) { return ""; } }
  function etat(t, ton) { var e = $("etat"); e.textContent = t; e.dataset.ton = ton || ""; }
  function el(tag, cls, txt) { var n = document.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }
  var heure = new Intl.DateTimeFormat("fr-CA", { timeZone: "America/Toronto", dateStyle: "medium", timeStyle: "short" });
  var regions = null; try { regions = new Intl.DisplayNames(["fr-CA"], { type: "region" }); } catch (e) {}
  function pays(cc) { try { return cc ? (regions && regions.of(cc)) || cc : ""; } catch (e) { return cc || ""; } }

  function groupes(liste) {
    var par = {}, ordre = [];
    liste.forEach(function (x) {
      var k = x.s || x.t;
      if (!par[k]) { par[k] = []; ordre.push(k); }
      par[k].push(x);
    });
    return ordre.map(function (k) { return par[k].slice().sort(function (a, b) { return a.t < b.t ? -1 : 1; }); });
  }

  function affiche() {
    var q = ($("cherche").value || "").trim().toLowerCase();
    var liste = $("liste"); liste.textContent = "";
    var convs = groupes(tous).filter(function (c) {
      return !q || c.some(function (x) { return [x.q, x.r, x.page, x.ville, x.region, x.ip, x.fournisseur].join(" ").toLowerCase().indexOf(q) >= 0; });
    });
    var ch = $("chiffres");
    if (tous.length) {
      ch.hidden = false; ch.textContent = "";
      var jour = Date.now() - 86400000, sem = Date.now() - 7 * 86400000;
      [["Conversations", groupes(tous).length], ["Questions", tous.length],
       ["Dernières 24 h", tous.filter(function (x) { return Date.parse(x.t) > jour; }).length],
       ["7 jours", tous.filter(function (x) { return Date.parse(x.t) > sem; }).length]].forEach(function (k) {
        var b = el("div", "cv-k"); b.appendChild(el("b", "", String(k[1]))); b.appendChild(el("span", "", k[0])); ch.appendChild(b);
      });
    }
    if (!convs.length) { liste.appendChild(el("p", "cv-vide", tous.length ? "Aucune conversation ne contient ce mot." : "Aucune conversation pour l’instant.")); return; }
    convs.forEach(function (c) {
      var d = el("details", "cv-c");
      var s = el("summary");
      var premier = c[0], dernier = c[c.length - 1];
      s.appendChild(el("b", "", premier.q.length > 110 ? premier.q.slice(0, 110) + "…" : premier.q));
      var lieu = [premier.ville, premier.region, pays(premier.pays)].filter(Boolean).join(", ");
      s.appendChild(el("span", "", heure.format(new Date(dernier.t)) + " · " + c.length + (c.length > 1 ? " questions" : " question") +
        (lieu ? " · " + lieu : "") + (premier.appareil ? " · " + premier.appareil : "") + " · " + (premier.page || "/")));
      if (premier.ip) s.appendChild(el("span", "cv-ip", premier.ip + (premier.fournisseur ? " · " + premier.fournisseur : "")));
      d.appendChild(s);
      c.forEach(function (x) {
        var m = el("div", "cv-m");
        m.appendChild(el("p", "cv-q", x.q));
        m.appendChild(el("p", "cv-r", x.r));
        m.appendChild(el("small", "", heure.format(new Date(x.t)) + " · " + (x.page || "/") + (x.lang === "en" ? " · anglais" : "")));
        d.appendChild(m);
      });
      liste.appendChild(d);
    });
    if (convs.length === 1) liste.querySelector("details").open = true;
  }

  function charge(suite) {
    var t = jeton();
    if (!t) { etat("Ouvrez le journal ci-dessus : les conversations suivent."); return; }
    if (!API) { etat("Le service du site n’est pas configuré.", "mal"); return; }
    if (occupe) return; occupe = true;
    etat("Chargement…");
    fetch(API + "/chats?limit=300" + (suite && curseur ? "&cursor=" + encodeURIComponent(curseur) : ""), { headers: { Authorization: "Bearer " + t }, cache: "no-store" })
      .then(function (r) {
        if (r.status === 401) { jeton(null); throw new Error("Jeton refusé. Vérifiez que c’est bien le jeton LEADS_TOKEN."); }
        if (r.status === 404) throw new Error("Le service ne connaît pas encore les conversations : il doit être redéployé.");
        if (!r.ok) throw new Error("Le service ne répond pas (" + r.status + ").");
        return r.json();
      })
      .then(function (d) {
        tous = suite ? tous.concat(d.echanges || []) : (d.echanges || []);
        curseur = d.cursor || null;
        $("plus").hidden = !curseur;
        root.classList.add("is-ouvert");
        etat(tous.length ? "À jour." : "Aucune conversation pour l’instant.", "bon");
        affiche();
      })
      .catch(function (e) { etat(e.message || "Erreur de chargement.", "mal"); })
      .then(function () { occupe = false; });
  }

  $("maj").addEventListener("click", function () { charge(false); });
  $("plus").addEventListener("click", function () { charge(true); });
  $("cherche").addEventListener("input", affiche);
  /* Le journal ci-dessus garde le jeton : on charge quand il l'a (ouverture, actualisation). */
  document.addEventListener("click", function (e) {
    if (e.target.closest && e.target.closest('[data-av="refresh"]')) setTimeout(function () { charge(false); }, 50);
    if (e.target.closest && e.target.closest('[data-av="forget"]')) { tous = []; root.classList.remove("is-ouvert"); $("liste").textContent = ""; $("chiffres").hidden = true; etat("Ouvrez le journal ci-dessus : les conversations suivent."); }
  });
  var formJ = document.querySelector('[data-av="form"]');
  if (formJ) formJ.addEventListener("submit", function () { setTimeout(function () { charge(false); }, 80); });
  if (jeton()) charge(false);
})();
