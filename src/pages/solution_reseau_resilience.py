# Solution 05 — Réseau et cybersécurité.

from pages._solution import solution_page

SHOWCASE = """
<div class="split" data-reveal>
  <figure class="showcase-frame" style="margin:0;">
    <img src="/media/solutions/reseau-resilience.webp"
         alt="Infrastructure réseau surveillée par JARVIS" loading="lazy">
    <figcaption>
      <span>TOPOLOGIE · SITE PRINCIPAL</span>
      <strong>Localiser une anomalie sans accuser tout le système.</strong>
    </figcaption>
  </figure>
  <aside class="console" style="max-width:none;">
    <header class="console-head"><span><i></i>SURVEILLANCE · ACTIVE</span><small>LOCAL</small></header>
    <div class="console-body">
      <small>ANOMALIE DÉTECTÉE</small>
      <strong>Lien de secours LTE dégradé depuis 14 minutes.</strong>
      <p>La carte isole la dégradation sur un lien précis tout en montrant que le reste du site
      demeure stable. Le lien principal et les services essentiels ne sont pas touchés.</p>
    </div>
    <ul class="console-signals">
      <li><span>APPAREILS</span><b>24 suivis</b></li>
      <li><span>LIEN PRINCIPAL</span><b>Stable</b></li>
      <li><span>ACTION</span><b>Vérification proposée</b></li>
    </ul>
  </aside>
</div>
"""

DATA = {
    "slug": "reseau-resilience",
    "title": "Réseau et cybersécurité",
    "description": "Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.",
    "image": "/media/solutions/reseau-resilience.webp",
    "h1": "Réseau et <em>cybersécurité.</em>",
    "lead": "Une vue claire du réseau et de ses risques, avant que chaque problème devienne une urgence.",
    "for": "Entreprises, multi-sites et environnements technologiques complexes",
    "problem_title": "Le réseau soutient tout le reste, <em>mais devient visible seulement lorsqu’il tombe.</em>",
    "problem_copy": (
        "Cette solution vise l’inventaire, la topologie, la disponibilité, les liens Internet, "
        "la segmentation et les accès privés. Elle joue le rôle d’une couche d’observation et "
        "d’assistance pour l’administrateur, sans promettre une cybersécurité magique."
    ),
    "change_title": "Une infrastructure visible avant qu’elle devienne urgente.",
    "change_copy": (
        "L’inventaire, la topologie et l’historique rendent les dépendances visibles avant "
        "qu’une panne ne devienne une enquête improvisée."
    ),
    "features": [
        ("Inventaire vivant", "Identifier les équipements autorisés, leur rôle, leur état et leurs dépendances."),
        ("Topologie compréhensible", "Montrer comment les sites, réseaux, passerelles et services essentiels sont reliés."),
        ("Disponibilité surveillée", "Repérer une dégradation de connexion, une perte de service ou un équipement instable."),
        ("Accès privé", "Préparer des accès distants limités, documentés et révocables plutôt qu’exposer les systèmes."),
        ("Segmentation progressive", "Séparer les appareils, utilisateurs et fonctions selon les risques et besoins réels."),
        ("Contexte pour le diagnostic", "Transmettre à Diagnostic & continuité les événements réseau pertinents lorsqu’une panne touche plusieurs systèmes."),
    ],
    "demo_title": "Localiser une anomalie <em>sans accuser tout le système.</em>",
    "demo_copy": (
        "Wi-Fi, VPN, LTE, Starlink et multi-sites : la même lecture claire des liens, "
        "des dépendances et de ce qui mérite une vérification."
    ),
    "showcase": SHOWCASE,
    "compat": ["Wi-Fi", "VPN", "LTE", "Starlink", "Pare-feu", "VLAN", "Journaux", "Multi-sites"],
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

DATA["demo_image"] = "/media/product/outils/reseau.jpg"
DATA["demo_caption"] = "Écran de référence de l’outil Réseau — maquette, données fictives."

PAGE = solution_page(DATA)
