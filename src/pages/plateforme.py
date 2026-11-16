# Le Hub et l'IA privée (/plateforme/) — ce qu'il y a sous le capot (refonte « essentiel »,
# novembre 2026) : le Hub, son IA, le noyau en Rust. /logiciel/ montre l'application; /offre/ dit
# comment ça se compose.

from demos import hub, rust

PAGE = {
    "url": "/plateforme/",
    "v2": True,
    "title": "Le Hub et l’IA privée | Sous le capot de JARVIS",
    "description": (
        "Le Hub installé chez vous, son IA locale en français et sept extensions qui "
        "travaillent ensemble : un système privé, local et contrôlé."
    ),
    "og_image": "/media/product/user/accueil-og.jpg",
    "assets": ["rust", "hub"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Sous le capot · le Hub et l’IA privée</p>
    <h1 data-rev>Votre système privé.<br><em>Un seul point d’entrée.</em></h1>
    <p class="lead" data-rev>Un boîtier chez vous, une IA privée, un noyau sûr.</p>
  </div>
</section>

<section class="sect hb-sect" id="hub" aria-label="Le Hub, cœur de JARVIS">
  """ + hub.coeur() + """
</section>

<section class="sect alt hb-sect" id="ia" aria-labelledby="ia-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">L’IA au cœur</p>
      <h2 id="ia-titre">Une IA qui comprend.<br><em>Et qui vous laisse décider.</em></h2>
    </div>
  </div>
  """ + hub.ia() + """
</section>

<section class="sect rust-sect" id="rust" aria-labelledby="rust-titre">
  <div class="head shead" data-rev>
    <p class="eyebrow">Le logiciel · écrit en Rust</p>
    <h2 id="rust-titre">Sûr par construction. <em>Pas par promesse.</em></h2>
  </div>
  """ + rust.html() + """
</section>

<section class="cta">
  <h2 data-rev>Un lieu qui mérite<br><span>son propre JARVIS?</span></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
  <p class="pro-suite" data-rev><a href="/logiciel/">Essayer le logiciel</a><a href="/offre/">L’offre</a></p>
</section>
""",
}
