# Carte noire de la zone desservie (accueil) : la Montérégie, huit villes cliquables.
# Même géographie que la Carte de l'app (demos/app_geo.py, Natural Earth, kilomètres depuis
# Saint-Hyacinthe), découpée ici autour de la région pour ne garder que les tracés utiles.
# Les villes viennent de config.ZONE : chaque point mène à sa page /regions/<ville>/.
# Styles : assets/demos/accueil.css (.ac-carte).

import math
import re

from config import ZONE
from demos.app_geo import GEO

LAT0, LON0 = 45.630, -72.957
KX = 111.32 * math.cos(math.radians(47.0))
KY = 111.13

# Cadre affiché, en kilomètres (gauche, haut, largeur, hauteur).
VUE = (-70.0, -60.0, 134.0, 112.0)

# (clé de config.ZONE) -> (latitude, longitude, nom court sur la carte, côté de l'étiquette :
# d = droite, g = gauche, b = dessous, h = dessus)
VILLES = {
    "saint-hyacinthe": (45.630, -72.957, "Saint-Hyacinthe", "h"),
    "granby": (45.400, -72.733, "Granby", "d"),
    "drummondville": (45.883, -72.484, "Drummondville", "g"),
    "longueuil-rive-sud": (45.531, -73.518, "Longueuil", "g"),
    "saint-jean-sur-richelieu": (45.307, -73.263, "Saint-Jean-sur-Richelieu", "d"),
    "sorel-tracy": (46.041, -73.113, "Sorel-Tracy", "d"),
    "beloeil-mont-saint-hilaire": (45.567, -73.200, "Beloeil", "b"),
    "acton-vale": (45.650, -72.566, "Acton Vale", "d"),
}
BASE = "saint-hyacinthe"


def _xy(lat, lon):
    return (lon - LON0) * KX, (LAT0 - lat) * KY


def _decoupe(d, marge=6.0):
    """Garde les sous-tracés qui touchent le cadre; coordonnées absolues arrondies au dixième."""
    x0, y0, w, h = VUE
    x0, y0, x1, y1 = x0 - marge, y0 - marge, x0 + w + marge, y0 + h + marge
    out = []
    for sous in d.split("M")[1:]:
        ferme = sous.rstrip().endswith("z")
        n = [float(v) for v in re.findall(r"-?\d*\.?\d+", sous)]
        x, y = n[0], n[1]
        pts = [(x, y)]
        for i in range(2, len(n) - 1, 2):
            x, y = x + n[i], y + n[i + 1]
            pts.append((x, y))
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
            continue
        if not ferme:
            # Lignes : seulement la partie proche du cadre (les rivières et les routes sont longues).
            pts = [p for i, p in enumerate(pts)
                   if any(x0 <= q[0] <= x1 and y0 <= q[1] <= y1 for q in pts[max(0, i - 1):i + 2])]
            if len(pts) < 2:
                continue
        out.append("M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + ("z" if ferme else ""))
    return "".join(out)


def carte():
    x0, y0, w, h = VUE
    ns = "vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round"
    g = {k: _decoupe(GEO[k]) for k in ("land", "urban", "lakes", "r1", "r2", "hw")}
    bx, by = _xy(*VILLES[BASE][:2])
    liens, points = [], []
    for cle, nom in ZONE:
        lat, lon, court, cote = VILLES[cle]
        x, y = _xy(lat, lon)
        if cle != BASE:
            liens.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{x:.1f}" y2="{y:.1f}"/>')
        base = " is-base" if cle == BASE else ""
        points.append(
            f'<a class="ac-ville c-{cote}{base}" href="/regions/{cle}/" title="{nom}" '
            f'style="left:{(x - x0) / w * 100:.2f}%;top:{(y - y0) / h * 100:.2f}%">'
            f'<i aria-hidden="true"></i><span>{court}</span></a>'
        )
    mx, my = _xy(45.635, -73.80)   # repère : Montréal, hors zone, étiquette discrète
    return f"""<div class="ac-carte" data-ac-carte>
  <svg viewBox="{x0} {y0} {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
    <rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#020203"/>
    <path d="{g["land"]}" style="fill:#111113;stroke:#2e2e32;stroke-width:.8px;{ns}"/>
    <path d="{g["urban"]}" style="fill:#19191c"/>
    <path d="{g["lakes"]}" style="fill:#020203;stroke:#2a2a2e;stroke-width:.7px;{ns}"/>
    <path d="{g["r2"]}" style="fill:none;stroke:#050506;stroke-width:1.2px;{ns}"/>
    <path d="{g["r1"]}" style="fill:none;stroke:#040405;stroke-width:2px;{ns}"/>
    <path d="{g["hw"]}" style="fill:none;stroke:#34343a;stroke-width:1px;{ns}"/>
    <g class="ac-carte-liens">{"".join(liens)}</g>
  </svg>
  <span class="ac-carte-rep" style="left:{(mx - x0) / w * 100:.2f}%;top:{(my - y0) / h * 100:.2f}%" aria-hidden="true">Montréal</span>
  <nav class="ac-villes" aria-label="Villes desservies">{"".join(points)}</nav>
</div>"""
