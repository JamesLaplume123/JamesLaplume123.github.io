# Solutions — les sept solutions, une ligne chacune (refonte « essentiel », novembre 2026).
# Chaque carte mène à la page de la solution, où se trouve sa démonstration.

from config import CAPABILITIES
import lieux

CARTES = "".join(
    f'<a class="card" href="/solutions/{c["slug"]}/" data-sol="{c["slug"]}" data-rev><small>{c["num"]}</small>'
    f'<h3>{c["title"]}</h3><p>{c["menu"]}</p>'
    + ('<span class="card-ent">Pour l’entreprise</span>' if lieux.SOLUTIONS_PUBLIC.get(c["slug"]) == "entreprise" else "")
    + "</a>"
    for c in CAPABILITIES
)

PAGE = {
    "url": "/solutions/",
    "v2": True,
    "title": "Solutions | JARVIS Private Systems",
    "schema": [{
        "@context": "https://schema.org", "@type": "ItemList", "name": "Les sept solutions JARVIS",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c["title"],
             "url": f"https://jarvisprivatesystems.com/solutions/{c['slug']}/"}
            for i, c in enumerate(CAPABILITIES)
        ],
    }],
    "description": (
        "Sept familles de solutions pour les environnements intelligents, l’IA privée, "
        "la sécurité, les opérations, le réseau, le diagnostic et la mobilité."
    ),
    "og_image": "/media/solutions/environnements-intelligents.webp",
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/environnements-intelligents.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <h1 data-rev>Sept solutions.<br><em>Un seul système.</em></h1>
    <p class="lead" data-rev>Commencez par un besoin; le reste s’ajoute sans tout reconstruire.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
    </div>
  </div>
</section>

<section class="sect" id="sept" aria-label="Les sept solutions">
  <div class="cards" data-sols>{CARTES}</div>
</section>

<section class="sect alt" id="par-besoin" aria-labelledby="pb-titre">
  <div class="sect-head">
    <div data-rev>
      <h2 id="pb-titre">Par type de lieu.</h2>
    </div>
  </div>
  <div class="cards">
    <a class="card" href="/solutions/maison-intelligente-cle-en-main/" data-rev><small>Maison</small><h3>Maison intelligente clé en main</h3><p>De la visite à la formation, un seul système.</p></a>
    <a class="card" href="/solutions/domotique-ferme-agricole/" data-rev><small>Ferme</small><h3>Domotique pour ferme</h3><p>Tous les bâtiments sur un seul écran.</p><span class="card-ent">Pour l’entreprise</span></a>
    <a class="card" href="/solutions/entreprise/" data-rev><small>Entreprise</small><h3>Toute votre entreprise</h3><p>Les appels, le travail, les lieux et la protection, dans un seul système.</p><span class="card-ent">Pour l’entreprise</span></a>
  </div>
  <p class="pro-suite" data-rev><a href="/offre/">Voir l’offre <i aria-hidden="true">→</i></a></p>
</section>

<section class="cta">
  <h2 data-rev>Par quoi commencer?</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
