# Solution 04 — Automatisation d'entreprise.

from demos.automatisation import HTML as DEMO
from pages._solution import solution_page

DATA = {
    "slug": "automatisation-operations",
    "title": "Automatisation d’entreprise",
    "description": "Faire circuler demandes, documents et approbations entre les outils que l’entreprise utilise déjà.",
    "image": "/media/solutions/jarvis-enterprise-operations-v1.webp",
    "h1": "L’entreprise agit plus vite. <em>Sans perdre le contrôle.</em>",
    "lead": (
        "JARVIS relie les outils de l’entreprise, comprend les demandes, prépare les actions, "
        "demande une validation lorsque nécessaire, exécute et conserve une trace complète."
    ),
    "for": "PME, entreprises de services et équipes terrain",
    "demo_title": "Une demande d’achat, du courriel au bon de commande. <em>Sans copier-coller.</em>",
    "demo_copy": (
        "Regardez JARVIS lire un courriel, remplir la demande, appliquer votre règle, puis "
        "s’arrêter pour vous demander votre accord. Vous jouez le gérant : rien ne part sans "
        "votre clic sur « Approuver ». Deux autres scénarios : un nouveau client et une "
        "facture qui ne concorde pas."
    ),
    "demo_html": DEMO,
    "assets": ["automatisation"],
    "clair": {
        "quoi": "JARVIS fait circuler le travail entre vos outils. <em>Vous gardez la décision.</em>",
        "exemple": (
            "Un employé demande par courriel un compresseur de 1 284 $. JARVIS lit le courriel, "
            "remplit la demande, voit que le montant dépasse 500 $ et vous demande d’approuver. "
            "Un clic, et le bon de commande part au fournisseur, avec une trace de qui a approuvé "
            "et à quelle heure."
        ),
        "avant": [
            "Le même renseignement est retapé dans trois logiciels.",
            "Les demandes dorment dans une boîte de courriel en attendant quelqu’un.",
            "Personne ne sait vraiment qui a approuvé quoi, ni quand.",
            "Une erreur de facture passe si personne ne compare à la main.",
        ],
        "apres": [
            "JARVIS lit la demande et remplit les champs à votre place.",
            "Vos règles décident de ce qui demande une approbation.",
            "Vous approuvez en un clic : l’action part, puis la confirmation revient.",
            "Chaque étape laisse une trace : source, règle, décision et heure.",
        ],
        "obtenez": [
            ("Moins de ressaisie", "Les informations passent d’un outil à l’autre, sans copier-coller."),
            ("Vos règles, appliquées", "Seuils, approbations, exceptions : écrits une fois, respectés à chaque fois."),
            ("Une trace complète", "Un journal clair de chaque étape, consultable en tout temps."),
        ],
    },
    "compat": ["Courriel", "CRM", "Calendrier", "Comptabilité", "RH", "Documents", "API métier"],
    "deploy_title": "Vos processus, vos règles, votre rythme.",
    "deploy_copy": (
        "Les connecteurs sont activés un à un, selon la valeur réelle. Les flux critiques "
        "peuvent fonctionner sur une infrastructure privée."
    ),
    "limit": (
        "JARVIS ne remplace ni le CRM, ni la comptabilité, ni les logiciels spécialisés. "
        "Il relie des systèmes autorisés et documentés ; chaque flux exige une conception validée."
    ),
    "cta_title": "Quel processus vous coûte le plus <em>de temps aujourd’hui?</em>",
    "cta_copy": (
        "Décrivez le parcours actuel d’une demande, les outils traversés et les étapes où "
        "l’information se perd ou se ressaisit."
    ),
}

PAGE = solution_page(DATA)
