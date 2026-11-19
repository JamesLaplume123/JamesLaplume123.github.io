# Les lieux du client : source unique (décision de James, novembre 2026).
# Les gens pensent « j'ai une ferme », pas « je veux Diagnostic & continuité ». Pour chaque lieu :
# les solutions qui comptent (une raison d'une ligne chacune), la démonstration à ouvrir, l'appareil
# conseillé et pourquoi. Sert à l'accueil (sélecteur), à la page Solutions (filtre), à l'offre
# (« lequel choisir »), au configurateur (première étape) et à la fiche de l'IA.
#
# Public (décision de James) : « Pour chez moi », « Pour mon entreprise » ou « Les deux ». Chaque lieu et
# chaque solution dit pour qui il est : "particulier", "entreprise" ou "les deux". Côté particulier, on ne
# montre pas ce qui est propre à l'entreprise (SOLUTIONS_PUBLIC, lieux de la famille « entreprise »).
# Le contenu reste dans le HTML : le filtrage se fait par l'attribut data-public (CSS et assets/js/wow.js).
#
# Cinq familles (docs/OFFRE.md, règle 1 : un cerveau par lieu) :
#   - chez vous, votre entreprise : un appareil JARVIS;
#   - lieux mobiles (on y vit) : un appareil JARVIS et un Boîtier VR;
#   - véhicules, aérien (on s'y déplace) : un Boîtier Mobilité, rien d'autre à bord.
# Aucun nom de lieu réel. Aucun prix ici.

import json
import os

from config import CAPABILITIES

ENV, IA, SECU, AUTO, RES, DIAG, MOB = (
    "environnements-intelligents", "ia-privee-connaissances", "securite-intelligente",
    "automatisation-operations", "reseau-resilience", "diagnostic-care", "mobilite",
)

FAMILLES = [
    ("chez-vous", "Chez vous"),
    ("entreprise", "Votre entreprise"),
    ("mobile", "Lieux mobiles"),
    ("vehicules", "Véhicules"),
    ("aerien", "Aérien"),
]

# Les solutions propres à l'entreprise (les autres servent aux deux publics)
SOLUTIONS_PUBLIC = {AUTO: "entreprise"}


def public_sol(slug):
    """Attribut data-public d'une solution : vide si elle sert aux deux publics."""
    return ' data-public="entreprise"' if SOLUTIONS_PUBLIC.get(slug) == "entreprise" else ""


# Les trois appareils (décision de James, 19 novembre 2026) : ils ne portent plus le nom des niveaux.
# Le client choisit un niveau (Base, Signature, Platinum); JARVIS choisit l'appareil de chaque lieu.
HUB_NOM = {"base": "JARVIS Mini", "signature": "JARVIS", "platinum": "JARVIS Pro"}

# id, nom, famille, appareil conseillé (clé « hub »; None : rien à bord), raison, solutions [(slug, raison)], démonstration
LIEUX = [
    # ---------------- Chez vous
    {"id": "maison", "nom": "Maison", "famille": "chez-vous", "hub": "signature",
     "raison": "L’IA tourne chez vous, sans Internet, et relie jusqu’à 100 appareils.",
     "solutions": [(ENV, "Lumières, chauffage et énergie sur un seul écran."),
                   (SECU, "Caméras, portes et alarme dans un seul fil."),
                   (RES, "Un Wi-Fi solide dans toute la maison.")],
     "demo": f"/solutions/{ENV}/#essayer"},
    {"id": "condo", "nom": "Condo", "famille": "chez-vous", "hub": "base",
     "raison": "Un lieu simple : quelques appareils, une fuite ou une porte à surveiller.",
     "solutions": [(ENV, "Chauffage et éclairage réglés selon votre journée."),
                   (DIAG, "Une fuite d’eau repérée avant le dégât.")],
     "demo": f"/solutions/{ENV}/#essayer"},
    {"id": "chalet", "nom": "Chalet", "famille": "chez-vous", "hub": "base",
     "raison": "Il veille sur un lieu fermé : gel, fuite, porte, batterie.",
     "solutions": [(DIAG, "Gel, fuite, panne : prévenu avant le dégât."),
                   (SECU, "Une porte ouverte ou un mouvement, vous le savez."),
                   (ENV, "Le chauffage monté avant votre arrivée.")],
     "demo": f"/solutions/{DIAG}/#essayer"},
    {"id": "domaine", "nom": "Domaine", "famille": "chez-vous", "hub": "platinum",
     "raison": "Plusieurs bâtiments, beaucoup de caméras, rien ne doit s’arrêter.",
     "solutions": [(SECU, "Caméras, plaques et accès de toute la propriété."),
                   (ENV, "Maison, garage et dépendances sur un seul écran."),
                   (RES, "Un réseau qui relie chaque bâtiment."),
                   (DIAG, "Eau, énergie et équipements suivis jour après jour.")],
     "demo": f"/solutions/{SECU}/#essayer"},
    # ---------------- Votre entreprise
    {"id": "bureau", "nom": "Bureau ou commerce", "famille": "entreprise", "hub": "signature",
     "raison": "Réceptionniste IA et jusqu’à dix automatisations, traitées sur place.",
     "solutions": [(AUTO, "La réception ne manque plus un appel."),
                   (IA, "Vos documents répondent aux questions de l’équipe."),
                   (RES, "Un réseau séparé pour les clients, les postes et les caméras.")],
     "demo": f"/solutions/{AUTO}/#essayer"},
    {"id": "atelier", "nom": "Atelier, entrepôt ou usine", "famille": "entreprise", "hub": "signature",
     "raison": "Accès, caméras et machines suivis au même endroit.",
     "solutions": [(SECU, "Qui entre, quand, et par quelle porte."),
                   (DIAG, "Une machine qui dérive se voit avant le bris."),
                   (RES, "Un réseau séparé pour les machines."),
                   (AUTO, "Commandes et bons qui circulent sans ressaisie.")],
     "demo": f"/solutions/{SECU}/#essayer"},
    {"id": "ferme", "nom": "Ferme", "famille": "entreprise", "hub": "platinum",
     "raison": "Des bâtiments et des animaux qui ne peuvent pas attendre : batterie et Internet de secours.",
     "solutions": [(DIAG, "Température, courant, eau : l’alerte avant la perte."),
                   (ENV, "Tous les bâtiments sur un seul écran."),
                   (RES, "Internet dans chaque bâtiment."),
                   (SECU, "Portes, barrières et visiteurs.")],
     "demo": "/solutions/domotique-ferme-agricole/"},
    {"id": "garage", "nom": "Garage ou hangar", "famille": "entreprise", "hub": "signature",
     "raison": "Des biens de valeur : caméras analysées sur place, accès contrôlés.",
     "solutions": [(SECU, "Chaque entrée et chaque sortie, avec l’image."),
                   (ENV, "Portes, humidité et température du bâtiment."),
                   (DIAG, "Batteries et équipements suivis.")],
     "demo": f"/solutions/{SECU}/#essayer"},
    # ---------------- Lieux mobiles (on y vit)
    {"id": "vr", "nom": "VR", "famille": "mobile", "hub": "signature", "boitier": "Boîtier VR",
     "raison": "Une maison qui roule : JARVIS et son Boîtier VR gèrent batteries, eau, chauffage et sécurité.",
     "solutions": [(ENV, "Batteries, eau, chauffage et lumières à bord."),
                   (MOB, "Un copilote qui propose le bon arrêt."),
                   (SECU, "Le véhicule surveillé quand vous êtes ailleurs."),
                   (DIAG, "Une batterie ou une pompe qui faiblit se voit tôt.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    {"id": "roulotte", "nom": "Roulotte", "famille": "mobile", "hub": "base", "boitier": "Boîtier VR",
     "raison": "Batteries, réservoirs, gel et porte : l’essentiel d’un petit lieu mobile.",
     "solutions": [(ENV, "Batteries et réservoirs d’un coup d’œil."),
                   (DIAG, "Le gel et les fuites signalés."),
                   (MOB, "Le trajet et les arrêts gardés sur la carte.")],
     "demo": f"/solutions/{ENV}/#essayer"},
    {"id": "bateau", "nom": "Bateau ou yacht", "famille": "mobile", "hub": "base", "boitier": "Boîtier VR",
     "raison": "À quai comme en route : énergie, cale et accès surveillés.",
     "solutions": [(ENV, "Énergie, réservoirs et confort à bord."),
                   (DIAG, "Pompe de cale et batteries suivies."),
                   (SECU, "Une présence à bord, vous le savez.")],
     "demo": f"/solutions/{ENV}/#essayer"},
    # ---------------- Véhicules (on s'y déplace)
    {"id": "auto", "nom": "Auto ou camion", "famille": "vehicules", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Un seul boîtier à bord : il donne la position, le diagnostic et l’antivol.",
     "solutions": [(MOB, "Position, diagnostic et antivol, de partout.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    {"id": "moto", "nom": "Moto", "famille": "vehicules", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Un seul boîtier à bord : le Boîtier Mobilité suffit.",
     "solutions": [(MOB, "Position et antivol, de partout.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    {"id": "flotte", "nom": "Flotte de véhicules", "famille": "vehicules", "public": "entreprise", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Un Boîtier Mobilité par véhicule : position, diagnostic et antivol pour toute la flotte.",
     "solutions": [(MOB, "Chaque véhicule, son état et ses trajets au même endroit."),
                   (DIAG, "L’entretien prévu avant la panne.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    # ---------------- Aérien : suivi au sol seulement, jamais l'avionique
    {"id": "avion", "nom": "Avion ou hélicoptère", "famille": "aerien", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Suivi au sol par son boîtier : position, batterie, alertes. Le hangar, lui, reçoit son propre JARVIS. Rien ne touche jamais à l’avionique.",
     "solutions": [(MOB, "L’appareil, sa position et son état au sol, au même endroit.")],
     "demo": f"/solutions/{ENV}/#essayer"},
]

# Quel niveau choisir : des bénéfices, pas des spécifications (décision de James). Chaque carte répond à
# « est-ce pour moi? » : une situation, une promesse, trois « Vous pouvez… », une limite honnête.
# Les faits restent ceux du comparatif du catalogue (C.COMPARE) : caméras analysées, IA locale ou par
# Internet, lieux reliés, batterie et Internet de secours.
HUBS_CHOIX = {
    "base": {
        "situation": "Un petit lieu à surveiller", "pour": "Chalet, condo, petit VR",
        "promesse": "Savoir que tout va bien, et agir à distance.",
        "peut": ["Être prévenu d’une fuite, du gel ou d’une porte ouverte",
                 "Régler le chauffage et les lumières de partout",
                 "Voir jusqu’à deux caméras"],
        "savoir": "L’assistant passe par Internet. Idéal comme deuxième lieu, relié à votre maison.",
    },
    "signature": {
        "situation": "La maison où vous vivez", "pour": "Maison, VR complet, petite entreprise", "pour_moi": "Maison, VR complet",
        "promesse": "Tout le lieu, et une IA qui reste chez vous.",
        "peut": ["Tout gérer dans une seule application",
                 "Parler à JARVIS, même sans Internet",
                 "Relier jusqu’à trois lieux : maison, chalet, VR"],
        "savoir": "Jusqu’à six caméras analysées.",
    },
    "platinum": {
        "situation": "Un lieu qui ne doit jamais s’arrêter", "pour": "Domaine, ferme, entreprise", "pour_moi": "Domaine",
        "promesse": "Plusieurs bâtiments, beaucoup de caméras, aucune coupure.",
        "peut": ["Continuer pendant une panne de courant ou d’Internet",
                 "Suivre tous vos bâtiments et vos lieux, sans limite",
                 "Recevoir des rapports et automatiser le travail"],
        "peut_moi": {2: "Analyser seize caméras et plus, sur place"},  # côté particulier, à la place du 3e point
        "savoir": "Pensé pour les grands lieux : trop pour une maison ordinaire.",
    },
}

for _l in LIEUX:
    _l.setdefault("public", "entreprise" if _l["famille"] == "entreprise" else "particulier" if _l["famille"] == "chez-vous" else "les deux")

PAR_ID = {l["id"]: l for l in LIEUX}
RANG = {"base": 1, "signature": 2, "platinum": 3}


def cerveaux(ids, niveau=None):
    """Les règles de l'offre (docs/OFFRE.md), comme « cerveaux » dans assets/js/wow.js : un seul niveau
    pour tous les lieux; le lieu principal (le premier qui demande le plus gros appareil) porte le
    niveau; aucun autre appareil ne dépasse le niveau. Un véhicule n'a pas d'appareil (None).
    Rend (niveau, lieu principal, {lieu: clé de l'appareil ou None})."""
    avec = [i for i in ids if PAR_ID[i]["hub"]]
    principal = max(avec, key=lambda i: RANG[PAR_ID[i]["hub"]], default=None)
    niveau = niveau or (PAR_ID[principal]["hub"] if principal else None)
    appareil = {}
    for i in ids:
        h = PAR_ID[i]["hub"]
        appareil[i] = None if not h else niveau if i == principal or RANG[h] > RANG[niveau] else h
    return niveau, principal, appareil
_TITRE = {c["slug"]: c["title"] for c in CAPABILITIES}


def donnees():
    """Ce que le script du site lit (assets/js/wow.js) : un seul bloc JSON, placé par selecteur()."""
    return json.dumps({
        l["id"]: {"nom": l["nom"], "famille": l["famille"], "public": l["public"], "hub": l["hub"], "hubNom": HUB_NOM.get(l["hub"]), "boitier": l.get("boitier"),
                  "raison": l["raison"], "demo": l["demo"],
                  "sols": [{"slug": s, "nom": _TITRE[s], "raison": r} for s, r in l["solutions"]]}
        for l in LIEUX
    }, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def selecteur(titre="Vos lieux.", sous="", ident="lieux"):
    """Le sélecteur de lieux de la page L'offre : cinq familles, gros boutons, plusieurs choix possibles.
    Toutes les familles sont toujours visibles : choisir un lieu d'entreprise fait apparaître, plus bas, ce
    qui est propre à l'entreprise (assets/js/wow.js règle <html data-public>). Sous les boutons,
    « Votre écosystème » se dessine (wow.js) : un cerveau par lieu. Le choix est gardé dans le navigateur
    (clé « jarvis-forfait »)."""
    groupes = []
    for fid, fnom in FAMILLES:
        boutons = "".join(f'<button type="button" class="lx-b" data-lieu="{l["id"]}" aria-pressed="false">{l["nom"]}</button>'
                          for l in LIEUX if l["famille"] == fid)
        groupes.append(f'<div class="lx-g"><p>{fnom}</p><div class="lx-bs">{boutons}</div></div>')
    return f"""<div class="lx" id="{ident}" data-lieux>
  <h2 class="lx-t">{titre}</h2>
  {f'<p class="lx-sous">{sous}</p>' if sous else ''}
  <div class="lx-gs">{"".join(groupes)}</div>
  <div class="lx-res lx-eco" data-lieux-res hidden aria-live="polite"></div>
  <script type="application/json" data-lieux-data>{donnees()}</script>
</div>"""


# ---------------------------------------------------------------------------------------------
# Le forfait partout (tiroir « Mon forfait », assets/js/wow.js) : sur chaque page, un petit bloc JSON
# donne le nom, l'appareil conseillé et la vignette de chaque lieu, et le nom et la vignette de chaque
# solution. Les vignettes sont produites par tools/vignettes.py (media/forfait/v-*.webp) à partir de
# la photo dédiée si elle existe, sinon d'une photo de repli.
# ---------------------------------------------------------------------------------------------
_RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_REPLI_LIEU = {
    "maison": "/media/accueil/lieu-maison.webp", "condo": "/media/vitrine/accueil/condo-urbain.webp",
    "chalet": "/media/vitrine/accueil/chalet-lac.webp", "domaine": "/media/accueil/lieu-domaine.webp",
    "bureau": "/media/vitrine/accueil/commerce-pme.webp", "atelier": "/media/accueil/lieu-entreprise.webp",
    "ferme": "/media/accueil/lieu-ferme.webp", "garage": "/media/vitrine/accueil/garage-lamborghini-ferrari.webp",
    "flotte": "/media/vitrine/accueil/allee-g63-escalade.webp", "vr": "/media/offre/vr.webp",
    "roulotte": "/media/offre/vr.webp", "bateau": "/media/vitrine/accueil/yacht-quai.webp",
    "auto": "/media/accueil/lieu-vehicule.webp", "moto": "/media/accueil/lieu-vehicule.webp",
    "avion": "/media/vitrine/accueil/jet-hangar.webp",
}
_CLE_SOL = {ENV: "environnements", IA: "ia", SECU: "securite", AUTO: "automatisation", RES: "reseau", DIAG: "diagnostic", MOB: "mobilite"}


def _existe(chemin):
    return os.path.exists(os.path.join(_RACINE, chemin.lstrip("/")))


def sources_vignettes():
    """(nom de vignette, photo source) pour tools/vignettes.py : la photo dédiée d'abord."""
    out = []
    for l in LIEUX:
        dedie = f"/media/forfait/lieu-{l['id']}.webp"
        out.append((f"lieu-{l['id']}", dedie if _existe(dedie) else _REPLI_LIEU[l["id"]]))
    for slug, cle in _CLE_SOL.items():
        dedie = f"/media/forfait/sol-{cle}.webp"
        out.append((f"sol-{cle}", dedie if _existe(dedie) else f"/media/accueil/sol-{cle}.webp"))
    for h in HUB_NOM:
        dedie = f"/media/hubs/hub-{h}.webp"
        out.append((f"hub-{h}", dedie if _existe(dedie) else "/media/hubs/hub-signature.webp"))
    return out


def _v(nom):
    chemin = f"/media/forfait/v-{nom}.webp"
    return chemin if _existe(chemin) else ""


def reference():
    """Le bloc JSON de référence du forfait, placé sur chaque page (src/partials.py)."""
    return json.dumps({
        "lieux": {l["id"]: {"n": l["nom"], "h": l["hub"], "b": l.get("boitier"), "p": l["public"], "img": _v(f"lieu-{l['id']}")} for l in LIEUX},
        "sols": {slug: {"n": _TITRE[slug], "img": _v(f"sol-{cle}")} for slug, cle in _CLE_SOL.items()},
        "hubs": {h: {"n": n, "img": _v(f"hub-{h}")} for h, n in HUB_NOM.items()},
    }, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
