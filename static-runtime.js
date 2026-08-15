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

  const tradingRoot = document.querySelector(".trading-live-shell");
  if (tradingRoot) {
    const apiUrl = "https://jameslaplume-jarvis.jlap1321.chatgpt.site/api/trading/public";
    const locale = isEnglish ? "en-CA" : "fr-CA";
    const usd = new Intl.NumberFormat(locale, { style: "currency", currency: "USD", maximumFractionDigits: 2 });
    const price = new Intl.NumberFormat(locale, { style: "currency", currency: "USD", maximumFractionDigits: 0 });
    const number = new Intl.NumberFormat(locale, { maximumFractionDigits: 6 });
    let latestReceivedAt = "";
    let latestSnapshot = null;

    const value = (selector, text) => {
      const element = tradingRoot.querySelector(selector);
      if (element) element.textContent = text;
    };

    const actionLabel = (action) => action === "BUY"
      ? (isEnglish ? "BUY" : "ACHETER")
      : action === "SELL"
        ? (isEnglish ? "SELL" : "VENDRE")
        : (isEnglish ? "WAIT" : "ATTENDRE");

    const drawEquity = (points) => {
      const canvas = tradingRoot.querySelector(".trading-equity-canvas");
      if (!(canvas instanceof HTMLCanvasElement)) return;
      const rect = canvas.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(1, Math.floor(rect.width * ratio));
      canvas.height = Math.max(1, Math.floor(rect.height * ratio));
      const context = canvas.getContext("2d");
      if (!context) return;
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      context.clearRect(0, 0, rect.width, rect.height);
      const visible = (Array.isArray(points) ? points : []).slice(-240);
      if (visible.length < 2) {
        context.fillStyle = "rgba(241,238,230,.42)";
        context.font = "12px Arial";
        context.fillText(isEnglish ? "The curve will appear after the first readings." : "La courbe apparaîtra après les premiers relevés.", 18, rect.height / 2);
        return;
      }
      const values = visible.map((point) => point.equityUsd);
      const minimum = Math.min(...values);
      const maximum = Math.max(...values);
      const spread = Math.max(maximum - minimum, 1);
      const padding = 22;
      context.strokeStyle = "rgba(241,238,230,.10)";
      context.lineWidth = 1;
      for (let line = 1; line < 4; line += 1) {
        const y = rect.height / 4 * line;
        context.beginPath(); context.moveTo(0, y); context.lineTo(rect.width, y); context.stroke();
      }
      const x = (index) => padding + index / (visible.length - 1) * (rect.width - padding * 2);
      const y = (amount) => padding + (maximum - amount) / spread * (rect.height - padding * 2);
      const positive = values.at(-1) >= values[0];
      const gradient = context.createLinearGradient(0, 0, 0, rect.height);
      gradient.addColorStop(0, positive ? "rgba(98,191,255,.28)" : "rgba(231,116,104,.25)");
      gradient.addColorStop(1, "rgba(98,191,255,0)");
      context.beginPath();
      visible.forEach((point, index) => index ? context.lineTo(x(index), y(point.equityUsd)) : context.moveTo(x(index), y(point.equityUsd)));
      context.lineTo(x(visible.length - 1), rect.height - padding); context.lineTo(x(0), rect.height - padding); context.closePath();
      context.fillStyle = gradient; context.fill();
      context.beginPath();
      visible.forEach((point, index) => index ? context.lineTo(x(index), y(point.equityUsd)) : context.moveTo(x(index), y(point.equityUsd)));
      context.strokeStyle = positive ? "#62bfff" : "#e77468"; context.lineWidth = 2; context.stroke();
    };

    const renderTrading = (snapshot, receivedAtUtc) => {
      latestSnapshot = snapshot;
      latestReceivedAt = receivedAtUtc || snapshot.observedAtUtc;
      const decision = tradingRoot.querySelector(".trading-decision-card");
      const decisionStrong = decision?.querySelector(":scope > strong");
      if (decisionStrong) {
        decisionStrong.textContent = actionLabel(snapshot.robotAction);
        decisionStrong.className = "action-" + snapshot.robotAction.toLowerCase();
      }
      const decisionReason = decision?.querySelector(":scope > p");
      if (decisionReason) decisionReason.textContent = snapshot.decisionReason;
      const decisionDetails = decision?.querySelectorAll("dd") || [];
      if (decisionDetails[0]) decisionDetails[0].textContent = snapshot.rawSignal;
      if (decisionDetails[1]) decisionDetails[1].textContent = snapshot.decisionStatus;
      if (decisionDetails[2]) decisionDetails[2].textContent = snapshot.strategyVersion;

      const gate = tradingRoot.querySelector(".trading-automation-gate");
      if (gate) {
        gate.className = "trading-automation-gate " + (snapshot.automationReady ? "ready" : "locked");
        const gateTitle = gate.querySelector("b");
        const gateCopy = gate.querySelector("p");
        if (gateTitle) gateTitle.textContent = snapshot.automationReady
          ? (isEnglish ? "AUTOMATION VALIDATED" : "AUTOMATISATION VALIDÉE")
          : (isEnglish ? "ROBOT LOCKED" : "ROBOT VERROUILLÉ");
        if (gateCopy) gateCopy.textContent = snapshot.automationReady
          ? (isEnglish ? "Quantitative criteria allow automatic paper trading." : "Les critères quantitatifs autorisent la simulation automatique.")
          : (snapshot.automationBlockers?.[0] || (isEnglish ? "Out-of-sample validation is incomplete." : "Validation hors échantillon incomplète."));
      }

      value(".trading-price-card strong", snapshot.lastPriceUsd > 0 ? price.format(snapshot.lastPriceUsd) : "—");
      value(".trading-price-card p", snapshot.historyBarCount.toLocaleString(locale) + (isEnglish ? " accumulated candles" : " chandelles cumulées"));

      const kpis = tradingRoot.querySelectorAll(".trading-kpis article");
      if (kpis[0]) kpis[0].querySelector("strong").textContent = usd.format(snapshot.equityUsd);
      if (kpis[1]) {
        const klass = snapshot.totalPnlUsd > 0 ? "positive" : snapshot.totalPnlUsd < 0 ? "negative" : "";
        const strong = kpis[1].querySelector("strong"); const small = kpis[1].querySelector("small");
        if (strong) { strong.textContent = usd.format(snapshot.totalPnlUsd); strong.className = klass; }
        if (small) { small.textContent = snapshot.totalReturnPct.toFixed(2) + " %"; small.className = klass; }
      }
      if (kpis[2]) {
        kpis[2].querySelector("strong").textContent = number.format(snapshot.btcQuantity) + " BTC";
        const opened = snapshot.positionOpenedAtUtc ? new Date(snapshot.positionOpenedAtUtc).toLocaleString(locale, { dateStyle: "short", timeStyle: "short" }) : "";
        kpis[2].querySelector("small").textContent = snapshot.averageEntryPriceUsd
          ? (isEnglish ? "Bought " : "Acheté ") + price.format(snapshot.averageEntryPriceUsd) + (opened ? " · " + opened : "")
          : (isEnglish ? "No open position" : "Aucune position");
      }
      if (kpis[3]) {
        kpis[3].querySelector("strong").textContent = usd.format(snapshot.feesPaidUsd);
        kpis[3].querySelector("small").textContent = snapshot.completedTrades + (isEnglish ? " completed trade(s)" : " trade(s) terminé(s)");
      }

      value(".trading-chart-card header strong", usd.format(snapshot.equityUsd));
      drawEquity(snapshot.points);
      const riskRows = tradingRoot.querySelectorAll(".trading-risk-card > div b");
      const riskValues = [
        "-" + Math.abs(snapshot.maxDrawdownPct).toFixed(2) + " %",
        snapshot.estimatedRoundTripCostPct.toFixed(2) + " %",
        snapshot.maxAllocationPct.toFixed(0) + " %",
        usd.format(snapshot.positionMarketValueUsd),
        snapshot.breakevenPriceUsd ? price.format(snapshot.breakevenPriceUsd) : "—",
        snapshot.stopLossUsd ? price.format(snapshot.stopLossUsd) : "—",
        snapshot.takeProfitUsd ? price.format(snapshot.takeProfitUsd) : "—",
      ];
      riskRows.forEach((row, index) => { if (riskValues[index] !== undefined) row.textContent = riskValues[index]; });
      value(".trading-risk-card > small", snapshot.costProfile);

      const journal = tradingRoot.querySelector(".trading-journal");
      const events = Array.isArray(snapshot.events) ? snapshot.events.slice().reverse().slice(0, 12) : [];
      const count = journal?.querySelector("header > span");
      if (count) count.textContent = events.length + (isEnglish ? " published operation(s)" : " opération(s) publiée(s)");
      const oldList = journal?.querySelector(".trading-event-list, .trading-empty");
      if (oldList && journal) {
        const container = document.createElement(events.length ? "div" : "p");
        container.className = events.length ? "trading-event-list" : "trading-empty";
        if (!events.length) container.textContent = isEnglish
          ? "No paper buy or sell has been published yet. The robot continues to analyze every new candle."
          : "Aucun achat ou vente fictif publié pour le moment. Le robot continue d’analyser chaque nouvelle chandelle.";
        events.forEach((event) => {
          const row = document.createElement("article");
          const cells = [
            ["time", new Date(event.observedAtUtc).toLocaleString(locale, { dateStyle: "short", timeStyle: "short" })],
            ["strong", event.action], ["span", number.format(event.quantityBtc) + " BTC"],
            ["span", price.format(event.priceUsd)], ["span", (isEnglish ? "Fees " : "Frais ") + usd.format(event.feesUsd)],
            ["p", event.reason],
          ];
          cells.forEach(([tag, text]) => { const cell = document.createElement(tag); cell.textContent = text; if (tag === "strong") cell.className = "action-" + event.action.toLowerCase(); row.appendChild(cell); });
          container.appendChild(row);
        });
        oldList.replaceWith(container);
      }
    };

    const updateConnection = () => {
      const connection = tradingRoot.querySelector(".trading-connection");
      const age = latestReceivedAt ? Math.max(0, Math.round((Date.now() - Date.parse(latestReceivedAt)) / 1000)) : null;
      const live = Boolean(latestSnapshot && age !== null && age <= 45 && latestSnapshot.dataState === "FRESH");
      if (connection) connection.className = "trading-connection " + (live ? "live" : "waiting");
      value(".trading-connection b", live ? (isEnglish ? "LIVE DATA" : "DONNÉES EN DIRECT") : (isEnglish ? "SECURE CONNECTION" : "CONNEXION SÉCURISÉE"));
      value(".trading-connection small", age !== null ? (isEnglish ? "Received " : "Reçu il y a ") + age + " s" : (isEnglish ? "Awaiting first publish" : "Premier envoi en attente"));
    };

    const loadTrading = async () => {
      try {
        const response = await fetch(apiUrl, { cache: "no-store", mode: "cors" });
        const payload = await response.json();
        if (!response.ok || !payload.available || !payload.snapshot) throw new Error("Trading data unavailable");
        renderTrading(payload.snapshot, payload.receivedAtUtc);
      } catch {
        latestSnapshot = null;
      }
      updateConnection();
    };

    loadTrading();
    window.setInterval(loadTrading, 10_000);
    window.setInterval(updateConnection, 1_000);
    window.addEventListener("resize", () => latestSnapshot && drawEquity(latestSnapshot.points));
  }
})();
