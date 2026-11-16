# Solution 04 — Automatisation d'entreprise.
# La vedette : la réception téléphonique IA (JARVIS répond sur la ligne IP et
# suit la procédure de l'équipe). Suivent « Votre secteur » (explorateur des
# vrais problèmes de chaque secteur, avec l'automatisation qui les règle), le
# socle commun des douze automatisations offertes à toutes les entreprises et
# la bande « La différence » face aux Environnements intelligents et à la Sécurité.

from demos.automatisation import HTML as DEMO, SECTEURS_HTML
from pages._solution import solution_page

DATA = {
    "slug": "automatisation-operations",
    "title": "Automatisation d’entreprise",
    "description": (
        "Réception téléphonique IA sur téléphonie IP, rendez-vous, courriels, devis, factures : "
        "JARVIS automatise les processus de l’entreprise, étape par étape, avec validation humaine."
    ),
    "image": "/media/solutions/jarvis-enterprise-operations-v1.webp",
    "h1": "Votre réception ne manque <em>plus un appel.</em>",
    "lead": "JARVIS répond au téléphone, fait circuler demandes, documents et approbations, et vous demande votre accord pour les gestes sensibles.",
    "demo_title": "Le téléphone sonne. <em>JARVIS répond.</em>",
    "demo_html": DEMO,
    "assets": ["automatisation"],
    "extra": SECTEURS_HTML,
    "cta_title": "Des appels manqués <em>cette semaine?</em>",
}

PAGE = solution_page(DATA)
