# Recherche — expliquer la méthode de validation. Version wow.

QUESTIONS = [
    ("Environnements intelligents", "Une automatisation peut-elle rester utile sans devenir imprévisible?",
     "Le contexte et une explication simple réduisent les corrections manuelles.", "Maison, atelier et véhicule · Laboratoire"),
    ("IA privée et connaissances", "Comment rendre une réponse vérifiable sans ralentir le travail?",
     "La provenance, les permissions et la mission améliorent la confiance utile.", "Documents et procédures autorisés · En développement"),
    ("Sécurité intelligente", "Le contexte peut-il réduire le bruit sans produire de fausse certitude?",
     "Une chronologie multi-source aide mieux qu’une accumulation d’alertes.", "Événements simulés · Feuille de route"),
    ("Automatisation d’entreprise", "Où placer l’humain pour accélérer sans perdre la responsabilité?",
     "Une approbation au bon endroit vaut mieux que des contrôles partout.", "Processus pilotes à définir · Priorité commerciale"),
    ("Réseau et cybersécurité", "Comment expliquer une dégradation avant qu’elle devienne une panne?",
     "Topologie, historique et dépendances réduisent le temps de diagnostic.", "Réseaux de laboratoire · Roadmap spécialisée"),
    ("Diagnostic & continuité", "Combien de causes peut-on éliminer avant l’intervention physique?",
     "Événements, capteurs et documentation rendent le dossier technicien plus utile.", "Équipements et véhicule · Prototype"),
]

MATURITY = [
    ("Idée", "Question formulée", "Aucune preuve fonctionnelle"),
    ("Laboratoire", "Essai contrôlé", "Conditions limitées"),
    ("Prototype", "Parcours fonctionnel", "Fiabilité incomplète"),
    ("Validé", "Critères mesurés", "Résultats documentés"),
    ("Pilote", "Déploiement supervisé", "Utilisateur réel"),
    ("Commercial", "Produit et soutien définis", "Offre répétable"),
]

QUESTIONS_HTML = "".join(
    f"""<article class="card" data-rev>
      <small>{domain}</small>
      <h3>{question}</h3>
      <p>{hypothesis}</p>
    </article>"""
    for domain, question, hypothesis, terrain in QUESTIONS
)

MATURITY_HTML = "".join(
    f"""<div class="row" data-rev>
      <i>Niveau {j + 1:02d}</i>
      <div><h3>{title}</h3><p>{a} · {b}</p></div>
    </div>"""
    for j, (title, a, b) in enumerate(MATURITY)
)

PAGE = {
    "url": "/recherche/",
    "v2": True,
    "title": "Recherche JARVIS | Méthode, essais et preuves",
    "description": "Le journal public des hypothèses, expériences, mesures et limites du projet JARVIS.",
    "og_image": "/media/solutions/diagnostic-care.webp",
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/diagnostic-care.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Recherche appliquée</p>
    <h1 data-rev>Des idées ambitieuses.<br><em>Des preuves vérifiables.</em></h1>
    <p class="lead" data-rev>Une question, un essai, une mesure : rien n’est promis avant la preuve.</p>
  </div>
</section>

<section class="sect alt" id="questions-de-recherche" aria-labelledby="rq-titre">
  <div class="sect-head">
    <div data-rev>
      <h2 id="rq-titre">Chaque solution a <em>sa question.</em></h2>
    </div>
  </div>
  <div class="cards">
    {QUESTIONS_HTML}
  </div>
</section>

<section class="sect" id="maturite" aria-labelledby="mat-titre">
  <div class="sect-head">
    <div data-rev>
      <h2 id="mat-titre">Six niveaux <em>de maturité.</em></h2>
    </div>
  </div>
  <div class="rows">
    {MATURITY_HTML}
  </div>
</section>

<section class="cta">
  <h2 data-rev>Un terrain d’essai<br><span>à proposer?</span></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
