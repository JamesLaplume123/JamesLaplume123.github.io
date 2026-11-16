# Page solution 05 — Réseau et cybersécurité. Démo : src/demos/reseau.py.

from demos.reseau import HTML as DEMO
from pages._solution import solution_page

DATA = {
    "slug": "reseau-resilience",
    "title": "Réseau et cybersécurité",
    "description": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
    "image": "/media/solutions/reseau-resilience.webp",
    "h1": "Un réseau et un Wi-Fi fiables. <em>La fondation de tout le reste.</em>",
    "lead": "Un Wi-Fi qui couvre partout, des zones séparées et une vue claire du réseau et de ses risques.",
    "demo_title": "Tout votre réseau, <em>dans une seule console.</em>",
    "demo_html": DEMO,
    "assets": ["reseau"],
    "cta_title": "Un réseau à remettre d’aplomb?",
}

PAGE = solution_page(DATA)
