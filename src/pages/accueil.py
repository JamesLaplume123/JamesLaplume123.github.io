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
      <a class="pill" href="#app">Découvrir JARVIS</a>
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
    <img src="/media/product/user/accueil.jpg"
         alt="JARVIS App — accueil personnel : Bonsoir Alex, votre journée, simplement" loading="lazy">
    <h2 class="t1">Voici JARVIS App.</h2>
    <p class="t2">Votre espace. À votre image. Votre accord pour chaque action.</p>
    <div class="t3">
      <span class="chip">Assistant intégré</span>
      <span class="chip">Agenda · messages · documents · carte</span>
      <span class="chip chip-sim">Conception en validation · données simulées</span>
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
      <span class="chip">Local d’abord</span>
      <span class="chip">Données privées</span>
      <span class="chip">Décisions humaines</span>
    </div>
  </div>
</section>

<!-- Trois modes -->
<section class="modes" id="modes">
  <div class="head" data-rev>
    <p class="eyebrow">Base · Signature · Platinum</p>
    <h2 style="margin-top:1.1rem">Votre espace.<br><em>À votre image.</em></h2>
    <p>Trois modes pour la même intelligence. Choisissez-en un : tout le site le suit,
    comme l’interface de JARVIS.</p>
  </div>
  <div class="mode-tabs" role="group" aria-label="Choisir un mode d’affichage" data-rev>
    <button type="button" data-mode-set="base" aria-pressed="false">
      <img src="/media/modes/base.webp" alt="" loading="lazy">
      <span class="txt"><b>Base</b><small>Verre fumé. Sobre, neutre, l’essentiel.</small></span>
    </button>
    <button type="button" class="is-on" data-mode-set="signature" aria-pressed="true">
      <img src="/media/modes/signature.webp" alt="" loading="lazy">
      <span class="txt"><b>Signature</b><small>Verre or. Noir profond et lumière chaude.</small></span>
    </button>
    <button type="button" data-mode-set="platinum" aria-pressed="false">
      <img src="/media/modes/platinum.webp" alt="" loading="lazy">
      <span class="txt"><b>Platinum</b><small>Cristal. Noir fumé et reflets froids.</small></span>
    </button>
  </div>
  <div class="mode-demo">
    <article class="card" data-rev>
      <small>Ma journée</small>
      <h3>Souper entre amis</h3>
      <p>19:00 – 22:00 · Chez nous</p>
    </article>
    <article class="card" data-rev>
      <small>Assistant JARVIS</small>
      <h3>Comment puis-je vous aider?</h3>
      <p>Il propose. Vous décidez.</p>
    </article>
    <article class="card" data-rev>
      <small>Recommandations</small>
      <h3>Préparer votre journée</h3>
      <p>Chaque suggestion montre sa source.</p>
    </article>
  </div>
  <p class="offer-note" data-rev>Apparences de l’interface JARVIS · exemples fictifs</p>
</section>

<!-- Scène 5 · Six capacités (bento) -->
<section class="bento" id="capacites">
  <div class="head" data-rev>
    <p class="kick">Six solutions · Un point de départ</p>
    <h2>Votre besoin.<br>La bonne solution.</h2>
    <p>Choisissez ce que vous aimeriez simplifier.<br>Un clic sur une carte ouvre directement sa solution.</p>
  </div>
  <nav class="grid" aria-label="Accéder aux six solutions">
    <a class="tile w3" href="/solutions/environnements-intelligents/" data-rev>
      <img src="/media/solutions/environnements-intelligents.webp" alt="" loading="lazy">
      <span class="lab"><small>01</small><b>Environnements intelligents</b><em>Lumières, confort et énergie réunis.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile w3" href="/solutions/ia-privee-connaissances/" data-rev>
      <img src="/media/solutions/ia-privee-connaissances.webp" alt="" loading="lazy">
      <span class="lab"><small>02</small><b>IA privée et connaissances</b><em>Retrouver vos documents et les bonnes réponses.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile" href="/solutions/securite-intelligente/" data-rev>
      <img src="/media/solutions/securite-intelligente.webp" alt="" loading="lazy">
      <span class="lab"><small>03</small><b>Sécurité intelligente</b><em>Comprendre les événements de vos lieux.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile" href="/solutions/automatisation-operations/" data-rev>
      <img src="/media/solutions/jarvis-enterprise-operations-v1.webp" alt="" loading="lazy">
      <span class="lab"><small>04</small><b>Automatisation d’entreprise</b><em>Faire avancer les demandes de votre équipe.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile" href="/solutions/reseau-resilience/" data-rev>
      <img src="/media/solutions/reseau-resilience.webp" alt="" loading="lazy">
      <span class="lab"><small>05</small><b>Réseau et cybersécurité</b><em>Garder vos connexions fiables et privées.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile w6" href="/solutions/diagnostic-care/" data-rev>
      <img src="/media/solutions/diagnostic-care.webp" alt="" loading="lazy">
      <span class="lab"><small>06</small><b>Diagnostic &amp; continuité</b><em>Comprendre un souci et préparer la suite.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
  </nav>
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
        <li>JARVIS Hub intégré au lieu</li>
        <li>Local d’abord, Internet seulement si permis</li>
      </ul>
      <a class="pill" href="/contact/">Réserver une démo</a>
    </article>
    <article class="plan star" data-rev>
      <small>Entreprise</small>
      <h3>Bureau · commerce · atelier</h3>
      <ul>
        <li>Automatisation entre vos outils existants</li>
        <li>Sécurité et réseau compréhensibles</li>
        <li>Une trace des décisions et des actions</li>
      </ul>
      <a class="pill" href="/contact/">Réserver une démo</a>
    </article>
    <article class="plan" data-rev>
      <small>Mobilité</small>
      <h3>Véhicule aménagé · VR · unité spécialisée</h3>
      <ul>
        <li>Énergie et réseau en déplacement</li>
        <li>Développé sur le laboratoire mobile</li>
        <li>Diagnostic pensé pour la route</li>
      </ul>
      <a class="pill" href="/contact/">Réserver une démo</a>
    </article>
  </div>
  <p class="offer-note" data-rev>JARVIS est en construction : ces environnements décrivent la
  direction du produit, pas une disponibilité immédiate.</p>
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
      <div><b>En cours</b><small>Construction réelle</small></div>
    </div>
    <p data-rev style="margin:0 0 3rem"><a class="pill ghost" href="/laboratoire-mobile/">Découvrir le laboratoire mobile</a></p>
  </div>
</section>

<!-- Scène 8 · Appel -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "JARVIS Private Systems",
  "url": "https://jameslaplume.ca",
  "logo": "https://jameslaplume.ca/favicon.svg",
  "email": "laplumejames@gmail.com",
  "founder": {"@type": "Person", "name": "James Laplume"},
  "address": {"@type": "PostalAddress", "addressRegion": "QC", "addressCountry": "CA"}
}
</script>

<section class="cta" id="demo">
  <h2 data-rev>Voyez JARVIS<br><span>de vos yeux.</span></h2>
  <p data-rev>Une rencontre, vos besoins réels, ce qui existe aujourd’hui —
  et la première preuve utile définie ensemble.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
