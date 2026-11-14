# Laboratoire des cartes : page privée (noindex, hors menus et sitemap, Disallow dans robots.txt).
# « Vivant » : un seul lieu poussé à fond, la Résidence de prestige. Une carte n'est plus un rectangle
# de chiffres : c'est la vraie pièce (la photo réagit aux commandes), des objets en 3D qu'on fait tourner
# (maquette de la maison, batteries) et des formes libres autour (cadran rond, ruban de la journée,
# panneau qui se déplie depuis une lampe, tiroir de pièce). Rendu : assets/demos/labo.js (WebGL pour la
# photo vivante, three.js chargé seulement ici pour la 3D). Sans WebGL : photos fixes, commandes intactes.
# Préfixe vv-.

import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NB = " "  # espace fine insécable


def fr(x, d=1):
    """Nombre à la française : virgule décimale."""
    return f"{x:.{d}f}".replace(".", ",")


# ---------------------------------------------------------------- Données d'exemple
# Scène figée : un mardi de novembre, 16 h 40, à la Résidence (mêmes valeurs que src/demos/env.py).
TH = {"set": 21.5, "inside": 21.0, "min": 15, "max": 26, "hum": 41}
EN = {"soc": 64, "cap": 27, "reserve": 20, "house": 2.9, "solar": 0.3, "today": 31.4,
      "packs": [{"name": "Batterie A", "soc": 65, "v": 52.1, "t": 19.5, "cycles": 212},
                {"name": "Batterie B", "soc": 63, "v": 52.0, "t": 19.8, "cycles": 209}]}


def photo(path, optional=False):
    """Une photo réelle du dépôt; une paire « éteint / ouvert » facultative est prise si elle existe."""
    if os.path.exists(os.path.join(ROOT, path.lstrip("/"))):
        return path
    return None if optional else path


# Chaque lumière : zones éclairées dans la photo (cx, cy, rx, ry en fractions de l'image).
# La photo montre tout allumé; éteindre une lumière assombrit seulement sa zone. Rien n'est recoloré.
SCENES = {
    "salon": {
        "label": "Salon", "img": photo("/media/vitrine/solutions/environnements/salon-prestige-soir.webp"),
        "off": photo("/media/labo/salon-eteint.webp", True),
        "alt": "Le salon de la résidence au crépuscule : foyer allumé, mur de pierre, grande baie vitrée sur la rivière",
        "ratio": [4, 3], "focus": "50% 46%", "amb": 0.17, "room": "salon",
        "sky": [[0.80, 0.27, 0.27, 0.30], [0.84, 0.60, 0.24, 0.10]],
        "window": [0.572, 0.115, 1.0, 0.02, 0.497],  # gauche, haut à gauche, droite, haut à droite, bas
        "fire": [0.203, 0.405, 0.345, 0.55],
        "spots": [
            {"id": "foyer", "kind": "fire", "label": "Foyer", "x": 27.2, "y": 44, "on": 1, "w": 0, "since": "15 h 50",
             "zones": [[0.27, 0.50, 0.19, 0.16], [0.30, 0.63, 0.20, 0.07]],
             "tip": "Le foyer réchauffe déjà le salon. La thermopompe ralentit pour ne pas chauffer en double."},
            {"id": "pierre", "kind": "light", "label": "Mur de pierre", "x": 24, "y": 19, "on": 1, "w": 46, "since": "16 h 05",
             "zones": [[0.25, 0.19, 0.17, 0.25]], "tip": "Éclairage rasant : il met la pierre en relief sans éblouir."},
            {"id": "biblio", "kind": "light", "label": "Bibliothèque", "x": 5.5, "y": 29, "on": 0, "w": 24, "since": "",
             "zones": [[0.04, 0.32, 0.10, 0.34]], "tip": "Je peux l’allumer chaque soir à 17 h, si vous le voulez."},
            {"id": "corniche", "kind": "light", "label": "Corniche du plafond", "x": 64, "y": 6.2, "on": 1, "w": 60, "since": "16 h 05",
             "zones": [[0.66, 0.05, 0.34, 0.07], [0.47, 0.16, 0.10, 0.10]], "tip": "À 40 % après 21 h, elle suffit pour circuler la nuit."},
            {"id": "manger", "kind": "light", "label": "Salle à manger", "x": 45.6, "y": 41.5, "on": 0, "w": 54, "since": "",
             "zones": [[0.46, 0.43, 0.09, 0.09]], "tip": "Souper prévu à 18 h : je l’allume à 17 h 45."},
            {"id": "table", "kind": "light", "label": "Lanternes de la table", "x": 49.5, "y": 61, "on": 1, "w": 12, "since": "16 h 20",
             "zones": [[0.48, 0.63, 0.17, 0.10], [0.72, 0.53, 0.05, 0.05]], "tip": "Lanternes à pile rechargeable : 82 % de charge."},
            {"id": "terrasse", "kind": "light", "label": "Terrasse", "x": 93.5, "y": 50.5, "on": 0, "w": 30, "since": "",
             "zones": [[0.93, 0.52, 0.09, 0.07]], "tip": "Elle s’allume seule quand quelqu’un sort après le coucher du soleil."},
            {"id": "stores", "kind": "blind", "label": "Stores de la baie", "x": 79, "y": 17, "on": 0,
             "tip": "Le soleil se couche à 16 h 24. Je baisse les stores à la tombée de la nuit pour garder la chaleur."},
        ],
    },
    "entree": {
        "label": "Entrée du garage", "img": photo("/media/solutions/camera-driveway-garage-v1.webp"),
        "off": photo("/media/labo/entree-eteinte.webp", True), "open": photo("/media/labo/entree-porte-ouverte.webp", True),
        "inside": photo("/media/env/garage.webp"),
        "alt": "L’entrée du garage de la résidence à la tombée de la nuit, porte fermée, allée éclairée",
        "ratio": [16, 9], "focus": "58% 44%", "amb": 0.42, "room": "garage",
        "door": [0.4474, 0.306, 0.7434, 0.267, 0.5356, 0.5186],  # gauche, haut G, droite, haut D, bas D, bas G
        "crop": [0.0, 0.34, 0.70, 0.93],
        "spots": [
            {"id": "porte", "kind": "door", "label": "Porte de garage 1", "x": 59.5, "y": 39, "on": 0,
             "tip": "La caméra de l’allée ne voit personne. La ventilation démarre à l’ouverture."},
            {"id": "appliques", "kind": "light", "label": "Appliques murales", "x": 40.8, "y": 30.5, "on": 1, "w": 28, "since": "16 h 24",
             "zones": [[0.408, 0.33, 0.05, 0.13], [0.775, 0.31, 0.05, 0.13], [0.97, 0.24, 0.07, 0.24]],
             "tip": "Allumées au coucher du soleil, éteintes à 23 h."},
            {"id": "soffite", "kind": "light", "label": "Encastrés du débord", "x": 65.2, "y": 20, "on": 1, "w": 18, "since": "16 h 24",
             "zones": [[0.58, 0.235, 0.20, 0.06], [0.60, 0.57, 0.26, 0.06]], "tip": "Ils éclairent le seuil quand une voiture arrive."},
            {"id": "jardin", "kind": "light", "label": "Jardin et façade", "x": 31, "y": 44, "on": 1, "w": 64, "since": "16 h 24",
             "zones": [[0.33, 0.46, 0.15, 0.10], [0.06, 0.50, 0.07, 0.08], [0.20, 0.30, 0.16, 0.10]], "tip": "Intensité réduite de moitié après minuit."},
            {"id": "allee", "kind": "light", "label": "Bornes de l’allée", "x": 86, "y": 55.5, "on": 0, "w": 22, "since": "",
             "zones": [[0.82, 0.50, 0.06, 0.06], [0.89, 0.63, 0.05, 0.20], [0.905, 0.88, 0.05, 0.08]],
             "tip": "Je les allume seules quand le portail s’ouvre."},
        ],
    },
    "collection": {
        "label": "Garage de collection", "img": photo("/media/vitrine/accueil/garage-lamborghini-ferrari.webp"),
        "off": photo("/media/labo/collection-eteinte.webp", True), "depth": photo("/media/labo/garage-profondeur.webp"),
        "alt": "Le coupé noir et la sportive rouge dans le garage de collection, sol poli, rubans de lumière au plafond",
        "ratio": [4, 3], "focus": "46% 52%", "amb": 0.30, "room": "garage",
        "beams": [[0.345, 0.522, 0.07], [0.585, 0.505, 0.035]],
        "spots": [
            {"id": "rubans", "kind": "light", "label": "Rubans du plafond", "x": 47, "y": 8.5, "on": 1, "w": 96, "since": "16 h 10",
             "zones": [[0.50, 0.08, 0.70, 0.10], [0.55, 0.62, 0.45, 0.22]], "tip": "Ils s’éteignent 5 minutes après le dernier mouvement."},
            {"id": "vitrine", "kind": "light", "label": "Vitrine", "x": 22, "y": 22.5, "on": 1, "w": 32, "since": "16 h 10",
             "zones": [[0.24, 0.25, 0.30, 0.12]], "tip": "Température de la vitrine stable à 18 °C."},
            {"id": "phares", "kind": "beam", "label": "Phares du coupé", "x": 37.5, "y": 54.5, "on": 0,
             "tip": "Essai des phares à distance. Ils s’éteignent seuls après 30 secondes."},
            {"id": "batt12", "kind": "info", "label": "Batterie du coupé", "x": 31, "y": 43.5,
             "rows": [["Tension", "12,8 V"], ["Mainteneur de charge", "Branché, en veille"], ["Dernier démarrage", "Il y a 12 jours"]],
             "tip": "La batterie tient bien. Un démarrage de 15 minutes est conseillé avant samedi."},
            {"id": "pneus", "kind": "info", "label": "Pneus du coupé", "x": 20.5, "y": 57,
             "rows": [["Avant", "2,3 bar"], ["Arrière", "2,2 bar"], ["Dernière vérification", "2 novembre"]],
             "tip": "Pression correcte pour le remisage. Rien à faire."},
            {"id": "rouge", "kind": "info", "label": "Sportive rouge, baie 2", "x": 80, "y": 41,
             "rows": [["Batterie", "12,6 V"], ["Borne de recharge", "Reportée à 21 h"], ["Housse", "Retirée"]],
             "tip": "Recharge reportée après la pointe : elle sera prête à 6 h."},
        ],
    },
}

# Pièces de la maquette. « scene » : la photo vivante qui lui correspond, s'il y en a une.
ROOMS = [
    {"id": "salon", "label": "Salon", "level": "rdc", "t": 21.0, "hum": 41, "scene": "salon", "lit": 1,
     "next": "18 h : ambiance « Souper »", "hist": ["16 h 20 Lanternes allumées", "16 h 05 Ambiance « Soirée » lancée", "15 h 50 Foyer allumé par James"],
     "acts": [["soiree", "Lancer l’ambiance « Soirée »"], ["eteindre", "Tout éteindre au salon"]]},
    {"id": "cuisine", "label": "Cuisine et cellier", "level": "rdc", "t": 20.5, "hum": 44, "lit": 1,
     "next": "17 h 30 : hotte en mode automatique", "hist": ["15 h 12 Cellier : porte ouverte 40 secondes", "12 h 05 Lave-vaisselle terminé", "7 h 02 Machine à café prête"],
     "extra": [["Cellier", "13 °C, 68 %"], ["Bouteilles", "1 200"]],
     "acts": [["cellier", "Verrouiller le cellier"]]},
    {"id": "garage", "label": "Garage chauffé", "level": "rdc", "t": 12.0, "hum": 45, "scene": "entree", "lit": 0,
     "next": "21 h : recharge des deux voitures", "hist": ["16 h 10 Rubans du plafond allumés", "9 h 41 Porte 2 fermée", "9 h 38 Départ du véhicule utilitaire"],
     "extra": [["Plancher radiant", "15 °C"], ["Places occupées", "2 sur 4"]],
     "acts": [["porte", "Ouvrir la porte 1"], ["ventiler", "Ventiler 10 minutes"]]},
    {"id": "suite", "label": "Suite principale", "level": "etage", "t": 19.0, "hum": 40, "lit": 0,
     "next": "22 h 30 : mode nuit", "hist": ["14 h 02 Fenêtre entrouverte", "8 h 15 Stores ouverts", "6 h 45 Réveil en douceur"],
     "extra": [["Fenêtre", "Entrouverte"], ["Stores", "Ouverts"]],
     "acts": [["fenetre", "Me rappeler de fermer la fenêtre"], ["prechauffer", "Préchauffer à 20 °C pour 22 h"]]},
    {"id": "cinema", "label": "Cinéma maison", "level": "etage", "t": 20.0, "hum": 42, "lit": 0,
     "next": "Samedi 20 h : soirée cinéma", "hist": ["Dimanche Séance de 2 h 10", "Dimanche Projecteur : 412 heures", "Samedi Mise à jour terminée"],
     "extra": [["Projecteur", "En veille"], ["Son", "Prêt"]],
     "acts": [["cinema", "Préparer la salle"]]},
]

DAY = [  # ruban de la journée : heure décimale, titre, détail, action liée
    (6.75, "Réveil", "6 h 45. Stores ouverts, plancher de la suite réchauffé.", ""),
    (7.15, "Départ", "7 h 10. Système armé, thermostat abaissé à 19 °C.", ""),
    (12.5, "Plein soleil", "De 9 h 30 à 15 h. 31,4 kWh produits, batteries remontées de 38 % à 64 %.", ""),
    (15.85, "Retour", "15 h 50. Foyer allumé, système désarmé au visage de James.", ""),
    (16.4, "Coucher du soleil", "16 h 24. Éclairage extérieur allumé.", ""),
    (18.0, "Souper", "18 h. Ambiance « Souper » : salle à manger à 70 %, corniche à 40 %.", "souper"),
    (21.0, "Recharge", "21 h. Recharge des deux voitures, après la pointe du soir.", ""),
    (22.5, "Nuit", "22 h 30. Portes verrouillées, stores baissés, système armé en mode nuit.", "nuit"),
]
NOW = 16 + 40 / 60

SUGG = [
    {"id": "pointe", "txt": "Pointe d’Hydro-Québec demain, de 6 h à 9 h. Je préchauffe la maison à 4 h 30 et je reporte la recharge des voitures ?",
     "yes": "Oui, prépare la pointe", "done": "C’est prévu. Préchauffage à 4 h 30, recharge reportée à 9 h."},
    {"id": "soleil", "txt": "Demain, le soleil couvre tout dès 9 h 30. Je recharge le coupé à ce moment-là plutôt que ce soir ?",
     "yes": "Oui, recharge au soleil", "done": "Entendu. Le coupé se rechargera demain à 9 h 30, sans toucher au réseau."},
    {"id": "fenetre", "txt": "La fenêtre de la suite est entrouverte et il fera −4 °C cette nuit. Je vous le rappelle à 21 h ?",
     "yes": "Oui, rappelle-le-moi", "done": "Rappel placé à 21 h."},
]

JOURNAL = [("16 h 24", "Éclairage extérieur allumé au coucher du soleil"), ("16 h 05", "Ambiance « Soirée » lancée au salon"),
           ("15 h 50", "Foyer allumé par James"), ("15 h 48", "Système désarmé, visage reconnu")]

I = {
    "minus": '<path d="M5 12h14"/>', "plus": '<path d="M12 5v14M5 12h14"/>', "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.6.5 1 1.2 1.1 2h5c.1-.8.5-1.5 1.1-2A6 6 0 0 0 12 3z"/>',
    "fire": '<path d="M12 3c.5 3-1.5 4.5-2.8 6.2C8 10.8 7 12.3 7 14.5a5 5 0 0 0 10 0c0-2-1-3.5-2-5-.3 1.3-1 2-2 2.5.5-3-.2-6.5-1-9z"/>',
    "blind": '<path d="M4 4h16M5 4v13h14V4M5 8.3h14M5 12.6h14M12 17v3"/>',
    "door": '<path d="M3 21V9l9-5 9 5v12"/><path d="M6.5 21v-9h11v9M6.5 15h11M6.5 18h11"/>',
    "beam": '<path d="M10 6a6 6 0 0 0 0 12c1.5 0 2-2.7 2-6s-.5-6-2-6z"/><path d="M15 8h5M15.5 12H21M15 16h5"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5M12 7.8v.2"/>',
    "moon": '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z"/>',
    "sun": '<circle cx="12" cy="12" r="3.75"/><path d="M12 2.75v2M12 19.25v2M2.75 12h2M19.25 12h2M5.45 5.45l1.4 1.4M17.15 17.15l1.4 1.4M5.45 18.55l1.4-1.4M17.15 6.85l1.4-1.4"/>',
    "spark": '<path d="M12 3l1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7z"/>',
    "rotate": '<path d="M4 12a8 8 0 0 1 14-5.3L20 9M20 4v5h-5M20 12a8 8 0 0 1-14 5.3L4 15M4 20v-5h5"/>',
}


def ic(k):
    return f'<svg class="vv-i" viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'


KIND_ICON = {"light": "bulb", "fire": "fire", "blind": "blind", "door": "door", "beam": "beam", "info": "info"}


def spots(key, sc):
    out = []
    for s in sc["spots"]:
        state = "" if s["kind"] == "info" else f' aria-pressed="{"true" if s.get("on") else "false"}"'
        out.append(f'<button type="button" class="vv-spot vv-k-{s["kind"]}" data-vv-spot="{key}:{s["id"]}" style="--x:{s["x"]}%;--y:{s["y"]}%"'
                   f'{state} aria-label="{s["label"]}"><i></i>{ic(KIND_ICON[s["kind"]])}<span>{s["label"]}</span></button>')
    return f'<div class="vv-spots" data-vv-spots="{key}"{"" if key == "salon" else " hidden"}>{"".join(out)}</div>'


def scene():
    imgs = "".join(
        f'<img class="vv-ph" data-vv-ph="{k}" src="{s["img"]}" alt="{s["alt"]}" style="object-position:{s["focus"]}" decoding="async"'
        f'{"" if k == "salon" else " hidden loading=lazy"}>' for k, s in SCENES.items())
    tabs = "".join(
        f'<button type="button" data-vv-tab="{k}" aria-pressed="{"true" if k == "salon" else "false"}">{s["label"]}</button>' for k, s in SCENES.items())
    return f"""
<div class="vv-scene" data-vv-scene>
  <div class="vv-view" data-vv-view>{imgs}<canvas class="vv-gl" data-vv-gl aria-hidden="true"></canvas>
    {"".join(spots(k, s) for k, s in SCENES.items())}
  </div>
  <div class="vv-scene-top">
    <p class="vv-where"><b data-vv-where>Salon</b><span data-vv-count>5 lumières allumées sur 7</span></p>
    <div class="vv-sky" role="group" aria-label="Moment de la journée">
      <button type="button" data-vv-sky="soir" aria-pressed="true">{ic("sun")}<span>Crépuscule</span></button>
      <button type="button" data-vv-sky="nuit" aria-pressed="false">{ic("moon")}<span>Nuit</span></button>
    </div>
  </div>
  <div class="vv-tabs" role="group" aria-label="Lieu affiché">{tabs}</div>
  <div class="vv-pop" data-vv-pop role="dialog" aria-label="Commande" hidden></div>
  {thermo()}
</div>"""


def house():
    levels = "".join(f'<button type="button" data-vv-level="{k}" aria-pressed="{"true" if k == "tout" else "false"}">{l}</button>'
                     for k, l in (("tout", "Maison entière"), ("etage", "Étage"), ("rdc", "Rez-de-chaussée")))
    rooms = "".join(f'<button type="button" data-vv-room="{r["id"]}"><b>{r["label"]}</b><span><i data-vv-room-t="{r["id"]}">{fr(r["t"], 0)}</i>{NB}°C</span></button>'
                    for r in ROOMS)
    return f"""
<div class="vv-house" data-vv-house>
  <div class="vv-h3d"><canvas data-vv-h3d aria-label="Maquette 3D de la résidence. Glissez pour la faire tourner, touchez une pièce pour l’ouvrir."></canvas>
    <p class="vv-hint">{ic("rotate")}Glissez pour tourner. Touchez une pièce.</p>
    <p class="vv-h3d-tag" data-vv-h3d-tag hidden></p>
  </div>
  <div class="vv-levels" role="group" aria-label="Niveau affiché">{levels}</div>
  <div class="vv-rooms" data-vv-rooms>{rooms}</div>
  <ul class="vv-sum">
    <li>Système<b>Désarmé, James est à la maison</b></li>
    <li>Ouvertures<b>1 fenêtre entrouverte</b></li>
    <li>Réseau<b>Fibre, 58 appareils</b></li>
  </ul>
</div>"""


def thermo():
    return f"""
<div class="vv-th" data-vv-th data-min="{TH['min']}" data-max="{TH['max']}" data-set="{TH['set']}" data-now="{TH['inside']}">
  <div class="vv-dial" data-vv-dial role="slider" tabindex="0" aria-label="Consigne de température du rez-de-chaussée"
       aria-valuemin="{TH['min']}" aria-valuemax="{TH['max']}" aria-valuenow="{TH['set']}">
    <svg viewBox="0 0 200 200" aria-hidden="true">
      <circle class="vv-d-track" cx="100" cy="100" r="88" pathLength="100" stroke-dasharray="75 100" transform="rotate(135 100 100)"/>
      <circle class="vv-d-val" data-vv-arc cx="100" cy="100" r="88" pathLength="100" stroke-dasharray="44 100" transform="rotate(135 100 100)"/>
      <circle class="vv-d-now" data-vv-nowdot cx="100" cy="12" r="2.2"/>
      <circle class="vv-d-knob" data-vv-knob cx="100" cy="12" r="5.5"/>
    </svg>
    <div class="vv-d-c">
      <span class="vv-d-l" data-vv-th-state>Chauffe doucement</span>
      <b class="vv-d-v"><span data-vv-set>{fr(TH['set'])}</span><small>°C</small></b>
      <span class="vv-d-n">Maintenant <i data-vv-inside>{fr(TH['inside'])}</i>{NB}°C, {TH['hum']}{NB}%</span>
    </div>
  </div>
  <div class="vv-th-b">
    <button type="button" data-vv-step="-0.5" aria-label="Baisser de un demi-degré">{ic("minus")}</button>
    <span data-vv-th-src>Auto</span>
    <button type="button" data-vv-step="0.5" aria-label="Monter de un demi-degré">{ic("plus")}</button>
  </div>
</div>"""


def ribbon():
    a, b = 5.5, 23.5
    pos = lambda h: (h - a) / (b - a) * 100
    ev = "".join(
        f'<button type="button" class="vv-ev{" is-past" if h < NOW else ""}{" is-r" if NOW - 1 < h < NOW else ""}" data-vv-ev="{i}" data-act="{act}" data-d="{d}" style="--p:{pos(h):.2f}%">'
        f'<i></i><span>{t}</span></button>' for i, (h, t, d, act) in enumerate(DAY))
    # courbe de production solaire du jour (cloche entre 7 h et 16 h 24)
    pts = []
    for k in range(0, 41):
        h = 7 + (16.4 - 7) * k / 40
        y = math.sin(math.pi * k / 40) ** 1.6
        pts.append(f"{pos(h) * 10:.1f},{30 - y * 24:.1f}")
    curve = f'<svg class="vv-sun" viewBox="0 0 1000 30" preserveAspectRatio="none" aria-hidden="true"><polygon points="{pos(7) * 10:.1f},30 {" ".join(pts)} {pos(16.4) * 10:.1f},30"/></svg>'
    return f"""
<section class="vv-ribbon" aria-label="La journée de la résidence">
  <div class="vv-rb" data-vv-rb><div class="vv-rb-in">{curve}<div class="vv-rb-past" style="width:{pos(NOW):.2f}%"></div>{ev}
    <div class="vv-now" style="--p:{pos(NOW):.2f}%"><b>16 h 40</b></div>
  </div></div>
  <p class="vv-rb-d" data-vv-rb-d aria-live="polite">La journée en un ruban. Touchez un moment pour le détail.</p>
</section>"""


def energy():
    packs = "".join(
        f'<li><b>{p["name"]}</b><span><i data-vv-pack="{i}">{p["soc"]}</i>{NB}%</span><span>{fr(p["v"])}{NB}V</span><span>{fr(p["t"])}{NB}°C</span><span>{p["cycles"]} cycles</span></li>'
        for i, p in enumerate(EN["packs"]))
    return f"""
<section class="vv-en" aria-label="Batteries domestiques">
  <div class="vv-b3d"><canvas data-vv-b3d aria-label="Les deux batteries domestiques en 3D. Glissez pour les faire tourner."></canvas></div>
  <div class="vv-en-t">
    <h2>Batteries domestiques</h2>
    <p class="vv-big"><b data-vv-soc>{EN['soc']}</b><small>%</small><span data-vv-auto>≈{NB}9{NB}h d’autonomie, charges essentielles</span></p>
    <ul class="vv-packs">{packs}</ul>
    <dl class="vv-flow">
      <div><dt>Maison</dt><dd><b data-vv-house-kw>{fr(EN['house'])}</b>{NB}kW</dd></div>
      <div><dt>Solaire</dt><dd><b data-vv-solar-kw>{fr(EN['solar'])}</b>{NB}kW</dd></div>
      <div><dt>Batteries</dt><dd><b data-vv-batt-kw>2,6</b>{NB}kW</dd></div>
      <div><dt>Produit aujourd’hui</dt><dd><b>{fr(EN['today'])}</b>{NB}kWh</dd></div>
    </dl>
    <div class="vv-res">
      <p><b>Réserve de secours</b><span>Jamais utilisée, sauf en panne</span></p>
      <div class="vv-stepper"><button type="button" data-vv-res="-5" aria-label="Réduire la réserve">{ic("minus")}</button><output data-vv-res-v>{EN['reserve']}{NB}%</output><button type="button" data-vv-res="5" aria-label="Augmenter la réserve">{ic("plus")}</button></div>
    </div>
    <p class="vv-en-src" data-vv-en-src>La maison tourne sur les batteries. Le réseau reste au repos.</p>
  </div>
</section>"""


def jarvis():
    cards = "".join(
        f'<li class="vv-sg" data-vv-sg="{s["id"]}" data-done="{s["done"]}"><p>{s["txt"]}</p>'
        f'<div class="vv-sg-a"><button type="button" class="vv-go" data-vv-yes>{s["yes"]}</button><button type="button" class="vv-no" data-vv-no>Pas maintenant</button></div></li>'
        for s in SUGG)
    jr = "".join(f"<li><time>{t}</time>{x}</li>" for t, x in JOURNAL)
    return f"""
<section class="vv-jv" aria-label="JARVIS propose">
  <h2>{ic("spark")}JARVIS propose</h2>
  <ul class="vv-sgs" data-vv-sgs>{cards}</ul>
  <h3>Dernières actions</h3>
  <ol class="vv-jr" data-vv-jr>{jr}</ol>
</section>"""


DATA = {"scenes": SCENES, "rooms": ROOMS, "th": TH, "en": EN,
        "modes": {"signature": "/media/modes/scene-signature.webp", "platinum": "/media/modes/scene-platinum.webp", "base": "/media/modes/base.webp"}}

CONTENT = f"""
<div class="vv" data-vv>
  <header class="vv-top">
    <div>
      <h1>Résidence de prestige</h1>
      <p>Saint-Hyacinthe, au bord de la Yamaska. Mardi, 16 h 40. Touchez une lampe, le foyer ou la porte : la pièce répond.</p>
    </div>
    <div class="vv-modes" role="group" aria-label="Mode d’affichage">
      <button type="button" data-mode-set="signature" aria-pressed="true" class="is-on">Signature</button>
      <button type="button" data-mode-set="platinum" aria-pressed="false">Platinum</button>
      <button type="button" data-mode-set="base" aria-pressed="false">Base</button>
    </div>
  </header>
  <div class="vv-stage">
    {scene()}
    <aside class="vv-side">{house()}</aside>
  </div>
  {ribbon()}
  <div class="vv-low">{energy()}{jarvis()}</div>
  <p class="vv-note">Données d’exemple. Les photos sont réelles et ne sont jamais recolorées : seules des couches de lumière et d’ombre s’y ajoutent.</p>
  <aside class="vv-drawer" data-vv-drawer aria-label="Détail de la pièce" hidden></aside>
  <p class="vv-toast" data-vv-toast role="status" aria-live="polite"></p>
  <script type="application/json" data-vv-data>{json.dumps(DATA, ensure_ascii=False)}</script>
</div>
"""

PAGE = {
    "url": "/labo-cartes/",
    "v2": True,
    "noindex": True,
    "title": "Laboratoire des cartes | JARVIS Private Systems",
    "description": "Page privée : la résidence vivante, en photo réactive et en 3D.",
    "body_class": "vv-page",
    "assets": ["labo"],
    "content": CONTENT,
}
