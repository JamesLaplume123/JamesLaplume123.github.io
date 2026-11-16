# Mentions légales et conditions d'utilisation du site.
# Seulement des faits vérifiables : responsable, courriel, nature de l'activité, état du projet.
# Aucun numéro d'entreprise, permis ou certification n'est indiqué tant qu'il n'existe pas :
# James complète cette page quand l'entreprise est immatriculée (voir la ligne « à compléter »).

import pro
from config import SITE

PAGE = {
    "url": "/mentions-legales/",
    "v2": True,
    "title": "Mentions légales et conditions d’utilisation | JARVIS",
    "description": (
        "Qui publie ce site, ce que fait JARVIS Private Systems et ce qu’elle ne fait pas, "
        "l’état du projet, la propriété des contenus et les conditions d’utilisation."
    ),
    "assets": ["pro"],
    "content": f"""
<section class="plain-top">
  {pro.fil("/mentions-legales/")}
  <p class="eyebrow" data-rev>Mentions légales</p>
  <h1 data-rev>Qui publie ce site,<br><em>et à quelles conditions.</em></h1>
  <p class="lead" data-rev>Des mentions courtes, en langage clair. Dernière mise à jour :
  15 novembre 2026.</p>
</section>

<section class="sect" style="padding-top:2rem" id="mentions" aria-label="Mentions légales">
  <div class="rows">
    <div class="row" data-rev>
      <i>01 · Éditeur</i>
      <div><h3>JARVIS Private Systems.</h3>
      <p>Ce site est publié par JARVIS Private Systems, entreprise en phase de lancement fondée par
      James Laplume et basée au Québec, Canada. Responsable de la
      publication : James Laplume. Pour nous joindre :
      <a href="mailto:{SITE['email']}" style="color:#fff">{SITE['email']}</a> ou le
      <a href="/contact/" style="color:#fff">formulaire de contact</a>.</p></div>
    </div>
    <div class="row" data-rev>
      <i>02 · Activité</i>
      <div><h3>Une entreprise de technologie et de sécurité.</h3>
      <p>JARVIS Private Systems conçoit et installe JARVIS, un système privé qui gère et protège des
      maisons, des fermes, des entreprises et des véhicules : domotique, réseau et cybersécurité,
      automatisation et IA privée. L’entreprise n’est pas une agence de sécurité, de gardiennage ou
      d’investigation, et n’offre aucun service de télésurveillance. Dans son nom, « Private » renvoie à la vie
      privée : les données du client restent chez lui.</p>
      <p>Au Québec, certaines activités, dont l’installation de systèmes d’alarme, de caméras de
      surveillance et de contrôles d’accès chez un client, sont encadrées par la Loi sur la sécurité
      privée. Lorsqu’un permis est requis, ces travaux doivent être faits par un titulaire de ce
      permis. Les travaux d’électricité relèvent d’un maître électricien.</p></div>
    </div>
    <div class="row" data-rev>
      <i>03 · État du projet</i>
      <div><h3>Un site de présentation, pas une offre ferme.</h3>
      <p>L’entreprise est en phase de lancement et le logiciel JARVIS est en construction. Les
      démonstrations du site utilisent des données d’exemple, clairement indiquées; plusieurs photos
      sont des illustrations. Les sections intitulées « vision »
      décrivent des intentions à long terme, pas des services offerts. Les prix du catalogue sont
      indicatifs : seule une soumission écrite, remise après une visite, engage l’entreprise.</p></div>
    </div>
    <div class="row" data-rev>
      <i>04 · Hébergement</i>
      <div><h3>Des services techniques identifiés.</h3>
      <p>Les pages du site sont hébergées par GitHub Pages. Le formulaire de contact et le journal
      des visites passent par les services décrits dans la
      <a href="/confidentialite/" style="color:#fff">politique de confidentialité</a>, qui explique
      aussi vos droits en vertu de la Loi 25.</p></div>
    </div>
    <div class="row" data-rev>
      <i>05 · Propriété</i>
      <div><h3>Les contenus appartiennent à leur auteur.</h3>
      <p>Les textes, les images, les démonstrations et le logiciel présentés ici appartiennent à
      JARVIS Private Systems, sauf indication contraire. Les noms de produits et de technologies de
      tiers (Home Assistant, Zigbee, Z-Wave, Matter et autres) appartiennent à leurs propriétaires
      respectifs; ils sont cités pour décrire des compatibilités, sans lien d’affiliation.</p></div>
    </div>
  </div>
</section>

<section class="sect alt" id="conditions" aria-labelledby="conditions-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Conditions d’utilisation</p>
      <h2 id="conditions-titre" style="margin-top:1rem">Utiliser ce site,<br><em>en quelques règles.</em></h2>
    </div>
    <p data-rev>En consultant ce site, vous acceptez les conditions qui suivent.</p>
  </div>
  <div class="rows">
    <div class="row" data-rev>
      <i>01 · Information</i>
      <div><h3>Un contenu donné à titre d’information.</h3>
      <p>Le site décrit un projet et des services en préparation. On s’efforce de le garder exact
      et à jour, sans garantir qu’il soit complet ni exempt d’erreurs. Il ne remplace pas l’avis
      d’un professionnel (électricien, juriste, assureur) pour votre situation.</p></div>
    </div>
    <div class="row" data-rev>
      <i>02 · Usage</i>
      <div><h3>Un usage normal et loyal.</h3>
      <p>Vous pouvez consulter le site, essayer les démonstrations et partager ses pages. Il est
      interdit de tenter d’en perturber le fonctionnement, d’en extraire massivement le contenu ou
      de s’en servir pour tromper quelqu’un.</p></div>
    </div>
    <div class="row" data-rev>
      <i>03 · Responsabilité</i>
      <div><h3>Dans les limites permises par la loi.</h3>
      <p>JARVIS Private Systems ne peut être tenue responsable d’un dommage découlant de
      l’utilisation du site ou d’une interruption de celui-ci, dans la mesure permise par la loi.
      Les liens vers d’autres sites sont fournis par commodité; leur contenu relève de leurs
      éditeurs.</p></div>
    </div>
    <div class="row" data-rev>
      <i>04 · Droit applicable</i>
      <div><h3>Les lois du Québec.</h3>
      <p>Ces conditions sont régies par les lois en vigueur au Québec. Elles peuvent être mises à
      jour; la date en tête de page indique la dernière révision.</p></div>
    </div>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Une question sur ces mentions?<br><span>Écrivez-nous.</span></h2>
  <p data-rev>James répond personnellement.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a>
  <a class="pill ghost" href="/confidentialite/">Politique de confidentialité</a></div>
</section>
""",
}
