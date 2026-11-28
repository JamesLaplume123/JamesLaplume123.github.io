# JARVIS Entreprise — la deuxième division (refonte « trois divisions », novembre 2026).
# Remplace l'ancienne page « Toute votre entreprise » (besoins.py), à la même adresse.
# Deux parties : Votre travail (Réceptionniste IA, Automatisations, Comptes et accès, Rapport du matin,
# Savoir de l'entreprise), puis Vos bâtiments (les cinq solutions de JARVIS Privé, version entreprise).
# Chaque carte nomme une pièce qui existe déjà dans l'offre (pages/catalogue.py) et mène à sa page.
# Aucun prix ici, et rien sur ce que comprend un niveau : c'est l'offre qui le dit.
# Données : src/divisions.py · Styles : assets/demos/divisions.css.

import divisions
import pro

URL = "/solutions/entreprise/"
NOM = "JARVIS Entreprise"
DESCRIPTION = (
    "JARVIS répond au téléphone, fait les suivis, relie vos outils et protège vos lieux et votre "
    "réseau. Toute l’entreprise dans un seul système privé, installé chez vous."
)

SUITE = [
    ("/solutions/automatisation-operations/#essayer", "Essayer la réceptionniste"),
    ("/solutions/automatisation-operations/#votre-secteur", "Trouver mon secteur"),
    ("/offre/#composer", "Composer pour mon entreprise"),
]

FAQ = [
    ("Par où commencer?",
     "Par le problème qui vous coûte le plus cher : les appels manqués, les suivis oubliés ou la "
     "sécurité. La page L’offre propose trois exemples selon la taille de l’entreprise; le reste "
     "s’ajoute au mois, quand vous en voyez le gain."),
    ("Jusqu’où JARVIS agit-il seul?",
     "C’est vous qui le décidez, domaine par domaine : il voit, il avertit, il propose, il agit avec "
     "votre accord, ou il agit selon vos règles et vous rend compte. Rien de sensible ne part sans "
     "l’accord d’une personne."),
    ("Dois-je changer mes logiciels ou mon annuaire?",
     "En général, non. JARVIS se relie aux outils que vous utilisez déjà (courriel, agenda, "
     "téléphonie, comptabilité) et à l’annuaire de votre entreprise (Microsoft 365, Active "
     "Directory). Il ne les remplace pas et ne gère pas vos postes de travail."),
]

LIENS = "\n  ".join(f'<a href="{u}">{t} <i aria-hidden="true">→</i></a>' for u, t in SUITE)

PAGE = {
    "url": URL,
    "v2": True,
    "title": "JARVIS pour votre entreprise : un seul système privé",
    "description": DESCRIPTION,
    "og_image": "/media/accueil/film-entreprise.webp",
    "public": "entreprise",
    "assets": ["divisions", "pro"],
    "schema": [
        pro.ld_service(NOM, DESCRIPTION, URL, "Système privé de gestion et de sécurité pour entreprise"),
        pro.ld_faq(FAQ),
    ],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/accueil/film-entreprise.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil(URL)}
    <h1 data-rev>JARVIS <em>Entreprise.</em></h1>
    <p class="lead" data-rev>Votre entreprise roule toute seule : JARVIS répond au téléphone, fait les suivis, surveille vos lieux et votre réseau, et vous fait rapport.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="#travail">Voir les solutions</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> Travailleurs autonomes, PME, fermes et commerces</p>
  </div>
</section>

<section class="sect" id="travail" aria-labelledby="en-travail">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Votre travail</p>
      <h2 id="en-travail">Le bureau <em>se fait tout seul.</em></h2>
    </div>
    <div class="side" data-rev><p>Les appels, les suivis, les accès et l’information : ce qui vous coûte des heures chaque semaine.</p></div>
  </div>
  <div class="gam gam-5">{divisions.gamme(divisions.ENTREPRISE_TRAVAIL)}</div>
</section>

<section class="sect alt" id="batiments" aria-labelledby="en-bat">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Vos bâtiments</p>
      <h2 id="en-bat">Vos lieux, <em>protégés et gérés.</em></h2>
    </div>
    <div class="side" data-rev><p>Les solutions de JARVIS Privé, à l’échelle de votre entreprise : bureaux, entrepôts, commerces et véhicules.</p></div>
  </div>
  <div class="gam gam-5">{divisions.gamme(divisions.ENTREPRISE_BATIMENTS)}</div>
  <p class="pro-suite" data-rev>{LIENS}</p>
</section>

{pro.faq_section(FAQ, NOM, "Questions fréquentes")}

<section class="cta">
  <h2 data-rev>Votre entreprise,<br><span>sans rien laisser tomber.</span></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
