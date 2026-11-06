# Démo « Réseau et cybersécurité » : la carte vivante du réseau d'une maison.
# Tout est simulé. Ce module produit le HTML (SVG compris) à partir d'une seule
# table de géométrie : disposition large (ordinateur) et haute (téléphone).
# Sans JavaScript, la carte reste lisible dans son état normal; le script
# assets/demos/reseau.js anime les paquets et joue les situations.

import re
from html import escape

# ---------------------------------------------------------------------------
# Icônes (traits, 24 × 24)
# ---------------------------------------------------------------------------
ICONS = {
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/>',
    "fibre": '<path d="M3 17c3.5 0 4.5-3 7.5-3s4 3 7.5 3"/><path d="M3 12c3.5 0 4.5-3 7.5-3s4 3 7.5 3"/><path d="M3 7c3.5 0 4.5-3 7.5-3s4 3 7.5 3"/><circle cx="20.6" cy="17" r="1.3"/>',
    "dish": '<path d="M4.5 19.5a8.5 8.5 0 0 1 0-12l12 12a8.5 8.5 0 0 1-12 0z"/><path d="M10.5 13.5l4.5-4.5"/><circle cx="16.4" cy="7.6" r="1.6"/><path d="M18.5 3.5a5 5 0 0 1 2 2"/>',
    "shield": '<path d="M12 3l7.5 3v5.4c0 4.5-3.1 8-7.5 9.9-4.4-1.9-7.5-5.4-7.5-9.9V6z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/>',
    "switch": '<rect x="2.5" y="7.5" width="19" height="9" rx="2.2"/><path d="M6.5 12h.01M9.5 12h.01M12.5 12h.01M15.5 12h.01" stroke-width="2.6"/><path d="M18.5 10.5v3"/>',
    "hub": '<path d="M12 2.6l8.2 4.7v9.4L12 21.4l-8.2-4.7V7.3z"/><circle cx="12" cy="12" r="3.2"/><path d="M12 2.6v6.2M20.2 16.7l-5.4-3.1M3.8 16.7l5.4-3.1"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.6"/><path d="M11 18.3h2"/>',
    "laptop": '<rect x="4.5" y="5" width="15" height="10.5" rx="1.6"/><path d="M2 19h20"/>',
    "tv": '<rect x="2.5" y="4" width="19" height="12.5" rx="2"/><path d="M8.5 20.5h7M12 16.5v4"/>',
    "gamepad": '<path d="M7 8h10a4.5 4.5 0 0 1 4.5 4.5v.8a3.3 3.3 0 0 1-6 1.9L14.4 14H9.6l-1.1 1.2a3.3 3.3 0 0 1-6-1.9v-.8A4.5 4.5 0 0 1 7 8z"/><path d="M7.5 10.6v3M6 12.1h3"/><path d="M16 11h.01M17.6 12.8h.01" stroke-width="2.4"/>',
    "thermo": '<circle cx="12" cy="12" r="9"/><path d="M7.6 15.4a5.6 5.6 0 0 1 8.8 0"/><path d="M12 12.6l3-3.4"/>',
    "bulb": '<path d="M9.2 18h5.6M10.2 21h3.6"/><path d="M12 3a6 6 0 0 0-3.7 10.7c.8.6 1.1 1.5 1.1 2.4h5.2c0-.9.3-1.8 1.1-2.4A6 6 0 0 0 12 3z"/>',
    "speaker": '<rect x="6" y="2.5" width="12" height="19" rx="2.6"/><circle cx="12" cy="14" r="3.4"/><path d="M12 7h.01" stroke-width="2.4"/>',
    "camera": '<rect x="2.5" y="7" width="13" height="10" rx="2.2"/><path d="M15.5 10.6l6-3v8.8l-6-3z"/>',
    "tablet": '<rect x="4.5" y="2.5" width="15" height="19" rx="2.2"/><path d="M11 18.3h2"/>',
}
SHIELD = "M0-9.5l7 2.8v4.9c0 4.1-2.9 7.3-7 9.1-4.1-1.8-7-5-7-9.1v-4.9z"

# ---------------------------------------------------------------------------
# Appareils et zones (données simulées)
# kind « net » : surtout Internet · « local » : parle surtout à JARVIS
# ---------------------------------------------------------------------------
ZONES = [
    ("famille", "Famille", [
        ("tel", "Téléphone", "Téléphone de la famille", "phone", "net", .5, "Wi-Fi · 42 Mb/s"),
        ("pc", "Ordinateur", "Ordinateur portable", "laptop", "net", .7, "Wi-Fi · 88 Mb/s"),
        ("tv", "Téléviseur", "Téléviseur du salon", "tv", "net", 1.0, "Câble · film en 4K · 25 Mb/s"),
        ("console", "Console", "Console de jeu", "gamepad", "net", .4, "Câble · 12 Mb/s"),
    ]),
    ("objets", "Objets connectés", [
        ("thermo", "Thermostat", "Thermostat du salon", "thermo", "local", .15, "Parle seulement à JARVIS"),
        ("bulb", "Ampoules", "Ampoules du salon", "bulb", "local", .2, "Parlent seulement à JARVIS"),
        ("speaker", "Haut-parleur", "Haut-parleur de la cuisine", "speaker", "net", .35, "Musique en continu · 0,3 Mb/s"),
    ]),
    ("cameras", "Caméras", [
        ("camg", "Garage", "Caméra du garage", "camera", "local", .6, "Port 7 · 6,5 W · enregistre chez JARVIS"),
        ("came", "Entrée", "Caméra de l’entrée", "camera", "local", .6, "Port 6 · 7 W · enregistre chez JARVIS"),
    ]),
    ("invites", "Invités", [
        ("gphone", "Téléphone", "Téléphone d’un invité", "phone", "net", .4, "Internet seulement"),
        ("gtab", "Tablette", "Tablette d’un invité", "tablet", "net", .3, "Internet seulement"),
    ]),
]
ZONE_NAMES = {z: n for z, n, _ in ZONES}

# Infrastructure : (id, nom, sous-titre, icône, info, état, large, haute, étiquette large, étiquette haute)
INFRA = [
    ("internet", "Internet", "", "globe", "Votre fournisseur", "Joignable",
     (52, 270), (200, 34), (0, 46, "middle"), (32, 5, "start")),
    ("fibre", "Fibre", "9 ms", "fibre", "Lien principal · 1 Gb/s", "Active",
     (162, 168), (90, 100), (0, 46, "middle"), (-34, -3, "end")),
    ("starlink", "Starlink", "secours", "dish", "Lien de secours par satellite", "En veille",
     (162, 372), (298, 100), (0, 46, "middle"), (34, -3, "start")),
    ("routeur", "Routeur", "pare-feu", "shield", "Sépare les quatre zones", "Actif",
     (272, 270), (200, 162), (0, 46, "middle"), (34, -3, "start")),
    ("switch", "Commutateur", "", "switch", "8 ports · alimente les caméras par le câble · 49 W sur 60 W", "Actif",
     (380, 270), (200, 228), (0, -38, "middle"), (-34, 4, "end")),
    ("jarvis", "JARVIS", "local", "hub", "Enregistre les caméras · fonctionne sans Internet", "Actif",
     (380, 430), (306, 228), (0, 46, "middle"), (34, -3, "start")),
]
POS = {i[0]: (i[6], i[7]) for i in INFRA}

VB_W, VB_T = (920, 540), (400, 646)
LANE_W = dict(x=468, w=440, y0=22, h=116, gap=12, bus=66, lab=(18, 26), dx=76, step=94)
LANE_T = dict(x=34, w=358, y0=274, h=86, gap=7, bus=46, lab=(16, 20), dx=50, step=86)


def lane_geo(L, i):
    y = L["y0"] + i * (L["h"] + L["gap"])
    return y, y + L["bus"]


def curve_h(a, b):
    """Courbe en S horizontale (disposition large)."""
    (ax, ay), (bx, by) = a, b
    mx = (ax + bx) / 2
    return f"M{ax} {ay}C{mx:.0f} {ay} {mx:.0f} {by} {bx} {by}"


def curve_v(a, b):
    """Courbe en S verticale (disposition haute)."""
    (ax, ay), (bx, by) = a, b
    my = (ay + by) / 2
    return f"M{ax} {ay}C{ax} {my:.0f} {bx} {my:.0f} {bx} {by}"


def fan_w(gy):
    sx, sy = POS["switch"][0]
    gx = LANE_W["x"]
    return f"M{sx} {sy}C{sx + 56} {sy} {gx - 40} {gy} {gx} {gy}"


def fan_t(gy):
    sx, sy = POS["switch"][1]
    tx = 14
    return (f"M{sx} {sy}L{sx} {sy + 22}C{sx} {sy + 40} {tx} {sy + 26} {tx} {sy + 46}"
            f"L{tx} {gy - 10}Q{tx} {gy} {tx + 10} {gy}L{LANE_T['x']} {gy}")


def a(v):
    return escape(str(v), quote=True)


def icon_use(name, size=20):
    h = size / 2
    return f'<use href="#rz-i-{name}" x="-{h}" y="-{h}" width="{size}" height="{size}"/>'


def link(lid, dw, dt, cls="rz-link"):
    return f'<path class="{cls}" data-link="{lid}" d="{dw}" data-gw="{dw}" data-gt="{dt}"/>'


def build_svg():
    defs = "".join(
        f'<symbol id="rz-i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()
    )
    defs += (
        '<pattern id="rz-dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="1.5" cy="1.5" r="1" fill="#ffffff" fill-opacity=".06"/></pattern>'
    )

    links, motion, buses, lanes, gates, devs = [], [], [], [], [], []

    # Liens de l'infrastructure (définis de l'amont vers l'aval)
    for lid, p, q in [("internet>fibre", "internet", "fibre"), ("internet>starlink", "internet", "starlink"),
                      ("fibre>routeur", "fibre", "routeur"), ("starlink>routeur", "starlink", "routeur"),
                      ("routeur>switch", "routeur", "switch"), ("switch>jarvis", "switch", "jarvis")]:
        cls = "rz-link"
        if "starlink" in lid:
            cls += " is-standby"
        if lid in ("routeur>switch", "switch>jarvis"):
            dw = f"M{POS[p][0][0]} {POS[p][0][1]}L{POS[q][0][0]} {POS[q][0][1]}"
            dt = f"M{POS[p][1][0]} {POS[p][1][1]}L{POS[q][1][0]} {POS[q][1][1]}"
        else:
            dw, dt = curve_h(POS[p][0], POS[q][0]), curve_v(POS[p][1], POS[q][1])
        links.append(link(lid, dw, dt, cls))

    # Zones : couloir, porte (mur), appareils posés sur une ligne
    for i, (zid, zname, dl) in enumerate(ZONES):
        yw, bw = lane_geo(LANE_W, i)
        yt, bt = lane_geo(LANE_T, i)
        lw, lt = LANE_W, LANE_T
        rect_w = f"{lw['x']},{yw},{lw['w']},{lw['h']}"
        rect_t = f"{lt['x']},{yt},{lt['w']},{lt['h']}"
        labw = f"{lw['x'] + lw['lab'][0]},{yw + lw['lab'][1]}"
        labt = f"{lt['x'] + lt['lab'][0]},{yt + lt['lab'][1]}"
        lanes.append(
            f'<g class="rz-zone z-{zid}" data-zone="{zid}">'
            f'<rect class="rz-lane" x="{lw["x"]}" y="{yw}" width="{lw["w"]}" height="{lw["h"]}" rx="16" '
            f'data-gw="{rect_w}" data-gt="{rect_t}"/>'
            f'<g class="rz-zl" transform="translate({labw.replace(",", " ")})" data-gw="{labw}" data-gt="{labt}">'
            f'<circle r="4" cy="-4"/><text x="12">{escape(zname.upper())}</text></g>'
            f"</g>"
        )
        links.append(link(f"switch>gate:{zid}", fan_w(bw), fan_t(bt), f"rz-link rz-fan z-{zid}"))
        gw, gt = f"{lw['x']},{bw}", f"{lt['x']},{bt}"
        gates.append(
            f'<g class="rz-gate z-{zid}" data-zone="{zid}" transform="translate({lw["x"]} {bw})" '
            f'data-gw="{gw}" data-gt="{gt}"><circle class="rz-gring" r="15"/>'
            f'<rect class="rz-gbox" x="-11" y="-13" width="22" height="26" rx="7"/>'
            f'<path class="rz-gsh" d="{SHIELD}" transform="scale(.82)"/></g>'
        )
        prev_w, prev_t = lw["x"], lt["x"]
        ids = [d[0] for d in dl]
        for j, (did, lab, name, ic, kind, w, info) in enumerate(dl):
            xw = lw["x"] + lw["dx"] + j * lw["step"]
            xt = lt["x"] + lt["dx"] + j * lt["step"]
            motion.append(link(f"gate:{zid}>{did}", f"M{lw['x']} {bw}L{xw} {bw}",
                               f"M{lt['x']} {bt}L{xt} {bt}", "rz-mp"))
            buses.append(
                f'<path class="rz-bus z-{zid}" data-devs="{" ".join(ids[j:])}" d="M{prev_w} {bw}L{xw} {bw}" '
                f'data-gw="M{prev_w} {bw}L{xw} {bw}" data-gt="M{prev_t} {bt}L{xt} {bt}"/>'
            )
            prev_w, prev_t = xw, xt
            label = f"{name}, zone {ZONE_NAMES[zid]}, en ligne"
            devs.append(
                f'<g class="rz-n rz-dev z-{zid}" data-id="{did}" data-zone="{zid}" data-kind="{kind}" '
                f'data-w8="{w}" data-name="{a(name)}" data-zname="{a(ZONE_NAMES[zid])}" data-info="{a(info)}" '
                f'data-state="En ligne" tabindex="0" role="img" aria-label="{a(label)}" '
                f'transform="translate({xw} {bw})" data-gw="{xw},{bw}" data-gt="{xt},{bt}">'
                f'<circle class="rz-ring" r="27"/><circle class="rz-iso" r="26"/><circle class="rz-disc" r="20"/>'
                f'{icon_use(ic)}<circle class="rz-led" cx="14.5" cy="-14.5" r="4"/>'
                f'<text class="rz-lbl" y="37">{escape(lab)}</text></g>'
            )

    infra = []
    for (iid, name, sub, ic, info, st, pw, pt, lw_, lt_) in INFRA:
        sub_el = f'<text class="rz-sub" y="14">{escape(sub)}</text>' if sub or iid in ("fibre", "starlink") else ""
        label = f"{name}, {info}"
        infra.append(
            f'<g class="rz-n rz-inf" data-id="{iid}" data-name="{a(name)}" data-zname="Infrastructure" '
            f'data-info="{a(info)}" data-state="{a(st)}" tabindex="0" role="img" aria-label="{a(label)}" '
            f'transform="translate({pw[0]} {pw[1]})" data-gw="{pw[0]},{pw[1]}" data-gt="{pt[0]},{pt[1]}">'
            f'<circle class="rz-ring" r="33"/><circle class="rz-disc" r="25"/>{icon_use(ic, 24)}'
            f'<circle class="rz-led" cx="18" cy="-18" r="4.2"/>'
            f'<g class="rz-lg" transform="translate({lw_[0]} {lw_[1]})" style="text-anchor:{lw_[2]}" '
            f'data-gw="{lw_[0]},{lw_[1]},{lw_[2]}" data-gt="{lt_[0]},{lt_[1]},{lt_[2]}">'
            f'<text class="rz-lbl">{escape(name)}</text>{sub_el}</g></g>'
        )

    # Bulle « port 7 » près du commutateur, marque de coupure, étiquette « Bloqué »
    sw, st_ = POS["switch"]
    call = (
        f'<g class="rz-call" transform="translate(300 372)" data-gw="300,372" data-gt="96,{st_[1] - 2}" '
        'data-k2="PORT 7 · RÉTABLI" data-v2="49 W utilisés · 60 W max" aria-hidden="true">'
        '<rect x="-78" y="-25" width="156" height="50" rx="12"/>'
        '<text class="rz-call-k" y="-5">PORT 7 · COUPÉ</text>'
        '<text class="rz-call-v" y="13">63 W demandés · 60 W max</text></g>'
    )
    cut = (
        '<g class="rz-cut" transform="translate(0 0)" aria-hidden="true"><circle r="11"/>'
        '<path d="M-4-4l8 8M4-4l-8 8"/></g>'
    )
    _, bfw = lane_geo(LANE_W, 0)
    _, bft = lane_geo(LANE_T, 0)
    blocked = (
        f'<g class="rz-blocked" transform="translate({LANE_W["x"] - 20} {bfw - 26})" '
        f'data-gw="{LANE_W["x"] - 20},{bfw - 26}" data-gt="{LANE_T["x"] + 24},{bft - 27}" aria-hidden="true">'
        '<rect x="-34" y="-11" width="68" height="22" rx="11"/><text y="4">BLOQUÉ</text></g>'
    )

    return f"""<svg class="rz-svg" viewBox="0 0 {VB_W[0]} {VB_W[1]}" data-vw="0 0 {VB_W[0]} {VB_W[1]}" data-vt="0 0 {VB_T[0]} {VB_T[1]}" role="group" aria-label="Carte du réseau de la maison : Internet, routeur, commutateur et quatre zones d’appareils">
  <defs>{defs}</defs>
  <rect class="rz-bg" width="100%" height="100%" fill="url(#rz-dots)"/>
  <g class="rz-lanes">{"".join(lanes)}</g>
  <g class="rz-links">{"".join(links)}{"".join(buses)}</g>
  <g class="rz-motion" aria-hidden="true">{"".join(motion)}</g>
  <path class="rz-trace" d="M0 0" aria-hidden="true"/>
  <g class="rz-pk" aria-hidden="true"></g>
  <g class="rz-gates">{"".join(gates)}</g>
  <g class="rz-nodes">{"".join(infra)}{"".join(devs)}</g>
  {cut}{blocked}{call}
</svg>"""


# ---------------------------------------------------------------------------
# Panneau de JARVIS : un article par situation
# ---------------------------------------------------------------------------
def steps(items):
    return '<ol class="rz-steps">' + "".join(
        f'<li><i aria-hidden="true"></i><div><b>{t}</b><span>{d}</span></div></li>' for t, d in items
    ) + "</ol>"


def proposal(title, text, flow, later):
    body = f"<p>{text}</p>" if text else ""
    fl = "".join(f'<li data-k="{k}"><i aria-hidden="true"></i><span>{v}</span></li>' for k, v in flow)
    return f"""<div class="rz-prop">
      <p class="rz-ph"><small>Proposition de JARVIS</small><span class="rz-st rz-st-wait">En attente de votre accord</span><span class="rz-st rz-st-ok">Approuvée par vous</span></p>
      <b>{title}</b>{body}
      <div class="rz-acts"><button type="button" data-act="ok">Approuver</button><button type="button" data-act="no">Plus tard</button></div>
      <ol class="rz-flow" aria-live="polite">{fl}</ol>
      <p class="rz-later">{later}</p>
    </div>"""


CARDS = f"""
<article class="rz-scn is-on" data-scn="normal">
  <p class="rz-kick"><i class="rz-pulse is-ok"></i>Surveillance · en continu</p>
  <h3>Tout fonctionne normalement.</h3>
  <p class="rz-lead">Onze appareils, quatre zones séparées, un lien Internet principal et un lien de secours. JARVIS surveille tout et vous parle seulement quand quelque chose mérite votre attention.</p>
  <ul class="rz-legend">
    <li><i class="lg lg-pk" aria-hidden="true"></i>Chaque point lumineux : des données qui circulent.</li>
    <li><i class="lg lg-w" aria-hidden="true"></i>Ligne plus épaisse : plus de trafic.</li>
    <li><i class="lg lg-z" aria-hidden="true"></i>Couleur : la zone de l’appareil.</li>
    <li><i class="lg lg-sh" aria-hidden="true"></i>Bouclier : le mur entre deux zones.</li>
  </ul>
  <p class="rz-note">Survolez ou touchez un appareil pour voir son état, puis choisissez une situation.</p>
</article>

<article class="rz-scn" data-scn="camera" hidden>
  <p class="rz-kick"><i class="rz-pulse is-bad"></i>Diagnostic · 17 h 42</p>
  <h3>La caméra du garage ne répond plus.</h3>
  {steps([
      ("Caméra du garage", "Aucune image depuis 17 h 42."),
      ("Câble et port 7", "Le câble répond, mais le port n’envoie plus d’électricité."),
      ("Commutateur · budget PoE dépassé", "Il alimente les caméras par leur câble. Au crépuscule, leurs lumières infrarouges ont demandé 63 W sur 60 W : il a coupé le port 7 pour se protéger."),
  ])}
  {proposal("Redémarrer le port 7", "La demande est redescendue à 49 W : le port peut repartir sans risque.",
            [("sent", "Envoyé au commutateur"), ("read", "Relecture de l’état du port 7"),
             ("ok", "Confirmé à 17 h 46 : la caméra du garage transmet de nouveau.")],
            "Mis de côté. Rien n’a été changé : JARVIS vous le rappellera ce soir.")}
</article>

<article class="rz-scn" data-scn="iot" hidden>
  <p class="rz-kick"><i class="rz-pulse is-warn"></i>Pare-feu · 17 h 51</p>
  <h3>Un objet connecté tente de joindre vos ordinateurs.</h3>
  <p class="rz-lead rz-reveal">Les ampoules du salon ont essayé de joindre l’ordinateur portable. Le mur entre les zones les a arrêtées : rien n’est passé.</p>
  <dl class="rz-facts rz-reveal">
    <div><dt>Source</dt><dd>Ampoules du salon · Objets connectés</dd></div>
    <div><dt>Cible</dt><dd>Ordinateur portable · Famille</dd></div>
    <div><dt>Résultat</dt><dd class="is-ok">Bloqué · aucune donnée transmise</dd></div>
  </dl>
  {proposal("Isoler les ampoules jusqu’à vérification",
            "Elles répondront encore à JARVIS et à l’interrupteur, mais ne pourront plus rien joindre d’autre.",
            [("sent", "Envoyé au routeur"), ("read", "Relecture des règles du pare-feu"),
             ("ok", "Confirmé à 17 h 52 : les ampoules sont isolées.")],
            "Mis de côté. Le mur continue de bloquer chaque tentative.")}
</article>

<article class="rz-scn" data-scn="internet" hidden>
  <p class="rz-kick"><i class="rz-pulse is-warn"></i>Continuité · 18 h 03</p>
  <h3>Panne Internet : la maison continue.</h3>
  {steps([
      ("Fibre coupée", "Le fournisseur ne répond plus depuis 18 h 03."),
      ("La maison continue en local", "Caméras, lumières et thermostat n’ont pas besoin d’Internet."),
      ("Bascule sur Starlink", "Automatique, en 3 secondes : règle approuvée à l’installation."),
  ])}
  {proposal("Reporter les sauvegardes en ligne jusqu’au retour de la fibre",
            "Starlink est plus lent : on garde la bande passante pour la maison.",
            [("sent", "Envoyé au planificateur"), ("read", "Relecture de l’horaire des sauvegardes"),
             ("ok", "Confirmé : les sauvegardes reprendront avec la fibre.")],
            "Mis de côté. Les sauvegardes passent par Starlink.")}
  <p class="rz-back">Fibre rétablie : retour automatique, 9 ms.</p>
  <button type="button" class="rz-linkbtn" data-act="fibre">Simuler le retour de la fibre</button>
</article>
"""

SCENARIOS = [
    ("normal", "Tout va bien", "Tout va bien", "Le réseau au quotidien"),
    ("camera", "Caméra du garage hors ligne", "Caméra hors ligne", "Trouver la vraie cause"),
    ("iot", "Un objet connecté tente de joindre vos ordinateurs", "Objet suspect", "Le mur entre les zones"),
    ("internet", "Panne Internet", "Panne Internet", "Bascule sur Starlink"),
]

def nb(html):
    """Espaces insécables : « 17 h 42 », « 63 W », « 9 ms », avant « : »."""
    html = re.sub(r"(\d) h (\d)", "\\1\u00a0h\u00a0\\2", html)
    html = re.sub(r"(\d) (W|ms|secondes|Mb/s)\b", "\\1\u00a0\\2", html)
    return html.replace(" :", "\u00a0:")


BAR = "".join(
    f'<button type="button" data-scn="{k}" aria-pressed="{"true" if k == "normal" else "false"}">'
    f'<i class="rz-bi rz-bi-{k}" aria-hidden="true"></i><span><b class="rz-l">{l}</b><b class="rz-s">{s}</b>'
    f"<small>{sub}</small></span></button>"
    for k, l, s, sub in SCENARIOS
)

HTML = f"""<div class="demo-shell" data-demo="reseau" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Réseau de la maison</b><span class="tag tag-sim">Démo · données simulées</span></div>
  <div class="demo-body">
    <div class="rz-bar" role="group" aria-label="Choisir une situation">{BAR}</div>
    <div class="rz-grid">
      <div class="rz-map">
        <dl class="rz-hud">
          <div data-hud="net"><dt>Internet</dt><dd><i class="rz-hled"></i><span>Fibre · 9 ms</span></dd></div>
          <div data-hud="dev"><dt>Appareils</dt><dd><span>11 / 11</span> en ligne</dd></div>
          <div data-hud="zones"><dt>Zones</dt><dd>4 séparées</dd></div>
          <div data-hud="alert"><dt>Alertes</dt><dd><span>0</span></dd></div>
        </dl>
        <div class="rz-wrap">
          {build_svg()}
          <button type="button" class="rz-jump" data-act="jump" hidden>Proposition de JARVIS ↓</button>
          <div class="rz-tip" aria-hidden="true" hidden><b></b><span class="rz-tz"></span><span class="rz-ts"></span><span class="rz-ti"></span></div>
        </div>
      </div>
      <div class="rz-card">
        <div class="rz-card-in">
          <div class="rz-card-top"><span>JARVIS</span><button type="button" class="rz-replay" data-act="replay" hidden>↻ Rejouer</button></div>
          <div class="rz-scns" aria-live="polite">{nb(CARDS)}</div>
        </div>
      </div>
    </div>
  </div>
</div>
<p class="demo-hint">Choisissez une situation · survolez un appareil · rien n’est appliqué sans « Approuver »</p>"""
