# Solution 03 — Sécurité intelligente.

from pages._solution import solution_page
from demos.securite import HTML as DEMO_HTML

DATA = {
    "slug": "securite-intelligente",
    "title": "Sécurité intelligente",
    "description": "Transformer caméras, accès et alarmes en événements compréhensibles plutôt qu’en notifications isolées.",
    "image": "/media/solutions/securite-intelligente.webp",
    "h1": "Sécurité <em>intelligente.</em>",
    "lead": "Une sécurité qui réunit le contexte, les preuves et les décisions, sans retirer le contrôle humain.",
    "for": "Résidences, entreprises et propriétés réparties sur plusieurs sites",
    "clair": {
        "quoi": "JARVIS regarde toutes vos caméras et vos capteurs en même temps, puis vous dit en une phrase <em>ce qui s’est vraiment passé.</em>",
        "exemple": (
            "Un livreur dépose un colis. Au lieu de six notifications (mouvement, personne, sonnette, "
            "colis…), vous en recevez une seule : « 21 h 42 — Livraison : un colis a été déposé à "
            "l’entrée. Rien d’anormal. » La nuit, si quelqu’un rôde, JARVIS vous propose d’allumer "
            "les lumières et attend votre accord."
        ),
        "avant": [
            "Des dizaines de notifications par jour, souvent pour un chat ou une branche.",
            "Chaque caméra a son application et raconte sa propre version.",
            "Pour comprendre, il faut ouvrir les vidéos une par une.",
            "La nuit, impossible de savoir si c’est grave ou non.",
        ],
        "apres": [
            "Les alertes d’une même situation deviennent un seul événement.",
            "Une phrase claire explique ce qui s’est passé, images à l’appui.",
            "Le normal reste discret; l’inhabituel ressort tout de suite.",
            "JARVIS propose une action (lumières, interphone) et attend votre accord.",
        ],
        "obtenez": [
            ("Un seul fil", "Caméras, sonnette, portes, détecteurs et alarme réunis dans une même chronologie."),
            ("Des preuves classées", "Les images utiles sont gardées avec l’événement, sur place, aussi longtemps que vous le décidez."),
            ("Le dernier mot", "Allumer, parler, prévenir : JARVIS propose, vous approuvez. Rien ne se déverrouille tout seul."),
        ],
    },
    "demo_title": "Six alertes. <em>Un seul événement compris.</em>",
    "demo_copy": (
        "Choisissez une situation. À gauche, les caméras repèrent ce qui bouge. À droite, les alertes "
        "arrivent une à une, puis JARVIS les regroupe en une phrase claire, avec les images comme "
        "preuves. Quand une action est utile, il la propose et attend votre accord."
    ),
    "demo_html": DEMO_HTML,
    "assets": ["securite"],
    "compat": ["Frigate", "ONVIF", "Contrôle d’accès", "Alarmes", "Capteurs", "Interphones", "Stockage local"],
    "deploy_title": "Les événements sensibles restent près du site.",
    "deploy_copy": (
        "L’analyse vidéo et la conservation peuvent être effectuées localement. "
        "Les accès distants passent par des mécanismes privés et auditables."
    ),
    "limit": (
        "Le système ne prétend pas identifier les intentions ni déterminer qu’une personne est "
        "dangereuse. Les règles, responsabilités et obligations légales doivent être définies "
        "avant tout déploiement."
    ),
    "cta_title": "Quel événement de sécurité manque aujourd’hui <em>de contexte?</em>",
    "cta_copy": (
        "Décrivez le site, les accès, les caméras et les alertes actuelles. Nous identifierons "
        "les preuves utiles et les limites à respecter."
    ),
}

PAGE = solution_page(DATA)
