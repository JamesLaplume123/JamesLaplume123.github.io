# Galeries photo du site : grandes images premium (cadre en cristal doré, cartes noires).
#
# Chaque emplacement prend automatiquement media/vitrine/<dossier>/<nom>.webp s'il existe au
# moment du build (déposer le fichier puis reconstruire, aucun changement de code). Sinon, il
# affiche un panneau noir sobre « Photo à venir » — jamais un dessin. Même mécanique que
# photo_ou_attente des démos. Les photos ne sont jamais recolorées : superpositions seulement.
#
# Trois formes :
#   mosaique()   : grande image vedette + cartes 4:3, clients ordinaires et de prestige;
#   panorama()   : image cinéma 21:9 pleine largeur, texte en superposition;
#   avant_apres(): deux images 3:2 côte à côte, « Avant » puis « Avec JARVIS ».

import os
from html import escape

_RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Registre des emplacements (rempli au build) : fichier, page, texte de remplacement, format.
PHOTOS = []

FORMATS = {
    "vedette": "4:3 · 2400 × 1800",
    "carte": "4:3 · 1600 × 1200",
    "panorama": "21:9 · 2560 × 1100",
    "paire": "3:2 · 1800 × 1200",
}


def _src(cle, page, alt, forme):
    """Chemin public de la photo si le fichier existe, sinon None. Note l'emplacement au registre."""
    fichier = "media/vitrine/" + cle + ".webp"
    if not any(p["fichier"] == fichier for p in PHOTOS):
        PHOTOS.append({"fichier": fichier, "page": page, "alt": alt, "format": FORMATS[forme]})
    if os.path.exists(os.path.join(_RACINE, fichier)):
        return "/" + fichier
    return None


def _visuel(cle, page, alt, forme, pos="50% 50%", attente="Photo à venir", eager=False):
    src = _src(cle, page, alt, forme)
    if src:
        lazy = "" if eager else ' loading="lazy"'
        return f'<img src="{src}" alt="{escape(alt)}"{lazy} style="object-position:{pos}">', False
    return (
        f'<div class="gl-ph" role="img" aria-label="{escape(alt)}">'
        f'<span class="gl-ph-f" aria-hidden="true"></span>'
        f'<span class="gl-ph-n">{attente}</span></div>'
    ), True


def _figure(c, page, forme, classes="", attente="Photo à venir"):
    vis, ph = _visuel(c["f"], page, c["alt"], forme, c.get("pos", "50% 50%"), attente)
    cls = " ".join(x for x in ("gl-fig", classes, "is-ph" if ph else "") if x)
    cap = ""
    k, t = _typo(c.get("k", "")), _typo(c.get("t", ""))
    if k or t:
        cap = "<figcaption>" + (f"<span>{k}</span>" if k else "") + (f"<b>{t}</b>" if t else "") + "</figcaption>"
    badge = f'<i class="gl-badge{" is-on" if c.get("on") else ""}">{c["badge"]}</i>' if c.get("badge") else ""
    return f'<figure class="{cls}" data-rev>{vis}{badge}{cap}</figure>'


def _typo(s):
    """Apostrophe typographique dans les textes visibles."""
    return s.replace("'", "’")


def _tete(eyebrow, titre, intro):
    return f"""<div class="sect-head">
    <div data-rev>
      <p class="eyebrow">{eyebrow}</p>
      <h2 style="margin-top:1rem">{titre}</h2>
    </div>
    <p data-rev>{intro}</p>
  </div>"""


def mosaique(page, ident, eyebrow, titre, intro, cartes, toc="", alt=False, attente="Photo à venir", note=""):
    """Grande mosaïque : la première carte est la vedette (2 × 2), les autres en 4:3."""
    figs = "".join(
        _figure(c, page, "vedette" if i == 0 else "carte", "is-big" if i == 0 else "", attente)
        for i, c in enumerate(cartes)
    )
    toc_attr = f' data-toc="{toc}"' if toc else ""
    note_html = f'<p class="gl-note" data-rev>{note}</p>' if note else ""
    return f"""
<section class="sect gl-sect{' alt' if alt else ''}" id="{ident}"{toc_attr}>
  {_tete(eyebrow, titre, intro)}
  <div class="gl-mos gl-n{len(cartes)}">{figs}</div>
  {note_html}
</section>"""


def panorama(page, c, eyebrow, titre, texte, ident="", toc="", attente="Photo à venir"):
    """Image cinéma pleine largeur, texte posé sur un dégradé noir (aucune teinte sur la photo)."""
    vis, ph = _visuel(c["f"], page, c["alt"], "panorama", c.get("pos", "50% 50%"), attente)
    id_attr = f' id="{ident}"' if ident else ""
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""
<section class="gl-pano"{id_attr}{toc_attr}>
  <figure class="gl-fig gl-wide{' is-ph' if ph else ''}" data-rev>
    {vis}
    <figcaption class="gl-wide-t">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{titre}</h2>
      <p>{texte}</p>
    </figcaption>
  </figure>
</section>"""


def avant_apres(page, avant, apres, eyebrow, titre, intro, ident="", toc="", alt=False, attente="Photo à venir",
                libelles=("Avant", "Avec JARVIS")):
    """Deux grandes images côte à côte : la situation d'aujourd'hui, puis la même avec JARVIS."""
    # La pastille dit déjà « Avant » / « Avec JARVIS » : la légende garde seulement la phrase.
    a = dict(avant, badge=libelles[0], k="")
    b = dict(apres, badge=libelles[1], on=True, k="")
    id_attr = f' id="{ident}"' if ident else ""
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""
<section class="sect gl-sect{' alt' if alt else ''}"{id_attr}{toc_attr}>
  {_tete(eyebrow, titre, intro)}
  <div class="gl-va">{_figure(a, page, "paire", "", attente)}<span class="gl-va-arrow" aria-hidden="true"></span>{_figure(b, page, "paire", "", attente)}</div>
</section>"""


# ---------------------------------------------------------------------------------------------
# Clients : du quotidien au prestige (accueil, et repris en anglais sur /en/).

CLIENTS = [
    {"f": "accueil/residence-prestige-soir", "pos": "50% 60%",
     "alt": "Résidence de prestige au bord d'un lac, le soir, toutes les lumières en ambiance dorée",
     "k": "Résidence de prestige", "t": "Le domaine s'éclaire seul au coucher du soleil"},
    {"f": "accueil/maison-familiale", "alt": "Maison familiale de banlieue québécoise au crépuscule, entrée éclairée",
     "k": "Maison familiale", "t": "Chauffage, portes et lumières dans une seule app"},
    {"f": "accueil/garage-lamborghini-ferrari", "alt": "Garage de collection avec une Lamborghini et une Ferrari sous un éclairage doré",
     "k": "Garage de collection", "t": "Chaque voiture surveillée, chaque accès noté"},
    {"f": "accueil/allee-g63-escalade", "alt": "Allée privée la nuit avec un Mercedes G63 noir et un Cadillac Escalade noir",
     "k": "Allée privée", "t": "Les véhicules de la maison reconnus à l'arrivée"},
    {"f": "accueil/condo-urbain", "alt": "Condo moderne en ville, salon sobre avec vue sur les lumières du centre-ville",
     "k": "Condo en ville", "t": "Simple, discret, sans abonnement au nuage"},
    {"f": "accueil/yacht-quai", "alt": "Yacht à moteur amarré à un quai privé au crépuscule, ponts éclairés",
     "k": "Yacht", "t": "Batteries, cales et caméras suivies depuis le quai"},
    {"f": "accueil/jet-hangar", "alt": "Jet d'affaires dans un hangar privé brillant, porte ouverte sur la piste au crépuscule",
     "k": "Jet d'affaires", "t": "Le hangar, l'accès et le départ préparés"},
    {"f": "accueil/chalet-lac", "alt": "Chalet en bois au bord d'un lac en hiver, fenêtres chaudes et neige bleutée",
     "k": "Chalet", "t": "Chauffé et vérifié avant votre arrivée"},
    {"f": "accueil/commerce-pme", "alt": "Petite boutique de quartier à la fermeture, vitrine éclairée et rideau à demi baissé",
     "k": "PME", "t": "La fermeture du soir faite en une touche"},
]

CLIENTS_EN = [
    ("Prestige residence", "The estate lights itself at sunset"),
    ("Family home", "Heating, doors and lights in one app"),
    ("Collector's garage", "Every car watched, every access logged"),
    ("Private driveway", "The household's vehicles recognized on arrival"),
    ("City condo", "Simple, discreet, no cloud subscription"),
    ("Yacht", "Batteries, bilges and cameras followed from the dock"),
    ("Business jet", "Hangar, access and departure prepared"),
    ("Cabin", "Heated and checked before you arrive"),
    ("Small business", "Evening closing done in one touch"),
]


def clients_fr(page="/"):
    return mosaique(
        page, "clients", "Pour qui · du quotidien au prestige",
        "Une maison familiale ou un domaine.<br><em>Le même soin.</em>",
        "Une famille, un collectionneur, un propriétaire de yacht ou une PME : JARVIS s’adapte au lieu, "
        "pas l’inverse. Chaque installation est privée, locale et faite sur mesure.",
        CLIENTS,
    )


def clients_en(page="/en/"):
    cartes = [dict(c, k=k, t=t) for c, (k, t) in zip(CLIENTS, CLIENTS_EN)]
    return mosaique(
        page, "clients", "Who it is for · everyday to prestige",
        "A family home or an estate.<br><em>The same care.</em>",
        "A family, a collector, a yacht owner or a small business: JARVIS adapts to the place, not the "
        "other way around. Every installation is private, local and made to measure.",
        cartes, attente="Photo coming soon",
    )


# ---------------------------------------------------------------------------------------------
# Pages de solution : « Sur le terrain » (trois scènes) et « Avant / avec JARVIS ».

SOLUTIONS = {
    "environnements-intelligents": {
        "titre": "Du bungalow au domaine.<br><em>Le lieu vous répond.</em>",
        "intro": "Lumière, chauffage, stores et accès réglés selon l’heure et les personnes présentes, "
                 "dans une maison ordinaire comme dans une résidence de prestige.",
        "cartes": [
            {"f": "solutions/environnements/salon-prestige-soir", "alt": "Grand salon d'une résidence de prestige le soir, éclairage indirect doré, baie vitrée sur un lac",
             "k": "Résidence de prestige", "t": "L’ambiance du soir se met en place seule"},
            {"f": "solutions/environnements/cuisine-familiale", "alt": "Cuisine familiale chaleureuse le matin, café, lumière douce et tablette murale",
             "k": "Maison familiale", "t": "Le matin prêt avant le réveil"},
            {"f": "solutions/environnements/penthouse-ville", "alt": "Penthouse en hauteur la nuit, stores à demi fermés, ville illuminée",
             "k": "Penthouse", "t": "Stores et climat selon le soleil"},
        ],
        "avant": {"f": "solutions/environnements/avant-telecommandes", "alt": "Table de salon encombrée de télécommandes et de téléphones, lumière froide et crue",
                  "k": "Aujourd’hui", "t": "Cinq applications, trois télécommandes"},
        "apres": {"f": "solutions/environnements/apres-ambiance", "alt": "Le même salon calme en ambiance dorée, une seule tablette posée sur la table",
                  "k": "Avec JARVIS", "t": "Une ambiance, une touche"},
    },
    "ia-privee-connaissances": {
        "titre": "Vos documents, vos réponses.<br><em>Sans quitter la maison.</em>",
        "intro": "Un bureau de direction, un cabinet de quartier ou la table de cuisine : l’IA privée cherche "
                 "dans vos sources, cite ses preuves et ne sort jamais de chez vous.",
        "cartes": [
            {"f": "solutions/ia/bureau-direction", "alt": "Bureau de direction en bois sombre dans une résidence de prestige, écran et lampe dorée la nuit",
             "k": "Bureau de direction", "t": "Les contrats retrouvés en une question"},
            {"f": "solutions/ia/cabinet-pme", "alt": "Petit cabinet professionnel ordonné, classeurs, écran et plante, fin de journée",
             "k": "Cabinet de quartier", "t": "Les dossiers des clients, cités et vérifiables"},
            {"f": "solutions/ia/table-famille-papiers", "alt": "Table de cuisine familiale avec factures, garanties et une tablette, lumière chaude",
             "k": "Famille", "t": "Garanties, factures et rendez-vous au même endroit"},
        ],
        "avant": {"f": "solutions/ia/avant-piles", "alt": "Bureau débordant de piles de papiers, de boîtes d'archives et de notes collées",
                  "k": "Aujourd’hui", "t": "Chercher prend plus de temps que décider"},
        "apres": {"f": "solutions/ia/apres-bureau-clair", "alt": "Le même bureau dégagé et rangé, une seule tablette et une tasse, lumière dorée",
                  "k": "Avec JARVIS", "t": "Une question, une réponse sourcée"},
    },
    "securite-intelligente": {
        "titre": "La maison, le garage, l’allée.<br><em>Chaque arrivée comprise.</em>",
        "intro": "Un colis à la porte d’une maison familiale ou une Lamborghini dans un garage de collection : "
                 "JARVIS distingue l’attendu de l’inhabituel et vous le dit en une phrase.",
        "cartes": [
            {"f": "solutions/securite/allee-g63-escalade-nuit", "alt": "Allée de résidence de prestige la nuit, Mercedes G63 noir et Cadillac Escalade noir sous des projecteurs dorés",
             "k": "Allée privée", "t": "Les véhicules de la maison reconnus, les autres signalés"},
            {"f": "solutions/securite/garage-lamborghini-ferrari", "alt": "Garage de collection immaculé, Lamborghini et Ferrari côte à côte, caméra discrète au plafond",
             "k": "Garage de collection", "t": "Chaque porte et chaque présence notées"},
            {"f": "solutions/securite/porche-colis", "alt": "Porche d'une maison familiale au crépuscule, colis déposé près de la porte, lumière d'entrée allumée",
             "k": "Maison familiale", "t": "« 21 h 42 — Livraison : un colis à l’entrée. »"},
        ],
        "avant": {"f": "solutions/securite/avant-allee-sombre", "alt": "Allée de maison plongée dans le noir, une seule lumière faible, silhouettes d'arbres",
                  "k": "Aujourd’hui", "t": "Des alertes sans contexte, la nuit dans le noir"},
        "apres": {"f": "solutions/securite/apres-allee-eclairee", "alt": "La même allée éclairée avec douceur, chemin balisé, entrée accueillante",
                  "k": "Avec JARVIS", "t": "La bonne lumière, la bonne alerte"},
    },
    "automatisation-operations": {
        "titre": "Du family office à l’atelier.<br><em>Le travail avance seul.</em>",
        "intro": "Demandes, documents et approbations qui suivent leur chemin entre vos outils, dans une PME de "
                 "quartier comme dans un bureau privé de gestion de patrimoine.",
        "cartes": [
            {"f": "solutions/automatisation/family-office", "alt": "Bureau privé de gestion de patrimoine en verre et bois sombre, vue sur la ville la nuit",
             "k": "Bureau privé", "t": "Les approbations prêtes à signer le matin"},
            {"f": "solutions/automatisation/atelier-pme", "alt": "Atelier de PME propre et organisé, établis, tablette sur support et bacs étiquetés",
             "k": "Atelier", "t": "Les bons de travail créés depuis un courriel"},
            {"f": "solutions/automatisation/entrepot-quai", "alt": "Quai de chargement d'un petit entrepôt au lever du jour, palettes alignées",
             "k": "Entrepôt", "t": "Les réceptions confirmées sans ressaisie"},
        ],
        "avant": {"f": "solutions/automatisation/avant-ressaisie", "alt": "Employé fatigué devant deux écrans et des papiers, recopiant des informations tard le soir",
                  "k": "Aujourd’hui", "t": "Les mêmes informations tapées trois fois"},
        "apres": {"f": "solutions/automatisation/apres-equipe", "alt": "Petite équipe détendue autour d'une table lumineuse, une tablette au centre, lumière de fin d'après-midi",
                  "k": "Avec JARVIS", "t": "L’équipe décide, le reste suit"},
    },
    "reseau-resilience": {
        "titre": "Du routeur de la maison<br><em>à la passerelle du yacht.</em>",
        "intro": "Un réseau compris, surveillé et privé : dans une PME, dans la salle technique d’un domaine "
                 "ou à bord d’un yacht relié par satellite.",
        "cartes": [
            {"f": "solutions/reseau/salle-technique-domaine", "alt": "Salle technique d'une résidence de prestige, baie réseau noire impeccable, câbles rangés, voyants ambrés",
             "k": "Salle technique", "t": "Chaque équipement connu, chaque lien suivi"},
            {"f": "solutions/reseau/yacht-passerelle", "alt": "Passerelle de commandement d'un yacht la nuit, écrans de navigation, mer sombre au-delà des vitres",
             "k": "Yacht", "t": "Satellite, LTE et Wi-Fi de bord sous contrôle"},
            {"f": "solutions/reseau/bureau-pme-routeur", "alt": "Petit bureau de PME, armoire réseau murale propre et bien étiquetée",
             "k": "PME", "t": "Le réseau visible avant qu’il tombe"},
        ],
        "avant": {"f": "solutions/reseau/avant-cables", "alt": "Placard technique en désordre, câbles emmêlés, routeurs empilés, poussière",
                  "k": "Aujourd’hui", "t": "Personne ne sait ce qui est branché"},
        "apres": {"f": "solutions/reseau/apres-baie", "alt": "Le même placard refait : baie noire, câbles peignés, voyants ordonnés",
                  "k": "Avec JARVIS", "t": "Tout est inventorié et surveillé"},
    },
    "diagnostic-care": {
        "titre": "Du chauffe-eau à la GT-R.<br><em>Chaque panne a son dossier.</em>",
        "intro": "Un symptôme relié aux preuves, puis un dossier clair pour le technicien : sur une fournaise "
                 "de maison, une Nissan GT-R R35 ou la salle des machines d’un yacht.",
        "cartes": [
            {"f": "solutions/diagnostic/garage-gtr-r35", "alt": "Nissan GT-R R35 noire sur un pont élévateur dans un atelier propre, tablette de diagnostic posée à côté",
             "k": "Atelier de performance", "t": "Les codes, l’historique et les mesures réunis"},
            {"f": "solutions/diagnostic/salle-machines-yacht", "alt": "Salle des machines d'un yacht impeccable, moteurs blancs, éclairage technique",
             "k": "Yacht", "t": "Moteurs et génératrices suivis entre deux sorties"},
            {"f": "solutions/diagnostic/chaufferie-maison", "alt": "Sous-sol de maison familiale, fournaise et chauffe-eau propres, lampe de travail",
             "k": "Maison familiale", "t": "La fournaise prévient avant de lâcher"},
        ],
        "avant": {"f": "solutions/diagnostic/avant-technicien", "alt": "Technicien perplexe devant un panneau électrique ouvert, lampe frontale, aucun historique",
                  "k": "Aujourd’hui", "t": "Chaque visite recommence à zéro"},
        "apres": {"f": "solutions/diagnostic/apres-dossier", "alt": "Technicien serein consultant un dossier clair sur une tablette devant le même panneau",
                  "k": "Avec JARVIS", "t": "Le dossier arrive avant le technicien"},
    },
    "mobilite": {
        "titre": "Le VR de la famille ou le G63.<br><em>La route mieux préparée.</em>",
        "intro": "Arrêts, recharge, météo et souvenirs de voyage : JARVIS accompagne un road trip familial "
                 "comme un départ en Range Rover vers le chalet.",
        "cartes": [
            {"f": "solutions/mobilite/range-rover-neige", "alt": "Range Rover noir sur une route de montagne enneigée au crépuscule, phares allumés",
             "k": "Vers le chalet", "t": "Le chalet chauffé avant l’arrivée"},
            {"f": "solutions/mobilite/audi-rs4-route", "alt": "Audi RS4 familiale sur une route côtière sinueuse au coucher du soleil",
             "k": "Road trip", "t": "Le bon arrêt au bon moment"},
            {"f": "solutions/mobilite/vr-familial", "alt": "VR familial garé au bord d'un lac au crépuscule, auvent ouvert, guirlande douce",
             "k": "VR familial", "t": "Eau, batteries et météo du campement"},
        ],
        "avant": {"f": "solutions/mobilite/avant-carte-papier", "alt": "Carte routière dépliée et téléphone sur le tableau de bord, conducteur perdu sous la pluie",
                  "k": "Aujourd’hui", "t": "Chercher au lieu de profiter"},
        "apres": {"f": "solutions/mobilite/apres-route", "alt": "Route ouverte au coucher du soleil vue depuis l'habitacle, tableau de bord sobre",
                  "k": "Avec JARVIS", "t": "La route prévue, l’esprit libre"},
    },
}


def terrain(slug, alt=False):
    """« Sur le terrain » + « Avant / avec JARVIS » pour une page de solution."""
    d = SOLUTIONS[slug]
    page = f"/solutions/{slug}/"
    return mosaique(page, "terrain", "Sur le terrain · ordinaire et prestige", d["titre"], d["intro"],
                    d["cartes"], toc="Sur le terrain", alt=alt) + avant_apres(
        page, d["avant"], d["apres"], "Avant · avec JARVIS",
        "Le même lieu.<br><em>Une autre façon d’y vivre.</em>",
        "À gauche, la situation d’aujourd’hui. À droite, la même avec JARVIS.", alt=not alt)


# ---------------------------------------------------------------------------------------------
# Autres pages.

def accueil_panorama():
    return panorama(
        "/", {"f": "accueil/panorama-domaine-crepuscule", "pos": "50% 55%",
              "alt": "Vue aérienne d'un domaine au bord d'un lac au crépuscule, maison, garage et quai éclairés en doré"},
        "Le soir tombe · JARVIS veille",
        "Tout le domaine.<br><em>Un seul regard.</em>",
        "Maison, garage, quai et chalet : les lumières, les accès et les caméras suivent la même règle, "
        "décidée par vous.", ident="domaine")


def plateforme_lieux():
    return mosaique(
        "/plateforme/", "lieux", "Un Hub · tous vos lieux",
        "Un seul Hub.<br><em>Partout où vous vivez.</em>",
        "Le même JARVIS dans une armoire technique, un penthouse, un chalet, à bord d’un yacht ou dans "
        "le hangar d’un jet. Vos règles vous suivent d’un lieu à l’autre.",
        [
            {"f": "plateforme/hub-armoire-technique", "alt": "Petit serveur JARVIS Hub noir dans une armoire technique vitrée d'une résidence de prestige, voyants ambrés",
             "k": "Le Hub, chez vous", "t": "Un petit serveur privé, rangé sous clé"},
            {"f": "plateforme/penthouse-nuit", "alt": "Salon de penthouse la nuit, mobilier sombre, ville scintillante derrière les baies",
             "k": "Penthouse", "t": "La ville, les stores et le climat"},
            {"f": "plateforme/chalet-hiver", "alt": "Chalet de bois et de verre dans la neige, foyer allumé visible à travers la baie",
             "k": "Chalet", "t": "Prêt avant votre arrivée"},
            {"f": "plateforme/yacht-salon-bord", "alt": "Salon intérieur d'un yacht en cuir crème et bois sombre, lumières douces, mer calme au crépuscule",
             "k": "Yacht", "t": "Le bord relié au même Hub"},
            {"f": "plateforme/jet-cabine", "alt": "Cabine de jet d'affaires en cuir crème, hublots au coucher du soleil, tablette sur l'accoudoir",
             "k": "Jet d’affaires", "t": "Votre agenda vous suit en vol"},
            {"f": "plateforme/atelier-pme", "alt": "Atelier de PME moderne et lumineux, établis propres et outils rangés",
             "k": "PME", "t": "Les mêmes droits pour toute l’équipe"},
        ], toc="Vos lieux", alt=True)


def solutions_clients():
    return mosaique(
        "/solutions/", "clients", "Ils font appel à JARVIS",
        "Des besoins réels,<br><em>du quotidien au prestige.</em>",
        "Une famille pressée, un collectionneur, un gestionnaire de plusieurs immeubles ou une ferme : "
        "chacun commence par un seul problème concret.",
        [
            {"f": "solutions/clients/collectionneur", "alt": "Collectionneur en habit sombre dans son garage, Lamborghini et Ferrari en arrière-plan, tablette à la main, vu de dos",
             "k": "Collectionneur", "t": "Sécurité et climat du garage de collection"},
            {"f": "solutions/clients/famille-cuisine", "alt": "Famille dans une cuisine lumineuse le matin, parents et enfants, ambiance chaleureuse",
             "k": "Famille", "t": "Moins d’applications, plus de temps"},
            {"f": "solutions/clients/gestionnaire-immeubles", "alt": "Gestionnaire immobilier devant une rangée de condos modernes au crépuscule, tablette en main, vu de dos",
             "k": "Gestionnaire", "t": "Plusieurs immeubles, une seule vue"},
            {"f": "solutions/clients/ferme-laitiere", "alt": "Ferme laitière québécoise au lever du soleil, étable et silos, brume légère",
             "k": "Ferme", "t": "Bâtiments, génératrice et alertes de nuit"},
            {"f": "solutions/clients/proprietaire-yacht", "alt": "Propriétaire marchant sur le quai vers son yacht au coucher du soleil, vu de dos",
             "k": "Propriétaire de yacht", "t": "Le bord vérifié avant le départ"},
            {"f": "solutions/clients/pme-bureau", "alt": "Petite équipe de PME dans un bureau à aire ouverte chaleureux, fin de journée",
             "k": "PME", "t": "Les demandes traitées sans ressaisie"},
        ])


def a_propos_terrain():
    return panorama(
        "/a-propos/", {"f": "a-propos/atelier-saint-hyacinthe", "pos": "50% 50%",
                       "alt": "Atelier technique la nuit : établi, câblage 12 V, ordinateur portable ouvert et ambulance en arrière-plan"},
        "L’atelier · Saint-Hyacinthe",
        "Construit à la main.<br><em>Vérifié sur le terrain.</em>",
        "Chaque fonction de JARVIS passe par l’établi avant d’entrer chez un client.") + mosaique(
        "/a-propos/", "terrain", "Sur le terrain",
        "De l’établi<br><em>jusque chez vous.</em>",
        "Installation, essai dans le froid québécois, puis remise des clés : vous comprenez ce qui a été fait.",
        [
            {"f": "a-propos/installation-residence", "alt": "Technicien vu de dos installant un panneau mural discret dans l'entrée d'une résidence de prestige",
             "k": "Installation", "t": "Propre, discrète, documentée"},
            {"f": "a-propos/essai-hiver", "alt": "Véhicule aménagé dans la neige la nuit, fenêtres chaudes, ciel étoilé",
             "k": "Essai réel", "t": "Testé par −25 °C"},
            {"f": "a-propos/remise-cles", "alt": "Mains qui remettent une tablette et une clé sur un comptoir de marbre, lumière dorée",
             "k": "Remise des clés", "t": "Vous repartez en sachant tout faire"},
        ], alt=True)


def confiance_visuels():
    return panorama(
        "/confiance/", {"f": "confiance/armoire-verrouillee", "pos": "50% 50%",
                        "alt": "Armoire technique noire verrouillée dans une salle sobre, voyants ambrés, porte vitrée fumée"},
        "Chez vous · sous clé",
        "Vos données dorment<br><em>chez vous.</em>",
        "Le Hub vit dans votre armoire, pas dans le nuage d’un fournisseur. Vous gardez la clé.") + mosaique(
        "/confiance/", "preuves", "Des limites visibles",
        "Voir, approuver,<br><em>pouvoir revenir en arrière.</em>",
        "Trois gestes concrets qui rendent la confiance vérifiable.",
        [
            {"f": "confiance/approbation-main", "alt": "Main qui approuve une demande sur une tablette noire posée sur un bureau de bois sombre",
             "k": "Accord humain", "t": "Rien de sensible sans votre accord"},
            {"f": "confiance/sauvegarde-coffre", "alt": "Disque de sauvegarde rangé dans un petit coffre-fort ouvert, lumière tamisée",
             "k": "Sauvegarde", "t": "Une copie hors ligne, testée"},
            {"f": "confiance/journal-ecran", "alt": "Écran sombre flou affichant des lignes de journal dorées, en très faible profondeur de champ",
             "k": "Journal", "t": "Chaque accès laisse une trace"},
        ])


def contact_visuels():
    return panorama(
        "/contact/", {"f": "contact/demo-salon-prestige", "pos": "50% 55%",
                      "alt": "Salon de prestige le soir, tablette posée sur une table basse en marbre, fauteuils accueillants"},
        "La rencontre",
        "Une heure ensemble.<br><em>Un plan clair.</em>",
        "Chez vous, au bureau ou à bord du laboratoire mobile : on regarde le lieu réel, puis on décide.") + mosaique(
        "/contact/", "rencontre", "Où se fait la démo",
        "Là où vous vivez<br><em>et travaillez.</em>",
        "Choisissez l’endroit : la démonstration part de votre situation réelle.",
        [
            {"f": "contact/demo-chez-vous", "alt": "Deux personnes vues de dos discutant devant une tablette dans un salon familial chaleureux",
             "k": "Chez vous", "t": "Votre maison, vos vraies habitudes"},
            {"f": "contact/demo-laboratoire", "alt": "Intérieur aménagé du laboratoire mobile la nuit, éclairage doré, écran de commande allumé",
             "k": "Laboratoire mobile", "t": "Le système en vrai, devant vous"},
            {"f": "contact/demo-entreprise", "alt": "Salle de réunion sobre d'une PME, grande table, écran éteint, lumière de fin de journée",
             "k": "En entreprise", "t": "Vos outils, vos contraintes"},
        ], alt=True)


def laboratoire_visuels():
    return avant_apres(
        "/laboratoire-mobile/",
        {"f": "laboratoire/ambulance-avant", "alt": "Intérieur médical d'origine d'une ambulance Ford : civière, armoires blanches, éclairage froid",
         "k": "À l’achat", "t": "Une ambulance québécoise retirée du service"},
        {"f": "laboratoire/ambulance-apres", "alt": "Le même intérieur transformé : banquette, cuisinette en bois sombre, éclairage doré indirect",
         "k": "Aujourd’hui", "t": "Habitation, atelier et banc d’essai"},
        "Avant · après", "La même ambulance.<br><em>Une autre vie.</em>",
        "Du véhicule d’urgence au premier environnement JARVIS complet. Photos de la vraie construction dès "
        "qu’elles sont prêtes.", ident="transformation", libelles=("Avant", "Après")) + mosaique(
        "/laboratoire-mobile/", "chantier", "Le chantier",
        "Chaque fil compte.<br><em>Chaque étape est montrée.</em>",
        "Énergie, câblage, toit solaire et premières nuits : la construction réelle, étape par étape.",
        [
            {"f": "laboratoire/bivouac-nuit", "alt": "Ambulance aménagée en bivouac la nuit au bord d'un lac, fenêtres dorées, ciel étoilé",
             "k": "Première nuit", "t": "Autonome, loin du réseau"},
            {"f": "laboratoire/batteries-lifepo4", "alt": "Deux batteries LiFePO4 bien fixées dans un compartiment propre, câbles rouges et noirs soignés",
             "k": "Énergie", "t": "560 Ah de batteries LiFePO₄"},
            {"f": "laboratoire/cablage-12v", "alt": "Panneau de distribution 12 V soigné, fusibles alignés, câbles étiquetés",
             "k": "Câblage 12 V", "t": "Chaque circuit étiqueté"},
            {"f": "laboratoire/toit-solaire", "alt": "Panneaux solaires sur le toit de l'ambulance, vue en plongée au lever du soleil",
             "k": "Solaire", "t": "500 W sur le toit"},
            {"f": "laboratoire/poste-commande", "alt": "Poste de commande à bord : écran tactile encastré dans le bois sombre, éclairage doré",
             "k": "Poste de commande", "t": "Tout le véhicule sur un écran"},
            {"f": "laboratoire/hiver-route", "alt": "Ambulance aménagée sur une route enneigée du Québec au crépuscule, phares allumés",
             "k": "Hiver", "t": "Validé dans le vrai froid"},
        ], toc="", alt=True)
