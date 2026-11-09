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

<section class="sect alt" id="en-profondeur" aria-labelledby="prof-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le projet, en profondeur</p>
      <h2 id="prof-titre">Tout ce qui se cache<br><em>derrière JARVIS.</em></h2>
    </div>
    <p data-rev>La vision, le terrain de preuve, la façon de protéger vos données et ce qui fait tourner
    le logiciel : chaque page reste ouverte à tous.</p>
  </div>
  <div class="cards prof-cards">
    <a class="card" href="/vision-roadmap/" data-rev><small>Notre vision</small><h3>Rendre les gens libres.</h3><p>Les horizons de JARVIS et l’état réel du projet, jalon par jalon.</p></a>
    <a class="card" href="/laboratoire-mobile/" data-rev><small>Laboratoire mobile</small><h3>Une ambulance devenue laboratoire.</h3><p>Le premier JARVIS sur la route, avec ses batteries en direct.</p></a>
    <a class="card" href="/confiance/" data-rev><small>Confiance et sécurité</small><h3>Vos données restent à vous.</h3><p>Comment JARVIS protège vos informations, vos accès et vos décisions.</p></a>
    <a class="card" href="/plateforme/" data-rev><small>Sous le capot</small><h3>Le Hub et l’IA privée.</h3><p>Le Hub, son IA locale, le noyau en Rust, les comptes et les droits.</p></a>
    <a class="card" href="/recherche/" data-rev><small>Recherche</small><h3>Une preuve avant chaque promesse.</h3><p>La méthode de recherche appliquée derrière chaque solution.</p></a>
    <a class="card" href="/confidentialite/" data-rev><small>Confidentialité</small><h3>Ce que le site recueille.</h3><p>Notre politique de confidentialité, en mots simples.</p></a>
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
