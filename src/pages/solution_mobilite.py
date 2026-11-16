# Solution 07 — Mobilité (extension « Mobilité » de JARVIS App).
# Règle convenue avec James : Environnements = le lieu où l'on vit ou travaille (la cellule du VR :
# lumières, eau, énergie); Mobilité = le mouvement : le trajet, le voyage, le véhicule.
# Démo : src/demos/mobilite.py.

from demos import mobilite
from pages._solution import bande, demo, points, fin

SLUG = "mobilite"
HERO = mobilite.photo("hero", "/media/vr/exterieur.webp")

PAGE = {
    "url": f"/solutions/{SLUG}/",
    "v2": True,
    "title": "Copilote de voyage, VR et voiture connectés | JARVIS Mobilité",
    "description": "Un copilote de route qui propose repas, eau, propane, entretien et sites à voir selon la "
                   "distance, les heures d’ouverture, le soleil et l’état du véhicule.",
    "og_image": HERO,
    "assets": ["coquille", "mobilite"],
    "content": bande(
        SLUG, "VR et véhicules connectés. <em>Partez l’esprit libre.</em>",
        "Vous roulez; JARVIS regarde la route, le véhicule et l’heure, et vous propose le bon arrêt au bon moment.",
        HERO,
    )
    + demo(SLUG, "Vous conduisez. <em>Le copilote s’occupe du reste.</em>", mobilite.HTML)
    + points(SLUG)
    + fin("Où partez-vous<br><span>la prochaine fois?</span>"),
}
