# Solutions — les trois divisions de JARVIS, du général au détail (refonte « trois divisions », novembre 2026).
# Trois grandes tuiles (Privé, Entreprise, Cyber), puis la gamme de chaque division, une carte par
# solution avec sa promesse. Chaque carte mène à la page de la solution, où se trouve sa démonstration.
# Les sept solutions gardent leur adresse; les pages « par type de lieu » restent en bas.
# Données : src/divisions.py · Styles : assets/demos/divisions.css.

from config import CAPABILITIES
import divisions

PAGE = {
    "url": "/solutions/",
    "v2": True,
    "title": "Solutions | JARVIS Private Systems",
    "assets": ["divisions"],
    "schema": [{
        "@context": "https://schema.org", "@type": "ItemList", "name": "Les solutions JARVIS",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c["title"],
             "url": f"https://jarvisprivatesystems.com/solutions/{c['slug']}/"}
            for i, c in enumerate(CAPABILITIES)
        ] + [{"@type": "ListItem", "position": len(CAPABILITIES) + 1, "name": "JARVIS Cyber",
              "url": "https://jarvisprivatesystems.com/solutions/cyber/"}],
    }],
    "description": (
        "Trois divisions, une seule IA : JARVIS Privé pour vos lieux et vos véhicules, JARVIS "
        "Entreprise pour vos opérations, JARVIS Cyber pour vérifier vos systèmes."
    ),
    "og_image": "/media/solutions/environnements-intelligents.webp",
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/environnements-intelligents.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <h1 data-rev>Trois divisions.<br><em>Une seule IA.</em></h1>
    <p class="lead" data-rev>Choisissez ce que vous voulez protéger. Chaque solution s’ajoute sans tout reconstruire.</p>
    <div class="acts" data-rev>
      <a class="pill" href="#prive">Commencer par JARVIS Privé</a>
      <a class="pill ghost" href="/pourquoi-jarvis/">Pourquoi JARVIS</a>
    </div>
  </div>
</section>

<section class="sect" id="divisions" aria-label="Les trois divisions">
  <div class="dv3">{divisions.tuiles()}</div>
</section>

<section class="sect" id="prive" aria-labelledby="prive-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">01 · JARVIS Privé</p>
      <h2 id="prive-titre">Votre maison. Votre chalet. <em>Vos véhicules.</em></h2>
    </div>
    <div class="side" data-rev><p>Protégés et gérés tout seuls, par une IA qui travaille chez vous.</p></div>
  </div>
  <div class="gam">{divisions.gamme(divisions.PRIVE)}</div>
</section>

<section class="sect alt" id="entreprise" aria-labelledby="entreprise-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">02 · JARVIS Entreprise</p>
      <h2 id="entreprise-titre">Votre entreprise <em>roule toute seule.</em></h2>
    </div>
    <div class="side" data-rev><p>Pour les travailleurs autonomes, les PME, les fermes et les commerces : votre travail, puis vos bâtiments.</p></div>
  </div>
  <p class="dv-sous" data-rev>Votre travail</p>
  <div class="gam gam-5">{divisions.gamme(divisions.ENTREPRISE_TRAVAIL)}</div>
  <p class="dv-sous" data-rev>Vos bâtiments</p>
  <div class="gam gam-5">{divisions.gamme(divisions.ENTREPRISE_BATIMENTS)}</div>
  <div class="dv-suite" data-rev><a class="pill" href="/solutions/entreprise/">Découvrir JARVIS Entreprise</a></div>
</section>

<section class="sect" id="cyber" aria-labelledby="cyber-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">03 · JARVIS Cyber</p>
      <h2 id="cyber-titre">Vos failles trouvées <em>avant un pirate.</em></h2>
    </div>
    <div class="side" data-rev><p>Nous vérifions vos propres systèmes, sur mandat écrit, puis nous corrigeons avec vous. Client de JARVIS ou non.</p></div>
  </div>
  <div class="gam gam-3">{divisions.gamme(divisions.CYBER)}</div>
  <div class="dv-suite" data-rev><a class="pill" href="/solutions/cyber/">Découvrir JARVIS Cyber</a></div>
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
