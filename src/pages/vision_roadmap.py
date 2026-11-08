# Vision et feuille de route — le manifeste de JARVIS : rendre les gens libres.
# Manifeste → horizons (maintenant, 12 mois, 3 ans, 10 ans) → une journée avec JARVIS
# (famille et résidence de prestige) → Personal Intelligence → firme de sécurité privée →
# tous vos lieux → recherche et partenariats → principes → feuille de route réelle.
# Les sections de vision sont des démonstrations à données d'exemple; la feuille de route
# est réelle (src/demos/feuille.py).

import re

from demos import feuille, pentest, vie, vision


def _fr(s):
    """Typographie française du texte de la page (pas des démos : leur géométrie reste intacte)."""
    s = re.sub(r"(\d) (minutes|h|ans|mois)\b", "\\1\u00a0\\2", s)
    s = re.sub(r"\s+([:;?!»])", "\u00a0\\1", s)
    return s.replace("« ", "«\u00a0")


def _head(num, eyebrow, titre, texte, chip=None, ident=""):
    chip_html = f'\n      <span class="chip chip-sim">{chip}</span>' if chip else ""
    return f"""<div class="sect-head vn-head">
    <div data-rev>
      <p class="eyebrow">{num} · {eyebrow}</p>
      <h2{ident} style="margin-top:1rem">{titre}</h2>
    </div>
    <div class="side" data-rev>
      <p>{texte}</p>{chip_html}
    </div>
  </div>"""


PAGE = {
    "url": "/vision-roadmap/",
    "v2": True,
    "title": "Vision JARVIS : rendre les gens libres | Feuille de route",
    "description": (
        "Le manifeste de JARVIS : un système privé installé chez vous qui rend du temps, garde "
        "vos données et vous laisse décider. Horizons à 12 mois, 3 ans et 10 ans, une journée "
        "avec JARVIS, la firme de sécurité privée, la recherche et l’état réel du projet."
    ),
    "og_image": "/media/concept/jarvis-future-ecosystem-v1.webp",
    "assets": ["vision", "vie", "pentest", "feuille"],
    "content": _fr("""
<section class="band top vn-hero">
  <div class="bg"><img src="/media/concept/jarvis-future-ecosystem-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Vision · le manifeste de JARVIS</p>
    <h1 data-rev style="max-width:none">Rendre les gens libres.<br><em>Un système privé à la fois.</em></h1>
    <p class="lead" data-rev>Une maison, une entreprise, un véhicule, un yacht ou un jet : JARVIS
    les comprend, les relie et s’en occupe, chez vous, avec votre accord. Voici où il va, et où il
    en est vraiment.</p>
    <div class="acts" data-rev>
      <a class="pill" href="#horizons">Voir les horizons</a>
      <a class="pill ghost" href="#journee">Une journée avec JARVIS</a>
      <a class="pill ghost" href="#feuille-de-route">Où en est JARVIS</a>
    </div>
    <div class="vn-hero-n" data-rev>
      <span><b>7</b>extensions reliées</span>
      <span><b>1</b>Hub, chez vous</span>
      <span><b>0</b>donnée vendue</span>
      <span><b>4</b>horizons, de maintenant à 10 ans</span>
    </div>
  </div>
</section>

<section class="sect" id="manifeste" data-toc="Le manifeste">
  @@MANIFESTE@@
</section>

<section class="sect alt" id="horizons" data-toc="Les horizons">
  """ + _head("01", "Ligne du temps", "Maintenant. 12 mois. 3 ans. <em>10 ans.</em>",
              "Quatre horizons, huit jalons chacun : le Hub et les sept extensions avancent ensemble, "
              "du laboratoire mobile d’aujourd’hui aux résidences de prestige de demain.",
              "Maintenant · réel · ensuite · objectifs") + """
  @@HORIZONS@@
</section>

<section class="sect" id="journee" data-toc="Une journée">
  """ + _head("02", "Une journée avec JARVIS", "Une famille. Une résidence de prestige. <em>La même liberté.</em>",
              "Du réveil à la nuit, ce que JARVIS fait seul et ce qu’il vous laisse décider. Choisissez "
              "un client, puis touchez un moment de la journée.",
              "Vision · données d’exemple") + """
  @@JOURNEE@@
</section>

<section class="sect alt" id="vie" data-toc="Personal Intelligence">
  """ + _head("03", "Personal Intelligence · vision", "Comprendre vos habitudes. <em>Choisir votre avenir.</em>",
              "Montre, téléphone, agenda, banque, maison et voiture savent chacun leur part. JARVIS relie "
              "seulement ce que vous autorisez, repère ce qui vous nuit et vous aide à atteindre vos "
              "objectifs. Vous décidez à chaque étape.",
              "Vision · données d’exemple") + """
  @@VIE@@
  <p class="form-note" data-rev style="max-width:76rem;margin:1.6rem auto 0">Règle centrale :
  JARVIS relie les outils choisis; il ne remplace ni le médecin, ni le conseiller financier, ni
  l’entraîneur. Bien-être seulement, aucun diagnostic. Les projections sont des estimations
  avec leur base, jamais des promesses. Les principes cités sont reformulés; seules des
  citations d’auteurs du domaine public sont reproduites. Chaque source possède sa propre
  permission, révocable séparément.</p>
</section>

<section class="sect" id="securite-pro" data-toc="La firme de sécurité">
  """ + _head("04", "Security Pro · vision", "Une vraie firme de sécurité privée, <em>augmentée par l’IA.</em>",
              "Six lignes de service, une même rigueur. Chaque mission part d’un mandat écrit; l’IA "
              "accélère, un professionnel valide, chaque accès est journalisé et chaque preuve est hachée.",
              "Vision · données fictives") + """
  @@FIRME@@
  <div style="margin-top:3.2rem">@@PENTEST@@</div>
  <p class="form-note" data-rev style="max-width:76rem;margin:1.6rem auto 0">Différence
  importante : l’administration réseau JARVIS surveille au quotidien; Security Pro intervient
  dans une mission limitée, autorisée et documentée. Méthodes de référence : PTES, OWASP WSTG,
  MITRE ATT&amp;CK, NIST SP 800-115 et 800-61, ISO/IEC 27037. Avant toute mission réelle : permis
  d’agence d’investigation du Bureau de la sécurité privée, assurance responsabilité et
  vérification des antécédents de chaque analyste.</p>
</section>

<section class="sect alt" id="multi-site" data-toc="Tous vos lieux">
  """ + _head("05", "JARVIS Multi-Site · vision à long terme", "Une décision. <em>Tous vos lieux qui se coordonnent.</em>",
              "Chaque lieu garde son Hub, ses fonctions locales et ses propres règles. Seul le petit "
              "événement utile et autorisé circule entre eux.",
              "Vision à long terme") + """
  @@LIEUX@@
</section>

<section class="sect" id="recherche" data-toc="Recherche">
  """ + _head("06", "Recherche", "IA locale, matériel et Rust. <em>Les fondations de demain.</em>",
              "Ce qui rend JARVIS possible sans nuage : une IA qui tourne chez vous, un Hub conçu pour "
              "durer et un noyau écrit pour être sûr.") + """
  @@RECHERCHE@@
</section>

<section class="sect alt" id="partenariats" data-toc="Partenariats">
  """ + _head("07", "Partenariats", "Seul, on va vite. <em>Ensemble, on va loin.</em>",
              "JARVIS coordonne; les métiers restent aux experts. Les partenaires cherchés aujourd’hui, "
              "pour installer, entretenir et protéger.") + """
  @@PARTENAIRES@@
</section>

<section class="sect" id="principes" data-toc="Principes">
  """ + _head("08", "Principes", "Ce qui ne changera jamais.",
              "Six engagements qui passent avant toute fonction, toute vente et toute croissance.") + """
  @@PRINCIPES@@
</section>

<section class="sect alt" id="feuille-de-route" data-toc="Où en est JARVIS">
  """ + _head("09", "État réel du projet", "Ce qui existe. Ce qui se construit. <em>Ce qui viendra après.</em>",
              "Tout ce qui précède est une vision. Voici le travail réel, jalon par jalon : filtrez par "
              "solution ou par état.") + """
  @@FEUILLE@@
</section>

<section class="cta">
  <h2 data-rev>Discuter de la vision, de la recherche<br><span>ou d’un partenariat ?</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement
  définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""")
    .replace("@@MANIFESTE@@", vision.manifeste())
    .replace("@@HORIZONS@@", vision.horizons())
    .replace("@@JOURNEE@@", vision.journee())
    .replace("@@VIE@@", vie.html())
    .replace("@@FIRME@@", vision.firme())
    .replace("@@PENTEST@@", pentest.html())
    .replace("@@LIEUX@@", vision.lieux())
    .replace("@@RECHERCHE@@", vision.recherche())
    .replace("@@PARTENAIRES@@", vision.partenaires())
    .replace("@@PRINCIPES@@", vision.principes())
    .replace("@@FEUILLE@@", feuille.html()),
}
