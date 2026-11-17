# Accueil — le parcours du visiteur (décision de James, novembre 2026) : voir, tester, comprendre,
# composer son forfait.
#   1. héros vivant : un film de six lieux (maison, domaine, garage, hangar, ferme, entreprise); la
#      maison réagit au toucher (assets/demos/accueil.js, shader WebGL);
#   2. « Votre lieu, votre Hub » (src/lieux.py, src/pages/offre.py) : le lieu choisi allume le Hub
#      conseillé, et mène au forfait (/offre/);
#   3. voir : les solutions en bande de photos, une ligne chacune;
#   4. tester : l'aperçu vivant de JARVIS App (démo complète sur /logiciel/);
#   5. l'exemple réel (le laboratoire mobile);
#   6. fin : « Parlons de votre projet » et « Posez votre question à JARVIS » (ouvre la bulle).
# Styles et scripts : assets/demos/accueil.css et accueil.js.

import json

from config import SITE, CAPABILITIES
from demos import app
from pages import offre
import lieux
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


# Le film du héros : après la maison (scène 0, interactive), cinq autres lieux, chacun avec ce que
# JARVIS y voit. (id, nom, photo, cadrage, [(libellé, état)])
SCENES = [
    ("domaine", "Domaine", "/media/vitrine/accueil/panorama-domaine-crepuscule.webp", "62% 55%",
     [("Périmètre", "Calme"), ("Quai", "Éclairé"), ("Bâtiments", "4 en ligne")]),
    ("garage", "Garage", "/media/vitrine/accueil/garage-lamborghini-ferrari.webp", "50% 60%",
     [("Portes", "Verrouillées"), ("Véhicules", "2 présents"), ("Climat", "18 °C · 45 %")]),
    ("hangar", "Hangar", "/media/vitrine/accueil/jet-hangar.webp", "55% 55%",
     [("Hangar", "Sécurisé"), ("Appareil", "Branché"), ("Accès", "Personnes autorisées")]),
    ("ferme", "Ferme", "/media/offre/ferme.webp", "50% 60%",
     [("Ventilation", "Automatique"), ("Étable", "17 °C"), ("Eau", "Débit normal")]),
    ("entreprise", "Entreprise", "/media/vitrine/accueil/commerce-pme.webp", "60% 50%",
     [("Alarme", "Armée"), ("Caméras", "6 sur 6"), ("Fermeture", "Faite à 21 h")]),
]


def _scenes():
    return "".join(
        f'<figure class="ac-sc" data-ac-sc><img data-src="{img}" alt="" style="object-position:{pos}">'
        f'<ul class="ac-hud">{"".join(f"<li><i></i><b>{a}</b><em>{b}</em></li>" for a, b in chips)}</ul></figure>'
        for _id, _nom, img, pos, chips in SCENES
    )


def _onglets():
    noms = ["Maison"] + [n for _id, n, *_ in SCENES]
    return "".join(
        f'<button type="button" data-ac-tab="{i}" aria-pressed="{"true" if i == 0 else "false"}"><i aria-hidden="true"></i><span>{n}</span></button>'
        for i, n in enumerate(noms)
    )


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
    <div class="ac-scenes" aria-hidden="true">{_scenes()}<span class="ac-balai"></span></div>
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
    <div class="ac-tabs" data-ac-tabs role="group" aria-label="Les lieux montrés">{_onglets()}</div>
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
        cartes += f"""<article class="ac-sol{'' if cartes else ' is-on'}" data-sol="{slug}"{lieux.public_sol(slug)}>
      <img src="/media/accueil/{img}.webp" alt="" loading="lazy" style="object-position:{pos}">
      <div class="ac-sol-t">
        <h3><a class="ac-sol-a" href="/solutions/{slug}/">{_TITRES[slug]}</a></h3>
        <p>{ligne}</p>
      </div>
    </article>"""
    return f"""<section class="ac-sect ac-faire" id="solutions" aria-labelledby="ac-faire-titre">
  <div class="ac-tete">
    <h2 id="ac-faire-titre">Vos solutions, un seul système.</h2>
    <a class="ac-lien" href="/solutions/">Comparer les solutions</a>
  </div>
  <div class="ac-sols" data-ac-sols data-sols>{cartes}</div>
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


# --- 2. Votre lieu, votre Hub : un seul geste (décision de James : « ça devrait être ensemble ») ---
# On choisit son lieu; la carte du Hub conseillé s'allume avec sa raison (assets/js/wow.js), puis on
# compose son forfait. Les solutions utiles au lieu sont mises en avant dans la bande suivante.
def _lieu():
    return f"""<section class="ac-sect ac-choisir" id="lieu" aria-label="Votre lieu, votre Hub">
  {lieux.selecteur("Votre lieu, votre Hub.", resultat=False)}
  {offre.hubs(guide=False)}
  <div class="ac-suite">
    <a class="pill" href="/offre/#composer">Composer mon forfait</a>
    <a class="ac-lien" href="/offre/">Comprendre l’offre</a>
  </div>
</section>"""


# --- 5. L'exemple réel : le laboratoire mobile ---------------------------------------------------
def _reel():
    return """<section class="ac-sect ac-composer" aria-label="L’exemple réel">
  <a class="ac-reel" href="/laboratoire-mobile/">
    <img src="/media/ambulance/ambulance-garage-lab-v1.webp" alt="" loading="lazy">
    <span><em>L’exemple réel</em><b>Un vrai JARVIS, qui tourne.</b><small>Le laboratoire mobile : une ambulance convertie, ses batteries en direct.</small></span>
  </a>
</section>"""


# --- 6. Fin : l'appel, et JARVIS pour les questions --------------------------------------------
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
    "content": "\n".join([_heros(), _lieu(), _solutions(), _logiciel(), _reel(), _fin()]) + "\n",
}
