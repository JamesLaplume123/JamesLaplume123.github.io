# Solution 06 — Diagnostic & continuité.

from demos.diagnostic import HTML as DEMO, EXTRA, DIAGS
from pages._solution import solution_page

DATA = {
    "slug": "diagnostic-care",
    "title": "Diagnostic & continuité",
    "description": "Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.",
    "image": "/media/solutions/diagnostic-care.webp",
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
    "titre": "Ce qui va briser, <em>JARVIS le voit venir.</em>",
    "quoi": "JARVIS surveille l’eau, le chauffage, l’électricité et vos appareils. Quand quelque chose change, il trouve la vraie cause et prépare la réparation.",
    "moments": [
        ("Lundi", "Votre congélateur se réchauffe d’un demi-degré."),
        ("Mercredi", "La dérive continue. JARVIS reconnaît le début d’une panne."),
        ("Mercredi, 18 h", "Vous êtes averti, avant que la nourriture se perde."),
    ],
    "message": "Le congélateur se réchauffe depuis trois jours. Cause probable : le ventilateur. Le dossier du réparateur est prêt.",
    "duel": ("Plus qu’un détecteur de fuite.", "Des détecteurs ordinaires", [
        ("Il sonne quand l’eau est déjà sur le plancher.",
         "La fuite est vue, et l’eau coupée en quelques secondes."),
        ("Une alarme sonne, sans dire pourquoi.",
         "Ce qui a changé, depuis quand et pourquoi, en mots simples."),
        ("Le congélateur lâche, et vous le découvrez trois jours plus tard.",
         "Une dérive lente est remarquée des jours avant la panne."),
        ("Au chalet, le gel fait éclater un tuyau sans que personne le sache.",
         "Chauffage, température et gel suivis à distance, avec une alerte avant le danger."),
        ("Le technicien arrive à l’aveugle et refait l’enquête.",
         "Il reçoit le dossier : les mesures, la cause probable et la pièce à apporter."),
        ("Personne ne vérifie que la réparation tient.",
         "JARVIS suit les mesures après l’intervention et confirme le retour à la normale."),
    ]),
    "capacites": [
        ("L’eau",
         "Des détecteurs sous l’évier, le chauffe-eau et la laveuse. Une fuite est vue et l’eau coupée en quelques secondes."),
        ("Le chauffage et le gel",
         "Fournaise, thermopompe et tuyaux surveillés jour et nuit, au chalet comme à la maison."),
        ("L’électricité",
         "Pannes, surtensions, génératrice et batteries de secours : vous savez ce qui tient, et pour combien de temps."),
        ("Vos appareils",
         "Frigo, congélateur, pompe de puits ou de puisard : l’anomalie est vue avant la panne."),
        ("La vraie cause",
         "JARVIS relit les mesures, écarte les fausses pistes une à une et vous dit ce qui a changé, depuis quand et pourquoi."),
        ("La réparation prouvée",
         "Le bon technicien reçoit le dossier. Après son passage, JARVIS confirme sur les mesures que tout est revenu."),
    ],
    "equipement": ("L’équipement", [
        "Détecteurs de fuite", "Vanne d’eau automatique", "Capteurs de température et de gel",
        "Détecteurs de fumée et de CO reliés", "Mesure d’énergie", "Boîtier de secours"],
        "Les travaux de plomberie et d’électricité sont faits par des entrepreneurs qualifiés."),
}

PAGE = solution_page(DATA)
