# Solution 06 — Diagnostic & continuité.

from demos.diagnostic import HTML as DEMO, EXTRA, DIAGS
from pages._solution import solution_page

DATA = {
    "slug": "diagnostic-care",
    "title": "Diagnostic & continuité",
    "description": "Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.",
    "image": "/media/solutions/diagnostic-care.webp",
    "h1": "Diagnostic & <em>continuité.</em>",
    "lead": "Comprendre plus vite ce qui a changé, quoi vérifier et comment transmettre un dossier utile à la bonne personne.",
    "for": "Tous les environnements équipés, du bâtiment au véhicule",
    "demo_title": "Du symptôme à la remise en service, <em>avec des preuves.</em>",
    "demo_copy": (
        "Une enquête guidée en cinq étapes : JARVIS lit les mesures, élimine les fausses pistes, "
        "prépare le dossier du technicien et vérifie le retour à la normale. Plus bas : "
        f"{len(DIAGS)} diagnostics mesurables, trois boucles complètes et la santé de chaque équipement."
    ),
    "demo_html": DEMO,
    "extra": EXTRA,
    "assets": ["diagnostic"],
    "compat": ["Capteurs", "Journaux", "OBD véhicule", "Énergie", "Réseau", "Procédures", "Historique"],
    "deploy_title": "Le dossier reste avec le lieu et ses responsables.",
    "deploy_copy": (
        "Les mesures, hypothèses et rapports demeurent dans l’environnement concerné. "
        "Ils peuvent être transmis à un technicien choisi, jamais diffusés par défaut."
    ),
    "limit": (
        "Le diagnostic assiste la compréhension et la préparation. Les interventions physiques, "
        "électriques ou mécaniques restent le travail de personnes qualifiées."
    ),
    "cta_title": "Quelle panne récurrente mérite enfin <em>une vraie enquête?</em>",
    "cta_copy": (
        "Décrivez le symptôme, les systèmes touchés et ce qui a déjà été tenté. Nous "
        "déterminerons les preuves à rassembler en premier."
    ),
}

DATA["clair"] = {
    "quoi": "Quand quelque chose ne marche plus, JARVIS mène l’enquête <em>et vous montre les preuves.</em>",
    "exemple": (
        "La chambre froide d’une épicerie n’atteint plus 3 °C. JARVIS relit 24 heures de mesures, "
        "écarte la porte, le courant et le thermostat, trouve le ventilateur arrêté et prépare le "
        "dossier du frigoriste. Après l’intervention, il confirme sur la courbe que tout est revenu."
    ),
    "avant": [
        "Une alarme sonne, sans dire pourquoi.",
        "Le technicien arrive à l’aveugle et refait l’enquête.",
        "On remplace des pièces au hasard, à vos frais.",
        "Personne ne vérifie que la réparation tient vraiment.",
    ],
    "apres": [
        "Le symptôme arrive avec ses mesures et son historique.",
        "Les causes sont vérifiées une à une, la plus simple d’abord.",
        "Le dossier technicien est prêt : preuves, cause probable, pièces.",
        "La remise en service est vérifiée sur les mesures, avec l’heure.",
    ],
    "obtenez": [
        ("Des réponses, pas des alarmes",
         "Ce qui a changé, depuis quand et ce que ça veut dire, en mots simples."),
        ("Un dossier prêt à transmettre",
         "Le bon technicien reçoit les preuves et la bonne pièce à apporter. Rien ne part sans votre accord."),
        ("Une réparation prouvée",
         "JARVIS suit les mesures après l’intervention et confirme le retour à la normale."),
    ],
}

PAGE = solution_page(DATA)
