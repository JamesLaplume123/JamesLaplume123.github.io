# Démo « Hub + extensions » de la page JARVIS (/plateforme/).
# Quatre blocs, chacun autonome :
#   coeur()    Le Hub, cœur de JARVIS : ce qu'il héberge et les sept extensions branchées (SVG animé).
#   ia()       L'IA au cœur : une conversation qui comprend, vérifie, propose, demande, explique.
#   ensemble() Comment les extensions travaillent ensemble : rôles, règle du bus, trois chaînes de bout en bout.
# Données de l'offre (HUB_INCLUS, SERVICES) : source unique, affichées sur /offre/ (src/pages/offre.py).
# Sans JavaScript, chaque bloc montre un état complet et lisible; assets/demos/hub.js anime le reste.
# Toutes les situations sont des données d'exemple.

import json
import math
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
HOSTED = [
    ("regles", "Règles", "Vos règles écrites une fois : seuils, horaires, qui approuve quoi."),
    ("comptes", "Comptes et droits", "Chaque personne et chaque extension n’a que les droits accordés."),
    ("journal", "Journal", "Chaque événement, décision et action, gardé sur place."),
    ("bus", "Bus d’événements", "Le fil où les extensions publient et s’écoutent."),
    ("iacore", "IA locale", "L’assistant de JARVIS, qui fonctionne sur le Hub."),
    ("sauve", "Sauvegardes", "Chiffrées, vérifiées, prêtes à restaurer."),
]

# Événements joués par le diagramme : source, abonnés, texte, l'IA y participe ?
HUB_EVENTS = [
    ("env", ["secu"], "Fenêtre du sous-sol ouverte pendant l’absence", True),
    ("diag", ["auto"], "Test du ventilateur 3 échoué", True),
    ("secu", ["env"], "Arrivée badgée à la porte nord", False),
    ("mob", ["env"], "Arrivée au chalet dans 30 minutes", True),
    ("res", ["diag", "secu"], "Caméra du garage hors ligne", False),
    ("auto", ["ia"], "Bon de travail fermé, rapport joint", False),
    ("ia", ["diag"], "Manuel du ventilateur retrouvé", True),
]

C = 380  # centre du diagramme (viewBox 760)
R_EXT = 286
R_RING_IN, R_RING_OUT = 122, 156


def _pol(r, deg):
    a = math.radians(deg)
    return C + r * math.cos(a), C + r * math.sin(a)


def _arc(r, a0, a1):
    x0, y0 = _pol(r, a0)
    x1, y1 = _pol(r, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}"


def _hub_svg():
    out = ['<svg class="hb-svg" viewBox="0 0 760 760" role="img" '
           'aria-label="Le Hub au centre, ce qu’il héberge en anneau, et les sept extensions branchées autour">']
    out.append('<defs>'
               '<radialGradient id="hbCore" cx="50%" cy="38%" r="70%"><stop offset="0" stop-color="#2a2620"/>'
               '<stop offset=".55" stop-color="#121110"/><stop offset="1" stop-color="#050505"/></radialGradient>'
               '<radialGradient id="hbHalo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="var(--mode-glow)" stop-opacity=".30"/>'
               '<stop offset=".45" stop-color="var(--mode-glow)" stop-opacity=".08"/><stop offset="1" stop-color="var(--mode-glow)" stop-opacity="0"/></radialGradient>'
               '<linearGradient id="hbRim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff6dd"/>'
               '<stop offset=".5" stop-color="var(--gold-soft)"/><stop offset="1" stop-color="#7a6236"/></linearGradient>'
               '<filter id="hbGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/>'
               '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
               '</defs>')
    out.append(f'<circle class="hb-halo" cx="{C}" cy="{C}" r="330" fill="url(#hbHalo)"/>')
    # anneaux décoratifs
    out.append(f'<circle class="hb-orbit" cx="{C}" cy="{C}" r="{R_EXT}"/>')
    out.append(f'<circle class="hb-orbit hb-orbit-dash hb-spin" cx="{C}" cy="{C}" r="218"/>')
    out.append(f'<circle class="hb-orbit hb-orbit-fine hb-spin-r" cx="{C}" cy="{C}" r="352"/>')
    # Internet (optionnel)
    ix, iy = 84, 676
    ex, ey = _pol(R_RING_OUT + 6, 135)
    sx0, sy0 = ix + 24, iy - 20
    out.append(f'<g class="hb-net" data-net>'
               f'<path class="hb-net-line" d="M{sx0} {sy0}L{ex:.1f} {ey:.1f}"/>'
               f'<g class="hb-net-cut" transform="translate({(sx0 + ex) / 2:.1f} {(sy0 + ey) / 2:.1f})"><circle r="13"/><path d="M-5-5L5 5M5-5L-5 5"/></g>'
               f'<g transform="translate({ix - 20} {iy - 20})"><rect class="hb-net-box" width="44" height="44" rx="13"/>'
               f'<g transform="translate(10 10)" class="hb-net-ic">{ICONS["cloud"]}</g></g>'
               f'<text class="hb-t hb-t-net" x="{ix + 2}" y="{iy + 46}" text-anchor="middle">Internet</text>'
               f'<text class="hb-t hb-t-sub hb-t-net2" x="{ix + 2}" y="{iy + 61}" text-anchor="middle">optionnel</text></g>')
    # rayons et nœuds des extensions
    spokes, nodes = [], []
    n = len(EXT)
    for i, e in enumerate(EXT):
        k = e[0]
        deg = -90 + i * 360 / n
        x, y = _pol(R_EXT, deg)
        sx, sy = _pol(R_RING_OUT + 4, deg)
        spokes.append(f'<path class="hb-spoke" data-spoke="{k}" style="--x:{e[4]}" d="M{sx:.1f} {sy:.1f}L{x:.1f} {y:.1f}" '
                      f'data-a="{sx:.1f},{sy:.1f}" data-b="{x:.1f},{y:.1f}"/>')
        above = math.sin(math.radians(deg)) < -0.4
        ly = y - 46 if above else y + 52
        nodes.append(f'<g class="hb-node" data-node="{k}" style="--x:{e[4]}" transform="translate({x:.1f} {y:.1f})">'
                     f'<circle class="hb-node-glow" r="44"/><circle class="hb-node-bg" r="31"/>'
                     f'<g transform="translate(-12 -12)" class="hb-node-ic">{ICONS[k]}</g></g>'
                     f'<text class="hb-t hb-t-ext" x="{x:.1f}" y="{ly:.1f}" text-anchor="middle">{e[2]}</text>')
    out.append('<g class="hb-spokes">' + "".join(spokes) + '</g>')
    # anneau de ce que le Hub héberge : six segments
    segs = []
    step = 60
    for i, (ik, name, _) in enumerate(HOSTED):
        a0 = -150 + i * step + 2.2
        a1 = a0 + step - 4.4
        mid = (a0 + a1) / 2
        path = _arc((R_RING_IN + R_RING_OUT) / 2, a0, a1)
        bottom = 10 < (mid % 360) < 170
        rm = (R_RING_IN + R_RING_OUT) / 2
        tp = _arc(rm, a1, a0) if bottom else _arc(rm, a0, a1)
        segs.append(f'<g class="hb-seg" data-seg="{ik}"><path class="hb-seg-band" d="{path}"/>'
                    f'<path id="hbTp{i}" class="hb-seg-tp" d="{tp}"/>'
                    f'<text class="hb-t hb-t-seg" dy="3.4"><textPath href="#hbTp{i}" startOffset="50%" text-anchor="middle">{escape(name.upper())}</textPath></text></g>')
    out.append('<g class="hb-ring">' + "".join(segs) + '</g>')
    # le cœur
    out.append(f'<g class="hb-core" transform="translate({C} {C})">'
               f'<circle class="hb-core-ring hb-spin" r="108"/>'
               f'<circle class="hb-core-bg" r="96" fill="url(#hbCore)"/>'
               f'<circle class="hb-core-rim" r="96" stroke="url(#hbRim)"/>'
               f'<circle class="hb-core-pulse" r="96"/>'
               f'<g class="hb-core-ic" transform="translate(-15 -62) scale(1.25)">{ICONS["hub"]}</g>'
               f'<text class="hb-core-t" y="10" text-anchor="middle">JARVIS</text>'
               f'<text class="hb-core-s" y="34" text-anchor="middle">HUB · SUR PLACE</text>'
               f'<g class="hb-core-live" transform="translate(-34 52)"><circle cx="6" cy="0" r="3.4"/>'
               f'<text x="15" y="4">EN MARCHE</text></g></g>')
    out.append('<g class="hb-nodes">' + "".join(nodes) + '</g>')
    out.append('<g class="hb-pk"></g></svg>')
    return "".join(out)


def coeur():
    hosted = "".join(
        f'<li data-host="{k}">{icon(k)}<div><b>{n}</b><span>{d}</span></div></li>' for k, n, d in HOSTED)
    legend = "".join(_chip_ext(e[0]) for e in EXT)
    data = [{"src": s, "to": t, "txt": x, "ia": a} for s, t, x, a in HUB_EVENTS]
    names = {e[0]: e[2] for e in EXT}
    return f"""
<div class="hb-coeur" data-demo="hub" data-hb="coeur">
  <div class="hb-stage hb-frame" data-rev>
    <div class="hb-stage-top">
      <span class="hb-live"><i></i>Hub en marche · données d’exemple</span>
      <button type="button" class="hb-net-btn" aria-pressed="false" hidden>{icon("cloud")}<span>Couper Internet</span></button>
    </div>
    {_hub_svg()}
    <div class="hb-legend">{legend}</div>
    <p class="hb-ticker" aria-live="polite"><span class="hb-tk-ic">{icon("bus")}</span><span class="hb-tk-txt"><b>Environnements</b> publie « Fenêtre du sous-sol ouverte pendant l’absence » · droits vérifiés · consigné au journal · reçu par <b>Sécurité</b></span></p>
    <p class="hb-offline" hidden>{icon("check")}<span><b>Internet est coupé.</b> Les règles, l’IA, le journal et les sept extensions continuent sur place.</span></p>
  </div>
  <div class="hb-coeur-copy">
    <p class="eyebrow" data-rev>Le Hub · cœur de JARVIS</p>
    <h2 data-rev>Un boîtier chez vous.<br><em>Tout le système dedans.</em></h2>
    <p class="hb-lead" data-rev>Le Hub est installé sur place, dans la maison, l’entreprise, la ferme ou le véhicule.
    Il fait tourner JARVIS au complet, sans dépendre du nuage : Internet sert seulement quand vous l’autorisez.</p>
    <ul class="hb-hosted" data-rev>{hosted}</ul>
    <div class="hb-coeur-facts" data-rev>
      <span>{icon("lock")}Fonctionne sans Internet</span>
      <span>{icon("check")}Mises à jour signées</span>
      <span>{icon("plus")}Sept extensions s’y branchent</span>
    </div>
  </div>
  <figure class="hb-photo" data-rev>
    <img src="/media/product/jarvis-hub-v1.webp" width="1672" height="941" loading="lazy"
         alt="JARVIS Hub intégré dans une résidence haut de gamme">
    <figcaption><small>Le boîtier sur place</small><b>Dimensionné selon le lieu, installé par nous.</b>
    <span>Une maison, une étable ou un VR : le même cœur, à la taille du besoin.</span></figcaption>
  </figure>
  <script type="application/json" class="hb-data">{_js({"events": data, "names": names})}</script>
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
    ("hub", "Le boîtier JARVIS Hub", "Dimensionné pour le lieu, installé et configuré sur place."),
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
