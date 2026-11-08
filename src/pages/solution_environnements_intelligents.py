# Solution 01 — Environnements intelligents. PAGE VEDETTE (sur mesure).
# Seule page de solution hors gabarit : la démo « Environnements » (un seul modèle de logiciel
# pour BouLance, résidence, chalet, entreprise, garage de collection, ferme, yacht et avion, dans JARVIS App),
# journée interactive et caméras. Données de la démo : src/demos/env.py.

import json

from demos import coquille, env
from pages._solution import clair_section

MOMENTS = {
    "matin": {
        "time": "06 H 58 · MATIN",
        "title": "La maison se réveille avant vous.",
        "copy": "L’éclairage de la chambre monte en douceur, la salle de bain gagne deux degrés et la cuisine prépare l’ambiance du déjeuner — selon la règle que vous avez choisie.",
        "l1": "Présence", "v1": "Chambre",
        "l2": "Salle de bain", "v2": "23 °C atteints",
        "l3": "Décision", "v3": "Règle approuvée par vous",
    },
    "depart": {
        "time": "08 H 12 · DÉPART",
        "title": "Vous partez. Tout se met en veille.",
        "copy": "Thermostats en mode économie, prises non essentielles coupées, périmètre armé. La maison cesse de dépenser dès que plus personne n’en profite.",
        "l1": "Présence", "v1": "Absence confirmée",
        "l2": "Énergie", "v2": "Consommation −38 %",
        "l3": "Sécurité", "v3": "Périmètre armé",
    },
    "retour": {
        "time": "17 H 26 · RETOUR",
        "title": "Retour prévu dans 32 minutes.",
        "copy": "La maison peut préparer l’éclairage d’arrivée, remonter la température de confort et reporter la recharge du véhicule après 21 h. Elle propose — vous approuvez.",
        "l1": "Retour estimé", "v1": "32 minutes",
        "l2": "Confort", "v2": "En préparation",
        "l3": "Décision", "v3": "Votre accord",
    },
    "soiree": {
        "time": "19 H 40 · SOIRÉE",
        "title": "Mode cinéma, sans y penser.",
        "copy": "Les lumières se tamisent, les stores descendent et les notifications deviennent discrètes. Un seul geste pour reprendre la main — toujours.",
        "l1": "Scène", "v1": "Cinéma",
        "l2": "Notifications", "v2": "Discrètes",
        "l3": "Reprise manuelle", "v3": "Un geste",
    },
    "nuit": {
        "time": "23 H 05 · NUIT",
        "title": "La maison veille. Vous dormez.",
        "copy": "Tout s’éteint, les portes sont vérifiées, le périmètre reste attentif. Vous n’êtes réveillé que si quelque chose compte vraiment.",
        "l1": "Portes", "v1": "Verrouillées",
        "l2": "Périmètre", "v2": "Calme",
        "l3": "Prochain réveil", "v3": "06 h 58",
    },
}

MOMENTS_JSON = json.dumps(MOMENTS, ensure_ascii=False)

# « En clair » : la solution expliquée simplement (avant / avec JARVIS).
CLAIR = {'quoi': 'JARVIS réunit les lumières, le chauffage, les portes et l’énergie de votre maison '
         '<em>dans une seule application simple.</em>',
 'exemple': 'Le soir, vous touchez « Soirée » : le salon passe à 60 %, la terrasse et la piscine '
            's’allument, le foyer démarre et le chauffage des chambres baisse. Une seule touche au '
            'lieu de cinq applications.',
 'avant': ['Une application par marque d’appareil',
           'Des automatisations que personne ne comprend',
           'Rien ne marche quand Internet tombe',
           'Aucune idée de ce qui consomme'],
 'apres': ['Toute la maison sur un seul écran',
           'Des ambiances claires, que vous approuvez',
           'Tout fonctionne en local, même sans Internet',
           'La consommation affichée pièce par pièce'],
 'obtenez': [('Un écran pour tout',
              'Lumières, chauffage, stores, verrous et énergie, pièce par pièce, sur téléphone, '
              'tablette ou ordinateur.'),
             ('Des ambiances en une touche',
              'Matin, Soirée, Cinéma, Nuit, Absent : chaque ambiance est réglée avec vous et reste '
              'modifiable.'),
             ('Le contrôle reste humain',
              'Les actions sensibles, comme déverrouiller ou ouvrir le garage, demandent toujours '
              'votre confirmation.')]}

PAGE = {
    "url": "/solutions/environnements-intelligents/",
    "v2": True,
    "title": "Environnements intelligents | Solutions JARVIS",
    "description": "Faire travailler ensemble les technologies d’un lieu, sans rendre son utilisation compliquée.",
    "og_image": "/media/solutions/environnements-intelligents.webp",
    "assets": ["coquille", "lumieres", "env"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/environnements-intelligents.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution 01 / 07</p>
    <h1 data-rev>Environnements <em>intelligents.</em></h1>
    <p class="lead" data-rev>Un environnement qui comprend son état, s’adapte au contexte et
    demeure contrôlable simplement.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="#journee">Vivre une journée</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> Maisons familiales · résidences de prestige · fermes · entreprises · yachts · hangars</p>
  </div>
</section>

<section class="sect sol-demo" id="essayer" data-toc="Essayer">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez · démonstration interactive</p>
      <h2>Un seul logiciel. <em>Tous vos lieux.</em></h2>
    </div>
    <p data-rev>L’accueil réunit tous vos lieux : alertes, sécurité, énergie, présence et entretien
    d’un seul regard, un mode appliqué à plusieurs lieux et un journal commun. Puis chaque tableau
    (BouLance, résidence de prestige, chalet d’architecte, bureau, garage de collection, ferme
    multi-élevage, yacht, avion d’affaires) garde les mêmes gestes.
    Chaque commande est envoyée, puis confirmée. Les batteries de BouLance sont réelles.</p>
  </div>
  {coquille.html("environnements-intelligents", env.html())}
</section>

<section class="sect alt" id="eclairage" data-toc="Éclairage">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Module Éclairage · concept en conception</p>
      <h2>La lumière qui comprend <em>le moment.</em></h2>
    </div>
    <p data-rev>« Bonsoir, James. Installez-vous. La soirée est à vous. » Chaque pièce, chaque
    ambiance, chaque nuance — pensées pour être belles ET honnêtes.</p>
  </div>
  <div class="cards" style="margin-top:2.6rem">
    <article class="card" data-rev>
      <small>Règle 01</small>
      <h3>Un aperçu n’envoie rien.</h3>
      <p>Composer un éclairage crée un brouillon : rien ne change dans la pièce avant que
      vous appliquiez. Les lumières éteintes le restent.</p>
    </article>
    <article class="card" data-rev>
      <small>Règle 02</small>
      <h3>Votre précédent est protégé.</h3>
      <p>Avant chaque application, l’éclairage en place est sauvegardé. Vous pouvez toujours
      revenir — même après avoir fermé JARVIS.</p>
    </article>
    <article class="card" data-rev>
      <small>Règle 03</small>
      <h3>Jamais de faux succès.</h3>
      <p>Une lumière qui ne répond pas est annoncée « à vérifier », pas « réglée ». Chaque
      état affiché vient d’une confirmation réelle.</p>
    </article>
  </div>
</section>

{clair_section(CLAIR)}

<section class="sect alt" id="journee" data-toc="Une journée">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Un exemple vécu</p>
      <h2>Une journée où tout <em>se tient.</em></h2>
    </div>
    <p data-rev>Choisissez un moment : la maison réagit au contexte, pas à une suite de
    commandes. Scénario illustratif — données simulées.</p>
  </div>
  <div class="moments" data-rev data-swap-group="moments-data" data-swap-scope="#journee">
    <div class="mom-btns" role="group" aria-label="Choisir un moment de la journée">
      <button type="button" class="is-on" aria-pressed="true" data-swap="matin">Matin</button>
      <button type="button" aria-pressed="false" data-swap="depart">Départ</button>
      <button type="button" aria-pressed="false" data-swap="retour">Retour</button>
      <button type="button" aria-pressed="false" data-swap="soiree">Soirée</button>
      <button type="button" aria-pressed="false" data-swap="nuit">Nuit</button>
    </div>
    <article class="mom-card">
      <div class="mom-left">
        <time data-swap-field="time">06 H 58 · MATIN</time>
        <h3 data-swap-field="title">La maison se réveille avant vous.</h3>
        <p data-swap-field="copy">L’éclairage de la chambre monte en douceur, la salle de bain
        gagne deux degrés et la cuisine prépare l’ambiance du déjeuner — selon la règle que
        vous avez choisie.</p>
        <ul class="mom-sig">
          <li><span data-swap-field="l1">Présence</span><b data-swap-field="v1">Chambre</b></li>
          <li><span data-swap-field="l2">Salle de bain</span><b data-swap-field="v2">23 °C atteints</b></li>
          <li><span data-swap-field="l3">Décision</span><b data-swap-field="v3">Règle approuvée par vous</b></li>
        </ul>
      </div>
      <figure class="mom-media" style="margin:0">
        <img src="/media/concept/jarvis-hero-architecture-v1.webp"
             alt="Résidence contemporaine coordonnée par JARVIS" loading="lazy">
      </figure>
    </article>
    <script type="application/json" id="moments-data">{MOMENTS_JSON}</script>
  </div>
</section>

<section class="sect" id="cameras" data-toc="Caméras">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Caméras de la propriété · données simulées</p>
      <h2>Toute la propriété. <em>Une seule expérience.</em></h2>
    </div>
    <p data-rev>Les caméras rejoignent le même écran que les lumières et le chauffage.
    Chaque commande reste visible, compréhensible et réversible.</p>
  </div>
  <div class="shots" data-rev style="margin-top:14px">
    <figure>
      <img src="/media/solutions/camera-front-entry-v1.webp" alt="Caméra de l’entrée avant de la résidence" loading="lazy">
      <figcaption><b>Entrée avant</b><span>Aucun événement à vérifier</span></figcaption>
    </figure>
    <figure>
      <img src="/media/solutions/camera-driveway-garage-v1.webp" alt="Caméra de l’allée et des portes de garage" loading="lazy">
      <figcaption><b>Allée et garage</b><span>Portes fermées</span></figcaption>
    </figure>
    <figure>
      <img src="/media/solutions/camera-rear-terrace-v1.webp" alt="Caméra de la terrasse arrière et du foyer" loading="lazy">
      <figcaption><b>Terrasse arrière</b><span>Accès fermé · foyer actif</span></figcaption>
    </figure>
  </div>
</section>

<section class="sect sol-trust" id="deploiement" data-toc="Déploiement">
  <div class="trust" data-rev>
    <div>
      <p class="eyebrow">Déploiement responsable</p>
      <h2>Les fonctions essentielles restent dans le lieu.</h2>
      <p>Les commandes essentielles, les règles et l’historique récent peuvent demeurer
      sur place. Les services infonuagiques restent optionnels et clairement identifiés.</p>
    </div>
    <dl>
      <div><dt>Accord humain</dt><dd>Les actions sensibles exigent une validation adaptée au risque.</dd></div>
      <div><dt>Limite publiée</dt><dd>JARVIS n’invente pas une nouvelle plateforme domotique. Il relie des systèmes
      compatibles, documentés et autorisés. Chaque installation exige une analyse technique.</dd></div>
      <div><dt>Compatibilités possibles</dt><dd class="chips"><span class="chip">Home Assistant</span><span class="chip">Matter</span><span class="chip">Zigbee</span><span class="chip">Z-Wave</span><span class="chip">KNX</span><span class="chip">ESPHome</span><span class="chip">Modbus</span><span class="chip">MQTT</span></dd></div>
    </dl>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Quel lieu mérite enfin de fonctionner<br><span>comme un ensemble?</span></h2>
  <p data-rev>Décrivez les appareils déjà en place, les irritants quotidiens et ce qui doit
  continuer de fonctionner même sans Internet.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
