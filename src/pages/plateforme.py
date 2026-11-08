# JARVIS (plateforme) — le produit en scène : le Hub et son IA, les extensions qui travaillent ensemble,
# l’App, le noyau en Rust et l’offre (Hub + extensions + services).

from demos import app, hub, rust

PAGE = {
    "url": "/plateforme/",
    "v2": True,
    "title": "JARVIS | Le Hub, son IA et ses extensions",
    "description": (
        "Le Hub installé chez vous, son IA locale en français et sept extensions qui "
        "travaillent ensemble : un système privé, local et contrôlé."
    ),
    "og_image": "/media/product/user/accueil-og.jpg",
    "assets": ["app", "rust", "hub"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>JARVIS · App, Core et Hub</p>
    <h1 data-rev>Votre système privé.<br><em>Un seul point d’entrée.</em></h1>
    <p class="lead" data-rev>Parlez à JARVIS App. JARVIS Core comprend le contexte et applique
    vos règles. JARVIS Hub garde l’intelligence près de vos systèmes.</p>
    <div class="acts" data-rev>
      <a class="pill" href="#hub">Découvrir le Hub</a>
      <a class="pill ghost" href="#app">Voir l’interface</a>
      <a class="pill ghost" href="#offre">L’offre</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip">Interface · JARVIS App</span>
      <span class="chip">Intelligence · JARVIS Core</span>
      <span class="chip">Sur place · JARVIS Hub</span>
    </div>
  </div>
</section>

<section class="sect hb-sect" id="hub" data-toc="Le Hub" aria-label="Le Hub, cœur de JARVIS">
  """ + hub.coeur() + """
</section>

<section class="sect alt hb-sect" id="ia" data-toc="L’IA" aria-labelledby="ia-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">L’IA au cœur</p>
      <h2 id="ia-titre">Une IA qui comprend.<br><em>Et qui vous laisse décider.</em></h2>
    </div>
    <p data-rev>Une seule IA, sur le Hub. Vous lui parlez normalement; elle propose un plan, explique
    pourquoi et attend votre accord.</p>
  </div>
  """ + hub.ia() + """
</section>

<section class="sect hb-sect" id="ensemble" data-toc="Les extensions ensemble" aria-labelledby="ensemble-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Comment les extensions travaillent ensemble</p>
      <h2 id="ensemble-titre">Chacune son rôle.<br><em>Toutes reliées par le Hub.</em></h2>
    </div>
    <p data-rev>Chaque extension garde son domaine et partage ce qu’elle observe. Le Hub fait respecter
    les droits et garde la trace.</p>
  </div>
  """ + hub.ensemble() + """
</section>

<section class="vitrine" id="app" data-toc="L’app" aria-label="JARVIS App">
  <div class="head" data-rev>
    <p class="eyebrow">JARVIS App · essayez-la</p>
    <h2>Votre espace. <em>À votre image.</em></h2>
  </div>
  """ + app.html() + """
</section>

<section class="sect" id="experience-user">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ce que l’app prévoit · 58 vues conçues</p>
      <h2>Tout votre quotidien. <em>Aucune surprise.</em></h2>
    </div>
    <p data-rev>Le parcours complet du compte personnel est dessiné, écran par écran. C’est la direction
    de conception : chaque fonction sera confirmée seulement une fois construite et prouvée.</p>
  </div>
  <ul class="feats">
    <li data-rev><small>Accès</small><h3>Sur invitation seulement.</h3><p>Aucune inscription publique : chaque compte est créé par l’administrateur du Hub. Clés d’accès prévues — votre biométrie reste sur votre appareil.</p></li>
    <li data-rev><small>Ma journée</small><h3>Agenda et tâches, enfin ensemble.</h3><p>Tous vos calendriers et vos listes, de toutes vos sources, dans une seule vue. Un calendrier en lecture seule le reste.</p></li>
    <li data-rev><small>Messages</small><h3>Vos conversations, chez vous.</h3><p>Texte, photos, documents, vocaux et appels sur le Hub. Micro et caméra ne s’activent jamais sans votre permission.</p></li>
    <li data-rev><small>Assistant</small><h3>Il propose. Vous décidez.</h3><p>En texte ou en voix, il prépare l’action puis attend votre confirmation. Jamais de succès affiché sans résultat réel.</p></li>
    <li data-rev><small>Recommandations</small><h3>Chaque suggestion montre d’où elle vient.</h3><p>Provenance et raison visibles. Une suggestion n’agit jamais à votre place.</p></li>
    <li data-rev><small>Partage</small><h3>Je choisis ce que je partage.</h3><p>Avec qui, pour combien de temps, révocable en tout temps. Un accès retiré disparaît partout.</p></li>
    <li data-rev><small>Carte</small><h3>Voir votre monde, pas celui des autres.</h3><p>Le Hub, vos appareils, et seulement les personnes qui ont choisi de partager. Jamais de fausse position.</p></li>
    <li data-rev><small>Personnalisation</small><h3>Votre accueil vous ressemble.</h3><p>Affichez, ordonnez et dimensionnez vos cartes. Vos préférences suivent votre compte, sans changer vos droits.</p></li>
  </ul>
</section>

<section class="sect" id="parcours">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le produit complet</p>
      <h2>Une seule expérience.<br><em>Du geste au système réel.</em></h2>
    </div>
    <p data-rev>L’App est ce que vous utilisez. Core comprend la demande. Le Hub garde
    l’intelligence près du site. Les équipements et logiciels existants exécutent le résultat.</p>
  </div>
  <div class="rows">
    <div class="row" data-rev>
      <i>Étape 01</i>
      <div><h3>Vous voyez et décidez — JARVIS App</h3>
      <p>Une interface cohérente sur ordinateur, tablette, téléphone et écrans intégrés :
      comprendre, demander, approuver et consulter les preuves.</p></div>
    </div>
    <div class="row" data-rev>
      <i>Étape 02</i>
      <div><h3>Le système comprend — JARVIS Core</h3>
      <p>Il rapproche les sources autorisées, applique les règles et prépare une action
      explicable : demande → contexte → permissions → plan prêt.</p></div>
    </div>
    <div class="row" data-rev>
      <i>Étape 03</i>
      <div><h3>Le site reste autonome — JARVIS Hub</h3>
      <p>L’infrastructure locale exécute Core et maintient les fonctions essentielles près du
      lieu. Local, privé, autonome.</p></div>
    </div>
    <div class="row" data-rev>
      <i>Étape 04</i>
      <div><h3>Le réel répond — vos systèmes</h3>
      <p>JARVIS relie les espaces, informations, logiciels et équipements qui font déjà le
      vrai travail : maison, entreprise ou véhicule.</p></div>
    </div>
  </div>
  <div class="chiprow" data-rev>
    <span class="chip chip-sim">Une identité</span>
    <span class="chip">Des permissions</span>
    <span class="chip">Sept extensions</span>
    <span class="chip">Une trace complète</span>
  </div>
</section>

<section class="sect rust-sect" id="rust" data-toc="Rust" aria-labelledby="rust-titre">
  <div class="head shead" data-rev>
    <p class="eyebrow">Le logiciel · écrit en Rust</p>
    <h2 id="rust-titre">Sûr par construction. <em>Pas par promesse.</em></h2>
    <p>Le noyau qui garde vos comptes, vos droits et vos secrets est écrit en Rust, le langage que
    recommandent les agences de cybersécurité pour le logiciel critique.</p>
  </div>
  """ + rust.html() + """
</section>

<section class="sect alt" id="experience" data-toc="Comptes et droits">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">JARVIS App · expérience de base</p>
      <h2>Votre identité. Vos règles.<br><em>Votre point d’entrée.</em></h2>
    </div>
    <p data-rev>Avant toute solution, JARVIS connaît seulement les personnes, les rôles et les
    limites que vous avez définis. Rien d’autre n’est relié par défaut.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>Identités configurées</small>
      <h3>Une seule interface, des responsabilités différentes.</h3>
      <p>Chaque personne possède son propre accès.</p>
      <ul>
        <li>Profil principal — administration et décisions sensibles</li>
        <li>Utilisateur autorisé — usage quotidien, actions permises seulement</li>
        <li>Invité temporaire — accès limité dans le temps et révocable</li>
      </ul>
    </article>
    <article class="card" data-rev>
      <small>Contrôle des actions</small>
      <h3>Voir, proposer, approuver et exécuter ne sont pas le même pouvoir.</h3>
      <p>Chaque capacité déclare ses sources, ses actions possibles et la personne qui doit
      approuver.</p>
    </article>
    <article class="card" data-rev>
      <small>Capacités</small>
      <h3>JARVIS se construit autour du besoin, une capacité à la fois.</h3>
      <p>Activer une capacité ne donne pas accès aux autres. Chaque connexion reste visible
      et révocable.</p>
    </article>
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Pour l’administrateur</p>
      <h2>Services et hébergement :<br><em>une seule entrée.</em></h2>
    </div>
    <p data-rev>L’administrateur voit où chaque logiciel fonctionne — sur le Hub, sur une
    machine qu’il contrôle ou chez un fournisseur — et ce que chaque connexion autorise.
    Les utilisateurs, eux, n’ont jamais de serveur à gérer.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>Où tout fonctionne</small>
      <h3>Hub, vos machines, fournisseurs — affichés séparément.</h3>
      <p>Le logiciel, sa connexion à JARVIS et vos droits sont trois choses distinctes.
      L’emplacement d’un serveur ne donne pas le droit de le gérer.</p>
    </article>
    <article class="card" data-rev>
      <small>Ajouter sans tout autoriser</small>
      <h3>Identifier, tester, puis accorder le nécessaire.</h3>
      <p>On identifie le serveur, on teste la connexion, puis on accorde seulement les
      capacités utiles — jamais un accès général.</p>
    </article>
    <article class="card" data-rev>
      <small>Réparer sans perdre</small>
      <h3>Déconnecter ne veut pas dire supprimer.</h3>
      <p>Une connexion interrompue ne veut pas dire logiciel arrêté. Les données et les
      sauvegardes restent séparées et protégées.</p>
    </article>
  </div>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Déjà dessinées, en validation</p>
      <h2>Les extensions <em>qui s’en viennent.</em></h2>
    </div>
    <p data-rev>Chaque extension a son dossier de conception complet — écrans, droits,
    règles et limites — avant la première ligne de code. Rien n’est annoncé sans dossier.</p>
  </div>
  <div class="rows">
    <div class="row" data-rev>
      <i>Communications</i>
      <div><h3>Une voix. Une équipe. Un système qui vous ressemble.</h3>
      <p>Appels internes et publics, accueil intelligent, distribution des appels et
      alertes — la téléphonie IP pensée pour la maison comme pour l’entreprise, avec des
      droits précis pour appeler, écouter et administrer.</p></div>
    </div>
    <div class="row" data-rev>
      <i>IA et connaissances</i>
      <div><h3>Vos documents restent à leur place. L’IA vous aide à les comprendre.</h3>
      <p>Guide complet des deux parcours — utilisateur et administration.
      <a href="/solutions/ia-privee-connaissances/" style="color:#fff">Voir la solution.</a></p></div>
    </div>
    <div class="row" data-rev>
      <i>Environnements</i>
      <div><h3>Éclairage, confort, énergie — module par module.</h3>
      <p>Les ambiances, les configurations protégées et la règle « jamais de faux
      succès ». <a href="/solutions/environnements-intelligents/" style="color:#fff">Voir la solution.</a></p></div>
    </div>
    <div class="row" data-rev>
      <i>Mobilité et voyage</i>
      <div><h3>Le trajet, les arrêts et le véhicule, dans le même contexte.</h3>
      <p>Développée sur le laboratoire mobile.
      <a href="/laboratoire-mobile/" style="color:#fff">Voir le laboratoire.</a></p></div>
    </div>
  </div>
  <div class="chiprow" data-rev>
    <span class="chip chip-sim">Dossiers de conception complets · en validation</span>
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le contrôle reste visible</p>
      <h2>Puissant ne veut pas dire <em>opaque.</em></h2>
    </div>
    <p data-rev>JARVIS montre qui accède à quoi, ce qui peut être exécuté et quand une décision
    humaine est obligatoire.</p>
  </div>
  <div class="cards two">
    <article class="card" data-rev>
      <small>Local d’abord</small>
      <h3>Les fonctions essentielles restent près du site.</h3>
      <p>Le cloud est utilisé seulement lorsqu’il apporte une valeur comprise et autorisée.</p>
    </article>
    <article class="card" data-rev>
      <small>Sources choisies</small>
      <h3>Chaque connexion est identifiable et révocable.</h3>
      <p>Une capacité ne reçoit jamais un accès général à tout votre environnement.</p>
    </article>
    <article class="card" data-rev>
      <small>Rôles précis</small>
      <h3>Chaque personne agit selon ses responsabilités.</h3>
      <p>Consulter, proposer, approuver et exécuter peuvent demander des droits différents.</p>
    </article>
    <article class="card" data-rev>
      <small>Trace complète</small>
      <h3>Les décisions importantes restent explicables.</h3>
      <p>Demandes, sources, approbations et résultats peuvent être conservés selon le mandat.</p>
    </article>
  </div>
</section>

<section class="sect alt hb-sect" id="offre" data-toc="L’offre" aria-labelledby="offre-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">L’offre</p>
      <h2 id="offre-titre">Le Hub, puis vos extensions.<br><em>Rien de plus que le nécessaire.</em></h2>
    </div>
    <p data-rev>Chaque client part du Hub. On ajoute les extensions utiles, maintenant ou plus tard, avec
    l’installation, l’entretien et le soutien.</p>
  </div>
  """ + hub.offre() + """
</section>

<section class="cta">
  <h2 data-rev>Quel environnement devrait recevoir<br><span>son propre JARVIS?</span></h2>
  <p data-rev>Présentez le lieu, les systèmes existants et le premier problème que vous
  souhaitez résoudre.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
