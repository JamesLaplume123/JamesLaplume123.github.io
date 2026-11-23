# Pages « par besoin » : une recherche réelle, une page (refonte « essentiel », novembre 2026).
# Chacune dit une idée, une fois : le titre et une phrase, trois points, trois questions repliées,
# un lien vers la solution concernée et un bouton. Rien d'inventé : aucun client, aucun chiffre,
# aucune installation réalisée n'est prétendue. Aucune mention de lieu.
# Blocs communs : src/pro.py. Styles : assets/demos/pro.css.

import pro
from pages import catalogue as offre


def page(d):
    url = f"/solutions/{d['slug']}/"
    cartes = "".join(f'<article class="card" data-rev><h3>{t}</h3><p>{p}</p></article>' for t, p in d["comprend"])
    # Sous les cartes : la suite (un lien, ou plusieurs pour la page Entreprise), puis l'offre.
    suites = d["suite"] if isinstance(d["suite"], list) else [d["suite"], ("/offre/", "Voir l’offre")]
    liens = "\n  ".join(f'<a href="{u}">{t} <i aria-hidden="true">→</i></a>' for u, t in suites)
    return {
        "url": url,
        "v2": True,
        "title": d["title"],
        "description": d["description"],
        "og_image": d["image"],
        "public": d.get("public", ""),
        "assets": ["pro"],
        "schema": [
            pro.ld_service(d["nom"], d["description"], url, d["genre"]),
            pro.ld_faq(d["faq"]),
        ],
        "content": f"""
<section class="band top">
  <div class="bg"><img src="{d['image']}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil(url)}
    <h1 data-rev>{d['h1']}</h1>
    <p class="lead" data-rev>{d['lead']}</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
    </div>
  </div>
</section>

<section class="sect" aria-label="Ce que ça comprend">
  <div class="cards">{cartes}</div>
  <p class="pro-suite" data-rev>{liens}</p>
</section>

{pro.faq_section(d['faq'], d['nom'], "Questions fréquentes")}

<section class="cta">
  <h2 data-rev>{d['cta']}</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
    }


MAISON = {
    "slug": "maison-intelligente-cle-en-main",
    "nom": "Maison intelligente clé en main",
    "genre": "Domotique résidentielle clé en main",
    "title": "Maison intelligente clé en main, sans rien assembler | JARVIS",
    "description": (
        "Une maison intelligente pensée, installée et expliquée par une seule entreprise : "
        "éclairage, chauffage, réseau, caméras et IA privée. Maison existante ou neuve."
    ),
    "image": "/media/offre/maison.webp",
    "h1": "Une maison intelligente, <em>clé en main.</em>",
    "lead": "On regarde votre maison, on dessine le système, on l’installe et on vous montre comment vous en servir.",
    "comprend": [
        ("Un plan écrit", "Pièce par pièce : ce qu’on relie, ce qu’on ajoute, ce qui peut attendre."),
        ("Un seul système", "Éclairage, chauffage, réseau, caméras et serrures dans une seule application."),
        ("La formation", "Chaque membre de la famille apprend à s’en servir; le plan et vos accès vous sont remis."),
    ],
    "suite": ("/solutions/environnements-intelligents/", "Essayer la démonstration de la domotique"),
    "faq": [
        ("Qu’est-ce qu’une maison intelligente « clé en main »?",
         "Un projet où une seule entreprise s’occupe de tout : le plan, le choix du matériel, "
         "l’installation, les réglages et la formation. Vous n’avez pas à assembler vous-même des "
         "appareils et des applications de marques différentes."),
        ("Combien coûte une maison intelligente?",
         "Ça dépend de la taille de la maison, de ce qui est déjà en place et de ce que vous voulez "
         "relier. Le prix est toujours remis par écrit, ligne par ligne, après une visite gratuite." + pro.VOIR_CATALOGUE),
        ("Est-ce que tout doit être fait en une seule fois?",
         "Non. On commence souvent par une partie, comme l’éclairage et le chauffage, puis le reste "
         "s’ajoute au même système sans tout refaire."),
    ],
    "cta": "Votre maison,<br><span>plus simple à vivre.</span>",
}


FERME = {
    "slug": "domotique-ferme-agricole",
    "public": "entreprise",
    "nom": "Domotique pour ferme et bâtiments agricoles",
    "genre": "Domotique agricole",
    "title": "Domotique pour ferme et bâtiments agricoles | JARVIS",
    "description": (
        "Températures, pannes de courant, eau, portes et réseau entre les bâtiments de la "
        "ferme, sur un seul écran. Un système local qui fonctionne même sans Internet."
    ),
    "image": "/media/offre/ferme.webp",
    "h1": "La ferme et ses bâtiments, <em>sur un seul écran.</em>",
    "lead": "Les mesures qui comptent, réunies dans un seul système qui vous prévient quand quelque chose sort de la normale.",
    "comprend": [
        ("Températures et courant", "Bâtiments, réservoirs, chambres froides : une alerte dès qu’une mesure sort de la plage fixée, ou qu’un bâtiment perd le courant."),
        ("Eau et accès", "Une pompe qui démarre trop souvent, une fuite, une porte restée ouverte : vous le voyez tôt."),
        ("Internet dans tous les bâtiments", "Un lien entre la maison, l’étable et le garage, puis un Wi-Fi là où vous travaillez."),
    ],
    "suite": ("/solutions/environnements-intelligents/", "Voir la démonstration de la ferme"),
    "faq": [
        ("Qu’est-ce que la domotique peut faire pour une ferme?",
         "Réunir sur un seul écran les mesures importantes de vos bâtiments : températures, courant, eau, "
         "portes et état du réseau. Vous êtes prévenu clairement quand quelque chose sort de la normale, "
         "sans faire le tour des bâtiments."),
        ("Est-ce que ça remplace mon système d’alarme de ventilation?",
         "Non. Les contrôleurs spécialisés et les alarmes exigées par votre assureur restent en place. "
         "JARVIS s’y ajoute pour réunir l’information et garder l’historique."),
        ("Comment avoir Internet dans l’étable ou le garage?",
         "On relie les bâtiments entre eux, par un câble enterré, de la fibre ou un lien sans fil selon "
         "la distance, puis on installe un point d’accès Wi-Fi dans chaque bâtiment où c’est utile."),
    ],
    "cta": "Votre ferme,<br><span>d’un seul coup d’œil.</span>",
}


# Toute l'entreprise (23 novembre 2026). La porte « Entreprise » menait à l'IA privée seulement, alors que
# Maison et Ferme couvrent tout le lieu. Six cartes, dans l'ordre où un propriétaire y pense; chacune est
# déjà dans l'offre (Réceptionniste IA, bibliothèque d'automatisations, Socle Entreprise, extensions).
# Le détail reste où il est : la démonstration, les secteurs et la bibliothèque sur la page Automatisation
# d'entreprise, les trois exemples pour commencer sur la page L'offre.
# Chaque carte nomme la pièce de l'offre qui la porte, avec les mots de l'offre (pages/catalogue.py) :
# on doit voir d'un coup d'œil ce que JARVIS offre à une entreprise.
N_AUTOS = sum(len(items) for _, items in offre.AUTOMATISATIONS)
ENTREPRISE = {
    "slug": "entreprise",
    "public": "entreprise",
    "nom": "JARVIS pour l’entreprise",
    "genre": "Système privé de gestion et de sécurité pour entreprise",
    "title": "JARVIS pour votre entreprise : un seul système privé",
    "description": (
        "JARVIS répond au téléphone, fait les suivis, relie vos outils et protège vos lieux et votre "
        "réseau. Toute l’entreprise dans un seul système privé, installé chez vous."
    ),
    "image": "/media/accueil/film-entreprise.webp",
    "h1": "Toute votre entreprise, <em>dans un seul système.</em>",
    "lead": "JARVIS répond au téléphone, fait les suivis, surveille vos lieux et votre réseau, et vous fait rapport.",
    "comprend": [
        ("Les appels", f"La {offre.ENT_RECEP['nom']} répond jour et nuit : messages, rendez-vous, rappels, urgences transférées."),
        ("Le travail", f"{N_AUTOS} automatisations prêtes à activer : soumissions, factures, stock, rapports. Rien à recopier."),
        ("Les gens", f"Le {offre.ENT_SOCLE['nom']} : un compte par employé, relié à votre annuaire. Un départ coupe tout d’un coup."),
        ("Le savoir", "L’IA privée connaît vos documents et vos procédures, et montre toujours sa source."),
        ("Les lieux", "Environnements, Diagnostic et Mobilité : bâtiments, équipements, énergie et véhicules, dans une seule application."),
        ("La protection", "Sécurité et Réseau : caméras, accès, alarme et réseau, surveillés ensemble."),
    ],
    "suite": [
        ("/solutions/automatisation-operations/#essayer", "Essayer la réceptionniste"),
        ("/solutions/automatisation-operations/#votre-secteur", "Trouver mon secteur"),
        ("/solutions/ia-privee-entreprise/", "L’IA privée pour entreprise"),
        ("/offre/#composer", "Composer pour mon entreprise"),
    ],
    "faq": [
        ("Par où commencer?",
         "Par le problème qui vous coûte le plus cher : les appels manqués, les suivis oubliés ou la "
         "sécurité. La page L’offre propose trois exemples selon la taille de l’entreprise; le reste "
         "s’ajoute au mois, quand vous en voyez le gain."),
        ("Jusqu’où JARVIS agit-il seul?",
         "C’est vous qui le décidez, domaine par domaine : il voit, il avertit, il propose, il agit avec "
         "votre accord, ou il agit selon vos règles et vous rend compte. Rien de sensible ne part sans "
         "l’accord d’une personne."),
        ("Dois-je changer mes logiciels ou mon annuaire?",
         "En général, non. JARVIS se relie aux outils que vous utilisez déjà (courriel, agenda, "
         "téléphonie, comptabilité) et à l’annuaire de votre entreprise (Microsoft 365, Active "
         "Directory). Il ne les remplace pas et ne gère pas vos postes de travail."),
    ],
    "cta": "Votre entreprise,<br><span>sans rien laisser tomber.</span>",
}


IA = {
    "slug": "ia-privee-entreprise",
    "public": "entreprise",
    "nom": "IA privée pour entreprise",
    "genre": "Intelligence artificielle locale pour entreprise",
    "title": "IA privée pour entreprise, hébergée chez vous | JARVIS",
    "description": (
        "Un assistant d’IA qui connaît les documents de votre entreprise "
        "et fonctionne dans vos murs. Vos données ne partent pas chez un fournisseur. Loi 25."
    ),
    "image": "/media/vitrine/plateforme/atelier-pme.webp",
    "h1": "Une IA pour votre entreprise, <em>dans vos murs.</em>",
    "lead": "Vos employés posent une question; l’assistant répond à partir de vos documents, montre sa source, et rien ne part chez un fournisseur d’IA.",
    "comprend": [
        ("Vos documents, à leur place", "Procédures, contrats, soumissions : l’assistant les lit là où ils sont déjà."),
        ("Toujours avec la source", "Chaque réponse montre le passage qui la justifie. On vérifie en un clic."),
        ("Chacun ses droits", "L’assistant respecte les accès de chaque employé et garde une trace de ce qui est consulté."),
    ],
    "suite": ("/solutions/ia-privee-connaissances/", "Essayer la démonstration de l’IA privée"),
    "faq": [
        ("Qu’est-ce qu’une IA privée pour entreprise?",
         "Une intelligence artificielle installée sur du matériel qui se trouve dans vos locaux. Elle "
         "répond à partir de vos documents, et ceux-ci ne sont pas envoyés à un fournisseur d’IA en ligne."),
        ("Est-ce conforme à la Loi 25?",
         "Garder les renseignements personnels sur place, limiter les accès et tenir un journal des "
         "consultations va dans le sens de la Loi 25. La conformité de l’entreprise dépend toutefois de "
         "l’ensemble de vos pratiques, pas d’un seul outil."),
        ("Une IA peut-elle se tromper?",
         "Oui. C’est pourquoi chaque réponse montre sa source et qu’aucune action ne part sans "
         "l’approbation d’une personne. L’assistant aide à trouver et à préparer; il ne décide pas."),
    ],
    "cta": "Vos documents,<br><span>enfin faciles à interroger.</span>",
}


PAGES = [page(MAISON), page(FERME), page(ENTREPRISE), page(IA)]
