# Accueil — vendre JARVIS, le logiciel (refonte « clarté », novembre 2026).
# Sept sections, une idée chacune : promesse (héros) → qu'est-ce qu'il vous faut (besoins) →
# le logiciel en grand (aperçu vivant, démo complète sur /logiciel/) → pour qui (galerie) →
# l'offre en bref (détail sur /offre/) → FAQ → démo.
# Les sept extensions en cartes et les compositions d'exemple vivent sur /offre/.
# Les questions de la FAQ alimentent aussi les données structurées (FAQPage).

import json

from demos import app
import galerie
import parcours


FAQ = [
    (
        "Qu’est-ce que JARVIS, concrètement?",
        "La domotique privée, la sécurité privée et l’IA privée réunies dans un seul système, "
        "installé chez vous dans un petit boîtier silencieux, le JARVIS Hub (un par lieu, entretenu par nous). Il relie ce que vous avez déjà — "
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
    "assets": ["app", "galerie", "parcours", "logiciel"],
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
        <a class="pill" href="/logiciel/" data-magnet>Essayer le logiciel</a>
        <a class="pill ghost" href="/contact/" data-magnet>Réserver une démo</a>
        <a class="pill ghost" href="/contact/" data-jarvis data-magnet>Parler à JARVIS</a>
      </div>
      <a class="live-pill" href="#logiciel" data-live-pill>
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

<!-- Qu'est-ce qu'il vous faut? Une carte par besoin, chacune mène à sa solution -->
{parcours.besoins()}

<!-- Le logiciel en grand : l'écran d'accueil vivant, non interactif; la démo complète sur /logiciel/ -->
<section class="lg-apercu" id="logiciel" aria-labelledby="logiciel-titre">
  <div class="lga-head" data-rev>
    <div>
      <p class="eyebrow">Le logiciel · JARVIS App</p>
      <h2 id="logiciel-titre">Une seule application.<br><em>Toute votre vie connectée.</em></h2>
    </div>
    <div class="lga-side">
      <p>Voici l’écran d’accueil de JARVIS, en direct : l’heure et la météo sont réelles. Assistant,
      messages, appels, carte de vos lieux et extensions vous attendent dans la démo complète.</p>
      <a class="pill" href="/logiciel/" data-magnet>Essayer le logiciel</a>
    </div>
  </div>
  <div class="lga-frame">
    <div class="lga-dev" inert>{app.apercu()}</div>
    <a class="lga-hit" href="/logiciel/"><span>Essayer le logiciel <i aria-hidden="true">→</i></span></a>
  </div>
</section>

<!-- Pour qui : clients ordinaires et de prestige (src/galerie.py) -->
{galerie.clients_fr()}

<!-- L'offre en bref : trois étapes, le détail sur /offre/ -->
{parcours.offre_bref()}

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
