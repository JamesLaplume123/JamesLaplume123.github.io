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
      <p><b style="color:var(--gold-soft);font-weight:550">Hypothèse.</b> {hypothesis}</p>
      <ul><li>Terrain · {terrain}</li></ul>
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
    <p class="lead" data-rev>Le projet avance par questions, prototypes, mesures et décisions
    documentées. Cette section devient la mémoire publique de ce qui est testé, appris et
    corrigé.</p>
    <div class="meta" data-rev>
      <span class="chip">Hypothèse → essai → preuve</span>
      <span class="chip">Limites publiées</span>
      <span class="chip">Détails sensibles privés</span>
    </div>
  </div>
</section>

<section class="statement">
  <p class="eyebrow" data-rev>Le cadre</p>
  <h2 data-rev style="margin-top:1.2rem">Le site présente.<br><em>La recherche démontre.</em></h2>
  <p data-rev>Chaque sujet public sera relié à une question précise, un protocole, des
  observations et une conclusion limitée. Les secrets, accès, données personnelles et
  architectures exploitables restent dans un dépôt privé. Une démonstration n’est pas encore
  une validation.</p>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Programme de recherche</p>
      <h2 style="margin-top:1rem">Les six solutions produisent <em>leurs propres
      questions.</em></h2>
    </div>
    <p data-rev>Le laboratoire mobile JARVIS est un premier terrain d’essai. D’autres
    environnements seront nécessaires pour éviter de confondre une preuve locale avec une
    solution générale.</p>
  </div>
  <div class="cards">
    {QUESTIONS_HTML}
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Niveaux de maturité</p>
      <h2 style="margin-top:1rem">Dire précisément où <em>chaque élément se trouve.</em></h2>
    </div>
    <p data-rev>Le même vocabulaire est utilisé dans le site, les documents de recherche et
    la feuille de route.</p>
  </div>
  <div class="rows">
    {MATURITY_HTML}
  </div>
</section>

<section class="cta">
  <h2 data-rev>Un centre de recherche, un partenaire<br><span>ou un terrain d’essai?</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement
  définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
