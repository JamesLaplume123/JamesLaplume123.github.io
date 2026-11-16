# Les lieux du client : source unique (décision de James, novembre 2026).
# Les gens pensent « j'ai une ferme », pas « je veux Diagnostic & continuité ». Pour chaque lieu :
# les solutions qui comptent (une raison d'une ligne chacune), la démonstration à ouvrir, le Hub
# conseillé et pourquoi. Sert à l'accueil (sélecteur), à la page Solutions (filtre), à l'offre
# (« lequel choisir »), au configurateur (première étape) et à la fiche de l'IA.
#
# Public (décision de James) : « Pour chez moi », « Pour mon entreprise » ou « Les deux ». Chaque lieu et
# chaque solution dit pour qui il est : "particulier", "entreprise" ou "les deux". Côté particulier, on ne
# montre pas ce qui est propre à l'entreprise (SOLUTIONS_PUBLIC, lieux de la famille « entreprise »).
# Le contenu reste dans le HTML : le filtrage se fait par l'attribut data-public (CSS et assets/js/wow.js).
#
# Trois familles. « En déplacement » distingue deux sortes, comme le catalogue :
#   - lieux mobiles (on y vit) : Hub + Boîtier VR, presque toutes les solutions d'un lieu, plus Mobilité;
#   - véhicules (on s'y déplace) : Boîtier Mobilité, sans Hub à bord.
# Aucun nom de lieu réel. Aucun prix ici.

import json

from config import CAPABILITIES

ENV, IA, SECU, AUTO, RES, DIAG, MOB = (
    "environnements-intelligents", "ia-privee-connaissances", "securite-intelligente",
    "automatisation-operations", "reseau-resilience", "diagnostic-care", "mobilite",
)

FAMILLES = [
    ("chez-vous", "Chez vous"),
    ("entreprise", "Votre entreprise"),
    ("deplacement", "En déplacement"),
]

# Les solutions propres à l'entreprise (les autres servent aux deux publics)
SOLUTIONS_PUBLIC = {AUTO: "entreprise"}


def public_sol(slug):
    """Attribut data-public d'une solution : vide si elle sert aux deux publics."""
    return ' data-public="entreprise"' if SOLUTIONS_PUBLIC.get(slug) == "entreprise" else ""


HUB_NOM = {"base": "Hub Base", "signature": "Hub Signature", "platinum": "Hub Platinum"}

# id, nom, famille, sorte, hub conseillé (None : aucun Hub à bord), raison, solutions [(slug, raison)], démonstration
LIEUX = [
    # ---------------- Chez vous
    {"id": "maison", "nom": "Maison", "famille": "chez-vous", "hub": "signature",
     "raison": "L’IA tourne dans le Hub, sans Internet, et relie jusqu’à 100 appareils.",
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
    {"id": "flotte", "nom": "Flotte de véhicules", "famille": "entreprise", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Un Boîtier Mobilité par véhicule : position, diagnostic et antivol pour toute la flotte.",
     "solutions": [(MOB, "Chaque véhicule, son état et ses trajets au même endroit."),
                   (DIAG, "L’entretien prévu avant la panne.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    # ---------------- En déplacement : lieux mobiles (on y vit)
    {"id": "vr", "nom": "VR", "famille": "deplacement", "sorte": "Lieu mobile", "hub": "signature", "boitier": "Boîtier VR",
     "raison": "Une maison qui roule : le Hub et le Boîtier VR gèrent batteries, eau, chauffage et sécurité.",
     "solutions": [(ENV, "Batteries, eau, chauffage et lumières à bord."),
                   (MOB, "Un copilote qui propose le bon arrêt."),
                   (SECU, "Le véhicule surveillé quand vous êtes ailleurs."),
                   (DIAG, "Une batterie ou une pompe qui faiblit se voit tôt.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    {"id": "roulotte", "nom": "Roulotte", "famille": "deplacement", "sorte": "Lieu mobile", "hub": "base", "boitier": "Boîtier VR",
     "raison": "Batteries, réservoirs, gel et porte : l’essentiel d’un petit lieu mobile.",
     "solutions": [(ENV, "Batteries et réservoirs d’un coup d’œil."),
                   (DIAG, "Le gel et les fuites signalés."),
                   (MOB, "Le trajet et les arrêts gardés sur la carte.")],
     "demo": f"/solutions/{ENV}/#essayer"},
    {"id": "bateau", "nom": "Bateau habitable", "famille": "deplacement", "sorte": "Lieu mobile", "hub": "base", "boitier": "Boîtier VR",
     "raison": "À quai comme en route : énergie, cale et accès surveillés.",
     "solutions": [(ENV, "Énergie, réservoirs et confort à bord."),
                   (DIAG, "Pompe de cale et batteries suivies."),
                   (SECU, "Une présence à bord, vous le savez.")],
     "demo": f"/solutions/{ENV}/#essayer"},
    # ---------------- En déplacement : véhicules (on s'y déplace)
    {"id": "auto", "nom": "Auto ou camion", "famille": "deplacement", "sorte": "Véhicule", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Aucun Hub à bord : le Boîtier Mobilité donne la position, le diagnostic et l’antivol.",
     "solutions": [(MOB, "Position, diagnostic et antivol, de partout.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    {"id": "moto", "nom": "Moto", "famille": "deplacement", "sorte": "Véhicule", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "Aucun Hub à bord : le Boîtier Mobilité suffit.",
     "solutions": [(MOB, "Position et antivol, de partout.")],
     "demo": f"/solutions/{MOB}/#essayer"},
    {"id": "avion", "nom": "Avion", "famille": "deplacement", "sorte": "Véhicule", "hub": None, "boitier": "Boîtier Mobilité",
     "raison": "L’appareil est suivi par son boîtier; le hangar, lui, reçoit un Hub.",
     "solutions": [(MOB, "L’appareil, son état et ses vols au même endroit.")],
     "demo": f"/solutions/{ENV}/#essayer"},
]

# Quel Hub choisir : des bénéfices, pas des spécifications (décision de James). Chaque carte répond à
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

# « Vous hésitez? » : trois questions, la carte conseillée et sa raison (lu par assets/demos/offre.js).
HESITE = [
    ("lieux", "Combien de lieux?", [("1", "Un seul"), ("3", "Deux ou trois"), ("9", "Plus de trois")]),
    ("ia", "L’IA doit-elle fonctionner sans Internet?", [("oui", "Oui"), ("non", "Non")]),
    ("panne", "Le lieu doit-il tourner pendant une panne?", [("oui", "Oui"), ("non", "Non")]),
]
HESITE_RAISON = {
    "base": "Hub Base : un seul petit lieu, l’assistant par Internet vous suffit.",
    "signature": "Hub Signature : l’IA reste chez vous et relie jusqu’à trois lieux.",
    "platinum": "Hub Platinum : batterie et Internet de secours, lieux sans limite.",
}

for _l in LIEUX:
    _l["public"] = "entreprise" if _l["famille"] == "entreprise" else "particulier" if _l["famille"] == "chez-vous" else "les deux"

PAR_ID = {l["id"]: l for l in LIEUX}
_TITRE = {c["slug"]: c["title"] for c in CAPABILITIES}


def par_hub(hub):
    """Les lieux pour lesquels ce Hub est conseillé (l'offre : « lequel choisir »)."""
    return [l for l in LIEUX if l["hub"] == hub]


def donnees():
    """Ce que le script du site lit (assets/js/wow.js) : un seul bloc JSON, placé par selecteur()."""
    return json.dumps({
        l["id"]: {"nom": l["nom"], "famille": l["famille"], "public": l["public"], "hub": l["hub"], "hubNom": HUB_NOM.get(l["hub"]), "boitier": l.get("boitier"),
                  "raison": l["raison"], "demo": l["demo"],
                  "sols": [{"slug": s, "nom": _TITRE[s], "raison": r} for s, r in l["solutions"]]}
        for l in LIEUX
    }, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


PUBLICS = [("moi", "Pour chez moi"), ("entreprise", "Pour mon entreprise"), ("deux", "Les deux")]


def choix_public(cls="pub"):
    """Le choix de premier niveau : trois gros boutons. Retenu dans le navigateur avec le forfait."""
    return (f'<div class="{cls}" role="group" aria-label="Pour qui">'
            + "".join(f'<button type="button" data-public-set="{k}" aria-pressed="false">{n}</button>' for k, n in PUBLICS)
            + "</div>")


def selecteur(titre="Quel est votre lieu?", ident="lieux"):
    """Le sélecteur de lieu : d'abord « Pour chez moi / Pour mon entreprise / Les deux », puis trois familles,
    gros boutons, plusieurs choix possibles. Les lieux d'entreprise ne s'affichent pas côté particulier.
    Le choix est gardé dans le navigateur (clé « jarvis-forfait ») et suit le visiteur jusqu'au configurateur."""
    groupes = []
    for fid, fnom in FAMILLES:
        boutons, sorte = "", None
        for l in LIEUX:
            if l["famille"] != fid:
                continue
            if l.get("sorte") and l["sorte"] != sorte:
                sorte = l["sorte"]
                boutons += f'<span class="lx-sorte">{"Lieux mobiles" if sorte == "Lieu mobile" else "Véhicules"}</span>'
            boutons += f'<button type="button" class="lx-b" data-lieu="{l["id"]}" aria-pressed="false">{l["nom"]}</button>'
        pub = ' data-public="entreprise"' if fid == "entreprise" else ' data-public="particulier"' if fid == "chez-vous" else ""
        groupes.append(f'<div class="lx-g"{pub}><p>{fnom}</p><div class="lx-bs">{boutons}</div></div>')
    return f"""<div class="lx" id="{ident}" data-lieux>
  <h2 class="lx-t">{titre}</h2>
  {choix_public()}
  <div class="lx-gs">{"".join(groupes)}</div>
  <div class="lx-res" data-lieux-res hidden aria-live="polite"></div>
  <script type="application/json" data-lieux-data>{donnees()}</script>
</div>"""
