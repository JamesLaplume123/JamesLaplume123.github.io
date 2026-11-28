# Les trois divisions de JARVIS (refonte « trois divisions », novembre 2026) : Privé, Entreprise, Cyber.
# Source unique pour l'accueil, la page Solutions et le menu. On va du général au détail :
# ce qu'est JARVIS → les trois divisions → la gamme de chaque division → chaque solution.
# Aucune page n'est retirée : les sept solutions gardent leur adresse et leur nom.
# Rien ici ne dit quelle solution est incluse dans quel niveau : c'est l'offre (/offre/) qui le dit.
# Styles : assets/demos/divisions.css.

DIVISIONS = [
    {"id": "prive", "num": "01", "etat": "Maintenant", "nom": "JARVIS Privé",
     "pour": "Votre maison, votre chalet et vos véhicules",
     "ligne": "Protégés et gérés tout seuls, par une IA qui travaille chez vous.",
     "url": "/solutions/#prive", "img": "/media/vitrine/accueil/residence-prestige-soir.webp", "pos": "30% 55%"},
    {"id": "entreprise", "num": "02", "etat": "Ensuite", "nom": "JARVIS Entreprise",
     "pour": "Travailleurs autonomes, PME, fermes et commerces",
     "ligne": "Les appels, les tâches et l’information se gèrent seuls.",
     "url": "/solutions/entreprise/", "img": "/media/accueil/sol-automatisation.webp", "pos": "50% 50%"},
    {"id": "cyber", "num": "03", "etat": "Maintenant", "nom": "JARVIS Cyber",
     "pour": "Toute maison ou entreprise, cliente ou non",
     "ligne": "Nous vérifions vos systèmes comme un pirate le ferait, puis nous corrigeons avec vous.",
     "url": "/solutions/cyber/", "img": "/media/vision/securite-centre.webp", "pos": "50% 45%"},
]

# La gamme de chaque division : (étiquette, nom, promesse, adresse, photo, cadrage)
PRIVE = [
    ("Le cœur", "L’appareil JARVIS", "Le cerveau de votre maison. Son IA fait marcher tout le reste, chez vous.",
     "/plateforme/", "/media/hubs/hub-signature.webp", "50% 60%"),
    ("Solution", "Réseau et cybersécurité", "Votre réseau, gardé comme celui d’une entreprise.",
     "/solutions/reseau-resilience/", "/media/accueil/sol-reseau.webp", "50% 40%"),
    ("Solution", "Sécurité intelligente", "Une alarme sonne. JARVIS, lui, comprend.",
     "/solutions/securite-intelligente/", "/media/accueil/sol-securite.webp", "50% 45%"),
    ("Solution", "Diagnostic & continuité", "Rien ne brise sans que JARVIS le voie venir.",
     "/solutions/diagnostic-care/", "/media/accueil/sol-diagnostic.webp", "50% 40%"),
    ("Solution", "Environnements intelligents", "Votre maison s’ajuste seule. Votre facture baisse.",
     "/solutions/environnements-intelligents/", "/media/accueil/sol-environnements.webp", "50% 55%"),
    ("Solution", "Mobilité", "Tout ce qui roule, flotte ou vole, sous votre œil.",
     "/solutions/mobilite/", "/media/accueil/lieu-vehicule.webp", "50% 55%"),
    ("Solution", "IA privée et connaissances", "Posez une question à vos documents. La source est montrée.",
     "/solutions/ia-privee-connaissances/", "/media/accueil/sol-ia.webp", "50% 50%"),
    ("Vision", "Intelligence de vie", "Vos habitudes comprises, et un coach pour aller mieux.",
     "/vision-roadmap/#vie", "/media/concept/jarvis-life-context-v3.webp", "60% 40%"),
]
# JARVIS Entreprise : deux parties. Votre travail (ce qui est propre à l'entreprise), puis vos bâtiments
# (les solutions de JARVIS Privé, en version entreprise). Chaque pièce existe déjà dans l'offre
# (Réceptionniste IA, bibliothèque d'automatisations, Socle Entreprise, extensions).
ENTREPRISE_TRAVAIL = [
    ("Votre travail", "Réceptionniste IA", "Plus jamais un appel manqué, jour et nuit.",
     "/solutions/automatisation-operations/#essayer", "/media/accueil/sol-automatisation.webp", "50% 55%"),
    ("Votre travail", "Automatisations", "Soumissions, factures, stock et suivis : rien à recopier.",
     "/solutions/automatisation-operations/#bibliotheque", "/media/vision/lieu-entreprise.webp", "50% 50%"),
    ("Votre travail", "Comptes et accès", "Un compte par employé. Un départ coupe tout, d’un coup.",
     "/offre/", "/media/solutions/security-enterprise-lobby-v1.webp", "50% 55%"),
    ("Votre travail", "Rapport du matin", "Appels, ventes et alertes : votre entreprise résumée chaque matin.",
     "/solutions/automatisation-operations/#bibliotheque", "/media/vitrine/accueil/commerce-pme.webp", "50% 50%"),
    ("Votre travail", "Savoir de l’entreprise", "La bonne réponse, avec sa source, sans que rien sorte de vos murs.",
     "/solutions/ia-privee-entreprise/", "/media/solutions/ia-privee-connaissances.webp", "50% 50%"),
]
ENTREPRISE_BATIMENTS = [
    ("Vos bâtiments", "Sécurité intelligente", "Caméras, accès et alarme : un seul événement clair, pas vingt alertes.",
     "/solutions/securite-intelligente/", "/media/solutions/security-enterprise-delivery-v1.webp", "50% 50%"),
    ("Vos bâtiments", "Réseau et cybersécurité", "Votre réseau surveillé jour et nuit, les intrus bloqués.",
     "/solutions/reseau-resilience/", "/media/vitrine/plateforme/hub-armoire-technique.webp", "50% 50%"),
    ("Vos bâtiments", "Diagnostic & continuité", "La panne vue avant qu’elle arrête vos équipements.",
     "/solutions/diagnostic-care/", "/media/vitrine/plateforme/atelier-pme.webp", "50% 50%"),
    ("Vos bâtiments", "Environnements intelligents", "Éclairage, chauffage et énergie de vos locaux, réglés seuls.",
     "/solutions/environnements-intelligents/", "/media/accueil/lieu-entreprise.webp", "50% 50%"),
    ("Vos bâtiments", "Flotte et véhicules", "Vos véhicules de service : position, entretien et vol, sous votre œil.",
     "/solutions/mobilite/", "/media/solutions/security-enterprise-parking-v1.webp", "50% 50%"),
]
# JARVIS Cyber : les services de la famille « Vérifier, protéger, former » de l'offre (catalogue.SERVICES).
CYBER = [
    ("Vérifier", "Vérification de vos systèmes", "Caméras, accès, réseau, Wi-Fi et sauvegardes : ce qui est faible, avant qu’un autre le trouve.",
     "/solutions/cyber/#services", "/media/solutions/camera-front-entry-v1.webp", "50% 50%"),
    ("Vérifier", "Test d’intrusion réseau", "Une attaque autorisée, sur mandat écrit, puis la correction avec vous.",
     "/solutions/cyber/#services", "/media/vision/recherche-rust.webp", "60% 50%"),
    ("Vérifier", "Revue de votre exposition en ligne", "Ce qu’un fraudeur trouverait sur vous en une heure, retiré avant lui.",
     "/solutions/cyber/#services", "/media/concept/jarvis-earth-network-v1.jpg", "40% 50%"),
    ("Protéger", "Accompagnement Loi 25", "Registre, politiques, incidents et consentements : votre entreprise conforme.",
     "/solutions/cyber/#services", "/media/vitrine/confiance/sauvegarde-coffre.webp", "50% 50%"),
    ("Protéger", "Mise à niveau du réseau", "Zones séparées, mises à jour et sauvegardes testées, en une journée.",
     "/solutions/cyber/#services", "/media/vitrine/confiance/armoire-verrouillee.webp", "62% 50%"),
    ("Former", "Formation d’équipe", "Hameçonnage, mots de passe et accès : les bons réflexes.",
     "/solutions/cyber/#services", "/media/vision/lieu-entreprise.webp", "50% 50%"),
]


def tuiles():
    """Les trois divisions, en grandes photos."""
    return "".join(f"""<a class="dv3-t" href="{d['url']}" data-rev>
      <img src="{d['img']}" alt="" loading="lazy" style="object-position:{d['pos']}">
      <span class="dv3-in"><em>{d['num']} · {d['etat']}</em><b>{d['nom']}</b><small>{d['pour']}</small><span>{d['ligne']}</span><i>Découvrir ›</i></span>
    </a>""" for d in DIVISIONS)


def gamme(items):
    """La gamme d'une division : une carte par solution, une phrase chacune."""
    return "".join(f"""<a class="gam-c" href="{u}" data-rev>
      <img src="{img}" alt="" loading="lazy" style="object-position:{pos}">
      <span class="gam-b"><em{' class="is-v"' if k == 'Vision' else ''}>{k}</em><b>{n}</b><span>{l}</span><i>En savoir plus ›</i></span>
    </a>""" for k, n, l, u, img, pos in items)


def cartes(items):
    """Les mêmes cartes que la gamme, sans lien : sur la page de la division elle-même."""
    return "".join(f"""<div class="gam-c gam-fixe" data-rev>
      <img src="{img}" alt="" loading="lazy" style="object-position:{pos}">
      <span class="gam-b"><em>{k}</em><b>{n}</b><span>{l}</span></span>
    </div>""" for k, n, l, _u, img, pos in items)
