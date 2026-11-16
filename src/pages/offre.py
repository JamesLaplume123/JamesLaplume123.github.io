# L'offre — comment se compose un JARVIS (alignée sur le catalogue, novembre 2026).
# Quatre étapes, avec les prix du catalogue : 1) le Hub (Base, Signature, Platinum), 2) les solutions
# par mois, 3) le matériel, 4) lieux, installation et services. Puis un exemple par lieu (un kit), trois
# factures types, les questions, la démo. Tous les prix viennent de src/pages/catalogue.py (source unique).
# Styles : assets/demos/parcours.css + assets/demos/offre.css.

from html import escape

from config import CAPABILITIES
from demos.hub import HUB_INCLUS, icon
from pages import catalogue as CAT
import pro

# Prix affiché sur chaque carte de solution (slug du site → texte)
SOL_BY_SLUG = {s["slug"]: s for s in CAT.SOLUTIONS}
PRIX_SOL = {s["slug"]: ("Inclus avec le Hub" if s["prix"] == 0 else f"{s['prix']} $/mois" + (" par véhicule" if s.get("unite") else ""))
            for s in CAT.SOLUTIONS}
PRIX_SOL["automatisation-operations"] = f"dès {CAT.ENT_SOCLE['prix']} $/mois + 9 $ par automatisation"


def _p(n):
    return f"{n:,}".replace(",", " ") + " $"


def _hub():
    inclus = "".join(
        f'<li data-rev>{icon(k)}<div><b>{n}</b><span>{d}</span></div></li>' for k, n, d in HUB_INCLUS
    )
    tuiles = []
    for h in CAT.HUBS:
        tag = f'<span class="of-h-tag">{escape(h["tag"])}</span>' if h["tag"] else ""
        pts = "".join(f"<li>{escape(x)}</li>" for x in h["pts"][:3])
        tuiles.append(f"""<a class="of-h" href="/catalogue/#hub" data-rev>
      {tag}<p class="of-h-k">{escape(h['pour'])}</p>
      <h3>{escape(h['nom'])}</h3>
      <p class="of-h-prix">{_p(h['prix'])}<small>une fois</small></p>
      <ul>{pts}</ul>
      <span class="of-h-go">Comparer dans le catalogue <i aria-hidden="true">→</i></span>
    </a>""")
    return f"""<div class="of-hub">
    <figure class="of-hub-ph" data-rev>
      <img src="/media/product/jarvis-hub-v1.webp" alt="Le boîtier JARVIS Hub" loading="lazy" decoding="async">
    </figure>
    <div class="of-hub-t">
      <p class="of-tag">{icon("hub")}Un par lieu, payé une fois</p>
      <p class="of-hub-p">Un petit boîtier silencieux qui garde vos données, fait tourner l’IA et applique vos règles,
      même quand Internet tombe. Livré prêt à brancher, ou installé par nous.</p>
      <ul class="of-inc">{inclus}</ul>
    </div>
  </div>
  <div class="of-hs">{"".join(tuiles)}</div>"""


def _solutions():
    cartes = []
    for c in CAPABILITIES:
        s = SOL_BY_SLUG.get(c["slug"])
        why = s["pourquoi"] if s else "Une réceptionniste qui ne manque aucun appel, et des automatisations à la carte."
        pts = s["pts"][:3] if s else ["Réceptionniste IA, 300 minutes par ligne", "25 automatisations prêtes, 9 à 29 $ chacune", "Socle Entreprise : journal, rapports, connexions"]
        inclus = "".join(f"<li>{escape(x)}</li>" for x in pts)
        cartes.append(f"""<article class="of-x" data-rev>
      <a class="of-x-ph" href="/solutions/{c['slug']}/" tabindex="-1" aria-hidden="true">
        <img src="{c['image']}" alt="" loading="lazy" decoding="async"><span>{c['num']}</span>
      </a>
      <div class="of-x-b">
        <p class="of-x-k">{c['label']}</p>
        <h3><a href="/solutions/{c['slug']}/">{c['title']}</a></h3>
        <p class="of-x-prix">{escape(PRIX_SOL[c['slug']])}</p>
        <p class="of-x-l">{escape(why)}</p>
        <ul class="of-x-inc">{inclus}</ul>
        <p class="of-x-go"><a href="/solutions/{c['slug']}/">Voir la solution <i aria-hidden="true">→</i></a>
        <a href="/catalogue/#solutions">Ajouter au panier <i aria-hidden="true">→</i></a></p>
      </div>
    </article>""")
    cartes.append(f"""<article class="of-x of-x-aide" data-rev>
      <div class="of-x-b">
        <p class="of-x-k">Meilleure valeur</p>
        <h3>{CAT.COMPLET['nom']} · {CAT.COMPLET['prix']} $/mois</h3>
        <p class="of-x-l">Les cinq solutions payantes, Mobilité pour un véhicule comprise. Valeur à la carte :
        {CAT.COMPLET['valeur']} $/mois. Annulable en tout temps.</p>
        <p class="of-x-go"><a href="/catalogue/#solutions">Choisir Complet <i aria-hidden="true">→</i></a>
        <a href="/contact/">Pas certain? On choisit avec vous <i aria-hidden="true">→</i></a></p>
      </div>
    </article>""")
    return "".join(cartes)


def _materiel():
    def mini(cat):
        items = dict((c, i) for c, i in CAT.MATERIEL)[cat]
        bas = min(p for _, _, p, _, _ in items)
        return bas, len(items)
    blocs = [
        ("Boîtiers JARVIS", "Boîtier VR (12 V, réservoirs, batteries), Boîtier Mobilité (voiture), Écran JARVIS, Boîtier Secours."),
        ("Capteurs", "Fuite, gel, porte, présence, fumée, propane, réservoir, pneus, énergie."),
        ("Caméras et accès", "Caméras 4K, sonnette, lecteur de plaques, serrures, interphone, clavier à badges."),
        ("Confort et réseau", "Thermostats, interrupteurs, stores, switch PoE, routeur 4G, Starlink, téléphone IP."),
    ]
    out = []
    for cat, d in blocs:
        bas, n = mini(cat)
        out.append(f"""<a class="card of-m" href="/catalogue/#materiel" data-rev>
      <small>{n} produits · dès {_p(bas)}</small><h3>{escape(cat)}</h3><p>{escape(d)}</p>
    </a>""")
    return "".join(out)


def _install():
    return "".join(f"""<article class="card of-sv" data-rev><small>{escape(aff)}</small><h3>{escape(n)}</h3><p>{escape(d)}</p></article>"""
                   for _, n, _, aff, d in CAT.INSTALL)


# Un exemple par lieu : (profil, lieux, titre, texte, numéro du kit (1 = premier), photo)
PROFILS = [
    ("Maison familiale", "Maison · condo", "Une maison qui se gère et se protège.",
     "L’eau coupée toute seule à la première fuite, la sonnette qui reconnaît le livreur, l’IA chez vous.", 4, "/media/offre/maison.webp"),
    ("Chalet", "Chalet fermé l’hiver · sans Internet", "Un chalet qui vous prévient avant le dégât.",
     "Gel, fuite, porte : le routeur 4G envoie l’alerte avant que le plancher lève au printemps.", 3, "/media/offre/maison.webp"),
    ("Entreprise", "Garage · clinique · bureau", "Une réception qui ne manque aucun appel.",
     "La réceptionniste IA répond 24/7, prend les rendez-vous et texte le rappel; les caméras et les accès sont réglés.", 6, "/media/solutions/jarvis-enterprise-operations-v1.webp"),
    ("Résidence de prestige", "Domaine · garage de collection · quai", "Un domaine entier, sur un seul écran.",
     "Caméras, plaques, serrures, interphone, eau et secours : rien n’entre, rien ne coule, rien ne s’arrête.", 7, "/media/vitrine/accueil/residence-prestige-soir.webp"),
    ("Ferme", "Ferme laitière · érablière · serre", "Des bâtiments surveillés, nuit et jour.",
     "Frigo, réservoir à lait, pompes et silo surveillés; la commande de moulée part toute seule.", 8, "/media/offre/ferme.webp"),
    ("Véhicule et VR", "VR · roulotte · bateau", "Un VR que vous voyez de partout.",
     "Batteries, réservoirs, propane, caméra et écran : le VR au complet dans votre poche, même sur la route.", 2, "/media/offre/vr.webp"),
]


def _profils():
    out = []
    for nom, lieux, h, texte, kn, img in PROFILS:
        k = CAT.KITS[kn - 1]
        plein, once, mois = CAT._kit_totaux(k)
        hub = CAT.HUB_BY_ID[k["hub"]]["nom"]
        out.append(f"""<article class="of-pf" data-rev>
      <div class="of-pf-ph"><img src="{img}" alt="" loading="lazy" decoding="async"></div>
      <div class="of-pf-b">
        <p class="of-pf-k">{nom} <span>· {lieux}</span></p>
        <h3>{h}</h3>
        <p>{texte}</p>
        <p class="of-pf-prix"><b>{_p(once)}</b> une fois <i>·</i> <b>{mois} $</b> par mois</p>
        <p class="of-pf-n">{escape(k['nom'])} : {hub} + {sum(k['mat'].values())} appareils, prix des pièces moins 8 %.</p>
        <p class="of-pf-f"><a class="pill" href="/catalogue/?kit={kn}">Partir de ce kit</a></p>
      </div>
    </article>""")
    return "".join(out)


def _factures():
    # Trois factures types, calculées à partir des kits (jamais tapées à la main).
    lignes = []
    for kn, titre in ((3, "Chalet"), (4, "Maison"), (6, "PME")):
        k = CAT.KITS[kn - 1]
        plein, once, mois = CAT._kit_totaux(k)
        lignes.append(f"""<article class="of-fact" data-rev>
      <p class="of-fact-k">{titre}</p>
      <p class="of-fact-n">{escape(k['nom'])}</p>
      <dl><div><dt>Aujourd’hui</dt><dd>{_p(once)}</dd></div><div><dt>Par mois</dt><dd>{mois} $</dd></div><div><dt>Première année</dt><dd>{_p(once + 12 * mois)}</dd></div></dl>
      <a href="/catalogue/?kit={kn}">Voir le détail <i aria-hidden="true">→</i></a>
    </article>""")
    return "".join(lignes)


FAQ = [
    ("Dois-je prendre toutes les solutions?",
     "Non. Environnements intelligents vient avec chaque Hub. Les autres s’ajoutent par mois, une à la fois, "
     "et s’annulent en tout temps. JARVIS Complet les regroupe à 49 $ si vous en voulez plusieurs."),
    ("Qu’est-ce que j’ai sans abonnement?",
     "Tout ce qui tourne chez vous : les scènes, le chauffage, les lumières, les serrures, l’IA du Hub. "
     "Les solutions par mois ajoutent l’accès de partout, les alertes sur votre téléphone et la veille 24/7."),
    ("Est-ce que je peux l’installer moi-même?",
     "Oui, et c’est inclus : prises identifiées, aucun fil à couper, plan et vidéo, mise en service à distance. "
     "Si vous préférez, un technicien vous guide en vidéo (149 $) ou vient sur place (110 $ l’heure)."),
    ("Et si Internet tombe?",
     "JARVIS continue : les règles, l’IA locale (Signature et Platinum), les caméras et le journal restent en marche "
     "sur place. Le Hub Platinum a en plus une batterie de deux heures et un Internet de secours."),
    ("Les prix sont-ils définitifs?",
     "Ce sont des points de départ, en dollars canadiens, taxes en sus. Chaque soumission est confirmée par écrit, "
     "ligne par ligne, avant que vous payiez quoi que ce soit."),
    ("Est-ce disponible aujourd’hui?",
     "JARVIS est en construction : le noyau du logiciel est en développement et le premier JARVIS tourne déjà "
     "dans le laboratoire mobile. Rien ne se vend avant une revue de sécurité par un expert externe. La démo, "
     "la visite et la soumission sont offertes dès maintenant."),
]

FAQ_HTML = pro.faq_items(FAQ)


def _etape(n):
    return f'<p class="of-num"><i>{n}</i><span>Étape {n} sur 4</span></p>'


PAGE = {
    "url": "/offre/",
    "v2": True,
    "title": "L’offre JARVIS | Un Hub, vos solutions, le matériel de votre lieu",
    "schema": [pro.ld_faq(FAQ)],
    "description": (
        "Un Hub payé une fois (dès 590 $), des solutions par mois (dès 10 $), le matériel qu’il vous faut. "
        "Composez votre JARVIS et voyez le total dans le catalogue."
    ),
    "og_image": "/media/offre/maison.webp",
    "assets": ["parcours", "offre"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/jarvis-spaces-property-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>L’offre JARVIS</p>
    <h1 data-rev>Un Hub. Vos solutions.<br><em>Rien de plus.</em></h1>
    <p class="lead" data-rev>Un Hub payé une fois. Des solutions par mois, comme des apps. Le matériel de votre lieu.
    Vos données restent chez vous.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/catalogue/">Composer mon JARVIS</a>
      <a class="pill ghost" href="/contact/">Réserver une démo</a>
    </div>
    <ol class="of-trois" data-rev>
      <li><a href="#hub"><i>1</i>Le Hub · dès {_p(CAT.HUBS[0]['prix'])}</a></li>
      <li><a href="#solutions"><i>2</i>Vos solutions · dès 10 $/mois</a></li>
      <li><a href="#materiel"><i>3</i>Le matériel</a></li>
      <li><a href="#installation"><i>4</i>Lieux et installation</a></li>
    </ol>
  </div>
</section>

<section class="sect" id="hub" data-toc="1 · Le Hub" aria-labelledby="hub-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(1)}
      <h2 id="hub-titre">Le Hub JARVIS.<br><em>Trois tailles, un seul logiciel.</em></h2>
    </div>
    <p data-rev>Base, Signature ou Platinum selon la taille de votre lieu. Même app, mêmes solutions; ce qui change,
    c’est la puissance, le nombre d’appareils, l’IA et la sécurité. Un lieu, un Hub; tous vos lieux dans une seule application.</p>
  </div>
  {_hub()}
</section>

<section class="sect alt" id="solutions" data-toc="2 · Vos solutions" aria-labelledby="ext-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(2)}
      <h2 id="ext-titre">Vos solutions.<br><em>Par mois, comme des apps.</em></h2>
    </div>
    <p data-rev>Chaque solution fait un travail précis, dans la même application. Vous prenez seulement ce qui vous sert,
    vous annulez quand vous voulez. Sans elles, JARVIS fonctionne quand même chez vous.</p>
  </div>
  <div class="of-xs">{_solutions()}</div>
</section>

<section class="sect" id="materiel" data-toc="3 · Le matériel" aria-labelledby="mat-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(3)}
      <h2 id="mat-titre">Le matériel<br><em>de votre lieu.</em></h2>
    </div>
    <p data-rev>Payé une fois, prêt à brancher : chaque appareil apparaît tout seul dans l’app. Déjà du Victron, de l’UniFi,
    des caméras ONVIF, un NAS ou Starlink? JARVIS s’y branche au lieu de les remplacer.</p>
  </div>
  <div class="cards of-ms">{_materiel()}</div>
</section>

<section class="sect alt" id="installation" data-toc="4 · Lieux et installation" aria-labelledby="sv-titre">
  <div class="sect-head">
    <div data-rev>
      {_etape(4)}
      <h2 id="sv-titre">Plusieurs lieux,<br><em>l’installation à votre goût.</em></h2>
    </div>
    <p data-rev>Un Hub par lieu, une seule app, et les solutions à −30 % dès le deuxième lieu. Pour l’installation,
    vous choisissez : vous-même, guidé en vidéo, ou on s’en occupe.</p>
  </div>
  <div class="cards of-svs of-inst">{_install()}</div>
  <p class="of-note of-note-svc" data-rev>Il vous faut plus qu’un Hub? Audit de sécurité, test d’intrusion réseau, revue de votre exposition en ligne,
  conformité Loi 25, formation d’équipe : <a href="/catalogue/#lieux">les services professionnels sont dans le catalogue</a>.</p>
</section>

<section class="sect" id="pour-qui" data-toc="Pour qui" aria-labelledby="pq-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Pour qui</p>
      <h2 id="pq-titre">Un point de départ<br><em>pour chaque lieu.</em></h2>
    </div>
    <p data-rev>Des kits prêts à partir, calculés à partir des pièces moins 8 %. Vous partez du kit, puis vous ajustez
    pièce par pièce dans le catalogue.</p>
  </div>
  <div class="of-pfs">{_profils()}</div>
</section>

<section class="sect alt" id="prix" data-toc="Combien ça coûte" aria-labelledby="prix-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Combien ça coûte</p>
      <h2 id="prix-titre">Des prix clairs,<br><em>un total en direct.</em></h2>
    </div>
    <p data-rev>Trois exemples, tirés des kits. Le vôtre se compose dans le catalogue : le panier additionne
    ce que vous payez aujourd’hui et ce que vous payez par mois.</p>
  </div>
  <div class="of-facts">{_factures()}</div>
  <p class="ob-acts" data-rev><a class="pill" href="/catalogue/">Composer mon JARVIS</a>
  <a class="pill ghost" href="/contact/">Demander une visite</a></p>
  <p class="of-note" data-rev>Dollars canadiens, taxes en sus. Points de départ : chaque soumission est confirmée par écrit,
  ligne par ligne. Au Québec, 47 % des réclamations d’assurance habitation sont des dégâts d’eau, à 12 000 $ en moyenne (BAC);
  Diagnostic et continuité coûte 15 $ par mois.</p>
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
  <p data-rev>Composez votre JARVIS en cinq minutes, ou parlons-en.</p>
  <div class="acts" data-rev><a class="pill" href="/catalogue/">Composer mon JARVIS</a>
  <a class="pill ghost" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
