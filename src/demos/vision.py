# Page Vision — le manifeste de JARVIS (assets/demos/vision.css et .js).
# Cinq blocs : manifeste, horizons, firme de sécurité privée, partenariats, principes.
# Les horizons sont une vision montrée avec des données d'exemple; l'état réel vit dans
# feuille.py. La journée type et « tous vos lieux » vivent sur la page Environnements
# intelligents; Rust et la recherche, sur /plateforme/#rust et /recherche/.
#
# Photos : chaque emplacement prend media/vision/<nom>.webp dès que le fichier existe au
# build (déposer le fichier, reconstruire, aucun changement de code); sinon un panneau noir
# « Photo à venir ». Liste complète : PHOTOS_ATTENDUES (nom, description, priorité, format).

import os
import re
from html import escape

from demos.hub import EXT, ICONS as _HUB_ICONS

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
NBSP = " "
PHOTOS_ATTENDUES = []  # (fichier, description)


def fr(s):
    """Typographie française : espaces insécables avant : ; ? ! » et dans les nombres."""
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) (h|min|km|ans|mois|%|\$)", rf"\1{NBSP}\2", s)
    s = re.sub(r"\s+([:;?!»])", rf"{NBSP}\1", s)
    return s.replace("« ", "«" + NBSP)


# ---------------------------------------------------------------------------
# Icônes (traits, 24 × 24) : celles du Hub, plus quelques-unes propres à la vision
# ---------------------------------------------------------------------------
ICONS = dict(_HUB_ICONS)
ICONS.update({
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/>',
    "moon": '<path d="M19.5 14.6A8 8 0 0 1 9.4 4.5a8 8 0 1 0 10.1 10.1z"/>',
    "anchor": '<circle cx="12" cy="5.2" r="2"/><path d="M12 7.2v13.3"/><path d="M8.5 11h7"/><path d="M4.5 13.5c0 3.9 3.4 7 7.5 7s7.5-3.1 7.5-7"/>',
    "plane": '<path d="M10.5 20.5l1.5-.8 1.5.8v-2.3l-1-1v-4.4l7.5 3v-2.2l-7.5-5V4.5a1 1 0 0 0-2 0v4.1l-7.5 5v2.2l7.5-3v4.4l-1 1z"/>',
    "car": '<path d="M3.5 15.5v-3.2l2.2-4.4c.3-.6.9-1 1.6-1h9.4c.7 0 1.3.4 1.6 1l2.2 4.4v3.2c0 .6-.4 1-1 1h-1"/><path d="M8.5 16.5h7"/><circle cx="6.5" cy="16.5" r="1.8"/><circle cx="17.5" cy="16.5" r="1.8"/><path d="M3.5 12.3h17"/>',
    "build": '<path d="M4 20.5V6.5l7-3v17"/><path d="M11 9.5h9v11"/><path d="M3 20.5h18"/><path d="M7 9h1M7 12.5h1M7 16h1M14.5 13h1.5M14.5 16.5h1.5"/>',
    "key": '<circle cx="8" cy="15" r="4.2"/><path d="M11 12l8.5-8.5M16.5 6.5l2.5 2.5M14 9l2 2"/>',
    "eye": '<path d="M2.5 12s3.5-6.5 9.5-6.5S21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/>',
    "hand": '<path d="M8 11.5V5.8a1.4 1.4 0 0 1 2.8 0v5"/><path d="M10.8 10.5V4.4a1.4 1.4 0 0 1 2.8 0v6.1"/><path d="M13.6 10.6V5.6a1.4 1.4 0 0 1 2.8 0v6.6"/><path d="M16.4 9.4a1.4 1.4 0 0 1 2.8 0v4.8c0 3.7-2.8 6.6-6.5 6.6h-.6c-2 0-3.6-.9-4.8-2.5L4.8 14a1.5 1.5 0 0 1 2.3-1.9l.9 1"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2.8v3.2M15 2.8v3.2M9 18v3.2M15 18v3.2M2.8 9h3.2M2.8 15h3.2M18 9h3.2M18 15h3.2"/><path d="M10 10h4v4h-4z"/>',
    "code": '<path d="M8.5 7.5L4 12l4.5 4.5M15.5 7.5L20 12l-4.5 4.5M13.5 5l-3 14"/>',
    "people": '<circle cx="8.5" cy="8" r="3"/><circle cx="16.5" cy="9" r="2.5"/><path d="M3 19.5c.5-3.1 2.7-5 5.5-5s5 1.9 5.5 5"/><path d="M14.5 14.8c.6-.2 1.3-.3 2-.3 2.4 0 4.2 1.6 4.6 4.6"/>',
    "scale": '<path d="M12 4v16.5M7.5 20.5h9"/><path d="M4.5 7.5h15"/><path d="M6.5 7.5l-3 6.5a3 3 0 0 0 6 0zM17.5 7.5l-3 6.5a3 3 0 0 0 6 0z"/>',
    "nosell": '<circle cx="12" cy="12" r="8.5"/><path d="M6 6l12 12"/><path d="M14.2 9.3c-.5-.8-1.3-1.2-2.3-1.2-1.4 0-2.4.8-2.4 1.9 0 2.6 5 1.4 5 4 0 1.1-1.1 1.9-2.6 1.9-1.1 0-2-.5-2.5-1.3M12 6.8v1.3M12 15.9v1.3"/>',
    "home": '<path d="M3.5 11.2L12 4l8.5 7.2"/><path d="M5.8 9.6V20h12.4V9.6"/><path d="M10 20v-5.2h4V20"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.9l-5.2 2.8 1-5.9-4.3-4.1 5.9-.8z"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4.5h12l-2.5 4 2.5 4H5"/>',
    "wave": '<path d="M3 15c2 0 2-1.5 4.5-1.5S9.5 15 12 15s2.5-1.5 4.5-1.5S19 15 21 15"/><path d="M3 19c2 0 2-1.5 4.5-1.5S9.5 19 12 19s2.5-1.5 4.5-1.5S19 19 21 19"/><path d="M8 11l4-7 4 7"/>',
})


def icon(name, cls="vn-i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


# « hub » s'ajoute aux sept extensions pour les filtres et les jalons
SOL = {"hub": ("hub", "", "Hub", "JARVIS Hub et logiciel", "#e9c98c")}
SOL.update({e[0]: e for e in EXT})
SOL_ORDER = ["hub"] + [e[0] for e in EXT]


def chip(k):
    e = SOL[k]
    return f'<span class="vn-x" style="--x:{e[4]}">{icon(k)}<b>{e[2]}</b></span>'


# ---------------------------------------------------------------------------
# Photos
# ---------------------------------------------------------------------------
def photo(nom, alt, description, priorite, fmt="16:9", repli=None, pos="50% 50%", cls=""):
    """media/vision/<nom>.webp s'il existe au build; sinon la photo réelle de repli si elle
    existe; sinon le panneau noir « Photo à venir » (jamais un dessin)."""
    PHOTOS_ATTENDUES.append(("media/vision/" + nom + ".webp", description, priorite, fmt))
    src = None
    if os.path.exists(os.path.join(_ROOT, "media", "vision", nom + ".webp")):
        src = "/media/vision/" + nom + ".webp"
    elif repli and os.path.exists(os.path.join(_ROOT, repli.lstrip("/"))):
        src = repli
    if src:
        return (f'<figure class="vn-ph {cls}"><img loading="lazy" decoding="async" src="{src}" '
                f'alt="{escape(alt)}" style="object-position:{pos}"></figure>')
    return (f'<figure class="vn-ph is-wait {cls}" role="img" aria-label="{escape(alt)}">'
            f'<span class="vn-ph-frame" aria-hidden="true"></span>'
            f'<span class="vn-ph-b">{icon("star", "vn-i vn-ph-i")}<small>Photo à venir</small>'
            f'<em>{escape(alt)}</em></span></figure>')


# ---------------------------------------------------------------------------
# 1. Manifeste
# ---------------------------------------------------------------------------
LIBERTES = [
    ("Libre de son temps", "sun",
     "Les petites tâches, les vérifications et les oublis passent à JARVIS. Les heures rendues "
     "reviennent à la famille, au travail qui compte, au repos."),
    ("Libre de ses données", "lock",
     "Tout vit sur le Hub, chez vous. Aucune donnée vendue, aucun profil publicitaire, aucune "
     "dépendance à un nuage que vous n’avez pas choisi."),
    ("Libre de ses choix", "hand",
     "JARVIS observe, explique et propose. La décision vous revient toujours : rien de sensible ne "
     "se fait sans votre « Approuver »."),
]

PILIERS = [
    ("Privé", "Installé chez vous, sur votre Hub."),
    ("Relié", "Sept extensions qui se parlent."),
    ("Humain", "Vous décidez, JARVIS exécute."),
    ("Prouvé", "Chaque étape vérifiée à l’écran."),
]


def manifeste():
    libs = "".join(
        f'<article class="vn-card vn-lib" data-rev><span class="vn-lib-i">{icon(i)}</span>'
        f'<h3>{t}</h3><p>{fr(p)}</p></article>'
        for t, i, p in LIBERTES
    )
    pils = "".join(
        f'<li><b>{t}</b><span>{fr(p)}</span></li>' for t, p in PILIERS
    )
    return f"""<div class="vn" data-demo="vision">
  <div class="vn-mani">
    <div class="vn-mani-txt" data-rev>
      <p class="vn-kick">Le manifeste</p>
      <p class="vn-big">La technologie devrait vous rendre <em>du temps</em>, pas vous en prendre.</p>
      <p class="vn-lead">{fr("Aujourd’hui, chaque maison, chaque voiture et chaque entreprise accumule des applications, des alertes et des mots de passe. Chacune réclame un peu d’attention. Ensemble, elles en réclament beaucoup trop. JARVIS fait l’inverse : un seul système privé qui comprend vos lieux, relie vos outils et s’occupe de ce qui peut l’être, pour que vous soyez libre de vivre le reste.")}</p>
      <ul class="vn-pils">{pils}</ul>
    </div>
    <div class="vn-mani-ph vn-framed" data-rev>
      {photo("vision-liberte", "Un matin calme : la maison s’occupe d’elle-même",
             "Matin calme dans une résidence moderne québécoise : une personne boit son café face à une grande fenêtre sur un lac au lever du soleil, téléphone posé, maison silencieuse et lumière dorée naturelle",
             1, "4:5", pos="50% 45%")}
      <div class="vn-mani-tag"><i></i>Ce que JARVIS vise : moins d’écrans, plus de vie</div>
    </div>
  </div>
  <div class="vn-libs">{libs}</div>
</div>"""


# ---------------------------------------------------------------------------
# 2. Horizons : maintenant, 12 mois, 3 ans, 10 ans
# ---------------------------------------------------------------------------
HORIZONS = [
    {
        "k": "maintenant", "t": "Maintenant", "s": "Bâtir les fondations",
        "h": "Un logiciel solide, prouvé sur un vrai véhicule.",
        "p": "Le noyau, les comptes et les interfaces se construisent une étape à la fois, avec des "
             "vérifications automatiques à chaque changement. Le laboratoire mobile sert de terrain réel.",
        "photo": ("horizon-maintenant", "Le Hub JARVIS sur l’établi du laboratoire mobile",
                  "Gros plan sur un petit boîtier Hub noir et doré posé sur un établi propre à l’intérieur d’une ambulance convertie, câbles bien rangés, écran du tableau allumé en arrière-plan, éclairage chaud",
                  2, "16:10", "/media/ambulance/ambulance-garage-lab-v1.webp"),
        "j": [
            ("hub", "Étape 1 en cours : premier démarrage, compte propriétaire, invitations, rôles, journal et coffre des secrets."),
            ("env", "L’ancien JARVIS garde déjà les lumières du laboratoire mobile sur Home Assistant."),
            ("mob", "Le laboratoire mobile roule : 560 Ah de batteries et 500 W solaires mesurés en vrai."),
            ("diag", "Les mesures réelles des batteries servent déjà à repérer les écarts."),
            ("ia", "Démonstration interactive : questions sur vos documents, avec la source affichée."),
            ("secu", "Démonstration interactive : caméras et accès réunis dans un seul fil."),
            ("auto", "Entrevues avec des entreprises pour écrire l’extension Entreprise."),
            ("res", "Démonstration interactive : la carte du réseau en mots simples."),
        ],
    },
    {
        "k": "12mois", "t": "12 mois", "s": "Le premier JARVIS en service",
        "h": "Le logiciel complet, installé, audité, prêt pour les premiers clients.",
        "p": "Les quatorze étapes du logiciel terminées, la mise en service sur le Hub du laboratoire "
             "mobile, quatorze jours d’essai en parallèle, puis une revue de sécurité externe avant toute vente.",
        "photo": ("horizon-12-mois", "Une résidence québécoise équipée de JARVIS, au crépuscule",
                  "Maison moderne québécoise au crépuscule, grandes fenêtres éclairées de lumière chaude, neige légère, un écran mural JARVIS visible dans l’entrée, ambiance accueillante et haut de gamme",
                  2, "16:10", "/media/solutions/environnements-intelligents.webp"),
        "j": [
            ("hub", "Mises à jour signées avec retour en arrière, sauvegardes chiffrées dont la restauration est prouvée."),
            ("env", "Appareils, éclairage et tableau du véhicule sur le nouveau logiciel, mis à jour en moins d’une seconde."),
            ("ia", "Assistant local par défaut : rien ne part vers un fournisseur externe sans accord."),
            ("secu", "Test d’intrusion externe et obligations de la Loi 25 complétées avant la vente."),
            ("auto", "Extension Entreprise définie avec James, d’après les entrevues."),
            ("res", "Accès à distance par un relais qui ne garde rien."),
            ("diag", "Erreurs, diagnostic et maintenance du Hub visibles en mots simples."),
            ("mob", "Le tableau du laboratoire mobile : énergie, eau, confort et voyage."),
        ],
    },
    {
        "k": "3ans", "t": "3 ans", "s": "Sept extensions, une firme",
        "h": "Des maisons, des entreprises et des véhicules reliés, partout au Québec.",
        "p": "Chaque extension devient un chantier complet, prouvé chez de vrais clients. La firme de "
             "sécurité privée obtient ses permis et réalise ses premières missions autorisées.",
        "photo": ("horizon-3-ans", "Une entreprise québécoise qui fonctionne avec JARVIS",
                  "Atelier ou bureau de PME moderne au Québec, équipe au travail, grand écran mural sombre affichant un tableau de bord noir et or, lumière naturelle, ambiance calme et professionnelle",
                  3, "16:10", "/media/solutions/jarvis-enterprise-operations-v1.webp"),
        "j": [
            ("hub", "Plusieurs Hubs reliés : maison, chalet, entreprise et véhicule sous un même compte."),
            ("env", "Ambiances apprises avec vous, énergie optimisée selon le tarif et la météo."),
            ("ia", "Mémoire documentaire de la famille ou de l’entreprise, toujours sur place."),
            ("secu", "Firme de sécurité privée : permis, assurance et premières missions sous mandat écrit."),
            ("auto", "Réception téléphonique, bons de travail et approbations chez les premières PME."),
            ("res", "Surveillance réseau assistée pour maisons connectées et petits multi-sites."),
            ("diag", "Dossiers prêts pour le technicien, partagés avec les partenaires de service."),
            ("mob", "Copilote de route pour VR, voitures électriques et vélos électriques."),
        ],
    },
    {
        "k": "10ans", "t": "10 ans", "s": "Le système privé de référence",
        "h": "Un seul JARVIS pour une vie entière, de la maison au yacht.",
        "p": "Des résidences de prestige, des collections automobiles, des yachts et des jets coordonnés "
             "par un même système privé. Un Hub conçu sur mesure, une IA locale qui tourne entièrement chez vous.",
        "photo": ("horizon-10-ans", "Résidence de prestige, yacht et jet coordonnés par JARVIS",
                  "Vue aérienne au coucher du soleil d’une résidence de prestige au bord de l’eau, un yacht à son quai privé et, au loin, un jet d’affaires sur une piste; tons dorés, ambiance cinématographique, aucune marque visible",
                  1, "16:10", None),
        "j": [
            ("hub", "Hub JARVIS conçu sur mesure : matériel maison, silencieux, réparable, garanti."),
            ("env", "Résidences de prestige, chalets et ateliers : chaque lieu avec ses propres règles."),
            ("ia", "IA locale entraînée pour le français du Québec, sans aucun appel au nuage."),
            ("secu", "Une firme reconnue : protection de résidences, d’événements et de collections."),
            ("auto", "Gestion complète d’une maison de famille : personnel, fournisseurs, horaires."),
            ("res", "Réseaux privés entre les lieux, la mer et les airs, avec liens de secours."),
            ("diag", "Entretien prévu avant la panne, pour le bâtiment, la voiture, le bateau et l’avion."),
            ("mob", "Voitures de collection, yacht et jet préparés avant votre arrivée."),
        ],
    },
]


def horizons():
    tabs = "".join(
        f'<button type="button" class="vn-hz-tab{" is-on" if i == 0 else ""}" role="tab" '
        f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="vn-hz-{h["k"]}" id="vn-hzt-{h["k"]}" data-hz="{i}">'
        f'<i aria-hidden="true"></i><b>{h["t"]}</b><span>{h["s"]}</span></button>'
        for i, h in enumerate(HORIZONS)
    )
    panels = []
    for i, h in enumerate(HORIZONS):
        nom, alt, desc, prio, fmt, repli = h["photo"]
        jal = "".join(
            f'<li style="--x:{SOL[k][4]}">{chip(k)}<p>{fr(t)}</p></li>' for k, t in h["j"]
        )
        state = "Réel · en cours" if i == 0 else "Objectif"
        panels.append(f"""<div class="vn-hz-panel{' is-on' if i == 0 else ''}" role="tabpanel" id="vn-hz-{h['k']}" aria-labelledby="vn-hzt-{h['k']}"{'' if i == 0 else ' hidden'}>
      <div class="vn-hz-top">
        {photo(nom, alt, desc, prio, fmt, repli, cls="vn-hz-ph")}
        <div class="vn-hz-txt">
          <span class="vn-state{' is-now' if i == 0 else ''}">{state}</span>
          <p class="vn-hz-n">{h['t']}</p>
          <h3>{fr(h['h'])}</h3>
          <p>{fr(h['p'])}</p>
        </div>
      </div>
      <ul class="vn-hz-j">{jal}</ul>
    </div>""")
    return f"""<div class="vn vn-hz vn-framed" data-demo="vision" data-vn="horizons" data-rev>
  <div class="vn-hz-rail" role="tablist" aria-label="Horizons">{tabs}<span class="vn-hz-line" aria-hidden="true"><i></i></span></div>
  {''.join(panels)}
  <p class="vn-note">Horizons visés, jamais des promesses de date : chaque étape avance seulement quand la précédente est prouvée à l’écran.</p>
</div>"""


# ---------------------------------------------------------------------------
# 3. Firme de sécurité privée (introduction, avant la démonstration Security Pro)
# ---------------------------------------------------------------------------
FIRME = [
    ("Tests d’intrusion", "key", "Attaquer vos systèmes avant les autres, sous mandat écrit, et prouver chaque faille."),
    ("Protection de résidences", "home", "Rondes, accès temporaires et surveillance des propriétés de prestige et des collections."),
    ("Enquêtes et OSINT", "eye", "Retrouver ce que l’on sait de vous en ligne, et le réduire."),
    ("Conformité Loi 25", "scale", "Registre, évaluation des facteurs relatifs à la vie privée, politiques et formation."),
    ("Réponse aux incidents", "flag", "Contenir, préserver les preuves, remettre en service et expliquer."),
    ("Soutien aux forces de l’ordre", "people", "Preuves hachées et chaîne de possession prêtes à transmettre, sur demande légale."),
]


def firme():
    lines = "".join(
        f'<li><span class="vn-fi-i">{icon(i)}</span><div><b>{t}</b><p>{fr(p)}</p></div></li>'
        for t, i, p in FIRME
    )
    return f"""<div class="vn vn-fi" data-demo="vision">
  <div class="vn-fi-ph vn-framed" data-rev>
    {photo("securite-centre", "Le centre des opérations de la firme de sécurité JARVIS",
           "Centre des opérations de sécurité privé, pièce sombre, mur d’écrans noirs avec cartes et flux de caméras en tons or, deux analystes de dos, ambiance calme et professionnelle, aucun logo",
           1, "16:10")}
    <div class="vn-fi-badge"><span>{icon("secu")}</span><div><b>Mandat d’abord</b><small>L’IA accélère · un professionnel valide · tout est journalisé</small></div></div>
  </div>
  <ul class="vn-fi-l" data-rev>{lines}</ul>
</div>"""


# ---------------------------------------------------------------------------
# 4. Partenariats
# ---------------------------------------------------------------------------
PARTENAIRES = [
    ("Installateurs et électriciens", "tool", "Poser le Hub, les capteurs et le câblage selon les règles de l’art."),
    ("Intégrateurs audio-vidéo", "eye", "Salles de cinéma, éclairage architectural et résidences de prestige."),
    ("Concessionnaires et ateliers", "car", "Entretien prévu des voitures de collection et des véhicules électriques."),
    ("Marinas et aviation d’affaires", "anchor", "Préparer le bateau et le vol à partir d’un seul message."),
    ("Assureurs", "secu", "Moins de dégâts d’eau, moins de vols, et la preuve que la protection fonctionne."),
    ("Universités et chercheurs", "iacore", "IA locale, sécurité et vie privée : recherche ouverte et publiée."),
]


def partenaires():
    cards = "".join(
        f'<li data-rev><span class="vn-pa-i">{icon(i)}</span><b>{t}</b><p>{fr(p)}</p></li>'
        for t, i, p in PARTENAIRES
    )
    return f"""<div class="vn vn-pa vn-framed" data-demo="vision" data-rev>
  <ul class="vn-pa-l">{cards}</ul>
  <p class="vn-pa-n">{icon("lock")}Chaque partenaire reçoit seulement ce que vous autorisez, pour une durée limitée, et chaque accès est journalisé.</p>
</div>"""


# ---------------------------------------------------------------------------
# 5. Principes
# ---------------------------------------------------------------------------
PRINCIPES = [
    ("01", "nosell", "Aucune donnée vendue", "Jamais. Ni vendue, ni louée, ni échangée, ni utilisée pour de la publicité."),
    ("02", "home", "Chez vous d’abord", "Tout vit sur le Hub. Le nuage ne sert qu’à ce que vous choisissez : relais d’accès, copie chiffrée."),
    ("03", "scale", "Loi 25, dès la conception", "Consentement clair, finalité précise, conservation limitée, export et suppression à la demande."),
    ("04", "hand", "Vous avez le dernier mot", "Déverrouiller, ouvrir, payer, partager : rien de sensible sans votre confirmation."),
    ("05", "journal", "Tout est tracé", "Un journal clair de chaque accès et de chaque action, consultable en tout temps."),
    ("06", "check", "Prouvé avant d’être vendu", "Chaque étape vérifiée à l’écran, puis une revue de sécurité externe avant toute vente."),
]


def principes():
    cards = "".join(
        f'<article class="vn-card vn-pr" data-rev><p class="vn-pr-n">{n}</p><span class="vn-pr-i">{icon(i)}</span>'
        f'<h3>{t}</h3><p>{fr(p)}</p></article>'
        for n, i, t, p in PRINCIPES
    )
    return f'<div class="vn vn-prs" data-demo="vision">{cards}</div>'
