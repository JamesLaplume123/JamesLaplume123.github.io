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
  <h2 data-rev>La technologie devrait libérer du temps,<br><em>pas en voler.</em></h2>
  <p data-rev>Les bons appareils, logiciels et modèles existent souvent déjà. Mon travail
  consiste à comprendre le système complet, construire les liens manquants et vérifier dans
  le réel que l’ensemble demeure utile, compréhensible et contrôlable. JARVIS est la
  plateforme. Le laboratoire mobile JARVIS est le premier grand terrain de preuve. À terme,
  JARVIS Private Systems veut devenir une entreprise de sécurité privée, avec la même exigence :
  protéger les lieux et les personnes, en expliquant toujours ce qui se passe.</p>
</section>

""" + galerie.a_propos_terrain() + """

<section class="sect">
  <div class="cards">
    <article class="card" data-rev>
      <small>01 · Liberté</small>
      <h3>Rendre du temps et du contrôle.</h3>
      <p>Ce qui se répète se fait seul; ce qui compte reste entre vos mains.</p>
    </article>
    <article class="card" data-rev>
      <small>02 · Clarté</small>
      <h3>Dire ce qui est réel.</h3>
      <p>Les concepts, prototypes, validations et offres futures sont identifiés séparément.</p>
    </article>
    <article class="card" data-rev>
      <small>03 · Contrôle</small>
      <h3>Laisser le dernier mot.</h3>
      <p>Le système propose et prépare; la personne demeure responsable des décisions
      sensibles.</p>
    </article>
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Collaborations recherchées</p>
      <h2>Des regards exigeants et <em>des terrains réels.</em></h2>
    </div>
    <div class="side" data-rev>
      <p>Le projet peut bénéficier de partenaires en recherche, énergie, véhicules, bâtiment,
      sécurité, réseau, expérience utilisateur et développement de produit.</p>
      <p>L’objectif n’est pas de prétendre tout maîtriser seul, mais de construire une
      architecture cohérente avec les bonnes expertises. Ouvert aux conversations sérieuses,
      aux critiques et aux collaborations structurées.</p>
    </div>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Parlons du problème, de l’expertise ou du terrain<br><span>que vous pourriez
  apporter.</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement
  définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
