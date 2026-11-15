# Pages locales : /regions/ et une page par ville de la zone desservie (référencement local).
# Chaque page est écrite pour sa ville : réalités locales vérifiables (MRC, habitat, agriculture,
# routes, hiver), exemples de projets présentés comme des exemples, questions locales.
# Rien d'inventé : aucune installation réalisée n'est prétendue dans ces villes; les distances
# sont approximatives et partent de Saint-Hyacinthe. En cas de doute, le texte reste général.
# Blocs communs : src/pro.py. Styles : assets/demos/pro.css.

import pro
from config import ZONE

NOMS = dict(ZONE)

S = "/solutions/"
DOMO, SECU, RESEAU, IA, AUTO, DIAG, MOB = (
    S + "environnements-intelligents/", S + "securite-intelligente/", S + "reseau-resilience/",
    S + "ia-privee-connaissances/", S + "automatisation-operations/", S + "diagnostic-care/", S + "mobilite/",
)
MAISON, FERME, IA_PME = (
    S + "maison-intelligente-cle-en-main/", S + "domotique-ferme-agricole/", S + "ia-privee-entreprise/",
)

VILLES = [
    {
        "slug": "saint-hyacinthe",
        "lieu": "Saint-Hyacinthe",
        "mrc": "MRC des Maskoutains",
        "title": "Domotique et systèmes intelligents à Saint-Hyacinthe | JARVIS",
        "description": (
            "Intégrateur de systèmes intelligents basé dans la région de Saint-Hyacinthe : "
            "domotique, réseau, caméras et IA privée pour maisons, fermes et PME maskoutaines."
        ),
        "image": "/media/vitrine/a-propos/atelier-saint-hyacinthe.webp",
        "h1": "Systèmes intelligents à Saint-Hyacinthe. <em>Ici, c’est chez nous.</em>",
        "lead": (
            "JARVIS Private Systems est basé dans la région de Saint-Hyacinthe. Maisons, fermes et "
            "entreprises de la MRC des Maskoutains sont nos voisines : on se déplace chez vous, sur "
            "rendez-vous."
        ),
        "route": ("Sur place", "Notre base. Une visite se planifie sur rendez-vous, selon vos disponibilités."),
        "realites": [
            ("Agroalimentaire", "Une ville tournée vers l’agriculture.",
             "Saint-Hyacinthe se présente comme une technopole agroalimentaire, avec sa faculté de "
             "médecine vétérinaire et son institut de technologie agroalimentaire. Autour de la ville, "
             "les terres de la plaine portent surtout du maïs, du soya et des élevages. Une bonne part "
             "des demandes vient donc de fermes et d’entreprises liées à l’alimentation."),
            ("Habitat", "Du centre ancien aux quartiers récents.",
             "Le centre-ville, près de la rivière Yamaska, compte des maisons et des immeubles anciens "
             "où l’on évite d’ouvrir les murs : les modules sans fil y sont précieux. Les quartiers plus "
             "récents et les rangs autour offrent de l’espace pour un réseau et des bâtiments reliés."),
            ("Verglas", "La panne de 1998 n’a pas été oubliée.",
             "En janvier 1998, Saint-Hyacinthe formait avec Granby et Saint-Jean-sur-Richelieu le "
             "« triangle noir » de la tempête de verglas; certains secteurs ont passé des semaines sans "
             "électricité. Prévoir ce qui doit continuer pendant une panne fait partie de chaque plan."),
        ],
        "projets": [
            ("Exemple · maison", "Chauffage et éclairage d’un bungalow", DOMO,
             "Des thermostats connectés pour les plinthes, quelques ambiances et une alerte de gel au sous-sol."),
            ("Exemple · ferme", "Un rang, trois bâtiments", FERME,
             "Températures, courant et portes de chaque bâtiment réunis, avec Internet jusqu’à l’étable."),
            ("Exemple · PME", "Un commerce du centre-ville", AUTO,
             "Les appels pris même quand tout le monde est occupé, et les demandes classées sans ressaisie."),
        ],
        "faq": [
            ("Où se trouve JARVIS Private Systems?",
             "L’entreprise est basée dans la région de Saint-Hyacinthe, en Montérégie. Il n’y a pas de "
             "boutique : on se déplace chez vous, sur rendez-vous."),
            ("Vous déplacez-vous dans les municipalités autour de Saint-Hyacinthe?",
             "Oui. Toute la MRC des Maskoutains est à courte distance, par exemple Sainte-Rosalie, "
             "Saint-Dominique, Saint-Pie, Saint-Liboire, La Présentation ou Saint-Damase."),
            ("Faites-vous des installations dans les fermes de la région?",
             "C’est un des usages prévus : suivre les bâtiments, le courant, l’eau et le réseau d’une "
             "ferme sur un seul écran. L’entreprise est en phase de lancement et choisit quelques "
             "premiers projets."),
            ("Que se passe-t-il pendant une panne de courant?",
             "Ce qui est branché sur une batterie ou une génératrice continue. On voit avec vous quels "
             "appareils doivent tenir : le Hub, le réseau, certaines alertes."),
        ],
        "voisins": ["beloeil-mont-saint-hilaire", "acton-vale", "granby"],
    },
    {
        "slug": "granby",
        "lieu": "Granby",
        "mrc": "MRC de La Haute-Yamaska",
        "title": "Domotique et maison intelligente à Granby | JARVIS",
        "description": (
            "Domotique, réseau, caméras reliées et IA privée à Granby et en Haute-Yamaska. Un "
            "intégrateur de la région de Saint-Hyacinthe, à environ 40 minutes de route."
        ),
        "image": "/media/vitrine/accueil/maison-familiale.webp",
        "h1": "Maison et entreprise intelligentes <em>à Granby.</em>",
        "lead": (
            "Granby et la Haute-Yamaska sont à environ 40 minutes de notre base. Maisons familiales, "
            "commerces et entreprises manufacturières y trouvent un seul intégrateur pour la "
            "domotique, le réseau et l’IA privée."
        ),
        "route": ("Environ 45 km · 40 min",
                  "Par la route 137 depuis Saint-Hyacinthe. Une visite se planifie sur rendez-vous."),
        "realites": [
            ("Région", "Aux portes des Cantons-de-l’Est.",
             "Granby est la ville-centre de la MRC de La Haute-Yamaska, rattachée à la région de "
             "l’Estrie depuis 2021. On y vient depuis Saint-Hyacinthe par la route 137; l’autoroute 10 "
             "passe juste au sud."),
            ("Habitat", "Beaucoup de maisons familiales, des quartiers en croissance.",
             "La ville compte de nombreux quartiers résidentiels, anciens autour du lac Boivin et plus "
             "récents en périphérie. Dans le neuf, on peut prévoir le câblage; dans l’existant, on relie "
             "sans ouvrir les murs."),
            ("Économie", "Une ville manufacturière et commerçante.",
             "Les parcs industriels et les commerces de Granby emploient beaucoup de monde. Pour une "
             "PME, les besoins reviennent souvent : un réseau fiable, des appels qui ne se perdent pas "
             "et des documents faciles à retrouver."),
            ("Verglas", "Un coin du « triangle noir » de 1998.",
             "Granby a été durement touchée par la tempête de verglas de janvier 1998. On prévoit donc "
             "toujours ce qui doit continuer de fonctionner pendant une panne."),
        ],
        "projets": [
            ("Exemple · maison", "Une maison neuve, câblée dès le départ", MAISON,
             "Le plan du réseau et des points d’accès remis avant la fermeture des murs."),
            ("Exemple · PME", "Un atelier et son bureau", RESEAU,
             "Un Wi-Fi qui couvre l’atelier, un réseau séparé pour les machines et un accès à distance privé."),
            ("Exemple · chalet", "Un chalet dans les Cantons", DOMO,
             "Chauffage abaissé pendant la semaine, alerte de gel et de fuite d’eau, tout prêt à votre arrivée."),
        ],
        "faq": [
            ("Vous déplacez-vous jusqu’à Granby?",
             "Oui. Granby est à environ 40 minutes de route de notre base, dans la région de "
             "Saint-Hyacinthe. Bromont, Waterloo, Roxton Pond et Saint-Paul-d’Abbotsford sont aussi "
             "dans notre zone."),
            ("Peut-on surveiller un chalet à distance?",
             "Oui : température, fuite d’eau, porte et courant. Si le chalet n’a pas Internet, un petit "
             "lien cellulaire suffit souvent pour recevoir les alertes."),
            ("Installez-vous dans une maison déjà construite?",
             "Oui. Des modules sans fil et des thermostats connectés permettent de relier une maison "
             "existante sans gros travaux."),
        ],
        "voisins": ["saint-hyacinthe", "acton-vale", "saint-jean-sur-richelieu"],
    },
    {
        "slug": "drummondville",
        "lieu": "Drummondville",
        "mrc": "MRC de Drummond",
        "title": "Automatisation et domotique à Drummondville | JARVIS",
        "description": (
            "Réseau, automatisation, IA privée et domotique pour les PME et les maisons de "
            "Drummondville. Un intégrateur à environ 35 minutes par l’autoroute 20."
        ),
        "image": "/media/secteurs/manufacturier.webp",
        "h1": "PME et maisons intelligentes <em>à Drummondville.</em>",
        "lead": (
            "Drummondville est à environ 35 minutes de notre base par l’autoroute 20. Ville de PME "
            "manufacturières et de services, elle a souvent besoin d’un réseau solide, d’opérations "
            "plus fluides et d’une IA qui garde les documents dans l’entreprise."
        ),
        "route": ("Environ 50 km · 35 min",
                  "Par l’autoroute 20 vers l’est depuis Saint-Hyacinthe. Visite sur rendez-vous."),
        "realites": [
            ("Région", "Au cœur du Centre-du-Québec.",
             "Drummondville est la ville-centre de la MRC de Drummond, dans le Centre-du-Québec, juste à "
             "l’est de la Montérégie. Elle se trouve au croisement des autoroutes 20 et 55, sur la "
             "rivière Saint-François."),
            ("Économie", "Beaucoup de PME manufacturières.",
             "L’économie locale repose sur un grand nombre de petites et moyennes entreprises de "
             "fabrication, de transport et de services. Ce sont des milieux où une panne de réseau ou "
             "un appel manqué coûte cher."),
            ("Habitat", "Une ville qui s’est beaucoup construite.",
             "Les quartiers résidentiels récents sont nombreux. Une maison neuve est le meilleur moment "
             "pour prévoir le câblage; une maison existante se relie avec des modules sans fil."),
        ],
        "projets": [
            ("Exemple · PME", "Une usine et ses bureaux", AUTO,
             "Les demandes et les approbations circulent seules, avec une trace de chaque décision."),
            ("Exemple · PME", "Les documents techniques, enfin trouvables", IA_PME,
             "Un assistant qui répond à partir des fiches et des procédures de l’entreprise, sur place."),
            ("Exemple · maison", "Une maison familiale", DOMO,
             "Chauffage, éclairage et ambiances sur un seul écran, sans abonnement au nuage."),
        ],
        "faq": [
            ("Desservez-vous Drummondville même si c’est hors de la Montérégie?",
             "Oui. Drummondville est dans le Centre-du-Québec, mais à environ 35 minutes de notre base "
             "par l’autoroute 20. Elle fait partie de notre zone."),
            ("Travaillez-vous avec les entreprises manufacturières?",
             "Notre rôle touche le réseau, les accès, les documents et la circulation des demandes. On ne "
             "programme pas les machines de production : on relie ce qui les entoure."),
            ("Peut-on commencer par un seul problème?",
             "Oui, c’est même la meilleure façon. On règle d’abord le problème qui revient le plus "
             "souvent, puis le système s’agrandit au besoin."),
        ],
        "voisins": ["acton-vale", "saint-hyacinthe", "sorel-tracy"],
    },
    {
        "slug": "longueuil-rive-sud",
        "lieu": "Longueuil et la Rive-Sud",
        "mrc": "Agglomération de Longueuil",
        "title": "Domotique à Longueuil et sur la Rive-Sud | JARVIS",
        "description": (
            "Maison intelligente, Wi-Fi fiable, caméras reliées et IA privée à Longueuil, Brossard, "
            "Boucherville, Saint-Bruno et Saint-Lambert. Un seul système, installé chez vous."
        ),
        "image": "/media/vitrine/accueil/condo-urbain.webp",
        "h1": "Maison et condo intelligents <em>sur la Rive-Sud.</em>",
        "lead": (
            "Longueuil, Brossard, Boucherville, Saint-Bruno-de-Montarville et Saint-Lambert sont à "
            "environ 40 minutes de notre base par l’autoroute 20. Bungalows, maisons en rangée et "
            "condos : chaque type d’habitation a sa façon de devenir intelligent."
        ),
        "route": ("Environ 45 km · 35 à 50 min",
                  "Par l’autoroute 20 vers l’ouest; le temps varie avec la circulation aux heures de pointe."),
        "realites": [
            ("Habitat", "Du bungalow au condo en hauteur.",
             "La Rive-Sud mêle des bungalows de l’après-guerre, des maisons en rangée et beaucoup de "
             "condos récents, notamment près du REM à Brossard. En copropriété, on travaille à "
             "l’intérieur de votre unité, avec du matériel sans fil et dans le respect du règlement de "
             "l’immeuble."),
            ("Wi-Fi", "Beaucoup de réseaux dans peu d’espace.",
             "Dans un immeuble ou un quartier dense, des dizaines de réseaux Wi-Fi se chevauchent. Un "
             "réseau bien réglé, avec des points d’accès câblés quand c’est possible, change tout pour "
             "le télétravail et les objets connectés."),
            ("Quotidien", "Des journées longues hors de la maison.",
             "Quand on travaille à Montréal ou sur la Rive-Sud, la maison passe la journée vide. Abaisser "
             "le chauffage, vérifier une porte ou recevoir un colis à distance sont les demandes les "
             "plus courantes."),
        ],
        "projets": [
            ("Exemple · condo", "Un condo, sans ouvrir un mur", DOMO,
             "Thermostats, éclairage et serrure reliés par des modules sans fil, dans une seule application."),
            ("Exemple · maison", "Un Wi-Fi qui couvre enfin le sous-sol", RESEAU,
             "Des points d’accès bien placés et un réseau séparé pour le télétravail et les objets connectés."),
            ("Exemple · professionnel", "Un bureau à la maison", IA,
             "Un assistant privé qui retrouve vos documents, sans les envoyer à un service en ligne."),
        ],
        "faq": [
            ("Vous déplacez-vous sur la Rive-Sud de Montréal?",
             "Oui : Longueuil (Vieux-Longueuil, Saint-Hubert, Greenfield Park), Brossard, Boucherville, "
             "Saint-Bruno-de-Montarville et Saint-Lambert, à environ 40 minutes de notre base."),
            ("Peut-on installer la domotique dans un condo?",
             "Oui. On utilise du matériel sans fil qui ne touche pas aux parties communes. Si un "
             "changement touche l’immeuble, comme une serrure de porte palière, l’accord du syndicat de "
             "copropriété peut être nécessaire."),
            ("Mon fournisseur Internet m’a donné un routeur. Est-ce suffisant?",
             "Pour naviguer, souvent. Pour une maison intelligente, un réseau avec des points d’accès "
             "bien placés et une zone séparée pour les objets connectés est plus fiable et plus sûr."),
        ],
        "voisins": ["beloeil-mont-saint-hilaire", "saint-jean-sur-richelieu", "saint-hyacinthe"],
    },
    {
        "slug": "saint-jean-sur-richelieu",
        "lieu": "Saint-Jean-sur-Richelieu",
        "mrc": "MRC du Haut-Richelieu",
        "title": "Domotique à Saint-Jean-sur-Richelieu | JARVIS",
        "description": (
            "Maison intelligente, capteurs d’eau, réseau et IA privée à Saint-Jean-sur-Richelieu "
            "et dans le Haut-Richelieu. Un intégrateur de la Montérégie, sur rendez-vous."
        ),
        "image": "/media/secteurs/residences.webp",
        "h1": "Systèmes intelligents <em>à Saint-Jean-sur-Richelieu.</em>",
        "lead": (
            "Saint-Jean-sur-Richelieu et le Haut-Richelieu sont à environ 50 minutes de notre base. "
            "Le long de la rivière comme dans les rangs, on relie la maison, le réseau et les capteurs "
            "dans un seul système qui vous prévient avant le dégât."
        ),
        "route": ("Environ 55 km · 50 min",
                  "Par les routes de la Montérégie depuis Saint-Hyacinthe. Visite sur rendez-vous."),
        "realites": [
            ("Rivière", "Vivre au bord du Richelieu.",
             "La ville s’étend sur les deux rives du Richelieu, à la tête du canal de Chambly. Les "
             "inondations du printemps 2011 dans le Haut-Richelieu ont marqué la région : des capteurs "
             "d’eau au sous-sol et une alerte sur la pompe de puisard sont ici des demandes naturelles."),
            ("Verglas", "Un coin du « triangle noir » de 1998.",
             "Saint-Jean-sur-Richelieu a été au cœur de la tempête de verglas de janvier 1998. On prévoit "
             "donc ce qui doit tenir pendant une panne : le Hub, le réseau et les alertes essentielles."),
            ("Territoire", "Une ville, et beaucoup de campagne autour.",
             "Le Haut-Richelieu compte de grandes terres agricoles, où l’on cultive surtout le maïs et le "
             "soya, et des villages le long de la rivière. Les projets vont de la maison de ville à la "
             "ferme avec plusieurs bâtiments."),
        ],
        "projets": [
            ("Exemple · maison", "Un sous-sol sous surveillance", DIAG,
             "Capteurs d’eau, suivi de la pompe de puisard et alerte claire si elle démarre trop souvent."),
            ("Exemple · maison", "Une maison au bord de l’eau", MAISON,
             "Éclairage, chauffage et capteurs réunis, avec une alerte quand vous êtes au loin."),
            ("Exemple · ferme", "Des bâtiments reliés", FERME,
             "Un lien entre la maison et les bâtiments, puis les températures et le courant sur un seul écran."),
        ],
        "faq": [
            ("Vous déplacez-vous à Saint-Jean-sur-Richelieu?",
             "Oui, ainsi que dans les environs : Iberville, Saint-Luc, Chambly, Carignan, "
             "Mont-Saint-Grégoire ou Saint-Blaise-sur-Richelieu. Comptez environ 50 minutes de route "
             "depuis notre base."),
            ("Un système peut-il m’avertir d’une infiltration d’eau?",
             "Oui. Des capteurs posés au sol signalent l’eau dès qu’elle apparaît, et le suivi de la "
             "pompe de puisard montre si elle travaille plus que d’habitude. Le système prévient; il ne "
             "remplace ni la pompe ni son alimentation de secours."),
            ("Est-ce que tout fonctionne encore sans électricité?",
             "Seulement ce qui est alimenté par une batterie ou une génératrice. On choisit avec vous les "
             "éléments à protéger en priorité."),
        ],
        "voisins": ["longueuil-rive-sud", "beloeil-mont-saint-hilaire", "granby"],
    },
    {
        "slug": "sorel-tracy",
        "lieu": "Sorel-Tracy",
        "mrc": "MRC de Pierre-De Saurel",
        "title": "Domotique et chalets connectés à Sorel-Tracy | JARVIS",
        "description": (
            "Maisons, chalets des îles, bateaux et entreprises de Sorel-Tracy : chauffage, "
            "alertes, réseau et IA privée réunis dans un seul système installé sur place."
        ),
        "image": "/media/vitrine/accueil/chalet-lac.webp",
        "h1": "Maisons et chalets intelligents <em>à Sorel-Tracy.</em>",
        "lead": (
            "Sorel-Tracy est à environ 50 minutes de notre base. Entre le Richelieu, le fleuve et les "
            "îles, on y trouve des maisons, des chalets qu’on ne visite pas tous les jours et des "
            "entreprises industrielles : autant de lieux à suivre à distance."
        ),
        "route": ("Environ 55 km · 50 min",
                  "Vers le nord depuis Saint-Hyacinthe. Visite sur rendez-vous."),
        "realites": [
            ("Eau", "Au confluent du Richelieu et du Saint-Laurent.",
             "La ville est bâtie là où le Richelieu rejoint le fleuve, à l’entrée des îles de Sorel et du "
             "lac Saint-Pierre, reconnu comme réserve de la biosphère. Chalets, quais et bateaux font "
             "partie du paysage."),
            ("Chalets", "Des lieux qu’on laisse seuls.",
             "Un chalet ou un bateau passe des semaines sans visite. Savoir que le chauffage tient, que "
             "rien ne gèle et que la porte est fermée, c’est exactement ce qu’un petit système "
             "autonome peut faire, même avec un simple lien cellulaire."),
            ("Industrie", "Un passé et un présent industriels.",
             "Sorel-Tracy est une ville de métallurgie et d’industrie lourde, au bout de l’autoroute 30. "
             "Autour, les ateliers et les sous-traitants ont besoin d’un réseau fiable et d’accès bien "
             "tenus."),
        ],
        "projets": [
            ("Exemple · chalet", "Un chalet des îles, suivi à distance", DOMO,
             "Température, fuite d’eau et porte, avec une alerte sur votre téléphone par lien cellulaire."),
            ("Exemple · bateau", "Les batteries du bateau au quai", MOB,
             "Tension des batteries, pompe de cale et alimentation du quai visibles de la maison."),
            ("Exemple · PME", "Un atelier industriel", RESEAU,
             "Un réseau séparé pour le bureau et l’atelier, et un accès à distance privé pour le propriétaire."),
        ],
        "faq": [
            ("Vous déplacez-vous à Sorel-Tracy?",
             "Oui, ainsi qu’à Saint-Joseph-de-Sorel, Sainte-Anne-de-Sorel, Saint-Ours, Saint-Robert et "
             "Yamaska, à environ 50 minutes de notre base."),
            ("Peut-on suivre un chalet qui n’a pas Internet?",
             "Oui. Un petit modem cellulaire suffit pour envoyer les alertes importantes : gel, fuite "
             "d’eau, panne de courant, porte ouverte."),
            ("Reliez-vous aussi un bateau?",
             "Oui pour l’énergie et les alertes : batteries, pompe de cale, alimentation du quai. C’est "
             "le même savoir-faire que pour un véhicule récréatif."),
        ],
        "voisins": ["saint-hyacinthe", "beloeil-mont-saint-hilaire", "drummondville"],
    },
    {
        "slug": "beloeil-mont-saint-hilaire",
        "lieu": "Beloeil et Mont-Saint-Hilaire",
        "mrc": "MRC de La Vallée-du-Richelieu",
        "title": "Domotique à Beloeil et Mont-Saint-Hilaire | JARVIS",
        "description": (
            "Maison intelligente clé en main, Wi-Fi fiable et caméras reliées à Beloeil, "
            "Mont-Saint-Hilaire et dans la Vallée-du-Richelieu, à 20 minutes de notre base."
        ),
        "image": "/media/offre/maison.webp",
        "h1": "Maisons intelligentes <em>à Beloeil et Mont-Saint-Hilaire.</em>",
        "lead": (
            "Beloeil et Mont-Saint-Hilaire se font face de chaque côté du Richelieu, à une vingtaine de "
            "minutes de notre base par l’autoroute 20. Ce sont surtout des maisons familiales, où l’on "
            "veut du confort, de la tranquillité et un Wi-Fi qui suit le télétravail."
        ),
        "route": ("Environ 25 km · 20 min",
                  "Par l’autoroute 20 vers l’ouest depuis Saint-Hyacinthe. Visite sur rendez-vous."),
        "realites": [
            ("Habitat", "Des quartiers de maisons familiales.",
             "La Vallée-du-Richelieu est surtout résidentielle : maisons unifamiliales, quartiers récents "
             "et rues anciennes près de la rivière. Beaucoup de résidents travaillent à Montréal ou sur "
             "la Rive-Sud, par l’autoroute 20 ou le train de banlieue."),
            ("Montagne", "Au pied du mont Saint-Hilaire.",
             "Le mont Saint-Hilaire, première réserve de la biosphère désignée au Canada, et ses vergers "
             "donnent son caractère au secteur. Sur les terrains boisés ou en pente, la couverture du "
             "Wi-Fi à l’extérieur et l’éclairage des accès demandent un peu plus de soin."),
            ("Télétravail", "La maison est aussi un bureau.",
             "Avec le télétravail, un réseau instable devient un problème de tous les jours. On sépare le "
             "travail, la famille et les objets connectés pour que chacun ait un service fiable."),
        ],
        "projets": [
            ("Exemple · maison", "Une maison familiale, clé en main", MAISON,
             "Éclairage, chauffage, réseau et capteurs pensés ensemble, puis expliqués à toute la famille."),
            ("Exemple · maison", "Le bureau au sous-sol, bien branché", RESEAU,
             "Des points d’accès câblés et une zone réservée au travail, à l’abri des autres appareils."),
            ("Exemple · maison", "L’entrée et la cour, sans fausses alertes", SECU,
             "Caméras et sonnette réunies en un seul événement clair, avec les images gardées à la maison."),
        ],
        "faq": [
            ("Vous déplacez-vous à Beloeil et à Mont-Saint-Hilaire?",
             "Oui, et dans toute la Vallée-du-Richelieu : Otterburn Park, McMasterville, "
             "Saint-Basile-le-Grand, Saint-Jean-Baptiste ou Saint-Mathieu-de-Beloeil. C’est à une "
             "vingtaine de minutes de notre base."),
            ("Par où commencer dans une maison familiale?",
             "Souvent par le chauffage et l’éclairage, parce qu’on en profite tous les jours, ou par le "
             "réseau s’il cause déjà des ennuis. Le reste s’ajoute au même système."),
            ("Les enfants et les invités peuvent-ils utiliser le système?",
             "Oui. Chaque personne a son compte et ses droits : un enfant peut allumer sa chambre sans "
             "pouvoir déverrouiller la porte, et un invité reçoit un accès temporaire."),
        ],
        "voisins": ["saint-hyacinthe", "longueuil-rive-sud", "saint-jean-sur-richelieu"],
    },
    {
        "slug": "acton-vale",
        "lieu": "Acton Vale",
        "mrc": "MRC d’Acton",
        "title": "Domotique pour maison et ferme à Acton Vale | JARVIS",
        "description": (
            "Systèmes intelligents pour maisons de campagne, fermes, érablières et PME d’Acton "
            "Vale et de la MRC d’Acton : alertes, réseau entre bâtiments, système local."
        ),
        "image": "/media/env/ferme/laitier-exterieur.webp",
        "h1": "Maisons et fermes intelligentes <em>à Acton Vale.</em>",
        "lead": (
            "Acton Vale est à environ 30 minutes de notre base par la route 116. Ici, on parle surtout de "
            "maisons de campagne, de fermes et de bâtiments éloignés les uns des autres : le système doit "
            "fonctionner sur place, même quand Internet est capricieux."
        ),
        "route": ("Environ 35 km · 30 min",
                  "Par la route 116 vers l’est depuis Saint-Hyacinthe. Visite sur rendez-vous."),
        "realites": [
            ("Territoire", "Une petite ville au milieu des terres.",
             "Acton Vale est la ville-centre de la MRC d’Acton, un territoire surtout agricole et "
             "forestier, entre Saint-Hyacinthe et Drummondville. Fermes, érablières et petites "
             "entreprises y côtoient les maisons de village."),
            ("Distances", "Des bâtiments loin de la maison.",
             "Étable, garage, cabane à sucre : quand les bâtiments sont à des centaines de mètres, "
             "c’est le lien entre eux qui fait tout. Câble enterré, fibre ou lien sans fil, on choisit "
             "selon le terrain."),
            ("Internet", "Un système qui ne dépend pas du nuage.",
             "En campagne, la connexion Internet n’est pas toujours aussi stable qu’en ville. Un système "
             "local continue de fonctionner sans elle, et un lien de secours peut transmettre les alertes "
             "importantes."),
        ],
        "projets": [
            ("Exemple · ferme", "La ferme sur un seul écran", FERME,
             "Températures, courant et portes des bâtiments, avec une alerte claire au bon moment."),
            ("Exemple · érablière", "La cabane à sucre, suivie de loin", DIAG,
             "Température, courant et état d’une pompe visibles de la maison, pendant la saison des sucres."),
            ("Exemple · maison", "Une maison de campagne", RESEAU,
             "Un Wi-Fi qui couvre la maison et le garage, et un lien de secours quand Internet tombe."),
        ],
        "faq": [
            ("Vous déplacez-vous à Acton Vale?",
             "Oui, et dans la MRC d’Acton : Upton, Roxton Falls, Saint-Théodore-d’Acton, Sainte-Christine "
             "ou Béthanie. Comptez environ 30 minutes de route depuis notre base."),
            ("Mon Internet est lent en campagne. Est-ce un problème?",
             "Pas pour le système lui-même : il fonctionne sur place. Internet ne sert qu’à l’accès à "
             "distance et aux alertes, qui demandent très peu de débit."),
            ("Peut-on relier une cabane à sucre ou un bâtiment sans électricité fiable?",
             "Souvent, oui, avec des capteurs à pile ou une petite alimentation solaire avec batterie. "
             "C’est un domaine que l’on connaît bien grâce aux véhicules récréatifs."),
        ],
        "voisins": ["saint-hyacinthe", "drummondville", "granby"],
    },
]


def _ville(v):
    url = f"/regions/{v['slug']}/"
    realites = "".join(
        f'<div class="row" data-rev><i>{k}</i><div><h3>{t}</h3><p>{p}</p></div></div>' for k, t, p in v["realites"]
    )
    projets = "".join(
        f'<a class="card" href="{u}" data-rev><small>{k}</small><h3>{t}</h3><p>{p}</p></a>'
        for k, t, u, p in v["projets"]
    )
    voisins = "".join(f'<a class="chip" href="/regions/{k}/">{NOMS[k]}</a>' for k in v["voisins"])
    zone = [{"@type": "City", "name": v["lieu"].replace(" et la Rive-Sud", "")},
            {"@type": "AdministrativeArea", "name": v["mrc"]}]
    return {
        "url": url,
        "v2": True,
        "title": v["title"],
        "description": v["description"],
        "og_image": v["image"],
        "assets": ["pro"],
        "schema": [
            pro.ld_service(f"Intégration de systèmes intelligents à {v['lieu']}", v["description"], url,
                           "Intégration de systèmes intelligents", zone),
            pro.ld_faq(v["faq"]),
        ],
        "content": f"""
<section class="band top">
  <div class="bg"><img src="{v['image']}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil(url)}
    <p class="eyebrow" data-rev>Régions desservies · {v['mrc']}</p>
    <h1 data-rev>{v['h1']}</h1>
    <p class="lead" data-rev>{v['lead']}</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="/logiciel/">Voir le logiciel</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip">{v['route'][0]}</span>
      <span class="chip">Visite sur rendez-vous</span>
      <span class="chip">Maisons · fermes · entreprises · véhicules</span>
    </div>
  </div>
</section>

<section class="sect" id="ici" data-toc="Ici" aria-labelledby="ici-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Les réalités d’ici</p>
      <h2 id="ici-titre" style="margin-top:1rem">Ce qui compte<br><em>à {v['lieu'].replace(' et la Rive-Sud', ' et sur la Rive-Sud')}.</em></h2>
    </div>
    <p data-rev>Un bon système part du lieu. Voici ce dont on tient compte ici, avant de parler de
    technologie.</p>
  </div>
  <div class="rows">{realites}
    <div class="row" data-rev><i>Déplacement</i><div><h3>{v['route'][0]}</h3><p>{v['route'][1]}</p></div></div>
  </div>
</section>

<section class="sect alt" id="exemples" data-toc="Exemples de projets" aria-labelledby="ex-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Exemples de projets typiques</p>
      <h2 id="ex-titre" style="margin-top:1rem">Ce qu’on peut faire<br><em>dans un lieu comme le vôtre.</em></h2>
    </div>
    <p data-rev>Ce sont des exemples, pas des réalisations : l’entreprise est en phase de lancement.
    Chaque carte mène à la solution qui s’y rattache.</p>
  </div>
  <div class="cards">{projets}</div>
</section>

{pro.faq_section(v['faq'], f"Questions fréquentes · {v['lieu']}", "Les questions <em>qu’on nous pose ici.</em>", toc="Questions")}

<section class="sect alt pro-zone-s" aria-labelledby="pres-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Tout près</p>
      <h2 id="pres-titre" style="margin-top:1rem">Aussi dans<br><em>la zone desservie.</em></h2>
    </div>
    <p data-rev>On se déplace à partir de la région de Saint-Hyacinthe.
    <a href="/regions/">Voir toute la zone</a> ou lire <a href="/a-propos/#comment-on-travaille">comment
    on travaille</a>.</p>
  </div>
  <div class="chiprow pro-zone" data-rev>{voisins}<a class="chip" href="/regions/">Toutes les régions</a></div>
</section>

<section class="cta">
  <h2 data-rev>Un projet à {v['lieu'].replace(' et la Rive-Sud', ' ou sur la Rive-Sud').replace('Beloeil et Mont-Saint-Hilaire', 'Beloeil ou à Mont-Saint-Hilaire')}?<br><span>Parlons-en.</span></h2>
  <p data-rev>Décrivez votre lieu en quelques lignes, ou laissez votre nom pour rester informé.
  Aucune pression.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a>
  <a class="pill ghost" href="/questions/">Questions avant d’appeler</a></div>
</section>
""",
    }


# ---------------------------------------------------------------------------
# /regions/ : la zone desservie
# ---------------------------------------------------------------------------
RESUMES = {
    "saint-hyacinthe": "Notre base. Maisons, fermes et PME de la MRC des Maskoutains.",
    "granby": "Maisons familiales, chalets des Cantons et PME de la Haute-Yamaska.",
    "drummondville": "PME manufacturières et maisons, au croisement des autoroutes 20 et 55.",
    "longueuil-rive-sud": "Bungalows, maisons en rangée et condos de l’agglomération de Longueuil.",
    "saint-jean-sur-richelieu": "Maisons au bord du Richelieu et fermes du Haut-Richelieu.",
    "sorel-tracy": "Maisons, chalets des îles, bateaux et ateliers industriels.",
    "beloeil-mont-saint-hilaire": "Maisons familiales de la Vallée-du-Richelieu, au pied de la montagne.",
    "acton-vale": "Maisons de campagne, fermes et érablières de la MRC d’Acton.",
}

FAQ_ZONE = [
    ("Quelles régions JARVIS Private Systems dessert-il?",
     "La Montérégie et ses environs, à partir de la région de Saint-Hyacinthe : Saint-Hyacinthe, "
     "Granby, Drummondville, Longueuil et la Rive-Sud, Saint-Jean-sur-Richelieu, Sorel-Tracy, Beloeil, "
     "Mont-Saint-Hilaire et Acton Vale, ainsi que les municipalités voisines."),
    ("Ma ville n’est pas dans la liste. Pouvez-vous venir?",
     "Probablement, si vous êtes à environ une heure de route de Saint-Hyacinthe. Écrivez-nous le nom de "
     "votre municipalité : on vous répondra franchement."),
    ("Y a-t-il des frais de déplacement?",
     "La première visite et la soumission sont gratuites. S’il devait y avoir des frais de "
     "déplacement pour un lieu éloigné, ils seraient indiqués par écrit avant tout déplacement."),
    ("Avez-vous une boutique ou une salle de montre?",
     "Non. On se déplace chez vous, sur rendez-vous, et le logiciel peut être essayé en ligne en tout "
     "temps."),
]

COMMUN = [
    ("Hiver", "Le froid décide de beaucoup de choses.",
     "Gel d’un chalet, fuite d’eau, chauffage qui lâche pendant une absence : ce sont les premières "
     "alertes qu’on installe. Le matériel placé à l’extérieur ou dans un bâtiment non chauffé est choisi "
     "pour ces conditions."),
    ("Électricité", "Chauffage électrique et heures de pointe.",
     "La plupart des maisons du Québec se chauffent à l’électricité. Hydro-Québec offre des options de "
     "tarification dynamique pour l’hiver; un système intelligent peut vous aider à réduire votre "
     "consommation pendant les heures de pointe, sans promettre un montant d’économie."),
    ("Pannes", "Prévoir ce qui doit continuer.",
     "La tempête de verglas de 1998 a durement touché la Montérégie. On décide avec vous de ce qui doit "
     "tenir pendant une panne : le Hub, le réseau, certaines alertes."),
    ("Agriculture", "Une grande région agricole.",
     "La Montérégie est l’une des principales régions agricoles du Québec : grandes cultures, lait, porc, "
     "volaille, vergers. Les fermes font pleinement partie des lieux qu’on relie."),
]

INDEX = {
    "url": "/regions/",
    "v2": True,
    "title": "Régions desservies : Saint-Hyacinthe et la Montérégie | JARVIS",
    "description": (
        "JARVIS se déplace en Montérégie, ville par ville : Saint-Hyacinthe, Granby, "
        "Drummondville, Longueuil, Saint-Jean-sur-Richelieu, Sorel-Tracy, Beloeil et Acton Vale."
    ),
    "og_image": "/media/vitrine/accueil/panorama-domaine-crepuscule.webp",
    "assets": ["pro"],
    "schema": [
        {
            "@context": "https://schema.org", "@type": "ItemList", "name": "Régions desservies par JARVIS Private Systems",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "url": f"{pro.D}/regions/{k}/"}
                for i, (k, n) in enumerate(ZONE)
            ],
        },
        pro.ld_faq(FAQ_ZONE),
    ],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/vitrine/accueil/panorama-domaine-crepuscule.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil("/regions/")}
    <p class="eyebrow" data-rev>Régions desservies</p>
    <h1 data-rev>Saint-Hyacinthe, la Montérégie <em>et les environs.</em></h1>
    <p class="lead" data-rev>JARVIS Private Systems est basé dans la région de Saint-Hyacinthe et se
    déplace chez vous, à environ une heure de route à la ronde. Maisons, fermes, entreprises et
    véhicules : un seul intégrateur, un seul système.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="#villes">Voir les villes</a>
    </div>
  </div>
</section>

<section class="sect" id="villes" data-toc="Les villes" aria-labelledby="villes-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ville par ville</p>
      <h2 id="villes-titre" style="margin-top:1rem">Huit secteurs.<br><em>Chacun ses réalités.</em></h2>
    </div>
    <p data-rev>Une maison de la Rive-Sud, une ferme d’Acton Vale et un chalet des îles de Sorel ne
    demandent pas le même système. Chaque page explique ce dont on tient compte sur place.</p>
  </div>
  <div class="cards">{"".join(
      f'<a class="card" href="/regions/{v["slug"]}/" data-rev><small>{v["route"][0]}</small>'
      f'<h3>{v["lieu"]}</h3><p>{RESUMES[v["slug"]]}</p></a>' for v in VILLES
  )}
    <a class="card pro-go" href="/contact/" data-rev><small>Ailleurs</small><h3>Votre ville n’y est pas?</h3>
    <p>Si vous êtes à environ une heure de Saint-Hyacinthe, écrivez-nous le nom de votre municipalité.</p></a>
  </div>
</section>

<section class="sect alt" id="partout" data-toc="Partout dans la région" aria-labelledby="partout-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Partout dans la région</p>
      <h2 id="partout-titre" style="margin-top:1rem">Ce qui est vrai<br><em>d’une ville à l’autre.</em></h2>
    </div>
    <p data-rev>Quatre réalités qui reviennent dans presque tous les projets de la Montérégie.</p>
  </div>
  <div class="rows">{"".join(
      f'<div class="row" data-rev><i>{k}</i><div><h3>{t}</h3><p>{p}</p></div></div>' for k, t, p in COMMUN
  )}</div>
</section>

{pro.faq_section(FAQ_ZONE, "Questions fréquentes · Zone desservie", "Où on va, <em>et comment.</em>", toc="Questions")}

<section class="cta">
  <h2 data-rev>Parlons de votre lieu,<br><span>où qu’il soit dans la région.</span></h2>
  <p data-rev>Décrivez votre lieu en quelques lignes, ou laissez votre nom pour rester informé.
  Aucune pression.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a>
  <a class="pill ghost" href="/a-propos/#comment-on-travaille">Comment on travaille</a></div>
</section>
""",
}

PAGES = [INDEX] + [_ville(v) for v in VILLES]
