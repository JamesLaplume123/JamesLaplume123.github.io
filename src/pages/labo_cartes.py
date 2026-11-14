# Laboratoire des cartes : page privée (noindex, hors menus et sitemap, Disallow dans robots.txt).
# « Matière » : quatre cartes faites de la matière de chaque mode, pas de dégradés qui imitent le métal.
# Signature = verre ambré et or liquide, Platinum = cristal taillé à dispersion, Base = verre fumé mat.
# Chaque carte est une dalle rendue par un shader WebGL2 (assets/demos/labo.js) qui réfracte la vraie
# scène du mode; le texte reste en HTML par-dessus pour des chiffres nets. Sans WebGL2, repli CSS avec
# les vraies images (assets/demos/labo.css). Préfixe mt-.

import math

# ---------------------------------------------------------------- Données d'exemple
# Scène figée : un mardi de novembre, 14 h 20, à la Résidence (mêmes valeurs que src/demos/env.py).
TH = {"set": 21.5, "inside": 21, "min": 15, "max": 26}
FLOW = {"solaire": 4.4, "maison": 2.8, "batteries": 1.2, "reseau": 0.4}  # kW
PACKS = [("Batterie A", 65, 52.1, 19.5), ("Batterie B", 63, 52.0, 19.8)]  # nom, %, V, °C
SOC, CAP, RESERVE = 64, 27, 20
CAR = {"v": 12.8, "hum": 45, "garage": 15, "img": "/media/vitrine/accueil/garage-lamborghini-ferrari.webp"}

NB = " "  # espace fine insécable


def fr(x, d=1):
    """Nombre à la française : virgule décimale."""
    return f"{x:.{d}f}".replace(".", ",")


def pol(r, deg):
    a = math.radians(deg - 90)
    return 100 + r * math.cos(a), 100 + r * math.sin(a)


def arc(r):
    (x0, y0), (x1, y1) = pol(r, -135), pol(r, 135)
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 1 1 {x1:.2f} {y1:.2f}"


I = {
    "minus": '<path d="M5 12h14"/>', "plus": '<path d="M12 5v14M5 12h14"/>',
    "home": '<path d="M4.5 10.2 12 4l7.5 6.2V19a1 1 0 0 1-1 1h-4v-5.5h-5V20h-4a1 1 0 0 1-1-1z"/>',
    "sun": '<circle cx="12" cy="12" r="3.75"/><path d="M12 2.75v2M12 19.25v2M2.75 12h2M19.25 12h2M5.45 5.45l1.4 1.4M17.15 17.15l1.4 1.4M5.45 18.55l1.4-1.4M17.15 6.85l1.4-1.4"/>',
    "battery": '<rect x="3" y="7" width="16" height="10" rx="2.25"/><path d="M21.25 10.5v3"/><path d="M6.5 10.25v3.5M9.5 10.25v3.5M12.5 10.25v3.5"/>',
    "grid": '<path d="M8 21 12 3l4 18M9.6 14h4.8M10.6 9.5h2.8M6 6.5h12M7 21h10"/>',
    "garage": '<path d="M3 21V9l9-5 9 5v12"/><path d="M6.5 21v-9h11v9M6.5 15h11M6.5 18h11"/>',
}


def ic(k):
    return f'<svg class="mt-i" viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'


def card(kind, label, inner, extra=""):
    return (f'<article class="mt-card mt-{kind}" data-mt="{kind}" aria-label="{label}"{extra}>'
            f'<canvas class="mt-gl" aria-hidden="true"></canvas><div class="mt-in">{inner}</div></article>')


def head(title, sub):
    return f'<header class="mt-head"><h2>{title}</h2><p>{sub}</p></header>'


# ---------------------------------------------------------------- 1. Thermostat
def c_thermo():
    f = (TH["set"] - TH["min"]) / (TH["max"] - TH["min"])
    inner = f"""
  {head("Thermostat", "Rez-de-chaussée, thermopompe")}
  <div class="mt-dial" data-mt-dial role="slider" tabindex="0" aria-label="Consigne de température"
       aria-valuemin="{TH['min']}" aria-valuemax="{TH['max']}" aria-valuenow="{TH['set']}"
       data-min="{TH['min']}" data-max="{TH['max']}" data-set="{TH['set']}" data-now="{TH['inside']}">
    <svg class="mt-dial-fb" viewBox="0 0 200 200" aria-hidden="true">
      <path class="mt-fb-track" d="{arc(86)}"/><path class="mt-fb-val" data-mt-arc d="{arc(86)}" pathLength="100" stroke-dasharray="{f * 100:.2f} 100"/>
    </svg>
    <div class="mt-dial-c">
      <span class="mt-dial-k">Consigne</span>
      <b class="mt-big"><span data-mt-set>{fr(TH['set'])}</span><sup>°C</sup></b>
      <span class="mt-dial-now">Intérieur {fr(TH['inside'], 0)}{NB}°C</span>
    </div>
  </div>
  <div class="mt-steps">
    <button type="button" class="mt-round" data-mt-step="-0.5" aria-label="Baisser la consigne d’un demi-degré">{ic("minus")}</button>
    <p class="mt-state" data-mt-state aria-live="polite">Chauffage en cours</p>
    <button type="button" class="mt-round" data-mt-step="0.5" aria-label="Monter la consigne d’un demi-degré">{ic("plus")}</button>
  </div>"""
    return card("thermo", "Thermostat", inner)


# ---------------------------------------------------------------- 2. Flux d'énergie
def c_flux():
    mx = FLOW["solaire"]

    def node(key, icon, name, val, role, flow=None):
        fl = f' data-flow="{flow / mx:.3f}"' if flow is not None else ""
        return (f'<div class="mt-node mt-n-{key}"><span class="mt-bead" data-mt-node{fl}>{ic(icon)}</span>'
                f'<span class="mt-node-t"><b>{fr(val)}<small>{NB}kW</small></b><em>{name}</em><small>{role}</small></span></div>')

    inner = f"""
  {head("Flux d’énergie", "En ce moment, le soleil alimente tout")}
  <div class="mt-flow">
    <svg class="mt-flow-fb" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M50 14 16 56M50 14v70M50 14l34 42"/></svg>
    {node("sol", "sun", "Solaire", FLOW["solaire"], "Production")}
    {node("bat", "battery", "Batteries", FLOW["batteries"], "En charge", FLOW["batteries"])}
    {node("mai", "home", "Maison", FLOW["maison"], "Consommation", FLOW["maison"])}
    {node("res", "grid", "Réseau", FLOW["reseau"], "Vendu", FLOW["reseau"])}
  </div>
  <p class="mt-foot">Autonomie solaire <b>100{NB}%</b> depuis 9\u00a0h\u00a040</p>"""
    return card("flux", "Flux d’énergie", inner)


# ---------------------------------------------------------------- 3. Batteries
def c_batt():
    packs = "".join(
        f'<div class="mt-pack"><div class="mt-pack-h"><span>{nm}</span><b>{p}{NB}%</b></div>'
        f'<div class="mt-tube" data-mt-tube data-level="{p / 100:.2f}" style="--lv:{p}%"><i></i></div>'
        f'<p class="mt-pack-d">{fr(v)}{NB}V<span>{fr(t)}{NB}°C</span></p></div>'
        for nm, p, v, t in PACKS)
    inner = f"""
  {head("Batteries", f"{CAP}{NB}kWh, réserve gardée à {RESERVE}{NB}%")}
  <div class="mt-soc"><b class="mt-big is-ok">{SOC}<sup>%</sup></b>
    <p><span class="mt-ok">En charge, +{fr(FLOW["batteries"])}{NB}kW</span><span>{fr(SOC * CAP / 100)}{NB}kWh disponibles</span><span>Pleine vers 22\u00a0h\u00a030</span></p></div>
  <div class="mt-packs">{packs}</div>
  <p class="mt-foot">Environ <b>9{NB}h</b> d’autonomie en cas de panne</p>"""
    return card("batt", "Batteries", inner, f' data-reserve="{RESERVE / 100}"')


# ---------------------------------------------------------------- 4. Véhicule de collection
def c_auto():
    ms = [("Mainteneur", f"{fr(CAR['v'])}", "V", "Charge d’entretien"), ("Humidité", f"{CAR['hum']}", "%", "Idéal 40 à 55"),
          ("Baie", f"{CAR['garage']}", "°C", "Plancher radiant")]
    m = "".join(f'<div class="mt-m"><span>{k}</span><b>{v}<small>{NB}{u}</small></b><em>{n}</em></div>' for k, v, u, n in ms)
    inner = f"""
  <figure class="mt-photo" data-mt-photo><img src="{CAR['img']}" alt="Le coupé noir et la sportive rouge dans le garage de collection éclairé" loading="lazy" decoding="async"></figure>
  {head("Coupé noir, baie 1", "Garage de collection, remisé depuis 12 jours")}
  <div class="mt-ms">{m}</div>
  <div class="mt-door"><p>Porte 1<b data-mt-door-v>Fermée</b></p>
    <button type="button" class="mt-btn" data-mt-door aria-pressed="false">{ic("garage")}<span data-mt-door-l>Ouvrir la porte 1</span></button></div>"""
    return card("auto", "Véhicule de collection", inner)


CONTENT = f"""
<div class="mt" data-mt-root>
  <section class="mt-top">
    <h1>Des cartes faites de matière</h1>
    <p class="mt-intro">Chaque carte est une dalle de la matière du mode, posée sur le sol poli : elle laisse voir la pièce derrière elle et accroche la lumière. Changez de mode, la matière change.</p>
    <div class="mt-modes" role="group" aria-label="Matière des cartes">
      <button type="button" data-mode-set="signature" aria-pressed="true" class="is-on"><b>Signature</b><small>Verre ambré, or liquide</small></button>
      <button type="button" data-mode-set="platinum" aria-pressed="false"><b>Platinum</b><small>Cristal taillé</small></button>
      <button type="button" data-mode-set="base" aria-pressed="false"><b>Base</b><small>Verre fumé</small></button>
    </div>
  </section>
  <section class="mt-stage" aria-label="Quatre cartes">{c_thermo()}{c_flux()}{c_batt()}{c_auto()}</section>
  <p class="mt-note">Données d’exemple, scène d’un mardi de novembre à 14 h 20. Glissez l’anneau du thermostat ou utilisez les boutons; bougez la souris, la lumière suit.</p>
</div>
"""

PAGE = {
    "url": "/labo-cartes/",
    "v2": True,
    "noindex": True,
    "title": "Laboratoire des cartes | JARVIS Private Systems",
    "description": "Page privée : des cartes faites de la matière de chaque mode.",
    "body_class": "mt-page",
    "assets": ["labo"],
    "content": CONTENT,
}
