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
        "quoi": "Vos caméras, portes et capteurs, lus ensemble. Un seul message clair.",
        "moments": [
            ("23 h 02", "Une auto inconnue passe."),
            ("23 h 06", "Elle repasse. Plaque inconnue."),
            ("23 h 06", "La cour s’illumine."),
        ],
        "message": "Une auto inconnue est passée deux fois. Vidéo jointe.",
        "duel": ("Plus qu’une caméra. <em>Plus qu’une alarme.</em>", "Caméras, serrure et alarme ordinaires", [
            ("Trente alertes par jour.", "Un message, quand ça compte."),
            ("Une application par appareil.", "Tout dans un seul fil."),
            ("Une auto filmée, sans plus.", "La plaque lue, l’auto suivie."),
            ("Les images dans le nuage.", "Les images chez vous."),
        ]),
        "capacites": [
            ("Un événement, pas vingt alertes", "L’inhabituel ressort. Le reste se tait."),
            ("Il reconnaît les vôtres", "Avec leur accord. Les inconnus restent sans nom."),
            ("Plaques et véhicules", "Lues, puis suivies de caméra en caméra."),
            ("Les accès sous contrôle", "Codes temporaires, badges, visiteurs QR."),
            ("Dehors et dans le réseau", "Un intrus, une seule réponse."),
            ("Un dossier en un clic", "Prêt pour la police ou l’assurance."),
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
