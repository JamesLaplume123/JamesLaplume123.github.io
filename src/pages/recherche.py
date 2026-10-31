# Recherche — expliquer la méthode de validation.

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
    f"""<article class="card" data-reveal>
      <p class="eyebrow">{domain}</p>
      <h3>{question}</h3>
      <p><b style="color:var(--gold-bright);font-weight:500;">Hypothèse.</b> {hypothesis}</p>
      <ul><li>Terrain · {terrain}</li></ul>
    </article>"""
    for domain, question, hypothesis, terrain in QUESTIONS
)

MATURITY_HTML = "".join(
    f"""<div>
      <h3>{title}</h3>
      <p>{a} · {b}</p>
    </div>"""
    for title, a, b in MATURITY
)

PAGE = {
    "url": "/recherche/",
    "title": "Recherche JARVIS | Méthode, essais et preuves",
    "description": "Le journal public des hypothèses, expériences, mesures et limites du projet JARVIS.",
    "og_image": "/media/solutions/diagnostic-care.webp",
    "content": f"""
<section class="hero page-hero">
  <div class="hero-media">
    <img src="/media/solutions/diagnostic-care.webp" alt="" fetchpriority="high">
  </div>
  <div class="shell hero-inner">
    <div>
      <p class="eyebrow">Recherche appliquée</p>
      <h1>Des idées ambitieuses.<br><em>Des preuves vérifiables.</em></h1>
      <p class="lead">Le projet avance par questions, prototypes, mesures et décisions
      documentées. Cette section devient la mémoire publique de ce qui est testé, appris et
      corrigé.</p>
      <div class="hero-meta">
        <div><span>Méthode</span><b>Hypothèse → essai → preuve</b></div>
        <div><span>Transparence</span><b>Limites publiées</b></div>
        <div><span>Sécurité</span><b>Détails sensibles privés</b></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div data-reveal>
      <p class="eyebrow">Le cadre</p>
      <h2>Le site présente. <em>La recherche démontre.</em></h2>
    </div>
    <p class="lead" data-reveal>Chaque sujet public sera relié à une question précise, un
    protocole, des observations et une conclusion limitée. Les secrets, accès, données
    personnelles et architectures exploitables restent dans un dépôt privé. Une démonstration
    n’est pas encore une validation.</p>
  </div>
</section>

<section class="section section-raised">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Programme de recherche</p>
        <h2>Les six solutions produisent <em>leurs propres questions.</em></h2>
      </div>
      <p>Le laboratoire mobile JARVIS est un premier terrain d’essai. D’autres environnements
      seront nécessaires pour éviter de confondre une preuve locale avec une solution
      générale.</p>
    </div>
    <div class="card-grid">
      {QUESTIONS_HTML}
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Niveaux de maturité</p>
        <h2>Dire précisément où <em>chaque élément se trouve.</em></h2>
      </div>
      <p>Le même vocabulaire est utilisé dans le site, les documents de recherche et la
      feuille de route.</p>
    </div>
    <div class="steps" data-reveal>
      {MATURITY_HTML}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="shell cta-inner" data-reveal>
    <div>
      <p class="eyebrow">Premier échange</p>
      <h2>Un centre de recherche, un partenaire ou <em>un terrain d’essai?</em></h2>
    </div>
    <div>
      <p>Décrivez le problème et son contexte. La première preuve utile sera clairement
      définie.</p>
      <a class="button button-fill" href="/contact/">Discuter du projet <span>↗</span></a>
    </div>
  </div>
</section>
""",
}
