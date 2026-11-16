# Accueil — aller à l'essentiel (novembre 2026). Cinq sections :
#   1. héros vivant : la photo de la résidence réagit (assets/demos/accueil.js, shader WebGL);
#   2. les sept solutions en bande de photos, une ligne chacune;
#   3. le logiciel : l'aperçu vivant de JARVIS App (démo complète sur /logiciel/);
#   4. l'offre : les trois Hubs en trois cartes (src/pages/offre.py), prix lus dans le catalogue;
#   5. fin : « Parlons de votre projet » et « Posez votre question à JARVIS » (ouvre la bulle).
# Les étapes vivent sur /a-propos/, les questions sur /questions/.
# Styles et scripts : assets/demos/accueil.css et accueil.js.

import json

from config import SITE, CAPABILITIES
from demos import app
from pages import offre
import pro


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
    <p class="ac-sig"><b>JARVIS Private Systems</b><span>{SITE["signature"]}</span></p>
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
# (solution, photo, cadrage, une ligne)
SOLUTIONS = [
    ("environnements-intelligents", "sol-environnements", "32% 50%", "Lumières, chauffage et énergie sur un seul écran."),
    ("ia-privee-connaissances", "sol-ia", "74% 50%", "Une IA qui lit vos documents, chez vous."),
    ("securite-intelligente", "sol-securite", "13% 50%", "Caméras, portes et alarme dans un seul fil."),
    ("automatisation-operations", "sol-automatisation", "47% 50%", "Demandes et approbations qui avancent seules."),
    ("reseau-resilience", "sol-reseau", "40% 50%", "Un Wi-Fi solide, partout, bien protégé."),
    ("diagnostic-care", "sol-diagnostic", "60% 50%", "La panne repérée avant le bris."),
    ("mobilite", "sol-mobilite", "72% 50%", "Le VR et les véhicules, suivis de partout."),
]
_TITRES = {c["slug"]: c["title"] for c in CAPABILITIES}


def _solutions():
    cartes = ""
    for slug, img, pos, ligne in SOLUTIONS:
        cartes += f"""<article class="ac-sol{'' if cartes else ' is-on'}">
      <img src="/media/accueil/{img}.webp" alt="" loading="lazy" style="object-position:{pos}">
      <div class="ac-sol-t">
        <h3><a class="ac-sol-a" href="/solutions/{slug}/">{_TITRES[slug]}</a></h3>
        <p>{ligne}</p>
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
    <h2 id="ac-log-titre">Une seule application.</h2>
    <a class="pill" href="/logiciel/">Essayer le logiciel</a>
  </div>
  <div class="ac-scene">
    <div class="ac-ecran">
      <div class="ac-dev" inert>{app.apercu()}</div>
      <a class="ac-ecran-a" href="/logiciel/" aria-label="Essayer le logiciel JARVIS" tabindex="-1"></a>
    </div>
  </div>
</section>"""


# --- 4. L'offre : les trois Hubs, prix lus dans le catalogue ------------------------------------
def _offre():
    return f"""<section class="ac-sect ac-offre" id="offre" aria-labelledby="ac-offre-titre">
  <div class="ac-tete">
    <h2 id="ac-offre-titre">Un Hub. Vos solutions.</h2>
    <a class="pill" href="/offre/">Voir l’offre</a>
  </div>
  {offre.hubs()}
  <p class="ac-offre-l">Puis vos solutions, par mois, annulables en tout temps.</p>
</section>"""


# --- 5. Fin : l'appel, et JARVIS pour les questions --------------------------------------------
# [data-jarvis] ouvre la bulle « Parler à JARVIS » (assets/js/guide.js); sans elle, le lien mène au contact.
def _fin():
    return """<section class="ac-fin" id="projet" aria-labelledby="ac-fin-titre">
  <img class="ac-fin-ph" src="/media/vitrine/contact/demo-salon-prestige.webp" alt="" loading="lazy" width="2560" height="1100">
  <div class="ac-fin-in">
    <h2 id="ac-fin-titre">Parlons de votre projet.</h2>
    <div class="ac-acts">
      <a class="pill" href="/contact/">Nous écrire</a>
      <a class="pill ghost" href="/contact/" data-jarvis>Posez votre question à JARVIS</a>
    </div>
  </div>
</section>"""


PAGE = {
    "url": "/",
    "v2": True,
    "title": "JARVIS Private Systems | Technologies de sécurité et intelligence privée",
    "schema": [pro.ld_entreprise(), pro.ld_site()],
    "assets": ["app", "offre", "accueil"],
    "lancement_integre": True,  # l'avis de lancement est dans le héros, pas sous la première section
    "description": (
        "JARVIS, un système privé qui gère et protège les maisons, les fermes, les entreprises "
        "et les véhicules. Domotique, réseau, caméras reliées et IA privée, chez vous."
    ),
    "content": "\n".join([_heros(), _solutions(), _logiciel(), _offre(), _fin()]) + "\n",
}
