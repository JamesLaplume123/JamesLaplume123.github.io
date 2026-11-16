# Accueil — impressionner en cinq secondes, se lire en trente (refonte « présence », novembre 2026).
# Six sections, chacune portée par une image ou une scène :
#   1. héros vivant : la photo de la résidence réagit (assets/demos/accueil.js, shader WebGL);
#   2. ce que nous faisons : les sept solutions en bande de photos;
#   3. le logiciel : l'aperçu vivant de JARVIS App (démo complète sur /logiciel/);
#   4. pour qui et où : cinq lieux en photos, carte noire de la Montérégie (src/carte_region.py);
#   5. comment on travaille : cinq étapes sur une ligne du temps (détail sur /a-propos/);
#   6. fin : trois questions clés et l'appel « Parlons de votre projet ».
# Les questions affichées alimentent les données structurées (FAQPage); les autres vivent sur /questions/.
# Styles et scripts : assets/demos/accueil.css et accueil.js.

import json

from config import SITE, CAPABILITIES
from demos import app
import carte_region
import pro


FAQ = [
    (
        "Que fait JARVIS Private Systems, concrètement?",
        "JARVIS Private Systems est un intégrateur de systèmes intelligents. On installe et on relie, "
        "dans un seul système, ce qui rend un lieu intelligent et sécurisé : la domotique, le réseau, "
        "les caméras et serrures connectées, et une IA privée. Tout passe par un petit boîtier "
        "silencieux installé chez vous, le JARVIS Hub, et par une seule application. Le système "
        "propose des actions; vous gardez la décision.",
    ),
    (
        "Mes données quittent-elles la maison ou l’entreprise?",
        "Pas par défaut. Tout vit sur le Hub, chez vous, et aucun abonnement au nuage n’est "
        "nécessaire. L’interface et les automatisations continuent de fonctionner sans Internet; "
        "le nuage ne sert qu’à ce que vous choisissez, comme un accès à distance par un relais qui "
        "ne garde rien ou une copie de sauvegarde chiffrée.",
    ),
    (
        "Est-ce disponible aujourd’hui, et combien ça coûte?",
        "L’entreprise est en phase de lancement : nous prenons les noms des personnes intéressées "
        "et choisissons quelques premiers projets. Le logiciel JARVIS est en construction : son "
        "noyau (comptes, droits, sécurité) est en développement et le tableau JARVIS Signature "
        "fonctionne déjà sur Home Assistant. Le prix dépend de votre lieu et de ce qu’on relie; "
        "il est toujours remis par écrit, après une visite gratuite.",
    ),
]

FAQ_HTML = pro.faq_items(FAQ)

# --- 1. Héros vivant --------------------------------------------------------------------------
# La photo montre tout allumé; éteindre une lumière assombrit seulement ses zones (cx, cy, rx, ry
# en fractions de la photo). La porte du garage remonte et laisse voir un intérieur (autre photo).
HEROS = {
    "img": "/media/vitrine/accueil/residence-prestige-soir.webp",
    "ratio": [1672, 941],
    "inside": "/media/accueil/garage-interieur.webp",
    "door": [0.088, 0.497, 0.293, 0.497, 0.728, 0.735],  # gauche, haut G, droite, haut D, bas D, bas G
    "crop": [0.36, 0.30, 0.86, 0.80],
    "spots": [
        {"id": "etage", "label": "Étage", "on": "Allumé", "off": "Éteint", "x": 64.5, "y": 29,
         "zones": [[0.655, 0.31, 0.105, 0.13], [0.40, 0.28, 0.075, 0.08]]},
        {"id": "salon", "label": "Salon", "on": "Allumé", "off": "Éteint", "x": 61.5, "y": 56,
         "zones": [[0.655, 0.545, 0.105, 0.12], [0.66, 0.69, 0.09, 0.03], [0.63, 0.83, 0.10, 0.09]]},
        {"id": "entree", "label": "Entrée", "on": "Allumée", "off": "Éteinte", "x": 43.6, "y": 53,
         "zones": [[0.41, 0.55, 0.07, 0.13], [0.44, 0.41, 0.11, 0.03], [0.32, 0.54, 0.025, 0.06],
                   [0.42, 0.70, 0.09, 0.035], [0.42, 0.84, 0.10, 0.08], [0.50, 0.55, 0.035, 0.11]]},
        {"id": "garage", "label": "Garage", "on": "Ouvert", "off": "Fermé", "x": 19, "y": 61, "door": True},
    ],
}


def _heros():
    spots = "".join(
        f'<button type="button" class="ac-spot" data-ac-spot="{s["id"]}" aria-pressed="{"false" if s.get("door") else "true"}">'
        f'<i aria-hidden="true"></i><span><b>{s["label"]}</b><em data-ac-etat>{s["off"] if s.get("door") else s["on"]}</em></span></button>'
        for s in HEROS["spots"]
    )
    w, h = HEROS["ratio"]
    return f"""<section class="ac-hero" data-ac-hero aria-labelledby="ac-titre">
  <div class="ac-view" data-ac-view>
    <img class="ac-ph" src="{HEROS["img"]}" width="{w}" height="{h}" fetchpriority="high"
         alt="Résidence contemporaine au crépuscule, fenêtres éclairées, dont les lumières et la porte de garage sont pilotées par JARVIS">
    <canvas class="ac-gl" data-ac-gl aria-hidden="true"></canvas>
    <div class="ac-spots" role="group" aria-label="Démonstration : commandes de la maison">{spots}</div>
  </div>
  <div class="ac-hero-in">
    <h1 id="ac-titre">Des lieux intelligents et sécurisés.</h1>
    <div class="ac-hero-bas">
      <p class="ac-phrase">{SITE["phrase"]}</p>
      <div class="ac-acts">
        <a class="pill" href="/logiciel/">Voir le logiciel</a>
        <a class="pill ghost" href="/contact/">Parlons de votre projet</a>
      </div>
    </div>
    <p class="ac-lanc"><i aria-hidden="true"></i><span>{SITE["lancement"]}</span>
      <a href="/contact/">Rester informé</a></p>
  </div>
  <p class="ac-demo" data-ac-demo aria-hidden="true">Démonstration : touchez un point de la maison</p>
  <script type="application/json" data-ac-data>{json.dumps(HEROS, ensure_ascii=False, separators=(",", ":"))}</script>
</section>"""


# --- 2. Ce que nous faisons : les sept solutions, dans l'ordre officiel -----------------------
# (solution, photo, cadrage, une ligne, [(page de service liée, libellé)])
SOLUTIONS = [
    ("environnements-intelligents", "sol-environnements", "32% 50%",
     "Lumières, chauffage et énergie sur un seul écran.",
     [("maison-intelligente-cle-en-main", "Maison clé en main"), ("domotique-ferme-agricole", "Ferme")]),
    ("ia-privee-connaissances", "sol-ia", "74% 50%",
     "Une IA qui lit vos documents, chez vous.",
     [("ia-privee-entreprise", "En entreprise")]),
    ("securite-intelligente", "sol-securite", "13% 50%",
     "Caméras, portes et alarme dans un seul fil.", []),
    ("automatisation-operations", "sol-automatisation", "47% 50%",
     "Demandes et approbations qui avancent seules.", []),
    ("reseau-resilience", "sol-reseau", "40% 50%",
     "Un Wi-Fi solide, partout, bien protégé.", []),
    ("diagnostic-care", "sol-diagnostic", "60% 50%",
     "La panne repérée avant le bris.", []),
    ("mobilite", "sol-mobilite", "72% 50%",
     "Le VR et les véhicules, suivis de partout.", []),
]
_TITRES = {c["slug"]: c["title"] for c in CAPABILITIES}


def _solutions():
    cartes = ""
    for slug, img, pos, ligne, services in SOLUTIONS:
        plus = "".join(f'<a href="/solutions/{k}/">{n}</a>' for k, n in services)
        plus = f'<span class="ac-sol-plus">{plus}</span>' if plus else ""
        cartes += f"""<article class="ac-sol{'' if cartes else ' is-on'}">
      <img src="/media/accueil/{img}.webp" alt="" loading="lazy" style="object-position:{pos}">
      <div class="ac-sol-t">
        <h3><a class="ac-sol-a" href="/solutions/{slug}/">{_TITRES[slug]}</a></h3>
        <p>{ligne}</p>{plus}
      </div>
    </article>"""
    return f"""<section class="ac-sect ac-faire" id="solutions" aria-labelledby="ac-faire-titre">
  <div class="ac-tete">
    <h2 id="ac-faire-titre">Sept solutions, un seul système.</h2>
    <a class="ac-lien" href="/solutions/">Comparer les sept solutions</a>
  </div>
  <div class="ac-sols" data-ac-sols>{cartes}</div>
</section>"""


# --- 3. Le logiciel ---------------------------------------------------------------------------
def _logiciel():
    return f"""<section class="ac-sect ac-log" id="logiciel" aria-labelledby="ac-log-titre">
  <div class="ac-tete">
    <div>
      <h2 id="ac-log-titre">Une seule application.</h2>
      <p>L’écran d’accueil de JARVIS, en direct : l’heure et la météo sont réelles.</p>
    </div>
    <a class="pill" href="/logiciel/">Essayer le logiciel</a>
  </div>
  <div class="ac-scene">
    <div class="ac-ecran">
      <div class="ac-dev" inert>{app.apercu()}</div>
      <a class="ac-ecran-a" href="/logiciel/" aria-label="Essayer le logiciel JARVIS" tabindex="-1"></a>
    </div>
  </div>
</section>"""


# --- 4. Pour qui et où ------------------------------------------------------------------------
LIEUX = [
    ("Maison", "Clé en main", "/solutions/maison-intelligente-cle-en-main/", "lieu-maison", "50% 58%"),
    ("Domaine", "Maison, garage, quai", "/solutions/environnements-intelligents/", "lieu-domaine", "62% 55%"),
    ("Ferme", "Bâtiments surveillés", "/solutions/domotique-ferme-agricole/", "lieu-ferme", "50% 62%"),
    ("Entreprise", "IA privée et automatisation", "/solutions/ia-privee-entreprise/", "lieu-entreprise", "50% 45%"),
    ("Véhicule", "VR et véhicules aménagés", "/solutions/mobilite/", "lieu-vehicule", "50% 60%"),
]


def _lieux():
    lames = "".join(
        f"""<a class="ac-lieu" href="{url}">
      <img src="/media/accueil/{img}.webp" alt="" loading="lazy" style="object-position:{pos}">
      <span><b>{nom}</b><em>{ligne}</em></span>
    </a>"""
        for nom, ligne, url, img, pos in LIEUX
    )
    return f"""<section class="ac-sect ac-ou" id="regions" aria-labelledby="ac-ou-titre">
  <div class="ac-tete">
    <h2 id="ac-ou-titre">Votre lieu, en Montérégie.</h2>
    <a class="ac-lien" href="/regions/">Toutes les régions desservies</a>
  </div>
  <div class="ac-ou-grille">
    <div class="ac-carte-cadre">
      {carte_region.carte()}
      <p class="ac-carte-note">Basé à Saint-Hyacinthe. On se déplace chez vous.</p>
    </div>
    <div class="ac-lieux">{lames}</div>
  </div>
</section>"""


# --- 5. Comment on travaille : les cinq étapes de pro.ETAPES, en très court -------------------
ETAPES = [
    ("etape-visite", "Chez vous, gratuite."),
    ("etape-plan", "Le prix, ligne par ligne."),
    ("etape-installation", "Propre, essayée avec vous."),
    ("etape-formation", "Sur votre téléphone."),
    ("etape-suivi", "Entretien et réglages."),
]


def _etapes():
    pas = "".join(
        f"""<li class="ac-pas">
      <i aria-hidden="true">{i + 1}</i>
      <img src="/media/accueil/{img}.webp" alt="" loading="lazy">
      <b>{pro.ETAPES[i][0]}</b>
      <span>{ligne}</span>
    </li>"""
        for i, (img, ligne) in enumerate(ETAPES)
    )
    return f"""<section class="ac-sect ac-travail" id="comment-on-travaille" aria-labelledby="ac-travail-titre">
  <div class="ac-tete">
    <h2 id="ac-travail-titre">Cinq étapes. Aucune surprise.</h2>
    <a class="ac-lien" href="/a-propos/#comment-on-travaille">Comment on travaille</a>
  </div>
  <ol class="ac-ligne">{pas}</ol>
</section>"""


# --- 6. Fin : trois questions et l'appel ------------------------------------------------------
def _fin():
    return f"""<section class="ac-fin" id="questions" aria-labelledby="ac-fin-titre">
  <img class="ac-fin-ph" src="/media/vitrine/contact/demo-salon-prestige.webp" alt="" loading="lazy" width="2560" height="1100">
  <div class="ac-fin-in">
    <div class="ac-fin-appel">
      <h2 id="ac-fin-titre">Commençons par une visite.</h2>
      <p>Gratuite, sans engagement. Vous voyez ce qui fonctionne déjà.</p>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
    </div>
    <div class="ac-fin-faq">
      <div class="faq-list">{FAQ_HTML}</div>
      <a class="ac-lien" href="/questions/">Toutes les questions</a>
    </div>
  </div>
</section>"""


PAGE = {
    "url": "/",
    "v2": True,
    "title": "JARVIS Private Systems | Intégrateur de systèmes intelligents",
    "schema": [pro.ld_entreprise(), pro.ld_site(), pro.ld_faq(FAQ)],
    "assets": ["app", "accueil"],
    "lancement_integre": True,  # l'avis de lancement est dans le héros, pas sous la première section
    "description": (
        "Maisons, fermes, entreprises et véhicules intelligents et sécurisés, en Montérégie. "
        "Domotique, réseau et IA privée dans un seul système. Saint-Hyacinthe."
    ),
    "content": "\n".join([_heros(), _solutions(), _logiciel(), _lieux(), _etapes(), _fin()]) + "\n",
}
