# Confiance — les huit principes, une ligne chacun (refonte « essentiel », novembre 2026).

PRINCIPLES = [
    ("Minimisation", "Utiliser seulement ce qui est nécessaire."),
    ("Provenance", "Montrer d’où vient l’information."),
    ("Approbation", "Adapter le contrôle au risque."),
    ("Réversibilité", "Prévoir l’arrêt et le retour."),
    ("Localité", "Garder les fonctions essentielles chez vous."),
    ("Honnêteté", "Publier la maturité et les limites."),
    ("Propriété", "Permettre l’export et définir la rétention."),
    ("Continuité", "Tester sauvegarde, restauration et reprise."),
]

RULES_HTML = "".join(
    f'<article class="card" data-rev><small>{i + 1:02d} · {name}</small><h3>{title}</h3></article>'
    for i, (name, title) in enumerate(PRINCIPLES)
)

PAGE = {
    "url": "/confiance/",
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
    <p class="eyebrow" data-rev>Confiance et gouvernance</p>
    <h1 data-rev>La capacité d’agir exige <em>des limites visibles.</em></h1>
    <p class="lead" data-rev>Huit principes décident de ce que JARVIS peut voir et faire.</p>
  </div>
</section>

<section class="sect" id="principes" aria-label="Les huit principes">
  <div class="cards">{RULES_HTML}</div>
</section>

<section class="cta">
  <h2 data-rev>Un projet sensible?</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
  <p class="pro-suite" data-rev><a href="/confidentialite/">Confidentialité</a><a href="/mentions-legales/">Mentions légales</a></p>
</section>
""",
}
