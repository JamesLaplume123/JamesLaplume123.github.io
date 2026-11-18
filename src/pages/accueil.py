# Accueil — une vitrine, pas un formulaire (décision de James, 18 novembre 2026 : « comme Apple,
# très prestigieux, que les gens veulent acheter »). Peu de mots, beaucoup d'espace, un bouton doré.
#   1. héros vivant : un film de six lieux; la maison réagit au toucher (accueil.js, shader WebGL);
#   2. le produit : le Hub, en grand, presque seul;
#   3. la gamme : Base, Signature, Platinum, une ligne chacun;
#   4. ce qu'il fait : les solutions en bande de photos, une ligne chacune;
#   5. tester : l'aperçu vivant de JARVIS App (démo complète sur /logiciel/);
#   6. l'exemple réel (le laboratoire mobile);
#   7. fin : « Parlons de votre projet » et « Posez votre question à JARVIS » (ouvre la bulle).
# Le choix du lieu se fait en composant son forfait (/offre/#composer), plus sur l'accueil.
# Styles et scripts : assets/demos/accueil.css et accueil.js.

import json

from config import SITE, CAPABILITIES
from demos import app
import pro


# --- 1. Héros vivant --------------------------------------------------------------------------
# La photo montre tout allumé; éteindre une lumière assombrit seulement ses zones (cx, cy, rx, ry
# en fractions de la photo). La porte du garage remonte et laisse voir un intérieur (autre photo).
HEROS = {
    "img": "/media/accueil/film-maison.webp",
    "ratio": [2880, 1620],
    "inside": "/media/accueil/film-maison-ouvert.webp",   # la même photo, porte ouverte (alignée au pixel)
    "door": [0.048, 0.345, 0.242, 0.345, 0.565, 0.575],  # gauche, haut G, droite, haut D, bas D, bas G
    "crop": [-1, 0, 0, 0],   # -1 : lire la photo « porte ouverte » au même endroit
    "spots": [
        {"id": "etage", "label": "Étage", "on": "Allumé", "off": "Éteint", "x": 66, "y": 16,
         "zones": [[0.66, 0.16, 0.15, 0.10], [0.45, 0.18, 0.05, 0.07]]},
        {"id": "salon", "label": "Salon", "on": "Allumé", "off": "Éteint", "x": 70, "y": 38,
         "zones": [[0.70, 0.38, 0.15, 0.09], [0.84, 0.36, 0.05, 0.06]]},
        {"id": "entree", "label": "Entrée", "on": "Allumée", "off": "Éteinte", "x": 40, "y": 33,
         "zones": [[0.40, 0.30, 0.05, 0.09], [0.42, 0.46, 0.08, 0.06], [0.47, 0.53, 0.07, 0.04]]},
        {"id": "garage", "label": "Garage", "on": "Ouvert", "off": "Fermé", "x": 14, "y": 45, "door": True},
    ],
}


# Le film du héros : après la maison (scène 0, interactive), cinq autres lieux, chacun avec ce que
# JARVIS y voit. (id, nom, photo, cadrage, [(libellé, état)])
SCENES = [
    ("domaine", "Domaine", "/media/accueil/film-domaine.webp", "50% 40%",
     [("Résidence", "Tout est calme", .22, .22), ("Piscine", "27 °C", .46, .33), ("Quai", "Éclairé", .84, .42)]),
    ("garage", "Garage", "/media/accueil/film-garage.webp", "50% 55%",
     [("Climat", "18 °C · 45 %", .25, .22), ("Place 1", "Présent · verrouillé", .33, .52), ("Place 2", "Présent · verrouillé", .80, .50)]),
    ("hangar", "Hangar", "/media/accueil/film-hangar.webp", "50% 55%",
     [("Appareil", "Branché", .52, .50), ("Accès", "Personnes autorisées", .41, .60), ("Salon", "Éclairé", .10, .45)]),
    ("ferme", "Ferme", "/media/accueil/film-ferme.webp", "50% 50%",
     [("Ventilation", "Automatique", .50, .14), ("Porte", "Fermée", .47, .44), ("Troupeau", "Calme", .50, .56)]),
    ("entreprise", "Entreprise", "/media/accueil/film-entreprise.webp", "50% 45%",
     [("Rideau", "Ouvert", .50, .26), ("Entrée", "Ouverte jusqu’à 21 h", .30, .52), ("Caméras", "6 sur 6", .80, .42)]),
]


def _scenes():
    """Chaque scène : la photo et ses repères, posés sur l'objet (x, y en fractions de la photo; placés
    par assets/demos/accueil.js selon le cadrage). Sur téléphone, les repères deviennent une courte liste."""
    return "".join(
        f'<figure class="ac-sc" data-ac-sc data-pos="{pos}"><div class="ac-sc-in"><img data-src="{img}" alt="" style="object-position:{pos}">'
        + '<ul class="ac-hud">'
        + "".join(f'<li data-x="{x}" data-y="{y}"><i></i><span><b>{a}</b><em>{b}</em></span></li>' for a, b, x, y in chips)
        + "</ul></div></figure>"
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
    <h1 id="ac-titre">Votre lieu.<br>Sous contrôle.</h1>
    <div class="ac-hero-bas">
      <p class="ac-phrase">{SITE["phrase"]}</p>
      <div class="ac-acts">
        <a class="pill" href="/offre/#composer">Composer mon forfait</a>
        <a class="ac-lien-f" href="/logiciel/">Essayer le logiciel <i aria-hidden="true">›</i></a>
      </div>
    </div>
    <div class="ac-tabs" data-ac-tabs role="group" aria-label="Les lieux montrés">{_onglets()}</div>
    <p class="ac-lanc"><i aria-hidden="true"></i><span>{SITE["lancement"]}</span>
      <a href="/contact/">Rester informé</a></p>
  </div>
  <p class="ac-demo" data-ac-demo aria-hidden="true">Démonstration : touchez un point de la maison</p>
  <script type="application/json" data-ac-data>{json.dumps(HEROS, ensure_ascii=False, separators=(",", ":"))}</script>
</section>"""


# --- 2. Le produit : le Hub, en grand, presque seul -------------------------------------------
# Décision de James (18 novembre 2026) : un site qui donne envie, comme Apple. On montre d'abord le
# produit; le choix du lieu ne se fait qu'en composant son forfait (/offre/#composer).
def _produit():
    return """<section class="ac-pro" aria-labelledby="ac-pro-titre">
  <p class="ac-pro-k">Hub JARVIS</p>
  <h2 id="ac-pro-titre">Un boîtier.<br><span>Tout votre lieu.</span></h2>
  <p class="ac-pro-p">Lumières, caméras, réseau et intelligence privée, réunis dans un seul appareil, chez vous.</p>
  <div class="ac-pro-acts">
    <a class="pill" href="/offre/#composer">Composer mon forfait</a>
    <a class="ac-lien-f" href="/offre/">Découvrir l’offre <i aria-hidden="true">›</i></a>
  </div>
  <img class="ac-pro-ph" src="/media/hubs/hub-signature.webp" alt="Le Hub JARVIS Signature posé dans un salon" loading="lazy" width="1600" height="1200">
</section>"""


# --- 3. La gamme : trois Hubs, une ligne chacun -------------------------------------------------
GAMME = [
    ("base", "Base", "L’essentiel, pour un petit lieu.", ""),
    ("signature", "Signature", "La maison où vous vivez.", "Le plus choisi"),
    ("platinum", "Platinum", "Un lieu qui ne s’arrête jamais.", ""),
]


def _gamme():
    cartes = "".join(f"""<a class="ac-g" href="/offre/#hub">
      <img src="/media/hubs/hub-{i}.webp" alt="Hub JARVIS {n}" loading="lazy" width="1600" height="1200">
      {f'<em class="ac-g-k">{k}</em>' if k else '<em class="ac-g-k" aria-hidden="true">&nbsp;</em>'}
      <h3>{n}</h3><p>{l}</p><span class="ac-lien-f">En savoir plus <i aria-hidden="true">›</i></span>
    </a>""" for i, n, l, k in GAMME)
    return f"""<section class="ac-gam" aria-labelledby="ac-gam-titre">
  <h2 id="ac-gam-titre">Choisissez votre Hub.</h2>
  <div class="ac-gs">{cartes}</div>
</section>"""


# --- 4. Ce que nous faisons : les sept solutions, dans l'ordre officiel -----------------------
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
    for n, (slug, img, pos, ligne) in enumerate(SOLUTIONS, 1):
        cartes += f"""<article class="ac-sol{'' if cartes else ' is-on'}" data-sol="{slug}">
      <img src="/media/accueil/{img}.webp" alt="" loading="lazy" style="object-position:{pos}">
      <div class="ac-sol-t">
        <h3><a class="ac-sol-a" href="/solutions/{slug}/">{_TITRES[slug]}</a></h3>
        <p>{ligne}</p>
        <span class="ac-sol-go" aria-hidden="true">Découvrir <i>→</i></span>
      </div>
    </article>"""
    return f"""<section class="ac-sect ac-faire" id="solutions" aria-labelledby="ac-faire-titre">
  <div class="ac-tete">
    <h2 id="ac-faire-titre">Ce qu’il fait.</h2>
    <a class="ac-lien-f" href="/solutions/">Toutes les solutions <i aria-hidden="true">›</i></a>
  </div>
  <div class="ac-sols" data-ac-sols data-sols>{cartes}</div>
</section>"""


# --- 3. Le logiciel ---------------------------------------------------------------------------
# L'écran se redresse en arrivant; une visite guidée le parcourt seule (cadre doré et légende, voir
# accueil.js); un grand bouton invite à l'essayer. Toute la scène mène à /logiciel/.
TOUR = [
    ("xc", "Vos extensions", "Maison, sécurité, réseau : tout au même endroit."),
    ("tl", "Votre journée", "Agenda et tâches, déjà prêts."),
    ("ask", "Assistant JARVIS", "Demandez en mots simples."),
    ("map", "Vos lieux", "Maison, chalet, véhicules : une seule carte."),
    ("search", "Recherche", "Trouvez ou commandez en un instant."),
]


def _logiciel():
    return f"""<section class="ac-sect ac-log" id="logiciel" aria-labelledby="ac-log-titre">
  <div class="ac-log-g">
    <div class="ac-log-t">
      <p class="ac-log-k">Démonstration en direct</p>
      <h2 id="ac-log-titre">Essayez <br>le logiciel.</h2>
      <p class="ac-log-p">La vraie interface, avec des données d’exemple. Cliquez : tout répond.</p>
      <ul class="ac-log-l">
        <li>Rien à installer</li>
        <li>Aucun compte à créer</li>
        <li>Ordinateur et téléphone</li>
      </ul>
      <a class="ac-jouer" href="/logiciel/"><i aria-hidden="true"></i>Essayer le logiciel</a>
    </div>
    <div class="ac-scene">
      <div class="ac-ecran" data-ac-ecran>
        <div class="ac-dev" inert>{app.apercu()}</div>
        <div class="ac-tour" data-ac-tour aria-hidden="true"><i class="ac-tour-b"></i><p class="ac-tour-l"><b></b><span></span></p></div>
        <a class="ac-ecran-a" href="/logiciel/" aria-label="Essayer le logiciel JARVIS" tabindex="-1"><span>Cliquez pour l’essayer</span></a>
        <script type="application/json" data-ac-tour-data>{json.dumps(TOUR, ensure_ascii=False)}</script>
      </div>
    </div>
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
    "assets": ["app", "accueil"],
    "lancement_integre": True,  # l'avis de lancement est dans le héros, pas sous la première section
    "description": (
        "JARVIS, un système privé qui gère et protège les maisons, les fermes, les entreprises "
        "et les véhicules. Domotique, réseau, caméras reliées et IA privée, chez vous."
    ),
    "content": "\n".join([_heros(), _produit(), _gamme(), _solutions(), _logiciel(), _reel(), _fin()]) + "\n",
}
