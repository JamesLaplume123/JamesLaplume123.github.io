# Accueil — vendre JARVIS, le logiciel (refonte novembre 2026).
# Parcours : promesse → manifeste → visite de l'app (épinglée, jamais coupée) →
# JARVIS en direct (vraies données + décisions simulées) → comment ça marche →
# où en est le projet → modes → six solutions → offre → laboratoire → FAQ → démo.
# Les questions de la FAQ alimentent aussi les données structurées (FAQPage).

import json

from demos import app, boulance, carte, maison

FAQ = [
    (
        "Qu’est-ce que JARVIS, concrètement?",
        "Un logiciel privé installé sur un petit serveur chez vous, le JARVIS Hub. Il relie "
        "ce que vous avez déjà — lumières, caméras, chauffage, batteries, agenda, documents — "
        "et vous le présente dans une seule application. Il propose des actions; vous gardez "
        "la décision.",
    ),
    (
        "Mes données quittent-elles la maison ou l’entreprise?",
        "Pas par défaut. JARVIS est conçu pour que tout vive sur le Hub, chez vous. Le nuage ne "
        "sert qu’à ce que vous choisissez : un accès à distance par un relais qui ne garde rien, "
        "ou une copie de sauvegarde chiffrée.",
    ),
    (
        "Dois-je changer mes appareils?",
        "Généralement non. JARVIS s’appuie sur Home Assistant et sur des standards ouverts comme "
        "Zigbee, Z-Wave, Matter et MQTT pour parler à des appareils de marques différentes. On "
        "commence par ce qui existe déjà.",
    ),
    (
        "Est-ce que ça fonctionne sans Internet?",
        "C’est le principe du local d’abord : l’interface et les automatisations continuent de "
        "fonctionner sur le réseau du lieu. Seul l’accès à distance demande une connexion.",
    ),
    (
        "Pour qui est JARVIS?",
        "Pour les résidences (maison, condo, chalet), les entreprises (bureau, commerce, atelier) "
        "et les véhicules aménagés (VR, unités spécialisées) qui veulent une domotique, une "
        "sécurité et une IA qui restent privées.",
    ),
    (
        "Est-ce disponible aujourd’hui?",
        "JARVIS est en construction. Le noyau du logiciel (comptes, droits, sécurité) est en "
        "développement et le tableau JARVIS Signature fonctionne déjà sur Home Assistant. Une "
        "démo vous montre honnêtement ce qui fonctionne aujourd’hui et ce qui reste à construire.",
    ),
    (
        "Combien ça coûte?",
        "Le prix dépend de votre environnement et de ce qu’on relie. On en parle après la "
        "première rencontre, une fois le besoin clair et la première preuve utile définie.",
    ),
    (
        "Où êtes-vous situé?",
        "JARVIS Private Systems est basé dans la région de Saint-Hyacinthe, au Québec. "
        "Écrivez-moi pour voir ce qui est possible chez vous.",
    ),
]

FAQ_HTML = "".join(
    f"""<details class="faq-item" data-rev>
      <summary><span>{q}</span><i aria-hidden="true"></i></summary>
      <div class="faq-a"><p>{a}</p></div>
    </details>"""
    for q, a in FAQ
)

SCHEMA = json.dumps(
    [
        {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "@id": "https://jameslaplume.ca/#entreprise",
            "name": "JARVIS Private Systems",
            "alternateName": "JARVIS",
            "url": "https://jameslaplume.ca/",
            "logo": "https://jameslaplume.ca/apple-touch-icon.png",
            "image": "https://jameslaplume.ca/media/product/user/accueil-og.jpg",
            "email": "laplumejames@gmail.com",
            "description": (
                "Domotique privée, sécurité intelligente, automatisation et IA locale : "
                "JARVIS relie les systèmes d’une maison, d’une entreprise ou d’un véhicule "
                "dans un logiciel installé sur place."
            ),
            "founder": {"@type": "Person", "name": "James Laplume"},
            "address": {
                "@type": "PostalAddress",
                "addressRegion": "QC",
                "addressCountry": "CA",
            },
            "areaServed": [
                {"@type": "City", "name": "Saint-Hyacinthe"},
                {"@type": "AdministrativeArea", "name": "Montérégie"},
                {"@type": "AdministrativeArea", "name": "Québec"},
            ],
            "knowsAbout": [
                "Domotique",
                "Maison intelligente",
                "Home Assistant",
                "Sécurité intelligente",
                "Caméras de surveillance privées",
                "Cybersécurité résidentielle",
                "Automatisation d’entreprise",
                "Intelligence artificielle locale",
                "Énergie solaire et batteries LiFePO4",
            ],
            "availableLanguage": ["fr", "en"],
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": "https://jameslaplume.ca/#site",
            "name": "JARVIS Private Systems",
            "url": "https://jameslaplume.ca/",
            "inLanguage": "fr-CA",
            "publisher": {"@id": "https://jameslaplume.ca/#entreprise"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in FAQ
            ],
        },
    ],
    ensure_ascii=False,
    indent=1,
)

STANDARDS = [
    "Home Assistant", "Zigbee", "Z-Wave", "Matter", "MQTT", "ESPHome",
    "Frigate", "WireGuard", "Starlink", "LiFePO₄", "Whisper", "Piper",
]
MARQUEE = "".join(f"<span>{s}</span>" for s in STANDARDS)

PAGE = {
    "url": "/",
    "v2": True,
    "title": "Domotique privée et sécurité intelligente au Québec | JARVIS",
    "assets": ["app", "maison", "boulance", "carte"],
    "description": (
        "Domotique privée, sécurité intelligente et IA locale, installées chez vous. "
        "JARVIS relie vos appareils sans envoyer vos données au nuage. Saint-Hyacinthe, Québec."
    ),
    "content": f"""
<!-- Héros : la maison s'allume, JARVIS prend la parole -->
<section class="hero" data-hero>
  <div class="bg" data-hero-bg>
    <img class="dark" src="/media/concept/jarvis-hero-architecture-v1.webp" width="1916" height="821" alt="" aria-hidden="true" fetchpriority="high">
    <img class="lit" src="/media/concept/jarvis-hero-architecture-v1.webp" width="1916" height="821"
         alt="Résidence contemporaine la nuit, systèmes JARVIS actifs">
  </div>
  <div class="hero-flash" aria-hidden="true"></div>
  <div class="hud" aria-hidden="true">
    <div class="hud-tag t-out" style="--x:8%;--y:58%;--px:24%;--py:34%"><i></i><span><small>Extérieur · réel</small><b data-live="temp-hud">— °C</b></span></div>
    <div class="hud-tag t-fire" style="--x:9%;--y:73%;--px:27%;--py:63%"><i></i><span><small>Terrasse</small><b>Foyer allumé</b></span></div>
    <div class="hud-tag t-salon" style="--x:12%;--y:89%;--px:34%;--py:77%"><i></i><span><small>Salon</small><b>Soirée · 60 %</b></span></div>
    <div class="hud-tag t-hub" style="--x:92%;--y:60%;--px:63%;--py:47%"><i></i><span><small>Cuisine</small><b>3 lumières · 40 %</b></span></div>
    <div class="hud-tag t-energy" style="--x:91%;--y:80%;--px:80%;--py:74%"><i></i><span><small>Énergie</small><b>1,2 kW · stable</b></span></div>
  </div>
  <div class="hero-inner">
    <p class="eyebrow hero-eyebrow"><span data-greet>Domotique · Sécurité · IA privée</span></p>
    <h1><span class="ln">Relier ce qui existe.</span><span class="ln l2">Faire agir l’ensemble.</span></h1>
    <p class="sub">Une intelligence privée, installée chez vous, qui comprend vos règles,
    coordonne vos systèmes et vous laisse les décisions importantes.</p>
    <div class="acts">
      <a class="pill" href="#app" data-magnet>Découvrir JARVIS</a>
      <a class="pill ghost" href="/contact/" data-magnet>Réserver une démo</a>
    </div>
    <a class="live-pill" href="#direct" data-live-pill>
      <i class="dot" aria-hidden="true"></i>
      <span>En direct<span class="lp-place"> · Saint-Hyacinthe</span></span>
      <b data-live="temp-short">—</b>
      <span class="sep" aria-hidden="true"></span>
      <span data-live="visits-short">Visites —</span>
    </a>
  </div>
  <i class="cue" aria-hidden="true"></i>
</section>

<!-- Manifeste -->
<section class="mani" aria-label="Manifeste">
  <div class="stick"><p>Vos appareils existent déjà. Vos informations existent déjà.
  Il manquait l’intelligence privée qui les comprend — et qui les fait travailler ensemble.</p></div>
</section>

<!-- Vitrine de l'app : JARVIS App rendue en vrai HTML (assets/demos/app.*) -->
<section class="vitrine" id="app" aria-label="JARVIS App">
  <div class="head" data-rev>
    <p class="eyebrow">JARVIS App · l’interface</p>
    <h2 data-split>Une seule application.<br><em>Toute votre vie connectée.</em></h2>
  </div>
  {app.html()}
</section>

<!-- Ma maison : démo interactive -->
<section class="sect maison-home" id="maison" aria-labelledby="maison-titre">
  <div class="head" data-rev style="max-width:52rem;margin:0 auto 3rem;text-align:center">
    <p class="eyebrow">Essayez · démonstration interactive</p>
    <h2 id="maison-titre" data-split style="margin:1.1rem 0 0;font-weight:700;font-size:clamp(2.2rem,5vw,4rem);letter-spacing:-.04em;line-height:1.06">Touchez une pièce.<br><em>Elle vous répond.</em></h2>
    <p style="color:#c4c4cc;max-width:40rem;margin:1.2rem auto 0">Choisissez une ambiance ou une pièce : lumière, chauffage, stores et verrous se règlent
    sous vos yeux. Chaque commande est envoyée, puis confirmée.</p>
  </div>
  {maison.html()}
</section>

<!-- JARVIS en direct : vraies données, décisions simulées -->
<section class="live" id="direct" aria-labelledby="direct-titre">
  <div class="head" data-rev>
    <p class="eyebrow"><i class="dot" aria-hidden="true"></i> En direct · Saint-Hyacinthe</p>
    <h2 id="direct-titre" data-split>JARVIS, maintenant.<br><em>Avec de vraies données.</em></h2>
    <p>À gauche, les conditions réelles reçues d’Environnement Canada. À droite, ce que les
    règles de JARVIS feraient avec elles. Les décisions sont simulées : aucun appareil réel
    n’est commandé.</p>
  </div>

  <div class="console" data-live-root data-rev>
    <div class="console-top">
      <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
      <b>JARVIS · Console</b>
      <span class="console-clock" data-live="clock">--:--:--</span>
      <span class="console-state" data-live="state">Connexion…</span>
    </div>

    <div class="console-grid">
      <!-- Ce que JARVIS voit -->
      <div class="panel panel-see">
        <p class="panel-kick">Ce que JARVIS voit <span class="tag tag-real">Données réelles</span></p>
        <div class="now">
          <div class="now-temp"><b data-live="temp" class="odo" aria-live="polite">--</b><i>°C</i></div>
          <div class="now-txt">
            <strong data-live="condition">Chargement…</strong>
            <span data-live="feels">&nbsp;</span>
          </div>
        </div>
        <dl class="metrics">
          <div><dt>Vent</dt><dd data-live="wind">—</dd></div>
          <div><dt>Rafales</dt><dd data-live="gust">—</dd></div>
          <div><dt>Humidité</dt><dd data-live="humidity">—</dd></div>
          <div><dt>Pression</dt><dd data-live="pressure">—</dd></div>
        </dl>
        <div class="sun">
          <svg viewBox="0 0 300 120" aria-hidden="true">
            <path class="sun-track" d="M20 105 A130 95 0 0 1 280 105"/>
            <path class="sun-done" data-live="sun-arc" d="M20 105 A130 95 0 0 1 280 105"/>
            <line x1="8" y1="105" x2="292" y2="105" class="sun-horizon"/>
            <circle class="sun-dot" data-live="sun-dot" cx="20" cy="105" r="7"/>
          </svg>
          <div class="sun-legend">
            <span>Lever <b data-live="sunrise">--:--</b></span>
            <span data-live="sun-state">&nbsp;</span>
            <span>Coucher <b data-live="sunset">--:--</b></span>
          </div>
        </div>
        <div class="hours" data-live="hours" aria-label="Prochaines heures"></div>
        <p class="src" data-live="source">Source : Environnement et Changement climatique Canada</p>
      </div>

      <!-- Ce que JARVIS ferait -->
      <div class="panel panel-do">
        <p class="panel-kick">Ce que JARVIS ferait <span class="tag tag-sim">Décisions simulées</span></p>
        <ul class="rules" data-live="rules">
          <li class="rule is-wait"><b>Analyse des règles…</b><small>En attente des données</small></li>
        </ul>
        <div class="visits">
          <span class="visits-k">Visites du site</span>
          <b class="odo" data-live="visits">—</b>
          <small>Compteur réel, sans témoin ni pistage</small>
        </div>
      </div>
    </div>

    <div class="journal" aria-label="Journal des décisions">
      <p class="panel-kick">Journal</p>
      <ol data-live="journal"></ol>
    </div>
  </div>
</section>

<!-- BouLance en direct : batteries réelles + radar -->
<section class="sect" id="boulance" aria-labelledby="boulance-titre">
  <div class="head" data-rev style="max-width:52rem;margin:0 auto 3rem;text-align:center">
    <p class="eyebrow" style="display:inline-flex;align-items:center;gap:.7rem"><i class="dot" aria-hidden="true"></i> Le laboratoire mobile · en direct</p>
    <h2 id="boulance-titre" style="margin:1.1rem 0 0;font-weight:700;font-size:clamp(2.2rem,5vw,4rem);letter-spacing:-.04em;line-height:1.06">Les batteries de l’ambulance.<br><em>Pour vrai, en ce moment.</em></h2>
    <p style="color:#c4c4cc;max-width:40rem;margin:1.2rem auto 0">Deux batteries LiFePO₄ de 280 Ah, lues par Home Assistant dans le véhicule et
    affichées ici en direct. C’est exactement ce que JARVIS fera chez vous : des données vraies, jamais inventées.</p>
  </div>
  {boulance.html()}
  <div style="height:16px"></div>
  {carte.html()}
</section>

<!-- Comment ça marche -->
<section class="how" id="fonctionnement" aria-labelledby="how-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Comment ça marche</p>
    <h2 id="how-titre" data-split>Domotique, sécurité et IA.<br><em>Un seul système, chez vous.</em></h2>
  </div>

  <div class="flow" data-rev>
    <svg class="flow-svg" viewBox="0 0 1000 420" aria-hidden="true">
      <defs>
        <linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".05"/><stop offset=".5" stop-color="currentColor" stop-opacity=".55"/><stop offset="1" stop-color="currentColor" stop-opacity=".05"/></linearGradient>
      </defs>
      <g class="flow-lines" fill="none" stroke="url(#fl)" stroke-width="1.4">
        <path id="p1" d="M210 50 C 360 50, 380 210, 500 210"/>
        <path id="p2" d="M210 120 C 360 120, 380 210, 500 210"/>
        <path id="p3" d="M210 190 C 360 190, 400 210, 500 210"/>
        <path id="p4" d="M210 260 C 360 260, 400 210, 500 210"/>
        <path id="p5" d="M210 330 C 360 330, 380 210, 500 210"/>
        <path id="p6" d="M210 395 C 360 395, 380 210, 500 210"/>
        <path id="p7" d="M500 210 C 640 210, 660 210, 790 210"/>
      </g>
      <g class="flow-pulses">
        <circle r="3.2"><animateMotion dur="3.4s" repeatCount="indefinite"><mpath href="#p1"/></animateMotion></circle>
        <circle r="3.2"><animateMotion dur="2.9s" begin=".6s" repeatCount="indefinite"><mpath href="#p2"/></animateMotion></circle>
        <circle r="3.2"><animateMotion dur="3.1s" begin="1.2s" repeatCount="indefinite"><mpath href="#p3"/></animateMotion></circle>
        <circle r="3.2"><animateMotion dur="3.6s" begin=".3s" repeatCount="indefinite"><mpath href="#p4"/></animateMotion></circle>
        <circle r="3.2"><animateMotion dur="3.3s" begin="1.6s" repeatCount="indefinite"><mpath href="#p5"/></animateMotion></circle>
        <circle r="3.2"><animateMotion dur="3s" begin=".9s" repeatCount="indefinite"><mpath href="#p6"/></animateMotion></circle>
        <circle r="4" class="out"><animateMotion dur="2.2s" begin="1s" repeatCount="indefinite"><mpath href="#p7"/></animateMotion></circle>
      </g>
    </svg>
    <ul class="flow-in">
      <li><b>Lumières</b><small>Zigbee · Z-Wave · Matter</small></li>
      <li><b>Caméras</b><small>Événements · détection locale</small></li>
      <li><b>Chauffage</b><small>Confort · horaires</small></li>
      <li><b>Énergie</b><small>Batteries · solaire</small></li>
      <li><b>Agenda et messages</b><small>Vos comptes reliés</small></li>
      <li><b>Documents</b><small>Procédures · dossiers</small></li>
    </ul>
    <div class="flow-hub">
      <span class="ring r1" aria-hidden="true"></span><span class="ring r2" aria-hidden="true"></span>
      <b>JARVIS Hub</b><small>Chez vous</small>
      <em>Règles · droits · journal · IA locale</em>
    </div>
    <div class="flow-out">
      <b>JARVIS App</b><small>Vous</small>
      <span class="approve"><i aria-hidden="true">✓</i> Votre accord</span>
    </div>
  </div>

  <ol class="steps">
    <li data-rev><i>01</i><h3>On regarde ce qui existe</h3>
      <p>Vos appareils, vos outils et ce qui vous fait perdre du temps. JARVIS part de votre
      réalité, pas d’un catalogue.</p></li>
    <li data-rev><i>02</i><h3>Une première preuve utile</h3>
      <p>Un cas concret défini avec vous et qui fonctionne chez vous : l’éclairage qui suit le
      coucher du soleil, une alerte caméra qui dit vraiment ce qui se passe.</p></li>
    <li data-rev><i>03</i><h3>On élargit à votre rythme</h3>
      <p>Chaque capacité s’ajoute comme une extension, activée par l’administrateur, avec des
      droits précis pour chaque personne.</p></li>
  </ol>

  <div class="marquee" aria-label="Standards ouverts sur lesquels JARVIS s’appuie">
    <p class="marquee-k">Conçu pour s’appuyer sur des standards ouverts</p>
    <div class="marquee-track"><div>{MARQUEE}</div><div aria-hidden="true">{MARQUEE}</div></div>
  </div>
</section>

<!-- Le Hub -->
<section class="hub" aria-labelledby="hub-titre">
  <figure class="hub-media wipe" data-rev>
    <img src="/media/product/jarvis-hub-v1.webp" width="1672" height="941"
         alt="JARVIS Hub posé sur un meuble d’une résidence contemporaine" loading="lazy">
  </figure>
  <div class="hub-copy" data-rev>
    <p class="eyebrow">JARVIS Hub</p>
    <h2 id="hub-titre">L’intelligence demeure <em>chez vous.</em></h2>
    <p>Un petit serveur installé sur place garde vos règles, vos comptes, votre journal et
    votre IA locale. Pas d’abonnement obligatoire au nuage pour que la maison fonctionne.</p>
    <div class="chiprow" style="margin-top:1.4rem">
      <span class="chip">Local d’abord</span>
      <span class="chip">Sauvegardes chiffrées</span>
      <span class="chip">Décisions humaines</span>
    </div>
  </div>
</section>

<!-- Où en est JARVIS -->
<section class="status" aria-labelledby="status-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Où en est JARVIS · novembre 2026</p>
    <h2 id="status-titre">Du concret, <em>pas des promesses.</em></h2>
  </div>
  <div class="status-grid">
    <article class="stat" data-rev><b><span data-n="161">161</span></b><h3>écrans conçus</h3>
      <p>Côté personne et côté administration, du premier démarrage au partage.</p></article>
    <article class="stat" data-rev><b>En service</b><h3>Tableau JARVIS Signature</h3>
      <p>Il pilote déjà l’éclairage du laboratoire mobile, sur Home Assistant.</p></article>
    <article class="stat" data-rev><b><span data-n="560">560</span><i>Ah</i></b><h3>premier terrain réel</h3>
      <p>Une ambulance Ford 2017 transformée : énergie, réseau et diagnostic.</p></article>
    <article class="stat" data-rev><b>En cours</b><h3>Noyau du logiciel</h3>
      <p>Comptes sur invitation, droits, double authentification, journal et sauvegardes.</p></article>
  </div>
  <ol class="road" data-rev aria-label="Grandes étapes">
    <li class="done"><span>Fondations</span></li>
    <li class="now"><span>Noyau et comptes</span></li>
    <li><span>Extensions</span></li>
    <li><span>Hub sur place</span></li>
    <li><span>Environnements intelligents</span></li>
    <li><span>Prêt à vendre</span></li>
  </ol>
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
</section>

<!-- Six solutions (bento) -->
<section class="bento" id="capacites">
  <div class="head" data-rev>
    <p class="kick">Six solutions · Un point de départ</p>
    <h2 data-split>Votre besoin.<br>La bonne solution.</h2>
    <p>Choisissez ce que vous aimeriez simplifier. Un clic sur une carte ouvre sa solution.</p>
  </div>
  <nav class="grid" aria-label="Accéder aux six solutions">
    <a class="tile w3" href="/solutions/environnements-intelligents/" data-rev data-tilt>
      <img src="/media/solutions/environnements-intelligents.webp" alt="" loading="lazy">
      <span class="lab"><small>01 · Domotique</small><b>Environnements intelligents</b><em>Lumières, confort et énergie réunis.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile w3" href="/solutions/ia-privee-connaissances/" data-rev data-tilt>
      <img src="/media/solutions/ia-privee-connaissances.webp" alt="" loading="lazy">
      <span class="lab"><small>02 · IA locale</small><b>IA privée et connaissances</b><em>Retrouver vos documents et les bonnes réponses.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile" href="/solutions/securite-intelligente/" data-rev data-tilt>
      <img src="/media/solutions/securite-intelligente.webp" alt="" loading="lazy">
      <span class="lab"><small>03 · Caméras</small><b>Sécurité intelligente</b><em>Comprendre les événements de vos lieux.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile" href="/solutions/automatisation-operations/" data-rev data-tilt>
      <img src="/media/solutions/jarvis-enterprise-operations-v1.webp" alt="" loading="lazy">
      <span class="lab"><small>04 · Entreprise</small><b>Automatisation d’entreprise</b><em>Faire avancer les demandes de votre équipe.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile" href="/solutions/reseau-resilience/" data-rev data-tilt>
      <img src="/media/solutions/reseau-resilience.webp" alt="" loading="lazy">
      <span class="lab"><small>05 · Réseau</small><b>Réseau et cybersécurité</b><em>Garder vos connexions fiables et privées.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
    <a class="tile w6" href="/solutions/diagnostic-care/" data-rev data-tilt>
      <img src="/media/solutions/diagnostic-care.webp" alt="" loading="lazy">
      <span class="lab"><small>06 · Continuité</small><b>Diagnostic &amp; continuité</b><em>Comprendre un souci et préparer la suite.</em><span class="go">Voir la solution <i aria-hidden="true">↗</i></span></span></a>
  </nav>
</section>

<!-- Offre -->
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
        <li>Domotique : confort, énergie et éclairage coordonnés</li>
        <li>Caméras et alarmes qui expliquent les événements</li>
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

<!-- Laboratoire (preuve) -->
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

<!-- Questions fréquentes -->
<section class="faq" id="questions" aria-labelledby="faq-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Questions fréquentes</p>
    <h2 id="faq-titre">Domotique privée : <em>vos questions.</em></h2>
  </div>
  <div class="faq-list">{FAQ_HTML}</div>
</section>

<script type="application/ld+json">
{SCHEMA}
</script>

<!-- Appel -->
<section class="cta" id="demo">
  <h2 data-rev>Voyez JARVIS<br><span>de vos yeux.</span></h2>
  <p data-rev>Une rencontre, vos besoins réels, ce qui existe aujourd’hui —
  et la première preuve utile définie ensemble.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/" data-magnet>Réserver une démo</a></div>
</section>
""",
}
