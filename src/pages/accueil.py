# Accueil — vendre JARVIS, le logiciel (allègement commercial, novembre 2026).
# Sept sections, une idée chacune : promesse (héros) → pour qui (galerie) → l'app → les sept
# extensions → l'offre → FAQ → démo. Les démonstrations « maison » (pièces, météo) vivent sur
# /solutions/environnements-intelligents/; le laboratoire, sur /laboratoire-mobile/.
# Les questions de la FAQ alimentent aussi les données structurées (FAQPage).

import json

from config import CAPABILITIES
from demos import app
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
        "La domotique privée, la sécurité privée et l’IA privée réunies dans un seul système, "
        "installé chez vous sur un petit serveur : le JARVIS Hub. Il relie ce que vous avez déjà — "
        "lumières, caméras, chauffage, batteries, agenda, documents — et vous le présente dans une "
        "seule application. Il propose des actions; vous gardez la décision.",
    ),
    (
        "Mes données quittent-elles la maison ou l’entreprise?",
        "Pas par défaut. Tout vit sur le Hub, chez vous, et aucun abonnement au nuage n’est "
        "nécessaire. L’interface et les automatisations continuent de fonctionner sans Internet; "
        "le nuage ne sert qu’à ce que vous choisissez, comme un accès à distance par un relais qui "
        "ne garde rien ou une copie de sauvegarde chiffrée.",
    ),
    (
        "Dois-je changer mes appareils?",
        "Généralement non. JARVIS s’appuie sur Home Assistant et sur des standards ouverts comme "
        "Zigbee, Z-Wave, Matter et MQTT pour parler à des appareils de marques différentes. On "
        "commence par ce qui existe déjà.",
    ),
    (
        "Est-ce disponible aujourd’hui, et combien ça coûte?",
        "JARVIS est en construction : le noyau du logiciel (comptes, droits, sécurité) est en "
        "développement et le tableau JARVIS Signature fonctionne déjà sur Home Assistant. Le prix "
        "dépend de votre lieu et de ce qu’on relie; on en parle après une première rencontre, "
        "qui montre honnêtement ce qui fonctionne déjà.",
    ),
    (
        "Où offrez-vous vos services au Québec?",
        "JARVIS Private Systems est basé dans la région de Saint-Hyacinthe, en Montérégie, au "
        "Québec. Résidences, entreprises et véhicules aménagés : écrivez-moi pour voir ce qui est "
        "possible chez vous.",
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

PAGE = {
    "url": "/",
    "v2": True,
    "title": "Domotique privée et sécurité intelligente au Québec | JARVIS",
    "assets": ["app", "galerie"],
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
      et vos informations. Il s’occupe de ce qui se répète; vous gardez les décisions. Une technologie qui rend libre,
      pas dépendant.</p>
      <div class="acts">
        <a class="pill" href="#app" data-magnet>Essayer l’app</a>
        <a class="pill ghost" href="/contact/" data-magnet>Réserver une démo</a>
      </div>
      <a class="live-pill" href="#app" data-live-pill>
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

<!-- L'offre : le Hub, puis les extensions utiles à chaque environnement (détail : /plateforme/#offre) -->
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

<!-- Questions fréquentes -->
<section class="faq" id="questions" aria-labelledby="faq-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Questions fréquentes · Saint-Hyacinthe, Québec</p>
    <h2 id="faq-titre">Domotique, sécurité et IA privées : <em>vos questions.</em></h2>
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
