# Laboratoire des cartes : page privée (noindex, hors menus et sitemap, Disallow dans robots.txt).
# « Édition prestige » : l'ADN exact du cadran de thermostat des Environnements (K.thermostat / dialCard
# de assets/demos/env.js), poussé au maximum sans changer d'identité : verre bombé, lunette usinée dont
# le reflet suit la souris, graduations qui s'allument jusqu'à la consigne, halo or vivant, curseur à
# traînée lumineuse, chiffres qui roulent. Quatre cartes de la même famille, et le thermostat actuel à
# côté pour comparer (rendu fidèle : mêmes classes et mêmes styles, assets/demos/env.css).
# Styles : assets/demos/labo.css · comportements : assets/demos/labo.js (préfixe px-).

import math

# ---------------------------------------------------------------- Données d'exemple
# Scène figée : un mardi de novembre, 14 h 20, à la Résidence (même thermostat que la démo).
TH = {"title": "Thermostat", "sub": "Rez-de-chaussée · thermopompe", "set": 21.5, "inside": 21, "min": 15, "max": 26,
      "rows": [["home", "Salon", "21", "°C"], ["fire", "Chauffage", "Thermopompe · Auto", ""],
               ["snowflake", "Climatisation", "Hors saison", ""]]}
FLOW = {"solaire": 4.4, "maison": 2.8, "batteries": 1.2, "reseau": 0.4}  # kW
SOLAR_MAX = 8.0
PACKS = [  # nom, %, V, °C, cycles
    ("Batterie A", 65, 52.1, 19.5, 212),
    ("Batterie B", 63, 52.0, 19.8, 209),
]
SOC, CAP, RESERVE = 64, 27, 20
CAR = {"nom": "Coupé noir", "baie": "Baie 1", "v": 12.8, "hum": 45, "garage": 15,
       "img": "/media/vitrine/accueil/garage-lamborghini-ferrari.webp"}

NB = " "  # espace fine insécable


def fr(x, d=1):
    """Nombre à la française : virgule décimale, signe moins typographique."""
    s = f"{abs(x):.{d}f}".replace(".", ",")
    return ("−" if x < 0 else "") + s


def P(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def pol(cx, cy, r, deg):
    """Point sur un cercle; 0° = midi, sens horaire."""
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1):
    if a1 - a0 < 0.05:
        a1 = a0 + 0.05
    x0, y0 = pol(cx, cy, r, a0)
    x1, y1 = pol(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{P(x0)} {P(y0)}A{P(r)} {P(r)} 0 {large} 1 {P(x1)} {P(y1)}"


def frac(v, lo, hi):
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


def ang(v, lo, hi):
    return -135 + 270 * frac(v, lo, hi)


# Pictogrammes : ceux de la démo Environnements (assets/demos/env.js), au trait fin.
I = {
    "thermo": '<path d="M10 14.3V5.2a2 2 0 0 1 4 0v9.1a4 4 0 1 1-4 0Z"/><path d="M12 9.5v7"/>',
    "home": '<path d="M4.5 10.2 12 4l7.5 6.2V19a1 1 0 0 1-1 1h-4v-5.5h-5V20h-4a1 1 0 0 1-1-1z"/>',
    "fire": '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.2 0-3.6 2.7-5.4 3.7-8.8 1.9 1.4 2.4 3.3 2.4 4.6 1-.6 1.7-1.8 1.8-3 2.4 1.9 5.1 4.5 5.1 7.4 0 3.4-2.6 6-6.5 6Z"/>',
    "snowflake": '<path d="M12 2.75v18.5M3.99 7.38l16.02 9.24M3.99 16.62l16.02-9.24"/><path d="m9.5 4.25 2.5 2 2.5-2M9.5 19.75l2.5-2 2.5 2"/>',
    "minus": '<path d="M5 12h14"/>', "plus": '<path d="M12 5v14M5 12h14"/>',
    "right": '<path d="m9.5 6 6 6-6 6"/>',
    "info": '<circle cx="12" cy="12" r="8.25"/><path d="M12 11v5"/><path d="M12 7.9v.1"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "bolt": '<path d="M13 2.75 5.5 13.25H12l-1 8 7.5-10.5H12z"/>',
    "sun": '<circle cx="12" cy="12" r="3.75"/><path d="M12 2.75v2M12 19.25v2M2.75 12h2M19.25 12h2M5.45 5.45l1.4 1.4M17.15 17.15l1.4 1.4M5.45 18.55l1.4-1.4M17.15 6.85l1.4-1.4"/>',
    "battery": '<rect x="3" y="7" width="16" height="10" rx="2.25"/><path d="M21.25 10.5v3"/><path d="M6.5 10.25v3.5M9.5 10.25v3.5M12.5 10.25v3.5"/>',
    "grid": '<path d="M8 21 12 3l4 18M9.6 14h4.8M10.6 9.5h2.8M6 6.5h12M7 21h10"/>',
    "drop": '<path d="M12 3.5s-6 6.4-6 10.9a6 6 0 0 0 12 0C18 9.9 12 3.5 12 3.5Z"/>',
    "plug": '<path d="M9 3v5M15 3v5M6.5 8h11v3.5a5.5 5.5 0 0 1-11 0zM12 17v4"/>',
    "garage": '<path d="M3 21V9l9-5 9 5v12"/><path d="M6.5 21v-9h11v9M6.5 15h11M6.5 18h11"/>',
    "car": '<path d="M5 16.5h14v-4l-2-5H7l-2 5z"/><path d="M5 12.5h14M6.5 16.5v2M17.5 16.5v2"/>',
    "clock": '<circle cx="12" cy="12" r="8.25"/><path d="M12 7.5V12l3 2"/>',
}


def ic(k, cls=""):
    return f'<svg class="ev-i{(" " + cls) if cls else ""}" viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'


def pi(k, cls=""):
    return f'<svg class="px-i{(" " + cls) if cls else ""}" viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'


# ================================================================ Thermostat actuel (copie fidèle)
# Même balisage que dialCard / K.thermostat de assets/demos/env.js, mêmes classes ev-*, styles de env.css.
EV_DEFS = ('<svg class="ev-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
           '<linearGradient id="evd-bezel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a4a4a"/><stop offset=".22" stop-color="#1b1b1b"/><stop offset=".55" stop-color="#0a0a0a"/><stop offset=".8" stop-color="#2b2b2b"/><stop offset="1" stop-color="#101010"/></linearGradient>'
           '<radialGradient id="evd-face" cx="50%" cy="38%" r="70%"><stop offset="0" stop-color="#1a1918"/><stop offset=".7" stop-color="#070707"/><stop offset="1" stop-color="#000"/></radialGradient>'
           '<linearGradient id="evd-glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
           '<linearGradient id="evd-heat" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ffb347"/><stop offset=".6" stop-color="#ff8a3d"/><stop offset="1" stop-color="#ff5f3d"/></linearGradient>'
           "</defs></svg>")


def ev_dial_svg(c):
    v, now = c["set"], c["inside"]
    aV, aN = ang(v, c["min"], c["max"]), ang(now, c["min"], c["max"])
    lo, hi = min(aV, aN), max(aV, aN)
    ticks = []
    for i in range(61):
        a = -135 + i * 4.5
        maj = i % 10 == 0
        x0, y0 = pol(100, 100, 70 if maj else 73, a)
        x1, y1 = pol(100, 100, 79, a)
        on = lo - 0.1 <= a <= hi + 0.1 and hi - lo > 0.5
        ticks.append(f'<line class="d-tk{" is-maj" if maj else ""}{" is-on" if on else ""}" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    kn, cn, cn2 = pol(100, 100, 62, aV), pol(100, 100, 86, aN), pol(100, 100, 92, aN)
    return ('<svg class="ev-dsvg is-heat" viewBox="0 0 200 200" aria-hidden="true">'
            '<circle cx="100" cy="100" r="98" fill="url(#evd-bezel)" class="d-bezel"/><circle cx="100" cy="100" r="90" class="d-bezel-in"/>'
            '<circle cx="100" cy="100" r="88" fill="url(#evd-face)"/>' + "".join(ticks) +
            f'<path class="d-track" d="{arc(100, 100, 62, -135, 135)}"/><path class="d-val is-heat" d="{arc(100, 100, 62, lo, hi)}"/>'
            f'<line class="d-now" x1="{cn[0]:.1f}" y1="{cn[1]:.1f}" x2="{cn2[0]:.1f}" y2="{cn2[1]:.1f}"/>'
            f'<circle class="d-knob is-heat" cx="{kn[0]:.1f}" cy="{kn[1]:.1f}" r="6.5"/>'
            '<ellipse cx="100" cy="58" rx="66" ry="40" fill="url(#evd-glass)" class="d-glass"/></svg>')


def ev_thermo():
    c = TH
    rows = "".join(
        f'<div class="ev-row is-lg"><span class="ev-ri t-gold">{ic(k)}</span><span><small>{lab}</small><b>'
        + (f'<span class="ev-num">{val}</span><small class="ev-u">{NB}{u}</small>' if u else val)
        + f'</b></span>{ic("right", "ev-chev")}</div>' for k, lab, val, u in c["rows"])
    return f"""
<div class="ev px-ref-ev">{EV_DEFS}
  <article class="ev-card px-ref-card" aria-label="Thermostat actuel de la démo">
    <div class="ev-thermo"><div><header class="ev-ch"><span class="ev-ci">{ic("thermo")}</span><div class="ev-ct"><h5>{c["title"]}</h5><p>{c["sub"]}</p></div></header>
      <div class="ev-dialw"><div class="ev-dial">
        <button type="button" class="ev-round" aria-label="Baisser la consigne" tabindex="-1">{ic("minus")}</button>
        <div class="ev-dial-g" aria-hidden="true">{ev_dial_svg(c)}<div class="ev-dial-v"><span class="ev-dial-m is-heat">{ic("fire")}Chauffage</span><b>{fr(c["set"])}<sup>°C</sup></b><small>Actuelle {c["inside"]}{NB}°C</small></div></div>
        <button type="button" class="ev-round" aria-label="Monter la consigne" tabindex="-1">{ic("plus")}</button></div>
        <span class="ev-sent is-idle">{ic("info")}Glissez sur le cadran ou utilisez + et −</span></div></div>
      <div class="ev-thermo-r">{rows}</div></div>
  </article>
</div>"""


# ================================================================ Édition prestige : cadran commun
def digits(txt):
    """Chiffres qui roulent : chaque chiffre est une bande 0-9 déplacée verticalement (voir labo.js)."""
    out, dec = [], False
    for ch in txt:
        if ch == ",":
            out.append('<span class="px-dec">,')
            dec = True
        elif ch.isdigit():
            out.append(f'<span class="px-dg" style="--d:{ch}"><span>' + "".join(f"<i>{n}</i>" for n in range(10)) + "</span></span>")
        else:
            out.append(f"<span class=\"px-sg\">{ch}</span>")
    if dec:
        out.append("</span>")
    return "".join(out)


def num(v, d, cls=""):
    return (f'<span class="px-n{(" " + cls) if cls else ""}" data-pn="{v}" data-d="{d}">'
            f'<span class="px-sr">{fr(v, d)}</span><span class="px-roll" aria-hidden="true">{digits(fr(v, d))}</span></span>')


def pdial(key, lo, hi, v, *, size="lg", tone="acc", step=0.1, maj=1.0, mid=None, now=None, marks=(), ends=None,
          center="", label="", interactive=False, unit="", d=1):
    """Cadran prestige : lunette usinée (HTML), cadran guilloché, graduations, arc, halo, curseur à traînée,
    verre bombé. viewBox 240; graduations entre r 89 et 100, arc sur r 80."""
    n = round((hi - lo) / step)
    ticks = []
    for i in range(n + 1):
        val = lo + i * step
        a = ang(val, lo, hi)
        is_maj = abs((val - lo) / maj - round((val - lo) / maj)) < 1e-6
        is_mid = mid and not is_maj and abs((val - lo) / mid - round((val - lo) / mid)) < 1e-6
        r0 = 88 if is_maj else (92 if is_mid else 94.5)
        x0, y0 = pol(120, 120, r0, a)
        x1, y1 = pol(120, 120, 100, a)
        cls = "t-maj" if is_maj else ("t-mid" if is_mid else "t")
        on = " is-on" if val <= v + 1e-6 else ""
        ticks.append(f'<line class="{cls}{on}" data-v="{P(val)}" style="--k:{i}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
    av = ang(v, lo, hi)
    kx, ky = pol(120, 120, 80, av)
    extra = []
    if now is not None:
        a = ang(now, lo, hi)
        x0, y0 = pol(120, 120, 102.5, a)
        x1, y1 = pol(120, 120, 108.5, a)
        extra.append(f'<line class="px-now" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
    for mv, mcls in marks:
        a = ang(mv, lo, hi)
        x0, y0 = pol(120, 120, 84, a)
        x1, y1 = pol(120, 120, 101, a)
        extra.append(f'<line class="px-mark {mcls}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
    if ends:
        for a, t in ((-135, ends[0]), (135, ends[1])):
            x, y = pol(120, 120, 66, a)
            extra.append(f'<text class="px-end" x="{P(x)}" y="{P(y + 4)}">{t}</text>')
    gid = f"pxg-{key}"
    svg = (f'<svg class="px-dsvg" viewBox="0 0 240 240" aria-hidden="true"><defs>'
           f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="40" y1="200" x2="200" y2="40"><stop offset="0" class="s0"/><stop offset=".55" class="s1"/><stop offset="1" class="s2"/></linearGradient>'
           f'<radialGradient id="{gid}-k" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#fff"/><stop offset=".35" class="k1"/><stop offset="1" class="k2"/></radialGradient></defs>'
           f'<g class="px-ticks">{"".join(ticks)}</g>'
           f'<path class="px-track" d="{arc(120, 120, 80, -135, 135)}"/>'
           f'<path class="px-halo" data-arc d="{arc(120, 120, 80, -135, av)}"/>'
           f'<path class="px-val" data-arc d="{arc(120, 120, 80, -135, av)}" stroke="url(#{gid})"/>'
           f'<path class="px-glint" data-arc pathLength="100" d="{arc(120, 120, 80, -135, av)}"/>'
           f'{"".join(extra)}'
           f'<g class="px-knob" data-knob transform="translate({P(kx)} {P(ky)})"><circle r="11.5" class="px-knob-o"/><circle r="7.6" fill="url(#{gid}-k)" class="px-knob-i"/></g>'
           f"</svg>")
    attrs = f'data-pdial="{key}" data-lo="{lo}" data-hi="{hi}" data-v="{v}" data-d="{d}" style="--ka:{P(av)}deg"'
    if interactive:
        attrs += (f' role="slider" tabindex="0" aria-label="{label}" aria-valuemin="{lo}" aria-valuemax="{hi}"'
                  f' aria-valuenow="{v}" aria-valuetext="{fr(v, d)} {unit}" data-step="0.5"')
    else:
        attrs += ' aria-hidden="true"'
    return (f'<div class="px-dial is-{size} t-{tone}{" is-live" if interactive else ""}" {attrs}>'
            '<span class="px-shadow"></span><span class="px-bz"></span><span class="px-bz-cut"></span>'
            '<span class="px-face"></span><span class="px-spill"></span>' + svg +
            '<span class="px-trail"></span><span class="px-glass"><i></i></span>'
            f'<div class="px-dv">{center}</div></div>')


def phead(icon, title, sub, tone="acc", right=""):
    return (f'<header class="px-ch"><span class="px-pas t-{tone}">{pi(icon)}</span>'
            f'<div class="px-ct"><h3>{title}</h3><p>{sub}</p></div>{right}</header>')


def prow(icon, label, value, tone="acc", extra="", chev=True):
    return (f'<div class="px-row"><span class="px-pas is-sm t-{tone}">{pi(icon)}</span>'
            f'<span class="px-rt"><small>{label}</small><b>{value}</b>{extra}</span>'
            + (pi("right", "px-chev") if chev else "") + "</div>")


def card(cls, inner, span, i, label):
    return (f'<article class="px-card {cls}" data-span="{span}" data-px style="--i:{i}" aria-label="{label}">'
            f'<span class="px-rim" aria-hidden="true"></span>{inner}</article>')


# ---------------------------------------------------------------- 1. Thermostat
def p_thermo():
    c = TH
    center = (f'<span class="px-mode is-heat" data-tmode>{pi("fire")}<span>Chauffage</span></span>'
              f'<b class="px-big">{num(c["set"], 1)}<sup>°C</sup></b>'
              f'<small class="px-now-l">Actuelle {c["inside"]}{NB}°C</small>')
    dial = pdial("thermo", c["min"], c["max"], c["set"], size="xl", now=c["inside"], ends=(c["min"], c["max"]),
                 center=center, label="Consigne · Thermostat", interactive=True, unit="°C")
    rows = "".join(prow(k, lab, (f'{val}<small>{NB}{u}</small>' if u else val)) for k, lab, val, u in c["rows"])
    rows += prow("drop", "Humidité", f'41<small>{NB}%</small>', extra='<em class="is-warn">Un peu sèche</em>')
    inner = f"""
  {phead("thermo", c["title"], c["sub"], right='<span class="px-tag">Édition prestige</span>')}
  <div class="px-thermo">
    <div class="px-dialw">
      <div class="px-dialrow">
        <button type="button" class="px-round" data-step="-1" aria-label="Baisser la consigne">{pi("minus")}</button>
        {dial}
        <button type="button" class="px-round" data-step="1" aria-label="Monter la consigne">{pi("plus")}</button>
      </div>
      <p class="px-sent is-idle" data-sent role="status">{pi("info")}<span>Glissez sur le cadran ou utilisez + et −</span></p>
    </div>
    <div class="px-rows">{rows}</div>
  </div>"""
    return card("px-c-thermo", inner, 7, 1, "Thermostat, édition prestige")


# ---------------------------------------------------------------- 2. Flux d'énergie
def p_flux():
    s = FLOW["solaire"]
    center = (f'<span class="px-mode is-sun">{pi("sun")}<span>Production</span></span>'
              f'<b class="px-big is-md">{num(s, 1)}<sup>kW</sup></b><small class="px-now-l">sur {fr(SOLAR_MAX, 0)}{NB}kW de crête</small>')
    big = pdial("solaire", 0, SOLAR_MAX, s, size="lg", step=0.1, maj=1, mid=0.5, center=center)
    items = [
        ("maison", "home", "Maison", FLOW["maison"], 6, "consommée en ce moment", "acc"),
        ("batteries", "battery", "Batteries", FLOW["batteries"], 3, "en charge · 64 %", "ok"),
        ("reseau", "grid", "Réseau", FLOW["reseau"], 3, "renvoyée au réseau", "acc"),
    ]
    rows, paths = [], []
    for j, (k, icn, lab, v, mx, note, tone) in enumerate(items):
        mini = pdial(f"f-{k}", 0, mx, v, size="sm", tone=tone, step=mx / 30, maj=mx / 6, center=pi(icn, "px-mini-i"))
        rows.append(
            f'<div class="px-frow" style="--j:{j}">{mini}'
            f'<span class="px-rt"><small>{lab}</small><b>{num(v, 1)}<small>{NB}kW</small></b><em>{note}</em></span>'
            f'{pi("right", "px-chev")}</div>')
        y = 40 + j * 80
        paths.append(f'<path class="px-wire t-{tone}" d="M0 120 C 46 120, 34 {y}, 80 {y}" style="--sp:{P(2.6 / max(v, .3))}s"/>')
    inner = f"""
  {phead("bolt", "Énergie en ce moment", "Mardi 14 h 20 · le toit couvre toute la maison", right='<span class="px-tag">Données d’exemple</span>')}
  <div class="px-flux">
    <div class="px-flux-src">{big}</div>
    <svg class="px-wires" viewBox="0 0 80 240" preserveAspectRatio="none" aria-hidden="true">{"".join(paths)}</svg>
    <div class="px-flux-l">{"".join(rows)}</div>
  </div>
  <p class="px-foot">{pi("check")}<span>Autonomie du jour : <b>78{NB}%</b> de la consommation couverte par le soleil.</span></p>"""
    return card("px-c-flux", inner, 7, 2, "Flux d’énergie")


# ---------------------------------------------------------------- 3. Batteries (vert)
def p_batt():
    kwh = SOC * CAP / 100
    center = (f'<span class="px-mode is-ok">{pi("bolt")}<span>En charge</span></span>'
              f'<b class="px-big">{num(SOC, 0)}<sup>%</sup></b><small class="px-now-l">{fr(kwh)}{NB}kWh disponibles</small>')
    big = pdial("batt", 0, 100, SOC, size="lg", tone="ok", step=2, maj=10, mid=None, marks=((RESERVE, "is-warn"),), center=center, d=0)
    packs = []
    for nm, p, vv, t, cy in PACKS:
        seg = "".join(f'<i class="{"is-on" if k * 5 < p else ""}" style="--k:{k}"></i>' for k in range(20))
        packs.append(
            f'<div class="px-pack"><span class="px-pas is-sm t-ok">{pi("battery")}</span>'
            f'<span class="px-rt"><small>{nm}</small><b>{num(p, 0)}<small>{NB}%</small></b>'
            f'<span class="px-seg" aria-hidden="true">{seg}</span>'
            f'<em>{fr(vv)}{NB}V · {fr(t)}{NB}°C · {cy} cycles</em></span></div>')
    inner = f"""
  {phead("battery", "Batteries", f"2 batteries · {CAP}{NB}kWh · réserve {RESERVE}{NB}%", tone="ok")}
  <div class="px-batt">
    <div class="px-batt-d">{big}</div>
    <div class="px-batt-l">{"".join(packs)}
      <p class="px-batt-eta">{pi("clock")}<span>Pleine vers <b>22 h 30</b> au rythme actuel</span></p>
    </div>
  </div>
  <div class="px-legend" aria-hidden="true"><span><i class="is-ok"></i>Charge</span><span><i class="is-warn"></i>Réserve {RESERVE}{NB}%</span><span><i class="is-err"></i>Critique</span></div>"""
    return card("px-c-batt", inner, 5, 3, "Batteries")


# ---------------------------------------------------------------- 4. Véhicule de collection
def p_car():
    gauges = [
        ("v-bat", 11, 14.5, CAR["v"], "Mainteneur", f'{num(CAR["v"], 1)}<small>{NB}V</small>', "ok", "Charge d’entretien", 0.1, 0.5, 1),
        ("v-hum", 0, 100, CAR["hum"], "Humidité", f'{num(CAR["hum"], 0)}<small>{NB}%</small>', "acc", "Idéal 40 à 55 %", 2, 10, 0),
        ("v-tmp", 0, 30, CAR["garage"], "Baie", f'{num(CAR["garage"], 0)}<small>{NB}°C</small>', "acc", "Plancher radiant", 0.5, 5, 0),
    ]
    g = "".join(
        f'<div class="px-gauge">{pdial(k, lo, hi, v, size="md", tone=t, step=st, maj=mj, d=dd, center=f"<b class=px-mid>{val}</b>")}'
        f'<span class="px-gl"><small>{lab}</small><em>{note}</em></span></div>'
        for k, lo, hi, v, lab, val, t, note, st, mj, dd in gauges)
    inner = f"""
  <figure class="px-photo"><img src="{CAR['img']}" alt="Le coupé noir et la sportive rouge dans le garage de collection éclairé" loading="lazy"></figure>
  <div class="px-car-in">
    {phead("car", f"{CAR['nom']} · {CAR['baie']}", "Garage de collection · remisé depuis 12 jours", right='<span class="px-state is-ok" data-door-state><i></i>Remisé</span>')}
    <div class="px-gauges">{g}</div>
    <div class="px-car-acts">
      {prow("garage", "Porte 1", '<span data-door-v>Fermée</span>', chev=False)}
      <button type="button" class="px-btn" data-door aria-pressed="false">{pi("garage")}<span data-door-l>Ouvrir la porte 1</span></button>
    </div>
  </div>"""
    return card("px-c-car", inner, 12, 4, "Véhicule de collection")


def p_ref():
    return f"""
<article class="px-ref" data-span="5" style="--i:0" aria-label="Thermostat actuel, pour comparer">
  <p class="px-ref-k">Aujourd’hui, dans la démo</p>
  {ev_thermo()}
</article>"""


CONTENT = f"""
<div class="px" data-px-root>
  <section class="px-top">
    <p class="px-k">Page privée · laboratoire des cartes</p>
    <h1>Édition prestige</h1>
    <p class="px-intro">Le cadran du thermostat que vous aimez, poussé au maximum sans changer d’identité : verre bombé, lunette usinée qui renvoie la lumière, graduations qui s’allument jusqu’à la consigne, halo or vivant. Trois autres cartes de la même famille suivent.</p>
    <p class="px-note">Données d’exemple · scène d’un mardi de novembre, 14 h 20 · survolez, glissez la consigne, ouvrez la porte</p>
  </section>
  <nav class="px-bar" aria-label="Mode d’affichage">
    <div class="px-bar-in">
      <span class="px-bar-t">Comparez dans les trois modes</span>
      <div class="px-modes" role="group" aria-label="Mode d’affichage">
        <button type="button" data-mode-set="signature" aria-pressed="true" class="is-on">Signature</button>
        <button type="button" data-mode-set="platinum" aria-pressed="false">Platinum</button>
        <button type="button" data-mode-set="base" aria-pressed="false">Base</button>
      </div>
    </div>
  </nav>
  <section class="px-sec" aria-labelledby="px-t">
    <h2 class="px-h2" id="px-t">Quatre cartes, une même famille</h2>
    <div class="px-grid">{p_ref()}{p_thermo()}{p_flux()}{p_batt()}{p_car()}</div>
  </section>
</div>
"""

PAGE = {
    "url": "/labo-cartes/",
    "v2": True,
    "noindex": True,
    "title": "Laboratoire des cartes | JARVIS Private Systems",
    "description": "Page privée : édition prestige des cartes de JARVIS.",
    "body_class": "px-page",
    "assets": ["env", "labo"],
    "content": CONTENT,
}
