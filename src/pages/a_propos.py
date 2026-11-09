# À propos — James, sa démarche et les collaborations recherchées. Version wow.

import galerie

PAGE = {
    "url": "/a-propos/",
    "assets": ["galerie"],
    "v2": True,
    "title": "À propos | James Laplume et JARVIS",
    "description": (
        "Découvrez James Laplume, la philosophie de JARVIS et l’approche de recherche "
        "appliquée derrière le projet."
    ),
    "og_image": "/media/solutions/automatisation-operations.webp",
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-life-context-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>À propos</p>
    <h1 data-rev>Rendre les gens libres, <em>par la technologie.</em></h1>
    <p class="lead" data-rev>Je m’appelle James Laplume. La liberté est ma valeur la plus forte.
    Je développe JARVIS pour la rendre concrète : du temps libéré, le contrôle de sa vie en toute
    simplicité, et une sécurité privée qui protège sans surveiller.</p>
    <div class="meta" data-rev>
      <span class="chip">Québec, Canada</span>
      <span class="chip">Prototypes et preuves</span>
      <span class="chip">Technique · recherche · terrain</span>
    </div>
  </div>
</section>

<section class="statement">
  <p class="eyebrow" data-rev>Pourquoi ce projet</p>
  <h2 data-rev>Comprendre le système complet.<br><em>Construire les liens manquants.</em></h2>
  <p data-rev>Les bons appareils, logiciels et modèles existent souvent déjà. Mon travail
  consiste à comprendre le système complet, construire les liens manquants et vérifier dans
  le réel que l’ensemble demeure utile, compréhensible et contrôlable. JARVIS est la
  plateforme. Le <a href="/laboratoire-mobile/">laboratoire mobile JARVIS</a> est le premier
  grand terrain de preuve, avec ses batteries en direct. À terme,
  JARVIS Private Systems veut devenir une entreprise de sécurité privée, avec la même exigence :
  protéger les lieux et les personnes, en expliquant toujours ce qui se passe.</p>
  <div class="acts" data-rev>
    <a class="pill ghost" href="/laboratoire-mobile/">Voir le laboratoire en direct</a>
    <a class="pill ghost" href="/vision-roadmap/#partenariats">Les partenaires recherchés</a>
  </div>
</section>

""" + galerie.a_propos_terrain() + """

<section class="cta">
  <h2 data-rev>Parlons du problème, de l’expertise ou du terrain<br><span>que vous pourriez
  apporter.</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement
  définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
