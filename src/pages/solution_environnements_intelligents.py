# Solution 01 — Environnements intelligents.

from pages._solution import solution_page

SHOWCASE = """
<figure class="showcase-frame" data-reveal>
  <img src="/media/solutions/jarvis-spaces-property-v3.webp"
       alt="Plan en trois dimensions d’une propriété intelligente avec résidence, terrasse, piscine et garage"
       loading="lazy">
  <figcaption>
    <span>JARVIS APP · RÉSIDENCE</span>
    <strong>Toute la propriété. Une seule expérience.</strong>
  </figcaption>
</figure>
<div class="cam-grid" data-reveal>
  <figure>
    <img src="/media/solutions/camera-front-entry-v1.webp" alt="Caméra de l’entrée avant de la résidence" loading="lazy">
    <figcaption><b>Entrée avant</b><span>Aucun événement à vérifier</span></figcaption>
  </figure>
  <figure>
    <img src="/media/solutions/camera-driveway-garage-v1.webp" alt="Caméra de l’allée et des portes de garage" loading="lazy">
    <figcaption><b>Allée et garage</b><span>Portes fermées</span></figcaption>
  </figure>
  <figure>
    <img src="/media/solutions/camera-garage-supercars-v1.webp" alt="Caméra intérieure du garage" loading="lazy">
    <figcaption><b>Garage intérieur</b><span>2 véhicules autorisés</span></figcaption>
  </figure>
  <figure>
    <img src="/media/solutions/camera-rear-terrace-v1.webp" alt="Caméra de la terrasse arrière et du foyer" loading="lazy">
    <figcaption><b>Terrasse arrière</b><span>Accès fermé · foyer actif</span></figcaption>
  </figure>
  <figure>
    <img src="/media/solutions/camera-pool-spa-v1.webp" alt="Caméra de la piscine et du spa" loading="lazy">
    <figcaption><b>Piscine et spa</b><span>Périmètre calme</span></figcaption>
  </figure>
  <aside class="console cam-grid-console">
    <header class="console-head"><span><i></i>JARVIS · ACTIF</span><small>LOCAL</small></header>
    <div class="console-body">
      <small>RECOMMANDATION</small>
      <strong>Reporter la recharge du véhicule après 21 h.</strong>
      <p>La capacité disponible sera plus favorable et les usages de confort resteront prioritaires.</p>
    </div>
    <ul class="console-signals">
      <li><span>SOLAIRE</span><b>1,7 kW</b></li>
      <li><span>MAISON</span><b>4,2 kW</b></li>
      <li><span>BATTERIE</span><b>74 %</b></li>
    </ul>
  </aside>
</div>
"""

DATA = {
    "slug": "environnements-intelligents",
    "title": "Environnements intelligents",
    "description": "Faire travailler ensemble les technologies d’un lieu, sans rendre son utilisation compliquée.",
    "image": "/media/solutions/environnements-intelligents.webp",
    "h1": "Environnements <em>intelligents.</em>",
    "lead": "Un environnement qui comprend son état, s’adapte au contexte et demeure contrôlable simplement.",
    "for": "Résidences, bâtiments, ateliers et véhicules aménagés",
    "problem_title": "Les appareils sont intelligents. <em>Le lieu, lui, reste fragmenté.</em>",
    "problem_copy": (
        "Éclairage, chauffage, énergie, accès, audio, capteurs et sécurité vivent dans des "
        "applications séparées. JARVIS construit une couche commune qui les observe et les "
        "coordonne sans remplacer ce qui fonctionne déjà."
    ),
    "change_title": "Votre lieu, réuni dans une expérience claire.",
    "change_copy": (
        "Le tableau de bord privilégie les états qui demandent une décision. "
        "Les protocoles et les intégrations restent en arrière-plan."
    ),
    "features": [
        ("Une seule lecture du lieu", "Voir les états importants, les anomalies et les actions possibles dans une expérience cohérente."),
        ("Des automatisations contextuelles", "Adapter le confort et l’énergie selon la présence, l’heure, la météo et les priorités choisies."),
        ("Un contrôle qui reste local", "Conserver les fonctions essentielles même lorsqu’Internet ou un service externe devient indisponible."),
        ("Des modes manuels clairs", "Chaque automatisation sensible peut être expliquée, suspendue ou reprise manuellement."),
        ("Un historique utile", "Comprendre ce qui s’est passé avant une anomalie plutôt que consulter une suite de journaux techniques."),
        ("Une base extensible", "Ajouter progressivement de nouveaux appareils sans reconstruire tout l’environnement."),
    ],
    "demo_title": "Toute la propriété. <em>Une seule expérience.</em>",
    "demo_copy": (
        "L’interface réunit les espaces, les ambiances, l’énergie et la sécurité. "
        "Chaque commande reste visible, compréhensible et réversible."
    ),
    "showcase": SHOWCASE,
    "compat": ["Home Assistant", "Matter", "Zigbee", "Z-Wave", "KNX", "ESPHome", "Modbus", "MQTT"],
    "deploy_title": "Les fonctions essentielles restent dans le lieu.",
    "deploy_copy": (
        "Les commandes essentielles, les règles et l’historique récent peuvent demeurer sur place. "
        "Les services infonuagiques restent optionnels et clairement identifiés."
    ),
    "limit": (
        "JARVIS n’invente pas une nouvelle plateforme domotique. Il relie des systèmes compatibles, "
        "documentés et autorisés. Chaque installation exige une analyse technique."
    ),
    "cta_title": "Quel lieu mérite enfin de fonctionner <em>comme un ensemble?</em>",
    "cta_copy": (
        "Décrivez les appareils déjà en place, les irritants quotidiens et ce qui doit "
        "continuer de fonctionner même sans Internet."
    ),
}

DATA["demo_image"] = "/media/solutions/jarvis-spaces-property-v3.webp"
DATA["demo_caption"] = "Toute la propriété. Une seule expérience. — Données simulées."
DATA["extra"] = """
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
"""

PAGE = solution_page(DATA)
