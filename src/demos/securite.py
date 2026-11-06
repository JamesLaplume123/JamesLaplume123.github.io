# Démo interactive — Sécurité intelligente (solution 03).
# « Six notifications deviennent un seul événement compris. »
# Mur de quatre caméras simulées + chronologie qui se construit, puis se
# regroupe en un seul événement. Le comportement vit dans
# assets/demos/securite.js ; le style dans assets/demos/securite.css.
#
# Sans JavaScript, ce balisage montre un état final lisible : les quatre
# caméras de la résidence et l'événement « Livraison » déjà résumé.
# Les cadrages ci-dessous doivent rester identiques à ceux de SITES.maison
# dans securite.js (mêmes images, mêmes fenêtres).

W, H = 1672, 941  # taille des images de caméra (px)
M = "/media/solutions/"


def _stage(v):
    """Style de la scène : l'image entière, placée pour que la fenêtre v soit visible."""
    vx, vy, vw, vh = v
    return (
        f"left:{-vx / vw * 100:.3f}%;top:{-vy / vh * 100:.3f}%;"
        f"width:{W / vw * 100:.3f}%;height:{H / vh * 100:.3f}%"
    )


def _v43(vx):
    """Fenêtre 4:3 sur toute la hauteur de l'image."""
    return (vx, 0, H * 4 / 3, H)


def _thumb_view(cx, cy, vw):
    """Fenêtre 16:10 centrée sur (cx, cy), bornée à l'image."""
    vh = vw / 1.6
    vx = min(max(cx - vw / 2, 0), W - vw)
    vy = min(max(cy - vh / 2, 0), H - vh)
    return (vx, vy, vw, vh)


CAMS = [
    ("camera-front-entry-v1.webp", "Entrée avant", _v43(60),
     "Caméra de l’entrée avant : porte, marches et allée éclairées le soir"),
    ("camera-driveway-garage-v1.webp", "Allée et garage", _v43(220),
     "Caméra de l’allée : porte de garage et entrée de cour"),
    ("camera-rear-terrace-v1.webp", "Terrasse arrière", _v43(400),
     "Caméra de la terrasse arrière : salon extérieur, table et piscine"),
    ("camera-pool-spa-v1.webp", "Piscine et spa", _v43(210),
     "Caméra de la piscine et du spa"),
]

SENSORS = [
    ("bell", "Sonnette", "Au repos"),
    ("door", "Porte d’entrée", "Verrouillée"),
    ("terrace", "Détecteur · terrasse", "Calme"),
    ("alarm", "Alarme", "Désarmée"),
]

# Preuves statiques de l'état final « Livraison » (cadrages des miniatures).
THUMBS = [
    ("camera-driveway-garage-v1.webp", _thumb_view(700, 520, 760), "Allée<span> · 21:42:11</span>"),
    ("camera-front-entry-v1.webp", _thumb_view(330, 380, 640), "Sonnette<span> · 21:42:38</span>"),
    ("camera-front-entry-v1.webp", _thumb_view(340, 470, 480), "Colis<span> · 21:42:50</span>"),
]


BITRATES = ("1,8", "2,1", "1,6", "1,9")  # débit affiché au repos (Mb/s), un par caméra


def _cam(i, img, name, view, alt):
    # .sec-pan : dérive lente de l'image (sous html.fx) · .sec-glitch : bref
    # artefact de compression quand un mouvement se déclenche · .sec-fx :
    # vignette de l'objectif. Le grain et l'exposition sont posés en CSS dans
    # la scène elle-même, sous les cadres de détection.
    return f"""
          <figure class="sec-cam" data-cam="{i}">
            <div class="sec-view">
              <div class="sec-pan">
                <div class="sec-stage" style="{_stage(view)}"><img src="{M}{img}" alt="{alt}" loading="lazy"></div>
              </div>
              <i class="sec-glitch" aria-hidden="true"></i>
              <i class="sec-fx" aria-hidden="true"></i>
            </div>
            <figcaption class="sec-hud">
              <span class="sec-name"><b>CAM 0{i + 1}</b> <span>{name}</span></span>
              <span class="sec-tr" aria-hidden="true"><span class="sec-br" data-sec-br>{BITRATES[i]} Mb/s</span><span class="sec-rec">REC</span></span>
              <span class="sec-ir" aria-hidden="true">IR<span> · nuit</span></span>
              <time class="sec-ts" data-sec-ts>21:42:58</time>
              <span class="sec-st t-calm" data-sec-st>Calme</span>
            </figcaption>
          </figure>"""


def _sensor(sid, name, state):
    return (
        f'<li class="sec-sen" data-sensor="{sid}"><i aria-hidden="true"></i>'
        f"<span>{name}</span><b>{state}</b></li>"
    )


def _thumb(img, view, cap):
    return (
        f'<figure class="sec-th"><div class="sec-th-view"><div class="sec-stage" style="{_stage(view)}">'
        f'<img src="{M}{img}" alt="" loading="lazy"></div></div><figcaption>{cap}</figcaption></figure>'
    )


HTML = f"""
<div class="demo-shell" data-demo="securite" data-rev>
  <div class="demo-top">
    <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
    <b>JARVIS · Sécurité</b>
    <span class="sec-site" data-sec-site>Résidence · 4 caméras</span>
    <span class="sec-clock" data-sec-clock aria-hidden="true">21:42:58</span>
    <span class="tag tag-sim">Démo · données simulées</span>
  </div>
  <div class="demo-body">
    <div class="sec-bar">
      <div class="sec-scen" role="group" aria-label="Choisir une situation simulée">
        <button type="button" data-sec-scen="livraison" aria-pressed="true"><small>21 h 42 · Résidence</small><b>Livraison</b></button>
        <button type="button" data-sec-scen="visiteur" aria-pressed="false"><small>2 h 13 · Résidence</small><b>Visiteur inconnu la nuit</b></button>
        <button type="button" data-sec-scen="entrepot" aria-pressed="false"><small>23 h 07 · Entreprise</small><b>Entrepôt après la fermeture</b></button>
      </div>
      <ul class="sec-legend" aria-label="Légende des détections">
        <li class="t-person">Personne</li><li class="t-vehicle">Véhicule</li><li class="t-parcel">Colis</li><li class="t-move">Mouvement</li><li class="t-alert">Alerte</li>
      </ul>
    </div>

    <div class="sec-grid">
      <div class="sec-left">
        <div class="sec-wall" data-sec-wall>{"".join(_cam(i, *c) for i, c in enumerate(CAMS))}
        </div>
        <ul class="sec-sensors" data-sec-sensors aria-label="Autres capteurs">
          {"".join(_sensor(*s) for s in SENSORS)}
        </ul>
      </div>

      <section class="sec-feed" aria-label="Chronologie des alertes">
        <div class="sec-feed-head">
          <p>Chronologie</p>
          <span class="sec-phase is-ok" data-sec-phase>1 événement compris</span>
          <button type="button" class="sec-replay" data-sec-replay aria-label="Rejouer la situation">
            <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8a5 5 0 1 0 1.6-3.7M3 2.5v2.8h2.8"/></svg>Rejouer
          </button>
        </div>
        <div class="sec-feed-stage">
          <p class="sec-empty" data-sec-empty hidden><i aria-hidden="true"></i>Caméras et capteurs en écoute · aucune alerte pour l’instant</p>
          <ol class="sec-raw" data-sec-raw aria-label="Alertes brutes"></ol>
          <article class="sec-inc is-on" data-sec-inc>
            <div class="sec-inc-top">
              <span class="sec-lvl is-ok" data-sec-lvl>Normal</span>
              <span class="sec-inc-k" data-sec-when>Durée · 50&nbsp;s</span>
            </div>
            <p class="sec-inc-sum" data-sec-sum><b>21&nbsp;h&nbsp;42 — Livraison :</b> un livreur a déposé un colis à l’entrée puis est reparti. Rien d’anormal.</p>
            <p class="sec-inc-why" data-sec-why><span>6 alertes regroupées · même personne suivie sur 2 caméras · sonnette · colis</span></p>
            <div class="sec-ev" data-sec-ev>{"".join(_thumb(*t) for t in THUMBS)}</div>
            <p class="sec-calm" data-sec-calm><svg viewBox="0 0 12 12" aria-hidden="true"><path d="m2.5 6.3 2.3 2.2 4.7-5"/></svg><span>Aucune action requise. Le colis reste sous l’œil de la caméra 01.</span></p>
            <div class="sec-acts" data-sec-acts hidden>
              <p class="sec-acts-k">JARVIS propose · vous décidez</p>
              <ul data-sec-actlist></ul>
            </div>
            <div class="sec-follow" data-sec-follow></div>
            <p class="sec-keep"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5.2a2.5 2.5 0 0 1 5 0V7"/></svg>Preuves conservées sur place · 30 jours</p>
          </article>
        </div>
        <div class="sec-count">
          <span class="sec-n"><b data-sec-n>6</b><small>alertes<br>brutes</small></span>
          <span class="sec-arrow" aria-hidden="true"><i></i><small>1 notification au lieu de 6</small></span>
          <span class="sec-n sec-n-one"><b>1</b><small>événement<br>compris</small></span>
        </div>
        <p class="sec-phone">Sur votre téléphone : <b>1 notification au lieu de 6.</b></p>
      </section>
    </div>
    <svg class="sec-wires" data-sec-wires aria-hidden="true"></svg>
    <p class="sec-sr" aria-live="polite" data-sec-live></p>
  </div>
</div>
<p class="demo-hint">Choisissez une situation · approuvez ou ignorez les actions proposées · tout est simulé</p>
"""
