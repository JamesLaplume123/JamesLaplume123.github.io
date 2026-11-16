# À propos — qui est derrière JARVIS, comment on travaille, ce qu'on s'engage à faire.
# Refonte « essentiel » (novembre 2026) : une phrase, cinq étapes, six engagements, une ligne de
# liens vers le reste (vision, laboratoire, confiance, offre). Aucune mention de lieu.

import pro

PAGE = {
    "url": "/a-propos/",
    "v2": True,
    "title": "À propos de JARVIS Private Systems",
    "description": (
        "Une entreprise de technologie et de sécurité fondée par James Laplume. Qui nous "
        "sommes, comment on travaille et ce que vous pouvez exiger de nous."
    ),
    "og_image": "/media/solutions/automatisation-operations.webp",
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-life-context-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>À propos · JARVIS Private Systems</p>
    <h1 data-rev>Protéger ce qui <em>vous appartient.</em></h1>
    <p class="lead" data-rev>Je m’appelle James Laplume. J’ai fondé JARVIS Private Systems pour
    protéger vos lieux, votre réseau et vos données, en vous laissant toujours la décision.</p>
  </div>
</section>

""" + pro.comment_on_travaille() + "\n\n" + pro.engagements() + """

<section class="cta">
  <h2 data-rev>Parlons de votre projet.</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
  <p class="pro-suite" data-rev><a href="/offre/">L’offre</a><a href="/vision-roadmap/">Notre vision</a>
  <a href="/laboratoire-mobile/">Laboratoire mobile</a><a href="/confiance/">Confiance</a>
  <a href="/questions/">Questions</a></p>
</section>
""",
}
