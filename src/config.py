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
    "og_image": "/media/product/jarvis-command-center-preview-og.jpg",
    "theme_color": "#07080a",
    # Incrémenter pour invalider le cache navigateur de site.css / site.js.
    "asset_version": "20261031b",
    "copyright": "© 2026 JARVIS Private Systems · Québec, Canada",
}

# Navigation principale (architecture d'information approuvée, docs/SITE_INFORMATION_ARCHITECTURE.md)
NAV = [
    {"url": "/solutions/", "label": "Solutions"},
    {"url": "/plateforme/", "label": "JARVIS"},
    {"url": "/laboratoire-mobile/", "label": "Laboratoire mobile"},
    {"url": "/vision-roadmap/", "label": "Vision"},
]

CTA = {"url": "/contact/", "label": "Parler du projet"}

# Appel à l'action des pages v2 (chantier wow — vente du logiciel)
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
            {"url": "/contact/", "label": "Contact"},
        ],
    },
]

FOOTER_STATUS = [
    "Plateforme en construction",
    "Laboratoire mobile en construction",
    "Ouvert aux collaborations",
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
