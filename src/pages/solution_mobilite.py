# Solution 07 — Mobilité (extension « Mobilité » de JARVIS App).
# Règle convenue avec James : Environnements = le lieu où l'on vit ou travaille (la cellule du VR :
# lumières, eau, énergie); Mobilité = le mouvement : le trajet, le voyage, le véhicule. Un VR a donc
# les deux; une voiture électrique ou une sportive va dans Mobilité.
# Page sur mesure (comme Environnements) : la numérotation « 07 / 07 » et les sections propres au
# voyage ne rentrent pas dans le gabarit commun. Démo : src/demos/mobilite.py.

from demos import coquille, mobilite
from pages._solution import clair_section

HERO = mobilite.photo("hero", "/media/vr/exterieur.webp")

CLAIR = {
    "quoi": "JARVIS devient votre copilote : il regarde la route, l’heure, le soleil et l’état du véhicule, "
            "puis vous propose <em>le bon arrêt au bon moment.</em>",
    "exemple": "Vous roulez vers Charlevoix avec 22 % d’eau propre. JARVIS affiche : « Eau propre 22 % : "
               "remplissage gratuit à 12 km, détour de 2 minutes. » Plus loin : « Coucher de soleil à 16 h 42 : "
               "arrivez au belvédère avant 16 h 20. » Vous touchez « Accepter », l’arrêt s’ajoute à l’itinéraire. "
               "La photo prise là-bas se place toute seule sur la carte du voyage.",
    "avant": ["Trois applications de cartes, une pour la météo, une autre pour le camping",
              "On découvre que le restaurant est fermé en arrivant",
              "Le propane manque au pire endroit, loin de tout",
              "Les photos du voyage dorment dans le téléphone, sans lieu ni histoire"],
    "apres": ["Un seul copilote qui tient compte de tout, en même temps",
              "Seulement des arrêts ouverts à votre heure d’arrivée",
              "Eau, propane, carburant et entretien prévus avant d’en manquer",
              "Chaque voyage revit sur la carte, photos à leur place"],
    "obtenez": [("Un copilote de route", "Repas, eau, propane, Webasto, mécanique, soleil et sites historiques : "
                 "proposés selon la distance et l’ouverture, avec le détour exact."),
                ("Un journal automatique", "Photos et points géolocalisés en roulant. Touchez un voyage passé : "
                 "le tracé, les photos et les statistiques reviennent."),
                ("Un garage connecté", "VR, voiture électrique, sportive ou vélo électrique : ce que le véhicule "
                 "offre, et un boîtier JARVIS de base pour les autres.")],
}

PAGE = {
    "url": "/solutions/mobilite/",
    "v2": True,
    "title": "Copilote de voyage, VR et voiture connectés | JARVIS Mobilité",
    "description": "Un copilote de route qui propose repas, eau, propane, entretien et sites à voir selon la "
                   "distance, les heures d’ouverture et le soleil, un journal de voyage sur la carte et un garage "
                   "connecté pour VR, voitures et vélos électriques. Québec.",
    "og_image": HERO,
    "assets": ["coquille", "mobilite"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="{HERO}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution 07 / 07</p>
    <h1 data-rev>Mobilité. <em>Partez l’esprit libre.</em></h1>
    <p class="lead" data-rev>Vous roulez; JARVIS regarde la route, le véhicule et l’heure, et vous propose
    le bon arrêt au bon moment. Chaque voyage reste ensuite sur la carte, photos comprises.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="#jarvis">Prendre la route</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> VR · voitures électriques · sportives · vélos électriques</p>
  </div>
</section>

<section class="sect sol-demo" id="essayer" data-toc="Essayer">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez · démonstration interactive</p>
      <h2>Saint-Hyacinthe → Lac-Saint-Jean. <em>Le copilote s’occupe du reste.</em></h2>
    </div>
    <p data-rev>À droite, JARVIS propose des arrêts selon la distance, les heures d’ouverture, le soleil
    et l’état du véhicule. Acceptez-en un : il s’ajoute à la route.</p>
  </div>
  {coquille.html("mobilite", mobilite.HTML)}
</section>

<section class="sect alt mb-rule-s" id="lieu-ou-route" data-toc="Lieu ou route">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Environnements ou Mobilité?</p>
      <h2>Le lieu d’un côté. <em>Le mouvement de l’autre.</em></h2>
    </div>
    <p data-rev><b>Environnements</b> gère l’endroit où l’on vit ou travaille; <b>Mobilité</b> gère le
    trajet, le voyage et le véhicule. Un VR profite donc des deux; une voiture ou un vélo électrique vit
    dans Mobilité.</p>
  </div>
  <div class="cards" style="margin-top:2.6rem">
    <article class="card" data-rev>
      <small>Environnements</small>
      <h3>La cellule du VR, comme une maison.</h3>
      <p>Lumières, eau, énergie, chauffage et ambiances : tout ce qui rend l’intérieur agréable, à l’arrêt
      comme en route.</p>
      <p style="margin-top:1rem"><a class="pill ghost" href="/solutions/environnements-intelligents/#jarvis">Ouvrir Environnements</a></p>
    </article>
    <article class="card" data-rev>
      <small>Mobilité</small>
      <h3>La route, le voyage, le véhicule.</h3>
      <p>Copilote de route, modes de voyage, journal sur la carte, état mécanique et commandes du véhicule,
      du VR à la sportive.</p>
    </article>
    <article class="card" data-rev>
      <small>Ensemble</small>
      <h3>Ils se parlent, sans doublon.</h3>
      <p>Le niveau d’eau de la cellule alimente le copilote; l’arrêt accepté prépare la cellule
      (chauffage, éclairage d’arrivée). Une seule application, deux rôles clairs.</p>
    </article>
  </div>
</section>

{clair_section(CLAIR)}

<section class="sect" id="modes-voyage" data-toc="Six façons de voyager">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Six façons de voyager</p>
      <h2>Choisissez votre guide. <em>JARVIS s’adapte.</em></h2>
    </div>
    <p data-rev>Chaque mode est un guide qui connaît vos priorités. Le même trajet devient une route
    patrimoniale, gourmande, sauvage ou autonome, sans rien chercher vous-même.</p>
  </div>
  <div class="cards" style="margin-top:2.6rem">
    <article class="card" data-rev><small>Découverte</small><h3>Ne rien manquer.</h3>
      <p>Sites historiques à quelques kilomètres de la route, incontournables et belvédères, au bon moment.</p></article>
    <article class="card" data-rev><small>Efficace</small><h3>Arriver, simplement.</h3>
      <p>Le moins de détours possible : carburant, eau et pauses seulement là où c’est utile.</p></article>
    <article class="card" data-rev><small>Nature</small><h3>La lumière au bon endroit.</h3>
      <p>Sentiers, faune et couchers de soleil : JARVIS vous dit quand rouler pour arriver à l’heure.</p></article>
    <article class="card" data-rev><small>Gourmand</small><h3>Le terroir sur la route.</h3>
      <p>Producteurs, tables régionales et spécialités, ouverts à votre heure d’arrivée.</p></article>
    <article class="card" data-rev><small>Famille</small><h3>Des pauses qui comptent.</h3>
      <p>Parcs, toilettes propres et activités pour les enfants, toutes les deux heures environ.</p></article>
    <article class="card" data-rev><small>Hors réseau</small><h3>L’autonomie d’abord.</h3>
      <p>Eau, propane, nuits gratuites et zones sans cellulaire : cartes et musique téléchargées d’avance.</p></article>
  </div>
</section>

<section class="sect alt" id="garage" data-toc="Vos véhicules">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Garage connecté</p>
      <h2>Chaque véhicule, selon ce qu’il offre. <em>Les autres aussi.</em></h2>
    </div>
    <p data-rev>Un véhicule qui a une connexion officielle du constructeur se contrôle par elle : préchauffage,
    recharge, verrouillage, surveillance. Une voiture sans application reçoit le boîtier JARVIS de base, branché
    au port OBD-II : position, état, pression des pneus, codes défaut, mode garage et géorepérage.</p>
  </div>
  <div class="cards" style="margin-top:2.6rem">
    <article class="card" data-rev><small>Connexion du constructeur</small><h3>Rien d’inventé.</h3>
      <p>JARVIS utilise seulement ce que le constructeur autorise. Si une commande n’existe pas, elle n’apparaît pas.</p></article>
    <article class="card" data-rev><small>Boîtier JARVIS de base</small><h3>OBD-II + GPS + batterie.</h3>
      <p>Pour toute voiture depuis 1996 : il se branche sous le tableau de bord et reste discret.</p></article>
    <article class="card" data-rev><small>Confirmation</small><h3>Vous gardez la main.</h3>
      <p>Déverrouiller, chauffer, désarmer un antivol : chaque commande demande votre accord, puis l’état est relu.</p></article>
  </div>
</section>

<section class="sect sol-trust" id="deploiement" data-toc="Déploiement">
  <div class="trust" data-rev>
    <div>
      <p class="eyebrow">Déploiement responsable</p>
      <h2>Votre route vous appartient.</h2>
      <p>Les trajets, les positions et les photos restent sur votre JARVIS. Le partage de position est
      désactivé par défaut et se donne, au besoin, pour une durée précise.</p>
    </div>
    <dl>
      <div><dt>Accord humain</dt><dd>Aucun arrêt ajouté, aucune commande envoyée sans votre « Accepter » ou « Confirmer ».</dd></div>
      <div><dt>Limite publiée</dt><dd>JARVIS ne conduit pas et ne remplace pas votre attention au volant. Les
      suggestions s’affichent pour le passager ou à l’arrêt; en conduite, elles sont lues brièvement. Les heures
      d’ouverture viennent de sources publiques et peuvent changer.</dd></div>
      <div><dt>Compatibilités possibles</dt><dd class="chips"><span class="chip">OBD-II</span><span class="chip">GPS</span>
      <span class="chip">Connexions de constructeurs</span><span class="chip">Home Assistant</span><span class="chip">Victron</span>
      <span class="chip">Webasto</span><span class="chip">Capteurs de réservoirs</span><span class="chip">Traceurs LTE</span></dd></div>
    </dl>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Où partez-vous<br><span>la prochaine fois?</span></h2>
  <p data-rev>Décrivez vos véhicules et votre façon de voyager. Nous verrons ce que chacun peut offrir et ce que
  le boîtier JARVIS ajoute.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
