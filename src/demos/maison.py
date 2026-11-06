# Démo « Ma maison » : plan de la propriété où chaque pièce s'allume et se règle.
# Une seule source de vérité : ROOMS (polygones en pixels de l'image 1586 × 992),
# transmise au script par un bloc JSON. Utilisée sur l'accueil et sur la page
# Environnements intelligents (assets/demos/maison.js et .css).

import json

W, H = 1586, 992
IMG = "/media/solutions/jarvis-spaces-property-v3.webp"

# clé, nom, polygone, watts à pleine intensité, extras (thermostat, verrou, porte, eau)
ROOMS = [
    ("salon", "Salon", [(242, 412), (608, 412), (608, 690), (242, 690)], 180, {"temp": 21, "store": True}),
    ("cuisine", "Cuisine", [(242, 236), (786, 236), (786, 412), (242, 412)], 220, {"temp": 21}),
    ("chambre", "Chambre", [(796, 226), (1012, 226), (1012, 446), (796, 446)], 90, {"temp": 19, "store": True}),
    ("sdb", "Salle de bain", [(1014, 230), (1142, 230), (1142, 446), (1014, 446)], 70, {"temp": 23}),
    ("bureau", "Bureau", [(790, 470), (1002, 470), (1002, 692), (790, 692)], 80, {"temp": 21}),
    ("entree", "Entrée", [(608, 440), (790, 440), (790, 700), (748, 700), (748, 905), (624, 905), (624, 700), (608, 700)], 60, {"lock": True}),
    ("garage", "Garage", [(1158, 308), (1452, 308), (1452, 628), (1158, 628)], 120, {"door": True}),
    ("terrasse", "Terrasse", [(225, 30), (640, 30), (640, 215), (225, 215)], 140, {"fire": True}),
    ("piscine", "Piscine", [(648, 82), (1360, 82), (1360, 262), (1178, 262), (1178, 212), (648, 212)], 300, {"water": 28}),
    ("exterieur", "Extérieur", [(60, 700), (624, 700), (624, 905), (748, 905), (748, 700), (1200, 700), (1200, 640),
                                (1440, 640), (1440, 950), (60, 950)], 160, {}),
]

# Ambiances : niveau d'éclairage (0 à 1) et couleur par pièce. Les pièces absentes sont éteintes.
SCENES = {
    "matin": {"label": "Matin", "rooms": {"chambre": [.45, "neutre"], "sdb": [.85, "froide"], "cuisine": [.9, "neutre"],
                                           "entree": [.3, "neutre"]}, "lock": False, "door": False},
    "soiree": {"label": "Soirée", "rooms": {"salon": [.6, "chaude"], "cuisine": [.45, "chaude"], "terrasse": [.75, "chaude"],
                                             "piscine": [.85, "eau"], "exterieur": [.6, "chaude"], "entree": [.4, "chaude"],
                                             "chambre": [.15, "chaude"]}, "lock": False, "door": False},
    "cinema": {"label": "Cinéma", "rooms": {"salon": [.22, "cinema"], "entree": [.08, "chaude"], "exterieur": [.25, "chaude"]},
               "lock": True, "door": False},
    "nuit": {"label": "Nuit", "rooms": {"exterieur": [.22, "chaude"], "entree": [.08, "chaude"]}, "lock": True, "door": False},
    "absent": {"label": "Absent", "rooms": {"salon": [.3, "chaude"]}, "lock": True, "door": False, "away": True},
}


def _pct(poly):
    return ", ".join(f"{x / W * 100:.2f}% {y / H * 100:.2f}%" for x, y in poly)


def _center(poly):
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return (min(xs) + max(xs)) / 2 / W * 100, (min(ys) + max(ys)) / 2 / H * 100


def _data():
    return {
        "rooms": [
            {"k": k, "name": n, "w": w, "x": round(_center(p)[0], 2), "y": round(_center(p)[1], 2), **extra}
            for k, n, p, w, extra in ROOMS
        ],
        "scenes": SCENES,
    }


ON = ' class="is-on"'
# Libellés courts pour les petits écrans (évite que les étiquettes se chevauchent).
SHORT = {"sdb": ' data-s="Bain"', "chambre": ' data-s="Chambre"', "exterieur": ' data-s="Ext."'}


def html(uid="maison"):
    """Markup complet. uid distingue deux démos sur une même page (non utilisé pour l'instant)."""
    lit = "".join(
        f'<img class="mz-lit" data-room="{k}" src="{IMG}" alt="" aria-hidden="true" '
        f'style="clip-path: polygon({_pct(p)})" loading="lazy" decoding="async">'
        for k, _n, p, _w, _e in ROOMS
    )
    polys = "".join(
        f'<polygon data-room="{k}" points="{" ".join(f"{x},{y}" for x, y in p)}"><title>{n}</title></polygon>'
        for k, n, p, _w, _e in ROOMS
    )
    labels = "".join(
        f'<button type="button" class="mz-tag" data-room="{k}" style="--x:{_center(p)[0]:.2f}%;--y:{_center(p)[1]:.2f}%">'
        f'<b{SHORT.get(k, "")}>{n}</b><span class="mz-tag-v">Éteint</span></button>'
        for k, n, p, _w, _e in ROOMS
    )
    blooms = "".join(
        f'<i class="mz-bloom" data-room="{k}" style="--x:{_center(p)[0]:.2f}%;--y:{_center(p)[1]:.2f}%"></i>'
        for k, _n, p, _w, _e in ROOMS
    )
    scenes = "".join(
        f'<button type="button" data-scene="{k}"{ON if k == "soiree" else ""}>{v["label"]}</button>'
        for k, v in SCENES.items()
    )
    return f"""<div class="demo-shell mz" data-demo="maison" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Ma maison</b>
    <span class="mz-clock" data-mz="state">Soirée · 19 h 42</span><span class="tag tag-sim">Démo · données simulées</span></div>
  <div class="demo-body mz-body">
    <div class="mz-stage">
      <div class="mz-plan" data-mz="plan">
        <img class="mz-base" src="{IMG}" alt="Plan d’une résidence vue de haut : salon, cuisine, chambre, piscine et garage" width="{W}" height="{H}" loading="lazy" decoding="async">
        {lit}
        <div class="mz-night" aria-hidden="true"></div>
        {blooms}
        <svg class="mz-hit" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">{polys}</svg>
        {labels}
      </div>
    </div>
    <aside class="mz-panel">
      <p class="mz-k">Ambiances</p>
      <div class="mz-scenes" role="group" aria-label="Ambiances de la maison">{scenes}</div>
      <div class="mz-room" data-mz="room" aria-live="polite">
        <div class="mz-room-head">
          <p class="mz-k">Pièce choisie</p>
          <h3 data-mz="room-name">Salon</h3>
          <span class="mz-ack" data-mz="ack"></span>
        </div>
        <div class="mz-row">
          <span>Lumière</span>
          <button type="button" class="mz-switch" data-mz="switch" role="switch" aria-checked="true" aria-label="Allumer ou éteindre"><i></i></button>
        </div>
        <label class="mz-slider"><span>Intensité <b data-mz="lvl-v">60 %</b></span>
          <input type="range" min="0" max="100" step="1" value="60" data-mz="lvl" aria-label="Intensité de la lumière"></label>
        <div class="mz-row mz-temps" role="group" aria-label="Couleur de la lumière">
          <button type="button" data-tone="chaude" class="is-on">Chaude</button>
          <button type="button" data-tone="neutre">Neutre</button>
          <button type="button" data-tone="froide">Froide</button>
        </div>
        <div class="mz-row mz-extra" data-mz="extra"></div>
      </div>
      <div class="mz-foot">
        <div><span>Consommation estimée</span><b data-mz="watts">— W</b></div>
        <div><span>Portes</span><b data-mz="locks">—</b></div>
      </div>
    </aside>
  </div>
  <script type="application/json" data-mz="data">{json.dumps(_data(), ensure_ascii=False)}</script>
</div>
<p class="demo-hint">Touchez une pièce ou choisissez une ambiance · démonstration, aucun appareil réel</p>"""
