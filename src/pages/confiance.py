# Confiance — les règles communes de gouvernance. Version wow.

import galerie
import pro

PRINCIPLES = [
    ("Minimisation", "Utiliser seulement ce qui est nécessaire.",
     "Une mission reçoit les sources, outils et durées utiles à son objectif, pas un accès général par défaut."),
    ("Provenance", "Montrer d’où vient l’information.",
     "Une réponse importante distingue les faits observés, les sources consultées et les hypothèses produites."),
    ("Approbation", "Adapter le contrôle au risque.",
     "Les actions sensibles, irréversibles ou externes demeurent entre les mains d’une personne autorisée."),
    ("Réversibilité", "Prévoir l’arrêt et le retour.",
     "Les automatisations doivent pouvoir être suspendues et les changements importants documentés."),
    ("Localité", "Garder les fonctions essentielles chez vous.",
     "Le cloud est utilisé lorsqu’il apporte une valeur comprise, jamais comme dépendance cachée."),
    ("Honnêteté", "Publier la maturité et les limites.",
     "Une idée, un prototype et une solution commerciale ne sont jamais présentés comme équivalents."),
    ("Propriété", "Permettre l’export et définir la rétention.",
     "Le propriétaire des données, leur durée de conservation et les possibilités d’export ou de suppression sont établis par le mandat."),
    ("Continuité", "Tester sauvegarde, restauration et reprise.",
     "Les configurations et données essentielles doivent pouvoir être restaurées selon une procédure vérifiée."),
]

RULES_HTML = "".join(
    f"""<div class="row" data-rev>
      <i>0{i + 1} · {name}</i>
      <div><h3>{title}</h3><p>{copy}</p></div>
    </div>"""
    for i, (name, title, copy) in enumerate(PRINCIPLES)
)

PAGE = {
    "url": "/confiance/",
    "assets": ["galerie"],
    "v2": True,
    "title": "Confiance et gouvernance | JARVIS",
    "description": (
        "Les principes de vie privée, permissions, provenance, contrôle humain et "
        "transparence qui guident JARVIS."
    ),
    "og_image": "/media/solutions/securite-intelligente.webp",
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-earth-network-v1.jpg" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil("/confiance/")}
    <h1 data-rev>La capacité d’agir exige <em>des limites visibles.</em></h1>
    <p class="lead" data-rev>Huit principes décident de ce que JARVIS peut voir et faire.</p>
    <div class="meta" data-rev>
      <span class="chip">Accès explicites</span>
      <span class="chip">Approbations selon le risque</span>
      <span class="chip">Preuves et journalisation</span>
    </div>
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Principes de conception</p>
      <h2 style="margin-top:1rem">Savoir qui peut voir, comprendre <em>et agir.</em></h2>
    </div>

  </div>
  <div class="rows">
    {RULES_HTML}
  </div>
</section>

{galerie.confiance_visuels()}

<section class="cta">
  <h2 data-rev>Un projet sensible?</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
  <p class="pro-suite" data-rev><a href="/confidentialite/">Confidentialité</a><a href="/mentions-legales/">Mentions légales</a></p>
</section>
""",
}
