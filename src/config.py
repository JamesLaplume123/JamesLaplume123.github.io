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
    "asset_version": "20261106e",
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
CAPABILITIES = [
    {
        "slug": "environnements-intelligents",
        "num": "01",
        "title": "Environnements intelligents",
        "short": "Faire travailler ensemble les technologies d’un lieu, sans rendre son utilisation compliquée.",
        "image": "/media/solutions/environnements-intelligents.webp",
    },
    {
        "slug": "ia-privee-connaissances",
        "num": "02",
        "title": "IA privée et connaissances",
        "short": "Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.",
        "image": "/media/solutions/ia-privee-connaissances.webp",
    },
    {
        "slug": "securite-intelligente",
        "num": "03",
        "title": "Sécurité intelligente",
        "short": "Transformer caméras, accès et alarmes en événements compréhensibles plutôt qu’en notifications isolées.",
        "image": "/media/solutions/securite-intelligente.webp",
    },
    {
        "slug": "automatisation-operations",
        "num": "04",
        "title": "Automatisation d’entreprise",
        "short": "Faire circuler demandes, documents et approbations entre les outils que l’entreprise utilise déjà.",
        "image": "/media/solutions/jarvis-enterprise-operations-v1.webp",
    },
    {
        "slug": "reseau-resilience",
        "num": "05",
        "title": "Réseau et cybersécurité",
        "short": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
        "image": "/media/solutions/reseau-resilience.webp",
    },
    {
        "slug": "diagnostic-care",
        "num": "06",
        "title": "Diagnostic & continuité",
        "short": "Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.",
        "image": "/media/solutions/diagnostic-care.webp",
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
        "diagnostic : six solutions privées qui fonctionnent seules ou ensemble.",
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
