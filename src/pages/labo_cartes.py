# Laboratoire des cartes : page privée (noindex, hors menus et sitemap, Disallow dans robots.txt).
# Trois directions radicalement différentes pour les cartes de JARVIS, mêmes six cartes, mêmes
# données d'exemple (la Résidence et le Garage de src/demos/env.py). Sert à choisir la direction
# avant de refaire les 69 types de cartes des démos. Ne touche à aucune démo existante.
#   A. Haute horlogerie      (préfixe ha-)
#   B. Cockpit futuriste     (préfixe ck-)
#   C. Architecture et lumière (préfixe al-)
# Styles : assets/demos/labo.css · comportements : assets/demos/labo.js

import math

# ---------------------------------------------------------------- Données d'exemple
# Scène figée : un mardi de novembre, 14 h 20, à la Résidence (bord de la Yamaska).
T_SET, T_IN, T_MIN, T_MAX = 21.5, 21.0, 15, 26
HUM, T_OUT = 41, -2
FLOW = {"solaire": 4.4, "maison": 2.8, "batteries": 1.2, "reseau": 0.4}  # kW, batteries en charge, réseau en injection
PACKS = [  # nom, % , V, °C, cycles, cellule haute, cellule basse
    ("Batterie A", 65, 52.1, 19.5, 212, 3.268, 3.259),
    ("Batterie B", 63, 52.0, 19.8, 209, 3.266, 3.258),
]
SOC, CAP, RESERVE = 64, 27, 20
CONS = [1.6, 1.4, 1.3, 1.3, 1.4, 2.2, 3.4, 3.1, 2.4, 1.9, 1.8, 1.7, 1.8, 1.7, 2.8, 2.6, 3.5, 4.2, 4.0, 3.6, 3.1, 2.6, 2.1, 1.8]
PROD = [0, 0, 0, 0, 0, 0, 0, 0.3, 1.4, 3.2, 5.1, 6.4, 6.9, 6.1, 4.4, 2.4, 0.6, 0, 0, 0, 0, 0, 0, 0]
NOW_H = 14  # heure de la scène
CAMS = [
    ("entree", "Entrée principale", "/media/solutions/camera-front-entry-v1.webp", "Aucun mouvement"),
    ("allee", "Allée du garage", "/media/solutions/camera-driveway-garage-v1.webp", "Aucun mouvement"),
    ("piscine", "Piscine et spa", "/media/solutions/camera-pool-spa-v1.webp", "Aucun mouvement"),
]
CAR = {"nom": "Lamborghini Huracán", "baie": "Baie 1", "v": 12.8, "hum": 45, "garage": 15,
       "img": "/media/vitrine/accueil/garage-lamborghini-ferrari.webp"}


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
    x0, y0 = pol(cx, cy, r, a0)
    x1, y1 = pol(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{P(x0)} {P(y0)}A{P(r)} {P(r)} 0 {large} 1 {P(x1)} {P(y1)}"


def frac(v, lo, hi):
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


TOT_C, TOT_P = sum(CONS), sum(PROD)
SELF = round(100 * sum(min(c, p) for c, p in zip(CONS, PROD)) / TOT_C)

I = {  # pictogrammes au trait fin (24 × 24)
    "sun": '<circle cx="12" cy="12" r="3.6"/><path d="M12 2.8v2.1M12 19.1v2.1M2.8 12h2.1M19.1 12h2.1M5.5 5.5 7 7M17 17l1.5 1.5M5.5 18.5 7 17M17 7l1.5-1.5"/>',
    "home": '<path d="M4.5 10.4 12 4.2l7.5 6.2V19a1 1 0 0 1-1 1h-4v-5.4h-5V20h-4a1 1 0 0 1-1-1z"/>',
    "bat": '<rect x="3" y="7" width="16" height="10" rx="2.2"/><path d="M21.2 10.4v3.2M6.4 10.2v3.6M9.4 10.2v3.6M12.4 10.2v3.6"/>',
    "grid": '<path d="M8 21 12 3l4 18M9.6 14h4.8M10.6 9.5h2.8M6 6.5h12M7 21h10"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "drop": '<path d="M12 3.8s-5.7 6.1-5.7 10.1a5.7 5.7 0 0 0 11.4 0c0-4-5.7-10.1-5.7-10.1Z"/>',
    "thermo": '<path d="M10 14.2V5.5a2 2 0 0 1 4 0v8.7a3.7 3.7 0 1 1-4 0Z"/><path d="M12 11v5"/>',
    "shield": '<path d="M12 3.5 19 6v5.5c0 4.4-2.9 7.6-7 9-4.1-1.4-7-4.6-7-9V6z"/><path d="m9 12 2.2 2.2L15.2 10"/>',
    "door": '<path d="M3 21V9l9-5 9 5v12"/><path d="M6.5 21v-9h11v9M6.5 15h11M6.5 18h11"/>',
    "minus": '<path d="M6 12h12"/>', "plus": '<path d="M12 6v12M6 12h12"/>',
    "left": '<path d="m14.5 6-6 6 6 6"/>', "right": '<path d="m9.5 6 6 6-6 6"/>',
    "fan": '<circle cx="12" cy="12" r="1.6"/><path d="M12 10.4c-.4-3.2.6-6 3-6.4 2.3-.3 3 2.4.6 4.2l-2.4 1.6M13.6 12c3.2-.4 6 .6 6.4 3 .3 2.3-2.4 3-4.2.6l-1.6-2.4M12 13.6c.4 3.2-.6 6-3 6.4-2.3.3-3-2.4-.6-4.2l2.4-1.6M10.4 12c-3.2.4-6-.6-6.4-3-.3-2.3 2.4-3 4.2-.6l1.6 2.4"/>',
    "car": '<path d="M4 16.5v-3l2-4.5a2 2 0 0 1 1.8-1.2h8.4a2 2 0 0 1 1.8 1.2l2 4.5v3"/><path d="M3.5 16.5h17M4.5 13.5h15"/><circle cx="7.5" cy="16.8" r="1.6"/><circle cx="16.5" cy="16.8" r="1.6"/>',
}


def ico(k, cls="lx-i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'


def series_json():
    return "[" + ",".join(f"[{c},{p}]" for c, p in zip(CONS, PROD)) + "]"


# ================================================================ A · Haute horlogerie
A_SWEEP = 270  # course de l'aiguille du thermostat


def a_thermo():
    cx = cy = 160
    span = T_MAX - T_MIN
    ang = lambda v: -135 + A_SWEEP * frac(v, T_MIN, T_MAX)  # noqa: E731
    ticks = []
    for i in range(span * 10 + 1):
        v = T_MIN + i / 10
        a = ang(v)
        maj, half = i % 10 == 0, i % 5 == 0
        r0 = 141 if maj else (144 if half else 146)
        x0, y0 = pol(cx, cy, r0, a)
        x1, y1 = pol(cx, cy, 150, a)
        cls = "ha-tk is-maj" if maj else ("ha-tk is-half" if half else "ha-tk")
        ticks.append(f'<line class="{cls}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
    idx, nums = [], []
    for v in range(T_MIN, T_MAX + 1):
        a = ang(v)
        long = v % 2 == 0
        # index appliqué : deux plaques (ombre portée puis métal), orientées vers le centre
        h = 17 if long else 10
        idx.append(
            f'<g transform="rotate({P(a)} {cx} {cy})"><rect class="ha-idx-sh" x="{cx - 2.6}" y="{cy - 136}" width="5.2" height="{h}" rx="1"/>'
            f'<rect class="ha-idx" x="{cx - 2.4}" y="{cy - 137.2}" width="4.8" height="{h}" rx="1"/>'
            f'<rect class="ha-idx-hi" x="{cx - 0.4}" y="{cy - 136.4}" width=".8" height="{h - 1.6}"/></g>')
        if long:
            x, y = pol(cx, cy, 104, a)
            nums.append(f'<text class="ha-num" x="{P(x)}" y="{P(y)}">{v}</text>')
    hx, hy = pol(cx, cy, 128, ang(T_IN))
    demand = arc(cx, cy, 124, ang(T_IN), ang(T_SET))
    # petit cadran d'humidité (à 6 h)
    scx, scy, sr = cx, 228, 30
    sub_t = []
    for i in range(0, 13):
        a = -120 + i * 20
        x0, y0 = pol(scx, scy, sr - (5 if i % 3 == 0 else 3), a)
        x1, y1 = pol(scx, scy, sr - 0.5, a)
        sub_t.append(f'<line class="ha-stk{" is-maj" if i % 3 == 0 else ""}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
    hum_a = -120 + 240 * frac(HUM, 20, 80)
    return f"""
<article class="lx-card ha ha-thermo" data-span="5" data-lx-tilt data-thermo="a" data-min="{T_MIN}" data-max="{T_MAX}" data-set="{T_SET}" data-in="{T_IN}">
  <div class="ha-case">
    <header class="ha-h"><h3>Confort</h3><p>Rez-de-chaussée · thermopompe</p></header>
    <div class="ha-dialwrap" data-dial>
      <div class="ha-guil" aria-hidden="true"></div>
      <svg class="ha-dial" viewBox="0 0 320 320" role="img" aria-label="Consigne {fr(T_SET)} degrés, intérieur {fr(T_IN)} degrés">
        <defs>
          <linearGradient id="ha-gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" class="ha-g1"/><stop offset=".5" class="ha-g2"/><stop offset="1" class="ha-g3"/></linearGradient>
          <linearGradient id="ha-steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5d636b"/><stop offset=".5" stop-color="#f4f6f8"/><stop offset="1" stop-color="#7a8088"/></linearGradient>
          <radialGradient id="ha-snail" cx=".5" cy=".5" r=".06" spreadMethod="repeat"><stop offset="0" stop-color="#151515"/><stop offset=".5" stop-color="#202020"/><stop offset="1" stop-color="#151515"/></radialGradient>
          <radialGradient id="ha-cap" cx=".38" cy=".3" r=".8"><stop offset="0" class="ha-g1"/><stop offset=".55" class="ha-g2"/><stop offset="1" class="ha-g3"/></radialGradient>
        </defs>
        <circle class="ha-chapter" cx="{cx}" cy="{cy}" r="151"/>
        <g class="ha-ticks">{''.join(ticks)}</g>
        <path class="ha-demand" d="{demand}" data-demand/>
        <g class="ha-idxs">{''.join(idx)}</g>
        <g class="ha-nums">{''.join(nums)}</g>
        <g class="ha-sub">
          <circle cx="{scx}" cy="{scy}" r="{sr + 2}" class="ha-sub-rim"/>
          <circle cx="{scx}" cy="{scy}" r="{sr}" fill="url(#ha-snail)"/>
          {''.join(sub_t)}
          <text class="ha-sub-l" x="{scx}" y="{scy + 13}">humidité</text>
          <g style="transform:rotate({P(hum_a)}deg);transform-origin:{scx}px {scy}px" class="ha-subhand"><path d="M{scx - 1} {scy + 5}L{scx} {scy - sr + 5}L{scx + 1} {scy + 5}Z"/></g>
          <circle cx="{scx}" cy="{scy}" r="2.4" class="ha-subcap"/>
        </g>
        <g class="ha-window">
          <rect class="ha-win-frame" x="121" y="80" width="78" height="34" rx="3.5"/>
          <rect class="ha-win-disc" x="124" y="83" width="72" height="28" rx="2"/>
          <text class="ha-win-t" x="160" y="104" data-out="set">{fr(T_SET)}°</text>
          <text class="ha-win-l" x="160" y="128">consigne</text>
        </g>
        <g class="ha-hand-in" style="--a:{P(ang(T_IN))}deg"><path d="M159.2 176 L160 {cy - 128} L160.8 176Z"/><circle cx="{P(hx)}" cy="{P(hy)}" r="0"/></g>
        <g class="ha-hand" data-hand style="--a:{P(ang(T_SET))}deg">
          <path class="ha-hand-sh" d="M156.5 186 L160 30 L163.5 186Z"/>
          <path class="ha-hand-b" d="M157 184 L158.6 64 L160 24 L161.4 64 L163 184Z"/>
          <path class="ha-hand-ridge" d="M160 26 L160 182"/>
          <circle cx="160" cy="188" r="7.5" class="ha-hand-tail"/>
        </g>
        <circle cx="160" cy="160" r="9" fill="url(#ha-cap)" class="ha-cap"/>
        <circle cx="160" cy="160" r="3" class="ha-jewel"/>
      </svg>
      <div class="ha-crystal" aria-hidden="true"></div>
    </div>
    <dl class="ha-comps">
      <div><dt>Intérieur</dt><dd><b data-out="in">{fr(T_IN)}</b> °C</dd></div>
      <div><dt>Humidité</dt><dd><b>{HUM}</b> %</dd></div>
      <div><dt>Extérieur</dt><dd><b>{fr(T_OUT, 0)}</b> °C</dd></div>
    </dl>
    <div class="ha-crowns">
      <button class="ha-crown" type="button" data-step="-0.5" aria-label="Baisser la consigne d’un demi-degré">{ico("minus")}</button>
      <p class="ha-status" data-out="status" aria-live="polite">Chauffe en douceur · {fr(T_SET)}° vers 14 h 50</p>
      <button class="ha-crown" type="button" data-step="0.5" aria-label="Monter la consigne d’un demi-degré">{ico("plus")}</button>
    </div>
  </div>
</article>"""


def a_subdial(key, label, cx, cy, r, val, vmax, unit_note):
    ticks = []
    for i in range(0, 41):
        a = -140 + i * 7
        maj = i % 10 == 0
        x0, y0 = pol(cx, cy, r - (7 if maj else 4), a)
        x1, y1 = pol(cx, cy, r - 1, a)
        ticks.append(f'<line class="ha-stk{" is-maj" if maj else ""}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
    a = -140 + 280 * frac(val, 0, vmax)
    return f"""<g class="ha-sd" data-node="{key}">
      <circle cx="{cx}" cy="{cy}" r="{r + 5}" class="ha-sd-rim"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ha-snail2)"/>
      <path class="ha-sd-val" d="{arc(cx, cy, r - 10, -140, a if a > -139 else -139)}" data-arc="{key}" data-cx="{cx}" data-cy="{cy}" data-r="{r - 10}" data-max="{vmax}"/>
      {''.join(ticks)}
      <g class="ha-sd-hand" data-hand-of="{key}" style="--a:{P(a)}deg;transform-origin:{cx}px {cy}px"><path d="M{cx - 1.1} {cy + 8}L{cx} {cy - r + 7}L{cx + 1.1} {cy + 8}Z"/></g>
      <circle cx="{cx}" cy="{cy}" r="2.6" class="ha-subcap"/>
      <text class="ha-sd-l" x="{cx}" y="{cy - 20}">{label}</text>
      <text class="ha-sd-v" x="{cx}" y="{cy + 18}"><tspan data-num="{key}" data-d="1">{fr(val)}</tspan><tspan class="ha-sd-u" dx="3">kW</tspan></text>
      <text class="ha-sd-n" x="{cx}" y="{cy + 33}">{unit_note}</text>

    </g>"""


def a_flux():
    # rouage : quatre compteurs reliés par des canaux gravés; billes d'or = énergie qui circule
    S, R, M, B, H = (320, 86), (104, 214), (536, 214), (320, 342), (320, 214)
    chans = {
        "s": f"M{S[0]} {S[1] + 62}L{H[0]} {H[1] - 30}",
        "m": f"M{H[0] + 30} {H[1]}L{M[0] - 62} {M[1]}",
        "b": f"M{H[0]} {H[1] + 30}L{B[0]} {B[1] - 62}",
        "r": f"M{H[0] - 30} {H[1]}L{R[0] + 62} {R[1]}",
    }
    beads = []
    for k, n, dur in (("s", 3, 2.6), ("m", 3, 2.8), ("b", 2, 3.2), ("r", 1, 3.6)):
        for i in range(n):
            beads.append(f'<circle r="3" class="ha-bead"><animateMotion dur="{dur}s" begin="-{P(dur * i / n)}s" repeatCount="indefinite"><mpath href="#ha-ch-{k}"/></animateMotion></circle>')
    chan_svg = "".join(f'<path id="ha-ch-{k}" class="ha-chan" d="{d}"/><path class="ha-chan-in" d="{d}"/>' for k, d in chans.items())
    # pont gravé (forme de platine) sous les compteurs
    bridge = f"M{S[0] - 40} {S[1] + 40}Q{H[0]} {H[1] - 60} {M[0] - 40} {M[1] - 40}Q{H[0] + 60} {H[1]} {B[0] + 40} {B[1] - 40}Q{H[0]} {H[1] + 60} {R[0] + 40} {R[1] + 40}Q{H[0] - 60} {H[1]} {S[0] - 40} {S[1] + 40}Z"
    balance = "".join(f'<line x1="{H[0]}" y1="{H[1]}" x2="{P(pol(H[0], H[1], 22, a)[0])}" y2="{P(pol(H[0], H[1], 22, a)[1])}"/>' for a in (0, 120, 240))
    legend = "".join(
        f'<div class="ha-leg-i"><dt>{lab}</dt><dd><b data-num="{k}" data-d="1">{fr(FLOW[k])}</b> kW<small>{note}</small></dd></div>'
        for k, lab, note in (("solaire", "Solaire", "toit · 14,4 kWc"), ("batteries", "Batteries", "en charge"),
                             ("maison", "Maison", "consommation"), ("reseau", "Hydro-Québec", "injection")))
    return f"""
<article class="lx-card ha ha-flux" data-span="7" data-lx-tilt data-flow>
  <div class="ha-case">
    <header class="ha-h"><h3>Flux d’énergie</h3><p>Le soleil couvre la maison et recharge les batteries</p></header>
    <div class="ha-movement">
      <div class="ha-perlage" aria-hidden="true"></div>
      <svg class="ha-flow" viewBox="0 0 640 428" role="img" aria-label="Solaire {fr(FLOW['solaire'])} kilowatts vers la maison, les batteries et le réseau">
        <defs>
          <radialGradient id="ha-snail2" cx=".5" cy=".5" r=".05" spreadMethod="repeat"><stop offset="0" stop-color="#141414"/><stop offset=".5" stop-color="#1e1e1e"/><stop offset="1" stop-color="#141414"/></radialGradient>
          <radialGradient id="ha-cap2" cx=".38" cy=".3" r=".8"><stop offset="0" class="ha-g1"/><stop offset=".55" class="ha-g2"/><stop offset="1" class="ha-g3"/></radialGradient>
        </defs>
        {chan_svg}
        <g class="ha-beads">{''.join(beads)}</g>
        {a_subdial("solaire", "Solaire", S[0], S[1], 58, FLOW["solaire"], 14.4, "production")}
        {a_subdial("reseau", "Hydro-Québec", R[0], R[1], 58, FLOW["reseau"], 10, "injection")}
        {a_subdial("maison", "Maison", M[0], M[1], 58, FLOW["maison"], 10, "consommation")}
        {a_subdial("batteries", "Batteries", B[0], B[1], 58, FLOW["batteries"], 10, "en charge")}
        <g class="ha-balance">
          <circle cx="{H[0]}" cy="{H[1]}" r="30" class="ha-bal-rim"/>
          <g class="ha-bal-wheel" style="transform-origin:{H[0]}px {H[1]}px"><circle cx="{H[0]}" cy="{H[1]}" r="22" class="ha-bal-ring"/>{balance}</g>
          <circle cx="{H[0]}" cy="{H[1]}" r="6" fill="url(#ha-cap2)"/>
          <circle cx="{H[0]}" cy="{H[1]}" r="2.2" class="ha-jewel"/>
        </g>
      </svg>
    </div>
    <dl class="ha-legend">{legend}</dl>
  </div>
</article>"""


def a_batt():
    cx, cy, r = 150, 150, 112
    a0, a1 = -60, 60
    ticks, nums = [], []
    for i in range(0, 41):
        a = a0 + (a1 - a0) * i / 40
        maj = i % 10 == 0
        x0, y0 = pol(cx, cy, r - (14 if maj else 8), a)
        x1, y1 = pol(cx, cy, r, a)
        ticks.append(f'<line class="ha-tk{" is-maj" if maj else ""}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
        if maj:
            x, y = pol(cx, cy, r - 28, a)
            nums.append(f'<text class="ha-num is-sm" x="{P(x)}" y="{P(y)}">{i * 100 // 40}</text>')
    soc_a = a0 + (a1 - a0) * SOC / 100
    res_a = a0 + (a1 - a0) * RESERVE / 100
    packs = "".join(f"""
      <div class="ha-pack">
        <div class="ha-pack-h"><span>{n}</span><b><span data-count="{p}">{p}</span> %</b></div>
        <div class="ha-lin" style="--p:{p}"><i></i>{''.join('<s></s>' for _ in range(11))}</div>
        <p class="ha-pack-m">{fr(v)} V · {fr(t)} °C · {cyc} cycles</p>
      </div>""" for n, p, v, t, cyc, hi, lo in PACKS)
    return f"""
<article class="lx-card ha ha-batt" data-span="4" data-lx-tilt>
  <div class="ha-case">
    <header class="ha-h"><h3>Batteries</h3><p>Réserve de marche · LiFePO₄ · {CAP} kWh</p></header>
    <div class="ha-reserve">
      <div class="ha-fan-guil" aria-hidden="true"></div>
      <svg class="ha-fan" viewBox="0 0 300 172" role="img" aria-label="Batteries à {SOC} pour cent">
        <path class="ha-fan-track" d="{arc(cx, cy, r + 6, a0, a1)}"/>
        <path class="ha-fan-res" d="{arc(cx, cy, r + 6, a0, res_a)}"/>
        <path class="ha-fan-val" d="{arc(cx, cy, r + 6, a0, a1)}" pathLength="100" style="--len:{P(100 * (soc_a - a0) / (a1 - a0))}"/>
        {''.join(ticks)}{''.join(nums)}
        <text class="ha-fan-res-l" x="{P(pol(cx, cy, r + 18, res_a)[0])}" y="{P(pol(cx, cy, r + 18, res_a)[1])}">réserve</text>
        <g class="ha-fan-hand" style="--a:{P(soc_a)}deg;transform-origin:{cx}px {cy}px"><path d="M{cx - 2.2} {cy - 58}L{cx - .6} {cy - r + 6}L{cx} {cy - r}L{cx + .6} {cy - r + 6}L{cx + 2.2} {cy - 58}Z"/><circle cx="{cx}" cy="{cy - 58}" r="3.2"/></g>
      </svg>
      <div class="ha-fan-read"><b><span data-count="{SOC}">{SOC}</span><small>%</small></b><span>{fr(CAP * SOC / 100)} kWh · ≈ 9 h de panne</span></div>
    </div>
    <div class="ha-packs">{packs}</div>
  </div>
</article>"""


def a_cams():
    main = CAMS[0]
    thumbs = "".join(
        f'<button type="button" class="ha-port{" is-on" if i == 0 else ""}" data-cam="{k}" data-src="{src}" data-name="{n}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'<img src="{src}" alt="" loading="lazy"><span>{n}</span></button>'
        for i, (k, n, src, _) in enumerate(CAMS))
    return f"""
<article class="lx-card ha ha-cams" data-span="8" data-lx-tilt data-cams>
  <div class="ha-case">
    <header class="ha-h"><h3>Sécurité</h3><p>3 caméras · système armé, mode nuit à 23 h</p></header>
    <div class="ha-cam-body">
      <figure class="ha-caseback">
        <img src="{main[2]}" alt="Vue de la caméra {main[1]}" data-cam-img>
        <div class="ha-sapphire" aria-hidden="true"></div>
        <figcaption>
          <span class="ha-cart" data-armed-l><i></i>Armé</span>
          <span class="ha-cam-n" data-cam-name>{main[1]}</span>
          <span class="ha-cam-t" data-clock>14:20:00</span>
        </figcaption>
      </figure>
      <div class="ha-cam-side">
        <div class="ha-ports" role="group" aria-label="Choisir une caméra">{thumbs}</div>
        <button type="button" class="ha-bolt is-on" data-arm aria-pressed="true"><span class="ha-bolt-t"><i></i></span><span><b data-arm-l>Système armé</b><small data-arm-s>Périmètre et mouvement</small></span></button>
      </div>
    </div>
  </div>
</article>"""


def a_hist():
    cx, cy = 170, 170
    base, k_out, k_in = 92, 6.8, 10.5

    # secteurs d'anneau : extérieur = production, intérieur = consommation
    def sector(r0, r1, a0, a1):
        p0 = pol(cx, cy, r0, a0); p1 = pol(cx, cy, r1, a0); p2 = pol(cx, cy, r1, a1); p3 = pol(cx, cy, r0, a1)
        return (f"M{P(p0[0])} {P(p0[1])}L{P(p1[0])} {P(p1[1])}A{P(r1)} {P(r1)} 0 0 1 {P(p2[0])} {P(p2[1])}"
                f"L{P(p3[0])} {P(p3[1])}A{P(r0)} {P(r0)} 0 0 0 {P(p0[0])} {P(p0[1])}Z")
    prod_pts = [f'<path class="ha-h-p" data-hs="{h}" d="{sector(base + 4, base + 4 + PROD[h] * k_out, h * 15 + 2.2, (h + 1) * 15 - 2.2)}"/>'
                for h in range(24) if PROD[h] > 0]
    cons_pts = [f'<path class="ha-h-c" data-hs="{h}" d="{sector(base - 2 - CONS[h] * k_in, base - 2, h * 15 + 4.5, (h + 1) * 15 - 4.5)}"/>'
                for h in range(24)]
    hits = "".join(f'<path class="ha-h-hit" data-h="{h}" d="{sector(30, 162, h * 15, (h + 1) * 15)}"/>' for h in range(24))
    bezel = []
    for h in range(24):
        a = h * 15
        x, y = pol(cx, cy, 158, a + 7.5)
        if h % 2 == 0:
            bezel.append(f'<text class="ha-bz" x="{P(x)}" y="{P(y)}">{h if h else 24}</text>')
        else:
            bezel.append(f'<circle class="ha-bz-dot" cx="{P(x)}" cy="{P(y)}" r="1.4"/>')
    now_a = NOW_H * 15 + 20 * 15 / 60
    return f"""
<article class="lx-card ha ha-hist" data-span="7" data-lx-tilt data-hist='{series_json()}'>
  <div class="ha-case">
    <header class="ha-h"><h3>Les dernières 24 heures</h3><p>Lunette 24 h · or : production · acier : consommation</p></header>
    <div class="ha-hist-body">
      <div class="ha-gmt">
        <div class="ha-gmt-guil" aria-hidden="true"></div>
        <svg viewBox="0 0 340 340" role="img" aria-label="Production {fr(TOT_P)} kilowattheures, consommation {fr(TOT_C)} kilowattheures sur 24 heures">
          <circle class="ha-bz-ring" cx="{cx}" cy="{cy}" r="166"/>
          <circle class="ha-bz-in" cx="{cx}" cy="{cy}" r="150"/>
          {''.join(bezel)}
          <circle class="ha-h-base" cx="{cx}" cy="{cy}" r="{base + 1}"/>
          <g>{''.join(cons_pts)}</g><g>{''.join(prod_pts)}</g>
          <g class="ha-h-hits">{hits}</g>
          <g class="ha-gmt-hand" style="--a:{P(now_a)}deg;transform-origin:{cx}px {cy}px"><path d="M{cx - 1.2} {cy + 14}L{cx} {cy - 146}L{cx + 1.2} {cy + 14}Z"/><path class="ha-gmt-tip" d="M{cx} {cy - 150}l-5 10h10z"/></g>
          <circle cx="{cx}" cy="{cy}" r="34" class="ha-gmt-win"/>
          <text class="ha-gmt-h" x="{cx}" y="{cy - 6}" data-hist-h>14 h</text>
          <text class="ha-gmt-v" x="{cx}" y="{cy + 13}" data-hist-v>4,4 · 2,8</text>
        </svg>
      </div>
      <dl class="ha-totals">
        <div><dt>Produit par le toit</dt><dd><b data-count="{TOT_P}" data-d="1">{fr(TOT_P)}</b> kWh</dd></div>
        <div><dt>Consommé par la maison</dt><dd><b data-count="{TOT_C}" data-d="1">{fr(TOT_C)}</b> kWh</dd></div>
        <div><dt>Couvert par le soleil</dt><dd><b data-count="{SELF}">{SELF}</b> %</dd></div>
        <p class="ha-hint">Survolez la lunette pour lire une heure.</p>
      </dl>
    </div>
  </div>
</article>"""


def a_car():
    def tri(key, label, val, vlo, vhi, unit, ticks_n, band=None, tone="acc", text=None):
        cx = cy = 50
        r = 40
        t = []
        for i in range(ticks_n + 1):
            a = -120 + 240 * i / ticks_n
            maj = i % (ticks_n // 4 or 1) == 0
            x0, y0 = pol(cx, cy, r - (6 if maj else 3.5), a)
            x1, y1 = pol(cx, cy, r, a)
            t.append(f'<line class="ha-stk{" is-maj" if maj else ""}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
        b = ""
        if band:
            b = f'<path class="ha-tri-band is-{tone}" d="{arc(cx, cy, r - 9, -120 + 240 * frac(band[0], vlo, vhi), -120 + 240 * frac(band[1], vlo, vhi))}"/>'
        a = -120 + 240 * frac(val, vlo, vhi)
        shown = text or f"{fr(val) if isinstance(val, float) else val}"
        return f"""<div class="ha-tri" data-tri="{key}">
          <svg viewBox="0 0 100 100" aria-hidden="true">
            <circle cx="50" cy="50" r="46" class="ha-sd-rim"/><circle cx="50" cy="50" r="{r + 1}" fill="url(#ha-snail3)"/>
            {b}{''.join(t)}
            <g class="ha-tri-hand" style="--a:{P(a)}deg" data-tri-hand><path d="M49 58L50 14L51 58Z"/></g>
            <circle cx="50" cy="50" r="3" class="ha-subcap"/>
          </svg>
          <p><b data-tri-v>{shown}</b>{f'<small>{unit}</small>' if unit else ''}</p><span>{label}</span>
        </div>"""
    return f"""
<article class="lx-card ha ha-car" data-span="5" data-lx-tilt data-car>
  <div class="ha-case">
    <header class="ha-h"><h3>{CAR['nom']}</h3><p>{CAR['baie']} · garage de collection · {CAR['garage']} °C</p></header>
    <figure class="ha-car-ph"><img src="{CAR['img']}" alt="La Lamborghini Huracán noire dans le garage de collection éclairé" loading="lazy"><div class="ha-sapphire" aria-hidden="true"></div></figure>
    <svg width="0" height="0" aria-hidden="true" style="position:absolute"><defs><radialGradient id="ha-snail3" cx=".5" cy=".5" r=".07" spreadMethod="repeat"><stop offset="0" stop-color="#141414"/><stop offset=".5" stop-color="#1f1f1f"/><stop offset="1" stop-color="#141414"/></radialGradient></defs></svg>
    <div class="ha-tris">
      {tri("v", "Mainteneur", CAR['v'], 11.8, 13.2, "V", 28, band=(12.4, 13.0), tone="ok")}
      {tri("hum", "Humidité", CAR['hum'], 20, 80, "%", 24, band=(40, 50), tone="water")}
      {tri("porte", "Porte 1", 1.0, 0, 1, "", 4, text="Fermée")}
    </div>
    <button type="button" class="ha-door" data-door aria-pressed="false">{ico("door")}<span data-door-l>Ouvrir la porte 1</span></button>
  </div>
</article>"""


# ================================================================ B · Cockpit futuriste
def ck_shell(cls, span, inner, extra=""):
    return f"""
<article class="lx-card ck {cls}" data-span="{span}" data-lx-tilt="3d"{extra}>
  <div class="ck-plate" aria-hidden="true"></div>
  <div class="ck-edge" aria-hidden="true"></div>
  <div class="ck-in">{inner}</div>
  <div class="ck-sweep" aria-hidden="true"></div>
</article>"""


def ck_head(title, sub, ic):
    return f'<header class="ck-h">{ico(ic, "ck-hi")}<div><h3>{title}</h3><p>{sub}</p></div><span class="ck-live"><i></i>En direct</span></header>'


def b_thermo():
    cx, cy, r = 200, 196, 160
    a0, a1 = -100, 100
    ang = lambda v: a0 + (a1 - a0) * frac(v, T_MIN, T_MAX)  # noqa: E731
    ticks = []
    for i in range((T_MAX - T_MIN) * 4 + 1):
        v = T_MIN + i / 4
        a = ang(v)
        maj = i % 4 == 0
        x0, y0 = pol(cx, cy, r + (8 if maj else 10), a)
        x1, y1 = pol(cx, cy, r + 16, a)
        ticks.append(f'<line class="ck-tk{" is-maj" if maj else ""}" x1="{P(x0)}" y1="{P(y0)}" x2="{P(x1)}" y2="{P(y1)}"/>')
        if maj and (T_MIN + i // 4) % 5 == 0 or (maj and v in (T_MIN, T_MAX)):
            x, y = pol(cx, cy, r + 30, a)
            ticks.append(f'<text class="ck-tn" x="{P(x)}" y="{P(y)}">{int(v)}</text>')
    track = arc(cx, cy, r, a0, a1)
    ix, iy = pol(cx, cy, r, ang(T_IN))
    inner = f"""
    {ck_head("Climat", "Rez-de-chaussée · thermopompe", "thermo")}
    <div class="ck-clim" data-dial>
      <svg class="ck-arc" viewBox="0 0 400 236" role="img" aria-label="Consigne {fr(T_SET)} degrés">
        <defs>
          <linearGradient id="ck-arcg" x1="0" x2="1"><stop offset="0" class="ck-s0"/><stop offset="1" class="ck-s1"/></linearGradient>
          <filter id="ck-glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
        </defs>
        <g class="ck-ticks">{''.join(ticks)}</g>
        <path class="ck-track" d="{track}"/>
        <path class="ck-val-glow" d="{track}" pathLength="100" filter="url(#ck-glow)" data-arcval/>
        <path class="ck-val" d="{track}" pathLength="100" data-arcval/>
        <circle class="ck-in-mark" cx="{P(ix)}" cy="{P(iy)}" r="3.2"/>
        <g class="ck-knob" data-knob style="--a:{P(ang(T_SET))}deg;transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy - r}" r="11" class="ck-knob-o"/><circle cx="{cx}" cy="{cy - r}" r="4" class="ck-knob-i"/></g>
      </svg>
      <div class="ck-read">
        <p class="ck-big"><span class="ck-seg" data-out="set">{fr(T_SET)}</span><small>°C</small></p>
        <p class="ck-sub" data-out="status">Chauffe · cible atteinte vers 14 h 50</p>
      </div>
      <button class="ck-pad is-l" type="button" data-step="-0.5" aria-label="Baisser la consigne d’un demi-degré">{ico("left")}</button>
      <button class="ck-pad is-r" type="button" data-step="0.5" aria-label="Monter la consigne d’un demi-degré">{ico("right")}</button>
    </div>
    <div class="ck-strip">
      <div><span>Intérieur</span><b><span data-out="in">{fr(T_IN)}</span><small>°C</small></b></div>
      <div><span>Humidité</span><b>{HUM}<small>%</small></b></div>
      <div><span>Extérieur</span><b>{fr(T_OUT, 0)}<small>°C</small></b></div>
      <div class="ck-fan"><span>Ventilation</span><i class="is-on"></i><i class="is-on"></i><i></i><i></i></div>
    </div>"""
    return ck_shell("ck-thermo", 5, inner, f' data-thermo="b" data-min="{T_MIN}" data-max="{T_MAX}" data-set="{T_SET}" data-in="{T_IN}"')


def b_flux():
    nodes = {"solaire": (90, 70, "sun", "Solaire", "14,4 kWc"), "reseau": (90, 270, "grid", "Hydro-Québec", "injection"),
             "maison": (550, 70, "home", "Maison", "consommation"), "batteries": (550, 270, "bat", "Batteries", "en charge")}
    hub = (320, 170)
    paths = {
        "solaire": f"M152 70 C240 70 250 170 {hub[0] - 26} {hub[1]}",
        "maison": f"M{hub[0] + 26} {hub[1]} C390 170 400 70 488 70",
        "batteries": f"M{hub[0] + 26} {hub[1]} C390 170 400 270 488 270",
        "reseau": f"M{hub[0] - 26} {hub[1]} C250 170 240 270 152 270",
    }
    rails = "".join(f'<path class="ck-rail" d="{d}"/><path class="ck-pulse is-{k}" d="{d}" pathLength="100"/>' for k, d in paths.items())
    chips = "".join(f"""
      <div class="ck-node is-{k}" style="--x:{x / 6.4}%;--y:{y / 3.4}%">
        {ico(ic, "ck-ni")}<div><span>{lab}</span><b><span data-num="{k}" data-d="1">{fr(FLOW[k])}</span><small>kW</small></b><em>{note}</em></div>
      </div>""" for k, (x, y, ic, lab, note) in nodes.items())
    inner = f"""
    {ck_head("Flux d’énergie", "Le soleil couvre la maison et recharge les batteries", "sun")}
    <div class="ck-flow" data-flow>
      <div class="ck-floor" aria-hidden="true"></div>
      <svg class="ck-flow-svg" viewBox="0 0 640 340" preserveAspectRatio="none" aria-hidden="true">{rails}</svg>
      <div class="ck-hub" style="--x:50%;--y:50%"><span>Autoconsommation</span><b>100<small>%</small></b></div>
      {chips}
    </div>"""
    return ck_shell("ck-flux", 7, inner)


def b_batt():
    mods = ""
    for n, p, v, t, cyc, hi, lo in PACKS:
        cells = []
        for i in range(16):
            cv = lo + (hi - lo) * ((i * 7) % 16) / 15
            cells.append(f'<i style="--h:{P(0.55 + 0.45 * (cv - 3.25) / 0.02)}" title="Cellule {i + 1} · {fr(cv, 3)} V"></i>')
        mods += f"""
      <div class="ck-mod" style="--p:{p}">
        <div class="ck-mod-h"><span>{n}</span><b><span data-count="{p}">{p}</span><small>%</small></b></div>
        <div class="ck-cells" aria-hidden="true">{''.join(cells)}<s></s></div>
        <p>{fr(v)} V · {fr(t)} °C · cellules {fr(lo, 3)} à {fr(hi, 3)} V</p>
      </div>"""
    inner = f"""
    {ck_head("Batteries", f"LiFePO₄ 16 S · {CAP} kWh", "bat")}
    <div class="ck-soc">
      <p class="ck-big is-ok"><span class="ck-seg" data-count="{SOC}">{SOC}</span><small>%</small></p>
      <div class="ck-soc-m"><b>{fr(CAP * SOC / 100)} kWh</b><span>≈ 9 h de panne · réserve {RESERVE} %</span><span class="ck-charge"><i></i>Charge +{fr(FLOW['batteries'])} kW</span></div>
    </div>
    <div class="ck-mods">{mods}</div>"""
    return ck_shell("ck-batt", 4, inner)


def b_cams():
    tabs = "".join(
        f'<button type="button" class="ck-tab{" is-on" if i == 0 else ""}" data-cam="{k}" data-src="{src}" data-name="{n}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'<img src="{src}" alt="" loading="lazy"><span>{n}</span></button>'
        for i, (k, n, src, _) in enumerate(CAMS))
    inner = f"""
    <div class="ck-feed">
      <img src="{CAMS[0][2]}" alt="Vue de la caméra {CAMS[0][1]}" data-cam-img>
      <div class="ck-hud" aria-hidden="true"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i><span class="ck-scan"></span></div>
      <div class="ck-feed-top">
        <span class="ck-armed" data-armed-l><i></i>Armé · mode nuit 23 h</span>
        <span class="ck-rec"><i></i><span data-clock>14:20:00</span></span>
      </div>
      <div class="ck-feed-bot">
        <div><h3 data-cam-name>{CAMS[0][1]}</h3><p>Aucun mouvement · 4K · vision nocturne</p></div>
        <button type="button" class="ck-arm is-on" data-arm aria-pressed="true"><span class="ck-arm-t"><i></i></span><span data-arm-l>Système armé</span></button>
      </div>
    </div>
    <div class="ck-tabs" role="group" aria-label="Choisir une caméra">{tabs}</div>"""
    return ck_shell("ck-cams", 8, inner, " data-cams")


def chart_paths(w, h, pad_t, pad_b, vmax, smooth=True):
    def pts(arr):
        return [(w * i / 23, pad_t + (h - pad_t - pad_b) * (1 - v / vmax)) for i, v in enumerate(arr)]

    def line(ps):
        d = f"M{P(ps[0][0])} {P(ps[0][1])}"
        for i in range(1, len(ps)):
            x0, y0 = ps[i - 1]
            x1, y1 = ps[i]
            mx = (x0 + x1) / 2
            d += f"C{P(mx)} {P(y0)} {P(mx)} {P(y1)} {P(x1)} {P(y1)}"
        return d
    pc, pp = pts(CONS), pts(PROD)
    base = h - pad_b
    lc, lp = line(pc), line(pp)
    return lc, lp, f"{lc}L{P(w)} {P(base)}L0 {P(base)}Z", f"{lp}L{P(w)} {P(base)}L0 {P(base)}Z"


def b_hist():
    W, H = 640, 220
    lc, lp, ac, ap = chart_paths(W, H, 16, 22, 8)
    grid = "".join(f'<line class="ck-gl" x1="0" x2="{W}" y1="{P(16 + (H - 38) * i / 4)}" y2="{P(16 + (H - 38) * i / 4)}"/>' for i in range(5))
    vgrid = "".join(f'<line class="ck-gl is-v" y1="16" y2="{H - 22}" x1="{P(W * i / 23)}" x2="{P(W * i / 23)}"/>' for i in range(0, 24, 3))
    labels = "".join(f'<span style="left:{P(100 * i / 23)}%">{i} h</span>' for i in range(0, 24, 3))
    inner = f"""
    {ck_head("Historique · 24 h", "Production solaire et consommation, heure par heure", "grid")}
    <div class="ck-kpis">
      <div><span>Produit</span><b class="is-acc"><span class="ck-seg" data-count="{TOT_P}" data-d="1">{fr(TOT_P)}</span><small>kWh</small></b></div>
      <div><span>Consommé</span><b><span class="ck-seg" data-count="{TOT_C}" data-d="1">{fr(TOT_C)}</span><small>kWh</small></b></div>
      <div><span>Couvert par le soleil</span><b><span class="ck-seg" data-count="{SELF}">{SELF}</span><small>%</small></b></div>
    </div>
    <div class="ck-chart" data-hist='{series_json()}' data-w="{W}">
      <svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">
        <defs>
          <linearGradient id="ck-ap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="ck-ap0"/><stop offset="1" class="ck-ap1"/></linearGradient>
          <linearGradient id="ck-ac" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
        </defs>
        {grid}{vgrid}
        <path class="ck-area-p" d="{ap}"/><path class="ck-area-c" d="{ac}"/>
        <path class="ck-line-c" d="{lc}" pathLength="100"/>
        <path class="ck-line-p-glow" d="{lp}" pathLength="100"/>
        <path class="ck-line-p" d="{lp}" pathLength="100"/>
        <line class="ck-now" x1="{P(W * (NOW_H + 1 / 3) / 23)}" x2="{P(W * (NOW_H + 1 / 3) / 23)}" y1="10" y2="{H - 22}"/>
      </svg>
      <div class="ck-cross" data-cross hidden><i></i><div class="ck-tip"><b data-tip-h>14 h</b><span><i class="is-p"></i><span data-tip-p>4,4</span> kW</span><span><i class="is-c"></i><span data-tip-c>2,8</span> kW</span></div></div>
      <div class="ck-xl">{labels}</div>
    </div>"""
    return ck_shell("ck-hist", 7, inner)


def b_car():
    callouts = [("v", 34, 58, "Mainteneur", f"{fr(CAR['v'])} V", "ok"), ("hum", 58, 16, "Humidité", f"{CAR['hum']} %", "water"),
                ("porte", 88, 40, "Porte 1", "Fermée", "acc")]
    co = "".join(f'<div class="ck-co is-{tone}{" is-l" if x > 70 else ""}" style="--x:{x}%;--y:{y}%" data-co="{k}"><i></i><span><em>{lab}</em><b data-co-v>{val}</b></span></div>'
                 for k, x, y, lab, val, tone in callouts)
    inner = f"""
    <div class="ck-car">
      <div class="ck-car-ph" data-depth><img src="{CAR['img']}" alt="La Lamborghini Huracán noire dans le garage de collection" loading="lazy"></div>
      <div class="ck-car-shade" aria-hidden="true"></div>
      <div class="ck-car-top">{ico("car", "ck-hi")}<div><h3>{CAR['nom']}</h3><p>{CAR['baie']} · garage {CAR['garage']} °C</p></div></div>
      <div class="ck-cos" data-depth2>{co}</div>
      <div class="ck-car-bot">
        <div class="ck-vbar"><span>Mainteneur de charge</span><div class="ck-vbar-t"><i style="--p:{P(100 * frac(CAR['v'], 11.8, 13.2))}"></i></div><b>{fr(CAR['v'])} V · 100 %</b></div>
        <button type="button" class="ck-door" data-door aria-pressed="false">{ico("door")}<span data-door-l>Ouvrir la porte 1</span></button>
      </div>
    </div>"""
    return ck_shell("ck-carc", 5, inner, " data-car")


# ================================================================ C · Architecture et lumière
def c_thermo():
    ticks = "".join(f'<i class="{"is-maj" if v % 1 == 0 else ""}" style="left:{P(100 * frac(v, T_MIN, T_MAX))}%"></i>' for v in [T_MIN + i / 2 for i in range((T_MAX - T_MIN) * 2 + 1)])
    nums = "".join(f'<span style="left:{P(100 * frac(v, T_MIN, T_MAX))}%">{v}</span>' for v in range(T_MIN + 1, T_MAX + 1, 2))
    return f"""
<article class="lx-card al al-thermo is-warm" data-span="5" data-lx-tilt data-thermo="c" data-min="{T_MIN}" data-max="{T_MAX}" data-set="{T_SET}" data-in="{T_IN}">
  <div class="al-ph"><img src="/media/solutions/environnements-intelligents.webp" alt="Le salon de la résidence au crépuscule, vue sur le lac" loading="lazy" style="object-position:62% 50%"></div>
  <div class="al-light" aria-hidden="true"></div>
  <div class="al-veil" aria-hidden="true"></div>
  <div class="al-in">
    <header class="al-h"><p class="al-k">Confort · salon</p><span class="al-state" data-out="state">Chauffe en douceur</span></header>
    <div class="al-hero">
      <p class="al-big"><span data-out="set">{fr(T_SET)}</span><sup>°</sup></p>
      <p class="al-lede" data-out="status">La pièce atteindra {fr(T_SET)}° vers 14 h 50. La thermopompe travaille au tiers de sa puissance.</p>
    </div>
    <div class="al-frost">
      <div class="al-slider" data-dial>
        <div class="al-rail">{ticks}<b class="al-fill"></b><b class="al-in-mark" style="left:{P(100 * frac(T_IN, T_MIN, T_MAX))}%"></b><b class="al-thumb" data-thumb></b></div>
        <div class="al-nums">{nums}</div>
      </div>
      <div class="al-row">
        <button class="al-btn" type="button" data-step="-0.5" aria-label="Baisser la consigne d’un demi-degré">{ico("minus")}</button>
        <dl class="al-facts">
          <div><dt>Intérieur</dt><dd><span data-out="in">{fr(T_IN)}</span>°</dd></div>
          <div><dt>Humidité</dt><dd>{HUM} %</dd></div>
          <div><dt>Dehors</dt><dd>{fr(T_OUT, 0)}°</dd></div>
        </dl>
        <button class="al-btn" type="button" data-step="0.5" aria-label="Monter la consigne d’un demi-degré">{ico("plus")}</button>
      </div>
    </div>
  </div>
</article>"""


def c_flux():
    steps = [("solaire", "Le toit produit", "14,4 kWc · plein sud"), ("maison", "La maison consomme", "chauffage, cellier, éclairage"),
             ("batteries", "Les batteries reçoivent", "64 % · pleines vers 17 h"), ("reseau", "Hydro-Québec reçoit le surplus", "injection au réseau")]
    rows = "".join(f'<li class="al-fl is-{k}"><span class="al-fl-dot"></span><div><p>{t}</p><small>{s}</small></div><b><span data-num="{k}" data-d="1">{fr(FLOW[k])}</span><small>kW</small></b></li>'
                   for k, t, s in steps)
    return f"""
<article class="lx-card al al-flux is-warm" data-span="7" data-lx-tilt data-flow>
  <div class="al-ph is-right"><img src="/media/vitrine/accueil/residence-prestige-soir.webp" alt="La résidence au crépuscule, toit solaire et fenêtres éclairées" loading="lazy" style="object-position:60% 50%"></div>
  <div class="al-light" aria-hidden="true"></div>
  <div class="al-veil is-side" aria-hidden="true"></div>
  <div class="al-in al-flux-in">
    <header class="al-h"><p class="al-k">Énergie · maintenant</p><span class="al-state">Autonome</span></header>
    <p class="al-big is-md"><span data-num="solaire" data-d="1">{fr(FLOW['solaire'])}</span><small>kW</small></p>
    <p class="al-lede">Le soleil couvre toute la maison et remplit les batteries. Le surplus part vers le réseau.</p>
    <ol class="al-flow">
      <li class="al-line" aria-hidden="true"><i class="al-sp"></i><i class="al-sp is-2"></i></li>
      {rows}
    </ol>
  </div>
</article>"""


def c_batt():
    packs = "".join(f'<div class="al-pk"><p>{n}</p><b><span data-count="{p}">{p}</span> %</b><small>{fr(v)} V · {fr(t)} °C · {cyc} cycles</small></div>' for n, p, v, t, cyc, hi, lo in PACKS)
    return f"""
<article class="lx-card al al-batt" data-span="4" data-lx-tilt>
  <div class="al-col" style="--p:{SOC}" aria-hidden="true"><i></i><span></span></div>
  <div class="al-in">
    <header class="al-h"><p class="al-k">Batteries · {CAP} kWh</p><span class="al-state is-ok">En charge</span></header>
    <p class="al-big is-ok"><span data-count="{SOC}">{SOC}</span><small>%</small></p>
    <p class="al-lede">{fr(CAP * SOC / 100)} kWh en réserve. Assez pour neuf heures de panne sur les circuits essentiels.</p>
    <div class="al-pks">{packs}</div>
    <p class="al-foot">Réserve de panne gardée à {RESERVE} % · charge +{fr(FLOW['batteries'])} kW</p>
  </div>
</article>"""


def c_cams():
    th = "".join(
        f'<button type="button" class="al-th{" is-on" if i == 0 else ""}" data-cam="{k}" data-src="{src}" data-name="{n}" aria-pressed="{"true" if i == 0 else "false"}"><img src="{src}" alt="" loading="lazy"><span>{n}</span></button>'
        for i, (k, n, src, _) in enumerate(CAMS))
    return f"""
<article class="lx-card al al-cams" data-span="8" data-lx-tilt data-cams data-alert-host>
  <div class="al-ph"><img src="{CAMS[0][2]}" alt="Vue de la caméra {CAMS[0][1]}" data-cam-img></div>
  <div class="al-light" aria-hidden="true"></div>
  <div class="al-veil" aria-hidden="true"></div>
  <div class="al-in al-cams-in">
    <header class="al-h"><p class="al-k">Sécurité · <span data-cam-name>{CAMS[0][1]}</span></p><span class="al-state"><span data-armed-l>Armé</span> · <span data-clock>14:20:00</span></span></header>
    <div class="al-cam-foot">
      <div>
        <p class="al-big is-sm" data-alert-title>Tout est calme.</p>
        <p class="al-lede" data-alert-text>Trois caméras veillent. Le mode nuit armera aussi les fenêtres à 23 h.</p>
        <div class="al-acts">
          <button type="button" class="al-pill is-on" data-arm aria-pressed="true"><span data-arm-l>Système armé</span></button>
          <button type="button" class="al-pill is-ghost" data-simulate>Simuler un mouvement</button>
        </div>
      </div>
      <div class="al-ths" role="group" aria-label="Choisir une caméra">{th}</div>
    </div>
  </div>
</article>"""


def c_hist():
    W, H = 640, 200
    lc, lp, ac, ap = chart_paths(W, H, 10, 2, 8)
    hours = "".join(f'<span style="left:{P(100 * i / 23)}%">{i} h</span>' for i in (0, 6, 12, 18, 23))
    return f"""
<article class="lx-card al al-hist" data-span="7" data-lx-tilt>
  <div class="al-in">
    <header class="al-h"><p class="al-k">Les dernières 24 heures</p><span class="al-state">Mardi</span></header>
    <div class="al-hist-top">
      <div><p class="al-big is-md"><span data-count="{TOT_P}" data-d="1">{fr(TOT_P)}</span><small>kWh</small></p><p class="al-cap"><i class="is-p"></i>produits par le toit</p></div>
      <div><p class="al-big is-md is-dim"><span data-count="{TOT_C}" data-d="1">{fr(TOT_C)}</span><small>kWh</small></p><p class="al-cap"><i class="is-c"></i>consommés par la maison</p></div>
      <div><p class="al-big is-md is-dim"><span data-count="{SELF}">{SELF}</span><small>%</small></p><p class="al-cap">couverts par le soleil</p></div>
    </div>
    <div class="al-chart" data-hist='{series_json()}' data-w="{W}">
      <svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">
        <defs><linearGradient id="al-ap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="al-ap0"/><stop offset="1" class="al-ap1"/></linearGradient></defs>
        <path class="al-area-p" d="{ap}"/>
        <path class="al-line-c" d="{lc}" pathLength="100"/>
        <path class="al-line-p" d="{lp}" pathLength="100"/>
        <line class="al-now" x1="{P(W * (NOW_H + 1 / 3) / 23)}" x2="{P(W * (NOW_H + 1 / 3) / 23)}" y1="0" y2="{H}"/>
      </svg>
      <div class="ck-cross al-cross" data-cross hidden><i></i><div class="ck-tip"><b data-tip-h>14 h</b><span><i class="is-p"></i><span data-tip-p>4,4</span> kW</span><span><i class="is-c"></i><span data-tip-c>2,8</span> kW</span></div></div>
      <div class="al-xl">{hours}</div>
    </div>
  </div>
</article>"""


def c_car():
    return f"""
<article class="lx-card al al-car" data-span="5" data-lx-tilt data-car data-alert-host>
  <div class="al-ph"><img src="{CAR['img']}" alt="La Lamborghini Huracán noire dans le garage de collection" loading="lazy" style="object-position:30% 50%"></div>
  <div class="al-light" aria-hidden="true"></div>
  <div class="al-veil" aria-hidden="true"></div>
  <div class="al-in">
    <header class="al-h"><p class="al-k">Collection · {CAR['baie']}</p><span class="al-state is-ok" data-door-state>Remisée</span></header>
    <div class="al-car-foot">
      <h3 class="al-title">Lamborghini Huracán</h3>
      <dl class="al-facts is-3">
        <div><dt>Mainteneur</dt><dd class="is-ok">{fr(CAR['v'])} V</dd></div>
        <div><dt>Humidité</dt><dd>{CAR['hum']} %</dd></div>
        <div><dt>Porte 1</dt><dd data-door-v>Fermée</dd></div>
      </dl>
      <button type="button" class="al-pill is-ghost" data-door aria-pressed="false"><span data-door-l>Ouvrir la porte 1</span></button>
    </div>
  </div>
</article>"""


# ================================================================ Page
DIRS = [
    ("a", "A", "Haute horlogerie",
     "Cadrans guillochés, lunettes usinées dont le reflet suit la souris, verre saphir bombé, index appliqués et aiguilles fines. Chaque carte se lit comme une montre.",
     [a_thermo, a_flux, a_batt, a_cams, a_hist, a_car]),
    ("b", "B", "Cockpit futuriste",
     "Verre en couches qui s’incline sous la main, bords en guide de lumière, grilles fines et chiffres affinés. L’habitacle d’une voiture électrique de luxe.",
     [b_thermo, b_flux, b_batt, b_cams, b_hist, b_car]),
    ("c", "C", "Architecture et lumière",
     "De grandes photos, du verre givré et une lumière d’ambiance qui suit l’état : chaude quand on chauffe, corail quand il faut regarder. La mise en page d’un magazine.",
     [c_thermo, c_flux, c_batt, c_cams, c_hist, c_car]),
]


def section(key, letter, name, text, makers):
    cards = "".join(m() for m in makers)
    return f"""
<section class="lx-dir is-{key}" id="direction-{key}" aria-labelledby="lx-t-{key}">
  <header class="lx-dir-h">
    <span class="lx-letter" aria-hidden="true">{letter}</span>
    <div><h2 id="lx-t-{key}">{name}</h2><p>{text}</p></div>
  </header>
  <div class="lx-grid">{cards}</div>
</section>"""


CONTENT = f"""
<div class="lx" data-lx>
  <section class="lx-top">
    <p class="lx-k">Page privée · laboratoire</p>
    <h1>Trois directions pour les cartes de JARVIS</h1>
    <p class="lx-intro">Les mêmes six cartes, les mêmes données, poussées dans trois directions. Changez de mode en haut, survolez, glissez la consigne, ouvrez une porte. Choisissez celle qui vous donne envie de la toucher.</p>
    <p class="lx-note">Données d’exemple · scène d’un mardi de novembre, 14 h 20</p>
  </section>
  <nav class="lx-bar" aria-label="Directions et mode">
    <div class="lx-bar-in">
      <div class="lx-dirs">{''.join(f'<a href="#direction-{k}"><b>{L}</b><span>{n}</span></a>' for k, L, n, _, _ in DIRS)}</div>
      <div class="lx-modes" role="group" aria-label="Mode d’affichage">
        <button type="button" data-mode-set="signature" aria-pressed="true" class="is-on">Signature</button>
        <button type="button" data-mode-set="platinum" aria-pressed="false">Platinum</button>
        <button type="button" data-mode-set="base" aria-pressed="false">Base</button>
      </div>
    </div>
  </nav>
  {''.join(section(*d) for d in DIRS)}
</div>
"""

PAGE = {
    "url": "/labo-cartes/",
    "v2": True,
    "noindex": True,
    "title": "Laboratoire des cartes | JARVIS Private Systems",
    "description": "Page privée : trois directions de design pour les cartes de JARVIS.",
    "body_class": "lx-page",
    "assets": ["labo"],
    "content": CONTENT,
}
