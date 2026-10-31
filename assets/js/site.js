/* JARVIS Private Systems — comportement du site.
   Un seul fichier, aucun framework. Chaque bloc échoue en silence :
   sans JavaScript, tout le contenu reste visible et navigable. */

(function () {
  "use strict";

  document.documentElement.classList.add("js");

  /* ----- En-tête : fond plein après défilement ----- */
  var head = document.querySelector("[data-head]");
  if (head) {
    var onScroll = function () {
      head.classList.toggle("is-solid", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ----- Menu mobile ----- */
  var toggle = document.querySelector("[data-nav-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll("[data-nav] a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ----- Révélations au défilement -----
     L'effet est un plus, jamais une condition : un filet de sécurité révèle
     tout élément encore caché (onglet en arrière-plan, observateur en retard,
     navigateur ancien). Le contenu ne peut jamais rester invisible. */
  var revealed = document.querySelectorAll("[data-reveal]");
  var revealAll = function () {
    revealed.forEach(function (el) {
      el.classList.add("is-in");
    });
  };
  if (revealed.length && "IntersectionObserver" in window && document.visibilityState === "visible") {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    revealed.forEach(function (el) {
      io.observe(el);
    });
    /* Filets de sécurité : onglet caché, impression, ou observateur en retard
       (vérification périodique de ce qui se trouve dans la fenêtre). */
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") revealAll();
    });
    window.addEventListener("beforeprint", revealAll);
    var patrol = window.setInterval(function () {
      var pending = false;
      revealed.forEach(function (el) {
        if (el.classList.contains("is-in")) return;
        pending = true;
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 1.1 && r.bottom > -40) {
          el.classList.add("is-in");
        }
      });
      if (!pending) window.clearInterval(patrol);
    }, 700);
  } else {
    revealAll();
  }

  /* ----- Explorateur de capacités (accueil) ----- */
  var capData = document.getElementById("cap-data");
  var capButtons = document.querySelectorAll("[data-cap]");
  if (capData && capButtons.length) {
    try {
      var caps = JSON.parse(capData.textContent);
      var img = document.querySelector("[data-cap-image]");
      var kicker = document.querySelector("[data-cap-kicker]");
      var title = document.querySelector("[data-cap-title]");
      var copy = document.querySelector("[data-cap-copy]");
      var link = document.querySelector("[data-cap-link]");
      capButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var cap = caps[btn.dataset.cap];
          if (!cap) return;
          capButtons.forEach(function (b) {
            b.classList.toggle("is-active", b === btn);
          });
          if (img && cap.image && img.getAttribute("src") !== cap.image) {
            img.style.opacity = "0";
            var swap = function () {
              img.setAttribute("src", cap.image);
              img.setAttribute("alt", cap.alt || "");
              img.style.opacity = "1";
            };
            window.setTimeout(swap, 180);
          }
          if (kicker) kicker.textContent = cap.kicker;
          if (title) title.textContent = cap.title;
          if (copy) copy.textContent = cap.copy;
          if (link) link.setAttribute("href", cap.url);
        });
      });
    } catch (err) {
      /* données illisibles : les boutons restent de simples liens visuels */
    }
  }

  /* ----- Sélecteur d'environnement (console du héros) ----- */
  var envData = document.getElementById("env-data");
  var envButtons = document.querySelectorAll("[data-env]");
  if (envData && envButtons.length) {
    try {
      var envs = JSON.parse(envData.textContent);
      var fields = {
        title: document.querySelector("[data-console-title]"),
        copy: document.querySelector("[data-console-copy]"),
        s1: document.querySelector("[data-console-s1]"),
        s2: document.querySelector("[data-console-s2]"),
        s3: document.querySelector("[data-console-s3]"),
        link: document.querySelector("[data-console-link]"),
      };
      envButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var env = envs[btn.dataset.env];
          if (!env) return;
          envButtons.forEach(function (b) {
            var active = b === btn;
            b.classList.toggle("is-active", active);
            b.setAttribute("aria-pressed", active ? "true" : "false");
          });
          if (fields.title) fields.title.textContent = env.title;
          if (fields.copy) fields.copy.textContent = env.copy;
          if (fields.s1) fields.s1.textContent = env.s1;
          if (fields.s2) fields.s2.textContent = env.s2;
          if (fields.s3) fields.s3.textContent = env.s3;
          if (fields.link && env.url) fields.link.setAttribute("href", env.url);
        });
      });
    } catch (err) {
      /* idem : échec silencieux */
    }
  }
})();
