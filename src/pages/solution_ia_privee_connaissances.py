# Solution 02 — IA privée et connaissances. Démo : src/demos/ia.py.

from demos.ia import HTML as DEMO
from pages._solution import bande, demo, points, fin

SLUG = "ia-privee-connaissances"

PAGE = {
    "url": f"/solutions/{SLUG}/",
    "v2": True,
    "title": "IA privée et connaissances | Solutions JARVIS",
    "description": "Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.",
    "og_image": "/media/product/outils/ia.jpg",
    "assets": ["coquille", "ia"],
    "content": bande(
        SLUG, "IA privée et <em>connaissances.</em>",
        "Vos documents restent chez vous; l’IA y répond et montre toujours d’où vient sa réponse.",
        "/media/solutions/ia-privee-connaissances.webp",
    )
    + demo(SLUG, "Parlez à vos propres documents. <em>Chaque réponse montre sa preuve.</em>", DEMO, ident="outil")
    + points(SLUG)
    + fin("Des documents à rendre<br><span>enfin retrouvables?</span>"),
}
