# Vision et feuille de route — une vie entière sur JARVIS (Personal Intelligence),
# l'audit de sécurité autorisé piloté par l'IA (Security Pro), Multi-Site, puis
# l'état réel du logiciel. Les deux premières sections sont des démonstrations
# interactives à données fictives; la feuille de route, elle, est réelle.

import re

from demos import feuille, pentest, vie


def _fr(s):
    """Typographie française du texte de la page (pas des démos : leur géométrie reste intacte)."""
    s = re.sub(r"(\d) (minutes|h)\b", "\\1\u00a0\\2", s)
    s = re.sub(r"\s+([:;?!»])", "\u00a0\\1", s)
    return s.replace("« ", "«\u00a0")


PAGE = {
    "url": "/vision-roadmap/",
    "v2": True,
    "title": "Vision JARVIS : une vie entière, un système privé | Feuille de route",
    "description": (
        "La vision à long terme de JARVIS : habitudes, sommeil, maison et sécurité reliés "
        "dans un système privé installé chez vous, un audit de sécurité autorisé piloté par "
        "l’IA, et l’état réel du projet."
    ),
    "og_image": "/media/concept/jarvis-future-ecosystem-v1.webp",
    "assets": ["vie", "pentest", "feuille"],
    "content": _fr("""
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-future-ecosystem-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Vision et feuille de route</p>
    <h1 data-rev style="max-width:none">Une vie entière.<br><em>Un seul système privé.</em></h1>
    <p class="lead" data-rev>Où va JARVIS à long terme, et où il en est aujourd’hui. Toujours installé
    chez vous, toujours avec votre accord.</p>
    <div class="acts" data-rev>
      <a class="pill" href="#feuille-de-route">Où en est JARVIS</a>
      <a class="pill ghost" href="#vie">Voir la vision</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip" style="display:inline-flex;align-items:center;gap:.6rem"><i class="dot" aria-hidden="true"></i>Aujourd’hui · étape 1 : noyau, comptes et interfaces</span>
      <span class="chip chip-sim">Vision · démonstrations à données fictives</span>
    </div>
  </div>
</section>

<section class="sect" id="vie" data-toc="Une vie entière">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">01 · Personal Intelligence · vision</p>
      <h2 style="margin-top:1rem">Comprendre vos habitudes. <em>Choisir votre avenir.</em></h2>
    </div>
    <div class="side" data-rev>
      <p>Montre, téléphone, agenda, banque, maison et voiture savent chacun leur part. JARVIS relie
      seulement ce que vous autorisez, repère ce qui vous nuit et vous aide à atteindre vos
      objectifs. Vous décidez à chaque étape.</p>
      <span class="chip chip-sim">Vision · données d’exemple</span>
    </div>
  </div>
  @@VIE@@
  <p class="form-note" data-rev style="max-width:76rem;margin:1.6rem auto 0">Règle centrale :
  JARVIS relie les outils choisis; il ne remplace ni le médecin, ni le conseiller financier, ni
  l’entraîneur. Bien-être seulement, aucun diagnostic. Les projections sont des estimations
  avec leur base, jamais des promesses. Les principes cités sont reformulés; seules des
  citations d’auteurs du domaine public sont reproduites. Chaque source possède sa propre
  permission, révocable séparément.</p>
</section>

<section class="sect alt" id="securite-pro" data-toc="Security Pro">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">02 · Security Pro · vision</p>
      <h2 style="margin-top:1rem">Une vraie firme de sécurité privée, <em>augmentée par l’IA.</em></h2>
    </div>
    <div class="side" data-rev>
      <p>Tests d’intrusion, red team, OSINT et enquêtes, conformité à la Loi 25, réponse aux
      incidents et soutien aux forces de l’ordre : six lignes de service, une même rigueur. Chaque
      mission part d’un mandat écrit; l’IA accélère, un professionnel valide, chaque accès est
      journalisé et chaque preuve est hachée.</p>
      <span class="chip chip-sim">Vision · données fictives</span>
    </div>
  </div>
  @@PENTEST@@
  <p class="form-note" data-rev style="max-width:76rem;margin:1.6rem auto 0">Différence
  importante : l’administration réseau JARVIS surveille au quotidien; Security Pro intervient
  dans une mission limitée, autorisée et documentée. Méthodes de référence : PTES, OWASP WSTG,
  MITRE ATT&amp;CK, NIST SP 800-115 et 800-61, ISO/IEC 27037. Avant toute mission réelle : permis
  d’agence d’investigation du Bureau de la sécurité privée, assurance responsabilité et
  vérification des antécédents de chaque analyste.</p>
</section>

<section class="sect" id="multi-site" data-toc="Plusieurs lieux">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">03 · JARVIS Multi-Site · vision à long terme</p>
      <h2 style="margin-top:1rem">Une décision. <em>Plusieurs environnements qui se
      coordonnent.</em></h2>
    </div>
    <div class="side" data-rev>
      <p>Chaque lieu conserve ses fonctions locales et ses propres règles. Seul le contexte
      nécessaire et autorisé circule entre les environnements.</p>
      <span class="chip chip-sim">Vision à long terme</span>
    </div>
  </div>
  <div class="shots" data-rev>
    <figure>
      <img src="/media/solutions/environnements-intelligents.webp" alt="Résidence reliée à JARVIS Multi-Site" loading="lazy">
      <figcaption><b>Maison</b><span>Son Hub · ses règles</span></figcaption>
    </figure>
    <figure>
      <img src="/media/ambulance/ambulance-garage-lab-v1.webp" alt="Laboratoire mobile relié à JARVIS Multi-Site" loading="lazy">
      <figcaption><b>Véhicule</b><span>Son Hub · ses données</span></figcaption>
    </figure>
    <figure>
      <img src="/media/solutions/jarvis-enterprise-operations-v1.webp" alt="Entreprise reliée à JARVIS Multi-Site" loading="lazy">
      <figcaption><b>Entreprise</b><span>Son Hub · ses permissions</span></figcaption>
    </figure>
  </div>
  <div class="cards two" style="margin-top:16px">
    <article class="card" data-rev>
      <h3>Les données détaillées ne sont pas fusionnées.</h3>
      <p>Vidéos, dossiers, positions détaillées et secrets techniques restent dans chaque
      lieu. Seul le petit événement utile circule : « arrivée prévue dans 32 minutes »,
      une alerte à vérifier, une décision approuvée.</p>
    </article>
    <article class="card" data-rev>
      <h3>Liaison interrompue : rien d’essentiel ne s’arrête.</h3>
      <p>Multi-Site améliore la coordination; il ne remplace jamais le fonctionnement local
      de la maison, du véhicule ou de l’entreprise.</p>
    </article>
  </div>
</section>

<section class="sect alt" id="feuille-de-route" data-toc="Où en est JARVIS">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">04 · État réel du projet</p>
      <h2 style="margin-top:1rem">Ce qui existe. Ce qui se construit. <em>Ce qui viendra
      après.</em></h2>
    </div>
    <p data-rev>Tout ce qui précède est une vision, montrée avec des données fictives. Le
    travail réel est précis : bâtir le logiciel étape par étape, le mettre en service sur le
    laboratoire mobile, puis le faire auditer avant toute vente.</p>
  </div>
  @@FEUILLE@@
  <div class="cards" style="margin-top:3.2rem">
    <article class="card" data-rev>
      <span class="chip" style="display:inline-flex;align-items:center;gap:.6rem"><i class="dot" aria-hidden="true"></i>Réel · en cours</span>
      <h3>Laboratoire mobile JARVIS</h3>
      <p>La conversion de la Ford 2017 V10 avance réellement : habitation, énergie, eau,
      confort, réseau, systèmes d’origine et instrumentation.</p>
    </article>
    <article class="card" data-rev>
      <span class="chip" style="display:inline-flex;align-items:center;gap:.6rem"><i class="dot" aria-hidden="true"></i>En construction · étape 1</span>
      <h3>Logiciel JARVIS : App, Core et Hub</h3>
      <p>Le noyau, les comptes et les deux interfaces se bâtissent maintenant, avec des
      vérifications automatiques à chaque changement et des modules simulés clairement
      identifiés.</p>
    </article>
    <article class="card" data-rev>
      <span class="chip chip-sim">Vision · en conception</span>
      <h3>Personal Intelligence, Security Pro, Multi-Site</h3>
      <p>Les démonstrations de cette page montrent le fonctionnement visé. Chaque extension
      deviendra un chantier à part, seulement après les preuves de l’étape précédente.</p>
    </article>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Discuter de la vision, de la recherche<br><span>ou d’un partenariat ?</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement
  définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""").replace("@@VIE@@", vie.html()).replace("@@PENTEST@@", pentest.html()).replace("@@FEUILLE@@", feuille.html()),
}
