# Solution 01 — Environnements intelligents.
# La démonstration « Environnements » : un seul modèle de logiciel pour tous les lieux, dans
# JARVIS App. Données de la démo : src/demos/env.py (le module Éclairage : src/demos/lumieres.py).

from demos import env
from pages._solution import bande, demo, points, fin

SLUG = "environnements-intelligents"

PAGE = {
    "url": f"/solutions/{SLUG}/",
    "v2": True,
    "title": "Environnements intelligents | Solutions JARVIS",
    "description": "Faire travailler ensemble les technologies d’un lieu, sans rendre son utilisation compliquée.",
    "og_image": "/media/solutions/environnements-intelligents.webp",
    "assets": ["coquille", "lumieres", "env"],
    "content": bande(
        SLUG, "Domotique résidentielle. <em>Toute la maison sur un seul écran.</em>",
        "Lumières, chauffage, énergie et appareils de marques différentes, réunis et simples à contrôler.",
        "/media/solutions/environnements-intelligents.webp",
    )
    + demo(SLUG, "Un seul logiciel. <em>Tous vos lieux.</em>", env.html())
    + points(SLUG)
    + fin("Un lieu à faire fonctionner<br><span>comme un ensemble?</span>"),
}
