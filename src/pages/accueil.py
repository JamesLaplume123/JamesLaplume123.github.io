# Accueil — version « wow » (chantier 2026) : vendre JARVIS, le logiciel.
# Parcours : promesse cinématique → manifeste → le logiciel en scène → le Hub →
# six capacités (bento) → offre par environnement → preuve (laboratoire) → démo.
# Les textes seront enrichis avec les PDF de James; la structure, elle, est finale.

PAGE = {
    "url": "/",
    "v2": True,
    "title": "JARVIS Private Systems | Intelligence privée et systèmes connectés",
    "description": (
        "JARVIS relie vos outils, vos informations et vos espaces dans une "
        "expérience privée, contextuelle et contrôlée. Réservez une démonstration."
    ),
    "content": """
<!-- Scène 1 · Héros -->
<section class="hero">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp"
       alt="Résidence contemporaine la nuit, systèmes JARVIS actifs" fetchpriority="high"></div>
  <div class="hero-inner">
    <p class="eyebrow">Intelligence privée</p>
    <h1>Relier ce qui existe.<span class="l2">Faire agir l’ensemble.</span></h1>
    <p class="sub">Une intelligence privée qui comprend vos règles, coordonne les systèmes
    autorisés et vous laisse les décisions importantes.</p>
    <div class="acts">
      <a class="pill" href="#app">Voir JARVIS en action</a>
      <a class="pill ghost" href="/contact/">Réserver une démo</a>
    </div>
  </div>
  <i class="cue" aria-hidden="true"></i>
</section>

<!-- Scène 2 · Manifeste -->
<section class="mani" aria-label="Manifeste">
  <div class="stick"><p>Vos appareils existent déjà. Vos informations existent déjà.
  Il manquait l’intelligence privée qui les comprend — et qui les fait travailler ensemble.</p></div>
</section>

<!-- Scène 3 · Le logiciel -->
<section class="scene app" id="app">
  <div class="stick">
    <img src="/media/product/jarvis-command-center-preview.png"
         alt="JARVIS App — vue d’ensemble de tous vos environnements" loading="lazy">
    <h2 class="t1">Voici JARVIS App.</h2>
    <p class="t2">Tous vos environnements. Une seule intelligence. Votre accord pour chaque action.</p>
    <div class="t3">
      <span class="chip">Assistant intégré</span>
      <span class="chip">Résidence · Entreprise · Véhicule</span>
      <span class="chip chip-sim">Prototype interactif · données simulées</span>
    </div>
  </div>
</section>

<!-- Scène 4 · Le Hub -->
<section class="scene">
  <div class="stick">
    <img src="/media/product/jarvis-hub-v1.webp"
         alt="JARVIS Hub posé sur un meuble d’une résidence contemporaine" loading="lazy">
    <h2 class="t1">JARVIS Hub</h2>
    <p class="t2">L’intelligence demeure chez vous — pas dans un nuage.</p>
    <div class="t3">
      <span class="chip">100 % local</span>
      <span class="chip">Données privées</span>
      <span class="chip">Décisions humaines</span>
    </div>
  </div>
</section>

<!-- Scène 5 · Six capacités (bento) -->
<section class="bento" id="capacites">
  <div class="head" data-rev>
    <h2>Une plateforme.<br>Six capacités.</h2>
    <p>La même identité, les mêmes permissions, la même trace —
    du salon à l’entreprise, jusqu’au véhicule.</p>
  </div>
  <div class="grid">
    <a class="tile w3" href="/solutions/environnements-intelligents/" data-rev>
      <img src="/media/solutions/environnements-intelligents.webp" alt="" loading="lazy">
      <span class="lab"><small>01 · Environnements</small><b>Le lieu répond à la situation.</b></span></a>
    <a class="tile w3" href="/solutions/ia-privee-connaissances/" data-rev>
      <img src="/media/solutions/ia-privee-connaissances.webp" alt="" loading="lazy">
      <span class="lab"><small>02 · IA privée</small><b>Parlez à vos informations.</b></span></a>
    <a class="tile" href="/solutions/securite-intelligente/" data-rev>
      <img src="/media/solutions/securite-intelligente.webp" alt="" loading="lazy">
      <span class="lab"><small>03 · Sécurité</small><b>Une situation claire.</b></span></a>
    <a class="tile" href="/solutions/automatisation-operations/" data-rev>
      <img src="/media/solutions/jarvis-enterprise-operations-v1.webp" alt="" loading="lazy">
      <span class="lab"><small>04 · Automatisation</small><b>Vos outils, reliés.</b></span></a>
    <a class="tile" href="/solutions/reseau-resilience/" data-rev>
      <img src="/media/solutions/reseau-resilience.webp" alt="" loading="lazy">
      <span class="lab"><small>05 · Réseau</small><b>Une vue vivante.</b></span></a>
    <a class="tile w6" href="/solutions/diagnostic-care/" data-rev>
      <img src="/media/solutions/diagnostic-care.webp" alt="" loading="lazy">
      <span class="lab"><small>06 · Diagnostic &amp; continuité</small>
      <b>D’un symptôme à une remise en service documentée.</b></span></a>
  </div>
</section>

<!-- Scène 6 · Offre -->
<section class="offer" id="offre">
  <div class="head" data-rev>
    <h2>Choisissez votre environnement.</h2>
    <p>Un seul JARVIS, configuré pour votre réalité. Chaque déploiement commence
    par une première preuve utile, définie avec vous.</p>
  </div>
  <div class="plans">
    <article class="plan" data-rev>
      <small>Résidence</small>
      <h3>Maison · condo · chalet</h3>
      <ul>
        <li>Confort, énergie et sécurité coordonnés</li>
        <li>JARVIS Hub installé chez vous</li>
        <li>Données 100 % locales</li>
      </ul>
      <a class="pill" href="/contact/">Réserver une démo</a>
    </article>
    <article class="plan star" data-rev>
      <small>Entreprise</small>
      <h3>Bureau · commerce · atelier</h3>
      <ul>
        <li>Automatisation entre vos outils existants</li>
        <li>Sécurité et réseau compréhensibles</li>
        <li>Journal d’audit complet</li>
      </ul>
      <a class="pill" href="/contact/">Réserver une démo</a>
    </article>
    <article class="plan" data-rev>
      <small>Mobilité</small>
      <h3>Véhicule aménagé · VR · unité spécialisée</h3>
      <ul>
        <li>Énergie et réseau en déplacement</li>
        <li>Éprouvé dans le laboratoire mobile</li>
        <li>Diagnostic embarqué</li>
      </ul>
      <a class="pill" href="/contact/">Réserver une démo</a>
    </article>
  </div>
  <p class="offer-note" data-rev>JARVIS est en développement actif —
  les premières démonstrations se réservent maintenant.</p>
</section>

<!-- Scène 7 · Laboratoire (preuve) -->
<section class="band">
  <div class="bg"><img src="/media/ambulance/ambulance-garage-lab-v1.webp"
       alt="Laboratoire mobile JARVIS — ambulance Ford 2017 dans le garage" loading="lazy"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Premier terrain de preuve</p>
    <h2 data-rev>Le système sort<br>de l’écran.</h2>
    <div class="specs" data-rev>
      <div><b><span data-n="560">560</span><i>Ah</i></b><small>Énergie</small></div>
      <div><b><span data-n="500">500</span><i>W</i></b><small>Solaire</small></div>
      <div><b>V10</b><small>Ford 2017</small></div>
      <div><b><span data-n="100">100</span><i>%</i></b><small>Réel</small></div>
    </div>
    <p data-rev style="margin:0 0 3rem"><a class="pill ghost" href="/laboratoire-mobile/">Découvrir le laboratoire mobile</a></p>
  </div>
</section>

<!-- Scène 8 · Appel -->
<section class="cta" id="demo">
  <h2 data-rev>Voyez JARVIS<br><span>de vos yeux.</span></h2>
  <p data-rev>Une rencontre, vos besoins réels, une démonstration en direct —
  et la première preuve utile définie ensemble.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
