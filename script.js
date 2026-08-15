(() => {
  const data = window.JL_DATA || {};
  const doc = document;
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const iconMap = {
    ambulance: "truck",
    "monitor-dot": "monitor",
    cctv: "camera",
    "scan-eye": "scan-eye"
  };

  const qs = (selector, root = doc) => root.querySelector(selector);
  const qsa = (selector, root = doc) => [...root.querySelectorAll(selector)];

  const escapeHTML = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  const renderIcon = (name) => `<i data-lucide="${iconMap[name] || name}" aria-hidden="true"></i>`;

  const refreshIcons = () => {
    if (window.lucide?.createIcons) {
      window.lucide.createIcons({
        attrs: {
          "stroke-width": 2
        }
      });
    }
  };

  const setActiveNavigation = () => {
    const current = location.pathname.split("/").pop() || "index.html";
    qsa(".main-nav a").forEach((link) => {
      const href = link.getAttribute("href");
      const active = href === current || (current === "" && href === "index.html");
      link.classList.toggle("is-active", active);
      if (active) link.setAttribute("aria-current", "page");
    });
  };

  const initHeader = () => {
    const header = qs("[data-header]");
    const toggle = qs("[data-nav-toggle]");
    const nav = qs("[data-nav]");

    const onScroll = () => {
      header?.classList.toggle("is-scrolled", window.scrollY > 18);
      if (!prefersReducedMotion) {
        const hero = qs("[data-hero] .hero-media");
        if (hero) {
          const offset = Math.min(window.scrollY * 0.08, 42);
          hero.style.transform = `scale(1.035) translateY(${offset}px)`;
        }
      }
    };

    toggle?.addEventListener("click", () => {
      const open = !nav?.classList.contains("is-open");
      nav?.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });

    qsa(".main-nav a").forEach((link) => {
      link.addEventListener("click", () => {
        nav?.classList.remove("is-open");
        toggle?.setAttribute("aria-expanded", "false");
      });
    });

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    setActiveNavigation();
  };

  const initReveal = () => {
    const elements = qsa(".reveal");
    if (!elements.length) return;
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      elements.forEach((element) => element.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.16, rootMargin: "0px 0px -8% 0px" }
    );

    elements.forEach((element) => observer.observe(element));
  };

  const renderServices = () => {
    const grid = qs("[data-services-grid]");
    if (!grid || !data.services) return;

    grid.innerHTML = data.services
      .map(
        (service) => `
          <article class="service-card reveal">
            ${renderIcon(service.icon)}
            <h3>${escapeHTML(service.title)}</h3>
            <p>${escapeHTML(service.intro)}</p>
            <details>
              <summary>Problèmes résolus et livrables</summary>
              <p>Problèmes typiques</p>
              <ul>${service.solves.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}</ul>
              <p>Exemples de livrables</p>
              <ul>${service.deliverables.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}</ul>
            </details>
            <a class="button button-secondary" href="contact.html">Décrire mon projet ${renderIcon("arrow-right")}</a>
          </article>
        `
      )
      .join("");
  };

  const renderSolutions = () => {
    const grid = qs("[data-solutions-grid]");
    if (!grid || !data.solutions) return;

    grid.innerHTML = data.solutions
      .map(
        (solution) => `
          <article class="solution-card reveal">
            ${renderIcon(solution.icon)}
            <h3>${escapeHTML(solution.title)}</h3>
            <p>${escapeHTML(solution.text)}</p>
            <ul>${solution.examples.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}</ul>
          </article>
        `
      )
      .join("");
  };

  const renderProcess = () => {
    const rail = qs("[data-process-rail]");
    if (!rail || !data.process) return;

    rail.innerHTML = data.process
      .map(
        (step) => `
          <article class="process-step reveal">
            <span>${escapeHTML(step.step)}</span>
            <h3>${escapeHTML(step.title)}</h3>
            <p>${escapeHTML(step.text)}</p>
          </article>
        `
      )
      .join("");
  };

  const renderArticleCards = (root, articles, asButtons = false) => {
    const tag = asButtons ? "button" : "article";
    root.innerHTML = articles
      .map(
        (article) => `
          <${tag} class="article-card reveal" ${asButtons ? `type="button" data-article-slug="${escapeHTML(article.slug)}"` : ""}>
            <div class="article-meta">
              <span>${escapeHTML(article.category)}</span>
              <span>${escapeHTML(article.status)}</span>
              <span>${escapeHTML(article.minutes)} min</span>
            </div>
            <h3>${escapeHTML(article.title)}</h3>
            <p>${articleBlurb(article.category)}</p>
          </${tag}>
        `
      )
      .join("");
  };

  const articleBlurb = (category) => {
    const blurbs = {
      "Sécurité": "Caméras, détection locale, stockage privé et alertes qui évitent le bruit.",
      "Home Assistant": "Automatiser utilement sans perdre la simplicité ni le contrôle manuel.",
      "Réseaux": "Organiser les accès, les objets connectés et les services privés avec méthode.",
      "Mobile": "Adapter les systèmes intelligents aux contraintes d'un véhicule réel.",
      "IA locale": "Explorer les assistants locaux sans prétendre que tout est déjà magique."
    };
    return blurbs[category] || "Note technique issue du lab et des projets en développement.";
  };

  const renderArticlePreview = () => {
    const root = qs("[data-article-preview]");
    if (!root || !data.articles) return;
    renderArticleCards(root, data.articles.slice(0, 6), false);
  };

  const renderArticleList = () => {
    const root = qs("[data-article-list]");
    const filters = qs("[data-article-filters]");
    if (!root || !filters || !data.articles) return;

    const categories = ["Tous", ...new Set(data.articles.map((article) => article.category))];
    filters.innerHTML = categories
      .map((category, index) => `<button type="button" class="${index === 0 ? "is-active" : ""}" data-filter="${escapeHTML(category)}">${escapeHTML(category)}</button>`)
      .join("");

    const render = (category = "Tous") => {
      const articles = category === "Tous" ? data.articles : data.articles.filter((article) => article.category === category);
      renderArticleCards(root, articles, true);
      bindArticleButtons();
      refreshIcons();
      initReveal();
    };

    filters.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-filter]");
      if (!button) return;
      qsa("button", filters).forEach((item) => item.classList.toggle("is-active", item === button));
      render(button.dataset.filter);
    });

    render();
  };

  const bindArticleButtons = () => {
    qsa("[data-article-slug]").forEach((button) => {
      button.addEventListener("click", () => openArticle(button.dataset.articleSlug));
    });
  };

  const openArticle = async (slug) => {
    const dialog = qs("[data-article-dialog]");
    const reader = qs("[data-article-reader]");
    if (!dialog || !reader) return;

    const article = data.articles?.find((item) => item.slug === slug);
    reader.innerHTML = `<p class="eyebrow">Chargement</p><h1>${escapeHTML(article?.title || "Article")}</h1>`;

    try {
      const response = await fetch(`articles/${slug}.md`, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const markdown = await response.text();
      reader.innerHTML = `
        <p class="eyebrow">${escapeHTML(article?.category || "Article")}</p>
        <h1>${escapeHTML(article?.title || "Article")}</h1>
        ${markdownToHTML(markdown)}
      `;
    } catch (error) {
      reader.innerHTML = `
        <p class="eyebrow">${escapeHTML(article?.category || "Article")}</p>
        <h1>${escapeHTML(article?.title || "Article")}</h1>
        <p>Impossible de charger le fichier Markdown localement. Sur GitHub Pages, l'article sera servi normalement.</p>
      `;
    }

    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
    refreshIcons();
  };

  const markdownToHTML = (markdown) => {
    const withoutFrontMatter = markdown.replace(/^---[\s\S]*?---\s*/, "");
    const lines = withoutFrontMatter.split(/\r?\n/);
    let html = "";
    let listOpen = false;
    const closeList = () => {
      if (listOpen) {
        html += "</ul>";
        listOpen = false;
      }
    };

    lines.forEach((line) => {
      if (!line.trim()) {
        closeList();
        return;
      }
      if (line.startsWith("# ")) {
        closeList();
        html += `<h1>${escapeHTML(line.slice(2))}</h1>`;
      } else if (line.startsWith("## ")) {
        closeList();
        html += `<h2>${escapeHTML(line.slice(3))}</h2>`;
      } else if (line.startsWith("- ")) {
        if (!listOpen) {
          html += "<ul>";
          listOpen = true;
        }
        html += `<li>${escapeHTML(line.slice(2))}</li>`;
      } else {
        closeList();
        html += `<p>${escapeHTML(line)}</p>`;
      }
    });
    closeList();
    return html;
  };

  const initDialogs = () => {
    const dialog = qs("[data-article-dialog]");
    qs("[data-close-dialog]")?.addEventListener("click", () => dialog?.close?.());
    dialog?.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close?.();
    });
  };

  const initScenarioDemo = () => {
    const tabs = qs("[data-scenario-tabs]");
    if (!tabs || !data.scenarios) return;

    const scenarios = Object.entries(data.scenarios);
    tabs.innerHTML = scenarios
      .map(([id, scenario], index) => `<button type="button" class="${index === 0 ? "is-active" : ""}" data-scenario="${id}">${escapeHTML(scenario.label)}</button>`)
      .join("");

    const activate = (id) => {
      const scenario = data.scenarios[id];
      if (!scenario) return;
      qsa("[data-scenario]", tabs).forEach((button) => button.classList.toggle("is-active", button.dataset.scenario === id));
      qs("[data-scenario-title]").textContent = scenario.title;
      qs("[data-scenario-summary]").textContent = scenario.summary;
      qs("[data-scenario-sequence]").innerHTML = scenario.sequence.map((item) => `<li>${escapeHTML(item)}</li>`).join("");
      Object.entries(scenario.values).forEach(([key, value]) => {
        const node = qs(`[data-value="${key}"]`);
        if (node) node.textContent = value;
      });
      qsa("[data-system]").forEach((node) => {
        node.classList.toggle("is-active", scenario.active.includes(node.dataset.system));
      });
    };

    tabs.addEventListener("click", (event) => {
      const button = event.target.closest("[data-scenario]");
      if (button) activate(button.dataset.scenario);
    });

    activate(scenarios[0][0]);
  };

  const initDashboardDemo = () => {
    const root = qs("[data-dashboard-actions]");
    if (!root || !data.dashboardActions) return;

    const activeMap = {
      "home-arrival": ["light", "climate", "security", "network"],
      "night-mode": ["light", "security", "camera"],
      "secure-property": ["security", "camera", "network"],
      "energy-save": ["energy", "climate", "light"],
      "office-ready": ["light", "network", "energy"],
      "person-detected": ["camera", "security", "network"]
    };

    root.innerHTML = data.dashboardActions
      .map(
        (action, index) => `
          <button type="button" class="${index === 0 ? "is-active" : ""}" data-dashboard-action="${escapeHTML(action.id)}">
            ${renderIcon(action.icon)}
            <span>${escapeHTML(action.label)}</span>
          </button>
        `
      )
      .join("");

    const activate = (id) => {
      const action = data.dashboardActions.find((item) => item.id === id);
      if (!action) return;
      qsa("[data-dashboard-action]", root).forEach((button) => button.classList.toggle("is-active", button.dataset.dashboardAction === id));
      qs("[data-dashboard-result]").textContent = action.result;
      qs("[data-dashboard-changes]").innerHTML = action.changes.map((change) => `<span>${escapeHTML(change)}</span>`).join("");
      qsa("[data-tile]").forEach((tile) => {
        tile.classList.toggle("is-active", activeMap[id]?.includes(tile.dataset.tile));
      });
    };

    root.addEventListener("click", (event) => {
      const button = event.target.closest("[data-dashboard-action]");
      if (button) activate(button.dataset.dashboardAction);
    });

    activate(data.dashboardActions[0].id);
  };

  const initSecurityDemo = () => {
    const controls = qs("[data-security-controls]");
    if (!controls || !data.securityModes) return;

    controls.innerHTML = data.securityModes
      .map((mode, index) => `<button type="button" class="${index === 0 ? "is-active" : ""}" data-security-mode="${escapeHTML(mode.id)}">${escapeHTML(mode.label)}</button>`)
      .join("");

    const activate = (id) => {
      const mode = data.securityModes.find((item) => item.id === id);
      if (!mode) return;
      qsa("[data-security-mode]", controls).forEach((button) => button.classList.toggle("is-active", button.dataset.securityMode === id));
      const feed = qs("[data-camera-feed]");
      if (feed) feed.dataset.mode = id;
      qs("[data-camera-mode-label]").textContent = mode.label;
      qs("[data-security-title]").textContent = mode.title;
      qs("[data-security-explanation]").textContent = mode.explanation;
      qs("[data-security-status]").innerHTML = mode.status.map((item) => `<li>${escapeHTML(item)}</li>`).join("");
    };

    controls.addEventListener("click", (event) => {
      const button = event.target.closest("[data-security-mode]");
      if (button) activate(button.dataset.securityMode);
    });

    activate(data.securityModes[0].id);
  };

  const initVehicleDemo = () => {
    const selectors = qsa("[data-vehicle-selector]");
    if (!selectors.length || !data.vehicleSystems) return;

    selectors.forEach((selector) => {
      selector.innerHTML = data.vehicleSystems
        .map(
          (system, index) => `
            <button type="button" class="${index === 0 ? "is-active" : ""}" data-vehicle-system="${escapeHTML(system.id)}">
              ${renderIcon(system.icon)}
              <span>${escapeHTML(system.title)}</span>
            </button>
          `
        )
        .join("");
    });

    const activate = (id) => {
      const system = data.vehicleSystems.find((item) => item.id === id);
      if (!system) return;
      qsa("[data-vehicle-system]").forEach((button) => button.classList.toggle("is-active", button.dataset.vehicleSystem === id));
      qsa("[data-vehicle-node]").forEach((node) => node.classList.toggle("is-active", node.dataset.vehicleNode === id));
      qsa("[data-vehicle-status]").forEach((node) => (node.textContent = system.status));
      qsa("[data-vehicle-title]").forEach((node) => (node.textContent = system.title));
      qsa("[data-vehicle-description]").forEach((node) => (node.textContent = system.description));
      qsa("[data-vehicle-details]").forEach((node) => {
        node.innerHTML = system.details.map((detail) => `<li>${escapeHTML(detail)}</li>`).join("");
      });
    };

    qsa("[data-vehicle-system]").forEach((button) => {
      button.addEventListener("click", () => activate(button.dataset.vehicleSystem));
    });

    activate(data.vehicleSystems[0].id);
  };

  const initRouteAtlas = () => {
    const atlases = qsa(".route-atlas");
    if (!atlases.length || !data.routes) return;

    atlases.forEach((atlas) => {
      const controls = qs("[data-route-controls]", atlas);
      if (!controls) return;
      controls.innerHTML = data.routes
        .map((route, index) => `<button type="button" class="${index === 0 ? "is-active" : ""}" data-route="${escapeHTML(route.id)}">${escapeHTML(route.label)}</button>`)
        .join("");

      const activate = (id) => {
        const route = data.routes.find((item) => item.id === id);
        if (!route) return;
        qsa("[data-route]", atlas).forEach((button) => button.classList.toggle("is-active", button.dataset.route === id));
        qsa("[data-route-path]", atlas).forEach((path) => path.classList.toggle("is-active", path.dataset.routePath === id));
        qs("[data-route-title]", atlas).textContent = route.label;
        qs("[data-route-summary]", atlas).textContent = route.summary;
        qs("[data-route-points]", atlas).innerHTML = route.points.map((point) => `<span>${escapeHTML(point)}</span>`).join("");
      };

      controls.addEventListener("click", (event) => {
        const button = event.target.closest("[data-route]");
        if (button) activate(button.dataset.route);
      });
      activate(data.routes[0].id);
    });
  };

  const initJarvisLab = () => {
    const response = qs("[data-jarvis-response]");
    const prompts = qsa("[data-jarvis-prompt]");
    if (!response || !prompts.length) return;

    const answers = {
      "Pourquoi la lumière extérieure s'est-elle activée?":
        "Réponse simulée: la caméra d'entrée a classé un mouvement dans la zone piétonne. La lumière a été activée pour 90 secondes, puis l'événement a été marqué dans la timeline locale.",
      "Montre l'état des batteries du véhicule.":
        "Réponse simulée: batterie auxiliaire à 82 %, charge solaire faible, consommation stable. Le système recommande de limiter les charges secondaires si le véhicule reste arrêté toute la nuit.",
      "Prépare la maison pour mon arrivée.":
        "Réponse simulée: scène arrivée prête. Hall, climat, bureau et sécurité passent dans un état confortable sans exposer l'accès publiquement.",
      "Quelle caméra a détecté un mouvement?":
        "Réponse simulée: caméra garage, zone entrée. Objet classé personne. Aucun flux réel n'est connecté à cette démo publique.",
      "Est-ce que le serveur fonctionne normalement?":
        "Réponse simulée: services principaux disponibles, VPN actif, stockage OK. Une alerte serait créée si une ressource dépassait la marge définie.",
      "Crée un résumé énergétique.":
        "Réponse simulée: consommation basse depuis 2 h, aucune anomalie, prochains tests recommandés sur ventilation et charge batterie."
    };

    prompts.forEach((button) => {
      button.addEventListener("click", () => {
        prompts.forEach((item) => item.classList.toggle("is-active", item === button));
        response.textContent = answers[button.dataset.jarvisPrompt] || "Commande simulée prête.";
      });
    });
  };

  const renderLab = () => {
    const grid = qs("[data-lab-grid]");
    const filter = qs("[data-lab-filter]");
    if (!grid || !filter || !data.labSystems) return;

    const statuses = ["Tous", ...new Set(data.labSystems.map((item) => item.status))];
    filter.innerHTML = statuses
      .map((status, index) => `<button type="button" class="${index === 0 ? "is-active" : ""}" data-lab-status="${escapeHTML(status)}">${escapeHTML(status)}</button>`)
      .join("");

    const render = (status = "Tous") => {
      const items = status === "Tous" ? data.labSystems : data.labSystems.filter((item) => item.status === status);
      grid.innerHTML = items
        .map(
          (item) => `
            <article class="lab-card reveal">
              <span class="lab-status status-${escapeHTML(item.status)}">${escapeHTML(item.status)}</span>
              <h3>${escapeHTML(item.name)}</h3>
              <p>${escapeHTML(item.area)}</p>
            </article>
          `
        )
        .join("");
      initReveal();
    };

    filter.addEventListener("click", (event) => {
      const button = event.target.closest("[data-lab-status]");
      if (!button) return;
      qsa("button", filter).forEach((item) => item.classList.toggle("is-active", item === button));
      render(button.dataset.labStatus);
    });

    render();
  };

  const renderStack = () => {
    const root = qs("[data-stack-cloud]");
    if (!root || !data.stack) return;
    root.innerHTML = data.stack.map((item) => `<span>${escapeHTML(item)}</span>`).join("");
  };

  const renderProjects = () => {
    const grid = qs("[data-project-grid]");
    if (!grid || !data.projects) return;

    grid.innerHTML = data.projects
      .map(
        (project) => `
          <article class="project-card reveal">
            <span class="project-status">${escapeHTML(project.status)}</span>
            <h3>${escapeHTML(project.title)}</h3>
            <p><strong>${escapeHTML(project.type)}</strong></p>
            <p>${escapeHTML(project.problem)}</p>
            <details>
              <summary>Contraintes et résultat</summary>
              <ul>${project.constraints.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}</ul>
              <p>${escapeHTML(project.result)}</p>
            </details>
          </article>
        `
      )
      .join("");
  };

  const renderRoadmap = () => {
    const grid = qs("[data-roadmap-grid]");
    if (!grid || !data.roadmap) return;
    grid.innerHTML = data.roadmap
      .map(
        (item) => `
          <article class="roadmap-card reveal">
            <span class="project-status">${escapeHTML(item.status)}</span>
            <h3>${escapeHTML(item.title)}</h3>
            <p>${escapeHTML(item.note)}</p>
          </article>
        `
      )
      .join("");
  };

  const initContactForm = () => {
    const form = qs("[data-contact-form]");
    if (!form) return;
    const status = qs("[data-form-status]");

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const lines = [...formData.entries()].map(([key, value]) => `${key}: ${value || "-"}`);
      const subject = encodeURIComponent("Projet intelligent - jameslaplume.ca");
      const body = encodeURIComponent(lines.join("\n"));
      status.textContent = "Courriel préparé dans votre application mail.";
      window.location.href = `mailto:contact@jameslaplume.ca?subject=${subject}&body=${body}`;
    });
  };

  const initBatteryStatus = async () => {
    const grid = qs("[data-battery-grid]");
    if (!grid) return;

    const formatMetric = (value, unit) =>
      value === null || value === undefined ? "En attente" : `${escapeHTML(value)}${unit ? ` ${unit}` : ""}`;

    try {
      const response = await fetch("data/battery-status.json", { cache: "no-store" });
      if (!response.ok) throw new Error("battery status unavailable");
      const status = await response.json();
      qs("[data-battery-system]").textContent = status.gateway?.label || "Passerelle Bluetooth connectée";
      qs("[data-battery-updated]").textContent = status.updatedAt
        ? `Dernière lecture : ${new Date(status.updatedAt).toLocaleString("fr-CA")}`
        : "Télémétrie en initialisation";
      grid.innerHTML = status.batteries.map((battery, index) => `
        <article class="battery-card">
          <div class="battery-card-head">
            <div>
              <span>Batterie ${index + 1}</span>
              <h3>${escapeHTML(battery.name)}</h3>
            </div>
            <span class="battery-state ${battery.connected ? "is-online" : ""}">
              ${battery.connected ? "En ligne" : "Détectée"}
            </span>
          </div>
          <div class="battery-charge" style="--charge:${Number(battery.soc || 0)}%">
            <strong>${formatMetric(battery.soc, "%")}</strong>
            <span><i></i></span>
          </div>
          <dl class="battery-metrics">
            <div><dt>Tension</dt><dd>${formatMetric(battery.voltage, "V")}</dd></div>
            <div><dt>Courant</dt><dd>${formatMetric(battery.current, "A")}</dd></div>
            <div><dt>Puissance</dt><dd>${formatMetric(battery.power, "W")}</dd></div>
            <div><dt>Température</dt><dd>${formatMetric(battery.temperature, "°C")}</dd></div>
          </dl>
          <p>${escapeHTML(battery.model)}</p>
        </article>
      `).join("");
    } catch (error) {
      grid.innerHTML = '<p class="battery-error">Les batteries sont détectées; la publication des mesures est en cours de branchement.</p>';
    }
  };

  const run = () => {
    initHeader();
    renderServices();
    renderSolutions();
    renderProcess();
    renderArticlePreview();
    renderArticleList();
    initDialogs();
    initScenarioDemo();
    initDashboardDemo();
    initSecurityDemo();
    initVehicleDemo();
    initRouteAtlas();
    initJarvisLab();
    renderLab();
    renderStack();
    renderProjects();
    renderRoadmap();
    initBatteryStatus();
    initContactForm();
    refreshIcons();
    initReveal();
  };

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
