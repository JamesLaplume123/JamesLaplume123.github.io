# Laboratoire mobile — où les idées sont testées dans le monde réel. Version wow.

from demos import boulance, carte
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
    "assets": ["boulance", "carte", "galerie"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/ambulance/ambulance-garage-lab-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Laboratoire mobile · Ford 2017 V10</p>
    <h1 data-rev>Construire le premier environnement JARVIS <em>dans le réel.</em></h1>
    <p class="lead" data-rev>Cette ancienne ambulance québécoise est transformée en véhicule
    habitable et en banc d’essai mobile. Le projet physique est en cours; les interfaces
    montrent la direction complète visée.</p>
    <div class="acts" data-rev>
      <a class="pill" href="#direct">Voir les batteries en direct</a>
      <a class="pill ghost" href="/solutions/environnements-intelligents/#essayer">Piloter BouLance dans JARVIS</a>
    </div>
    <div class="specs" data-rev>
      <div><b><span data-n="560">560</span><i>Ah</i></b><small>Énergie LiFePO₄</small></div>
      <div><b><span data-n="500">500</span><i>W</i></b><small>Solaire</small></div>
      <div><b>V10</b><small>Ford 2017</small></div>
      <div><b>En cours</b><small>Construction réelle</small></div>
    </div>
  </div>
</section>

<section class="statement">
  <p class="eyebrow" data-rev>Le projet concret</p>
  <h2 data-rev>Le véhicule existe.<br><em>JARVIS doit relier ce qui
  le fait vivre.</em></h2>
  <p data-rev>Le Laboratoire mobile n’est pas une offre séparée. C’est le premier endroit où
  l’énergie, l’eau, le confort, le véhicule, le réseau, la sécurité et le diagnostic devront
  fonctionner ensemble dans des conditions réelles.</p>
</section>

""" + galerie.laboratoire_visuels() + """

<section class="sect" id="direct">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow"><i class="dot" aria-hidden="true"></i> En direct · données réelles</p>
      <h2>Les batteries de l’ambulance, <em>en ce moment.</em></h2>
    </div>
    <p data-rev>Ces valeurs viennent directement des deux batteries LiFePO₄ de BouLance, lues par
    Home Assistant dans le véhicule. Rien n’est simulé : si la liaison tombe, le panneau le dit.</p>
  </div>
""" + boulance.html() + """
  <div style="height:16px"></div>
""" + carte.html() + """
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le véhicule complet</p>
      <h2>Habitation, véhicule et laboratoire <em>partagent la même
      réalité.</em></h2>
    </div>
    <p data-rev>Les caractéristiques évoluent avec la construction. Le site distingue ce qui
    est prévu, installé, mesuré et réellement validé.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>Énergie</small>
      <h3>Produire, stocker et arbitrer</h3>
      <p>560 Ah LiFePO₄, extension prévue, 500 W solaire, DC-DC 60 A, génératrice et
      délestage progressif.</p>
    </article>
    <article class="card" data-rev>
      <small>Confort</small>
      <h3>Habiter en toute saison</h3>
      <p>Chauffage diesel, climatisation, foyer au propane, deux ventilateurs, éclairage et
      scènes adaptées.</p>
    </article>
    <article class="card" data-rev>
      <small>Eau et habitation</small>
      <h3>Voir avant de manquer</h3>
      <p>Réservoirs, chauffe-eau, douche, pompe, frigo 110 V, TV et estimation des besoins à
      venir.</p>
    </article>
    <article class="card" data-rev>
      <small>Réseau</small>
      <h3>Rester relié sans dépendre d’un seul lien</h3>
      <p>Starlink, LTE, Wi-Fi, VPN, services locaux et choix d’arrêt selon la couverture
      prévue.</p>
    </article>
    <article class="card" data-rev>
      <small>Véhicule</small>
      <h3>Conserver les systèmes d’origine</h3>
      <p>Les fonctions Ford et ambulance doivent rester opérationnelles et rejoindre JARVIS
      lorsque l’interface le permet.</p>
    </article>
    <article class="card" data-rev>
      <small>Sécurité</small>
      <h3>Comprendre ce qui entoure le véhicule</h3>
      <p>Caméras, accès, présence, périmètres et capteurs pourront enrichir le contexte
      autorisé.</p>
    </article>
  </div>
  <figure class="frame" data-rev style="margin-top:16px">
    <img src="/media/ambulance/ambulance-cutaway-control-v1.webp"
         alt="Vue en coupe du laboratoire mobile et de ses espaces contrôlables" loading="lazy">
    <figcaption><span>Vue en coupe · mode camp</span><strong>Chaque espace du véhicule, contrôlable au même endroit.</strong></figcaption>
  </figure>
  <p class="sol-all" data-rev><a class="pill ghost" href="/solutions/environnements-intelligents/#essayer">Essayer le tableau de BouLance dans JARVIS</a></p>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Automatisations envisagées</p>
      <h2>Le comportement dépend du lieu, du moment <em>et de la
      priorité.</em></h2>
    </div>
    <p data-rev>Chaque règle importante doit pouvoir être expliquée, refusée et reprise
    manuellement.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>Stationnement</small>
      <h3>Demander avant de produire du bruit.</h3>
      <p>Vérifier l’heure, la position, les règles choisies et la réserve avant de proposer
      la génératrice.</p>
    </article>
    <article class="card" data-rev>
      <small>Confort</small>
      <h3>Préparer sans gaspiller.</h3>
      <p>Chauffer l’eau ou climatiser au moment utile, puis réduire les charges si la
      projection se dégrade.</p>
    </article>
    <article class="card" data-rev>
      <small>Trajet</small>
      <h3>Anticiper l’arrêt utile.</h3>
      <p>Rapprocher couverture Internet, eau, énergie, destination et durée de conduite
      prévue.</p>
    </article>
    <article class="card" data-rev>
      <small>Maintenance</small>
      <h3>Voir les dérives avant le code.</h3>
      <p>Comparer les capteurs mécaniques, les conditions de route et l’historique avant de
      préparer un rapport.</p>
    </article>
    <article class="card" data-rev>
      <small>Sécurité</small>
      <h3>Adapter la vigilance au contexte.</h3>
      <p>Différencier un arrêt connu, une présence autorisée et un événement qui mérite une
      vérification.</p>
    </article>
    <article class="card" data-rev>
      <small>Diagnostic</small>
      <h3>Passer du symptôme au dossier.</h3>
      <p>Classer les causes, guider les contrôles, trouver la documentation et préparer le
      partage au technicien.</p>
    </article>
  </div>
</section>

<section class="statement">
  <p class="eyebrow" data-rev>La règle du laboratoire</p>
  <h2 data-rev>Tout mesurer. Tout expliquer.<br><em>Ne rien
  prétendre avant la preuve.</em></h2>
  <p data-rev>Une hypothèse guidée ne remplace jamais la validation d’un mécanicien ou d’un
  technicien qualifié.</p>
  <div class="acts" data-rev>
    <a class="pill ghost" href="/recherche/">Découvrir la méthode de recherche</a>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Suivre le laboratoire<br><span>ou contribuer à une validation?</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement
  définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
