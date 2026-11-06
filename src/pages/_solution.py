# Gabarit commun des six pages de solution — version « wow ».
# Chaque module de solution fournit un dict DATA ; solution_page() le
# transforme en page complète : bande immersive → problème → ce qui change →
# aperçu → déploiement responsable → démo.
# Le champ DATA["showcase"] (démonstrations v1) est conservé mais inutilisé :
# les aperçus détaillés reviendront avec le contenu final (PDF).

from config import CAPABILITIES


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
    features = "".join(
        f"""<article class="card" data-rev>
          <small>0{i + 1}</small>
          <h3>{f[0]}</h3>
          <p>{f[1]}</p>
        </article>"""
        for i, f in enumerate(d["features"])
    )
    compat = "".join(f'<span class="chip">{c}</span>' for c in d["compat"])
    return {
        "url": f"/solutions/{d['slug']}/",
        "v2": True,
        "title": f"{d['title']} | Solutions JARVIS",
        "description": d["description"],
        "og_image": d["image"],
        "assets": d.get("assets", []),
        "content": f"""
<section class="band top">
  <div class="bg"><img src="{d['image']}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution {num} / 06</p>
    <h1 data-rev>{d['h1']}</h1>
    <p class="lead" data-rev>{d['lead']}</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="/solutions/">Toutes les solutions</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip chip-sim">Interface conceptuelle · fondation en construction</span>
      <span class="chip">{d['for']}</span>
      <span class="chip">Local, privé ou hybride</span>
      <span class="chip">Contrôle humain</span>
    </div>
  </div>
</section>

{clair_section(d.get("clair"))}

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le problème à résoudre</p>
      <h2 style="margin-top:1rem">{d['problem_title']}</h2>
    </div>
    <p data-rev>{d['problem_copy']}</p>
  </div>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ce que la solution change</p>
      <h2 style="margin-top:1rem">{d['change_title']}</h2>
    </div>
    <p data-rev>{d['change_copy']}</p>
  </div>
  <div class="cards">
    {features}
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Aperçu conceptuel · données simulées</p>
      <h2 style="margin-top:1rem">{d['demo_title']}</h2>
    </div>
    <p data-rev>{d['demo_copy']}</p>
  </div>
  {d.get('demo_html') or FRAME.format(img=d.get('demo_image', d['image']), title=d['title'], up=d['title'].upper(), cap=d.get('demo_caption', 'Prototype interactif — données simulées.'))}
  {d.get('extra', '')}
  <div class="chiprow" data-rev>
    <span class="chip chip-sim">Compatibilités possibles</span>
    {compat}
  </div>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Déploiement responsable</p>
      <h2 style="margin-top:1rem">{d['deploy_title']}</h2>
    </div>
    <p data-rev>{d['deploy_copy']}</p>
  </div>
  <div class="cards two">
    <article class="card" data-rev>
      <small>Accord humain</small>
      <h3>Les actions sensibles exigent une validation adaptée au risque.</h3>
    </article>
    <article class="card" data-rev>
      <small>Limite publiée</small>
      <h3 style="font-weight:500;font-size:1rem;color:#b9b9c2;line-height:1.6">{d['limit']}</h3>
    </article>
  </div>
</section>

<section class="cta">
  <h2 data-rev>{d['cta_title']}</h2>
  <p data-rev>{d['cta_copy']}</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
    }
