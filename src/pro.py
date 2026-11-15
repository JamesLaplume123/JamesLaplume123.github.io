# Positionnement professionnel et référencement local (novembre 2026).
# Une seule entreprise : JARVIS Private Systems, intégrateur de systèmes intelligents.
#
#   - Données structurées (JSON-LD) : entreprise, site, services, FAQ, fil d'Ariane;
#   - blocs réutilisés : FAQ, fil d'Ariane visible, « Comment on travaille », engagements;
#   - gabarits des pages « par besoin » (src/pages/besoins.py) et des pages locales
#     (src/pages/regions.py).
#
# Règles : rien d'inventé (aucun avis, client, chiffre, permis ou certification). L'entreprise
# n'est jamais présentée comme une agence de sécurité, de gardiennage ou d'investigation.
# Styles : assets/demos/pro.css.

import json
import re

from config import SITE, CAPABILITIES, ZONE, BESOINS_PAGES

D = SITE["domain"]
ENT = D + "/#entreprise"

# Nom court de chaque page pour le fil d'Ariane (les autres : titre avant « | »).
NOMS = {
    "/logiciel/": "Le logiciel",
    "/offre/": "L’offre",
    "/catalogue/": "Catalogue et prix",
    "/solutions/": "Solutions",
    "/plateforme/": "Le Hub et l’IA privée",
    "/laboratoire-mobile/": "Laboratoire mobile",
    "/vision-roadmap/": "Vision et feuille de route",
    "/recherche/": "Recherche",
    "/confiance/": "Confiance",
    "/a-propos/": "À propos",
    "/contact/": "Contact",
    "/confidentialite/": "Confidentialité",
    "/mentions-legales/": "Mentions légales",
    "/questions/": "Questions avant d’appeler",
    "/regions/": "Régions desservies",
}
NOMS.update({f"/solutions/{c['slug']}/": c["title"] for c in CAPABILITIES})
NOMS.update({f"/solutions/{k}/": n for k, n in BESOINS_PAGES})
NOMS.update({f"/regions/{k}/": n for k, n in ZONE})

PARENTS = {"/solutions/": "/solutions/", "/regions/": "/regions/"}


def _texte(html):
    """Texte brut d'une réponse (pour les données structurées)."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


# ---------------------------------------------------------------------------
# Fil d'Ariane
# ---------------------------------------------------------------------------
def miettes(page):
    """[(nom, url)] de l'accueil jusqu'à la page. Vide pour l'accueil et les pages hors index."""
    url = page["url"]
    if url == "/" or url.endswith(".html") or page.get("noindex") or page.get("lang") == "en":
        return []
    out = [("Accueil", "/")]
    for racine in PARENTS:
        if url.startswith(racine) and url != racine:
            out.append((NOMS[racine], racine))
    out.append((NOMS.get(url) or page["title"].split(" | ")[0], url))
    return out


def fil(url):
    """Fil d'Ariane visible, en tête des nouvelles pages."""
    m = miettes({"url": url, "title": NOMS[url]})
    liens = "".join(f'<a href="{u}">{n}</a><i aria-hidden="true">›</i>' for n, u in m[:-1])
    return f'<nav class="fil" aria-label="Fil d’Ariane" data-rev>{liens}<span aria-current="page">{m[-1][0]}</span></nav>'


def ld_fil(page):
    m = miettes(page)
    if not m:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": D + u} for i, (n, u) in enumerate(m)
        ],
    }


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
ZONE_LD = [
    {"@type": "City", "name": n} for n in (
        "Saint-Hyacinthe", "Granby", "Drummondville", "Longueuil", "Saint-Jean-sur-Richelieu",
        "Sorel-Tracy", "Beloeil", "Mont-Saint-Hilaire", "Acton Vale",
    )
] + [{"@type": "AdministrativeArea", "name": "Montérégie"}]


def ld_service(nom, description, url, genre, zone=None):
    """Un service de l'entreprise (solution, page par besoin ou page locale)."""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": D + url + "#service",
        "name": nom,
        "serviceType": genre,
        "description": description,
        "url": D + url,
        "provider": {"@id": ENT},
        "areaServed": zone or ZONE_LD,
    }


def ld_entreprise():
    """L'entreprise : seulement ce qui existe réellement (aucun téléphone, aucune adresse civique)."""
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": ENT,
        "name": SITE["name"],
        "alternateName": "JARVIS",
        "slogan": SITE["phrase"],
        "url": D + "/",
        "logo": D + "/apple-touch-icon.png",
        "image": D + SITE["og_image"],
        "email": SITE["email"],
        "description": (
            "Intégrateur de systèmes intelligents basé dans la région de Saint-Hyacinthe. "
            "Domotique, réseau, caméras et serrures connectées, automatisation et IA privée "
            "réunis dans un seul système installé chez le client : maisons, fermes, "
            "entreprises et véhicules, en Montérégie."
        ),
        "founder": {"@type": "Person", "name": "James Laplume"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Saint-Hyacinthe",
            "addressRegion": "QC",
            "addressCountry": "CA",
        },
        "areaServed": ZONE_LD,
        "knowsAbout": [
            "Domotique",
            "Maison intelligente",
            "Home Assistant",
            "Zigbee, Z-Wave et Matter",
            "Domotique agricole",
            "Réseau et Wi-Fi",
            "Cybersécurité résidentielle et de PME",
            "Intégration de caméras et de serrures connectées",
            "Automatisation d’entreprise",
            "Intelligence artificielle locale",
            "Systèmes électriques 12 V de véhicules récréatifs",
            "Énergie solaire et batteries LiFePO4",
            "Loi 25 (protection des renseignements personnels)",
        ],
        "availableLanguage": ["fr", "en"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Solutions JARVIS",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "@id": f"{D}/solutions/{c['slug']}/#service",
                        "name": c["title"],
                        "description": c["short"],
                        "url": f"{D}/solutions/{c['slug']}/",
                    },
                }
                for c in CAPABILITIES
            ],
        },
    }


def ld_site():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": D + "/#site",
        "name": SITE["name"],
        "url": D + "/",
        "inLanguage": "fr-CA",
        "publisher": {"@id": ENT},
    }


def ld_faq(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": _texte(q), "acceptedAnswer": {"@type": "Answer", "text": _texte(a)}}
            for q, a in faq
        ],
    }


def ld_script(objets):
    """Un seul bloc JSON-LD par page, placé dans le <head>."""
    objets = [o for o in objets if o]
    if not objets:
        return ""
    corps = json.dumps(objets if len(objets) > 1 else objets[0], ensure_ascii=False, indent=1)
    return '\n<script type="application/ld+json">\n' + corps.replace("</", "<\\/") + "\n</script>"


# ---------------------------------------------------------------------------
# Blocs réutilisés
# ---------------------------------------------------------------------------
def faq_items(faq):
    return "".join(
        f"""<details class="faq-item" data-rev>
      <summary><span>{q}</span><i aria-hidden="true"></i></summary>
      <div class="faq-a"><p>{a}</p></div>
    </details>"""
        for q, a in faq
    )


def faq_section(faq, eyebrow, titre, ident="questions", toc=""):
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""<section class="faq" id="{ident}"{toc_attr} aria-labelledby="{ident}-titre">
  <div class="head" data-rev>
    <p class="eyebrow">{eyebrow}</p>
    <h2 id="{ident}-titre">{titre}</h2>
  </div>
  <div class="faq-list">{faq_items(faq)}</div>
</section>"""


ETAPES = [
    ("Visite et écoute",
     "On se déplace chez vous. On regarde ce qui est déjà en place et on écoute ce qui vous dérange "
     "vraiment. C’est gratuit et sans engagement."),
    ("Plan et soumission écrite",
     "Vous recevez un plan clair : ce qu’on relie, ce qu’on ajoute, ce qui peut attendre. Le prix est "
     "écrit ligne par ligne, avant toute décision."),
    ("Installation",
     "Sur place, proprement, en réutilisant vos appareils quand c’est possible. Chaque règle est "
     "essayée avec vous avant qu’on parte."),
    ("Formation",
     "Les personnes qui vivent ou travaillent dans le lieu apprennent à s’en servir, à leur rythme, "
     "sur leur propre téléphone."),
    ("Suivi",
     "Entretien, mises à jour et réglages quand vos besoins changent, avec une personne qui connaît "
     "votre installation."),
]


def comment_on_travaille(ident="comment-on-travaille", toc="Comment on travaille", alt=True):
    cartes = "".join(
        f'<article class="card" data-rev><small>Étape {i + 1} sur 5</small><h3>{t}</h3><p>{p}</p></article>'
        for i, (t, p) in enumerate(ETAPES)
    )
    return f"""<section class="sect{' alt' if alt else ''}" id="{ident}" data-toc="{toc}" aria-labelledby="{ident}-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Comment on travaille</p>
      <h2 id="{ident}-titre" style="margin-top:1rem">Cinq étapes.<br><em>Aucune surprise.</em></h2>
    </div>
    <p data-rev>Voici comment se déroule un projet, de la première visite au suivi : vous savez
    toujours où on en est, ce qui est prévu et ce que ça coûte. Aucune pression : on avance à votre
    rythme.</p>
  </div>
  <div class="cards">{cartes}
    <article class="card pro-go" data-rev><small>En phase de lancement</small><h3>On choisit quelques premiers projets.</h3>
    <p>Décrivez votre lieu en quelques lignes, ou laissez simplement votre nom pour rester informé.</p>
    <p class="pro-go-a"><a class="pill" href="/contact/">Parlons de votre projet</a></p></article>
  </div>
</section>"""


ENGAGEMENTS = [
    ("Vos données restent chez vous",
     "Le système fonctionne sur un boîtier installé dans votre lieu. Rien n’est vendu, et rien ne sort "
     "sans votre accord."),
    ("Soumission gratuite et écrite",
     "Après la visite, le prix est détaillé ligne par ligne. Vous décidez maintenant, plus tard ou pas "
     "du tout."),
    ("Un système documenté, remis au client",
     "Le plan, la liste des appareils, les règles et vos accès vous sont remis par écrit. Votre "
     "installation vous appartient."),
    ("La Loi 25 respectée",
     "On recueille le minimum de renseignements personnels, on vous dit où ils sont gardés et qui y a "
     "accès, comme l’exige la loi québécoise."),
    ("Vous gardez la décision",
     "Déverrouiller une porte ou ouvrir un garage demande toujours votre confirmation. Le système "
     "propose; vous approuvez."),
    ("L’heure juste",
     "L’entreprise est en démarrage. On vous montre ce qui fonctionne aujourd’hui et on vous dit "
     "clairement ce qui n’est pas encore prêt."),
]


def engagements(ident="engagements", toc="Nos engagements", alt=False):
    cartes = "".join(
        f'<article class="card" data-rev><small>Engagement {i + 1:02d}</small><h3>{t}</h3><p>{p}</p></article>'
        for i, (t, p) in enumerate(ENGAGEMENTS)
    )
    return f"""<section class="sect{' alt' if alt else ''}" id="{ident}" data-toc="{toc}" aria-labelledby="{ident}-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Nos engagements</p>
      <h2 id="{ident}-titre" style="margin-top:1rem">Ce que vous pouvez<br><em>exiger de nous.</em></h2>
    </div>
    <p data-rev>Six engagements concrets, écrits ici pour que vous puissiez nous les rappeler.
    Le détail : <a href="/confiance/">confiance</a>, <a href="/confidentialite/">confidentialité</a>
    et <a href="/mentions-legales/">mentions légales</a>.</p>
  </div>
  <div class="cards">{cartes}</div>
</section>"""


def un_systeme(ident="un-systeme", toc="Un seul système", alt=True):
    """Les pièces d'UN système (pas sept métiers) : porte d'entrée, même installation, fondation, différence."""
    pieces = [
        ("La porte d’entrée", "La domotique", "/solutions/environnements-intelligents/",
         "Lumières, chauffage, énergie et appareils réunis sur un seul écran. C’est par là que la plupart "
         "des clients commencent."),
        ("La même installation", "Caméras, serrures et capteurs", "/solutions/securite-intelligente/",
         "Ils se relient au même système : une seule application, des événements clairs, des images "
         "gardées chez vous."),
        ("La fondation", "Le réseau", "/solutions/reseau-resilience/",
         "Un Wi-Fi qui couvre partout et des zones séparées. Sans un réseau solide, rien d’autre ne "
         "tient."),
        ("La différence", "L’IA privée", "/solutions/ia-privee-connaissances/",
         "Une intelligence artificielle qui fonctionne sur votre boîtier. Vos documents et vos images "
         "ne partent pas chez un géant du Web."),
    ]
    cartes = "".join(
        f'<a class="card" href="{u}" data-rev><small>{k}</small><h3>{t}</h3><p>{p}</p></a>' for k, t, u, p in pieces
    )
    return f"""<section class="sect{' alt' if alt else ''}" id="{ident}" data-toc="{toc}" aria-labelledby="{ident}-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Un seul système</p>
      <h2 id="{ident}-titre" style="margin-top:1rem">Quatre pièces.<br><em>Une seule installation.</em></h2>
    </div>
    <p data-rev>JARVIS Private Systems fait un seul métier : intégrer. Tout ce qu’on installe se parle
    et se pilote au même endroit. L’automatisation d’entreprise, le diagnostic et la mobilité
    s’ajoutent ensuite, selon vos besoins : <a href="/solutions/">les sept solutions</a>.</p>
  </div>
  <div class="cards two">{cartes}</div>
</section>"""


def zone_liens(sauf=""):
    """Liens vers les pages locales (maillage interne)."""
    return "".join(
        f'<a class="chip" href="/regions/{k}/">{n}</a>' for k, n in ZONE if k != sauf
    )


# ---------------------------------------------------------------------------
# Pages de solution : questions fréquentes et données structurées (ajoutées par partials.py)
# ---------------------------------------------------------------------------
_PERMIS = (
    "Au Québec, la pose de systèmes d’alarme, de caméras de surveillance et de contrôles d’accès chez "
    "un client est encadrée par la Loi sur la sécurité privée. Quand un permis est requis, cette "
    "partie doit être faite par un installateur qui le détient; JARVIS relie ensuite ces appareils "
    "au système et à l’application."
)
_PAS_AGENCE = (
    "Non. JARVIS Private Systems est un intégrateur de systèmes intelligents : on installe et on "
    "relie des technologies chez nos clients. L’entreprise n’offre ni gardiennage, ni agents, ni "
    "enquête, ni centrale de télésurveillance. « Private », dans notre nom, renvoie à la vie privée : "
    "vos données restent chez vous."
)

SOLUTIONS_FAQ = {
    "environnements-intelligents": [
        ("Quelles marques d’appareils sont compatibles?",
         "JARVIS s’appuie sur Home Assistant et sur les standards ouverts Zigbee, Z-Wave, Matter et "
         "MQTT. La plupart des thermostats, interrupteurs, prises, capteurs et serrures connectés du "
         "marché peuvent donc être reliés. On vérifie vos appareils un par un pendant la visite."),
        ("La domotique fonctionne-t-elle sans Internet?",
         "Oui. Les règles et l’application tournent sur le Hub, dans votre maison : une panne "
         "d’Internet n’arrête ni l’éclairage, ni le chauffage, ni vos ambiances. Pendant une panne de "
         "courant, seuls les appareils alimentés par une batterie ou une génératrice continuent."),
        ("Peut-on rendre intelligente une maison existante sans ouvrir les murs?",
         "Souvent, oui. Beaucoup de modules sans fil se posent derrière les interrupteurs existants, et "
         "des thermostats connectés remplacent ceux des plinthes électriques. Quand des travaux "
         "électriques sont nécessaires, ils sont faits par un maître électricien."),
    ],
    "ia-privee-connaissances": [
        ("Mes documents sont-ils envoyés à un service d’IA en ligne?",
         "Pas par défaut. L’IA fonctionne sur le Hub, chez vous. Un service externe n’est utilisé que "
         "si vous l’autorisez, pour une tâche précise."),
        ("L’IA peut-elle se tromper?",
         "Oui, comme toute IA. C’est pourquoi chaque réponse montre le passage du document qui la "
         "justifie : vous vérifiez en un clic au lieu de croire sur parole."),
        ("Quel matériel faut-il?",
         "L’IA tourne sur le Hub. Sa puissance se choisit selon le nombre de personnes et la quantité "
         "de documents; on le détermine avec vous pendant la visite."),
    ],
    "securite-intelligente": [
        ("JARVIS Private Systems est-il une agence de sécurité?", _PAS_AGENCE),
        ("Où sont gardées les images de mes caméras?",
         "Sur place, sur votre Hub ou sur un enregistreur dans votre bâtiment, aussi longtemps que vous "
         "le décidez. Aucune image n’est envoyée à un service en ligne sans votre accord, et personne "
         "chez nous ne les regarde."),
        ("Qui installe les caméras, l’alarme et les serrures?", _PERMIS),
    ],
    "automatisation-operations": [
        ("Dois-je changer mes logiciels?",
         "En général, non. On part des outils que vous utilisez déjà (courriel, agenda, téléphonie, "
         "comptabilité) et on les relie quand ils le permettent. La visite sert à le vérifier."),
        ("La réceptionniste remplace-t-elle mon personnel?",
         "Non. Elle prend les appels que personne ne peut prendre, note les messages, propose un "
         "rendez-vous et transfère les urgences selon vos règles. Vos employés gardent les décisions."),
        ("Pour quelles entreprises est-ce fait?",
         "Les PME, les commerces, les ateliers, les bureaux de professionnels et les fermes de la "
         "Montérégie qui perdent du temps à recopier les mêmes informations d’un outil à l’autre."),
    ],
    "reseau-resilience": [
        ("Pourquoi mon Wi-Fi est-il lent ou instable à certains endroits?",
         "Le plus souvent, un seul routeur tente de couvrir tout le bâtiment à travers les murs et les "
         "planchers. La solution durable : des points d’accès bien placés, reliés par câble, et un "
         "réseau séparé pour les objets connectés."),
        ("Peut-on relier plusieurs bâtiments, comme la maison, le garage et l’étable?",
         "Oui. Selon la distance et le terrain : un câble enterré, de la fibre optique ou un lien sans "
         "fil de bâtiment à bâtiment. Chaque bâtiment reçoit ensuite sa propre couverture Wi-Fi."),
        ("Que se passe-t-il quand Internet tombe?",
         "Ce qui est local continue de fonctionner : domotique, caméras, application à la maison. Un "
         "lien de secours, cellulaire ou par satellite, peut prendre le relais pour l’essentiel."),
    ],
    "diagnostic-care": [
        ("JARVIS répare-t-il les équipements?",
         "Non. JARVIS trouve ce qui a changé, rassemble les mesures et prépare un dossier clair pour le "
         "bon technicien, qui arrive en sachant quoi vérifier."),
        ("Quels équipements peut-on suivre?",
         "Ceux qu’on peut mesurer : température, consommation électrique, débit d’eau, batteries, "
         "pompes, réfrigération, chauffage. Un capteur s’ajoute quand l’équipement n’en a pas."),
        ("Faut-il déjà avoir un Hub JARVIS?",
         "Oui. Le diagnostic s’appuie sur les mesures que le Hub garde jour après jour; c’est une "
         "extension qui s’ajoute à une installation."),
    ],
    "mobilite": [
        ("Quels véhicules peut-on relier?",
         "Les VR et les véhicules aménagés, les voitures qui offrent une connexion du constructeur, "
         "les véhicules électriques et les vélos électriques. Chaque commande à distance demande "
         "votre confirmation."),
        ("Le système fonctionne-t-il sans réseau cellulaire?",
         "À bord, oui : le tableau du véhicule (batteries, eau, chauffage) tourne sur le Hub du "
         "véhicule. Les suggestions de route et la météo demandent une connexion."),
        ("Reliez-vous les batteries et le solaire d’un VR?",
         "Oui : batteries, panneaux solaires, réservoirs et chauffage sont réunis sur le tableau "
         "JARVIS. Le laboratoire mobile de l’entreprise, une ambulance convertie, sert de banc d’essai."),
    ],
}

_SLUGS = {c["slug"]: c for c in CAPABILITIES}


def _solution(page):
    slug = page["url"].strip("/").split("/")[-1]
    return _SLUGS.get(slug) if page["url"].startswith("/solutions/") else None


def solution_faq(page):
    """Section FAQ d'une page de solution (insérée avant l'appel final)."""
    c = _solution(page)
    if not c:
        return ""
    return faq_section(SOLUTIONS_FAQ[c["slug"]], f"Questions fréquentes · {c['title']}",
                       "Ce qu’on nous demande <em>le plus souvent.</em>", ident="questions", toc="Questions")


def schemas(page):
    """Toutes les données structurées d'une page : les siennes, sa solution, son fil d'Ariane."""
    out = list(page.get("schema", []))
    c = _solution(page)
    if c:
        out.append(ld_service(c["title"], c["short"], page["url"], c["label"]))
        out.append(ld_faq(SOLUTIONS_FAQ[c["slug"]]))
    out.append(ld_fil(page))
    return out
