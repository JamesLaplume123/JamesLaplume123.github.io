# Solution 05 — Réseau et cybersécurité.

from demos.reseau import HTML as DEMO
from pages._solution import solution_page

DATA = {
    "slug": "reseau-resilience",
    "title": "Réseau et cybersécurité",
    "description": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
    "image": "/media/solutions/reseau-resilience.webp",
    "h1": "Réseau et <em>cybersécurité.</em>",
    "lead": "Une vue claire du réseau et de ses risques, avant que chaque problème devienne une urgence.",
    "for": "Maisons connectées, PME et petits multi-sites qui dépendent de leur réseau",
    "problem_title": "Le réseau soutient tout le reste, <em>mais devient visible seulement lorsqu’il tombe.</em>",
    "problem_copy": (
        "Cette solution vise l’inventaire, la topologie, la disponibilité, les liens Internet, "
        "la segmentation et les accès privés. Elle joue le rôle d’une couche d’observation et "
        "d’assistance pour l’administrateur, sans promettre une cybersécurité magique."
    ),
    "change_title": "Une infrastructure visible avant qu’elle devienne urgente.",
    "change_copy": (
        "L’inventaire, la topologie et l’historique rendent les dépendances visibles avant "
        "qu’une panne ne devienne une enquête improvisée."
    ),
    "features": [
        ("Inventaire vivant", "Identifier les équipements autorisés, leur rôle, leur état et leurs dépendances."),
        ("Topologie compréhensible", "Montrer comment les sites, réseaux, passerelles et services essentiels sont reliés."),
        ("Disponibilité surveillée", "Repérer une dégradation de connexion, une perte de service ou un équipement instable."),
        ("Accès privé", "Préparer des accès distants limités, documentés et révocables plutôt qu’exposer les systèmes."),
        ("Segmentation progressive", "Séparer les appareils, utilisateurs et fonctions selon les risques et besoins réels."),
        ("Contexte pour le diagnostic", "Transmettre à Diagnostic & continuité les événements réseau pertinents lorsqu’une panne touche plusieurs systèmes."),
    ],
    "demo_title": "Votre réseau, <em>comme une carte vivante.</em>",
    "demo_copy": (
        "Choisissez une situation : JARVIS montre ce qui se passe, explique pourquoi en une "
        "phrase et attend votre accord avant d’agir. Tout ce que vous voyez est simulé."
    ),
    "demo_html": DEMO,
    "assets": ["reseau"],
    "compat": ["Wi-Fi", "VPN", "LTE", "Starlink", "Pare-feu", "VLAN", "Journaux", "Multi-sites"],
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
    "quoi": "JARVIS dessine votre réseau comme une carte vivante et vous dit, en mots simples, <em>pourquoi quelque chose ne marche pas.</em>",
    "exemple": (
        "La caméra du garage cesse d’enregistrer. Au lieu de tout redémarrer au hasard, JARVIS "
        "remonte le câble jusqu’au commutateur, trouve le port coupé et propose de le relancer. "
        "Vous approuvez; il confirme que l’image est revenue."
    ),
    "avant": [
        "Quand quelque chose ne marche plus, on redémarre tout et on espère.",
        "Personne ne sait vraiment quels appareils sont branchés au réseau.",
        "Une ampoule connectée peut voir les mêmes ordinateurs que vous.",
        "Une panne Internet arrête aussi les caméras et les lumières.",
    ],
    "apres": [
        "La carte montre l’appareil touché et le chemin jusqu’à la cause.",
        "Chaque appareil est connu, rangé dans sa zone et suivi.",
        "Des murs séparent la famille, les objets, les caméras et les invités.",
        "Le lien de secours prend le relais et la maison continue en local.",
    ],
    "obtenez": [
        ("Une carte que tout le monde comprend",
         "Internet, routeur, zones et appareils, avec ce qui circule en direct. Aucun jargon à décoder."),
        ("Des diagnostics en mots simples",
         "La vraie cause, le chemin pour la trouver et une seule action proposée, que vous approuvez."),
        ("Une maison qui tient bon",
         "Zones séparées, lien de secours et fonctions essentielles qui marchent même sans Internet."),
    ],
}

PAGE = solution_page(DATA)
