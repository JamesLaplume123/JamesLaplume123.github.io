# « Météo en direct » : le ciel de Saint-Hyacinthe, 100 % réel.
# Prévisions, conditions et alertes : Environnement et Changement climatique Canada (API GeoMet,
# collection citypageweather-realtime, lieu qc-22). Mesures de la station la plus proche : Granby
# (SMC, collection swob-realtime, station 7022802, à 32 km). Lune : calcul astronomique local.
# Le ciel animé suit l'heure réelle par rapport au lever et au coucher du soleil, la couverture
# nuageuse, les précipitations et le vent réels. Les décisions de JARVIS sont simulées.
# Script : assets/demos/meteo.js ; styles : assets/demos/meteo.css. Le compteur de visites
# (data-live="visits") est rempli par assets/js/wow.js.

import math

NB = " "


def _compass():
    """Cadran de la boussole : graduations tous les 10°, points cardinaux en français."""
    ticks = []
    for i in range(36):
        a = math.radians(i * 10)
        major = i % 9 == 0
        r1, r2 = (44, 52) if major else (48, 52)
        x1, y1 = 60 + r1 * math.sin(a), 60 - r1 * math.cos(a)
        x2, y2 = 60 + r2 * math.sin(a), 60 - r2 * math.cos(a)
        cls = ' class="mj"' if major else ""
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"{cls}/>')
    labels = "".join(
        f'<text x="{60 + 36 * math.sin(math.radians(d)):.1f}" y="{60 - 36 * math.cos(math.radians(d)) + 4.5:.1f}">{t}</text>'
        for d, t in ((0, "N"), (90, "E"), (180, "S"), (270, "O"))
    )
    return f"""<svg class="mt-compass" viewBox="0 0 120 120" aria-hidden="true">
          <g class="mt-ticks">{"".join(ticks)}</g>
          <g class="mt-cards">{labels}</g>
          <g class="mt-needle" data-mt="needle">
            <path class="tail" d="M60 101 V113"/>
            <path class="head" d="M60 3 L54 17 Q60 14.5 66 17 Z"/>
          </g>
        </svg>"""


def html():
    return f"""<div class="demo-shell mt" data-demo="meteo" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Météo locale</b>
    <span class="mt-state" data-mt="state"><i class="dot is-off" aria-hidden="true"></i><span>Connexion…</span></span>
    <span class="tag tag-real">Données réelles</span></div>

  <div class="mt-alerts" data-mt="alerts" role="status" hidden></div>

  <div class="mt-hero" data-mt="hero">
    <canvas class="mt-sky" data-mt="sky" aria-hidden="true"></canvas>
    <div class="mt-veil" aria-hidden="true"></div>
    <span class="mt-arc-l" data-mt="arc-rise" aria-hidden="true"></span>
    <span class="mt-arc-r" data-mt="arc-set" aria-hidden="true"></span>
    <div class="mt-now">
      <p class="mt-place">Saint-Hyacinthe<span data-mt="daypart"></span></p>
      <p class="mt-temp" data-mt="temp-box" role="img" aria-label="Température en attente"><b data-mt="temp" aria-hidden="true">—</b><span class="mt-dec" data-mt="dec" aria-hidden="true"></span><span class="mt-deg" aria-hidden="true">°</span></p>
      <p class="mt-cond" data-mt="cond">Chargement des conditions…</p>
      <p class="mt-hilo" data-mt="hilo"></p>
      <p class="mt-feel" data-mt="feels"></p>
    </div>
    <p class="mt-noalert" data-mt="noalert" hidden>Aucune alerte en vigueur</p>
    <p class="mt-obs" data-mt="obs"></p>
  </div>

  <div class="mt-body">
    <section class="mt-card mt-hours" aria-labelledby="mt-h24">
      <header class="mt-head"><h3 class="mt-k" id="mt-h24">Prochaines 24{NB}heures</h3><p class="mt-sum" data-mt="h24-sum"></p></header>
      <div class="mt-scroll" data-mt="hours" tabindex="0" aria-label="Température, ciel et probabilité de précipitations, heure par heure">
        <p class="mt-wait">En attente des prévisions…</p>
      </div>
    </section>

    <div class="mt-split">
      <section class="mt-card mt-days" aria-labelledby="mt-d7">
        <header class="mt-head"><h3 class="mt-k" id="mt-d7">7{NB}jours</h3><p class="mt-sum" data-mt="normals"></p></header>
        <ol class="mt-week" data-mt="days"><li class="mt-wait">En attente des prévisions…</li></ol>
      </section>

      <div class="mt-tiles">
        <section class="mt-tile mt-wind" aria-labelledby="mt-t-wind">
          <h3 class="mt-k" id="mt-t-wind">Vent</h3>
          <div class="mt-dial">{_compass()}
            <p class="mt-dial-v"><b data-mt="wind">—</b><span>km/h</span></p>
          </div>
          <p class="mt-note" data-mt="wind-txt">&nbsp;</p>
        </section>
        <section class="mt-tile" aria-labelledby="mt-t-hum">
          <h3 class="mt-k" id="mt-t-hum">Humidité</h3>
          <p class="mt-big"><b data-mt="hum">—</b><span>{NB}%</span></p>
          <div class="mt-gauge" aria-hidden="true"><i data-mt="hum-bar"></i></div>
          <p class="mt-note" data-mt="dew">&nbsp;</p>
        </section>
        <section class="mt-tile" aria-labelledby="mt-t-pres">
          <h3 class="mt-k" id="mt-t-pres">Pression</h3>
          <p class="mt-big"><b data-mt="pres">—</b><span>{NB}kPa</span></p>
          <div class="mt-scale" aria-hidden="true"><i data-mt="pres-mark"></i></div>
          <p class="mt-note" data-mt="pres-txt">&nbsp;</p>
        </section>
        <section class="mt-tile" aria-labelledby="mt-t-uv">
          <h3 class="mt-k" id="mt-t-uv">Indice UV</h3>
          <p class="mt-big"><b data-mt="uv">—</b><span data-mt="uv-cat"></span></p>
          <div class="mt-scale mt-uvscale" aria-hidden="true"><i data-mt="uv-mark"></i></div>
          <p class="mt-note" data-mt="uv-txt">&nbsp;</p>
        </section>
        <section class="mt-tile" aria-labelledby="mt-t-sun">
          <h3 class="mt-k" id="mt-t-sun" data-mt="sun-k">Soleil</h3>
          <p class="mt-big"><b data-mt="sun-next">—</b></p>
          <div class="mt-gauge" aria-hidden="true"><i data-mt="sun-bar"></i></div>
          <p class="mt-note" data-mt="sun-txt">&nbsp;</p>
          <p class="mt-note" data-mt="moon-txt">&nbsp;</p>
        </section>
        <section class="mt-tile" aria-labelledby="mt-t-stn">
          <h3 class="mt-k" id="mt-t-stn">Station proche</h3>
          <p class="mt-big"><b data-mt="stn-temp">—</b><span>{NB}°C</span></p>
          <p class="mt-note" data-mt="stn-rain">&nbsp;</p>
          <p class="mt-note" data-mt="stn-txt">Granby · en attente</p>
        </section>
      </div>
    </div>

    <section class="mt-rules" aria-labelledby="mt-r">
      <header class="mt-rules-head">
        <h3 id="mt-r">Ce que JARVIS ferait avec cette météo</h3>
        <span class="tag tag-sim">Décisions simulées<span class="mt-tag-x"> · aucun appareil commandé</span></span>
      </header>
      <ul class="mt-rule-list" data-mt="rules">
        <li class="mt-rule is-info"><p class="mt-rule-k">Analyse</p><b>En attente des données réelles</b><p>Les règles s’évaluent dès que la météo arrive.</p></li>
      </ul>
    </section>
  </div>

  <footer class="mt-foot">
    <p class="mt-src" data-mt="src">Source : Environnement et Changement climatique Canada</p>
    <p class="mt-visits"><span class="mt-k">Visites du site</span><b class="odo" data-live="visits">—</b><small>Compteur réel, sans témoin ni pistage</small></p>
  </footer>
</div>"""
