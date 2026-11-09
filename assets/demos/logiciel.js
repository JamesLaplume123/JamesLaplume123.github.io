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
    if (stage.classList.contains("is-phone")) return;
    var w = host.clientWidth;
    if (w >= DESIGN || w < 700) return;
    app.style.width = DESIGN + "px";
    app.style.zoom = (w / DESIGN).toFixed(4);
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
