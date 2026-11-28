# Positionnement professionnel et référencement local (novembre 2026).
# Une seule entreprise : JARVIS Private Systems, entreprise de technologie et de sécurité.
# JARVIS est son produit; le fil conducteur est « protéger » : les lieux, le réseau, les données.
#
#   - Données structurées (JSON-LD) : entreprise, site, services, FAQ, fil d'Ariane;
#   - blocs réutilisés : FAQ, fil d'Ariane visible, « Comment on travaille », engagements;
#   - gabarit des pages « par besoin » (src/pages/besoins.py).
# Aucune mention de lieu ni de zone desservie (décision de James, novembre 2026).
#
# Règles : rien d'inventé (aucun avis, client, chiffre, permis ou certification). L'entreprise
# n'est jamais présentée comme une agence de sécurité, de gardiennage ou d'investigation, ni
# comme une centrale de surveillance; « sécurité privée » n'est jamais une activité offerte.
# Styles : assets/demos/pro.css.

import json
import re

from config import SITE, CAPABILITIES, BESOINS_PAGES

D = SITE["domain"]
ENT = D + "/#entreprise"

# Prix publics ou non (SITE["prix_publics"]) : une seule phrase remplace tout montant pendant le lancement.
PRIX = SITE["prix_publics"]
SOUMISSION = "Prix sur soumission, confirmé par écrit avant tout achat."
# Phrase des questions fréquentes qui renvoie au configurateur.
VOIR_CATALOGUE = ' Vous pouvez déjà <a href="/offre/#composer">composer votre forfait</a>.' 

# Nom court de chaque page pour le fil d'Ariane (les autres : titre avant « | »).
NOMS = {
    "/logiciel/": "Le logiciel",
    "/offre/": "L’offre",
    "/solutions/": "Solutions",
    "/plateforme/": "L’appareil",
    "/laboratoire-mobile/": "Laboratoire mobile",
    "/vision-roadmap/": "Vision",
    "/recherche/": "Recherche",
    "/confiance/": "Confiance",
    "/a-propos/": "À propos",
    "/contact/": "Contact",
    "/confidentialite/": "Confidentialité",
    "/mentions-legales/": "Mentions légales",
    "/questions/": "Questions",
    "/plan-du-site/": "Plan du site",
    "/solutions/cyber/": "JARVIS Cyber",
    "/pourquoi-jarvis/": "Pourquoi JARVIS",
}
NOMS.update({f"/solutions/{c['slug']}/": c["title"] for c in CAPABILITIES})
NOMS.update({f"/solutions/{k}/": n for k, n in BESOINS_PAGES})

# Page mère de chaque page intérieure (fil d'Ariane) : les solutions sous Solutions, les pages de l'entreprise sous À propos.
MERES = {"/vision-roadmap/": "/a-propos/", "/laboratoire-mobile/": "/a-propos/",
         "/plateforme/": "/a-propos/", "/confiance/": "/a-propos/", "/questions/": "/a-propos/",
         "/recherche/": "/a-propos/", "/pourquoi-jarvis/": "/a-propos/"}


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
    mere = MERES.get(url) or ("/solutions/" if url.startswith("/solutions/") and url != "/solutions/" else None)
    if mere:
        out.append((NOMS[mere], mere))
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
def ld_service(nom, description, url, genre):
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
    }


def ld_entreprise():
    """L'entreprise : seulement ce qui existe réellement (aucun téléphone, aucune adresse civique)."""
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": ENT,
        "name": SITE["name"],
        "alternateName": "JARVIS",
        "slogan": SITE["signature"],
        "url": D + "/",
        "logo": D + "/apple-touch-icon.png",
        "image": D + SITE["og_image"],
        "email": SITE["email"],
        "description": (
            "Entreprise de technologie et de sécurité. "
            "Elle conçoit et installe JARVIS, un système privé qui gère et protège les maisons, "
            "les fermes, les entreprises et les véhicules : domotique, réseau et "
            "cybersécurité, caméras et serrures connectées, et IA privée dont les données "
            "restent chez le client."
        ),
        "founder": {"@type": "Person", "name": "James Laplume"},
        "knowsAbout": [
            "Cybersécurité résidentielle et de PME",
            "Réseau et Wi-Fi",
            "Domotique",
            "IA privée et locale",
            "Maison intelligente",
            "Home Assistant",
            "Zigbee, Z-Wave et Matter",
            "Domotique agricole",
            "Logiciel de caméras et de serrures connectées",
            "Automatisation d’entreprise",
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
    <p data-rev>De la première visite au suivi : vous savez toujours où on en est.</p>
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
     "accès, comme l’exige la loi."),
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
    <p data-rev>Six engagements concrets, écrits ici pour que vous puissiez nous les rappeler.</p>
  </div>
  <div class="cards">{cartes}</div>
</section>"""


# ---------------------------------------------------------------------------
# Pages de solution : questions fréquentes et données structurées (ajoutées par partials.py)
# ---------------------------------------------------------------------------
_PERMIS = (
    "La pose de systèmes d’alarme, de caméras de surveillance et de contrôles d’accès chez "
    "un client est encadrée par la Loi sur la sécurité privée. Quand un permis est requis, cette "
    "partie doit être faite par un installateur qui le détient; JARVIS relie ensuite ces appareils "
    "au système et à l’application."
)
_PAS_AGENCE = (
    "Non. JARVIS Private Systems est une entreprise de technologie et de sécurité : la sécurité "
    "dont on parle est celle de votre système, c’est-à-dire vos lieux reliés par le logiciel, votre "
    "réseau et vos données. L’entreprise n’offre ni gardiennage, ni agents, ni enquête, ni centrale "
    "de télésurveillance. « Private », dans notre nom, renvoie à la vie privée : vos données "
    "restent chez vous."
)

SOLUTIONS_FAQ = {
    "environnements-intelligents": [
        ("Quelles marques d’appareils sont compatibles?",
         "JARVIS s’appuie sur Home Assistant et sur les standards ouverts Zigbee, Z-Wave, Matter et "
         "MQTT. La plupart des thermostats, interrupteurs, prises, capteurs et serrures connectés du "
         "marché peuvent donc être reliés. On vérifie vos appareils un par un pendant la visite."),
        ("La domotique fonctionne-t-elle sans Internet?",
         "Oui. Les règles et l’application tournent sur votre JARVIS, dans votre maison : une panne "
         "d’Internet n’arrête ni l’éclairage, ni le chauffage, ni vos ambiances. Pendant une panne de "
         "courant, seuls les appareils alimentés par une batterie ou une génératrice continuent."),
        ("Peut-on rendre intelligente une maison existante sans ouvrir les murs?",
         "Souvent, oui. Beaucoup de modules sans fil se posent derrière les interrupteurs existants, et "
         "des thermostats connectés remplacent ceux des plinthes électriques. Quand des travaux "
         "électriques sont nécessaires, ils sont faits par un maître électricien."),
    ],
    "ia-privee-connaissances": [
        ("Mes documents sont-ils envoyés à un service d’IA en ligne?",
         "Pas par défaut. L’IA fonctionne sur votre JARVIS, chez vous. Un service externe n’est utilisé que "
         "si vous l’autorisez, pour une tâche précise."),
        ("L’IA peut-elle se tromper?",
         "Oui, comme toute IA. C’est pourquoi chaque réponse montre le passage du document qui la "
         "justifie : vous vérifiez en un clic au lieu de croire sur parole."),
        ("Quel matériel faut-il?",
         "L’IA tourne sur votre JARVIS. Sa puissance se choisit selon le nombre de personnes et la quantité "
         "de documents; on le détermine avec vous pendant la visite."),
    ],
    "securite-intelligente": [
        ("JARVIS Private Systems est-il une agence de sécurité?", _PAS_AGENCE),
        ("Où sont gardées les images de mes caméras?",
         "Sur place, sur votre JARVIS ou sur un enregistreur dans votre bâtiment, aussi longtemps que vous "
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
         "Les PME, les commerces, les ateliers, les bureaux de professionnels et les fermes qui perdent du temps à recopier les mêmes informations d’un outil à l’autre."),
        ("JARVIS se branche-t-il sur notre Microsoft 365 ou notre Active Directory?",
         "Oui, c’est compris dans le Socle Entreprise. Vos employés entrent dans JARVIS avec leur compte "
         "de travail, et un compte désactivé perd d’un coup ses portes, ses caméras et ses documents. "
         "JARVIS ne remplace pas votre annuaire et ne gère pas vos postes de travail."),
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
        ("Faut-il déjà avoir un appareil JARVIS?",
         "Oui. Le diagnostic s’appuie sur les mesures que votre JARVIS garde jour après jour; c’est une "
         "extension qui s’ajoute à une installation."),
    ],
    "mobilite": [
        ("Quels véhicules peut-on relier?",
         "Les VR et les véhicules aménagés, les voitures qui offrent une connexion du constructeur, "
         "les véhicules électriques et les vélos électriques. Chaque commande à distance demande "
         "votre confirmation."),
        ("Le système fonctionne-t-il sans réseau cellulaire?",
         "À bord, oui : le tableau du véhicule (batteries, eau, chauffage) tourne sur le JARVIS du "
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
    return faq_section(SOLUTIONS_FAQ[c["slug"]], c["title"], "Questions fréquentes")


def schemas(page):
    """Toutes les données structurées d'une page : les siennes, sa solution, son fil d'Ariane."""
    out = list(page.get("schema", []))
    c = _solution(page)
    if c:
        out.append(ld_service(c["title"], c["short"], page["url"], c["label"]))
        out.append(ld_faq(SOLUTIONS_FAQ[c["slug"]]))
    out.append(ld_fil(page))
    return out
