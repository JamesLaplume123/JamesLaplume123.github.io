# Démo interactive — Mobilité (extension 07).
# Règle convenue avec James : Environnements = le lieu où l'on vit ou travaille (la cellule du VR :
# lumières, eau, énergie); Mobilité = le mouvement : le trajet, le voyage, le véhicule.
#
# Trois onglets dans JARVIS App :
#   1. Copilote de route : carte vectorielle noire (aucune tuile), le VR qui avance de
#      Saint-Hyacinthe au Lac-Saint-Jean, et des suggestions calculées selon la distance, les
#      heures d'ouverture, le soleil et l'état du véhicule. Six modes de voyage replanifient.
#   2. Journal de voyage : photos et points géolocalisés sur la carte, chronologie, « Mes voyages ».
#   3. Véhicules : garage connecté (VR, berline électrique, sportive, vélo électrique), ce qui passe
#      par la connexion du constructeur et ce qui passe par le boîtier JARVIS de base.
#
# La géométrie (fleuve, fjord, lac, routes, trajets) est calculée ici en kilomètres, puis transmise à
# assets/demos/mobilite.js en JSON. Les étiquettes et repères sont en HTML par-dessus la carte pour
# rester nets à toutes les tailles. Style : assets/demos/mobilite.css.
#
# Photos : chaque emplacement prend media/mobilite/<nom>.webp s'il existe au moment du build,
# sinon une photo existante du site qui convient, sinon un panneau noir « Photo à venir ».

import json
import math
import os

from demos.app import icon as app_icon

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
NB = " "


def photo(nom, repli=None):
    """Chemin de la photo media/mobilite/<nom>.webp si elle existe, sinon la photo de repli (ou None)."""
    if os.path.exists(os.path.join(ROOT, "media", "mobilite", f"{nom}.webp")):
        return f"/media/mobilite/{nom}.webp"
    return repli


# ---------------------------------------------------------------------------------------------
# Icônes (même trait que JARVIS App : 24 × 24, contour 1,5)
# ---------------------------------------------------------------------------------------------
ICO = {
    "repas": '<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10"/><path d="M16.5 21V3c-2 1.4-3 4-3 7 0 1.6.9 2.5 3 2.5"/>',
    "eau": '<path d="M12 3.5c3.2 4 5.5 7.1 5.5 10a5.5 5.5 0 0 1-11 0c0-2.9 2.3-6 5.5-10Z"/><path d="M9.3 14.4a2.8 2.8 0 0 0 2.4 2.6"/>',
    "propane": '<rect x="7" y="6.5" width="10" height="14" rx="4.5"/><path d="M10 6.5V4h4v2.5M7.5 12h9"/>',
    "webasto": '<path d="M5 19h14M7 15c0-2 2-2 2-4s-2-2-2-4M12 15c0-2 2-2 2-4s-2-2-2-4M17 15c0-2 2-2 2-4s-2-2-2-4"/>',
    "meca": '<path d="M14.5 6.2a4 4 0 0 0 5 5L12 18.7a2.3 2.3 0 0 1-3.3-3.3l7.5-7.5"/><path d="M14.5 6.2 17 3.7"/>',
    "soleil": '<path d="M4 17h16M7.5 17a4.5 4.5 0 0 1 9 0M12 7v2.2M5.6 9.6l1.6 1.6M18.4 9.6l-1.6 1.6M3 13.5h2M19 13.5h2"/><path d="M9 20.5h6"/>',
    "histoire": '<path d="M4 20h16M5 9.5h14L12 4.5Z"/><path d="M7 10v7.5M10.3 10v7.5M13.7 10v7.5M17 10v7.5"/>',
    "nature": '<path d="m3 19 6.5-11 3.6 6 2.2-3.4L21 19Z"/><path d="M9.5 8 11 10.6"/>',
    "famille": '<circle cx="8" cy="6.5" r="2.2"/><circle cx="16.5" cy="9" r="1.8"/><path d="M4.5 20v-4.5A3.5 3.5 0 0 1 8 12a3.5 3.5 0 0 1 3.5 3.5V20M13.5 20v-3.6a3 3 0 0 1 6 0V20"/>',
    "nuit": '<path d="M3 19.5h18M5 19.5 12 6l7 13.5M12 6v13.5M9.5 19.5 12 15l2.5 4.5"/>',
    "signal": '<path d="M5 18.5h2v-3H5zM10 18.5h2v-6h-2zM15 18.5h2V9h-2z"/><path d="m4 4 16 16"/>',
    "traversier": '<path d="M3 15.5h18l-2.6 4H5.6Z"/><path d="M6 15.5v-4h12v4M9 11.5V8h6v3.5M12 8V5"/>',
    "photo": '<path d="M4 8h3.2L9 5.5h6L16.8 8H20v11H4Z"/><circle cx="12" cy="13.3" r="3.3"/>',
    "pause": '<path d="M9 6v12M15 6v12"/>',
    "play": '<path d="M8 5.5v13L18.5 12Z"/>',
    "restart": '<path d="M5 12a7 7 0 1 0 2-4.9M5 4.5V8h3.5"/>',
    "check": '<path d="m5 12.5 4.3 4.3L19 7"/>',
    "x": '<path d="m6.5 6.5 11 11M17.5 6.5l-11 11"/>',
    "route": '<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8.2 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.8"/>',
    "garage": '<path d="M3.5 20V9.5L12 4l8.5 5.5V20"/><path d="M7 20v-7h10v7M7 16h10"/>',
    "journal": '<path d="M6 3.5h11a1.5 1.5 0 0 1 1.5 1.5v15.5H7.5A1.5 1.5 0 0 1 6 19Z"/><path d="M6 17.5h12.5M9.5 8h5.5M9.5 11.5h4"/>',
    "vr": '<path d="M2.5 16.5V7.5a1 1 0 0 1 1-1h11.5v10M15 9.5h3.2l3.3 3.5v3.5H15"/><circle cx="7" cy="17.3" r="1.8"/><circle cx="17.6" cy="17.3" r="1.8"/><path d="M6 9.5h5M8.5 7v5"/>',
    "berline": '<path d="M3 16.5v-3l2.2-.6L8 8.8h7.4l3.4 4 2.2.7v3"/><circle cx="7" cy="16.8" r="1.8"/><circle cx="17" cy="16.8" r="1.8"/><path d="M8.8 16.8h6.4M8.6 12.6h9"/>',
    "sportive": '<path d="M2.5 16.3v-2l3.2-1.3 3.3-2.8h5.6l3.8 2.8 3.1.8v2.5"/><circle cx="7" cy="16.6" r="1.8"/><circle cx="17.3" cy="16.6" r="1.8"/><path d="M8.8 16.6h6.7"/>',
    "velo": '<circle cx="6" cy="16" r="3.5"/><circle cx="18" cy="16" r="3.5"/><path d="M6 16l4-7h5l3 7M10 9 8.8 6.5H7M15 9l-1.6-3h2.4M12.5 16 10 9"/>',
    "lock": '<rect x="5.5" y="10.5" width="13" height="9.5" rx="2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "unlock": '<rect x="5.5" y="10.5" width="13" height="9.5" rx="2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 6.8-1.2"/>',
    "chaud": '<path d="M12 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0Z"/><path d="M14 9v7"/>',
    "bolt": '<path d="M13 3 6 13.5h5.5L10.5 21 18 10.5h-5.5Z"/>',
    "pin": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/>',
    "shield": '<path d="M12 3.5 5 6.2v5.2c0 4.4 3 7.7 7 9.1 4-1.4 7-4.7 7-9.1V6.2Z"/><path d="m9 12 2.2 2.2L15.3 10"/>',
    "eye": '<path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="2.8"/>',
    "pneu": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5"/><path d="M12 3.5v5M12 15.5v5M3.5 12h5M15.5 12h5"/>',
    "zone": '<circle cx="12" cy="12" r="8.5" stroke-dasharray="2.4 2.4"/><path d="M12 15.5s-3-2.9-3-5.1a3 3 0 0 1 6 0c0 2.2-3 5.1-3 5.1Z"/>',
    "obd": '<rect x="3.5" y="7" width="17" height="10" rx="2.5"/><path d="M7 10.5h.01M10 10.5h.01M13 10.5h.01M16 10.5h.01M8.5 13.5h.01M11.5 13.5h.01M14.5 13.5h.01"/>',
    "son": '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4Z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
    "fleche": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "etoile": '<path d="m12 4 2.4 5 5.4.6-4 3.7 1.1 5.4L12 16l-4.9 2.7 1.1-5.4-4-3.7 5.4-.6Z"/>',
}


def ico(name, cls=""):
    c = f"mb-i {cls}".strip()
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{ICO[name]}</svg>'


# ---------------------------------------------------------------------------------------------
# Projection : kilomètres, origine au coin nord-ouest de la carte (73,9° O · 48,95° N)
# ---------------------------------------------------------------------------------------------
LON0, LAT1, LAT0 = -73.9, 48.95, 45.15
KX = 111.32 * math.cos(math.radians(47.05))
KY = 111.13
W = round((-68.4 - LON0) * KX, 1)
H = round((LAT1 - LAT0) * KY, 1)
ROAD = 1.16  # sinuosité : kilomètres de route par kilomètre à vol d’oiseau sur la carte


def P(lat, lon):
    return ((lon - LON0) * KX, (LAT1 - lat) * KY)


def _cr(pts, n=8, close=False):
    """Courbe lisse (Catmull-Rom) échantillonnée, passant par les points (lat, lon)."""
    xy = [P(*p) for p in pts]
    if close:
        ext = [xy[-1]] + xy + xy[:2]
    else:
        ext = [xy[0]] + xy + [xy[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                       + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)
                for j in (0, 1)))
    if not close:
        out.append(xy[-1])
    return out


def _d(xy, close=False):
    s = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
    return s + ("Z" if close else "")


# --- Eau --------------------------------------------------------------------------------------
NORTH_SHORE = [(45.36, -74.2), (45.52, -73.62), (45.66, -73.47), (45.86, -73.29), (46.03, -73.13), (46.22, -72.92),
               (46.28, -72.76), (46.37, -72.54), (46.46, -72.24), (46.62, -71.95), (46.72, -71.62), (46.80, -71.24),
               (46.87, -71.12), (46.99, -70.86), (47.11, -70.68), (47.28, -70.50), (47.43, -70.44), (47.52, -70.24),
               (47.64, -70.10), (47.80, -69.93), (47.97, -69.79), (48.13, -69.67), (48.30, -69.40), (48.50, -69.22),
               (48.74, -69.02), (48.98, -68.68), (49.22, -68.12), (49.30, -67.6)]
SOUTH_SHORE = [(45.33, -74.2), (45.50, -73.52), (45.73, -73.31), (45.96, -73.09), (46.10, -72.88), (46.22, -72.62),
               (46.32, -72.44), (46.47, -72.14), (46.60, -71.88), (46.71, -71.32), (46.79, -71.16), (46.84, -70.92),
               (46.96, -70.58), (47.10, -70.33), (47.30, -70.08), (47.56, -69.84), (47.83, -69.50), (48.12, -69.15),
               (48.30, -68.85), (48.45, -68.50), (48.58, -68.12), (48.70, -67.6)]
ORLEANS = [(46.84, -71.09), (46.88, -71.03), (46.95, -70.92), (47.01, -70.81), (47.03, -70.77), (46.99, -70.80),
           (46.93, -70.89), (46.87, -70.99)]
COUDRES = [(47.37, -70.42), (47.40, -70.37), (47.42, -70.34), (47.40, -70.33), (47.37, -70.38)]
LAC_ST_JEAN = [(48.44, -71.98), (48.47, -72.12), (48.52, -72.21), (48.62, -72.26), (48.73, -72.22), (48.81, -72.07),
               (48.80, -71.90), (48.73, -71.76), (48.62, -71.70), (48.53, -71.72), (48.47, -71.84)]
SAGUENAY = [(48.13, -69.70), (48.19, -69.86), (48.25, -70.02), (48.28, -70.25), (48.33, -70.52), (48.38, -70.78),
            (48.42, -70.95), (48.43, -71.07), (48.45, -71.25), (48.50, -71.45), (48.54, -71.62)]
RIVIERES = [
    [(46.35, -72.54), (46.50, -72.70), (46.62, -72.74), (46.78, -72.66), (46.98, -72.72), (47.20, -72.80), (47.44, -72.78), (47.70, -72.90), (47.95, -73.05)],
    [(45.05, -73.30), (45.31, -73.26), (45.53, -73.21), (46.04, -73.11)],  # Richelieu
    [(45.05, -72.27), (45.15, -72.27), (45.24, -72.24), (45.30, -72.21), (45.35, -72.25)],  # Memphrémagog
    [(48.52, -72.23), (48.64, -72.45), (48.78, -72.62), (48.98, -72.68)],  # Ashuapmushuan
    [(48.80, -71.90), (48.95, -71.85), (49.10, -71.80)],  # Péribonka
]

# --- Routes (secondaires, discrètes) ----------------------------------------------------------
ROADS = [
    [(45.52, -73.62), (46.10, -73.20), (46.36, -72.58), (46.62, -72.02), (46.80, -71.32)],  # 40
    [(45.50, -73.50), (45.44, -73.05), (45.40, -72.73), (45.30, -72.20), (45.39, -71.90)],  # 10
    [(45.88, -72.48), (45.62, -72.18), (45.40, -71.90)],  # 55 sud
    [(45.88, -72.48), (46.14, -72.52), (46.35, -72.56)],  # 55 nord
    [(46.80, -71.10), (46.92, -70.56), (47.18, -70.16), (47.50, -69.86), (47.80, -69.55), (48.10, -69.20), (48.43, -68.53)],  # 20 / 132
    [(46.86, -71.28), (47.10, -71.36), (47.45, -71.24), (47.80, -71.20), (48.10, -71.14), (48.41, -71.08)],  # 175
    [(46.36, -72.53), (46.56, -72.73), (46.86, -72.66), (47.16, -72.74), (47.45, -72.75)],  # 155
    [(48.13, -69.72), (48.33, -69.47), (48.73, -69.12), (48.98, -68.80)],  # 138 est
    [(48.52, -72.25), (48.63, -72.30), (48.76, -72.26), (48.86, -72.02), (48.82, -71.84), (48.70, -71.70), (48.56, -71.66)],  # 169 nord
]

# --- Relief : courbes de niveau fines, masquées par l'eau --------------------------------------
RELIEF = [  # (lat, lon, rayon km, anneaux, phase)
    (47.62, -71.30, 52, 7, 0.4), (47.66, -70.62, 26, 5, 1.7), (48.62, -70.75, 30, 5, 2.6),
    (46.82, -73.05, 30, 5, 3.4), (45.30, -72.30, 17, 4, 4.1), (46.30, -70.75, 26, 4, 5.0),
    (47.35, -72.30, 34, 5, 0.9), (48.05, -72.60, 34, 5, 2.2),
]


def _dc(xy):
    """Contour fermé lisse : Catmull-Rom converti en courbes de Bézier."""
    n = len(xy)
    out = [f"M{xy[0][0]:.0f} {xy[0][1]:.0f}"]
    for i in range(n):
        p0, p1, p2, p3 = xy[i - 1], xy[i], xy[(i + 1) % n], xy[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(f"C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {p2[0]:.0f} {p2[1]:.0f}")
    return "".join(out) + "Z"


def _relief():
    out = []
    for lat, lon, r0, n, ph in RELIEF:
        cx, cy = P(lat, lon)
        for k in range(n):
            r = r0 * (1 - k / (n + 0.6))
            pts = []
            for s in range(22):
                a = s / 22 * 2 * math.pi
                f = 1 + 0.17 * math.sin(3 * a + ph + k * 0.35) + 0.09 * math.sin(5 * a + ph * 2 - k * 0.2) + 0.05 * math.sin(9 * a + ph)
                pts.append((cx + math.cos(a) * r * f * 1.15, cy + math.sin(a) * r * f * 0.85))
            out.append(_dc(pts))
    return out


# --- Trajet du copilote : Saint-Hyacinthe → Québec → Charlevoix → Tadoussac → Lac-Saint-Jean --
ROUTE_WP = [(45.63, -72.96), (45.76, -72.68), (45.88, -72.48), (46.05, -72.18), (46.22, -71.95), (46.40, -71.75),
            (46.57, -71.54), (46.70, -71.36), (46.81, -71.21), (46.88, -71.16), (46.94, -71.02), (46.99, -70.90),
            (47.06, -70.78), (47.20, -70.70), (47.34, -70.60), (47.44, -70.51), (47.53, -70.36), (47.65, -70.17),
            (47.80, -70.00), (47.97, -69.86), (48.10, -69.74), (48.15, -69.73), (48.27, -69.93), (48.33, -70.25),
            (48.38, -70.55), (48.43, -70.86), (48.42, -71.06), (48.47, -71.30), (48.52, -71.50), (48.55, -71.66),
            (48.44, -71.84), (48.42, -72.00), (48.46, -72.16), (48.52, -72.26)]

STOPS = [  # (nom, lat, lon, importance) — importance 2 : ville du trajet, 1 : repère discret
    ("Saint-Hyacinthe", 45.63, -72.96, 2), ("Drummondville", 45.88, -72.48, 1), ("Québec", 46.81, -71.21, 2),
    ("Baie-Saint-Paul", 47.44, -70.50, 2), ("La Malbaie", 47.65, -70.15, 2), ("Tadoussac", 48.14, -69.72, 2),
    ("Saguenay", 48.42, -71.06, 2, "b"), ("Alma", 48.55, -71.65, 1), ("Roberval", 48.52, -72.23, 2, "l"),
    ("Montréal", 45.50, -73.57, 1), ("Trois-Rivières", 46.35, -72.55, 1), ("Rivière-du-Loup", 47.83, -69.53, 1),
    ("Rimouski", 48.45, -68.52, 1), ("Sherbrooke", 45.40, -71.89, 1), ("La Tuque", 47.44, -72.78, 1),
]
WATER_LABELS = [("Fleuve Saint-Laurent", 47.55, -69.65, -38), ("Fjord du Saguenay", 48.33, -70.42, -10),
                ("Lac Saint-Jean", 48.64, -71.98, 0), ("Lac Saint-Pierre", 46.19, -72.85, -25)]
REGION_LABELS = [("Charlevoix", 47.78, -70.62), ("Réserve des Laurentides", 47.62, -71.35), ("Mauricie", 46.95, -73.25),
                 ("Bas-Saint-Laurent", 47.95, -68.95), ("Cantons-de-l’Est", 45.55, -71.75), ("Centre-du-Québec", 46.10, -71.85)]


def _route():
    pts = _cr(ROUTE_WP, 10)
    km = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        km.append(km[-1] + math.hypot(x1 - x0, y1 - y0) * ROAD)
    return pts, km


ROUTE_PTS, ROUTE_KM = _route()
ROUTE_LEN = ROUTE_KM[-1]


def _km_of(lat, lon):
    x, y = P(lat, lon)
    i = min(range(len(ROUTE_PTS)), key=lambda k: (ROUTE_PTS[k][0] - x) ** 2 + (ROUTE_PTS[k][1] - y) ** 2)
    return ROUTE_KM[i]


def _at(km, off=0.0):
    """Point du trajet au kilomètre km, décalé de off km vers la gauche de la direction."""
    i = 1
    while i < len(ROUTE_KM) - 1 and ROUTE_KM[i] < km:
        i += 1
    (x0, y0), (x1, y1) = ROUTE_PTS[i - 1], ROUTE_PTS[i]
    seg = max(ROUTE_KM[i] - ROUTE_KM[i - 1], 1e-6)
    t = min(max((km - ROUTE_KM[i - 1]) / seg, 0), 1)
    x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy) or 1
    return x + dy / n * off, y - dx / n * off


K = {st[0]: _km_of(st[1], st[2]) for st in STOPS if st[3] == 2 or st[0] in ("Drummondville", "Alma")}

# ---------------------------------------------------------------------------------------------
# Points d'intérêt du copilote (Données d'exemple : aucun commerce réel n'est nommé)
#   cat : repas · eau · propane · webasto · meca · soleil · histoire · nature · famille · nuit · signal · traversier
#   km : position sur le trajet (repère + écart) · off : distance de la route (km) · stop : durée de l'arrêt (min)
#   h : heures d'ouverture (début, fin) en minutes · photo : souvenir enregistré au journal si accepté
# ---------------------------------------------------------------------------------------------
def _poi(pid, cat, nom, ref, dk, off, stop, h, why, photo_nom=None, val=None):
    return {"id": pid, "cat": cat, "nom": nom, "km": round(K[ref] + dk, 1), "off": off, "stop": stop,
            "h": h, "why": why, "photo": photo_nom, "val": val}


POIS = [
    _poi("eau1", "eau", "Halte routière · eau potable gratuite", "Québec", -48, 0.4, 12, (0, 1440),
         "Remplissage gratuit, accès facile pour un véhicule de 7 m."),
    _poi("diner1", "repas", "Bistro au bord du fleuve", "Québec", -9, 1.6, 50, (660, 1260),
         "Terrasse vue sur le fleuve, stationnement pour véhicules longs.", "bistro-fleuve"),
    _poi("vieuxqc", "histoire", "Vieux-Québec", "Québec", 3, 4, 120, (0, 1440),
         "Site du patrimoine mondial : remparts, Petit-Champlain, terrasse Dufferin.", "vieux-quebec"),
    _poi("montmo", "nature", "Chute Montmorency", "Québec", 13, 0.5, 40, (540, 1080),
         "Plus haute que les chutes Niagara : 83 m. Escalier panoramique et pont suspendu.", "chute-montmorency"),
    _poi("orleans", "repas", "Île d’Orléans · route des produits locaux", "Québec", 17, 5, 75, (600, 1080),
         "Fromages, cidres et petits fruits chez les producteurs de l’île.", "ile-orleans"),
    _poi("propane1", "propane", "Station-service · poste de propane", "Québec", 27, 0.6, 15, (420, 1200),
         "Remplissage de bonbonne et de réservoir fixe sur place."),
    _poi("famille1", "famille", "Parc et aire de jeux au bord du fleuve", "Québec", 38, 0.8, 30, (480, 1200),
         "Grands espaces, toilettes propres, sentier plat pour les enfants."),
    _poi("webasto", "webasto", "Garage spécialisé · chauffage d’appoint", "Baie-Saint-Paul", -6, 1.2, 60, (480, 1020),
         "450 h de fonctionnement depuis le dernier entretien : nettoyage et vérification avant l’hiver.", None, "450 h"),
    _poi("bsp", "histoire", "Baie-Saint-Paul · village des artistes", "Baie-Saint-Paul", 0, 0.6, 60, (600, 1080),
         "Galeries d’art et rue Saint-Jean-Baptiste, à pied depuis le stationnement.", "baie-saint-paul"),
    _poi("belv1", "soleil", "Belvédère sur le fleuve · Charlevoix", "Baie-Saint-Paul", 21, 0.4, 35, (0, 1440),
         "Vue dégagée vers l’ouest : le soleil se couche dans l’axe du fleuve.", "charlevoix-belvedere"),
    _poi("meca1", "meca", "Vérification des freins avant les côtes", "Baie-Saint-Paul", 4, 0.9, 20, (480, 1020),
         "Descente de 12 % vers Baie-Saint-Paul : JARVIS a mesuré une chauffe des freins à la dernière côte.", None),
    _poi("souper", "repas", "Table du terroir de Charlevoix", "La Malbaie", 2, 1.4, 70, (1050, 1290),
         "Menu du terroir, réservation conseillée le samedi.", "table-terroir"),
    _poi("eau2", "eau", "Poste de vidange et eau potable", "La Malbaie", 14, 0.9, 15, (480, 1260),
         "Vidange des eaux grises et remplissage au même endroit.", None),
    _poi("traversier", "traversier", "Traversier Baie-Sainte-Catherine → Tadoussac", "Tadoussac", -4, 0, 20, (0, 1440),
         "Gratuit, départ aux 20 minutes; JARVIS calcule l’attente selon votre heure d’arrivée.", None),
    _poi("baleines", "nature", "Observation des baleines", "Tadoussac", 3, 0.5, 150, (540, 1080),
         "Bélugas et rorquals jusqu’à la fin d’octobre; sorties en mer et sentier de la Pointe-de-l’Islet.", "tadoussac-fjord"),
    _poi("belv2", "soleil", "Pointe-Noire · embouchure du fjord", "Tadoussac", -2, 0.8, 30, (0, 1440),
         "Le soleil se couche sur le fjord : la falaise s’allume en orange 20 minutes avant.", "pointe-noire"),
    _poi("signal1", "signal", "Zone sans réseau cellulaire · 62 km", "Tadoussac", 26, 0, 0, (0, 1440),
         "Cartes, itinéraire et musique téléchargés d’avance par JARVIS.", None),
    _poi("propane2", "propane", "Dernier poste de propane avant le fjord", "Tadoussac", 6, 0.7, 15, (480, 1080),
         "Après ce poste, le prochain ouvert est à Saguenay.", None),
    _poi("nuit1", "nuit", "Emplacement gratuit au bord du fjord", "Tadoussac", 52, 1.8, 0, (0, 1440),
         "Toléré pour une nuit, sans services; vue sur le fjord au lever du soleil.", "fjord-saguenay"),
    _poi("fjordparc", "nature", "Parc national du Fjord-du-Saguenay · sentier", "Tadoussac", 70, 3.5, 120, (480, 1080),
         "Sentier de la Statue : 7 km aller-retour, falaises de 350 m au-dessus du fjord.", "fjord-sentier"),
    _poi("famille2", "famille", "Village historique et chute · Lac-Saint-Jean", "Roberval", -14, 3, 120, (570, 1050),
         "Village ouvrier de 1901, chute de 72 m, téléphérique : idéal avec des enfants.", "val-jalbert"),
    _poi("bleuets", "repas", "Comptoir de bleuets et chocolaterie", "Alma", 9, 0.5, 20, (540, 1140),
         "Spécialités du Lac-Saint-Jean : bleuets enrobés de chocolat.", None),
    _poi("plage", "nature", "Grande plage du Lac-Saint-Jean", "Alma", 24, 1.2, 60, (0, 1440),
         "Sable fin et coucher de soleil sur le lac; aurores possibles par nuit claire.", "lac-saint-jean"),
    _poi("diner2", "repas", "Casse-croûte de la route du fjord", "Saguenay", -38, 0.3, 35, (660, 1200),
         "Poutine et guédille, service rapide.", None),
    _poi("eau3", "eau", "Camping municipal · eau et vidange", "Saguenay", 6, 1.5, 15, (480, 1260),
         "Remplissage sans réservation, 5 $ pour les visiteurs.", None),
]
WATER_POLY = _cr(NORTH_SHORE, 6) + list(reversed(_cr(SOUTH_SHORE, 6)))
LAKE_POLY = _cr(LAC_ST_JEAN, 6, close=True)


def _inside(pt, poly):
    x, y = pt
    c = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def _wet(pt):
    return _inside(pt, WATER_POLY) or _inside(pt, LAKE_POLY)


for p in POIS:
    vis = max(p["off"], 4.2)  # écart visuel minimal : le repère ne cache ni la route ni la ville
    a, b = _at(p["km"], vis), _at(p["km"], -vis)
    x, y = b if _wet(a) and not _wet(b) else a
    p["x"], p["y"] = round(x, 2), round(y, 2)

# Souvenirs pris automatiquement en roulant (Voyage en cours) : photo géolocalisée au passage.
AUTO_SHOTS = [
    ("Drummondville", 3, "Lever du jour sur l’autoroute 20, première pause café", "aube-autoroute-20"),
    ("Québec", 2, "Arrivée sur le pont, le Château Frontenac au loin", "vieux-quebec"),
    ("Baie-Saint-Paul", -9, "La descente vers Baie-Saint-Paul et l’Isle-aux-Coudres", "baie-saint-paul"),
    ("La Malbaie", 6, "Le fleuve à marée haute, La Malbaie", "charlevoix-belvedere"),
    ("Tadoussac", 1, "Le traversier entre dans l’embouchure du fjord", "tadoussac-fjord"),
    ("Saguenay", -60, "Les falaises du fjord depuis la route 172", "fjord-saguenay"),
    ("Roberval", -2, "Le Lac-Saint-Jean à perte de vue", "lac-saint-jean"),
]

# ---------------------------------------------------------------------------------------------
# Photos du journal : media/mobilite/<nom>.webp, sinon une photo existante qui convient
# ---------------------------------------------------------------------------------------------
REPLI = {  # photos existantes du site qui conviennent, en attendant les photos de media/mobilite/
    "lac-saint-jean": "/media/app/banniere-lac.webp",
    "charlevoix-belvedere": "/media/ambiances/heure-doree.webp",
    "mauricie-lac": "/media/vr/chambre.webp",
    "mauricie-aurores": "/media/ambiances/aurore.webp",
    "mauricie-bivouac": "/media/vr/exterieur.webp",
}
PHOTOS = {}
PHOTO_DESC = {
    "aube-autoroute-20": "Lever du jour sur une autoroute du Centre-du-Québec, champs givrés, VR noir de dos",
    "hero": "VR noir sur une route de Charlevoix à l’heure dorée, le fleuve en contrebas (bannière de la page)",
    "vieux-quebec": "Vieux-Québec en soirée d’automne : remparts, rues de pierre, Château Frontenac au loin",
    "bistro-fleuve": "Terrasse de bistro au bord du fleuve à Lévis, Québec en face (aucune enseigne lisible)",
    "chute-montmorency": "Chute Montmorency avec le pont suspendu, lumière d’automne",
    "ile-orleans": "Champs et kiosque de produits sur l’Île d’Orléans, le fleuve derrière",
    "baie-saint-paul": "Baie-Saint-Paul vue de la côte : la baie, le village et l’Isle-aux-Coudres",
    "charlevoix-belvedere": "Coucher de soleil sur le fleuve depuis un belvédère de Charlevoix",
    "table-terroir": "Table dressée avec produits du terroir de Charlevoix, fenêtre sur le fleuve",
    "tadoussac-fjord": "Embouchure du fjord à Tadoussac : dunes, eau sombre, dos de baleine",
    "pointe-noire": "Falaise de la Pointe-Noire au coucher du soleil, fjord orangé",
    "fjord-saguenay": "VR noir garé au belvédère du fjord du Saguenay, falaises au lever du jour",
    "fjord-sentier": "Randonneur au sommet d’une falaise de 350 m au-dessus du fjord",
    "val-jalbert": "Chute de 72 m et vieux village ouvrier du Lac-Saint-Jean",
    "lac-saint-jean": "Plage du Lac-Saint-Jean au crépuscule, horizon d’eau à perte de vue",
    "mauricie-aurores": "Aurores boréales au-dessus d’un lac de la Haute-Mauricie, vues depuis le VR",
    "mauricie-bivouac": "VR noir en bivouac au bord de la rivière Saint-Maurice, montagnes au crépuscule",
    "trois-rivieres": "Vieux-Trois-Rivières et le fleuve au coucher du soleil",
    "shawinigan": "Chute et centrale historique de Shawinigan",
    "mauricie-lac": "Lac du parc national de la Mauricie au matin, canot sur la rive",
    "la-tuque": "Rivière Saint-Maurice et forêt boréale près de La Tuque",
    "magog": "Lac Memphrémagog et le mont Orford, fin de journée",
    "north-hatley": "Village de North Hatley au bord du lac Massawippi",
    "vignoble": "Vignoble des Cantons-de-l’Est, rangs de vigne en pente",
    "sherbrooke": "Gorge de la rivière Magog à Sherbrooke",
    "cote-beaupre": "Route de la Côte-de-Beaupré, fleuve et Île d’Orléans à droite",
    "sainte-anne": "Canyon et chute Sainte-Anne, passerelle suspendue",
    "berline-electrique": "Berline électrique noire sans logo, recharge dans un garage moderne",
    "sportive": "Voiture sport rouge sans logo dans un garage sombre",
    "velo-electrique": "Vélo électrique noir et or appuyé contre un mur, lumière du soir",
}


def ph(nom):
    if nom not in PHOTOS:
        PHOTOS[nom] = photo(nom, REPLI.get(nom))
    return PHOTOS[nom]


# ---------------------------------------------------------------------------------------------
# Journal : voyages passés et voyage en cours
# ---------------------------------------------------------------------------------------------
TRIPS = [
    {"id": "encours", "nom": "Charlevoix, fjord et Lac-Saint-Jean", "quand": "En cours · 8 novembre 2026",
     "jours": 3, "wp": None, "cover": "lac-saint-jean", "live": True,
     "entries": [
         ("Saint-Hyacinthe", 45.63, -72.96, "9 h 05", "Départ · plein d’essence fait, eau propre à 24 %", None),
     ]},
    {"id": "mauricie", "nom": "Mauricie et Haute-Mauricie", "quand": "Août 2026 · 4 jours", "jours": 4,
     "wp": [(45.63, -72.96), (45.88, -72.48), (46.14, -72.52), (46.35, -72.55), (46.56, -72.74), (46.76, -72.82),
            (46.86, -72.66), (47.16, -72.74), (47.44, -72.78)],
     "cover": "mauricie-lac",
     "entries": [
         ("Trois-Rivières", 46.35, -72.55, "Jour 1 · 11 h 20", "Dîner au Vieux-Trois-Rivières, vue sur le fleuve", "trois-rivieres"),
         ("Shawinigan", 46.56, -72.74, "Jour 1 · 15 h 40", "Les chutes et la vieille centrale", "shawinigan"),
         ("Parc national de la Mauricie", 46.76, -72.82, "Jour 2 · 7 h 10", "Réveil au bord du lac, canot avant le déjeuner", "mauricie-lac"),
         ("Haute-Mauricie", 47.16, -72.74, "Jour 3 · 22 h 40", "Aurores boréales au-dessus du lac, vues depuis le lit", "mauricie-aurores"),
         ("La Tuque", 47.44, -72.78, "Jour 4 · 19 h 05", "Bivouac au bord de la Saint-Maurice", "mauricie-bivouac"),
     ]},
    {"id": "cantons", "nom": "Cantons-de-l’Est", "quand": "Juin 2026 · 2 jours", "jours": 2,
     "wp": [(45.63, -72.96), (45.48, -72.80), (45.40, -72.73), (45.30, -72.40), (45.27, -72.15), (45.24, -72.02),
            (45.29, -71.96), (45.40, -71.89)],
     "cover": "magog",
     "entries": [
         ("Granby", 45.40, -72.73, "Jour 1 · 10 h 15", "Café et marché public", None),
         ("Magog", 45.27, -72.15, "Jour 1 · 16 h 30", "Le lac Memphrémagog et le mont Orford", "magog"),
         ("Vignoble", 45.24, -72.02, "Jour 2 · 13 h 00", "Dégustation sur les pentes", "vignoble"),
         ("North Hatley", 45.29, -71.96, "Jour 2 · 15 h 20", "Promenade au bord du lac Massawippi", "north-hatley"),
         ("Sherbrooke", 45.40, -71.89, "Jour 2 · 18 h 10", "La gorge de la rivière Magog", "sherbrooke"),
     ]},
    {"id": "beaupre", "nom": "Côte-de-Beaupré et Île d’Orléans", "quand": "Septembre 2026 · 2 jours", "jours": 2,
     "wp": [(46.81, -71.21), (46.88, -71.16), (46.94, -71.02), (46.92, -70.95), (46.99, -70.86), (47.06, -70.78),
            (47.07, -70.58)],
     "cover": "ile-orleans",
     "entries": [
         ("Chute Montmorency", 46.89, -71.15, "Jour 1 · 10 h 00", "Le pont suspendu au-dessus de la chute", "chute-montmorency"),
         ("Île d’Orléans", 46.95, -70.95, "Jour 1 · 13 h 30", "Cidre et fraises d’automne", "ile-orleans"),
         ("Côte-de-Beaupré", 47.03, -70.82, "Jour 2 · 9 h 15", "La route du fleuve au matin", "cote-beaupre"),
         ("Canyon Sainte-Anne", 47.07, -70.58, "Jour 2 · 11 h 40", "Passerelle au-dessus du canyon", "sainte-anne"),
     ]},
]

# Statistiques des voyages (calculées à partir des tracés : aucune donnée inventée à la main)


def _trip_geo(t):
    if t["wp"] is None:
        pts = ROUTE_PTS
    else:
        pts = _cr(t["wp"], 8)
    km = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])) * ROAD
    return pts, km


TRIPS_JS = []
for t in TRIPS:
    pts, km = _trip_geo(t)
    ents = []
    for nom, lat, lon, quand, note, pnom in t["entries"]:
        x, y = P(lat, lon)
        ents.append({"lieu": nom, "x": round(x, 2), "y": round(y, 2), "quand": quand, "note": note,
                     "src": ph(pnom) if pnom else None, "geo": f"{lat:.2f}".replace(".", ",") + "° N · "
                     + f"{-lon:.2f}".replace(".", ",") + "° O"})
    TRIPS_JS.append({"id": t["id"], "nom": t["nom"], "quand": t["quand"], "jours": t["jours"], "km": round(km),
                     "live": t.get("live", False), "d": _d(pts), "cover": ph(t["cover"]), "entries": ents})

AUTO_JS = []
for ref, dk, note, pnom in AUTO_SHOTS:
    km = K[ref] + dk
    x, y = _at(km)
    AUTO_JS.append({"km": round(km, 1), "x": round(x, 2), "y": round(y, 2), "note": note, "src": ph(pnom), "lieu": ref})

for p in POIS:
    p["src"] = ph(p["photo"]) if p["photo"] else None


# ---------------------------------------------------------------------------------------------
# Modes de voyage : chaque mode est un guide qui pondère les catégories (0 = jamais proposé)
# ---------------------------------------------------------------------------------------------
MODES = [
    ("decouverte", "Découverte", "Histoire, patrimoine et incontournables, sans rien manquer.", "histoire",
     {"histoire": 3, "nature": 2, "soleil": 2, "repas": 1.5, "famille": .5, "eau": 1, "propane": 1, "webasto": 1, "meca": 1, "traversier": 1, "nuit": .8, "signal": .6}),
    ("efficace", "Efficace", "Le moins de détours possible : seulement l’essentiel, au plus près de la route.", "route",
     {"repas": 1.2, "eau": 1.5, "propane": 1.5, "webasto": .8, "meca": 1.5, "traversier": 2, "signal": 1, "soleil": .4}),
    ("nature", "Nature", "Belvédères, sentiers, faune et lumière du jour au bon moment.", "nature",
     {"nature": 3, "soleil": 3, "nuit": 1.5, "eau": 1, "propane": 1, "repas": .8, "histoire": .5, "webasto": 1, "meca": 1, "traversier": 1, "signal": .8}),
    ("gourmand", "Gourmand", "Tables du terroir, producteurs et spécialités régionales.", "repas",
     {"repas": 3, "histoire": 1, "nature": .8, "soleil": 1, "eau": 1, "propane": 1, "webasto": 1, "meca": 1, "traversier": 1}),
    ("famille", "Famille", "Pauses régulières, parcs, toilettes et activités pour les enfants.", "famille",
     {"famille": 3, "repas": 2, "nature": 1.5, "histoire": 1, "eau": 1.2, "propane": 1, "webasto": 1, "meca": 1.2, "traversier": 1.5, "soleil": 1}),
    ("horsreseau", "Hors réseau", "Autonomie d’abord : eau, propane, nuits gratuites et zones sans réseau.", "signal",
     {"eau": 3, "propane": 3, "nuit": 3, "signal": 3, "webasto": 2, "meca": 1.5, "nature": 1.5, "soleil": 1.2, "repas": .6, "traversier": 1}),
]

CAT_LABEL = {"repas": "Repas", "eau": "Eau propre", "propane": "Propane", "webasto": "Webasto", "meca": "Entretien mécanique",
             "soleil": "Soleil", "histoire": "Histoire", "nature": "Nature", "famille": "Famille", "nuit": "Nuit",
             "signal": "Réseau", "traversier": "Traversier"}

# ---------------------------------------------------------------------------------------------
# Garage : véhicules connectés
#   src : « c » = connexion du constructeur · « b » = boîtier JARVIS (OBD-II + GPS + batterie)
#         « t » = traceur JARVIS (GPS + mouvement) · None = non offert
# ---------------------------------------------------------------------------------------------
CAPS = [("loc", "Localisation", "pin"), ("lock", "Verrouillage", "lock"), ("clim", "Préchauffage / climatisation", "chaud"),
        ("nrj", "Énergie et recharge", "bolt"), ("pneus", "Pression des pneus", "pneu"), ("diag", "Codes défaut (diagnostic)", "obd"),
        ("garde", "Alerte de mouvement", "eye"), ("zone", "Géorepérage", "zone")]

VEHICLES = [
    {"id": "vr", "nom": "VR BouLance", "type": "Ambulance Ford 2017 convertie", "ico": "vr",
     "img": "/media/ambulance/ambulance-ford-2017-hd.jpg", "pos": "50% 62%", "real_photo": True,
     "conn": "Boîtier JARVIS + Hub de la cellule", "connk": "b",
     "where": "En route · A-20, près de Québec", "lvl": ("Carburant", 54),
     "caps": {"loc": "b", "lock": None, "clim": None, "nrj": "b", "pneus": "b", "diag": "b", "garde": "b", "zone": "b"},
     "stats": [("Carburant", "54 % · 410 km", 54), ("Batterie du moteur", "12,7 V", 92), ("Eau propre · cellule", "22 %", 22), ("Propane · cellule", "31 %", 31)],
     "info": [("Webasto", "Entretien dû · 450 h"), ("Pneus", "80 psi · 4 sur 4 conformes"), ("Kilométrage", "148 320 km"), ("Codes défaut", "Aucun")],
     "cmds": [("diag", "Lancer un diagnostic OBD-II", "obd", "Lire les codes défaut et l’état du moteur maintenant?",
               "Confirmé · aucun code défaut, moteur à 88 °C, freins à surveiller dans les côtes."),
              ("garde", "Activer l’alerte de mouvement", "eye", "Activer l’alerte si le VR bouge sans vous?",
               "Confirmé · alerte de mouvement armée."),
              ("partage", "Partager ma position pendant 2 h", "pin", "Partager la position du VR avec Camille pendant 2 heures?",
               "Confirmé · position partagée jusqu’à 13 h 05, arrêt automatique ensuite.")],
     "note": "La cellule (lumières, eau, énergie, chauffage Webasto) se gère dans Environnements; ses niveaux d’eau et de propane guident le copilote. Ici : le véhicule et le trajet."},
    {"id": "ev", "nom": "Berline électrique", "type": "Connexion du constructeur", "ico": "berline",
     "img": ph("berline-electrique") or "/media/solutions/camera-garage-supercars-v1.webp", "pos": "36% 66%",
     "zoom": not bool(photo("berline-electrique")),
     "conn": "Connexion du constructeur (application officielle autorisée)", "connk": "c",
     "where": "Maison · garage, Saint-Hyacinthe", "lvl": ("Batterie", 72),
     "caps": {"loc": "c", "lock": "c", "clim": "c", "nrj": "c", "pneus": "c", "diag": "b", "garde": "c", "zone": "b"},
     "stats": [("Batterie", "72 % · 338 km", 72), ("Limite de recharge", "80 %", 80)],
     "info": [("Recharge", "Branchée · reprise à 21 h (tarif réduit)"), ("Mode Sentinelle", "Désactivé à la maison"), ("Portes", "Verrouillées")],
     "cmds": [("clim", "Préchauffer l’habitacle", "chaud", "Préchauffer l’habitacle à 21 °C pour un départ à 7 h 30?",
               "Confirmé · habitacle à 21 °C à 7 h 30, dégivrage compris."),
              ("lock", "Déverrouiller", "unlock", "Déverrouiller la berline? Elle est dans le garage, à 0 m de vous.",
               "Confirmé · état relu : portes déverrouillées. Reverrouillage automatique dans 2 min."),
              ("sentinelle", "Activer le mode Sentinelle", "eye", "Activer le mode Sentinelle (caméras du véhicule en veille)?",
               "Confirmé · Sentinelle active."),
              ("charge", "Recharger maintenant", "bolt", "Commencer la recharge maintenant, au tarif de jour?",
               "Confirmé · recharge en cours, 11 kW.")],
     "note": "Tout ce que le constructeur autorise passe par sa connexion officielle; JARVIS n’invente pas de commande."},
    {"id": "sport", "nom": "Sportive", "type": "Sans application · boîtier JARVIS de base", "ico": "sportive",
     "img": ph("sportive") or "/media/solutions/camera-garage-supercars-v1.webp", "pos": "74% 64%",
     "zoom": not bool(photo("sportive")),
     "conn": "Boîtier JARVIS de base : OBD-II + GPS + batterie de secours", "connk": "b",
     "where": "Remisée · garage, Saint-Hyacinthe", "lvl": ("Batterie 12 V", 88),
     "caps": {"loc": "b", "lock": None, "clim": None, "nrj": "b", "pneus": "b", "diag": "b", "garde": "b", "zone": "b"},
     "stats": [("Batterie 12 V", "12,6 V · 88 %", 88), ("Essence", "61 %", 61)],
     "tires": ["34", "34", "36", "35"],
     "info": [("Codes défaut", "Aucun"), ("Remisage", "Mainteneur de charge branché"), ("Zone", "Garage · rayon de 150 m")],
     "cmds": [("garage", "Activer le mode garage", "garage", "Activer le mode garage? Vous serez averti si le moteur démarre ou si la voiture sort de la zone.",
               "Confirmé · mode garage actif, zone de 150 m."),
              ("zone", "Me prévenir si elle sort de la zone", "zone", "Activer l’alerte de géorepérage autour du garage?",
               "Confirmé · géorepérage actif.")],
     "note": "Pas d’application? Le boîtier se branche au port OBD-II : état, pneus, position et alertes. Verrouiller ou chauffer à distance demande la connexion du constructeur."},
    {"id": "velo", "nom": "Vélo électrique", "type": "Traceur JARVIS · GPS + mouvement", "ico": "velo",
     "img": ph("velo-electrique"), "pos": "50% 50%",
     "conn": "Traceur JARVIS dissimulé dans le cadre", "connk": "t",
     "where": "Porte-vélo du VR · en route", "lvl": ("Batterie", 64),
     "caps": {"loc": "t", "lock": None, "clim": None, "nrj": "t", "pneus": None, "diag": None, "garde": "t", "zone": "t"},
     "stats": [("Batterie", "64 % · 48 km", 64)],
     "info": [("Antivol", "Armé · alarme sonore et alerte"), ("Position", "Suit le VR (porte-vélo)")],
     "cmds": [("son", "Faire sonner le vélo", "son", "Faire sonner l’alarme du vélo pendant 10 secondes?",
               "Confirmé · alarme déclenchée 10 s."),
              ("antivol", "Désarmer l’antivol", "unlock", "Désarmer l’antivol du vélo? Il ne vous préviendra plus s’il bouge.",
               "Confirmé · antivol désarmé. Réarmement automatique à 22 h.")],
     "note": "Un petit traceur suffit : batterie, position et alerte si quelqu’un le déplace."},
]


# ---------------------------------------------------------------------------------------------
# Rendu
# ---------------------------------------------------------------------------------------------
VB_CO = (26, 0, 356, 404)  # cadrage du copilote : le trajet, sans les marges vides
VB_JO = (0, 0, W, H)        # journal : toute la région (Mauricie et Cantons-de-l’Est compris)


def _pct(x, y, vb=VB_CO):
    return f"left:{(x - vb[0]) / vb[2] * 100:.2f}%;top:{(y - vb[1]) / vb[3] * 100:.2f}%"


WATER_D = _d(_cr(NORTH_SHORE, 6) + list(reversed(_cr(SOUTH_SHORE, 6))), True)
LAKE_D = _d(_cr(LAC_ST_JEAN, 6, close=True), True)
ISLES_D = _d(_cr(ORLEANS, 4, close=True), True) + _d(_cr(COUDRES, 4, close=True), True)
FJORD_D = _d(_cr(SAGUENAY, 6))
RIVERS_D = "".join(_d(_cr(r, 6)) for r in RIVIERES)
ROADS_D = "".join(_d(_cr(r, 6)) for r in ROADS)
RELIEF_D = "".join(_relief())
ROUTE_D = _d(ROUTE_PTS)


def defs_svg():
    """Fond de carte partagé (une seule copie dans la page) : terre, relief fin, eau, routes."""
    grat = "".join(f"M0 {P(lat, LON0)[1]:.1f}H{W}" for lat in (46, 47, 48)) + "".join(
        f"M{P(LAT1, lon)[0]:.1f} 0V{H}" for lon in (-73, -72, -71, -70, -69))
    return f"""<svg class="mb-defs" width="0" height="0" aria-hidden="true" focusable="false">
  <defs>
    <radialGradient id="mb-glow" cx="55%" cy="45%" r="70%"><stop offset="0" stop-color="#16140f"/><stop offset=".6" stop-color="#0a0908"/><stop offset="1" stop-color="#040404"/></radialGradient>
    <pattern id="mb-dots" width="3.2" height="3.2" patternUnits="userSpaceOnUse"><circle cx="1.6" cy="1.6" r=".32" fill="#fff" fill-opacity=".07"/></pattern>
    <mask id="mb-land" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/><path d="{WATER_D}{LAKE_D}" fill="#000"/><path d="{FJORD_D}" stroke="#000" stroke-width="3" fill="none"/><path d="{ISLES_D}" fill="#fff"/></mask>
    <linearGradient id="mb-route" gradientUnits="userSpaceOnUse" x1="{ROUTE_PTS[0][0]:.0f}" y1="{ROUTE_PTS[0][1]:.0f}" x2="{ROUTE_PTS[-1][0]:.0f}" y2="{ROUTE_PTS[-1][1]:.0f}"><stop offset="0" class="mb-g0"/><stop offset=".55" class="mb-g1"/><stop offset="1" class="mb-g0"/></linearGradient>
    <g id="mb-base">
      <rect width="{W}" height="{H}" fill="url(#mb-glow)"/>
      <g mask="url(#mb-land)"><rect width="{W}" height="{H}" fill="url(#mb-dots)"/><path class="mb-relief" d="{RELIEF_D}"/></g>
      <path class="mb-grat" d="{grat}"/>
      <path class="mb-water" d="{WATER_D}"/>
      <path class="mb-water" d="{LAKE_D}"/>
      <path class="mb-isle" d="{ISLES_D}"/>
      <path class="mb-fjord-b" d="{FJORD_D}"/><path class="mb-fjord" d="{FJORD_D}"/>
      <path class="mb-river" d="{RIVERS_D}"/>
      <path class="mb-road" d="{ROADS_D}"/>
    </g>
  </defs>
</svg>"""


def base_svg(extra="", vb=VB_CO):
    return f"""<svg class="mb-svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">
  <use href="#mb-base"/>
  {extra}
</svg>"""


def _labels(route_only=False, vb=VB_CO):
    out = []
    for nom, lat, lon, imp, *pl in STOPS:
        if route_only and imp < 2:
            continue
        x, y = P(lat, lon)
        side = {"b": " is-b", "l": " is-l"}.get(pl[0], "") if pl else ""
        out.append(f'<span class="mb-city{" is-major" if imp == 2 else ""}{side}" style="{_pct(x, y, vb)}"><i></i><b>{nom}</b></span>')
    for nom, lat, lon, rot in WATER_LABELS:
        x, y = P(lat, lon)
        out.append(f'<span class="mb-wl" style="{_pct(x, y, vb)};--r:{rot}deg">{nom}</span>')
    for nom, lat, lon in REGION_LABELS:
        x, y = P(lat, lon)
        out.append(f'<span class="mb-rl" style="{_pct(x, y, vb)}">{nom}</span>')
    for lat in (46, 47, 48):
        out.append(f'<span class="mb-gl mb-gl-y" style="top:{(P(lat, LON0)[1] - vb[1]) / vb[3] * 100:.2f}%">{lat}° N</span>')
    for lon in (-72, -70):
        out.append(f'<span class="mb-gl mb-gl-x" style="left:{(P(LAT1, lon)[0] - vb[0]) / vb[2] * 100:.2f}%">{-lon}° O</span>')
    return "".join(out)


def _photo_box(src, alt, cls="", pos=None):
    if src:
        st = f' style="object-position:{pos}"' if pos else ""
        return f'<img class="{cls}" src="{src}" alt="{alt}" loading="lazy" decoding="async"{st}>'
    return f'<span class="mb-noph {cls}" role="img" aria-label="{alt} · photo à venir">{ico("photo")}<small>Photo à venir</small></span>'


def _modes():
    return "".join(
        f'<button type="button" class="mb-mode{" is-on" if i == 0 else ""}" data-mode="{k}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'{ico(ic)}<span><b>{lab}</b><small>{desc}</small></span></button>'
        for i, (k, lab, desc, ic, _w) in enumerate(MODES))


def _gauge(key, label, val, icn):
    return (f'<li class="mb-gauge" data-g="{key}">{ico(icn)}<span class="mb-g-t"><small>{label}</small>'
            f'<b><span data-gv="{key}">{val}</span>{NB}%</b></span><span class="mb-bar"><i data-gb="{key}" style="width:{val}%"></i></span></li>')


def _copilote():
    pins = "".join(
        f'<button type="button" class="mb-poi c-{p["cat"]}" data-poi="{p["id"]}" style="{_pct(p["x"], p["y"])}" '
        f'aria-label="{CAT_LABEL[p["cat"]]} · {p["nom"]}" tabindex="-1">{ico(p["cat"])}</button>'
        for p in POIS)
    sx, sy = ROUTE_PTS[0]
    extra = (f'<defs><path id="mb-rt" d="{ROUTE_D}" pathLength="{ROUTE_LEN:.1f}"/></defs>'
             '<use class="mb-route-base" href="#mb-rt"/>'
             '<use class="mb-route-glow" href="#mb-rt" data-mb-done/>'
             '<use class="mb-route-done" href="#mb-rt" data-mb-done/>'
             '<g data-mb-detours></g>')
    return f"""
<div class="mb-pane is-on" data-pane="copilote" role="tabpanel" aria-label="Copilote de route">
  <div class="mb-modes" role="group" aria-label="Mode de voyage">{_modes()}</div>
  <div class="mb-co">
    <div class="mb-mapwrap">
      <div class="mb-map" data-mb-map="co" style="aspect-ratio:{VB_CO[2]} / {VB_CO[3]}">
        {base_svg(extra)}
        <div class="mb-ov">{_labels()}{pins}
          <span class="mb-car" data-mb-car style="{_pct(sx, sy)}"><i class="mb-car-pulse"></i><i class="mb-car-dot">{ico("fleche")}</i></span>
        </div>
        <div class="mb-hud mb-hud-t">
          <span class="mb-live"><i></i>En route</span>
          <b>Saint-Hyacinthe → Lac-Saint-Jean</b>
          <span class="mb-prog"><i data-mb-prog></i></span>
          <small><span data-mb-kmdone>0</span>{NB}km parcourus · <span data-mb-kmleft>{round(ROUTE_LEN)}</span>{NB}km restants</small>
        </div>
        <div class="mb-hud mb-hud-b">
          <div><small>Heure</small><b data-mb-clock>9 h 05</b></div>
          <div><small>Vitesse</small><b><span data-mb-speed>92</span>{NB}km/h</b></div>
          <div><small>Prochaine étape</small><b data-mb-next>Québec</b><em data-mb-nexteta>dans 2 h 40</em></div>
          <div class="mb-sun"><small>Soleil</small><svg viewBox="0 0 80 30" aria-hidden="true"><path d="M4 27a36 36 0 0 1 72 0" class="mb-sun-arc"/><circle r="3.4" cx="4" cy="27" class="mb-sun-dot" data-mb-sun/></svg><em>Coucher 16{NB}h{NB}42</em></div>
        </div>
        <div class="mb-ctrl">
          <button type="button" class="mb-btn-r" data-mb-play aria-label="Pause">{ico("pause", "i-pause")}{ico("play", "i-play")}</button>
          <button type="button" class="mb-btn-r" data-mb-restart aria-label="Recommencer le trajet">{ico("restart")}</button>
        </div>
        <p class="mb-toast" data-mb-toast role="status" aria-live="polite"></p>
      </div>
      <ul class="mb-gauges" aria-label="État du VR BouLance">
        {_gauge("eau", "Eau propre", 22, "eau")}{_gauge("propane", "Propane", 31, "propane")}{_gauge("carb", "Carburant", 54, "bolt")}{_gauge("batt", "Batteries", 78, "bolt")}
        <li class="mb-gauge mb-gauge-w">{ico("webasto")}<span class="mb-g-t"><small>Webasto</small><b data-mb-webasto>Dû · 450 h</b></span></li>
      </ul>
    </div>
    <aside class="mb-feed" aria-label="Suggestions du copilote">
      <header class="mb-feed-h">
        <span class="mb-orb" aria-hidden="true"></span>
        <span><b>Copilote JARVIS</b><small data-mb-modeline>Mode Découverte · histoire et incontournables</small></span>
      </header>
      <p class="mb-plan" data-mb-plan aria-live="polite"></p>
      <ol class="mb-cards" data-mb-cards aria-live="polite"></ol>
      <p class="mb-feed-f">Calculé selon la distance, les heures d’ouverture, le soleil et l’état du véhicule. Rien n’est ajouté sans votre accord.</p>
    </aside>
  </div>
</div>"""


def _journal():
    trips_svg = "".join(f'<path class="mb-trip" data-trip="{t["id"]}" d="{t["d"]}"/>' for t in TRIPS_JS) + "".join(
        f'<path class="mb-trip-hit" data-trip-hit="{t["id"]}" d="{t["d"]}"/>' for t in TRIPS_JS)
    extra = f'<g class="mb-trips">{trips_svg}</g>'
    cards = "".join(
        f"""<button type="button" class="mb-tripc{' is-on' if i == 0 else ''}" data-trip="{t['id']}" aria-pressed="{'true' if i == 0 else 'false'}">
          {_photo_box(t['cover'], t['nom'], 'mb-tripc-ph')}
          <span class="mb-tripc-t"><small>{t['quand']}</small><b>{t['nom']}</b>
          <em data-tripn="{t['id']}">{t['km']}{NB}km · {len(t['entries'])}{NB}souvenir{"s" if len(t['entries']) > 1 else ""}</em></span>
        </button>"""
        for i, t in enumerate(TRIPS_JS))
    return f"""
<div class="mb-pane" data-pane="journal" role="tabpanel" aria-label="Journal de voyage" hidden>
  <div class="mb-jo">
    <div class="mb-mapwrap">
      <div class="mb-map" data-mb-map="jo" style="aspect-ratio:{VB_JO[2]} / {VB_JO[3]}">
        {base_svg(extra, VB_JO)}
        <div class="mb-ov">{_labels(True, VB_JO)}<div class="mb-jpins" data-mb-jpins></div></div>
        <div class="mb-hud mb-hud-t mb-jhud">
          <span class="mb-live is-rec"><i></i>Journal automatique</span>
          <b data-mb-jtitle>Charlevoix, fjord et Lac-Saint-Jean</b>
          <small>Chaque photo prise en route se place seule sur la carte.</small>
        </div>
        <div class="mb-ctrl"><button type="button" class="mb-pill" data-mb-replay>{ico("play")}<span>Revoir le voyage</span></button></div>
      </div>
      <div class="mb-trips-l" role="group" aria-label="Mes voyages">
        <p class="mb-k">Mes voyages · touchez un voyage ou son tracé</p>
        <div class="mb-tripcs">{cards}</div>
      </div>
    </div>
    <aside class="mb-jside">
      <figure class="mb-viewer" data-mb-viewer>
        <div class="mb-viewer-ph" data-mb-vph></div>
        <figcaption><b data-mb-vlieu></b><span data-mb-vnote></span><small data-mb-vgeo></small></figcaption>
      </figure>
      <dl class="mb-jstats" data-mb-jstats></dl>
      <ol class="mb-tl" data-mb-tl aria-label="Chronologie du voyage"></ol>
    </aside>
  </div>
</div>"""


def _cap_rows(v):
    rows = []
    for k, lab, ic in CAPS:
        s = v["caps"].get(k)
        tag = {"c": '<em class="s-c">Constructeur</em>', "b": '<em class="s-b">Boîtier JARVIS</em>',
               "t": '<em class="s-b">Traceur JARVIS</em>', None: '<em class="s-n">Non offert</em>'}[s]
        rows.append(f'<li class="{"is-off" if s is None else ""}">{ico(ic)}<span>{lab}</span>{tag}</li>')
    return "".join(rows)


def _lvl_cls(v):
    return "ok" if v >= 50 else ("mid" if v >= 25 else "low")


def _vehicle_panel(v, first):
    stats = "".join(
        f'<li><small>{lab}</small><b>{txt}</b><span class="mb-bar"><i class="l-{_lvl_cls(n)}" style="width:{n}%"></i></span></li>'
        for lab, txt, n in v["stats"])
    info = "".join(f"<li><small>{a}</small><b>{b}</b></li>" for a, b in v["info"])
    tires = ""
    if v.get("tires"):
        t = v["tires"]
        tires = f"""<div class="mb-tires" aria-label="Pression des pneus (psi)"><small>Pression des pneus · psi</small>
          <div class="mb-tires-g"><b>{t[0]}</b><b>{t[1]}</b><span class="mb-tires-car">{ico("sportive")}</span><b>{t[2]}</b><b>{t[3]}</b></div></div>"""
    cmds = "".join(
        f'<button type="button" class="mb-cmd" data-cmd="{k}" data-q="{q}" data-ok="{ok}">{ico(ic)}<span>{lab}</span></button>'
        for k, lab, ic, q, ok in v["cmds"])
    link = ""
    if v["id"] == "vr":
        link = (f'<a class="mb-envlink" href="/solutions/environnements-intelligents/#jarvis">{app_icon("home")}'
                f'<span><b>Ouvrir la cellule dans Environnements</b><small>Lumières, eau, énergie et chauffage du VR</small></span>{ico("fleche")}</a>')
    conn_cls = {"c": "is-c", "b": "is-b", "t": "is-b"}[v["connk"]]
    zoom = " is-zoom" if v.get("zoom") else ""
    real = '<span class="mb-real">Photo réelle</span>' if v.get("real_photo") else ""
    return f"""<article class="mb-veh" data-veh="{v['id']}"{'' if first else ' hidden'}>
      <figure class="mb-veh-ph{zoom}">{_photo_box(v['img'], v['nom'], '', v['pos'])}{real}
        <figcaption><small>{v['type']}</small><b>{v['nom']}</b><span>{ico('pin')}{v['where']}</span></figcaption>
      </figure>
      <div class="mb-veh-body">
        <p class="mb-conn {conn_cls}">{ico('obd' if v['connk'] != 'c' else 'shield')}<span><small>Connexion</small><b>{v['conn']}</b></span></p>
        <ul class="mb-vstats">{stats}</ul>
        {tires}
        <ul class="mb-vinfo">{info}</ul>
        <div class="mb-cmds"><p class="mb-k">Commandes · confirmation demandée</p>{cmds}
          <div class="mb-confirm" data-mb-confirm hidden role="alertdialog" aria-live="polite">
            <p data-mb-cq></p>
            <div><button type="button" class="mb-yes" data-mb-yes>Confirmer</button><button type="button" class="mb-no" data-mb-no>Annuler</button></div>
          </div>
          <p class="mb-cres" data-mb-cres role="status" aria-live="polite"></p>
        </div>
        {link}
      </div>
      <div class="mb-caps"><p class="mb-k">Ce que JARVIS peut faire avec ce véhicule</p><ul>{_cap_rows(v)}</ul>
        <p class="mb-vnote">{v['note']}</p></div>
    </article>"""


def _vehicules():
    tabs = "".join(
        f"""<button type="button" class="mb-vtab{' is-on' if i == 0 else ''}" data-veh="{v['id']}" aria-pressed="{'true' if i == 0 else 'false'}">
          <span class="mb-vtab-i">{ico(v['ico'])}</span><span class="mb-vtab-t"><b>{v['nom']}</b><small>{v['where']}</small></span>
          <span class="mb-vtab-l l-{_lvl_cls(v['lvl'][1])}"><i style="width:{v['lvl'][1]}%"></i></span><em>{v['lvl'][0]} {v['lvl'][1]}{NB}%</em>
        </button>"""
        for i, v in enumerate(VEHICLES))
    panels = "".join(_vehicle_panel(v, i == 0) for i, v in enumerate(VEHICLES))
    return f"""
<div class="mb-pane" data-pane="vehicules" role="tabpanel" aria-label="Véhicules" hidden>
  <div class="mb-garage">
    <div class="mb-vtabs" role="group" aria-label="Mes véhicules">{tabs}
      <div class="mb-addv">{ico("obd")}<span><b>Votre voiture n’a pas d’application?</b>
        <small>Le boîtier JARVIS de base se branche au port OBD-II : position, état, pneus et alertes, dans n’importe quelle voiture depuis 1996.</small></span></div>
    </div>
    <div class="mb-vpanels">{panels}</div>
  </div>
</div>"""


DATA = {
    "W": W, "H": H, "len": round(ROUTE_LEN, 1), "vbco": VB_CO, "vbjo": VB_JO,
    "route": [[round(x, 2), round(y, 2)] for x, y in ROUTE_PTS],
    "km": [round(k, 2) for k in ROUTE_KM],
    "stops": [{"nom": n, "km": round(K[n], 1)} for n in ("Québec", "Baie-Saint-Paul", "La Malbaie", "Tadoussac", "Saguenay", "Alma", "Roberval")],
    "pois": [{k: p[k] for k in ("id", "cat", "nom", "km", "off", "stop", "h", "why", "x", "y", "src", "val")} for p in POIS],
    "modes": {k: {"nom": lab, "desc": desc, "w": w} for k, lab, desc, _ic, w in MODES},
    "cats": CAT_LABEL,
    "icons": {k: ICO[k] for k in list(CAT_LABEL) + ["photo", "check", "x", "pin", "etoile"]},
    "trips": TRIPS_JS,
    "auto": AUTO_JS,
}


def html():
    tabs = [("copilote", "Copilote<i> de route</i>", "route"), ("journal", "Journal<i> de voyage</i>", "journal"), ("vehicules", "Véhicules", "garage")]
    tabbar = "".join(
        f'<button type="button" class="mb-tab{" is-on" if i == 0 else ""}" data-tab="{k}" aria-pressed="{"true" if i == 0 else "false"}">{ico(ic)}<span>{lab}</span></button>'
        for i, (k, lab, ic) in enumerate(tabs))
    return f"""
<div class="demo-shell" data-demo="mobilite" data-rev>
  <div class="demo-top">
    <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
    <b>JARVIS · Mobilité</b>
    <nav class="mb-tabs" aria-label="Sections de Mobilité">{tabbar}</nav>
    <span class="tag tag-sim">Données d’exemple</span>
  </div>
  <div class="demo-body">
    {defs_svg()}
    {_copilote()}
    {_journal()}
    {_vehicules()}
  </div>
  <script type="application/json" id="mb-data">{json.dumps(DATA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")}</script>
</div>"""


HTML = html()
