# Solution 04 — Automatisation d'entreprise.
# La vedette : la réception téléphonique IA (JARVIS répond sur la ligne IP et
# suit la procédure de l'équipe). Suivent « Votre secteur » (explorateur des
# vrais problèmes de chaque secteur, avec l'automatisation qui les règle), le
# socle commun des douze automatisations offertes à toutes les entreprises et
# la bande « La différence » face aux Environnements intelligents et à la Sécurité.

from demos.automatisation import HTML as DEMO, SECTEURS, SECTEURS_HTML, fr
from pages._solution import solution_page

# Icônes fines (trait 1.5) du catalogue.
CAT_ICONS = {
    "phone": '<path d="M7.4 3.6c.6 0 1.1.4 1.3 1l.9 2.5c.2.6 0 1.2-.5 1.6l-1.1 1a12.6 12.6 0 0 0 6.3 6.3l1-1.1c.4-.5 1-.7 1.6-.5l2.5.9c.6.2 1 .7 1 1.3v2c0 1-.8 1.8-1.8 1.7C10.8 19.7 4.3 13.2 3.7 5.4c-.1-1 .7-1.8 1.7-1.8z"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "devis": '<path d="M14 3H7.5A2.5 2.5 0 0 0 5 5.5v13A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 16.5h4.5"/>',
    "recu": '<path d="M6 3.5h12V21l-2.4-1.6L13.2 21l-2.4-1.6L8.4 21 6 19.4z"/><path d="M9.5 8.5h5M9.5 12h5"/>',
    "userplus": '<circle cx="10" cy="8" r="3.6"/><path d="M3.5 20c.4-3.6 3.1-6 6.5-6 1.1 0 2.1.2 3 .7"/><path d="M17.5 14.5v6M14.5 17.5h6"/>',
    "boite": '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5 12 12l8-4.5M12 12v9"/>',
    "horloge": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "graph": '<path d="M4 4v16h16"/><path d="M8.5 15.5v-5M12.5 15.5v-8M16.5 15.5v-3"/>',
    "camion": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    "bouclier": '<path d="M12 3.5 19 6v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="m9 11.8 2.2 2.2 3.8-4"/>',
    "alerte": '<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.5M12 17v.01"/>',
}

# (icône, étiquette, titre, une ligne, vedette?)
CATALOGUE = [
    ("phone", "Accueil", "Réception et appels",
     "JARVIS répond sur la ligne IP, identifie l’appelant et suit la procédure de votre équipe.", True),
    ("cal", "Accueil", "Prise de rendez-vous",
     "Agenda vérifié, créneaux proposés, confirmation envoyée par courriel et SMS.", False),
    ("mail", "Accueil", "Tri du courriel entrant",
     "Chaque message est classé, résumé et acheminé à la bonne personne.", False),
    ("devis", "Ventes", "Soumissions et devis",
     "La demande devient un devis prêt à relire, avec vos prix et vos modèles.", False),
    ("recu", "Finances", "Facturation et relances",
     "Factures préparées, écarts détectés, rappels polis aux retardataires.", False),
    ("userplus", "RH", "Accueil d’un nouvel employé",
     "Comptes, accès, équipement, formation : la liste se déroule sans oubli.", False),
    ("boite", "Opérations", "Inventaire et commandes",
     "Seuils surveillés, bons de commande préparés quand le stock baisse.", False),
    ("horloge", "RH", "Horaires d’équipe et rappels",
     "Quarts publiés, remplacements proposés, rappels envoyés à chacun.", False),
    ("graph", "Direction", "Rapports hebdomadaires automatiques",
     "Ventes, chantiers, heures : le portrait de la semaine, sans compilation à la main.", False),
    ("camion", "Opérations", "Suivi de flotte et véhicules",
     "Kilométrage, entretiens et inspections consignés, rappels avant échéance.", False),
    ("bouclier", "Conformité", "Registres et conformité",
     "Les documents exigés, tenus à jour et prêts pour une vérification.", False),
    ("alerte", "Opérations", "Alertes d’équipement et maintenance",
     "Un équipement dérive : l’équipe est prévenue avant la panne.", False),
]

DIFF = [
    ("/solutions/environnements-intelligents/", "Le lieu physique", "Environnements intelligents",
     "JARVIS s’occupe du lieu : bâtiments, énergie, équipements.", False),
    ("/solutions/automatisation-operations/", "Les processus", "Automatisation d’entreprise",
     "JARVIS s’occupe des processus : appels, documents, approbations, suivis.", True),
    ("/solutions/securite-intelligente/", "La protection", "Sécurité intelligente",
     "JARVIS s’occupe de la protection : caméras, accès, incidents.", False),
]


def _icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{CAT_ICONS[name]}</svg>'


def _catalogue():
    items = "".join(
        f"""<li{' class="is-star"' if star else ''}>
      <span class="au-cat-tag">{_icon(ic)}<span>{fr(tag)}</span>{'<em class="au-cat-star">La vedette</em>' if star else ''}</span>
      <b>{fr(title)}</b><p>{fr(line)}</p>
    </li>"""
        for ic, tag, title, line, star in CATALOGUE
    )
    return f"""<div class="au-sect au-cat" data-rev>
    <div class="au-cat-head">
      <p class="eyebrow">Le socle commun · dans tous les secteurs</p>
      <h3>Ce que JARVIS prend en charge partout</h3>
      <p>Peu importe le métier, ces douze automatisations servent dans chaque entreprise. JARVIS et ses extensions,
      c’est l’équivalent d’une équipe d’une dizaine de personnes déjà en poste — réceptionniste, archiviste,
      commis, technicien.</p>
    </div>
    <ul class="au-cat-grid">{items}</ul>
    <p class="au-cat-foot"><b>Chaque automatisation est construite sur mesure, étape par étape, validée avec vous.</b>
    {fr("Votre processus n’est ni ici ni dans votre secteur ? Décrivez-le-nous : s’il suit des règles, il s’automatise.")}</p>
  </div>"""


def _diff():
    cards = "".join(
        f"""<a href="{url}"{' class="is-here" aria-current="page"' if here else ''}>
      <small>{fr(k)}{' · vous êtes ici' if here else ''}</small><b>{fr(title)}</b><p>{fr(line)}</p>
    </a>"""
        for url, k, title, line, here in DIFF
    )
    return f"""<div class="au-sect au-diff" data-rev>
    <div class="au-diff-head">
      <p class="eyebrow">La différence</p>
      <h3>Trois solutions, trois terrains.</h3>
      <p>Le même JARVIS, trois responsabilités distinctes — et elles se parlent.</p>
    </div>
    <div class="au-diff-grid">{cards}</div>
  </div>"""


DATA = {
    "slug": "automatisation-operations",
    "title": "Automatisation d’entreprise",
    "description": (
        "Réception téléphonique IA sur téléphonie IP, rendez-vous, courriels, devis, factures : "
        "JARVIS automatise les processus de l’entreprise, étape par étape, avec validation humaine."
    ),
    "image": "/media/solutions/jarvis-enterprise-operations-v1.webp",
    "h1": "Votre réception ne manque <em>plus un appel.</em>",
    "lead": (
        "JARVIS répond au téléphone de l’entreprise comme une réceptionniste : il identifie l’appelant, "
        "suit la procédure de votre équipe, demande un accord humain pour les gestes sensibles et "
        "consigne tout. Et derrière le téléphone, il fait circuler demandes, documents et approbations."
    ),
    "for": "PME, entreprises de services et équipes terrain",
    "demo_title": "Le téléphone sonne. <em>JARVIS répond.</em>",
    "demo_copy": (
        "Regardez JARVIS prendre un appel réel : il reconnaît la cliente, déplace son rendez-vous et "
        "s’arrête net quand la procédure exige un humain — vous. Essayez aussi « Je veux parler à "
        "quelqu’un » : l’appel est transféré avec tout le contexte. Trois autres scénarios : une "
        "demande d’achat, un nouveau client, une facture qui ne concorde pas. Plus bas : votre "
        f"secteur, parmi {len(SECTEURS)}, avec ses vrais problèmes et l’automatisation qui règle chacun."
    ),
    "demo_html": DEMO,
    "assets": ["automatisation"],
    "extra": SECTEURS_HTML + _catalogue() + _diff(),
    "clair": {
        "quoi": "JARVIS répond, trie et fait circuler le travail. <em>Vous gardez la décision.</em>",
        "exemple": (
            "Une cliente appelle pour déplacer son rendez-vous. JARVIS répond avant la deuxième "
            "sonnerie, retrouve son dossier, propose deux créneaux et confirme le nouveau. Elle "
            "demande un remboursement de 45 $ : la procédure exige un humain, alors JARVIS vous "
            "notifie et attend votre accord — la cliente patiente trente secondes, pas deux jours. "
            "Tout est consigné : transcription, décision, heure."
        ),
        "avant": [
            "Le téléphone sonne occupé : l’appel tombe dans la boîte vocale et personne ne rappelle.",
            "Le même renseignement est retapé dans trois logiciels.",
            "Les demandes dorment dans une boîte de courriel en attendant quelqu’un.",
            "Personne ne sait vraiment qui a approuvé quoi, ni quand.",
        ],
        "apres": [
            "JARVIS répond à chaque appel et suit la procédure écrite avec votre équipe.",
            "Les informations passent d’un outil à l’autre, sans copier-coller.",
            "Vos règles décident de ce qui exige une approbation humaine.",
            "Chaque étape laisse une trace : source, règle, décision et heure.",
        ],
        "obtenez": [
            ("Une réception toujours en ligne", "Chaque appel est pris, suivi et consigné — et un humain reste joignable à tout moment."),
            ("Vos règles, appliquées", "Seuils, approbations, exceptions : écrits une fois, respectés à chaque fois."),
            ("Une trace complète", "Un journal clair de chaque appel et de chaque étape, consultable en tout temps."),
        ],
    },
    "compat": ["Téléphonie IP", "Courriel", "CRM", "Calendrier", "Comptabilité", "RH", "Documents", "API métier"],
    "deploy_title": "Vos processus, vos règles, votre rythme.",
    "deploy_copy": (
        "La réception téléphonique s’installe d’abord en écoute, puis prend les appels simples, puis "
        "le reste — à votre rythme. Les connecteurs sont activés un à un, selon la valeur réelle. "
        "Les flux critiques peuvent fonctionner sur une infrastructure privée."
    ),
    "limit": (
        "JARVIS ne remplace ni le CRM, ni la comptabilité, ni les logiciels spécialisés — ni votre "
        "équipe : il exécute ce qu’elle a décidé. Il relie des systèmes autorisés et documentés ; "
        "chaque flux exige une conception validée."
    ),
    "cta_title": "Combien d’appels manqués <em>cette semaine?</em>",
    "cta_copy": (
        "Décrivez votre réception actuelle et le parcours d’une demande : les outils traversés, "
        "les étapes où l’information se perd, les appels qui tombent dans la boîte vocale."
    ),
}

PAGE = solution_page(DATA)
