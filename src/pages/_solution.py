# Gabarit commun des pages de solution.
# Chaque module fournit un dict DATA ; solution_page() le transforme en page :
# bande immersive → démonstration interactive (le cœur) → « En clair »
# (avant / avec JARVIS, ce que vous obtenez) → déploiement responsable → démo.

from config import CAPABILITIES
from demos import coquille


# Image d'aperçu, utilisée tant qu'une solution n'a pas sa démo interactive (DATA["demo_html"]).
FRAME = """<figure class="frame" data-rev>
    <img src="{img}" alt="Aperçu conceptuel — {title}" loading="lazy">
    <figcaption>
      <span>JARVIS App · {up}</span>
      <strong>{cap}</strong>
    </figcaption>
  </figure>"""


def clair_section(c):
    """Bloc « En clair » : la solution expliquée simplement, avant / avec JARVIS."""
    if not c:
        return ""
    avant = "".join(f"<li>{x}</li>" for x in c["avant"])
    apres = "".join(f"<li>{x}</li>" for x in c["apres"])
    obtenez = "".join(
        f"""<article class="card" data-rev><small>{i + 1:02d}</small><h3>{t}</h3><p>{p}</p></article>"""
        for i, (t, p) in enumerate(c["obtenez"])
    )
    return f"""
<section class="clair" aria-labelledby="clair-titre">
  <div class="clair-head" data-rev>
    <p class="eyebrow">En clair</p>
    <h2 id="clair-titre">{c['quoi']}</h2>
    <p class="clair-ex"><b>Exemple concret.</b> {c['exemple']}</p>
  </div>
  <div class="vs" data-rev>
    <div class="vs-col vs-before"><p class="vs-k">Aujourd’hui, sans JARVIS</p><ul>{avant}</ul></div>
    <div class="vs-arrow" aria-hidden="true"><span></span></div>
    <div class="vs-col vs-after"><p class="vs-k">Avec JARVIS</p><ul>{apres}</ul></div>
  </div>
  <p class="eyebrow clair-k" data-rev>Ce que vous obtenez</p>
  <div class="cards">{obtenez}</div>
</section>"""


def solution_page(d):
    num = next((c["num"] for c in CAPABILITIES if c["slug"] == d["slug"]), "0X")
    compat = "".join(f'<span class="chip">{c}</span>' for c in d["compat"])
    return {
        "url": f"/solutions/{d['slug']}/",
        "v2": True,
        "title": f"{d['title']} | Solutions JARVIS",
        "description": d["description"],
        "og_image": d["image"],
        "assets": ["coquille", *d.get("assets", [])],
        "content": f"""
<section class="band top">
  <div class="bg"><img src="{d['image']}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution {num} / 07</p>
    <h1 data-rev>{d['h1']}</h1>
    <p class="lead" data-rev>{d['lead']}</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="/solutions/">Toutes les solutions</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> {d['for']}</p>
  </div>
</section>

<section class="sect sol-demo">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez · démonstration interactive</p>
      <h2>{d['demo_title']}</h2>
    </div>
    <p data-rev>{d['demo_copy']}</p>
  </div>
  {coquille.html(d['slug'], d.get('demo_html') or FRAME.format(img=d.get('demo_image', d['image']), title=d['title'], up=d['title'].upper(), cap=d.get('demo_caption', 'Prototype interactif — données simulées.')))}
  {d.get('extra', '')}
</section>

{clair_section(d.get("clair"))}

<section class="sect sol-trust">
  <div class="trust" data-rev>
    <div>
      <p class="eyebrow">Déploiement responsable</p>
      <h2>{d['deploy_title']}</h2>
      <p>{d['deploy_copy']}</p>
    </div>
    <dl>
      <div><dt>Accord humain</dt><dd>Les actions sensibles exigent une validation adaptée au risque.</dd></div>
      <div><dt>Limite publiée</dt><dd>{d['limit']}</dd></div>
      <div><dt>Compatibilités possibles</dt><dd class="chips">{compat}</dd></div>
    </dl>
  </div>
</section>

<section class="cta">
  <h2 data-rev>{d['cta_title']}</h2>
  <p data-rev>{d['cta_copy']}</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
    }
