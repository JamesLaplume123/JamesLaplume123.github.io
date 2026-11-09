# L'offre — comment se compose une installation JARVIS (refonte « clarté », novembre 2026).
# Trois étapes : 1) le Hub, 2) vos extensions, 3) installation, formation et accompagnement.
# Puis pour qui (exemples d'assemblage), combien ça coûte (aucun prix inventé), questions, démo.
# Remplace la section #offre de /plateforme/ et l'offre de l'accueil (qui renvoient ici).
# Données du Hub, des extensions et des services : src/demos/hub.py (source unique).
# Styles : assets/demos/parcours.css.

from html import escape

from config import CAPABILITIES
from demos.hub import EXT, HUB_INCLUS, SERVICES, icon

EXT_SLUG = {e[1]: e for e in EXT}
CLE = {e[0]: e for e in EXT}


def _hub():
    inclus = "".join(
        f'<li data-rev>{icon(k)}<div><b>{n}</b><span>{d}</span></div></li>' for k, n, d in HUB_INCLUS
    )
    return f"""<div class="of-hub">
    <figure class="of-hub-ph" data-rev>
      <img src="/media/product/jarvis-hub-v1.webp" alt="Le boîtier JARVIS Hub, installé sur place" loading="lazy" decoding="async">
    </figure>
    <div class="of-hub-t">
      <p class="of-tag">{icon("hub")}La base de chaque client</p>
      <p class="of-hub-p">Chaque installation JARVIS commence par lui. Il contient tout ce qu’il faut pour que le
      système fonctionne, chez vous, avant même la première extension.</p>
      <ul class="of-inc">{inclus}</ul>
    </div>
  </div>"""


def _extensions():
    cartes = []
    for c in CAPABILITIES:
        e = EXT_SLUG.get(c["slug"])
        inclus = "".join(f"<li>{escape(p)}</li>" for p in e[8]) if e else ""
        cartes.append(f"""<article class="of-x" data-rev>
      <a class="of-x-ph" href="/solutions/{c['slug']}/" tabindex="-1" aria-hidden="true">
        <img src="{c['image']}" alt="" loading="lazy" decoding="async"><span>{c['num']}</span>
      </a>
      <div class="of-x-b">
        <p class="of-x-k">{c['label']}</p>
        <h3><a href="/solutions/{c['slug']}/">{c['title']}</a></h3>
        <p class="of-x-l">{c['short']}</p>
        <p class="of-x-for"><span>Pour</span> {c['pour']}</p>
        <ul class="of-x-inc">{inclus}</ul>
        <p class="of-x-go"><a href="/solutions/{c['slug']}/">Voir la solution <i aria-hidden="true">→</i></a>
        <a href="/solutions/{c['slug']}/#jarvis">Essayer dans JARVIS <i aria-hidden="true">↗</i></a></p>
      </div>
    </article>""")
    cartes.append("""<article class="of-x of-x-aide" data-rev>
      <div class="of-x-b">
        <p class="of-x-k">Pas certain?</p>
        <h3>On choisit avec vous.</h3>
        <p class="of-x-l">Racontez-nous votre lieu et ce qui vous dérange. Nous vous dirons quelle extension
        règle le problème, et laquelle peut attendre.</p>
        <p class="of-x-go"><a href="/contact/">Réserver une démo <i aria-hidden="true">→</i></a>
        <a href="/solutions/">Comparer les sept solutions <i aria-hidden="true">→</i></a></p>
      </div>
    </article>""")
    return "".join(cartes)


def _services():
    return "".join(
        f'<article class="of-sv card" data-rev>{icon(k)}<h3>{n}</h3>'
        f'<ul>{"".join(f"<li>{escape(i)}</li>" for i in items)}</ul></article>'
        for k, n, items in SERVICES
    )


# Pour qui : (profil, lieux, titre, texte, extensions, photo)
PROFILS = [
    ("Maison familiale", "Maison · condo · chalet",
     "Une maison qui se gère et se protège.",
     "Le confort et l’énergie, la sécurité et un réseau solide. L’IA privée s’ajoute si la famille veut "
     "retrouver ses documents.",
     ["env", "secu", "res", "ia"], "/media/offre/maison.webp"),
    ("Résidence de prestige", "Domaine · garage de collection · quai",
     "Un domaine entier, sur un seul écran.",
     "Plusieurs bâtiments, des véhicules de collection, un quai : chaque accès noté, chaque lieu suivi, "
     "et un réseau qui tient bon.",
     ["env", "secu", "res", "ia", "mob"], "/media/vitrine/accueil/residence-prestige-soir.webp"),
    ("Entreprise", "Bureau · commerce · atelier",
     "Une réception qui ne manque aucun appel.",
     "Les appels, les demandes et les approbations circulent seuls. Les accès et le réseau sont protégés, "
     "et la mémoire de l’entreprise se retrouve en une question.",
     ["auto", "secu", "res", "ia"], "/media/solutions/jarvis-enterprise-operations-v1.webp"),
    ("Ferme", "Bâtiments et équipes",
     "Des bâtiments surveillés, des équipes qui suivent.",
     "Les capteurs des bâtiments, le diagnostic des équipements, les bons de travail et la garde, "
     "les accès et la mémoire documentaire de l’entreprise.",
     ["env", "diag", "auto", "secu", "res", "ia"], "/media/offre/ferme.webp"),
    ("Véhicule et VR", "VR · véhicule aménagé · unité spécialisée",
     "Un VR autonome, qui pense à la route.",
     "Les batteries, l’eau et le confort à bord, le copilote de route, le diagnostic et la connexion "
     "en voyage.",
     ["env", "mob", "diag", "res"], "/media/offre/vr.webp"),
]


def _profils():
    out = []
    for nom, lieux, h, p, xs, img in PROFILS:
        chips = "".join(
            f'<a class="of-chip" href="/solutions/{CLE[k][1]}/">{icon(k)}<span>{CLE[k][2]}</span></a>' for k in xs
        )
        out.append(f"""<article class="of-pf" data-rev>
      <div class="of-pf-ph"><img src="{img}" alt="" loading="lazy" decoding="async"></div>
      <div class="of-pf-b">
        <p class="of-pf-k">{nom} <span>· {lieux}</span></p>
        <h3>{h}</h3>
        <p>{p}</p>
        <p class="of-pf-f"><span class="of-chip is-hub">{icon("hub")}<span>Hub</span></span><i aria-hidden="true">+</i>{chips}</p>
        <p class="of-pf-n">Exemple d’assemblage · {len(xs)} extensions</p>
      </div>
    </article>""")
    return "".join(out)


VARIE = [
    ("La taille du lieu", "Une pièce, une maison, un domaine ou plusieurs bâtiments."),
    ("Le nombre de lieux", "Un Hub par lieu : la maison, puis un chalet, un garage ou un VR, chacun avec le sien."),
    ("Le nombre d’extensions", "Vous commencez par une seule; les autres s’ajoutent plus tard."),
    ("Ce qui est déjà en place", "On réutilise vos appareils quand c’est possible. Il en coûte moins."),
    ("Les appareils à ajouter", "Caméras, capteurs, serrures ou boîtier de véhicule, s’il en faut."),
    ("Le câblage et les travaux", "Un réseau à refaire ou des fils à passer changent le temps sur place."),
    ("L’entretien et le soutien", "Le niveau de suivi que vous choisissez après l’installation."),
]

FAQ = [
    ("Dois-je prendre toutes les extensions?",
     "Non. Chaque installation part du Hub, puis on ajoute seulement les extensions qui règlent un vrai "
     "problème chez vous. Beaucoup de clients commencent par une seule."),
    ("Puis-je ajouter une extension plus tard?",
     "Oui. Le Hub est prévu pour ça : une extension s’ajoute sans tout reconstruire, avec ses propres "
     "droits. Vous pouvez aussi en retirer une."),
    ("Qu’est-ce qui vient avec le Hub?",
     "Le boîtier installé chez vous, JARVIS Core (règles, comptes et journal), l’IA locale en français, "
     "l’application pour chaque compte, les sauvegardes et les mises à jour. L’essentiel continue de "
     "fonctionner sans Internet."),
    ("Faut-il un abonnement?",
     "Aucun abonnement au nuage n’est nécessaire pour que JARVIS fonctionne. L’entretien et le soutien que "
     "vous choisissez sont décrits dans la soumission, ligne par ligne, avant que vous décidiez."),
    ("Est-ce disponible aujourd’hui?",
     "JARVIS est en construction : le noyau du logiciel est en développement et le premier JARVIS tourne déjà "
     "dans le laboratoire mobile. Rien ne se vend avant une revue de sécurité par un expert externe. La démo "
     "et la visite, elles, sont offertes dès maintenant."),
]

FAQ_HTML = "".join(
    f"""<details class="faq-item" data-rev>
      <summary><span>{q}</span><i aria-hidden="true"></i></summary>
      <div class="faq-a"><p>{a}</p></div>
    </details>"""
    for q, a in FAQ
)


def _etape(n):
    return f'<p class="of-num"><i>{n}</i><span>Étape {n} sur 3</span></p>'


PAGE = {
    "url": "/offre/",
    "v2": True,
    "title": "L’offre JARVIS | Le Hub, vos extensions, l’installation",
    "description": (
        "Le Hub, puis seulement les extensions utiles, avec l’installation, la formation et le soutien. "
        "Soumission gratuite après une visite."
    ),
    "og_image": "/media/offre/maison.webp",
    "assets": ["parcours"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/jarvis-spaces-property-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>L’offre JARVIS</p>
    <h1 data-rev>Le Hub, puis vos extensions.<br><em>Rien de plus.</em></h1>
    <p class="lead" data-rev>Chaque client part du Hub. On ajoute les extensions utiles, maintenant ou plus
    tard, avec l’installation, la formation et le soutien.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="#prix">Combien ça coûte</a>
    </div>
    <ol class="of-trois" data-rev>
      <li><a href="#hub"><i>1</i>Le Hub</a></li>
      <li><a href="#extensions"><i>2</i>Vos extensions</a></li>
      <li><a href="#accompagnement"><i>3</i>Installation et soutien</a></li>
    </ol>
  </div>
</section>

<section class="sect" id="hub" data-toc="1 · Le Hub" aria-labelledby="hub-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(1)}
      <h2 id="hub-titre">Le Hub JARVIS.<br><em>Votre système, chez vous.</em></h2>
    </div>
    <p data-rev>Un petit boîtier silencieux, installé et entretenu par nous : rien à gérer. Il garde vos
    données, fait tourner l’IA et applique vos règles, même quand Internet tombe. Un lieu, un Hub;
    tous vos lieux dans une seule application.</p>
  </div>
  {_hub()}
</section>

<section class="sect alt" id="extensions" data-toc="2 · Vos extensions" aria-labelledby="ext-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(2)}
      <h2 id="ext-titre">Vous choisissez<br><em>vos extensions.</em></h2>
    </div>
    <p data-rev>Réceptionniste, gardien, archiviste, technicien : chaque extension fait un travail précis,
    dans la même application. Prenez seulement ce dont vous avez besoin.</p>
  </div>
  <div class="of-xs">{_extensions()}</div>
</section>

<section class="sect" id="accompagnement" data-toc="3 · Installation et soutien" aria-labelledby="sv-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(3)}
      <h2 id="sv-titre">Installation, formation<br><em>et accompagnement.</em></h2>
    </div>
    <p data-rev>Vous n’avez rien à configurer. On installe, on forme les personnes qui utiliseront JARVIS,
    puis on reste là.</p>
  </div>
  <div class="cards of-svs">{_services()}</div>
</section>

<section class="sect alt" id="pour-qui" data-toc="Pour qui" aria-labelledby="pq-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Pour qui</p>
      <h2 id="pq-titre">Un exemple<br><em>pour chaque lieu.</em></h2>
    </div>
    <p data-rev>Des exemples d’assemblage, pas des forfaits. Le vôtre se compose après une visite.</p>
  </div>
  <div class="of-pfs">{_profils()}</div>
  <div class="of-mesure" data-rev>
    <span class="of-chip is-hub">{icon("plus")}<span>Sur mesure</span></span>
    <p><b>Votre lieu ne ressemble à aucun exemple?</b> Choisissez les extensions qui vous ressemblent. Nous
    partons de votre lieu et de votre premier problème, puis nous composons ensemble.</p>
  </div>
</section>

<section class="sect" id="prix" data-toc="Combien ça coûte" aria-labelledby="prix-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Combien ça coûte</p>
      <h2 id="prix-titre">Un prix juste,<br><em>après avoir vu votre lieu.</em></h2>
    </div>
    <p data-rev>Aucun prix affiché : chaque composition est chiffrée après la visite du lieu, par écrit,
    avec ce qui est inclus ligne par ligne.</p>
  </div>
  <div class="of-prix">
    <article class="card of-sq" data-rev>
      <small>Soumission gratuite</small>
      <h3>Trois étapes, sans engagement.</h3>
      <ol>
        <li><i>1</i><div><b>Une visite de votre lieu</b><span>On regarde ce qui existe déjà et le premier problème à régler.</span></div></li>
        <li><i>2</i><div><b>Une soumission écrite</b><span>Le Hub, les extensions, les appareils et les services, ligne par ligne.</span></div></li>
        <li><i>3</i><div><b>Vous décidez</b><span>Maintenant, plus tard ou pas du tout. Aucune pression.</span></div></li>
      </ol>
      <a class="pill" href="/contact/">Demander une visite</a>
    </article>
    <div class="of-varie" data-rev>
      <p class="of-varie-k">Ce qui fait varier le prix</p>
      <ul>{"".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in VARIE)}</ul>
    </div>
  </div>
  <p class="of-note" data-rev>JARVIS est en construction : la démo montre honnêtement ce qui fonctionne
  aujourd’hui. <a href="/vision-roadmap/#feuille-de-route">Où en est le projet</a></p>
</section>

<section class="faq" id="questions" aria-labelledby="faq-titre">
  <div class="head" data-rev>
    <p class="eyebrow">Questions sur l’offre</p>
    <h2 id="faq-titre">Ce qu’on nous demande <em>le plus souvent.</em></h2>
  </div>
  <div class="faq-list">{FAQ_HTML}</div>
</section>

<section class="cta">
  <h2 data-rev>Voyons ce qu’il vous faut,<br><span>chez vous.</span></h2>
  <p data-rev>Une rencontre, vos besoins réels, et ce qui fonctionne déjà aujourd’hui.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a>
  <a class="pill ghost" href="/logiciel/">Essayer le logiciel</a></div>
</section>
""",
}
