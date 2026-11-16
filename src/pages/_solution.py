# Gabarit commun des pages de solution (refonte « essentiel », novembre 2026).
# Une page = une idée, dite une fois : le titre et une phrase, LA démonstration interactive,
# trois points clés (config.CAPABILITIES), trois questions repliées (src/pro.py, ajoutées par
# partials.document) et un bouton.

from config import CAPABILITIES
from pages import catalogue as CAT
from demos import coquille
import pro

PRIX = {s["slug"]: ("Inclus avec chaque Hub" if s["prix"] == 0 else f"{s['prix']} $ par mois" + (" par véhicule" if s.get("unite") else "")) for s in CAT.SOLUTIONS}
PRIX["automatisation-operations"] = f"Dès {CAT.ENT_SOCLE['prix']} $ par mois, puis 9 à 29 $ par automatisation"

_CAP = {c["slug"]: c for c in CAPABILITIES}


def bande(slug, h1, lead, image):
    """Ouverture : le titre, une phrase, un bouton, le prix."""
    c = _CAP[slug]
    return f"""
<section class="band top">
  <div class="bg"><img src="{image}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil(f"/solutions/{slug}/")}
    <h1 data-rev>{h1}</h1>
    <p class="lead" data-rev>{lead}</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
    </div>
    <p class="for-line" data-rev><span>Prix</span> {PRIX.get(slug, 'Voir le catalogue')} · <a href="/catalogue/#solutions" style="color:var(--gold-soft)">Voir le catalogue</a></p>
  </div>
</section>
"""


def demo(slug, titre, html, extra="", ident="essayer"):
    """La démonstration interactive : le produit. Rien autour, sauf son titre."""
    return f"""
<section class="sect sol-demo" id="{ident}">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Démonstration interactive</p>
      <h2>{titre}</h2>
    </div>
  </div>
  {coquille.html(slug, html)}
  {extra}
</section>
"""


def points(slug):
    """Au plus trois points clés, une ligne chacun."""
    cartes = "".join(
        f'<article class="card" data-rev><h3>{t}</h3><p>{p}</p></article>' for t, p in _CAP[slug]["points"][:3]
    )
    return f"""
<section class="sect sol-points" aria-label="L’essentiel">
  <div class="cards">{cartes}</div>
</section>
"""


def fin(titre):
    return f"""
<section class="cta">
  <h2 data-rev>{titre}</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
"""


def solution_page(d):
    slug = d["slug"]
    return {
        "url": f"/solutions/{slug}/",
        "v2": True,
        "title": f"{d['title']} | Solutions JARVIS",
        "description": d["description"],
        "og_image": d["image"],
        "assets": ["coquille", *d.get("assets", [])],
        "content": bande(slug, d["h1"], d["lead"], d["image"])
        + demo(slug, d["demo_title"], d["demo_html"], d.get("extra", ""))
        + points(slug)
        + fin(d["cta_title"]),
    }
