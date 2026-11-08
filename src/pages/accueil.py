# Accueil — vendre JARVIS, le logiciel (audit de simplicité, novembre 2026).
# Chaque section répond à trois questions : c'est quoi, qu'est-ce que ça fait pour moi, où cliquer.
# Parcours : promesse → mission (trois liens) → l'app → les sept extensions (la suite logique) →
# la maison à essayer → la météo réelle → comment ça marche (liens vers /plateforme/) → l'offre →
# laboratoire mobile (batteries en direct) → FAQ → démo. Rust, modes et feuille de route vivent
# sur leurs propres pages (/plateforme/#rust, pied de page, /vision-roadmap/).
# Les questions de la FAQ alimentent aussi les données structurées (FAQPage).

import json

from config import CAPABILITIES
from demos import app, maison, meteo
from partials import ext_icon
import galerie


def apercu_solutions():
    """Les solutions en un coup d'œil; chacune s'ouvre dans JARVIS, comme une extension."""
    cartes = []
    for c in CAPABILITIES:
        cartes.append(f"""<article class="sol-card" data-rev>
      <a class="sol-shot" href="/solutions/{c['slug']}/#jarvis" tabindex="-1" aria-hidden="true">
        <img src="{c['image']}" alt="" loading="lazy" decoding="async">
        <span class="sol-num">{c['num']}</span>
      </a>
      <div class="sol-body">
        <p class="sol-kick">{c['label']}</p>
        <h3><a href="/solutions/{c['slug']}/#jarvis">{c['title']}</a></h3>
        <p class="sol-line">{c['short']}</p>
        <span class="sol-go" aria-hidden="true">Essayer dans JARVIS <i>↗</i></span>
      </div>
    </article>""")
    return "\n    ".join(cartes)


# L'offre : chaque environnement mène directement aux extensions qui le servent.
OFFRE = [
    ("Résidence", "Maison · condo · chalet",
     ["environnements-intelligents", "securite-intelligente", "ia-privee-connaissances"]),
    ("Entreprise", "Bureau · commerce · atelier",
     ["automatisation-operations", "securite-intelligente", "reseau-resilience"]),
    ("Mobilité", "VR · véhicule aménagé · unité spécialisée",
     ["mobilite", "diagnostic-care", "reseau-resilience"]),
]
TITRES = {c["slug"]: c["title"] for c in CAPABILITIES}


def offre_plans():
    cartes = []
    for i, (k, h, slugs) in enumerate(OFFRE):
        liens = "".join(
            f'<li><a href="/solutions/{s}/#jarvis">{ext_icon(s)}<span>{TITRES[s]}</span></a></li>' for s in slugs
        )
        cartes.append(f"""<article class="plan{' star' if i == 1 else ''}" data-rev>
      <small>{k}</small>
      <h3>{h}</h3>
      <p class="plan-k">Hub JARVIS, plus par exemple :</p>
      <ul class="plan-x">{liens}</ul>
    </article>""")
    return "\n    ".join(cartes)


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
    "Rust", "Home Assistant", "Zigbee", "Z-Wave", "Matter", "MQTT", "ESPHome",
    "Frigate", "WireGuard", "Starlink", "LiFePO₄", "Whisper", "Piper",
]
MARQUEE = "".join(f"<span>{s}</span>" for s in STANDARDS)

PAGE = {
    "url": "/",
    "v2": True,
    "title": "Domotique privée et sécurité intelligente au Québec | JARVIS",
    "assets": ["app", "maison", "meteo", "labdirect", "galerie"],
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
  <div class="hero-inner">
    <div class="hero-copy">
      <p class="eyebrow hero-eyebrow">Sécurité privée · domotique · IA — Québec</p>
      <h1><span class="ln">Libérez votre temps.</span><span class="ln l2">Gardez le contrôle.</span></h1>
      <p class="sub">Un logiciel privé, installé chez vous, qui réunit votre maison, votre sécurité
      et vos informations. Il s’occupe de ce qui se répète; vous gardez les décisions.</p>
      <div class="acts">
        <a class="pill" href="#app" data-magnet>Essayer l’app</a>
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
    <aside class="hp" data-hero-panel aria-label="Aperçu de JARVIS : la maison en ce moment">
      <div class="hp-head"><span class="hp-brand">JARVIS</span><span>Maison · <time data-hp-clock>—</time></span></div>
      <div class="hp-wx">
        <b data-live="temp-short">—</b>
        <span><span data-live="cond">Conditions actuelles</span><br>Saint-Hyacinthe · <em class="hp-tag real">réel</em></span>
      </div>
      <ul class="hp-rooms">
        <li data-room="salon"><span>Salon</span><b>Soirée · 60 %</b><i style="--v:.6"></i></li>
        <li data-room="chambre"><span>Chambres</span><b>19 °C</b><i style="--v:.42"></i></li>
        <li data-room="entree"><span>Entrée</span><b>Déverrouillée</b></li>
        <li data-room="energie"><span>Énergie</span><b>1,2 kW</b><i style="--v:.3"></i></li>
      </ul>
      <div class="hp-ask" data-hp-ask>
        <small>JARVIS propose</small>
        <p data-hp-text>Passer la maison en mode nuit à 23 h ? Portes verrouillées, caméras en détection.</p>
        <div class="hp-acts"><button type="button" data-hp="no">Plus tard</button><button type="button" class="ok" data-hp="ok">Approuver</button></div>
        <p class="hp-state" role="status" aria-live="polite"></p>
      </div>
      <p class="hp-foot">Démonstration · pièces simulées, aucun appareil commandé</p>
    </aside>
  </div>
  <i class="cue" aria-hidden="true"></i>
</section>

<!-- Mission : la liberté, par le temps et le contrôle -->
<section class="mission" aria-labelledby="mission-titre">
  <div class="mission-head" data-rev>
    <p class="eyebrow">Notre mission</p>
    <h2 id="mission-titre">La technologie doit rendre libre. <em>Pas dépendant.</em></h2>
  </div>
  <ol class="pillars">
    <li data-rev>
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></svg>
      <h3>Du temps libéré</h3>
      <p>Ce qui se répète se fait seul, selon vos règles.</p>
      <a class="pillar-go" href="/solutions/automatisation-operations/">Voir l’automatisation <i aria-hidden="true">→</i></a>
    </li>
    <li data-rev>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>
      <h3>Le contrôle, simplement</h3>
      <p>Une seule app, des mots simples, rien sans votre accord.</p>
      <a class="pillar-go" href="/plateforme/#ia">Voir comment l’IA demande la permission <i aria-hidden="true">→</i></a>
    </li>
    <li data-rev>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v5.5c0 4.3-3 7.9-7 9.5-4-1.6-7-5.2-7-9.5V6z"/><path d="M9 12l2 2 4-4"/></svg>
      <h3>La sécurité privée</h3>
      <p>Vos données restent chez vous, sur le Hub, et non dans le nuage.</p>
      <a class="pillar-go" href="/plateforme/#hub">Voir le Hub <i aria-hidden="true">→</i></a>
    </li>
  </ol>
</section>

<!-- Pour qui : clients ordinaires et de prestige (src/galerie.py) -->
{galerie.clients_fr()}

<!-- Vitrine de l'app (dossier User v25) : le logiciel dans une seule fenêtre (assets/demos/app.*) -->
<section class="vitrine" id="app" aria-label="JARVIS App">
  <div class="head" data-rev>
    <p class="eyebrow">JARVIS App · l’interface</p>
    <h2 data-split>Une seule application.<br><em>Toute votre vie connectée.</em></h2>
    <p class="vitrine-lead">Le vrai logiciel. Choisissez un écran à gauche&nbsp;: il s’ouvre ici.</p>
  </div>
  {app.html()}
</section>

<!-- Les sept extensions : la suite logique après l'app; chacune s'ouvre dans JARVIS -->
<section class="bento sols" id="capacites" aria-labelledby="ext-titre">
  <div class="head" data-rev>
    <p class="kick">Sept extensions · une équipe</p>
    <h2 id="ext-titre" data-split>Ajoutez seulement<br><em>ce dont vous avez besoin.</em></h2>
    <p>Réceptionniste, gardien, archiviste, technicien : chaque extension fait un travail précis, dans
    la même app. Touchez-en une pour l’essayer.</p>
  </div>
  <div class="sol-grid">
    {apercu_solutions()}
  </div>
  <p class="sol-all" data-rev><a class="pill ghost" href="/solutions/">Comparer les sept solutions</a>
  <a class="pill ghost" href="/plateforme/#ensemble">Comment elles travaillent ensemble</a></p>
</section>

<!-- Ma maison : démo interactive -->
<section class="sect maison-home" id="maison" aria-labelledby="maison-titre">
  <div class="head shead" data-rev>
    <p class="eyebrow">Essayez · démonstration interactive</p>
    <h2 id="maison-titre" data-split>Touchez une pièce.<br><em>Elle vous répond.</em></h2>
    <p>Choisissez une ambiance ou une pièce : lumière, chauffage, stores et verrous répondent.</p>
  </div>
  {maison.html()}
</section>

<!-- Météo en direct : le vrai ciel de Saint-Hyacinthe, et ce que JARVIS en ferait (décisions simulées) -->
<section class="sect" id="direct" aria-labelledby="direct-titre">
  <div class="head shead" data-rev>
    <p class="eyebrow"><i class="dot" aria-hidden="true"></i> En direct · Saint-Hyacinthe</p>
    <h2 id="direct-titre" data-split>Le ciel d’ici, en ce moment.<br><em>Et ce que JARVIS en ferait.</em></h2>
    <p>Données réelles d’Environnement Canada. Les gestes que JARVIS propose sont simulés.</p>
  </div>
  {meteo.html()}
</section>

<!-- Comment ça marche -->
<section class="how" id="fonctionnement" aria-labelledby="how-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Comment ça marche</p>
    <h2 id="how-titre" data-split>Domotique, sécurité et IA.<br><em>Un seul système, chez vous.</em></h2>
    <p>Tout passe par le JARVIS Hub, un petit serveur installé chez vous. Aucun abonnement au nuage
    n’est nécessaire pour que tout fonctionne.</p>
  </div>

  <div class="flow" data-rev>
    <svg class="flow-svg" viewBox="0 0 1000 420" aria-hidden="true">
      <defs>
        <linearGradient id="fl2" gradientUnits="userSpaceOnUse" x1="600" y1="0" x2="790" y2="0"><stop offset="0" stop-color="currentColor" stop-opacity=".7"/><stop offset="1" stop-color="currentColor" stop-opacity=".25"/></linearGradient>
        <linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".05"/><stop offset=".5" stop-color="currentColor" stop-opacity=".55"/><stop offset="1" stop-color="currentColor" stop-opacity=".05"/></linearGradient>
      </defs>
      <g class="flow-lines" fill="none" stroke="url(#fl)" stroke-width="1.4">
        <path id="p1" d="M210 50 C 360 50, 380 210, 500 210"/>
        <path id="p2" d="M210 120 C 360 120, 380 210, 500 210"/>
        <path id="p3" d="M210 190 C 360 190, 400 210, 500 210"/>
        <path id="p4" d="M210 260 C 360 260, 400 210, 500 210"/>
        <path id="p5" d="M210 330 C 360 330, 380 210, 500 210"/>
        <path id="p6" d="M210 395 C 360 395, 380 210, 500 210"/>
        <path id="p7" d="M500 210 C 640 210, 660 210, 790 210" stroke="url(#fl2)"/>
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
      <p>Vos appareils, vos outils et ce qui vous fait perdre du temps.</p></li>
    <li data-rev><i>02</i><h3>Une première preuve utile</h3>
      <p>Un cas concret qui fonctionne chez vous, par exemple une alerte caméra qui dit vraiment ce qui se passe.</p></li>
    <li data-rev><i>03</i><h3>On élargit à votre rythme</h3>
      <p>On ajoute une extension à la fois, avec des droits précis pour chaque personne.</p></li>
  </ol>

  <nav class="how-go" aria-label="En savoir plus sur JARVIS" data-rev>
    <a href="/plateforme/#hub"><small>Le Hub</small><b>Le boîtier chez vous, et ce qu’il contient</b><i aria-hidden="true">→</i></a>
    <a href="/plateforme/#ia"><small>L’IA</small><b>Elle propose, vous approuvez</b><i aria-hidden="true">→</i></a>
    <a href="/plateforme/#ensemble"><small>Ensemble</small><b>Comment les extensions se parlent</b><i aria-hidden="true">→</i></a>
    <a href="/vision-roadmap/#feuille-de-route"><small>Où en est JARVIS</small><b>Ce qui existe, ce qui se construit</b><i aria-hidden="true">→</i></a>
  </nav>

  <div class="marquee" aria-label="Standards ouverts sur lesquels JARVIS s’appuie">
    <p class="marquee-k">Conçu pour s’appuyer sur des standards ouverts</p>
    <div class="marquee-track"><div>{MARQUEE}</div><div aria-hidden="true">{MARQUEE}</div></div>
  </div>
</section>

<!-- L'offre : le Hub, puis les extensions utiles à chaque environnement (détail : /plateforme/#offre) -->
{galerie.accueil_panorama()}

<section class="offer" id="offre" aria-labelledby="offre-titre">
  <div class="head" data-rev>
    <p class="eyebrow">L’offre</p>
    <h2 id="offre-titre">Le Hub, puis <em>vos extensions.</em></h2>
    <p>Chaque installation part du Hub. On ajoute les extensions utiles à votre lieu, avec
    l’installation, l’entretien et le soutien.</p>
  </div>
  <div class="plans">
    {offre_plans()}
  </div>
  <p class="sol-all" data-rev><a class="pill" href="/plateforme/#offre">Voir l’offre en détail</a>
  <a class="pill ghost" href="/contact/">Réserver une démo</a></p>
  <p class="offer-note" data-rev>JARVIS est en construction : la démo montre honnêtement ce qui
  fonctionne aujourd’hui.</p>
</section>

<!-- Laboratoire (preuve) -->
<section class="band">
  <div class="bg"><img src="/media/ambulance/ambulance-garage-lab-v1.webp"
       alt="Laboratoire mobile JARVIS — ambulance Ford 2017 dans le garage" loading="lazy"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev><i class="dot ld-dot" aria-hidden="true"></i> Laboratoire mobile · en direct</p>
    <h2 data-rev>Le système sort<br><em>de l’écran.</em></h2>
    <p class="ld-lead" data-rev>Une ambulance Ford 2017 devenue laboratoire. Ses deux batteries sont
    lues par Home Assistant et affichées ici, en direct.</p>
    <div class="specs ld" data-labdirect data-rev>
      <div class="ld-bat"><b><span data-ld="a">--</span><i>%</i></b><small>Batterie A</small></div>
      <div class="ld-bat"><b><span data-ld="b">--</span><i>%</i></b><small>Batterie B</small></div>
      <div><b><span data-ld="kwh">560</span><i data-ld="unit">Ah</i></b><small data-ld="kwh-l">Capacité</small></div>
      <div><b><span data-n="500">500</span><i>W</i></b><small>Solaire</small></div>
    </div>
    <p class="ld-state" data-ld="state" data-rev>Connexion aux batteries…</p>
    <p data-rev style="margin:0 0 3rem"><a class="pill ghost" href="/laboratoire-mobile/">Voir le laboratoire en direct</a></p>
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
  <p data-rev>Une rencontre, vos besoins réels, et ce qui fonctionne déjà aujourd’hui.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/" data-magnet>Réserver une démo</a></div>
</section>
""",
}
