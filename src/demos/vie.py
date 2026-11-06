# Démo « Personal Intelligence : une vie entière, un seul système »
# (assets/demos/vie.css et vie.js).
#
# Une journée d'Alex défile d'un réveil à l'autre (lundi 6 h 30 → mardi 6 h 30).
# Quatre sources, chacune avec sa propre permission révocable : montre, téléphone,
# agenda, maison. Leurs données arrivent au fil de la journée sur le Hub privé;
# JARVIS relie les points (chaque lien montre son « pourquoi » et ses sources),
# puis, au réveil, propose d'échanger une habitude contre une meilleure. Rien ne
# change sans accord; l'essai de 14 jours s'anime ensuite dans la progression.
# Bien-être seulement, aucun diagnostic. Données entièrement fictives.
#
# Une seule source de vérité : les listes ci-dessous. Python produit l'état final
# statique (lisible sans JavaScript : journée complète, liens, proposition et
# progression) et toute la géométrie; le script reçoit le reste par un bloc JSON.

import json
import math
import re
from html import escape

NBSP = " "


def fr(s):
    """Espaces insécables de la typographie française (heures, unités, ponctuation, guillemets)."""
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) h (\d)", rf"\1{NBSP}h{NBSP}\2", s)
    s = re.sub(r"(\d) (h|min|ms|%|°C|pas|soirs?|jours?|nuits?|semaines?|après-midi|rencontres?|minutes)\b",
               rf"\1{NBSP}\2", s)
    s = re.sub(r" ([:;?!»])", rf"{NBSP}\1", s)
    return s.replace("« ", "«" + NBSP)


# ---------------------------------------------------------------------------
# Icônes (traits, 24 × 24)
# ---------------------------------------------------------------------------
ICONS = {
    "watch": '<rect x="6.4" y="6.4" width="11.2" height="11.2" rx="3.2"/><path d="M9 6.4 9.6 3h4.8l.6 3.4M9 17.6l.6 3.4h4.8l.6-3.4"/><path d="M12 9.6V12l1.6 1"/>',
    "phone": '<rect x="7" y="2.8" width="10" height="18.4" rx="2.6"/><path d="M11 18h2"/>',
    "calendar": '<rect x="3.6" y="5" width="16.8" height="15" rx="2.2"/><path d="M3.6 10h16.8M8 3v4M16 3v4"/>',
    "home": '<path d="M3.5 10.6 12 4l8.5 6.6"/><path d="M5.6 9.2v10.3h12.8V9.2"/><path d="M10 19.5v-5h4v5"/>',
    "moon": '<path d="M19.6 14.6A7.9 7.9 0 1 1 9.4 4.4a6.4 6.4 0 0 0 10.2 10.2z"/>',
    "coffee": '<path d="M4.6 9.2h11.8v4.6a5 5 0 0 1-5 5h-1.8a5 5 0 0 1-5-5z"/><path d="M16.4 10.6h1.4a2.5 2.5 0 0 1 0 5h-1.6"/>',
    "check": '<path d="m5 12.5 4.4 4.3L19 7.2"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
    "erase": '<path d="M4.5 7h15M9.5 7V4.8h5V7"/><path d="M6.6 7 7.5 20h9l.9-13"/>',
    "spark": '<path d="M12 3.5 13.9 9l5.6 1.9-5.6 1.9L12 18.4l-1.9-5.6-5.6-1.9L10.1 9z"/>',
    "pause": '<path d="M9 5.5v13M15 5.5v13"/>',
    "play": '<path d="M8 5.2v13.6L18.6 12z"/>',
    "replay": '<path d="M3 12a9 9 0 1 0 2.8-6.5"/><path d="M3 3.5v4.4h4.4"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# L'axe du temps : lundi 6 h 30 → mardi 6 h 30 (1 440 minutes).
# Les heures du lendemain s'écrivent 24:xx à 30:30.
# ---------------------------------------------------------------------------
DAY = 1440
START = 6 * 60 + 30


def T(hm):
    h, m = map(int, hm.split(":"))
    return h * 60 + m - START


def pc(mins):
    return round(mins / DAY * 100, 3)


def clock(mins):
    m = (mins + START) % DAY
    return f"{m // 60} h {m % 60:02d}"


# ---------------------------------------------------------------------------
# Les sources et leurs données de la journée (fictives)
# ---------------------------------------------------------------------------
SOURCES = [
    ("montre", "Montre", "Sommeil · pas · VFC", "watch"),
    ("tel", "Téléphone", "Temps d’écran", "phone"),
    ("agenda", "Agenda", "Rencontres", "calendar"),
    ("maison", "Maison", "Lumière · température", "home"),
]
SRC_NAME = {k: n for k, n, _s, _i in SOURCES}

# Montre : pas par tranche de 30 minutes (de 6 h 30 à minuit), puis sommeil.
STEPS = [140, 300, 400, 240, 160, 30, 20, 40, 20, 50, 30, 40, 300, 330, 80, 30, 20, 60,
         30, 40, 170, 220, 340, 260, 130, 120, 150, 90, 50, 40, 70, 50, 60, 70, 30]
IN_BED, ASLEEP = T("23:35"), T("24:48")
# Hypnogramme : (stade, minutes) dès l'endormissement. W éveil · R paradoxal · L léger · P profond
SLEEP = [("L", 20), ("P", 45), ("L", 30), ("R", 18), ("L", 25), ("P", 35), ("L", 30), ("R", 22),
         ("W", 4), ("L", 40), ("R", 25), ("L", 28), ("L", 20)]
STAGE_Y = {"W": 18, "R": 38, "L": 57, "P": 76}
HRV = [38, 40, 44, 42, 39, 43, 41, 45, 40, 42, 41]  # VFC la nuit, aux 30 minutes dès 1 h

# Téléphone : séances d'écran (début, fin, au lit ?)
SCREEN = [("6:40", "7:02", 0), ("8:12", "8:20", 0), ("10:24", "10:29", 0), ("12:44", "13:08", 0),
          ("15:06", "15:12", 0), ("17:32", "17:47", 0), ("20:35", "21:15", 0), ("21:48", "22:06", 0),
          ("23:39", "24:31", 1)]

# Agenda : (début, fin, titre, personnel ?)
MEETINGS = [("9:00", "10:00", "Équipe", 0), ("10:00", "11:00", "Client", 0), ("11:00", "12:40", "Revue de projet", 0),
            ("14:00", "15:30", "Atelier", 0), ("15:30", "16:30", "Appel fournisseur", 0),
            ("18:15", "19:00", "Souper en famille", 1)]

# Maison : lumière (début, fin, niveau 0–1, pièce, au lit ?) et température (heure, °C)
LIGHT = [("6:30", "8:00", .75, "Cuisine", 0), ("8:00", "9:00", .3, "Salon", 0), ("9:00", "16:30", .5, "Bureau", 0),
         ("16:30", "17:00", .65, "Cuisine", 0), ("17:00", "21:00", .9, "Salon", 0),
         ("21:00", "23:35", .55, "Salon tamisé", 0), ("23:35", "24:31", .42, "Chambre", 1), ("24:31", "30:30", 0, "Éteinte", 0)]
TEMP = [("6:30", 20.5), ("7:00", 21.0), ("9:00", 21.0), ("12:00", 21.2), ("15:00", 21.4), ("16:30", 21.0),
        ("18:00", 21.5), ("20:00", 21.0), ("22:00", 20.5), ("23:00", 19.5), ("24:00", 19.0), ("27:00", 18.6),
        ("29:30", 18.8), ("30:00", 20.0), ("30:30", 20.5)]
COFFEE = [("7:05", 0), ("16:40", 1)]
SUN = (T("6:40"), T("16:32"))

# ---------------------------------------------------------------------------
# Ce que JARVIS relie : (heure d'arrivée, titre, pourquoi, sources, surlignages)
# surlignage : (voie, début, fin, étiquette)
# ---------------------------------------------------------------------------
INSIGHTS = [
    ("12:40", "3 h 40 de rencontres sans pause",
     "Agenda plein de 9 h à 12 h 40 · {sit} pas pendant ce temps.",
     ["agenda", "montre"], [("agenda", "9:00", "12:40", "3 h 40"), ("montre", "9:00", "12:30", "")]),
    ("16:44", "Café à 16 h 40",
     "Les jours de café après 15 h, sa récupération de nuit baisse de 18 % (21 jours observés).",
     ["maison", "montre"], [("maison", "16:30", "16:52", "")]),
    ("24:31", "52 minutes d’écran au lit",
     "Téléphone actif de 23 h 39 à 0 h 31, lumière de la chambre allumée tout ce temps.",
     ["tel", "maison"], [("tel", "23:39", "24:31", "Au lit"), ("maison", "23:35", "24:31", "")]),
    ("25:20", "Endormie 17 minutes après l’écran",
     "Écran éteint à 0 h 31, sommeil à 0 h 48 : le même écart que 11 soirs sur 14.",
     ["montre", "tel"], [("montre", "24:31", "24:48", "")]),
    ("30:30", "Nuit de 5 h 42",
     "1 h 18 sous son objectif de 7 h · récupération (VFC) de 41 ms, sous sa moyenne de 52.",
     ["montre"], [("montre", "24:48", "30:30", "5 h 42")]),
]

# ---------------------------------------------------------------------------
# Les échanges d'habitude proposés au réveil, et leur essai de 14 jours
# ---------------------------------------------------------------------------
HABITS = [
    {
        "tab": "Téléphone au lit", "best": True,
        "old": "Téléphone au lit", "new": "20 minutes de lecture",
        "uses": ["tel", "maison", "montre"], "links": [2, 3, 4],
        "sugg": "Et si le téléphone dormait dans la cuisine ? À 22 h 30, la chambre passe en lumière de lecture "
                "et le téléphone en mode nuit. Vingt minutes de lecture remplacent le défilement.",
        "why": "Les 4 soirs sur 14 où l’écran s’est éteint avant 22 h 45, Alex s’est endormie 31 minutes plus tôt.",
        "plan": ["22 h 30 · la chambre passe en lumière de lecture",
                 "22 h 30 · téléphone en mode nuit, appels urgents permis",
                 "Essai de 14 jours, puis un bilan : Alex décide de la suite"],
        "metric": "Sommeil par nuit", "goal": "objectif : 7 h", "fmt": "dur", "base": 342, "lo": 300, "hi": 480,
        "pts": [356, 371, 349, 392, 405, 388, 414, 409, 426, 401, 431, 437, 433, 446],
        "streak": "11011110111111",
        "delta": "+{gainL} par nuit",
        "kpis": [("Sommeil", "+{gain}", "min", "par nuit · 7 dernières nuits"),
                 ("Écran au lit", "9", "min", "avant : 52 min"),
                 ("Lecture", "{streak}", "soirs sur 14", "objectif : 10")],
    },
    {
        "tab": "Café tardif", "best": False,
        "old": "Café à 16 h 40", "new": "Tisane après 15 h",
        "uses": ["maison", "montre"], "links": [1, 4],
        "sugg": "Après 15 h, la machine à café propose d’abord une tisane : même pause, même rituel, sans caféine. "
                "Le café reste possible — il suffit de le demander.",
        "why": "Les jours où le dernier café est pris avant 14 h, sa récupération de nuit est 18 % meilleure (21 jours observés).",
        "plan": ["Dès 15 h · la machine propose la tisane en premier",
                 "Le café reste à un geste, sans commentaire",
                 "Essai de 14 jours, puis un bilan : Alex décide de la suite"],
        "metric": "Récupération de nuit (VFC)", "goal": "plus haut = mieux récupérée", "fmt": "ms", "base": 41, "lo": 30, "hi": 60,
        "pts": [42, 44, 41, 46, 47, 45, 49, 48, 51, 47, 52, 53, 51, 54],
        "streak": "11011011101111",
        "delta": "+{gain} ms la nuit",
        "kpis": [("Récupération", "+{gain}", "ms", "VFC · 7 dernières nuits"),
                 ("Dernier café", "14 h 50", "", "avant : 16 h 40"),
                 ("Tisane", "{streak}", "après-midi sur 14", "proposée dès 15 h")],
    },
    {
        "tab": "Assise tout le jour", "best": False,
        "old": "Assise 9 h par jour", "new": "Pause marche aux 90 minutes",
        "uses": ["montre", "agenda"], "links": [0],
        "sugg": "Après 90 minutes sans pause, et seulement si l’agenda est libre, la montre propose 8 minutes "
                "de marche. Jamais pendant une rencontre, jamais après 18 h.",
        "why": "Les journées avec au moins trois pauses comptent 3 000 pas de plus, sans réduire le temps de travail concentré.",
        "plan": ["Après 90 minutes sans pause · rappel discret sur la montre",
                 "Seulement si l’agenda est libre, jamais après 18 h",
                 "Essai de 14 jours, puis un bilan : Alex décide de la suite"],
        "metric": "Pas par jour", "goal": "objectif : 7 000", "fmt": "int", "base": 4210, "lo": 2000, "hi": 9000,
        "pts": [4310, 5120, 3980, 5800, 6240, 5010, 6650, 7020, 4400, 6890, 7310, 7120, 7480, 7650],
        "streak": "01011011011111",
        "delta": "+{gain} pas par jour",
        "kpis": [("Pas par jour", "+{gain}", "", "moyenne · 7 derniers jours"),
                 ("Temps assis", "−1 h 10", "", "avant : 9 h 20"),
                 ("Pauses", "{streak}", "jours sur 14", "objectif : 10")],
    },
]


def _fmt(v, kind):
    if kind == "dur":
        return f"{int(v) // 60} h {int(v) % 60:02d}"
    if kind == "ms":
        return f"{int(round(v))} ms"
    return f"{int(round(v)):,}".replace(",", " ")


# ---------------------------------------------------------------------------
# Géométrie des voies (pourcentages de la voie : gauche, largeur, haut, hauteur)
# ---------------------------------------------------------------------------
def _steps_bins():
    peak = max(STEPS)
    return [(pc(i * 30), pc(30), round(v / peak * 72, 2)) for i, v in enumerate(STEPS)]


def _sleep_segs():
    out, t = [], ASLEEP
    for st, mins in SLEEP:
        out.append((st, pc(t), pc(mins)))
        t += mins
    return out


def _hrv_path():
    lo, hi = 34, 48
    pts = [(T("25:00") + i * 30, 15 - (v - lo) / (hi - lo) * 11) for i, v in enumerate(HRV)]
    return "M" + " L".join(f"{x:.1f} {y:.2f}" for x, y in pts)


def _temp_y(c):
    return 8 + (21.8 - c) / (21.8 - 18.4) * 36  # 18,4 °C en bas de bande, 21,8 °C en haut


def _temp_path():
    pts = [(T(h), _temp_y(c)) for h, c in TEMP]
    d = f"M{pts[0][0]} {pts[0][1]:.2f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx = (x0 + x1) / 2
        d += f" C{mx:.1f} {y0:.2f} {mx:.1f} {y1:.2f} {x1} {y1:.2f}"
    return d


def _light_path():
    d = f"M0 100"
    for a, b, lv, _room, _f in LIGHT:
        y = 100 - lv * 46
        d += f" L{T(a) + 4} {y:.1f} L{T(b) - 4} {y:.1f}"
    return d + f" L{DAY} 100 Z"


def _light_edge():
    d = ""
    for i, (a, b, lv, _room, _f) in enumerate(LIGHT):
        y = 100 - lv * 46
        d += f"{'M' if i == 0 else ' L'}{T(a) + 4} {y:.1f} L{T(b) - 4} {y:.1f}"
    return d


def _sun_path():
    rise, sset = SUN
    pts = []
    for i in range(41):
        x = rise + (sset - rise) * i / 40
        pts.append((x, 70 - math.sin(math.pi * i / 40) * 60))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _sit_steps():
    a, b = T("9:00"), T("12:30")
    return sum(v for i, v in enumerate(STEPS) if a <= i * 30 < b)


# ---------------------------------------------------------------------------
# Les données transmises au script
# ---------------------------------------------------------------------------
def _ins_data():
    out = []
    for i, (t, title, why, srcs, hls) in enumerate(INSIGHTS):
        out.append({"t": T(t), "src": srcs})
    return out


def _habit_data(h):
    last7 = sum(h["pts"][-7:]) / 7
    gain = round(last7 - h["base"], -1 if h["fmt"] == "int" else 0)
    g = f"{int(gain):,}".replace(",", " ")
    gl = f"{int(gain) // 60} h {int(gain) % 60:02d}" if h["fmt"] == "dur" and gain >= 60 else f"{g} min"
    streak = h["streak"].count("1")
    span = h["hi"] - h["lo"]
    vals = [round((v - h["lo"]) / span, 4) for v in h["pts"]]
    return {
        "old": fr(h["old"]), "new": fr(h["new"]), "uses": h["uses"], "links": h["links"],
        "sugg": fr(h["sugg"]), "why": fr(h["why"]), "plan": [fr(p) for p in h["plan"]],
        "metric": fr(h["metric"]), "goal": fr(h["goal"]),
        "vals": vals, "streak": h["streak"],
        "avg": round((last7 - h["lo"]) / span * 100, 2), "avgL": fr("Semaine 2 : " + _fmt(last7, h["fmt"])),
        "base": round((h["base"] - h["lo"]) / span * 100, 2), "baseL": fr("Avant : " + _fmt(h["base"], h["fmt"])),
        "end": fr(_fmt(h["pts"][-1], h["fmt"])), "top": fr(_fmt(h["hi"], h["fmt"])), "bottom": fr(_fmt(h["lo"], h["fmt"])),
        "delta": fr(h["delta"].replace("{gainL}", gl).replace("{gain}", g)),
        "kpis": [{"l": l, "v": fr(v.replace("{gain}", g).replace("{streak}", str(streak))), "u": fr(u), "c": fr(c)}
                 for l, v, u, c in h["kpis"]],
    }


def _data():
    return {
        "day": DAY,
        "steps": STEPS, "inBed": IN_BED, "asleep": ASLEEP,
        "screen": [[T(a), T(b)] for a, b, _f in SCREEN],
        "meet": [[T(a), T(b), fr(t)] for a, b, t, _p in MEETINGS],
        "light": [[T(a), T(b), fr(room)] for a, b, _l, room, _f in LIGHT],
        "temp": [[T(h), c] for h, c in TEMP],
        "sun": list(SUN),
        "ins": _ins_data(),
        "habits": [_habit_data(h) for h in HABITS],
        "names": SRC_NAME,
    }


# ---------------------------------------------------------------------------
# Balisage
# ---------------------------------------------------------------------------
def _pos(a, w):
    return f"--a:{a};--w:{w}"


def _hl_html(lane):
    out = []
    for i, (_t, _ti, _w, _s, hls) in enumerate(INSIGHTS):
        for ln, a, b, label in hls:
            if ln != lane:
                continue
            lab = f'<em>{escape(fr(label))}</em>' if label else ""
            out.append(f'<i class="pi-hl" data-ins="{i}" style="{_pos(pc(T(a)), pc(T(b) - T(a)))}">'
                       f'<b>{i + 1}</b>{lab}</i>')
    return "".join(out)


def _grid_html():
    return '<span class="pi-grid" aria-hidden="true">' + "".join(
        f'<i style="--a:{pc(T(f"{h}:00"))}"></i>' for h in (9, 12, 15, 18, 21, 24, 27, 30)) + "</span>"


def _hypno_path():
    """Ligne en escalier de l'hypnogramme, du milieu d'un stade au suivant."""
    d = ""
    t = ASLEEP
    for i, (st, mins) in enumerate(SLEEP):
        y = STAGE_Y[st] + 5.5
        d += (f"M{t} {y}" if i == 0 else f" V{y}") + f" H{t + mins}"
        t += mins
    return d


def _lane_montre():
    bars = "".join(f'<i style="{_pos(a, w)};--h:{h}"></i>' for a, w, h in _steps_bins() if h > 0)
    bed = f'<span class="pi-bed" style="{_pos(pc(IN_BED), pc(ASLEEP - IN_BED))}"></span>'
    sleep = "".join(f'<i data-st="{st}" style="{_pos(a, w)};--y:{STAGE_Y[st]}"></i>' for st, a, w in _sleep_segs())
    night = (f'<svg class="pi-hrv" viewBox="0 0 {DAY} 100" preserveAspectRatio="none" aria-hidden="true">'
             f'<path class="pi-hyp" d="{_hypno_path()}" vector-effect="non-scaling-stroke"/>'
             f'<path class="pi-vfc" d="{_hrv_path()}" vector-effect="non-scaling-stroke"/></svg>')
    return f'<span class="pi-steps">{bars}</span>{bed}{night}<span class="pi-sleep">{sleep}</span>'


def _lane_tel():
    return "".join(
        f'<i class="pi-sess{" is-bad" if bad else ""}" style="{_pos(pc(T(a)), pc(T(b) - T(a)))}"></i>'
        for a, b, bad in SCREEN
    )


def _lane_agenda():
    return "".join(
        f'<i class="pi-meet{" is-perso" if perso else ""}" style="{_pos(pc(T(a)), pc(T(b) - T(a)))}" title="{escape(fr(t))}"></i>'
        for a, b, t, perso in MEETINGS
    )


def _lane_maison():
    light = (f'<svg class="pi-light" viewBox="0 0 {DAY} 100" preserveAspectRatio="none" aria-hidden="true">'
             f'<defs><linearGradient id="pi-light-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".5"/>'
             f'<stop offset="1" stop-color="currentColor" stop-opacity=".06"/></linearGradient></defs>'
             f'<path class="pi-light-a" d="{_light_path()}" fill="url(#pi-light-g)"/>'
             f'<path class="pi-light-e" d="{_light_edge()}" vector-effect="non-scaling-stroke"/>'
             f'<path class="pi-temp" d="{_temp_path()}" vector-effect="non-scaling-stroke"/></svg>')
    bad = "".join(
        f'<span class="pi-bedlight" style="{_pos(pc(T(a)), pc(T(b) - T(a)))}"></span>'
        for a, b, _l, _r, f in LIGHT if f)
    cups = "".join(
        f'<span class="pi-cup{" is-bad" if b else ""}" style="--a:{pc(T(t))}">{icon("coffee")}</span>' for t, b in COFFEE)
    temps = (f'<span class="pi-tag pi-tag-t" style="--a:{pc(T("12:00"))};--t:{_temp_y(21.2) + 7:.1f}">21,2{NBSP}°C</span>'
             f'<span class="pi-tag pi-tag-t" style="--a:{pc(T("26:30"))};--t:{_temp_y(18.7) + 7:.1f}">18,7{NBSP}°C</span>')
    return light + bad + cups + temps


LANES = {"montre": _lane_montre, "tel": _lane_tel, "agenda": _lane_agenda, "maison": _lane_maison}
FIRST_VAL = {"montre": "Sommeil · 5 h 42", "tel": "3 h 10", "agenda": "Libre", "maison": "20,5 °C · Éteinte"}


def _rows_html():
    out = []
    for k, name, sub, ic in SOURCES:
        out.append(
            f'<div class="pi-row" data-src="{k}">'
            f'<div class="pi-src"><span class="pi-src-ic">{icon(ic)}</span>'
            f'<span class="pi-src-t"><b>{name}</b><small>{escape(fr(sub))}</small></span>'
            f'<span class="pi-src-v" data-pi-v>{escape(fr(FIRST_VAL[k]))}</span>'
            f'<button type="button" class="pi-sw" role="switch" aria-checked="true" '
            f'aria-label="Permission · {name}"><i></i></button></div>'
            f'<span class="pi-conn" aria-hidden="true"><i></i><i></i><b></b></span>'
            f'<div class="pi-lane pi-lane-{k}">{_grid_html()}{LANES[k]()}{_hl_html(k)}'
            f'<span class="pi-cover" aria-hidden="true"></span>'
            f'<span class="pi-off">{icon("lock")}Permission retirée · rien n’est reçu</span></div></div>'
        )
    return "".join(out)


def _sky_html():
    rise, sset = SUN
    return (
        f'<svg viewBox="0 0 {DAY} 100" preserveAspectRatio="none" aria-hidden="true">'
        f'<defs><linearGradient id="pi-sky-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".34"/>'
        f'<stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>'
        f'<path class="pi-sky-a" d="{_sun_path()} L{sset} 70 L{rise} 70 Z" fill="url(#pi-sky-g)"/>'
        f'<path class="pi-sky-l" d="{_sun_path()}" vector-effect="non-scaling-stroke"/>'
        f'<path class="pi-horizon" d="M0 70 H{DAY}" vector-effect="non-scaling-stroke"/></svg>'
        f'<span class="pi-sky-t" style="--a:{pc(rise)}"><i>Lever </i>6{NBSP}h{NBSP}40</span>'
        f'<span class="pi-sky-t" style="--a:{pc(sset)}"><i>Coucher </i>16{NBSP}h{NBSP}32</span>'
        f'<span class="pi-sun" aria-hidden="true"><i></i></span>'
    )


def _axis_html():
    ticks = "".join(
        f'<span style="--a:{pc(T(f"{h}:00"))}">{h % 24}{NBSP}h</span>' for h in (9, 12, 15, 18, 21, 24, 27, 30))
    marks = "".join(
        f'<b class="pi-mark" data-ins="{i}" style="--a:{pc(T(t))}">{i + 1}</b>' for i, (t, *_r) in enumerate(INSIGHTS))
    return ticks + marks


def _feed_html():
    out = []
    sit = f"{_sit_steps()}"
    for i in reversed(range(len(INSIGHTS))):
        t, title, why, srcs, _h = INSIGHTS[i]
        chips = "".join(f'<span data-src="{s}">{SRC_NAME[s]}</span>' for s in srcs)
        out.append(
            f'<li class="pi-ins" data-ins="{i}" tabindex="0"><span class="pi-ins-n">{i + 1}</span>'
            f'<div class="pi-ins-b"><p class="pi-ins-h"><time>{clock(T(t))}</time><b>{escape(fr(title))}</b></p>'
            f'<p class="pi-ins-why"><span>Pourquoi{NBSP}:</span> {escape(fr(why.replace("{sit}", sit)))}</p>'
            f'<p class="pi-ins-off">Non relié{NBSP}: une permission est retirée. JARVIS ne devine pas.</p>'
            f'<p class="pi-chips">{chips}</p></div></li>'
        )
    return "".join(out)


def _swap_html(h, d):
    q = lambda s: f"«{NBSP}{s}{NBSP}»"  # noqa: E731
    tabs = "".join(
        f'<button type="button" data-habit="{i}" aria-pressed="{"true" if i == 0 else "false"}">{escape(fr(x["tab"]))}'
        f'{"<em>Plus grand effet</em>" if x["best"] else ""}</button>'
        for i, x in enumerate(HABITS))
    chips = "".join(f'<span data-src="{s}">{SRC_NAME[s]}</span>' for s in h["uses"])
    plan = "".join(f'<li style="--i:{i}">{escape(p)}</li>' for i, p in enumerate(d["plan"]))
    return f"""<section class="pi-swap" data-pi="swap" data-state="ready" aria-label="Proposition du matin">
        <div class="pi-swap-head"><p class="pi-k">{icon("spark")}<span>Proposition du matin · <span class="pi-nw">mardi 6{NBSP}h{NBSP}30</span></span></p>
          <span class="pi-chip">Bien-être · aucun diagnostic</span></div>
        <div class="pi-tabs" role="group" aria-label="Choisir l’habitude à remplacer">{tabs}</div>
        <p class="pi-swap-big"><s data-pi="old">{q(escape(d["old"]))}</s><span class="pi-arrow" aria-hidden="true">→</span><b data-pi="new">{q(escape(d["new"]))}</b></p>
        <p class="pi-sugg" data-pi="sugg">{escape(d["sugg"])}</p>
        <div class="pi-why"><p><b>Pourquoi{NBSP}?</b> <span data-pi="why">{escape(d["why"])}</span></p>
          <p class="pi-chips" data-pi="uses">{chips}</p></div>
        <ul class="pi-plan" data-pi="plan">{plan}</ul>
        <div class="pi-ask">
          <button type="button" class="pi-yes" data-pi="yes">Approuver pour 14{NBSP}jours</button>
          <button type="button" class="pi-no" data-pi="no">Pas maintenant</button>
        </div>
        <p class="pi-wait">{icon("moon")}<span>Proposition prête au réveil · JARVIS observe encore la journée</span></p>
        <p class="pi-ok">{icon("check")}<span><b data-pi="ok-who">Approuvé par Alex</b> · révocable en un geste, à tout moment</span></p>
        <p class="pi-declined">Rien n’a changé. JARVIS ne reproposera pas cette idée avant 7{NBSP}jours.
          <button type="button" data-pi="again">Revoir la proposition</button></p>
        <p class="pi-blocked">{icon("lock")}<span>Cette proposition a besoin de{NBSP}: <b data-pi="need">Téléphone</b>.
          Permission retirée{NBSP}: JARVIS ne propose rien sans elle.</span></p>
      </section>"""


def _week_html(d):
    bars = "".join(f'<i style="--v:{v};--i:{i}"></i>' for i, v in enumerate(d["vals"]))
    dots = "".join(f'<i class="{"is-ok" if c == "1" else ""}" style="--i:{i}"></i>' for i, c in enumerate(d["streak"]))
    kpis = "".join(
        f'<div class="pi-kpi" style="--i:{i}"><span class="pi-kpi-l" data-pi="kpi-l">{escape(k["l"])}</span>'
        f'<b><span data-pi="kpi-v">{escape(k["v"])}</span> <small data-pi="kpi-u">{escape(k["u"])}</small></b>'
        f'<span class="pi-kpi-c" data-pi="kpi-c">{escape(k["c"])}</span></div>'
        for i, k in enumerate(d["kpis"]))
    return f"""<section class="pi-week" data-pi="week" data-state="on" aria-label="Progression de l’essai">
        <div class="pi-week-head"><p class="pi-k">Progression · essai de 14{NBSP}jours</p>
          <span class="pi-delta" data-pi="delta">{escape(d["delta"])}</span></div>
        <p class="pi-metric"><b data-pi="metric">{escape(d["metric"])}</b> <small data-pi="goal">{escape(d["goal"])}</small></p>
        <div class="pi-chart">
          <div class="pi-yax" aria-hidden="true"><span data-pi="ax-t">{d["top"]}</span><span data-pi="ax-b">{d["bottom"]}</span></div>
          <div class="pi-plot">
            <span class="pi-base" data-pi="base" style="--y:{d["base"]}"><span data-pi="base-l">{d["baseL"]}</span></span>
            <div class="pi-bars" data-pi="bars" style="--b:{d["base"]}">{bars}</div>
            <span class="pi-avg" data-pi="avg" style="--y:{d["avg"]}"><span data-pi="avg-l">{d["avgL"]}</span></span>
            <span class="pi-end" data-pi="end" style="--e:{round(d["vals"][-1] * 100, 2)}">{d["end"]}</span>
            <p class="pi-ghost">L’essai commence avec votre accord.</p>
            <p class="pi-paused">{icon("lock")}Suivi en pause · permission retirée</p>
          </div>
          <span class="pi-streak" data-pi="streak" aria-hidden="true">{dots}</span>
          <div class="pi-days" aria-hidden="true"><span>Jour 1</span><span>Jour 7</span><span>Jour 14</span></div>
        </div>
        <div class="pi-kpis">{kpis}</div>
      </section>"""


def html():
    h0 = HABITS[0]
    d0 = _habit_data(h0)
    return f"""<div class="demo-shell pi" data-demo="vie" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Personal Intelligence</b>
    <span class="pi-clock" data-pi="clock">Mardi · 6{NBSP}h{NBSP}30</span><span class="tag tag-sim">Démo · données fictives</span></div>
  <div class="demo-body pi-body" data-pi="body">
    <div class="pi-top">
      <section class="pi-day" data-pi="day" aria-label="La journée d’Alex">
        <div class="pi-day-head">
          <div class="pi-who"><img src="/media/vision/alex-portrait.webp" alt="Alex, la personne de la démonstration" width="320" height="320" loading="lazy" decoding="async">
            <p><b>Journée d’Alex</b><span>Lundi 2{NBSP}novembre · d’un réveil à l’autre</span></p></div>
          <div class="pi-now">
            <div class="pi-ctl"><button type="button" data-pi="play" aria-label="Mettre en pause">{icon("pause", "is-pause")}{icon("play", "is-play")}</button>
              <button type="button" data-pi="replay" aria-label="Rejouer la journée">{icon("replay")}</button></div>
            <p><b data-pi="time">6{NBSP}h{NBSP}30</b><span data-pi="date">Mardi 3{NBSP}novembre</span></p>
          </div>
        </div>
        <div class="pi-tl" data-pi="tl">
          <div class="pi-row pi-row-sky">
            <p class="pi-src-k">{icon("lock")}<span>Sources · <b data-pi="count">4 sur 4</b></span></p>
            <span></span>
            <div class="pi-sky" data-pi="sky" role="slider" tabindex="0" aria-label="Heure de la journée d’Alex"
              aria-valuemin="0" aria-valuemax="{DAY}" aria-valuenow="{DAY}" aria-valuetext="Mardi, 6 h 30">{_sky_html()}</div>
          </div>
          {_rows_html()}
          <div class="pi-row pi-row-axis"><span></span><span></span><div class="pi-axis" aria-hidden="true">{_axis_html()}</div></div>
        </div>
        <p class="pi-hub">{icon("lock")}<span>Analysé sur le <b>Hub privé</b>, à la maison · rien ne quitte la maison</span></p>
      </section>
      <section class="pi-feed" aria-label="Ce que JARVIS relie">
        <div class="pi-feed-head"><p class="pi-k">{icon("spark")}JARVIS relie les points</p><span data-pi="links">5 liens</span></div>
        <p class="pi-feed-empty">JARVIS observe la journée. Chaque lien apparaîtra ici, avec sa raison et ses sources.</p>
        <ol class="pi-ins-list" data-pi="feed">{_feed_html()}</ol>
      </section>
    </div>
    <div class="pi-bottom">
      {_swap_html(h0, d0)}
      {_week_html(d0)}
    </div>
    <div class="pi-erased" data-pi="erased" hidden>
      {icon("erase")}
      <p><b>Données de la démo effacées.</b> Sur un vrai Hub{NBSP}: un seul geste, aucune copie
      ailleurs, une ligne au journal pour le prouver.</p>
      <button type="button" data-pi="restart">Recommencer la démo</button>
    </div>
  </div>
  <div class="pi-foot">
    <ul class="pi-rules">
      <li>{icon("spark")}Chaque lien est expliqué</li>
      <li>{icon("check")}Rien ne se fait sans votre accord</li>
      <li>{icon("lock")}Une permission par source, révocable</li>
    </ul>
    <button type="button" class="pi-erase" data-pi="erase">{icon("erase")}<span>Effacer les données</span></button>
  </div>
  <p class="pi-sr" aria-live="polite" data-pi="live"></p>
  <script type="application/json" data-pi="data">{json.dumps(_data(), ensure_ascii=False)}</script>
</div>
<p class="demo-hint">Retirez une permission · faites glisser la journée · approuvez ou refusez · bien-être seulement, aucun diagnostic · tout est fictif</p>"""
