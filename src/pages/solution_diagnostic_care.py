# Page solution 06 — Diagnostic & continuité. Démo : src/demos/diagnostic.py.

from demos.diagnostic import HTML as DEMO, EXTRA
from pages._solution import solution_page

DATA = {
    "slug": "diagnostic-care",
    "title": "Diagnostic & continuité",
    "description": "Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.",
    "image": "/media/solutions/diagnostic-care.webp",
    "h1": "Diagnostic & <em>continuité.</em>",
    "lead": "Comprendre ce qui a changé, quoi vérifier, et remettre un dossier clair à la bonne personne.",
    "demo_title": "Du symptôme à la remise en service, <em>avec des preuves.</em>",
    "demo_html": DEMO,
    "extra": EXTRA,
    "assets": ["diagnostic"],
    "cta_title": "Une panne qui revient?",
}

PAGE = solution_page(DATA)
