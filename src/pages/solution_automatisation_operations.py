# Solution 04 — Automatisation d'entreprise.
# La vedette : la réception téléphonique IA (JARVIS répond sur la ligne IP et
# suit la procédure de l'équipe). Suivent « Votre secteur » (explorateur des
# vrais problèmes de chaque secteur, avec l'automatisation qui les règle), la
# bibliothèque d'automatisations (une seule, celle de l'offre) et la bande « La différence »
# face aux Environnements intelligents et à la Sécurité.
#
# Une seule bibliothèque (22 novembre 2026) : cette page lit celle de l'offre
# (src/pages/catalogue.py : ENT_RECEP, AUTOMATISATIONS). Rien n'est annoncé ici
# qui ne se compose pas sur la page L'offre, et l'inverse.

from demos.automatisation import HTML as DEMO, SECTEURS, SECTEURS_HTML, fr
from pages import catalogue as offre
from pages._solution import solution_page

# Icônes fines (trait 1.5), une par famille de la bibliothèque.
CAT_ICONS = {
    "phone": '<path d="M7.4 3.6c.6 0 1.1.4 1.3 1l.9 2.5c.2.6 0 1.2-.5 1.6l-1.1 1a12.6 12.6 0 0 0 6.3 6.3l1-1.1c.4-.5 1-.7 1.6-.5l2.5.9c.6.2 1 .7 1 1.3v2c0 1-.8 1.8-1.8 1.7C10.8 19.7 4.3 13.2 3.7 5.4c-.1-1 .7-1.8 1.7-1.8z"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
    "devis": '<path d="M14 3H7.5A2.5 2.5 0 0 0 5 5.5v13A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 16.5h4.5"/>',
    "recu": '<path d="M6 3.5h12V21l-2.4-1.6L13.2 21l-2.4-1.6L8.4 21 6 19.4z"/><path d="M9.5 8.5h5M9.5 12h5"/>',
    "userplus": '<circle cx="10" cy="8" r="3.6"/><path d="M3.5 20c.4-3.6 3.1-6 6.5-6 1.1 0 2.1.2 3 .7"/><path d="M17.5 14.5v6M14.5 17.5h6"/>',
    "boite": '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5 12 12l8-4.5M12 12v9"/>',
    "graph": '<path d="M4 4v16h16"/><path d="M8.5 15.5v-5M12.5 15.5v-8M16.5 15.5v-3"/>',
    "alerte": '<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.5M12 17v.01"/>',
}
# L'icône de chaque famille de la bibliothèque (les familles elles-mêmes viennent de l'offre).
FAMILLE_ICONE = {"Réception": "cal", "Ventes": "devis", "Facturation": "recu", "Opérations": "boite",
                 "Direction": "graph", "Employés et accès": "userplus", "Ferme et commerce": "alerte"}
assert set(FAMILLE_ICONE) == {cat for cat, _ in offre.AUTOMATISATIONS}, "une famille de la bibliothèque n'a pas d'icône (ou une icône n'a plus de famille)"

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
    """La bibliothèque, telle que l'offre la vend : la réceptionniste en vedette, puis une carte par famille."""
    n = len(offre.AUTOS_BY_ID)
    vedette = f"""<li class="is-star">
      <span class="au-cat-tag">{_icon('phone')}<span>Par ligne</span><em class="au-cat-star">La vedette</em></span>
      <b>{fr(offre.ENT_RECEP['nom'])}</b><p>{fr(offre.ENT_RECEP['d'].split('. ')[0])}.</p>
    </li>"""
    familles = "".join(
        f"""<li>
      <span class="au-cat-tag">{_icon(FAMILLE_ICONE[cat])}<span>{len(items)} automatisations</span></span>
      <b>{fr(cat)}</b><ul>{"".join(f"<li>{fr(a[1])}</li>" for a in items)}</ul>
    </li>"""
        for cat, items in offre.AUTOMATISATIONS
    )
    return f"""<div class="au-sect au-cat" data-rev id="bibliotheque">
    <div class="au-cat-head">
      <p class="eyebrow">La bibliothèque · {n} automatisations</p>
      <h3>Ce que JARVIS prend en charge partout</h3>
      <p>Peu importe le métier, ces {n} automatisations servent dans chaque entreprise. Vous les activez une à la
      fois, au mois. JARVIS et ses extensions, c’est l’équivalent d’une équipe d’une dizaine de personnes toujours en
      poste — réceptionniste, archiviste, commis, technicien.</p>
    </div>
    <ul class="au-cat-grid">{vedette}{familles}</ul>
    <p class="au-cat-foot"><b>Votre processus n’est pas ici?</b>
    {fr("S’il suit des règles, il se fait sur mesure, étape par étape, validé avec vous.")}
    <a href="/offre/#composer">Composer pour mon entreprise <i aria-hidden="true">→</i></a></p>
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
    "for": "PME, commerces, entreprises de services et équipes terrain",
    "demo_title": "Le téléphone sonne. <em>JARVIS répond.</em>",
    "demo_copy": (
        "Regardez JARVIS prendre un appel : il reconnaît la cliente, déplace son rendez-vous et "
        "s’arrête quand la procédure exige un humain — vous. Plus bas : votre secteur, parmi "
        f"{len(SECTEURS)}, et l’automatisation qui règle chacun de ses problèmes."
    ),
    "demo_html": DEMO,
    "assets": ["automatisation"],
    "extra": SECTEURS_HTML + _catalogue() + _diff(),
    "clair": {
        "titre": "Plus un appel manqué. <em>Plus rien à recopier.</em>",
        "quoi": "JARVIS répond au téléphone, trie les demandes et fait circuler le travail entre vos logiciels. Vous gardez la décision.",
        "moments": [
            ("10 h 12", "Une cliente appelle pour déplacer son rendez-vous."),
            ("10 h 12", "JARVIS répond avant la deuxième sonnerie et confirme un nouveau créneau."),
            ("10 h 13", "Elle demande un remboursement de 45 $. La procédure exige un humain."),
        ],
        "message": "Une cliente demande un remboursement de 45 $. Approuver?",
        "pourquoi": False,
        "duel": ("Plus qu’une boîte vocale.", "Une boîte vocale et des outils séparés", [
            ("Le téléphone sonne occupé : l’appel tombe dans la boîte vocale, souvent sans rappel.",
             "Chaque appel est pris, jour et nuit, selon la procédure de votre équipe."),
            ("Le même renseignement est retapé dans trois logiciels.",
             "Les informations passent d’un outil à l’autre, sans copier-coller."),
            ("Les demandes dorment dans une boîte de courriel.",
             "Chaque demande est triée et envoyée à la bonne personne."),
            ("Personne ne sait qui a approuvé quoi, ni quand.",
             "Chaque étape laisse une trace : la source, la règle, la décision et l’heure."),
            ("Le matin, il faut fouiller pour savoir où on en est.",
             "Le rapport du matin : appels, ventes, retards et alertes, sur une page."),
        ]),
        "capacites": [
            ("Une réception toujours en ligne",
             "Chaque appel est pris, suivi et consigné. Un humain reste joignable en tout temps."),
            ("Vos règles, appliquées",
             "Seuils, approbations et exceptions : écrits une fois, respectés à chaque fois."),
            ("Rien à recopier",
             "Soumissions, factures, stock et suivis passent d’un logiciel à l’autre, tout seuls."),
            ("Le bon geste, à la bonne personne",
             "Ce qui exige un humain vous arrive avec tout le dossier, prêt à approuver."),
            ("Le rapport du matin",
             "Appels, ventes, retards et alertes : votre entreprise résumée chaque matin."),
            ("Une trace complète",
             "Un journal clair de chaque appel et de chaque étape, consultable en tout temps."),
        ],
        "equipement": ("Ce qu’on relie", [
            "Votre ligne téléphonique", "Courriel et calendrier", "CRM et comptabilité",
            "Vos logiciels métier", "Un appareil JARVIS sur place, ou une infrastructure privée"], ""),
    },
    "compat": ["Téléphonie IP", "Courriel", "CRM", "Calendrier", "Comptabilité", "RH", "Documents", "Annuaire d’entreprise", "API métier"],
    "deploy_title": "Vos processus, vos règles, votre rythme.",
    "deploy_copy": (
        "La réception téléphonique s’installe d’abord en écoute, puis prend les appels simples, puis "
        "le reste — à votre rythme. Les connecteurs sont activés un à un, selon la valeur réelle. "
        "Les flux critiques peuvent fonctionner sur une infrastructure privée."
    ),
    "limit": (
        "JARVIS ne remplace ni le CRM, ni la comptabilité, ni votre annuaire, ni les logiciels "
        "spécialisés — ni votre équipe : il exécute ce qu’elle a décidé. Il relie des systèmes "
        "autorisés et documentés ; chaque flux exige une conception validée."
    ),
    "cta_title": "Combien d’appels manqués <em>cette semaine?</em>",
    "cta_copy": (
        "Décrivez votre réception actuelle et le parcours d’une demande : les outils traversés, "
        "les étapes où l’information se perd, les appels qui tombent dans la boîte vocale."
    ),
}

PAGE = solution_page(DATA)
PAGE["public"] = "entreprise"  # propre à l'entreprise : avis et bascule côté « Pour chez moi »
