# Confiance — les règles communes de gouvernance.

PRINCIPLES = [
    ("Minimisation", "Utiliser seulement ce qui est nécessaire.",
     "Une mission reçoit les sources, outils et durées utiles à son objectif, pas un accès général par défaut."),
    ("Provenance", "Montrer d’où vient l’information.",
     "Une réponse importante distingue les faits observés, les sources consultées et les hypothèses produites."),
    ("Approbation", "Adapter le contrôle au risque.",
     "Les actions sensibles, irréversibles ou externes demeurent entre les mains d’une personne autorisée."),
    ("Réversibilité", "Prévoir l’arrêt et le retour.",
     "Les automatisations doivent pouvoir être suspendues et les changements importants documentés."),
    ("Localité", "Garder les fonctions essentielles près du site.",
     "Le cloud est utilisé lorsqu’il apporte une valeur comprise, jamais comme dépendance cachée."),
    ("Honnêteté", "Publier la maturité et les limites.",
     "Une idée, un prototype et une solution commerciale ne sont jamais présentés comme équivalents."),
    ("Propriété", "Permettre l’export et définir la rétention.",
     "Le propriétaire des données, leur durée de conservation et les possibilités d’export ou de suppression sont établis par le mandat."),
    ("Continuité", "Tester sauvegarde, restauration et reprise.",
     "Les configurations et données essentielles doivent pouvoir être restaurées selon une procédure vérifiée."),
]

RULES_HTML = "".join(
    f"""<div data-reveal>
      <span>0{i + 1} · {name}</span>
      <div>
        <h3>{title}</h3>
        <p>{copy}</p>
      </div>
    </div>"""
    for i, (name, title, copy) in enumerate(PRINCIPLES)
)

PAGE = {
    "url": "/confiance/",
    "title": "Confiance et gouvernance | JARVIS",
    "description": (
        "Les principes de vie privée, permissions, provenance, contrôle humain et "
        "transparence qui guident JARVIS."
    ),
    "og_image": "/media/solutions/securite-intelligente.webp",
    "content": f"""
<section class="hero page-hero">
  <div class="hero-media">
    <img src="/media/solutions/securite-intelligente.webp" alt="" fetchpriority="high">
  </div>
  <div class="shell hero-inner">
    <div>
      <p class="eyebrow">Confiance et gouvernance</p>
      <h1>La capacité d’agir exige <em>des limites visibles.</em></h1>
      <p class="lead">Vie privée, sécurité, provenance et contrôle humain ne sont pas des
      options ajoutées après coup. Ils définissent la manière dont JARVIS peut accéder à une
      source ou agir dans le monde réel.</p>
      <div class="hero-meta">
        <div><span>Données</span><b>Accès explicites</b></div>
        <div><span>Actions</span><b>Approbations selon le risque</b></div>
        <div><span>Historique</span><b>Preuves et journalisation</b></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Principes de conception</p>
        <h2>Savoir qui peut voir, comprendre <em>et agir.</em></h2>
      </div>
      <p>Ces principes sont des objectifs d’architecture. Leur mise en œuvre doit être
      vérifiée pour chaque solution et chaque déploiement.</p>
    </div>
    <div class="rules">
      {RULES_HTML}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="shell cta-inner" data-reveal>
    <div>
      <p class="eyebrow">Premier échange</p>
      <h2>Un projet sensible commence par définir <em>les responsabilités.</em></h2>
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
