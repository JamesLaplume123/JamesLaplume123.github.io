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
    "quoi": "L’eau, le chauffage, l’électricité et vos appareils, surveillés. La panne, vue avant.",
    "moments": [
        ("Lundi", "Le congélateur se réchauffe un peu."),
        ("Mercredi", "JARVIS reconnaît une panne qui commence."),
        ("Mercredi, 18 h", "Vous êtes averti à temps."),
    ],
    "message": "Le congélateur se réchauffe depuis trois jours. Dossier du réparateur prêt.",
    "duel": ("Plus qu’un détecteur de fuite.", "Des détecteurs ordinaires", [
        ("L’eau est déjà au plancher.", "L’eau est coupée en secondes."),
        ("Une alarme, sans raison.", "La vraie cause, en mots simples."),
        ("Le technicien arrive à l’aveugle.", "Il reçoit le dossier complet."),
        ("Personne ne vérifie la réparation.", "JARVIS confirme que tout est revenu."),
    ]),
    "capacites": [
        ("L’eau", "Fuite vue, eau coupée."),
        ("Le chauffage et le gel", "Surveillés jour et nuit, même au chalet."),
        ("L’électricité", "Pannes, génératrice et batteries suivies."),
        ("Vos appareils", "Frigo et pompes, avant la panne."),
        ("La vraie cause", "Ce qui a changé, et pourquoi."),
        ("La réparation prouvée", "Confirmée sur les mesures."),
    ],
    "equipement": ("L’équipement", [
        "Détecteurs de fuite", "Vanne d’eau automatique", "Capteurs de température et de gel",
        "Détecteurs de fumée et de CO reliés", "Mesure d’énergie", "Boîtier de secours"],
        "Les travaux de plomberie et d’électricité sont faits par des entrepreneurs qualifiés."),
}

PAGE = solution_page(DATA)
