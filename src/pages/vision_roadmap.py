# Vision et feuille de route — le manifeste de JARVIS : rendre les gens libres.
# Refonte « essentiel » (novembre 2026) : manifeste → horizons (maintenant, 12 mois, 3 ans,
# 10 ans) → feuille de route réelle (src/demos/feuille.py). Les démonstrations de vision
# « Personal Intelligence » (src/demos/vie.py) et « Security Pro » (src/demos/pentest.py) ne sont
# plus affichées; leurs modules restent dans le dépôt.

import re

from demos import feuille, vision
import pro


def _fr(s):
    """Typographie française du texte de la page (pas des démos : leur géométrie reste intacte)."""
    s = re.sub(r"(\d) (minutes|h|ans|mois)\b", "\\1\u00a0\\2", s)
    s = re.sub(r"\s+([:;?!»])", "\u00a0\\1", s)
    return s.replace("« ", "«\u00a0")


def _head(titre):
    return f"""<div class="sect-head vn-head">
    <div data-rev>
      <h2>{titre}</h2>
    </div>
  </div>"""


PAGE = {
    "url": "/vision-roadmap/",
    "v2": True,
    "title": "Vision JARVIS : rendre les gens libres | Feuille de route",
    "description": (
        "Le manifeste de JARVIS : un système privé installé chez vous qui rend du temps, garde "
        "vos données et vous laisse décider. Horizons à 12 mois, 3 ans et 10 ans, et l’état réel du projet."
    ),
    "og_image": "/media/concept/jarvis-future-ecosystem-v1.webp",
    "assets": ["vision", "feuille"],
    "content": _fr("""
<section class="band top vn-hero">
  <div class="bg"><img src="/media/concept/jarvis-future-ecosystem-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    """ + pro.fil("/vision-roadmap/") + """
    <h1 data-rev style="max-width:none">Rendre les gens libres.<br><em>Un système privé à la fois.</em></h1>
    <p class="lead" data-rev>Où va JARVIS, et où il en est vraiment.</p>
  </div>
</section>

<section class="sect" id="manifeste">
  @@MANIFESTE@@
</section>

<section class="sect alt" id="horizons">
  """ + _head("Maintenant. 12 mois. 3 ans. <em>10 ans.</em>") + """
  @@HORIZONS@@
</section>

<section class="sect" id="feuille-de-route">
  """ + _head("Ce qui existe. Ce qui se construit. <em>Ce qui viendra après.</em>") + """
  @@FEUILLE@@
</section>

<section class="cta">
  <h2 data-rev>Discuter de la vision<br><span>ou d’un partenariat ?</span></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
  <p class="pro-suite" data-rev><a href="/recherche/">La méthode de recherche</a><a href="/laboratoire-mobile/">Laboratoire mobile</a></p>
</section>
""")
    .replace("@@MANIFESTE@@", vision.manifeste())
    .replace("@@HORIZONS@@", vision.horizons())
    .replace("@@FEUILLE@@", feuille.html()),
}
