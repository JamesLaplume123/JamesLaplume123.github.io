# Démo « Personal Intelligence : comprendre ses habitudes, choisir son avenir »
# (assets/demos/vie.css et vie.js).
#
# Treize sources, chacune avec sa propre permission révocable, alimentent le
# modèle personnel d'Alex sur le Hub JARVIS (flux animés). JARVIS en tire des
# habitudes avec leurs preuves; pour l'habitude choisie, deux avenirs sont
# projetés (« Si vous continuez » / « Si vous changez ») sur 30, 90 ou 365 jours,
# toujours étiquetés comme estimation avec leur base. Une automatisation attend
# l'accord : Approuver montre l'effet, Refuser montre la conséquence honnête,
# sans culpabiliser. Le coach de vie relie objectifs, semaine réelle, conseils
# (principe d'un livre, reformulé, et une citation du domaine public) et
# engagements choisis par la personne, révocables.
# Bien-être seulement, aucun diagnostic. Données d'exemple entièrement fictives.
#
# Une seule source de vérité : les listes ci-dessous. Python produit l'état
# initial complet (lisible sans JavaScript) et le script reçoit le reste par un
# bloc JSON. Les formules des projections existent aussi dans vie.js (project).

import json
import math
import re
from html import escape

NBSP = "\u00a0"


def fr(s):
    """Espaces insécables de la typographie française (heures, unités, ponctuation, guillemets)."""
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) h (\d)", rf"\1{NBSP}h{NBSP}\2", s)
    s = re.sub(r"(\d) (h|min|ms|bpm|K|\$|%|°C|pas|soirs?|jours?|nuits?|semaines?|séances?|achats?|points?|km)(?=[\s,.;:)·]|$)",
               rf"\1{NBSP}\2", s)
    s = re.sub(r" ([:;?!»])", rf"{NBSP}\1", s)
    return s.replace("« ", "«" + NBSP)


def e(s):
    return escape(fr(s))


# ---------------------------------------------------------------------------
# Icônes (traits, 24 × 24)
# ---------------------------------------------------------------------------
ICONS = {
    "sleep": '<path d="M19.6 14.6A7.9 7.9 0 1 1 9.4 4.4a6.4 6.4 0 0 0 10.2 10.2z"/>',
    "activity": '<path d="M3 12h3.6l2.2-5.6 4.2 11.2 2.4-5.6H21"/>',
    "heart": '<path d="M12 19.6s-7.6-4.4-7.6-10a4.2 4.2 0 0 1 7.6-2.5 4.2 4.2 0 0 1 7.6 2.5c0 5.6-7.6 10-7.6 10z"/>',
    "calendar": '<rect x="3.6" y="5" width="16.8" height="15" rx="2.2"/><path d="M3.6 10h16.8M8 3v4M16 3v4"/>',
    "phone": '<rect x="7" y="2.8" width="10" height="18.4" rx="2.6"/><path d="M11 18h2"/>',
    "card": '<rect x="3" y="5.6" width="18" height="12.8" rx="2.2"/><path d="M3 10h18M6.6 14.6h3.6"/>',
    "meal": '<circle cx="12" cy="12" r="5.6"/><path d="M3.4 4v5.2a1.8 1.8 0 0 0 1.8 1.8v9M5.2 4v4M20.6 4c-1.8 1-2.4 3-2.4 5.4v2h2.4v8.6"/>',
    "pin": '<path d="M12 21s-6.4-6-6.4-11.1a6.4 6.4 0 0 1 12.8 0C18.4 15 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.3"/>',
    "cloud": '<path d="M7.4 18.4h9.8a3.8 3.8 0 0 0 .5-7.6 5.6 5.6 0 0 0-10.8-1.2 4.4 4.4 0 0 0 .5 8.8z"/>',
    "home": '<path d="M3.5 10.6 12 4l8.5 6.6"/><path d="M5.6 9.2v10.3h12.8V9.2"/><path d="M10 19.5v-5h4v5"/>',
    "car": '<path d="M4.4 15.6v-3.2l1.8-4.6a2 2 0 0 1 1.9-1.3h7.8a2 2 0 0 1 1.9 1.3l1.8 4.6v3.2"/><path d="M3.4 12.4h17.2v4.4H3.4zM6 16.8v2M18 16.8v2"/><circle cx="7.4" cy="14.6" r=".6"/><circle cx="16.6" cy="14.6" r=".6"/>',
    "mood": '<circle cx="12" cy="12" r="8.6"/><path d="M8.6 14.4a4.4 4.4 0 0 0 6.8 0M9.2 9.6h.01M14.8 9.6h.01"/>',
    "target": '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="4.8"/><circle cx="12" cy="12" r="1.2"/>',
    "check": '<path d="m5 12.5 4.4 4.3L19 7.2"/>',
    "x": '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
    "spark": '<path d="M12 3.5 13.9 9l5.6 1.9-5.6 1.9L12 18.4l-1.9-5.6-5.6-1.9L10.1 9z"/>',
    "bolt": '<path d="M13 3 5.5 13.4h6L10.8 21l7.7-10.6h-6z"/>',
    "book": '<path d="M12 6.6C10.2 5.1 7.6 4.5 3.8 4.7v13.4c3.8-.2 6.4.4 8.2 1.9 1.8-1.5 4.4-2.1 8.2-1.9V4.7c-3.8-.2-6.4.4-8.2 1.9zM12 6.6V20"/>',
    "quote": '<path d="M5 17.6c2.4-.6 3.6-2.4 3.6-5V7H4.4v5.6h4.2M15 17.6c2.4-.6 3.6-2.4 3.6-5V7h-4.2v5.6h4.2"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.3-3 7.9-7 9.5-4-1.6-7-5.2-7-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9.6 9.6h4.8v4.8H9.6zM9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "undo": '<path d="M8.4 6.6 4 11l4.4 4.4"/><path d="M4 11h10.4a5.6 5.6 0 0 1 0 11.2H11"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# 1. Les sources : (clé, nom, appareil, ce qu'elle lit, valeur du jour, icône, signaux par jour)
# Côté gauche : les sept premières; côté droit : les six autres.
# ---------------------------------------------------------------------------
SOURCES = [
    ("sommeil", "Sommeil", "Montre", "Durée, phases, réveils", "6 h 12 · 2 réveils", "sleep", 96),
    ("activite", "Activité", "Montre", "Pas, séances, minutes actives", "7 840 pas", "activity", 48),
    ("coeur", "Fréquence cardiaque", "Montre", "Repos et variabilité, la nuit", "Repos 61 bpm", "heart", 288),
    ("agenda", "Agenda", "Calendrier", "Heures occupées, jamais le contenu", "5 rencontres", "calendar", 12),
    ("ecran", "Temps d’écran", "Téléphone", "Minutes par heure, pas les applications", "52 min après 23 h", "phone", 24),
    ("depenses", "Dépenses", "Banque", "Catégories seulement, jamais le détail", "Café · Achats en ligne", "card", 9),
    ("repas", "Repas", "Photo ou saisie", "Heure et type de repas", "Midi sauté", "meal", 4),
    ("lieux", "Localisation", "Téléphone", "Lieux fréquents, jamais le trajet exact", "Bureau · Maison", "pin", 18),
    ("meteo", "Météo", "Prévisions locales", "Pluie, température, lever du jour", "Sec demain 6 h", "cloud", 24),
    ("maison", "Maison", "Hub JARVIS", "Heures de lumière, thermostat", "Chambre allumée 0 h 31", "home", 64),
    ("voiture", "Voiture", "Véhicule connecté", "Trajets et heures d’arrivée", "Retour 18 h 52", "car", 6),
    ("humeur", "Humeur", "Saisie volontaire", "Une note de 1 à 5, si vous voulez", "2 sur 5 · fatiguée", "mood", 2),
    ("objectifs", "Objectifs", "Choisis par vous", "Ce que vous voulez atteindre", "3 objectifs actifs", "target", 1),
]
SRC = {s[0]: s for s in SOURCES}
LEFT, RIGHT = SOURCES[:7], SOURCES[7:]

# ---------------------------------------------------------------------------
# 2–4. Habitudes, deux avenirs et automatisations
# Mesures : niveau (s → c si l'on continue, s → n si l'on change; constantes tc, tn
# en jours) ou cumul (s + taux par jour). « w » : changer seul, sans automatisation
# (35 % de l'effet, plus lentement). Les mesures absentes : aucun effet direct estimé.
# ---------------------------------------------------------------------------
METRICS = [
    ("sommeil", "Sommeil", "par nuit", 7.0, "Objectif : 7 h"),
    ("energie", "Énergie", "sur 100", None, ""),
    ("argent", "Épargne", "cumulée", 3000, "Objectif : 3 000 $"),
    ("objectif", "Objectif lié", "progression", 100, "Atteint"),
]
WILL = 0.35

HABITS = [
    {
        "k": "ecran", "name": "Écran après 23 h", "freq": "5 soirs sur 7", "days": "1101101",
        "effect": "Endormissement +42 min",
        "evidence": "Les 5 soirs où l’écran restait allumé au lit, Alex s’est endormie 42 min plus tard en moyenne, "
                    "lumière de la chambre allumée tout ce temps.",
        "srcs": ["ecran", "sommeil", "maison", "objectifs"],
        "goal": "Dormir 7 h",
        "basis": "21 nuits d’Alex observées + effet moyen rapporté pour ce type de changement",
        "m": {
            "sommeil": {"s": 6.2, "c": 6.05, "n": 6.92, "tc": 120, "tn": 16},
            "energie": {"s": 62, "c": 58, "n": 74, "tc": 120, "tn": 22},
            "objectif": {"s": 31, "c": 27, "n": 94, "tc": 120, "tn": 24},
        },
        "auto": {
            "name": "Soirée douce", "touch": ["Maison", "Téléphone"],
            "steps": [("22 h 30", "Lumières chaudes à 2 700 K au salon et dans la chambre"),
                      ("22 h 45", "Téléphone en mode nuit · appels de la famille permis"),
                      ("23 h 00", "Rappel doux : « Il est 23 h. Lecture ? »"),
                      ("Matin", "Bilan : heure d’endormissement, sans jugement")],
            "book": "Atomic Habits", "author": "James Clear",
            "principle": "rendre la mauvaise habitude difficile et la bonne évidente : le décor décide avant la volonté.",
            "yes": "Actif dès ce soir. Effet estimé : +{d} de sommeil par nuit d’ici {h} jours.",
            "no": "Rien ne change dans la maison. Si l’habitude continue : environ {c} par nuit, soit {lost} de sommeil "
                  "en moins sur {h} jours par rapport au changement. Vous pouvez aussi changer par vous-même; "
                  "l’effet estimé est alors plus faible, parce qu’il repose sur la volonté chaque soir.",
        },
    },
    {
        "k": "cafe", "name": "Café après 15 h", "freq": "4 jours sur 7", "days": "1011010",
        "effect": "Sommeil profond −18 %",
        "evidence": "Achat dans la catégorie café après 15 h, près du bureau. Ces nuits-là : sommeil profond −18 %, "
                    "fréquence au repos +4 bpm.",
        "srcs": ["depenses", "sommeil", "coeur", "lieux"],
        "goal": "Économiser 3 000 $",
        "basis": "21 jours d’achats et de nuits d’Alex + effet moyen rapporté de la caféine en fin de journée",
        "m": {
            "sommeil": {"s": 6.2, "c": 6.15, "n": 6.55, "tc": 120, "tn": 12},
            "energie": {"s": 62, "c": 60, "n": 69, "tc": 120, "tn": 18},
            "argent": {"s": 1140, "rc": 4.1, "rn": 7.0},
            "objectif": {"s": 38, "rc": .137, "rn": .233, "lin": 1},
        },
        "auto": {
            "name": "Dernier café", "touch": ["Téléphone", "Montre"],
            "steps": [("14 h 30", "Rappel : « Dernier café de la journée ? »"),
                      ("Après 15 h", "Proposition : décaféiné ou 10 minutes de marche"),
                      ("Vendredi", "Bilan : nuits avec et sans café tardif, côte à côte")],
            "book": "Why We Sleep", "author": "Matthew Walker",
            "principle": "la caféine agit encore des heures après la tasse : une heure limite fixe vaut mieux que la sensation du moment.",
            "yes": "Actif dès demain. Effet estimé : +{d} de sommeil par nuit d’ici {h} jours.",
            "no": "Rien ne change. Si l’habitude continue : environ {c} par nuit sur {h} jours. "
                  "Le café reste votre choix; JARVIS ne reproposera pas cette idée avant 7 jours.",
        },
    },
    {
        "k": "achats", "name": "Achats en ligne le soir", "freq": "6 achats en 14 jours", "days": "0100110",
        "effect": "≈ 186 $ par mois",
        "evidence": "Entre 21 h et 23 h, surtout les soirs notés 2 sur 5. Écart avec l’objectif d’épargne : 186 $ par mois.",
        "srcs": ["depenses", "ecran", "humeur", "objectifs"],
        "goal": "Économiser 3 000 $",
        "basis": "60 jours de catégories de dépenses d’Alex + notes d’humeur saisies volontairement",
        "m": {
            "energie": {"s": 62, "c": 61, "n": 64, "tc": 120, "tn": 30},
            "argent": {"s": 1140, "rc": 4.1, "rn": 10.3},
            "objectif": {"s": 38, "rc": .137, "rn": .343, "lin": 1},
        },
        "auto": {
            "name": "Panier qui dort", "touch": ["Téléphone", "Banque · lecture seule"],
            "steps": [("21 h à 23 h", "Les achats en ligne attendent 24 h dans un panier"),
                      ("Le lendemain", "Question : « Toujours envie ? » · oui ou non, sans commentaire"),
                      ("Vendredi", "Les montants évités sont proposés à l’épargne, avec votre accord")],
            "book": "Nudge", "author": "Richard Thaler et Cass Sunstein",
            "principle": "changer le chemin par défaut plutôt que compter sur la volonté : l’attente fait le tri à votre place.",
            "yes": "Actif dès ce soir. Effet estimé : {d} de plus vers l’épargne d’ici {h} jours.",
            "no": "Rien ne change. Si l’habitude continue : environ {c} d’épargne à {h} jours, "
                  "{lost} de moins qu’avec le changement. C’est votre argent et votre décision.",
        },
    },
    {
        "k": "course", "name": "Course sautée après 18 h", "freq": "2 séances sur 3", "days": "0101000",
        "effect": "10 km : 3 semaines de retard",
        "evidence": "Mardi et jeudi : réunion jusqu’à 18 h, retour en voiture à 18 h 52, course annulée. "
                    "Le matin, la météo est sèche 5 jours sur 7.",
        "srcs": ["agenda", "activite", "voiture", "meteo", "objectifs"],
        "goal": "Courir un 10 km en mars",
        "basis": "6 semaines de séances, d’agenda et de trajets d’Alex + progression type d’un plan 10 km",
        "m": {
            "sommeil": {"s": 6.2, "c": 6.15, "n": 6.45, "tc": 120, "tn": 30},
            "energie": {"s": 62, "c": 58, "n": 72, "tc": 120, "tn": 28},
            "objectif": {"s": 46, "c": 58, "n": 100, "tc": 160, "tn": 40},
        },
        "auto": {
            "name": "Course du matin", "touch": ["Agenda", "Maison", "Montre"],
            "steps": [("Veille", "Réunion après 17 h 30 ? La course passe à 6 h 45"),
                      ("21 h 45", "Rappel : vêtements prêts, réveil réglé à 6 h 20"),
                      ("6 h 20", "Thermostat à 20 °C, lumière progressive"),
                      ("Pluie", "Parcours couvert proposé, même durée")],
            "book": "Tiny Habits", "author": "BJ Fogg",
            "principle": "accrocher la nouvelle habitude à une habitude déjà solide : après le réveil, les chaussures.",
            "yes": "Actif dès mardi. Effet estimé : objectif 10 km à {n} d’ici {h} jours.",
            "no": "Rien ne change dans l’agenda. Si l’habitude continue : objectif 10 km à environ {c} à {h} jours. "
                  "Vous pouvez aussi ajuster l’objectif lui-même : c’est une option honnête.",
        },
    },
    {
        "k": "repas", "name": "Repas du midi sauté", "freq": "3 jours sur 5", "days": "1011000",
        "effect": "Énergie −22 % vers 15 h",
        "evidence": "Les jours sans repas du midi (photo absente, agenda plein de 11 h à 13 h), l’humeur notée baisse "
                    "et la fréquence cardiaque monte en après-midi.",
        "srcs": ["repas", "agenda", "humeur", "coeur"],
        "goal": "Courir un 10 km en mars",
        "basis": "4 semaines de repas saisis et de notes d’humeur d’Alex · lien observé, pas une cause prouvée",
        "m": {
            "energie": {"s": 62, "c": 57, "n": 75, "tc": 120, "tn": 14},
            "objectif": {"s": 46, "c": 50, "n": 62, "tc": 160, "tn": 60},
        },
        "auto": {
            "name": "Midi protégé", "touch": ["Agenda", "Téléphone"],
            "steps": [("Chaque jour", "Bloc protégé de 11 h 45 à 12 h 30 dans l’agenda"),
                      ("11 h 40", "Rappel : « Repas ? » · une photo suffit"),
                      ("Dimanche", "Trois idées de repas préparés, d’après vos photos")],
            "book": "The Power of Habit", "author": "Charles Duhigg",
            "principle": "garder le signal et la récompense, changer seulement la routine : la pause reste, le repas s’y installe.",
            "yes": "Actif dès demain. Effet estimé : énergie à {n} d’ici {h} jours.",
            "no": "Rien ne change dans l’agenda. Si l’habitude continue : énergie à environ {c} à {h} jours. "
                  "Lien observé chez Alex, pas une cause prouvée.",
        },
    },
]

# ---------------------------------------------------------------------------
# 5. Coach de vie : objectifs, semaine, conseils (3 tons), engagements
# ---------------------------------------------------------------------------
GOALS = [
    {"k": "course", "name": "Courir un 10 km en mars", "now": "6,2 km", "target": "10 km", "p": 46,
     "next": "Prochaine étape : 7 km samedi", "src": "activite"},
    {"k": "argent", "name": "Économiser 3 000 $", "now": "1 140 $", "target": "3 000 $", "p": 38,
     "next": "75 $ par semaine pour y arriver en juin", "src": "depenses"},
    {"k": "sommeil", "name": "Dormir 7 h", "now": "6 h 12", "target": "7 h", "p": 31,
     "next": "2 nuits sur 7 au-dessus de 7 h", "src": "sommeil"},
]

DAYS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
# Plan de la semaine : (jour, voie, libellé, état) · état : ok, miss, plan, move
WEEK = [
    (0, "course", "5 km à 18 h 30", "ok"),
    (1, "course", "5 km à 18 h 30", "miss"),
    (3, "course", "5 km à 18 h 30", "miss"),
    (5, "course", "Sortie de 7 km", "plan"),
    (4, "argent", "Virement de 75 $", "plan"),
    (0, "sommeil", "Coucher 23 h 40", "miss"),
    (1, "sommeil", "Coucher 22 h 55", "ok"),
    (2, "sommeil", "Coucher 0 h 34", "miss"),
    (3, "sommeil", "Coucher 23 h 05", "ok"),
    (4, "sommeil", "Coucher 23 h", "plan"),
    (5, "sommeil", "Coucher 23 h", "plan"),
    (6, "sommeil", "Coucher 23 h", "plan"),
]
LANE_NAME = {"course": "Course", "argent": "Épargne", "sommeil": "Sommeil"}

TONES = [("doux", "Doux"), ("direct", "Direct"), ("exigeant", "Exigeant")]
ADVICE = [
    {
        "k": "course", "srcs": ["agenda", "activite", "meteo"],
        "seen": "Mardi et jeudi ratés : vos réunions de 18 h.",
        "t": {"doux": "Ces soirs-là, la journée décide pour vous. Déplaçons la course à 6 h 45 : la météo est sèche et l’agenda est libre.",
              "direct": "Deux courses ratées, même cause : les réunions de 18 h. Mardi et jeudi, course à 6 h 45.",
              "exigeant": "Deux séances perdues, trois semaines de retard sur le 10 km. Mardi et jeudi, c’est 6 h 45. "
                          "Si ce n’est pas possible, changeons l’objectif plutôt que de le rater en silence."},
        "act": "Déplacer à 6 h 45", "done": "Déplacée à 6 h 45 · mardi et jeudi",
        "book": "Atomic Habits", "author": "James Clear",
        "principle": "miser sur le système plutôt que sur la motivation : une heure fixe protège mieux qu’une bonne intention.",
        "quote": "Chaque habitude se fortifie par les actes qui lui correspondent : celle de courir, en courant.",
        "qa": "Épictète", "qw": "Entretiens, II, 18",
    },
    {
        "k": "sommeil", "srcs": ["ecran", "sommeil", "maison"],
        "seen": "Mercredi : 1 h 12 d’écran au lit, endormie à 0 h 34.",
        "t": {"doux": "Et si le téléphone dormait dans la cuisine dès 22 h 45 ? Le réveil de la chambre prend le relais.",
              "direct": "Le téléphone au lit vous coûte 42 min de sommeil. Chargez-le dans la cuisine dès 22 h 45.",
              "exigeant": "Cinq soirs sur sept, l’écran gagne. À 22 h 45, le téléphone sort de la chambre, sans exception en semaine."},
        "act": "Ajouter au plan", "done": "Ajouté · chaque soir à 22 h 45",
        "book": "Digital Minimalism", "author": "Cal Newport",
        "principle": "choisir ses outils d’après ce qui compte pour soi, puis leur donner une place et une heure.",
        "quote": "Ce n’est pas que nous ayons peu de temps, c’est que nous en perdons beaucoup.",
        "qa": "Sénèque", "qw": "De la brièveté de la vie",
    },
    {
        "k": "argent", "srcs": ["depenses", "humeur", "objectifs"],
        "seen": "Jeudi soir : 2 achats en ligne (84 $) après une journée notée 2 sur 5.",
        "t": {"doux": "Les soirs difficiles coûtent cher, et c’est humain. Ces soirs-là, le panier peut attendre 24 h.",
              "direct": "84 $ jeudi soir, une journée notée 2 sur 5. Panier d’attente de 24 h après 21 h.",
              "exigeant": "186 $ par mois partent le soir, c’est 4 mois de retard sur votre épargne. "
                          "Le virement de 75 $ part vendredi, avant toute autre dépense."},
        "act": "Activer le panier d’attente", "done": "Panier d’attente actif · 21 h à 23 h",
        "book": "The Psychology of Money", "author": "Morgan Housel",
        "principle": "l’épargne naît de l’écart entre ce qu’on gagne et ce qu’on désire, bien plus que du revenu.",
        "quote": "Prenez garde aux petites dépenses : une petite voie d’eau suffit à couler un grand navire.",
        "qa": "Benjamin Franklin", "qw": "Le Chemin de la fortune",
    },
    {
        "k": "sommeil", "srcs": ["sommeil", "humeur"],
        "seen": "Dimanche : coucher à 0 h 40, lundi noté 2 sur 5.",
        "t": {"doux": "Visons la même heure de coucher chaque soir, même le week-end : 23 h, à 30 minutes près.",
              "direct": "Coucher irrégulier de 1 h 45 entre la semaine et le week-end. Cible : 23 h, tous les soirs.",
              "exigeant": "Le dimanche défait la semaine. 23 h tous les soirs, week-end compris; le rappel ne se reporte pas."},
        "act": "Fixer 23 h ± 30 min", "done": "Coucher cible : 23 h ± 30 min, 7 soirs sur 7",
        "book": "Why We Sleep", "author": "Matthew Walker",
        "principle": "la régularité de l’heure du coucher compte presque autant que la durée de la nuit.",
        "quote": "Au point du jour, quand tu as peine à te lever, dis-toi : je me lève pour faire œuvre d’homme.",
        "qa": "Marc Aurèle", "qw": "Pensées, V, 1",
    },
]

PACTS = [
    ("ami", "Prévenir Sam, mon ami de course, si je saute deux séances de suite", "Message court, jamais vos données", "course"),
    ("virement", "Virement automatique de 75 $ chaque vendredi vers l’épargne", "Avant les autres dépenses", "argent"),
    ("reveil", "Réveil à l’autre bout de la chambre", "Rappel au coucher s’il est resté sur la table de chevet", "sommeil"),
    ("verrou", "Mode nuit verrouillé de 23 h à 6 h", "Déverrouiller demande 60 secondes d’attente", "sommeil"),
]
PACT_BOOK = ("Indistractable", "Nir Eyal",
             "un engagement décidé à froid protège des moments faibles, à condition qu’on l’ait choisi soi-même.")
PACT_QUOTE = ("Nous avons plus de force que de volonté.", "La Rochefoucauld", "Maximes, 30")

# ---------------------------------------------------------------------------
# Projections (même formule dans vie.js : project)
# ---------------------------------------------------------------------------
HORIZONS = [30, 90, 365]
H0, M0, HOR0 = 0, "sommeil", 90


def _lvl(s, end, tau, t):
    return s + (end - s) * (1 - math.exp(-t / tau))


def project(spec, kind, t):
    """Valeur à t jours : kind = c (continuer), n (changer), w (changer seul)."""
    if "rc" in spec:
        rc, rn = spec["rc"], spec["rn"]
        r = {"c": rc, "n": rn, "w": rc + WILL * (rn - rc)}[kind]
        v = spec["s"] + r * t
    else:
        s, c, n = spec["s"], spec["c"], spec["n"]
        if kind == "c":
            v = _lvl(s, c, spec["tc"], t)
        elif kind == "n":
            v = _lvl(s, n, spec["tn"], t)
        else:
            v = _lvl(s, c + WILL * (n - c), spec["tn"] * 1.6, t)
    return v


def _cap(m, v):
    return min(v, 100) if m in ("objectif", "energie") else v


def fmt(m, v):
    if m == "sommeil":
        mins = round(v * 60)
        return f"{mins // 60}{NBSP}h{NBSP}{mins % 60:02d}"
    if m == "argent":
        return fr(f"{round(v / 10) * 10:,}".replace(",", " ")) + NBSP + "$"
    if m == "objectif":
        return f"{round(v)}{NBSP}%"
    return f"{round(v)}"


def _nice(lo, hi, m):
    span = hi - lo
    raw = span / 3
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    step = next(s * mag for s in (1, 2, 2.5, 5, 10) if s * mag >= raw)
    if m == "sommeil":
        step = max(0.25, round(step * 4) / 4)
    a = math.floor(lo / step) * step
    b = math.ceil(hi / step) * step
    return a, b, step


def chart_model(h, m, hor):
    spec = h["m"][m]
    n = 48
    ts = [hor * i / n for i in range(n + 1)]
    ser = {k: [_cap(m, project(spec, k, t)) for t in ts] for k in "cnw"}
    vals = ser["c"] + ser["n"] + ser["w"]
    goal = dict((x[0], x[3]) for x in METRICS)[m]
    lo, hi = min(vals), max(vals)
    if goal is not None and goal <= hi * 1.25 and goal >= lo:
        hi = max(hi, goal)
    pad = (hi - lo) * .12 or 1
    a, b, step = _nice(lo - pad, hi + pad, m)
    if m in ("objectif", "energie"):
        b = min(b, 100)
    return ts, ser, a, b, step


def _path(ts, vals, a, b, hor):
    pts = [(t / hor * 1000, 400 - (v - a) / (b - a) * 400) for t, v in zip(ts, vals)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _band(ts, ser, a, b, hor):
    up, dn = [], []
    for t, c, n in zip(ts, ser["c"], ser["n"]):
        d = abs(n - c) * .15
        up.append((t, n + d))
        dn.append((t, n - d))
    pts = up + dn[::-1]
    return "M" + " L".join(f"{t / hor * 1000:.1f} {400 - (v - a) / (b - a) * 400:.1f}" for t, v in pts) + " Z"


# ---------------------------------------------------------------------------
# Balisage
# ---------------------------------------------------------------------------
def _src_row(s, side, i):
    k, name, dev, reads, val, ic, sig = s
    return (f'<li class="pi-src" data-src="{k}" style="--i:{i}"><span class="pi-src-ic">{icon(ic)}</span>'
            f'<span class="pi-src-t"><b>{e(name)}<small>{e(dev)}</small></b><span class="pi-src-r">{e(reads)}</span>'
            f'<span class="pi-src-v" data-pi-v>{e(val)}</span></span>'
            f'<button type="button" class="pi-sw" role="switch" aria-checked="true" aria-label="Permission · {e(name)}"><i></i></button>'
            f'</li>')


def _flows(side, n):
    out = []
    for i in range(n):
        y = (i + .5) / n * 700
        if side == "l":
            d = f"M0 {y:.1f} C55 {y:.1f} 45 350 100 350"
        else:
            d = f"M100 {y:.1f} C45 {y:.1f} 55 350 0 350"
        out.append(f'<path class="pi-fl" data-i="{i}" d="{d}" vector-effect="non-scaling-stroke"/>'
                   f'<path class="pi-fd" data-i="{i}" d="{d}" pathLength="100" vector-effect="non-scaling-stroke" style="--d:{(i * .37) % 1.6:.2f}s"/>')
    return (f'<svg class="pi-flows pi-flows-{side}" viewBox="0 0 100 700" preserveAspectRatio="none" aria-hidden="true">'
            + "".join(out) + "</svg>")


def _ring(r, p, cls):
    c = 2 * math.pi * r
    return (f'<circle class="pi-ring-bg" cx="60" cy="60" r="{r}"/>'
            f'<circle class="pi-ring {cls}" cx="60" cy="60" r="{r}" pathLength="100" style="--p:{p}"/>')


def _core():
    total = sum(s[6] for s in SOURCES)
    return f"""<div class="pi-core" data-pi="core">
        <div class="pi-core-in pi-rim">
          <p class="pi-k">{icon("chip")}<span>Modèle personnel</span></p>
          <div class="pi-orb">
            <svg viewBox="0 0 120 120" aria-hidden="true">{_ring(54, 89, "r1")}{_ring(45, 64, "r2")}{_ring(36, 38, "r3")}</svg>
            <img src="/media/vision/alex-portrait.webp" alt="Alex, la personne de la démonstration" width="320" height="320" loading="lazy" decoding="async">
          </div>
          <ul class="pi-legend">
            <li><i class="r1"></i>Sommeil <b>6{NBSP}h{NBSP}12</b><small>sur 7{NBSP}h</small></li>
            <li><i class="r2"></i>Énergie <b>64</b><small>sur 100</small></li>
            <li><i class="r3"></i>Objectifs <b>38{NBSP}%</b><small>en moyenne</small></li>
          </ul>
          <div class="pi-core-stats">
            <p><b data-pi="count">13</b><span>sources sur 13</span></p>
            <p><b data-pi="signals">{fr(f"{total * 7:,}".replace(",", " "))}</b><span>signaux cette semaine</span></p>
          </div>
          <p class="pi-core-hub">{icon("lock")}<span>Calculé sur le <b>Hub JARVIS</b>, chez Alex</span></p>
        </div>
      </div>"""


def _sources_html():
    left = "".join(_src_row(s, "l", i) for i, s in enumerate(LEFT))
    right = "".join(_src_row(s, "r", i) for i, s in enumerate(RIGHT))
    return f"""<section class="pi-sec pi-feedsec" aria-label="Sources et modèle personnel">
      <header class="pi-sh"><span class="pi-n">1</span><div><h3>Treize sources, <em>une permission chacune</em></h3>
        <p>Chaque source dit ce qu’elle lit. Retirez-en une : son flux s’arrête et JARVIS cesse d’en déduire quoi que ce soit.</p></div></header>
      <div class="pi-net">
        <ul class="pi-srcs pi-srcs-l">{left}</ul>
        {_flows("l", len(LEFT))}
        {_core()}
        {_flows("r", len(RIGHT))}
        <ul class="pi-srcs pi-srcs-r">{right}</ul>
      </div>
    </section>"""


def _chips(srcs):
    return "".join(f'<span data-src="{s}">{icon(SRC[s][5])}{e(SRC[s][1])}</span>' for s in srcs)


def _habit_card(i, h):
    dots = "".join(f'<i class="{"is-on" if c == "1" else ""}" title="{DAYS[j]}"></i>' for j, c in enumerate(h["days"]))
    return (f'<li><button type="button" class="pi-hab" data-habit="{i}" aria-pressed="{"true" if i == H0 else "false"}">'
            f'<span class="pi-hab-top"><b>{e(h["name"])}</b></span>'
            f'<span class="pi-hab-row"><span class="pi-hab-dots" aria-hidden="true">{dots}</span>'
            f'<span class="pi-hab-f">{e(h["freq"])}</span></span>'
            f'<span class="pi-hab-fx">{icon("bolt")}<span>{e(h["effect"])}</span></span>'
            f'<span class="pi-hab-miss">{icon("lock")}<span>Non détectée · il manque <b data-pi-need></b></span></span>'
            f'</button></li>')


def _kpis(h, hor):
    out = []
    for m, label, unit, _g, _gl in METRICS:
        spec = h["m"].get(m)
        if spec:
            c, n = _cap(m, project(spec, "c", hor)), _cap(m, project(spec, "n", hor))
            val = _delta(m, n - c)
        else:
            val = "Aucun effet estimé"
        out.append(f'<button type="button" class="pi-kpi" data-metric="{m}" aria-pressed="{"true" if m == M0 else "false"}"'
                   f'{" disabled" if not spec else ""}><span>{e(label)}</span><b data-pi-kv>{val}</b></button>')
    return "".join(out)


def _delta(m, d):
    sign = "+" if d >= 0 else "−"
    a = abs(d)
    if m == "sommeil":
        return f"{sign}{round(a * 60)}{NBSP}min par nuit"
    if m == "argent":
        return f"{sign}{fr(f'{round(a / 10) * 10:,}'.replace(',', ' '))}{NBSP}$"
    if m == "objectif":
        return f"{sign}{round(a)}{NBSP}points"
    return f"{sign}{round(a)}{NBSP}points"


def _chart_html(h):
    ts, ser, a, b, step = chart_model(h, M0, HOR0)
    ticks = []
    v = a
    while v <= b + 1e-9:
        ticks.append(f'<span style="--y:{(v - a) / (b - a) * 100:.2f}">{fmt(M0, v)}</span>')
        v += step
    goal = 7.0
    gy = (goal - a) / (b - a) * 100
    hors = "".join(f'<button type="button" data-hor="{x}" aria-pressed="{"true" if x == HOR0 else "false"}">{x}{NBSP}jours</button>'
                   for x in HORIZONS)
    cend, nend = ser["c"][-1], ser["n"][-1]
    return f"""<div class="pi-fut pi-rim" data-pi="fut">
          <div class="pi-fut-head">
            <p class="pi-k">{icon("spark")}<span>Deux avenirs · <b data-pi="mlabel">Sommeil par nuit</b></span></p>
            <div class="pi-seg" role="group" aria-label="Horizon de la projection">{hors}</div>
          </div>
          <div class="pi-kpis" role="group" aria-label="Mesure projetée">{_kpis(h, HOR0)}</div>
          <div class="pi-chart" data-pi="chart">
            <div class="pi-yax" data-pi="yax" aria-hidden="true">{"".join(ticks)}</div>
            <div class="pi-plot" data-pi="plot" role="img" aria-label="Projection estimée">
              <svg viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true">
                <defs><linearGradient id="pi-gain" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".26"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>
                <path class="pi-band" data-pi="band" d="{_band(ts, ser, a, b, HOR0)}"/>
                <path class="pi-ln pi-ln-c" data-pi="lc" pathLength="1" d="{_path(ts, ser["c"], a, b, HOR0)}" vector-effect="non-scaling-stroke"/>
                <path class="pi-ln pi-ln-w" data-pi="lw" pathLength="1" d="{_path(ts, ser["w"], a, b, HOR0)}" vector-effect="non-scaling-stroke"/>
                <path class="pi-ln pi-ln-n" data-pi="ln" pathLength="1" d="{_path(ts, ser["n"], a, b, HOR0)}" vector-effect="non-scaling-stroke"/>
              </svg>
              <span class="pi-goal" data-pi="goal" style="--y:{gy:.2f}"><span>Objectif : 7{NBSP}h</span></span>
              <span class="pi-end pi-end-n" data-pi="en" style="--y:{(nend - a) / (b - a) * 100:.2f}"><b>{fmt(M0, nend)}</b><span data-pi="en-l">Si vous changez</span></span>
              <span class="pi-end pi-end-w" data-pi="ew"><b></b><span>Par vous-même</span></span>
              <span class="pi-end pi-end-c" data-pi="ec" style="--y:{(cend - a) / (b - a) * 100:.2f}"><b>{fmt(M0, cend)}</b><span>Si vous continuez</span></span>
              <span class="pi-cross" data-pi="cross" aria-hidden="true"><i class="c"></i><i class="n"></i><i class="w"></i></span>
              <div class="pi-tip" data-pi="tip" aria-hidden="true"></div>
            </div>
            <div class="pi-xax" data-pi="xax" aria-hidden="true"><span>Aujourd’hui</span><span data-pi="xmid">Jour {HOR0 // 2}</span><span data-pi="xend">Jour {HOR0}</span></div>
          </div>
          <div class="pi-lgd">
            <span class="c"><i></i>Si vous continuez</span>
            <span class="n"><i></i><span data-pi="nl">Si vous changez</span></span>
            <span class="w"><i></i>Par vous-même, sans automatisation</span>
            <span class="b"><i></i>Marge d’estimation ± 15{NBSP}%</span>
          </div>
          <p class="pi-basis">{icon("spark")}<span><b>Estimation, pas une promesse.</b> Base : <span data-pi="basis">{e(h["basis"])}</span>.</span></p>
        </div>"""


def _auto_html(h):
    a = h["auto"]
    steps = "".join(f'<li style="--i:{i}"><time>{e(t)}</time><span>{e(x)}</span></li>' for i, (t, x) in enumerate(a["steps"]))
    touch = "".join(f"<span>{e(t)}</span>" for t in a["touch"])
    return f"""<div class="pi-auto pi-rim" data-pi="auto" data-state="ask">
          <div class="pi-auto-head">
            <p class="pi-k">{icon("bolt")}<span>L’automatisation qui règle ça</span></p>
            <span class="pi-touch" data-pi="touch">{touch}</span>
          </div>
          <h4 data-pi="aname">{e(a["name"])}</h4>
          <ol class="pi-steps" data-pi="steps">{steps}</ol>
          <p class="pi-book">{icon("book")}<span>Principe tiré de <cite data-pi="abook">{e(a["book"])}</cite> (<span data-pi="aauth">{e(a["author"])}</span>) : <span data-pi="aprin">{e(a["principle"])}</span></span></p>
          <div class="pi-ask">
            <button type="button" class="pi-yes" data-pi="yes">{icon("check")}Approuver</button>
            <button type="button" class="pi-no" data-pi="no">Refuser</button>
          </div>
          <div class="pi-out pi-out-yes">{icon("check")}<p><b>Approuvé · révocable en un geste.</b> <span data-pi="yes-t"></span></p>
            <button type="button" data-pi="undo">{icon("undo")}Retirer l’accord</button></div>
          <div class="pi-out pi-out-no">{icon("x")}<p><b>Refusé, c’est noté.</b> <span data-pi="no-t"></span></p>
            <button type="button" data-pi="undo2">{icon("undo")}Revoir ma décision</button></div>
          <p class="pi-blocked">{icon("lock")}<span>Cette habitude a besoin de <b data-pi="need">Temps d’écran</b>. Permission retirée : JARVIS ne déduit rien sans elle.</span></p>
        </div>"""


def _habits_html():
    h = HABITS[H0]
    cards = "".join(_habit_card(i, x) for i, x in enumerate(HABITS))
    return f"""<section class="pi-sec pi-hsec" aria-label="Habitudes, deux avenirs et automatisations">
      <header class="pi-sh"><span class="pi-n">2</span><div><h3>Vos habitudes, <em>leurs effets, deux avenirs</em></h3>
        <p>Chaque habitude vient avec sa preuve. Choisissez-en une : JARVIS projette ce qui arrive si vous continuez,
        et ce qui change si vous changez.</p></div></header>
      <div class="pi-hgrid">
        <div class="pi-hcol">
          <p class="pi-k">{icon("spark")}<span>Habitudes détectées · 3 semaines</span></p>
          <ul class="pi-habs">{cards}</ul>
          <div class="pi-evi" data-pi="evi">
            <p class="pi-evi-k">Preuve</p>
            <p data-pi="evidence">{e(h["evidence"])}</p>
            <p class="pi-chips" data-pi="chips">{_chips(h["srcs"])}</p>
          </div>
        </div>
        <div class="pi-rcol">
          {_chart_html(h)}
          {_auto_html(h)}
        </div>
      </div>
    </section>"""


def _goal_ring(p):
    return (f'<svg viewBox="0 0 48 48" aria-hidden="true"><circle class="pi-gr-bg" cx="24" cy="24" r="20"/>'
            f'<circle class="pi-gr" cx="24" cy="24" r="20" pathLength="100" style="--p:{p}"/></svg>')


def _coach_html():
    goals = "".join(
        f'<li class="pi-goalc" data-goal="{g["k"]}" style="--i:{i}"><div class="pi-gring">{_goal_ring(g["p"])}<b>{g["p"]}<small>%</small></b></div>'
        f'<div><p class="pi-gname">{e(g["name"])}</p><p class="pi-gnow"><b>{e(g["now"])}</b> sur {e(g["target"])}</p>'
        f'<p class="pi-gnext">{e(g["next"])}</p></div></li>' for i, g in enumerate(GOALS))
    heads = "".join(f"<span>{d}</span>" for d in DAYS)
    lanes = []
    for lane in ("course", "sommeil", "argent"):
        cells = []
        for d in range(7):
            items = [w for w in WEEK if w[0] == d and w[1] == lane]
            inner = ""
            for _d, _l, lab, st in items:
                ic = {"ok": icon("check"), "miss": icon("x"), "plan": ""}[st]
                inner += f'<span class="pi-it is-{st}" data-day="{d}" title="{e(lab)}">{ic}<em>{e(lab)}</em></span>'
            cells.append(f'<div class="pi-cell">{inner}</div>')
        lanes.append(f'<div class="pi-lane" data-lane="{lane}"><span class="pi-lane-n">{LANE_NAME[lane]}</span>{"".join(cells)}</div>')
    tones = "".join(f'<button type="button" data-tone="{k}" aria-pressed="{"true" if k == "doux" else "false"}">{n}</button>'
                    for k, n in TONES)
    advice = "".join(
        f'<li class="pi-adv" data-adv="{i}" data-state="ask" style="--i:{i}">'
        f'<p class="pi-seen">{icon("spark")}<span>{e(a["seen"])}</span></p>'
        f'<p class="pi-say" data-pi-say>{e(a["t"]["doux"])}</p>'
        f'<p class="pi-book">{icon("book")}<span>Principe tiré de <cite>{e(a["book"])}</cite> ({e(a["author"])}) : {e(a["principle"])}</span></p>'
        f'<blockquote class="pi-q">{icon("quote")}<p>{e(a["quote"])}</p><footer>{e(a["qa"])}, <cite>{e(a["qw"])}</cite></footer></blockquote>'
        f'<div class="pi-adv-act"><button type="button" class="pi-apply" data-pi-apply>{e(a["act"])}</button>'
        f'<span class="pi-done">{icon("check")}{e(a["done"])}</span></div>'
        f'<p class="pi-adv-off">{icon("lock")}Conseil en pause · il manque <b data-pi-need></b></p></li>'
        for i, a in enumerate(ADVICE))
    pacts = "".join(
        f'<li class="pi-pact" data-pact="{k}"><div><b>{e(t)}</b><small>{e(sub)}</small></div>'
        f'<button type="button" class="pi-sw" role="switch" aria-checked="false" aria-label="{e(t)}"><i></i></button>'
        f'<span class="pi-pact-on">{icon("check")}Choisi par vous aujourd’hui · révocable en un geste</span></li>'
        for k, t, sub, _g in PACTS)
    b, au, pr = PACT_BOOK
    q, qa, qw = PACT_QUOTE
    return f"""<section class="pi-sec pi-csec" aria-label="Coach de vie">
      <header class="pi-sh"><span class="pi-n">3</span><div><h3>Un coach de vie <em>qui voit votre vraie semaine</em></h3>
        <p>Vos objectifs, ce qui s’est réellement passé, des conseils concrets tirés des meilleurs livres,
        et des engagements que vous choisissez pour vous tenir à ce que vous voulez.</p></div>
        <div class="pi-tone"><span>Style du coach</span><div class="pi-seg" role="group" aria-label="Style du coach">{tones}</div></div></header>
      <div class="pi-cgrid">
        <div class="pi-goals-w">
          <p class="pi-k">{icon("target")}<span>Objectifs choisis par Alex</span></p>
          <ul class="pi-goals">{goals}</ul>
        </div>
        <div class="pi-week-w">
          <div class="pi-week-h"><p class="pi-k">{icon("calendar")}<span>Semaine du 2 novembre · aujourd’hui vendredi</span></p>
            <span class="pi-week-s"><b>{sum(w[3] == "ok" for w in WEEK)}</b> faits · <b>{sum(w[3] == "miss" for w in WEEK)}</b> ratés · <b>{sum(w[3] == "plan" for w in WEEK)}</b> prévus</span></div>
          <div class="pi-week" data-pi="week"><div class="pi-wh"><span></span>{heads}</div>{"".join(lanes)}</div>
          <p class="pi-adapt" data-pi="adapt">{icon("spark")}<span>Le plan s’ajuste à ce qui arrive vraiment : agenda, météo, fatigue. Rien ne bouge sans votre accord.</span></p>
        </div>
      </div>
      <div class="pi-advw">
        <p class="pi-k">{icon("spark")}<span>Conseils de la semaine · d’après ce qui s’est passé</span></p>
        <ol class="pi-advs">{advice}</ol>
      </div>
      <div class="pi-pacts-w pi-rim">
        <div class="pi-pacts-h">
          <p class="pi-k">{icon("shield")}<span>Engagements · vous choisissez, vous pouvez retirer</span></p>
          <span class="pi-pacts-c"><b data-pi="pacts">0</b> actif sur 4</span>
        </div>
        <ul class="pi-pacts">{pacts}</ul>
        <div class="pi-pacts-f">
          <p class="pi-book">{icon("book")}<span>Principe tiré de <cite>{e(b)}</cite> ({e(au)}) : {e(pr)}</span></p>
          <blockquote class="pi-q">{icon("quote")}<p>{e(q)}</p><footer>{e(qa)}, <cite>{e(qw)}</cite></footer></blockquote>
        </div>
      </div>
    </section>"""


def _data():
    return {
        "sources": [{"k": s[0], "name": fr(s[1]), "sig": s[6], "side": 0 if i < len(LEFT) else 1,
                     "i": i if i < len(LEFT) else i - len(LEFT)} for i, s in enumerate(SOURCES)],
        "metrics": [{"k": m, "label": fr(lab), "goal": g, "goalL": fr(gl)} for m, lab, _u, g, gl in METRICS],
        "will": WILL,
        "habits": [{
            "k": h["k"], "srcs": h["srcs"], "evidence": fr(h["evidence"]), "basis": fr(h["basis"]), "goal": fr(h["goal"]),
            "m": h["m"], "chips": _chips(h["srcs"]),
            "auto": {"name": fr(h["auto"]["name"]), "touch": [fr(t) for t in h["auto"]["touch"]],
                     "steps": [[fr(t), fr(x)] for t, x in h["auto"]["steps"]],
                     "book": fr(h["auto"]["book"]), "author": fr(h["auto"]["author"]), "principle": fr(h["auto"]["principle"]),
                     "yes": fr(h["auto"]["yes"]), "no": fr(h["auto"]["no"])},
        } for h in HABITS],
        "advice": [{"k": a["k"], "srcs": a["srcs"], "t": {k: fr(v) for k, v in a["t"].items()}} for a in ADVICE],
        "move": [1, 3],
    }


def html():
    return f"""<div class="demo-shell pi" data-demo="vie" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Personal Intelligence</b>
    <span class="pi-clock">Alex · semaine du 2{NBSP}novembre</span><span class="tag tag-sim">Données d’exemple</span></div>
  <div class="demo-body pi-body">
    {_sources_html()}
    {_habits_html()}
    {_coach_html()}
  </div>
  <div class="pi-foot">
    <p class="pi-priv">{icon("lock")}<span><b>Tout est calculé localement sur le JARVIS Hub, chez vous.</b>
      Aucune donnée ne part dans un nuage; chaque source se retire en un geste et ce qui en venait est effacé.</span></p>
    <ul class="pi-rules">
      <li>{icon("spark")}Chaque déduction montre sa preuve</li>
      <li>{icon("check")}Rien ne change sans votre accord</li>
      <li>{icon("shield")}Bien-être seulement, aucun diagnostic</li>
    </ul>
  </div>
  <p class="pi-sr" aria-live="polite" data-pi="live"></p>
  <script type="application/json" data-pi="data">{json.dumps(_data(), ensure_ascii=False)}</script>
</div>
<p class="demo-hint">Retirez une permission · choisissez une habitude et un horizon · approuvez ou refusez · changez le style du coach · tout est fictif</p>"""
