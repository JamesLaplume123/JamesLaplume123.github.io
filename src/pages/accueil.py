# Accueil — comprendre l'ensemble en moins d'une minute.
# Rôle (docs/SITE_INFORMATION_ARCHITECTURE.md) : promesse, JARVIS en une vue,
# six capacités, laboratoire mobile comme preuve, une ouverture vers la vision,
# un appel à discuter.

import json

from config import CAPABILITIES

CAP_PHRASES = {
    "environnements-intelligents": {
        "title": "Le lieu répond à la situation, pas à une suite de commandes.",
        "copy": "Éclairage, climat, sécurité et énergie se coordonnent dans une interface unique.",
    },
    "ia-privee-connaissances": {
        "title": "Parlez à vos informations, recevez des réponses avec leurs preuves.",
        "copy": "Documents, courriels, photos et procédures redeviennent une mémoire utilisable.",
    },
    "securite-intelligente": {
        "title": "Une situation compréhensible plutôt qu’une pluie de notifications.",
        "copy": "Caméras, accès et alarmes racontent une chronologie claire, avec une action proportionnée.",
    },
    "automatisation-operations": {
        "title": "Les demandes avancent entre vos outils sans perdre leur contexte.",
        "copy": "Courriels, documents et approbations circulent, et chaque action sensible attend votre accord.",
    },
    "reseau-resilience": {
        "title": "Une vue vivante du réseau, de ses dépendances et de ses accès.",
        "copy": "Inventaire, topologie, disponibilité et accès privés surveillés en continu.",
    },
    "diagnostic-care": {
        "title": "D’un symptôme à une remise en service documentée.",
        "copy": "Hypothèses, vérifications guidées et rapport prêt pour l’intervention.",
    },
}

CAP_JSON = json.dumps(
    {
        c["slug"]: {
            "kicker": c["title"].upper(),
            "title": CAP_PHRASES[c["slug"]]["title"],
            "copy": CAP_PHRASES[c["slug"]]["copy"],
            "image": c["image"],
            "alt": f"Aperçu conceptuel — {c['title']}",
            "url": f"/solutions/{c['slug']}/",
        }
        for c in CAPABILITIES
    },
    ensure_ascii=False,
)

ENV_JSON = json.dumps(
    {
        "maison": {
            "title": "Retour prévu dans 32 minutes.",
            "copy": "La maison peut préparer l’éclairage d’arrivée et maintenir la recharge après 21 h.",
            "s1": "Absence confirmée",
            "s2": "Réserve 74 %",
            "s3": "Votre accord",
            "url": "/solutions/environnements-intelligents/",
        },
        "entreprise": {
            "title": "Livraison détectée au quai 2.",
            "copy": "Le fournisseur est attendu : l’accès peut s’ouvrir dix minutes et prévenir la réception.",
            "s1": "Visiteur attendu",
            "s2": "Zone déverrouillable",
            "s3": "Votre accord",
            "url": "/solutions/securite-intelligente/",
        },
        "vehicule": {
            "title": "Réserve solaire excédentaire.",
            "copy": "Le véhicule peut précharger la batterie habitacle avant la route de demain matin.",
            "s1": "Soleil 500 W",
            "s2": "Batteries 560 Ah",
            "s3": "Votre accord",
            "url": "/laboratoire-mobile/",
        },
    },
    ensure_ascii=False,
)

CAP_BUTTONS = "".join(
    f"""<button type="button" data-cap="{c['slug']}"{' class="is-active"' if i == 0 else ''}>
      <span>{c['num']}</span><b>{c['title']}</b>
      <small>{c['short']}</small>
    </button>"""
    for i, c in enumerate(CAPABILITIES)
)

PAGE = {
    "url": "/",
    "title": "JARVIS Private Systems | Intelligence privée et systèmes connectés",
    "description": (
        "JARVIS relie vos outils, vos informations et vos espaces dans une "
        "expérience privée, contextuelle et contrôlée."
    ),
    "content": f"""
<!-- Héros : promesse + console de décision -->
<section class="hero hero-home">
  <div class="hero-media">
    <img src="/media/concept/jarvis-hero-architecture-v1.webp"
         alt="Résidence contemporaine intégrant les systèmes JARVIS" fetchpriority="high">
  </div>
  <div class="shell hero-inner">
    <div>
      <p class="eyebrow">JARVIS · Intelligence privée</p>
      <h1>Relier ce qui existe.<br><em>Faire agir l’ensemble.</em></h1>
      <p class="lead">Une intelligence privée qui comprend vos règles, coordonne les
      systèmes autorisés et vous laisse les décisions importantes.</p>
      <div class="hero-actions">
        <a class="button button-gold" href="/plateforme/">Découvrir JARVIS <span>↗</span></a>
        <a class="button" href="/solutions/">Explorer les capacités</a>
      </div>
    </div>
    <div>
      <aside class="console" aria-label="Exemple de décision JARVIS">
        <header class="console-head"><span><i></i>JARVIS · ACTIF</span><small>LOCAL</small></header>
        <div class="console-body">
          <small>CONTEXTE ACTUEL</small>
          <strong data-console-title>Retour prévu dans 32 minutes.</strong>
          <p data-console-copy>La maison peut préparer l’éclairage d’arrivée et maintenir la recharge après 21 h.</p>
        </div>
        <ul class="console-signals">
          <li><span>PRÉSENCE</span><b data-console-s1>Absence confirmée</b></li>
          <li><span>ÉNERGIE</span><b data-console-s2>Réserve 74 %</b></li>
          <li><span>DÉCISION</span><b data-console-s3>Votre accord</b></li>
        </ul>
        <a class="console-link" href="/solutions/environnements-intelligents/" data-console-link>Voir cette capacité <span>→</span></a>
      </aside>
      <div class="env-switch" role="group" aria-label="Choisir un environnement">
        <button type="button" class="is-active" aria-pressed="true" data-env="maison">Maison</button>
        <button type="button" aria-pressed="false" data-env="entreprise">Entreprise</button>
        <button type="button" aria-pressed="false" data-env="vehicule">Véhicule</button>
      </div>
      <script type="application/json" id="env-data">{ENV_JSON}</script>
    </div>
  </div>
</section>

<!-- JARVIS en une vue : App, Core, Hub -->
<section class="section manifesto">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">La plateforme</p>
        <h2>Tout existe déjà.<br><em>JARVIS fait travailler l’ensemble.</em></h2>
      </div>
      <p>Les bons appareils, logiciels et services sont déjà là. JARVIS ajoute le
      lien qui manque : une identité, du contexte, des permissions et une façon
      claire de décider.</p>
    </div>
    <div class="manifesto-grid">
      <figure data-reveal>
        <img src="/media/product/jarvis-hub-v1.webp"
             alt="JARVIS Hub intégré dans une résidence contemporaine" loading="lazy">
        <figcaption>
          <span>JARVIS HUB</span>
          <strong>L’intelligence demeure près du lieu.</strong>
        </figcaption>
      </figure>
      <div data-reveal>
        <div class="card-grid" style="grid-template-columns: 1fr;">
          <article class="card">
            <p class="eyebrow">Interface</p>
            <h3>JARVIS App</h3>
            <p>Comprendre, demander, approuver et consulter les preuves — sur les
            écrans que vous autorisez.</p>
          </article>
          <article class="card">
            <p class="eyebrow">Intelligence</p>
            <h3>JARVIS Core</h3>
            <p>Contexte, mémoire autorisée, permissions, automatisations et
            journal d’audit : le logiciel central.</p>
          </article>
          <article class="card">
            <p class="eyebrow">Sur place</p>
            <h3>JARVIS Hub</h3>
            <p>L’infrastructure locale qui exécute JARVIS Core et garde vos
            données près de vos systèmes.</p>
          </article>
        </div>
        <div class="badge-row">
          <span class="badge"><i></i>LOCAL</span>
          <span class="badge badge-gold"><i></i>PRIVÉ</span>
          <span class="badge badge-cyan"><i></i>AUTONOME</span>
        </div>
        <p style="margin-top:1.8rem;"><a class="link-arrow" href="/plateforme/">Comprendre l’architecture <span>↗</span></a></p>
      </div>
    </div>
  </div>
</section>

<!-- Six capacités -->
<section class="section section-raised" id="capacites">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Une plateforme · Six capacités</p>
        <h2>Le bon outil.<br><em>Au bon moment.</em></h2>
      </div>
      <p>Chaque capacité utilise la même identité, les mêmes permissions et la
      même trace. On commence par un besoin réel, puis on relie seulement ce qui
      apporte une valeur claire.</p>
    </div>
    <div class="cap-stage" data-reveal>
      <nav class="cap-list" aria-label="Explorer les six capacités">
        {CAP_BUTTONS}
      </nav>
      <article class="cap-preview">
        <img data-cap-image src="/media/solutions/environnements-intelligents.webp"
             alt="Aperçu conceptuel — Environnements intelligents" loading="lazy">
        <section>
          <span data-cap-kicker>ENVIRONNEMENTS INTELLIGENTS</span>
          <h3 data-cap-title>Le lieu répond à la situation, pas à une suite de commandes.</h3>
          <p data-cap-copy>Éclairage, climat, sécurité et énergie se coordonnent dans une interface unique.</p>
          <a class="link-arrow" data-cap-link href="/solutions/environnements-intelligents/">Explorer cette capacité <span>↗</span></a>
        </section>
      </article>
      <script type="application/json" id="cap-data">{CAP_JSON}</script>
    </div>
  </div>
</section>

<!-- Preuve : laboratoire mobile -->
<section class="section">
  <div class="shell proof-grid">
    <figure data-reveal>
      <img src="/media/ambulance/ambulance-garage-lab-v1.webp"
           alt="Ambulance Ford 2017 dans le garage du laboratoire mobile JARVIS" loading="lazy">
    </figure>
    <div data-reveal>
      <p class="eyebrow">Premier terrain de preuve</p>
      <h2>Le système sort<br><em>de l’écran.</em></h2>
      <p>Une Ford 2017 V10 devient un environnement d’essai réel pour l’énergie,
      le réseau, le confort, la sécurité, le diagnostic et l’automatisation.</p>
      <dl class="stat-row">
        <div><dt>Énergie</dt><dd>560 Ah</dd></div>
        <div><dt>Solaire</dt><dd>500 W</dd></div>
        <div><dt>Contexte</dt><dd>Mobile</dd></div>
      </dl>
      <a class="link-arrow" href="/laboratoire-mobile/">Découvrir le laboratoire mobile <span>↗</span></a>
    </div>
  </div>
</section>

<!-- Vision -->
<section class="vision-band">
  <img src="/media/concept/jarvis-earth-network-v1.png"
       alt="La Terre nocturne vue de l’espace, centrée sur l’Amérique du Nord" loading="lazy">
  <div class="shell" data-reveal>
    <p class="eyebrow">Vision à long terme</p>
    <h2>Une intelligence privée.<br>Des environnements autonomes.<br><em>Une vie plus fluide.</em></h2>
    <p style="margin-top:1.6rem;"><a class="link-arrow" href="/vision-roadmap/">Découvrir la vision <span>→</span></a></p>
  </div>
</section>

<!-- Appel -->
<section class="cta-band">
  <div class="shell cta-inner" data-reveal>
    <div>
      <p class="eyebrow">Premier échange</p>
      <h2>Construisons une première preuve <em>qui compte.</em></h2>
    </div>
    <div>
      <p>Décrivez le problème et son contexte. La première preuve utile sera
      clairement définie.</p>
      <a class="button button-fill" href="/contact/">Discuter du projet <span>↗</span></a>
    </div>
  </div>
</section>
""",
}
