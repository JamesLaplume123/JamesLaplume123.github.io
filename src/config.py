# Configuration centrale du site jameslaplume.ca
# Toute donnée partagée entre les pages vit ici : identité, navigation,
# redirections et version de cache des actifs.

SITE = {
    "name": "JARVIS Private Systems",
    "domain": "https://jameslaplume.ca",
    "locale": "fr-CA",
    "description": (
        "JARVIS relie vos outils, vos informations et vos espaces dans une "
        "expérience privée, contextuelle et contrôlée."
    ),
    "og_image": "/media/product/user/accueil-og.jpg",
    "theme_color": "#000000",
    # Incrémenter pour invalider le cache navigateur de wow.css / wow.js.
    "asset_version": "20261108j",
    # Adresse du service du site (formulaire → Resend → JARVIS, compteur). Vide tant
    # que le Worker Cloudflare n'est pas déployé : le formulaire passe alors par FormSubmit.
    "api": "https://jarvis-site-api.laplumejames.workers.dev",
    "copyright": "© 2026 JARVIS Private Systems · Québec, Canada",
}

# Navigation principale (architecture d'information approuvée, docs/SITE_INFORMATION_ARCHITECTURE.md)
NAV = [
    {"url": "/solutions/", "label": "Solutions"},
    {"url": "/plateforme/", "label": "JARVIS"},
    {"url": "/laboratoire-mobile/", "label": "Laboratoire mobile"},
    {"url": "/vision-roadmap/", "label": "Vision"},
]

# Appel à l'action principal (chantier wow — vente du logiciel)
CTA_V2 = {"url": "/contact/", "label": "Réserver une démo"}

FOOTER_COLUMNS = [
    {
        "title": "Explorer",
        "links": [
            {"url": "/solutions/", "label": "Solutions"},
            {"url": "/plateforme/", "label": "JARVIS"},
            {"url": "/laboratoire-mobile/", "label": "Laboratoire mobile"},
            {"url": "/recherche/", "label": "Recherche"},
        ],
    },
    {
        "title": "Projet",
        "links": [
            {"url": "/vision-roadmap/", "label": "Vision et feuille de route"},
            {"url": "/confiance/", "label": "Confiance"},
            {"url": "/a-propos/", "label": "À propos"},
            {"url": "/confidentialite/", "label": "Confidentialité"},
            {"url": "/contact/", "label": "Contact"},
        ],
    },
]

# Les six capacités : source unique pour l'accueil, la page Solutions et les sous-pages.
# « pour », « line » et « points » alimentent l'aperçu complet de l'accueil : même contenu
# que les pages de solution, en plus court.
CAPABILITIES = [
    {
        "slug": "environnements-intelligents",
        "num": "01",
        "title": "Environnements intelligents",
        "label": "Domotique",
        "short": "Faire travailler ensemble les technologies d’un lieu, sans rendre son utilisation compliquée.",
        "image": "/media/solutions/environnements-intelligents.webp",
        "pour": "Maisons, chalets et petits bâtiments",
        "line": "Un environnement qui comprend son état, s’adapte au contexte et demeure contrôlable simplement.",
        "points": [
            ("Un écran pour tout", "Lumières, chauffage, stores, verrous et énergie, pièce par pièce."),
            ("Des ambiances en une touche", "Matin, Soirée, Cinéma, Nuit, Absent : réglées avec vous, modifiables."),
            ("Le contrôle reste humain", "Déverrouiller ou ouvrir le garage demande toujours votre confirmation."),
        ],
    },
    {
        "slug": "ia-privee-connaissances",
        "num": "02",
        "title": "IA privée et connaissances",
        "label": "IA locale",
        "short": "Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.",
        "image": "/media/solutions/ia-privee-connaissances.webp",
        "pour": "Familles, professionnels et équipes avec beaucoup de documents",
        "line": "Vos documents restent à leur place. L’IA vous aide à les comprendre et montre toujours d’où vient sa réponse.",
        "points": [
            ("Des réponses vérifiables", "Un clic sur la source affiche le passage qui justifie la réponse."),
            ("Vos documents restent chez vous", "Traitement local sur le Hub, ou externe seulement si vous l’autorisez."),
            ("Des actions avec permission", "Rien ne part sans votre « Approuver »."),
        ],
    },
    {
        "slug": "securite-intelligente",
        "num": "03",
        "title": "Sécurité intelligente",
        "label": "Sécurité",
        "short": "Transformer caméras, accès et alarmes en événements compréhensibles plutôt qu’en notifications isolées.",
        "image": "/media/solutions/securite-intelligente.webp",
        "pour": "Résidences, entreprises et propriétés réparties sur plusieurs sites",
        "line": "Une sécurité qui réunit le contexte, les preuves et les décisions, sans retirer le contrôle humain.",
        "points": [
            ("Un seul fil", "Caméras, sonnette, portes, détecteurs et alarme dans une même chronologie."),
            ("Des preuves classées", "Les images utiles sont gardées avec l’événement, sur place."),
            ("Le dernier mot", "JARVIS propose, vous approuvez. Rien ne se déverrouille tout seul."),
        ],
    },
    {
        "slug": "automatisation-operations",
        "num": "04",
        "title": "Automatisation d’entreprise",
        "label": "Entreprise",
        "short": "Répondre au téléphone de l’entreprise et faire circuler demandes, documents et approbations, étape par étape.",
        "image": "/media/solutions/jarvis-enterprise-operations-v1.webp",
        "pour": "PME, entreprises de services et équipes terrain",
        "line": "JARVIS répond à la réception, relie les outils de l’entreprise, demande une validation et conserve une trace.",
        "points": [
            ("Moins de ressaisie", "Les informations passent d’un outil à l’autre, sans copier-coller."),
            ("Vos règles, appliquées", "Seuils, approbations, exceptions : écrits une fois, respectés chaque fois."),
            ("Une trace complète", "Un journal clair de chaque étape, consultable en tout temps."),
        ],
    },
    {
        "slug": "reseau-resilience",
        "num": "05",
        "title": "Réseau et cybersécurité",
        "label": "Réseau",
        "short": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
        "image": "/media/solutions/reseau-resilience.webp",
        "pour": "Maisons connectées, PME et petits multi-sites",
        "line": "Une vue claire du réseau et de ses risques, avant que chaque problème devienne une urgence.",
        "points": [
            ("Une carte que tout le monde comprend", "Internet, routeur, zones et appareils, avec ce qui circule en direct."),
            ("Des diagnostics en mots simples", "La vraie cause et une seule action proposée, que vous approuvez."),
            ("Une maison qui tient bon", "Zones séparées, lien de secours, essentiel qui marche même sans Internet."),
        ],
    },
    {
        "slug": "diagnostic-care",
        "num": "06",
        "title": "Diagnostic & continuité",
        "label": "Continuité",
        "short": "Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.",
        "image": "/media/solutions/diagnostic-care.webp",
        "pour": "Tous les environnements équipés, du bâtiment au véhicule",
        "line": "Comprendre plus vite ce qui a changé, quoi vérifier et comment transmettre un dossier utile.",
        "points": [
            ("Des réponses, pas des alarmes", "Ce qui a changé, depuis quand et ce que ça veut dire, en mots simples."),
            ("Un dossier prêt à transmettre", "Le bon technicien reçoit les preuves et la bonne pièce à apporter."),
            ("Une réparation prouvée", "JARVIS suit les mesures après l’intervention et confirme le retour à la normale."),
        ],
    },
    {
        "slug": "mobilite",
        "num": "07",
        "title": "Mobilité",
        "label": "Mobilité",
        "short": "Un copilote de route qui conseille selon la distance, les heures d’ouverture, le soleil et l’état du véhicule, et garde chaque voyage sur la carte.",
        "image": "/media/vr/exterieur.webp",
        "pour": "VR, voitures, véhicules électriques et vélos électriques",
        "line": "Vous roulez; JARVIS regarde la route, le véhicule et l’heure, et vous propose le bon arrêt au bon moment.",
        "points": [
            ("Un copilote qui pense à tout", "Repas, eau, propane, entretien, soleil et sites à voir, selon la distance et les heures d’ouverture."),
            ("Chaque voyage sur la carte", "Les photos et les arrêts s’enregistrent seuls; touchez un voyage pour le revivre."),
            ("Tous vos véhicules", "Connexion du constructeur ou boîtier JARVIS de base : chaque commande demande votre confirmation."),
        ],
    },
]

# Anciennes URL → nouvelles destinations. Le générateur produit un petit
# fichier de redirection pour chacune afin de ne casser aucun lien externe.
REDIRECTS = {
    "about.html": "/a-propos/",
    "contact.html": "/contact/",
    "lab.html": "/laboratoire-mobile/",
    "learn.html": "/recherche/",
    "mobile-lab.html": "/laboratoire-mobile/",
    "projects.html": "/laboratoire-mobile/",
    "solutions.html": "/solutions/",
    "services/index.html": "/solutions/",
    "ambulance-lab/index.html": "/laboratoire-mobile/",
    "jarvis-builder/index.html": "/plateforme/",
    "jarvis-twin/index.html": "/plateforme/",
    "trading-lab/index.html": "/",
    "about/index.html": "/a-propos/",
    "concept-home/index.html": "/",
    "ui-system-preview/index.html": "/plateforme/",
    "en/about/index.html": "/en/",
    "en/ambulance-lab/index.html": "/laboratoire-mobile/",
    "en/contact/index.html": "/contact/",
    "en/jarvis-builder/index.html": "/en/",
    "en/jarvis-twin/index.html": "/en/",
    "en/services/index.html": "/en/",
    "en/trading-lab/index.html": "/en/",
}

# Titres et descriptions pensés pour Google (domotique, sécurité, IA privée, Québec).
# Ils remplacent ceux des pages au moment de produire le <head>, sans toucher au contenu.
SEO = {
    "/solutions/": (
        "Solutions de domotique, sécurité et IA privée | JARVIS",
        "Domotique, sécurité intelligente, IA locale, automatisation d’entreprise, réseau et "
        "diagnostic : sept solutions privées qui fonctionnent seules ou ensemble.",
    ),
    "/solutions/environnements-intelligents/": (
        "Domotique privée et maison intelligente au Québec | JARVIS",
        "Lumières, chauffage, énergie et appareils de marques différentes réunis dans une "
        "domotique locale, sans dépendre du nuage. Home Assistant, Zigbee, Z-Wave, Matter.",
    ),
    "/solutions/securite-intelligente/": (
        "Sécurité intelligente et caméras privées | JARVIS Québec",
        "Caméras, accès et alarmes transformés en événements clairs, traités sur place. "
        "Une surveillance privée pour maisons et entreprises au Québec.",
    ),
    "/solutions/ia-privee-connaissances/": (
        "IA privée et locale pour vos documents | JARVIS",
        "Une intelligence artificielle qui répond à partir de vos propres documents, montre "
        "ses sources et garde vos données chez vous.",
    ),
    "/solutions/automatisation-operations/": (
        "Automatisation d’entreprise sur mesure au Québec | JARVIS",
        "Demandes, documents et approbations qui circulent entre vos outils existants, avec "
        "une trace de chaque décision. Pour bureaux, commerces et ateliers.",
    ),
    "/solutions/reseau-resilience/": (
        "Réseau et cybersécurité pour maison et PME | JARVIS",
        "Comprendre votre réseau, séparer les objets connectés, surveiller les dépendances et "
        "garder des accès à distance privés et fiables.",
    ),
    "/solutions/diagnostic-care/": (
        "Diagnostic technique et continuité des systèmes | JARVIS",
        "Passer d’un symptôme à des preuves : événements, capteurs et documentation pour "
        "réparer plus vite et remettre en service proprement.",
    ),
    "/plateforme/": (
        "Logiciel JARVIS : App, Core et Hub installés chez vous",
        "JARVIS App, JARVIS Core et JARVIS Hub forment un système privé et local : comptes sur "
        "invitation, droits précis, journal et IA locale.",
    ),
    "/laboratoire-mobile/": (
        "Ambulance convertie en VR connecté | Laboratoire JARVIS",
        "Une ambulance Ford 2017 transformée en laboratoire mobile : 560 Ah LiFePO₄, 500 W "
        "solaire et un tableau JARVIS sur Home Assistant.",
    ),
    "/contact/": (
        "Réserver une démo de domotique privée | JARVIS",
        "Présentez votre maison, votre entreprise ou votre véhicule. James vous montre ce que "
        "JARVIS fait aujourd’hui et la première preuve utile possible chez vous.",
    ),
}
