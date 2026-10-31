# Solution 04 — Automatisation d'entreprise.

from pages._solution import solution_page

SHOWCASE = """
<dl class="stat-row" data-reveal style="max-width:860px;">
  <div><dt>Automatisations actives</dt><dd>12</dd></div>
  <div><dt>Heures rendues disponibles / mois</dt><dd>47 h</dd></div>
  <div><dt>Décisions en attente d’approbation</dt><dd>3</dd></div>
</dl>
<p class="form-note" data-reveal>Aperçu conceptuel · données simulées pour illustrer le produit.</p>
<div class="guide-rows" data-reveal style="margin-top:2rem;">
  <a href="/contact/">
    <span>Courriel → compréhension → CRM → calendrier → mission → réponse préparée</span>
    <strong>Demande client</strong>
  </a>
  <a href="/contact/">
    <span>PDF → extraction → comparaison → exception → approbation → comptabilité</span>
    <strong>Facture fournisseur</strong>
  </a>
  <a href="/contact/">
    <span>Formulaire → qualification → CRM → priorité → attribution → suivi</span>
    <strong>Nouveau prospect</strong>
  </a>
  <a href="/contact/">
    <span>RH → comptes → permissions → matériel → calendrier → accueil</span>
    <strong>Nouvel employé</strong>
  </a>
  <a href="/contact/">
    <span>Échéance → contrat → responsable → tâches → message approuvé → CRM</span>
    <strong>Renouvellement client</strong>
  </a>
  <a href="/contact/">
    <span>Alerte → contexte → cause probable → recommandation → exécution supervisée</span>
    <strong>Incident opérationnel</strong>
  </a>
</div>
"""

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
    "problem_title": "Le travail circule entre vos logiciels. <em>Le contexte, lui, se perd.</em>",
    "problem_copy": (
        "Le courriel, le CRM, le calendrier, les documents et les logiciels spécialisés continuent "
        "de faire leur travail. JARVIS organise ce qui se passe entre eux : il transforme ce qui "
        "entre dans l’entreprise en actions compréhensibles et supervisées."
    ),
    "change_title": "Un centre d’opérations, plusieurs processus.",
    "change_copy": (
        "Chaque flux montre d’où viennent les informations, ce que JARVIS comprend, "
        "ce qu’il prépare et où l’humain décide."
    ),
    "features": [
        ("Courriel transformé en dossier", "Une demande entrante devient un dossier qualifié avec le client, le contexte et l’historique."),
        ("Documents et tâches préparés", "Les pièces jointes sont extraites, comparées et classées ; les tâches sont créées au bon endroit."),
        ("Approbation avant chaque action sensible", "Un envoi, un paiement ou un engagement attend une validation humaine explicite."),
        ("Exécution journalisée", "Chaque étape conserve sa source, sa règle et son résultat dans un journal consultable."),
        ("Exceptions visibles", "Ce qui sort du cadre prévu est mis en file plutôt qu’exécuté en silence."),
        ("Conception assistée", "Décrivez le résultat attendu : JARVIS prépare un brouillon de flux, modifiable avant tout essai."),
    ],
    "demo_title": "Six scénarios réels. <em>Un même principe.</em>",
    "demo_copy": (
        "D’un courriel client à un incident opérationnel : l’information avance entre les "
        "systèmes autorisés et chaque décision importante reste humaine."
    ),
    "showcase": SHOWCASE,
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
