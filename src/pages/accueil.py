# Accueil — vendre JARVIS, le logiciel (refonte « clarté », novembre 2026).
# Sept sections, une idée chacune : promesse (héros) → qu'est-ce qu'il vous faut (besoins) →
# le logiciel en grand (aperçu vivant, démo complète sur /logiciel/) → pour qui (galerie) →
# l'offre en bref (détail sur /offre/) → FAQ → démo.
# Les sept extensions en cartes et les compositions d'exemple vivent sur /offre/.
# Les questions de la FAQ alimentent aussi les données structurées (FAQPage).

from demos import app
import galerie
import parcours
import pro


FAQ = [
    (
        "Que fait JARVIS Private Systems, concrètement?",
        "JARVIS Private Systems est un intégrateur de systèmes intelligents. On installe et on relie, "
        "dans un seul système, ce qui rend un lieu intelligent et sécurisé : la domotique, le réseau, "
        "les caméras et serrures connectées, et une IA privée. Tout passe par un petit boîtier "
        "silencieux installé chez vous, le JARVIS Hub, et par une seule application. Le système "
        "propose des actions; vous gardez la décision.",
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
        "L’entreprise est en phase de lancement : nous prenons les noms des personnes intéressées "
        "et choisissons quelques premiers projets. Le logiciel JARVIS est en construction : son "
        "noyau (comptes, droits, sécurité) est en développement et le tableau JARVIS Signature "
        "fonctionne déjà sur Home Assistant. Le prix dépend de votre lieu et de ce qu’on relie; "
        "il est toujours remis par écrit, après une visite gratuite.",
    ),
    (
        "Quelles régions desservez-vous?",
        "JARVIS Private Systems est basé dans la région de Saint-Hyacinthe et se déplace en "
        "Montérégie et aux environs : Saint-Hyacinthe, Granby, Drummondville, Longueuil et la "
        "Rive-Sud, Saint-Jean-sur-Richelieu, Sorel-Tracy, Beloeil, Mont-Saint-Hilaire et Acton Vale. "
        "Maisons, fermes, entreprises et véhicules aménagés.",
    ),
]

FAQ_HTML = pro.faq_items(FAQ)

PAGE = {
    "url": "/",
    "v2": True,
    "title": "JARVIS Private Systems | Intégrateur de systèmes intelligents",
    "schema": [pro.ld_entreprise(), pro.ld_site(), pro.ld_faq(FAQ)],
    "assets": ["app", "galerie", "parcours", "logiciel"],
    "description": (
        "Maisons, fermes, entreprises et véhicules intelligents et sécurisés, en Montérégie. "
        "Domotique, réseau et IA privée dans un seul système. Saint-Hyacinthe."
    ),
    "content": f"""
<!-- Héros : la maison s'allume, JARVIS prend la parole -->
<section class="hero" data-hero>
  <div class="bg" data-hero-bg>
    <img class="dark" src="/media/concept/jarvis-hero-architecture-v1.webp" width="1916" height="821" alt="" aria-hidden="true" fetchpriority="high">
    <img class="lit" src="/media/concept/jarvis-hero-architecture-v1.webp" width="1916" height="821"
         alt="Résidence contemporaine la nuit, éclairée par son système intelligent JARVIS">
  </div>
  <div class="hero-flash" aria-hidden="true"></div>
  <div class="hero-inner">
    <div class="hero-copy">
      <p class="eyebrow hero-eyebrow">Intégrateur de systèmes intelligents · Montérégie</p>
      <h1><span class="ln">Des lieux intelligents</span><span class="ln l2">et sécurisés.</span></h1>
      <p class="sub"><strong>Maisons, fermes, entreprises et véhicules intelligents et sécurisés, en
      Montérégie.</strong> On installe chez vous un seul système qui réunit la domotique, le réseau, les
      caméras et une IA privée. Il s’occupe de ce qui se répète; vous gardez les décisions.</p>
      <div class="acts">
        <a class="pill" href="/contact/" data-magnet>Parlons de votre projet</a>
        <a class="pill ghost" href="/logiciel/" data-magnet>Voir le logiciel</a>
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

<!-- Un seul système : les pièces d'une même installation -->
{pro.un_systeme(toc="", alt=True).replace(' data-toc=""', '')}

<!-- Questions fréquentes -->
<section class="faq" id="questions" aria-labelledby="faq-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Questions fréquentes · Saint-Hyacinthe, Montérégie</p>
    <h2 id="faq-titre">Domotique, réseau, caméras et IA privée : <em>vos questions.</em></h2>
    <p class="faq-more"><a href="/questions/">Toutes les questions avant d’appeler <i aria-hidden="true">→</i></a></p>
  </div>
  <div class="faq-list">{FAQ_HTML}</div>
</section>

<!-- Appel -->
<section class="cta" id="demo">
  <h2 data-rev>Voyez JARVIS<br><span>de vos yeux.</span></h2>
  <p data-rev>Vos besoins réels, et ce qui fonctionne déjà aujourd’hui. Sans pression.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/" data-magnet>Parlons de votre projet</a>
  <a class="pill ghost" href="/regions/">Régions desservies</a></div>
</section>
""",
}
