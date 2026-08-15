(() => {
  const main = document.querySelector("main");
  const isEnglish = main?.getAttribute("lang")?.startsWith("en") || document.documentElement.lang.startsWith("en");

  const menuButton = document.querySelector(".nav-toggle");
  const navigation = document.querySelector("#primary-nav");
  menuButton?.addEventListener("click", () => {
    const open = navigation?.classList.toggle("open") ?? false;
    menuButton.setAttribute("aria-expanded", String(open));
  });
  navigation?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => navigation.classList.remove("open")));

  const diagnostic = {
    fr: [
      ["Signal", "14:32:18", "Caméra arrière inaccessible.", "Le flux vidéo cesse. JARVIS vérifie les dépendances avant de conclure."],
      ["Contexte", "14:32:21", "Le réseau répond toujours.", "Le switch et le routeur sont joignables. La tension du circuit arrière chute au même moment."],
      ["Hypothèse", "14:32:24", "Perte d’alimentation locale probable.", "L’hypothèse simulée est classée devant la panne caméra et l’incident réseau."],
      ["Test sûr", "14:32:27", "Mesurer avant de redémarrer.", "Vérifier la tension au connecteur, puis le fusible. Aucune action critique sans confirmation."],
    ],
    en: [
      ["Signal", "14:32:18", "Rear camera unavailable.", "The video stream stops. JARVIS checks dependencies before drawing a conclusion."],
      ["Context", "14:32:21", "The network is still responding.", "The switch and router are reachable. Rear circuit voltage drops at the same time."],
      ["Hypothesis", "14:32:24", "Local power loss is probable.", "The simulated hypothesis ranks ahead of a camera failure or network incident."],
      ["Safe test", "14:32:27", "Measure before restarting.", "Check voltage at the connector, then the fuse. No critical action without confirmation."],
    ],
  };

  const demoButtons = [...document.querySelectorAll(".demo-tabs button")];
  const demoCopy = document.querySelector(".demo-copy");
  demoButtons.forEach((button, index) => button.addEventListener("click", () => {
    const item = diagnostic[isEnglish ? "en" : "fr"][index];
    demoButtons.forEach((candidate, candidateIndex) => {
      candidate.classList.toggle("active", candidateIndex === index);
      candidate.setAttribute("aria-selected", String(candidateIndex === index));
    });
    const progress = document.querySelector(".progress-step");
    if (progress) progress.className = "progress-step p" + (index + 1);
    if (demoCopy) {
      const time = demoCopy.querySelector("div b");
      const label = demoCopy.querySelector(":scope > p");
      const title = demoCopy.querySelector("h3");
      const detail = demoCopy.querySelector("small");
      if (time) time.textContent = item[1];
      if (label) label.textContent = item[0];
      if (title) title.textContent = item[2];
      if (detail) detail.textContent = item[3];
    }
  }));

  const systems = {
    fr: [
      ["Énergie", "Solaire, batteries, alternateur et charges deviennent un seul système observable.", "Tension · courant · état de charge · production · alarmes"],
      ["Caméras", "L’état des flux et du stockage est relié aux événements et aux autres dépendances.", "Disponibilité · détection · stockage · événements"],
      ["Sécurité", "Les portes, caméras et accès locaux sont documentés sans exposer le véhicule sur Internet.", "Accès · zones · événements · historique"],
      ["Climat", "Chauffage, ventilation et température sont compris avec leur consommation et leur contexte.", "Consigne · température · état · consommation"],
      ["Réseau", "Routeur, VPN, serveur local et appareils restent visibles, même lorsque le lien externe change.", "WAN · DNS · VPN · clients · bascule"],
      ["Automatisation", "Home Assistant exécute les scènes; JARVIS explique, recommande et respecte les permissions.", "Scènes · relais · interfaces · journal"],
      ["Twin", "Le futur jumeau numérique reliera les dépendances, la chronologie et les réparations confirmées.", "Concept · prototype · développement planifié"],
    ],
    en: [
      ["Energy", "Solar, batteries, alternator, and loads become one observable system.", "Voltage · current · state of charge · production · alerts"],
      ["Cameras", "Stream and storage health connect to events and the surrounding dependencies.", "Availability · detection · storage · events"],
      ["Security", "Doors, cameras, and local access are documented without exposing the vehicle to the Internet.", "Access · zones · events · history"],
      ["Climate", "Heating, ventilation, and temperature are understood with consumption and context.", "Setpoint · temperature · state · consumption"],
      ["Network", "Router, VPN, local server, and devices stay visible as the external link changes.", "WAN · DNS · VPN · clients · failover"],
      ["Automation", "Home Assistant runs scenes; JARVIS explains, recommends, and respects permissions.", "Scenes · relays · interfaces · logs"],
      ["Twin", "The future digital twin will connect dependencies, timelines, and confirmed repairs.", "Concept · prototype · planned development"],
    ],
  };

  const systemButtons = [...document.querySelectorAll(".systems-nav button")];
  const systemDetail = document.querySelector(".system-detail");
  systemButtons.forEach((button, index) => button.addEventListener("click", () => {
    const item = systems[isEnglish ? "en" : "fr"][index];
    systemButtons.forEach((candidate, candidateIndex) => {
      candidate.classList.toggle("active", candidateIndex === index);
      candidate.setAttribute("aria-selected", String(candidateIndex === index));
    });
    if (systemDetail) {
      const title = systemDetail.querySelector("h3");
      const copy = systemDetail.querySelector("p");
      const details = systemDetail.querySelector("small");
      if (title) title.textContent = item[0];
      if (copy) copy.textContent = item[1];
      if (details) details.textContent = item[2];
    }
  }));

  const initBatteryTelemetry = async () => {
    if (isEnglish || !document.querySelector(".home-hero")) return;
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = "/battery-live.css";
    document.head.appendChild(stylesheet);

    const section = document.createElement("section");
    section.className = "battery-live-section";
    section.id = "batteries";
    section.innerHTML = `<div class="battery-live-heading"><p class="section-label">Premier signal réel</p><h2>Deux batteries. Un système qui commence à parler.</h2><p>Les deux BMS JBD du véhicule sont détectés par la passerelle Bluetooth Waveshare. Cette vue publique reste limitée aux mesures utiles et ne donne aucun accès au réseau privé.</p></div><div class="battery-system-bar"><i aria-hidden="true"></i><b data-battery-gateway>Waveshare ESP32 · Bluetooth connecté</b><span data-battery-updated>Télémétrie en initialisation</span></div><div class="battery-live-grid" data-battery-grid aria-live="polite"></div><p class="battery-privacy">Charge, tension, courant, puissance et température seulement. Aucun jeton Home Assistant, adresse privée, contrôle ou identifiant Bluetooth n’est publié.</p>`;
    document.querySelector(".services-preview")?.before(section);
    const grid = section.querySelector("[data-battery-grid]");
    const metric = (value, unit) => value == null ? "En attente" : `${value} ${unit}`;
    try {
      const response = await fetch("/data/battery-status.json", { cache: "no-store" });
      if (!response.ok) throw new Error("battery telemetry unavailable");
      const status = await response.json();
      section.querySelector("[data-battery-gateway]").textContent = status.gateway;
      section.querySelector("[data-battery-updated]").textContent = status.updatedAt ? `Dernière lecture : ${new Date(status.updatedAt).toLocaleString("fr-CA")}` : "Télémétrie en initialisation";
      grid.innerHTML = status.batteries.map((battery, index) => `<article class="battery-live-card"><header><div><span>Batterie ${index + 1}</span><h3>${battery.name}</h3></div><em class="battery-state ${battery.connected ? "online" : ""}">${battery.connected ? "En ligne" : "Détectée"}</em></header><div class="battery-soc" style="--soc:${Number(battery.soc || 0)}%"><strong>${metric(battery.soc, "%")}</strong><span><i></i></span></div><dl class="battery-metrics"><div><dt>Tension</dt><dd>${metric(battery.voltage, "V")}</dd></div><div><dt>Courant</dt><dd>${metric(battery.current, "A")}</dd></div><div><dt>Puissance</dt><dd>${metric(battery.power, "W")}</dd></div><div><dt>Température</dt><dd>${metric(battery.temperature, "°C")}</dd></div></dl><p>${battery.model}</p></article>`).join("");
    } catch (error) {
      grid.innerHTML = '<p class="battery-live-error">Les batteries sont détectées; la publication des mesures est en cours de branchement.</p>';
    }
  };

  initBatteryTelemetry();

  const form = document.querySelector(".pilot-form");
  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const subject = isEnglish ? "JARVIS Twin pilot application" : "Candidature pilote JARVIS Twin";
    const labels = isEnglish
      ? { name: "Name", organization: "Organization", email: "Email", environmentType: "Environment", currentProblem: "Current problem", systemsInstalled: "Installed systems", desiredOutcome: "Desired outcome" }
      : { name: "Nom", organization: "Organisation", email: "Courriel", environmentType: "Environnement", currentProblem: "Problème actuel", systemsInstalled: "Systèmes installés", desiredOutcome: "Résultat recherché" };
    const body = Object.entries(labels).map(([key, label]) => label + ": " + (data.get(key) || "—")).join("\n\n");
    const status = form.querySelector(".form-submit p");
    if (status) status.textContent = isEnglish ? "Your email application is ready to send." : "Votre candidature par courriel est prête à envoyer.";
    window.location.href = "mailto:contact@jameslaplume.ca?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  });
})();
