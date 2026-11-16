# Laboratoire mobile — où les idées sont testées dans le monde réel. Version wow.

from demos import boulance
import galerie

PAGE = {
    "url": "/laboratoire-mobile/",
    "v2": True,
    "title": "Laboratoire mobile JARVIS | Projet réel",
    "description": (
        "Une ambulance Ford 2017 V10 transformée en laboratoire réel pour l’énergie, "
        "le réseau, la sécurité, le diagnostic et l’automatisation."
    ),
    "og_image": "/media/ambulance/ambulance-garage-lab-v1.webp",
    "assets": ["boulance", "galerie"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/ambulance/ambulance-garage-lab-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Laboratoire mobile · Ford 2017 V10</p>
    <h1 data-rev>Construire le premier environnement JARVIS <em>dans le réel.</em></h1>
    <p class="lead" data-rev>Une ancienne ambulance transformée en véhicule habitable et en banc
    d’essai : le premier JARVIS sur la route.</p>
    <div class="specs" data-rev>
      <div><b><span data-n="560">560</span><i>Ah</i></b><small>Énergie LiFePO₄</small></div>
      <div><b><span data-n="500">500</span><i>W</i></b><small>Solaire</small></div>
      <div><b>V10</b><small>Ford 2017</small></div>
      <div><b>En cours</b><small>Construction réelle</small></div>
    </div>
  </div>
</section>

""" + galerie.laboratoire_visuels() + """

<section class="sect" id="direct">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow"><i class="dot" aria-hidden="true"></i> En direct · données réelles</p>
      <h2>Les batteries de l’ambulance, <em>en ce moment.</em></h2>
    </div>
    <p data-rev>Rien n’est simulé : si la liaison tombe, le panneau le dit.</p>
  </div>
""" + boulance.html() + """
</section>

<section class="cta">
  <h2 data-rev>Suivre le laboratoire?</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
  <p class="pro-suite" data-rev><a href="/solutions/environnements-intelligents/#essayer">Piloter BouLance dans JARVIS</a><a href="/solutions/mobilite/">Mobilité</a></p>
</section>
""",
}
