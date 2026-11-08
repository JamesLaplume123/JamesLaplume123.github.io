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
        "On ne sait pas si les sauvegardes marchent ni si un équipement a une faille connue.",
    ],
    "apres": [
        "La carte montre l’appareil touché et le chemin jusqu’à la cause.",
        "Chaque appareil est connu, rangé dans sa zone et suivi.",
        "Des murs séparent la famille, les objets, les caméras et les invités.",
        "Le lien de secours prend le relais et la maison continue en local.",
        "Les sauvegardes sont testées chaque mois et chaque faille a sa date de correction.",
    ],
    "obtenez": [
        ("Une console complète, lisible par tous",
         "Carte du réseau, appareils, Wi-Fi par pièce, trafic, menaces et score de la semaine, avec ce qui circule en direct."),
        ("Des diagnostics en mots simples",
         "La vraie cause, le chemin pour la trouver et une seule action proposée, que vous approuvez."),
        ("Une maison qui tient bon",
         "Zones séparées, lien de secours et fonctions essentielles qui marchent même sans Internet."),
    ],
}

PAGE = solution_page(DATA)
