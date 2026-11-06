# « BouLance en direct » : les deux batteries LiFePO₄ de l'ambulance, lues dans Home Assistant
# par le service du site (integrations/site-api, GET /live et /history). Données réelles.
# Sans service configuré, le panneau l'annonce honnêtement au lieu d'inventer des valeurs.


def _battery(i, name):
    return f"""<article class="bl-bat" data-bat="{i}">
      <div class="bl-pack" aria-hidden="true">
        <span class="bl-cap"></span>
        <div class="bl-cell">
          <svg class="bl-liquid" viewBox="0 0 200 400" preserveAspectRatio="none">
            <path class="bl-wave w1" d=""></path><path class="bl-wave w2" d=""></path>
          </svg>
          <div class="bl-shine"></div>
          <b class="bl-soc"><span data-bl="soc">--</span><i>%</i></b>
        </div>
      </div>
      <div class="bl-info">
        <p class="bl-k">Batterie {name} <span class="bl-flag" data-bl="flag"></span></p>
        <dl class="bl-stats">
          <div><dt>Tension</dt><dd data-bl="v">—</dd></div>
          <div><dt>Courant</dt><dd data-bl="a">—</dd></div>
          <div><dt>Température</dt><dd data-bl="t">—</dd></div>
          <div><dt>Énergie</dt><dd data-bl="wh">—</dd></div>
          <div><dt>Écart cellules</dt><dd data-bl="cells">—</dd></div>
          <div><dt>Cycles</dt><dd data-bl="cycles">—</dd></div>
        </dl>
        <p class="bl-mos"><span data-bl="chg">Charge</span><span data-bl="dsg">Décharge</span><span data-bl="bal">Équilibrage</span></p>
      </div>
    </article>"""


def html():
    return f"""<div class="demo-shell bl" data-demo="boulance" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · BouLance · Énergie</b>
    <span class="bl-state" data-bl="state"><i class="dot is-off" aria-hidden="true"></i>Connexion…</span>
    <span class="tag tag-real">Données réelles</span></div>
  <div class="demo-body bl-body">
    {_battery(0, "A")}
    <div class="bl-mid">
      <p class="bl-k">Réserve totale</p>
      <p class="bl-total"><b data-bl="kwh">—</b><i>kWh</i></p>
      <p class="bl-sub"><span data-bl="ah">— Ah</span> · <span data-bl="w">— W</span></p>
      <div class="bl-flow" data-bl="flow" aria-hidden="true">
        <span class="bl-node n-in">Solaire<br>et chargeur</span>
        <span class="bl-node n-bat">Batteries</span>
        <span class="bl-node n-out">Ambulance</span>
        <svg viewBox="0 0 300 60" preserveAspectRatio="none"><path class="bl-wire" d="M40 30 H150 H260"/>
          <circle class="bl-dot d1" r="4"/><circle class="bl-dot d2" r="4"/><circle class="bl-dot d3" r="4"/></svg>
      </div>
      <p class="bl-mode" data-bl="mode">—</p>
      <div class="bl-chart">
        <p class="bl-k">24 dernières heures</p>
        <svg viewBox="0 0 300 90" preserveAspectRatio="none" data-bl="chart" aria-label="Énergie stockée sur 24 heures">
          <defs><linearGradient id="blg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".45"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>
          <path class="bl-area" d=""/><path class="bl-line" d=""/>
        </svg>
        <p class="bl-axis"><span>il y a 24 h</span><span data-bl="range">—</span><span>maintenant</span></p>
      </div>
    </div>
    {_battery(1, "B")}
    <div class="bl-wait" role="status">
      <span class="bl-wait-ico" aria-hidden="true"><i></i><i></i><i></i></span>
      <b>Liaison avec l’ambulance en cours</b>
      <p>Les deux batteries s’affichent ici en direct, mesurées aux 5 secondes dans le véhicule.
      Tant que la liaison ne répond pas, rien n’est inventé.</p>
    </div>
  </div>
  <p class="bl-foot"><span data-bl="age">En attente de la première mesure</span> · actualisé toutes les 5 secondes ·
  source : Home Assistant de l’ambulance (BMS Bluetooth)</p>
</div>"""
