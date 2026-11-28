# Solution 03 — Sécurité intelligente.

from pages._solution import solution_page
from demos.securite import HTML as DEMO_HTML

DATA = {
    "slug": "securite-intelligente",
    "title": "Sécurité intelligente",
    "description": "Un logiciel qui réunit vos caméras, serrures et capteurs en événements clairs, traités et gardés chez vous : mur vidéo, accès, véhicules, zones, incidents et conformité à la Loi 25.",
    "image": "/media/solutions/securite-intelligente.webp",
    "for": "Résidences, entreprises, entrepôts, campus et organisations réparties sur plusieurs sites",
    "clair": {
        "titre": "Une alarme sonne. <em>JARVIS, lui, comprend.</em>",
        "quoi": "JARVIS regarde toutes vos caméras, vos portes et vos capteurs en même temps, puis vous dit en une phrase ce qui s’est vraiment passé.",
        "moments": [
            ("23 h 02", "Une auto inconnue passe devant chez vous."),
            ("23 h 06", "Elle repasse. JARVIS lit la plaque : personne ne la connaît."),
            ("23 h 06", "Les lumières de la cour s’allument, comme vous l’avez réglé."),
        ],
        "message": "Une auto inconnue est passée deux fois. Plaque lue, lumières allumées. Vidéo jointe.",
        "duel": ("Plus qu’une caméra. <em>Plus qu’une alarme.</em>", "Caméras, serrure et alarme ordinaires", [
            ("« Mouvement détecté », trente fois par jour, pour un chat ou une branche.",
             "Un seul message par événement : qui, quoi, où, et si c’est normal."),
            ("Chaque appareil a son application et raconte sa propre version.",
             "Caméras, sonnette, portes et alarme réunies dans un seul fil."),
            ("La caméra filme une auto, sans savoir qu’elle est déjà passée.",
             "JARVIS lit la plaque, reconnaît une auto qui revient et la suit d’une caméra à l’autre."),
            ("La serrure s’ouvre avec un code, peu importe qui le tape ou à quelle heure.",
             "Codes temporaires, horaires et visiteurs : chaque entrée est connue et notée."),
            ("Les images partent souvent dans le nuage d’une compagnie.",
             "Les images restent chez vous, dans votre JARVIS."),
            ("Après un vol, vous fouillez des heures de vidéo.",
             "Le dossier est prêt en un clic : chronologie, extraits et preuve d’intégrité."),
        ]),
        "capacites": [
            ("Un événement, pas vingt alertes",
             "Caméras, sonnette, portes et alarme sont lues ensemble. Le livreur et le chat restent discrets; l’inhabituel ressort tout de suite."),
            ("Il reconnaît les vôtres",
             "Famille, employés et habitués sont inscrits avec leur consentement. Un inconnu est signalé sans nom, et les visages sont masqués hors incident."),
            ("Plaques et véhicules",
             "JARVIS lit les plaques, reconnaît une auto qui revient et la suit d’une caméra à l’autre."),
            ("Les accès sous contrôle",
             "Serrures, badges, horaires et codes temporaires. Un visiteur reçoit un code QR valide le temps de sa visite. Rien ne se déverrouille tout seul."),
            ("Dehors et dans le réseau, le même réflexe",
             "Reliée à <a href=\"/solutions/reseau-resilience/\">Réseau et cybersécurité</a> : un intrus dans la cour ou un appareil inconnu sur le Wi-Fi déclenche la même réponse."),
            ("Un dossier prêt en un clic",
             "Chronologie, extraits, plan et empreinte vérifiable pour la police ou l’assurance, avec les personnes non concernées masquées."),
        ],
        "equipement": ("L’équipement", [
            "Caméras 4K à vision de nuit", "Sonnette vidéo", "Serrures connectées", "Capteurs de porte et de fenêtre",
            "Sirène", "Lecture de plaques", "Badges et codes QR"],
            "Quand la loi l’exige, la pose est faite par un installateur qui détient le permis requis. JARVIS relie ensuite le tout."),
    },
    "demo_title": "Neuf modules. <em>Une seule plateforme de sécurité.</em>",
    "demo_copy": (
        "Le mur vidéo regroupe les alertes en un seul événement compris. Autour de lui : accès, "
        "véhicules, zones, incidents, sites, rondes et Loi 25. Passez d’un module à l’autre en haut de "
        "la fenêtre. Données d’exemple : les agents et les rondes montrés sont ceux de l’organisation "
        "qui utilise le logiciel. JARVIS fournit le logiciel, pas de gardiennage."
    ),
    "demo_html": DEMO_HTML,
    "assets": ["securite"],
    "compat": ["Frigate", "ONVIF", "Contrôle d’accès", "Lecteurs de plaques", "Badges et codes QR", "Étiquettes NFC de ronde", "Alarmes", "Capteurs", "Interphones", "Stockage local"],
    "deploy_title": "Les événements sensibles restent près du site.",
    "deploy_copy": (
        "L’analyse vidéo et la conservation peuvent être effectuées localement. "
        "Les accès distants passent par des mécanismes privés et auditables."
    ),
    "limit": (
        "Le système ne prétend pas identifier les intentions ni déterminer qu’une personne est "
        "dangereuse. L’identification se limite aux personnes inscrites qui y ont consenti; les "
        "autres sont signalées sans nom. Les règles, responsabilités et obligations légales, dont "
        "la déclaration d’une banque biométrique, doivent être définies avant tout déploiement. "
        "JARVIS Private Systems fournit le logiciel : ce n’est pas une agence de sécurité, et aucune "
        "centrale ni aucun agent ne surveille vos images. La pose de caméras de "
        "surveillance, d’alarmes et de contrôles d’accès chez un client est encadrée par la Loi sur "
        "la sécurité privée : quand un permis est requis, elle doit être faite par un installateur "
        "qui le détient; JARVIS relie ensuite ces appareils au système."
    ),
    "cta_title": "Quel événement de sécurité manque aujourd’hui <em>de contexte?</em>",
    "cta_copy": (
        "Décrivez le site, les accès, les caméras et les alertes actuelles. Nous identifierons "
        "les preuves utiles et les limites à respecter."
    ),
}

PAGE = solution_page(DATA)
