const JL_DATA = {
  services: [
    {
      id: "plan",
      icon: "route",
      title: "Plan directeur intelligent",
      intro:
        "Une architecture claire avant d'acheter des équipements: objectifs, réseau, automatisations, sécurité et étapes réalistes.",
      solves: [
        "Trop d'options et aucun plan d'ensemble",
        "Équipements incompatibles ou inutiles",
        "Projet qui grossit sans contrôle"
      ],
      deliverables: [
        "Schéma d'architecture",
        "Liste d'équipements priorisée",
        "Plan d'intégration et de sécurité"
      ]
    },
    {
      id: "home",
      icon: "house",
      title: "Maison intelligente",
      intro:
        "Home Assistant, tableaux de bord, capteurs, scènes et automatisations utiles pour rendre la maison plus simple à vivre.",
      solves: [
        "Applications séparées pour chaque gadget",
        "Automatisations fragiles",
        "Aucune vue claire de la maison"
      ],
      deliverables: [
        "Dashboard personnalisé",
        "Automatisations documentées",
        "Intégrations Home Assistant"
      ]
    },
    {
      id: "security",
      icon: "cctv",
      title: "Sécurité privée",
      intro:
        "Caméras, Frigate, zones de détection, enregistrement local et notifications intelligentes sans dépendre inutilement du cloud.",
      solves: [
        "Trop de fausses alertes",
        "Images stockées chez des tiers",
        "Accès distant mal sécurisé"
      ],
      deliverables: [
        "Plan caméra et zones",
        "Détection personne/véhicule",
        "Accès privé par VPN"
      ]
    },
    {
      id: "network",
      icon: "network",
      title: "Fondation réseau",
      intro:
        "Wi-Fi, PoE, séparation IoT, VPN, serveurs privés et accès distant pensés comme une fondation fiable.",
      solves: [
        "Wi-Fi instable",
        "Objets connectés sur le réseau principal",
        "Services difficiles à atteindre à distance"
      ],
      deliverables: [
        "Plan réseau",
        "VPN privé",
        "Organisation IoT et serveurs"
      ]
    },
    {
      id: "mobile",
      icon: "ambulance",
      title: "Mobilité intelligente",
      intro:
        "Internet mobile, énergie, caméras, monitoring et automatisation pour vans, VR, remorques et véhicules de travail.",
      solves: [
        "Système mobile impossible à diagnostiquer",
        "Batteries, réseau et caméras séparés",
        "Aucune interface de route"
      ],
      deliverables: [
        "Architecture 12 V/120 V",
        "Dashboard véhicule",
        "Caméras et accès distant"
      ]
    },
    {
      id: "lab",
      icon: "cpu",
      title: "Laboratoire sur mesure",
      intro:
        "Prototypes combinant capteurs, logiciels, IA locale, voix, automatisation et interfaces adaptées à l'utilisateur.",
      solves: [
        "Idée technique difficile à concrétiser",
        "Trop de plateformes à connecter",
        "Prototype sans structure"
      ],
      deliverables: [
        "Prototype fonctionnel",
        "Documentation technique",
        "Roadmap d'amélioration"
      ]
    }
  ],

  scenarios: {
    arrive: {
      label: "J'arrive",
      title: "Arrivée détectée",
      summary:
        "La maison prépare l'entrée, ajuste le climat et remet l'espace de travail dans son état normal.",
      sequence: [
        "Présence détectée dans la zone d'entrée",
        "Éclairage du passage activé",
        "Température ajustée selon l'heure",
        "Système de sécurité désarmé",
        "Bureau préparé et dashboard ouvert"
      ],
      active: ["light", "climate", "presence", "dashboard"],
      values: { energy: "Normal", security: "Désarmé", comfort: "22 °C" }
    },
    leave: {
      label: "Je quitte",
      title: "Maison sécurisée",
      summary:
        "Les lumières inutiles s'éteignent, les portes sont vérifiées et l'énergie passe en mode sobre.",
      sequence: [
        "Absence confirmée après délai",
        "Éclairage général éteint",
        "Portes et fenêtres vérifiées",
        "Caméras extérieures en veille active",
        "Consommation réduite automatiquement"
      ],
      active: ["security", "camera", "energy", "presence"],
      values: { energy: "Réduit", security: "Armé", comfort: "Éco" }
    },
    night: {
      label: "Bonne nuit",
      title: "Mode nuit",
      summary:
        "La maison devient calme, sécurisée et lisible sans éclairage agressif.",
      sequence: [
        "Scène nocturne déclenchée",
        "Éclairage chaud minimal",
        "Portes verrouillées",
        "Notifications silencieuses filtrées",
        "Caméras sensibles aux mouvements extérieurs"
      ],
      active: ["light", "security", "camera", "climate"],
      values: { energy: "Bas", security: "Nuit", comfort: "20 °C" }
    },
    secure: {
      label: "Mode sécurité",
      title: "Surveillance renforcée",
      summary:
        "Les zones sensibles sont priorisées et chaque événement est classé localement.",
      sequence: [
        "Mode sécurité activé",
        "Zones caméra haute priorité",
        "Détection personne/véhicule simulée",
        "Enregistrement local marqué",
        "Notification intelligente préparée"
      ],
      active: ["security", "camera", "network", "dashboard"],
      values: { energy: "Normal", security: "Renforcé", comfort: "Stable" }
    },
    energy: {
      label: "Économie d'énergie",
      title: "Charge réduite",
      summary:
        "Le système coupe ce qui n'est pas utile et garde le confort dans une marge réaliste.",
      sequence: [
        "Consommation instantanée analysée",
        "Charges secondaires retardées",
        "Climat ajusté par zone",
        "Éclairage abaissé",
        "Résumé énergétique disponible"
      ],
      active: ["energy", "climate", "light", "dashboard"],
      values: { energy: "Éco", security: "Normal", comfort: "21 °C" }
    },
    vacation: {
      label: "Vacances",
      title: "Présence simulée",
      summary:
        "La maison reste surveillée, sobre et capable de signaler les anomalies importantes.",
      sequence: [
        "Mode absence longue activé",
        "Présence lumineuse simulée",
        "Caméras et capteurs priorisés",
        "Accès VPN vérifié",
        "Rapport quotidien préparé"
      ],
      active: ["security", "camera", "network", "energy"],
      values: { energy: "Vacances", security: "Armé", comfort: "Hors gel" }
    }
  },

  dashboardActions: [
    {
      id: "home-arrival",
      label: "Arrivée maison",
      icon: "door-open",
      result: "Entrée, climat et bureau synchronisés.",
      changes: ["Hall allumé", "Climat confort", "Sécurité désarmée", "Dashboard actif"]
    },
    {
      id: "night-mode",
      label: "Mode nuit",
      icon: "moon",
      result: "La maison passe en veille calme.",
      changes: ["Lumières basses", "Portes vérifiées", "Caméras sensibles", "Audio coupé"]
    },
    {
      id: "secure-property",
      label: "Sécuriser",
      icon: "shield-check",
      result: "La propriété est priorisée pour les événements utiles.",
      changes: ["Zones actives", "Frigate prêt", "VPN disponible", "Timeline marquée"]
    },
    {
      id: "energy-save",
      label: "Réduire conso",
      icon: "leaf",
      result: "Les charges secondaires sont abaissées.",
      changes: ["Éclairage 40 %", "Climat éco", "Serveur stable", "Rapport énergie"]
    },
    {
      id: "office-ready",
      label: "Préparer bureau",
      icon: "monitor-dot",
      result: "L'espace de travail redevient disponible.",
      changes: ["Bureau allumé", "Réseau vérifié", "Audio prêt", "Dashboard ouvert"]
    },
    {
      id: "person-detected",
      label: "Détection extérieure",
      icon: "scan-face",
      result: "Événement classé localement, sans alerte inutile.",
      changes: ["Personne détectée", "Zone entrée", "Clip local", "Notification filtrée"]
    }
  ],

  securityModes: [
    {
      id: "person",
      label: "Personne",
      title: "Personne détectée à l'entrée",
      explanation:
        "Frigate classe l'objet localement, Home Assistant reçoit l'événement et une notification peut être envoyée par VPN.",
      status: ["Zone entrée active", "Clip local marqué", "Notification intelligente", "Aucun cloud requis"]
    },
    {
      id: "vehicle",
      label: "Véhicule",
      title: "Véhicule dans l'allée",
      explanation:
        "La zone véhicule évite de déclencher des alertes pour chaque mouvement de rue.",
      status: ["Zone allée active", "Objet véhicule", "Timeline filtrée", "Caméra nuit prête"]
    },
    {
      id: "night",
      label: "Nuit",
      title: "Vision nocturne sobre",
      explanation:
        "Le mode nuit augmente l'attention sur les zones sensibles et diminue le bruit des alertes.",
      status: ["Sensibilité ajustée", "Éclairage discret", "Enregistrement local", "VPN distant"]
    },
    {
      id: "outage",
      label: "Panne Internet",
      title: "Le système local continue",
      explanation:
        "Même sans Internet, les caméras, l'enregistrement et les automatisations locales peuvent continuer.",
      status: ["Internet hors ligne", "LAN opérationnel", "Stockage local", "Alertes en attente"]
    }
  ],

  vehicleSystems: [
    {
      id: "cameras",
      title: "Quatre caméras",
      icon: "cctv",
      status: "En conception",
      description:
        "Vision avant, arrière et latérale pour documenter la route, sécuriser le véhicule et tester la détection locale.",
      details: ["Caméras PoE possibles", "Zones Frigate par angle", "Enregistrement local prioritaire"]
    },
    {
      id: "router",
      title: "Routeur 5G",
      icon: "router",
      status: "Planifié",
      description:
        "Connexion mobile avec accès privé au dashboard, aux caméras et aux services internes.",
      details: ["SIM/5G", "Failover possible", "Accès VPN seulement"]
    },
    {
      id: "poe",
      title: "Réseau PoE",
      icon: "network",
      status: "Architecture",
      description:
        "Un petit réseau embarqué pour alimenter caméras, points d'accès et modules sans câblage inutile.",
      details: ["Switch PoE", "Segments IoT", "Câblage documenté"]
    },
    {
      id: "frigate",
      title: "Frigate",
      icon: "scan",
      status: "Prototype",
      description:
        "Détection locale de personnes et véhicules, pensée pour réduire le bruit des événements.",
      details: ["Détection locale", "Timeline utile", "Intégration Home Assistant"]
    },
    {
      id: "assistant",
      title: "Assistant local",
      icon: "bot",
      status: "Recherche",
      description:
        "Interface Jarvis locale pour comprendre l'état du véhicule, résumer les événements et préparer des routines.",
      details: ["Ollama", "Whisper", "Piper", "Prototype seulement"]
    },
    {
      id: "energy",
      title: "Solaire et batteries",
      icon: "battery-charging",
      status: "Étude",
      description:
        "Monitoring de l'énergie, priorités de charge et alertes avant que le système devienne critique.",
      details: ["Batteries auxiliaires", "Panneaux solaires", "Courbes d'autonomie"]
    },
    {
      id: "climate",
      title: "Ventilation intelligente",
      icon: "fan",
      status: "À tester",
      description:
        "Capteurs d'humidité, température et CO2 pour garder l'intérieur utilisable et sécuritaire.",
      details: ["Capteurs environnement", "Ventilation automatique", "Alertes chaleur/froid"]
    },
    {
      id: "lighting",
      title: "Éclairage",
      icon: "lightbulb",
      status: "Planifié",
      description:
        "Scènes de travail, nuit, route et présentation pour transformer l'ambulance en showroom mobile.",
      details: ["Scènes Home Assistant", "Éclairage basse conso", "Contrôle manuel conservé"]
    },
    {
      id: "vpn",
      title: "VPN privé",
      icon: "lock-keyhole",
      status: "Prioritaire",
      description:
        "Accès distant sans exposer les services du véhicule directement à Internet.",
      details: ["Tailscale/WireGuard", "Aucun port public", "Accès multi-appareil"]
    }
  ],

  routes: [
    {
      id: "florida",
      label: "Floride",
      summary: "Québec vers la Floride et retour par la route.",
      points: ["Québec", "New York", "Carolines", "Floride", "Retour Québec"]
    },
    {
      id: "bc",
      label: "BC + nord USA",
      summary: "Traversée vers la Colombie-Britannique, retour par le nord des États-Unis.",
      points: ["Québec", "Prairies", "Colombie-Britannique", "Nord USA", "Québec"]
    },
    {
      id: "california",
      label: "Californie",
      summary: "Vol vers la Californie, exploration en voiture sur place.",
      points: ["YUL", "Californie", "Côte", "Déserts", "Retour avion"]
    },
    {
      id: "hawaii",
      label: "Hawaii",
      summary: "Vol vers Hawaii, exploration des îles en voiture.",
      points: ["YUL", "Pacifique", "Hawaii", "Routes côtières", "Retour"]
    },
    {
      id: "costa",
      label: "Costa Rica + Caraïbes",
      summary: "Costa Rica, route dans les Caraïbes, retour via Miami puis YUL.",
      points: ["YUL", "Costa Rica", "Caraïbes", "Miami", "YUL"]
    }
  ],

  process: [
    {
      step: "01",
      title: "Comprendre",
      text: "On clarifie le problème réel, l'environnement, les contraintes, les appareils existants et le niveau de confort technique."
    },
    {
      step: "02",
      title: "Concevoir",
      text: "On transforme les idées en architecture: réseau, sécurité, automatisations, interfaces et priorités."
    },
    {
      step: "03",
      title: "Sélectionner",
      text: "On choisit l'équipement avec une logique de fiabilité, de compatibilité et de maintenance."
    },
    {
      step: "04",
      title: "Intégrer",
      text: "On connecte les systèmes progressivement, en gardant les contrôles manuels et la documentation."
    },
    {
      step: "05",
      title: "Tester et documenter",
      text: "On valide les scénarios, les accès, les alertes et les limites avant d'ajouter plus de complexité."
    }
  ],

  articles: [
    { slug: "reseau-cameras-prive", title: "Créer un réseau de caméras privé", category: "Sécurité", minutes: 7, status: "Guide" },
    { slug: "comprendre-home-assistant", title: "Comprendre Home Assistant sans jargon", category: "Home Assistant", minutes: 6, status: "Guide" },
    { slug: "integrer-frigate", title: "Intégrer Frigate dans un système local", category: "Sécurité", minutes: 8, status: "Lab note" },
    { slug: "acces-distance-vpn", title: "Accéder à distance sans ouvrir de ports", category: "Réseaux", minutes: 5, status: "Guide" },
    { slug: "separer-iot", title: "Séparer les objets connectés du réseau principal", category: "Réseaux", minutes: 7, status: "Architecture" },
    { slug: "vehicule-connecte", title: "Concevoir un véhicule connecté", category: "Mobile", minutes: 9, status: "Projet" },
    { slug: "batterie-solaire-monitoring", title: "Surveiller une batterie et un système solaire", category: "Mobile", minutes: 6, status: "Expérience" },
    { slug: "dashboard-adapte", title: "Créer une interface Home Assistant adaptée à son utilisateur", category: "Home Assistant", minutes: 6, status: "Guide" },
    { slug: "whisper-piper-local", title: "Utiliser Whisper et Piper localement", category: "IA locale", minutes: 8, status: "Expérience" },
    { slug: "limites-assistant-local", title: "Comprendre les limites d'un assistant IA local", category: "IA locale", minutes: 7, status: "Recherche" },
    { slug: "erreurs-domotique", title: "Éviter les erreurs courantes en domotique", category: "Home Assistant", minutes: 5, status: "Checklist" },
    { slug: "documenter-ambulance", title: "Documenter une conversion d'ambulance", category: "Mobile", minutes: 9, status: "Journal" }
  ],

  projects: [
    {
      slug: "ambulance-connectee",
      title: "Ambulance connectée Ford 2017 V10",
      status: "Projet phare en développement",
      type: "Mobile Lab",
      problem:
        "Transformer une ambulance québécoise en laboratoire mobile pour démontrer des systèmes intelligents dans des conditions réelles.",
      constraints: ["Énergie limitée", "Vibrations", "Réseau mobile variable", "Espace technique restreint"],
      result:
        "Architecture en conception: Home Assistant mobile, Frigate, réseau PoE, batteries, ventilation, accès VPN et assistant local."
    },
    {
      slug: "jarvis-interface",
      title: "Interface Jarvis locale",
      status: "Prototype de recherche",
      type: "IA locale",
      problem:
        "Créer une interface capable d'expliquer l'état d'un système sans exposer la maison ou le véhicule à un service externe.",
      constraints: ["Latence", "Confidentialité", "Compréhension du contexte", "Limites des modèles locaux"],
      result:
        "Prototype expérimental avec Ollama, Whisper, Piper, Open WebUI et APIs Home Assistant."
    },
    {
      slug: "camera-network",
      title: "Réseau caméra privé",
      status: "Expérience documentée",
      type: "Sécurité",
      problem:
        "Réduire les fausses alertes et garder les vidéos importantes localement.",
      constraints: ["Zones de détection", "Stockage", "Accès distant", "Éclairage de nuit"],
      result:
        "Architecture Frigate/Home Assistant prête à être adaptée selon la propriété."
    }
  ],

  labSystems: [
    { name: "Home Assistant OS sur Raspberry Pi 5", status: "running", area: "Automation" },
    { name: "Centaines d'entités et dashboards", status: "running", area: "Dashboards" },
    { name: "Docker et services auto-hébergés", status: "testing", area: "Servers" },
    { name: "Ubuntu virtual machines", status: "testing", area: "Servers" },
    { name: "Tailscale / accès privé", status: "running", area: "Network" },
    { name: "Frigate computer vision", status: "testing", area: "Security" },
    { name: "Ollama + Open WebUI", status: "testing", area: "Local AI" },
    { name: "Whisper et Piper", status: "planned", area: "Voice" },
    { name: "Proxmox architecture", status: "planned", area: "Infrastructure" },
    { name: "VLAN, STP, HSRP, ACL", status: "learning", area: "Network study" }
  ],

  roadmap: [
    { title: "CCNA", status: "Roadmap", note: "Réseaux, routage, commutation et dépannage." },
    { title: "Microsoft Azure Fundamentals", status: "Roadmap", note: "Notions cloud pour mieux intégrer privé et public." },
    { title: "AI-900", status: "Roadmap", note: "Fondations IA, limites et cas d'usage." },
    { title: "DP-900", status: "Roadmap", note: "Fondations données et plateformes." },
    { title: "AZ-104", status: "Plus tard", note: "Administration Azure quand les bases seront consolidées." },
    { title: "Investigation privée", status: "Intérêt", note: "Méthode, observation, documentation et sécurité." },
    { title: "Cybersécurité et automatisation", status: "Continu", note: "Études et expériences appliquées." }
  ],

  stack: [
    "Home Assistant",
    "Frigate",
    "Raspberry Pi 5",
    "Linux",
    "Windows",
    "Ubuntu VM",
    "Docker",
    "Tailscale",
    "MQTT",
    "ESPHome",
    "Zigbee / Z-Wave",
    "PoE",
    "Ollama",
    "Open WebUI",
    "Whisper",
    "Piper",
    "Proxmox",
    "Grafana"
  ],

  solutions: [
    {
      title: "Confort",
      icon: "sofa",
      text: "Des scènes et routines qui rendent l'espace plus naturel: arrivée, nuit, travail, absence, invités.",
      examples: ["Éclairage adaptatif", "Climat par présence", "Dashboard famille"]
    },
    {
      title: "Sécurité",
      icon: "shield",
      text: "Voir les événements importants, filtrer le bruit et garder les images localement.",
      examples: ["Frigate", "Zones caméra", "Notifications utiles"]
    },
    {
      title: "Énergie",
      icon: "bolt",
      text: "Comprendre la consommation, les batteries, le solaire et les priorités de charge.",
      examples: ["Monitoring", "Alertes", "Mode économie"]
    },
    {
      title: "Connectivité",
      icon: "wifi",
      text: "Rendre le réseau plus propre, plus lisible et plus stable pour les appareils essentiels.",
      examples: ["Wi-Fi", "PoE", "Organisation IoT"]
    },
    {
      title: "Vie privée",
      icon: "fingerprint",
      text: "Favoriser les systèmes locaux et les accès contrôlés plutôt que tout exposer au cloud.",
      examples: ["Stockage local", "VPN", "Services privés"]
    },
    {
      title: "Accès distant",
      icon: "key-round",
      text: "Accéder à la maison, au serveur ou au véhicule sans ouvrir les portes inutiles d'Internet.",
      examples: ["Tailscale", "WireGuard", "Portail privé"]
    },
    {
      title: "Systèmes mobiles",
      icon: "truck",
      text: "Appliquer l'automatisation à un véhicule qui bouge, vibre, perd Internet et vit sur batteries.",
      examples: ["Ambulance", "Van", "VR"]
    }
  ]
};

window.JL_DATA = JL_DATA;
