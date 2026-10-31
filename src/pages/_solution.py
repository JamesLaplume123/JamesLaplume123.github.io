# Gabarit commun des six pages de solution.
# Chaque module de solution fournit un dict DATA ; solution_page() le
# transforme en page complète, structurée selon docs/SITE_INFORMATION_ARCHITECTURE.md :
# problème → résultat → bénéfices → aperçu → gouvernance → appel.


def solution_page(d):
    features = "".join(
        f"""<article class="card" data-reveal>
          <p class="eyebrow">0{i + 1}</p>
          <h3>{f[0]}</h3>
          <p>{f[1]}</p>
        </article>"""
        for i, f in enumerate(d["features"])
    )
    compat = "".join(f'<span class="badge"><i></i>{c}</span>' for c in d["compat"])
    return {
        "url": f"/solutions/{d['slug']}/",
        "title": f"{d['title']} | Solutions JARVIS",
        "description": d["description"],
        "og_image": d["image"],
        "content": f"""
<section class="hero page-hero">
  <div class="hero-media"><img src="{d['image']}" alt="" fetchpriority="high"></div>
  <div class="shell hero-inner">
    <div>
      <p class="eyebrow">Interface conceptuelle · fondation en construction</p>
      <h1>{d['h1']}</h1>
      <p class="lead">{d['lead']}</p>
      <div class="hero-actions">
        <a class="button button-gold" href="/contact/">Présenter un besoin <span>↗</span></a>
        <a class="button" href="/solutions/">Comparer les solutions</a>
      </div>
      <div class="hero-meta">
        <div><span>Pour</span><b>{d['for']}</b></div>
        <div><span>Déploiement</span><b>Local, privé ou hybride</b></div>
        <div><span>Principe</span><b>Contrôle humain</b></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div data-reveal>
      <p class="eyebrow">Le problème à résoudre</p>
      <h2>{d['problem_title']}</h2>
    </div>
    <p class="lead" data-reveal>{d['problem_copy']}</p>
  </div>
</section>

<section class="section section-raised">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Ce que la solution change</p>
        <h2>{d['change_title']}</h2>
      </div>
      <p>{d['change_copy']}</p>
    </div>
    <div class="card-grid">
      {features}
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Aperçu conceptuel · données simulées</p>
        <h2>{d['demo_title']}</h2>
      </div>
      <p>{d['demo_copy']}</p>
    </div>
    {d['showcase']}
    <div class="badge-row" data-reveal style="margin-top:2.5rem;">
      <span class="badge badge-gold"><i></i>COMPATIBILITÉS POSSIBLES</span>
      {compat}
    </div>
  </div>
</section>

<section class="section section-raised">
  <div class="shell split">
    <div data-reveal>
      <p class="eyebrow">Déploiement responsable</p>
      <h2>{d['deploy_title']}</h2>
      <p>{d['deploy_copy']}</p>
    </div>
    <div class="card-grid" style="grid-template-columns:1fr;" data-reveal>
      <article class="card">
        <h3>Accord humain</h3>
        <p>Les actions sensibles exigent une validation adaptée au risque.</p>
      </article>
      <article class="card">
        <h3>Limite publiée</h3>
        <p>{d['limit']}</p>
      </article>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="shell cta-inner" data-reveal>
    <div>
      <p class="eyebrow">Premier échange</p>
      <h2>{d['cta_title']}</h2>
    </div>
    <div>
      <p>{d['cta_copy']}</p>
      <a class="button button-fill" href="/contact/">Discuter du projet <span>↗</span></a>
    </div>
  </div>
</section>
""",
    }
