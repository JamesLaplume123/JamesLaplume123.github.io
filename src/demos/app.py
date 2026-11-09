# Démo « JARVIS App » : l'application rendue en vrai HTML/CSS, nette à toutes les tailles.
# Fidèle au dossier User révision 25 : menu Accueil, Mon espace, Carte, Mes outils, Administration;
# bannière du lac au coucher du soleil; barre latérale dorée vitreuse. Neuf écrans (Accueil, Assistant,
# Mon espace, Ma journée, Mes partages, Mes messages, Mes appels, Carte, Mes outils), pilotés par la
# barre latérale (barre d'onglets en bas sur cellulaire). Toute la barre du haut fonctionne : recherche
# (palette de commandes), météo réelle (panneau détaillé), Mes appels, Carte et menu du profil (espace,
# mode d'affichage du site). Un sélecteur Personnel | Professionnel bascule le contenu des deux espaces.
# La Carte est une vraie carte vectorielle noire du sud du Québec (demos/app_geo.py, Natural Earth)
# avec les environnements de James. Styles et script : assets/demos/app.css et app.js.
# Données fictives, sauf l'heure locale, la météo réelle de Saint-Hyacinthe et les batteries de BouLance.

import json
import math
import os
import re

from config import CAPABILITIES
from demos.app_geo import BOX, GEO, ROUTE_KM, SHIELDS

NB = "\u00a0"
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def fr(s):
    """Typographie française : espaces insécables avant : ; ? ! », après «, dans les heures et unités."""
    s = re.sub(r" ([:;?!»])", NB + r"\1", s)
    s = s.replace("« ", "«" + NB)
    s = re.sub(r"(\d) h (\d)", rf"\1{NB}h{NB}\2", s)
    s = re.sub(r"(\d) h\b", rf"\1{NB}h", s)
    s = re.sub(r"(\d) (°C|%|min\b|km\b|Ko\b|jours?\b|pages?\b)", rf"\1{NB}\2", s)
    return s.replace(" – ", NB + "–" + NB).replace(" · ", NB + "· ")


def media(path):
    """Chemin public d'une photo si elle existe au moment du build, sinon None."""
    return path if os.path.exists(os.path.join(_ROOT, path.lstrip("/"))) else None


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
    "micoff": '<path d="M15 10.5V6.5a3 3 0 0 0-5.6-1.5M9 9v2.5a3 3 0 0 0 4.6 2.5"/><path d="M5.75 11.5a6.25 6.25 0 0 0 10.4 4.7M18.25 11.5a6 6 0 0 1-.5 2.4M12 17.75v2.75M4 4l16 16"/>',
    "clip": '<path d="m19.5 11.5-7.4 7.4a4.5 4.5 0 0 1-6.4-6.4l7.7-7.7a3 3 0 0 1 4.2 4.2l-7.5 7.5a1.5 1.5 0 0 1-2.1-2.1l6.8-6.8"/>',
    "doc": '<path d="M7 3.5h6.5L18 8v12.5H7z"/><path d="M13.5 3.5V8H18M9.75 12.5h5.5M9.75 16h5.5"/>',
    "clock": '<circle cx="12" cy="12" r="8.25"/><path d="M12 7.5V12l3 2"/>',
    "user": '<circle cx="12" cy="8.5" r="3.75"/><path d="M4.75 20c.9-3.6 3.75-5.5 7.25-5.5s6.35 1.9 7.25 5.5"/>',
    "users": '<circle cx="9" cy="8.75" r="3.25"/><path d="M3 19.5c.7-3.1 3-4.75 6-4.75s5.3 1.65 6 4.75"/>'
             '<path d="M15.5 5.75a3.25 3.25 0 0 1 0 6M17.5 14.9c1.9.5 3.1 2 3.5 4.6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "checks": '<path d="m2.75 12.75 4 4L15.5 8"/><path d="m11.25 16.25.5.5L20.5 8"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.25"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "info": '<circle cx="12" cy="12" r="8.25"/><path d="M12 11v5"/><path d="M12 7.9v.1"/>',
    "star": '<path d="m12 4 2.4 5 5.35.65-3.95 3.7 1.05 5.35L12 16.05 7.15 18.7l1.05-5.35-3.95-3.7L9.6 9z"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="m4 7.5 8 5.5 8-5.5"/>',
    "chat": '<path d="M4.5 6.5a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H11l-4.25 3.5V16.5H6.5a2 2 0 0 1-2-2z"/><path d="M8.5 9.25h7M8.5 12.25h4.5"/>',
    "map": '<path d="M9 4.75 3.75 6.5v12.75L9 17.5l6 1.75 5.25-1.75V4.75L15 6.5z"/><path d="M9 4.75V17.5M15 6.5v12.75"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "locate": '<circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="1.6"/><path d="M12 2.75v3M12 18.25v3M2.75 12h3M18.25 12h3"/>',
    "expand": '<path d="M4.5 9V4.5H9M15 4.5h4.5V9M19.5 15v4.5H15M9 19.5H4.5V15"/>',
    "phone": '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 17.75h2"/>',
    "call": '<path d="M5.1 4.25h2.8a1 1 0 0 1 .95.68l.97 2.84a1 1 0 0 1-.33 1.1L7.75 10.3a12.4 12.4 0 0 0 5.95 5.95l1.43-1.74a1 1 0 0 1 1.1-.33l2.84.97a1 1 0 0 1 .68.95v2.8a1.15 1.15 0 0 1-1.25 1.15C11 19.4 4.6 13 3.95 5.5A1.15 1.15 0 0 1 5.1 4.25Z"/>',
    "hang": '<path d="M3.2 14.6c-.5-.5-.6-1.3-.1-1.9C5.4 10 8.6 8.6 12 8.6s6.6 1.4 8.9 4.1c.5.6.4 1.4-.1 1.9l-1.6 1.5a1 1 0 0 1-1.2.1l-2.2-1.4a1 1 0 0 1-.45-.9l.1-1.8a10 10 0 0 0-6.9 0l.1 1.8a1 1 0 0 1-.45.9l-2.2 1.4a1 1 0 0 1-1.2-.1z"/>',
    "speaker": '<path d="M4.5 9.5h3l4.5-4v13l-4.5-4h-3z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
    "screen": '<rect x="3" y="4.5" width="18" height="12" rx="2"/><path d="M8.5 20h7M12 16.5V20M12 13V8M9.75 10.25 12 8l2.25 2.25"/>',
    "arrin": '<path d="M18.5 5.5 11 13M11 7.75V13h5.25"/>',
    "arrout": '<path d="M11 13l7.5-7.5M12.75 5.5H18.5v5.75"/>',
    "camera": '<rect x="3.5" y="7" width="12.5" height="10" rx="2.25"/><path d="m16 10.5 4.5-2.5v8L16 13.5"/>',
    "camoff": '<path d="M9.5 7H13.75a2.25 2.25 0 0 1 2.25 2.25v1.25l4.5-2.5v8l-1.6-.9M16 16.25a2.25 2.25 0 0 1-2.25.75H5.75A2.25 2.25 0 0 1 3.5 14.75v-5.5A2.25 2.25 0 0 1 5 7.1M3 3l18 18"/>',
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
    "wind": '<path d="M3.5 9.5h11a2.75 2.75 0 1 0-2.75-2.75M3.5 14h15a2.75 2.75 0 1 1-2.75 2.75M3.5 11.75h6"/>',
    "drop": '<path d="M12 3.75s-5.75 6.1-5.75 10.1a5.75 5.75 0 0 0 11.5 0c0-4-5.75-10.1-5.75-10.1Z"/>',
    "gauge": '<path d="M4.5 16.5a7.5 7.5 0 1 1 15 0"/><path d="m12 16.5 3.5-4.5M12 16.5v.1"/>',
    "thermo": '<path d="M10 14.25V5.5a2 2 0 0 1 4 0v8.75a3.75 3.75 0 1 1-4 0Z"/><path d="M12 11v5"/>',
    "grid": '<rect x="4" y="4" width="6.75" height="6.75" rx="1.75"/><rect x="13.25" y="4" width="6.75" height="6.75" rx="1.75"/>'
            '<rect x="4" y="13.25" width="6.75" height="6.75" rx="1.75"/><rect x="13.25" y="13.25" width="6.75" height="6.75" rx="1.75"/>',
    "sliders": '<path d="M4 7h9M17 7h3M4 12h3M11 12h9M4 17h11M19 17h1"/><path d="M15 5v4M9 10v4M17 15v4"/>',
    "devices": '<rect x="3" y="5" width="13" height="9.5" rx="1.5"/><path d="M2 17.5h15"/><rect x="17.5" y="9" width="4.5" height="9.5" rx="1.2"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.2M12 18.3v2.2M3.5 12h2.2M18.3 12h2.2M6 6l1.55 1.55M16.45 16.45 18 18M6 18l1.55-1.55M16.45 7.55 18 6"/>',
    "flow": '<rect x="3.5" y="4" width="7" height="5.5" rx="1.5"/><rect x="13.5" y="14.5" width="7" height="5.5" rx="1.5"/><path d="M7 9.5v3.25a2 2 0 0 0 2 2h4.5"/><path d="m11.5 12.75 2 2-2 2"/>',
    "net": '<circle cx="12" cy="5.5" r="2"/><circle cx="5" cy="18.5" r="2"/><circle cx="19" cy="18.5" r="2"/><circle cx="12" cy="13" r="2"/><path d="M12 7.5V11M10.4 14.3l-3.9 2.9M13.6 14.3l3.9 2.9"/>',
    "pulse": '<path d="M3 12.5h4l2.25-5.5 4 11 2.5-5.5H21"/>',
    "image": '<rect x="3.5" y="5" width="17" height="14" rx="2.25"/><circle cx="9" cy="10" r="1.6"/><path d="m4 17 5-4.5 4 3.5 3-2.5 4 3.5"/>',
    "rv": '<rect x="2.5" y="6" width="19" height="10.5" rx="2"/><path d="M2.5 10.75h19M7.5 6v4.75M12.5 6v4.75M17.5 6v4.75"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    "barn": '<path d="M3.5 21V10L12 4l8.5 6v11z"/><path d="M8.5 21v-6.5h7V21M8.5 14.5l7 6.5M15.5 14.5 8.5 21M10 9.5h4"/>',
    "garage": '<path d="M3 21V9l9-5 9 5v12"/><path d="M6.5 21v-9h11v9M6.5 15h11M6.5 18h11"/>',
    "tree": '<path d="M12 3 6.5 10.5h3l-4 6h13l-4-6h3zM12 16.5V21"/>',
    "plane": '<path d="M12 3c.9 0 1.5.9 1.5 2v4.5l7 4v2l-7-2v4l2 1.5v1.5l-3.5-1-3.5 1V19.5l2-1.5v-4l-7 2v-2l7-4V5c0-1.1.6-2 1.5-2Z"/>',
    "battery": '<rect x="3" y="7" width="16" height="10" rx="2.25"/><path d="M21.25 10.5v3"/><path d="M6.5 10.25v3.5M9.5 10.25v3.5M12.5 10.25v3.5"/>',
    "logout": '<path d="M14.5 4.5h3a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2h-3M10 16.5 5.5 12 10 7.5M5.5 12h10"/>',
    "palette": '<path d="M12 3.5a8.5 8.5 0 0 0 0 17c1.4 0 2-.9 2-1.9 0-1.4-1.2-1.6-1.2-2.8 0-1 .8-1.8 1.8-1.8h2.2a3.7 3.7 0 0 0 3.7-3.7C20.5 6.6 16.7 3.5 12 3.5Z"/><circle cx="7.75" cy="11.5" r="1"/><circle cx="10.5" cy="7.75" r="1"/><circle cx="15" cy="7.75" r="1"/>',
}


def icon(name, cls=""):
    c = f' class="ap-i {cls}"' if cls else ' class="ap-i"'
    return f'<svg{c} viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


WX = "".join(icon(k, f"wx-{k}") for k in ("sun", "moon", "cloud", "rain", "snow", "fog"))


def mono(initials, tone):
    return f'<span class="ap-mono t-{tone}" aria-hidden="true">{initials}</span>'


def face(src):
    return f'<img class="ap-mono ap-face" src="{src}" alt="" aria-hidden="true" loading="lazy" decoding="async" width="96" height="96">'


# ---------------------------------------------------------------------------------------------
# Menu (révision 25) : clé, libellé, libellé court (cellulaire), icône
# ---------------------------------------------------------------------------------------------
NAV = [
    ("accueil", "Accueil", "Accueil", "home"),
    ("espace", "Mon espace", "Espace", "user"),
    ("carte", "Carte", "Carte", "pin"),
    ("outils", "Mes outils", "Outils", "grid"),
]
ADMIN_NOTE = "Administration : comptes, droits et extensions. Réservée à l’administrateur de votre système."
TITLE = {"accueil": "Accueil", "assistant": "Assistant JARVIS", "espace": "Mon espace", "journee": "Ma journée",
         "partage": "Mes partages", "messages": "Mes messages", "appels": "Mes appels", "carte": "Carte",
         "outils": "Mes outils"}
# Chapitres de la séquence de l'accueil (un appareil par écran)
SEQUENCE = ["accueil", "assistant", "espace", "journee", "partage", "messages", "appels", "carte", "outils"]

# Les écrans, dans l'ordre de la visite : clé, entrée du menu, durée (ms), légende
SCREENS = [
    ("accueil", "accueil", 7500, "Votre journée, sur un seul écran.",
     "Agenda, messages, appels et vos extensions, avec leur état du moment : chacune travaille pour vous et vous dit où elle en est."),
    ("assistant", "accueil", 13000, "Il propose. Vous décidez.",
     "Demandez en mots simples. JARVIS prépare l’action, montre ses sources et attend votre accord."),
    ("espace", "espace", 7500, "Votre quotidien, à votre image.",
     "Agenda, messages, documents, appareils, partages et appels : chaque chose à sa place, en personnel comme en professionnel."),
    ("journee", "espace", 8000, "Tous vos agendas, enfin ensemble.",
     "Calendriers et tâches de toutes vos sources. Ce qui est en lecture seule le reste."),
    ("partage", "espace", 8500, "Vous choisissez ce que vous partagez.",
     "Avec qui, pour combien de temps, et sous votre contrôle. Un accès retiré disparaît partout."),
    ("messages", "espace", 9500, "Vos conversations, chez vous.",
     "Textes, documents, photos et messages vocaux. Un appel ou une visio part d’un seul geste, et tout passe par votre Hub."),
    ("appels", "espace", 8500, "JARVIS répond quand vous ne pouvez pas.",
     "Appels et visioconférences, en personnel comme en professionnel. Un numéro inconnu est filtré d’abord par JARVIS, et vous gardez le dernier mot."),
    ("carte", "carte", 9500, "Tous vos lieux, d’un coup d’œil.",
     "BouLance au Lac-Saint-Jean, la résidence, le chalet, le bureau, le garage de collection et la ferme : chaque environnement en direct, à sa vraie place."),
    ("outils", "outils", 7000, "Toutes vos extensions, au même endroit.",
     "Domotique, IA, caméras, entreprise, réseau, diagnostic, mobilité : chacune s’ouvre d’un seul clic, directement dans JARVIS."),
]


class _ExtIcons(dict):
    """Icône d'une extension; une extension ajoutée plus tard reçoit une icône par défaut."""

    def __missing__(self, key):
        return "grid"


# Mes outils : les extensions sont les solutions du site (config.py); chacune ouvre sa page, dans JARVIS.
EXT_ICON = _ExtIcons({"environnements-intelligents": "home", "ia-privee-connaissances": "spark", "securite-intelligente": "shield",
                      "automatisation-operations": "flow", "reseau-resilience": "net", "diagnostic-care": "pulse",
                      "mobilite": "route", "mobilite-voyage": "route"})
EXT_OFF = {"diagnostic-care"}  # offertes sur demande; toute autre extension est activée
EXT_ON = {c["slug"] for c in CAPABILITIES if c["slug"] not in EXT_OFF}


def ext_href(slug):
    return f"/solutions/{slug}/#jarvis"


# Bannière et visages repris du dossier User v25 (texte incrusté retiré); photos d'ambiance du site.
BANNER = "/media/app/banniere-lac.webp"
AV_ALEX = "/media/app/alex.webp"
AV_CAMILLE = "/media/app/camille.webp"
AV_EQUIPE = "/media/app/equipe.webp"
PH_SOUPER = "/media/solutions/camera-rear-terrace-v1.webp"
PH_DOCS = "/media/solutions/ia-privee-connaissances.webp"
PH_RECO = BANNER
ENV_HREF = "/solutions/environnements-intelligents/#jarvis"


# ---------------------------------------------------------------------------------------------
# Carte : sud du Québec en kilomètres (origine Saint-Hyacinthe), même projection que app_geo.py
# ---------------------------------------------------------------------------------------------
LAT0, LON0 = 45.630, -72.957
KX = 111.32 * math.cos(math.radians(47.0))
KY = 111.13


def P(lat, lon):
    return (lon - LON0) * KX, (LAT0 - lat) * KY


# Les environnements de James (positions d'affichage; données d'exemple sauf les batteries de BouLance).
# Groupe « sth » : les quatre lieux de Saint-Hyacinthe, réunis en une bulle quand la carte est éloignée.
ENVS = [
    {"key": "boulance", "name": "BouLance", "kind": "Véhicule récréatif", "place": "Roberval · Lac-Saint-Jean",
     "lat": 48.515, "lon": -72.226, "icon": "rv", "img": "/media/env/boulance.webp", "pos": "62% 50%", "w": 74,
     "short": "Stationné · au bord du lac", "state": "ok",
     "chips": [("battery", "Batteries", "—", "soc"), ("shield", "Alarme", "Armée", ""), ("thermo", "Intérieur", "19 °C", "")],
     "rows": [("route", f"Arrivé hier, 17 h 40 · {ROUTE_KM} km depuis la Maison"), ("pin", "Camping municipal de Roberval · Tour du Lac-Saint-Jean"),
              ("info", "Batteries mesurées en direct · le reste, données d’exemple")]},
    {"key": "maison", "name": "Résidence", "kind": "Résidence de prestige", "place": "Saint-Hyacinthe",
     "lat": 45.655, "lon": -73.020, "icon": "home", "img": "/media/solutions/environnements-intelligents.webp", "pos": "70% 42%",
     "w": 22, "grp": "sth", "short": "21 °C · chauffage réduit", "state": "ok",
     "chips": [("shield", "Système", "Armé", ""), ("thermo", "Salon", "21 °C", ""), ("users", "Présence", "Personne", "")],
     "rows": [("clock", "Retour prévu pour 17 h · préchauffage à 16 h 15"), ("check", "Portes verrouillées · stores fermés"),
              ("info", "Données d’exemple")]},
    {"key": "chalet", "name": "Chalet", "kind": "Chalet d’architecte", "place": "Saint-Donat · Lac Archambault",
     "lat": 46.318, "lon": -74.222, "icon": "tree", "img": "/media/concept/jarvis-hero-architecture-v1.webp", "pos": "30% 50%",
     "w": 60, "short": "Hors saison · 12 °C maintenu", "state": "ok",
     "chips": [("drop", "Eau", "Coupée", ""), ("camera", "Caméras", "Actives", ""), ("thermo", "Intérieur", "12 °C", "")],
     "rows": [("check", "Dernière visite il y a 9 jours · tout est fermé"), ("shield", "Aucun mouvement détecté cette semaine"),
              ("info", "Données d’exemple")]},
    {"key": "bureau", "name": "Bureau", "kind": "Entreprise · bureaux", "place": "Saint-Hyacinthe · centre-ville",
     "lat": 45.627, "lon": -72.953, "icon": "brief", "img": "/media/solutions/jarvis-enterprise-operations-v1.webp", "pos": "50% 50%",
     "w": 22, "grp": "sth", "short": "Fermé · système armé", "state": "ok",
     "chips": [("lock", "Accès", "Verrouillés", ""), ("devices", "Postes", "3 en veille", ""), ("thermo", "Bureaux", "17 °C", "")],
     "rows": [("calendar", "Ouverture lundi, 8 h · chauffage à 7 h 15"), ("check", "Sauvegarde de la nuit réussie"),
              ("info", "Données d’exemple")]},
    {"key": "atelier", "name": "Garage", "kind": "Garage de collection", "place": "Sainte-Rosalie",
     "lat": 45.643, "lon": -72.893, "icon": "garage", "img": "/media/solutions/camera-garage-supercars-v1.webp", "pos": "55% 40%",
     "w": 22, "grp": "sth", "short": "Portes fermées · 6 voitures sur 7", "state": "ok",
     "chips": [("garage", "Portes", "Fermées", ""), ("drop", "Humidité", "45 %", ""), ("thermo", "Garage", "15 °C", "")],
     "rows": [("check", "Mainteneurs de charge : 6 sur 6"), ("route", "Escalade noir de retour vers 18 h"), ("info", "Données d’exemple")]},
    {"key": "ferme", "name": "Ferme", "kind": "Ferme multi-élevage", "place": "Montérégie",
     "lat": 45.565, "lon": -72.950, "icon": "barn", "img": media("/media/env/ferme.webp"), "pos": "50% 50%",
     "w": 22, "grp": "sth", "short": "Traite de 17 h terminée", "state": "ok",
     "chips": [("thermo", "Étable", "8 °C", ""), ("drop", "Abreuvoirs", "Normaux", ""), ("shield", "Bâtiments", "Fermés", "")],
     "rows": [("clock", "Prochaine traite à 5 h · robot prêt"), ("check", "Ventilation automatique · 62 % d’humidité"),
              ("info", "Données d’exemple")]},
    {"key": "hangar", "name": "Hangar", "kind": "Hangar privé · turbopropulseur et jet", "place": "Saint-Jean-sur-Richelieu · aéroport",
     "lat": 45.295, "lon": -73.281, "icon": "plane", "img": media("/media/vision/lieu-jet.webp"), "pos": "62% 46%", "w": 40,
     "short": "2 appareils · jet en préparation", "state": "ok",
     "chips": [("plane", "Appareils", "2 au hangar", ""), ("shield", "Hangar", "Armé", ""), ("thermo", "Cabine du jet", "9 °C", "")],
     "rows": [("calendar", "Jet vers Miami demain, 9 h · préchauffage de la cabine à 7 h"), ("check", "Turbopropulseur prêt · vol vers Sherbrooke demain, 10 h"),
              ("info", "Données d’exemple")]},
]
GROUP_STH = "sth"
CLUSTER_W = 120  # au-delà de cette largeur visible (km), les lieux de Saint-Hyacinthe se regroupent


def _env_photo(e, cls, w=320):
    if e["img"]:
        return (f'<img class="{cls}" src="{e["img"]}" alt="" loading="lazy" decoding="async" '
                f'style="object-position:{e["pos"]}">')
    return f'<span class="{cls} ap-ph" aria-hidden="true"><small>Photo à venir</small></span>'


def _cam_all(pad=1.3):
    xs = [P(e["lat"], e["lon"])[0] for e in ENVS]
    ys = [P(e["lat"], e["lon"])[1] for e in ENVS]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return cx, cy, (max(xs) - min(xs)) * pad, (max(ys) - min(ys)) * pad


# Repères (nom, lat, lon, largeur visible maximale en km pour l'afficher; 0 = toujours)
CITIES = [
    ("Montréal", 45.508, -73.561, 0, 2), ("Québec", 46.813, -71.208, 0, 2), ("Trois-Rivières", 46.345, -72.543, 0, 1),
    ("Saguenay", 48.428, -71.068, 0, 1), ("Sherbrooke", 45.404, -71.893, 0, 1), ("Ottawa", 45.421, -75.697, 0, 1),
    ("Drummondville", 45.883, -72.484, 400, 1), ("Granby", 45.400, -72.733, 330, 1), ("Alma", 48.550, -71.650, 520, 1),
    ("Dolbeau-Mistassini", 48.879, -72.231, 560, 1), ("La Tuque", 47.436, -72.783, 640, 1), ("Shawinigan", 46.567, -72.746, 330, 1),
    ("Joliette", 46.022, -73.440, 300, 1), ("Saint-Jérôme", 45.780, -74.004, 330, 1), ("Mont-Tremblant", 46.119, -74.596, 560, 1),
    ("Saint-Jean-sur-Richelieu", 45.307, -73.262, 330, 1), ("Sorel-Tracy", 46.040, -73.113, 250, 1), ("Victoriaville", 46.057, -71.960, 330, 1),
    ("Saint-Hyacinthe", 45.612, -72.957, CLUSTER_W, 1), ("Beloeil", 45.567, -73.205, 150, 0), ("Saint-Pie", 45.507, -72.909, 80, 0),
    ("Saint-Dominique", 45.571, -72.853, 80, 0), ("Saint-Damase", 45.531, -73.003, 80, 0), ("Saint-Liboire", 45.651, -72.763, 80, 0),
    ("Saint-Simon", 45.723, -72.839, 80, 0), ("Roberval", 48.519, -72.222, 0, -1), ("Chambord", 48.430, -72.063, 160, 0),
    ("Saint-Félicien", 48.650, -72.450, 220, 0), ("Saint-Donat", 46.319, -74.222, 0, -1),
]
# Eaux et régions (nom, lat, lon, rotation, largeur visible minimale, maximale)
WATERS = [
    ("Fleuve Saint-Laurent", 46.62, -71.80, -33, 0, 9999), ("Fleuve Saint-Laurent", 45.86, -73.24, -50, 0, 260),
    ("Lac Saint-Jean", 48.665, -71.93, 0, 0, 9999), ("Lac Saint-Pierre", 46.21, -72.84, -30, 0, 360),
    ("Rivière Saguenay", 48.33, -70.55, -18, 0, 9999), ("Réservoir Gouin", 48.42, -74.25, 0, 0, 9999),
    ("Lac Champlain", 44.80, -73.33, -78, 0, 9999), ("Rivière Yamaska", 45.70, -72.975, -78, 0, 90),
    ("Rivière Richelieu", 45.68, -73.19, -80, 0, 110),
]
REGIONS = [
    ("ONTARIO", 45.55, -76.45, 300), ("ÉTATS-UNIS", 44.80, -71.90, 300), ("MAURICIE", 47.25, -73.35, 300),
    ("LAURENTIDES", 46.55, -75.05, 300), ("SAGUENAY–LAC-SAINT-JEAN", 49.12, -71.55, 300), ("CAPITALE-NATIONALE", 47.30, -71.05, 300),
    ("MONTÉRÉGIE", 45.30, -73.05, 200), ("ESTRIE", 45.35, -71.55, 300), ("CENTRE-DU-QUÉBEC", 46.10, -72.15, 300),
]


def geo_defs(uid):
    """La géographie, une seule fois par appareil : la grande carte et la carte de l'accueil la réutilisent (<use>).
    Les styles sont écrits sur les tracés : les copies d'un <use> ne reçoivent pas les règles de la page.
    Fond noir, terres gris très foncé, eaux noires à rive fine, routes en gris; seul le trajet est doré."""
    x, y, w, h = BOX
    g = GEO
    ns = "vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round"
    roads = "opacity:var(--roads,1);fill:none;" + ns
    return f"""<svg class="ap-geo-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
<g id="{uid}">
  <rect x="{x - 400}" y="{y - 400}" width="{w + 800}" height="{h + 800}" style="fill:#020203"/>
  <path d="{g["land"]}" style="fill:#141416;stroke:#323236;stroke-width:.8px;{ns}"/>
  <path d="{g["urban"]}" style="fill:#1e1e21"/>
  <path d="{g["lakes"]}" style="fill:#020203;stroke:#2c2c30;stroke-width:.7px;{ns}"/>
  <path d="{g["r3"]}" style="fill:none;stroke:#060607;stroke-width:calc(.7px + var(--zk,0) * 1px);{ns}"/>
  <path d="{g["r2"]}" style="fill:none;stroke:#050506;stroke-width:calc(1px + var(--zk,0) * 1.4px);{ns}"/>
  <path d="{g["r1"]}" style="fill:none;stroke:#040405;stroke-width:calc(1.5px + var(--zk,0) * 2px);{ns}"/>
  <path d="{g["border"]}" style="fill:none;stroke:#55555b;stroke-width:1px;stroke-dasharray:5 4;{ns}"/>
  <path d="{g["sec"]}" style="stroke:#323236;stroke-width:calc(.7px + var(--zk,0) * 1.1px);{roads}"/>
  <path d="{g["hw"]}" style="stroke:#0b0b0c;stroke-width:calc(2.8px + var(--zk,0) * 2.6px);{roads}"/>
  <path d="{g["hw"]}" style="stroke:#58585e;stroke-width:calc(1.2px + var(--zk,0) * 1.8px);{roads}"/>
</g>
<g id="{uid}-route">
  <path d="{g["route"]}" style="fill:none;stroke:var(--gold-soft);stroke-opacity:.3;stroke-width:7px;filter:blur(2.5px);{ns}"/>
  <path d="{g["route"]}" style="fill:none;stroke:var(--gold-soft);stroke-width:2.4px;stroke-dasharray:.5 6;{ns}"/>
</g>
</defs></svg>"""


def _xy(lat, lon):
    x, y = P(lat, lon)
    return f'data-x="{x:.1f}" data-y="{y:.1f}"'


def map_svg(uid, cam, route=True):
    cx, cy, w, h = cam
    vb = f"{cx - w / 2:.1f} {cy - h / 2:.1f} {w:.1f} {h:.1f}"
    r = f'<use class="ap-route" data-layer="trajet" href="#{uid}-route"/>' if route else ""
    return (f'<svg class="ap-map-svg" viewBox="{vb}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<use href="#{uid}"/>{r}</svg>')


def _env_pin(e, small=False):
    grp = f' data-grp="{e["grp"]}" data-maxw="{CLUSTER_W}"' if e.get("grp") else ""
    if small:
        return (f'<span class="ap-dotpin" {_xy(e["lat"], e["lon"])}{grp} aria-hidden="true">'
                f'<i></i><b>{e["name"]}</b></span>')
    return (f'<button type="button" class="ap-env" data-env="{e["key"]}" data-w="{e["w"]}" {_xy(e["lat"], e["lon"])}{grp} '
            f'aria-label="{e["name"]} · {e["place"]}">'
            f'<span class="ap-env-ph">{_env_photo(e, "ap-env-img")}<i class="ap-env-ic">{icon(e["icon"])}</i></span>'
            f'<span class="ap-env-lab"><b>{e["name"]}</b><small><i class="ap-env-dot" aria-hidden="true"></i>'
            f'<span data-env-short="{e["key"]}">{e["short"]}</span></small></span></button>')


def _cluster(small=False):
    g = [e for e in ENVS if e.get("grp") == GROUP_STH]
    xs = [P(e["lat"], e["lon"]) for e in g]
    cx, cy = sum(p[0] for p in xs) / len(xs), sum(p[1] for p in xs) / len(xs)
    if small:
        return (f'<span class="ap-dotpin is-grp" data-x="{cx:.1f}" data-y="{cy:.1f}" data-minw="{CLUSTER_W}" aria-hidden="true">'
                f'<i></i><b>{len(g)} lieux · Saint-Hyacinthe</b></span>')
    thumbs = "".join(_env_photo(e, "ap-cl-img") for e in g[:3])
    return (f'<button type="button" class="ap-cluster" data-cluster="{GROUP_STH}" data-x="{cx:.1f}" data-y="{cy:.1f}" '
            f'data-minw="{CLUSTER_W}" data-w="26" aria-label="{len(g)} lieux à Saint-Hyacinthe : rapprocher">'
            f'<span class="ap-cl-ph">{thumbs}</span><span class="ap-cl-t"><b>{len(g)} lieux</b><small>Saint-Hyacinthe</small></span></button>')


SHIELD_W = {"10": 240, "15": 300, "30": 240, "55": 300, "40": 420, "20": 700}


def map_overlays(big=True):
    out = []
    if big:
        for name, la, lo, rot, mn, mx in WATERS:
            out.append(f'<span class="ap-water" {_xy(la, lo)} data-minw="{mn}" data-maxw="{mx}" data-layer="villes" '
                       f'style="--rot:{rot}deg" aria-hidden="true">{name}</span>')
        for name, la, lo, mx in REGIONS:
            out.append(f'<span class="ap-region" {_xy(la, lo)} data-minw="{mx}" data-layer="villes" aria-hidden="true">{name}</span>')
        for num, x, y in SHIELDS:
            out.append(f'<span class="ap-shield{" is-a" if len(num) <= 2 else ""}" data-x="{x}" data-y="{y}" data-maxw="{SHIELD_W.get(num, 700)}" '
                       f'data-layer="routes" aria-hidden="true">{num}</span>')
    for name, la, lo, mx, imp in CITIES:
        if imp < 0 or (not big and imp < 2):
            continue
        mx_attr = f' data-maxw="{mx}"' if mx else ""
        out.append(f'<span class="ap-city c{imp}" {_xy(la, lo)}{mx_attr} data-layer="villes"><i></i><b>{name}</b></span>')
    if big:
        out.append(_cluster())
        out += [_env_pin(e) for e in ENVS]
    else:
        out.append(_cluster(small=True))
        out += [_env_pin(e, small=True) for e in ENVS]
    return "".join(out)


# ---------------------------------------------------------------------------------------------
# Écrans
# ---------------------------------------------------------------------------------------------
_GEO = {"uid": "apgeo"}  # identifiant de la géographie de l'appareil en cours de rendu


def _head(crumb, title, sub, extra=""):
    c = f'<p class="ap-crumb">{crumb}</p>' if crumb else ""
    return f"""<div class="ap-head" data-r>
  <div>{c}<h3 class="ap-h1">{title}</h3><p class="ap-sub">{sub}</p></div>{extra}
</div>"""


def _card_h(ic, title, more=""):
    return f'<header class="ap-card-h">{icon(ic)}<h4>{title}</h4>{more}</header>'


def _pp():
    """Sélecteur Personnel | Professionnel (un même état pour tout l'appareil, tenu par app.js)."""
    return f"""<div class="ap-seg ap-pp" role="group" aria-label="Espace affiché">
  <button type="button" class="is-on" data-pp="perso" aria-pressed="true">{icon("user")}Personnel</button>
  <button type="button" data-pp="pro" aria-pressed="false">{icon("brief")}Professionnel</button>
</div>"""


def _px(perso, pro):
    """Deux textes, un seul affiché selon l'espace choisi (Personnel ou Professionnel)."""
    return f'<span data-pp-only="perso">{perso}</span><span data-pp-only="pro">{pro}</span>'


# Accueil : l'état du moment de chaque extension (perso, pro ou None). Une extension sans entrée
# affiche sa description courte : la bande accepte autant d'extensions que config.CAPABILITIES.
HOME_STATE = {
    "environnements-intelligents": ("6 lieux en ligne · BouLance au Lac-Saint-Jean", None),
    "securite-intelligente": ("Nuit calme · système armé · 2 véhicules reconnus", None),
    "automatisation-operations": ("1 appel répondu par JARVIS ce matin", "2 appels d’affaires répondus ce matin"),
    "ia-privee-connaissances": ("3 documents classés · résumé prêt", None),
    "reseau-resilience": ("Tout fonctionne · sauvegarde de 3 h réussie", None),
    "diagnostic-care": ("Disponible sur demande", None),
    "mobilite": ("Disponible sur demande · copilote de route", None),
}


def v_accueil():
    notifs = f"""<div class="ap-card ap-notifs" data-r>
  <div class="ap-nt"><span class="ap-ring">{icon("bell")}</span><span><b>Notifications</b>
    <small><i class="ap-dot is-red" aria-hidden="true"></i><span data-ap-n="2">2</span> non lues</small></span></div>
  <button type="button" class="ap-nt" data-go="messages" data-conv="camille">{face(AV_CAMILLE)}<span><b>Camille</b><small>Nouveau message</small></span><i class="ap-dot is-red" aria-hidden="true"></i></button>
  <button type="button" class="ap-nt" data-go="journee"><span class="ap-ring">{icon("calendar")}</span><span><b>Ma journée</b><small>Demain à 8 h 30</small></span><i class="ap-dot is-red" aria-hidden="true"></i></button>
  <div class="ap-nt ap-nt-all"><button type="button" class="ap-link" data-go="espace">Tout voir{icon("right")}</button></div>
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

    def state(c):
        perso, pro = HOME_STATE.get(c["slug"], (c["short"], None))
        return _px(perso, pro) if pro else perso

    xcards = "".join(
        f"""<a class="ap-xc{"" if c["slug"] in EXT_ON else " is-off"}" href="{ext_href(c["slug"])}" aria-label="Ouvrir l’extension {c["label"]}">
      <img src="{c['image']}" alt="" loading="lazy" decoding="async">
      <span class="ap-xc-i">{icon(EXT_ICON[c["slug"]])}</span>
      <span class="ap-xc-t"><b>{c['label']}</b><small>{state(c)}</small></span>
      <span class="ap-xc-go" aria-hidden="true">Ouvrir{icon("right")}</span>
      <span class="ap-xc-dot" aria-hidden="true"></span>
    </a>"""
        for c in CAPABILITIES
    )
    exts = f"""<section class="ap-xh" data-r aria-label="Vos extensions">
    <header class="ap-xh-h"><span class="ap-ring">{icon("grid")}</span><b>Vos extensions</b>
      <small><i class="ap-dot is-ok" aria-hidden="true"></i>Tout fonctionne</small>
      <button type="button" class="ap-link" data-go="outils">Tout voir{icon("right")}</button></header>
    <div class="ap-xh-g" style="--n:{len(CAPABILITIES)}">{xcards}</div>
  </section>"""
    msgs = "".join(
        f'<li><button type="button" data-go="messages" data-conv="{k}">{av}<span><b>{n}</b><small>{t}</small></span><time>{w}</time></button></li>'
        for k, av, n, t, w in [
            ("camille", face(AV_CAMILLE), "Camille", "Parfait, j’apporte le vin. À tout à l’heure !", "12 min"),
            ("equipe", face(AV_EQUIPE), "Équipe Atelier", "La soumission révisée est prête. On en discute demain matin.", "2 h"),
        ]
    )
    cam = _cam_all(1.3)
    return f"""{_head("", '<span data-ap="greet">Bonsoir</span> <em>Alex</em>', "Votre journée, simplement.",
                      '<div class="ap-today"><span data-ap="date">Aujourd’hui</span><b><span data-ap="clock">19 h 42</span></b></div>')}
{notifs}
{exts}
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
      {_card_h("star", "Recommandations JARVIS")}
      <img src="{PH_RECO}" alt="" loading="lazy" decoding="async">
      <div class="ap-reco-b"><span><b>Préparer votre journée</b>
        <small>Vos rendez-vous, la météo et l’essentiel pour bien commencer.</small></span>
        <button type="button" class="ap-btn ap-reco-go" data-go="journee">Voir{icon("right")}</button></div>
    </article>
  </div>
</div>
<div class="ap-home-b">
  <article class="ap-card ap-minimap" data-r>
    {_card_h("map", "Mes lieux", '<button type="button" class="ap-link" data-go="carte">Ouvrir' + icon("right") + '</button>')}
    <button type="button" class="ap-map ap-map-mini" data-map data-go="carte" data-cam="{cam[0]:.1f},{cam[1]:.1f},{cam[2]:.1f},{cam[3]:.1f}" data-box="{",".join(str(v) for v in BOX)}" aria-label="Ouvrir la carte de vos lieux">
      {map_svg(_GEO["uid"], cam)}
      <span class="ap-ov">{map_overlays(big=False)}</span>
    </button>
  </article>
  <article class="ap-card ap-favs" data-r>
    {_card_h("star", "Mes favoris")}
    <ul class="ap-rows">
      <li><button type="button" data-go="journee">{icon("calendar")}<span><b>Mon agenda</b><small>Vos prochains événements</small></span>{icon("right", "ap-chev")}</button></li>
      <li><button type="button" data-go="partage">{icon("share")}<span><b>Mes partages</b><small>Qui voit quoi, et jusqu’à quand</small></span>{icon("right", "ap-chev")}</button></li>
      <li><button type="button" data-go="carte" data-env-go="boulance">{icon("rv")}<span><b>BouLance</b><small>Au Lac-Saint-Jean · batteries en direct</small></span>{icon("right", "ap-chev")}</button></li>
    </ul>
  </article>
  <article class="ap-card ap-msgs" data-r>
    {_card_h("chat", "Mes messages", '<button type="button" class="ap-link" data-go="messages">Ouvrir' + icon("right") + '</button>')}
    <ul class="ap-rows">{msgs}</ul>
  </article>
</div>"""



def v_assistant():
    def src(ic, a, b):
        return f'<span class="ap-src">{icon(ic)}{a}<em>{b}</em></span>'

    me = face(AV_ALEX)
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




def v_espace():
    # (icône, titre, texte, action, photo, cadrage) : chaque tuile repose sur une photo du site, comme la bande des extensions
    tiles = [
        ("calendar", "Ma journée", "Vos rendez-vous et priorités du jour.", 'data-go="journee"',
         "/media/concept/jarvis-life-context-v3.webp", "58% 40%"),
        ("chat", "Mes messages", "Conversations, documents et vocaux.", 'data-go="messages"', PH_SOUPER, "62% 60%"),
        ("doc", "Mes documents", "Vos fichiers au même endroit.",
         'data-toast="Mes documents : vos fichiers, depuis les sources que vous avez autorisées."', PH_DOCS, "40% 45%"),
        ("devices", "Mes appareils", "Vos appareils personnels.",
         'data-toast="Mes appareils : chaque appareil connecté à votre compte, et ses sessions."',
         "/media/product/jarvis-hub-v1.webp", "60% 55%"),
        ("link", "Mes connexions", "Vos services autorisés.",
         'data-toast="Mes connexions : agenda, documents, messagerie. Vous choisissez ce que JARVIS peut lire."',
         "/media/solutions/reseau-resilience.webp", "50% 40%"),
        ("share", "Mes partages", "Je choisis ce que je partage.", 'data-go="partage"',
         "/media/solutions/camera-front-entry-v1.webp", "50% 55%"),
        ("gear", "Mes préférences", "Mon accueil, mes réglages.",
         'data-toast="Mes préférences : langue, notifications et cartes de votre accueil."',
         "/media/ambiances/heure-doree.webp", "50% 60%"),
    ]
    grid = "".join(
        f'<button type="button" class="ap-card ap-tile" {act} data-r>'
        f'<img class="ap-tile-ph" src="{ph}" alt="" loading="lazy" decoding="async" style="object-position:{pos}">'
        f'<span class="ap-tile-i">{icon(ic)}</span>'
        f'<span class="ap-tile-t"><b>{t}</b><small>{d}</small></span><i class="ap-tile-go">{icon("right")}</i></button>'
        for ic, t, d, act, ph, pos in tiles
    )
    notes = [
        ("is-unread", face(AV_CAMILLE), "Camille", "Nouveau message", "JARVIS", "il y a 10 min", 'data-go="messages" data-conv="camille"'),
        ("is-unread", f'<span class="ap-ring">{icon("calendar")}</span>', "Ma journée", "Préparer les documents demain à 8 h 30",
         "Agenda personnel", "il y a 1 h", 'data-go="journee"'),
        ("", f'<span class="ap-ring is-blue">{icon("doc")}</span>', "Mes documents", "Camille a partagé Liste de matériel.pdf",
         "Document partagé", "hier", 'data-go="messages" data-conv="camille"'),
    ]
    nl = "".join(
        f'<li class="{c}"><button type="button" {go}>{av}<span><b>{t}</b><small>{d}</small><em>{tag}</em></span><time>{when}</time></button></li>'
        for c, av, t, d, tag, when, go in notes
    )
    appels_tile = f"""<button type="button" class="ap-card ap-tile ap-tile-call" data-go="appels" data-r>
      <img class="ap-tile-ph" src="/media/concept/jarvis-future-ecosystem-v1.webp" alt="" loading="lazy" decoding="async" style="object-position:60% 45%">
      <span class="ap-tile-i">{icon("call")}</span>
      <span class="ap-tile-t"><b>Mes appels</b><small>{_px("Appels et visioconférences · 1 appel répondu par JARVIS ce matin",
                                                           "Appels d’affaires et visioconférences · 2 réponses de JARVIS ce matin")}</small></span>
      <i class="ap-tile-go">{icon("right")}</i>
    </button>"""
    return f"""{_head("", "Mon <em>espace</em>", "Votre quotidien, à votre image.", _pp())}
<div class="ap-es">
  <div class="ap-es-main">
    <div class="ap-tiles">{grid}{appels_tile}</div>
    <button type="button" class="ap-card ap-explore" data-go="carte" data-r>
      <img src="{BANNER}" alt="" loading="lazy" decoding="async">
      <span class="ap-tile-i">{icon("map")}</span>
      <span class="ap-tile-t"><b>Explorer la carte</b><small>BouLance, la résidence, le chalet, le bureau, le garage de collection et la ferme, en direct.</small></span>
      <span class="ap-btn">Ouvrir la carte{icon("right")}</span>
    </button>
  </div>
  <aside class="ap-card ap-notes" data-r>
    <header class="ap-card-h">{icon("bell")}<h4>Notifications</h4><span class="ap-count"><b data-ap="unread">2</b> non lues</span></header>
    <div class="ap-seg" role="group" aria-label="Filtrer"><button type="button" class="is-on" data-nf="all" aria-pressed="true">Toutes</button><button type="button" data-nf="unread" aria-pressed="false">Non lues</button></div>
    <ul class="ap-nl">{nl}</ul>
    <button type="button" class="ap-btn ap-markread" data-ap="markread">{icon("check")}<span>Tout marquer comme lu</span></button>
  </aside>
</div>"""


# ---------------------------------------------------------------------------------------------
# Mes messages : conversations, documents, vocaux, photos, appels et visio (tout simulé)
# ---------------------------------------------------------------------------------------------
# Les personnes (appels, visio, messages). « hd » : une photo de visio plus grande, prise si elle existe.
PEOPLE = {
    "camille": {"n": "Camille", "img": AV_CAMILLE, "role": "Amie", "hd": media("/media/app/visio-camille.webp")},
    "equipe": {"n": "Équipe Atelier", "img": AV_EQUIPE, "role": "4 membres", "hd": media("/media/app/visio-equipe.webp"),
               "group": ["equipe", "camille"]},
    "marc": {"n": "Marc", "ini": "MA", "tone": "teal", "role": "Frère"},
    "maman": {"n": "Maman", "ini": "M", "tone": "violet", "role": "Famille"},
    "tremblay": {"n": "Mme Tremblay", "ini": "MT", "tone": "violet", "role": "Cliente"},
    "belanger": {"n": "Fournisseur Bélanger", "ini": "FB", "tone": "stone", "role": "Fournisseur"},
    "fortin": {"n": "Atelier Fortin", "ini": "AF", "tone": "gold", "role": "Client"},
    "inconnu": {"n": "Numéro inconnu", "ini": "?", "tone": "stone", "role": "Filtré par JARVIS"},
    "alex": {"n": "Alex", "img": AV_ALEX, "hd": media("/media/app/visio-alex.webp")},
}


def _av(k):
    p = PEOPLE[k]
    return face(p["img"]) if p.get("img") else mono(p["ini"], p["tone"])


def _pdf_page(title, sub, rows, total=None):
    """Aperçu de la première page d'un PDF : du vrai texte, mis en page comme un document."""
    body = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    tot = f'<tr class="is-tot"><td>{total[0]}</td><td>{total[1]}</td></tr>' if total else ""
    return (f'<span class="ap-pdf-page" aria-hidden="true"><span class="ap-pdf-brand">JARVIS · Ma vie</span>'
            f'<b>{title}</b><small>{sub}</small><table>{body}{tot}</table>'
            f'<span class="ap-pdf-foot">Données d’exemple · page 1</span></span>')


DOCS = {
    "liste": ("Liste de matériel.pdf", "2 pages · 184 Ko",
              _pdf_page("Liste de matériel", "Souper du samedi · 8 personnes",
                        [("Brochettes marinées", "16"), ("Salade grecque", "1 grand bol"), ("Pain de campagne", "2"),
                         ("Vin rouge", "3 bouteilles"), ("Lanternes de terrasse", "6"), ("Chaises pliantes", "4")])),
    "soumission": ("Soumission 2026-118.pdf", "3 pages · 412 Ko",
                   _pdf_page("Soumission no 2026-118", "Atelier · cliente : Mme Tremblay",
                             [("Diagnostic complet", "180,00 $"), ("Pièces et fournitures", "642,50 $"),
                              ("Main-d’œuvre · 6 h", "540,00 $"), ("TPS et TVQ", "204,04 $")], ("Total", "1 566,54 $"))),
    "plan": ("Plan de la terrasse.pdf", "1 page · 96 Ko",
             _pdf_page("Plan de la terrasse", "Éclairage et prises extérieures",
                       [("Lanternes murales", "4 × 12 W"), ("Guirlande", "18 m"), ("Prises étanches", "3"),
                        ("Minuterie", "Coucher du soleil")])),
}
# Barres du message vocal (hauteurs fixes : rien d'aléatoire au build)
_WAVE = [30, 52, 70, 44, 86, 62, 38, 74, 92, 58, 40, 66, 84, 50, 34, 60, 78, 46, 28, 54, 72, 88, 64, 42, 30, 48, 68, 56, 36, 24]


def _wave(sec):
    bars = "".join(f'<i style="--h:{h}%"></i>' for h in _WAVE)
    return (f'<span class="ap-voice" data-voice="{sec}"><button type="button" class="ap-voice-b" aria-label="Écouter le message vocal">'
            f'{icon("play", "i-play")}{icon("pause", "i-pause")}</button>'
            f'<span class="ap-wave"><span class="ap-wave-a">{bars}</span><span class="ap-wave-b" aria-hidden="true">{bars}</span></span>'
            f'<time>0:{sec:02d}</time></span>')


def _doc_card(k):
    name, meta, page = DOCS[k]
    return (f'<button type="button" class="ap-doc" data-doc="{k}" aria-label="Ouvrir {name}">'
            f'<span class="ap-doc-pv">{page}</span>'
            f'<span class="ap-doc-f"><span class="ap-doc-ic">PDF</span><span><b>{name}</b><small>{meta}</small></span>{icon("right", "ap-chev")}</span>'
            f'</button>')


def _receipt(state):
    lab = {"read": "Lu", "dlv": "Distribué", "sent": "Envoyé"}[state]
    return f'<span class="ap-rcpt is-{state}">{icon("checks" if state != "sent" else "check")}<span>{lab}</span></span>'


def _msg(m):
    kind, side = m[0], m[1]
    t = m[-1]
    if kind == "day":
        return f'<p class="ap-day-sep"><span>{side}</span></p>'
    if kind == "typing":
        return (f'<div class="ap-bub-row in is-typing-row" data-typing hidden>{_av(side)}'
                f'<div class="ap-bubx is-typing"><i class="ap-dots" aria-hidden="true"><i></i><i></i><i></i></i>'
                f'<span class="ap-sr">écrit…</span></div></div>')
    meta = f'<span class="ap-bub-meta"><time>{t}</time>{_receipt(m[-2]) if side == "out" else ""}</span>'
    if kind == "txt":
        inner = f'<div class="ap-bubx">{m[2]}</div>'
    elif kind == "doc":
        inner = f'<div class="ap-bubx is-doc">{_doc_card(m[2])}{f"<p>{m[3]}</p>" if m[3] else ""}</div>'
    elif kind == "voice":
        inner = f'<div class="ap-bubx is-voice">{_wave(m[2])}</div>'
    elif kind == "photo":
        inner = (f'<div class="ap-bubx is-photo"><img src="{m[2]}" alt="" loading="lazy" decoding="async" style="object-position:{m[3]}">'
                 f'{f"<p>{m[4]}</p>" if m[4] else ""}</div>')
    else:
        inner = ""
    av = _av(m[-2]) if side == "in" else ""
    return f'<div class="ap-bub-row {side}{" has-av" if av else ""}">{av}<div class="ap-bub-c">{inner}{meta}</div></div>'


# Conversations : clé, espace, aperçu, heure, non lus, fil (messages), réponse automatique simulée
# Message : (sorte, côté, contenu…, [accusé], heure). Côté « in » : l'avant-dernier champ est l'auteur.
CONVS = [
    ("camille", "perso", "Parfait, j’apporte le vin.", "18 h 21", 1, [
        ("day", "Aujourd’hui"),
        ("txt", "in", "Tu es disponible pour le souper ce soir ?", "camille", "17 h 48"),
        ("txt", "out", "Oui ! Je finis vers 18 h 30.", "read", "17 h 50"),
        ("doc", "in", "liste", "J’ai fait la liste pour samedi, tu peux regarder ?", "camille", "17 h 56"),
        ("voice", "out", 14, "read", "18 h 02"),
        ("photo", "in", PH_SOUPER, "62% 60%", "La terrasse est prête pour ce soir.", "camille", "18 h 15"),
        ("txt", "out", "Parfait, j’apporte le vin.", "read", "18 h 21"),
        ("typing", "camille", ""),
    ], "Super, à tout à l’heure !"),
    ("marc", "perso", "Oui, vers 10 h.", "16 h 10", 0, [
        ("day", "Aujourd’hui"),
        ("txt", "in", "Tu passes chercher la remorque samedi ?", "marc", "15 h 52"),
        ("txt", "out", "Oui, vers 10 h.", "read", "16 h 10"),
        ("typing", "marc", ""),
    ], "Parfait, je la laisse devant le garage."),
    ("maman", "perso", "Embrasse Camille pour moi !", "Hier", 0, [
        ("day", "Hier"),
        ("txt", "in", "Bon souper demain soir. Embrasse Camille pour moi !", "maman", "20 h 04"),
        ("txt", "out", "Promis. Bonne soirée, maman.", "read", "20 h 11"),
        ("typing", "maman", ""),
    ], "Merci, bonne soirée à vous deux !"),
    ("equipe", "pro", "Revue de chantier demain, 9 h 30.", "17 h 05", 2, [
        ("day", "Aujourd’hui"),
        ("doc", "in", "soumission", "Voici la soumission révisée pour Mme Tremblay.", "equipe", "15 h 40"),
        ("txt", "out", "Merci, je la relis ce soir.", "read", "15 h 46"),
        ("voice", "in", 22, "equipe", "16 h 30"),
        ("txt", "in", "Revue de chantier demain, 9 h 30. On la fait en visio ?", "equipe", "17 h 05"),
        ("typing", "equipe", ""),
    ], "Parfait, j’envoie l’invitation à toute l’équipe."),
    ("tremblay", "pro", "La livraison de jeudi tient toujours ?", "11 h 12", 0, [
        ("day", "Aujourd’hui"),
        ("txt", "in", "Bonjour ! La livraison de jeudi tient toujours ?", "tremblay", "11 h 12"),
        ("txt", "out", "Oui, jeudi à 14 h comme prévu.", "dlv", "11 h 20"),
        ("typing", "tremblay", ""),
    ], "Merci beaucoup, à jeudi."),
    ("belanger", "pro", "Commande expédiée ce matin.", "Hier", 0, [
        ("day", "Hier"),
        ("txt", "in", "Commande expédiée ce matin. Livraison prévue lundi.", "belanger", "9 h 02"),
        ("txt", "out", "Merci, bien reçu.", "read", "9 h 15"),
        ("typing", "belanger", ""),
    ], "Je vous confirme l’heure lundi matin."),
]


def v_messages():
    rows, threads = "", ""
    for k, scope, prev, when, unread, msgs, reply in CONVS:
        p = PEOPLE[k]
        first = k in ("camille", "equipe")
        rows += (f'<li data-pp-only="{scope}"><button type="button" class="ap-cv-i{" is-on" if first else ""}" data-conv-open="{k}"'
                 f' aria-pressed="{"true" if first else "false"}">{_av(k)}'
                 f'<span class="ap-cv-t"><b>{p["n"]}</b><small data-conv-prev="{k}">{prev}</small></span>'
                 f'<span class="ap-cv-m"><time>{when}</time>{f"<i class=ap-cv-n>{unread}</i>" if unread else ""}</span></button></li>')
        threads += (f'<div class="ap-cv" data-cv="{k}" data-reply="{reply}"{"" if first else " hidden"}>'
                    f'<header class="ap-cv-h">{_av(k)}<span class="ap-cv-ht"><b>{p["n"]}</b>'
                    f'<small>{"<i class=ap-online></i>En ligne" if k in ("camille", "equipe") else p["role"]}</small></span>'
                    f'<button type="button" class="ap-cv-b" data-call-start="{k}" data-call-kind="audio" aria-label="Appeler {p["n"]}">{icon("call")}<span>Appel</span></button>'
                    f'<button type="button" class="ap-cv-b" data-call-start="{k}" data-call-kind="video" aria-label="Visio avec {p["n"]}">{icon("camera")}<span>Visio</span></button>'
                    f'</header><div class="ap-cv-th" data-thread>{"".join(_msg(m) for m in msgs)}</div></div>')
    return f"""{_head('Mon espace <span>/</span> <b>Mes messages</b>', 'Mes <em>messages</em>',
                      "Vos conversations, chez vous : rien ne passe par un nuage.", _pp())}
<div class="ap-ms">
  <aside class="ap-card ap-ms-list" data-r>
    <label class="ap-ms-q">{icon("search")}<input type="search" placeholder="Rechercher une conversation" aria-label="Rechercher une conversation" data-conv-q></label>
    <ul class="ap-cvl">{rows}</ul>
    <p class="ap-fine">{icon("lock")}<span>Chiffré de bout en bout · conservé sur votre Hub</span></p>
  </aside>
  <section class="ap-card ap-ms-conv" data-r aria-label="Conversation">
    {threads}
    <div class="ap-attach" data-attach hidden>
      <button type="button" data-attach-k="doc">{icon("doc")}<span><b>Document</b><small>PDF, notes, plans</small></span></button>
      <button type="button" data-attach-k="photo">{icon("image")}<span><b>Photo</b><small>De votre galerie</small></span></button>
      <button type="button" data-attach-k="pos">{icon("pin")}<span><b>Position</b><small>Le Hub, jamais la vôtre sans accord</small></span></button>
    </div>
    <form class="ap-ms-form" data-compose autocomplete="off">
      <button type="button" class="ap-ms-clip" data-attach-t aria-label="Joindre un fichier" aria-expanded="false">{icon("clip")}</button>
      <input type="text" class="ap-ms-in" placeholder="Écrire un message…" aria-label="Écrire un message" maxlength="240">
      <button type="button" class="ap-ms-mic" data-voice-rec aria-label="Enregistrer un message vocal">{icon("mic")}</button>
      <button type="submit" class="ap-go" aria-label="Envoyer">{icon("send")}</button>
    </form>
    <div class="ap-docv" data-docv hidden role="dialog" aria-label="Aperçu du document">
      <header><b data-docv-n></b><small data-docv-m></small>
        <button type="button" class="ap-btn" data-toast="Simulation : le document serait enregistré dans Mes documents.">{icon("folder")}Enregistrer</button>
        <button type="button" class="ap-x" data-docv-x aria-label="Fermer l’aperçu">{icon("x")}</button></header>
      <div class="ap-docv-b" data-docv-b></div>
    </div>
  </section>
</div>"""


def v_appels():
    jv = '<em class="ap-jvb">JARVIS a répondu</em>'

    def rappel(k):
        return f'<button type="button" class="ap-btn" data-call-start="{k}" data-call-kind="audio">{icon("call")}Rappeler</button>'

    def quote(txt):
        return f'<p class="ap-call-q">{icon("doc")}<span>« {txt} »</span></p>'

    calls = f"""
<li class="ap-call" data-pp-only="perso">
  <button type="button" class="ap-call-r is-dial" data-call-start="camille" data-call-kind="audio" aria-label="Appeler Camille">{face(AV_CAMILLE)}<span class="ap-call-t"><b>Camille</b><small>{icon("arrin", "i-in")}Entrant · accepté</small></span><time>Ce midi · 7 min</time>{icon("call", "ap-call-ch")}</button>
</li>
<li class="ap-call is-jv" data-pp-only="perso">
  <button type="button" class="ap-call-r" data-call aria-expanded="false">
    <span class="ap-orb sm" aria-hidden="true"></span>
    <span class="ap-call-t"><b>Numéro inconnu</b><small>{jv} · message pris</small></span>
    <time>9 h 05</time>{icon("down", "ap-call-ch")}
  </button>
  <div class="ap-call-d">
    {quote("JARVIS a pris le message, proposé jeudi 14 h, noté au calendrier.")}
    <div class="ap-call-a">{rappel("inconnu")}<span class="ap-state is-ok"><i aria-hidden="true"></i><span>Noté au calendrier</span></span></div>
  </div>
</li>
<li class="ap-call" data-pp-only="perso">
  <button type="button" class="ap-call-r is-dial" data-call-start="marc" data-call-kind="audio" aria-label="Appeler Marc">{mono("MA", "teal")}<span class="ap-call-t"><b>Marc</b><small>{icon("arrout", "i-out")}Sortant</small></span><time>Hier · 12 min</time>{icon("call", "ap-call-ch")}</button>
</li>
<li class="ap-call is-more" data-pp-only="perso">
  <button type="button" class="ap-call-r is-dial" data-call-start="maman" data-call-kind="audio" aria-label="Appeler Maman">{mono("M", "violet")}<span class="ap-call-t"><b>Maman</b><small>{icon("arrin", "i-in")}Entrant · accepté</small></span><time>Hier · 18 min</time>{icon("call", "ap-call-ch")}</button>
</li>
<li class="ap-call is-jv" data-pp-only="pro">
  <button type="button" class="ap-call-r" data-call aria-expanded="false">
    <span class="ap-orb sm" aria-hidden="true"></span>
    <span class="ap-call-t"><b>Atelier Fortin</b><small>{jv} · client</small></span>
    <time>10 h 20</time>{icon("down", "ap-call-ch")}
  </button>
  <div class="ap-call-d">
    {quote("Commande prête jeudi. JARVIS a proposé une livraison à 14 h et noté le suivi au calendrier.")}
    <div class="ap-call-a">{rappel("fortin")}<span class="ap-state is-ok"><i aria-hidden="true"></i><span>Suivi noté</span></span></div>
  </div>
</li>
<li class="ap-call" data-pp-only="pro">
  <button type="button" class="ap-call-r is-dial" data-call-start="tremblay" data-call-kind="audio" aria-label="Appeler Mme Tremblay">{mono("MT", "violet")}<span class="ap-call-t"><b>Mme Tremblay</b><small>{icon("arrin", "i-in")}Entrant · accepté</small></span><time>Ce matin · 4 min</time>{icon("call", "ap-call-ch")}</button>
</li>
<li class="ap-call" data-pp-only="pro">
  <button type="button" class="ap-call-r is-dial" data-call-start="belanger" data-call-kind="audio" aria-label="Appeler le fournisseur Bélanger">{mono("FB", "stone")}<span class="ap-call-t"><b>Fournisseur Bélanger</b><small>{icon("arrout", "i-out")}Sortant</small></span><time>Hier · 9 min</time>{icon("call", "ap-call-ch")}</button>
</li>"""

    def rejoindre(k):
        return f'<button type="button" class="ap-btn is-primary" data-call-start="{k}" data-call-kind="video">{icon("camera")}Rejoindre</button>'

    visio = f"""<article class="ap-card ap-visio" data-r>
  {_card_h("camera", "Visioconférence")}
  <div class="ap-vnext" data-pp-only="perso">
    <small>Ce soir · 20 h</small><b>Appel vidéo — Camille</b>
    <div class="ap-vrow"><span class="ap-faces">{face(AV_ALEX)}{face(AV_CAMILLE)}</span>{rejoindre("camille")}</div>
    <p class="ap-vok">{icon("check")}<span>Téléviseur du salon prêt · caméra et micro vérifiés</span></p>
  </div>
  <div class="ap-vnext" data-pp-only="pro">
    <small>Demain · 9 h 30 – 10 h 15</small><b>Revue de chantier — Atelier</b>
    <div class="ap-vrow"><span class="ap-faces">{face(AV_ALEX)}{face(AV_CAMILLE)}{face(AV_EQUIPE)}<i>+2</i></span>{rejoindre("equipe")}</div>
    <p class="ap-vok">{icon("check")}<span>Salle de réunion prête · caméra et micro vérifiés</span></p>
  </div>
  <div class="ap-vpast">
    <span><small>Hier · 15 h</small><b>{_px("Appel avec les parents", "Point d’équipe")}</b></span>
    <button type="button" class="ap-vsum" data-toast="Le résumé serait affiché ici : préparé par votre JARVIS, chez vous.">{icon("doc")}Résumé par JARVIS disponible</button>
  </div>
</article>"""
    priv = f"""<div class="ap-card ap-priv" data-r>
  <span class="ap-ring">{icon("lock")}</span>
  <p>Vos appels restent chez vous : la téléphonie passe par votre JARVIS Hub.</p>
</div>"""
    return f"""{_head('Mon espace <span>/</span> <b>Mes appels</b>', 'Mes <em>appels</em>',
                      "Appels et visioconférences, répondus avec vous — ou pour vous.", _pp())}
<div class="ap-ap">
  <div class="ap-card ap-callc" data-r>
    {_card_h("call", "Appels récents")}
    <ul class="ap-calls">{calls}</ul>
    <p class="ap-fine">{icon("info")}<span>Un numéro inconnu est filtré d’abord par JARVIS : il répond, prend le message, vous décidez.</span></p>
  </div>
  <div class="ap-col">{visio}{priv}</div>
</div>"""


def v_outils():
    """Un clic sur une extension l'ouvre directement : la page de la solution, déjà dans sa démo (#jarvis)."""
    cards = "".join(
        f'''<a class="ap-card ap-ext{" is-on" if c["slug"] in EXT_ON else ""}" href="{ext_href(c["slug"])}" data-ext="{c["slug"]}" data-r
   aria-label="Ouvrir l’extension {c["label"]} : {c["title"]}">
  <img src="{c["image"]}" alt="" loading="lazy" decoding="async">
  <span class="ap-ext-i">{icon(EXT_ICON[c["slug"]])}</span>
  <span class="ap-ext-t"><small>{c["label"]}</small><b>{c["title"]}</b><span>{c["short"]}</span></span>
  <span class="ap-ext-f"><em>{"Activée" if c["slug"] in EXT_ON else "Disponible · sur demande"}</em>
    <i class="ap-ext-go">Ouvrir l’extension{icon("right")}</i></span>
</a>'''
        for c in CAPABILITIES
    )
    on = sum(1 for c in CAPABILITIES if c["slug"] in EXT_ON)
    return f"""{_head("", "Mes <em>outils</em>", "Vos extensions : un clic, et elle s’ouvre dans JARVIS.",
                      f'<p class="ap-ext-n"><b>{len(CAPABILITIES)}</b> extensions · <b>{on}</b> activées</p>')}
<div class="ap-exts" style="--n:{len(CAPABILITIES)}">{cards}</div>"""


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
    cam = _cam_all()
    lst = "".join(
        f'<li><button type="button" class="ap-envl" data-env-go="{e["key"]}" aria-pressed="false">'
        f'{_env_photo(e, "ap-envl-img")}<span class="ap-envl-t"><b>{e["name"]}</b><small>{e["place"]}</small></span>'
        f'<span class="ap-envl-s"><i class="ap-env-dot" aria-hidden="true"></i><span data-env-short="{e["key"]}">{e["short"]}</span></span></button></li>'
        for e in ENVS
    )
    cards = ""
    for e in ENVS:
        chips = "".join(
            f'<span class="ap-chip"{f" data-live-{lv}" if lv else ""}>{icon(ic)}<small>{lab}</small><b>{val}</b></span>'
            for ic, lab, val, lv in e["chips"]
        )
        rows = "".join(f"<li>{icon(ic)}<span>{t}</span></li>" for ic, t in e["rows"])
        cards += f"""<article class="ap-envc" data-envc="{e["key"]}" hidden aria-label="{e["name"]}">
  <div class="ap-envc-ph">{_env_photo(e, "ap-envc-img")}
    <button type="button" class="ap-x" data-envc-x aria-label="Fermer">{icon("x")}</button>
    <span class="ap-envc-live"><i aria-hidden="true"></i>{"En direct" if e["key"] == "boulance" else "En ligne"}</span></div>
  <div class="ap-envc-b">
    <p class="ap-kick">{icon(e["icon"])}{e["kind"]}</p>
    <h4>{e["name"]}</h4><p class="ap-envc-pl">{icon("pin")}{e["place"]}</p>
    <div class="ap-chips">{chips}</div>
    <ul class="ap-envc-r">{rows}</ul>
    <div class="ap-envc-f">
      <a class="ap-btn is-primary" href="{ENV_HREF}">Ouvrir{icon("right")}</a>
      {f'<button type="button" class="ap-btn" data-route-t aria-pressed="true">{icon("route")}Trajet</button>' if e["key"] == "boulance" else
       f'<button type="button" class="ap-btn" data-envc-zoom>{icon("locate")}Centrer</button>'}
    </div>
  </div>
</article>"""
    return f"""{_head("", "Carte", "Vos environnements, à leur vraie place.",
                      '<p class="ap-ext-n"><b>6</b> lieux · <b>6</b> en ligne</p>')}
<div class="ap-ct">
  <div class="ap-card ap-map ap-map-big" data-r data-map data-cam="{cam[0]:.1f},{cam[1]:.1f},{cam[2]:.1f},{cam[3]:.1f}"
       data-box="{",".join(str(v) for v in BOX)}">
    {map_svg(_GEO["uid"], cam)}
    <div class="ap-ov">{map_overlays()}</div>
    <div class="ap-envcs">{cards}</div>
    <div class="ap-zoom"><button type="button" data-zoom="1" aria-label="Rapprocher">{icon("plus")}</button>
      <button type="button" data-zoom="-1" aria-label="Éloigner">{icon("minus")}</button>
      <button type="button" data-zoom="0" aria-label="Voir tous mes lieux">{icon("expand")}</button></div>
    <p class="ap-scale" aria-hidden="true"><i data-scale-bar></i><span data-scale-t>100 km</span></p>
    <p class="ap-nopos">{icon("lock")}<span>Aucune position de personne sans permission</span></p>
    <p class="ap-toast" data-ap="toast" role="status"></p>
  </div>
  <div class="ap-ct-side">
    <aside class="ap-card ap-envs" data-r>
      <header class="ap-card-h">{icon("pin")}<h4>Mes environnements</h4><span class="ap-count"><i class="ap-dot is-ok" aria-hidden="true"></i> en ligne</span></header>
      <ul>{lst}</ul>
    </aside>
    <aside class="ap-card ap-layers" data-r>
      <h4 class="ap-k">Afficher</h4>
      <div class="ap-lchips">
        <button type="button" class="ap-lchip" data-layer-t="villes" aria-pressed="true">{icon("city")}Villes</button>
        <button type="button" class="ap-lchip" data-layer-t="routes" aria-pressed="true">{icon("route")}Routes</button>
        <button type="button" class="ap-lchip" data-layer-t="trajet" aria-pressed="true">{icon("rv")}Trajet</button>
        <button type="button" class="ap-lchip" data-layer-t="personnes" aria-pressed="false">{icon("users")}Personnes</button>
      </div>
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
  {face(AV_CAMILLE) if ini == "CL" else mono(ini, tone)}
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


VIEWS = {"accueil": v_accueil, "assistant": v_assistant, "espace": v_espace, "journee": v_journee,
         "partage": v_partage, "messages": v_messages, "appels": v_appels, "carte": v_carte, "outils": v_outils}


def _stagger(html):
    """Chaque carte reçoit son rang d'apparition (--r) pour la révélation en cascade."""
    k = iter(range(100))
    return re.sub(r"data-r(?=[\s>])", lambda m: f'data-r style="--r:{next(k)}"', html)


ON = ' class="is-on"'


# ---------------------------------------------------------------------------------------------
# Barre du haut : palette de recherche, météo détaillée, menu du profil; appel en cours
# ---------------------------------------------------------------------------------------------
def _cmd_item(ic, label, sub, attrs, hint="", keys=""):
    k = f"{label} {sub} {keys}".lower()
    tag = "a" if attrs.startswith("href=") else "button"
    typ = "" if tag == "a" else ' type="button"'
    return (f'<{tag}{typ} class="ap-cmd-i" role="option" data-k="{k}" {attrs}><span class="ap-cmd-ic">{icon(ic)}</span>'
            f'<span class="ap-cmd-t"><b>{label}</b><small>{sub}</small></span><em>{hint}</em></{tag}>')


def _cmd():
    screens = [("accueil", "home", "Votre journée, sur un seul écran"), ("assistant", "spark", "Demander à JARVIS"),
               ("espace", "user", "Agenda, documents, partages"), ("journee", "calendar", "Agenda et tâches"),
               ("messages", "chat", "Conversations, documents, vocaux"), ("appels", "call", "Appels et visioconférences"),
               ("partage", "share", "Qui voit quoi, et jusqu’à quand"), ("carte", "map", "Vos environnements"),
               ("outils", "grid", "Toutes vos extensions")]
    g_screens = "".join(_cmd_item(ic, TITLE[k], sub, f'data-go="{k}"', "Écran") for k, ic, sub in screens)
    g_people = (
        _cmd_item("chat", "Camille", "Ouvrir la conversation", 'data-go="messages" data-conv="camille"', "Message", "amie souper")
        + _cmd_item("call", "Appeler Camille", "Appel audio par votre Hub", 'data-call-start="camille" data-call-kind="audio"', "Appel")
        + _cmd_item("camera", "Visio avec Camille", "Caméra et micro vérifiés", 'data-call-start="camille" data-call-kind="video"', "Visio")
        + _cmd_item("users", "Équipe Atelier", "Conversation de l’équipe", 'data-go="messages" data-conv="equipe" data-pp-set="pro"', "Message", "travail soumission")
        + _cmd_item("camera", "Visio avec l’équipe", "Revue de chantier", 'data-call-start="equipe" data-call-kind="video"', "Visio", "atelier")
    )
    g_places = "".join(
        _cmd_item(e["icon"], e["name"], f'{e["kind"]} · {e["place"]}', f'data-go="carte" data-env-go="{e["key"]}"', "Lieu", e["short"])
        for e in ENVS
    )
    g_ext = "".join(
        _cmd_item(EXT_ICON[c["slug"]], c["label"], c["title"], f'href="{ext_href(c["slug"])}"', "Extension", c["short"])
        for c in CAPABILITIES
    )
    g_set = (
        "".join(_cmd_item("palette", f"Mode {m}", "Mode d’affichage du site", f'data-mode-pick="{m.lower()}"', "Réglage", "apparence thème")
                for m in ("Signature", "Platinum", "Base"))
        + _cmd_item("brief", "Espace professionnel", "Clients, équipe, appels d’affaires", 'data-pp-set="pro"', "Réglage", "travail pro")
        + _cmd_item("user", "Espace personnel", "Famille, amis, maison", 'data-pp-set="perso"', "Réglage", "perso")
        + _cmd_item("sun", "Météo de Saint-Hyacinthe", "Prévisions réelles, heure par heure", 'data-pop-open="wx"', "Météo", "temps température pluie neige")
    )
    groups = [("Écrans", g_screens), ("Personnes", g_people), ("Lieux", g_places), ("Extensions", g_ext), ("Réglages", g_set)]
    body = "".join(f'<div class="ap-cmd-grp"><p class="ap-cmd-g">{t}</p>{h}</div>' for t, h in groups)
    return f"""<div class="ap-pop ap-cmd" data-pop-panel="cmd" hidden role="dialog" aria-label="Rechercher dans JARVIS">
  <label class="ap-cmd-q">{icon("search")}<input type="search" placeholder="Un écran, une personne, un lieu, une extension…" aria-label="Rechercher" data-cmd-q autocomplete="off"><kbd>Échap</kbd></label>
  <div class="ap-cmd-r" role="listbox" aria-label="Résultats">{body}
    <p class="ap-cmd-none" hidden>{icon("search")}<span>Aucun résultat pour « <b data-cmd-term></b> ».</span></p></div>
  <footer class="ap-cmd-f"><span><kbd>↑</kbd><kbd>↓</kbd> choisir</span><span><kbd>Entrée</kbd> ouvrir</span><span class="ap-cmd-sim">Données d’exemple</span></footer>
</div>"""


def _wx_defs(uid):
    """Pictogrammes météo en couleur (dégradés), une fois par appareil, réutilisés par le panneau météo."""
    cloud = "M19 48h27a10 10 0 0 0 1.6-19.9A14 14 0 0 0 20.6 31 8.6 8.6 0 0 0 19 48Z"
    cloud_s = "M17 41h25a9 9 0 0 0 1.4-17.9A12.6 12.6 0 0 0 19 26.2 7.7 7.7 0 0 0 17 41Z"
    rays = "".join(
        f'<path d="M{32 + 18 * math.cos(a):.1f} {32 + 18 * math.sin(a):.1f}L{32 + 24 * math.cos(a):.1f} {32 + 24 * math.sin(a):.1f}"/>'
        for a in [i * math.pi / 4 for i in range(8)]
    )
    rays_s = "".join(
        f'<path d="M{24 + 13 * math.cos(a):.1f} {24 + 13 * math.sin(a):.1f}L{24 + 17.5 * math.cos(a):.1f} {24 + 17.5 * math.sin(a):.1f}"/>'
        for a in [i * math.pi / 4 for i in range(8)]
    )
    moon = "M40.5 41.5A15 15 0 0 1 26.5 19a15 15 0 1 0 14 22.5Z"
    return f"""<svg class="ap-geo-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
<radialGradient id="{uid}-gsun" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#fff7dc"/><stop offset=".45" stop-color="#ffd27a"/><stop offset="1" stop-color="#e9a23b"/></radialGradient>
<linearGradient id="{uid}-gcl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbfbfc"/><stop offset="1" stop-color="#a7a7b0"/></linearGradient>
<linearGradient id="{uid}-gcd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9d9de"/><stop offset="1" stop-color="#6e6e78"/></linearGradient>
<linearGradient id="{uid}-gmo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf6ea"/><stop offset="1" stop-color="#b8b0a2"/></linearGradient>
<symbol id="{uid}-sun" viewBox="0 0 64 64"><g stroke="#ffd98a" stroke-width="3.2" stroke-linecap="round">{rays}</g><circle cx="32" cy="32" r="12.5" fill="url(#{uid}-gsun)"/></symbol>
<symbol id="{uid}-moon" viewBox="0 0 64 64"><path d="{moon}" fill="url(#{uid}-gmo)"/><circle cx="46" cy="18" r="1.4" fill="#f4efe4"/><circle cx="51" cy="28" r="1" fill="#f4efe4" opacity=".7"/></symbol>
<symbol id="{uid}-cloud" viewBox="0 0 64 64"><path d="{cloud}" fill="url(#{uid}-gcl)"/></symbol>
<symbol id="{uid}-partly" viewBox="0 0 64 64"><g stroke="#ffd98a" stroke-width="2.6" stroke-linecap="round">{rays_s}</g><circle cx="24" cy="24" r="9.5" fill="url(#{uid}-gsun)"/><path d="{cloud}" fill="url(#{uid}-gcl)" transform="translate(4 4)"/></symbol>
<symbol id="{uid}-partlyn" viewBox="0 0 64 64"><path d="M30 30A11 11 0 0 1 19.6 13.5a11 11 0 1 0 10.4 16.5Z" fill="url(#{uid}-gmo)"/><path d="{cloud}" fill="url(#{uid}-gcl)" transform="translate(4 4)"/></symbol>
<symbol id="{uid}-rain" viewBox="0 0 64 64"><path d="{cloud_s}" fill="url(#{uid}-gcd)"/><g stroke="#cfd6df" stroke-width="2.6" stroke-linecap="round"><path d="M22 47l-2.5 6M32 47l-2.5 6M42 47l-2.5 6"/></g></symbol>
<symbol id="{uid}-snow" viewBox="0 0 64 64"><path d="{cloud_s}" fill="url(#{uid}-gcd)"/><g fill="#f6f7f9"><circle cx="21" cy="49" r="2.2"/><circle cx="31" cy="53" r="2.2"/><circle cx="41" cy="49" r="2.2"/><circle cx="26" cy="58" r="1.8"/><circle cx="36" cy="58" r="1.8"/></g></symbol>
<symbol id="{uid}-storm" viewBox="0 0 64 64"><path d="{cloud_s}" fill="url(#{uid}-gcd)"/><path d="M33 42l-6 10h5l-3 9 9-12h-5l3-7z" fill="url(#{uid}-gsun)"/></symbol>
<symbol id="{uid}-fog" viewBox="0 0 64 64"><path d="{cloud_s}" fill="url(#{uid}-gcl)" opacity=".85"/><g stroke="#c9c9cf" stroke-width="3" stroke-linecap="round"><path d="M12 47h40M18 54h30"/></g></symbol>
</defs></svg>"""


def _wxp(uid):
    return f"""<div class="ap-pop ap-wxp" data-pop-panel="wx" hidden role="dialog" aria-label="Météo de Saint-Hyacinthe">
  <div class="ap-wxp-hero" data-wxp-sky>
    <div class="ap-wxp-now"><small>{icon("pin")}Saint-Hyacinthe<span class="ap-live"> · en direct</span></small>
      <b><span data-wxp="t">—</span><sup>°C</sup></b><span class="ap-wxp-cond" data-wxp="cond">Chargement de la météo…</span>
      <small class="ap-wxp-hl" data-wxp="hl"></small></div>
    <svg class="ap-wxp-art" viewBox="0 0 64 64" aria-hidden="true"><use data-wxp="art" href="#{uid}-cloud"/></svg>
    <button type="button" class="ap-x" data-pop-close aria-label="Fermer la météo">{icon("x")}</button>
  </div>
  <div class="ap-wxp-body">
    <section class="ap-wxp-sec"><p class="ap-wxp-k">{icon("clock")}Les prochaines heures</p>
      <div class="ap-wxp-hours" data-wxp="hours"></div></section>
    <div class="ap-wxp-cols">
      <section class="ap-wxp-sec"><p class="ap-wxp-k">{icon("calendar")}Les prochains jours</p><ol class="ap-wxp-days" data-wxp="days"></ol></section>
      <div class="ap-wxp-side">
        <div class="ap-wxp-grid" data-wxp="grid"></div>
        <section class="ap-wxp-sec ap-wxp-sun"><p class="ap-wxp-k">{icon("sun")}Soleil</p><div data-wxp="sun"></div></section>
      </div>
    </div>
    <p class="ap-wxp-src">{icon("info")}<span data-wxp="src">Environnement Canada · données réelles</span></p>
  </div>
</div>"""


def _me_menu():
    modes = "".join(
        f'<button type="button" class="ap-mode" data-mode-pick="{m}" aria-pressed="false"><img src="/media/modes/{m}.webp" alt="" loading="lazy" decoding="async">'
        f'<span>{lab}</span></button>'
        for m, lab in (("signature", "Signature"), ("platinum", "Platinum"), ("base", "Base"))
    )
    return f"""<div class="ap-pop ap-menu" data-pop-panel="me" hidden role="dialog" aria-label="Profil d’Alex">
  <div class="ap-me-h">{face(AV_ALEX)}<span><b>Alex</b><small>Compte personnel · Hub de Saint-Hyacinthe</small></span></div>
  <button type="button" class="ap-mi" data-toast="Mon profil : nom, photo et clés d’accès. Votre biométrie reste sur votre appareil.">{icon("user")}<span><b>Mon profil</b><small>Nom, photo, clés d’accès</small></span></button>
  <p class="ap-mk">Espace affiché</p>
  {_pp()}
  <p class="ap-mk">Mode d’affichage du site</p>
  <div class="ap-modes">{modes}</div>
  <button type="button" class="ap-mi" data-go="espace">{icon("bell")}<span><b>Notifications</b><small>2 non lues</small></span><i class="ap-dot is-red" aria-hidden="true"></i></button>
  <button type="button" class="ap-mi is-lock" data-toast="{fr(ADMIN_NOTE)}">{icon("sliders")}<span><b>Administration</b><small>Réservée à l’administrateur du Hub</small></span>{icon("lock", "ap-mi-lock")}</button>
  <button type="button" class="ap-mi" data-toast="Simulation : vous resteriez connecté sur cet appareil jusqu’à votre retour.">{icon("logout")}<span><b>Se déconnecter</b><small>Cet appareil seulement</small></span></button>
</div>"""


def _callov():
    return f"""<div class="ap-callov" data-callov hidden role="dialog" aria-label="Appel en cours">
  <div class="ap-co-top"><span class="ap-co-sec">{icon("lock")}Chiffré · par votre Hub</span>
    <b data-co="title">Camille</b><span class="ap-co-time" data-co="time">Appel…</span></div>
  <div class="ap-co-audio">
    <span class="ap-co-face"><i></i><i></i><span data-co="av"></span></span>
    <b data-co="name">Camille</b><small data-co="state">Appel en cours</small>
  </div>
  <div class="ap-co-video"><div class="ap-co-tiles" data-co="tiles"></div>
    <div class="ap-co-self" data-co="self"><img src="{PEOPLE["alex"]["hd"] or AV_ALEX}" alt="" decoding="async"><span>Vous</span>
      <em>{icon("camoff")}Caméra coupée</em></div></div>
  <div class="ap-co-ctrl">
    <button type="button" class="ap-co-b" data-co-t="mute" aria-pressed="false">{icon("mic", "i-on")}{icon("micoff", "i-off")}<small>Micro</small></button>
    <button type="button" class="ap-co-b is-a" data-co-t="spk" aria-pressed="false">{icon("speaker")}<small>Haut-parleur</small></button>
    <button type="button" class="ap-co-b" data-co-t="cam" aria-pressed="false">{icon("camera", "i-on")}{icon("camoff", "i-off")}<small>Caméra</small></button>
    <button type="button" class="ap-co-b is-v" data-co-t="screen" aria-pressed="false">{icon("screen")}<small>Partager</small></button>
    <button type="button" class="ap-co-b is-end" data-co-end aria-label="Raccrocher">{icon("hang")}<small>Raccrocher</small></button>
  </div>
  <p class="ap-co-sim">Simulation : aucun appel réel n’est lancé.</p>
</div>"""


def _people_json():
    out = {}
    for k, p in PEOPLE.items():
        out[k] = {"n": p["n"], "img": p.get("img"), "hd": p.get("hd"), "ini": p.get("ini"), "tone": p.get("tone"),
                  "role": p.get("role", ""), "group": p.get("group")}
    return json.dumps(out, ensure_ascii=False).replace("</", "<\\/")


_DEVICE_N = iter(range(1, 1000))


def _device(only=None):
    """L'appareil. `only` = clé d'écran : un seul écran, la barre latérale devient un index des chapitres
    (menu de la révision 25)."""
    single = only is not None
    uid = f"apgeo{next(_DEVICE_N)}"
    _GEO["uid"] = uid
    if single:
        parent = next(n for (k, n, _d, _t, _p) in SCREENS if k == only)
        items = "".join(
            f'<a class="ap-jump{" is-on" if k == parent else ""}" href="#ecran-{k}"'
            f'{" aria-current=\'true\'" if k == parent else ""} aria-label="{lab}">{icon(ic)}'
            f'<span class="l-long">{lab}</span><span class="l-short" aria-hidden="true">{short}</span></a>'
            for (k, lab, short, ic) in NAV
        )
        nav = f'<div class="ap-nav" aria-label="Écrans de JARVIS App">{items}</div>'
        picked = [x for x in SCREENS if x[0] == only]
        views = "".join(
            f'<section class="ap-view ap-v-{k} is-on" role="group" id="ap-p-{k}-s" aria-label="{TITLE[k]}" '
            f'data-view="{k}" data-nav="{n}" data-dur="{d}">{_stagger(fr(VIEWS[k]()))}</section>'
            for (k, n, d, _t, _p) in picked
        )
        caps = ""
        geo = geo_defs(uid) if only in ("accueil", "carte") else ""
    else:
        tabs = "".join(
            f'<button type="button" role="tab" id="ap-t-{k}" aria-controls="ap-p-{k}" aria-selected="{"true" if i == 0 else "false"}" '
            f'tabindex="{0 if i == 0 else -1}" data-nav="{k}" aria-label="{lab}"{ON if i == 0 else ""}>{icon(ic)}'
            f'<span class="l-long">{lab}</span><span class="l-short" aria-hidden="true">{short}</span></button>'
            for i, (k, lab, short, ic) in enumerate(NAV)
        )
        nav = (f'<div class="ap-nav" role="tablist" aria-label="Écrans de JARVIS App" aria-orientation="vertical">'
               f'<i class="ap-ind" aria-hidden="true"><i class="ap-prog"></i></i>{tabs}</div>')
        views = "".join(
            f'<section class="ap-view ap-v-{k}{" is-on" if i == 0 else ""}" role="tabpanel" id="ap-p-{k}" aria-labelledby="ap-t-{n}" '
            f'data-view="{k}" data-nav="{n}" data-title="{TITLE[k]}" data-dur="{d}"{"" if i == 0 else " inert"}>{_stagger(fr(VIEWS[k]()))}</section>'
            for i, (k, n, d, _t, _p) in enumerate(SCREENS)
        )
        caps = f"""
  <div class="ap-caps">
    <div class="ap-cap-txt" aria-live="polite">{"".join(
        f'<div class="ap-cap{" is-on" if i == 0 else ""}"><h3>{fr(t)}</h3><p>{fr(p)}</p></div>'
        for i, (_k, _n, _d, t, p) in enumerate(SCREENS))}</div>
    <div class="ap-ctrl">
      <span class="ap-step"><b data-ap="step">01</b> / {len(SCREENS):02d}</span>
      <button type="button" class="ap-play" data-ap="play" aria-label="Mettre la visite en pause">{icon("pause", "i-pause")}{icon("play", "i-play")}<span>Pause</span></button>
      <span class="ap-hint">Touchez un écran : tout y est cliquable</span>
    </div>
  </div>"""
        geo = geo_defs(uid)

    label = "JARVIS App, démonstration avec données fictives"
    return f"""<div class="ap{" is-single" if single else ""}" data-demo="app" data-geo="{uid}"{f' data-single="{only}"' if single else ""}>
  <div class="ap-stage">
    <div class="ap-glow" aria-hidden="true"></div>
    <div class="ap-tilt">
      <div class="ap-device">
        <div class="ap-win">
          <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
          <b>JARVIS · Ma vie</b>
          <span class="ap-win-sep" aria-hidden="true">/</span>
          <span class="ap-win-name" data-ap="winname">{TITLE[only] if single else "Accueil"}</span>
          <span class="tag tag-sim">Démo · données fictives</span>
        </div>
        <div class="ap-screen" role="group" aria-roledescription="démonstration" aria-label="{label}">
          {geo}{_wx_defs(uid)}
          <script type="application/json" class="ap-people">{_people_json()}</script>
          <div class="ap-bg" aria-hidden="true"></div>
          <img class="ap-banner" src="{BANNER}" alt="" aria-hidden="true" loading="lazy" decoding="async" width="1990" height="342">
          <nav class="ap-side" aria-label="JARVIS App">
            <div class="ap-brand" aria-hidden="true"><b>JARVIS</b><small>Private Systems</small><em class="ap-modename"></em></div>
            {nav}
            <button type="button" class="ap-admin" data-toast="{fr(ADMIN_NOTE)}">{icon("sliders")}<span class="l-long">Administration</span></button>
            <div class="ap-side-f"><p class="ap-motto">Votre espace.<br>À votre image.</p></div>
          </nav>
          <div class="ap-main">
            <header class="ap-top">
              <button type="button" class="ap-search" data-pop-open="cmd" aria-haspopup="dialog" aria-label="Rechercher dans JARVIS">{icon("search")}<span>Que souhaitez-vous faire{NB}?</span><kbd>Ctrl K</kbd></button>
              <span class="ap-status-time" data-ap="clock">19{NB}h{NB}42</span>
              <button type="button" class="ap-wx" data-pop-open="wx" aria-haspopup="dialog" aria-label="Météo de Saint-Hyacinthe">
                <span class="ap-wx-i" aria-hidden="true">{WX}</span>
                <span><b><span data-ap="temp">—</span><span class="ap-unit">{NB}°C</span></b><small>Saint-Hyacinthe<span class="ap-live"> · en direct</span></small></span>
              </button>
              <button type="button" class="ap-top-call" data-go="appels" aria-label="Mes appels" title="Mes appels">{icon("call")}</button>
              <button type="button" class="ap-top-call ap-pin" data-go="carte" aria-label="Carte de mes lieux" title="Carte de mes lieux">{icon("pin")}</button>
              <button type="button" class="ap-me" data-pop-open="me" aria-haspopup="dialog" aria-label="Profil d’Alex">{face(AV_ALEX)}<b>Alex</b>{icon("down")}</button>
            </header>
            <div class="ap-views">{views}</div>
          </div>
          <div class="ap-scrim" data-scrim hidden></div>
          {fr(_cmd())}{_wxp(uid)}{fr(_me_menu())}{fr(_callov())}
          <p class="ap-flash" role="status" aria-live="polite"></p>
        </div>
        <i class="ap-sweep" aria-hidden="true"></i>
      </div>
    </div>
  </div>{caps}
</div>"""


def html():
    """Un seul appareil, visite automatique des neuf écrans."""
    return _device()


def sequence():
    """Les écrans principaux déroulés l'un sous l'autre : un chapitre, un appareil, beaucoup d'air."""
    info = {k: (t, p) for (k, _n, _d, t, p) in SCREENS}
    rail = "".join(
        f'<li><a href="#ecran-{k}"><i>{i + 1:02d}</i><span>{TITLE[k]}</span></a></li>'
        for i, k in enumerate(SEQUENCE)
    )
    chapters = "".join(
        f"""<section class="apx-ch" id="ecran-{k}" aria-labelledby="ecran-{k}-t">
  <div class="apx-head" data-rev>
    <p class="apx-k"><i>{i + 1:02d}</i><span>{TITLE[k]}</span></p>
    <h3 id="ecran-{k}-t">{fr(info[k][0])}</h3>
    <p>{fr(info[k][1])}</p>
  </div>
  {_device(k)}
</section>"""
        for i, k in enumerate(SEQUENCE)
    )
    return f"""<div class="apx">
  <nav class="apx-rail" aria-label="Les écrans de JARVIS App"><ol>{rail}</ol>
    <p class="apx-note">{icon("info")}<span>Données fictives{NB}· tout est cliquable</span></p>
  </nav>
  {chapters}
</div>"""
