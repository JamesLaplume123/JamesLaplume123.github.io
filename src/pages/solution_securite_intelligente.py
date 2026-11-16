# Page solution 03 — Sécurité intelligente. Démo : src/demos/securite.py.

from pages._solution import solution_page
from demos.securite import HTML as DEMO_HTML

DATA = {
    "slug": "securite-intelligente",
    "title": "Sécurité intelligente",
    "description": "Un logiciel qui réunit vos caméras, serrures et capteurs en événements clairs, traités et gardés chez vous : mur vidéo, accès, véhicules, zones, incidents et conformité à la Loi 25.",
    "image": "/media/solutions/securite-intelligente.webp",
    "h1": "Sécurité <em>intelligente.</em>",
    "lead": "Vos caméras, vos serrures et vos capteurs réunis dans une seule application; les images restent chez vous.",
    "demo_title": "Neuf modules. <em>Une seule plateforme.</em>",
    "demo_html": DEMO_HTML,
    "assets": ["securite"],
    "cta_title": "Un lieu à protéger?",
}

PAGE = solution_page(DATA)
