# Solution 06 — Diagnostic & continuité.

from pages._solution import solution_page

SHOWCASE = """
<div class="split" data-reveal>
  <div class="steps" style="align-self:stretch;">
    <div>
      <h3>Observer le symptôme</h3>
      <p>Arrêt intermittent, dérive de température, perte de communication : l’état est capté
      avec son historique plutôt que décrit de mémoire.</p>
    </div>
    <div>
      <h3>Vérifier dans le bon ordre</h3>
      <p>Alimentation, communications, contexte des changements récents : les contrôles les
      moins risqués passent en premier.</p>
    </div>
    <div>
      <h3>Décider avec des preuves</h3>
      <p>Chaque hypothèse est confirmée, écartée ou laissée ouverte, avec la mesure qui le justifie.</p>
    </div>
    <div>
      <h3>Documenter la remise en service</h3>
      <p>Le dossier conserve les mesures, les étapes faites et la vérification de stabilité après l’intervention.</p>
    </div>
  </div>
  <aside class="console" style="max-width:none;">
    <header class="console-head"><span><i></i>DOSSIER K-041</span><small>LOCAL</small></header>
    <div class="console-body">
      <small>DOSSIER TECHNICIEN PRÉPARÉ</small>
      <strong>Arrêt intermittent de la génératrice.</strong>
      <p>Mesures, photos, historique d’entretien, pièces possibles et étapes déjà vérifiées :
      la personne qui intervient reçoit le contexte complet, pas un symptôme isolé.</p>
    </div>
    <ul class="console-signals">
      <li><span>SOURCES</span><b>4 reliées</b></li>
      <li><span>VÉRIFICATIONS</span><b>2 faites · 1 proposée</b></li>
      <li><span>ACTION</span><b>Aucune exécutée</b></li>
    </ul>
  </aside>
</div>
"""

DATA = {
    "slug": "diagnostic-care",
    "title": "Diagnostic & continuité",
    "description": "Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.",
    "image": "/media/product/jarvis-hub-v1.webp",
    "h1": "Diagnostic & <em>continuité.</em>",
    "lead": "Comprendre plus vite ce qui a changé, quoi vérifier et comment transmettre un dossier utile à la bonne personne.",
    "for": "Tous les environnements équipés, du bâtiment au véhicule",
    "problem_title": "Une panne traverse plusieurs systèmes <em>et personne ne possède toute l’histoire.</em>",
    "problem_copy": (
        "Cette capacité réunit les états, événements, changements et procédures autorisés pour "
        "construire un diagnostic progressif. Elle prépare les vérifications, documente le "
        "résultat et facilite la continuité après l’installation."
    ),
    "change_title": "Du symptôme au dossier utile, sans sauter aux conclusions.",
    "change_copy": (
        "Diagnostic & continuité rapproche les symptômes, les changements et les mesures "
        "disponibles pour guider les vérifications sans prétendre connaître la cause trop tôt."
    ),
    "features": [
        ("Détection précoce", "Repérer les dérives de capteurs, températures, consommations ou communications avant un arrêt complet."),
        ("Arbre de vérification", "Classer les causes possibles et proposer les contrôles les moins risqués en premier."),
        ("Contexte des changements", "Relier le symptôme aux mises à jour, interventions et événements qui l’ont précédé."),
        ("Dossier technicien", "Préparer mesures, photos, historique, pièces possibles et étapes déjà vérifiées."),
        ("Sauvegarde et retour", "Documenter les configurations, mises à jour et options de retour lorsque le système le permet."),
        ("Suivi continu", "Vérifier après l’intervention que le service est réellement stable et que la cause est comprise."),
    ],
    "demo_title": "Vérifier les causes <em>dans le bon ordre.</em>",
    "demo_copy": (
        "Équipement, infrastructure, logiciel ou véhicule : le même principe s’applique — "
        "vérifier l’alimentation, les communications et le contexte avant de proposer une action."
    ),
    "showcase": SHOWCASE,
    "compat": ["Capteurs", "Journaux", "OBD véhicule", "Énergie", "Réseau", "Procédures", "Historique"],
    "deploy_title": "Le dossier reste avec le lieu et ses responsables.",
    "deploy_copy": (
        "Les mesures, hypothèses et rapports demeurent dans l’environnement concerné. "
        "Ils peuvent être transmis à un technicien choisi, jamais diffusés par défaut."
    ),
    "limit": (
        "Le diagnostic assiste la compréhension et la préparation. Les interventions physiques, "
        "électriques ou mécaniques restent le travail de personnes qualifiées."
    ),
    "cta_title": "Quelle panne récurrente mérite enfin <em>une vraie enquête?</em>",
    "cta_copy": (
        "Décrivez le symptôme, les systèmes touchés et ce qui a déjà été tenté. Nous "
        "déterminerons les preuves à rassembler en premier."
    ),
}

PAGE = solution_page(DATA)
