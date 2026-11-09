# Démo « Hub + extensions » de la page JARVIS (/plateforme/).
# Quatre blocs, chacun autonome :
#   coeur()    Le Hub, cœur de JARVIS : le boîtier en photo, sa lumière et ce qu'il fait marcher; un Hub
#              par lieu, une seule app; en petit, ce qu'il héberge et les extensions branchées.
#   ia()       L'IA au cœur : une conversation qui comprend, vérifie, propose, demande, explique.
#   ensemble() Comment les extensions travaillent ensemble : rôles, règle du bus, trois chaînes de bout en bout.
# Données de l'offre (HUB_INCLUS, SERVICES) : source unique, affichées sur /offre/ (src/pages/offre.py).
# Sans JavaScript, chaque bloc montre un état complet et lisible; assets/demos/hub.js anime le reste.
# Toutes les situations sont des données d'exemple.

import json
import os
from html import escape



def _js(obj):
    """JSON prêt à glisser dans <script type="application/json"> (aucune fin de balise possible)."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


# ---------------------------------------------------------------------------
# Icônes (traits, 24 × 24)
# ---------------------------------------------------------------------------
ICONS = {
    "env": '<path d="M3.5 11.2L12 4l8.5 7.2"/><path d="M5.8 9.6V20h12.4V9.6"/><path d="M10 20v-5.2h4V20"/>',
    "ia": '<path d="M12 3.2l1.9 4.9 4.9 1.9-4.9 1.9L12 16.8l-1.9-4.9-4.9-1.9 4.9-1.9z"/><path d="M18.6 15.4l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/><path d="M5.4 15.8l.6 1.5 1.5.6-1.5.6-.6 1.5-.6-1.5-1.5-.6 1.5-.6z"/>',
    "secu": '<path d="M12 3l7.5 3v5.4c0 4.5-3.1 8-7.5 9.9-4.4-1.9-7.5-5.4-7.5-9.9V6z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/>',
    "auto": '<rect x="3.5" y="7" width="17" height="12.5" rx="2.2"/><path d="M9 7V5.2c0-.9.7-1.7 1.7-1.7h2.6c.9 0 1.7.8 1.7 1.7V7"/><path d="M3.5 12.4h17"/><path d="M11 12.4v2h2v-2"/>',
    "res": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="18.5" r="2.2"/><circle cx="19" cy="18.5" r="2.2"/><circle cx="12" cy="13" r="2.2"/><path d="M12 7.2v3.6M10.3 14.4l-3.7 2.8M13.7 14.4l3.7 2.8"/>',
    "diag": '<path d="M3 12.5h3.6l2.2-5.4 3.8 10.4 2.6-6.6 1.6 1.6H21"/>',
    "mob": '<path d="M4 15.5V9.8c0-1.1.9-2.1 2.1-2.3l8.7-1.4c.9-.1 1.8.3 2.3 1.1l2.6 4.2c.2.4.3.8.3 1.2v2.9c0 .6-.5 1-1 1h-1.2"/><path d="M8.9 16.5h5.6"/><circle cx="6.7" cy="16.6" r="1.9"/><circle cx="16.8" cy="16.6" r="1.9"/><path d="M4 11.8h11.6"/>',
    "hub": '<path d="M12 2.6l8.2 4.7v9.4L12 21.4l-8.2-4.7V7.3z"/><circle cx="12" cy="12" r="3.2"/><path d="M12 2.6v6.2M20.2 16.7l-5.4-3.1M3.8 16.7l5.4-3.1"/>',
    "regles": '<path d="M6 3.5h9l3.5 3.5v13.5H6z"/><path d="M14.5 3.5V7.5h4"/><path d="M9 12h6.5M9 15.5h6.5M9 8.8h3"/>',
    "comptes": '<circle cx="9" cy="8.5" r="3.2"/><path d="M3.5 19.5c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5"/><rect x="14.5" y="10.5" width="6" height="5" rx="1.2"/><path d="M15.9 10.5V9.2a1.6 1.6 0 0 1 3.2 0v1.3"/>',
    "journal": '<path d="M5 4.5h11.5a2 2 0 0 1 2 2v13H7a2 2 0 0 1-2-2z"/><path d="M5 17.5a2 2 0 0 1 2-2h11.5"/><path d="M8.5 8.5h6.5M8.5 11.5h4.5"/>',
    "bus": '<path d="M3 8h18M3 16h18"/><circle cx="7" cy="8" r="1.6"/><circle cx="15" cy="16" r="1.6"/><path d="M11 8v8"/>',
    "iacore": '<rect x="6" y="6" width="12" height="12" rx="2.4"/><path d="M9.5 9.5h5v5h-5z"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "sauve": '<ellipse cx="12" cy="6" rx="7" ry="2.6"/><path d="M5 6v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6V6"/><path d="M5 12v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6v-6"/>',
    "cloud": '<path d="M7 18.5h10.2a4.3 4.3 0 0 0 .6-8.6A6 6 0 0 0 6.3 11a3.8 3.8 0 0 0 .7 7.5z"/>',
    "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8 10.5V7.8a4 4 0 0 1 8 0v2.7"/>',
    "play": '<path d="M8 5.5v13l10-6.5z"/>',
    "pause": '<path d="M8.5 5.5v13M15.5 5.5v13"/>',
    "prev": '<path d="M15 5.5L8.5 12l6.5 6.5"/>',
    "next": '<path d="M9 5.5l6.5 6.5L9 18.5"/>',
    "replay": '<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3"/><path d="M4.5 4.5v4h4"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "tool": '<path d="M14.6 6.2a4 4 0 0 0-5.3 5.1L4 16.6 7.4 20l5.3-5.3a4 4 0 0 0 5.1-5.3l-2.5 2.5-2.6-.6-.6-2.6z"/>',
    "soutien": '<path d="M4.5 13v-1.5a7.5 7.5 0 0 1 15 0V13"/><rect x="3.5" y="13" width="4" height="6" rx="1.5"/><rect x="16.5" y="13" width="4" height="6" rx="1.5"/><path d="M18.5 19c0 1.2-1.6 2-4 2h-1.5"/>',
    "install": '<path d="M12 3.5v11"/><path d="M7.5 10.5L12 15l4.5-4.5"/><path d="M4.5 16.5v2.5c0 .8.7 1.5 1.5 1.5h12c.8 0 1.5-.7 1.5-1.5v-2.5"/>',
    "mesure": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M7 15l3.5-4 3 2.5L19 7"/>',
    "lampe": '<path d="M9 18.5h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2v.5h5V16c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "camera": '<rect x="3" y="7" width="13" height="10" rx="2.2"/><path d="M16 10.5l5-2.8v8.6l-5-2.8"/><circle cx="9.5" cy="12" r="2.2"/>',
    "porte": '<path d="M6 21V4.5c0-.6.5-1 1-1h10c.6 0 1 .4 1 1V21"/><path d="M3.5 21h17"/><circle cx="14.6" cy="12.5" r=".9"/>',
    "thermo": '<path d="M10 14.2V5a2 2 0 0 1 4 0v9.2a4 4 0 1 1-4 0z"/><path d="M12 9v7.5"/>',
    "phone": '<rect x="6.5" y="2.8" width="11" height="18.4" rx="2.6"/><path d="M10.5 18h3"/>',
    "mic": '<rect x="9" y="3.5" width="6" height="11" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v2.5"/>',
}


def icon(name, cls="hb-i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# Les sept extensions (ordre et noms de config.CAPABILITIES)
# ---------------------------------------------------------------------------
EXT = [
    # clé, slug, nom court, nom complet, couleur, rôle (une ligne), publie, s'abonne à, inclus
    ("env", "environnements-intelligents", "Environnements", "Environnements intelligents", "#7cc4ff",
     "Les capteurs et les équipements du lieu.",
     "Mesures, états, équipements qui changent",
     "Arrivées, absences, heures de la journée",
     ["Lumières, chauffage, stores, verrous et énergie, pièce par pièce",
      "Capteurs du lieu : température, eau, air, présence",
      "Ambiances en une touche : Matin, Soirée, Nuit, Absent",
      "Verrous et garage toujours sur confirmation"]),
    ("ia", "ia-privee-connaissances", "IA privée", "IA privée et connaissances", "#c8adff",
     "La mémoire documentaire.",
     "Documents classés, passages retrouvés",
     "Rapports, bons fermés, garanties",
     ["Recherche dans vos documents, manuels, contrats et notes",
      "Chaque réponse montre le passage qui la justifie",
      "Classement automatique des rapports et des factures",
      "Traitement sur le Hub; externe seulement si vous l’autorisez"]),
    ("secu", "securite-intelligente", "Sécurité", "Sécurité intelligente", "#ff9f7f",
     "Protéger et consigner.",
     "Accès, arrivées, alarmes, images utiles",
     "Absences, interventions prévues, appareils hors ligne",
     ["Caméras, sonnette, portes, détecteurs et alarme dans un même fil",
      "Accès temporaires et badges, limités dans le temps et l’espace",
      "Preuves gardées sur place, avec l’événement",
      "Rien ne se déverrouille tout seul"]),
    ("auto", "automatisation-operations", "Entreprise", "Automatisation d’entreprise", "#f5c56b",
     "Les personnes et les processus : bons de travail, appels, approbations.",
     "Bons de travail, appels, approbations",
     "Diagnostics, demandes de clients, seuils dépassés",
     ["Réception téléphonique et prise de messages",
      "Bons de travail avec le contexte, au bon employé",
      "Garde, relances et appel si personne ne répond",
      "Approbations, seuils et exceptions écrits une fois"]),
    ("res", "reseau-resilience", "Réseau", "Réseau et cybersécurité", "#8ea2ff",
     "Relier et défendre.",
     "Liens, appareils, menaces bloquées",
     "Nouveaux appareils, besoins de bande passante",
     ["Carte du réseau en direct, en mots simples",
      "Zones séparées : famille, objets, caméras, invités",
      "Lien de secours quand Internet tombe",
      "Appareil suspect isolé, sur votre approbation"]),
    ("diag", "diagnostic-care", "Diagnostic", "Diagnostic et continuité", "#62dbd2",
     "Mesurer, tester, comprendre.",
     "Écarts confirmés, résultats de tests, retours à la normale",
     "Mesures hors seuil, interventions terminées",
     ["Tests guidés et mesures comparées à la normale",
      "Cause probable en mots simples",
      "Dossier prêt pour le technicien, avec la bonne pièce",
      "Suivi du retour à la normale après la réparation"]),
    ("mob", "mobilite", "Mobilité", "Mobilité", "#4ade80",
     "Le déplacement.",
     "Trajets, heures d’arrivée, état du véhicule",
     "Autonomie, besoins d’arrêt, météo de la route",
     ["Copilote de route : arrêts, heures d’ouverture, soleil",
      "État du véhicule et de ses batteries",
      "Chaque voyage gardé sur la carte",
      "Commandes du véhicule toujours sur confirmation"]),
]
EXT_BY = {e[0]: e for e in EXT}


def _chip_ext(k, extra=""):
    e = EXT_BY[k]
    return f'<span class="hb-x hb-x-{k}{extra}" style="--x:{e[4]}">{icon(k)}<b>{e[2]}</b></span>'


# ---------------------------------------------------------------------------
# 1. Le Hub, cœur de JARVIS
# ---------------------------------------------------------------------------
# Le Hub montré comme un bel objet : la vraie photo du boîtier, une lumière or qui respire, et des fils
# de lumière doux vers les choses de la vie, avec des phrases humaines. Puis « Un Hub par lieu, une seule
# app » (photos des lieux du site, chacun avec son petit Hub, reliés au téléphone), quatre réponses
# courtes, les deux formats du Hub, et, en petit, ce qu'il y a dedans pour les curieux.

# Photo du boîtier : les positions (en % de l'image 16:9) de la lumière avant et du boîtier servent aux
# fils de lumière et au halo. Changer de photo demande de revoir HUB_LED et HUB_HALO.
HUB_PHOTO = "/media/product/jarvis-hub-v1.webp"
HUB_LED = (44.0, 56.0)
HUB_HALO = (34.0, 55.0)

# Les choses de la vie : clé, icône, chose, phrases (la première est affichée sans JavaScript),
# position de la carte sur la photo (gauche %, haut %), côté d'attache du fil.
VIE = [
    ("lumieres", "lampe", "Les lumières", ["Les lumières du soir s’allument", "Ambiance Soirée, douce et chaude", "Tout s’éteint quand vous dormez"],
     (3, 7), "bas"),
    ("cameras", "camera", "Les caméras", ["Les caméras veillent", "Un colis déposé à 14 h 12, photo gardée", "Personne autour de la maison"],
     (3, 24), "droite"),
    ("porte", "porte", "La porte d’entrée", ["La porte est verrouillée", "Verrouillée à 22 h 04, comme chaque soir", "Ouverte pour la gardienne à 15 h 30"],
     (75.5, 6), "gauche"),
    ("chalet", "thermo", "Le chalet", ["Le chalet est chauffé pour vendredi", "21 °C à votre arrivée, vendredi 18 h", "L’eau est coupée en votre absence"],
     (75.5, 24.5), "gauche"),
    ("voiture", "mob", "La voiture", ["La voiture est chargée à 80 %", "Prête pour demain, 7 h 30", "Le garage se ferme derrière vous"],
     (75.5, 43), "gauche"),
    ("app", "phone", "Votre téléphone", ["Tout est dans votre application", "Une touche : « Je pars »", "Même à l’autre bout du monde"],
     (75.5, 61.5), "gauche"),
]
VIE_W, VIE_H = 21.5, 4.9  # largeur d'une carte et demi-hauteur, en % de la scène


def _insec(t):
    """Espaces insécables devant %, °C et h (« 80 % » ne se coupe pas)."""
    return t.replace(" %", "\u00a0%").replace(" °C", "\u00a0°C").replace(" h ", "\u00a0h\u00a0")


def _fil(left, top, cote):
    """Courbe douce (viewBox 1600 × 900) de la lumière du Hub vers l'attache d'une carte."""
    x0, y0 = HUB_LED[0] * 16, HUB_LED[1] * 9
    if cote == "gauche":
        x1, y1 = (left + 1.2) * 16, (top + VIE_H) * 9
    elif cote == "droite":
        x1, y1 = (left + VIE_W - 1.2) * 16, (top + VIE_H) * 9
    else:
        x1, y1 = (left + VIE_W * .6) * 16, (top + VIE_H * 2 - .6) * 9
    if cote == "bas":
        c1, c2 = (x0 - 160, y0 - 40), (x1 + 20, y1 + 170)
    else:
        dx = x1 - x0
        c1, c2 = (x0 + dx * .42, y0 - 30), (x1 - dx * .38, y1)
    return f"M{x0:.0f} {y0:.0f}C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {x1:.0f} {y1:.0f}"


def _scene():
    fils = "".join(
        f'<g class="hb-fil" data-fil="{k}"><path class="hb-fil-base" d="{_fil(*pos, cote)}"/>'
        f'<path class="hb-fil-halo" pathLength="1000" d="{_fil(*pos, cote)}"/>'
        f'<path class="hb-fil-lum" pathLength="1000" d="{_fil(*pos, cote)}"/></g>'
        for k, _, _, _, pos, cote in VIE)
    cartes = "".join(
        f'<li class="hb-vie" data-vie="{k}" style="--l:{pos[0]}%;--t:{pos[1]}%">'
        f'<span class="hb-vie-ic">{icon(ic)}</span><span class="hb-vie-tx"><small>{escape(chose)}</small>'
        f'<b>{escape(_insec(ph[0]))}</b></span><i class="hb-vie-ok" aria-hidden="true"></i></li>'
        for k, ic, chose, ph, pos, _ in VIE)
    return f"""
  <div class="hb-scene hb-frame" data-rev style="--led-x:{HUB_LED[0]}%;--led-y:{HUB_LED[1]}%;--halo-x:{HUB_HALO[0]}%;--halo-y:{HUB_HALO[1]}%">
    <div class="hb-sc-photo">
      <img src="{HUB_PHOTO}" width="1672" height="941" loading="lazy" decoding="async"
           alt="Le boîtier JARVIS Hub, posé sur un meuble dans un salon, sa petite lumière avant allumée">
      <span class="hb-sc-veil" aria-hidden="true"></span>
      <span class="hb-sc-halo" aria-hidden="true"></span>
      <span class="hb-sc-led" aria-hidden="true"></span>
      <svg class="hb-fils" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{fils}</svg>
      <p class="hb-sc-cap"><small>JARVIS Hub</small><b>En marche, en silence.</b><span>Installé et entretenu par nous.</span></p>
    </div>
    <ul class="hb-vies" aria-label="Ce que le Hub fait marcher (données d’exemple)">{cartes}</ul>
    <div class="hb-sc-bar">
      <span class="hb-live"><i></i>Données d’exemple</span>
      <p class="hb-offline" aria-live="polite" hidden>{icon("check")}<span><b>Internet est coupé.</b> Rien ne change chez vous : le Hub continue tout seul.</span></p>
      <button type="button" class="hb-net-btn" aria-pressed="false" hidden>{icon("cloud")}<span>Couper Internet</span></button>
    </div>
  </div>"""


# Un Hub par lieu, une seule app : clé, photo, lieu, sorte de Hub, état (données d'exemple).
LIEUX = [
    ("maison", "/media/vitrine/plateforme/penthouse-nuit.webp", "La maison", "Hub principal", "Tout est calme · 21 °C"),
    ("chalet", "/media/vitrine/plateforme/chalet-hiver.webp", "Le chalet", "Hub", "Chauffé pour vendredi"),
    ("garage", "/media/env/garage.webp", "Le garage de collection", "Hub", "Fermé, sous surveillance"),
    ("ferme", "/media/env/ferme.webp", "La ferme", "Hub", "Étables ventilées"),
    ("yacht", "/media/env/bateau.webp", "Le yacht", "Hub", "À quai, amarres surveillées"),
    ("vr", "/media/env/boulance.webp", "Le VR", "Hub compact · mobile", "En route vers le chalet"),
]

REPONSES = [
    ("Faut-il un ordinateur?", "Non.", "Le Hub est un petit boîtier silencieux, sans écran. Rien à gérer, aucune mise à jour à faire."),
    ("Et si Internet coupe?", "Tout continue.", "Chaque Hub fait marcher son lieu tout seul : portes, chauffage, lumières et règles restent en marche."),
    ("Combien de Hubs?", "Un par lieu.", "La maison a le Hub principal. Le chalet, le garage ou la ferme ont le leur; le VR, un Hub compact."),
    ("Qui s’en occupe?", "Nous.", "On l’installe, on l’entretient et on le met à jour pour vous. Vous gardez seulement l’application."),
]

# Les deux formats du Hub : photo du site, ou media/vitrine/plateforme/<nom>.webp quand James la fournit
# (sinon un panneau noir « Photo à venir », jamais un dessin).
_RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FORMATS = [
    ("hub-principal", HUB_PHOTO, "Hub principal", "Pour la maison, un domaine ou une entreprise. Il garde le système complet."),
    ("hub-compact", None, "Hub compact · mobile", "Pour le VR, un véhicule ou un bateau. Le même cœur, en plus petit."),
]


def _photo_format(nom, repli):
    fichier = f"/media/vitrine/plateforme/{nom}.webp"
    if os.path.exists(os.path.join(_RACINE, fichier.lstrip("/"))):
        return fichier
    return repli


def _lieux():
    def tuile(i, k, img, nom, sorte, etat):
        cote = "g" if i < 3 else "d"
        return (f'<li class="hb-lx-t is-{cote}" data-lieu="{k}">'
                f'<img src="{img}" alt="" loading="lazy" decoding="async">'
                f'<span class="hb-lx-hub"><i></i>{escape(sorte)}</span>'
                f'<span class="hb-lx-tx"><b>{escape(nom)}</b><small>{escape(etat)}</small></span></li>')
    gauche = "".join(tuile(i, *l) for i, l in enumerate(LIEUX[:3]))
    droite = "".join(tuile(i + 3, *l) for i, l in enumerate(LIEUX[3:]))
    rangs = "".join(
        f'<li data-rang="{k}"><img src="{img}" alt="" loading="lazy" decoding="async">'
        f'<span><b>{escape(nom)}</b><small>{escape(etat)}</small></span><i></i></li>'
        for k, img, nom, _, etat in LIEUX)
    reponses = "".join(
        f'<li data-rev><small>{escape(q)}</small><b>{escape(r)}</b><span>{escape(d)}</span></li>'
        for q, r, d in REPONSES)
    formats = []
    for nom, repli, titre, texte in FORMATS:
        src = _photo_format(nom, repli)
        vis = (f'<img src="{src}" alt="{escape(titre)}" loading="lazy" decoding="async">' if src else
               f'<span class="hb-fm-wait">{icon("hub")}<b>Photo à venir</b><small>{nom}.webp</small></span>')
        formats.append(f'<figure class="hb-fm{"" if src else " is-wait"}">{vis}'
                       f'<figcaption><b>{escape(titre)}</b><span>{escape(texte)}</span></figcaption></figure>')
    return f"""
  <div class="hb-lieux-head" data-rev>
    <p class="eyebrow">Plusieurs lieux?</p>
    <h3>Un Hub par lieu.<br><em>Une seule application.</em></h3>
    <p>Chaque lieu a son petit Hub, qui le fait marcher tout seul, même sans Internet. Vos Hubs se parlent
    par un lien privé et chiffré. Vous, vous ouvrez une seule application, avec tous vos lieux dedans.</p>
  </div>
  <div class="hb-lieux hb-frame" data-rev>
    <div class="hb-lx-body">
      <svg class="hb-lx-fils" aria-hidden="true"></svg>
      <ul class="hb-lx-col is-g">{gauche}</ul>
      <div class="hb-lx-tel" aria-label="L’application JARVIS : tous vos lieux (données d’exemple)">
        <div class="hb-tel-ecran">
          <p class="hb-tel-top"><b>Mes lieux</b><small>6 lieux · tout va bien</small></p>
          <ul class="hb-tel-rangs">{rangs}</ul>
          <p class="hb-tel-pied">{icon("lock")}Lien privé et chiffré</p>
        </div>
      </div>
      <ul class="hb-lx-col is-d">{droite}</ul>
    </div>
    <p class="hb-lx-note"><span class="hb-live"><i></i>Données d’exemple</span>
    <span>Bureau, hangar ou entrepôt : même principe, un Hub par lieu.</span></p>
  </div>
  <ul class="hb-reps">{reponses}</ul>
  <div class="hb-fms" data-rev>{"".join(formats)}</div>"""


# Pour les curieux : ce que le Hub héberge (en petit, plus bas).
HOSTED = [
    ("regles", "Règles", "Vos règles écrites une fois : seuils, horaires, qui approuve quoi."),
    ("comptes", "Comptes et droits", "Chaque personne et chaque extension n’a que les droits accordés."),
    ("journal", "Journal", "Chaque événement, décision et action, gardé sur place."),
    ("bus", "Bus d’événements", "Le fil où les extensions publient et s’écoutent."),
    ("iacore", "IA locale", "L’assistant de JARVIS, qui fonctionne sur le Hub."),
    ("sauve", "Sauvegardes", "Chiffrées, vérifiées, prêtes à restaurer."),
]


def coeur():
    hosted = "".join(
        f'<li>{icon(k)}<div><b>{n}</b><span>{d}</span></div></li>' for k, n, d in HOSTED)
    legend = "".join(_chip_ext(e[0]) for e in EXT)
    phrases = {k: [_insec(p) for p in ph] for k, _, _, ph, _, _ in VIE}
    return f"""
<div class="hb-coeur" data-demo="hub" data-hb="coeur">
  <div class="hb-coeur-head">
    <p class="eyebrow" data-rev>Le Hub · cœur de JARVIS</p>
    <h2 data-rev>Un petit boîtier, en silence.<br><em>Et toute la maison suit.</em></h2>
    <p class="hb-lead" data-rev>Le Hub est installé chez vous et entretenu par nous. Pas d’écran, rien à gérer :
    il fait marcher les portes, le chauffage, les lumières et les caméras, même quand Internet tombe.
    Vous, vous gardez seulement l’application.</p>
  </div>
  {_scene()}
  <div class="hb-coeur-facts" data-rev>
    <span>{icon("hub")}Silencieux, sans écran</span>
    <span>{icon("lock")}Fonctionne sans Internet</span>
    <span>{icon("tool")}Installé et entretenu par nous</span>
    <span>{icon("plus")}Sept extensions s’y branchent</span>
  </div>
  {_lieux()}
  <details class="hb-curieux" data-rev>
    <summary><span>Pour les curieux</span><b>Ce qu’il y a dans le Hub</b><i aria-hidden="true"></i></summary>
    <div class="hb-cu-b">
      <ul class="hb-hosted">{hosted}</ul>
      <div class="hb-cu-side">
        <p><b>Les sept extensions s’y branchent</b></p>
        <div class="hb-legend">{legend}</div>
        <p><b>Les appareils</b>Zigbee, Z-Wave, Matter, MQTT, Wi-Fi et réseau filaire : des marques différentes, un seul système.</p>
        <p><b>Les mises à jour</b>Signées, appliquées par nous, avec retour en arrière possible.</p>
        <p><b>Entre vos Hubs</b>Un réseau privé chiffré; rien n’est ouvert sur Internet.</p>
      </div>
    </div>
  </details>
  <script type="application/json" class="hb-data">{_js({"vie": phrases})}</script>
</div>"""


# ---------------------------------------------------------------------------
# 2. L'IA au cœur
# ---------------------------------------------------------------------------
TRAITS = [
    ("comprend", "Comprend le français de tous les jours", "Pas de commandes à apprendre : vous parlez ou écrivez normalement."),
    ("raisonne", "Raisonne entre les extensions", "Elle croise le lieu, les mesures, l’agenda et les personnes."),
    ("propose", "Propose des actions", "Un plan clair, étape par étape, prêt à appliquer."),
    ("confirme", "Demande votre confirmation", "Rien d’important ne se fait sans votre « Confirmer »."),
    ("explique", "Explique ses décisions", "Touchez « Pourquoi? » : elle montre ses raisons et ses sources."),
    ("apprend", "Apprend vos habitudes", "Vos réglages préférés deviennent ses propositions, jamais des ordres."),
    ("local", "Ne sort jamais vos données", "Elle fonctionne sur le Hub. Rien ne part sans votre permission."),
]

IA_SCENES = [
    {
        "id": "maison", "tab": "Maison", "sub": "Départ au chalet",
        "ask": "On part au chalet jusqu’à dimanche. Prépare la maison.",
        "intent": ["Absence", "Vendredi au dimanche", "Toute la maison"],
        "checks": [
            ("env", "Fenêtre du sous-sol ouverte; chauffage à 21 °C"),
            ("secu", "Alarme désarmée; deux caméras en ligne"),
            ("res", "Réseau stable; lien de secours prêt"),
            ("mob", "Départ prévu à 16 h 30, arrivée vers 18 h 40"),
        ],
        "plan": [
            "Passer en mode Absent au départ : chauffage à 17 °C",
            "Armer l’alarme dès que la voiture quitte l’entrée",
            "Allumer quelques lampes le soir, à des heures variées",
            "Vous rappeler de fermer la fenêtre du sous-sol",
        ],
        "why": "J’ai choisi 17 °C parce que c’est votre réglage pour les absences de plus d’une nuit, "
               "appris sur vos six derniers départs. La fenêtre n’est pas fermée à distance : elle n’a pas de moteur.",
        "learn": "Habitude apprise : 17 °C pour les absences",
        "log": "4 actions approuvées par vous · consignées au journal",
    },
    {
        "id": "ferme", "tab": "Ferme", "sub": "La nuit à l’étable",
        "ask": "Est-ce que l’étable 2 est correcte pour la nuit?",
        "intent": ["État de l’étable 2", "Cette nuit", "Ventilation et air"],
        "checks": [
            ("env", "Ammoniac à 14 ppm, température 9 °C, 4 ventilateurs sur 4 en marche"),
            ("diag", "Ventilateur 3 : courant en hausse de 18 % depuis mardi"),
            ("auto", "Technicien de garde cette nuit : poste 2, joignable"),
            ("ia", "Manuel du ventilateur : roulement à vérifier aux 2000 heures"),
        ],
        "plan": [
            "Surveiller le ventilateur 3 toutes les 5 minutes cette nuit",
            "Prévenir le technicien de garde si le courant dépasse 7 A",
            "Créer un bon de travail pour vérifier le roulement demain",
        ],
        "why": "Le courant du ventilateur 3 monte lentement, comme avant une usure de roulement. Le manuel prévoit "
               "une vérification aux 2000 heures; il en est à 2140. Rien n’est urgent, mais mieux vaut le voir demain.",
        "learn": "Habitude apprise : bons de travail créés le matin",
        "log": "3 actions approuvées par vous · consignées au journal",
    },
    {
        "id": "vr", "tab": "VR", "sub": "Nuit sans branchement",
        "ask": "J’ai assez de batterie pour passer la nuit ici sans me brancher?",
        "intent": ["Autonomie", "Cette nuit", "Sans borne électrique"],
        "checks": [
            ("env", "Batteries à 78 %, chauffage réglé à 19 °C"),
            ("diag", "Consommation de nuit habituelle : 41 % à 4 °C dehors"),
            ("mob", "Prévision de 3 °C cette nuit; camping avec borne à 12 km"),
        ],
        "plan": [
            "Rester ici : il restera environ 30 % au matin",
            "Baisser le chauffage à 17 °C de minuit à 6 h",
            "Couper l’onduleur du salon pendant la nuit",
        ],
        "why": "Vos nuits à cette température consomment 41 % en moyenne. Avec 17 °C la nuit et l’onduleur coupé, "
               "je prévois environ 30 % au réveil, au-dessus de votre minimum de 20 %.",
        "learn": "Habitude apprise : minimum de 20 % au réveil",
        "log": "2 actions approuvées par vous · consignées au journal",
    },
]


def _ia_scene_html(s):
    checks = "".join(
        f'<li style="--x:{EXT_BY[k][4]}">{icon(k)}<b>{EXT_BY[k][2]}</b><span>{escape(t)}</span><i>{icon("check")}</i></li>'
        for k, t in s["checks"])
    plan = "".join(f'<li><i>{n + 1}</i>{escape(p)}</li>' for n, p in enumerate(s["plan"]))
    intent = "".join(f'<span>{escape(t)}</span>' for t in s["intent"])
    return f"""
      <div class="hb-msg hb-msg-me" data-st="comprend"><p class="hb-ask">{escape(s["ask"])}</p></div>
      <div class="hb-step" data-st="comprend"><small>{icon("iacore")}Je comprends</small><div class="hb-intent">{intent}</div></div>
      <div class="hb-step" data-st="raisonne"><small>{icon("bus")}Je vérifie auprès des extensions</small><ul class="hb-checks">{checks}</ul></div>
      <div class="hb-step hb-plan" data-st="propose"><small>{icon("regles")}Je propose</small><ol>{plan}</ol>
        <div class="hb-plan-acts" data-st="confirme"><button type="button" class="hb-ok" tabindex="-1">Confirmer</button><button type="button" class="hb-mod" tabindex="-1">Modifier</button><button type="button" class="hb-why-b" tabindex="-1">Pourquoi?</button></div>
      </div>
      <div class="hb-step hb-why" data-st="explique"><small>{icon("ia")}Pourquoi</small><p>{escape(s["why"])}</p></div>
      <div class="hb-step hb-done" data-st="apprend"><span class="hb-learn">{icon("check")}{escape(s["learn"])}</span><span class="hb-log">{icon("journal")}{escape(s["log"])}</span></div>"""


def ia():
    tabs = "".join(
        f'<button type="button" role="tab" data-scene="{s["id"]}" aria-selected="{"true" if i == 0 else "false"}">'
        f'<b>{s["tab"]}</b><small>{s["sub"]}</small></button>' for i, s in enumerate(IA_SCENES))
    traits = "".join(
        f'<li data-trait="{k}"><i></i><div><b>{t}</b><span>{d}</span></div></li>' for k, t, d in TRAITS)
    scenes = {s["id"]: _ia_scene_html(s) for s in IA_SCENES}
    return f"""
<div class="hb-ia" data-demo="hub" data-hb="ia">
  <div class="hb-ia-copy">
    <ul class="hb-traits" data-rev>{traits}</ul>
  </div>
  <div class="hb-console hb-frame" data-rev>
    <div class="hb-con-top">
      <span class="hb-con-id">{icon("iacore")}<span><b>IA de JARVIS</b><small>Sur le Hub · en français</small></span></span>
      <span class="hb-con-zero"><i></i><b data-zero>0 octet</b> envoyé à l’extérieur</span>
    </div>
    <div class="hb-con-tabs" role="tablist" aria-label="Exemples de demandes" hidden>{tabs}</div>
    <div class="hb-con-body" aria-live="polite">{scenes[IA_SCENES[0]["id"]]}</div>
    <div class="hb-con-input"><span class="hb-con-mic">{icon("mic")}</span><span class="hb-con-ph">Parlez ou écrivez à JARVIS…</span><span class="hb-con-tag">Données d’exemple</span></div>
  </div>
  <div class="hb-two" data-rev>
    <article class="hb-two-c is-core">
      <small>Incluse dans chaque Hub</small>
      <h3>{icon("iacore")}L’IA de JARVIS</h3>
      <p>L’assistant qui fait tourner l’ensemble : il comprend vos demandes, interroge les extensions et prépare les actions que vous confirmez.</p>
    </article>
    <span class="hb-two-vs" aria-hidden="true">et</span>
    <article class="hb-two-c is-ext" style="--x:{EXT_BY["ia"][4]}">
      <small>Extension · au besoin</small>
      <h3>{icon("ia")}IA privée et connaissances</h3>
      <p>La mémoire documentaire : vos documents, manuels et contrats, interrogés avec la source de chaque réponse.
      Les autres extensions s’en servent aussi : Diagnostic y retrouve le manuel d’un appareil, Entreprise le contrat d’un client.</p>
    </article>
  </div>
  <script type="application/json" class="hb-data">{_js({"scenes": scenes})}</script>
</div>"""


# ---------------------------------------------------------------------------
# 3. Comment les extensions travaillent ensemble
# ---------------------------------------------------------------------------
CHAINS = [
    {
        "id": "ferme", "tab": "Ferme", "sub": "Air de l’étable 2, la nuit",
        "lieu": "Ferme laitière · étable 2 · 2 h 14 du matin",
        "steps": [
            {"x": "env", "t": "02 h 14", "h": "La sonde d’ammoniac dépasse le seuil",
             "p": "La sonde NH₃ de l’étable 2 mesure 28 ppm. Le seuil fixé par vos règles est de 20 ppm. "
                  "Environnements ne décide rien : il publie la mesure.",
             "ev": "Mesure hors seuil · étable 2", "to": ["diag"],
             "perm": "Diagnostic a le droit de lire les sondes de l’étable",
             "m": {"l": "Ammoniac", "v": "28 ppm", "s": "seuil 20 ppm", "f": 0.82, "st": "bad"}},
            {"x": "diag", "t": "02 h 15", "h": "Écart confirmé, ventilateur testé",
             "p": "Une deuxième sonde confirme l’écart. Diagnostic teste le ventilateur 3 : 0,4 A au lieu de 6,1 A. "
                  "Le moteur ne tourne plus; cause probable : le condensateur de démarrage.",
             "ev": "Test échoué · ventilateur 3", "to": ["auto", "ia"],
             "perm": "Diagnostic peut lancer un test, pas réparer",
             "m": {"l": "Courant du ventilateur 3", "v": "0,4 A", "s": "normal 6,1 A", "f": 0.07, "st": "bad"}},
            {"x": "auto", "t": "02 h 16", "h": "Bon de travail au technicien de garde",
             "p": "Entreprise crée le bon de travail et l’envoie au technicien de garde avec les mesures, le résultat du test, "
                  "le plan de l’étable et la pièce probable. Pas de réponse en 10 minutes : appel automatique à 2 h 26. "
                  "Accepté à 2 h 28.",
             "ev": "Bon de travail accepté", "to": ["secu"],
             "perm": "Entreprise peut joindre l’employé de garde",
             "m": {"l": "Délai avant l’appel", "v": "10 min", "s": "accepté à 2 h 28", "f": 1.0, "st": "warn"}},
            {"x": "secu", "t": "02 h 51", "h": "Arrivée du technicien, badgée",
             "p": "Le technicien badge à la porte nord. Sécurité lui ouvre l’étable 2 seulement, pour trois heures, "
                  "et consigne l’arrivée avec l’image de la caméra.",
             "ev": "Accès accordé · étable 2", "to": ["env"],
             "perm": "Accès limité à l’étable 2, jusqu’à 5 h 51",
             "m": {"l": "Accès temporaire", "v": "3 h", "s": "étable 2 seulement", "f": 0.6, "st": "ok"}},
            {"x": "diag", "t": "03 h 40", "h": "Retour à la normale mesuré, rapport",
             "p": "Ventilateur remplacé : 6,0 A. L’ammoniac redescend à 12 ppm en 25 minutes. Diagnostic confirme le "
                  "retour à la normale, joint le rapport au bon de travail; Entreprise ferme le bon.",
             "ev": "Retour à la normale", "to": ["auto", "ia"],
             "perm": "Le rapport est classé dans la mémoire documentaire",
             "m": {"l": "Ammoniac", "v": "12 ppm", "s": "seuil 20 ppm", "f": 0.35, "st": "ok"}},
        ],
    },
    {
        "id": "vr", "tab": "VR", "sub": "Cellule de batterie faible",
        "lieu": "Véhicule récréatif · autoroute 20 · 14 h 02",
        "steps": [
            {"x": "env", "t": "14 h 02", "h": "Une cellule de la batterie décroche",
             "p": "Le gestionnaire de batterie signale la cellule 3 à 3,02 V, alors que les trois autres sont à 3,31 V. "
                  "Environnements publie l’écart.",
             "ev": "Écart entre cellules · batterie de service", "to": ["diag"],
             "perm": "Diagnostic peut lire la batterie",
             "m": {"l": "Cellule 3", "v": "3,02 V", "s": "les autres 3,31 V", "f": 0.42, "st": "bad"}},
            {"x": "diag", "t": "14 h 03", "h": "Test sous charge : cellule défaillante",
             "p": "Sous une charge de 40 A, la cellule 3 chute à 2,88 V et sa résistance interne a triplé. "
                  "Autonomie prévue : 6 heures au lieu de 19.",
             "ev": "Cellule défaillante · autonomie réduite", "to": ["env", "mob"],
             "perm": "Diagnostic peut lancer un test de charge court",
             "m": {"l": "Autonomie prévue", "v": "6 h", "s": "normale 19 h", "f": 0.31, "st": "warn"}},
            {"x": "env", "t": "14 h 04", "h": "Délestage, confirmé par vous",
             "p": "L’IA propose de couper le chauffe-eau et l’onduleur du salon, en gardant le réfrigérateur et le chauffage. "
                  "Vous touchez « Confirmer » sur le téléphone; Environnements applique.",
             "ev": "Délestage appliqué", "to": ["diag"],
             "perm": "Couper un équipement demande votre confirmation",
             "m": {"l": "Consommation", "v": "180 W", "s": "avant 640 W", "f": 0.28, "st": "ok"}},
            {"x": "mob", "t": "14 h 05", "h": "Trajet modifié vers une borne",
             "p": "Mobilité trouve un camping avec une borne de 30 A à 38 km, ouvert jusqu’à 21 h, et met le trajet à jour. "
                  "Arrivée prévue à 14 h 41.",
             "ev": "Arrêt ajouté · borne 30 A", "to": ["env"],
             "perm": "Le trajet change seulement après votre accord",
             "m": {"l": "Distance de la borne", "v": "38 km", "s": "arrivée 14 h 41", "f": 0.5, "st": "ok"}},
            {"x": "diag", "t": "14 h 44", "h": "Branché : surveillance et dossier",
             "p": "La cellule est surveillée toutes les 10 secondes pendant la recharge. Diagnostic prépare le dossier pour le "
                  "garage : courbes, test de charge et pièce à commander.",
             "ev": "Dossier prêt · cellule à remplacer", "to": ["ia"],
             "perm": "Le dossier reste sur le Hub jusqu’à votre envoi",
             "m": {"l": "Recharge", "v": "62 %", "s": "cellule 3 surveillée", "f": 0.62, "st": "ok"}},
        ],
    },
    {
        "id": "maison", "tab": "Maison", "sub": "Fuite d’eau pendant la journée",
        "lieu": "Maison · sous-sol · 10 h 12, personne à la maison",
        "steps": [
            {"x": "env", "t": "10 h 12", "h": "De l’eau sous le chauffe-eau",
             "p": "Le détecteur sous le chauffe-eau signale de l’eau. Le compteur indique 4,2 L/min alors que personne n’est là.",
             "ev": "Eau détectée · sous-sol", "to": ["diag", "secu"],
             "perm": "Diagnostic peut lire le compteur d’eau",
             "m": {"l": "Débit", "v": "4,2 L/min", "s": "maison vide : 0", "f": 0.7, "st": "bad"}},
            {"x": "diag", "t": "10 h 13", "h": "Fuite confirmée au chauffe-eau",
             "p": "Débit continu depuis 6 minutes, aucun robinet ouvert, pression qui baisse : la fuite vient du chauffe-eau.",
             "ev": "Fuite confirmée", "to": ["env", "ia"],
             "perm": "Diagnostic conclut, il n’agit pas",
             "m": {"l": "Pression", "v": "38 psi", "s": "normale 55 psi", "f": 0.55, "st": "bad"}},
            {"x": "env", "t": "10 h 13", "h": "Valve principale fermée",
             "p": "Vous aviez approuvé cette règle à l’installation : en cas de fuite confirmée, fermer la valve principale "
                  "et couper le chauffe-eau. Débit : zéro. Vous recevez l’avis.",
             "ev": "Eau fermée · chauffe-eau coupé", "to": ["secu"],
             "perm": "Règle approuvée par vous le jour de l’installation",
             "m": {"l": "Débit", "v": "0 L/min", "s": "valve fermée", "f": 0.02, "st": "ok"}},
            {"x": "ia", "t": "10 h 15", "h": "Garantie et assurance retrouvées",
             "p": "La mémoire documentaire retrouve la facture du chauffe-eau (garantie de 10 ans, encore valide) "
                  "et votre police d’assurance. La déclaration est préparée avec les photos et les mesures.",
             "ev": "Déclaration prête", "to": ["auto"],
             "perm": "Rien n’est envoyé sans votre « Approuver »",
             "m": {"l": "Garantie", "v": "4 ans restants", "s": "sur 10 ans", "f": 0.4, "st": "ok"}},
            {"x": "secu", "t": "13 h 02", "h": "Le plombier entre avec un code temporaire",
             "p": "Code valide de 13 h à 15 h, porte de service seulement. La caméra de l’entrée consigne l’arrivée et le départ.",
             "ev": "Accès accordé · porte de service", "to": ["env"],
             "perm": "Accès limité à 2 heures, révoqué ensuite",
             "m": {"l": "Accès temporaire", "v": "2 h", "s": "porte de service", "f": 0.4, "st": "ok"}},
            {"x": "diag", "t": "15 h 40", "h": "Retour à la normale, 24 h de suivi",
             "p": "Eau rouverte, pression stable à 55 psi, aucun débit hors usage. Diagnostic surveille 24 heures puis ferme le dossier.",
             "ev": "Retour à la normale", "to": ["ia"],
             "perm": "Le rapport est classé avec la facture",
             "m": {"l": "Pression", "v": "55 psi", "s": "normale", "f": 1.0, "st": "ok"}},
        ],
    },
]


def _chain_rail(c):
    out = []
    for i, s in enumerate(c["steps"]):
        e = EXT_BY[s["x"]]
        on = ' class="is-on"' if i == 0 else ""
        out.append(f'<li data-i="{i}" style="--x:{e[4]}"{on}>'
                   f'<button type="button" tabindex="-1"><span class="hb-r-dot">{icon(s["x"])}</span>'
                   f'<span class="hb-r-tx"><small>{e[2]}</small><b>{escape(s["h"])}</b><em>{s["t"]}</em></span></button></li>')
    return "".join(out)


def _chain_detail(c, i):
    s = c["steps"][i]
    e = EXT_BY[s["x"]]
    m = s["m"]
    subs = "".join(_chip_ext(k) for k in s["to"])
    return (f'<div class="hb-d" style="--x:{e[4]}">'
            f'<p class="hb-d-k">Étape {i + 1} sur {len(c["steps"])} · {e[3]} · {s["t"]}</p>'
            f'<h4>{escape(s["h"])}</h4><p class="hb-d-p">{escape(s["p"])}</p>'
            f'<div class="hb-d-m is-{m["st"]}"><span><small>{escape(m["l"])}</small><b>{escape(m["v"])}</b><em>{escape(m["s"])}</em></span>'
            f'<i><u style="--f:{m["f"]}"></u></i></div>'
            f'<dl class="hb-d-flow"><div><dt>{icon("bus")}Publie sur le Hub</dt><dd>« {escape(s["ev"])} »</dd></div>'
            f'<div><dt>{icon("comptes")}Droit vérifié</dt><dd>{escape(s["perm"])}</dd></div>'
            f'<div><dt>{icon("plus")}Reçu par</dt><dd class="hb-d-subs">{subs}</dd></div></dl></div>')


ROLES_ORDER = ["env", "diag", "auto", "secu", "res", "ia", "mob"]


def ensemble():
    roles = "".join(
        f'<li style="--x:{EXT_BY[k][4]}" data-role="{k}"><span class="hb-ro-ic">{icon(k)}</span>'
        f'<div><b>{EXT_BY[k][2]}</b><p>{EXT_BY[k][5]}</p>'
        f'<small><em>Publie</em> {EXT_BY[k][6]}</small><small><em>Écoute</em> {EXT_BY[k][7]}</small></div></li>'
        for k in ROLES_ORDER) + (
        f'<li class="is-hub" style="--x:var(--gold-soft)"><span class="hb-ro-ic">{icon("hub")}</span>'
        '<div><b>Le Hub</b><p>Faire respecter les droits et garder la trace.</p>'
        '<small><em>Relaie</em> seulement les événements autorisés</small>'
        '<small><em>Consigne</em> chaque passage au journal</small></div></li>')
    tabs = "".join(
        f'<button type="button" role="tab" data-chain="{c["id"]}" aria-selected="{"true" if i == 0 else "false"}">'
        f'<b>{c["tab"]}</b><small>{c["sub"]}</small></button>' for i, c in enumerate(CHAINS))
    c0 = CHAINS[0]
    data = {
        c["id"]: {
            "lieu": c["lieu"],
            "rail": _chain_rail(c),
            "details": [_chain_detail(c, i) for i in range(len(c["steps"]))],
            "steps": [{"x": s["x"], "t": s["t"], "ev": s["ev"], "to": s["to"], "n": EXT_BY[s["x"]][2],
                       "c": EXT_BY[s["x"]][4]} for s in c["steps"]],
        } for c in CHAINS
    }
    return f"""
<div class="hb-ens" data-demo="hub" data-hb="ensemble">
  <ul class="hb-roles" data-rev>{roles}</ul>

  <div class="hb-rule" data-rev>
    <div class="hb-rule-s"><i>1</i><b>Chaque extension possède son domaine.</b><span>Elle seule lit ses capteurs et commande ses équipements.</span></div>
    <div class="hb-rule-s"><i>2</i><b>Elle publie ses événements sur le Hub.</b><span>« Mesure hors seuil », « test échoué », « accès accordé »…</span></div>
    <div class="hb-rule-s"><i>3</i><b>Les autres s’abonnent.</b><span>Chacune réagit dans son propre domaine, jamais dans celui d’une autre.</span></div>
    <div class="hb-rule-s is-hub"><i>{icon("hub")}</i><b>Le Hub applique les droits et consigne tout.</b><span>Un événement non autorisé ne passe pas. Chaque passage est au journal.</span></div>
  </div>

  <div class="hb-chain hb-frame" data-rev>
    <div class="hb-ch-top">
      <div class="hb-ch-tabs" role="tablist" aria-label="Chaînes d’exemple">{tabs}</div>
      <div class="hb-ch-ctl" hidden>
        <button type="button" class="hb-ch-prev" aria-label="Étape précédente">{icon("prev")}</button>
        <button type="button" class="hb-ch-play" aria-label="Pause">{icon("pause")}{icon("play")}</button>
        <button type="button" class="hb-ch-next" aria-label="Étape suivante">{icon("next")}</button>
      </div>
    </div>
    <p class="hb-ch-lieu"><span>Données d’exemple</span><b>{escape(c0["lieu"])}</b></p>
    <div class="hb-ch-bus"><span>{icon("bus")}Bus d’événements du Hub</span><i class="hb-ch-pulse"></i></div>
    <ol class="hb-ch-rail" style="--n:{len(c0["steps"])}">{_chain_rail(c0)}</ol>
    <div class="hb-ch-main">
      <div class="hb-ch-detail" aria-live="polite">{_chain_detail(c0, 0)}</div>
      <aside class="hb-ch-log"><p>{icon("journal")}Journal du Hub</p><ol></ol></aside>
    </div>
  </div>

  <div class="hb-answer" data-rev>
    <p class="eyebrow">Alors, diagnostic ou entreprise?</p>
    <h3><span style="--x:{EXT_BY["diag"][4]}">Diagnostic</span> décide <em>quoi</em> ne va pas.
    <span style="--x:{EXT_BY["auto"][4]}">Entreprise</span> décide <em>qui</em> agit, et fait le suivi.</h3>
    <p>À la ferme, le même problème passe par les deux, chacune dans son rôle. Sans l’extension Entreprise,
    l’alerte arrive simplement sur votre téléphone; avec elle, elle devient un bon de travail suivi jusqu’au bout.</p>
  </div>
  <script type="application/json" class="hb-data">{_js(data)}</script>
</div>"""


# ---------------------------------------------------------------------------
# 4. L'offre : ce que comprend le Hub et les services (affichés sur /offre/)
# ---------------------------------------------------------------------------
HUB_INCLUS = [
    ("hub", "Le boîtier JARVIS Hub", "Un par lieu, installé et configuré sur place. Tous vos lieux dans la même application."),
    ("regles", "JARVIS Core", "Règles, comptes et droits, journal et bus d’événements."),
    ("iacore", "L’IA de JARVIS", "L’assistant local, en français, sur le Hub."),
    ("comptes", "JARVIS App pour chaque compte", "Ordinateur, tablette et téléphone, selon les droits de chacun."),
    ("sauve", "Sauvegardes et mises à jour", "Sauvegardes chiffrées et mises à jour signées, avec retour en arrière."),
    ("lock", "L’essentiel sans Internet", "Les règles, l’IA, le journal et les extensions restent en marche sur place."),
]

SERVICES = [
    ("install", "Installation", [
        "Visite du lieu et inventaire de ce qui existe déjà",
        "Plan écrit : Hub, extensions, droits et règles",
        "Installation, câblage et configuration sur place",
        "Formation des personnes qui utiliseront JARVIS",
    ]),
    ("tool", "Entretien", [
        "Vérification de l’état du Hub et des sauvegardes",
        "Application des mises à jour signées",
        "Réglage des règles quand vos besoins changent",
        "Remplacement d’un équipement qui fait défaut",
    ]),
    ("soutien", "Soutien", [
        "Une personne qui connaît votre installation",
        "Aide à distance seulement avec votre permission",
        "Déplacement sur place quand c’est nécessaire",
        "Chaque intervention consignée au journal",
    ]),
]
