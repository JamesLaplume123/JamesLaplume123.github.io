# Solution 03 — Sécurité intelligente.

from pages._solution import solution_page
from demos.securite import HTML as DEMO_HTML

DATA = {
    "slug": "securite-intelligente",
    "title": "Sécurité intelligente",
    "description": "Un logiciel qui réunit vos caméras, serrures et capteurs en événements clairs, traités et gardés chez vous : mur vidéo, accès, véhicules, zones, incidents et conformité à la Loi 25.",
    "image": "/media/solutions/securite-intelligente.webp",
    "h1": "Sécurité <em>intelligente.</em>",
    "lead": "Un logiciel installé chez vous, qui réunit vos caméras, vos serrures, vos capteurs et vos preuves dans la même application que le reste du lieu. Vous gardez le contrôle, et les images restent sur place.",
    "for": "Résidences, entreprises, entrepôts, campus et organisations réparties sur plusieurs sites",
    "clair": {
        "quoi": "JARVIS regarde toutes vos caméras et vos capteurs en même temps, puis vous dit en une phrase <em>ce qui s’est vraiment passé.</em>",
        "exemple": (
            "Un livreur dépose un colis. Au lieu de six notifications (mouvement, personne, sonnette, "
            "colis…), vous en recevez une seule : « 21 h 42 — Livraison : un colis a été déposé à "
            "l’entrée. Rien d’anormal. » La nuit, si quelqu’un rôde, JARVIS vous propose d’allumer "
            "les lumières et attend votre accord."
        ),
        "avant": [
            "Des dizaines de notifications par jour, souvent pour un chat ou une branche.",
            "Chaque caméra a son application et raconte sa propre version.",
            "Pour comprendre, il faut ouvrir les vidéos une par une.",
            "La nuit, impossible de savoir si c’est grave ou non.",
        ],
        "apres": [
            "Les alertes d’une même situation deviennent un seul événement.",
            "Une phrase claire explique ce qui s’est passé, images à l’appui.",
            "Le normal reste discret; l’inhabituel ressort tout de suite.",
            "JARVIS propose une action (lumières, interphone) et attend votre accord.",
        ],
        "obtenez": [
            ("Un seul fil", "Caméras, sonnette, portes, détecteurs et alarme réunis dans une même chronologie."),
            ("Des preuves classées", "Les images utiles sont gardées avec l’événement, sur place, aussi longtemps que vous le décidez."),
            ("Le dernier mot", "Allumer, parler, prévenir : JARVIS propose, vous approuvez. Rien ne se déverrouille tout seul."),
            ("Les accès et les véhicules", "Badges, horaires, talonnage, visiteurs avec code QR, lecture de plaques et suivi d’un véhicule d’une caméra à l’autre."),
            ("Un dossier prêt à remettre", "Chronologie, extraits, plan et empreinte vérifiable, exportés en un clic avec les personnes non concernées masquées."),
            ("La Loi 25 intégrée", "Identification seulement des personnes inscrites avec leur consentement, masquage des visages hors incident, chaque consultation journalisée."),
        ],
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
        "centrale ni aucun agent ne surveille vos images. Au Québec, la pose de caméras de "
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
