# Solution 05 — Réseau et cybersécurité.

from demos.reseau import HTML as DEMO
from pages._solution import solution_page

DATA = {
    "slug": "reseau-resilience",
    "title": "Réseau et cybersécurité",
    "description": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
    "image": "/media/solutions/reseau-resilience.webp",
    "for": "Maisons connectées, PME et petits multi-sites qui dépendent de leur réseau",
    "demo_title": "Tout votre réseau, <em>dans une seule console.</em>",
    "demo_copy": (
        "Douze modules, de la carte du réseau au score de la semaine : appareils, Wi-Fi, trafic, "
        "menaces, VPN, contrôles parentaux, continuité, sauvegardes, mises à jour et segmentation. "
        "JARVIS explique en une phrase et attend votre accord avant d’agir. Données d’exemple."
    ),
    "demo_html": DEMO,
    "assets": ["reseau"],
    "compat": ["Wi-Fi 7", "VLAN", "Pare-feu", "Détection d’intrusion", "VPN", "5G", "Satellite", "PoE", "Sauvegardes 3-2-1", "Multi-sites"],
    "deploy_title": "L’observation reste sur votre infrastructure.",
    "deploy_copy": (
        "Les sondes, journaux et inventaires peuvent demeurer locaux. Les accès distants "
        "passent par des mécanismes privés, limités et auditables."
    ),
    "limit": (
        "Cette solution observe, documente et assiste l’administration. Elle ne remplace ni un "
        "pare-feu, ni une équipe de sécurité, ni un programme complet de cybersécurité."
    ),
    "cta_title": "Quelle partie de votre infrastructure reste <em>un angle mort?</em>",
    "cta_copy": (
        "Décrivez les sites, les liens Internet, les équipements critiques et les incidents "
        "récents. Nous identifierons la première visibilité utile."
    ),
}

DATA["clair"] = {
    "titre": "Votre réseau, gardé <em>comme celui d’une entreprise.</em>",
    "quoi": "Chaque appareil connu. Chaque intrus mis à l’écart. Tout expliqué simplement.",
    "moments": [
        ("2 h 14", "Un inconnu se branche au Wi-Fi."),
        ("2 h 14", "JARVIS l’isole de vos ordinateurs."),
        ("7 h 00", "Il vous demande si vous le connaissez."),
    ],
    "message": "Un appareil inconnu est isolé. Le connaissez-vous?",
    "duel": ("Plus qu’un routeur.", "Un routeur ordinaire", [
        ("Le mot de passe suffit.", "Chaque appareil est reconnu."),
        ("Tout le monde voit tout.", "Des zones séparées."),
        ("Une attaque passe inaperçue.", "Elle est bloquée, puis expliquée."),
        ("Internet tombe, tout arrête.", "Le secours prend le relais."),
    ]),
    "capacites": [
        ("Il connaît chaque appareil", "Un nouveau venu doit être accepté."),
        ("Il bloque les intrus", "Et vous explique pourquoi."),
        ("Des zones séparées", "Les objets, loin de vos ordinateurs."),
        ("Du Wi-Fi partout", "Dans chaque pièce, avec un secours."),
        ("Accès à distance privé", "Sans rien ouvrir sur Internet."),
        ("Parents et rapport", "Heures d’écran et bilan chaque semaine."),
    ],
    "equipement": ("L’équipement", [
        "Wi-Fi maillé", "Commutateur (switch)", "Pare-feu", "Sauvegarde chiffrée",
        "Routeur 4G ou 5G de secours, selon le lieu"], ""),
}

PAGE = solution_page(DATA)
