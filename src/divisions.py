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
     "url": "/solutions/#prive", "img": "/media/accueil/lieu-maison.webp"},
    {"id": "entreprise", "num": "02", "etat": "Ensuite", "nom": "JARVIS Entreprise",
     "pour": "Travailleurs autonomes, PME, fermes et commerces",
     "ligne": "Les appels, les tâches et l’information se gèrent seuls.",
     "url": "/solutions/#entreprise", "img": "/media/accueil/sol-automatisation.webp"},
    {"id": "cyber", "num": "03", "etat": "Maintenant", "nom": "JARVIS Cyber",
     "pour": "Toute maison ou entreprise, cliente ou non",
     "ligne": "Nous vérifions vos systèmes comme un pirate le ferait, puis nous corrigeons avec vous.",
     "url": "/solutions/cyber/", "img": "/media/accueil/sol-reseau.webp"},
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
ENTREPRISE = [
    ("Solution", "Automatisation d’entreprise", "Plus jamais un appel manqué. Les demandes circulent seules.",
     "/solutions/automatisation-operations/", "/media/accueil/sol-automatisation.webp", "50% 50%"),
    ("Solution", "IA privée pour entreprise", "La bonne réponse, avec sa source, sans que rien sorte de vos murs.",
     "/solutions/ia-privee-entreprise/", "/media/solutions/ia-privee-connaissances.webp", "50% 50%"),
    ("Par lieu", "Toute votre entreprise", "Les appels, le travail, les lieux et la protection, dans un seul système.",
     "/solutions/entreprise/", "/media/accueil/lieu-entreprise.webp", "50% 50%"),
    ("Par lieu", "Domotique pour ferme", "Tous les bâtiments sur un seul écran.",
     "/solutions/domotique-ferme-agricole/", "/media/accueil/lieu-ferme.webp", "50% 50%"),
]
# JARVIS Cyber : les services de la famille « Vérifier, protéger, former » de l'offre (catalogue.SERVICES).
CYBER = [
    ("Vérifier", "Vérification de vos systèmes", "Caméras, accès, réseau, Wi-Fi et sauvegardes : ce qui est faible, avant qu’un autre le trouve."),
    ("Vérifier", "Test d’intrusion réseau", "Une attaque autorisée, sur mandat écrit, puis la correction avec vous."),
    ("Vérifier", "Revue de votre exposition en ligne", "Ce qu’un fraudeur trouverait sur vous en une heure, retiré avant lui."),
    ("Protéger", "Accompagnement Loi 25", "Registre, politiques, incidents et consentements : votre entreprise conforme."),
    ("Protéger", "Mise à niveau du réseau", "Zones séparées, mises à jour et sauvegardes testées, en une journée."),
    ("Former", "Formation d’équipe", "Hameçonnage, mots de passe et accès : les bons réflexes."),
]


def tuiles():
    """Les trois divisions, en grandes photos."""
    return "".join(f"""<a class="dv3-t" href="{d['url']}" data-rev>
      <img src="{d['img']}" alt="" loading="lazy">
      <span class="dv3-in"><em>{d['num']} · {d['etat']}</em><b>{d['nom']}</b><small>{d['pour']}</small><span>{d['ligne']}</span><i>Découvrir ›</i></span>
    </a>""" for d in DIVISIONS)


def gamme(items):
    """La gamme d'une division : une carte par solution, une phrase chacune."""
    return "".join(f"""<a class="gam-c" href="{u}" data-rev>
      <img src="{img}" alt="" loading="lazy" style="object-position:{pos}">
      <span class="gam-b"><em{' class="is-v"' if k == 'Vision' else ''}>{k}</em><b>{n}</b><span>{l}</span><i>En savoir plus ›</i></span>
    </a>""" for k, n, l, u, img, pos in items)
