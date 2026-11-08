# Démo « Environnements intelligents » : un seul modèle de logiciel pour tous les lieux.
# BouLance (le véhicule récréatif), résidence de prestige, chalet d'architecte, entreprise, garage de
# collection, ferme, yacht à moteur et avion d'affaires
# partagent les mêmes sections (Vue d'ensemble, Éclairage, Confort, Énergie, Eau, Sécurité,
# Internet, Équipements, Voyage et entretien, Modes et activité) et les mêmes cartes.
# Seules les données changent : « Le même modèle, uniquement vos données lorsqu'elles seront reliées. »
#
# Ce fichier est la source de vérité : un dictionnaire par environnement, transmis au script
# (assets/demos/env.js) dans un bloc JSON. Le script dessine chaque section seulement quand elle
# s'ouvre. Le module Éclairage vient de demos/lumieres.py (contrat window.JarvisLumieres).
#
# Toutes les valeurs sont des données d'exemple, sauf les batteries de BouLance (service /live du
# site, étiquetées « réel ») et les calculs astronomiques (soleil et lune pour la vraie date).
#
# Carte d'un onglet : {"type": <sorte de carte>, "w": <largeur sur 12 colonnes>, ...champs propres}.
# Section : liste de cartes (un seul écran) ou liste d'onglets [clé, libellé, [cartes]].
# Temps relatifs : "d" = jours depuis aujourd'hui, "h" = heure locale « 14:00 », "ago" = minutes écoulées.

import json
import os
import re

try:
    from demos import lumieres
except ImportError:  # module d'éclairage livré séparément
    lumieres = None

NB = " "


def _fr(s):
    """Typographie française : espaces insécables avant : ; ? ! », après «, dans les heures et unités."""
    s = re.sub(r" ([:;?!»])", NB + r"\1", s)
    s = s.replace("« ", "«" + NB)
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NB}\2", s)
    s = re.sub(r"(\d) h (\d)", rf"\1{NB}h{NB}\2", s)
    s = re.sub(r"(\d) h\b", rf"\1{NB}h", s)
    s = re.sub(r"(\d) (°C|°|%|min\b|km\b|km/h|kW|kWh|kWc|Wc|W\b|L\b|Go\b|Mbit/s|Gbit/s|ms\b|ppm|hPa|bar\b|kg\b|Ah\b|V\b|A\b|kV|psi|nœuds|m\b|j\b|jours?\b|lb\b|t\b|pi\b)", rf"\1{NB}\2", s)
    return s.replace(" – ", NB + "–" + NB).replace(" · ", NB + "· ")


_SKIP = {"type", "icon", "img", "art", "pos", "map", "go", "key", "k", "tone", "kind", "sky", "p24", "amb", "id"}


def _typo(v, key=None):
    if isinstance(v, str):
        return v if key in _SKIP or v.startswith("/") else _fr(v)
    if isinstance(v, list):
        return [_typo(x, key) for x in v]
    if isinstance(v, dict):
        return {k: _typo(x, k) for k, x in v.items()}
    return v


def C(t, w=12, **kw):
    """Une carte : sorte, largeur (sur 12), champs propres."""
    return {"type": t, "w": w, **kw}


def photo_ou_attente(cle, alt, pos="50% 50%"):
    """Bannière d'un environnement : la photo media/env/<clé>.webp dès qu'elle existe
    (déposer le fichier puis reconstruire, aucun changement de code); sinon le panneau
    d'attente premium (verre noir, filet doré, « Photo à venir » — jamais de dessin)."""
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "media", "env", cle + ".webp")
    if os.path.exists(chemin):
        return {"img": "/media/env/" + cle + ".webp", "pos": pos, "alt": alt}
    return {"ph": True, "alt": alt}


_MEDIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "media", "env")
PHOTOS_ATTENDUES = []  # (fichier, description) : photos que James peut générer plus tard


def _slug(s):
    s = s.lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c"), ("œ", "oe")):
        for ch in a:
            s = s.replace(ch, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _photo(dossier, nom, description):
    """Emplacement photo : media/env/<dossier>/<nom>.webp s'il existe au build, sinon None (panneau « Photo à venir »)."""
    PHOTOS_ATTENDUES.append(("media/env/" + dossier + "/" + nom + ".webp", description))
    if os.path.exists(os.path.join(_MEDIA, dossier, nom + ".webp")):
        return "/media/env/" + dossier + "/" + nom + ".webp"
    return None


# ---------------------------------------------------------------------------------------------
# Sources des listes et de l'entretien : d'où vient chaque élément, et comment l'échéance est calculée.
#   fab      Manuel du fabricant (intervalle)          compteur  Compteur kilométrique ou heures moteur
#   capteur  Mesure d'un capteur                        saison    Saison et météo
#   vous     Ajouté par vous                            jarvis    Recommandé par JARVIS selon l'usage
#   regle    Règlement en vigueur
# Une source s'écrit « sorte|détail » dans les listes; l'entretien utilise les fonctions ci-dessous.
# ---------------------------------------------------------------------------------------------

def _src(s):
    if isinstance(s, dict) or s is None:
        return s
    k, _, t = s.partition("|")
    return {"k": k, "t": t}


def M(icon, title, detail, src):
    """Ligne d'entretien : l'échéance (jours) et l'état découlent de la source."""
    due = src["due"]
    return [icon, title, detail, due, "late" if due < 0 else "soon" if due <= 14 else "ok", src]


def fab(ref, every, n, last):
    """Intervalle du fabricant : fait il y a -last jours, à refaire aux n jours."""
    return {"k": "fab", "ref": ref, "every": every, "basis": "date", "n": n, "last": last, "due": last + n}


def compteur(ref, every, now, at, rate, unit="km", k="compteur"):
    """Compteur (km, heures, cycles, traites) : now depuis le dernier entretien, à refaire à at, rythme moyen rate par jour."""
    return {"k": k, "ref": ref, "every": every, "basis": "count", "now": now, "at": at, "rate": rate, "unit": unit,
            "due": int(round((at - now) / rate))}


def src_fixe(k, ref, due, why=""):
    """Échéance fixée par une saison, un capteur, vous, JARVIS ou un règlement."""
    return {"k": k, "ref": ref, "why": why, "basis": "fixed", "due": due}


def regle_date(ref, mmdd, why=""):
    """Règlement à date fixe (MM-JJ) : l'échéance est calculée pour la vraie date."""
    import datetime
    today = datetime.date.today()
    m, d = (int(x) for x in mmdd.split("-"))
    t = datetime.date(today.year, m, d)
    if t < today:
        t = datetime.date(today.year + 1, m, d)
    return {"k": "regle", "ref": ref, "why": why, "basis": "date-fixe", "mmdd": mmdd, "due": (t - today).days}


def O(label, state, tone, zone, ago, who="", lock=None, icon=None):
    """Une ouverture (porte, fenêtre, trappe) : état, zone, dernière ouverture (minutes) et par qui."""
    o = {"label": label, "state": state, "tone": tone, "zone": zone, "ago": ago, "who": who}
    if lock is not None:
        o["lock"] = lock
    if icon:
        o["icon"] = icon
    return o


# =============================================================================================
# BouLance · véhicule récréatif (le laboratoire mobile). Scénario : stationné à Roberval,
# Lac-Saint-Jean, pendant le Tour du Lac-Saint-Jean. Batteries réelles quand la liaison répond.
# =============================================================================================

LAC = {  # Lac-Saint-Jean stylisé (géographie illustrative, 5 unités par kilomètre)
    "km": 5,
    "water": [[[150, 62], [190, 44], [236, 40], [272, 48], [302, 70], [318, 100], [320, 132], [306, 164],
               [276, 186], [236, 198], [194, 198], [158, 186], [130, 166], [116, 138], [118, 106], [130, 80]]],
    "rivers": [[[118, 108], [86, 92], [56, 70], [20, 52], [0, 46]], [[178, 46], [174, 20], [168, 0]],
               [[250, 42], [258, 18], [266, 0]], [[318, 122], [350, 116], [376, 120], [400, 126]],
               [[136, 172], [118, 204], [110, 240]]],
    "roads": [{"pts": [[106, 150], [96, 124], [80, 98], [104, 66], [138, 44], [170, 30], [210, 24], [252, 32],
                       [296, 46], [326, 78], [340, 112], [334, 134], [316, 170], [282, 200], [236, 212],
                       [198, 212], [160, 202], [128, 180], [106, 150]], "n": "169", "at": [92, 112]},
              {"pts": [[334, 134], [366, 142], [400, 152]], "n": "170", "at": [372, 144]},
              {"pts": [[160, 202], [154, 222], [150, 240]], "n": "155", "at": [155, 224]},
              {"pts": [[80, 98], [48, 112], [0, 120]], "minor": True},
              {"pts": [[106, 150], [70, 166], [30, 176], [0, 180]], "minor": True}],
    "towns": [[104, 151, "Roberval", "b"], [76, 92, "Saint-Félicien", "a"], [170, 24, "Dolbeau-Mistassini"],
              [252, 26, "Péribonka"], [344, 134, "Alma"], [236, 220, "Métabetchouan"], [158, 210, "Chambord"]],
    "lake": [218, 122, "Lac Saint-Jean"],
    "me": [104, 150],
}

BOULANCE_TRIP = {
    "done": [[334, 134], [316, 170], [282, 200], [236, 212], [198, 212], [160, 202], [128, 180], [104, 150]],
    "next": [[104, 150], [96, 124], [80, 98]],
    "later": [[80, 98], [104, 66], [138, 44], [170, 30], [210, 24], [252, 32], [296, 46], [326, 78], [340, 112], [334, 134]],
}

BOULANCE_POINTS = [
    {"n": 1, "x": 114, "y": 130, "kind": "eau", "name": "Aire de service du lac", "what": "Remplissage", "dist": "2,4 km",
     "info": "Eau potable : à confirmer · horaires : à confirmer"},
    {"n": 2, "x": 84, "y": 168, "kind": "vidange", "name": "Station municipale", "what": "Vidange", "dist": "5,8 km",
     "info": "Accès : à confirmer · tarif : à confirmer"},
    {"n": 3, "x": 134, "y": 186, "kind": "eau", "name": "Relais routier", "what": "Eau et vidange", "dist": "8,1 km",
     "info": "Accès : à confirmer · ouvert à l’année (exemple)"},
    {"n": 4, "x": 80, "y": 126, "kind": "carburant", "name": "Station-service", "what": "Carburant", "dist": "6,1 km",
     "info": "Prix non vérifiés · diesel et propane (exemple)"},
]

BOULANCE = {
    "key": "boulance", "name": "BouLance", "kind": "Véhicule récréatif", "place": "Roberval · Lac-Saint-Jean",
    "mobile": True, "icon": "rv", "meIcon": "rv", "points": BOULANCE_POINTS,
    "geo": {"lat": 48.52, "lon": -72.23, "place": "Roberval, Lac-Saint-Jean"},
    "banner": {"img": "/media/env/boulance.webp", "pos": "62% 50%", "alt": "BouLance, le véhicule récréatif, au bord d’un lac au crépuscule"},
    "titles": {"voyage": "Voyage et entretien"},
    "subs": {
        "apercu": "L’essentiel de votre véhicule et de votre séjour.",
        "eclairage": "Des ambiances adaptées à chaque moment.",
        "confort": "Chaleur, air et météo du stationnement.",
        "energie": "Batteries, sources et consommation à bord.",
        "eau": "Réservoirs, eau chaude et points de service.",
        "securite": "Ouvertures, détection et alertes du secteur.",
        "internet": "Connexions et réseau à bord.",
        "equipements": "Les équipements du véhicule en un regard.",
        "voyage": "Le véhicule prêt pour la prochaine étape.",
        "modes": "Des routines claires et des effets visibles.",
    },
    "status": [["battery", "Batteries", "live", "ok"], ["drop", "Eau propre", "72 %", "water"], ["thermo", "Intérieur", "21 °C", "gold"]],
    "maps": {"lac": LAC},
    "wx": {
        "now": 3, "cond": "Ciel variable", "icon": "cloudsun", "feels": -2, "hi": 4, "lo": -6, "hum": 74, "dew": -1,
        "pop": 20, "wind": 18, "dir": "Nord-ouest", "gust": 32, "vis": 24, "hpa": 1021, "trend": "En hausse", "uv": 1, "cas": 2,
        "t24": [-3, -4, -4, -5, -5, -6, -6, -5, -3, -1, 1, 2, 3, 4, 4, 3, 2, 0, -1, -2, -2, -3, -3, -4],
        "sky": "dddddddpppddddppcccdddpp", "p24": "000000001111222211100000",
        "days": [["cloudsun", 4, -6, 20], ["snow", 1, -8, 60], ["cloud", -1, -9, 30], ["sun", 3, -5, 10], ["rain", 6, -1, 70]],
        "src": "Environnement Canada · exemple", "upd": 8,
    },
    "energy": {
        "unit": "Ah", "cap": 560, "nominal": "12,8 V", "chem": "LiFePO₄", "soc": 78, "v": "13,2 V", "reserve": 10, "load": 270,
        "packs": [{"name": "Batterie A", "cap": 280, "soc": 79, "v": 13.21, "a": 2.4, "t": 12.4, "cycles": 38, "hi": 3.304, "lo": 3.298},
                  {"name": "Batterie B", "cap": 280, "soc": 77, "v": 13.19, "a": 2.1, "t": 12.9, "cycles": 41, "hi": 3.301, "lo": 3.296}],
        "sources": [["solaire", "Solaire", "sun", "solar"], ["alt", "Alternateur", "alt", 0], ["secteur", "Secteur", "plug", 0]],
        "store": "Batteries", "loads": "Charges",
        "solar": {"peak": 500, "cloud": .35, "base": 230, "eve": 340},
        "live": True,
    },
    "s": {
        "apercu": [
            C("kpi", 3, icon="battery", label="Batteries", value="78 %", sub="Autonomie estimée : 18 h", bar=78, tone="bat", go="energie", live="soc"),
            C("kpi", 3, icon="drop", label="Eau propre", value="72 %", sub="108 sur 150 L · ≈ 4 jours au rythme actuel", bar=72, tone="water", go="eau"),
            C("kpi", 3, icon="thermo", label="Intérieur", value="21 °C", sub="Consigne 21 °C · fournaise au propane", subicon="fire", tone="heat", go="confort"),
            C("kpi", 3, icon="wifi", label="Internet", value="LTE active", dot="ok", sub="62 Go restants · Starlink en secours", subicon="satellite", tone="ok", go="internet"),
            C("conditions", 7, title="Conditions au stationnement"),
            C("lumieres", 5),
            C("upcoming", 7, title="Prochaines 48 heures", icon="snowflake", note="Nuit froide prévue : −6 °C vers 5 h.",
              text="Câble chauffant des conduites branché · consigne de nuit à 18 °C suggérée.", go="confort"),
            C("secsum", 5),
            C("around", 7, title="Autour de BouLance", map="lac", view=[40, 96, 200, 120],
              list=[["drop", "water", "Remplissage d’eau", "2 à proximité · 2,4 km"], ["dump", "ok", "Vidange", "3 à proximité · 1,1 km"],
                    ["fuel", "muted", "Carburant", "4 à proximité · 0,8 km"]],
              pins="points", btn=["Points de service", "eau:points"]),
            C("checklist", 5, id="depart", title="Préparer le départ", icon="clip",
              items=[["Coffres fermés", True, "capteur|Contacteurs des coffres · lu il y a 2 min"],
                     ["Objets rangés", True, "vous|Coché par Marie ce matin"],
                     ["Câble extérieur débranché", False, "capteur|Prise de quai · 30 A encore détectés"],
                     ["Marche rentrée", False, "capteur|Fin de course de la marche électrique"],
                     ["Propane fermé pour la route", False, "fab|Manuel du véhicule · avant chaque déplacement"]]),
            C("trip", 12, title="Mon voyage", name="Tour du Lac-Saint-Jean", next="Prochaine étape : Saint-Félicien", go="voyage",
              stages=["Alma", "Chambord", "Roberval", "Saint-Félicien", "Dolbeau-Mistassini", "Péribonka", "Alma"], at=2,
              done="146 km", left="110 km", eta="Départ dans 2 jours · 10 h"),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Thermostat", sub="Température et mode de confort", set=22, min=10, max=28, inside=21,
                  rows=[["home", "Température intérieure", "21 °C"], ["fire", "Chauffage", "Auto · fournaise au propane"],
                        ["snowflake", "Climatisation", "En veille"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température intérieure", "value": "21 °C", "state": "Stable", "tone": "ok", "c": "gold",
                     "pts": [20.4, 20.6, 20.9, 21.2, 21.0, 20.7, 20.8, 21.1, 21.3, 21.1, 21.0, 21.0], "min": 14, "max": 26},
                    {"icon": "drop", "title": "Humidité", "value": "45 %", "state": "Normale", "tone": "ok", "c": "blue",
                     "pts": [47, 46, 45, 44, 45, 47, 48, 46, 44, 45, 46, 45], "min": 20, "max": 80}]),
                C("ventilation", 3, speed=2, max=4, rows=[["fan", "Extraction", "Auto"]]),
                C("air", 3, co2=620, quality="Bonne qualité", rows=[["thermo", "Air", "21 °C"], ["drop", "Humidité", "45 %"], ["leaf", "Qualité", "Bonne"]]),
                C("outside", 3),
                C("cold", 3, title="Réfrigération", sub="Températures actuelles",
                  rows=[["fridge", "Réfrigérateur", "4 °C"], ["snowflake", "Congélateur", "−18 °C"]]),
            ]],
            ["meteo", "Météo", [C("wxnow", 7), C("days", 5), C("hourly", 12)]],
            ["soleil", "Soleil et lune", [C("sun", 8), C("moments", 4), C("sunpos", 7), C("moon", 5)]],
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["fridge", "Réfrigérateur", 90], ["fan", "Ventilation", 60], ["bulb", "Éclairage", 40], ["dots", "Autres", 80]]),
                C("chips", 12, items=[["inverter", "Onduleur", "Disponible", "ok"], ["solar", "Source active", "src", "gold"],
                                      ["bolt", "Charge batterie", "Selon la mesure", "live"]]),
            ]],
            ["batterie", "Batteries", [
                C("packs", 8),
                C("list", 4, icon="shield", title="Protection des batteries", sub="Système de gestion (BMS)", live="bms",
                  rows=[["check", "Charge autorisée", "Oui", "ok"], ["check", "Décharge autorisée", "Oui", "ok"],
                        ["sliders", "Équilibrage des cellules", "Au besoin", "muted"], ["bell", "Alarme", "Aucune", "ok"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="0,6 kWh", sub="Prévision · neige probable", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "500 Wc"], ["compass", "Orientation", "Toit · à plat"], ["sliders", "Inclinaison", "0°"],
                        ["pin", "Position", "Roberval · exemple"]]),
                C("solar", 9),
                C("fwx", 12, cond="Nuages variables", cloud=45, quality=2, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("tanks", 7, items=[["Eau propre", 72, 150, "clean"], ["Eaux grises", 34, 100, "grey"], ["Eaux noires", 18, 80, "black"]]),
                C("hotwater", 5, set=50, now=48, min=35, max=60, mode="Éco"),
                C("pump", 4, state="Disponible", flow="0,0 L/min", pressure="2,4 bar"),
                C("leaks", 4, sensors=[["tap", "Cuisine", "Sec"], ["shower", "Salle d’eau", "Sec"], ["heater", "Chauffe-eau", "Sec"]]),
                C("gauge", 4, icon="tank", title="Propane", sub="Niveau et estimation", pct=62, value="11,2 / 18 kg",
                  est="~ 9 jours", estsub="au rythme du chauffage actuel"),
                C("usage", 6, total=26, unit="L", seed=3),
                C("fill", 6, map="lac", point=1),
            ]],
            ["points", "Points de service", [
                C("levels", 12, items=[["Eau propre", 72, 150, "clean"], ["Eaux grises", 34, 100, "grey"], ["Eaux noires", 18, 80, "black"]]),
                C("points", 12, map="lac", view=[40, 96, 200, 120]),
                C("note", 12, icon="info", text="Source : exemple · données relevées il y a 2 jours. Vérifier les services et la potabilité sur place : aucune disponibilité n’est garantie."),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Ouvertures", sub="Portes, coffres, fenêtres et lanterneaux", env="boulance",
                  points=[O("Porte de la cellule", "Verrouillée", "ok", "Accès", 42, "Marie", lock=True, icon="door"),
                          O("Portière du conducteur", "Verrouillée", "ok", "Accès", 260, "James", lock=True, icon="car"),
                          O("Portière du passager", "Verrouillée", "ok", "Accès", 1440, "James", lock=True, icon="car"),
                          O("Coffre de rangement", "Fermé", "ok", "Soutes et coffres", 46, "Marie", lock=False, icon="box"),
                          O("Soute des réservoirs", "Fermée", "ok", "Soutes et coffres", 2900, "James", lock=False, icon="tank"),
                          O("Baie de la cuisine", "Entrouverte", "warn", "Fenêtres et toit", 190, "Aération pendant la cuisson", icon="window"),
                          O("Lanterneau du salon", "Fermé", "ok", "Fenêtres et toit", 600, "", icon="window")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs de sécurité à bord",
                  rows=[["co", "Monoxyde de carbone", "0 ppm", "ok"], ["flame", "Propane", "Normal", "ok"],
                        ["smoke", "Fumée", "Normal", "ok"], ["thermo", "Gel des conduites", "Surveillé", "ok"]]),
                C("cams", 4, items=[], empty="Aucune caméra n’est encore reliée à BouLance.",
                  emptysub="Les caméras de recul et d’entrée apparaîtront ici dès leur branchement. Aucune image n’est simulée."),
                C("events", 4, items=[[42, "Porte cellule fermée", "Accès sécurisé", "ok"], [46, "Coffre fermé", "Accès sécurisé", "ok"],
                                      [57, "Mode Nuit prévisualisé", "Aucun changement appliqué", "gold"],
                                      [190, "Baie cuisine entrouverte", "Aération pendant la cuisson", "warn"]]),
                C("toggle", 6, icon="shield", key="surv", title="Surveillance des ouvertures", sub="Surveillance active de tous les accès", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Alertes de sécurité sur vos appareils", on=True),
                C("note", 12, icon="info", text="Toute commande critique demande confirmation."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · secteur du VR", counts=[0, 0, 1, 0, 1],
                  alert={"level": "Avis", "title": "Bourrasques de neige", "text": "Visibilité réduite par endroits sur la route 169 demain matin · consulter le bulletin avant le départ.",
                         "src": "Environnement Canada · exemple", "ago": 8}),
                C("danger", 6, title="SOPFEU · Feux et restrictions", level=1, fires="0 feu dans un rayon de 25 km",
                  note="Saison de protection jusqu’au 15 novembre", src="SOPFEU · exemple", ago=13),
                C("zone", 6, title="Zone consultée · 25 km", map="lac", radius=25),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="LTE", icon="antenna", dbm=-78, bars=3, down=8.4, up=1.2, ping=42, loss="0,2 %"),
                C("meter", 4, icon="doc", title="Forfait LTE", used=38, total=100, unit="Go", note="62 Go disponibles · renouvellement le 1er décembre"),
                C("list", 4, icon="link", title="Autres connexions",
                  rows=[["satellite", "Starlink", "Secours prêt", "ok"], ["wifi", "Wi-Fi du camping", "Disponible", "ok"]]),
                C("devices", 7, total=6, groups=[["phone", 2, "téléphones"], ["laptop", 2, "ordinateurs"], ["tv", 1, "téléviseur"], ["cpu", 1, "Hub JARVIS"]]),
                C("prio", 5, items=[["antenna", "LTE"], ["satellite", "Starlink"], ["wifi", "Wi-Fi du camping"]]),
            ]],
            ["diagnostic", "Diagnostic", [
                C("sys", 4, icon="cpu", title="Processeur", value=18, spark=True, sub="Utilisation actuelle"),
                C("meter", 4, icon="mem", title="Mémoire", used=1.8, total=4, unit="Go", note="Utilisation de la mémoire"),
                C("meter", 4, icon="disk", title="Stockage", used=24, total=128, unit="Go", note="Utilisation du stockage"),
                C("list", 7, icon="db", title="État des services",
                  rows=[["cpu", "Hub JARVIS", "En ligne", "ok"], ["home", "Home Assistant", "En ligne", "ok"],
                        ["cloud", "Connecteur météo", "À jour", "ok"], ["battery", "Liaison des batteries", "live:link", "ok"],
                        ["road", "Source travaux routiers", "Indisponible", "warn"]]),
                C("list", 5, icon="clock", title="Dernier démarrage", rows=[["", "Dernier démarrage", "d:-3 08:00"], ["", "Dernière sauvegarde", "d:0 04:00"],
                                                                             ["", "Disponibilité", "3 j 14 h"]]),
                C("list", 12, icon="db", title="Fraîcheur des données",
                  rows=[["cloud", "Météo", "Dernière lecture : il y a 5 min", "ok"], ["wifi", "Réseau", "Dernière lecture : il y a 12 s", "ok"],
                        ["battery", "Batteries", "live:seen", "ok"], ["road", "Travaux routiers", "Aucune donnée récente · source indisponible", "warn"]]),
                C("actions", 12),
            ]],
        ],
        "equipements": [
            C("status", 12, moving=True, still="Véhicule à l’arrêt", ok="Commandes disponibles", lock="Commandes verrouillées en mouvement"),
            C("equip", 4, icon="awning", title="Auvent", sub="Protection extérieure", state="Rentré", tone="ok",
              rows=[["Vent", "18 km/h"]], act={"label": "Déployer", "icon": "play", "confirm": "Déployer l’auvent? Le vent actuel est de 18 km/h (limite : 30 km/h).",
                                                "done": "Déployé", "back": "Rentrer", "moving": True}, note="Confirmation requise"),
            C("equip", 4, icon="step", title="Marche", sub="Marche d’accès électrique", state="Rentrée", tone="ok",
              act={"label": "Sortir", "icon": "play", "confirm": "Sortir la marche d’accès?", "done": "Sortie", "back": "Rentrer", "moving": True},
              note="Véhicule à l’arrêt uniquement"),
            C("equip", 4, icon="jacks", title="Vérins", sub="Stabilisation du véhicule", state="Relevés", tone="ok",
              rows=[["Inclinaison", "+0,4°"]], act={"label": "Aperçu du nivellement", "icon": "list", "preview": True,
                                                    "text": "Aperçu : avant gauche +12 mm, avant droit +4 mm, arrière 0 mm. Aucun vérin ne bouge sans votre confirmation."}),
            C("equip", 4, icon="fridge", title="Réfrigérateur", sub="Réfrigérateur à compression", state="4 °C", tone="ok",
              rows=[["Mode", "Auto"], ["Tendance", "Température stable"]], spark=[4.2, 4.1, 3.9, 4.0, 4.2, 4.3, 4.1, 4.0, 3.9, 4.0, 4.1, 4.0]),
            C("equip", 4, icon="tv", title="Téléviseur", sub="Salon", state="Veille", tone="muted",
              rows=[["Source", "HDMI 1"]], toggle={"label": "Allumer", "on": "Allumé", "off": "Veille"}),
            C("list", 4, icon="door", title="Ouvertures techniques", sub="Soutes, trappes et accès",
              rows=[["box", "Soutes", "Fermées", "ok"], ["drop", "Trappe d’eau", "Fermée", "ok"], ["garage", "Garage arrière", "Fermé", "ok"]]),
            C("inspection", 12, title="Prochaine inspection", sub="Auvent et joints d’étanchéité", d=5, go="voyage:entretien"),
        ],
        "voyage": [
            ["voyage", "Voyage", [
                C("trip", 8, big=True, title="Voyage lié", name="Tour du Lac-Saint-Jean", next="Prochaine étape · Saint-Félicien",
                  dist="24 km", dur="25 min", map="lac", view=[20, 0, 360, 216], route=BOULANCE_TRIP),
                C("arrival", 4, place="Saint-Félicien", temp=2, icon="cloud", cond="Nuageux", wind="Vent 14 km/h"),
                C("list", 6, icon="warn", title="Travaux sur le trajet", sub="Québec 511 · 2 entraves d’exemple",
                  rows=[["cone", "Route 169 · circulation alternée", "6 km", "warn"], ["cone", "Accès local · détour temporaire", "11 km", "warn"]],
                  note="Disponibilité réelle à vérifier."),
                C("list", 6, icon="clip", title="Avant de partir",
                  rows=[["rv", "Gabarit du véhicule : 3,6 m · à vérifier", "", "", True], ["height", "Hauteurs et restrictions : à vérifier", "", "", True],
                        ["drop", "Eau, vidange et carburant : points à confirmer", "", "", True]]),
            ]],
            ["agenda", "Agenda", [
                C("agenda", 12, events=[[-1, "14:00", "15:00", "Arrivée au camping", "res"], [-1, "08:00", "", "Séjour au camping", "stay", 3],
                                       [2, "10:00", "11:00", "Départ", "res"], [3, "14:00", "15:00", "Inspection des joints", "maint"],
                                       [1, "09:00", "10:30", "Vidange et remplissage", "maint"]]),
                C("next", 4, icon="wrench", kick="Prochain événement", title="Vidange et remplissage", d=1, h="09:00"),
                C("next", 4, icon="clock", kick="Départ du camping", title="Vers Saint-Félicien", d=2, h="10:00", countdown=True),
                C("next", 4, icon="tent", kick="Réservation d’exemple", title="Camping du lac", text="Arrivée hier 14 h · départ dans 2 jours · 3 nuits"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, lists=[
                    {"k": "depart", "l": "Départ", "sub": "Les étapes essentielles avant de prendre la route.", "icon": "list",
                     "items": [["Fermer les fenêtres", "Baie de la cuisine encore entrouverte", True, "capteur|Contacteurs des fenêtres"],
                               ["Verrouiller les coffres", "Confirmé par capteur", True, "capteur|Contacteurs des coffres · lu il y a 2 min"],
                               ["Débrancher l’alimentation", "Prise de quai", True, "capteur|Prise de quai · courant mesuré"],
                               ["Ranger les objets mobiles", "Contrôler la cuisine et les surfaces.", False, "vous|Ajouté par Marie · votre liste"],
                               ["Vérifier les niveaux", "Eau, propane et batteries.", False, "jarvis|Niveaux lus par JARVIS · eau 72 %, propane 62 %"],
                               ["Fermer le propane", "Robinet de la bonbonne", False, "fab|Manuel du véhicule · avant chaque déplacement"],
                               ["Replier le marchepied", "Confirmé par capteur", False, "capteur|Fin de course de la marche électrique"]]},
                    {"k": "install", "l": "Installation", "sub": "À l’arrivée sur le site.", "icon": "tent",
                     "items": [["Mettre de niveau", "Vérins et cales", True, "capteur|Inclinomètre · +0,4° mesuré"],
                               ["Brancher l’alimentation", "Secteur 30 A", True, "capteur|Prise de quai · courant mesuré"],
                               ["Ouvrir l’eau", "Pompe ou raccord municipal", False, "fab|Manuel du véhicule · mise en service"],
                               ["Déployer l’auvent", "Si le vent le permet (limite 30 km/h)", False, "saison|Vent mesuré : 18 km/h"],
                               ["Allumer le chauffage", "Consigne 21 °C", False, "saison|Nuit à −6 °C prévue"]]},
                    {"k": "hiver", "l": "Froid", "sub": "Nuits sous zéro.", "icon": "snowflake",
                     "items": [["Câble chauffant des conduites", "Vérifier le branchement", True, "saison|Nuits sous 0 °C prévues · Environnement Canada (exemple)"],
                               ["Réservoirs à moins de 80 %", "Laisser de la place au gel", False, "capteur|Jauges des réservoirs · eaux grises 34 %"],
                               ["Antigel dans les siphons", "Eaux grises et noires", False, "fab|Manuel du véhicule · sous −5 °C"],
                               ["Couvercles des évents", "Ventilation sans infiltration", False, "jarvis|Recommandé : neige prévue jeudi"]]},
                    {"k": "courses", "l": "Courses", "sub": "Haltes et ravitaillement.", "icon": "cart",
                     "items": [["Propane", "Remplir une bonbonne", True, "jarvis|Propane à 62 % · ≈ 9 jours au rythme du chauffage"],
                               ["Eau potable", "Bidons de 20 L", True, "vous|Ajouté par vous"], ["Épicerie", "Roberval", True, "vous|Ajouté par vous"],
                               ["Bleuets séchés", "Spécialité de la région", True, "vous|Ajouté par Marie"], ["Lave-glace −40 °C", "", False, "saison|Neige et froid prévus"],
                               ["Piles AA", "", False, "jarvis|Pile faible : détecteur de fumée"], ["Bois d’allumage", "", False, "vous|Ajouté par vous"],
                               ["Café", "", False, "vous|Ajouté par Marie"], ["Fromage en grains", "", False, "vous|Ajouté par vous"]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("wheel", "Pneus d’hiver", "Pose avant la date limite",
                      regle_date("Règlement québécois : pneus d’hiver obligatoires du 1er décembre au 15 mars", "12-01")),
                    M("awning", "Inspection de l’auvent et des joints", "Atelier d’exemple · étanchéité du toit",
                      fab("Manuel du fabricant du véhicule · joints et scellants", "aux 12 mois", 365, -360)),
                    M("engine", "Vidange d’huile du moteur", "Huile et filtre",
                      compteur("Compteur kilométrique · lu par la prise de diagnostic du moteur", "aux 8 000 km", 6240, 8000, 80)),
                    M("battery", "Contrôle des batteries", "Serrage des bornes et équilibrage des cellules",
                      compteur("Recommandé par JARVIS selon l’usage réel des batteries", "aux 60 cycles", 41, 60, 0.9, "cycles", "jarvis")),
                    M("wheel", "Pression des pneus", "Pneu avant gauche à 74 psi · cible 80 psi",
                      src_fixe("capteur", "Capteurs de pression des pneus", 2, "Écart de 6 psi mesuré ce matin, à froid")),
                    M("drop", "Purge du chauffe-eau", "Avant les nuits sous −5 °C",
                      src_fixe("saison", "Météo du secteur et saison", 4, "Trois nuits sous −5 °C prévues cette semaine")),
                    M("fire", "Entretien de la fournaise", "Annuel · fait le 2 octobre",
                      fab("Manuel de la fournaise au propane", "aux 12 mois", 365, -37)),
                    M("co", "Détecteurs CO et propane", "Bouton d’essai et alarme sonore",
                      fab("Manuel des détecteurs", "test mensuel", 30, -32)),
                    M("clip", "Nettoyer les moustiquaires", "Baie de la cuisine et lanterneau",
                      src_fixe("vous", "Ajouté par Marie le 3 novembre", 12)),
                ]),
                C("next", 4, icon="wrench", kick="Prochain rendez-vous", title="Inspection de l’auvent et des joints", d=5, h="14:00"),
                C("next", 4, icon="wheel", kick="À planifier", title="Pose des pneus d’hiver", text="Le Québec exige les pneus d’hiver du 1er décembre au 15 mars."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="camping", items=[
                    {"k": "nuit", "icon": "moon", "label": "Nuit", "sub": "Repos et discrétion",
                     "fx": [["bulb", "Éclairage", "Ambiance Nuit douce", "Nuit douce", "light", "nuit-douce"], ["thermo", "Chauffage", "Consigne de nuit", "18 °C"],
                            ["shield", "Ouvertures", "Surveillance renforcée", "Activée", "crit"], ["bell", "Notifications", "Seulement l’essentiel", "Discrètes"]],
                     "autos": [["lock", "Vérifier les ouvertures à 23 h", "Rappel si une ouverture reste ouverte"]]},
                    {"k": "camping", "icon": "tent", "label": "Camping", "sub": "Confort sur site",
                     "fx": [["bulb", "Éclairage extérieur", "Allées, auvent, ambiance", "Heure dorée", "light", "heure-doree"],
                            ["thermo", "Confort intérieur", "Température cible", "21 °C"], ["wifi", "Connexion", "Réseau prioritaire", "Priorité LTE"]],
                     "autos": [["sun", "Éclairage au coucher du soleil", "Déclencheur : coucher du soleil"], ["battery", "Alerte batterie sous 25 %", "Déclencheur : franchissement du seuil"]]},
                    {"k": "route", "icon": "road", "label": "Route", "sub": "Conduite optimisée",
                     "fx": [["cube", "Équipements", "Auvent, marche et vérins verrouillés", "Verrouillés", "crit"], ["fridge", "Réfrigérateur", "Alimentation par l’alternateur", "12 V"],
                            ["bulb", "Éclairage intérieur", "Tout éteint", "Éteint"], ["wifi", "Connexion", "Bascule automatique", "LTE puis Starlink", "fail"]],
                     "autos": [["lock", "Verrouiller les commandes en mouvement", "Déclencheur : vitesse au-dessus de 5 km/h"]]},
                    {"k": "absence", "icon": "home", "label": "Absence", "sub": "Sécurité et économie",
                     "fx": [["thermo", "Chauffage", "Hors-gel", "10 °C"], ["shield", "Surveillance", "Ouvertures et mouvement", "Armée", "crit"],
                            ["bulb", "Éclairage", "Présence simulée le soir", "Activée", "light", "lecture"], ["fridge", "Réfrigérateur", "Maintenu", "4 °C"]],
                     "autos": [["bell", "Alerte d’ouverture", "Déclencheur : porte ou coffre ouvert"]]},
                    {"k": "hivernage", "icon": "snowflake", "label": "Hivernage", "sub": "Protection renforcée",
                     "fx": [["drop", "Eau", "Pompe coupée, conduites purgées", "Purgées", "crit"], ["thermo", "Chauffage", "Hors-gel minimal", "5 °C"],
                            ["battery", "Batteries", "Maintien et coupure des charges", "Stockage"], ["wifi", "Connexion", "Vérification quotidienne", "1 fois par jour"]],
                     "autos": [["thermo", "Alerte de gel", "Déclencheur : intérieur sous 3 °C"]]},
                ], scenarios=[["Arrivée sur site", "Active éclairage, confort et connexion"], ["Soirée", "Ambiance lumineuse et température réduite"],
                              ["Départ du site", "Extinction, vérification des fermetures"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["sun", "Éclairage au coucher du soleil", "Allume l’extérieur à 30 % au coucher du soleil", "Coucher du soleil", True],
                                     ["battery", "Alerte batterie sous 25 %", "Notification sur vos appareils", "Seuil de 25 %", True],
                                     ["snowflake", "Protection contre le gel", "Câble chauffant si l’extérieur passe sous −2 °C", "Température extérieure", True],
                                     ["lock", "Verrouillage en mouvement", "Bloque auvent, marche et vérins", "Vitesse au-dessus de 5 km/h", True],
                                     ["drop", "Eaux grises à 80 %", "Rappel de vidange", "Niveau du réservoir", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[4, "Système", "Mesure des batteries reçue"], [38, "Marie", "Mode Camping prévisualisé"],
                                        [53, "Alex", "Priorité réseau modifiée : LTE avant Starlink"], [68, "Système", "Vérification de départ terminée"],
                                        [190, "James", "Consigne de chauffage portée à 21 °C"], [900, "Système", "Protection contre le gel activée"]]),
            ]],
        ],
    },
}

# =============================================================================================
# Briques communes aux environnements fixes
# =============================================================================================

def T_meteo():
    return ["meteo", "Météo", [C("wxnow", 7), C("days", 5), C("hourly", 12)]]


def T_soleil():
    return ["soleil", "Soleil et lune", [C("sun", 8), C("moments", 4), C("sunpos", 7), C("moon", 5)]]


def T_diag(services, fresh, cpu=14, mem=(1.6, 4), disk=(31, 128), boot="d:-6 03:10", uptime="6 j 2 h"):
    return ["diagnostic", "Diagnostic", [
        C("sys", 4, icon="cpu", title="Processeur", value=cpu, spark=True, sub="Utilisation actuelle du Hub"),
        C("meter", 4, icon="mem", title="Mémoire", used=mem[0], total=mem[1], unit="Go", note="Utilisation de la mémoire"),
        C("meter", 4, icon="disk", title="Stockage", used=disk[0], total=disk[1], unit="Go", note="Historique local et sauvegardes"),
        C("list", 7, icon="db", title="État des services", rows=[["cpu", "Hub JARVIS", "En ligne", "ok"], ["home", "Home Assistant", "En ligne", "ok"]] + services),
        C("list", 5, icon="clock", title="Dernier démarrage", rows=[["", "Dernier démarrage", boot], ["", "Dernière sauvegarde", "d:0 04:00"], ["", "Disponibilité", uptime]]),
        C("list", 12, icon="db", title="Fraîcheur des données", rows=fresh),
        C("actions", 12),
    ]]


def wx(t24, sky, p24, days, **kw):
    assert len(t24) == 24 and len(sky) == 24 and len(p24) == 24
    base = {"hum": 70, "dew": -2, "wind": 12, "dir": "Ouest", "gust": 22, "vis": 30, "hpa": 1019, "trend": "Stable", "uv": 1, "cas": 2,
            "src": "Environnement Canada · exemple", "upd": 6, "icon": "cloudsun"}
    base.update(kw)
    base.update({"t24": t24, "sky": sky, "p24": p24, "days": days})
    return base


WX_SH = wx([0, -1, -1, -2, -2, -2, -1, 0, 2, 4, 6, 7, 8, 8, 7, 6, 4, 3, 2, 2, 1, 1, 0, 0],
           "ddddddppppcccccppddddddd", "000000000111111000000000",
           [["cloudsun", 8, -2, 10], ["rain", 9, 2, 70], ["cloud", 6, 0, 30], ["sun", 5, -3, 0], ["snow", 2, -4, 40]],
           hum=68, dew=-2, wind=12, dir="Ouest", gust=22, vis=30, hpa=1019, trend="Stable", uv=1, cas=3)


# =============================================================================================
# Résidence de prestige · Saint-Hyacinthe (piscine, spa, cellier, cinéma maison, garage chauffé 4 places)
# =============================================================================================

QUARTIER = {  # quartier stylisé au bord de la Yamaska (200 unités par kilomètre)
    "km": 200, "note": "Quartier illustratif",
    "water": [[[0, 22], [70, 30], [140, 50], [200, 90], [246, 140], [276, 196], [292, 240], [330, 240], [312, 186], [280, 128],
               [230, 74], [160, 30], [90, 8], [0, 0]]],
    "roads": [{"pts": [[0, 214], [120, 206], [250, 178], [400, 150]]},
              {"pts": [[40, 70], [40, 240]], "straight": True, "minor": True}, {"pts": [[100, 92], [100, 240]], "straight": True, "minor": True},
              {"pts": [[160, 116], [160, 240]], "straight": True, "minor": True}, {"pts": [[0, 120], [190, 120]], "straight": True, "minor": True},
              {"pts": [[0, 166], [214, 166]], "straight": True, "minor": True}, {"pts": [[300, 0], [330, 100], [360, 240]]},
              {"pts": [[340, 120], [400, 104]], "minor": True}],
    "blocks": [[52, 128, 14, 10], [72, 128, 14, 10], [52, 146, 14, 10], [72, 146, 14, 10], [112, 128, 14, 10], [112, 146, 14, 10],
               [132, 146, 16, 12, "hi"], [52, 176, 14, 10], [72, 176, 14, 10], [112, 176, 14, 10], [132, 176, 14, 10], [172, 176, 14, 10],
               [10, 176, 22, 50, "park"], [172, 128, 12, 10], [350, 160, 40, 40], [356, 40, 34, 22]],
    "labels": [[214, 80, "Rivière Yamaska", "water"], [22, 168, "Parc"]],
    "me": [140, 152],
}

MAISON = {
    "key": "maison", "name": "Résidence", "kind": "Résidence de prestige", "place": "Saint-Hyacinthe · bord de la Yamaska", "icon": "home", "meIcon": "home",
    "geo": {"lat": 45.63, "lon": -72.96, "place": "Saint-Hyacinthe, Montérégie"},
    "banner": {"img": "/media/solutions/environnements-intelligents.webp", "pos": "70% 42%", "alt": "Intérieur d’une résidence de prestige au crépuscule, vue sur l’eau"},
    "titles": {"voyage": "Entretien"}, "voyageIcon": "calendar",
    "subs": {"apercu": "L’essentiel de la résidence en un regard.", "confort": "Chauffage, cellier, air et météo du quartier.",
             "energie": "Solaire, batterie et réseau d’Hydro-Québec.", "eau": "Eau chaude, fuites et consommation.",
             "securite": "Portes, fenêtres, caméras et alertes du secteur.", "internet": "La fibre, le secours et tous les appareils.",
             "equipements": "Piscine, spa, cellier, cinéma et garage chauffé en un regard.", "voyage": "Rendez-vous, listes et entretien de la résidence.",
             "modes": "Matin, soirée, nuit : des routines claires."},
    "status": [["thermo", "Intérieur", "21 °C", "gold"], ["battery", "Batterie", "64 %", "ok"], ["shield", "Système", "Armé", "ok"]],
    "maps": {"quartier": QUARTIER},
    "wx": WX_SH,
    "energy": {"unit": "kWh", "cap": 27, "nominal": "51,2 V", "chem": "LiFePO₄", "soc": 64, "v": "52,1 V", "reserve": 20, "load": 2900, "battW": 0,
               "autonomy": "≈ 9 h · charges essentielles", "ringTitle": "Batteries domestiques", "packsTitle": "Batteries domestiques",
               "packs": [{"name": "Batterie domestique A", "cap": 13.5, "soc": 65, "v": 52.1, "a": 0.0, "t": 19.5, "cycles": 212, "hi": 3.268, "lo": 3.259},
                         {"name": "Batterie domestique B", "cap": 13.5, "soc": 63, "v": 52.0, "a": 0.0, "t": 19.8, "cycles": 209, "hi": 3.266, "lo": 3.258}],
               "sources": [["solaire", "Solaire · 14,4 kWc", "sun", "solar"], ["reseau", "Hydro-Québec", "hydro", "grid"]],
               "store": "Batteries", "loads": "Résidence",
               "solar": {"peak": 14400, "cloud": .3, "base": 2100, "eve": 4200, "tilt": 35, "morn": .6}},
    "s": {
        "apercu": [
            C("kpi", 3, icon="thermo", label="Intérieur", value="21 °C", sub="Humidité 41 %", subicon="drop", tone="gold", go="confort"),
            C("kpi", 3, icon="battery", label="Batteries domestiques", value="64 %", sub="27 kWh · ≈ 9 h en cas de panne", bar=64, tone="bat", go="energie"),
            C("kpi", 3, icon="shield", label="Système", value="Armé", dot="ok", sub="Mode nuit · 1 fenêtre entrouverte", subicon="window", tone="ok", go="securite"),
            C("kpi", 3, icon="wifi", label="Internet", value="Fibre", dot="ok", sub="58 appareils · LTE en secours", subicon="router", tone="ok", go="internet"),
            C("conditions", 7, title="Conditions au quartier"),
            C("lumieres", 5),
            C("around", 7, title="Autour de la résidence", map="quartier", listTitle="Dans le secteur",
              list=[["plug", "ok", "Bornes de recharge", "2 à moins de 1 km"], ["hydro", "ok", "Hydro-Québec", "Aucune panne dans le secteur"],
                    ["drop", "water", "Avis d’eau potable", "Aucun avis en vigueur"]],
              pinsList=[{"x": 205, "y": 186, "icon": "plug", "tone": "ok", "title": "Borne de recharge"}, {"x": 330, "y": 120, "icon": "plug", "tone": "ok", "title": "Borne de recharge"}],
              btn=["Alertes du secteur", "securite:alertes"]),
            C("checklist", 5, id="nuit", title="Avant la nuit", icon="moon",
              items=[["Portes verrouillées", True], ["Portes du garage fermées", True], ["Fenêtre de la chambre fermée", False], ["Couverture du spa posée", False]]),
            C("upcoming", 7, title="Prochaines 48 heures", icon="bolt", note="Pointe Hydro-Québec demain, de 6 h à 9 h.",
              text="Le préchauffage commencera à 4 h 30, la piscine et la recharge des voitures seront reportées.", go="energie:pointe"),
            C("next", 5, icon="wrench", kick="Prochain rendez-vous", title="Entretien de la thermopompe", d=3, h="10:00"),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Thermostat", sub="Rez-de-chaussée · thermopompe", set=21.5, min=15, max=26, inside=21,
                  rows=[["home", "Salon", "21 °C"], ["fire", "Chauffage", "Thermopompe · Auto"], ["snowflake", "Climatisation", "Hors saison"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température intérieure", "value": "21 °C", "state": "Stable", "tone": "ok", "c": "gold",
                     "pts": [20.6, 20.8, 21.0, 21.1, 21.0, 20.9, 21.0, 21.2, 21.1, 21.0, 21.0, 21.0], "min": 14, "max": 26},
                    {"icon": "drop", "title": "Humidité", "value": "41 %", "state": "Un peu sèche", "tone": "warn", "c": "blue",
                     "pts": [43, 43, 42, 42, 41, 41, 42, 41, 40, 41, 41, 41], "min": 20, "max": 80}]),
                C("ventilation", 3, speed=2, max=4, rows=[["fan", "Échangeur d’air", "Auto · 20 min/h"]]),
                C("air", 3, co2=540, quality="Bonne qualité", rows=[["thermo", "Air", "21 °C"], ["drop", "Humidité", "41 %"], ["leaf", "Qualité", "Bonne"]]),
                C("outside", 3),
                C("cold", 3, icon="thermo", title="Pièces", sub="Températures par pièce",
                  rows=[["home", "Suite principale", "19 °C"], ["fridge", "Cellier · 1 200 bouteilles", "13 °C · 68 %"], ["tv", "Cinéma maison", "20 °C"], ["garage", "Garage chauffé", "12 °C"]]),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["fire", "Géothermie et plancher radiant", 1400], ["pool", "Piscine · thermopompe", 620], ["heater", "Chauffe-eau", 420],
                        ["fridge", "Cellier et électroménagers", 310], ["bulb", "Éclairage", 150], ["evcharge", "Bornes (reportées)", 0]]),
                C("chips", 12, items=[["hydro", "Tarif", "Flex D · exemple", "gold"], ["solar", "Source active", "src", "gold"],
                                      ["evcharge", "Bornes de recharge", "Reportées à 21 h", "muted"]]),
            ]],
            ["pointe", "Tarif et pointes", [
                C("kpi", 3, icon="bolt", label="Prochaine pointe", value="Demain", sub="De 6 h à 9 h · Hydro-Québec", tone="gold"),
                C("kpi", 3, icon="clock", label="Période actuelle", value="Hors pointe", sub="Tarif Flex D · exemple", tone="ok"),
                C("kpi", 3, icon="leaf", label="Pointes réussies", value="4 / 4", sub="Depuis le 1er décembre dernier", tone="ok"),
                C("kpi", 3, icon="chart", label="Économie de la saison", value="38 $", sub="Estimation d’exemple", tone="gold"),
                C("list", 7, icon="list", title="Préparation de la prochaine pointe", sub="Rien n’est appliqué sans votre accord",
                  rows=[["thermo", "Préchauffage", "Dès 4 h 30 · +1 °C", "ok"], ["heater", "Chauffe-eau", "Coupé de 6 h à 9 h", "ok"],
                        ["evcharge", "Bornes de recharge", "Reportées après 9 h", "ok"], ["battery", "Batteries domestiques", "Réservées à la pointe", "ok"]]),
                C("list", 5, icon="hydro", title="Hydro-Québec", sub="Données d’exemple",
                  rows=[["clock", "Dernière pointe", "Mardi · 16 h – 20 h"], ["chart", "Réduction obtenue", "−2,4 kW"], ["bell", "Avis", "La veille, vers 15 h"]]),
            ]],
            ["batterie", "Batterie", [
                C("packs", 8),
                C("list", 4, icon="shield", title="Protection des batteries", sub="Système de gestion (BMS)",
                  rows=[["check", "Charge autorisée", "Oui", "ok"], ["check", "Décharge autorisée", "Oui", "ok"], ["sliders", "Réserve de panne", "20 %", "muted"], ["bell", "Alarme", "Aucune", "ok"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="8,2 kWh", sub="Prévision · pluie", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "14,4 kWc"], ["compass", "Orientation", "Sud-sud-ouest"], ["sliders", "Inclinaison", "35°"], ["pin", "Position", "Saint-Hyacinthe"]]),
                C("solar", 9), C("fwx", 12, cond="Passages nuageux", cloud=40, quality=3, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("hotwater", 5, set=60, now=58, min=50, max=65, mode="Normal · cycle antibactérien le dimanche"),
                C("leaks", 7, sensors=[["tap", "Cuisine", "Sec"], ["shower", "Suite principale", "Sec"], ["heater", "Chauffe-eau", "Sec"],
                                      ["pool", "Local technique de la piscine", "Sec"], ["fridge", "Cellier", "Sec"], ["pump", "Puisard", "Sec"]]),
                C("equip", 4, icon="valve", title="Vanne d’eau principale", sub="Coupure automatique en cas de fuite", state="Ouverte", tone="ok",
                  act={"label": "Fermer la vanne", "icon": "x", "confirm": "Fermer la vanne principale? Toute l’eau de la résidence sera coupée.", "done": "Fermée", "back": "Ouvrir la vanne"},
                  note="Confirmation requise"),
                C("pump", 4, icon="pump", title="Pompe de puisard", sub="Sous-sol", state="En attente", flow="0 cycle · 24 h", pressure="12 %",
                  l1="Cycles", l2="Niveau du puits"),
                C("usage", 4, total=640, unit="L", seed=5),
            ]],
            ["conso", "Consommation", [
                C("usage", 8, total=640, unit="L", seed=6, title="Eau utilisée · 24 dernières heures"),
                C("list", 4, icon="chart", title="Ce mois-ci", rows=[["drop", "Consommation", "15,2 m³"], ["chart", "Moyenne quotidienne", "507 L"],
                                                                      ["leaf", "Comparé à octobre", "−6 %", "ok"], ["shower", "Plus gros poste", "Douches · 38 %"]]),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Ouvertures", sub="Portes et fenêtres de la résidence", env="maison",
                  points=[O("Porte avant", "Verrouillée", "ok", "Portes", 95, "Marie", lock=True, icon="door"),
                          O("Porte-patio de la piscine", "Verrouillée", "ok", "Portes", 300, "Léa", lock=True, icon="door"),
                          O("Porte du cellier", "Verrouillée", "ok", "Portes", 640, "Marie", lock=True, icon="door"),
                          O("Porte du garage intérieure", "Fermée", "ok", "Portes", 52, "James", lock=False, icon="door"),
                          O("Portes du garage · 4 places", "Fermées", "ok", "Garage", 50, "James", lock=False, icon="garage"),
                          O("Fenêtre de la chambre", "Entrouverte", "warn", "Fenêtres", 180, "Aération de la chambre", icon="window"),
                          O("Fenêtres du salon", "Fermées", "ok", "Fenêtres", 4300, "", icon="window")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs de la résidence",
                  rows=[["smoke", "Fumée", "Normal", "ok"], ["co", "Monoxyde de carbone · garage", "0 ppm", "ok"], ["drop", "Dégât d’eau", "Aucun", "ok"],
                        ["fridge", "Cellier", "13 °C · 68 %", "ok"]]),
                C("cams", 4, items=[["/media/solutions/camera-front-entry-v1.webp", "Entrée avant", "Caméra de l’entrée avant", "Aucun événement"],
                                     ["/media/solutions/camera-driveway-garage-v1.webp", "Allée et garage", "Caméra de l’allée et du garage", "Portes fermées"],
                                     ["/media/solutions/camera-rear-terrace-v1.webp", "Terrasse", "Caméra de la terrasse arrière", "Accès fermé"],
                                     ["/media/solutions/camera-pool-spa-v1.webp", "Piscine et spa", "Caméra de la piscine", "Spa couvert"]]),
                C("events", 4, items=[[12, "Porte du garage fermée", "Par Alex · confirmé", "ok"], [35, "Mouvement · allée", "Livraison d’exemple", "gold"],
                                      [180, "Système armé · nuit", "Automatisation de 23 h", "ok"], [300, "Fenêtre de la chambre entrouverte", "Depuis 19 h 40", "warn"]]),
                C("toggle", 6, icon="shield", key="surv", title="Système d’alarme", sub="Armé · mode nuit", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Alertes sur vos appareils", on=True),
                C("note", 12, icon="info", text="Déverrouiller, désarmer ou ouvrir le garage demande toujours votre confirmation."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · Saint-Hyacinthe", counts=[0, 1, 0, 0, 0],
                  alert={"level": "Veille", "title": "Pluie verglaçante", "text": "Possible demain soir en Montérégie · prévoir du temps pour déglacer l’entrée et la voiture.",
                         "src": "Environnement Canada · exemple", "ago": 22}),
                C("list", 6, icon="hydro", title="Hydro-Québec · pannes et pointes", sub="Données d’exemple",
                  rows=[["hydro", "Pannes dans le secteur", "Aucune", "ok"], ["bolt", "Événement de pointe", "Demain 6 h – 9 h", "warn"],
                        ["clock", "Dernière panne", "12 octobre · 18 min", "muted"]]),
                C("list", 6, icon="leaf", title="Air et eau", sub="Données d’exemple",
                  rows=[["leaf", "Cote air santé", "3 · risque faible", "ok"], ["fire", "Feux à ciel ouvert", "Permis municipal requis", "muted"],
                        ["drop", "Avis d’eau potable", "Aucun", "ok"]]),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Fibre · 1 Gbit/s", icon="router", sig="Fibre optique", bars=4, down=86, up=21, ping=6, loss="0 %"),
                C("meter", 4, icon="chart", title="Données du mois", used=412, total=1000, unit="Go", note="Forfait illimité · indicateur seulement"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["antenna", "LTE de secours", "Prêt", "ok"], ["wifi", "Wi-Fi des invités", "3 appareils", "ok"]]),
                C("devices", 7, total=34, groups=[["phone", 6, "téléphones"], ["laptop", 4, "ordinateurs"], ["tv", 3, "téléviseurs"], ["cpu", 21, "objets connectés"]]),
                C("prio", 5, items=[["router", "Fibre"], ["antenna", "LTE de secours"]]),
            ]],
            T_diag([["radar", "Zigbee · 48 appareils", "En ligne", "ok"], ["camera", "Caméras · 4 flux", "En ligne", "ok"],
                    ["hydro", "Hydro-Québec · pointes", "À jour", "ok"], ["cloud", "Connecteur météo", "À jour", "ok"]],
                   [["cloud", "Météo", "Dernière lecture : il y a 6 min", "ok"], ["camera", "Caméras", "En direct · il y a 2 s", "ok"],
                    ["hydro", "Hydro-Québec", "Dernière lecture : il y a 1 h", "ok"], ["radar", "Capteurs Zigbee", "Dernière lecture : il y a 8 s", "ok"]],
                   cpu=11, mem=(2.1, 8), disk=(64, 256)),
        ],
        "equipements": [
            C("equip", 4, icon="pool", title="Piscine", sub="Creusée · chauffée · hivernée", state="Hivernée", tone="muted", rows=[["Toile", "Toile d’hiver posée"], ["Ouverture", "Mai"]],
              act={"label": "Voir l’état", "icon": "eye", "preview": True, "text": "Piscine hivernée le 4 octobre. Aucune commande n’est disponible avant l’ouverture."}),
            C("equip", 4, icon="spa", title="Spa", sub="Terrasse de la piscine · 7 places", state="38 °C", tone="ok", rows=[["Couvercle", "Fermé"], ["Filtration", "2 cycles par jour"]],
              act={"label": "Chauffer à 39 °C", "icon": "fire", "confirm": "Monter le spa à 39 °C? Délai estimé : 50 minutes.", "done": "En chauffe · 39 °C", "back": "Revenir à 38 °C"}),
            C("equip", 4, icon="fridge", title="Cellier", sub="1 200 bouteilles · climatisé", state="13 °C · 68 %", tone="ok", rows=[["Consigne", "13 °C · 65 à 70 %"], ["Porte", "Verrouillée"]],
              act={"label": "Voir l’historique", "icon": "eye", "preview": True, "text": "Température stable à ± 0,3 °C depuis 30 jours. Alerte si le cellier dépasse 15 °C ou 75 % d’humidité."}),
            C("equip", 4, icon="tv", title="Cinéma maison", sub="Salle de 10 places · son immersif", state="En veille", tone="muted", rows=[["Projecteur", "Prêt"], ["Ambiance", "Cinéma"]],
              act={"label": "Préparer une séance", "icon": "play", "confirm": "Préparer le cinéma? Stores fermés, éclairage tamisé, projecteur et son allumés.", "done": "Séance prête", "back": "Remettre en veille"}),
            C("equip", 4, icon="garage", title="Garage chauffé", sub="4 places · 12 °C", state="Portes fermées", tone="ok", rows=[["Véhicules", "3 sur 4 · un VUS sorti"], ["Détecteur de CO", "0 ppm"]],
              act={"label": "Ouvrir la porte 1", "icon": "up", "confirm": "Ouvrir la porte 1 du garage? Vérifiez que l’allée est dégagée.", "done": "Porte 1 ouverte", "back": "Fermer"}, note="Confirmation requise"),
            C("equip", 4, icon="evcharge", title="Bornes de recharge", sub="2 bornes · niveau 2 · 11 kW", state="Branchée · en attente", tone="gold",
              rows=[["Recharge", "Reportée à 21 h"], ["VUS électrique", "72 %"]],
              act={"label": "Recharger maintenant", "icon": "bolt", "confirm": "Démarrer la recharge maintenant? Elle coûtera plus cher qu’après 21 h.", "done": "En recharge · 7,2 kW", "back": "Reporter à 21 h"}),
            C("equip", 4, icon="lock", title="Serrure avant", sub="Porte d’entrée", state="Verrouillée", tone="ok",
              act={"label": "Déverrouiller", "icon": "unlock", "confirm": "Déverrouiller la porte avant? L’action sera inscrite au journal.", "done": "Déverrouillée", "back": "Verrouiller"},
              note="Action critique · inscrite au journal"),
            C("equip", 4, icon="blinds", title="Stores du salon", sub="Motorisés", state="Fermés", tone="ok",
              act={"label": "Ouvrir", "icon": "up", "confirm": "Ouvrir les stores du salon?", "done": "Ouverts", "back": "Fermer"}),
            C("equip", 4, icon="fireplace", title="Foyer du salon", sub="Au gaz · double face", state="Éteint", tone="muted",
              act={"label": "Allumer", "icon": "fire", "confirm": "Allumer le foyer du salon? Vérifiez que l’écran de verre est dégagé.", "done": "Allumé", "back": "Éteindre"}, note="Confirmation requise"),
            C("inspection", 12, title="Prochain entretien", sub="Thermopompe · nettoyage et vérification", d=3, h="10:00", go="voyage:entretien"),
        ],
        "voyage": [
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Événements (collectes, pointes)", l2="Entretien (rendez-vous, rappels)",
                  events=[[-3, "09:00", "10:00", "Changement des filtres", "maint"], [-1, "08:00", "09:00", "Collecte du recyclage", "event"],
                          [0, "10:00", "11:00", "Livraison de bois", "event"], [1, "08:00", "09:00", "Pointe Hydro-Québec", "peak"],
                          [3, "10:00", "12:00", "Entretien de la thermopompe", "maint"], [5, "13:00", "14:30", "Ramonage", "maint"]]),
                C("next", 4, icon="wrench", kick="Prochain rendez-vous", title="Entretien de la thermopompe", d=3, h="10:00"),
                C("next", 4, icon="bolt", kick="Prochaine pointe", title="Hydro-Québec · 6 h à 9 h", d=1, h="06:00", countdown=True),
                C("next", 4, icon="calendar", kick="Collecte", title="Recyclage", text="Chaque semaine · bac bleu au chemin la veille."),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes de la résidence", sub="Des listes simples, partagées avec la famille et le personnel.", lists=[
                    {"k": "partir", "l": "Avant de partir", "sub": "Fermer la résidence en confiance.", "icon": "home",
                     "items": [["Fermer les fenêtres", "Capteurs de fenêtres", False], ["Verrouiller les portes", "Confirmé par les serrures", True],
                               ["Baisser le chauffage", "Mode Absent", True], ["Couper l’eau de la laveuse", "Validation manuelle", False], ["Armer le système", "Confirmation requise", False]]},
                    {"k": "hiver", "l": "Hiver", "sub": "Avant les grands froids.", "icon": "snowflake",
                     "items": [["Pneus d’hiver posés", "Obligatoires dès le 1er décembre", True], ["Piscine hivernée", "", True], ["Robinets extérieurs purgés", "", False],
                               ["Contrat de déneigement", "Signé", True], ["Filtres de l’échangeur d’air", "Aux 3 mois", False]]},
                    {"k": "entretien", "l": "Entretien", "sub": "Les petites choses du mois.", "icon": "wrench",
                     "items": [["Tester les détecteurs", "Fumée et CO", True], ["Nettoyer les gouttières", "", True], ["Vérifier le puisard", "", False]]},
                    {"k": "courses", "l": "Courses", "sub": "Épicerie et quincaillerie.", "icon": "cart",
                     "items": [["Sel de déglaçage", "", False], ["Produits du spa", "Brome et équilibre", True], ["Piles 9 V", "Détecteurs", False], ["Café", "", True]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("fan", "Filtres de l’échangeur d’air", "Filtres lavables",
                      fab("Manuel de l’échangeur d’air", "aux 3 mois", 90, -92)),
                    M("fire", "Thermopompe", "Entretien annuel avant l’hiver",
                      fab("Manuel de la thermopompe · nettoyage des serpentins", "aux 12 mois", 365, -362)),
                    M("fireplace", "Ramonage de la cheminée", "Avant la saison de chauffage",
                      src_fixe("saison", "Saison de chauffage", 5, "Premières flambées prévues ce week-end")),
                    M("drop", "Robinets extérieurs", "Purger avant le gel",
                      src_fixe("saison", "Météo du quartier", 1, "Première nuit sous −2 °C prévue demain")),
                    M("smoke", "Détecteurs de fumée et CO", "Test mensuel",
                      fab("Manuel des détecteurs", "test mensuel", 30, -16)),
                    M("heater", "Chauffe-eau", "Vidange annuelle",
                      compteur("Recommandé par JARVIS selon la consommation d’eau chaude", "aux 60 000 L", 41800, 60000, 150, "L", "jarvis")),
                ]),
                C("next", 4, icon="wrench", kick="Prochain rendez-vous", title="Entretien de la thermopompe", d=3, h="10:00"),
                C("next", 4, icon="fan", kick="En retard", title="Filtres de l’échangeur d’air", text="Prévu il y a 2 jours · 10 minutes à faire soi-même."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="soiree", items=[
                    {"k": "matin", "icon": "sunrise", "label": "Matin", "sub": "Réveil en douceur",
                     "fx": [["bulb", "Éclairage", "Cuisine et salle de bain", "Lecture", "light", "lecture"], ["thermo", "Chauffage", "Retour au confort", "21 °C"],
                            ["blinds", "Stores", "Ouverture douce", "Ouverts"], ["shield", "Système", "Désarmement", "Désarmé", "crit"]],
                     "autos": [["clock", "Réveil à 6 h 45", "Les jours de semaine"]]},
                    {"k": "soiree", "icon": "fireplace", "label": "Soirée", "sub": "Salon et terrasse",
                     "fx": [["bulb", "Éclairage", "Salon et terrasse", "Heure dorée", "light", "heure-doree"], ["fireplace", "Foyer", "Allumage", "Allumé", "crit"],
                            ["thermo", "Chambres", "Baisse du chauffage", "19 °C"], ["blinds", "Stores", "Fermeture", "Fermés"]],
                     "autos": [["sun", "Au coucher du soleil", "Propose le mode Soirée"]]},
                    {"k": "nuit", "icon": "moon", "label": "Nuit", "sub": "Tout veille",
                     "fx": [["bulb", "Éclairage", "Veilleuses seulement", "Nuit douce", "light", "nuit-douce"], ["lock", "Portes", "Verrouillage", "Verrouillées", "crit"],
                            ["shield", "Système", "Armé · nuit", "Armé", "crit"], ["thermo", "Chauffage", "Nuit", "18 °C"]],
                     "autos": [["clock", "Tous les soirs à 23 h", "Propose le mode Nuit"]]},
                    {"k": "absent", "icon": "car", "label": "Absent", "sub": "Économie et sécurité",
                     "fx": [["thermo", "Chauffage", "Économie", "17 °C"], ["plug", "Prises non essentielles", "Coupées", "Coupées"],
                            ["shield", "Système", "Armé · absence", "Armé", "crit"], ["bulb", "Éclairage", "Tout éteint", "Éteint"]],
                     "autos": [["users", "Dernier départ détecté", "Propose le mode Absent"]]},
                    {"k": "vacances", "icon": "plane", "label": "Vacances", "sub": "Longue absence",
                     "fx": [["thermo", "Chauffage", "Hors-gel prolongé", "15 °C"], ["bulb", "Présence simulée", "Le soir, au hasard", "Activée", "light", "lecture"],
                            ["valve", "Vanne d’eau principale", "Fermée pendant l’absence", "Fermée", "crit fail"], ["heater", "Chauffe-eau", "Mode vacances", "Vacances"]],
                     "autos": [["calendar", "Retour planifié", "Remonte le chauffage 6 h avant"]]},
                ], scenarios=[["Arrivée à la maison", "Entrée éclairée, alarme désarmée après confirmation"], ["Cinéma", "Stores fermés, éclairage tamisé, projecteur et son allumés"],
                              ["Pointe Hydro-Québec", "Préchauffage, chauffe-eau coupé, borne reportée"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["sun", "Éclairage au coucher du soleil", "Entrée et allée à 40 %", "Coucher du soleil", True],
                                     ["bolt", "Préparation des pointes", "Préchauffage et délestage", "Avis d’Hydro-Québec", True],
                                     ["drop", "Fuite détectée", "Ferme la vanne principale et vous avertit", "Capteur de fuite", True],
                                     ["lock", "Verrouillage de nuit", "Vérifie les portes à 23 h", "Heure", True],
                                     ["evcharge", "Recharge de nuit", "Démarre à 21 h", "Heure et tarif", True], ["blinds", "Stores en été", "Ferme au soleil de l’après-midi", "Ensoleillement", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[12, "Alex", "Porte du garage fermée"], [65, "Système", "Mode Soirée proposé au coucher du soleil"],
                                        [70, "Camille", "Mode Soirée appliqué · 4 / 4 effets confirmés"], [180, "Système", "Système armé · mode nuit (hier)"],
                                        [600, "James", "Consigne de la chambre portée à 19 °C"]]),
            ]],
        ],
    },
}

# =============================================================================================
# Chalet d'architecte · Saint-Donat, Lac Archambault (résidence secondaire, hors saison)
# =============================================================================================

ARCHAMBAULT = {  # lac stylisé (20 unités par kilomètre)
    "km": 20,
    "water": [[[104, 214], [128, 186], [158, 160], [186, 128], [214, 98], [246, 70], [282, 48], [312, 40], [322, 56], [300, 78],
               [272, 100], [246, 130], [222, 160], [190, 190], [158, 214], [126, 226]],
              [[330, 196], [360, 180], [386, 196], [372, 222], [338, 222]], [[36, 64], [62, 52], [78, 70], [58, 88], [34, 82]]],
    "rivers": [[[312, 40], [330, 20], [344, 0]], [[104, 214], [80, 226], [56, 240]]],
    "roads": [{"pts": [[60, 240], [96, 220], [118, 200], [146, 176], [170, 150], [200, 112], [226, 84], [250, 56], [276, 28], [300, 0]], "n": "125", "at": [168, 140]},
              {"pts": [[118, 200], [190, 214], [260, 210], [330, 190], [400, 170]], "n": "329", "at": [300, 202]},
              {"pts": [[200, 112], [174, 104], [150, 108]], "minor": True}, {"pts": [[0, 150], [60, 166], [118, 200]], "minor": True}],
    "towns": [[110, 226, "Saint-Donat", "l"]],
    "labels": [[244, 104, "Lac Archambault", "water"], [356, 206, "Lac Ouareau", "water"], [176, 96, "Chemin du lac"]],
    "lake": None,
    "me": [168, 114],
}
del ARCHAMBAULT["lake"]

CHALET = {
    "key": "chalet", "name": "Chalet", "kind": "Chalet d’architecte", "place": "Saint-Donat · Lac Archambault", "icon": "tree", "meIcon": "home",
    "geo": {"lat": 46.32, "lon": -74.22, "place": "Saint-Donat, Lanaudière"},
    "banner": {"img": "/media/concept/jarvis-hero-architecture-v1.webp", "pos": "30% 50%", "alt": "Chalet d’architecte vitré au bord d’un lac, au crépuscule"},
    "titles": {"voyage": "Entretien"}, "voyageIcon": "calendar",
    "subs": {"apercu": "Le chalet surveillé, même à distance.", "confort": "Hors-gel, chauffage et météo du lac.",
             "energie": "Réseau, solaire, batterie et génératrice.", "eau": "Puits, eau chaude et hors-gel.",
             "securite": "Accès, détection et alertes de la forêt.", "internet": "Starlink, secours et capteurs.",
             "equipements": "Foyer, spa, sauna, génératrice et barrière.", "voyage": "Arrivées, listes et entretien du chalet.",
             "modes": "Arrivée, séjour, départ : le chalet suit."},
    "status": [["thermo", "Hors-gel", "12 °C", "water"], ["drop", "Puits", "2,8 bar", "ok"], ["shield", "Système", "Armé", "ok"]],
    "maps": {"lac": ARCHAMBAULT},
    "wx": wx([-5, -6, -6, -7, -7, -7, -6, -4, -2, 0, 2, 3, 3, 3, 2, 1, -1, -2, -3, -3, -4, -4, -5, -5],
             "ddddddppppcccccccwwccddd", "000000001112333355420000",
             [["cloud", 3, -7, 30], ["snow", 1, -9, 80], ["snow", -2, -11, 60], ["cloudsun", 2, -8, 10], ["sun", 4, -5, 0]],
             hum=82, dew=-5, wind=10, dir="Nord", gust=18, vis=16, hpa=1012, trend="En baisse", uv=1, cas=1),
    "energy": {"unit": "kWh", "cap": 10, "nominal": "51,2 V", "chem": "LiFePO₄", "soc": 92, "v": "53,0 V", "reserve": 30, "load": 650, "battW": 0,
               "autonomy": "≈ 15 h · hors-gel en cas de panne", "ringTitle": "Batterie de secours", "packsTitle": "Batterie de secours",
               "packs": [{"name": "Batterie de secours", "cap": 10, "soc": 92, "v": 53.0, "a": 0.0, "t": 11.2, "cycles": 64, "hi": 3.321, "lo": 3.314}],
               "sources": [["solaire", "Solaire · 3 kWc", "sun", "solar"], ["reseau", "Hydro-Québec", "hydro", "grid"], ["gen", "Génératrice", "gen", 0, "en veille"]],
               "store": "Batterie", "loads": "Chalet",
               "solar": {"peak": 3000, "cloud": .45, "base": 560, "eve": 640, "tilt": 40, "morn": .1}},
    "s": {
        "apercu": [
            C("kpi", 3, icon="thermo", label="Intérieur", value="12 °C", sub="Hors-gel · inoccupé", subicon="snowflake", tone="water", go="confort"),
            C("kpi", 3, icon="drop", label="Puits", value="2,8 bar", sub="Vanne fermée", subicon="valve", tone="water", go="eau"),
            C("kpi", 3, icon="battery", label="Batterie de secours", value="92 %", sub="Génératrice prête", bar=92, tone="bat", go="energie"),
            C("kpi", 3, icon="satellite", label="Internet", value="Starlink", dot="ok", sub="LTE en secours", subicon="antenna", tone="ok", go="internet"),
            C("conditions", 7, title="Conditions au lac"),
            C("lumieres", 5),
            C("around", 7, title="Autour du chalet", map="lac", view=[80, 50, 200, 120], listTitle="Dans le secteur",
              list=[["anchor", "water", "Quai", "Retiré pour l’hiver"], ["cart", "muted", "Dépanneur", "Village · 6 km"], ["fire", "ok", "SOPFEU", "Danger bas"]],
              pinsList=[{"x": 194, "y": 130, "icon": "anchor", "tone": "water", "title": "Quai"}],
              btn=["Alertes du secteur", "securite:alertes"]),
            C("checklist", 5, id="arrivee", title="Préparer l’arrivée", icon="clip",
              items=[["Déneigement du chemin", True], ["Chauffage remonté 6 h avant", False], ["Eau ouverte et purgée", False], ["Spa préchauffé", False]]),
            C("upcoming", 7, title="Prochaines 48 heures", icon="snowflake", note="Avertissement de neige : 15 à 20 cm.",
              text="Le chemin du lac sera déneigé demain matin. Arrivée prévue dans quelques jours.", go="securite:alertes"),
            C("next", 5, icon="home", kick="Prochaine arrivée", title="Séjour en famille", d=6, h="18:00", countdown=True),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Thermostat", sub="Séjour · plinthes électriques", set=12, min=5, max=24, inside=12,
                  rows=[["home", "Séjour", "12 °C"], ["fire", "Chauffage", "Hors-gel · plinthes"], ["fireplace", "Foyer", "Éteint"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température intérieure", "value": "12 °C", "state": "Hors-gel", "tone": "ok", "c": "gold",
                     "pts": [12.2, 12.1, 12.0, 11.9, 12.0, 12.1, 12.2, 12.1, 12.0, 12.0, 11.9, 12.0], "min": 4, "max": 24},
                    {"icon": "drop", "title": "Humidité", "value": "55 %", "state": "Normale", "tone": "ok", "c": "blue",
                     "pts": [56, 56, 55, 55, 54, 55, 55, 56, 55, 55, 55, 55], "min": 20, "max": 80}]),
                C("ventilation", 3, speed=1, max=4, rows=[["fan", "Échangeur d’air", "Minimum · absence"]]),
                C("air", 3, co2=430, quality="Excellente", rows=[["thermo", "Air", "12 °C"], ["drop", "Humidité", "55 %"], ["leaf", "Radon", "Faible"]]),
                C("outside", 3),
                C("cold", 3, icon="snowflake", title="Hors-gel", sub="Points sensibles",
                  rows=[["drop", "Vide sanitaire", "6 °C"], ["pump", "Pompe du puits", "5 °C"], ["heater", "Chauffe-eau", "49 °C"]]),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["heater", "Plinthes · hors-gel", 380], ["thermo", "Câble chauffant", 120], ["pump", "Pompe du puits", 60],
                        ["fridge", "Réfrigérateur", 50], ["wifi", "Réseau et capteurs", 40]]),
                C("chips", 12, items=[["gen", "Génératrice", "Prête · essai samedi", "ok"], ["solar", "Source active", "src", "gold"], ["hydro", "Réseau", "Disponible", "ok"]]),
            ]],
            ["secours", "Secours", [
                C("packs", 7),
                C("gauge", 5, icon="gen", title="Génératrice au propane", sub="12 kW · démarrage automatique", pct=68, value="Réservoir 68 %",
                  est="≈ 4 jours", estsub="de panne complète, chauffage compris"),
                C("list", 12, icon="gen", title="Génératrice", sub="Essai hebdomadaire automatique",
                  rows=[["clock", "Dernier essai", "d:-1 10:00", "ok"], ["gear", "Démarrage automatique", "Moins de 15 s après une panne", "ok"],
                        ["bolt", "Charges secourues", "Chauffage, puits, réfrigérateur, réseau", "ok"], ["wrench", "Prochain entretien", "Au printemps", "muted"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="0,4 kWh", sub="Prévision · neige", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "3 kWc"], ["compass", "Orientation", "Sud"], ["sliders", "Inclinaison", "40°"], ["pin", "Position", "Toit du garage"]]),
                C("solar", 9), C("fwx", 12, cond="Nuageux, neige le soir", cloud=70, quality=2, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("pump", 4, icon="pump", title="Pompe du puits", sub="Puits artésien", state="Disponible", flow="0 L/min", pressure="2,8 bar"),
                C("hotwater", 4, set=50, now=49, min=40, max=60, mode="Vacances · maintien"),
                C("equip", 4, icon="valve", title="Vanne d’eau principale", sub="Fermée pendant l’absence", state="Fermée", tone="muted",
                  act={"label": "Ouvrir la vanne", "icon": "drop", "confirm": "Ouvrir la vanne principale du chalet? Vérifiez d’abord l’absence de fuite au vide sanitaire.",
                       "done": "Ouverte", "back": "Fermer la vanne"}, note="Confirmation requise"),
                C("leaks", 6, sensors=[["tap", "Cuisine", "Sec"], ["shower", "Salle d’eau", "Sec"], ["heater", "Chauffe-eau", "Sec"], ["box", "Vide sanitaire", "Sec"]]),
                C("gauge", 6, icon="tank", title="Propane", sub="Foyer et génératrice", pct=68, value="Réservoir de 500 lb", est="≈ 7 semaines", estsub="au rythme actuel"),
            ]],
            ["puits", "Puits", [
                C("list", 7, icon="drop", title="Puits artésien", sub="Mesures d’exemple",
                  rows=[["drop", "Niveau statique", "18 m"], ["gauge", "Pression", "2,8 bar"], ["chart", "Débit de la pompe", "32 L/min"],
                        ["calendar", "Dernière analyse d’eau", "Juin · conforme", "ok"]]),
                C("usage", 5, total=12, unit="L", seed=9, title="Eau utilisée · 24 dernières heures"),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Ouvertures", sub="Accès du chalet", env="chalet",
                  points=[O("Porte principale", "Verrouillée", "ok", "Portes", 7200, "James", lock=True, icon="door"),
                          O("Mur de verre coulissant · façade du lac", "Verrouillé", "ok", "Portes", 7300, "James", lock=True, icon="door"),
                          O("Remise", "Verrouillée", "ok", "Dépendances", 7250, "James", lock=True, icon="box"),
                          O("Fenêtre de la mezzanine", "Fermée", "ok", "Fenêtres", 12000, "", icon="window"),
                          O("Trappe du vide sanitaire", "Fermée", "ok", "Dépendances", 40000, "", icon="box")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs du chalet",
                  rows=[["smoke", "Fumée", "Normal", "ok"], ["co", "Monoxyde de carbone", "0 ppm", "ok"], ["flame", "Propane", "Normal", "ok"],
                        ["thermo", "Gel", "Intérieur 12 °C", "ok"], ["eye", "Mouvement", "Aucun depuis 5 jours", "ok"]]),
                C("cams", 4, items=[], empty="La caméra du chemin n’est pas encore reliée.", emptysub="Elle apparaîtra ici dès son branchement. Aucune image n’est simulée."),
                C("events", 4, items=[[110, "Déneigeur détecté", "Chemin du lac · prévu", "gold"], [2900, "Mode Hors saison appliqué", "Par James · 4 / 4 confirmés", "ok"],
                                      [2920, "Vanne principale fermée", "Confirmée", "ok"], [2930, "Porte principale verrouillée", "Confirmée", "ok"]]),
                C("toggle", 6, icon="shield", key="surv", title="Système d’alarme", sub="Armé · absence", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Alertes sur vos appareils", on=True),
                C("note", 12, icon="info", text="Personne n’est sur place : toute commande à distance demande confirmation, et le foyer est limité à 2 heures."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · Saint-Donat", counts=[1, 0, 0, 1, 0],
                  alert={"level": "Avertissement", "title": "Neige", "text": "15 à 20 cm prévus d’ici demain matin · routes glissantes vers le chalet.",
                         "src": "Environnement Canada · exemple", "ago": 35, "tone": "err", "icon": "snowflake"}),
                C("danger", 6, title="SOPFEU · Feux et restrictions", level=1, fires="0 feu dans un rayon de 25 km", note="Saison de protection jusqu’au 15 novembre",
                  src="SOPFEU · exemple", ago=40),
                C("zone", 6, title="Zone consultée · 5 km", map="lac", radius=5),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Starlink", icon="satellite", sig="Ciel dégagé à 98 %", bars=4, down=118, up=14, ping=38, loss="0,4 %"),
                C("meter", 4, icon="chart", title="Données du mois", used=48, total=1000, unit="Go", note="Forfait résidentiel · sans limite"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["antenna", "LTE de secours", "Signal faible", "warn"]]),
                C("devices", 7, total=12, groups=[["cpu", 9, "capteurs et relais"], ["router", 1, "point d’accès"], ["tv", 1, "téléviseur"], ["thermo", 1, "thermostat"]]),
                C("prio", 5, items=[["satellite", "Starlink"], ["antenna", "LTE de secours"]]),
            ]],
            T_diag([["gen", "Génératrice", "En ligne", "ok"], ["radar", "Z-Wave · 14 appareils", "En ligne", "ok"], ["cloud", "Connecteur météo", "À jour", "ok"]],
                   [["cloud", "Météo", "Dernière lecture : il y a 9 min", "ok"], ["thermo", "Hors-gel", "Dernière lecture : il y a 30 s", "ok"],
                    ["gen", "Génératrice", "Dernier essai : hier", "ok"], ["camera", "Caméra du chemin", "Non reliée", "muted"]],
                   cpu=6, mem=(1.2, 4), disk=(18, 128), boot="d:-12 14:22", uptime="12 j 4 h"),
        ],
        "equipements": [
            C("equip", 4, icon="fireplace", title="Foyer au gaz", sub="Séjour", state="Éteint", tone="muted",
              act={"label": "Allumer", "icon": "fire", "confirm": "Allumer le foyer à distance? Personne n’est sur place : il s’éteindra seul après 2 heures.",
                   "done": "Allumé · 2 h", "back": "Éteindre"}, note="Action critique · limitée à 2 heures"),
            C("equip", 4, icon="fire", title="Sauna nordique", sub="Pavillon du quai", state="Arrêté", tone="muted", rows=[["Préchauffage", "45 minutes"]],
              act={"label": "Chauffer pour l’arrivée", "icon": "fire", "confirm": "Chauffer le sauna à 80 °C pour l’arrivée de vendredi, 18 h?", "done": "Planifié · vendredi 17 h 15", "back": "Annuler"}, note="Confirmation requise"),
            C("equip", 4, icon="spa", title="Spa", sub="Terrasse en porte-à-faux", state="Maintien · 30 °C", tone="muted",
              act={"label": "Préchauffer pour l’arrivée", "icon": "fire", "confirm": "Monter le spa à 38 °C pour l’arrivée prévue? Délai : environ 6 heures.",
                   "done": "Planifié · arrivée", "back": "Annuler le préchauffage"}),
            C("equip", 4, icon="snowflake", title="Hors-gel", sub="Chauffage minimal", state="Actif · 12 °C", tone="ok",
              rows=[["Vide sanitaire", "6 °C"], ["Câble chauffant", "Actif"]]),
            C("equip", 4, icon="gen", title="Génératrice", sub="Propane · 12 kW", state="Prête", tone="ok", rows=[["Dernier essai", "Hier · 15 min"]],
              act={"label": "Lancer un essai", "icon": "play", "confirm": "Lancer un essai de 10 minutes de la génératrice?", "done": "Essai réussi · 10 min", "back": "Lancer un essai"}),
            C("equip", 4, icon="fence", title="Barrière du chemin", sub="Entrée du terrain", state="Fermée", tone="ok",
              act={"label": "Ouvrir", "icon": "unlock", "confirm": "Ouvrir la barrière du chemin pour le déneigeur?", "done": "Ouverte", "back": "Fermer"}, note="Confirmation requise"),
            C("equip", 4, icon="pump", title="Pompe du puits", sub="Puits artésien", state="Disponible", tone="ok", rows=[["Pression", "2,8 bar"], ["Température", "5 °C"]]),
            C("inspection", 12, title="Prochain entretien", sub="Ramonage du foyer et de la cheminée", d=9, go="voyage:entretien"),
        ],
        "voyage": [
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Séjours et livraisons", l2="Entretien (rendez-vous, rappels)",
                  events=[[-1, "10:00", "10:30", "Essai de la génératrice", "maint"], [1, "08:00", "09:00", "Déneigement", "maint"],
                          [3, "13:00", "15:00", "Livraison de propane", "event"], [6, "16:00", "18:00", "Arrivée en famille", "stay", 2]]),
                C("next", 4, icon="home", kick="Prochaine arrivée", title="Séjour en famille", d=6, h="18:00", countdown=True),
                C("next", 4, icon="tank", kick="Livraison", title="Propane", d=3, h="13:00"),
                C("next", 4, icon="snowflake", kick="Déneigement", title="Chemin du lac", d=1, h="08:00"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes du chalet", sub="Arriver et repartir sans rien oublier.", lists=[
                    {"k": "arrivee", "l": "Arrivée", "sub": "Remettre le chalet en marche.", "icon": "home",
                     "items": [["Ouvrir la vanne principale", "Confirmation requise", False], ["Remonter le chauffage", "21 °C", False],
                               ["Allumer le chauffe-eau", "Mode normal", False], ["Désarmer le système", "Confirmation requise", False]]},
                    {"k": "depart", "l": "Départ", "sub": "Fermer pour la semaine.", "icon": "lock",
                     "items": [["Fermer la vanne principale", "", True], ["Hors-gel à 12 °C", "", True], ["Vider le réfrigérateur", "", True], ["Armer le système", "", True]]},
                    {"k": "hiver", "l": "Hiver", "sub": "Avant les grands froids.", "icon": "snowflake",
                     "items": [["Antigel dans les siphons", "", True], ["Quai retiré", "", True], ["Contrat de déneigement", "", True], ["Pneus d’hiver", "", True], ["Ramonage", "", False]]},
                    {"k": "courses", "l": "Courses", "sub": "Au village.", "icon": "cart",
                     "items": [["Bois d’allumage", "", False], ["Sel", "", False], ["Café", "", False]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("fireplace", "Ramonage du foyer", "Avant l’usage de la saison",
                      fab("Manuel du foyer au gaz", "aux 12 mois", 365, -356)),
                    M("gen", "Génératrice", "Entretien annuel",
                      compteur("Compteur d’heures de la génératrice", "aux 100 heures", 52, 100, 0.3, "h")),
                    M("drop", "Analyse de l’eau du puits", "Bactéries et nitrates",
                      fab("Recommandation pour les puits privés", "aux 12 mois", 365, -145)),
                    M("smoke", "Détecteurs", "Test mensuel",
                      fab("Manuel des détecteurs", "test mensuel", 30, -34)),
                    M("tank", "Inspection du réservoir de propane", "Fournisseur",
                      src_fixe("vous", "Ajouté par James · rendez-vous du fournisseur", 40)),
                ]),
                C("next", 4, icon="fireplace", kick="Prochain rendez-vous", title="Ramonage du foyer", d=9, h="10:00"),
                C("next", 4, icon="smoke", kick="En retard", title="Test des détecteurs", text="À faire à la prochaine arrivée."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="horssaison", items=[
                    {"k": "arrivee", "icon": "home", "label": "Arrivée", "sub": "Préparer le chalet",
                     "fx": [["thermo", "Chauffage", "Remonter 6 h avant l’arrivée", "21 °C"], ["valve", "Vanne d’eau principale", "Ouverture", "Ouverte", "crit"],
                            ["heater", "Chauffe-eau", "Remise en marche", "55 °C"], ["bulb", "Éclairage", "Allée et entrée", "Heure dorée", "light", "heure-doree"],
                            ["spa", "Spa", "Préchauffage", "38 °C", "fail"]],
                     "autos": [["calendar", "Arrivée inscrite à l’agenda", "Lance le mode 6 h avant"]]},
                    {"k": "sejour", "icon": "fireplace", "label": "Séjour", "sub": "Confort sur place",
                     "fx": [["thermo", "Chauffage", "Confort", "21 °C"], ["shield", "Système", "Désarmé · présence", "Désarmé", "crit"],
                            ["bulb", "Éclairage", "Soirée au coin du feu", "Lecture", "light", "lecture"], ["wifi", "Starlink", "Priorité aux appels vidéo", "Activée"]],
                     "autos": [["sun", "Coucher du soleil", "Éclairage de la terrasse"]]},
                    {"k": "depart", "icon": "lock", "label": "Départ", "sub": "Fermer en confiance",
                     "fx": [["valve", "Vanne d’eau principale", "Fermeture", "Fermée", "crit"], ["thermo", "Chauffage", "Hors-gel", "12 °C"],
                            ["bulb", "Éclairage", "Tout éteint", "Éteint"], ["shield", "Système", "Armé · absence", "Armé", "crit"]],
                     "autos": [["users", "Dernier départ", "Propose le mode Départ"]]},
                    {"k": "horssaison", "icon": "snowflake", "label": "Hors saison", "sub": "Surveillance seulement",
                     "fx": [["thermo", "Chauffage", "Hors-gel", "12 °C"], ["shield", "Système", "Armé", "Armé", "crit"],
                            ["pump", "Pompe du puits", "Coupée", "Coupée"], ["wifi", "Connexion", "Vérification quotidienne", "1 fois par jour"]],
                     "autos": [["thermo", "Alerte de gel", "Intérieur sous 5 °C"], ["hydro", "Panne de courant", "Génératrice et avis"]]},
                ], scenarios=[["Arrivée tardive", "Allée éclairée jusqu’à minuit"], ["Tempête", "Batterie réservée au hors-gel"], ["Location", "Codes d’accès temporaires"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["thermo", "Alerte de gel", "Vous avertit si l’intérieur passe sous 5 °C", "Température intérieure", True],
                                     ["hydro", "Panne de courant", "Démarre la génératrice et vous avertit", "Perte du réseau", True],
                                     ["drop", "Fuite au vide sanitaire", "Ferme la vanne et vous avertit", "Capteur de fuite", True],
                                     ["calendar", "Arrivée planifiée", "Lance le mode Arrivée 6 h avant", "Agenda partagé", True],
                                     ["snowflake", "Déneigement", "Ouvre la barrière au passage du déneigeur", "Plaque reconnue", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[110, "Système", "Déneigeur détecté au chemin"], [1440, "Système", "Essai de la génératrice réussi · 15 min"],
                                        [2900, "James", "Mode Hors saison appliqué · 4 / 4 effets confirmés"], [2930, "James", "Porte principale verrouillée"]]),
            ]],
        ],
    },
}


# =============================================================================================
# Bureau · entreprise au centre-ville de Saint-Hyacinthe
# =============================================================================================

CENTRE = {
    "km": 200, "note": "Centre-ville illustratif",
    "water": [[[0, 200], [80, 190], [170, 196], [260, 214], [330, 232], [400, 236], [400, 240], [0, 240]]],
    "roads": [{"pts": [[0, 60], [400, 60]], "straight": True}, {"pts": [[0, 130], [400, 130]], "straight": True},
              {"pts": [[90, 0], [90, 196]], "straight": True}, {"pts": [[210, 0], [210, 200]], "straight": True}, {"pts": [[320, 0], [320, 226]], "straight": True},
              {"pts": [[0, 95], [400, 95]], "straight": True, "minor": True}, {"pts": [[150, 0], [150, 196]], "straight": True, "minor": True},
              {"pts": [[265, 0], [265, 210]], "straight": True, "minor": True}, {"pts": [[0, 165], [400, 165]], "straight": True, "minor": True}],
    "blocks": [[10, 10, 70, 40], [100, 10, 40, 40], [160, 10, 40, 40], [220, 10, 36, 40], [276, 10, 36, 40], [330, 10, 60, 40],
               [10, 70, 70, 18], [100, 70, 40, 18], [160, 70, 40, 18], [220, 70, 36, 18], [276, 70, 36, 18], [330, 70, 60, 18],
               [10, 104, 70, 18], [100, 104, 40, 18], [160, 104, 40, 18, "hi"], [220, 104, 36, 18, "park"], [276, 104, 36, 18], [330, 104, 60, 18],
               [10, 140, 70, 18], [100, 140, 40, 18, "park"], [160, 140, 40, 18], [220, 140, 36, 18], [276, 140, 36, 18], [330, 140, 60, 18]],
    "labels": [[180, 222, "Rivière Yamaska", "water"], [238, 99, "P"], [120, 135, "P"]],
    "me": [180, 113],
}

ENTREPRISE = {
    "key": "entreprise", "name": "Bureau", "kind": "Entreprise · bureaux", "place": "Saint-Hyacinthe · centre-ville", "icon": "brief", "meIcon": "city",
    "geo": {"lat": 45.626, "lon": -72.957, "place": "Saint-Hyacinthe, centre-ville"},
    "banner": {"img": "/media/solutions/jarvis-enterprise-operations-v1.webp", "pos": "50% 50%", "alt": "Bureaux de direction au crépuscule, vue sur la ville"},
    "titles": {"voyage": "Entretien"}, "voyageIcon": "calendar",
    "subs": {"apercu": "Les bureaux, les accès et l’énergie en un regard.", "confort": "Ventilation, CO₂ et températures des zones.",
             "energie": "Puissance appelée, pointes et solaire.", "eau": "Eau chaude, fuites et gicleurs.",
             "securite": "Accès, badges, caméras et alertes.", "internet": "Lien dédié, secours et réseaux séparés.",
             "equipements": "Portes, salles, CVC et affichage.", "voyage": "Rendez-vous, inspections et listes de l’équipe.",
             "modes": "Ouverture, fermeture, fin de semaine."},
    "status": [["users", "Occupation", "14 / 22", "gold"], ["bolt", "Puissance", "42 kW", "ok"], ["key", "Accès", "Contrôlés", "ok"]],
    "maps": {"centre": CENTRE},
    "wx": WX_SH,
    "energy": {"unit": "kWh", "cap": 20, "nominal": "400 V", "chem": "LiFePO₄", "soc": 100, "v": "408 V", "reserve": 50, "load": 42000, "battW": 0,
               "autonomy": "≈ 25 min · serveurs et réseau", "ringTitle": "Alimentation sans coupure", "packsTitle": "Alimentation sans coupure",
               "packs": [{"name": "Module A", "cap": 10, "soc": 100, "v": 204.1, "a": 0.0, "t": 21.0, "cycles": 9, "hi": 3.402, "lo": 3.398},
                         {"name": "Module B", "cap": 10, "soc": 100, "v": 204.0, "a": 0.0, "t": 21.3, "cycles": 9, "hi": 3.401, "lo": 3.396}],
               "sources": [["solaire", "Solaire · 30 kWc", "sun", "solar"], ["reseau", "Hydro-Québec · tarif M", "hydro", "grid"]],
               "store": "Onduleur", "loads": "Bâtiment",
               "solar": {"peak": 30000, "cloud": .3, "base": 9000, "day": 41000, "eve": 12000, "tilt": 10, "morn": 0}},
    "s": {
        "apercu": [
            C("kpi", 3, icon="users", label="Occupation", value="14 / 22", sub="Salle de réunion libre", subicon="clock", tone="gold", go="equipements"),
            C("kpi", 3, icon="bolt", label="Puissance appelée", value="42 kW", sub="Pointe du mois : 58 kW", bar=72, tone="gold", go="energie:pointe"),
            C("kpi", 3, icon="thermo", label="Zone bureaux", value="21,5 °C", sub="CO₂ 780 ppm", subicon="wind", tone="gold", go="confort"),
            C("kpi", 3, icon="router", label="Internet", value="Fibre", dot="ok", sub="Dédiée · 86 appareils", subicon="link", tone="ok", go="internet"),
            C("conditions", 7, title="Conditions au centre-ville"),
            C("lumieres", 5),
            C("around", 7, title="Autour du bureau", map="centre", listTitle="Aujourd’hui",
              list=[["parking", "water", "Stationnement", "18 / 40 places libres"], ["truck", "gold", "Livraisons attendues", "2 · quai arrière"],
                    ["users", "ok", "Visiteurs", "3 inscrits"]],
              pinsList=[{"x": 238, "y": 113, "icon": "parking", "tone": "water", "title": "Stationnement"}, {"x": 120, "y": 149, "icon": "parking", "tone": "water", "title": "Stationnement"}],
              btn=["Accès et caméras", "securite"]),
            C("checklist", 5, id="ouverture", title="Ouverture des bureaux", icon="clip",
              items=[["Portes en mode horaire", True], ["CVC en mode occupé", True], ["Accueil allumé", True], ["Salle de réunion préparée", False]]),
            C("upcoming", 7, title="Prochaines 48 heures", icon="bolt", note="Événement de pointe demain, de 7 h à 9 h.",
              text="Le plan de délestage réduira les bornes et préchauffera le bâtiment dès 6 h.", go="energie:pointe"),
            C("next", 5, icon="wrench", kick="Prochaine inspection", title="Gicleurs · inspection annuelle", d=5, h="09:00"),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Zone bureaux", sub="CVC · mode occupé", set=21.5, min=16, max=26, inside=21.5,
                  rows=[["users", "Occupation", "14 personnes"], ["fan", "CVC", "Occupé · Auto"], ["snowflake", "Climatisation", "Hors saison"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température moyenne", "value": "21,5 °C", "state": "Stable", "tone": "ok", "c": "gold",
                     "pts": [20.8, 21.0, 21.3, 21.5, 21.6, 21.5, 21.4, 21.5, 21.6, 21.5, 21.5, 21.5], "min": 14, "max": 26},
                    {"icon": "wind", "title": "CO₂ moyen", "value": "780 ppm", "state": "Correct", "tone": "ok", "c": "blue",
                     "pts": [520, 560, 640, 710, 760, 800, 820, 790, 770, 780, 790, 780], "min": 400, "max": 1400}]),
                C("ventilation", 3, speed=3, max=4, rows=[["fan", "Air neuf", "Selon le CO₂"]]),
                C("air", 3, co2=780, quality="Correcte", rows=[["thermo", "Air", "21,5 °C"], ["drop", "Humidité", "34 %"], ["users", "Personnes", "14"]]),
                C("outside", 3),
                C("cold", 3, icon="thermo", title="Salles", sub="Températures actuelles",
                  rows=[["cpu", "Salle des serveurs", "20 °C"], ["users", "Salle de réunion", "22 °C"], ["fridge", "Cuisinette", "4 °C"]]),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["fan", "CVC", 18000], ["evcharge", "Bornes (4)", 11000], ["laptop", "Postes de travail", 5400], ["cpu", "Serveurs et réseau", 4200],
                        ["bulb", "Éclairage", 3100]]),
                C("chips", 12, items=[["hydro", "Tarif", "M · puissance", "gold"], ["bolt", "Pointe du mois", "58 kW", "warn"], ["evcharge", "Bornes", "Délestage prêt", "ok"]]),
            ]],
            ["pointe", "Pointe et tarif", [
                C("kpi", 3, icon="bolt", label="Puissance appelée", value="42 kW", sub="Maintenant · exemple", bar=72, tone="gold"),
                C("kpi", 3, icon="chart", label="Pointe du mois", value="58 kW", sub="Le 21 octobre · 8 h 45", tone="gold"),
                C("kpi", 3, icon="calendar", label="Prochain événement", value="Demain", sub="De 7 h à 9 h · Hydro-Québec", tone="gold"),
                C("kpi", 3, icon="leaf", label="Objectif de pointe", value="≤ 50 kW", sub="Plan de délestage prêt", tone="ok"),
                C("list", 7, icon="list", title="Plan de délestage", sub="Appliqué seulement pendant l’événement, après votre accord",
                  rows=[["evcharge", "Bornes de recharge", "Réduites à 3,6 kW", "ok"], ["fan", "CVC", "Préchauffage à 6 h, puis −1 °C", "ok"],
                        ["heater", "Chauffe-eau", "Coupé de 7 h à 9 h", "ok"], ["bulb", "Aires communes", "Éclairage à 70 %", "ok"]]),
                C("list", 5, icon="hydro", title="Facturation d’exemple", sub="Tarif M · données fictives",
                  rows=[["chart", "Consommation du mois", "6 840 kWh"], ["bolt", "Puissance facturée", "58 kW"], ["leaf", "Production solaire", "9 % des besoins"]]),
            ]],
            ["batterie", "Alimentation sans coupure", [
                C("packs", 8),
                C("list", 4, icon="shield", title="Protection", sub="Onduleur et batteries",
                  rows=[["check", "Mode", "En ligne", "ok"], ["cpu", "Charges protégées", "Serveurs, réseau, accès", "ok"], ["clock", "Dernier test", "d:-12 06:00", "ok"], ["bell", "Alarme", "Aucune", "ok"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="31 kWh", sub="Prévision · pluie", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "30 kWc"], ["compass", "Orientation", "Toit plat · sud"], ["sliders", "Inclinaison", "10°"], ["pin", "Position", "Toit du bâtiment"]]),
                C("solar", 9), C("fwx", 12, cond="Passages nuageux", cloud=40, quality=3, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("hotwater", 5, set=60, now=59, min=55, max=65, mode="Normal · anti-légionellose"),
                C("leaks", 7, sensors=[["tap", "Cuisinette", "Sec"], ["shower", "Toilettes", "Sec"], ["heater", "Salle mécanique", "Sec"], ["cpu", "Salle des serveurs", "Sec"]]),
                C("pump", 4, icon="shield", title="Gicleurs", sub="Réseau incendie", state="Sous pression", flow="Ouverte", pressure="5,2 bar", l1="Vanne de section", l2="Pression"),
                C("equip", 4, icon="valve", title="Vanne d’eau principale", sub="Coupure en cas de fuite", state="Ouverte", tone="ok",
                  act={"label": "Fermer la vanne", "icon": "x", "confirm": "Fermer la vanne principale? Les toilettes et la cuisinette n’auront plus d’eau. Les gicleurs restent alimentés.",
                       "done": "Fermée", "back": "Ouvrir la vanne"}, note="Confirmation requise"),
                C("usage", 4, total=1840, unit="L", seed=11),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Accès", sub="Portes et zones protégées", env="entreprise",
                  points=[O("Entrée principale", "Ouverte · horaire", "ok", "Entrées", 3, "Badge de l’accueil", lock=True, icon="door"),
                          O("Porte de service", "Verrouillée", "ok", "Entrées", 140, "Livreur accompagné", lock=True, icon="door"),
                          O("Issue de secours", "Fermée", "ok", "Entrées", 20000, "", lock=False, icon="door"),
                          O("Salle des serveurs", "Verrouillée · badge requis", "ok", "Zones protégées", 75, "Alex", lock=True, icon="cpu"),
                          O("Salle de réunion", "Libre", "ok", "Zones protégées", 30, "Équipe des ventes", lock=False, icon="users")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs du bâtiment",
                  rows=[["smoke", "Fumée", "Normal", "ok"], ["co", "Monoxyde de carbone", "0 ppm", "ok"], ["drop", "Inondation · serveurs", "Sec", "ok"],
                        ["eye", "Intrusion", "Désarmée · heures d’ouverture", "muted"]]),
                C("cams", 4, items=[["/media/solutions/security-enterprise-delivery-v1.webp", "Quai de livraison", "Caméra du quai de livraison", "Livraison attendue"],
                                     ["/media/solutions/security-enterprise-parking-v1.webp", "Stationnement", "Caméra du stationnement", "18 places libres"]]),
                C("events", 4, items=[[6, "Badge accepté · porte de service", "Livreur d’exemple · accompagné", "ok"], [48, "Visiteur inscrit", "Accueil", "gold"],
                                      [95, "Mode Ouverture appliqué", "Automatique · 7 h 30", "ok"], [610, "Alarme de la porte de service", "Fausse alerte · vérifiée par Sophie", "warn"]]),
                C("toggle", 6, icon="shield", key="surv", title="Contrôle d’accès", sub="Badges et horaires actifs", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Responsable de garde", on=True),
                C("note", 12, icon="info", text="Verrouiller, déverrouiller ou désactiver un badge demande confirmation et laisse une trace."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · Saint-Hyacinthe", counts=[0, 1, 0, 0, 0],
                  alert={"level": "Veille", "title": "Pluie verglaçante", "text": "Possible demain soir · prévoir l’épandage d’abrasif à l’entrée et au stationnement.",
                         "src": "Environnement Canada · exemple", "ago": 22}),
                C("list", 6, icon="hydro", title="Hydro-Québec", sub="Données d’exemple",
                  rows=[["hydro", "Pannes dans le secteur", "Aucune", "ok"], ["bolt", "Événement de pointe", "Demain 7 h – 9 h", "warn"]]),
                C("list", 6, icon="key", title="Accès hors heures", sub="Dernières 24 h",
                  rows=[["key", "Entrées hors horaire", "1 · autorisée", "ok"], ["x", "Badges refusés", "0", "ok"], ["users", "Visiteurs", "3 inscrits", "muted"]]),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Fibre dédiée · 1 Gbit/s", icon="router", sig="Lien symétrique", bars=4, down=380, up=210, ping=4, loss="0 %"),
                C("meter", 4, icon="gauge", title="Bande passante · pointe", used=380, total=1000, unit="Mbit/s", note="Pointe de la journée à 10 h 20"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["link", "Câble · 400 Mbit/s", "Secours prêt", "ok"], ["antenna", "LTE", "Ultime secours", "ok"]]),
                C("devices", 7, total=86, groups=[["laptop", 24, "ordinateurs"], ["phone", 31, "téléphones"], ["camera", 9, "caméras"], ["cpu", 22, "objets connectés"]]),
                C("prio", 5, items=[["router", "Fibre dédiée"], ["link", "Câble"], ["antenna", "LTE"]]),
            ]],
            T_diag([["key", "Contrôle d’accès", "En ligne", "ok"], ["camera", "Enregistreur · 9 caméras", "En ligne", "ok"], ["shield", "Réseau des invités", "Isolé", "ok"],
                    ["hydro", "Hydro-Québec · pointes", "À jour", "ok"]],
                   [["key", "Badges", "Dernière lecture : il y a 6 min", "ok"], ["camera", "Caméras", "En direct · il y a 1 s", "ok"],
                    ["hydro", "Hydro-Québec", "Dernière lecture : il y a 40 min", "ok"], ["cloud", "Météo", "Dernière lecture : il y a 6 min", "ok"]],
                   cpu=23, mem=(5.4, 16), disk=(310, 1000), boot="d:-21 02:00", uptime="21 j 9 h"),
        ],
        "equipements": [
            C("equip", 4, icon="door", title="Portes extérieures", sub="Horaire 7 h 30 – 18 h", state="Horaire · ouvertes", tone="ok",
              act={"label": "Tout verrouiller", "icon": "lock", "confirm": "Verrouiller toutes les portes extérieures maintenant? Les badges resteront actifs.",
                   "done": "Verrouillées", "back": "Revenir à l’horaire"}, note="Action critique · inscrite au journal"),
            C("equip", 4, icon="users", title="Salle de réunion", sub="12 places", state="Libre jusqu’à 14 h", tone="ok",
              act={"label": "Préparer la salle", "icon": "play", "confirm": "Préparer la salle : éclairage 80 %, écran allumé, 21 °C?", "done": "Prête", "back": "Libérer la salle"}),
            C("equip", 4, icon="fan", title="CVC", sub="Toit · 3 zones", state="Occupé · 21,5 °C", tone="ok", rows=[["Air neuf", "Selon le CO₂"], ["Filtres", "62 %"]]),
            C("equip", 4, icon="blinds", title="Stores", sub="Façade sud", state="Auto · soleil", tone="ok",
              act={"label": "Tout fermer", "icon": "down", "confirm": "Fermer tous les stores de la façade sud?", "done": "Fermés", "back": "Revenir en auto"}),
            C("equip", 4, icon="tv", title="Écran d’accueil", sub="Hall d’entrée", state="Veille", tone="muted", rows=[["Contenu", "Bienvenue · visiteurs"]],
              toggle={"label": "Allumer", "on": "Allumé", "off": "Veille"}),
            C("list", 4, icon="key", title="Contrôle d’accès", sub="Badges et visiteurs",
              rows=[["key", "Badges actifs", "22", "ok"], ["users", "Visiteurs", "3 inscrits", "ok"], ["x", "Badges suspendus", "1", "muted"]]),
            C("list", 6, icon="users", title="Occupation par étage", sub="Capteurs de présence · données d’exemple",
              rows=[["users", "Rez-de-chaussée · accueil et ventes", "8 / 12 postes", "ok"], ["users", "Étage · direction et comptabilité", "6 / 10 postes", "ok"],
                    ["users", "Salles de réunion", "1 / 3 occupées", "ok"]]),
            C("list", 6, icon="phone", title="Réception et appels", sub="Aperçu · voir l’extension Entreprise",
              rows=[["phone", "Appels à la réception", "0 en attente", "ok"], ["users", "Visiteur annoncé", "1 · à 14 h", "gold"], ["bell", "Accueil", "Ouvert jusqu’à 18 h", "ok"]]),
            C("inspection", 12, title="Prochaine inspection", sub="Gicleurs · inspection annuelle obligatoire", d=5, h="09:00", go="voyage:entretien"),
        ],
        "voyage": [
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Événements (livraisons, réunions, pointes)", l2="Entretien (inspections, contrats)",
                  events=[[-4, "10:00", "11:30", "Réunion de direction", "event"], [-2, "13:00", "15:00", "Entretien du CVC", "maint"], [-1, "08:00", "09:00", "Livraison", "event"],
                          [1, "07:00", "09:00", "Pointe Hydro-Québec", "peak"], [2, "10:00", "11:30", "Réunion d’équipe", "event"], [5, "09:00", "11:00", "Inspection des gicleurs", "maint"]]),
                C("next", 4, icon="wrench", kick="Prochaine inspection", title="Gicleurs", d=5, h="09:00"),
                C("next", 4, icon="bolt", kick="Prochaine pointe", title="Hydro-Québec · 7 h à 9 h", d=1, h="07:00", countdown=True),
                C("next", 4, icon="users", kick="Prochaine réunion", title="Réunion d’équipe", d=2, h="10:00"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes de l’équipe", sub="Ouvrir, fermer et accueillir.", lists=[
                    {"k": "ouverture", "l": "Ouverture", "sub": "Chaque matin.", "icon": "sunrise",
                     "items": [["Portes en mode horaire", "Automatique", True], ["CVC en mode occupé", "Automatique", True], ["Vérifier le quai", "Caméra", True], ["Accueil allumé", "", False]]},
                    {"k": "fermeture", "l": "Fermeture", "sub": "Chaque soir.", "icon": "lock",
                     "items": [["Fenêtres fermées", "Capteurs", False], ["Salle de réunion libérée", "", False], ["Portes verrouillées", "Confirmation requise", False], ["Alarme armée", "", False]]},
                    {"k": "visiteur", "l": "Visiteurs", "sub": "Accueillir en sécurité.", "icon": "users",
                     "items": [["Inscription", "Nom et responsable", True], ["Badge temporaire", "Expire à 18 h", True], ["Accompagnement", "", False]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("shield", "Gicleurs", "Inspection annuelle",
                      src_fixe("regle", "Code de sécurité incendie · inspection annuelle obligatoire", 5)),
                    M("fan", "Filtres du CVC", "Aux 3 mois",
                      compteur("Recommandé par JARVIS selon les heures de ventilation", "aux 1 000 heures", 820, 1000, 10, "h", "jarvis")),
                    M("battery", "Onduleur", "Test de décharge",
                      fab("Manuel de l’onduleur", "aux 6 mois", 182, -152)),
                    M("smoke", "Alarme incendie", "Vérification annuelle",
                      src_fixe("regle", "Code de sécurité incendie · vérification annuelle", 60)),
                    M("door", "Porte de service", "Ferme-porte à ajuster",
                      src_fixe("capteur", "Contacteur de la porte de service", -1, "Fermeture lente mesurée : 9 s au lieu de 4 s")),
                ]),
                C("next", 4, icon="shield", kick="Prochaine inspection", title="Gicleurs", d=5, h="09:00"),
                C("next", 4, icon="door", kick="En retard", title="Ferme-porte de la porte de service", text="Signalé hier par l’équipe."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="findesemaine", items=[
                    {"k": "ouverture", "icon": "sunrise", "label": "Ouverture", "sub": "Accueillir l’équipe",
                     "fx": [["door", "Portes", "Mode horaire", "Déverrouillées", "crit"], ["fan", "CVC", "Mode occupé", "21,5 °C"],
                            ["bulb", "Éclairage", "Bureaux et accueil", "Lecture", "light", "lecture"], ["tv", "Écran d’accueil", "Allumé", "Allumé"]],
                     "autos": [["clock", "Jours ouvrables à 7 h 30", "Lance le mode Ouverture"]]},
                    {"k": "fermeture", "icon": "lock", "label": "Fermeture", "sub": "Fin de journée",
                     "fx": [["door", "Portes", "Verrouillage", "Verrouillées", "crit"], ["fan", "CVC", "Inoccupé", "18 °C"],
                            ["bulb", "Éclairage", "Veilleuses et sorties", "Nuit douce", "light", "nuit-douce"], ["shield", "Alarme", "Armée", "Armée", "crit"]],
                     "autos": [["users", "Dernier badge sorti", "Propose le mode Fermeture"]]},
                    {"k": "findesemaine", "icon": "calendar", "label": "Fin de semaine", "sub": "Bâtiment au repos",
                     "fx": [["fan", "CVC", "Économie", "17 °C"], ["evcharge", "Bornes", "Réservées aux employés de garde", "Limitées"],
                            ["shield", "Alarme", "Armée", "Armée", "crit"], ["camera", "Caméras", "Enregistrement continu", "Actives", "fail"]],
                     "autos": [["clock", "Vendredi à 18 h", "Lance le mode Fin de semaine"]]},
                ], scenarios=[["Événement de pointe", "Délestage en trois étapes"], ["Visiteur important", "Hall, salle et stationnement prêts"], ["Alerte incendie", "Portes déverrouillées, CVC arrêté"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["clock", "Horaire des portes", "Déverrouille à 7 h 30, verrouille à 18 h", "Jours ouvrables", True],
                                     ["wind", "Air neuf selon le CO₂", "Plus d’air quand les salles se remplissent", "CO₂ au-dessus de 900 ppm", True],
                                     ["bolt", "Délestage de pointe", "Bornes, CVC et chauffe-eau", "Avis d’Hydro-Québec", True],
                                     ["drop", "Fuite en salle des serveurs", "Avertit le responsable de garde", "Capteur de fuite", True],
                                     ["users", "Salle réservée", "Prépare la salle 10 min avant", "Agenda de l’équipe", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[6, "Système", "Badge accepté à la porte de service"], [95, "Système", "Mode Ouverture appliqué · 4 / 4 effets confirmés"],
                                        [1500, "Sophie", "Plan de délestage approuvé pour la pointe"], [2900, "Système", "Mode Fermeture appliqué · 4 / 4"]]),
            ]],
        ],
    },
}

# =============================================================================================
# Garage de collection · Sainte-Rosalie (Saint-Hyacinthe) : sept voitures, mainteneurs de charge,
# humidité contrôlée, portes, caméras et coin d'entretien. Les modèles nommés sont les véhicules du
# client (données d'exemple), jamais une association avec un constructeur; aucun logo.
# =============================================================================================

PARC = {
    "km": 100, "note": "Secteur illustratif",
    "roads": [{"pts": [[0, 34], [400, 22]], "n": "20", "at": [330, 24]}, {"pts": [[0, 120], [400, 120]], "straight": True},
              {"pts": [[120, 34], [120, 240]], "straight": True}, {"pts": [[280, 26], [280, 240]], "straight": True},
              {"pts": [[0, 200], [400, 196]], "rail": True}, {"pts": [[200, 120], [200, 196]], "straight": True, "minor": True}],
    "blocks": [[20, 60, 80, 44], [140, 56, 120, 48], [300, 52, 80, 52], [20, 134, 80, 50], [136, 134, 52, 46, "hi"], [212, 134, 52, 46],
               [300, 134, 80, 50], [140, 214, 120, 22], [20, 214, 80, 22, "park"]],
    "labels": [[200, 206, "Voie ferrée"], [60, 82, "Esthétique automobile"], [340, 78, "Station-service"], [238, 160, "Lave-auto"]],
    "me": [162, 157],
}

_GARAGE_BANNER = photo_ou_attente("garage", "Le garage de collection éclairé, voitures sport alignées", "55% 40%")
if _GARAGE_BANNER.get("ph"):
    _GARAGE_BANNER = {"img": "/media/solutions/camera-garage-supercars-v1.webp", "pos": "55% 40%", "alt": "Le garage de collection éclairé, voitures sport alignées"}

COLLECTION = [  # baie, voiture, état, mainteneur de charge
    ["1", "Lamborghini Huracán", "Remisée · 12,8 V", "ok"],
    ["2", "Ferrari 296 GTB", "Remisée · 12,7 V", "ok"],
    ["3", "Nissan GT-R R35", "Remisée · 12,7 V", "ok"],
    ["4", "Audi RS4 Avant", "Prête à rouler · 12,6 V", "ok"],
    ["5", "Mercedes-AMG G63 noir", "Prêt à rouler · 12,6 V", "ok"],
    ["6", "Range Rover", "Prêt à rouler · 12,5 V", "ok"],
    ["7", "Cadillac Escalade noir", "Sorti · retour vers 18 h", "gold"],
]

GARAGE = {
    "key": "garage", "name": "Garage", "kind": "Garage de collection · 8 places", "place": "Saint-Hyacinthe · Sainte-Rosalie", "icon": "garage", "meIcon": "garage",
    "geo": {"lat": 45.645, "lon": -72.905, "place": "Sainte-Rosalie, Saint-Hyacinthe"},
    "banner": _GARAGE_BANNER,
    "titles": {"voyage": "Entretien"}, "voyageIcon": "calendar",
    "subs": {"apercu": "La collection, l’air et les portes en un regard.", "confort": "Température, humidité et air du garage.",
             "energie": "Mainteneurs de charge, bornes et solaire.", "eau": "Aire de lavage, séparateur et fuites.",
             "securite": "Portes, caméras, clés et alertes.", "internet": "Connexions du garage.",
             "equipements": "Portes, mainteneurs, déshumidificateur et bornes.", "voyage": "Esthétique, entretiens et sorties.",
             "modes": "Exposition, fermé, ventilation, remisage d’hiver."},
    "status": [["drop", "Humidité", "45 %", "ok"], ["battery", "Mainteneurs", "6 / 6", "ok"], ["garage", "Portes", "Fermées", "ok"]],
    "maps": {"parc": PARC},
    "wx": WX_SH,
    "energy": {"unit": "kWh", "cap": 10, "nominal": "51,2 V", "chem": "LiFePO₄", "soc": 81, "v": "52,8 V", "reserve": 30, "load": 1900, "battW": 0,
               "autonomy": "≈ 5 h · portes, caméras, mainteneurs et humidité", "ringTitle": "Batterie du garage", "packsTitle": "Batterie du garage",
               "packs": [{"name": "Batterie du garage", "cap": 10, "soc": 81, "v": 52.8, "a": 0.0, "t": 15.1, "cycles": 131, "hi": 3.302, "lo": 3.295}],
               "sources": [["solaire", "Solaire · 10 kWc", "sun", "solar"], ["reseau", "Hydro-Québec", "hydro", "grid"]],
               "store": "Batterie", "loads": "Garage",
               "solar": {"peak": 10000, "cloud": .3, "base": 900, "day": 2400, "eve": 1300, "tilt": 30, "morn": 0}},
    "s": {
        "apercu": [
            C("kpi", 3, icon="thermo", label="Garage", value="15 °C", sub="Plancher radiant · stable", subicon="fire", tone="gold", go="confort"),
            C("kpi", 3, icon="drop", label="Humidité", value="45 %", sub="Cible 40 à 50 % · déshumidificateur auto", subicon="fan", tone="water", go="confort"),
            C("kpi", 3, icon="battery", label="Mainteneurs de charge", value="6 / 6", sub="Escalade sorti · baie 7 libre", subicon="check", tone="ok", go="equipements"),
            C("kpi", 3, icon="garage", label="Portes", value="Fermées", dot="ok", sub="2 portes · porte d’homme verrouillée", subicon="lock", tone="ok", go="securite"),
            C("conditions", 7, title="Conditions au garage"),
            C("lumieres", 5),
            C("list", 7, icon="garage", title="La collection", sub="Baie, voiture et mainteneur de charge · données d’exemple",
              rows=[["garage", "Baie " + b + " · " + v, etat, t] for b, v, etat, t in COLLECTION] + [["garage", "Baie 8", "Libre · voiture de passage", "muted"]]),
            C("checklist", 5, id="fermeture", title="Fermer le garage", icon="clip",
              items=[["Portes de garage fermées", True], ["Mainteneurs branchés", True], ["Armoire à clés verrouillée", True], ["Alarme armée", False]]),
            C("around", 7, title="Autour du garage", map="parc", listTitle="Dans le secteur",
              list=[["car", "gold", "Esthétique automobile", "Rendez-vous de la Huracán jeudi"], ["evcharge", "ok", "Borne rapide", "1,8 km"], ["fuel", "muted", "Super 94 sans éthanol", "Station-service · 2,1 km"]],
              pinsList=[{"x": 60, "y": 82, "icon": "car", "tone": "gold", "title": "Esthétique automobile"}, {"x": 340, "y": 68, "icon": "fuel", "tone": "muted", "title": "Station-service"}],
              btn=["Agenda du garage", "voyage:agenda"]),
            C("upcoming", 5, title="Prochaines 48 heures", icon="car", note="Escalade noir de retour vers 18 h.", text="La porte 1 s’ouvrira à son arrivée, après votre confirmation et un coup d’œil à la caméra.", go="equipements"),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Chauffage radiant", sub="Plancher du garage · température stable pour les voitures", set=15, min=8, max=20, inside=15,
                  rows=[["garage", "Salle d’exposition", "15 °C"], ["fire", "Plancher radiant", "Actif · faible"], ["drop", "Déshumidificateur", "Auto · 45 %"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température du garage", "value": "15 °C", "state": "Stable · ± 0,4 °C", "tone": "ok", "c": "gold",
                     "pts": [14.8, 14.9, 15.0, 15.1, 15.0, 14.9, 15.0, 15.1, 15.2, 15.0, 15.0, 15.0], "min": 6, "max": 24},
                    {"icon": "drop", "title": "Humidité", "value": "45 %", "state": "Dans la cible", "tone": "ok", "c": "blue",
                     "pts": [52, 51, 49, 48, 47, 46, 46, 45, 45, 45, 45, 45], "min": 20, "max": 80}]),
                C("ventilation", 3, speed=1, max=4, rows=[["fan", "Extraction", "Auto · seuil 25 ppm de CO"]]),
                C("air", 3, title="Air du garage", co2=520, quality="Bonne qualité", rows=[["co", "CO", "0 ppm"], ["drop", "Humidité", "45 %"], ["smoke", "Vapeurs d’essence", "Aucune"]]),
                C("outside", 3),
                C("cold", 3, icon="thermo", title="Locaux", sub="Températures actuelles",
                  rows=[["garage", "Salle d’exposition", "15 °C"], ["wrench", "Coin d’entretien", "16 °C"], ["home", "Salon des invités", "20 °C"]]),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["fire", "Plancher radiant", 1100], ["drop", "Déshumidificateur", 420], ["bulb", "Éclairage d’exposition", 260], ["battery", "Mainteneurs de charge · 6", 48], ["evcharge", "Bornes", 0]]),
                C("chips", 12, items=[["battery", "Mainteneurs", "6 branchés · 1 baie libre", "ok"], ["solar", "Source active", "src", "gold"], ["evcharge", "Bornes", "2 disponibles", "ok"]]),
            ]],
            ["batterie", "Batterie", [
                C("packs", 8),
                C("list", 4, icon="shield", title="Protection", sub="Système de gestion (BMS)",
                  rows=[["check", "Charge autorisée", "Oui", "ok"], ["check", "Décharge autorisée", "Oui", "ok"], ["sliders", "Réserve de panne", "30 %", "muted"], ["bell", "Alarme", "Aucune", "ok"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="6,0 kWh", sub="Prévision · pluie", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "10 kWc"], ["compass", "Orientation", "Sud"], ["sliders", "Inclinaison", "30°"], ["pin", "Position", "Toit du garage"]]),
                C("solar", 9), C("fwx", 12, cond="Passages nuageux", cloud=40, quality=3, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("hotwater", 5, set=55, now=54, min=45, max=60, mode="Normal · aire de lavage"),
                C("leaks", 7, sensors=[["tap", "Aire de lavage", "Sec"], ["heater", "Chauffe-eau", "Sec"], ["drop", "Drain de plancher", "Sec"], ["fan", "Déshumidificateur", "Sec"]]),
                C("pump", 4, icon="waves", title="Séparateur eau-huile", sub="Drain de l’aire de lavage", state="Normal", flow="12 %", pressure="Dans 90 jours", l1="Niveau d’huile", l2="Prochaine vidange"),
                C("gauge", 4, icon="drop", title="Bac du déshumidificateur", sub="Vidange automatique au drain", pct=35, value="35 %", est="Vidange à 80 %", estsub="ou au besoin"),
                C("usage", 4, total=140, unit="L", seed=13),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Ouvertures", sub="Portes et accès du garage", env="garage",
                  points=[O("Porte de garage 1", "Fermée", "ok", "Baies", 120, "Alexandre", lock=False, icon="garage"),
                          O("Porte de garage 2", "Fermée", "ok", "Baies", 900, "Julien", lock=False, icon="garage"),
                          O("Porte d’homme", "Verrouillée", "ok", "Entrées", 64, "Julien", lock=True, icon="door"),
                          O("Porte du salon des invités", "Verrouillée", "ok", "Entrées", 3000, "", lock=True, icon="door"),
                          O("Armoire à clés", "Verrouillée", "ok", "Rangement", 240, "Alexandre", lock=True, icon="key")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs du garage",
                  rows=[["co", "Monoxyde de carbone", "0 ppm", "ok"], ["flame", "Vapeurs d’essence", "Normal", "ok"], ["smoke", "Fumée", "Normal", "ok"], ["drop", "Inondation", "Aucune", "ok"],
                        ["eye", "Mouvement", "Aucun · armé", "ok"]]),
                C("cams", 4, items=[["/media/solutions/camera-garage-supercars-v1.webp", "Intérieur", "Caméra de la salle d’exposition", "Allée centrale"],
                                     ["/media/solutions/camera-driveway-garage-v1.webp", "Entrée", "Caméra de l’entrée", "Aucun mouvement"]]),
                C("events", 4, items=[[120, "Escalade noir sorti", "Porte 1 · par Alexandre · confirmé", "ok"], [240, "Armoire à clés ouverte", "Clé de l’Escalade · Alexandre", "gold"],
                                      [64, "Porte d’homme déverrouillée", "Badge de Julien", "ok"], [900, "Extraction forcée · 15 min", "Démarrage à froid du G63", "warn"]]),
                C("toggle", 6, icon="shield", key="surv", title="Alarme du garage", sub="Armée · périmètre et mouvement", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Intrusion, CO et humidité", on=True),
                C("note", 12, icon="info", text="Ouvrir une porte de garage ou l’armoire à clés à distance demande confirmation et vérifie d’abord la caméra."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · Saint-Hyacinthe", counts=[0, 1, 0, 0, 0],
                  alert={"level": "Veille", "title": "Pluie verglaçante", "text": "Possible demain soir · sel sur les routes : garder les voitures de collection à l’intérieur.", "src": "Environnement Canada · exemple", "ago": 22}),
                C("list", 6, icon="hydro", title="Hydro-Québec", sub="Données d’exemple", rows=[["hydro", "Pannes dans le secteur", "Aucune", "ok"], ["bolt", "Événement de pointe", "Demain 6 h – 9 h", "warn"]]),
                C("list", 6, icon="road", title="Routes · exemple", sub="Québec 511", rows=[["road", "Autoroute 20", "Chaussée mouillée · sel épandu", "warn"], ["cone", "Rang de la Presqu’île", "Aucune entrave", "ok"]]),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Fibre · 1 Gbit/s", icon="router", sig="Fibre optique", bars=4, down=86, up=21, ping=6, loss="0 %"),
                C("meter", 4, icon="chart", title="Données du mois", used=164, total=1000, unit="Go", note="Forfait illimité · indicateur seulement"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["antenna", "LTE de secours", "Prêt", "ok"]]),
                C("devices", 7, total=19, groups=[["camera", 4, "caméras"], ["battery", 7, "mainteneurs de charge"], ["cpu", 6, "capteurs"], ["phone", 2, "téléphones"]]),
                C("prio", 5, items=[["router", "Fibre"], ["antenna", "LTE de secours"]]),
            ]],
            T_diag([["camera", "Caméras · 4 flux", "En ligne", "ok"], ["battery", "Mainteneurs de charge", "En ligne", "ok"], ["co", "Détecteurs de CO", "En ligne", "ok"], ["cloud", "Connecteur météo", "À jour", "ok"]],
                   [["drop", "Humidité", "Dernière lecture : il y a 8 s", "ok"], ["camera", "Caméras", "En direct · il y a 2 s", "ok"], ["battery", "Mainteneurs", "Dernière lecture : il y a 1 min", "ok"]],
                   cpu=9, mem=(1.4, 4), disk=(44, 128)),
        ],
        "equipements": [
            C("equip", 4, icon="garage", title="Porte de garage 1", sub="Baies 1 à 4", state="Fermée", tone="ok",
              act={"label": "Ouvrir", "icon": "up", "confirm": "Ouvrir la porte de garage 1? Vérifiez la caméra : l’entrée doit être dégagée.", "done": "Ouverte", "back": "Fermer"}, note="Confirmation requise"),
            C("equip", 4, icon="garage", title="Porte de garage 2", sub="Baies 5 à 8", state="Fermée", tone="ok",
              act={"label": "Ouvrir", "icon": "up", "confirm": "Ouvrir la porte de garage 2?", "done": "Ouverte", "back": "Fermer"}, note="Confirmation requise"),
            C("equip", 4, icon="battery", title="Mainteneurs de charge", sub="7 sorties · une par baie", state="6 branchés · 12,5 à 12,8 V", tone="ok",
              rows=[["Huracán · 296 · GT-R", "Mode remisage"], ["RS4 · G63 · Range Rover", "Mode maintien"]]),
            C("equip", 4, icon="drop", title="Déshumidificateur", sub="Salle d’exposition", state="Auto · 45 %", tone="ok", rows=[["Cible", "40 à 50 %"]],
              toggle={"label": "En marche", "on": "Actif", "off": "Arrêté"}),
            C("equip", 4, icon="evcharge", title="Bornes de recharge", sub="2 bornes · niveau 2 · 11 kW", state="Disponibles", tone="ok",
              act={"label": "Activer la borne 1", "icon": "bolt", "confirm": "Activer la borne 1 pour une session de 4 heures?", "done": "Session active · 4 h", "back": "Arrêter la session"}),
            C("equip", 4, icon="fan", title="Extraction", sub="Gaz d’échappement", state="Auto · 0 ppm", tone="ok",
              act={"label": "Forcer 30 minutes", "icon": "fan", "confirm": "Forcer l’extraction au maximum pendant 30 minutes?", "done": "Maximum · 30 min", "back": "Revenir en auto"}),
            C("equip", 4, icon="fire", title="Plancher radiant", sub="Chaudière électrique", state="15 °C", tone="ok", rows=[["Retour", "26 °C"], ["Mode", "Exposition"]]),
            C("equip", 4, icon="key", title="Armoire à clés", sub="7 clés · ouverture journalisée", state="Verrouillée · 6 clés", tone="ok",
              act={"label": "Déverrouiller", "icon": "unlock", "confirm": "Déverrouiller l’armoire à clés? L’ouverture sera inscrite au journal.", "done": "Déverrouillée", "back": "Verrouiller"},
              note="Action critique · inscrite au journal"),
            C("equip", 4, icon="bulb", title="Éclairage d’exposition", sub="Rampes DEL au-dessus des baies", state="Éteint", tone="muted", toggle={"label": "Allumer", "on": "Allumé", "off": "Éteint"}),
            C("inspection", 12, title="Prochain entretien", sub="Ferrari 296 GTB · entretien annuel chez le concessionnaire", d=11, go="voyage:entretien"),
        ],
        "voyage": [
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Sorties et rendez-vous", l2="Entretien (voitures et garage)",
                  events=[[-3, "09:00", "12:00", "Lavage et céramique · G63", "event"], [0, "18:00", "18:30", "Retour de l’Escalade", "event"], [2, "09:00", "16:00", "Esthétique · Huracán", "event"],
                          [4, "10:00", "11:00", "Inspection des portes de garage", "maint"], [11, "09:00", "12:00", "Entretien annuel · 296 GTB", "maint"]]),
                C("next", 4, icon="car", kick="Retour", title="Escalade noir", d=0, h="18:00", countdown=True),
                C("next", 4, icon="car", kick="Esthétique", title="Lamborghini Huracán", d=2, h="09:00"),
                C("next", 4, icon="wrench", kick="Entretien", title="Ferrari 296 GTB", d=11, h="09:00"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes du garage", sub="Sortir, rentrer et remiser une voiture.", lists=[
                    {"k": "sortie", "l": "Sortie", "sub": "Avant de prendre une voiture.", "icon": "car",
                     "items": [["Pression des pneus", "Lue par le boîtier ou l’application", True], ["Mainteneur débranché", "", True], ["Clé signée à l’armoire", "Journal", True], ["Météo sans sel", "", False]]},
                    {"k": "retour", "l": "Retour", "sub": "En rentrant.", "icon": "garage",
                     "items": [["Mainteneur rebranché", "Capteur", False], ["Clé remise", "", False], ["Extraction 15 min", "Auto", True], ["Porte fermée", "Capteur", True]]},
                    {"k": "hiver", "l": "Remisage d’hiver", "sub": "Avant le sel.", "icon": "snowflake",
                     "items": [["Plein et stabilisant", "Huracán, 296 et GT-R", True], ["Pneus gonflés pour le remisage", "", True], ["Housses posées", "", False], ["Assurance en mode remisage", "", False]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("car", "Ferrari 296 GTB · entretien annuel", "Concessionnaire · exemple",
                      fab("Carnet d’entretien du constructeur", "aux 12 mois", 365, -354)),
                    M("car", "Lamborghini Huracán · huile et filtres", "Atelier spécialisé · exemple",
                      fab("Carnet d’entretien du constructeur", "aux 12 mois", 365, -301)),
                    M("car", "Nissan GT-R R35 · huile de boîte", "Atelier spécialisé · exemple",
                      compteur("Compteur kilométrique (boîtier JARVIS)", "aux 30 000 km", 27400, 30000, 25)),
                    M("garage", "Portes de garage", "Inspection annuelle",
                      fab("Manuel des ouvre-portes", "aux 12 mois", 365, -361)),
                    M("drop", "Déshumidificateur", "Nettoyage du filtre",
                      compteur("Recommandé par JARVIS selon les heures de marche", "aux 400 heures", 388, 400, 6, "h", "jarvis")),
                ]),
                C("next", 4, icon="garage", kick="Prochaine inspection", title="Portes de garage", d=4, h="10:00"),
                C("next", 4, icon="drop", kick="Bientôt", title="Filtre du déshumidificateur", text="Dans environ 2 jours."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="ferme", items=[
                    {"k": "exposition", "icon": "star", "label": "Exposition", "sub": "Recevoir des invités",
                     "fx": [["bulb", "Éclairage", "Rampes des baies", "Vitrine", "light", "lecture"], ["fire", "Plancher radiant", "Confort des invités", "17 °C"],
                            ["home", "Salon des invités", "Déverrouillé", "Ouvert", "crit"], ["shield", "Alarme", "Désarmée", "Désarmée", "crit"]],
                     "autos": [["calendar", "Visite à l’agenda", "Propose le mode Exposition"]]},
                    {"k": "ferme", "icon": "lock", "label": "Fermé", "sub": "Nuit et absence",
                     "fx": [["garage", "Portes", "Vérification et fermeture", "Fermées", "crit"], ["key", "Armoire à clés", "Verrouillage", "Verrouillée"],
                            ["drop", "Humidité", "Cible 45 %", "Auto"], ["shield", "Alarme", "Armée", "Armée", "crit"]],
                     "autos": [["clock", "À 22 h", "Propose le mode Fermé"]]},
                    {"k": "ventilation", "icon": "fan", "label": "Ventilation", "sub": "Après un démarrage",
                     "fx": [["fan", "Extraction", "Maximum", "15 min"], ["garage", "Porte 2", "Entrouverte pour l’air", "30 cm", "crit fail"], ["co", "CO", "Surveillance rapprochée", "Active"]],
                     "autos": [["co", "Moteur démarré dans le garage", "Propose le mode Ventilation"]]},
                    {"k": "hiver", "icon": "snowflake", "label": "Remisage d’hiver", "sub": "De novembre à avril",
                     "fx": [["battery", "Mainteneurs", "Mode remisage", "Remisage"], ["drop", "Humidité", "Cible 40 %", "40 %"],
                            ["fire", "Plancher radiant", "Économie", "12 °C"], ["shield", "Alarme", "Armée en permanence", "Armée", "crit"]],
                     "autos": [["calendar", "15 novembre", "Propose le remisage d’hiver"]]},
                ], scenarios=[["Arrivée d’une voiture", "Porte, éclairage et mainteneur rappelé"], ["Visite d’invités", "Éclairage d’exposition, salon ouvert"], ["Fin de soirée", "Portes, clés, alarme"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["drop", "Humidité au-dessus de 55 %", "Démarre le déshumidificateur et vous avertit", "Sonde d’humidité", True],
                                     ["battery", "Batterie sous 12,4 V", "Alerte avec la baie et la voiture", "Mainteneurs de charge", True],
                                     ["co", "Extraction selon le CO", "Force l’extraction au-dessus de 25 ppm", "Détecteur de CO", True],
                                     ["garage", "Porte restée ouverte", "Avertit après 10 minutes", "Capteur de porte", True],
                                     ["key", "Clé sortie sans voiture", "Alerte si la clé n’est pas rendue après 12 h", "Armoire à clés", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[120, "Alexandre", "Escalade noir sorti · porte 1 refermée"], [240, "Alexandre", "Clé de l’Escalade sortie de l’armoire"],
                                        [900, "Système", "Extraction forcée 15 min · démarrage à froid du G63"], [1400, "Système", "Mode Fermé appliqué · 4 / 4"]]),
            ]],
        ],
    },
}

# =============================================================================================
# Ferme · exploitation multi-élevage, Montérégie (données d’exemple) : étable laitière et veaux,
# pondoir, poulets de chair, porcherie, écurie, silos et séchoir, machinerie, fosse à lisier.
# Vue d'ensemble (plan noir de la cour et une tuile par bâtiment), puis le détail par bâtiment dans
# « Ambiance des bâtiments ». Génératrice avec transfert automatique, pointe Hydro-Québec, biosécurité.
# La photo media/env/ferme.webp est utilisée dès qu’elle existe (voir photo_ou_attente).
# =============================================================================================

RANGS = {
    "km": 40, "note": "Rangs et champs illustratifs",
    "fields": [[[10, 20], [150, 20], [150, 110], [10, 110]], [[160, 20], [300, 20], [300, 110], [160, 110]], [[310, 20], [390, 20], [390, 110], [310, 110]],
               [[10, 130], [100, 130], [100, 230], [10, 230]], [[200, 130], [300, 130], [300, 230], [200, 230]], [[310, 130], [390, 130], [390, 230], [310, 230]]],
    "rivers": [[[0, 236], [80, 214], [150, 226], [230, 236], [330, 216], [400, 222]]],
    "roads": [{"pts": [[0, 120], [400, 120]], "straight": True, "n": "Rang", "at": [60, 120]}, {"pts": [[155, 0], [155, 240]], "straight": True, "minor": True},
              {"pts": [[305, 0], [305, 240]], "straight": True, "minor": True}, {"pts": [[150, 120], [150, 160]], "minor": True}],
    "blocks": [[112, 140, 60, 22, "hi"], [112, 168, 34, 18], [154, 166, 12, 12], [176, 144, 14, 14]],
    "labels": [[80, 64, "Champ nord · maïs"], [230, 64, "Prairie"], [56, 180, "Pâturage"], [250, 180, "Soya"], [200, 228, "Rivière Noire", "water"]],
    "me": [142, 151],
}

COUR = {  # plan de la cour de la ferme (400 unités par kilomètre)
    "km": 400, "note": "Plan de la cour illustratif",
    "fields": [[[0, 0], [400, 0], [400, 14], [0, 14]]],
    "roads": [{"pts": [[0, 226], [400, 226]], "straight": True, "n": "Rang", "at": [40, 226]},
              {"pts": [[205, 226], [205, 24]], "straight": True, "minor": True}, {"pts": [[40, 118], [370, 118]], "straight": True, "minor": True}],
    "blocks": [[24, 30, 128, 46, "hi"], [156, 40, 30, 24], [24, 84, 56, 22],
               [226, 26, 112, 24], [226, 58, 140, 26], [226, 128, 128, 36],
               [30, 132, 74, 26], [24, 166, 96, 44, "park"],
               [140, 128, 16, 16], [160, 128, 16, 16], [180, 128, 16, 16], [140, 150, 40, 16],
               [256, 176, 74, 34], [346, 176, 36, 36], [148, 186, 26, 18]],
    "labels": [[88, 53, "Étable laitière"], [282, 38, "Pondoir"], [296, 71, "Poulets de chair"], [290, 146, "Porcherie"],
               [67, 145, "Écurie"], [72, 196, "Paddock"], [168, 176, "Silos"], [293, 193, "Machinerie"], [364, 168, "Fosse"]],
    "me": [161, 195],
}

# Vue d'ensemble : un bâtiment par tuile (photo extérieure, état, trois mesures, alerte, lien vers le détail).
FERME_BATIMENTS = [
    {"k": "laitier", "name": "Étable laitière et veaux", "icon": "milk", "tone": "ok", "map": [88, 53], "state": "Normal",
     "kpis": [["Vaches", "124"], ["Étable", "12,4 °C"], ["Tank", "2,8 °C"]], "alert": "Traite du soir à 17 h", "go": "confort:laitier"},
    {"k": "pondoir", "name": "Pondoir · poules pondeuses", "icon": "sparkle", "tone": "ok", "map": [282, 38], "state": "Normal",
     "kpis": [["Poules", "24 000"], ["Œufs", "21 840"], ["NH₃", "12 ppm"]], "alert": "Silo de moulée ≈ 4 jours", "go": "confort:pondoir"},
    {"k": "chair", "name": "Poulets de chair", "icon": "gauge", "tone": "warn", "map": [296, 71], "state": "À vérifier",
     "kpis": [["Lot", "Jour 24"], ["Poids", "1,18 kg"], ["Zone 3", "25,6 °C"]], "alert": "Aérotherme no 3 en défaut", "go": "confort:chair"},
    {"k": "porcherie", "name": "Porcherie", "icon": "barn", "tone": "gold", "map": [290, 146], "state": "Surveillé",
     "kpis": [["Porcs", "3 680"], ["Fosses", "62 %"], ["H₂S", "0,4 ppm"]], "alert": "Abreuvoir à débit faible · pouponnière", "go": "confort:porcherie"},
    {"k": "ecurie", "name": "Écurie", "icon": "fence", "tone": "ok", "map": [67, 145], "state": "Normal",
     "kpis": [["Chevaux", "10"], ["Abreuvoirs", "8 °C"], ["Foin", "9 sem."]], "alert": "Paddock fermé · chevaux rentrés", "go": "confort:ecurie"},
    {"k": "grains", "name": "Silos, séchoir et machinerie", "icon": "silo", "tone": "gold", "map": [168, 140], "state": "Séchage",
     "kpis": [["Maïs", "730 t"], ["Humidité", "17,2 %"], ["Fosse", "78 %"]], "alert": "Séchage en cours · cible 15,5 %", "go": "confort:grains"},
]

# En-tête du détail d'un bâtiment : photos (intérieur et extérieur), capacité, état et sources de données.
FERME_BAT = {
    "laitier": {"k": "laitier", "name": "Étable laitière et veaux", "icon": "milk", "sub": "124 vaches en lactation · 38 veaux · 52 taures",
                "chips": [["thermo", "Étable", "12,4 °C", "ok"], ["milk", "Tank à lait", "2,8 °C", "ok"], ["fan", "Ventilation", "Auto · 45 %", "ok"]],
                "sources": ["Contrôleur de ventilation", "Sondes NH₃ et CO₂", "Contrôleur de la laiterie", "Compteurs d’eau"]},
    "pondoir": {"k": "pondoir", "name": "Pondoir · poules pondeuses", "icon": "sparkle", "sub": "24 000 poules en volière · salle d’emballage",
                "chips": [["thermo", "Température", "20,5 °C", "ok"], ["wind", "NH₃", "12 ppm", "ok"], ["bulb", "Éclairage", "16 h par jour", "ok"]],
                "sources": ["Contrôleur d’ambiance", "Compteur d’œufs", "Compteur d’eau", "Pesée du silo"]},
    "chair": {"k": "chair", "name": "Poulets de chair", "icon": "gauge", "sub": "Lot de 30 000 poulets · jour 24 sur 35 · 4 zones",
              "chips": [["thermo", "Zone 3", "25,6 °C", "warn"], ["gauge", "Poids moyen", "1,18 kg", "ok"], ["chart", "Mortalité", "2,1 %", "ok"]],
              "sources": ["Contrôleur par zone", "Balances de pesée", "Compteurs d’eau et de moulée", "Pesée du silo"]},
    "porcherie": {"k": "porcherie", "name": "Porcherie", "icon": "barn", "sub": "Maternité, pouponnière et engraissement · 3 680 porcs",
                  "chips": [["thermo", "Engraissement", "19 °C", "ok"], ["drop", "Fosses", "62 %", "ok"], ["drop", "Abreuvoir", "Salle 2", "warn"]],
                  "sources": ["Contrôleurs par salle", "Sondes NH₃ et H₂S", "Compteurs d’eau", "Sondes de niveau des fosses"]},
    "ecurie": {"k": "ecurie", "name": "Écurie", "icon": "fence", "sub": "12 boxes · 10 chevaux · sellerie et paddock",
               "chips": [["thermo", "Écurie", "7,2 °C", "ok"], ["trough", "Abreuvoirs", "8 °C", "ok"], ["fence", "Paddock", "Fermé", "ok"]],
               "sources": ["Sondes d’ambiance", "Capteurs des abreuvoirs", "Capteur de porte", "Inventaire du foin"]},
    "grains": {"k": "grains", "name": "Silos à grain, séchoir et cour", "icon": "silo", "sub": "3 silos · séchoir au propane · machinerie, fosse et génératrice",
               "chips": [["silo", "Silos", "778 t", "ok"], ["fire", "Séchoir", "17,2 %", "gold"], ["drop", "Fosse", "78 %", "gold"]],
               "sources": ["Câbles de température", "Automate du séchoir", "Sonde de la fosse", "Contrôleur de la génératrice"]},
}

FERME = {
    "key": "ferme", "name": "Ferme", "kind": "Ferme multi-élevage · 7 bâtiments", "place": "Montérégie", "icon": "barn", "meIcon": "barn",
    "geo": {"lat": 45.55, "lon": -72.95, "place": "Montérégie"},
    "banner": photo_ou_attente("ferme", "Les bâtiments de la ferme : étable, poulaillers, porcherie, écurie et silos"),
    "titles": {"voyage": "Entretien", "confort": "Ambiance des bâtiments"}, "voyageIcon": "calendar",
    "subs": {"apercu": "Tous les bâtiments de la ferme en un regard.",
             "confort": "Le détail de chaque bâtiment : ambiance, animaux, eau, moulée et alarmes.",
             "energie": "Génératrice, pointe Hydro-Québec et consommation par bâtiment.",
             "eau": "Abreuvoirs, puits et eau de lavage : le troupeau d’abord.",
             "securite": "Biosécurité, alarmes et surveillance des bâtiments.",
             "internet": "Liaison rurale, capteurs et secours.",
             "equipements": "Tank à lait, traite, alimentation, séchoir et bâtiments.",
             "voyage": "Collectes, visites et entretien planifié.",
             "modes": "Traite, nuit, canicule, panne de courant, biosécurité."},
    "status": [["thermo", "Étable", "12,4 °C", "gold"], ["milk", "Tank à lait", "2,8 °C", "water"], ["gen", "Génératrice", "Prête", "ok"]],
    "maps": {"rangs": RANGS, "cour": COUR},
    "wx": wx([-1, -2, -2, -3, -3, -3, -2, -1, 1, 3, 5, 6, 7, 7, 6, 5, 3, 2, 1, 0, 0, -1, -1, -1],
             "ddddddpppppcccccppdddddd", "000000000011111000000000",
             [["cloudsun", 7, -3, 10], ["rain", 8, 1, 70], ["cloud", 5, -1, 30], ["sun", 4, -4, 0], ["snow", 1, -5, 40]],
             hum=74, dew=-3, wind=16, dir="Ouest", gust=28, vis=30, hpa=1018, trend="Stable", uv=1, cas=2),
    "energy": {"unit": "kWh", "cap": 20, "nominal": "51,2 V", "chem": "LiFePO₄", "soc": 88, "v": "53,1 V", "reserve": 40, "load": 21000, "battW": 0,
               "autonomy": "≈ 1 h · alarmes, contrôleurs et lait", "ringTitle": "Batterie de secours", "packsTitle": "Batterie de secours",
               "packs": [{"name": "Batterie A", "cap": 10, "soc": 88, "v": 53.1, "a": 0.0, "t": 10.4, "cycles": 77, "hi": 3.318, "lo": 3.309},
                         {"name": "Batterie B", "cap": 10, "soc": 87, "v": 53.0, "a": 0.0, "t": 10.9, "cycles": 79, "hi": 3.316, "lo": 3.307}],
               "sources": [["solaire", "Solaire · 60 kWc", "sun", "solar"], ["reseau", "Hydro-Québec · triphasé", "hydro", "grid"], ["gen", "Génératrice diesel · 150 kW", "gen", 0, "en veille"]],
               "store": "Batterie", "loads": "Ferme",
               "solar": {"peak": 60000, "cloud": .3, "base": 17000, "day": 21000, "eve": 26000, "tilt": 30, "morn": .8}},
    "s": {
        "apercu": [
            C("kpi", 4, icon="thermo", label="Étable laitière", value="12,4 °C", sub="124 vaches · ventilation auto", subicon="fan", tone="gold", go="confort:laitier"),
            C("kpi", 4, icon="milk", label="Tank à lait", value="2,8 °C", sub="6 400 L · collecte demain 9 h", subicon="truck", tone="water", go="equipements"),
            C("kpi", 4, icon="sparkle", label="Œufs du jour · pondoir", value="21 840", sub="Taux de ponte 91 % · 24 000 poules", subicon="check", tone="gold", go="confort:pondoir"),
            C("kpi", 4, icon="gauge", label="Poulets de chair · jour 24", value="1,18 kg", sub="Zone 3 à 25,6 °C · consigne 27 °C", subicon="warn", tone="gold", go="confort:chair"),
            C("kpi", 4, icon="barn", label="Porcherie", value="3 680 porcs", sub="Fosses sous lattes à 62 % · aucune alarme", subicon="check", tone="ok", go="confort:porcherie"),
            C("kpi", 4, icon="gen", label="Génératrice", value="Prête", dot="ok", sub="150 kW · diesel 74 % · essai lundi", subicon="fuel", tone="ok", go="energie:secours"),
            C("batiments", 12, title="Les bâtiments de la ferme", sub="Un coup d’œil sur chaque bâtiment · touchez-en un pour le détail", items=FERME_BATIMENTS),
            C("around", 7, title="Plan de la cour", map="cour", listTitle="À surveiller aujourd’hui",
              list=[["thermo", "warn", "Poulets de chair · zone 3", "25,6 °C · chauffage à vérifier"], ["drop", "gold", "Fosse à lisier", "78 % · ≈ 140 jours de capacité"],
                    ["truck", "gold", "Collecte du lait", "Demain 9 h · quai dégagé"], ["silo", "ok", "Séchoir à grain", "Maïs à 17,2 % · cible 15,5 %"]],
              pinsList=[{"x": b["map"][0], "y": b["map"][1], "icon": b["icon"], "tone": b["tone"], "title": b["name"]} for b in FERME_BATIMENTS],
              btn=["Ambiance des bâtiments", "confort"]),
            C("checklist", 5, id="soir", title="Tournée du soir", icon="clip",
              items=[["Traite terminée", False], ["Œufs ramassés · convoyeur arrêté", True], ["Poulets · zone 3 vérifiée", False], ["Abreuvoirs de la porcherie", True],
                     ["Chevaux rentrés · paddock fermé", True], ["Registre des visiteurs à jour", True]]),
            C("conditions", 7, title="Conditions aux champs"),
            C("lumieres", 5),
            C("upcoming", 7, title="Prochaines 48 heures", icon="fan", note="Panne de ventilation = urgence animale.",
              text="Les poulaillers et la porcherie passent en premier sur la génératrice · dernier essai en charge lundi, réussi.", go="energie:secours"),
            C("next", 5, icon="milk", kick="Prochaine traite", title="Traite du soir", d=0, h="17:00", countdown=True),
        ],
        "confort": [
            ["laitier", "Laitier", [
                C("batiment", 12, **FERME_BAT["laitier"]),
                C("thermostat", 7, title="Étable des vaches", sub="Consigne du troupeau · ventilation automatique", set=12, min=0, max=20, inside=12,
                  rows=[["barn", "Étable des vaches", "12,4 °C"], ["fan", "Ventilation", "Auto · 45 % · 12 ventilateurs"], ["blinds", "Rideaux latéraux", "Ouverts à 30 % · selon le vent"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température de l’étable", "value": "12,4 °C", "state": "Dans la cible", "tone": "ok", "c": "gold",
                     "pts": [11.6, 11.8, 12.1, 12.4, 12.6, 12.5, 12.4, 12.3, 12.4, 12.5, 12.4, 12.4], "min": 0, "max": 20},
                    {"icon": "drop", "title": "Humidité de l’étable", "value": "68 %", "state": "Sous le seuil de 80 %", "tone": "ok", "c": "blue",
                     "pts": [72, 71, 70, 69, 68, 68, 69, 70, 69, 68, 68, 68], "min": 40, "max": 95}]),
                C("list", 4, icon="barn", title="Étable des vaches", sub="124 places · logettes",
                  rows=[["thermo", "Température", "12,4 °C", "ok"], ["drop", "Humidité", "68 %", "ok"], ["wind", "Ammoniac (NH₃)", "9 ppm · seuil 20", "ok"],
                        ["wind", "CO₂", "2 400 ppm · seuil 3 000", "ok"], ["fan", "Ventilation", "Auto · 45 %", "ok"]]),
                C("list", 4, icon="barn", title="Pouponnière des veaux", sub="Cases individuelles et niches",
                  rows=[["thermo", "Température", "16,8 °C", "ok"], ["drop", "Humidité", "62 %", "ok"], ["wind", "Ammoniac (NH₃)", "6 ppm · seuil 20", "ok"],
                        ["wind", "Courants d’air", "Aucun détecté", "ok"], ["fan", "Ventilation", "Tubes d’air · minimum", "ok"]]),
                C("list", 4, icon="barn", title="Taures et génisses", sub="Bâtiment froid · ventilation naturelle",
                  rows=[["thermo", "Température", "8,9 °C", "ok"], ["drop", "Humidité", "71 %", "ok"], ["wind", "Ammoniac (NH₃)", "11 ppm · seuil 20", "ok"],
                        ["wind", "CO₂", "2 100 ppm · seuil 3 000", "ok"], ["blinds", "Rideaux", "Auto · selon le vent", "ok"]]),
                C("note", 12, icon="info", text="Seuils d’alerte : NH₃ 20 ppm, CO₂ 3 000 ppm, humidité 80 %. Tout dépassement avertit immédiatement le responsable de garde."),
            ]],
            ["pondoir", "Pondoir", [
                C("batiment", 12, **FERME_BAT["pondoir"]),
                C("kpi", 3, icon="thermo", label="Température", value="20,5 °C", sub="Consigne 20 °C · stable", tone="gold"),
                C("kpi", 3, icon="wind", label="Ammoniac (NH₃)", value="12 ppm", dot="ok", sub="Seuil d’alerte 25 ppm", tone="ok"),
                C("kpi", 3, icon="sparkle", label="Œufs du jour", value="21 840", sub="Taux de ponte 91 % · hier 21 760", tone="gold"),
                C("kpi", 3, icon="silo", label="Silo de moulée", value="64 %", sub="11,5 t · ≈ 4 jours", bar=64, tone="gold"),
                C("trends", 7, items=[
                    {"icon": "thermo", "title": "Température du pondoir", "value": "20,5 °C", "state": "Dans la cible", "tone": "ok", "c": "gold",
                     "pts": [20.1, 20.2, 20.2, 20.3, 20.4, 20.6, 20.7, 20.6, 20.5, 20.5, 20.4, 20.5], "min": 14, "max": 26},
                    {"icon": "drop", "title": "Humidité du poulailler", "value": "58 %", "state": "Dans la cible", "tone": "ok", "c": "blue",
                     "pts": [60, 60, 59, 59, 58, 58, 59, 58, 58, 57, 58, 58], "min": 30, "max": 90}]),
                C("list", 5, icon="list", title="Eau, moulée et lumière", sub="Mesures de la journée · exemple",
                  rows=[["drop", "Eau consommée", "4 600 L · 192 ml par poule", "ok"], ["silo", "Moulée distribuée", "2,6 t · 108 g par poule", "ok"],
                        ["bulb", "Éclairage programmé", "16 h · de 4 h 30 à 20 h 30", "ok"], ["fan", "Ventilation", "Auto · 38 %", "ok"], ["sparkle", "Œufs fêlés ou sales", "0,8 %", "ok"]]),
                C("equip", 4, icon="bulb", title="Éclairage du pondoir", sub="Programme de ponte · 16 h", state="Allumé · aube à 4 h 30", tone="ok",
                  act={"label": "Voir le programme", "icon": "list", "preview": True, "text": "Aube progressive de 4 h 30 à 4 h 45, plein éclairage jusqu’à 20 h 15, crépuscule de 15 minutes. Changer la durée demande votre confirmation : elle agit sur la ponte."}),
                C("equip", 4, icon="fan", title="Ventilation du pondoir", sub="8 ventilateurs · entrées d’air", state="Auto · 38 %", tone="ok",
                  act={"label": "Forcer à 70 % · 30 min", "icon": "fan", "confirm": "Forcer la ventilation du pondoir à 70 % pendant 30 minutes? La température baissera d’environ 1 °C.", "done": "70 % · 30 min", "back": "Revenir en auto"}),
                C("equip", 4, icon="swap", title="Convoyeur à œufs", sub="Ramassage vers la salle d’emballage", state="Arrêté · ramassage fait à 10 h", tone="muted",
                  act={"label": "Lancer un ramassage", "icon": "play", "confirm": "Démarrer le convoyeur à œufs? Vérifiez que personne n’est dans l’allée du convoyeur.", "done": "Ramassage en cours", "back": "Arrêter"}, note="Confirmation requise"),
                C("events", 6, items=[[50, "Ramassage des œufs terminé", "21 840 œufs · salle d’emballage", "ok"], [190, "Moulée distribuée", "Passage 3 de 4", "ok"],
                                      [720, "Aube du pondoir", "Éclairage programmé · 4 h 30", "ok"]]),
                C("note", 6, icon="info", text="Sources : contrôleur d’ambiance du poulailler, compteur d’œufs du convoyeur, compteur d’eau et pesée du silo. Seuils : NH₃ 25 ppm, température 16 à 24 °C."),
            ]],
            ["chair", "Poulets de chair", [
                C("batiment", 12, **FERME_BAT["chair"]),
                C("kpi", 3, icon="gauge", label="Poids moyen du lot", value="1,18 kg", sub="Jour 24 · objectif 1,15 kg", tone="gold"),
                C("kpi", 3, icon="chart", label="Mortalité", value="2,1 %", sub="Cumulée · 0,04 % aujourd’hui", tone="ok"),
                C("kpi", 3, icon="thermo", label="Zone 3", value="25,6 °C", sub="Consigne 27 °C · 1 aérotherme en défaut", subicon="warn", tone="gold"),
                C("kpi", 3, icon="silo", label="Silo de moulée", value="58 %", sub="6,1 t · ≈ 3 jours", bar=58, tone="gold"),
                C("list", 5, icon="thermo", title="Température par zone", sub="Consigne 27 °C au jour 24",
                  rows=[["thermo", "Zone 1 · avant", "26,8 °C", "ok"], ["thermo", "Zone 2", "27,0 °C", "ok"], ["thermo", "Zone 3", "25,6 °C · sous la consigne", "warn"],
                        ["thermo", "Zone 4 · arrière", "26,9 °C", "ok"], ["drop", "Humidité moyenne", "61 %", "ok"]]),
                C("trends", 7, items=[
                    {"icon": "drop", "title": "Humidité moyenne", "value": "61 %", "state": "Dans la cible", "tone": "ok", "c": "blue",
                     "pts": [63, 63, 62, 62, 62, 61, 61, 62, 61, 61, 61, 61], "min": 30, "max": 90},
                    {"icon": "thermo", "title": "Zone 3 · température", "value": "25,6 °C", "state": "En baisse depuis 2 h", "tone": "warn", "c": "gold",
                     "pts": [27.0, 27.0, 26.9, 27.0, 27.1, 27.0, 26.8, 26.5, 26.2, 25.9, 25.7, 25.6], "min": 22, "max": 30}]),
                C("equip", 4, icon="fire", title="Chauffage · zone 3", sub="Aérotherme au propane no 3", state="En défaut · flamme non détectée", tone="warn",
                  rows=[["Zones 1, 2 et 4", "Normaux"]],
                  act={"label": "Relancer l’aérotherme", "icon": "refresh", "confirm": "Relancer l’aérotherme no 3? Si la flamme n’est pas détectée de nouveau, le technicien de garde sera appelé.", "done": "Relancé · 26,1 °C et en hausse", "back": "Relancer encore"},
                  note="Confirmation requise"),
                C("equip", 4, icon="fan", title="Ventilation", sub="Minimum et tunnel · 12 ventilateurs", state="Minimum · 22 %", tone="ok",
                  act={"label": "Passer en tunnel · 20 min", "icon": "fan", "confirm": "Passer en ventilation tunnel pendant 20 minutes? À éviter tant que la zone 3 est froide.", "done": "Tunnel · 20 min", "back": "Revenir au minimum"}),
                C("equip", 4, icon="silo", title="Silo de moulée", sub="Moulée de croissance", state="58 % · 6,1 t", tone="gold", rows=[["Consommation", "2,1 t par jour"]],
                  act={"label": "Voir la prévision", "icon": "chart", "preview": True, "text": "Au rythme du lot, le silo sera vide dans environ 3 jours. Commande suggérée demain : aucune commande n’est passée sans votre accord."}),
                C("events", 6, items=[[25, "Aérotherme no 3 en défaut", "Flamme non détectée · zone 3", "warn"], [140, "Pesée automatique", "1,18 kg · 412 poulets pesés", "ok"],
                                      [480, "Ramassage de la mortalité", "12 poulets · inscrit au registre", "ok"]]),
                C("note", 6, icon="info", text="Sources : contrôleur d’ambiance par zone, balances de pesée automatique, compteurs d’eau et de moulée, pesée du silo. Lot de 30 000 poulets · sortie prévue au jour 35."),
            ]],
            ["porcherie", "Porcherie", [
                C("batiment", 12, **FERME_BAT["porcherie"]),
                C("list", 4, icon="barn", title="Maternité", sub="120 places · 112 truies",
                  rows=[["thermo", "Salle", "22,0 °C", "ok"], ["fire", "Nids des porcelets", "30 °C · lampes chauffantes", "ok"], ["wind", "Ammoniac (NH₃)", "8 ppm", "ok"],
                        ["drop", "Abreuvoirs", "Débit normal", "ok"]]),
                C("list", 4, icon="barn", title="Pouponnière", sub="1 100 places · 1 040 porcelets",
                  rows=[["thermo", "Salle", "26,2 °C", "ok"], ["drop", "Abreuvoirs · salle 2", "Débit faible depuis 20 min", "warn"], ["wind", "Ammoniac (NH₃)", "11 ppm", "ok"],
                        ["fan", "Ventilation", "Auto · 30 %", "ok"]]),
                C("list", 4, icon="barn", title="Engraissement", sub="2 400 places · 2 528 porcs en rotation",
                  rows=[["thermo", "Salles", "18,8 à 19,6 °C", "ok"], ["wind", "Ammoniac (NH₃)", "14 ppm · seuil 25", "ok"], ["wind", "H₂S", "0,4 ppm", "ok"],
                        ["fan", "Ventilation", "Auto · 52 %", "ok"]]),
                C("gauge", 4, icon="drop", title="Fosses sous lattes", sub="Niveau moyen · 6 salles", pct=62, value="62 %", est="Vidange vers la fosse dans ≈ 18 jours", estsub="selon le niveau mesuré"),
                C("list", 8, icon="bell", title="Alarmes de la porcherie", sub="Testées chaque semaine · exemple",
                  rows=[["thermo", "Haute température", "Aucune · seuil 30 °C", "ok"], ["fan", "Panne de ventilation", "Aucune", "ok"], ["wind", "H₂S et NH₃", "Sous les seuils", "ok"],
                        ["drop", "Débit des abreuvoirs", "Pouponnière · salle 2 à vérifier", "warn"], ["hydro", "Panne de courant", "Génératrice prête", "ok"]]),
                C("equip", 4, icon="fan", title="Ventilation · engraissement", sub="Contrôleur par salle", state="Auto · 52 %", tone="ok",
                  act={"label": "Forcer à 80 % · 30 min", "icon": "fan", "confirm": "Forcer la ventilation de l’engraissement à 80 % pendant 30 minutes?", "done": "80 % · 30 min", "back": "Revenir en auto"}),
                C("equip", 4, icon="bulb", title="Lampes chauffantes", sub="Maternité · nids des porcelets", state="Actives · 30 °C", tone="ok", toggle={"label": "En marche", "on": "Actives", "off": "Coupées"}),
                C("equip", 4, icon="waves", title="Brassage de la fosse", sub="Avant la vidange · dégage du H₂S", state="Arrêté", tone="muted",
                  act={"label": "Démarrer le brassage", "icon": "play", "confirm": "Démarrer le brassage de la fosse? Le H₂S peut monter rapidement : personne ne doit entrer dans la porcherie pendant le brassage. Ventilation forcée au maximum.", "done": "Brassage en cours · ventilation au maximum", "back": "Arrêter"},
                  note="Action critique · accès interdit pendant le brassage"),
                C("note", 12, icon="info", text="Sources : contrôleurs d’ambiance par salle, sondes NH₃ et H₂S, compteurs d’eau par salle, sondes de niveau des fosses. Toute alarme appelle le responsable de garde, puis le suivant après 10 minutes."),
            ]],
            ["ecurie", "Écurie", [
                C("batiment", 12, **FERME_BAT["ecurie"]),
                C("kpi", 3, icon="thermo", label="Écurie", value="7,2 °C", sub="Humidité 64 % · ventilation naturelle", tone="gold"),
                C("kpi", 3, icon="trough", label="Abreuvoirs chauffés", value="10 / 10", dot="ok", sub="Eau à 8 °C dans chaque box", tone="ok"),
                C("kpi", 3, icon="silo", label="Foin au grenier", value="640 balles", sub="≈ 9 semaines · 10 chevaux", bar=58, tone="gold"),
                C("kpi", 3, icon="fence", label="Porte du paddock", value="Fermée", dot="ok", sub="Chevaux rentrés à 16 h 40", tone="ok"),
                C("list", 7, icon="barn", title="Boxes", sub="12 boxes · 10 chevaux · données d’exemple",
                  rows=[["barn", "Box 1 à 4 · juments", "Occupés · abreuvoirs 8 °C", "ok"], ["barn", "Box 5 à 8 · hongres", "Occupés · abreuvoirs 8 °C", "ok"],
                        ["barn", "Box 9 · poulain", "Occupé · lampe d’appoint", "ok"], ["barn", "Box 10 · étalon", "Occupé · porte renforcée verrouillée", "ok"],
                        ["barn", "Box 11 et 12", "Libres · litière faite", "muted"]]),
                C("list", 5, icon="camera", title="Caméras de l’écurie", sub="Accès : propriétaire et palefrenier",
                  rows=[["camera", "Allée des boxes", "En ligne · aucun mouvement", "ok"], ["camera", "Box de poulinage", "En ligne · vision de nuit", "ok"],
                        ["camera", "Paddock et porte", "En ligne", "ok"], ["camera", "Sellerie", "En ligne · porte verrouillée", "ok"]]),
                C("equip", 4, icon="fence", title="Porte du paddock", sub="Porte motorisée · paddock nord", state="Fermée", tone="ok",
                  act={"label": "Ouvrir", "icon": "up", "confirm": "Ouvrir la porte du paddock? Vérifiez la caméra : aucun cheval ne doit être dans le passage.", "done": "Ouverte", "back": "Fermer"}, note="Confirmation requise"),
                C("equip", 4, icon="trough", title="Abreuvoirs chauffés", sub="10 boxes · résistances 250 W", state="Actifs · 8 °C", tone="ok", toggle={"label": "Chauffage", "on": "Actifs", "off": "Coupés"}),
                C("equip", 4, icon="bulb", title="Éclairage de l’écurie", sub="Allée et boxes", state="Veilleuses", tone="muted", toggle={"label": "Plein éclairage", "on": "Allumé", "off": "Veilleuses"}),
                C("note", 12, icon="info", text="Sources : sondes d’ambiance, capteurs des abreuvoirs, capteur de porte du paddock, inventaire du foin saisi par le palefrenier. Alerte si un abreuvoir descend sous 2 °C."),
            ]],
            ["grains", "Grains et cour", [
                C("batiment", 12, **FERME_BAT["grains"]),
                C("list", 5, icon="silo", title="Silos à grain", sub="Câbles de température dans chaque silo",
                  rows=[["silo", "Silo 1 · maïs", "82 % · 410 t · 4 °C", "ok"], ["silo", "Silo 2 · maïs", "64 % · 320 t · 5 °C", "ok"], ["silo", "Silo 3 · soya", "12 % · 48 t · 6 °C", "ok"],
                        ["thermo", "Point chaud", "Aucun détecté", "ok"]]),
                C("equip", 4, icon="fire", title="Séchoir à grain", sub="Au propane · 25 t/h", state="En marche · maïs à 17,2 %", tone="gold", rows=[["Cible", "15,5 % d’humidité"], ["Propane", "Réservoir à 61 %"]],
                  act={"label": "Arrêter le séchoir", "icon": "power", "confirm": "Arrêter le séchoir à grain? Le grain en cours restera dans la colonne.", "done": "Arrêté", "back": "Redémarrer"}, note="Confirmation requise"),
                C("gauge", 3, icon="drop", title="Fosse à lisier", sub="Fosse circulaire · 4 200 m³", pct=78, value="78 %", est="≈ 140 jours de capacité", estsub="épandage terminé pour la saison"),
                C("equip", 4, icon="garage", title="Entrepôt de machinerie", sub="2 portes · 6 tracteurs et la moissonneuse", state="Portes fermées", tone="ok",
                  act={"label": "Ouvrir la porte est", "icon": "up", "confirm": "Ouvrir la porte est de l’entrepôt de machinerie?", "done": "Ouverte", "back": "Fermer"}),
                C("list", 4, icon="gen", title="Génératrice de secours", sub="150 kW · transfert automatique",
                  rows=[["fuel", "Diesel", "740 L sur 1 000 L", "ok"], ["clock", "Dernier essai en charge", "Lundi · réussi", "ok"], ["bolt", "Priorités", "Ventilation des bâtiments d’abord", "ok"]]),
                C("list", 4, icon="fence", title="Clôtures et puits", sub="Mesures en direct · exemple",
                  rows=[["fence", "Pâturage nord", "7,8 kV", "ok"], ["fence", "Paddock des chevaux", "6,9 kV", "ok"], ["pump", "Puits 1 · étable", "22 m · 3,1 bar", "ok"], ["pump", "Puits 2 · poulaillers", "19 m · 3,0 bar", "ok"]]),
                C("note", 12, icon="info", text="Sources : câbles de température des silos, automate du séchoir, sonde de niveau de la fosse, contrôleur de la génératrice, électrificateurs et pressostats des puits."),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommation par bâtiment", sub="Puissance instantanée · exemple",
                  rows=[["fire", "Séchoir à grain", 6800], ["barn", "Porcherie", 4600], ["barn", "Étable laitière et veaux", 4200], ["milk", "Laiterie · tank et lavage", 3600],
                        ["sparkle", "Pondoir", 2100], ["gauge", "Poulets de chair", 1900], ["fence", "Écurie", 600], ["home", "Résidence et bureau", 900]]),
                C("chips", 12, items=[["gen", "Génératrice", "Prête · essai lundi", "ok"], ["solar", "Source active", "src", "gold"], ["bolt", "Pointe Hydro-Québec", "Demain 6 h – 9 h", "warn"]]),
            ]],
            ["secours", "Génératrice", [
                C("gauge", 5, icon="fuel", title="Diesel de la génératrice", sub="Réservoir de 1 000 L", pct=74, value="740 L", est="≈ 22 h", estsub="à pleine charge, ventilation de tous les bâtiments comprise"),
                C("list", 7, icon="gen", title="Génératrice de secours", sub="150 kW · transfert automatique",
                  rows=[["clock", "Dernier essai en charge", "d:-4 10:00", "ok"], ["gear", "Transfert automatique", "Moins de 10 s après une panne", "ok"],
                        ["bolt", "Charges vitales", "Ventilation des poulaillers et de la porcherie, tank à lait, abreuvoirs", "ok"], ["wrench", "Prochain entretien", "Dans 3 jours", "warn"]]),
                C("packs", 12),
            ]],
            ["pointe", "Pointe Hydro-Québec", [
                C("kpi", 3, icon="bolt", label="Prochaine pointe", value="Demain", sub="De 6 h à 9 h · Hydro-Québec", tone="gold"),
                C("kpi", 3, icon="clock", label="Période actuelle", value="Hors pointe", sub="Crédit hivernal · exemple", tone="ok"),
                C("kpi", 3, icon="leaf", label="Pointes réussies", value="6 / 6", sub="Depuis le 1er décembre dernier", tone="ok"),
                C("kpi", 3, icon="chart", label="Réduction visée", value="−48 kW", sub="Séchoir en pause · animaux jamais touchés", tone="gold"),
                C("list", 7, icon="list", title="Plan pendant la pointe", sub="Rien n’est appliqué sans votre accord",
                  rows=[["fire", "Séchoir à grain", "En pause de 6 h à 9 h", "ok"], ["heater", "Eau de lavage", "Chauffée avant 6 h", "ok"], ["milk", "Tank à lait", "Refroidissement maintenu · jamais délesté", "ok"],
                        ["fan", "Ventilation des bâtiments", "Maintenue · jamais délestée", "ok"], ["gen", "Génératrice", "Disponible si la réduction ne suffit pas", "ok"]]),
                C("list", 5, icon="hydro", title="Hydro-Québec", sub="Données d’exemple",
                  rows=[["clock", "Dernière pointe", "Mardi · 6 h – 9 h"], ["chart", "Réduction obtenue", "−19 kW"], ["bell", "Avis", "La veille, vers 15 h"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="42 kWh", sub="Prévision · pluie", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "60 kWc"], ["compass", "Orientation", "Sud-est"], ["sliders", "Inclinaison", "30°"], ["pin", "Position", "Toits de l’étable et des poulaillers"]]),
                C("solar", 9), C("fwx", 12, cond="Passages nuageux", cloud=40, quality=3, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("list", 7, icon="trough", title="Abreuvoirs par bâtiment", sub="Température de l’eau et débit · exemple",
                  rows=[["trough", "Étable des vaches · rangée 1", "5 °C · 18 L/min", "ok"], ["trough", "Étable des vaches · rangée 2", "5 °C · 17 L/min", "ok"],
                        ["trough", "Pouponnière des veaux", "16 °C · débit normal", "ok"], ["trough", "Taures et génisses", "4 °C · chauffage actif", "ok"],
                        ["sparkle", "Pondoir · pipettes", "4 600 L/jour · normal", "ok"], ["gauge", "Poulets de chair · pipettes", "5 800 L/jour · normal", "ok"],
                        ["barn", "Porcherie · pouponnière, salle 2", "Débit faible depuis 20 min · vérifier", "warn"], ["fence", "Écurie · abreuvoirs chauffés", "8 °C · 10 sur 10", "ok"]]),
                C("pump", 5, icon="pump", title="Puits 1 et 2", sub="Pompes submersibles · étable et poulaillers", state="Disponibles", flow="22 m", pressure="3,1 bar", l1="Niveau", l2="Pression"),
                C("hotwater", 5, title="Eau chaude de lavage", sub="Tank et système de traite", set=75, now=74, min=60, max=85, mode="Lavage après chaque traite et chaque collecte"),
                C("leaks", 7, sensors=[["milk", "Laiterie", "Sec"], ["tap", "Salle de traite", "Sec"], ["sparkle", "Salle d’emballage des œufs", "Sec"], ["pump", "Puits", "Sec"], ["heater", "Chauffe-eau", "Sec"]]),
                C("usage", 6, total=48000, unit="L", seed=17),
                C("equip", 6, icon="valve", title="Vanne principale", sub="Réseau des bâtiments", state="Ouverte", tone="ok",
                  act={"label": "Fermer la vanne", "icon": "x", "confirm": "Fermer la vanne principale? Les abreuvoirs ne seront plus alimentés.", "done": "Fermée", "back": "Ouvrir la vanne"},
                  note="Action critique · le troupeau dépend de l’eau"),
                C("note", 12, icon="info", text="Un débit anormal sur un abreuvoir ou une ligne de pipettes déclenche une alerte après 15 minutes : des animaux sans eau sont une urgence."),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Bâtiments", sub="Portes et accès de la ferme", env="ferme",
                  points=[O("Étable des vaches", "Fermée", "ok", "Bâtiments d’élevage", 70, "Tournée du matin", lock=False, icon="barn"),
                          O("Laiterie", "Fermée · code", "ok", "Bâtiments d’élevage", 210, "Camion de lait", lock=True, icon="milk"),
                          O("Pondoir · sas sanitaire", "Fermé · code", "ok", "Volailles", 50, "Ramassage des œufs", lock=True, icon="door"),
                          O("Poulets de chair · sas sanitaire", "Fermé · code", "ok", "Volailles", 140, "Pesée", lock=True, icon="door"),
                          O("Porcherie · douche d’entrée", "Fermée · code", "ok", "Porcs", 300, "Tournée du matin", lock=True, icon="door"),
                          O("Écurie · porte du paddock", "Fermée", "ok", "Écurie", 140, "Rentrée des chevaux", lock=False, icon="fence"),
                          O("Grange", "Ouverte", "warn", "Bâtiments d’élevage", 35, "Livraison de foin", lock=False, icon="barn"),
                          O("Entrepôt de machinerie", "Fermé", "ok", "Cour", 400, "Philippe", lock=False, icon="garage"),
                          O("Barrière du chemin", "Fermée", "ok", "Cour", 210, "Camion de lait", lock=False, icon="fence")]),
                C("list", 4, icon="bell", title="Alarmes", sub="Testées chaque semaine · exemple",
                  rows=[["smoke", "Incendie · tous les bâtiments", "Normal", "ok"], ["fan", "Ventilation · 6 bâtiments", "Aucune panne", "ok"], ["thermo", "Poulets de chair · zone 3", "25,6 °C · basse", "warn"],
                        ["wind", "H₂S · porcherie", "0,4 ppm", "ok"], ["milk", "Température du tank", "2,8 °C", "ok"], ["gen", "Génératrice", "Prête · aucune alarme", "ok"]]),
                C("cams", 4, items=[], empty="Les caméras d’étable ne sont pas encore reliées.",
                  emptysub="Allées, enclos de vêlage et quai de collecte apparaîtront ici dès leur branchement. Aucune image n’est simulée."),
                C("events", 4, items=[[25, "Aérotherme no 3 en défaut", "Poulets de chair · zone 3", "warn"], [35, "Porte de la grange ouverte", "Chargement de foin", "warn"], [95, "Visiteur inscrit au registre", "Vétérinaire · zone propre", "ok"],
                                      [400, "Traite du matin terminée", "124 vaches · 2 h 05", "ok"], [520, "Collecte du lait", "6 200 L · tank lavé", "ok"]]),
                C("list", 12, icon="shield", title="Accès biosécurité", sub="Registre et zones · données d’exemple",
                  rows=[["users", "Registre des visiteurs", "2 aujourd’hui · vétérinaire, livreur", "ok"], ["key", "Sas des poulaillers et douche de la porcherie", "Code · zone propre", "ok"],
                        ["shield", "Zone propre / zone sale", "Vestiaire et bottes à l’entrée de l’étable", "muted"], ["truck", "Livraisons", "Quai extérieur · hors zone d’élevage", "ok"],
                        ["x", "Accès refusés · 7 derniers jours", "0", "ok"]]),
                C("toggle", 6, icon="shield", key="surv", title="Surveillance des bâtiments", sub="Portes, alarmes et température du lait", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Responsable de garde · cette nuit", on=True),
                C("note", 12, icon="info", text="Couper la clôture, l’eau ou la ventilation demande toujours confirmation : le troupeau en dépend."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · Montérégie", counts=[0, 0, 1, 0, 0],
                  alert={"level": "Avis", "title": "Vents forts", "text": "Rafales jusqu’à 60 km/h demain après-midi · reporter l’épandage et vérifier les rideaux de l’étable.",
                         "src": "Environnement Canada · exemple", "ago": 14, "icon": "wind"}),
                C("danger", 6, title="SOPFEU · Feux et brûlage", level=1, fires="0 feu dans un rayon de 25 km", note="Brûlage agricole : permis municipal", src="SOPFEU · exemple", ago=40),
                C("list", 6, icon="leaf", title="Agriculture · exemple", sub="Indices utiles aux travaux",
                  rows=[["thermo", "Sol à 10 cm", "5 °C", "muted"], ["drop", "Pluie des 7 derniers jours", "18 mm", "muted"], ["wind", "Épandage demain", "Déconseillé · vent", "warn"],
                        ["snowflake", "Gel au sol", "Prévu cette nuit", "warn"]]),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Sans-fil fixe · 50 Mbit/s", icon="antenna", sig="Tour à 6 km", bars=3, down=18, up=4, ping=29, loss="0,6 %"),
                C("meter", 4, icon="doc", title="Forfait rural", used=210, total=400, unit="Go", note="190 Go disponibles · renouvellement le 1er décembre"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["satellite", "Starlink", "Secours prêt", "ok"]]),
                C("devices", 7, total=74, groups=[["cpu", 58, "capteurs et sondes"], ["camera", 8, "caméras"], ["phone", 6, "téléphones"], ["laptop", 2, "ordinateurs"]]),
                C("prio", 5, items=[["antenna", "Sans-fil fixe"], ["satellite", "Starlink"]]),
            ]],
            T_diag([["milk", "Contrôleur de la laiterie", "En ligne", "ok"], ["fan", "Ventilation de l’étable", "En ligne", "ok"], ["gen", "Génératrice", "En ligne", "ok"],
                    ["wind", "Sondes NH₃ et CO₂", "En ligne", "ok"], ["cloud", "Connecteur météo", "À jour", "ok"]],
                   [["milk", "Tank à lait", "Dernière lecture : il y a 20 s", "ok"], ["trough", "Abreuvoirs", "Dernière lecture : il y a 1 min", "ok"],
                    ["wind", "Sondes NH₃ et CO₂", "Dernière lecture : il y a 45 s", "ok"], ["cloud", "Météo", "Dernière lecture : il y a 8 min", "ok"],
                    ["radar", "Capteurs du champ nord", "Batterie faible · il y a 3 h", "warn"]],
                   cpu=12, mem=(1.9, 4), disk=(52, 128)),
        ],
        "equipements": [
            C("equip", 4, icon="milk", title="Tank à lait", sub="Réservoir réfrigéré · 8 000 L", state="2,8 °C", tone="ok",
              rows=[["Volume", "6 400 L"], ["Agitation", "Auto · aux 15 min"], ["Collecte prévue", "Demain 9 h"]],
              spark=[2.8, 2.9, 2.8, 2.7, 2.8, 2.8, 2.9, 2.8, 2.8, 2.7, 2.8, 2.8]),
            C("equip", 4, icon="pump", title="Salon de traite", sub="2 × 8 postes · pompe à vide", state="Arrêté · prochaine traite 17 h", tone="muted",
              act={"label": "Démarrer le lavage", "icon": "drop", "confirm": "Démarrer le cycle de lavage du système de traite (75 °C)?", "done": "Lavage en cours", "back": "Arrêter le lavage"}),
            C("equip", 4, icon="swap", title="Convoyeur à moulée", sub="Alimentation automatisée", state="En cours · ration 3 de 5", tone="gold",
              rows=[["Prochain passage", "15 h 30"]],
              act={"label": "Voir le programme", "icon": "list", "preview": True, "text": "5 rations par jour : 5 h, 9 h, 13 h, 15 h 30 et 19 h. Toute modification du programme demande confirmation."}),
            C("equip", 4, icon="silo", title="Silos", sub="Moulée et ensilage", state="Niveaux suivis", tone="ok",
              rows=[["Silo 1 · moulée", "48 % · ≈ 11 jours"], ["Silo 2 · ensilage", "71 % · ≈ 26 jours"]],
              act={"label": "Voir la prévision", "icon": "chart", "preview": True, "text": "Au rythme actuel, commande de moulée suggérée dans 8 jours. Aucune commande n’est passée sans votre accord."}),
            C("equip", 4, icon="fence", title="Clôtures électriques", sub="Pâturage et enclos", state="7,8 kV", tone="ok",
              rows=[["Pâturage nord", "7,8 kV"], ["Enclos des taures", "7,6 kV"]],
              act={"label": "Couper les clôtures", "icon": "power", "confirm": "Couper les clôtures électriques? Les animaux au pâturage ne seront plus contenus.", "done": "Coupées", "back": "Rétablir"},
              note="Action critique · confirmation requise"),
            C("equip", 4, icon="fire", title="Séchoir à grain", sub="Au propane · 25 t/h", state="En marche · 17,2 %", tone="gold", rows=[["Cible", "15,5 %"]],
              act={"label": "Voir le séchage", "icon": "chart", "preview": True, "text": "Maïs entré à 24 %, sortie à 15,5 %. Fin estimée ce soir vers 22 h selon le débit actuel. L’arrêt se commande dans Grains et cour, avec confirmation."}),
            C("equip", 4, icon="barn", title="Portes de grange", sub="Porte principale et quai", state="Grange ouverte", tone="warn",
              rows=[["Quai de collecte", "Fermé"]],
              act={"label": "Fermer la grange", "icon": "down", "confirm": "Fermer la porte de la grange? Vérifiez qu’aucun tracteur n’est dans le passage.", "done": "Fermée", "back": "Ouvrir"}),
            C("equip", 4, icon="gen", title="Génératrice", sub="Diesel · 150 kW · transfert automatique", state="Prête · 740 L", tone="ok",
              act={"label": "Lancer un essai à vide", "icon": "power", "confirm": "Lancer un essai à vide de 15 minutes? Le réseau reste branché; aucun bâtiment n’est transféré.", "done": "Essai en cours · 15 min", "back": "Arrêter l’essai"}),
            C("inspection", 12, title="Prochain entretien", sub="Génératrice · vidange et essai en charge", d=3, go="voyage:entretien"),
        ],
        "voyage": [
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Traites, collectes et visites", l2="Entretien (génératrice, sondes, tank)",
                  events=[[-1, "05:00", "07:10", "Traite du matin", "event"], [0, "17:00", "19:00", "Traite du soir", "event"], [1, "09:00", "10:00", "Collecte du lait", "event"],
                          [2, "10:00", "11:00", "Vétérinaire · suivi du troupeau", "maint"], [3, "13:00", "15:00", "Génératrice · essai en charge", "maint"],
                          [4, "07:00", "09:00", "Livraison de moulée · pondoir et poulets", "event"], [5, "09:00", "10:00", "Calibration des sondes", "maint"],
                          [11, "05:00", "09:00", "Sortie du lot de poulets", "event"]]),
                C("next", 4, icon="milk", kick="Prochaine traite", title="Traite du soir", d=0, h="17:00", countdown=True),
                C("next", 4, icon="truck", kick="Collecte", title="Camion de lait", d=1, h="09:00"),
                C("next", 4, icon="users", kick="Visite", title="Vétérinaire · suivi du troupeau", d=2, h="10:00"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes de la ferme", sub="Les routines qui protègent le troupeau.", lists=[
                    {"k": "soir", "l": "Tournée du soir", "sub": "Après la traite.", "icon": "moon",
                     "items": [["Lavage du système de traite", "", False], ["Œufs ramassés", "Compteur du convoyeur", True], ["Poulets · mortalité ramassée", "", True],
                               ["Abreuvoirs vérifiés", "", True], ["Chevaux rentrés", "Capteur du paddock", True], ["Clôtures électriques", "7,8 kV", True], ["Portes fermées", "", False]]},
                    {"k": "biosecurite", "l": "Biosécurité", "sub": "À chaque visite.", "icon": "shield",
                     "items": [["Registre signé à l’entrée", "", True], ["Bottes et survêtement fournis", "", True], ["Lavage des bottes à la sortie", "", False], ["Véhicule hors zone d’élevage", "", True]]},
                    {"k": "hiver", "l": "Hiver", "sub": "Avant le gel.", "icon": "snowflake",
                     "items": [["Abreuvoirs du pâturage hivernisés", "", True], ["Rideaux de l’étable réglés", "", True], ["Diesel de la génératrice", "74 %", True], ["Entretien de la génératrice", "", False]]},
                    {"k": "achats", "l": "Achats", "sub": "Coopérative.", "icon": "cart",
                     "items": [["Minéraux", "", False], ["Litière", "", True], ["Manchons de trayeuse", "", False], ["Copeaux pour le poulailler", "", False], ["Foin · 200 balles", "Écurie", False]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("gen", "Génératrice · essai en charge et vidange", "Contrat d’entretien · exemple",
                      compteur("Compteur d’heures de la génératrice", "aux 250 heures", 241, 250, 3, "h")),
                    M("milk", "Lavage acide du tank à lait", "Cycle complet le dimanche",
                      fab("Manuel du tank à lait", "chaque semaine", 7, -5)),
                    M("sliders", "Calibration des sondes", "Température, NH₃ et CO₂",
                      fab("Manuel des sondes d’ambiance", "aux 6 mois", 182, -177)),
                    M("fan", "Ventilateurs · nettoyage des pales", "Poussière et efficacité",
                      src_fixe("capteur", "Courant des moteurs de ventilation", -3, "Consommation en hausse de 12 % : pales encrassées")),
                    M("milk", "Manchons de la trayeuse", "Remplacement",
                      compteur("Compteur de traites de la trayeuse", "aux 2 500 traites", 2210, 2500, 24, "traites")),
                    M("fence", "Clôtures · isolateurs et tension", "Avant l’hiver",
                      src_fixe("saison", "Saison · avant le gel du sol", 30)),
                    M("fire", "Aérothermes des poulets de chair", "Nettoyage et allumeurs",
                      src_fixe("capteur", "Contrôleur d’ambiance · défaut de flamme", 1, "Aérotherme no 3 en défaut aujourd’hui")),
                    M("waves", "Fosses de la porcherie", "Vidange vers la fosse extérieure",
                      src_fixe("capteur", "Sondes de niveau des fosses", 18, "Niveau moyen à 62 %")),
                ]),
                C("next", 4, icon="gen", kick="Prochain entretien", title="Génératrice · essai en charge", d=3, h="13:00"),
                C("next", 4, icon="fan", kick="En retard", title="Ventilateurs de l’étable", text="Nettoyage des pales prévu il y a 3 jours."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="traite", items=[
                    {"k": "traite", "icon": "milk", "label": "Traite", "sub": "Deux fois par jour",
                     "fx": [["milk", "Pompe à vide", "Démarrage", "En marche", "crit"], ["heater", "Eau de lavage", "Préchauffage", "75 °C"],
                            ["bulb", "Éclairage", "Salle de traite", "Lecture", "light", "lecture"], ["fan", "Ventilation", "Salle de traite", "60 %", "fail"]],
                     "autos": [["clock", "5 h et 17 h", "Propose le mode Traite"]]},
                    {"k": "nuit", "icon": "moon", "label": "Nuit", "sub": "Repos du troupeau",
                     "fx": [["bulb", "Éclairage", "Veilleuses rouges", "Nuit douce", "light", "nuit-douce"], ["barn", "Portes", "Fermeture", "Fermées", "crit"],
                            ["bell", "Alertes", "Responsable de garde", "Activées"], ["fan", "Ventilation", "Minimum", "25 %"]],
                     "autos": [["clock", "À 21 h", "Propose le mode Nuit"]]},
                    {"k": "canicule", "icon": "sun", "label": "Canicule", "sub": "Protéger du stress thermique",
                     "fx": [["fan", "Ventilation", "Tunnel dans les poulaillers · maximum ailleurs", "100 %"], ["drop", "Brumisation", "Étable et porcherie · cycles de 3 minutes", "Activée", "crit"],
                            ["blinds", "Rideaux", "Grand ouverts", "Ouverts"], ["trough", "Abreuvoirs", "Débit maximum", "Maximum"]],
                     "autos": [["thermo", "Indice de stress thermique", "Propose le mode Canicule"]]},
                    {"k": "panne", "icon": "gen", "label": "Panne de courant", "sub": "Le troupeau d’abord",
                     "fx": [["gen", "Génératrice", "Transfert automatique", "Démarrée", "crit"], ["fan", "Ventilation", "Priorité absolue", "Maintenue"],
                            ["milk", "Tank à lait", "Refroidissement maintenu", "Maintenu"], ["clip", "Liste de vérification", "Envoyée au responsable", "8 points"],
                            ["bulb", "Éclairage", "Réduit aux allées", "30 %", "fail"]],
                     "autos": [["hydro", "Perte du réseau", "Lance le mode Panne de courant"]]},
                    {"k": "biosecurite", "icon": "shield", "label": "Biosécurité renforcée", "sub": "Visites restreintes",
                     "fx": [["key", "Accès", "Visiteurs essentiels seulement", "Restreints", "crit"], ["users", "Registre", "Obligatoire à chaque entrée", "Activé"],
                            ["truck", "Livraisons", "Quai extérieur seulement", "Déviées"], ["bell", "Équipe", "Avis envoyé à l’équipe", "Avisée"]],
                     "autos": [["warn", "Avis sanitaire du secteur", "Propose la biosécurité renforcée"]]},
                ], scenarios=[["Panne de courant", "Génératrice, ventilation et lait d’abord"], ["Vêlage", "Éclairage de l’enclos et alerte à l’équipe"], ["Collecte du lait", "Barrière et quai ouverts au camion"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["milk", "Lait au-dessus de 4 °C", "Alerte immédiate au responsable de garde", "Température du tank", True],
                                     ["fan", "Panne de ventilation", "Alarme, génératrice et rappel aux 10 minutes", "Perte de débit d’air", True],
                                     ["hydro", "Panne de courant", "Transfert sur la génératrice en moins de 10 s", "Perte du réseau", True],
                                     ["trough", "Débit d’eau anormal", "Alerte si un abreuvoir coule plus de 15 min", "Débitmètre", True],
                                     ["wind", "NH₃ au-dessus de 20 ppm", "Ventilation forcée et alerte", "Sonde d’ammoniac", True],
                                     ["fence", "Clôture sous 5 kV", "Alerte au responsable", "Tension de la clôture", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[20, "Système", "Ration 3 de 5 distribuée · convoyeur à moulée"], [95, "Luc", "Visiteur inscrit au registre · vétérinaire"],
                                        [400, "Système", "Mode Traite appliqué · 3 / 4 effets confirmés · ventilation à vérifier"],
                                        [520, "Système", "Collecte du lait · 6 200 L · lavage du tank terminé"],
                                        [5800, "Système", "Essai en charge de la génératrice réussi · 20 min"]]),
            ]],
        ],
    },
}


# =============================================================================================
# Bateau · yacht à moteur de 52 pieds (deux moteurs diesel, génératrice, annexe) à la marina de Sorel-Tracy
# =============================================================================================

FLEUVE = {
    "km": 20, "note": "Fleuve illustratif",
    "water": [[[0, 150], [60, 128], [120, 112], [180, 96], [240, 76], [300, 58], [360, 40], [400, 30], [400, 0], [330, 0], [270, 18], [210, 36],
               [150, 54], [90, 72], [40, 92], [0, 104]],
              [[150, 140], [168, 120], [176, 100], [190, 98], [186, 124], [170, 150], [158, 180], [150, 240], [136, 240], [140, 190]]],
    "roads": [{"pts": [[0, 176], [80, 160], [140, 150], [190, 130], [260, 104], [340, 84], [400, 72]], "n": "132", "at": [300, 100]},
              {"pts": [[188, 136], [204, 190], [214, 240]], "minor": True}],
    "towns": [[178, 92, "Sorel-Tracy", "l"], [88, 130, "Contrecœur", "b"], [330, 28, "Lac Saint-Pierre", "a"]],
    "labels": [[110, 92, "Fleuve Saint-Laurent", "water"], [176, 200, "Rivière Richelieu", "water"], [250, 46, "Îles de Sorel", "water"]],
    "me": [184, 104],
}

BATEAU_POINTS = [
    {"n": 1, "x": 198, "y": 94, "kind": "carburant", "name": "Poste d’essence de la marina", "what": "Carburant", "dist": "0,3 km", "info": "Ouvert jusqu’au 15 novembre (exemple)"},
    {"n": 2, "x": 170, "y": 114, "kind": "vidange", "name": "Station de pompage", "what": "Vidange des eaux usées", "dist": "0,4 km", "info": "Gratuite pour les membres (exemple)"},
    {"n": 3, "x": 214, "y": 86, "kind": "eau", "name": "Quai municipal", "what": "Eau potable", "dist": "1,8 km", "info": "Fermée après la saison (exemple)"},
    {"n": 4, "x": 90, "y": 126, "kind": "service", "name": "Chantier d’hivernage", "what": "Sortie de l’eau", "dist": "18 km", "info": "Réservation confirmée (exemple)"},
]

BATEAU = {
    "key": "bateau", "name": "Yacht", "kind": "Yacht à moteur de 52 pieds", "place": "Sorel-Tracy · fleuve Saint-Laurent", "icon": "boat", "meIcon": "boat",
    "mobile": True, "points": BATEAU_POINTS,
    "geo": {"lat": 46.04, "lon": -73.12, "place": "Marina de Sorel-Tracy"},
    "banner": photo_ou_attente("bateau", "Le yacht à moteur de 52 pieds amarré au quai de la marina", "50% 55%"),
    "titles": {"voyage": "Navigation et entretien", "eau": "Eau et réservoirs"}, "voyageIcon": "anchor",
    "subs": {"apercu": "Le yacht au quai, prêt pour la dernière sortie.", "confort": "Salon, cabines, humidité et météo du fleuve.",
             "energie": "Quai, génératrice, alternateurs, solaire et batteries.", "eau": "Eau douce, eaux noires, carburant et cale.",
             "securite": "Ouvertures, cale et météo maritime.", "internet": "Wi-Fi de la marina, LTE et satellite.",
             "equipements": "Guindeau, cale, quai, génératrice et annexe.", "voyage": "Convoyage, hivernage et entretien.",
             "modes": "Au quai, navigation, mouillage, hivernage."},
    "status": [["battery", "Batteries", "86 %", "ok"], ["anchor", "Amarrage", "Au quai", "ok"], ["wind", "Vent", "24 km/h", "gold"]],
    "maps": {"fleuve": FLEUVE},
    "wx": wx([1, 0, 0, -1, -1, -1, 0, 1, 3, 4, 6, 7, 7, 7, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1],
             "ddddddppppcccccppddddddd", "000000000111222100000000",
             [["cloudsun", 7, -1, 20], ["rain", 8, 2, 70], ["cloud", 5, 0, 40], ["sun", 4, -2, 0], ["snow", 2, -3, 40]],
             hum=78, dew=-1, wind=24, dir="Sud-ouest", gust=40, vis=24, hpa=1016, trend="En baisse", uv=1, cas=2),
    "energy": {"unit": "Ah", "cap": 800, "nominal": "25,6 V", "chem": "LiFePO₄", "soc": 86, "v": "26,6 V", "reserve": 20, "load": 640, "battW": 120,
               "packs": [{"name": "Batterie de service A", "cap": 400, "soc": 87, "v": 26.62, "a": 2.4, "t": 6.8, "cycles": 112, "hi": 3.329, "lo": 3.324},
                         {"name": "Batterie de service B", "cap": 400, "soc": 85, "v": 26.60, "a": 2.2, "t": 7.1, "cycles": 115, "hi": 3.328, "lo": 3.322}],
               "sources": [["quai", "Quai · 2 × 50 A", "plug", "grid"], ["gen", "Génératrice · 13,5 kW", "gen", 0, "en veille"], ["alt", "Alternateurs", "alt", 0], ["solaire", "Solaire · 800 W", "sun", "solar"]],
               "store": "Batteries", "loads": "Bord", "packsTitle": "Batteries de service",
               "solar": {"peak": 800, "cloud": .4, "base": 520, "eve": 760, "morn": .2}},
    "s": {
        "apercu": [
            C("kpi", 3, icon="battery", label="Batteries de service", value="86 %", sub="Branché au quai · en charge", bar=86, tone="bat", go="energie"),
            C("kpi", 3, icon="drop", label="Eau douce", value="40 %", sub="240 sur 600 L", bar=40, tone="water", go="eau"),
            C("kpi", 3, icon="pump", label="Cales", value="Sèches", dot="ok", sub="3 pompes auto · 0 cycle en 24 h", subicon="pump", tone="ok", go="eau"),
            C("kpi", 3, icon="wifi", label="Internet", value="Wi-Fi", dot="ok", sub="Marina · LTE en secours", subicon="antenna", tone="ok", go="internet"),
            C("conditions", 7, title="Conditions au quai"),
            C("lumieres", 5),
            C("around", 7, title="Autour du yacht", map="fleuve", view=[146, 76, 80, 48], pins="points",
              list=[["fuel", "muted", "Carburant", "Poste de la marina · 0,3 km"], ["dump", "ok", "Pompage des eaux usées", "0,4 km"], ["anchor", "gold", "Chantier d’hivernage", "18 km"]],
              btn=["Points de service", "eau:points"]),
            C("checklist", 5, id="sortie", title="Préparer la sortie", icon="clip",
              items=[["Météo maritime consultée", True], ["Gilets et fusées à bord", True], ["Alimentation de quai débranchée", False], ["Moteurs réchauffés", False]]),
            C("upcoming", 7, title="Prochaines 48 heures", icon="wind", note="Avis de vent fort cet après-midi.", text="Sud-ouest 20 nœuds en rafales · reporter le convoyage à demain matin.", go="securite:alertes"),
            C("trip", 5, title="Mon convoyage", name="Vers le chantier d’hivernage", next="Sortie de l’eau dans quelques jours", go="voyage"),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Salon et cabines", sub="Climatisation réversible · 4 zones", set=14, min=5, max=22, inside=13,
                  rows=[["boat", "Salon", "13 °C"], ["bed", "Cabine du propriétaire", "13 °C"], ["fire", "Chauffage", "Réversible · alimentation de quai"], ["drop", "Humidité", "Déshumidificateur actif"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température du salon", "value": "13 °C", "state": "Stable", "tone": "ok", "c": "gold",
                     "pts": [12.0, 12.3, 12.6, 13.0, 13.2, 13.1, 13.0, 12.9, 13.0, 13.1, 13.0, 13.0], "min": 0, "max": 24},
                    {"icon": "drop", "title": "Humidité", "value": "64 %", "state": "En baisse", "tone": "ok", "c": "blue",
                     "pts": [78, 76, 74, 72, 70, 69, 68, 67, 66, 65, 64, 64], "min": 30, "max": 95}]),
                C("ventilation", 3, speed=1, max=4, rows=[["fan", "Aérateurs", "Solaires · actifs"]]),
                C("air", 3, title="Air du salon", co2=520, quality="Bonne qualité", rows=[["co", "CO", "0 ppm"], ["drop", "Humidité", "64 %"], ["flame", "Propane", "Aucun"]]),
                C("outside", 3),
                C("cold", 3, icon="fridge", title="Froid et fleuve", sub="Températures actuelles", rows=[["fridge", "Cave à vin", "12 °C"], ["fridge", "Réfrigérateur", "4 °C"], ["waves", "Eau du fleuve", "6 °C"]]),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["fire", "Climatisation réversible", 380], ["heater", "Déshumidificateurs", 120], ["fridge", "Réfrigérateur et cave à vin", 80], ["radar", "Électronique de bord", 40], ["bulb", "Éclairage", 18], ["pump", "Pompes de cale (veille)", 2]]),
                C("chips", 12, items=[["plug", "Alimentation de quai", "Branchée · 2 × 50 A", "ok"], ["gen", "Génératrice", "Prête · 1 240 h", "ok"], ["battery", "Batteries des moteurs", "24,8 V", "ok"]]),
            ]],
            ["batterie", "Batteries", [
                C("packs", 8),
                C("list", 4, icon="shield", title="Protection des batteries", sub="Système de gestion (BMS)",
                  rows=[["check", "Charge autorisée", "Oui", "ok"], ["check", "Décharge autorisée", "Oui", "ok"], ["battery", "Batteries des moteurs", "24,8 V · séparées", "ok"], ["bell", "Alarme", "Aucune", "ok"]]),
            ]],
            ["prevision", "Prévision solaire", [
                C("kpi", 3, icon="sun", label="Aujourd’hui", value="solar:today", sub="Prévision · production solaire", tone="gold"),
                C("kpi", 3, icon="calendar", label="Demain", value="0,9 kWh", sub="Prévision · pluie", tone="gold"),
                C("kpi", 3, icon="chart", label="Produit jusqu’ici", value="solar:sofar", sub="Mesure d’exemple", tone="gold"),
                C("list", 3, h=2, icon="gear", title="Installation déclarée",
                  rows=[["bolt", "Puissance", "800 Wc"], ["compass", "Orientation", "Hardtop · variable"], ["sliders", "Inclinaison", "0°"], ["pin", "Position", "Marina de Sorel"]]),
                C("solar", 9), C("fwx", 12, cond="Passages nuageux", cloud=45, quality=2, src="Scénario météo d’exemple"),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("tanks", 7, items=[["Eau douce", 40, 600, "clean"], ["Eaux noires", 55, 300, "black"], ["Diesel", 70, 2800, "fuel"]]),
                C("pump", 5, icon="pump", title="Pompes de cale", sub="3 pompes automatiques · flotteurs", state="Prêtes · cales sèches", flow="0 cycle", pressure="Sec",
                  l1="Cycles · 24 h", l2="Fond de cale"),
                C("leaks", 4, sensors=[["drop", "Cale avant", "Sec"], ["engine", "Salle des moteurs", "Sec"], ["waves", "Presse-étoupes", "Sec"], ["gen", "Génératrice", "Sec"]]),
                C("gauge", 4, icon="fuel", title="Diesel", sub="Moteurs et génératrice", pct=70, value="1 960 / 2 800 L", est="≈ 9 h de route", estsub="à 18 nœuds, réserve de 20 % comprise"),
                C("fill", 4, map="fleuve", point=2, title="Pompage des eaux usées"),
            ]],
            ["points", "Points de service", [
                C("levels", 12, items=[["Eau douce", 40, 600, "clean"], ["Eaux noires", 55, 300, "black"], ["Diesel", 70, 2800, "fuel"]]),
                C("points", 12, map="fleuve", view=[60, 50, 200, 120], filters=[["tous", "Tous"], ["eau", "Eau"], ["vidange", "Pompage"], ["carburant", "Carburant"]]),
                C("note", 12, icon="info", text="Source : exemple. Plusieurs services ferment après la saison : confirmer par radio VHF ou par téléphone avant de s’y rendre."),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Ouvertures", sub="Accès du yacht", env="bateau",
                  points=[O("Porte vitrée du salon", "Verrouillée", "ok", "Cockpit", 160, "James", lock=True, icon="door"),
                          O("Écoutille avant", "Fermée", "ok", "Pont", 3000, "", icon="window"),
                          O("Garage de l’annexe", "Fermé", "ok", "Plateforme de bain", 170, "James", lock=False, icon="box"),
                          O("Baille à mouillage", "Fermée", "ok", "Pont", 5800, "", icon="anchor"),
                          O("Hublot de la cabine du propriétaire", "Entrouvert", "warn", "Cabines", 400, "Aération de la cabine", icon="window")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs à bord",
                  rows=[["co", "Monoxyde de carbone · génératrice", "0 ppm", "ok"], ["smoke", "Fumée · salle des moteurs", "Normal", "ok"], ["drop", "Eau dans les cales", "Sec", "ok"],
                        ["anchor", "Alarme de mouillage", "Au quai · inactive", "muted"]]),
                C("cams", 4, items=[], empty="Les caméras du cockpit et de la salle des moteurs ne sont pas encore reliées.", emptysub="Elle apparaîtra ici dès son branchement. Aucune image n’est simulée."),
                C("events", 4, items=[[30, "Alimentation de quai rétablie", "Après une coupure de 2 min", "gold"], [160, "Porte du salon verrouillée", "Par James", "ok"],
                                      [400, "Hublot de la cabine entrouvert", "Aération de la cabine", "warn"], [1500, "Pompes de cale · test", "Réussi", "ok"]]),
                C("toggle", 6, icon="shield", key="surv", title="Surveillance du yacht", sub="Ouvertures, cales et quai", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Cale et coupure de quai", on=True),
                C("note", 12, icon="info", text="En navigation, les commandes d’ouverture sont verrouillées. Toute commande critique demande confirmation."),
            ]],
            ["alertes", "Alertes extérieures", [
                C("ec", 12, title="Météo · secteur de Sorel", counts=[0, 0, 1, 0, 0],
                  alert={"level": "Avis", "title": "Vents forts sur le fleuve", "text": "Sud-ouest 15 à 20 nœuds, rafales à 25 cet après-midi · reporter les sorties.",
                         "src": "Environnement Canada · exemple", "ago": 18, "icon": "wind"}),
                C("list", 6, icon="waves", title="Prévisions maritimes · exemple", sub="Fleuve Saint-Laurent, secteur de Sorel",
                  rows=[["wind", "Vent", "Sud-ouest 15 à 20 nœuds", "warn"], ["waves", "Vagues", "0,5 à 1 m", "muted"], ["eye", "Visibilité", "Bonne", "ok"],
                        ["warn", "Avertissement", "Vent fort cet après-midi", "warn"]]),
                C("list", 6, icon="waves", title="Niveau d’eau · exemple", sub="Pêches et Océans Canada",
                  rows=[["waves", "Niveau à Sorel", "5,1 m · sous la moyenne", "warn"], ["chart", "Tendance", "Baisse de 4 cm par jour", "muted"],
                        ["anchor", "Bouées de balisage", "Retrait en cours pour l’hiver", "warn"]]),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Wi-Fi de la marina", icon="wifi", dbm=-67, bars=3, down=12, up=3, ping=34, loss="1,1 %"),
                C("meter", 4, icon="doc", title="Forfait LTE", used=9, total=30, unit="Go", note="21 Go disponibles · renouvellement le 1er décembre"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["antenna", "LTE", "Secours prêt", "ok"], ["satellite", "Starlink Maritime", "Prêt · en veille", "ok"]]),
                C("devices", 7, total=14, groups=[["phone", 4, "téléphones"], ["laptop", 2, "tablettes"], ["tv", 2, "téléviseurs"], ["radar", 5, "électronique de bord"], ["cpu", 1, "Hub JARVIS"]]),
                C("prio", 5, items=[["wifi", "Wi-Fi de la marina"], ["satellite", "Starlink Maritime"], ["antenna", "LTE"]]),
            ]],
            T_diag([["radar", "Électronique de bord (NMEA 2000)", "En ligne", "ok"], ["pump", "Pompe de cale", "En ligne", "ok"], ["waves", "Niveaux d’eau", "À jour", "ok"]],
                   [["drop", "Cale", "Dernière lecture : il y a 10 s", "ok"], ["battery", "Batteries", "Dernière lecture : il y a 15 s", "ok"],
                    ["waves", "Niveaux d’eau", "Dernière lecture : il y a 1 h", "ok"], ["cloud", "Météo maritime", "Dernière lecture : il y a 18 min", "ok"]],
                   cpu=8, mem=(1.1, 4), disk=(12, 64)),
        ],
        "equipements": [
            C("status", 12, moving=True, still="Au quai · amarré", ok="Commandes disponibles", lock="Commandes verrouillées en navigation", moveLabel="En navigation"),
            C("equip", 4, icon="anchor", title="Guindeau", sub="Ancre de 35 kg · 60 m de chaîne", state="Ancre remontée", tone="ok",
              act={"label": "Descendre l’ancre", "icon": "down", "confirm": "Descendre l’ancre? À utiliser seulement au mouillage, jamais au quai.", "done": "Ancre au fond", "back": "Remonter l’ancre"},
              note="Confirmation requise"),
            C("equip", 4, icon="pump", title="Pompes de cale", sub="3 pompes automatiques", state="Prêtes", tone="ok", rows=[["Cycles · 24 h", "0"]],
              act={"label": "Tester les pompes", "icon": "play", "confirm": "Faire tourner les pompes de cale pendant 10 secondes?", "done": "Test réussi", "back": "Tester à nouveau"}),
            C("equip", 4, icon="plug", title="Alimentation de quai", sub="2 × 50 A · 240 V", state="Branchée", tone="ok",
              act={"label": "Passer sur batteries", "icon": "battery", "confirm": "Couper l’alimentation de quai? Le bord passera sur les batteries de service.", "done": "Sur batteries",
                   "back": "Rebrancher le quai", "moving": True}),
            C("equip", 4, icon="bulb", title="Feux de navigation", sub="Mât radar et côtés", state="Éteints", tone="muted", toggle={"label": "Allumer", "on": "Allumés", "off": "Éteints"}),
            C("equip", 4, icon="fire", title="Climatisation réversible", sub="4 zones · salon et cabines", state="14 °C", tone="ok", rows=[["Source", "Quai ou génératrice"]]),
            C("equip", 4, icon="gen", title="Génératrice", sub="Diesel · 13,5 kW", state="En veille · 1 240 h", tone="ok", rows=[["Démarrage", "Auto si le quai coupe"]],
              act={"label": "Démarrer", "icon": "power", "confirm": "Démarrer la génératrice? Vérifiez que la prise d’eau de mer est ouverte.", "done": "En marche · 13,5 kW", "back": "Arrêter"},
              note="Confirmation requise"),
            C("equip", 4, icon="boat", title="Annexe", sub="Semi-rigide 3,4 m · bossoir de la plateforme", state="Rangée au garage", tone="ok", rows=[["Moteur hors-bord", "20 ch · plein fait"]],
              act={"label": "Mettre à l’eau", "icon": "down", "confirm": "Abaisser la plateforme et mettre l’annexe à l’eau? Vérifiez qu’aucun baigneur n’est derrière.", "done": "À l’eau", "back": "Remonter l’annexe", "moving": True},
              note="Confirmation requise"),
            C("list", 4, icon="door", title="Ouvertures techniques", sub="Coffres et trappes",
              rows=[["box", "Coffres de cockpit", "Fermés", "ok"], ["fuel", "Nable de carburant", "Fermé", "ok"], ["drop", "Nable d’eau", "Fermé", "ok"]]),
            C("inspection", 12, title="Prochaine étape", sub="Sortie de l’eau et hivernage au chantier", d=7, go="voyage:entretien"),
        ],
        "voyage": [
            ["voyage", "Convoyage", [
                C("trip", 8, big=True, title="Convoyage lié", name="Vers le chantier d’hivernage", next="Prochaine étape · sortie de l’eau",
                  dist="18 km", dur="40 min à 15 nœuds", map="fleuve", view=[40, 40, 240, 144],
                  route={"next": [[184, 104], [160, 104], [130, 110], [104, 117], [90, 126]]}),
                C("arrival", 4, place="Chantier d’hivernage", temp=6, icon="cloud", cond="Nuageux", wind="Vent sud-ouest 12 nœuds"),
                C("list", 6, icon="warn", title="Avis aux navigateurs", sub="Exemple · à vérifier",
                  rows=[["anchor", "Bouées retirées pour l’hiver", "Chenal secondaire", "warn"], ["waves", "Niveau d’eau bas", "Prudence près des îles", "warn"]],
                  note="Consulter les avis officiels avant de partir."),
                C("list", 6, icon="clip", title="Avant de partir",
                  rows=[["waves", "Météo maritime : vent sous 15 nœuds", "", "", True], ["fuel", "Carburant : 70 % · suffisant", "", "", True], ["users", "Équipier confirmé", "", "", True]]),
            ]],
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Sorties et réservations", l2="Entretien (chantier, rappels)",
                  events=[[-2, "13:00", "16:00", "Dernière sortie", "event"], [1, "09:00", "11:00", "Convoyage", "event"], [7, "09:00", "12:00", "Sortie de l’eau", "maint"],
                          [3, "10:00", "11:00", "Pompage des eaux usées", "maint"]]),
                C("next", 4, icon="boat", kick="Convoyage", title="Vers le chantier", d=1, h="09:00", countdown=True),
                C("next", 4, icon="anchor", kick="Chantier", title="Sortie de l’eau", d=7, h="09:00"),
                C("next", 4, icon="dump", kick="À faire", title="Pompage des eaux usées", d=3, h="10:00"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes de bord", sub="Naviguer et hiverner l’esprit tranquille.", lists=[
                    {"k": "sortie", "l": "Sortie", "sub": "Avant de larguer les amarres.", "icon": "boat",
                     "items": [["Météo maritime", "Vent sous 15 nœuds", True], ["Gilets et fusées", "", True], ["Débrancher le quai", "", False], ["Réchauffer les moteurs", "5 minutes", False], ["VHF canal 16", "", False]]},
                    {"k": "hivernage", "l": "Hivernage", "sub": "Avant la sortie de l’eau.", "icon": "snowflake",
                     "items": [["Vider l’eau douce", "", False], ["Antigel dans les circuits", "", False], ["Pomper les eaux noires", "", False], ["Retirer l’électronique", "", False], ["Annexe hivernée", "", True]]},
                    {"k": "entretien", "l": "Entretien", "sub": "Contrôles réguliers.", "icon": "wrench",
                     "items": [["Anodes", "", True], ["Courroies d’alternateur", "", True], ["Huile des moteurs", "", False], ["Filtres de la génératrice", "", False]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("anchor", "Sortie de l’eau et hivernage", "Chantier d’exemple",
                      src_fixe("saison", "Saison de navigation · eau à 6 °C", 7, "Rendez-vous du chantier confirmé")),
                    M("engine", "Hivernage des moteurs", "Deux moteurs diesel · antigel et huile",
                      compteur("Compteur d’heures des moteurs", "aux 250 heures ou à l’hivernage", 238, 250, 1.6, "h")),
                    M("drop", "Anodes", "Remplacement annuel",
                      fab("Manuel des moteurs et des hélices", "aux 12 mois", 365, -205)),
                    M("waves", "Peinture antisalissure", "Au printemps",
                      src_fixe("saison", "Saison · avant la mise à l’eau", 170)),
                    M("shield", "Fusées de détresse", "Expirent en mai",
                      src_fixe("regle", "Règlement sur les petits bâtiments · date de péremption", 190)),
                ]),
                C("next", 4, icon="anchor", kick="Prochain rendez-vous", title="Sortie de l’eau", d=7, h="09:00"),
                C("next", 4, icon="engine", kick="Avec le chantier", title="Hivernage des moteurs", text="Antigel, huile et filtres au moment de la sortie."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="quai", items=[
                    {"k": "quai", "icon": "plug", "label": "Au quai", "sub": "Branché et surveillé",
                     "fx": [["plug", "Alimentation", "Quai · 30 A", "Branchée"], ["heater", "Déshumidificateur", "Actif", "Actif"], ["shield", "Surveillance", "Cale et ouvertures", "Activée", "crit"],
                            ["bulb", "Éclairage", "Cockpit le soir", "Lecture", "light", "lecture"]],
                     "autos": [["plug", "Coupure de quai", "Alerte immédiate"]]},
                    {"k": "navigation", "icon": "boat", "label": "Navigation", "sub": "En route",
                     "fx": [["bulb", "Feux de navigation", "Au coucher du soleil", "Auto"], ["lock", "Commandes", "Verrouillées en navigation", "Verrouillées", "crit"],
                            ["radar", "Électronique", "Traceurs, radar et AIS", "Allumés", "fail"], ["gen", "Génératrice", "Au besoin", "Auto"]],
                     "autos": [["wind", "Rafales au-dessus de 25 nœuds", "Alerte à la barre"]]},
                    {"k": "mouillage", "icon": "anchor", "label": "Mouillage", "sub": "À l’ancre",
                     "fx": [["anchor", "Alarme de mouillage", "Rayon de 40 m", "Armée", "crit"], ["bulb", "Feu de mouillage", "Tête de mât", "Allumé"],
                            ["bulb", "Cabine", "Ambiance de soirée", "Nuit douce", "light", "nuit-douce"], ["battery", "Batteries", "Surveillance de la décharge", "Seuil 40 %"]],
                     "autos": [["anchor", "Dérive de l’ancre", "Alerte et position"]]},
                    {"k": "hivernage", "icon": "snowflake", "label": "Hivernage", "sub": "Au chantier",
                     "fx": [["drop", "Eau", "Circuits vidés", "Purgés", "crit"], ["battery", "Batteries", "Stockage à 60 %", "Stockage"],
                            ["wifi", "Connexion", "Vérification hebdomadaire", "1 fois par semaine"], ["shield", "Surveillance", "Bâche et intrusion", "Activée"]],
                     "autos": [["thermo", "Gel en cabine", "Alerte sous 0 °C"]]},
                ], scenarios=[["Coupure de quai", "Alerte et bascule sur batteries"], ["Arrivée au mouillage", "Alarme et feu de mouillage"], ["Tempête", "Aussières et cale surveillées"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["pump", "Cale qui se remplit", "Alerte si la pompe tourne plus de 3 fois en 1 h", "Cycles de la pompe", True],
                                     ["plug", "Coupure de quai", "Alerte immédiate", "Perte du 30 A", True],
                                     ["anchor", "Dérive au mouillage", "Alerte au-delà de 40 m", "Position GPS", True],
                                     ["drop", "Humidité de la cabine", "Déshumidificateur au-dessus de 65 %", "Humidité", True], ["sun", "Feux de navigation", "Allumage au coucher du soleil", "Coucher du soleil", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[30, "Système", "Alimentation de quai rétablie après 2 minutes"], [160, "James", "Porte du salon verrouillée"],
                                        [1500, "Système", "Test de la pompe de cale réussi"], [2900, "James", "Mode Au quai appliqué · 4 / 4 effets confirmés"]]),
            ]],
        ],
    },
}

# =============================================================================================
# Avion · turbopropulseur d'affaires (8 places) dans un hangar privé, aéroport de Saint-Jean-sur-Richelieu (CYJN)
# =============================================================================================

AEROPORT = {
    "km": 100, "note": "Plan d’aéroport illustratif",
    "water": [[[372, 0], [400, 0], [400, 240], [356, 240], [362, 160], [366, 80]]],
    "strips": [[[54, 186], [330, 70], 12], [[84, 52], [316, 176], 10]],
    "roads": [{"pts": [[110, 158], [150, 190], [200, 206]], "minor": True}, {"pts": [[200, 206], [270, 206]], "straight": True, "minor": True},
              {"pts": [[0, 226], [340, 226]], "straight": True}],
    "blocks": [[200, 196, 70, 18], [150, 200, 16, 10], [172, 200, 16, 10], [282, 196, 30, 18, "park"], [236, 196, 14, 10, "hi"]],
    "labels": [[118, 142, "Piste 06-24"], [120, 74, "Piste 11-29"], [384, 120, "Richelieu", "water"], [235, 184, "Aérogare"]],
    "me": [243, 201],
}

REGION = {
    "km": 1.6, "note": "Carte régionale illustrative",
    "water": [[[300, 150], [312, 170], [318, 200], [312, 240], [296, 240], [300, 200], [294, 170]], [[220, 150], [236, 146], [240, 160], [226, 168]]],
    "rivers": [[[40, 0], [44, 60], [40, 120], [46, 180], [40, 240]], [[0, 20], [120, 8], [240, 0]]],
    "roads": [{"pts": [[0, 116], [80, 112], [160, 114], [250, 116], [340, 100], [400, 92]], "n": "10", "at": [160, 114]}],
    "towns": [[50, 118, "Saint-Jean", "b"], [160, 104, "Granby", "a"], [348, 92, "Sherbrooke", "b"], [300, 150, "Magog", "l"]],
    "labels": [[306, 214, "Memphrémagog", "water"], [230, 176, "Lac Brome", "water"], [30, 70, "Richelieu", "water"]],
    "me": [50, 118],
}

AVION_POINTS = [
    {"n": 1, "x": 214, "y": 190, "kind": "carburant", "name": "Avitaillement", "what": "Jet A-1", "dist": "350 m", "info": "Camion-citerne sur appel · prix non vérifiés (exemple)"},
    {"n": 2, "x": 168, "y": 192, "kind": "service", "name": "Atelier d’entretien", "what": "Mécanique", "dist": "500 m", "info": "Sur rendez-vous (exemple)"},
    {"n": 3, "x": 262, "y": 190, "kind": "eau", "name": "Aérogare", "what": "Eau et services", "dist": "120 m", "info": "Ouverte de 7 h à 19 h (exemple)"},
]

AVION = {
    "key": "avion", "name": "Avion", "kind": "Turbopropulseur d’affaires · 8 places", "place": "Saint-Jean-sur-Richelieu · hangar privé", "icon": "plane", "meIcon": "hangar",
    "mobile": True, "points": AVION_POINTS,
    "geo": {"lat": 45.29, "lon": -73.28, "place": "Aéroport de Saint-Jean-sur-Richelieu"},
    "banner": photo_ou_attente("avion", "Le turbopropulseur d’affaires dans son hangar privé éclairé", "50% 55%"),
    "titles": {"voyage": "Vols et entretien", "eau": "Eau et carburant", "confort": "Climat du hangar"}, "voyageIcon": "plane",
    "subs": {"apercu": "L’avion au hangar, prêt pour le prochain vol.", "confort": "Hangar, moteur et météo du terrain.",
             "energie": "Batterie de bord, groupe de parc et préchauffage.", "eau": "Carburant, purges et eau du hangar.",
             "securite": "Hangar, avion et météo aéronautique.", "internet": "Wi-Fi du hangar et secours.",
             "equipements": "Préchauffage, groupe de parc, porte du hangar et chargeur.", "voyage": "Vols, listes de vérification et entretien.",
             "modes": "Au hangar, prévol, après vol."},
    "status": [["fuel", "Carburant", "62 %", "gold"], ["engine", "Préchauffage", "Planifié", "water"], ["plane", "État", "Au hangar", "ok"]],
    "maps": {"aeroport": AEROPORT, "region": REGION},
    "wx": wx([1, 0, 0, -1, -1, -1, 0, 1, 3, 5, 7, 8, 9, 9, 8, 6, 5, 4, 3, 2, 2, 1, 1, 1],
             "ddddddpppppcccccppdddddd", "000000000011122200000000",
             [["cloudsun", 9, -1, 10], ["rain", 9, 3, 70], ["cloud", 6, 0, 30], ["sun", 5, -3, 0], ["snow", 2, -4, 40]],
             hum=66, dew=-4, wind=22, dir="Ouest-sud-ouest", gust=34, vis=24, hpa=1020, trend="Stable", uv=1, cas=2),
    "energy": {"unit": "Ah", "cap": 42, "nominal": "24 V", "chem": "Plomb-acide scellée", "soc": 96, "v": "25,4 V", "reserve": 50, "load": 250, "battW": 18,
               "autonomy": "Maintien de charge actif", "ringTitle": "Batterie de bord", "packsTitle": "Batterie de bord",
               "packs": [{"name": "Batterie de bord", "cap": 42, "soc": 96, "v": 25.4, "a": 0.7, "t": 6.5, "cycles": -1, "hi": 0, "lo": 0}],
               "sources": [["secteur", "Prise du hangar", "plug", "grid"], ["gpu", "Groupe de parc · 28 V", "plug", 0, "prêt"], ["alt", "Démarreur-génératrice", "alt", 0, "moteur arrêté"]],
               "store": "Batterie de bord", "loads": "Hangar",
               "solar": {"peak": 0, "cloud": 0, "base": 250, "eve": 260, "morn": 0}},
    "s": {
        "apercu": [
            C("kpi", 3, icon="fuel", label="Carburant", value="942 L", sub="Jet A-1 · 62 % · ≈ 3 h de vol", bar=62, tone="gold", go="eau"),
            C("kpi", 3, icon="engine", label="Turbine", value="7 °C", sub="Préchauffage demain 7 h", subicon="clock", tone="water", go="equipements"),
            C("kpi", 3, icon="battery", label="Batterie de bord", value="96 %", sub="Chargeur de maintien", bar=96, tone="bat", go="energie"),
            C("kpi", 3, icon="sun", label="Conditions", value="VFR", dot="ok", sub="Vent 250° · 12 nœuds", subicon="wind", tone="ok", go="securite:alertes"),
            C("conditions", 7, title="Conditions au terrain"),
            C("lumieres", 5),
            C("around", 7, title="Autour du hangar", map="aeroport", pins="points", listTitle="Services du terrain",
              list=[["fuel", "muted", "Jet A-1", "Avitaillement sur appel · 350 m"], ["wrench", "gold", "Atelier d’entretien", "500 m"], ["drop", "water", "Aérogare", "120 m"]],
              btn=["Services du terrain", "eau:points"]),
            C("checklist", 5, id="prevol", title="Préparer le vol", icon="clip",
              items=[["Météo et NOTAM consultés", True], ["Plan de vol déposé", False], ["Purges de carburant", False], ["Caches d’entrée d’air retirés", False]]),
            C("upcoming", 7, title="Prochaines 48 heures", icon="warn", note="Piste 11-29 fermée pour travaux (exemple).", text="Décollage prévu sur la piste 24 · vent 250° à 12 nœuds.", go="securite:alertes"),
            C("trip", 5, title="Mon prochain vol", name="Vers Sherbrooke (CYSC)", next="Départ prévu demain à 10 h", go="voyage"),
        ],
        "confort": [
            ["synthese", "Synthèse", [
                C("thermostat", 7, title="Hangar privé", sub="Chauffé · hors-gel et humidité", set=5, min=2, max=18, inside=6,
                  rows=[["hangar", "Hangar", "6 °C"], ["fire", "Chauffage", "Hors-gel"], ["drop", "Humidité", "Déshumidificateur actif"]]),
                C("trends", 5, items=[
                    {"icon": "thermo", "title": "Température du hangar", "value": "6 °C", "state": "Hors-gel", "tone": "ok", "c": "gold",
                     "pts": [5.2, 5.4, 5.6, 5.9, 6.1, 6.0, 5.9, 6.0, 6.1, 6.0, 6.0, 6.0], "min": -4, "max": 16},
                    {"icon": "drop", "title": "Humidité", "value": "48 %", "state": "Bonne pour l’avion", "tone": "ok", "c": "blue",
                     "pts": [55, 54, 53, 52, 51, 50, 49, 49, 48, 48, 48, 48], "min": 20, "max": 90}]),
                C("ventilation", 3, speed=1, max=4, rows=[["fan", "Ventilation", "Minimum"]]),
                C("air", 3, title="Air du hangar", co2=470, quality="Bonne qualité", rows=[["flame", "Vapeurs de carburant", "Aucune"], ["co", "CO", "0 ppm"], ["drop", "Humidité", "48 %"]]),
                C("outside", 3),
                C("cold", 3, icon="engine", title="Avion", sub="Températures actuelles", rows=[["engine", "Huile de la turbine", "7 °C"], ["battery", "Batterie de bord", "7 °C"], ["plane", "Cabine", "8 °C"]]),
            ]],
            T_meteo(), T_soleil(),
        ],
        "energie": [
            ["synthese", "Synthèse", [
                C("flow", 8), C("ring", 4), C("history", 7, title="Consommation du hangar"),
                C("bars", 5, title="Consommateurs", sub="Puissance instantanée · exemple",
                  rows=[["heater", "Déshumidificateur de cabine", 230], ["battery", "Chargeur de maintien", 18], ["bulb", "Éclairage du hangar", 0], ["engine", "Préchauffage (planifié)", 0], ["plug", "Groupe de parc (prêt)", 0]]),
                C("chips", 12, items=[["plug", "Groupe de parc", "Prêt · 28 V", "ok"], ["engine", "Préchauffage", "Planifié · 7 h", "gold"], ["battery", "Chargeur", "Maintien", "ok"]]),
            ]],
            ["batterie", "Batterie de bord", [
                C("packs", 8),
                C("list", 4, icon="shield", title="Batterie de bord", sub="Entretien et contrôle",
                  rows=[["check", "Chargeur de maintien", "Actif", "ok"], ["clock", "Dernier test de capacité", "Il y a 13 mois", "warn"], ["sliders", "Seuil de démarrage", "24,2 V", "muted"],
                        ["bell", "Alarme", "Aucune", "ok"]]),
            ]],
        ],
        "eau": [
            ["synthese", "Synthèse", [
                C("tanks", 7, title="Carburant et huile", sub="Niveaux déclarés après le dernier vol",
                  items=[["Aile gauche", 64, 760, "fuel"], ["Aile droite", 60, 760, "fuel"], ["Huile de la turbine", 88, 14, "oil"]]),
                C("gauge", 5, icon="fuel", title="Carburant total", sub="Jet A-1 · 1 520 L utilisables", pct=62, value="942 / 1 520 L", est="≈ 3 h de vol", estsub="à 250 L/h, réserve de 45 min comprise"),
                C("list", 6, icon="drop", title="Eau dans le carburant", sub="Purges avant chaque vol",
                  rows=[["drop", "Purge de l’aile gauche", "Claire · aucun dépôt", "ok"], ["drop", "Purge de l’aile droite", "Claire", "ok"], ["drop", "Purge du filtre", "À faire avant le vol", "warn"]]),
                C("leaks", 6, title="Fuites", text="Aucune fuite détectée", sensors=[["fuel", "Sous l’avion", "Sec"], ["tap", "Lavabo du hangar", "Sec"], ["heater", "Chauffe-eau", "Sec"]]),
            ]],
            ["points", "Services du terrain", [
                C("levels", 12, items=[["Aile gauche", 64, 760, "fuel"], ["Aile droite", 60, 760, "fuel"], ["Huile de la turbine", 88, 14, "oil"]]),
                C("points", 12, map="aeroport", view=[120, 150, 160, 96], title="Services du terrain", sub="Carburant, entretien et aérogare",
                  filters=[["tous", "Tous"], ["carburant", "Carburant"], ["service", "Entretien"], ["eau", "Aérogare"]]),
                C("note", 12, icon="info", text="Source : exemple. Vérifier la disponibilité du carburant et les heures de l’aérogare avant de partir."),
            ]],
        ],
        "securite": [
            ["synthese", "Synthèse", [
                C("openings", 12, title="Hangar et avion", sub="Accès et ouvertures", env="avion",
                  points=[O("Porte du hangar", "Fermée", "ok", "Hangar", 1300, "James", lock=True, icon="hangar"),
                          O("Porte de l’équipage", "Verrouillée", "ok", "Avion", 1305, "James", lock=True, icon="plane"),
                          O("Porte passagers et cargo", "Verrouillée", "ok", "Avion", 1305, "James", lock=True, icon="plane"),
                          O("Soute à bagages", "Fermée", "ok", "Avion", 1310, "James", lock=False, icon="box"),
                          O("Trappe à huile", "Fermée", "ok", "Avion", 1500, "Inspection prévol", lock=False, icon="engine")]),
                C("list", 4, icon="radar", title="Détection", sub="Capteurs du hangar",
                  rows=[["co", "CO · hangar", "0 ppm", "ok"], ["flame", "Vapeurs de carburant", "Aucune", "ok"], ["smoke", "Fumée", "Normal", "ok"], ["eye", "Mouvement", "Aucun", "ok"]]),
                C("cams", 4, items=[], empty="La caméra du hangar n’est pas encore reliée.", emptysub="Elle apparaîtra ici dès son branchement. Aucune image n’est simulée."),
                C("events", 4, items=[[1300, "Porte du hangar fermée", "Après le vol · par James", "ok"], [1310, "Housse du moteur posée", "Liste après vol", "ok"],
                                      [1320, "Avion rentré au hangar", "Vol local · 1 h 10", "ok"]]),
                C("toggle", 6, icon="shield", key="surv", title="Surveillance du hangar", sub="Porte, mouvement et vapeurs", on=True, critical=True),
                C("toggle", 6, icon="bell", key="notif", title="Notifications", sub="Sur vos appareils", on=True),
                C("note", 12, icon="info", text="Moteur en marche, les commandes du hangar sont verrouillées. Toute commande critique demande confirmation."),
            ]],
            ["alertes", "Météo aéronautique", [
                C("metar", 12, station="CYJN · Saint-Jean-sur-Richelieu", sub="Observation d’exemple", cat="VFR",
                  raw="CYJN 071300Z 25012KT 15SM FEW040 BKN090 03/M04 A3012 RMK SC1AC5 SLP209",
                  rows=[["wind", "Vent", "250° · 12 nœuds"], ["eye", "Visibilité", "15 milles terrestres"], ["cloud", "Nuages", "Quelques à 4 000 pi · fragmentés à 9 000 pi"],
                        ["thermo", "Température / point de rosée", "3 °C / −4 °C"], ["gauge", "Altimètre", "30,12 po Hg"], ["plane", "Piste en service", "24"]],
                  taf="TAF CYJN 071140Z 0712/0800 26012KT P6SM FEW040 BKN090 TEMPO 0718/0800 5SM -SHSN BKN030"),
                C("ec", 6, title="Météo · Saint-Jean-sur-Richelieu", counts=[0, 0, 0, 1, 0]),
                C("list", 6, icon="doc", title="NOTAM · exemple", sub="NAV CANADA · consulter les avis officiels",
                  rows=[["warn", "Piste 11-29", "Fermée pour travaux", "warn"], ["bulb", "Balisage lumineux", "Normal", "ok"], ["plane", "Circuit", "Écoles de pilotage actives", "muted"]]),
            ]],
        ],
        "internet": [
            ["connexions", "Connexions", [
                C("link", 8, h=2, kind="Wi-Fi du hangar", icon="wifi", dbm=-58, bars=4, down=25, up=6, ping=19, loss="0,2 %"),
                C("meter", 4, icon="doc", title="Forfait LTE", used=3, total=10, unit="Go", note="7 Go disponibles · renouvellement le 1er décembre"),
                C("list", 4, icon="link", title="Autres connexions", rows=[["antenna", "LTE", "Secours prêt", "ok"]]),
                C("devices", 7, total=4, groups=[["cpu", 1, "Hub JARVIS"], ["thermo", 2, "capteurs"], ["phone", 1, "tablette de vol"]]),
                C("prio", 5, items=[["wifi", "Wi-Fi du hangar"], ["antenna", "LTE"]]),
            ]],
            T_diag([["engine", "Préchauffage moteur", "En ligne", "ok"], ["plane", "Météo aéronautique", "À jour", "ok"], ["doc", "NOTAM", "À jour", "ok"]],
                   [["plane", "METAR", "Dernière lecture : il y a 12 min", "ok"], ["doc", "NOTAM", "Dernière lecture : il y a 1 h", "ok"],
                    ["thermo", "Hangar", "Dernière lecture : il y a 20 s", "ok"]],
                   cpu=5, mem=(0.9, 4), disk=(9, 64)),
        ],
        "equipements": [
            C("status", 12, moving=True, still="Au hangar · moteur arrêté", ok="Commandes disponibles", lock="Commandes verrouillées moteur en marche", moveLabel="Moteur en marche"),
            C("equip", 4, icon="engine", title="Préchauffage", sub="Turbine, huile et cabine", state="Planifié · demain 7 h", tone="gold", rows=[["Durée", "3 h avant le vol"], ["Huile", "7 °C"]],
              act={"label": "Démarrer maintenant", "icon": "fire", "confirm": "Démarrer le préchauffage de la turbine et de la cabine maintenant? Il fonctionnera 3 heures.", "done": "En marche · 3 h", "back": "Arrêter", "moving": True}),
            C("equip", 4, icon="hangar", title="Porte du hangar", sub="Porte motorisée · 18 m", state="Fermée", tone="ok",
              act={"label": "Ouvrir", "icon": "up", "confirm": "Ouvrir la porte du hangar? Vérifiez que la zone devant la porte est dégagée.", "done": "Ouverte", "back": "Fermer", "moving": True},
              note="Confirmation requise"),
            C("equip", 4, icon="battery", title="Chargeur de batterie", sub="Maintien 24 V", state="Maintien · 25,4 V", tone="ok", rows=[["Courant", "0,7 A"]]),
            C("equip", 4, icon="plug", title="Groupe de parc", sub="28 V · démarrage et cabine", state="Prêt · débranché", tone="ok", rows=[["Câble", "Rangé sur l’enrouleur"]],
              act={"label": "Brancher et alimenter", "icon": "bolt", "confirm": "Alimenter l’avion avec le groupe de parc 28 V? Vérifiez que le câble est branché à la prise extérieure.", "done": "Alimenté · 28 V", "back": "Couper", "moving": True},
              note="Confirmation requise"),
            C("equip", 4, icon="heater", title="Déshumidificateur de cabine", sub="Pare-brise et instruments", state="Actif", tone="ok", toggle={"label": "En marche", "on": "Actif", "off": "Arrêté"}),
            C("equip", 4, icon="bulb", title="Éclairage du hangar", sub="DEL", state="Éteint", tone="muted", toggle={"label": "Allumer", "on": "Allumé", "off": "Éteint"}),
            C("list", 4, icon="clip", title="Housses et caches", sub="À retirer avant le vol",
              rows=[["plane", "Caches-pitot", "En place", "warn"], ["engine", "Caches d’entrée d’air et d’échappement", "En place", "warn"], ["box", "Cales de roues", "En place", "warn"]]),
            C("inspection", 12, title="Prochaine inspection", sub="Inspection annuelle · atelier d’exemple", d=24, go="voyage:entretien"),
        ],
        "voyage": [
            ["vol", "Vol", [
                C("trip", 8, big=True, title="Vol planifié", name="Vers Sherbrooke (CYSC)", next="Départ prévu · demain 10 h", dist="126 km", dur="20 min à 260 nœuds",
                  map="region", view=[0, 0, 400, 240], route={"next": [[50, 118], [160, 112], [348, 92]]}),
                C("arrival", 4, place="Sherbrooke (CYSC)", temp=1, icon="cloud", cond="Nuageux · plafond 4 500 pi", wind="Vent 270° · 14 nœuds"),
                C("list", 6, icon="doc", title="NOTAM sur la route", sub="Exemple · consulter les avis officiels",
                  rows=[["warn", "CYJN · piste 11-29 fermée", "Départ en 24", "warn"], ["plane", "CYSC · carburant Jet A-1", "Disponible", "ok"]]),
                C("list", 6, icon="clip", title="Avant de partir",
                  rows=[["doc", "Plan de vol : à déposer", "", "", True], ["fuel", "Carburant : 942 L · suffisant", "", "", True], ["drop", "Purges : à faire", "", "", True],
                        ["list", "Liste de vérification prévol", "", "", True]]),
            ]],
            ["agenda", "Agenda", [
                C("agenda", 12, l1="Vols", l2="Entretien (inspections, rappels)",
                  events=[[-1, "10:00", "11:10", "Vol local", "flight"], [1, "08:00", "10:00", "Préchauffage", "maint"], [1, "10:00", "11:00", "Vol vers Sherbrooke", "flight"],
                          [1, "15:00", "16:00", "Retour à CYJN", "flight"], [6, "09:00", "12:00", "Test de la batterie", "maint"]]),
                C("next", 4, icon="plane", kick="Prochain vol", title="Vers Sherbrooke", d=1, h="10:00", countdown=True),
                C("next", 4, icon="engine", kick="Préchauffage", title="Moteur · 3 h avant", d=1, h="07:00"),
                C("next", 4, icon="wrench", kick="Inspection annuelle", title="Atelier d’exemple", d=24, h="09:00"),
            ]],
            ["listes", "Listes", [
                C("lists", 12, title="Listes de vérification", sub="Les mêmes gestes, chaque fois.", lists=[
                    {"k": "prevol", "l": "Prévol", "sub": "Autour de l’avion.", "icon": "plane",
                     "items": [["Météo et NOTAM", "Consultés", True], ["Purges de carburant", "Ailes et filtre", False], ["Niveau d’huile de la turbine", "Selon le manuel", True],
                               ["Caches retirés", "Pitot, entrée d’air, échappement", False], ["Cales retirées", "", False], ["Gouvernes libres", "", False]]},
                    {"k": "apres", "l": "Après vol", "sub": "Rentrer l’avion.", "icon": "hangar",
                     "items": [["Caches d’entrée d’air", "", True], ["Caches-pitot", "", True], ["Chargeur branché", "", True], ["Carnet de route", "1 h 10", True]]},
                    {"k": "hangar", "l": "Hangar", "sub": "Fermeture.", "icon": "lock",
                     "items": [["Porte fermée", "", True], ["Chauffage hors-gel", "5 °C", True], ["Éclairage éteint", "", True]]},
                ]),
            ]],
            ["entretien", "Entretien", [
                C("maint", 8, h=2, rows=[
                    M("wrench", "Inspection annuelle", "Atelier d’exemple",
                      src_fixe("regle", "Règlement de l’aviation canadien · inspection annuelle", 24)),
                    M("engine", "Inspection de la turbine", "Endoscopie et filtres",
                      compteur("Compteur d’heures de la turbine", "aux 100 heures", 82, 100, 0.6, "h")),
                    M("battery", "Batterie de bord", "Test de capacité",
                      fab("Manuel de la batterie", "aux 6 mois", 182, -185)),
                    M("radar", "Balise de détresse (ELT)", "Batterie à remplacer",
                      fab("Manuel de la balise", "date de péremption de la pile", 1825, -1705)),
                    M("doc", "Certificat de navigabilité", "À jour",
                      src_fixe("regle", "Règlement de l’aviation canadien", 200)),
                ]),
                C("next", 4, icon="wrench", kick="Prochain rendez-vous", title="Inspection annuelle", d=24, h="09:00"),
                C("next", 4, icon="battery", kick="En retard", title="Test de la batterie de bord", text="Prévu il y a 3 jours."),
            ]],
        ],
        "modes": [
            ["modes", "Modes", [
                C("modes", 12, current="hangar", items=[
                    {"k": "hangar", "icon": "hangar", "label": "Au hangar", "sub": "Surveillance et maintien",
                     "fx": [["thermo", "Hangar", "Hors-gel", "5 °C"], ["battery", "Batterie", "Chargeur de maintien", "Actif"], ["heater", "Cabine", "Déshumidificateur", "Actif"],
                            ["shield", "Surveillance", "Porte et mouvement", "Activée", "crit"]],
                     "autos": [["thermo", "Hangar sous 2 °C", "Alerte et chauffage"]]},
                    {"k": "prevol", "icon": "list", "label": "Prévol", "sub": "Préparer le vol",
                     "fx": [["engine", "Préchauffage", "3 h avant le départ", "Démarré", "crit"], ["bulb", "Éclairage", "Hangar pleine lumière", "Lecture", "light", "lecture"],
                            ["hangar", "Porte du hangar", "Ouverture", "Ouverte", "crit"], ["heater", "Déshumidificateur", "Arrêt", "Arrêté", "fail"]],
                     "autos": [["calendar", "Vol inscrit à l’agenda", "Lance le préchauffage 3 h avant"]]},
                    {"k": "apres", "icon": "check", "label": "Après vol", "sub": "Rentrer et protéger",
                     "fx": [["hangar", "Porte du hangar", "Fermeture", "Fermée", "crit"], ["battery", "Chargeur", "Branchement", "Maintien"],
                            ["heater", "Déshumidificateur", "Remise en marche", "Actif"], ["bulb", "Éclairage", "Extinction", "Éteint"]],
                     "autos": [["doc", "Fin du vol", "Ouvre le carnet de route"]]},
                ], scenarios=[["Matin de vol", "Préchauffage, porte et éclairage"], ["Retour de nuit", "Balisage du hangar"], ["Grand froid", "Préchauffage prolongé"]]),
            ]],
            ["autos", "Automatisations", [
                C("autos", 12, rows=[["engine", "Préchauffage automatique", "3 h avant chaque vol planifié", "Agenda des vols", True],
                                     ["thermo", "Hangar trop froid", "Alerte sous 2 °C", "Température", True], ["flame", "Vapeurs de carburant", "Ventilation et alerte", "Détecteur", True],
                                     ["battery", "Batterie faible", "Alerte sous 24,2 V", "Tension", True], ["plane", "METAR défavorable", "Alerte la veille du vol", "Météo aéronautique", False]]),
            ]],
            ["activite", "Activité", [
                C("activity", 12, rows=[[1300, "James", "Porte du hangar fermée après le vol"], [1310, "James", "Mode Après vol appliqué · 4 / 4 effets confirmés"],
                                        [1400, "Système", "Vol local enregistré · 1 h 10"], [1500, "Marc-André", "Mode Prévol appliqué · 3 / 4 effets confirmés · déshumidificateur à vérifier"]]),
            ]],
        ],
    },
}

ENVS = [BOULANCE, MAISON, CHALET, ENTREPRISE, GARAGE, FERME, BATEAU, AVION]

# =============================================================================================
# Multisite : l'état de chaque lieu vu de l'accueil (présence, sécurité, alertes) et la
# correspondance des modes communs (Absence, Nuit, Grand froid) avec les modes propres au lieu.
# Les retards d'entretien et les ouvertures restées ouvertes s'ajoutent seuls aux alertes.
# =============================================================================================

SITES = {
    "boulance": {"who": "James et Marie · à bord", "n": 2, "armed": True, "arm": "Ouvertures surveillées", "inside": 21,
                 "alerts": [["water", "Nuit froide : −6 °C vers 5 h", "Conduites protégées · consigne de nuit suggérée", "confort"]],
                 "multi": {"absence": "absence", "nuit": "nuit", "froid": "hivernage"}},
    "maison": {"who": "Léa · à la maison", "n": 1, "armed": True, "arm": "Armé · périmètre", "inside": 21,
               "alerts": [["gold", "Pointe Hydro-Québec demain, de 6 h à 9 h", "Préchauffage prévu à 5 h", "energie"]],
               "multi": {"absence": "absent", "nuit": "nuit", "froid": "vacances"}},
    "chalet": {"who": "Personne · inoccupé depuis 5 jours", "n": 0, "armed": True, "arm": "Armé · hors saison", "inside": 12,
               "alerts": [["warn", "Avertissement de neige : 15 à 20 cm", "Déneigeur prévu · chemin du lac", "securite:alertes"]],
               "multi": {"absence": "horssaison", "nuit": "horssaison", "froid": "horssaison"}},
    "entreprise": {"who": "14 personnes sur 22", "n": 14, "armed": False, "arm": "Désarmé · heures d’ouverture", "inside": 21.5,
                   "alerts": [["gold", "Événement de pointe demain, de 7 h à 9 h", "Plan de délestage prêt", "energie"]],
                   "multi": {"absence": "fermeture", "nuit": "fermeture", "froid": "findesemaine"}},
    "garage": {"who": "Personne · garage fermé", "n": 0, "armed": True, "arm": "Armé · périmètre et mouvement", "inside": 15,
               "alerts": [["gold", "Escalade noir de retour vers 18 h", "Porte 1 à ouvrir après confirmation", "equipements"]],
               "multi": {"absence": "ferme", "nuit": "ferme", "froid": "hiver"}},
    "ferme": {"who": "Philippe et Sophie · tournée à 17 h", "n": 2, "armed": True, "arm": "Périmètre surveillé", "inside": 12.4,
              "alerts": [["warn", "Poulets de chair · zone 3 à 25,6 °C", "Aérotherme no 3 en défaut · consigne 27 °C", "confort:chair"]],
              "multi": {"absence": None, "nuit": "nuit", "froid": None}},
    "bateau": {"who": "Personne · au quai", "n": 0, "armed": True, "arm": "Armé · au quai", "inside": 13,
               "alerts": [["warn", "Avis de vent fort cet après-midi", "Sud-ouest 20 nœuds en rafales", "securite:alertes"]],
               "multi": {"absence": "quai", "nuit": "quai", "froid": "hivernage"}},
    "avion": {"who": "Personne · au hangar", "n": 0, "armed": True, "arm": "Armé · hangar fermé", "inside": 6,
              "alerts": [["gold", "Piste 11-29 fermée pour travaux", "Décollage prévu sur la piste 24", "securite:alertes"]],
              "multi": {"absence": "hangar", "nuit": "hangar", "froid": "hangar"}},
}

MULTI_MODES = [
    {"k": "absence", "icon": "lock", "label": "Absence", "sub": "Sécurité et économie partout"},
    {"k": "nuit", "icon": "moon", "label": "Nuit", "sub": "Tout veille, l’essentiel reste actif"},
    {"k": "froid", "icon": "snowflake", "label": "Grand froid", "sub": "Protection contre le gel"},
]


def _cards(e):
    """Toutes les cartes d'un environnement, quels que soient les onglets."""
    for sec in e["s"].values():
        if sec and isinstance(sec[0], list):
            for tab in sec:
                yield from tab[2]
        else:
            yield from sec


def _source_devinee(label, note, liste):
    """Source d'un élément de liste sans source écrite : capteur si le texte le dit, saison pour les listes
    de froid ou d'hivernage, vous pour les courses, sinon la liste type de JARVIS pour ce lieu."""
    t = (label + " " + (note or "")).lower()
    if "capteur" in t:
        return {"k": "capteur", "t": "Confirmé par capteur"}
    if liste in ("hiver", "froid", "hivernage", "hivernal", "saison") or "gel" in t or "antigel" in t:
        return {"k": "saison", "t": "Saison et météo du lieu"}
    if liste in ("courses", "achats", "epicerie"):
        return {"k": "vous", "t": "Ajouté par vous"}
    return {"k": "jarvis", "t": "Liste type de JARVIS pour ce lieu · modifiable"}


def _prepare(e):
    """Complète un environnement pour l'affichage : sources, emplacements photo, état multisite."""
    e = dict(e)
    e["site"] = SITES.get(e["key"], {})
    for c in _cards(e):
        if c["type"] == "checklist":
            c["items"] = [[it[0], it[1], _src(it[2]) if len(it) > 2 else _source_devinee(it[0], "", c.get("id", ""))] for it in c["items"]]
        elif c["type"] == "lists":
            for L in c["lists"]:
                L["items"] = [[it[0], it[1], it[2], _src(it[3]) if len(it) > 3 else _source_devinee(it[0], it[1], L["k"])] for it in L["items"]]
        elif c["type"] == "equip":
            nom = e["key"] + "-" + _slug(c["title"])
            c["photo"] = _photo("equip", nom, c["title"] + " · " + c.get("sub", "") + " (" + e["name"] + ")")
        elif c["type"] == "batiments":
            for b in c["items"]:
                b["photo"] = _photo("ferme", b["k"] + "-exterieur", "Extérieur · " + b["name"] + " (" + e["name"] + ")")
        elif c["type"] == "batiment":
            c["photoExt"] = _photo("ferme", c["k"] + "-exterieur", "Extérieur · " + c["name"] + " (" + e["name"] + ")")
            c["photoInt"] = _photo("ferme", c["k"] + "-interieur", "Intérieur · " + c["name"] + " (" + e["name"] + ")")
        elif c["type"] == "openings":
            for o in c["points"]:
                nom = e["key"] + "-" + _slug(o["label"])
                o["photo"] = _photo("ouvertures", nom, o["label"] + " (" + e["name"] + ")")
    return e


def data():
    del PHOTOS_ATTENDUES[:]
    envs = [_prepare(e) for e in ENVS]
    return {"order": [e["key"] for e in ENVS], "envs": _typo(envs), "multi": _typo(MULTI_MODES)}


def html():
    payload = json.dumps(data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    lum = lumieres.html() if lumieres else ""
    return f"""<div class="ev" data-demo="env">
  <div class="ev-app" data-ev-app aria-live="off"></div>
  <noscript><p class="ev-nos">Activez JavaScript pour essayer les environnements intelligents.</p></noscript>
  <dialog class="ev-dlg" data-ev-dlg aria-labelledby="ev-dlg-t"></dialog>
  <div class="ev-toast" data-ev-toast role="status" aria-live="polite"></div>
  <script type="application/json" id="env-data">{payload}</script>
</div>{lum}"""
