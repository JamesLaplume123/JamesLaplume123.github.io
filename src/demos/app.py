# Démo « JARVIS App » : l'application rendue en vrai HTML/CSS, nette à toutes les tailles.
# Remplace les captures floues de la vitrine de l'accueil. Cinq écrans (Accueil, Assistant,
# Ma journée, Carte, Partage) dans un même appareil, pilotés par la barre latérale
# (barre d'onglets en bas sur cellulaire). Styles et script : assets/demos/app.css et app.js.
# Données fictives, sauf l'heure locale et la météo réelle de Saint-Hyacinthe.

import math
import re

NB = " "


def fr(s):
    """Typographie française : espaces insécables avant : ; ? ! », après «, dans les heures et unités."""
    s = re.sub(r" ([:;?!»])", NB + r"\1", s)
    s = s.replace("« ", "«" + NB)
    s = re.sub(r"(\d) h (\d)", rf"\1{NB}h{NB}\2", s)
    s = re.sub(r"(\d) h\b", rf"\1{NB}h", s)
    s = re.sub(r"(\d) (°C|%|min\b|km\b|jours?\b)", rf"\1{NB}\2", s)
    return s.replace(" – ", NB + "–" + NB).replace(" · ", NB + "· ")


# ---------------------------------------------------------------------------------------------
# Icônes vectorielles (grille 24, trait 1,5 px, extrémités arrondies)
# ---------------------------------------------------------------------------------------------
ICONS = {
    "home": '<path d="M4.5 10.2 12 4l7.5 6.2V19a1 1 0 0 1-1 1h-4v-5.5h-5V20h-4a1 1 0 0 1-1-1z"/>',
    "spark": '<path d="M11 3.5c.6 4 2.5 5.9 6.5 6.5-4 .6-5.9 2.5-6.5 6.5-.6-4-2.5-5.9-6.5-6.5 4-.6 5.9-2.5 6.5-6.5Z"/>'
             '<path d="M18 14.5c.3 1.7 1 2.4 2.7 2.7-1.7.3-2.4 1-2.7 2.7-.3-1.7-1-2.4-2.7-2.7 1.7-.3 2.4-1 2.7-2.7Z"/>',
    "calendar": '<rect x="3.75" y="5" width="16.5" height="15" rx="2.5"/><path d="M3.75 9.75h16.5M8 3v4M16 3v4"/>',
    "pin": '<path d="M12 20.5s-6.25-5.4-6.25-10.6a6.25 6.25 0 0 1 12.5 0c0 5.2-6.25 10.6-6.25 10.6Z"/><circle cx="12" cy="9.9" r="2.3"/>',
    "pinoff": '<path d="M8.2 5a6.25 6.25 0 0 1 10 4.9c0 1.8-.7 3.6-1.7 5.2M14.6 17.8c-1.4 1.6-2.6 2.7-2.6 2.7s-6.25-5.4-6.25-10.6c0-.7.1-1.4.3-2"/><path d="m4 4 16 16"/>',
    "share": '<circle cx="17.5" cy="5.75" r="2.25"/><circle cx="6.5" cy="12" r="2.25"/><circle cx="17.5" cy="18.25" r="2.25"/>'
             '<path d="m8.5 10.9 7-4M8.5 13.1l7 4"/>',
    "search": '<circle cx="11" cy="11" r="6.25"/><path d="m20 20-4.5-4.5"/>',
    "bell": '<path d="M6.5 16.5v-5a5.5 5.5 0 0 1 11 0v5l1.5 1.75H5z"/><path d="M10 20.75a2.3 2.3 0 0 0 4 0"/>',
    "right": '<path d="m9.5 6 6 6-6 6"/>',
    "left": '<path d="m14.5 6-6 6 6 6"/>',
    "down": '<path d="m6 9.5 6 6 6-6"/>',
    "send": '<path d="M5 12h13.5M13 6.5l5.5 5.5-5.5 5.5"/>',
    "mic": '<rect x="9" y="3.5" width="6" height="11" rx="3"/><path d="M5.75 11.5a6.25 6.25 0 0 0 12.5 0M12 17.75v2.75"/>',
    "clip": '<path d="m19.5 11.5-7.4 7.4a4.5 4.5 0 0 1-6.4-6.4l7.7-7.7a3 3 0 0 1 4.2 4.2l-7.5 7.5a1.5 1.5 0 0 1-2.1-2.1l6.8-6.8"/>',
    "doc": '<path d="M7 3.5h6.5L18 8v12.5H7z"/><path d="M13.5 3.5V8H18M9.75 12.5h5.5M9.75 16h5.5"/>',
    "clock": '<circle cx="12" cy="12" r="8.25"/><path d="M12 7.5V12l3 2"/>',
    "user": '<circle cx="12" cy="8.5" r="3.75"/><path d="M4.75 20c.9-3.6 3.75-5.5 7.25-5.5s6.35 1.9 7.25 5.5"/>',
    "users": '<circle cx="9" cy="8.75" r="3.25"/><path d="M3 19.5c.7-3.1 3-4.75 6-4.75s5.3 1.65 6 4.75"/>'
             '<path d="M15.5 5.75a3.25 3.25 0 0 1 0 6M17.5 14.9c1.9.5 3.1 2 3.5 4.6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.25"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "info": '<circle cx="12" cy="12" r="8.25"/><path d="M12 11v5"/><path d="M12 7.9v.1"/>',
    "star": '<path d="m12 4 2.4 5 5.35.65-3.95 3.7 1.05 5.35L12 16.05 7.15 18.7l1.05-5.35-3.95-3.7L9.6 9z"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="m4 7.5 8 5.5 8-5.5"/>',
    "map": '<path d="M9 4.75 3.75 6.5v12.75L9 17.5l6 1.75 5.25-1.75V4.75L15 6.5z"/><path d="M9 4.75V17.5M15 6.5v12.75"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "locate": '<circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="1.6"/><path d="M12 2.75v3M12 18.25v3M2.75 12h3M18.25 12h3"/>',
    "phone": '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 17.75h2"/>',
    "camera": '<rect x="3.5" y="7" width="12.5" height="10" rx="2.25"/><path d="m16 10.5 4.5-2.5v8L16 13.5"/>',
    "folder": '<path d="M3.5 7.5a2 2 0 0 1 2-2h3.8l2 2.25h7.2a2 2 0 0 1 2 2V17a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>',
    "key": '<circle cx="8" cy="15" r="3.75"/><path d="m10.7 12.3 8.3-8.3M16 7l2.5 2.5M14 9l1.75 1.75"/>',
    "fork": '<path d="M7 3.5V11M5 3.5v4.75a2 2 0 0 0 4 0V3.5M7 11v9.5M16.5 20.5v-17c-2 1.5-3 4-3 7V13h3"/>',
    "brief": '<rect x="3.5" y="7.5" width="17" height="12" rx="2.25"/><path d="M9 7.5V6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 6v1.5M3.5 12.5h17"/>',
    "link": '<path d="M10.5 13.5a3.75 3.75 0 0 0 5.3 0l3-3a3.75 3.75 0 0 0-5.3-5.3l-1 1"/><path d="M13.5 10.5a3.75 3.75 0 0 0-5.3 0l-3 3a3.75 3.75 0 0 0 5.3 5.3l1-1"/>',
    "shield": '<path d="M12 3.5 19 6v5.5c0 4.4-2.9 7.6-7 9-4.1-1.4-7-4.6-7-9V6z"/><path d="m9 12 2.2 2.2L15.2 10"/>',
    "route": '<path d="M7.5 20.5 10 3.5M16.5 20.5 14 3.5M12 6v1.75M12 11v1.75M12 16v1.75"/>',
    "city": '<path d="M3.5 20.5h17M5.5 20.5V9.5l6-3.5v14.5M11.5 10l7 2.75v7.75"/><path d="M8.25 10.5v.1M8.25 13.5v.1M8.25 16.5v.1M15 14.75v.1M15 17.5v.1"/>',
    "pause": '<path d="M9 6.5v11M15 6.5v11"/>',
    "play": '<path d="M8.5 5.75v12.5L18.5 12z"/>',
    "x": '<path d="m6.5 6.5 11 11M17.5 6.5l-11 11"/>',
    "edit": '<path d="M4.5 19.5h4l10-10a2.8 2.8 0 0 0-4-4l-10 10z"/><path d="m13.5 6.5 4 4"/>',
    "sun": '<circle cx="12" cy="12" r="3.75"/><path d="M12 2.75v2M12 19.25v2M2.75 12h2M19.25 12h2M5.45 5.45l1.4 1.4M17.15 17.15l1.4 1.4M5.45 18.55l1.4-1.4M17.15 6.85l1.4-1.4"/>',
    "moon": '<path d="M19 14.6A7.5 7.5 0 0 1 9.4 5a7.5 7.5 0 1 0 9.6 9.6Z"/>',
    "cloud": '<path d="M7.25 18.5h9.5a4 4 0 0 0 .55-7.95 5.5 5.5 0 0 0-10.6 1.35 3.3 3.3 0 0 0 .55 6.6Z"/>',
    "rain": '<path d="M7.25 15h9.5a4 4 0 0 0 .55-7.95 5.5 5.5 0 0 0-10.6 1.35 3.3 3.3 0 0 0 .55 6.6Z"/><path d="m8.5 18-1 2.25M12.5 18l-1 2.25M16.5 18l-1 2.25"/>',
    "snow": '<path d="M7.25 15h9.5a4 4 0 0 0 .55-7.95 5.5 5.5 0 0 0-10.6 1.35 3.3 3.3 0 0 0 .55 6.6Z"/><path d="M8 18.5v.1M12 19.75v.1M16 18.5v.1M10 21.5v.1M14 21.5v.1"/>',
    "fog": '<path d="M4 9.5h16M6 13h12M4 16.5h16M8 20h8"/>',
}


def icon(name, cls=""):
    c = f' class="ap-i {cls}"' if cls else ' class="ap-i"'
    return f'<svg{c} viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


WX = "".join(icon(k, f"wx-{k}") for k in ("sun", "moon", "cloud", "rain", "snow", "fog"))


def mono(initials, tone):
    return f'<span class="ap-mono t-{tone}" aria-hidden="true">{initials}</span>'


# ---------------------------------------------------------------------------------------------
# Les cinq écrans : clé, libellé, libellé court (cellulaire), icône, durée (ms), légende
# ---------------------------------------------------------------------------------------------
SCREENS = [
    ("accueil", "Accueil", "Accueil", "home", 7000, "Votre journée, sur un seul écran.",
     "Messages, agenda, lieux et assistant réunis, à votre image."),
    ("assistant", "Assistant", "Assistant", "spark", 13000, "Il propose. Vous décidez.",
     "Demandez en mots simples. JARVIS prépare l’action, montre ses sources et attend votre accord."),
    ("journee", "Ma journée", "Journée", "calendar", 8000, "Tous vos agendas, enfin ensemble.",
     "Calendriers et tâches de toutes vos sources. Ce qui est en lecture seule le reste."),
    ("carte", "Carte", "Carte", "pin", 8000, "Vos lieux, sans surveillance.",
     "La carte n’affiche que ce que vous êtes autorisé à voir. Aucune position inventée."),
    ("partage", "Partage", "Partage", "share", 8500, "Vous choisissez ce que vous partagez.",
     "Avec qui, pour combien de temps, et sous votre contrôle. Un accès retiré disparaît partout."),
]

# Photos d'ambiance (déjà sur le site, recadrées) : jamais les captures floues du PDF.
BANNER = "/media/concept/jarvis-hero-architecture-v1.webp"
PH_SOUPER = "/media/solutions/camera-rear-terrace-v1.webp"
PH_DOCS = "/media/solutions/ia-privee-connaissances.webp"
PH_RECO = "/media/ambiances/heure-doree.webp"


# ---------------------------------------------------------------------------------------------
# Carte vectorielle de la région (kilomètres, origine à Saint-Hyacinthe)
# ---------------------------------------------------------------------------------------------
LAT0, LON0 = 45.630, -72.957
KX = 111.32 * math.cos(math.radians(LAT0))
KY = 111.13


def P(lat, lon):
    return (lon - LON0) * KX, (LAT0 - lat) * KY


def _smooth(pts, close=False):
    """Courbe lisse (Catmull-Rom → Bézier) passant par les points (lat, lon)."""
    xy = [P(*p) for p in pts]
    if close:
        xy = xy + xy[:2]
        ext = [xy[-3]] + xy
    else:
        ext = [xy[0]] + xy + [xy[-1]]
    d = f"M{ext[1][0]:.1f} {ext[1][1]:.1f}"
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + (" Z" if close else "")


FLEUVE = [(45.30, -74.40), (45.36, -74.10), (45.41, -73.87), (45.43, -73.68), (45.46, -73.57), (45.50, -73.54),
          (45.56, -73.51), (45.63, -73.47), (45.69, -73.43), (45.77, -73.36), (45.85, -73.27), (45.94, -73.19),
          (46.03, -73.12), (46.09, -73.03), (46.17, -72.86), (46.25, -72.70), (46.32, -72.57), (46.38, -72.45),
          (46.46, -72.30), (46.55, -72.10)]
LAC_ST_PIERRE = [(46.08, -73.06), (46.15, -73.02), (46.22, -72.90), (46.29, -72.76), (46.35, -72.62), (46.37, -72.53),
                 (46.32, -72.52), (46.25, -72.58), (46.17, -72.68), (46.11, -72.80), (46.07, -72.93)]
PRAIRIES = [(45.49, -73.92), (45.53, -73.76), (45.58, -73.66), (45.64, -73.56), (45.70, -73.48)]
MILLE_ILES = [(45.54, -74.02), (45.60, -73.85), (45.66, -73.68), (45.71, -73.53), (45.73, -73.47)]
RICHELIEU = [(44.95, -73.34), (45.15, -73.27), (45.31, -73.255), (45.44, -73.29), (45.53, -73.22), (45.60, -73.20),
             (45.70, -73.18), (45.80, -73.15), (45.89, -73.15), (45.98, -73.13), (46.04, -73.11)]
YAMASKA = [(45.10, -72.82), (45.22, -72.92), (45.31, -72.97), (45.41, -72.99), (45.51, -72.97), (45.59, -72.95),
           (45.63, -72.955), (45.68, -72.98), (45.76, -72.96), (45.85, -72.94), (45.94, -72.92), (46.02, -72.91),
           (46.08, -72.93)]
ST_FRANCOIS = [(45.40, -71.89), (45.52, -72.00), (45.66, -72.15), (45.76, -72.30), (45.84, -72.42), (45.88, -72.485),
               (45.95, -72.58), (46.02, -72.70), (46.08, -72.80), (46.12, -72.86)]
ILE_MTL = [(45.41, -73.96), (45.42, -73.85), (45.435, -73.68), (45.46, -73.575), (45.50, -73.548), (45.56, -73.518),
           (45.63, -73.48), (45.70, -73.47), (45.65, -73.55), (45.58, -73.67), (45.53, -73.77), (45.49, -73.89),
           (45.45, -73.95)]
LAVAL = [(45.50, -73.90), (45.55, -73.76), (45.61, -73.65), (45.68, -73.53), (45.71, -73.51), (45.67, -73.64),
         (45.60, -73.82), (45.54, -73.93)]
RIVE_SUD = [(45.46, -73.53), (45.50, -73.505), (45.56, -73.475), (45.60, -73.44), (45.57, -73.36), (45.50, -73.38),
            (45.45, -73.45)]

ROADS = {
    "a20": [(45.53, -73.47), (45.55, -73.36), (45.565, -73.22), (45.60, -73.08), (45.618, -72.975), (45.66, -72.86),
            (45.73, -72.72), (45.80, -72.60), (45.865, -72.50), (45.95, -72.38), (46.06, -72.18)],
    "a10": [(45.48, -73.50), (45.445, -73.38), (45.42, -73.20), (45.40, -73.00), (45.39, -72.85), (45.385, -72.74),
            (45.36, -72.55), (45.33, -72.30), (45.30, -72.00)],
    "a30": [(45.30, -73.95), (45.36, -73.62), (45.42, -73.43), (45.52, -73.37), (45.63, -73.36), (45.74, -73.32),
            (45.86, -73.22), (45.97, -73.13), (46.03, -73.105)],
    "a55": [(46.32, -72.56), (46.12, -72.54), (45.98, -72.50), (45.89, -72.475), (45.75, -72.30), (45.58, -72.10),
            (45.42, -71.94)],
    "r137": [(45.63, -72.955), (45.56, -72.89), (45.47, -72.80), (45.40, -72.735)],
    "r116": [(45.565, -73.21), (45.60, -73.10), (45.625, -72.96), (45.64, -72.75), (45.65, -72.56), (45.70, -72.38)],
}
HILLS = [(45.55, -73.15, 2.6), (45.46, -72.87, 2.2), (45.35, -72.60, 2.1), (45.43, -73.05, 2.2)]
TOWNS = [(45.63, -72.957, 4.2), (45.40, -72.733, 3.8), (45.883, -72.484, 4.6), (46.04, -73.113, 3.4),
         (45.307, -73.262, 3.8), (45.567, -73.205, 2.4), (45.65, -72.565, 1.6)]
# (nom, lat, lon, importance) : 2 = grande ville, 1 = ville, 0 = repère
CITIES = [("Montréal", 45.508, -73.561, 2), ("Saint-Hyacinthe", 45.630, -72.957, 2), ("Granby", 45.400, -72.733, 1),
          ("Drummondville", 45.883, -72.484, 1), ("Sorel-Tracy", 46.040, -73.113, 1),
          ("Beloeil", 45.567, -73.205, 0)]
SHIELDS = [("20", 45.70, -72.77), ("10", 45.405, -73.08), ("55", 45.66, -72.20), ("30", 45.80, -73.27)]
FOCUS = (-64, -54, 116, 88)  # x, y, largeur, hauteur (km) : les cinq villes doivent rester visibles
FOCUS_MINI = (-60, -52, 108, 90)


def _vb(focus, aspect):
    """viewBox qui couvre un cadre de ratio donné en gardant la zone d'intérêt visible."""
    x, y, w, h = focus
    if w / h < aspect:
        nw = h * aspect
        return x - (nw - w) / 2, y, nw, h
    nh = w / aspect
    return x, y - (nh - h) / 2, w, nh


def map_svg(uid, focus, aspect, big=True):
    vx, vy, vw, vh = _vb(focus, aspect)
    roads = "".join(
        f'<path class="r-{k}{" r-major" if k.startswith("a") else ""}" d="{_smooth(p)}"/>' for k, p in ROADS.items()
    )
    hills = "".join(
        f'<circle cx="{P(la, lo)[0]:.1f}" cy="{P(la, lo)[1]:.1f}" r="{r * k:.1f}"/>'
        for la, lo, r in HILLS for k in (1, .55)
    )
    towns = "".join(f'<circle cx="{P(la, lo)[0]:.1f}" cy="{P(la, lo)[1]:.1f}" r="{r}"/>' for la, lo, r in TOWNS)
    return f"""<svg class="ap-map-svg" viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
  <defs>
    <pattern id="{uid}-rang" width="1.7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-36)">
      <path d="M0 0V7M0 0H1.7" class="m-rang"/></pattern>
    <pattern id="{uid}-urb" width="1.1" height="1.1" patternUnits="userSpaceOnUse"><circle cx=".55" cy=".55" r=".2" class="m-urb-dot"/></pattern>
    <radialGradient id="{uid}-hub"><stop offset="0" class="m-hub-a"/><stop offset="1" class="m-hub-b"/></radialGradient>
  </defs>
  <rect class="m-land" x="-160" y="-140" width="320" height="260"/>
  <rect x="-160" y="-140" width="320" height="260" fill="url(#{uid}-rang)" class="m-fields"/>
  <g class="m-hills">{hills}</g>
  <g class="m-urban" fill="url(#{uid}-urb)">
    <path d="{_smooth(ILE_MTL, True)}"/><path d="{_smooth(LAVAL, True)}"/><path d="{_smooth(RIVE_SUD, True)}"/>{towns}
  </g>
  <g class="m-water">
    <path class="w-fleuve" d="{_smooth(FLEUVE)}"/>
    <path class="w-lac" d="{_smooth(LAC_ST_PIERRE, True)}"/>
    <path class="w-riv" d="{_smooth(PRAIRIES)}"/><path class="w-riv" d="{_smooth(MILLE_ILES)}"/>
    <path class="w-riv" d="{_smooth(RICHELIEU)}"/><path class="w-riv w-yam" d="{_smooth(YAMASKA)}"/>
    <path class="w-riv" d="{_smooth(ST_FRANCOIS)}"/>
  </g>
  <g class="m-roads" data-layer="routes">{roads}</g>
  <circle class="m-hubglow" data-layer="hub" cx="0" cy="0" r="{16 if big else 13}" fill="url(#{uid}-hub)"/>
</svg>"""


def _pos(lat, lon, focus, aspect):
    vx, vy, vw, vh = _vb(focus, aspect)
    x, y = P(lat, lon)
    return (x - vx) / vw * 100, (y - vy) / vh * 100, x, y


def map_overlays(focus, aspect, big=True):
    out = []
    for name, la, lo, imp in CITIES:
        if not big and imp == 0:
            continue
        if name == "Saint-Hyacinthe":
            continue  # le Hub porte déjà le nom
        px, py, x, y = _pos(la, lo, focus, aspect)
        out.append(f'<span class="ap-city c{imp}" data-layer="villes" data-x="{x:.1f}" data-y="{y:.1f}" '
                   f'style="left:{px:.2f}%;top:{py:.2f}%"><i></i><b>{name}</b></span>')
    if big:
        for num, la, lo in SHIELDS:
            px, py, x, y = _pos(la, lo, focus, aspect)
            out.append(f'<span class="ap-shield" data-layer="routes" data-x="{x:.1f}" data-y="{y:.1f}" '
                       f'style="left:{px:.2f}%;top:{py:.2f}%" aria-hidden="true">{num}</span>')
    px, py, _x, _y = _pos(LAT0, LON0, focus, aspect)
    lab = ('<span class="ap-hub-lab"><b>Hub</b><small>Saint-Hyacinthe · emplacement de référence</small></span>'
           if big else '<span class="ap-hub-lab"><b>Hub</b><small>Saint-Hyacinthe</small></span>')
    if not big:
        lab = ""
    if big:
        wx, wy = P(45.83, -73.29)
        px, py, _x, _y = _pos(45.83, -73.29, focus, aspect)
        out.append(f'<span class="ap-water" data-x="{wx:.1f}" data-y="{wy:.1f}" style="left:{px:.2f}%;top:{py:.2f}%;--rot:-55deg" '
                   'aria-hidden="true">Fleuve Saint-Laurent</span>')
    out.append(f'<span class="ap-hub" data-layer="hub" data-x="0" data-y="0" style="left:{px:.2f}%;top:{py:.2f}%">'
               f'<span class="ap-hub-pin"><i class="ap-hub-ring" aria-hidden="true"></i>{icon("home")}</span>{lab}</span>')
    return "".join(out)


# ---------------------------------------------------------------------------------------------
# Écrans
# ---------------------------------------------------------------------------------------------
def _head(crumb, title, sub, extra=""):
    c = f'<p class="ap-crumb">{crumb}</p>' if crumb else ""
    return f"""<div class="ap-head" data-r>
  <div>{c}<h3 class="ap-h1">{title}</h3><p class="ap-sub">{sub}</p></div>{extra}
</div>"""


def _card_h(ic, title, more=""):
    return f'<header class="ap-card-h">{icon(ic)}<h4>{title}</h4>{more}</header>'


def v_accueil():
    notifs = f"""<div class="ap-card ap-notifs" data-r>
  <div class="ap-nt"><span class="ap-ring">{icon("bell")}</span><span><b>Notifications</b>
    <small><i class="ap-dot is-red" aria-hidden="true"></i><span data-ap-n="2">2</span> non lues</small></span></div>
  <div class="ap-nt">{mono("CL", "gold")}<span><b>Camille</b><small>Un message</small></span><i class="ap-dot is-red" aria-hidden="true"></i></div>
  <div class="ap-nt"><span class="ap-ring">{icon("calendar")}</span><span><b>Ma journée</b><small>Demain à 8 h 30</small></span></div>
  <div class="ap-nt"><span class="ap-ring is-ok">{icon("shield")}</span><span><b>Maison</b><small>Tout est calme</small></span></div>
</div>"""
    agenda = f"""<ol class="ap-tl" data-seg-panel="agenda">
      <li class="s-perso"><div class="ap-tl-t"><small>Ce soir · 19 h – 22 h</small><b>Souper entre amis</b>
        <span class="ap-meta">{icon("fork")}Chez nous · Personnel</span></div>
        <img src="{PH_SOUPER}" alt="" loading="lazy" decoding="async" style="object-position:62% 60%"></li>
      <li class="s-trav"><div class="ap-tl-t"><small>Demain · 8 h 30 – 10 h</small><b>Préparer les documents</b>
        <span class="ap-meta">{icon("brief")}Travail</span></div>
        <img src="{PH_DOCS}" alt="" loading="lazy" decoding="async" style="object-position:40% 45%"></li>
    </ol>
    <ul class="ap-mini-tasks" data-seg-panel="taches" hidden>
      <li><span class="ap-box"></span><span><b>Relire le dossier</b><small>Demain, 14 h · Personnel</small></span></li>
      <li class="is-done"><span class="ap-box">{icon("check")}</span><span><b>Réserver le souper</b><small>Fait · Personnel</small></span></li>
      <li class="is-ro"><span class="ap-box">{icon("lock")}</span><span><b>Valider la soumission</b><small>Travail · lecture seule</small></span></li>
    </ul>"""
    return f"""{_head("", '<span data-ap="greet">Bonsoir</span> <em>Alex</em>', "Votre journée, simplement.",
                      '<div class="ap-today"><span data-ap="date">Aujourd’hui</span><b><span data-ap="clock">19 h 42</span></b></div>')}
{notifs}
<div class="ap-home-a">
  <article class="ap-card ap-day" data-r>
    {_card_h("calendar", "Ma journée", '<button type="button" class="ap-link" data-go="journee">Voir tout' + icon("right") + '</button>')}
    <div class="ap-seg" role="group" aria-label="Afficher"><button type="button" class="is-on" data-seg="agenda" aria-pressed="true">Agenda</button><button type="button" data-seg="taches" aria-pressed="false">Tâches</button></div>
    {agenda}
  </article>
  <div class="ap-col">
    <article class="ap-card ap-asst" data-r>
      <div class="ap-asst-h"><span class="ap-orb" aria-hidden="true"></span><span><b>Assistant JARVIS</b><small>Comment puis-je vous aider ?</small></span></div>
      <button type="button" class="ap-ask" data-go="assistant">{icon("spark")}<span>Écrire à JARVIS…</span><i>{icon("send")}</i></button>
    </article>
    <article class="ap-card ap-reco" data-r>
      <img src="{PH_RECO}" alt="" loading="lazy" decoding="async">
      <div><p class="ap-kick">{icon("star")}Recommandation</p><b>Ambiance Soirée</b>
        <small data-ap="reco">Au coucher du soleil, si vous l’acceptez.</small></div>
    </article>
  </div>
</div>
<div class="ap-home-b">
  <article class="ap-card ap-minimap" data-r>
    {_card_h("map", "Ma carte", '<button type="button" class="ap-link" data-go="carte">Ouvrir' + icon("right") + '</button>')}
    <div class="ap-map ap-map-mini" data-map data-focus="{",".join(map(str, FOCUS_MINI))}">
      {map_svg("apm", FOCUS_MINI, 2.3, big=False)}
      <div class="ap-ov">{map_overlays(FOCUS_MINI, 2.3, big=False)}</div>
    </div>
  </article>
  <article class="ap-card ap-favs" data-r>
    {_card_h("star", "Mes favoris")}
    <ul class="ap-rows">
      <li><button type="button" data-go="journee">{icon("calendar")}<span><b>Mon agenda</b><small>Vos prochains événements</small></span>{icon("right", "ap-chev")}</button></li>
      <li><button type="button" data-go="partage">{icon("share")}<span><b>Mes partages</b><small>Qui voit quoi, et jusqu’à quand</small></span>{icon("right", "ap-chev")}</button></li>
      <li><button type="button" data-go="carte">{icon("pin")}<span><b>Mes lieux</b><small>Le Hub et vos couches</small></span>{icon("right", "ap-chev")}</button></li>
    </ul>
  </article>
  <article class="ap-card ap-msgs" data-r>
    {_card_h("mail", "Mes messages")}
    <ul class="ap-rows">
      <li><div>{mono("CL", "gold")}<span><b>Camille</b><small>Tu es disponible pour le souper ce soir ?</small></span><time>12 min</time></div></li>
      <li><div>{mono("ÉA", "teal")}<span><b>Équipe Atelier</b><small>Le dossier est prêt. On en discute demain matin.</small></span><time>2 h</time></div></li>
    </ul>
  </article>
</div>"""


def v_assistant():
    def src(ic, a, b):
        return f'<span class="ap-src">{icon(ic)}{a}<em>{b}</em></span>'

    me = mono("A", "stone")
    return f"""{_head('Accueil <span>/</span> <b>Assistant</b>', 'Assistant <em>JARVIS</em>', "Parlez à JARVIS, tout simplement.")}
<div class="ap-card ap-chat" data-r>
  <div class="ap-prompts" aria-hidden="true">
    <span>{icon("calendar")}Organiser ma journée</span><span>{icon("search")}Retrouver une information</span><span>{icon("bell")}Préparer un rappel</span>
  </div>
  <div class="ap-thread" data-ap="thread">
    <div class="ap-msg me" data-step><div class="ap-bub">Peux-tu m’aider à préparer ma journée ?</div><time data-ap="now">18 h 23</time>{me}</div>
    <div class="ap-msg jv" data-step><span class="ap-orb sm" aria-hidden="true"></span>
      <div class="ap-bub-w"><div class="ap-bub"><i class="ap-dots" aria-hidden="true"><i></i><i></i><i></i></i><span data-type>Bien sûr. Ce soir, souper à 19 h ; demain, un dossier à relire. Que voulez-vous préparer ?</span></div>
        <div class="ap-srcs"><small>Sources</small>{src("calendar", "Agenda", "Personnel")}{src("check", "Tâches", "Personnel")}</div></div>
      <time data-ap="now">18 h 23</time></div>
    <div class="ap-msg me" data-step><div class="ap-bub">Rappelle-moi de relire le dossier demain à 14 h.</div><time data-ap="now">18 h 23</time>{me}</div>
    <div class="ap-msg jv" data-step><span class="ap-orb sm" aria-hidden="true"></span>
      <div class="ap-bub-w"><div class="ap-bub"><i class="ap-dots" aria-hidden="true"><i></i><i></i><i></i></i><span data-type>Demain à 14 h, votre agenda est libre. Je prépare le rappel : vérifiez-le avant de le créer.</span></div>
        <div class="ap-srcs"><small>Source</small>{src("calendar", "Agenda", "Personnel")}</div></div>
      <time data-ap="now">18 h 24</time></div>
    <div class="ap-action" data-step data-ap="action">
      <div class="ap-action-h"><span class="ap-ring">{icon("bell")}</span>
        <span><small>Action préparée · rien n’est créé sans vous</small><b>Créer le rappel ?</b></span>
        <span class="ap-state" data-ap="state"><i aria-hidden="true"></i><span>En attente de votre accord</span></span></div>
      <ul class="ap-fields">
        <li>{icon("doc")}Relire le dossier{icon("check", "ap-ok")}</li><li>{icon("clock")}Demain, 14 h 00{icon("check", "ap-ok")}</li>
        <li>{icon("user")}Personnel{icon("check", "ap-ok")}</li><li>{icon("bell")}15 min avant{icon("check", "ap-ok")}</li>
      </ul>
      <div class="ap-action-f">
        <p class="ap-fine">{icon("info")}<span data-ap="fine">Aucune action effectuée.</span></p>
        <button type="button" class="ap-btn" data-ap="verify">Vérifier</button>
        <button type="button" class="ap-btn is-primary" data-ap="approve">Approuver</button>
      </div>
    </div>
  </div>
  <div class="ap-composer" aria-hidden="true">{icon("clip")}<span>Écrire à JARVIS…</span>
    <span class="ap-talk">{icon("mic")}Parler</span><span class="ap-go">{icon("send")}</span></div>
</div>"""


# Agenda : (jour 0 à 2, début h, fin h, titre, source, lieu ou détail, icône)
EVENTS = [
    (0, 10, 11, "Appel notaire", "trav", "Travail", "brief"),
    (0, 19, 22, "Souper entre amis", "perso", "Chez nous", "fork"),
    (1, 8.5, 10, "Préparer les documents", "trav", "Travail", "brief"),
    (1, 13, 14.5, "Hockey de Léo", "fam", "Aréna · lecture seule", "lock"),
    (2, 10.5, 12, "Brunch chez Camille", "perso", "Personnel", "fork"),
    (2, 14, 16.5, "Marche au mont Saint-Hilaire", "perso", "Personnel", "pin"),
]
H0, H1 = 8, 22


def _hh(h):
    m = int(round((h % 1) * 60))
    return f"{int(h)} h {m:02d}" if m else f"{int(h)} h"


def v_journee():
    cals = [("perso", "Personnel", "Votre compte", False), ("trav", "Travail", "L’atelier", False),
            ("fam", "Famille", "Lecture seule", True)]
    cal_html = "".join(
        f'<li><button type="button" class="ap-cal s-{k}" data-cal="{k}" aria-pressed="true"><span class="ap-box">{icon("check")}</span>'
        f'<span><b>{n}</b>{"<small class=ap-ro-l>" + icon("lock", "ap-ro") + d + "</small>" if ro else "<small>" + d + "</small>"}</span></button></li>'
        for k, n, d, ro in cals
    )
    cols = ""
    for day, label in enumerate(("Aujourd’hui", "Demain", "Après-demain")):
        evs = "".join(
            f'<div class="ap-ev s-{s}{" is-ro" if ic == "lock" else ""}{" is-short" if b - a < 2 else ""}" data-src="{s}" '
            f'style="top:{(a - H0) / (H1 - H0) * 100:.3f}%;height:{(b - a) / (H1 - H0) * 100:.3f}%">'
            f'<b>{t}</b><small>{_hh(a)} – {_hh(b)}{" · " + d if ic != "lock" else ""}</small>'
            f'{"<small class=ap-ro-l>" + icon("lock") + "Lecture seule</small>" if ic == "lock" else ""}</div>'
            for dd, a, b, t, s, d, ic in EVENTS if dd == day
        )
        now = '<i class="ap-now" data-ap="nowline" hidden><b data-ap="clock">19 h 42</b></i>' if day == 0 else ""
        cols += f'<div class="ap-wk-col{" is-today" if day == 0 else ""}">{evs}{now}</div>'
    heads = "".join(
        f'<div class="ap-wk-d{" is-today" if i == 0 else ""}"><b data-ap="dname{i}">{lab}</b><small data-ap="dnum{i}"></small></div>'
        for i, lab in enumerate(("Aujourd’hui", "Demain", "Après-demain"))
    )
    hours = "".join(f'<span style="top:{(h - H0) / (H1 - H0) * 100:.3f}%">{h} h</span>' for h in range(H0, H1 + 1, 2))
    tasks = [
        ("Relire le dossier", "Demain, 14 h", "perso", "Personnel", False, False),
        ("Réserver le souper", "Fait", "perso", "Personnel", True, False),
        ("Renouveler l’assurance", "Lundi", "perso", "Personnel", False, False),
        ("Valider la soumission", "Vendredi", "trav", "Travail", False, True),
        ("Patins de Léo", "Demain, 12 h 30", "fam", "Famille", False, True),
    ]
    task_html = "".join(
        f'<li class="s-{s}{" is-done" if done else ""}{" is-ro" if ro else ""}">'
        + (f'<span class="ap-box" title="Lecture seule">{icon("lock")}</span>' if ro else
           f'<button type="button" class="ap-box" aria-pressed="{"true" if done else "false"}" aria-label="Marquer « {t} » comme faite">{icon("check")}</button>')
        + f'<span><b>{t}</b><small><i class="ap-sw" aria-hidden="true"></i>{src} · {when}{" · lecture seule" if ro else ""}</small></span></li>'
        for t, when, s, src, done, ro in tasks
    )
    extra = f'<button type="button" class="ap-btn ap-new" tabindex="-1" aria-hidden="true">{icon("plus")}Événement</button>'
    return f"""{_head('Mon espace <span>/</span> <b>Ma journée</b>', 'Ma <em>journée</em>', "Tous vos agendas, enfin ensemble.", extra)}
<div class="ap-jr">
  <aside class="ap-card ap-cals" data-r>
    <h4 class="ap-k">Mes calendriers</h4>
    <ul>{cal_html}</ul>
    <p class="ap-cals-f">{icon("link")}<span>3 sources reliées<small>À jour il y a 2 min</small></span></p>
  </aside>
  <div class="ap-card ap-week" data-r>
    <div class="ap-wk-top"><span class="ap-wk-nav" aria-hidden="true">{icon("left")}{icon("right")}</span>
      <b data-ap="range">Cette semaine</b><span class="ap-pill">3 jours{icon("down")}</span></div>
    <div class="ap-wk-heads"><span></span>{heads}</div>
    <div class="ap-wk-body"><div class="ap-wk-hours" aria-hidden="true">{hours}</div><div class="ap-wk-grid">{cols}</div></div>
  </div>
  <aside class="ap-card ap-tasks" data-r>
    <header class="ap-card-h">{icon("check")}<h4>Tâches</h4><span class="ap-count"><b data-ap="done">1</b> / 5 faites</span></header>
    <ul>{task_html}</ul>
  </aside>
</div>"""


def v_carte():
    layers = [
        ("hub", "home", "Hub", "1 position affichée", True),
        ("villes", "city", "Villes", "Repères de la région", True),
        ("routes", "route", "Routes", "Autoroutes et routes", True),
        ("appareils", "phone", "Mes appareils", "0 position disponible", False),
        ("personnes", "users", "Personnes partagées", "0 position disponible", False),
    ]
    lay = "".join(
        f'<li><button type="button" class="ap-layer" data-layer-t="{k}" aria-pressed="{"true" if on else "false"}">'
        f'<span class="ap-box">{icon("check")}</span>{icon(ic)}<span><b>{n}</b><small>{d}</small></span></button></li>'
        for k, ic, n, d, on in layers
    )
    return f"""{_head("", "Carte", "Les éléments que vous êtes autorisé à voir.")}
<div class="ap-ct">
  <div class="ap-card ap-map ap-map-big" data-r data-map data-focus="{",".join(map(str, FOCUS))}">
    {map_svg("apb", FOCUS, 1.45)}
    <div class="ap-ov">{map_overlays(FOCUS, 1.45)}</div>
    <div class="ap-zoom"><button type="button" data-zoom="1" aria-label="Rapprocher">{icon("plus")}</button>
      <button type="button" data-zoom="-1" aria-label="Éloigner">{icon("minus")}</button>
      <button type="button" data-zoom="0" aria-label="Recentrer sur le Hub">{icon("locate")}</button></div>
    <p class="ap-nopos">{icon("info")}<span>Aucune position sans permission</span></p>
    <p class="ap-toast" data-ap="toast" role="status"></p>
  </div>
  <div class="ap-ct-side">
    <aside class="ap-card ap-layers" data-r><h4 class="ap-k">Couches d’affichage</h4><ul>{lay}</ul></aside>
    <aside class="ap-card ap-posc" data-r>
      <header class="ap-card-h">{icon("pin")}<h4>Position de cet appareil</h4></header>
      <p class="ap-deny">{icon("pinoff")}Non autorisée</p>
      <p>La carte utilise l’emplacement du Hub, pas votre position. Le partage avec d’autres personnes reste un choix séparé.</p>
      <button type="button" class="ap-btn" data-ap="askpos">{icon("pin")}Autoriser la position</button>
      <p class="ap-fine" data-ap="posnote" hidden>{icon("info")}<span>Démo : rien n’est demandé à votre appareil.</span></p>
    </aside>
  </div>
</div>"""


SHARES = [
    ("CL", "gold", "Camille", "Amie", "doc", "« Notes de réunion »", "Lecture seule", "Encore 6 jours", 80,
     ["Téléphone de Camille", "Documents", "Hub"]),
    ("MA", "teal", "Marc", "Frère", "camera", "Caméra de l’entrée", "Événements seulement", "Jusqu’à dimanche", 45,
     ["Téléphone de Marc", "Caméra", "Hub"]),
    ("SO", "violet", "Sophie", "Gardienne", "key", "Serrure de l’entrée", "Code temporaire", "Ce soir, 18 h – 23 h", 20,
     ["Téléphone de Sophie", "Serrure", "Hub"]),
    ("ÉA", "stone", "Équipe Atelier", "4 personnes", "folder", "Dossier « Soumissions »", "Lecture et commentaires",
     "Encore 30 jours", 92, ["Comptes de l’équipe", "Documents", "Hub"]),
    ("SJ", "gold", "Soutien JARVIS", "Technicien", "shield", "Journal du Hub", "Diagnostic, lecture seule", "Encore 2 h", 30,
     ["Session de soutien", "Journal", "Hub"]),
]


def v_partage():
    rows = ""
    for i, (ini, tone, name, role, ic, what, right, dur, pct, where) in enumerate(SHARES):
        steps = "".join(f"<li>{icon('check')}{w}</li>" for w in where)
        rows += f"""<li class="ap-acc" data-acc="{i}">
  {mono(ini, tone)}
  <span class="ap-acc-who"><b>{name}</b><small>{role}</small></span>
  <span class="ap-acc-what">{icon(ic)}<span><b>{what}</b><small>{right}</small></span></span>
  <span class="ap-acc-dur"><b>{dur}</b><i class="ap-bar" aria-hidden="true"><i style="transform:scaleX({pct / 100:.2f})"></i></i></span>
  <span class="ap-acc-act">
    <button type="button" class="ap-btn ap-revoke" data-ap="revoke" aria-label="Retirer l’accès de {name}">Retirer</button>
    <span class="ap-confirm" hidden><span>Retirer partout ?</span><button type="button" class="ap-btn" data-ap="keep">Annuler</button><button type="button" class="ap-btn is-danger" data-ap="sure">Retirer</button></span>
  </span>
  <ol class="ap-prop" aria-label="Retrait en cours">{steps}</ol>
</li>"""
    log = [("Il y a 40 min", "Session de soutien ouverte, 2 h maximum"), ("Il y a 2 h", "Camille a ouvert « Notes de réunion »"),
           ("Hier", "Accès de Marc prolongé jusqu’à dimanche"), ("Lundi", "Code temporaire créé pour Sophie"),
           ("1er novembre", "Accès de Julie retiré partout")]
    log_html = "".join(f"<li><time>{t}</time><span>{x}</span></li>" for t, x in log)
    return f"""{_head('Mon espace <span>/</span> <b>Mes partages</b>', 'Je choisis <em>ce que je partage</em>',
                  "Avec qui, pour combien de temps, et sous votre contrôle.")}
<div class="ap-pt">
  <div class="ap-card ap-access" data-r>
    <header class="ap-card-h">{icon("users")}<h4>Accès actifs</h4><span class="ap-count"><b data-ap="active" data-ap-n="5">5</b> accès<span class="ap-count-x"> · rien n’est partagé par défaut</span></span></header>
    <ul>{rows}</ul>
    <p class="ap-fine">{icon("info")}<span>Une confirmation est demandée avant chaque retrait.</span></p>
  </div>
  <div class="ap-col">
    <div class="ap-card ap-mypos" data-r>
      <span class="ap-ring lg">{icon("pinoff")}</span>
      <div><p class="ap-kick">Position personnelle</p><b>Non partagée</b>
        <small>Autoriser la position sur cet appareil ne la partage pas automatiquement.</small></div>
    </div>
    <div class="ap-card ap-log" data-r>
      {_card_h("clock", "Journal des partages")}
      <ol data-ap="log"><li class="ap-log-new" hidden><time>À l’instant</time><span></span></li>{log_html}</ol>
    </div>
  </div>
</div>"""


VIEWS = {"accueil": v_accueil, "assistant": v_assistant, "journee": v_journee, "carte": v_carte, "partage": v_partage}


def _stagger(html):
    """Chaque carte reçoit son rang d'apparition (--r) pour la révélation en cascade."""
    k = iter(range(100))
    return re.sub(r"data-r(?=[\s>])", lambda m: f'data-r style="--r:{next(k)}"', html)


ON = ' class="is-on"'


def html():
    tabs = "".join(
        f'<button type="button" role="tab" id="ap-t-{k}" aria-controls="ap-p-{k}" aria-selected="{"true" if i == 0 else "false"}" '
        f'tabindex="{0 if i == 0 else -1}" data-i="{i}" aria-label="{lab}"{ON if i == 0 else ""}>{icon(ic)}'
        f'<span class="l-long">{lab}</span><span class="l-short" aria-hidden="true">{short}</span></button>'
        for i, (k, lab, short, ic, _d, _t, _p) in enumerate(SCREENS)
    )
    views = "".join(
        f'<section class="ap-view ap-v-{k}{" is-on" if i == 0 else ""}" role="tabpanel" id="ap-p-{k}" aria-labelledby="ap-t-{k}" '
        f'data-view="{k}" data-dur="{d}"{"" if i == 0 else " inert"}>{_stagger(fr(VIEWS[k]()))}</section>'
        for i, (k, _l, _s, _ic, d, _t, _p) in enumerate(SCREENS)
    )
    caps = "".join(
        f'<div class="ap-cap{" is-on" if i == 0 else ""}"><h3>{fr(t)}</h3><p>{fr(p)}</p></div>'
        for i, (_k, _l, _s, _ic, _d, t, p) in enumerate(SCREENS)
    )
    return f"""<div class="ap" data-demo="app">
  <div class="ap-stage">
    <div class="ap-glow" aria-hidden="true"></div>
    <div class="ap-tilt">
      <div class="ap-device">
        <p class="ap-badge"><span>Démo · données fictives</span></p>
        <div class="ap-screen" role="group" aria-roledescription="démonstration" aria-label="JARVIS App, démonstration avec données fictives">
          <div class="ap-bg" aria-hidden="true"></div>
          <img class="ap-banner" src="{BANNER}" alt="" aria-hidden="true" loading="lazy" decoding="async" width="1916" height="821">
          <nav class="ap-side" aria-label="JARVIS App">
            <div class="ap-brand" aria-hidden="true"><b>JARVIS</b><small>Private Systems</small><em class="ap-modename"></em></div>
            <div class="ap-nav" role="tablist" aria-label="Écrans de JARVIS App" aria-orientation="vertical">
              <i class="ap-ind" aria-hidden="true"><i class="ap-prog"></i></i>{tabs}
            </div>
            <div class="ap-side-f"><p class="ap-hubst"><i class="ap-dot is-ok" aria-hidden="true"></i><span><b>Hub en ligne</b><small>Saint-Hyacinthe</small></span></p>
              <p class="ap-motto">Votre espace.<br>À votre image.</p></div>
          </nav>
          <div class="ap-main">
            <header class="ap-top">
              <button type="button" class="ap-search" data-go="assistant">{icon("search")}<span>Que souhaitez-vous faire{NB}?</span></button>
              <span class="ap-status-time" data-ap="clock">19{NB}h{NB}42</span>
              <span class="ap-wx" title="Saint-Hyacinthe · Environnement Canada">
                <span class="ap-wx-i" aria-hidden="true">{WX}</span>
                <span><b><span data-ap="temp">—</span><span class="ap-unit">{NB}°C</span></b><small>Saint-Hyacinthe<span class="ap-live"> · en direct</span></small></span>
              </span>
              <span class="ap-me">{mono("A", "stone")}<b>Alex</b>{icon("down")}</span>
            </header>
            <div class="ap-views">{views}</div>
          </div>
        </div>
        <i class="ap-sweep" aria-hidden="true"></i>
      </div>
    </div>
  </div>
  <div class="ap-caps">
    <div class="ap-cap-txt" aria-live="polite">{caps}</div>
    <div class="ap-ctrl">
      <span class="ap-step"><b data-ap="step">01</b> / 0{len(SCREENS)}</span>
      <button type="button" class="ap-play" data-ap="play" aria-label="Mettre la visite en pause">{icon("pause", "i-pause")}{icon("play", "i-play")}<span>Pause</span></button>
      <span class="ap-hint">Touchez un écran : tout y est cliquable</span>
    </div>
  </div>
</div>"""
