const year = document.querySelector("[data-year]");
const header = document.querySelector("[data-header]");
const langButtons = document.querySelectorAll("[data-lang]");
const demo = document.querySelector("[data-demo]");
const demoButtons = document.querySelectorAll("[data-mode]");
const routeMap = document.querySelector("[data-route-map]");
const routeButtons = document.querySelectorAll("[data-route]");
const routeTitle = document.querySelector("[data-route-title]");
const routeCopy = document.querySelector("[data-route-copy]");
const contactForm = document.querySelector("[data-contact-form]");
const formStatus = document.querySelector("[data-form-status]");

let currentLang = localStorage.getItem("site-language") || "fr";
let currentDemoMode = "home";
let currentRoute = "florida";

const translations = {
  fr: {
    "nav.positioning": "Smart systems studio",
    "nav.services": "Services",
    "nav.demo": "Demo",
    "nav.ambulance": "Ambulance",
    "nav.journal": "Journal",
    "nav.contact": "Contact",
    "hero.eyebrow": "Studio de systèmes intelligents",
    "hero.positioning": "Smart spaces. Private systems. Real automation.",
    "hero.text":
      "Des systèmes sur mesure pour maisons intelligentes, serveurs privés, caméras locales, vans connectés et tableaux de bord qui servent vraiment.",
    "hero.cta.primary": "Parler d'un projet",
    "hero.cta.secondary": "Voir la démo",
    "hero.panel.title": "Architecture privée",
    "hero.panel.item1.label": "Contrôle",
    "hero.panel.item1.value": "Local d'abord",
    "hero.panel.item2.label": "Accès",
    "hero.panel.item2.value": "VPN privé",
    "hero.panel.item3.label": "Approche",
    "hero.panel.item3.value": "Pilotes et systèmes custom",
    "services.kicker": "Services",
    "services.title": "Des espaces qui comprennent ce qui se passe.",
    "services.text":
      "Le travail commence par des besoins réels: voir, contrôler, automatiser, sécuriser et garder les données proches de vous.",
    "service.home.title": "Maisons intelligentes",
    "service.home.text":
      "Home Assistant, capteurs, éclairage, énergie, présence, scènes et interfaces simples pour les routines quotidiennes.",
    "service.vision.title": "Vision et sécurité locale",
    "service.vision.text":
      "Caméras IP, Frigate, détection locale, alertes propres et accès privé sans transformer la maison en produit cloud.",
    "service.private.title": "Serveurs et accès privé",
    "service.private.text":
      "Docker, Linux, sauvegardes, DNS, VPN, accès distant et bases fiables pour héberger vos propres outils.",
    "service.mobile.title": "Vans, RV et systèmes mobiles",
    "service.mobile.text":
      "Énergie, réseau, surveillance, tableaux de bord et automatisation pour véhicules aménagés, ateliers mobiles et projets pilotes.",
    "demo.kicker": "Démonstration",
    "demo.title": "Un système intelligent doit rester lisible.",
    "demo.text":
      "Cette démonstration montre comment les capteurs, caméras, serveurs et dashboards peuvent être organisés autour d'une logique claire.",
    "demo.mode.home": "Résidence",
    "demo.mode.vision": "Vision",
    "demo.mode.server": "Serveur",
    "demo.mode.mobile": "Mobile",
    "demo.readout.label": "Scénario",
    "ambulance.kicker": "Projet en vedette",
    "ambulance.title": "Connected Ambulance: un laboratoire mobile pour vrais systèmes.",
    "ambulance.text":
      "Un projet pilote personnel autour d'une ambulance connectée: énergie, réseau, caméras, accès VPN, interfaces embarquées et automatisations pensées pour bouger.",
    "ambulance.card.title": "Ce que le projet explore",
    "ambulance.card.item1": "Réseau embarqué et accès VPN privé.",
    "ambulance.card.item2": "Caméras et vision locale pour surveillance autour du véhicule.",
    "ambulance.card.item3": "Dashboard pour énergie, état, température et alertes.",
    "ambulance.card.item4": "Base technique réutilisable pour vans, RV et ateliers mobiles.",
    "routes.kicker": "Carte terrain",
    "routes.title": "Routes, essais et idées mobiles.",
    "routes.text":
      "Une carte stylisée des trajets qui inspirent les systèmes mobiles: longues routes, retours par les États-Unis, vols, boucles locales et arrivée vers Montréal.",
    "route.florida.short": "Floride",
    "route.bc.short": "BC + nord USA",
    "route.california.short": "Californie",
    "route.hawaii.short": "Hawaii",
    "route.costa.short": "Costa Rica + Caraïbes",
    "process.kicker": "Processus",
    "process.title": "Une méthode simple en cinq étapes.",
    "process.step1.title": "Clarifier le besoin",
    "process.step1.text": "Ce qui doit être vu, contrôlé, automatisé ou protégé.",
    "process.step2.title": "Cartographier le système",
    "process.step2.text": "Réseau, appareils, capteurs, permissions et contraintes physiques.",
    "process.step3.title": "Construire un pilote",
    "process.step3.text": "Un prototype limité, testable et compréhensible avant de grossir.",
    "process.step4.title": "Déployer proprement",
    "process.step4.text": "Documentation, accès, sauvegardes et interfaces utilisables.",
    "process.step5.title": "Améliorer sur le terrain",
    "process.step5.text": "Ajustements après usage réel, pas seulement après un plan parfait.",
    "journal.kicker": "Journal technique",
    "journal.title": "Notes ouvertes sur les expériences en cours.",
    "journal.text":
      "Pas de fausses études de cas. Le journal sert à documenter les essais, pilotes et décisions techniques au fur et à mesure.",
    "journal.item1.tag": "Pilote",
    "journal.item1.title": "Ambulance connectée",
    "journal.item1.text":
      "Réseau mobile, caméras, dashboard et accès privé dans un véhicule qui doit rester utilisable hors du garage.",
    "journal.item2.tag": "Expérience",
    "journal.item2.title": "Vision locale avec Frigate",
    "journal.item2.text":
      "Détection locale, zones utiles, alertes propres et stockage maîtrisé pour éviter la dépendance au cloud.",
    "journal.item3.tag": "Infrastructure",
    "journal.item3.title": "Serveur privé et VPN",
    "journal.item3.text":
      "Héberger des services, exposer le minimum, sauvegarder les données et garder un accès distant clair.",
    "stack.kicker": "Stack",
    "stack.title": "Technologies possibles selon le projet.",
    "stack.text":
      "La stack n'est pas une religion. Elle se choisit selon le budget, la fiabilité requise, la confidentialité et la maintenance.",
    "contact.kicker": "Contact",
    "contact.title": "Un projet pilote ou un système custom?",
    "contact.text":
      "Décrivez ce que vous voulez connecter, automatiser ou sécuriser. Le formulaire prépare un courriel; rien n'est envoyé sans votre app de mail.",
    "form.name": "Nom",
    "form.email": "Courriel",
    "form.project": "Type de projet",
    "form.project.home": "Maison intelligente",
    "form.project.camera": "Caméras et Frigate",
    "form.project.server": "Serveur privé / VPN",
    "form.project.mobile": "Van, RV ou système mobile",
    "form.project.other": "Autre système custom",
    "form.message": "Message",
    "form.placeholder": "Parlez-moi du lieu, des appareils, du problème et du résultat voulu.",
    "form.submit": "Préparer le courriel",
    "form.status": "Courriel préparé dans votre application de mail.",
    "footer.top": "Retour en haut"
  },
  en: {
    "nav.positioning": "Smart systems studio",
    "nav.services": "Services",
    "nav.demo": "Demo",
    "nav.ambulance": "Ambulance",
    "nav.journal": "Journal",
    "nav.contact": "Contact",
    "hero.eyebrow": "Smart systems studio",
    "hero.positioning": "Smart spaces. Private systems. Real automation.",
    "hero.text":
      "Custom systems for smart homes, private servers, local cameras, connected vans and dashboards that are actually useful.",
    "hero.cta.primary": "Discuss a project",
    "hero.cta.secondary": "View the demo",
    "hero.panel.title": "Private architecture",
    "hero.panel.item1.label": "Control",
    "hero.panel.item1.value": "Local first",
    "hero.panel.item2.label": "Access",
    "hero.panel.item2.value": "Private VPN",
    "hero.panel.item3.label": "Approach",
    "hero.panel.item3.value": "Pilots and custom systems",
    "services.kicker": "Services",
    "services.title": "Spaces that understand what is happening.",
    "services.text":
      "The work starts with real needs: seeing, controlling, automating, securing and keeping data close to you.",
    "service.home.title": "Smart homes",
    "service.home.text":
      "Home Assistant, sensors, lighting, energy, presence, scenes and simple interfaces for everyday routines.",
    "service.vision.title": "Local vision and security",
    "service.vision.text":
      "IP cameras, Frigate, local detection, clean alerts and private access without turning the home into a cloud product.",
    "service.private.title": "Servers and private access",
    "service.private.text":
      "Docker, Linux, backups, DNS, VPN, remote access and reliable foundations for hosting your own tools.",
    "service.mobile.title": "Vans, RVs and mobile systems",
    "service.mobile.text":
      "Energy, networking, monitoring, dashboards and automation for converted vehicles, mobile workshops and pilot projects.",
    "demo.kicker": "Demonstration",
    "demo.title": "A smart system should stay readable.",
    "demo.text":
      "This demo shows how sensors, cameras, servers and dashboards can be organized around clear logic.",
    "demo.mode.home": "Residence",
    "demo.mode.vision": "Vision",
    "demo.mode.server": "Server",
    "demo.mode.mobile": "Mobile",
    "demo.readout.label": "Scenario",
    "ambulance.kicker": "Featured project",
    "ambulance.title": "Connected Ambulance: a mobile lab for real systems.",
    "ambulance.text":
      "A personal pilot project around a connected ambulance: energy, networking, cameras, VPN access, onboard interfaces and automation designed to move.",
    "ambulance.card.title": "What the project explores",
    "ambulance.card.item1": "Onboard networking and private VPN access.",
    "ambulance.card.item2": "Cameras and local vision for vehicle-side awareness.",
    "ambulance.card.item3": "Dashboard for energy, status, temperature and alerts.",
    "ambulance.card.item4": "Reusable technical base for vans, RVs and mobile workshops.",
    "routes.kicker": "Field map",
    "routes.title": "Routes, testing and mobile ideas.",
    "routes.text":
      "A stylized map of routes that inspire mobile systems: long drives, returns through the United States, flights, local loops and arrival back toward Montreal.",
    "route.florida.short": "Florida",
    "route.bc.short": "BC + north USA",
    "route.california.short": "California",
    "route.hawaii.short": "Hawaii",
    "route.costa.short": "Costa Rica + Caribbean",
    "process.kicker": "Process",
    "process.title": "A simple five-step method.",
    "process.step1.title": "Clarify the need",
    "process.step1.text": "What needs to be seen, controlled, automated or protected.",
    "process.step2.title": "Map the system",
    "process.step2.text": "Network, devices, sensors, permissions and physical constraints.",
    "process.step3.title": "Build a pilot",
    "process.step3.text": "A limited, testable and understandable prototype before scaling.",
    "process.step4.title": "Deploy cleanly",
    "process.step4.text": "Documentation, access, backups and usable interfaces.",
    "process.step5.title": "Improve in the field",
    "process.step5.text": "Adjustments after real use, not just after a perfect plan.",
    "journal.kicker": "Technical journal",
    "journal.title": "Open notes on work in progress.",
    "journal.text":
      "No fake case studies. The journal documents experiments, pilots and technical decisions over time.",
    "journal.item1.tag": "Pilot",
    "journal.item1.title": "Connected ambulance",
    "journal.item1.text":
      "Mobile network, cameras, dashboard and private access inside a vehicle that has to stay useful away from the garage.",
    "journal.item2.tag": "Experiment",
    "journal.item2.title": "Local vision with Frigate",
    "journal.item2.text":
      "Local detection, useful zones, clean alerts and controlled storage to avoid cloud dependence.",
    "journal.item3.tag": "Infrastructure",
    "journal.item3.title": "Private server and VPN",
    "journal.item3.text":
      "Host services, expose the minimum, back up data and keep remote access understandable.",
    "stack.kicker": "Stack",
    "stack.title": "Possible technologies depending on the project.",
    "stack.text":
      "The stack is not a religion. It is chosen around budget, reliability, privacy and maintenance.",
    "contact.kicker": "Contact",
    "contact.title": "A pilot project or custom system?",
    "contact.text":
      "Describe what you want to connect, automate or secure. The form prepares an email; nothing is sent without your mail app.",
    "form.name": "Name",
    "form.email": "Email",
    "form.project": "Project type",
    "form.project.home": "Smart home",
    "form.project.camera": "Cameras and Frigate",
    "form.project.server": "Private server / VPN",
    "form.project.mobile": "Van, RV or mobile system",
    "form.project.other": "Other custom system",
    "form.message": "Message",
    "form.placeholder": "Tell me about the place, devices, problem and desired outcome.",
    "form.submit": "Prepare email",
    "form.status": "Email prepared in your mail application.",
    "footer.top": "Back to top"
  }
};

const demoModes = {
  fr: {
    home: {
      title: "Résidence privée",
      copy:
        "Capteurs de présence, éclairage, température, énergie et scènes Home Assistant avec logique locale.",
      nodes: ["Capteurs", "Automations", "Serveur", "Dashboard"],
      signals: ["Présence et luminosité", "Énergie et climat", "Scènes simples", "Contrôle local"]
    },
    vision: {
      title: "Caméras et Frigate",
      copy:
        "Détection locale, zones utiles, alertes filtrées et accès privé aux événements importants.",
      nodes: ["Caméras", "Frigate", "Stockage", "Alertes"],
      signals: ["Détection locale", "Zones configurées", "Événements pertinents", "Accès privé"]
    },
    server: {
      title: "Serveur privé",
      copy:
        "Services Docker, sauvegardes, accès VPN et tableaux de bord sans exposer plus que nécessaire.",
      nodes: ["VPN", "Services", "Backup", "Monitoring"],
      signals: ["Accès distant", "Sauvegardes", "DNS propre", "Surface réduite"]
    },
    mobile: {
      title: "Système mobile",
      copy:
        "Réseau embarqué, énergie, caméras et dashboard pour van, RV ou laboratoire mobile.",
      nodes: ["Énergie", "Réseau", "Vision", "Route"],
      signals: ["État batterie", "Lien mobile", "Caméras autour", "Mode hors ligne"]
    }
  },
  en: {
    home: {
      title: "Private residence",
      copy:
        "Presence sensors, lighting, temperature, energy and Home Assistant scenes with local logic.",
      nodes: ["Sensors", "Automation", "Server", "Dashboard"],
      signals: ["Presence and light", "Energy and climate", "Simple scenes", "Local control"]
    },
    vision: {
      title: "Cameras and Frigate",
      copy:
        "Local detection, useful zones, filtered alerts and private access to important events.",
      nodes: ["Cameras", "Frigate", "Storage", "Alerts"],
      signals: ["Local detection", "Configured zones", "Relevant events", "Private access"]
    },
    server: {
      title: "Private server",
      copy:
        "Docker services, backups, VPN access and dashboards without exposing more than needed.",
      nodes: ["VPN", "Services", "Backup", "Monitoring"],
      signals: ["Remote access", "Backups", "Clean DNS", "Reduced exposure"]
    },
    mobile: {
      title: "Mobile system",
      copy:
        "Onboard networking, energy, cameras and dashboard for a van, RV or mobile lab.",
      nodes: ["Energy", "Network", "Vision", "Route"],
      signals: ["Battery state", "Mobile link", "Perimeter cameras", "Offline mode"]
    }
  }
};

const routeData = {
  fr: {
    florida: {
      title: "Floride aller-retour",
      copy:
        "Long trajet routier vers la Floride et retour: parfait pour penser alimentation, réseau mobile, caméra et accès distant."
    },
    bc: {
      title: "BC et retour par le nord des USA",
      copy:
        "Grande traversée vers l'ouest, retour par les routes du nord: autonomie, navigation, connectivité et endurance du système."
    },
    california: {
      title: "Californie: vol et boucle routière",
      copy:
        "Arrivée en avion, exploration en voiture: bon modèle pour un système mobile qui se reconnecte à plusieurs contextes."
    },
    hawaii: {
      title: "Hawaii: vol et tour en voiture",
      copy:
        "Route isolée, conditions changeantes, boucle locale: penser dashboards simples, cartes et journal de terrain."
    },
    costa: {
      title: "Costa Rica, Caraïbes, Miami, YUL",
      copy:
        "Segment avion, routes locales, retour par Miami puis Montréal: une inspiration pour les systèmes multi-régions et mobiles."
    }
  },
  en: {
    florida: {
      title: "Florida round trip",
      copy:
        "A long drive to Florida and back: perfect for thinking about power, mobile networking, cameras and remote access."
    },
    bc: {
      title: "BC and back through northern USA",
      copy:
        "A large westbound crossing and return through northern roads: autonomy, navigation, connectivity and system endurance."
    },
    california: {
      title: "California: flight and road loop",
      copy:
        "Arrival by plane, exploration by car: a useful model for mobile systems that reconnect across contexts."
    },
    hawaii: {
      title: "Hawaii: flight and road loop",
      copy:
        "Isolated roads, changing conditions, local loop: simple dashboards, maps and field journals."
    },
    costa: {
      title: "Costa Rica, Caribbean, Miami, YUL",
      copy:
        "Flight segment, local routes, return through Miami and Montreal: inspiration for mobile, multi-region systems."
    }
  }
};

year.textContent = new Date().getFullYear();

if (window.lucide) {
  window.lucide.createIcons();
} else {
  window.addEventListener("load", () => window.lucide?.createIcons());
}

document.addEventListener("scroll", () => {
  header.classList.toggle("is-scrolled", window.scrollY > 12);
});

langButtons.forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});

demoButtons.forEach((button) => {
  button.addEventListener("click", () => setDemoMode(button.dataset.mode));
});

routeButtons.forEach((button) => {
  button.addEventListener("click", () => setRoute(button.dataset.route));
});

contactForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(contactForm);
  const name = formData.get("name");
  const email = formData.get("email");
  const project = formData.get("project");
  const message = formData.get("message");
  const subject =
    currentLang === "fr"
      ? `Projet système intelligent - ${project}`
      : `Smart system project - ${project}`;
  const body =
    currentLang === "fr"
      ? `Nom: ${name}\nCourriel: ${email}\nProjet: ${project}\n\n${message}`
      : `Name: ${name}\nEmail: ${email}\nProject: ${project}\n\n${message}`;

  window.location.href = `mailto:contact@jameslaplume.ca?subject=${encodeURIComponent(
    subject
  )}&body=${encodeURIComponent(body)}`;
  formStatus.textContent = translations[currentLang]["form.status"];
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));

setLanguage(currentLang);
setDemoMode(currentDemoMode);
setRoute(currentRoute);

function setLanguage(lang) {
  currentLang = lang === "en" ? "en" : "fr";
  localStorage.setItem("site-language", currentLang);
  document.documentElement.lang = currentLang === "fr" ? "fr-CA" : "en-CA";

  langButtons.forEach((button) => {
    const isActive = button.dataset.lang === currentLang;
    button.setAttribute("aria-pressed", String(isActive));
  });

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    const value = translations[currentLang][key];
    if (value) element.textContent = value;
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    const key = element.dataset.i18nPlaceholder;
    const value = translations[currentLang][key];
    if (value) element.setAttribute("placeholder", value);
  });

  setDemoMode(currentDemoMode);
  setRoute(currentRoute);
}

function setDemoMode(mode) {
  currentDemoMode = demoModes[currentLang][mode] ? mode : "home";
  const data = demoModes[currentLang][currentDemoMode];

  demo.dataset.activeMode = currentDemoMode;
  demoButtons.forEach((button) => {
    button.setAttribute("aria-selected", String(button.dataset.mode === currentDemoMode));
  });

  document.querySelector("[data-demo-title]").textContent = data.title;
  document.querySelector("[data-demo-copy]").textContent = data.copy;

  document.querySelectorAll("[data-demo-svg]").forEach((node, index) => {
    node.textContent = data.nodes[index];
  });

  const list = document.querySelector("[data-demo-signals]");
  list.replaceChildren(
    ...data.signals.map((signal) => {
      const item = document.createElement("li");
      item.textContent = signal;
      return item;
    })
  );
}

function setRoute(route) {
  currentRoute = routeData[currentLang][route] ? route : "florida";
  const data = routeData[currentLang][currentRoute];

  routeMap.dataset.activeRoute = currentRoute;
  routeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.route === currentRoute);
  });

  routeTitle.textContent = data.title;
  routeCopy.textContent = data.copy;
}
