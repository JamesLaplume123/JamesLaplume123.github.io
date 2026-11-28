# Solution 05 — Réseau et cybersécurité.

from demos.reseau import HTML as DEMO
from pages._solution import solution_page

DATA = {
    "slug": "reseau-resilience",
    "title": "Réseau et cybersécurité",
    "description": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
    "image": "/media/solutions/reseau-resilience.webp",
    "for": "Maisons connectées, PME et petits multi-sites qui dépendent de leur réseau",
    "demo_title": "Tout votre réseau, <em>dans une seule console.</em>",
    "demo_copy": (
        "Douze modules, de la carte du réseau au score de la semaine : appareils, Wi-Fi, trafic, "
        "menaces, VPN, contrôles parentaux, continuité, sauvegardes, mises à jour et segmentation. "
        "JARVIS explique en une phrase et attend votre accord avant d’agir. Données d’exemple."
    ),
    "demo_html": DEMO,
    "assets": ["reseau"],
    "compat": ["Wi-Fi 7", "VLAN", "Pare-feu", "Détection d’intrusion", "VPN", "5G", "Satellite", "PoE", "Sauvegardes 3-2-1", "Multi-sites"],
    "deploy_title": "L’observation reste sur votre infrastructure.",
    "deploy_copy": (
        "Les sondes, journaux et inventaires peuvent demeurer locaux. Les accès distants "
        "passent par des mécanismes privés, limités et auditables."
    ),
    "limit": (
        "Cette solution observe, documente et assiste l’administration. Elle ne remplace ni un "
        "pare-feu, ni une équipe de sécurité, ni un programme complet de cybersécurité."
    ),
    "cta_title": "Quelle partie de votre infrastructure reste <em>un angle mort?</em>",
    "cta_copy": (
        "Décrivez les sites, les liens Internet, les équipements critiques et les incidents "
        "récents. Nous identifierons la première visibilité utile."
    ),
}

DATA["clair"] = {
    "titre": "Votre réseau, gardé <em>comme celui d’une entreprise.</em>",
    "quoi": "JARVIS connaît chaque appareil branché chez vous, sépare ce qui doit l’être et met à l’écart ce qui n’a rien à faire là. Il vous explique tout en mots simples.",
    "moments": [
        ("2 h 14", "Un appareil inconnu se branche sur votre Wi-Fi."),
        ("2 h 14", "JARVIS le met en quarantaine, loin de vos ordinateurs."),
        ("7 h 00", "À votre réveil, il vous demande si vous le connaissez."),
    ],
    "message": "Un appareil inconnu s’est branché à 2 h 14. Il est isolé. Le connaissez-vous?",
    "duel": ("Plus qu’un routeur.", "Un routeur ordinaire", [
        ("Il donne Internet à tout ce qui a le mot de passe.",
         "Chaque appareil est reconnu, nommé et rangé dans sa zone."),
        ("Une ampoule connectée voit les mêmes ordinateurs que vous.",
         "Des zones séparées : la famille, les objets, les caméras et les invités ne se voient pas."),
        ("Une attaque passe sans que personne le sache.",
         "Une menace est repérée, mise à l’écart, et vous êtes averti en mots simples."),
        ("Le Wi-Fi faiblit au sous-sol et dans la cour.",
         "Un Wi-Fi solide dans chaque pièce, mesuré pièce par pièce."),
        ("Internet tombe : tout arrête.",
         "Le lien de secours prend le relais, et la maison continue en local."),
        ("Quand quelque chose ne marche plus, on redémarre tout et on espère.",
         "La carte du réseau montre l’appareil touché et la vraie cause."),
    ]),
    "capacites": [
        ("Il connaît chaque appareil",
         "Téléphone, télé, caméra ou ampoule : tout ce qui se branche est reconnu. Un nouveau venu doit être accepté."),
        ("Il bloque les intrus",
         "Un appareil suspect ou un trafic anormal est mis à l’écart, et vous recevez une explication claire, pas un code d’erreur."),
        ("Des zones séparées",
         "Les caméras et les objets connectés n’ont pas accès à vos ordinateurs. Les invités ont leur propre Wi-Fi."),
        ("Du Wi-Fi solide partout",
         "Dans chaque pièce, avec Internet de secours au besoin. Vos sauvegardes sont testées chaque mois."),
        ("Un accès à distance privé",
         "Votre maison ou votre commerce, de partout, par un tunnel privé, sans rien ouvrir sur Internet."),
        ("Contrôle parental et rapport",
         "Les heures d’écran réglées pour chaque enfant, et votre sécurité résumée chaque semaine."),
    ],
    "equipement": ("L’équipement", [
        "Wi-Fi maillé", "Commutateur (switch)", "Pare-feu", "Sauvegarde chiffrée",
        "Routeur 4G ou 5G de secours, selon le lieu"], ""),
}

PAGE = solution_page(DATA)
