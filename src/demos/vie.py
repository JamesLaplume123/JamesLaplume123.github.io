# Démo « Une vie entière, un seul système » (assets/demos/vie.css et vie.js).
# Au centre, une personne; autour, les domaines de sa vie; entre les deux, le Hub
# privé installé à la maison, qui reçoit seulement les signaux autorisés.
# Un coach d'habitudes montre comment JARVIS aide à remplacer une mauvaise
# habitude par une bonne : signaux consentis → suggestion expliquée → accord →
# 14 jours → rapport du matin. Bien-être seulement, aucun diagnostic.
#
# Une seule source de vérité : NODES et HABITS. Python produit l'état statique
# (lisible sans JavaScript : la première habitude, étapes empilées) et toute la
# géométrie (orbite, graphiques), transmise au script par un bloc JSON.
# Données entièrement fictives.

import json
import math
import re
from html import escape

NBSP = " "


def fr(s):
    """Espaces insécables de la typographie française (heures, unités, ponctuation, guillemets)."""
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) h (\d)", rf"\1{NBSP}h{NBSP}\2", s)
    s = re.sub(r"(\d) (h|min|%|°C|kWh|pas|soirs?|jours?|nuits?|semaines?|tasses?|après-midi|rencontres?|minutes)\b",
               rf"\1{NBSP}\2", s)
    s = re.sub(r" ([:;?!»])", rf"{NBSP}\1", s)
    return s.replace("« ", "«" + NBSP)


RAW = {"ic", "sp", "line", "area", "k", "uses", "acts", "streak"}  # géométrie et clés : jamais retouchées


def _fr_all(v):
    if isinstance(v, str):
        return fr(v)
    if isinstance(v, list):
        return [_fr_all(x) for x in v]
    if isinstance(v, dict):
        return {k: (x if k in RAW else _fr_all(x)) for k, x in v.items()}
    return v


# ---------------------------------------------------------------------------
# Icônes (traits, 24 × 24)
# ---------------------------------------------------------------------------
ICONS = {
    "home": '<path d="M3.5 10.6 12 4l8.5 6.6"/><path d="M5.6 9.2v10.3h12.8V9.2"/><path d="M10 19.5v-5h4v5"/>',
    "moon": '<path d="M19.6 14.6A7.9 7.9 0 1 1 9.4 4.4a6.4 6.4 0 0 0 10.2 10.2z"/>',
    "rings": '<path d="M12 3.5a8.5 8.5 0 1 1-8.5 8.5"/><path d="M12 7a5 5 0 1 1-5 5"/><circle cx="12" cy="12" r="1.3"/>',
    "repeat": '<path d="M4.5 11A7.6 7.6 0 0 1 17.4 6.6l1.9 1.9"/><path d="M19.6 4.2v4.6H15"/>'
              '<path d="M19.5 13a7.6 7.6 0 0 1-12.9 4.4l-1.9-1.9"/><path d="M4.4 19.8v-4.6H9"/>',
    "case": '<rect x="3.5" y="7.5" width="17" height="12" rx="2.2"/><path d="M9 7.5V5.6c0-.9.7-1.6 1.6-1.6h2.8c.9 0 1.6.7 1.6 1.6v1.9"/><path d="M3.5 12.6h17"/>',
    "people": '<circle cx="9" cy="8.2" r="3.1"/><path d="M3.4 19.6a5.6 5.6 0 0 1 11.2 0"/><circle cx="17.2" cy="9.6" r="2.4"/><path d="M16 14.4a4.5 4.5 0 0 1 4.6 5.2"/>',
    "bolt": '<path d="M13.2 3 5.4 13.6h6l-1 7.4 8.2-10.8h-6.2z"/>',
    "nav": '<path d="M12 3.2 19 20.4l-7-3.7-7 3.7z"/>',
    "shield": '<path d="M12 3.2l7.4 3v5.3c0 4.4-3 7.9-7.4 9.8-4.4-1.9-7.4-5.4-7.4-9.8V6.2z"/><path d="m9 12.1 2.1 2.1 4-4.2"/>',
    "phone": '<rect x="7" y="2.8" width="10" height="18.4" rx="2.6"/><path d="M11 18h2"/>',
    "watch": '<rect x="6.4" y="6.4" width="11.2" height="11.2" rx="3.2"/><path d="M9 6.4 9.6 3h4.8l.6 3.4M9 17.6l.6 3.4h4.8l.6-3.4"/><path d="M12 9.6V12l1.6 1"/>',
    "bulb": '<path d="M9.2 18h5.6M10.2 21h3.6"/><path d="M12 3a6 6 0 0 0-3.7 10.7c.8.6 1.1 1.5 1.1 2.4h5.2c0-.9.3-1.8 1.1-2.4A6 6 0 0 0 12 3z"/>',
    "coffee": '<path d="M4.6 9.2h11.8v4.6a5 5 0 0 1-5 5h-1.8a5 5 0 0 1-5-5z"/><path d="M16.4 10.6h1.4a2.5 2.5 0 0 1 0 5h-1.6"/><path d="M8.6 3.6c-.6.9.6 1.6 0 2.6M12.2 3.6c-.6.9.6 1.6 0 2.6"/>',
    "calendar": '<rect x="3.6" y="5" width="16.8" height="15" rx="2.2"/><path d="M3.6 10h16.8M8 3v4M16 3v4"/>',
    "book": '<path d="M12 6.6C10 5.1 7.1 4.6 3.6 5v13c3.5-.4 6.4.1 8.4 1.6 2-1.5 4.9-2 8.4-1.6V5c-3.5-.4-6.4.1-8.4 1.6z"/><path d="M12 6.6v13"/>',
    "check": '<path d="m5 12.5 4.4 4.3L19 7.2"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
    "erase": '<path d="M4.5 7h15M9.5 7V4.8h5V7"/><path d="M6.6 7 7.5 20h9l.9-13"/>',
    "spark": '<path d="M12 3.5 13.9 9l5.6 1.9-5.6 1.9L12 18.4l-1.9-5.6-5.6-1.9L10.1 9z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# Les domaines de la vie (clé, nom, nom court, icône, valeur au repos)
# ---------------------------------------------------------------------------
NODES = [
    ("maison", "Maison", "Maison", "home", "21 °C · calme"),
    ("sommeil", "Sommeil", "Sommeil", "moon", "7 h 02"),
    ("activite", "Activité", "Activité", "rings", "6 840 pas"),
    ("habitudes", "Habitudes", "Habitudes", "repeat", "3 en cours"),
    ("travail", "Travail", "Travail", "case", "3 rencontres"),
    ("famille", "Famille", "Famille", "people", "Souper 18 h 15"),
    ("energie", "Énergie", "Énergie", "bolt", "8,4 kWh"),
    ("deplacements", "Déplacements", "Trajets", "nav", "Départ 8 h 05"),
    ("securite", "Sécurité", "Sécurité", "shield", "Verrouillée"),
]

# Géométrie de l'orbite (repère 1000 × 1000, centre 500 × 500)
R_NODE, R_HUB, R_ME = 382, 172, 118
NODE_EDGE = 60  # rayon visuel d'une pastille, en unités du repère


def _angle(i):
    return math.radians(-90 + i * 360 / len(NODES))


def _node_pos(i):
    a = _angle(i)
    return 500 + R_NODE * math.cos(a), 500 + R_NODE * math.sin(a)


def _spoke(i):
    """Rayon du nœud vers l'anneau du Hub (sens du flux : vers le Hub)."""
    a = _angle(i)
    r1, r2 = R_NODE - NODE_EDGE, R_HUB + 10
    return (f"M{500 + r1 * math.cos(a):.1f} {500 + r1 * math.sin(a):.1f} "
            f"L{500 + r2 * math.cos(a):.1f} {500 + r2 * math.sin(a):.1f}")


# ---------------------------------------------------------------------------
# Les habitudes (données fictives)
# ---------------------------------------------------------------------------
HABITS = [
    {
        "k": "lecture",
        "tab": "Téléphone au lit",
        "old": "Téléphone au lit",
        "new": "20 minutes de lecture",
        "uses": ["sommeil", "maison", "habitudes"],
        "acts": ["maison"],
        "signals": [
            ("phone", "Écran au lit", "Téléphone · autorisé", "52 min", [48, 61, 44, 57, 52, 63, 49]),
            ("watch", "Endormissement", "Montre · autorisée", "0 h 48", [40, 55, 38, 52, 47, 58, 46]),
            ("bulb", "Lumière éteinte", "Chambre · capteur local", "0 h 31", [30, 44, 26, 41, 35, 47, 33]),
        ],
        "when": "Lundi · 21 h 04",
        "sugg": "Et si le téléphone dormait dans la cuisine ? À 22 h 30, la chambre passe en lumière "
                "de lecture et le téléphone en mode nuit. Vingt minutes de lecture remplacent le défilement.",
        "why": "Les 4 soirs sur 14 où l’écran s’est éteint avant 22 h 45, Alex s’est endormie 31 minutes plus tôt.",
        "plan": ["22 h 30 · la chambre passe en lumière de lecture",
                 "22 h 30 · le téléphone passe en mode nuit, appels urgents permis",
                 "Essai de 14 jours, puis un bilan : Alex décide de la suite"],
        "chart": {"label": "Heure d’endormissement", "fmt": "time", "base": 48, "lo": -15, "hi": 60, "invert": True,
                  "pts": [44, 39, 51, 30, 26, 33, 18, 41, 15, 12, 20, 8, 10, 6]},
        "streak": "11011110111111",
        "streak_label": "Soirs de lecture",
        "kpis": [
            ("Endormissement", "{gain}", "min", "plus tôt · 7 derniers soirs"),
            ("Écran au lit", "9", "min", "avant : 52 min"),
            ("Lecture", "{streak}", "soirs sur 14", "objectif : 10"),
        ],
        "sig": {"sommeil": "Endormie 0 h 48", "maison": "Chambre allumée", "habitudes": "Écran 52 min"},
        "after": {"sommeil": "7 h 26", "maison": "Lecture 22 h 30", "habitudes": "Série · 6 soirs"},
        "report": [
            ("moon", "Sommeil", "7 h 26 · 38 min de plus que la moyenne"),
            ("book", "Lecture", "12 soirs sur 14 · série en cours : 6"),
            ("case", "Aujourd’hui", "3 rencontres · la première à 9 h"),
            ("nav", "Départ conseillé", "8 h 05 · chaussée glissante annoncée"),
        ],
        "tip": "Marche de 15 minutes à 12 h 10 ? L’agenda est libre.",
        "tipwhy": "2 100 pas hier avant midi.",
    },
    {
        "k": "tisane",
        "tab": "Café tardif",
        "old": "Café à 16 h 40",
        "new": "Tisane après 15 h",
        "uses": ["maison", "sommeil", "travail"],
        "acts": ["maison"],
        "signals": [
            ("coffee", "Dernier café", "Machine à café · Maison", "16 h 40", [44, 52, 38, 60, 47, 55, 41]),
            ("watch", "Durée du sommeil", "Montre · autorisée", "6 h 35", [52, 40, 58, 36, 47, 42, 50]),
            ("calendar", "Rencontres après 15 h", "Agenda · lecture seule", "4 / sem.", [30, 45, 40, 55, 35, 50, 45]),
        ],
        "when": "Lundi · 14 h 52",
        "sugg": "Après 15 h, la machine à café propose d’abord une tisane : même pause, même rituel, sans "
                "caféine. Le café reste possible — il suffit de le demander.",
        "why": "Les jours où le dernier café est pris avant 14 h, Alex dort 41 minutes de plus en moyenne (21 jours observés).",
        "plan": ["Dès 15 h · la machine propose la tisane en premier",
                 "Le café reste à un geste, sans commentaire",
                 "Essai de 14 jours, puis un bilan : Alex décide de la suite"],
        "chart": {"label": "Durée du sommeil", "fmt": "dur", "base": 395, "lo": 360, "hi": 460, "invert": False,
                  "pts": [392, 401, 388, 410, 415, 398, 422, 419, 430, 404, 428, 436, 431, 438]},
        "streak": "11011011101111",
        "streak_label": "Après-midi à la tisane",
        "kpis": [
            ("Sommeil", "{gain}", "min", "de plus · 7 dernières nuits"),
            ("Dernier café", "14 h 50", "", "avant : 16 h 40"),
            ("Tisane", "{streak}", "après-midi sur 14", "sans effort de mémoire"),
        ],
        "sig": {"maison": "Café 16 h 40", "sommeil": "6 h 35", "travail": "4 rencontres PM"},
        "after": {"maison": "Tisane 15 h 20", "sommeil": "7 h 18", "travail": "2 rencontres"},
        "report": [
            ("moon", "Sommeil", "7 h 18 · 36 min de plus qu’il y a deux semaines"),
            ("coffee", "Tisane", "11 après-midi sur 14 · proposée dès 15 h"),
            ("case", "Aujourd’hui", "2 rencontres · la dernière finit à 16 h"),
            ("bolt", "Énergie", "Chauffe-eau décalé à 2 h · tarif plus bas"),
        ],
        "tip": "Coucher vers 22 h 45 ce soir ? Le réveil sonne à 6 h 30.",
        "tipwhy": "c’est le rythme de ses 14 dernières nuits.",
    },
    {
        "k": "marche",
        "tab": "Assise tout le jour",
        "old": "Assise 9 h par jour",
        "new": "Pause marche aux 90 minutes",
        "uses": ["activite", "travail", "habitudes"],
        "acts": ["travail"],
        "signals": [
            ("watch", "Temps assis", "Montre · autorisée", "9 h 20", [55, 48, 60, 52, 58, 45, 57]),
            ("calendar", "Rencontres sans pause", "Agenda · lecture seule", "3 h 40", [40, 58, 35, 50, 62, 44, 48]),
            ("rings", "Pas par jour", "Montre · autorisée", "4 200", [42, 38, 47, 35, 40, 52, 39]),
        ],
        "when": "Lundi · 10 h 15",
        "sugg": "Après 90 minutes de travail sans pause, et seulement si l’agenda est libre, JARVIS propose "
                "8 minutes de marche. Jamais pendant une rencontre, jamais après 18 h.",
        "why": "Les journées avec au moins trois pauses comptent 3 000 pas de plus, sans réduire le temps de travail concentré.",
        "plan": ["Après 90 minutes sans pause · rappel discret sur la montre",
                 "Seulement si l’agenda est libre, jamais après 18 h",
                 "Essai de 14 jours, puis un bilan : Alex décide de la suite"],
        "chart": {"label": "Pas par jour", "fmt": "int", "base": 4200, "lo": 3000, "hi": 8500, "invert": False,
                  "pts": [4310, 5120, 3980, 5800, 6240, 5010, 6650, 7020, 4400, 6890, 7310, 7120, 7480, 7650]},
        "streak": "01011011011111",
        "streak_label": "Jours avec pauses",
        "kpis": [
            ("Pas par jour", "+{gain}", "", "moyenne · 7 derniers jours"),
            ("Temps assis", "−1 h 10", "", "avant : 9 h 20"),
            ("Pauses", "{streak}", "jours sur 14", "objectif : 10"),
        ],
        "sig": {"activite": "4 200 pas", "travail": "3 h 40 sans pause", "habitudes": "9 h 20 assise"},
        "after": {"activite": "7 650 pas", "travail": "Pause 10 h 30", "habitudes": "Série · 5 jours"},
        "report": [
            ("rings", "Activité", "Hier : 7 650 pas · objectif atteint"),
            ("repeat", "Pauses marche", "10 jours sur 14 · aux 90 minutes"),
            ("case", "Aujourd’hui", "Concentration de 9 h à 11 h 30 · pause à 10 h 30"),
            ("people", "Famille", "Souper à 18 h 15 · Léa rentre à 17 h 40"),
        ],
        "tip": "Aller à pied à la rencontre de 14 h ? 12 minutes, temps sec.",
        "tipwhy": "en voiture, le trajet prend 9 minutes avec le stationnement.",
    },
]

STEPS = ["Signaux", "Suggestion", "14 jours", "Rapport"]
CLOCK = ["14 jours observés", None, "Jours 1 à 14", "Mardi · 6 h 30"]

# Graphique (repère 560 × 190)
CW, CH, CPAD = 560, 190, 14


def _fmt(v, kind):
    if kind == "time":
        m = int(round(v)) % (24 * 60)
        return f"{m // 60} h {m % 60:02d}"
    if kind == "dur":
        return f"{int(v) // 60} h {int(v) % 60:02d}"
    return f"{int(round(v)):,}".replace(",", " ")


def _y(v, c):
    t = (v - c["lo"]) / (c["hi"] - c["lo"])
    if c["invert"]:
        t = 1 - t
    return CPAD + (1 - t) * (CH - 2 * CPAD)


def _chart(h):
    c = h["chart"]
    n = len(c["pts"])
    xs = [CPAD + i * (CW - 2 * CPAD) / (n - 1) for i in range(n)]
    ys = [_y(v, c) for v in c["pts"]]
    # Courbe lissée (Catmull-Rom → Bézier)
    d = f"M{xs[0]:.1f} {ys[0]:.1f}"
    for i in range(n - 1):
        x0, y0 = (xs[i - 1], ys[i - 1]) if i else (xs[i], ys[i])
        x1, y1, x2, y2 = xs[i], ys[i], xs[i + 1], ys[i + 1]
        x3, y3 = (xs[i + 2], ys[i + 2]) if i + 2 < n else (x2, y2)
        d += (f" C{x1 + (x2 - x0) / 6:.1f} {y1 + (y2 - y0) / 6:.1f} "
              f"{x2 - (x3 - x1) / 6:.1f} {y2 - (y3 - y1) / 6:.1f} {x2:.1f} {y2:.1f}")
    area = d + f" L{xs[-1]:.1f} {CH} L{xs[0]:.1f} {CH} Z"
    base = c["base"]
    last7 = sum(c["pts"][-7:]) / 7
    gain = round(abs(base - last7), -1 if c["fmt"] == "int" else 0)
    # Étiquettes de l'axe : la plus haute valeur affichée est toujours « la meilleure »
    top, bottom = (c["lo"], c["hi"]) if c["invert"] else (c["hi"], c["lo"])
    return {
        "label": c["label"],
        "line": d,
        "area": area,
        "baseY": round(_y(base, c) / CH * 100, 2),
        "baseL": "Avant : " + _fmt(base, c["fmt"]),
        "endX": round(xs[-1] / CW * 100, 2),
        "endY": round(ys[-1] / CH * 100, 2),
        "endL": _fmt(c["pts"][-1], c["fmt"]),
        "top": _fmt(top, c["fmt"]),
        "bottom": _fmt(bottom, c["fmt"]),
        "gain": gain,
    }


def _spark(vals):
    """Petite courbe de 7 jours (repère 84 × 28)."""
    lo, hi = min(vals), max(vals)
    pts = [(2 + i * 80 / (len(vals) - 1), 25 - (v - lo) / max(1, hi - lo) * 21) for i, v in enumerate(vals)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _habit_data(h):
    ch = _chart(h)
    streak = h["streak"].count("1")
    gain = f"{int(ch['gain']):,}".replace(",", " ")
    kpis = [
        {"l": l, "v": v.replace("{gain}", gain).replace("{streak}", str(streak)), "u": u, "c": c}
        for l, v, u, c in h["kpis"]
    ]
    return {
        "k": h["k"], "old": h["old"], "new": h["new"], "uses": h["uses"], "acts": h["acts"],
        "signals": [{"ic": ICONS[ic], "t": t, "src": src, "v": v, "sp": _spark(sp)} for ic, t, src, v, sp in h["signals"]],
        "when": h["when"], "sugg": h["sugg"], "why": h["why"], "plan": h["plan"],
        "chart": ch, "streak": h["streak"], "streakL": h["streak_label"], "kpis": kpis,
        "sig": h["sig"], "after": h["after"],
        "report": [{"ic": ICONS[ic], "l": l, "v": v} for ic, l, v in h["report"]],
        "tip": h["tip"], "tipwhy": h["tipwhy"],
    }


DATA = _fr_all({
    "habits": [_habit_data(h) for h in HABITS],
    "nodes": {k: v for k, _n, _s, _i, v in NODES},
    "clock": CLOCK,
})


# ---------------------------------------------------------------------------
# Balisage
# ---------------------------------------------------------------------------
def _nodes_html():
    out = []
    for i, (k, name, short, ic, val) in enumerate(NODES):
        x, y = _node_pos(i)
        s = f' data-s="{short}"' if short != name else ""
        up = " is-up" if math.sin(_angle(i)) < -0.5 else ""  # en haut : étiquette au-dessus, loin du rayon
        out.append(
            f'<div class="vi-node{up}" data-node="{k}" style="--x:{x / 10:.2f}%;--y:{y / 10:.2f}%">'
            f'<span class="vi-dot">{icon(ic)}</span>'
            f'<b{s}>{name}</b><small data-vi-v>{escape(fr(val))}</small></div>'
        )
    return "".join(out)


def _spokes_svg():
    out = []
    for i, (k, *_r) in enumerate(NODES):
        d = _spoke(i)
        out.append(
            f'<g data-node="{k}" style="--d:{(i * 0.37) % 2.6:.2f}s">'
            f'<path class="vi-spoke" d="{d}"/>'
            f'<path class="vi-pulse" d="{d}" pathLength="100"/>'
            f'<path class="vi-pulse vi-pulse-b" d="{d}" pathLength="100"/></g>'
        )
    return "".join(out)


def _signals_html(d):
    return "".join(
        f'<li class="vi-sig" style="--i:{i}"><span class="vi-ic">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" data-vi="sig-ic">{s["ic"]}</svg></span>'
        f'<span class="vi-sig-t"><b data-vi="sig-t">{escape(s["t"])}</b><small data-vi="sig-src">{escape(s["src"])}</small></span>'
        f'<svg class="vi-spark" viewBox="0 0 84 28" aria-hidden="true"><path data-vi="sig-sp" d="{s["sp"]}" pathLength="1"/></svg>'
        f'<span class="vi-sig-v" data-vi="sig-v">{escape(s["v"])}</span></li>'
        for i, s in enumerate(d["signals"])
    )


def _streak_html(d):
    return "".join(f'<i class="{"is-ok" if c == "1" else ""}" style="--i:{i}"></i>' for i, c in enumerate(d["streak"]))


def _kpis_html(d):
    return "".join(
        f'<div class="vi-kpi" style="--i:{i}"><span class="vi-kpi-l" data-vi="kpi-l">{escape(k["l"])}</span>'
        f'<b><span data-vi="kpi-v">{escape(k["v"])}</span> <small data-vi="kpi-u">{escape(k["u"])}</small></b>'
        f'<span class="vi-kpi-c" data-vi="kpi-c">{escape(k["c"])}</span></div>'
        for i, k in enumerate(d["kpis"])
    )


def _report_html(d):
    return "".join(
        f'<li style="--i:{i}"><span class="vi-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" data-vi="rep-ic">{r["ic"]}</svg></span>'
        f'<span class="vi-rep-l" data-vi="rep-l">{escape(r["l"])}</span><span class="vi-rep-v" data-vi="rep-v">{escape(r["v"])}</span></li>'
        for i, r in enumerate(d["report"])
    )


def html():
    d = DATA["habits"][0]
    c = d["chart"]
    tabs = "".join(
        f'<button type="button" data-habit="{i}" aria-pressed="{"true" if i == 0 else "false"}">{escape(fr(h["tab"]))}</button>'
        for i, h in enumerate(HABITS)
    )
    cur = ' aria-current="step"'
    steps = "".join(
        f'<li><button type="button" data-step="{i}"{cur if i == 0 else ""}>'
        f'<i>{i + 1:02d}</i><span>{s}</span><em class="vi-bar" aria-hidden="true"></em></button></li>'
        for i, s in enumerate(STEPS)
    )
    q = lambda s: f"«{NBSP}{s}{NBSP}»"  # noqa: E731
    plan = "".join(f'<li style="--i:{i}">{escape(x)}</li>' for i, x in enumerate(d["plan"]))
    return f"""<div class="demo-shell vi" data-demo="vie" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Ma vie</b>
    <span class="vi-clock" data-vi="clock">{fr(CLOCK[0])}</span><span class="tag tag-sim">Démo · données fictives</span></div>
  <div class="demo-body vi-body">
    <div class="vi-stage">
      <div class="vi-orbit" data-vi="orbit">
        <svg class="vi-svg" viewBox="0 0 1000 1000" aria-hidden="true">
          <defs>
            <radialGradient id="vi-halo"><stop offset="0" stop-color="currentColor" stop-opacity=".22"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></radialGradient>
          </defs>
          <circle class="vi-halo" cx="500" cy="500" r="330" fill="url(#vi-halo)"/>
          <circle class="vi-ring-out" cx="500" cy="500" r="{R_NODE}"/>
          <g class="vi-spokes">{_spokes_svg()}</g>
          <circle class="vi-hub-ring" cx="500" cy="500" r="{R_HUB}"/>
          <g class="vi-hub-ticks"><circle cx="500" cy="500" r="{R_HUB + 18}" pathLength="360"/></g>
          <circle class="vi-wave" cx="500" cy="500" r="{R_ME + 6}"/>
          <circle class="vi-wave vi-wave-b" cx="500" cy="500" r="{R_ME + 6}"/>
        </svg>
        <div class="vi-me"><img src="/media/vision/alex-portrait.webp" alt="Alex, la personne au centre de la démonstration" width="320" height="320" loading="lazy" decoding="async"></div>
        <p class="vi-hub-label">{icon("lock")}<span><b>Hub privé</b> · à la maison</span></p>
        {_nodes_html()}
      </div>
    </div>

    <div class="vi-panel">
      <div class="vi-coach-head">
        <p class="vi-k">Coach d’habitudes</p>
        <div class="vi-habits" role="group" aria-label="Choisir l’habitude à remplacer">{tabs}</div>
      </div>
      <p class="vi-swap"><span class="vi-old" data-vi="old">{q(escape(fr(d["old"])))}</span>
        <span class="vi-arrow" aria-hidden="true">→</span>
        <span class="vi-new" data-vi="new">{q(escape(fr(d["new"])))}</span></p>
      <ol class="vi-steps" aria-label="Étapes">{steps}</ol>

      <div class="vi-views">
        <section class="vi-view is-on" data-view="0" aria-label="Signaux">
          <p class="vi-k">Ce que JARVIS remarque · avec permission</p>
          <ul class="vi-sigs">{_signals_html(d)}</ul>
          <p class="vi-note">{icon("lock")}<span>Sources autorisées une par une · analysées sur le Hub, rien ne quitte la maison</span></p>
        </section>

        <section class="vi-view" data-view="1" aria-label="Suggestion">
          <div class="vi-msg">
            <p class="vi-k">{icon("spark")}JARVIS propose · <span data-vi="when">{fr(d["when"])}</span></p>
            <p class="vi-sugg" data-vi="sugg">{escape(d["sugg"])}</p>
            <p class="vi-why"><b>Pourquoi{NBSP}?</b> <span data-vi="why">{escape(d["why"])}</span></p>
          </div>
          <div class="vi-plan">
            <p class="vi-k">Si Alex approuve</p>
            <ul data-vi="plan">{plan}</ul>
          </div>
          <div class="vi-ask" data-vi="ask">
            <button type="button" class="vi-yes" data-vi="yes">Approuver pour 14 jours</button>
            <button type="button" class="vi-no" data-vi="no">Pas maintenant</button>
          </div>
          <p class="vi-ok" data-vi="ok" hidden>{icon("check")}<span><b data-vi="ok-who">Approuvé par Alex</b> · révocable en un geste, à tout moment</span></p>
          <p class="vi-declined" data-vi="declined" hidden>Rien n’a changé. JARVIS ne reproposera pas cette idée avant 7{NBSP}jours.
            <button type="button" data-vi="again">Revoir la suggestion</button></p>
        </section>

        <section class="vi-view" data-view="2" aria-label="14 jours">
          <div class="vi-chart-head"><p class="vi-k" data-vi="chart-l">{escape(c["label"])}</p>
            <span class="vi-legend"><i aria-hidden="true"></i><span data-vi="streak-l">{escape(d["streakL"])}</span></span></div>
          <div class="vi-chart">
            <div class="vi-yax" aria-hidden="true"><span data-vi="ax-t">{c["top"]}</span><span data-vi="ax-b">{c["bottom"]}</span></div>
            <div class="vi-plot">
              <svg viewBox="0 0 {CW} {CH}" aria-hidden="true">
                <defs><linearGradient id="vi-area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".24"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>
                <path class="vi-grid" d="M0 {CPAD} H{CW} M0 {CH // 2} H{CW} M0 {CH - CPAD} H{CW}"/>
                <path class="vi-area" data-vi="area" d="{c["area"]}" fill="url(#vi-area)"/>
                <path class="vi-line" data-vi="line" d="{c["line"]}" pathLength="1"/>
              </svg>
              <span class="vi-base" data-vi="base" style="--y:{c["baseY"]}%"><span data-vi="base-l">{c["baseL"]}</span></span>
              <span class="vi-end" data-vi="end" style="--x:{c["endX"]}%;--y:{c["endY"]}%"><span data-vi="end-l">{c["endL"]}</span></span>
            </div>
            <span class="vi-dots" data-vi="dots" aria-hidden="true">{_streak_html(d)}</span>
            <div class="vi-days" aria-hidden="true"><span>Jour 1</span><span>Jour 7</span><span>Jour 14</span></div>
          </div>
          <div class="vi-kpis" data-vi="kpis">{_kpis_html(d)}</div>
        </section>

        <section class="vi-view" data-view="3" aria-label="Rapport du matin">
          <div class="vi-report">
            <div class="vi-rep-head"><p class="vi-k">Rapport du matin</p><span>Matin · Soir · Semaine</span></div>
            <p class="vi-hello">Bonjour Alex.</p>
            <ul class="vi-rep" data-vi="rep">{_report_html(d)}</ul>
            <div class="vi-tip">
              <p><b>Suggestion du jour.</b> <span data-vi="tip">{escape(d["tip"])}</span></p>
              <p class="vi-tip-why">Pourquoi{NBSP}: <span data-vi="tipwhy">{escape(d["tipwhy"])}</span></p>
              <button type="button" data-vi="tip-add">Ajouter à l’agenda</button>
            </div>
          </div>
        </section>
      </div>
      <div class="vi-erased" data-vi="erased" hidden>
        {icon("erase")}
        <p><b>Données de la démo effacées.</b> Sur un vrai Hub{NBSP}: un seul geste, aucune copie
        ailleurs, une ligne au journal pour le prouver.</p>
        <button type="button" data-vi="restart">Recommencer la démo</button>
      </div>
    </div>
  </div>
  <div class="vi-foot">
    <ul class="vi-rules">
      <li>{icon("spark")}Chaque suggestion est expliquée</li>
      <li>{icon("check")}Rien ne se fait sans votre accord</li>
      <li>{icon("lock")}Données gardées chez vous, effaçables</li>
    </ul>
    <button type="button" class="vi-erase" data-vi="erase">{icon("erase")}<span>Effacer les données</span></button>
  </div>
  <p class="vi-sr" aria-live="polite" data-vi="live"></p>
  <script type="application/json" data-vi="data">{json.dumps(DATA, ensure_ascii=False)}</script>
</div>
<p class="demo-hint">Choisissez une habitude · approuvez ou refusez · bien-être seulement, aucun diagnostic · tout est fictif</p>"""
