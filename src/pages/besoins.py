# Pages « par besoin » : une recherche réelle, une page (référencement local, novembre 2026).
# Elles complètent les sept solutions sans les répéter : chacune explique un projet complet
# (ce que ça comprend, pour qui, les limites, les questions) et renvoie aux solutions concernées.
# Rien d'inventé : aucun client, aucun chiffre, aucune installation réalisée n'est prétendue.
# Gabarit et blocs communs : src/pro.py. Styles : assets/demos/pro.css.

import pro


def _cartes(cartes):
    return "".join(
        f'<article class="card" data-rev><small>{k}</small><h3>{t}</h3><p>{p}</p></article>' for k, t, p in cartes
    )


def _rangs(rangs):
    return "".join(
        f"""<article class="frow{' flip' if i % 2 else ''}">
      <figure class="media" data-rev><img src="{img}" alt="{alt}" loading="lazy"></figure>
      <div data-rev>
        <p class="num">{k}</p>
        <h3>{t}</h3>
        <p class="res">{p}</p>
        <ul>{''.join(f'<li>{x}</li>' for x in pts)}</ul>
        <a class="pill ghost" href="{url}">{lien}</a>
      </div>
    </article>"""
        for i, (k, t, p, pts, img, alt, url, lien) in enumerate(rangs)
    )


def _limites(limites):
    return "".join(
        f'<div class="row" data-rev><i>{k}</i><div><h3>{t}</h3><p>{p}</p></div></div>' for k, t, p in limites
    )


def page(d):
    url = f"/solutions/{d['slug']}/"
    return {
        "url": url,
        "v2": True,
        "title": d["title"],
        "description": d["description"],
        "og_image": d["image"],
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
    <p class="eyebrow" data-rev>{d['eyebrow']}</p>
    <h1 data-rev>{d['h1']}</h1>
    <p class="lead" data-rev>{d['lead']}</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="/logiciel/">Voir le logiciel</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> {d['pour']}</p>
  </div>
</section>

<section class="sect" id="comprend" data-toc="Ce que ça comprend" aria-labelledby="comprend-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ce que ça comprend</p>
      <h2 id="comprend-titre" style="margin-top:1rem">{d['comprend_titre']}</h2>
    </div>
    <p data-rev>{d['comprend_intro']}</p>
  </div>
  <div class="cards">{_cartes(d['comprend'])}</div>
</section>

<section class="sect alt" id="concret" data-toc="Concrètement" aria-labelledby="concret-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Concrètement</p>
      <h2 id="concret-titre" style="margin-top:1rem">{d['concret_titre']}</h2>
    </div>
    <p data-rev>{d['concret_intro']}</p>
  </div>
  {_rangs(d['rangs'])}
</section>

<section class="sect" id="limites" data-toc="L’heure juste" aria-labelledby="limites-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">L’heure juste</p>
      <h2 id="limites-titre" style="margin-top:1rem">Ce que ce système fait,<br><em>et ce qu’il ne fait pas.</em></h2>
    </div>
    <p data-rev>Mieux vaut le savoir avant. Voyez aussi <a href="/a-propos/#comment-on-travaille">comment
    on travaille</a> et <a href="/a-propos/#engagements">nos engagements</a>.</p>
  </div>
  <div class="rows">{_limites(d['limites'])}</div>
</section>

{pro.faq_section(d['faq'], d['faq_eyebrow'], "Ce qu’on nous demande <em>le plus souvent.</em>", toc="Questions")}

<section class="sect alt pro-zone-s" aria-labelledby="ou-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Où</p>
      <h2 id="ou-titre" style="margin-top:1rem">En Montérégie<br><em>et aux environs.</em></h2>
    </div>
    <p data-rev>On se déplace à partir de la région de Saint-Hyacinthe. Chaque ville de la
    <a href="/regions/">zone desservie</a> a sa page.</p>
  </div>
  <div class="chiprow pro-zone" data-rev>{pro.zone_liens()}</div>
</section>

<section class="cta">
  <h2 data-rev>{d['cta']}</h2>
  <p data-rev>Décrivez votre lieu en quelques lignes, ou laissez votre nom pour rester informé.
  Aucune pression.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a>
  <a class="pill ghost" href="/questions/">Questions avant d’appeler</a></div>
</section>
""",
    }


MAISON = {
    "slug": "maison-intelligente-cle-en-main",
    "nom": "Maison intelligente clé en main",
    "genre": "Domotique résidentielle clé en main",
    "title": "Maison intelligente clé en main en Montérégie | JARVIS",
    "description": (
        "Une maison intelligente pensée, installée et expliquée par un seul intégrateur : "
        "éclairage, chauffage, réseau, caméras et IA privée. Maison existante ou neuve."
    ),
    "image": "/media/offre/maison.webp",
    "eyebrow": "Maison intelligente clé en main · Montérégie",
    "h1": "Une maison intelligente, <em>clé en main.</em>",
    "lead": (
        "Vous n’avez pas à choisir des marques, à comparer des protocoles ni à tout configurer. "
        "On regarde votre maison, on dessine le système, on l’installe et on vous montre comment "
        "vous en servir. Un seul intégrateur, un seul système, une seule application."
    ),
    "pour": "Propriétaires d’une maison, d’un condo ou d’un chalet, existant ou en construction",
    "comprend_titre": "Tout ce qu’il faut,<br><em>rien à assembler vous-même.</em>",
    "comprend_intro": (
        "« Clé en main » veut dire qu’une seule personne répond de l’ensemble : le plan, le "
        "matériel, les réglages et la formation."
    ),
    "comprend": [
        ("Le plan", "Un système dessiné pour votre maison",
         "Pièce par pièce : ce qu’on relie, ce qu’on ajoute, ce qui peut attendre. Remis par écrit."),
        ("Le cœur", "Le Hub JARVIS",
         "Un petit boîtier silencieux qui fait tourner la maison sur place, même sans Internet."),
        ("Le confort", "Éclairage, chauffage et ambiances",
         "Matin, Soirée, Nuit, Absent : des ambiances réglées avec vous, modifiables en tout temps."),
        ("La fondation", "Un réseau et un Wi-Fi solides",
         "Une couverture complète et un réseau séparé pour les objets connectés."),
        ("La tranquillité", "Caméras, serrures et capteurs réunis",
         "Fuite d’eau, porte restée ouverte, livraison : des événements clairs, des images gardées chez vous."),
        ("La remise", "Formation et dossier de la maison",
         "Chaque membre de la famille apprend à s’en servir. Le plan et vos accès vous sont remis."),
    ],
    "concret_titre": "Maison existante<br><em>ou construction neuve.</em>",
    "concret_intro": (
        "Le point de départ change la méthode, pas le résultat. Voici comment on aborde chaque cas."
    ),
    "rangs": [
        ("Maison existante", "On part de ce que vous avez.",
         "La plupart des maisons du Québec se chauffent à l’électricité, souvent avec des plinthes : "
         "des thermostats connectés et des modules sans fil suffisent souvent à tout relier, sans ouvrir "
         "les murs.",
         ["Inventaire de vos appareils et de vos applications actuelles",
          "Modules discrets derrière les interrupteurs existants",
          "Travaux électriques confiés à un maître électricien, au besoin"],
         "/media/vitrine/accueil/maison-familiale.webp",
         "Maison familiale en soirée, fenêtres éclairées (photo d’illustration)",
         "/solutions/environnements-intelligents/", "La domotique résidentielle en détail"),
        ("Construction neuve ou rénovation majeure", "On prévoit avant de fermer les murs.",
         "C’est le meilleur moment pour passer les bons câbles au bon endroit : réseau, points d’accès "
         "Wi-Fi, caméras, écran mural. On remet un plan que votre entrepreneur et votre électricien "
         "peuvent suivre.",
         ["Plan de câblage réseau et emplacement de l’armoire technique",
          "Emplacements prévus pour les capteurs, caméras et écrans",
          "Coordination avec l’entrepreneur et l’électricien du chantier"],
         "/media/vitrine/plateforme/hub-armoire-technique.webp",
         "Armoire technique bien rangée avec le Hub et le câblage réseau (photo d’illustration)",
         "/solutions/reseau-resilience/", "Le réseau, fondation du système"),
    ],
    "limites": [
        ("01 · Hiver", "Pensé pour le climat d’ici.",
         "Alerte de gel dans une pièce ou un chalet, détection de fuite d’eau, suivi du chauffage pendant "
         "une absence. Pendant une panne de courant, seuls les appareils alimentés par une batterie ou une "
         "génératrice continuent de fonctionner."),
        ("02 · Énergie", "Aider à consommer mieux, sans promettre un montant.",
         "Le système peut abaisser le chauffage quand la maison est vide et déplacer certaines charges hors "
         "des heures de pointe d’hiver. Les économies dépendent de votre maison et de votre tarif "
         "d’électricité : on ne promet aucun chiffre."),
        ("03 · Métiers", "Chacun son métier.",
         "L’électricité est faite par un maître électricien. La pose d’alarmes, de caméras de surveillance "
         "et de contrôles d’accès est encadrée par la Loi sur la sécurité privée : quand un permis est "
         "requis, elle est faite par un installateur qui le détient. JARVIS relie le tout."),
        ("04 · Démarrage", "Une entreprise en phase de lancement.",
         "On choisit quelques premiers projets et on avance avec soin. Le logiciel JARVIS est en "
         "construction; la visite montre honnêtement ce qui fonctionne aujourd’hui."),
    ],
    "faq_eyebrow": "Questions fréquentes · Maison intelligente",
    "faq": [
        ("Qu’est-ce qu’une maison intelligente « clé en main »?",
         "Un projet où un seul intégrateur s’occupe de tout : le plan, le choix du matériel, "
         "l’installation, les réglages et la formation. Vous n’avez pas à assembler vous-même des "
         "appareils et des applications de marques différentes."),
        ("Combien coûte une maison intelligente?",
         "Ça dépend de la taille de la maison, de ce qui est déjà en place et de ce que vous voulez "
         "relier. Le prix est toujours remis par écrit, ligne par ligne, après une visite gratuite. Le "
         "<a href=\"/catalogue/\">catalogue</a> donne une idée des composantes."),
        ("Est-ce que tout doit être fait en une seule fois?",
         "Non. On commence souvent par une partie, comme l’éclairage et le chauffage, puis le reste "
         "s’ajoute au même système sans tout refaire."),
        ("Que se passe-t-il si je vends la maison?",
         "Le système est documenté : le plan, la liste des appareils et les accès peuvent être remis au "
         "nouveau propriétaire. Vous pouvez aussi faire retirer ce qui vous appartient."),
        ("Mes données restent-elles privées?",
         "Oui. Le système fonctionne sur le Hub, dans votre maison. Rien n’est vendu, et rien ne sort "
         "sans votre accord."),
    ],
    "cta": "Votre maison,<br><span>plus simple à vivre.</span>",
}


FERME = {
    "slug": "domotique-ferme-agricole",
    "nom": "Domotique pour ferme et bâtiments agricoles",
    "genre": "Domotique agricole",
    "title": "Domotique pour ferme et bâtiments agricoles | JARVIS",
    "description": (
        "Températures, pannes de courant, eau, portes et réseau entre les bâtiments de la "
        "ferme, sur un seul écran. Un système local qui fonctionne sans Internet, en Montérégie."
    ),
    "image": "/media/offre/ferme.webp",
    "eyebrow": "Domotique agricole · Montérégie",
    "h1": "La ferme et ses bâtiments, <em>sur un seul écran.</em>",
    "lead": (
        "Une ferme, c’est plusieurs bâtiments, des équipements qui ne doivent pas s’arrêter et peu de "
        "temps pour tout surveiller. On relie les mesures qui comptent dans un seul système, installé "
        "à la ferme, qui vous prévient clairement quand quelque chose sort de la normale."
    ),
    "pour": "Fermes laitières, porcines, avicoles, de grandes cultures et écuries",
    "comprend_titre": "Savoir ce qui se passe,<br><em>sans faire le tour des bâtiments.</em>",
    "comprend_intro": (
        "On commence par ce qui vous inquiète le plus, souvent une température ou une panne de "
        "courant, puis on ajoute le reste."
    ),
    "comprend": [
        ("Températures", "Bâtiments, réservoirs et chambres froides",
         "Des capteurs suivent la température et vous alertent dès qu’elle sort de la plage que vous avez fixée."),
        ("Courant", "Panne détectée, génératrice suivie",
         "Vous savez qu’un bâtiment a perdu le courant, et si la génératrice a bien pris le relais."),
        ("Eau", "Puits, pompes et fuites",
         "Une pompe qui démarre trop souvent ou une fuite se voit tôt, avant le dégât."),
        ("Accès", "Portes, barrières et visiteurs",
         "Quelle porte est restée ouverte, qui est entré dans quel bâtiment et quand."),
        ("Réseau", "Internet dans tous les bâtiments",
         "Un lien entre la maison, l’étable et le garage, puis un Wi-Fi qui couvre où vous travaillez."),
        ("Équipe", "Les bonnes alertes aux bonnes personnes",
         "Le propriétaire, la relève et les employés reçoivent chacun ce qui les concerne."),
    ],
    "concret_titre": "Du bâtiment<br><em>jusqu’à votre téléphone.</em>",
    "concret_intro": (
        "Deux exemples de ce qu’un tel système peut suivre. Les écrans montrés sur le site utilisent "
        "des données d’exemple."
    ),
    "rangs": [
        ("Exemple · bâtiment d’élevage", "Une alerte claire, pas dix notifications.",
         "Température, ventilation, courant et portes sont lus ensemble. Au lieu d’une série d’alarmes, "
         "vous recevez une phrase : ce qui a changé, où et depuis quand.",
         ["Seuils réglés avec vous, pour chaque bâtiment",
          "Alerte par l’application, même quand Internet est coupé à la ferme si un lien de secours est prévu",
          "Historique des mesures pour comprendre ce qui s’est passé"],
         "/media/env/ferme/laitier-interieur.webp",
         "Intérieur d’une étable laitière moderne (photo d’illustration)",
         "/solutions/environnements-intelligents/", "Voir la démonstration de la ferme"),
        ("Exemple · réservoir à lait et réfrigération", "Voir venir la panne.",
         "Une courbe de refroidissement qui s’allonge ou un compresseur qui force se remarquent avant "
         "le bris. Le système prépare un dossier pour le technicien, avec les mesures.",
         ["Suivi de la température et des cycles",
          "Écart signalé par rapport aux jours précédents",
          "Dossier prêt à transmettre au technicien en réfrigération"],
         "/media/diagnostic/tank-lait.webp",
         "Réservoir à lait en acier inoxydable dans une laiterie de ferme (photo d’illustration)",
         "/solutions/diagnostic-care/", "Le diagnostic en détail"),
    ],
    "limites": [
        ("01 · Complément", "Il s’ajoute à vos systèmes, il ne les remplace pas.",
         "Vos contrôleurs de ventilation, votre robot de traite et l’alarme exigée par votre assureur "
         "restent en place. JARVIS se relie à ce qui peut l’être et ajoute une vue d’ensemble."),
        ("02 · Local", "Il fonctionne à la ferme, même sans Internet.",
         "Les mesures et les règles tournent sur le Hub, sur place. Pour recevoir une alerte à distance "
         "quand Internet est coupé, il faut prévoir un lien de secours, cellulaire ou par satellite."),
        ("03 · Animaux", "Aucune décision à votre place.",
         "Le système mesure et prévient. Il ne remplace ni votre jugement, ni votre vétérinaire, ni vos "
         "protocoles de biosécurité."),
        ("04 · Démarrage", "Une entreprise en phase de lancement.",
         "On choisit quelques premiers projets. Si votre ferme vous semble un bon terrain, écrivez-nous : "
         "on vous dira honnêtement ce qui est possible aujourd’hui."),
    ],
    "faq_eyebrow": "Questions fréquentes · Ferme",
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
        ("Le système résiste-t-il à la poussière, à l’humidité et au froid?",
         "Le Hub s’installe dans un endroit propre et tempéré, comme le bureau de la ferme. Dans les "
         "bâtiments, on choisit des capteurs et des boîtiers prévus pour ces conditions."),
        ("Quelles fermes desservez-vous?",
         "Les fermes de la Montérégie et des environs, à partir de la région de Saint-Hyacinthe : "
         "production laitière, porcine, avicole, grandes cultures et écuries."),
    ],
    "cta": "Votre ferme,<br><span>d’un seul coup d’œil.</span>",
}


IA = {
    "slug": "ia-privee-entreprise",
    "nom": "IA privée pour entreprise",
    "genre": "Intelligence artificielle locale pour entreprise",
    "title": "IA privée pour entreprise, hébergée chez vous | JARVIS",
    "description": (
        "Un assistant d’IA qui connaît les documents de votre entreprise "
        "et fonctionne dans vos murs. Vos données ne partent pas chez un fournisseur. Loi 25."
    ),
    "image": "/media/vitrine/plateforme/atelier-pme.webp",
    "eyebrow": "IA privée pour entreprise · Montérégie",
    "h1": "Une IA pour votre entreprise, <em>dans vos murs.</em>",
    "lead": (
        "Vos employés posent une question en français; l’assistant répond à partir de vos propres "
        "documents et montre d’où vient la réponse. Il fonctionne sur un boîtier installé dans "
        "l’entreprise : contrats, soumissions et dossiers clients ne partent pas chez un fournisseur d’IA."
    ),
    "pour": "PME, bureaux de professionnels, ateliers et commerces qui ont beaucoup de documents",
    "comprend_titre": "Une IA utile,<br><em>qui reste chez vous.</em>",
    "comprend_intro": (
        "La différence avec un service d’IA en ligne : l’endroit où vos données se trouvent, et qui "
        "y a accès."
    ),
    "comprend": [
        ("Le matériel", "Un Hub dimensionné pour l’IA",
         "Installé dans vos locaux et entretenu par nous. Sa puissance se choisit selon votre équipe."),
        ("Les sources", "Vos documents, à leur place",
         "Procédures, contrats, fiches techniques, soumissions : l’assistant les lit là où ils sont déjà."),
        ("Les réponses", "Toujours avec la source",
         "Chaque réponse montre le passage qui la justifie. On vérifie en un clic."),
        ("Les droits", "Chacun voit ce qu’il a le droit de voir",
         "L’assistant respecte les accès de chaque employé. Les dossiers de la direction restent à la direction."),
        ("Le journal", "Une trace de ce qui est consulté",
         "Qui a demandé quoi et quelles sources ont servi, pour répondre aux exigences de la Loi 25."),
        ("La formation", "Votre équipe apprend à s’en servir",
         "Comment poser une bonne question, quand vérifier, quoi ne pas lui confier."),
    ],
    "concret_titre": "À quoi ça sert,<br><em>un mardi matin.</em>",
    "concret_intro": (
        "Deux usages simples, présentés comme des exemples. La démonstration du site utilise des "
        "données d’exemple."
    ),
    "rangs": [
        ("Exemple · retrouver", "« Quelle garantie avons-nous donnée à ce client? »",
         "Au lieu de fouiller dans les dossiers, l’employé pose la question. L’assistant cite le contrat "
         "et la clause, et indique s’il n’a rien trouvé plutôt que d’inventer.",
         ["Recherche dans les documents que l’employé a le droit de voir",
          "Passage exact affiché à côté de la réponse",
          "Aucune réponse sans source"],
         "/media/solutions/ia-privee-connaissances.webp",
         "Poste de travail affichant un assistant qui cite ses sources (image d’illustration)",
         "/solutions/ia-privee-connaissances/", "Essayer la démonstration de l’IA privée"),
        ("Exemple · préparer", "Un brouillon, puis votre accord.",
         "L’assistant peut préparer une réponse à un courriel ou un résumé de dossier. Rien ne part sans "
         "qu’une personne ait relu et approuvé.",
         ["Brouillons à partir de vos modèles",
          "Approbation humaine avant tout envoi",
          "Peut se relier à l’automatisation de vos demandes"],
         "/media/solutions/jarvis-enterprise-operations-v1.webp",
         "Bureau d’entreprise avec un tableau de bord sombre sur grand écran (image d’illustration)",
         "/solutions/automatisation-operations/", "L’automatisation d’entreprise en détail"),
    ],
    "limites": [
        ("01 · Erreurs", "Une IA peut se tromper.",
         "C’est pourquoi chaque réponse montre sa source et qu’aucune action ne part sans approbation. "
         "L’assistant aide à trouver et à préparer; il ne décide pas."),
        ("02 · Puissance", "Un modèle local n’est pas le plus gros modèle du monde.",
         "Il est très bon pour chercher, résumer et rédiger à partir de vos documents. Pour une tâche qui "
         "demande un grand modèle en ligne, vous pouvez l’autoriser au cas par cas, en sachant ce qui sort."),
        ("03 · Loi 25", "Un outil qui aide, pas un avis juridique.",
         "Garder les renseignements personnels dans vos murs simplifie vos obligations, mais ne les "
         "remplace pas. Votre responsable de la protection des renseignements personnels reste maître des règles."),
        ("04 · Démarrage", "Une entreprise en phase de lancement.",
         "Le logiciel JARVIS est en construction et on choisit quelques premiers projets. La rencontre "
         "montre honnêtement ce qui fonctionne aujourd’hui."),
    ],
    "faq_eyebrow": "Questions fréquentes · IA privée en entreprise",
    "faq": [
        ("Qu’est-ce qu’une IA privée pour entreprise?",
         "Une intelligence artificielle installée sur du matériel qui se trouve dans vos locaux. Elle "
         "répond à partir de vos documents, et ceux-ci ne sont pas envoyés à un fournisseur d’IA en ligne."),
        ("Quelle différence avec un assistant d’IA en ligne?",
         "Avec un service en ligne, vos questions et vos documents passent par les serveurs d’un "
         "fournisseur. Avec une IA privée, le traitement se fait chez vous, selon les droits d’accès de "
         "chaque employé."),
        ("Est-ce conforme à la Loi 25?",
         "Garder les renseignements personnels sur place, limiter les accès et tenir un journal des "
         "consultations va dans le sens de la Loi 25. La conformité de l’entreprise dépend toutefois de "
         "l’ensemble de vos pratiques, pas d’un seul outil."),
        ("Nos documents doivent-ils être déplacés ou réorganisés?",
         "Non. L’assistant lit les documents là où ils se trouvent déjà, avec les autorisations que vous "
         "lui donnez. Un peu de ménage améliore quand même les réponses."),
        ("Fonctionne-t-elle en français?",
         "Oui. L’assistant comprend et répond en français, et peut lire des documents en anglais."),
    ],
    "cta": "Vos documents,<br><span>enfin faciles à interroger.</span>",
}


PAGES = [page(MAISON), page(FERME), page(IA)]
