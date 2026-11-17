/* Le logiciel (/logiciel/) : visite guidée de JARVIS App.
   - Une étape ouvre l'écran correspondant (événement « ap:go » de app.js); l'app annonce chaque
     écran ouvert (« ap:screen »), le guide suit, même pendant la visite automatique.
   - L'appareil est dessiné à 1240 px puis réduit à la place disponible : le gabarit complet de
     l'app reste visible sur ordinateur et tablette (sous 700 px, le gabarit téléphone de l'app).
   - Plein écran (API du navigateur, sinon position fixe) et aperçu téléphone.
   - /logiciel/#ecran-<clé> ouvre directement un écran.
   Rien ne s'exécute sur les pages sans visite (l'accueil n'utilise que logiciel.css). */
(function () {
  var tour = document.querySelector(".lg-tour");
  if (!tour) return;
  var root = tour.querySelector('[data-demo="app"]');
  var stage = tour.querySelector("[data-lg-stage]"), host = tour.querySelector("[data-lg-host]"), app = tour.querySelector("[data-lg-app]");
  var steps = [].slice.call(tour.querySelectorAll("[data-step]"));
  var now = tour.querySelector(".lg-now"), list = tour.querySelector(".lg-steps");
  if (!root || !stage || !host || !app) return;
  var DESIGN = 1240;

  function mark(key) {
    var hit = null;
    steps.forEach(function (b) {
      var on = b.getAttribute("data-step") === key;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on) hit = b;
    });
    if (!hit) return;
    var d = hit.querySelector(".lg-step-d");
    if (now && d) now.innerHTML = d.innerHTML;
    // Rangée d'étapes (tablette, téléphone) : l'étape ouverte reste visible, sans faire défiler la page.
    if (list && list.scrollWidth > list.clientWidth) {
      var li = hit.parentNode, x = li.offsetLeft - (list.clientWidth - li.offsetWidth) / 2;
      list.scrollTo({ left: Math.max(0, x), behavior: "smooth" });
    }
  }
  function open(key) {
    root.dispatchEvent(new CustomEvent("ap:go", { detail: key }));
    mark(key);
  }
  root.addEventListener("ap:screen", function (e) { mark(e.detail.key); });
  steps.forEach(function (b) {
    b.addEventListener("click", function () { open(b.getAttribute("data-step")); });
  });

  /* Mise à l'échelle : l'app est dessinée à 1240 px et réduite à la largeur disponible. */
  function fit() {
    app.style.width = "";
    app.style.zoom = "";
    var plein = stage.classList.contains("is-full"), tel = stage.classList.contains("is-phone");
    var w = host.clientWidth;
    if (!tel && w < 700) return;
    /* Règle du site : le cadre tient en entier dans la fenêtre. En plein écran, il prend la fenêtre (moins le
       bouton « Quitter »); sinon la fenêtre moins la barre du site. L'app est dessinée à 1240 px (400 px en
       aperçu téléphone), puis réduite. */
    var large = tel ? 400 : DESIGN;
    app.style.width = large + "px";
    var ecran = app.querySelector(".ap-screen");
    if (ecran) ecran.style.height = "";
    /* Plein écran : l'app remplit la largeur de la fenêtre; l'écran prend la hauteur qui reste et son contenu
       défile à l'intérieur. Tout devient plus gros, rien ne déborde. */
    if (plein && !tel && ecran) {
      var zp = Math.min(1.8, w / large), cible = (window.innerHeight - 56) / zp;
      ecran.style.height = "600px";
      var cadre = app.offsetHeight - ecran.offsetHeight;   /* barre du haut, légendes : tout sauf l'écran */
      ecran.style.height = Math.max(420, Math.floor(cible - Math.max(cadre, 0))) + "px";
      /* L'app se remet en page après coup (barre du haut, légendes) : on corrige l'écart une fois posée. */
      [120, 450].forEach(function (t) {
        setTimeout(function () {
          if (!stage.classList.contains("is-full")) return;
          var ecart = app.offsetHeight - cible;
          if (Math.abs(ecart) > 2) ecran.style.height = Math.max(420, Math.floor(ecran.offsetHeight - ecart)) + "px";
        }, t);
      });
      app.style.zoom = zp.toFixed(4);
      return;
    }
    var h = app.offsetHeight;
    var dispo = window.innerHeight - (plein ? 56 : 96);
    /* En plein écran, l'app grossit jusqu'à remplir la fenêtre (plus de plafond à 100 %). */
    var z = Math.min(plein ? 2.2 : 1, w / large, h ? dispo / h : 1);
    if (!plein && z >= 1) { if (!tel && w >= DESIGN) app.style.width = ""; return; }
    app.style.zoom = z.toFixed(4);
  }
  var fitT = 0;
  function refit() {
    clearTimeout(fitT);
    fitT = setTimeout(function () { fit(); window.dispatchEvent(new Event("resize")); }, 60);
  }
  if ("ResizeObserver" in window) {
    var lastW = 0;
    new ResizeObserver(function () {
      var w = host.clientWidth;
      if (w !== lastW) { lastW = w; fit(); }
    }).observe(host);
  } else addEventListener("resize", fit);
  addEventListener("resize", fit);
  fit();

  /* Aperçu téléphone */
  var phoneBtn = tour.querySelector('[data-lg="phone"]');
  if (phoneBtn) phoneBtn.addEventListener("click", function () {
    var on = !stage.classList.contains("is-phone");
    stage.classList.toggle("is-phone", on);
    phoneBtn.setAttribute("aria-pressed", on ? "true" : "false");
    phoneBtn.lastChild.textContent = on ? "Aperçu ordinateur" : "Aperçu téléphone";
    refit();
  });

  /* Plein écran */
  var fullBtn = tour.querySelector('[data-lg="full"]'), exitBtn = tour.querySelector('[data-lg="exit"]');
  var native = !!(stage.requestFullscreen && document.fullscreenEnabled);
  function setFull(on) {
    stage.classList.toggle("is-full", on);
    document.body.classList.toggle("lg-full-open", on);
    refit();
    if (on && exitBtn) exitBtn.focus({ preventScroll: true });
    if (!on && fullBtn) fullBtn.focus({ preventScroll: true });
  }
  if (fullBtn) fullBtn.addEventListener("click", function () {
    if (native) stage.requestFullscreen().catch(function () { setFull(true); });
    else setFull(true);
  });
  if (exitBtn) exitBtn.addEventListener("click", function () {
    if (document.fullscreenElement) document.exitFullscreen();
    else setFull(false);
  });
  document.addEventListener("fullscreenchange", function () { setFull(document.fullscreenElement === stage); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && stage.classList.contains("is-full") && !document.fullscreenElement) setFull(false);
  });

  /* /logiciel/#ecran-<clé> */
  function fromHash() {
    var m = /^#ecran-([a-z]+)$/.exec(location.hash);
    if (!m || !steps.some(function (b) { return b.getAttribute("data-step") === m[1]; })) return;
    open(m[1]);
    tour.scrollIntoView({ block: "start" });
  }
  fromHash();
  addEventListener("hashchange", fromHash);
})();
