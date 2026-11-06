# Démo « Ma maison » : plan de la propriété où chaque pièce s'allume et se règle.
# Une seule source de vérité : ROOMS (polygones en pixels de l'image 1586 × 992) et
# LUMIERE (luminaires et ouvertures), transmises au script par un bloc JSON. Le script
# en tire les couches de lumière posées sur la photo, qui n'est jamais retouchée.
# Utilisée sur l'accueil et sur la page Environnements intelligents
# (assets/demos/maison.js et .css).

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

# Lumière de chaque pièce, en pixels de l'image :
#   f = luminaires (x, y, portée, sorte : 1 principal, 2 d'appoint, 3 écran allumé en Cinéma) : la lumière part de là;
#   d = ouvertures (x, y, rx, ry) : portes, passages et fenêtres où elle déborde un peu.
LUMIERE = {
    "salon": {"f": [(488, 562, 150, 1), (282, 545, 70, 2), (512, 625, 40, 2), (296, 548, 165, 3)],
              "d": [(624, 530, 24, 52), (440, 414, 140, 22), (428, 680, 120, 16)]},
    "cuisine": {"f": [(405, 338, 125, 1), (622, 345, 115, 1), (552, 272, 60, 2), (272, 330, 40, 2)],
                "d": [(440, 414, 140, 22), (690, 424, 52, 26), (480, 236, 190, 16)]},
    "chambre": {"f": [(898, 330, 110, 1), (827, 292, 34, 2), (966, 292, 34, 2)],
                "d": [(790, 440, 30, 26), (900, 230, 70, 10)]},
    "sdb": {"f": [(1078, 320, 78, 1), (1030, 312, 34, 2)], "d": [(1106, 444, 28, 18)]},
    "bureau": {"f": [(896, 588, 105, 1), (812, 580, 34, 2)], "d": [(910, 472, 34, 16), (850, 686, 70, 14)]},
    "entree": {"f": [(690, 520, 66, 1), (690, 625, 66, 1), (688, 790, 62, 2), (610, 718, 26, 2), (768, 718, 26, 2)],
               "d": [(624, 530, 24, 52), (690, 424, 52, 26)]},
    "garage": {"f": [(1243, 362, 105, 1), (1361, 362, 105, 1), (1302, 520, 150, 2)], "d": [(1305, 632, 118, 30)]},
    "terrasse": {"f": [(392, 150, 110, 1), (520, 158, 105, 1), (272, 150, 46, 2)], "d": [(480, 222, 190, 14)]},
    "piscine": {"f": [(705, 108, 62, 1), (790, 108, 62, 1), (885, 108, 62, 1), (975, 108, 62, 1), (1102, 140, 60, 1),
                      (845, 150, 190, 2), (1270, 195, 60, 2)], "d": [(640, 140, 18, 56)]},
    "exterieur": {"f": [(370, 845, 50, 1), (560, 868, 46, 1), (793, 868, 46, 1), (1025, 845, 50, 1), (1180, 745, 46, 1),
                        (340, 760, 40, 2), (445, 760, 40, 2), (895, 760, 40, 2), (1100, 760, 40, 2), (605, 825, 40, 1),
                        (755, 825, 40, 1), (170, 790, 70, 2), (140, 700, 66, 2), (535, 815, 58, 2), (815, 815, 58, 2),
                        (1230, 672, 42, 2), (1385, 672, 42, 2), (1210, 918, 40, 2), (1420, 918, 40, 2),
                        (1474, 690, 40, 2), (1470, 880, 40, 2), (1305, 790, 150, 2)], "d": []},
}
# Eau de la piscine et du spa (rectangles x0, y0, x1, y1) : reflets animés quand la piscine est éclairée.
EAU = [(657, 92, 1031, 199), (1047, 96, 1157, 181)]
# Foyer extérieur (centre de la flamme) : il vacille quand on l'allume.
FOYER = (716, 61)

# Ambiances : niveau d'éclairage (0 à 1) et couleur par pièce. Les pièces absentes sont éteintes.
# L'ordre des pièces est celui de la séquence : elles s'allument l'une après l'autre.
SCENES = {
    "matin": {"label": "Matin", "rooms": {"chambre": [.45, "neutre"], "sdb": [.85, "froide"], "cuisine": [.9, "neutre"],
                                           "entree": [.3, "neutre"]}, "lock": False, "door": False},
    "soiree": {"label": "Soirée", "rooms": {"entree": [.4, "chaude"], "salon": [.6, "chaude"], "cuisine": [.45, "chaude"],
                                             "terrasse": [.75, "chaude"], "piscine": [.85, "eau"], "exterieur": [.6, "chaude"],
                                             "chambre": [.15, "chaude"]}, "lock": False, "door": False},
    "cinema": {"label": "Cinéma", "rooms": {"salon": [.22, "cinema"], "entree": [.08, "chaude"], "exterieur": [.25, "chaude"]},
               "lock": True, "door": False},
    "nuit": {"label": "Nuit", "rooms": {"exterieur": [.22, "chaude"], "entree": [.08, "chaude"]}, "lock": True, "door": False},
    "absent": {"label": "Absent", "rooms": {"salon": [.3, "chaude"]}, "lock": True, "door": False, "away": True},
}


def _center(poly):
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return (min(xs) + max(xs)) / 2 / W * 100, (min(ys) + max(ys)) / 2 / H * 100


def _data():
    return {
        "size": [W, H],
        "rooms": [
            {"k": k, "name": n, "w": w, "poly": p, "f": LUMIERE[k]["f"], "d": LUMIERE[k]["d"], **extra}
            for k, n, p, w, extra in ROOMS
        ],
        "scenes": SCENES,
    }


def _box(x0, y0, x1, y1):
    """Position et taille d'un rectangle de l'image, en % du plan."""
    return (f"left:{x0 / W * 100:.2f}%;top:{y0 / H * 100:.2f}%;"
            f"width:{(x1 - x0) / W * 100:.2f}%;height:{(y1 - y0) / H * 100:.2f}%")


def _eau():
    """Reflets de la piscine : un seul calque découpé sur l'eau (bassin et spa)."""
    x0, y0 = min(r[0] for r in EAU), min(r[1] for r in EAU)
    x1, y1 = max(r[2] for r in EAU), max(r[3] for r in EAU)
    bw, bh = x1 - x0, y1 - y0
    pt = lambda x, y: f"{(x - x0) / bw * 100:.2f}% {(y - y0) / bh * 100:.2f}%"  # noqa: E731
    # Deux rectangles reliés par un segment sans épaisseur (même polygone).
    pts = []
    for a, b, c, d in EAU:
        pts += [pt(a, b), pt(c, b), pt(c, d), pt(a, d), pt(a, b)]
    return (f'<div class="mz-water" aria-hidden="true" style="{_box(x0, y0, x1, y1)};'
            f'clip-path:polygon({", ".join(pts)})"><i></i><i></i></div>')


ON = ' class="is-on"'
# Libellés courts pour les petits écrans (évite que les étiquettes se chevauchent).
SHORT = {"sdb": ' data-s="Bain"', "chambre": ' data-s="Chambre"', "exterieur": ' data-s="Ext."'}


def html(uid="maison"):
    """Markup complet. uid distingue deux démos sur une même page (non utilisé pour l'instant)."""
    polys = "".join(
        f'<polygon data-room="{k}" points="{" ".join(f"{x},{y}" for x, y in p)}"><title>{n}</title></polygon>'
        for k, n, p, _w, _e in ROOMS
    )
    labels = "".join(
        f'<button type="button" class="mz-tag" data-room="{k}" style="--x:{_center(p)[0]:.2f}%;--y:{_center(p)[1]:.2f}%">'
        f'<b{SHORT.get(k, "")}>{n}</b><span class="mz-tag-v">Éteint</span></button>'
        for k, n, p, _w, _e in ROOMS
    )
    scenes = "".join(
        f'<button type="button" data-scene="{k}"{ON if k == "soiree" else ""}>{v["label"]}</button>'
        for k, v in SCENES.items()
    )
    fx, fy = FOYER
    return f"""<div class="demo-shell mz" data-demo="maison" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Ma maison</b>
    <span class="mz-clock" data-mz="state">Soirée · 19 h 42</span><span class="tag tag-sim">Démo · données simulées</span></div>
  <div class="demo-body mz-body">
    <div class="mz-stage">
      <div class="mz-plan" data-mz="plan">
        <img class="mz-base" src="{IMG}" alt="Plan d’une résidence vue de haut : salon, cuisine, chambre, piscine et garage" width="{W}" height="{H}" loading="lazy" decoding="async">
        <div class="mz-dark" aria-hidden="true"><i></i><i></i></div>
        <div class="mz-lights" data-mz="lights" aria-hidden="true"></div>
        {_eau()}
        <i class="mz-fire" aria-hidden="true" style="{_box(fx - 90, fy - 48, fx + 90, fy + 62)}"></i>
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
  <script type="application/json" data-mz="data">{json.dumps(_data(), ensure_ascii=False, separators=(",", ":"))}</script>
</div>
<p class="demo-hint">Touchez une pièce ou choisissez une ambiance · démonstration, aucun appareil réel</p>"""
