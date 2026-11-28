# Solution 07 — Mobilité (extension « Mobilité » de JARVIS App).
# Règle convenue avec James : Environnements = le lieu où l'on vit ou travaille (la cellule du VR :
# lumières, eau, énergie); Mobilité = le mouvement : le trajet, le voyage, le véhicule. Un VR a donc
# les deux; une voiture familiale, une voiture de collection ou un vélo électrique va dans Mobilité.
# Page sur mesure (comme Environnements) : la numérotation « 07 / 07 » et les sections propres au
# voyage ne rentrent pas dans le gabarit commun. Démo : src/demos/mobilite.py.

from demos import coquille, mobilite
from pages._solution import clair_section, fiche_section, avec_bande
import galerie

HERO = mobilite.photo("hero", "/media/vr/exterieur.webp")

# « En clair », bâti comme l'offre (voir pages/_solution.py, clair_section). Mobilité = tous les
# véhicules (auto, camion, moto, VÉ, VR, bateau, avion), pas seulement le VR.
CLAIR = {
    "titre": "Tout ce qui roule, flotte ou vole. <em>Sous votre œil.</em>",
    "quoi": "Auto, camion, moto, VR, bateau ou avion. Vol, panne et route, sous votre œil.",
    "moments": [
        ("6 h 00", "−25 °C dehors."),
        ("6 h 00", "Un pneu perd de la pression."),
        ("6 h 05", "JARVIS propose de préchauffer l’auto."),
    ],
    "message": "Pneu avant gauche en baisse. Je préchauffe l’auto pour 6 h 30?",
    "duel": ("Plus qu’un traceur GPS.", "Un traceur ou l’application du constructeur", [
        ("Une application par véhicule.", "Tous vos véhicules, une application."),
        ("Où il est, une fois volé.", "Une alerte dès qu’il bouge sans vous."),
        ("Un voyant, sans explication.", "Le problème, en mots simples."),
        ("Le VR oublié tout l’hiver.", "Suivi à distance, même entreposé."),
    ]),
    "capacites": [
        ("Tous vos véhicules", "Auto, camion, moto, VR, bateau, avion."),
        ("Vol et position", "Alerte et position en direct."),
        ("La santé du véhicule", "Codes, batterie, pneus, entretien."),
        ("Le véhicule électrique", "Recharge au meilleur moment."),
        ("Le copilote de route", "Le bon arrêt, ouvert à votre arrivée."),
        ("VR et bateau", "Batteries, eau et propane, de partout."),
    ],
    "equipement": ("L’équipement", [
        "Connexion du constructeur, quand le véhicule l’offre", "Boîtier Mobilité sur la prise de diagnostic",
        "Boîtier VR pour VR, roulotte et bateau"], ""),
}

POUR = "Autos, camions, motos, véhicules électriques, VR, bateaux et avions · flottes d’entreprise"

PAGE = {
    "url": "/solutions/mobilite/",
    "v2": True,
    "title": "Mobilité : tous vos véhicules sous votre œil | JARVIS",
    "description": "Un guide de voyage qui propose destinations et itinéraires, un copilote de route qui propose repas, eau, propane, entretien et sites à voir selon la "
                   "distance, les heures d’ouverture et le soleil, un journal de voyage sur la carte et un garage "
                   "connecté pour VR, voitures familiales, voitures de collection et vélos électriques.",
    "og_image": HERO,
    "assets": ["coquille", "mobilite", "galerie"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="{HERO}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution 07 / 07 · Mobilité</p>
    <h1 data-rev>VR et véhicules connectés. <em>Partez l’esprit libre.</em></h1>
    <p class="lead" data-rev>Vous roulez; JARVIS regarde la route, le véhicule et l’heure, et vous propose
    le bon arrêt au bon moment. Chaque voyage reste ensuite sur la carte, photos comprises.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="#jarvis">Prendre la route</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> VR · voitures familiales · voitures de collection · vélos électriques</p>
    <p class="for-line" data-rev><span>Prix</span> 15 $ par mois par véhicule, données cellulaires comprises · <a href="/offre/#solutions" style="color:var(--gold-soft)">Ajouter au panier</a></p>
  </div>
</section>

{clair_section(CLAIR, "mobilite")}

<section class="sect sol-demo" id="essayer" data-toc="Essayer">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez · démonstration interactive</p>
      <h2>Vous conduisez. <em>Le copilote s’occupe du reste.</em></h2>
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
      <p>Guide de voyage, copilote de route, modes de voyage, journal sur la carte, état mécanique et commandes du véhicule,
      du VR à la voiture de collection.</p>
    </article>
    <article class="card" data-rev>
      <small>Ensemble</small>
      <h3>Ils se parlent, sans doublon.</h3>
      <p>Le niveau d’eau de la cellule alimente le copilote; l’arrêt accepté prépare la cellule
      (chauffage, éclairage d’arrivée). Une seule application, deux rôles clairs.</p>
    </article>
  </div>
</section>

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
      <h2>De la familiale à la collection. <em>Chaque véhicule, selon ce qu’il offre.</em></h2>
    </div>
    <p data-rev>Un véhicule qui a une connexion officielle du constructeur se contrôle par elle : préchauffage,
    recharge, verrouillage, surveillance. Une voiture sans application reçoit le boîtier JARVIS de base, branché
    au port OBD-II : position, état, pression des pneus, codes défaut, mode garage et géorepérage.</p>
  </div>
  <div class="cards" style="margin-top:2.6rem">
    <article class="card" data-rev><small>Connexion du constructeur</small><h3>Rien d’inventé.</h3>
      <p>JARVIS utilise seulement ce que le constructeur autorise. Si une commande n’existe pas, elle n’apparaît pas.</p></article>
    <article class="card" data-rev><small>Boîtier JARVIS de base</small><h3>OBD-II + GPS + batterie.</h3>
      <p>Pour toute voiture depuis 1996, de la familiale à la supercar sans application : il se branche sous le tableau de bord et reste discret.</p></article>
    <article class="card" data-rev><small>Confirmation</small><h3>Vous gardez la main.</h3>
      <p>Déverrouiller, chauffer, désarmer un antivol : chaque commande demande votre accord, puis l’état est relu.</p></article>
  </div>
</section>

{galerie.terrain("mobilite")}

{fiche_section(CLAIR, "mobilite", POUR)}
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
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}

PAGE["content"] = avec_bande(PAGE["content"], "mobilite", "Mobilité", CLAIR, HERO)

