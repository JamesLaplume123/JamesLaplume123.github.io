# Démo « Réseau et cybersécurité » (solution 05) : la console réseau de JARVIS.
# Douze modules autour d'une carte vivante : topologie, appareils, Wi-Fi, trafic,
# menaces, VPN, contrôles, continuité, sauvegardes, mises à jour, segmentation
# et score de la semaine. Tout est simulé (« Données d'exemple »).
#
# Ce module produit tout le HTML (la carte en SVG comprise). Sans JavaScript,
# seule la topologie s'affiche, dans son état normal et lisible. Le script
# assets/demos/reseau.js rend la console vivante : lumière qui circule sur les
# liens, chiffres en direct, situations jouées avec accord avant d'agir, carte
# des menaces, carte de chaleur Wi-Fi et graphiques.
# La carte du monde en points vient de reseau_geo.py (fichier généré).

import json
import re
from html import escape
from math import hypot

from demos import reseau_geo as GEO

NB = "\u00a0"


def a(v):
    return escape(str(v), quote=True)


def _nb_text(t):
    t = re.sub(r"(\d) h (\d)", "\\1\u00a0h\u00a0\\2", t)
    t = re.sub(r"(\d) (W|ms|s|min|h|j|Mb/s|Gb/s|Go|Mo|To|%|dBm|ports|appareils|essais|clients|kW)(?![\w])", "\\1\u00a0\\2", t)
    t = re.sub(r"(\d) (\d{3})\b", "\\1\u00a0\\2", t)
    return t.replace(" :", "\u00a0:").replace(" ?", "\u00a0?")


def nb(html):
    """Espaces insécables (« 17 h 42 », « 63 W », « 1 284 », avant « : ») dans le texte seulement,
    jamais dans les balises (chemins SVG, attributs)."""
    return re.sub(r">([^<]+)<", lambda m: ">" + _nb_text(m.group(1)) + "<", html)


# ---------------------------------------------------------------------------
# Icônes (trait, 16 × 16)
# ---------------------------------------------------------------------------
IC = {
    "topo": '<rect x="6" y="1.8" width="4" height="3.4" rx=".8"/><rect x="1.5" y="10.8" width="4" height="3.4" rx=".8"/><rect x="10.5" y="10.8" width="4" height="3.4" rx=".8"/><path d="M8 5.2v2.6M3.5 10.8V8.6c0-.5.3-.8.8-.8h7.4c.5 0 .8.3.8.8v2.2"/>',
    "devices": '<rect x="1.8" y="3" width="9.4" height="7" rx="1"/><path d="M.8 12.6h11.4"/><rect x="11.4" y="5.6" width="3.8" height="7.6" rx=".9"/>',
    "wifi": '<path d="M1.6 6.2a9.2 9.2 0 0 1 12.8 0M3.8 8.6a6 6 0 0 1 8.4 0M6 11a2.8 2.8 0 0 1 4 0"/><circle cx="8" cy="13.2" r=".6" fill="currentColor"/>',
    "trafic": '<path d="M1.5 9.5h2.6l1.8-5 2.6 9 2-6.2 1.2 2.2h2.8"/>',
    "menaces": '<circle cx="8" cy="8" r="6.3"/><circle cx="8" cy="8" r="3.2"/><path d="M8 8l4.4-4.4"/><circle cx="8" cy="8" r=".7" fill="currentColor"/>',
    "vpn": '<rect x="3" y="7" width="10" height="7" rx="1.6"/><path d="M5.2 7V5.2a2.8 2.8 0 0 1 5.6 0V7"/><path d="M8 9.6v1.8"/>',
    "controles": '<path d="M2 4.5h7M12 4.5h2M2 11.5h2M7 11.5h7"/><circle cx="10.5" cy="4.5" r="1.5"/><circle cx="5.5" cy="11.5" r="1.5"/>',
    "continuite": '<path d="M1.8 5.5h9.6l-2.4-2.4M14.2 10.5H4.6L7 12.9"/>',
    "sauvegardes": '<ellipse cx="8" cy="3.8" rx="5.6" ry="2"/><path d="M2.4 3.8v8.4c0 1.1 2.5 2 5.6 2s5.6-.9 5.6-2V3.8M2.4 8c0 1.1 2.5 2 5.6 2s5.6-.9 5.6-2"/>',
    "maj": '<path d="M13.4 6.4A5.6 5.6 0 0 0 3 4.6M2.6 9.6A5.6 5.6 0 0 0 13 11.4"/><path d="M3 1.8v2.8h2.8M13 14.2v-2.8h-2.8"/>',
    "segmentation": '<rect x="1.8" y="1.8" width="5" height="5" rx="1"/><rect x="9.2" y="1.8" width="5" height="5" rx="1"/><rect x="1.8" y="9.2" width="5" height="5" rx="1"/><rect x="9.2" y="9.2" width="5" height="5" rx="1" stroke-dasharray="1.6 1.3"/>',
    "score": '<path d="M2.2 11.6a6 6 0 1 1 11.6 0"/><path d="M8 10.2l2.8-3.6"/><circle cx="8" cy="10.6" r=".9" fill="currentColor"/>',
    # appareils
    "phone": '<rect x="4.6" y="1.5" width="6.8" height="13" rx="1.6"/><path d="M7.2 12.4h1.6"/>',
    "laptop": '<rect x="2.6" y="3.2" width="10.8" height="7.4" rx="1"/><path d="M1 12.8h14"/>',
    "tablet": '<rect x="3" y="1.6" width="10" height="12.8" rx="1.5"/><path d="M7.2 12.2h1.6"/>',
    "tv": '<rect x="1.4" y="2.6" width="13.2" height="8.6" rx="1.2"/><path d="M5.6 13.8h4.8"/>',
    "console": '<path d="M4.6 5.2h6.8a3 3 0 0 1 3 3v.6a2.2 2.2 0 0 1-4 1.2l-.6-.8H6.2l-.6.8a2.2 2.2 0 0 1-4-1.2v-.6a3 3 0 0 1 3-3z"/><path d="M4.8 7v2M3.8 8h2"/>',
    "camera": '<rect x="1.4" y="4.4" width="9" height="7.2" rx="1.4"/><path d="M10.4 7l4.2-2.2v6.4L10.4 9z"/>',
    "thermo": '<circle cx="8" cy="8" r="6.2"/><path d="M5 10.4a3.8 3.8 0 0 1 6 0M8 8.4l2-2.2"/>',
    "bulb": '<path d="M6.2 12h3.6M6.8 14h2.4"/><path d="M8 2a4 4 0 0 0-2.4 7.2c.5.4.7 1 .7 1.6h3.4c0-.6.2-1.2.7-1.6A4 4 0 0 0 8 2z"/>',
    "speaker": '<rect x="4" y="1.6" width="8" height="12.8" rx="1.8"/><circle cx="8" cy="9.4" r="2.2"/><circle cx="8" cy="4.6" r=".5" fill="currentColor"/>',
    "plug": '<path d="M5.6 1.8v3M10.4 1.8v3M3.6 4.8h8.8v2.6a4.4 4.4 0 0 1-8.8 0z"/><path d="M8 11.8v2.4"/>',
    "server": '<rect x="2" y="2" width="12" height="5" rx="1"/><rect x="2" y="9" width="12" height="5" rx="1"/><path d="M4.6 4.5h.01M4.6 11.5h.01" stroke-width="2"/>',
    "printer": '<path d="M4.4 6V2h7.2v4"/><rect x="1.6" y="6" width="12.8" height="5.4" rx="1"/><path d="M4.4 9.6h7.2V14H4.4z"/>',
    "charger": '<rect x="3.4" y="1.8" width="7" height="12.4" rx="1.4"/><path d="M7.4 4.6l-1.6 3h2.4L6.6 11"/><path d="M10.4 6h1.4a1 1 0 0 1 1 1v4.4a1 1 0 0 0 2 0V5"/>',
    "unknown": '<circle cx="8" cy="8" r="6.2"/><path d="M6.2 6.2a1.9 1.9 0 1 1 2.6 1.8c-.5.2-.8.6-.8 1.1v.6"/><circle cx="8" cy="11.6" r=".5" fill="currentColor"/>',
    "ap": '<circle cx="8" cy="9" r="5.4"/><circle cx="8" cy="9" r="1.2"/><path d="M4.4 3.4a6.6 6.6 0 0 1 7.2 0"/>',
    "check": '<path d="M3.4 8.4l2.9 2.9 6.3-6.6"/>',
    "x": '<path d="M4.4 4.4l7.2 7.2M11.6 4.4l-7.2 7.2"/>',
    "arrow": '<path d="M3 8h10M9.4 4.4 13 8l-3.6 3.6"/>',
    "link": '<path d="M6.6 9.4l2.8-2.8M5.2 7.4 3.8 8.8a2.4 2.4 0 0 0 3.4 3.4l1.4-1.4M10.8 8.6l1.4-1.4a2.4 2.4 0 0 0-3.4-3.4L7.4 5.2"/>',
}


def ic(name, cls="rs-ic"):
    return f'<svg class="{cls}" viewBox="0 0 16 16" aria-hidden="true">{IC[name]}</svg>'


# ---------------------------------------------------------------------------
# Zones (VLAN) : identifiant, numéro, nom, appareils, débit de base (Mb/s)
# ---------------------------------------------------------------------------
VLANS = [
    ("perso", 10, "Personnel", 14, 186.0, "Ordinateurs, téléphones et tablettes de la famille"),
    ("invites", 20, "Invités", 3, 22.0, "Internet seulement, appareils isolés entre eux"),
    ("objets", 30, "Objets connectés", 18, 31.0, "Ne parlent qu’à JARVIS, jamais à vos ordinateurs"),
    ("cameras", 40, "Caméras", 6, 24.6, "Enregistrent chez JARVIS, aucun accès à Internet"),
    ("serveurs", 50, "Serveurs", 3, 48.0, "JARVIS et le stockage, joignables sur demande seulement"),
]
VL = {v[0]: v for v in VLANS}

# ---------------------------------------------------------------------------
# Topologie : géométrie de la carte (unités du viewBox)
# ---------------------------------------------------------------------------
TW, TH = 1080, 520
# id: (x centre, y centre, largeur, hauteur)
NODES = {
    "fibre": (82, 142, 140, 76),
    "g5": (82, 262, 140, 76),
    "star": (82, 382, 140, 76),
    "gw": (282, 262, 168, 118),
    "core": (494, 262, 176, 118),
    "ap1": (700, 62, 156, 76),
    "ap2": (700, 158, 156, 76),
    "ap3": (700, 254, 156, 76),
    "poe": (700, 350, 156, 76),
    "nas": (700, 446, 156, 76),
}
TRUNK_X = 822
BAND_X, BAND_W, BAND_H = 852, 214, 76
BAND_Y = [62, 158, 254, 350, 446]


def _edge(nid, side):
    x, y, w, h = NODES[nid]
    return (x + w / 2, y) if side == "r" else (x - w / 2, y)


def _ortho(p, q, mx, r=12):
    """Lien orthogonal à coins arrondis : p → (mx, p.y) → (mx, q.y) → q."""
    (px, py), (qx, qy) = p, q
    if abs(qy - py) < 1:
        return f"M{px:g} {py:g}H{qx:g}", abs(qx - px)
    s = 1 if qy > py else -1
    rr = min(r, abs(qy - py) / 2)
    d = (f"M{px:g} {py:g}H{mx - rr:g}Q{mx:g} {py:g} {mx:g} {py + s * rr:g}"
         f"V{qy - s * rr:g}Q{mx:g} {qy:g} {mx + rr:g} {qy:g}H{qx:g}")
    ln = abs(mx - px) + abs(qy - py) + abs(qx - mx)
    return d, ln


# Liens : id, de, vers, coude x, classe, flux (débit relatif 0..1)
def _links():
    L = []
    for nid, cls, w in (("fibre", "is-wan is-main", 1.0), ("g5", "is-wan is-standby", 0), ("star", "is-wan is-standby", 0)):
        d, ln = _ortho(_edge(nid, "r"), _edge("gw", "l"), 172)
        L.append((f"{nid}-gw", d, ln, cls, w))
    d, ln = _ortho(_edge("gw", "r"), _edge("core", "l"), 0)
    L.append(("gw-core", d, ln, "is-10g", 1.0))
    for nid, w in (("ap1", .8), ("ap2", .6), ("ap3", .35), ("poe", .5), ("nas", .55)):
        d, ln = _ortho(_edge("core", "r"), _edge(nid, "l"), 600)
        L.append((f"core-{nid}", d, ln, "", w))
    for nid, w in (("ap1", .7), ("ap2", .5), ("ap3", .3), ("poe", .45), ("nas", .5)):
        x, y, wd, h = NODES[nid]
        d, ln = _ortho((x + wd / 2, y), (TRUNK_X, y), TRUNK_X)
        L.append((f"{nid}-trunk", d, ln, "is-short", w))
    for i, (vid, *_r) in enumerate(VLANS):
        y = BAND_Y[i]
        L.append((f"trunk-{vid}", f"M{TRUNK_X} {y}H{BAND_X}", BAND_X - TRUNK_X, f"is-vlan z-{vid}", .6))
    return L


def _flow(lid, d, ln, w, rev=False, cls=""):
    """Trois traits superposés, même période : la lumière et sa traînée (comète)."""
    period = 260 + (1 - w) * 260
    dur = max(1.1, (ln + period) / (150 + 120 * w))
    head, mid, tail = 4, 16, 46
    o = []
    for k, L in (("t", tail), ("m", mid), ("h", head)):
        lo = 0 if rev else tail - L  # la tête est toujours à l'avant du mouvement
        o.append(
            f'<path class="rs-fl rs-fl-{k}{cls}" d="{d}" style="--p:{period:.0f};--l:{L};--lo:{lo};'
            f'--dur:{dur:.2f}s;--del:-{(sum(map(ord, lid)) * 37 % 97) / 97 * dur:.2f}s"/>'
        )
    return f'<g class="rs-flow{" is-up" if rev else ""}" data-flow="{lid}">{"".join(o)}</g>'


def _ports(n_on):
    """Rangée de ports du commutateur cœur : 2 × 12 voyants."""
    out = []
    for i in range(24):
        r, c = divmod(i, 12)
        x = -72 + c * 12.2
        y = 30 + r * 8
        st = "is-poe" if i in (2, 3, 6, 7, 10, 11) else ("is-on" if i < n_on or i in (22, 23) else "")
        if i in (22, 23):
            st += " is-sfp"
        out.append(f'<rect class="rs-port {st}" x="{x:.1f}" y="{y}" width="9" height="5.2" rx="1.2" style="--d:{(i * 37) % 23 / 10:.1f}s"/>')
    return "".join(out)


def _node(nid, kick, title, meta, live=None, extra="", cls=""):
    x, y, w, h = NODES[nid]
    lv = f'<text class="rs-n-live" x="{-w / 2 + 14:g}" y="{-h / 2 + 64:g}" data-live="{live[0]}">{live[1]}</text>' if live else ""
    return (
        f'<g class="rs-node {cls}" data-node="{nid}" transform="translate({x} {y})" tabindex="0" role="img" '
        f'aria-label="{a(kick + " · " + title + " · " + meta)}">'
        f'<rect class="rs-n-glow" x="{-w / 2 - 6:g}" y="{-h / 2 - 6:g}" width="{w + 12}" height="{h + 12}" rx="16"/>'
        f'<rect class="rs-n-box" x="{-w / 2:g}" y="{-h / 2:g}" width="{w}" height="{h}" rx="11"/>'
        f'<path class="rs-n-spec" d="M{-w / 2 + 11:g} {-h / 2 + .6:g}H{w / 2 - 11:g}"/>'
        f'<circle class="rs-n-dot" cx="{w / 2 - 13:g}" cy="{-h / 2 + 13:g}" r="3.4"/>'
        f'<text class="rs-n-k" x="{-w / 2 + 14:g}" y="{-h / 2 + 17:g}">{escape(kick)}</text>'
        f'<text class="rs-n-t" x="{-w / 2 + 14:g}" y="{-h / 2 + 34:g}">{escape(title)}</text>'
        f'<text class="rs-n-m" x="{-w / 2 + 14:g}" y="{-h / 2 + 49:g}" data-meta="{nid}">{escape(meta)}</text>'
        f"{lv}{extra}</g>"
    )


def topology_svg():
    links = _links()
    base, flows = [], []
    for lid, d, ln, cls, w in links:
        base.append(f'<path class="rs-link {cls}" data-link="{lid}" d="{d}"/>')
        if w > 0 or "is-standby" in cls:
            zc = ""
            m = re.search(r"z-(\w+)", cls)
            if m:
                zc = f" z-{m.group(1)}"
            flows.append(_flow(lid, d, ln, max(w, .5), cls=zc))
            if w >= .5 and "is-vlan" not in cls:
                flows.append(_flow(lid + "^", d, ln, w * .5, rev=True))
    # Tronc 802.1Q
    trunk = (
        f'<path class="rs-trunk" d="M{TRUNK_X} {BAND_Y[0] - 22}V{BAND_Y[-1] + 22}"/>'
        f'<text class="rs-trunk-l" transform="translate({TRUNK_X - 7} {BAND_Y[-1] + 18}) rotate(-90)">TRONC 802.1Q · 5 VLAN</text>'
    )
    bands = []
    for i, (vid, num, name, n, mbps, _desc) in enumerate(VLANS):
        y = BAND_Y[i]
        dots = "".join(
            f'<circle class="rs-b-dev" cx="{BAND_X + 16 + (k % 18) * 10.6:g}" cy="{y + 25}" r="2.6"/>'
            for k in range(min(n, 18))
        )
        bands.append(
            f'<g class="rs-band z-{vid}" data-band="{vid}" tabindex="0" role="img" '
            f'aria-label="{a(f"VLAN {num} · {name} · {n} appareils")}">'
            f'<rect class="rs-b-box" x="{BAND_X}" y="{y - BAND_H / 2:g}" width="{BAND_W}" height="{BAND_H}" rx="12"/>'
            f'<rect class="rs-b-bar" x="{BAND_X}" y="{y - BAND_H / 2 + 14:g}" width="2.4" height="{BAND_H - 28}" rx="1.2"/>'
            f'<text class="rs-n-k" x="{BAND_X + 14}" y="{y - 19}">VLAN {num}</text>'
            f'<text class="rs-b-n" x="{BAND_X + BAND_W - 14}" y="{y - 19}" data-live="vl-{vid}">{mbps:.0f} Mb/s</text>'
            f'<text class="rs-n-t" x="{BAND_X + 14}" y="{y - 2}">{escape(name)}</text>'
            f'<text class="rs-b-c" x="{BAND_X + BAND_W - 14}" y="{y - 2}" data-count="{vid}">{n} appareils</text>'
            f"{dots}</g>"
        )
    nodes = [
        _node("fibre", "PRINCIPAL", "Fibre 1 Gb/s", "Symétrique · 9 ms", ("wan-fibre", "↓ 312 · ↑ 41 Mb/s"), cls="is-wan"),
        _node("g5", "SECOURS 1", "Routeur 5G", "En veille · 31 ms", ("wan-g5", "−84 dBm · 4 barres"), cls="is-wan is-standby"),
        _node("star", "SECOURS 2", "Satellite", "En veille · 38 ms", ("wan-star", "Ciel dégagé · 98 %"), cls="is-wan is-standby"),
        _node("gw", "PASSERELLE", "Pare-feu", "Détection d’intrusion active",
              ("gw", "CPU 18 % · 1 284 blocages"),
              extra=(f'<g class="rs-gw-sh" transform="translate(52 22)"><circle r="17"/>'
                     f'<path d="M0-9.5l7 2.8v4.9c0 4.1-2.9 7.3-7 9.1-4.1-1.8-7-5-7-9.1v-4.9z"/>'
                     f'<path d="M-3.2.2l2.2 2.2 4.2-4.4"/></g>')),
        _node("core", "COMMUTATEUR CŒUR", "24 ports · 10 Gb/s", "19 ports actifs · 2 liens 10 G",
              None, extra=_ports(13)),
        _node("ap1", "WI-FI 7 · SALON", "Point d’accès", "17 clients · canal 149", ("ap1", "−48 dBm moy.")),
        _node("ap2", "WI-FI 7 · ÉTAGE", "Point d’accès", "11 clients · canal 36", ("ap2", "−53 dBm moy.")),
        _node("ap3", "WI-FI 6 · EXTÉRIEUR", "Point d’accès", "6 clients · canal 6", ("ap3", "−61 dBm moy.")),
        _node("poe", "COMMUTATEUR PoE", "Caméras · 8 ports", "6 caméras alimentées", ("poe", "112 W / 180 W"),
              extra='<rect class="rs-poe-bar" x="36" y="22" width="30" height="3" rx="1.5"/>'
                    '<rect class="rs-poe-fill" x="36" y="22" width="19" height="3" rx="1.5"/>'),
        _node("nas", "SERVEURS", "JARVIS et stockage", "Local · 10 Gb/s", ("nas", "Disques 41 % · 38 °C")),
    ]
    marks = (
        # Coupure (panne fibre), blocage (objet suspect), port coupé (caméra)
        f'<g class="rs-mk rs-mk-cut" transform="translate(172 {NODES["fibre"][1]})"><circle r="12"/><path d="M-4.2-4.2l8.4 8.4M4.2-4.2l-8.4 8.4"/></g>'
        f'<g class="rs-mk rs-mk-block" transform="translate({TRUNK_X} {BAND_Y[2]})"><circle r="13"/>'
        f'<path d="M0-8l6 2.4v4.2c0 3.5-2.5 6.2-6 7.8-3.5-1.6-6-4.3-6-7.8v-4.2z"/></g>'
        f'<g class="rs-mk rs-mk-tag" transform="translate({TRUNK_X - 64} {BAND_Y[2] + 30})"><rect x="-44" y="-11" width="88" height="22" rx="11"/>'
        f'<text y="4">BLOQUÉ · 0 octet</text></g>'
        f'<path class="rs-intr" d="M{BAND_X} {BAND_Y[2]}H{TRUNK_X}V{BAND_Y[0] + 8}"/>'
    )
    return f"""<svg class="rs-topo" viewBox="0 0 {TW} {TH}" role="group" aria-label="Topologie du réseau : trois liens Internet, la passerelle pare-feu, le commutateur cœur, trois points d’accès Wi-Fi, le commutateur des caméras, les serveurs et cinq réseaux séparés (VLAN)">
  <defs>
    <pattern id="rs-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#fff" stroke-opacity=".035" stroke-width=".6"/></pattern>
    <radialGradient id="rs-vig" cx="45%" cy="50%" r="70%"><stop offset="0" stop-color="#fff" stop-opacity=".045"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <linearGradient id="rs-box" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1c1f"/><stop offset="1" stop-color="#09090a"/></linearGradient>
    <filter id="rs-soft" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity=".7"/></filter>
    <filter id="rs-bloom" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="{TW}" height="{TH}" fill="url(#rs-grid)"/>
  <rect width="{TW}" height="{TH}" fill="url(#rs-vig)"/>
  <text class="rs-col" x="82" y="22">INTERNET</text><text class="rs-col" x="282" y="22">SÉCURITÉ</text>
  <text class="rs-col" x="494" y="22">CŒUR</text><text class="rs-col" x="959" y="14">RÉSEAUX SÉPARÉS</text>
  <g class="rs-links">{"".join(base)}{trunk}</g>
  <g class="rs-flows" filter="url(#rs-bloom)">{"".join(flows)}</g>
  <g class="rs-bands">{"".join(bands)}</g>
  <g class="rs-nodes">{"".join(nodes)}</g>
  {marks}
</svg>"""


# ---------------------------------------------------------------------------
# Situations de la topologie (l'idée d'origine : diagnostiquer, expliquer,
# proposer une seule action, attendre l'accord)
# ---------------------------------------------------------------------------
def steps(items):
    return '<ol class="rs-steps">' + "".join(
        f'<li><i aria-hidden="true"></i><div><b>{t}</b><span>{d}</span></div></li>' for t, d in items
    ) + "</ol>"


def proposal(title, text, flow, later, ok="Approuver"):
    fl = "".join(f'<li><i aria-hidden="true"></i><span>{v}</span></li>' for v in flow)
    return f"""<div class="rs-prop">
      <p class="rs-ph"><small>Proposition de JARVIS</small><span class="rs-st rs-st-wait">En attente de votre accord</span><span class="rs-st rs-st-ok">Approuvée par vous</span><span class="rs-st rs-st-no">Mise de côté</span></p>
      <b>{title}</b>{f"<p>{text}</p>" if text else ""}
      <div class="rs-acts"><button type="button" class="rs-btn rs-btn-pri" data-act="ok">{ok}</button><button type="button" class="rs-btn" data-act="no">Plus tard</button></div>
      <ol class="rs-flowl" aria-live="polite">{fl}</ol>
      <p class="rs-later">{later}</p>
    </div>"""


SITUATIONS = [
    ("normal", "Tout va bien", "Le réseau au quotidien"),
    ("camera", "Caméra hors ligne", "Trouver la vraie cause"),
    ("iot", "Objet suspect", "Le mur entre les zones"),
    ("panne", "Panne de la fibre", "Bascule automatique"),
]

SCN = f"""
<article class="rs-scn is-on" data-scn="normal">
  <p class="rs-kick"><i class="rs-dot is-ok"></i>Surveillance continue</p>
  <h4>Tout fonctionne normalement.</h4>
  <p class="rs-lead">44 appareils répartis dans 5 réseaux séparés, 7 équipements réseau, un lien Internet principal et deux liens de secours. Chaque trait de lumière, ce sont des données qui circulent en ce moment.</p>
  <ul class="rs-legend">
    <li><i class="lg lg-d"></i>Lumière vive : vers vos appareils</li>
    <li><i class="lg lg-u"></i>Lumière pâle : vers Internet</li>
    <li><i class="lg lg-s"></i>Pointillé : lien de secours en veille</li>
  </ul>
</article>
<article class="rs-scn" data-scn="camera" hidden>
  <p class="rs-kick"><i class="rs-dot is-bad"></i>Diagnostic · 17 h 42</p>
  <h4>La caméra du garage ne répond plus.</h4>
  {steps([
      ("Caméra du garage", "Aucune image depuis 17 h 42 · VLAN 40."),
      ("Câble et port 7", "Le câble répond, mais le port n’envoie plus d’électricité."),
      ("Commutateur PoE · budget dépassé", "Au crépuscule, l’infrarouge des 6 caméras a demandé 186 W sur 180 W : le commutateur a coupé le port 7 pour se protéger."),
  ])}
  {proposal("Relancer le port 7 et réserver 12 W par caméra",
            "La demande est redescendue à 112 W. La réserve évite que ça se reproduise la nuit prochaine.",
            ["Envoyé au commutateur PoE", "Relecture de l’état du port 7", "Confirmé à 17 h 46 : la caméra du garage transmet de nouveau."],
            "Mis de côté. Rien n’a été changé : JARVIS vous le rappellera ce soir.")}
</article>
<article class="rs-scn" data-scn="iot" hidden>
  <p class="rs-kick"><i class="rs-dot is-warn"></i>Pare-feu · 17 h 51</p>
  <h4>Un objet connecté tente de joindre vos ordinateurs.</h4>
  <dl class="rs-facts">
    <div><dt>Source</dt><dd>Prise connectée · VLAN 30</dd></div>
    <div><dt>Cible</dt><dd>Ordinateur portable · VLAN 10 · port 445</dd></div>
    <div><dt>Résultat</dt><dd class="is-ok">Bloqué par la règle 30 → 10 · 0 octet transmis</dd></div>
  </dl>
  {proposal("Mettre la prise en quarantaine jusqu’à vérification",
            "Elle répondra encore à JARVIS, mais ne pourra plus rien joindre d’autre.",
            ["Envoyé à la passerelle", "Relecture des règles du pare-feu", "Confirmé à 17 h 52 : la prise est en quarantaine (VLAN 99)."],
            "Mis de côté. Le mur entre les zones continue de bloquer chaque tentative.")}
</article>
<article class="rs-scn" data-scn="panne" hidden>
  <p class="rs-kick"><i class="rs-dot is-warn"></i>Continuité · 18 h 03</p>
  <h4>Fibre coupée : la maison continue.</h4>
  {steps([
      ("18:03:00 · Fibre muette", "Aucune réponse du fournisseur, 3 sondes sur 3."),
      ("18:03:02 · Bascule sur la 5G", "Automatique, règle approuvée à l’installation. Appels et VPN reconnectés."),
      ("En local, rien ne s’arrête", "Caméras, lumières, thermostat et JARVIS n’ont pas besoin d’Internet."),
  ])}
  {proposal("Reporter les sauvegardes hors site jusqu’au retour de la fibre",
            "La 5G est facturée au volume : on la garde pour la maison.",
            ["Envoyé au planificateur", "Relecture de l’horaire", "Confirmé : les sauvegardes reprendront avec la fibre."],
            "Mis de côté. Les sauvegardes passent par la 5G.")}
</article>
"""

# ---------------------------------------------------------------------------
# Modules
# ---------------------------------------------------------------------------
MODULES = [
    ("topo", "Topologie", "En direct"),
    ("appareils", "Appareils", "44 · 1 nouveau"),
    ("wifi", "Wi-Fi", "1 pièce faible"),
    ("trafic", "Trafic", "312 Mb/s"),
    ("menaces", "Menaces", "1 284 bloquées"),
    ("vpn", "VPN", "3 sessions"),
    ("controles", "Contrôles", "Enfants · 21 h"),
    ("continuite", "Continuité", "Fibre · 9 ms"),
    ("sauvegardes", "Sauvegardes", "Il y a 2 h"),
    ("maj", "Mises à jour", "1 critique"),
    ("segmentation", "Segmentation", "18 règles"),
    ("score", "Score", "86 / 100"),
]
MOD_IC = {"topo": "topo", "appareils": "devices", "wifi": "wifi", "trafic": "trafic", "menaces": "menaces",
          "vpn": "vpn", "controles": "controles", "continuite": "continuite", "sauvegardes": "sauvegardes",
          "maj": "maj", "segmentation": "segmentation", "score": "score"}
WARN = {"appareils", "wifi", "maj"}


def head(title, lead, kpis):
    k = "".join(
        f'<div class="rs-kpi{" " + c if c else ""}"><dt>{t}</dt><dd{f" data-live={chr(34)}{d}{chr(34)}" if d else ""}>{v}</dd></div>'
        for t, v, c, d in kpis
    )
    return (f'<header class="rs-mh"><div><h4>{title}</h4><p>{lead} <span class="rs-ex">Données d’exemple</span></p></div>'
            f'<dl class="rs-kpis">{k}</dl></header>')


def card(title, body, cls="", aside=""):
    t = f'<div class="rs-ch"><h5>{title}</h5>{aside}</div>' if title else ""
    return f'<section class="rs-card {cls}">{t}{body}</section>'


def pill(text, tone=""):
    return f'<span class="rs-pill{" is-" + tone if tone else ""}">{text}</span>'


# ---------- Topologie ----------
def mod_topo():
    bar = "".join(
        f'<button type="button" data-scn="{k}" aria-pressed="{"true" if k == "normal" else "false"}">'
        f'<i class="rs-sdot rs-sdot-{k}" aria-hidden="true"></i><span><b>{t}</b><small>{s}</small></span></button>'
        for k, t, s in SITUATIONS
    )
    return (
        head("Topologie", "Tout le réseau sur une seule carte, du lien Internet jusqu’au dernier appareil.",
             [("Internet", '<i class="rs-dot is-ok"></i><span data-live="wan">Fibre · 9 ms</span>', "", ""),
              ("Débit", '<span data-live="down">312</span><small> ↓ Mb/s</small>', "", ""),
              ("Équipements", "7 / 7", "", ""),
              ("Alertes", '<span data-live="alerts">0</span>', "", "")])
        + f'<div class="rs-topo-wrap"><div class="rs-topo-scroll">{topology_svg()}</div>'
          f'<p class="rs-swipe" aria-hidden="true">Glissez pour voir tout le réseau</p></div>'
        + f'<div class="rs-sit"><div class="rs-sbar" role="group" aria-label="Choisir une situation">{bar}</div>'
          f'<div class="rs-scns" aria-live="polite">{SCN}</div></div>'
    )


# ---------- Appareils ----------
# icône, nom, identification, confiance, vlan, ip, connexion, débit (Mb/s), état
DEVICES = [
    ("laptop", "Ordinateur portable · bureau", "Portable · système de bureau", 99, "perso", "10.0.10.21", "Wi-Fi 7 · Étage · −49 dBm", 48.0, "on"),
    ("phone", "Téléphone principal", "Téléphone intelligent", 98, "perso", "10.0.10.34", "Wi-Fi 7 · Salon · −52 dBm", 6.2, "on"),
    ("phone", "Téléphone · adolescent", "Téléphone intelligent · profil Adolescent", 97, "perso", "10.0.10.37", "Wi-Fi 7 · Étage · −55 dBm", 14.8, "on"),
    ("tablet", "Tablette · enfants", "Tablette · profil Enfants", 96, "perso", "10.0.10.41", "Wi-Fi 6 · Salon · −57 dBm", 9.1, "on"),
    ("console", "Console de jeu", "Console · téléchargement en cours", 99, "perso", "10.0.10.52", "Câble · port 9 · 1 Gb/s", 86.0, "on"),
    ("tv", "Téléviseur du salon", "Téléviseur intelligent · film en 4K", 99, "objets", "10.0.30.12", "Câble · port 14", 25.0, "on"),
    ("speaker", "Haut-parleur · cuisine", "Haut-parleur · musique en continu", 95, "objets", "10.0.30.44", "Wi-Fi 5 GHz · Salon", .3, "on"),
    ("thermo", "Thermostat du salon", "Thermostat · parle seulement à JARVIS", 97, "objets", "10.0.30.21", "Wi-Fi 2,4 GHz · Salon", .01, "on"),
    ("bulb", "Pont d’éclairage", "Pont d’éclairage · 22 ampoules", 99, "objets", "10.0.30.30", "Câble · port 15", .02, "on"),
    ("charger", "Borne de recharge · garage", "Borne de niveau 2 · 7,2 kW", 93, "objets", "10.0.30.70", "Câble · commutateur PoE · port 8", .05, "on"),
    ("printer", "Imprimante", "Imprimante laser · en veille", 94, "objets", "10.0.30.60", "Wi-Fi 2,4 GHz · Étage", 0.0, "idle"),
    ("camera", "Caméra · entrée", "Caméra 4K · infrarouge", 99, "cameras", "10.0.40.11", "PoE · port 3 · 6,1 W", 4.2, "on"),
    ("camera", "Caméra · garage", "Caméra 4K · infrarouge", 99, "cameras", "10.0.40.12", "PoE · port 7 · 6,5 W", 4.1, "on"),
    ("server", "JARVIS · serveur local", "Serveur · automatisation et vidéo", 100, "serveurs", "10.0.50.2", "Câble · 10 Gb/s · port 24", 31.0, "on"),
    ("server", "Stockage", "Stockage réseau · 4 disques", 100, "serveurs", "10.0.50.5", "Câble · 10 Gb/s · port 23", 17.0, "on"),
    ("phone", "Téléphone d’un invité", "Téléphone intelligent", 88, "invites", "10.0.20.103", "Wi-Fi 6 · Salon · −58 dBm", 5.6, "on"),
]


def mod_appareils():
    chips = '<button type="button" class="rs-chip" aria-pressed="true" data-vf="all">Tous <b>44</b></button>' + "".join(
        f'<button type="button" class="rs-chip z-{vid}" aria-pressed="false" data-vf="{vid}"><i></i>{name} <b>{n}</b></button>'
        for vid, num, name, n, *_ in VLANS
    )
    rows = []
    for icn, name, ident, conf, vid, ip, conn, mbps, st in DEVICES:
        v = VL[vid]
        rows.append(
            f'<tr data-vlan="{vid}" data-q="{a((name + " " + ident + " " + ip).lower())}">'
            f'<td><span class="rs-dv">{ic(icn)}<span><b>{name}</b><small>{ident}</small></span></span></td>'
            f'<td><span class="rs-conf" style="--v:{conf}%"><i></i>{conf} %</span></td>'
            f'<td><span class="rs-vtag z-{vid}">VLAN {v[1]}</span></td>'
            f'<td class="rs-mono">{ip}</td><td class="rs-dim">{conn}</td>'
            f'<td class="rs-mono rs-r" data-dev-mbps="{mbps}">{("%.1f" % mbps).replace(".", ",") if mbps >= .1 else "< 0,1"}</td>'
            f'<td>{pill("En ligne", "ok") if st == "on" else pill("En veille")}</td></tr>'
        )
    alert = f"""<div class="rs-new" data-new>
      <div class="rs-new-i">{ic("unknown")}<i class="rs-ping"></i></div>
      <div class="rs-new-t">
        <p class="rs-kick"><i class="rs-dot is-warn"></i>Nouvel appareil · 17 h 39</p>
        <b>Inconnu, puis identifié : prise connectée</b>
        <span>Empreinte DHCP, mDNS et TLS concordante à 91 % · fabricant d’après l’adresse MAC · arrivée par le Wi-Fi extérieur (−63 dBm). Placée d’office en <b>quarantaine</b> (VLAN 99) : elle n’atteint rien.</span>
      </div>
      {proposal("L’accepter dans les objets connectés (VLAN 30)",
                "Elle pourra parler à JARVIS seulement, comme les 18 autres objets.",
                ["Adresse réservée : 10.0.30.88", "Règles du VLAN 30 appliquées", "Confirmé : la prise est rangée et suivie."],
                "Mise de côté. Elle reste en quarantaine.", ok="Accepter")}
    </div>"""
    table = f"""<div class="rs-tools"><label class="rs-search">{ic("menaces")}<input type="search" placeholder="Chercher un appareil, une adresse…" aria-label="Chercher un appareil" data-dev-q></label><div class="rs-chips" role="group" aria-label="Filtrer par réseau">{chips}</div></div>
    <div class="rs-tablew"><table class="rs-table"><thead><tr><th>Appareil</th><th>Empreinte</th><th>Réseau</th><th>Adresse</th><th>Connexion</th><th class="rs-r">Mb/s</th><th>État</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
    <p class="rs-foot">16 appareils affichés sur 44 · chaque appareil est identifié par son empreinte réseau, sans logiciel à installer.</p>"""
    return (
        head("Appareils", "Chaque appareil connu, identifié et rangé dans sa zone. Un inconnu est isolé avant même qu’on vous le présente.",
             [("En ligne", "43 / 44", "", ""), ("Nouveaux · 7 j", "1", "is-warn", ""),
              ("Identifiés", "98 %", "", ""), ("Équipements réseau", "7", "", "")])
        + alert + card("Inventaire", table, "rs-inv")
    )


# ---------- Wi-Fi ----------
ROOMS = [
    # nom, x, y, w, h (plan du rez-de-chaussée, unités du viewBox 640 × 360)
    ("Salon", 20, 20, 250, 170), ("Cuisine", 270, 20, 180, 120), ("Salle à manger", 450, 20, 170, 120),
    ("Entrée", 270, 140, 110, 90), ("Bureau", 380, 140, 240, 90), ("Garage", 20, 190, 250, 150),
    ("Terrasse", 270, 230, 350, 110),
]
APS = [("Salon", 110, 96, "ap1"), ("Extérieur", 600, 240, "ap3")]
# Signal visé au centre de chaque pièce (dBm), cohérent avec le tableau des pièces.
ROOM_T = {"Salon": -46, "Cuisine": -54, "Salle à manger": -57, "Entrée": -52, "Bureau": -58, "Garage": -71, "Terrasse": -55}
WROOMS = [
    # pièce, étage, signal, débit, point d'accès, note
    ("Salon", "Rez-de-chaussée", -46, 1340, "Salon", "ok"),
    ("Cuisine", "Rez-de-chaussée", -54, 980, "Salon", "ok"),
    ("Bureau", "Rez-de-chaussée", -58, 720, "Salon", "ok"),
    ("Garage", "Rez-de-chaussée", -71, 96, "Salon", "warn"),
    ("Terrasse", "Extérieur", -55, 610, "Extérieur", "ok"),
    ("Chambre principale", "Étage", -50, 1120, "Étage", "ok"),
    ("Chambre des enfants", "Étage", -56, 840, "Étage", "ok"),
    ("Salle de jeu", "Sous-sol", -69, 140, "Étage", "warn"),
]


def mod_wifi():
    walls = "".join(f'<rect class="rs-room" x="{x}" y="{y}" width="{w}" height="{h}"/>' for _, x, y, w, h in ROOMS)
    labels = "".join(
        f'<g class="rs-rl" transform="translate({x + 12} {y + 22})"><text>{escape(n.upper())}</text>'
        f'<text class="rs-rv" y="16" data-room="{a(n)}"></text></g>'
        for n, x, y, w, h in ROOMS
    )
    doors = "".join(f'<rect class="rs-door" x="{x}" y="{y}" width="{w}" height="{h}"/>' for x, y, w, h in
                    [(150, 186, 40, 8), (266, 60, 8, 40), (446, 60, 8, 36), (300, 136, 40, 8), (376, 170, 8, 34),
                     (266, 260, 8, 40), (430, 226, 60, 8)])
    aps = "".join(
        f'<g class="rs-ap" transform="translate({x} {y})"><circle class="rs-ap-r" r="14"/><circle r="5"/>'
        f'<text y="-20">{escape(n.upper())}</text></g>' for n, x, y, _ in APS
    )
    plan = f"""<div class="rs-plan" data-wifi="{a(json.dumps({"aps": [[x, y] for _, x, y, _ in APS], "rooms": [[n, x, y, w, h, ROOM_T[n]] for n, x, y, w, h in ROOMS]}, ensure_ascii=False))}">
      <canvas class="rs-heat" width="640" height="360" aria-hidden="true"></canvas>
      <svg viewBox="0 0 640 360" role="img" aria-label="Plan du rez-de-chaussée avec la force du signal Wi-Fi par pièce">{walls}{doors}{labels}{aps}</svg>
      <div class="rs-scale" aria-hidden="true"><span>Excellent</span><i></i><span>Faible</span></div>
    </div>"""
    tr = "".join(
        f'<tr><td><b>{r}</b><small>{f}</small></td><td class="rs-mono">{s} dBm</td>'
        f'<td><span class="rs-meter is-{n}" style="--v:{min(100, max(8, (s + 90) * 2.5)):.0f}%"><i></i></span></td>'
        f'<td class="rs-mono rs-r">{d:,} Mb/s</td><td class="rs-dim">{p}</td></tr>'.replace(",", "\u202f")
        for r, f, s, d, p, n in WROOMS
    )
    aps_t = "".join(
        f'<li><span>{ic("ap")}<b>{n}</b><small>{std}</small></span><span class="rs-mono">{ch}</span>'
        f'<span class="rs-util" style="--v:{u}%"><i></i><em>{u} %</em></span><span class="rs-mono">{c}</span></li>'
        for n, std, ch, u, c in [("Salon", "Wi-Fi 7 · 2,4 / 5 / 6 GHz", "149 · 160 MHz", 34, "17 clients"),
                                 ("Étage", "Wi-Fi 7 · 2,4 / 5 / 6 GHz", "36 · 160 MHz", 22, "11 clients"),
                                 ("Extérieur", "Wi-Fi 6 · 2,4 / 5 GHz", "6 · 20 MHz", 41, "6 clients")]
    )
    ssid = "".join(
        f'<li><b>{n}</b><span>{d}</span>{pill(s, t)}</li>'
        for n, d, s, t in [("Maison", "WPA3 · VLAN 10 · 5 et 6 GHz", "Actif", "ok"),
                           ("Maison · Objets", "WPA2/WPA3 · VLAN 30 · 2,4 GHz", "Actif", "ok"),
                           ("Maison · Invités", "WPA3 · VLAN 20 · isolé", "Actif", "ok")]
    )
    tip = f"""<div class="rs-advice"><p class="rs-kick"><i class="rs-dot is-warn"></i>Conseil de JARVIS</p>
      <b>Garage et salle de jeu : signal faible.</b>
      <span>Le garage reçoit −71 dBm à travers deux murs. Déplacer le point d’accès du salon de 2 m vers la porte du garage gagnerait environ 9 dB; pour la salle de jeu, un point d’accès mural sur le port 12 du commutateur règle tout.</span></div>"""
    return (
        head("Wi-Fi", "La qualité du signal pièce par pièce, mesurée par les appareils eux-mêmes.",
             [("Qualité moyenne", "92 %", "", ""), ("Clients", "34", "", ""), ("Interférences", "Faibles", "", ""),
              ("Pièces faibles", "2", "is-warn", "")])
        + '<div class="rs-g2"><div class="rs-stack">'
        + card("Rez-de-chaussée · carte de chaleur", plan, "rs-c-plan",
               '<span class="rs-tag-live"><i></i>Mesure continue</span>')
        + card("Points d’accès", f'<ul class="rs-aps">{aps_t}</ul>')
        + "</div>"
        + card("Pièces", f'<div class="rs-tablew"><table class="rs-table rs-t-sm"><thead><tr><th>Pièce</th><th>Signal</th><th></th><th class="rs-r">Débit</th><th>Accès</th></tr></thead><tbody>{tr}</tbody></table></div>{tip}')
        + "</div>"
        + card("Réseaux diffusés", f'<ul class="rs-ssid rs-ssid-row">{ssid}</ul>')
    )


# ---------- Trafic ----------
APPS = [
    ("Diffusion vidéo", 118.0), ("Téléchargement de jeux", 86.0), ("Sauvegarde hors site", 42.0),
    ("Visioconférence", 24.0), ("Caméras (local)", 24.6), ("Navigation Web", 11.0), ("Mises à jour", 6.0),
]


def mod_trafic():
    tops = "".join(
        f'<li data-tdev="{i}"><span class="rs-dv">{ic(icn)}<b>{name}</b></span><span class="rs-bar"><i></i></span>'
        f'<span class="rs-mono" data-v>{("%.1f" % m).replace(".", ",")}</span></li>'
        for i, (icn, name, _i, _c, _v, _ip, _cn, m, _s) in enumerate(sorted(DEVICES, key=lambda d: -d[7])[:6])
    )
    apps = "".join(
        f'<li data-tapp="{i}"><span>{n}</span><span class="rs-bar"><i></i></span><span class="rs-mono" data-v>{("%.0f" % m)}</span></li>'
        for i, (n, m) in enumerate(APPS)
    )
    chart = """<div class="rs-chart"><canvas class="rs-tc" aria-hidden="true"></canvas>
      <div class="rs-chart-l"><span><i class="lg lg-d"></i>Réception</span><span><i class="lg lg-u"></i>Envoi</span><span class="rs-dim">60 dernières secondes</span></div>
      <p class="rs-chart-v"><b data-live="down">312</b><small>↓ Mb/s</small><b data-live="up">41</b><small>↑ Mb/s</small></p></div>"""
    month = "".join(
        f'<li><span>{n}</span><b class="rs-mono">{v}</b></li>'
        for n, v in [("Ce mois-ci", "2,84 To"), ("Moyenne par jour", "354 Go"), ("Heure de pointe", "20 h · 640 Mb/s"),
                     ("Plafond du forfait", "Illimité")]
    )
    return (
        head("Trafic", "Qui utilise la bande passante, et pour quoi, à la seconde près.",
             [("Réception", '<span data-live="down">312</span><small> Mb/s</small>', "", ""),
              ("Envoi", '<span data-live="up">41</span><small> Mb/s</small>', "", ""),
              ("Utilisation du lien", '<span data-live="pct">31</span> %', "", ""),
              ("Latence", '<span data-live="lat">9</span> ms', "", "")])
        + card("Débit en direct", chart, "rs-c-chart", '<span class="rs-tag-live"><i></i>En direct</span>')
        + '<div class="rs-g3">'
        + card("Par appareil", f'<ul class="rs-tops">{tops}</ul>')
        + card("Par usage", f'<ul class="rs-tops rs-apps">{apps}</ul>')
        + card("Volume", f'<ul class="rs-kv">{month}</ul><p class="rs-note">La qualité de service garde toujours 40 Mb/s pour la visioconférence et les appels, même quand la console télécharge.</p>')
        + "</div>"
    )


# ---------- Menaces ----------
HOME = (45.63, -72.96)
THREATS = [
    # heure, type, détail, source, pays, lat, lon, ton
    ("17:42:08", "Intrusion bloquée", "Balayage de 1 412 ports sur la passerelle", "203.0.113.47", "Pays-Bas", 52.37, 4.9, "bad"),
    ("17:40:51", "Force brute", "212 essais de connexion au VPN · adresse bannie 24 h", "198.51.100.23", "Brésil", -23.55, -46.63, "bad"),
    ("17:38:12", "Domaine malveillant", "suivi-colis-livraison[.]top · hameçonnage · Téléphone principal", "192.0.2.91", "Singapour", 1.35, 103.82, "warn"),
    ("17:33:40", "Objet suspect", "Prise connectée → serveur inconnu · pays inhabituel", "192.0.2.200", "Kazakhstan", 43.24, 76.89, "bad"),
    ("17:21:05", "Force brute", "Connexion au stockage depuis Internet · port fermé", "198.51.100.77", "Inde", 19.07, 72.88, "warn"),
    ("17:12:44", "Exploit connu", "Signature « injection dans un routeur » · CVSS 9,8", "203.0.113.9", "Roumanie", 44.43, 26.1, "bad"),
    ("16:58:10", "Domaine malveillant", "mise-a-jour-securite[.]click · publicité piégée · Tablette enfants", "192.0.2.14", "États-Unis", 37.77, -122.42, "warn"),
    ("16:40:02", "Commande et contrôle", "Réponse vers un réseau de zombies connu · 0 octet sorti", "203.0.113.150", "Afrique du Sud", -26.2, 28.05, "bad"),
    ("16:22:37", "Intrusion bloquée", "Balayage du port 3389 (bureau à distance)", "198.51.100.140", "Allemagne", 50.11, 8.68, "warn"),
    ("15:57:19", "Force brute", "Tentatives de mot de passe sur la caméra (depuis Internet)", "203.0.113.66", "Japon", 35.68, 139.69, "warn"),
]


def mod_menaces():
    data = {"rows": GEO.ROWS, "cols": GEO.COLS, "u": GEO.U, "lat0": GEO.LAT0, "lon0": GEO.LON0, "step": GEO.STEP,
            "home": HOME, "ev": [list(t) for t in THREATS]}
    W, H = GEO.SIZE
    feed = "".join(
        f'<li class="is-{t[7]}"><time>{t[0]}</time><span><b>{t[1]}</b><small>{escape(t[2])}</small>'
        f'<em>{t[3]} · {t[4]}</em></span>{pill("Bloqué", "ok")}</li>'
        for t in THREATS[:6]
    )
    cats = "".join(
        f'<li><span>{n}</span><span class="rs-bar" style="--v:{v / 6.42:.1f}%"><i></i></span><b class="rs-mono">{v}</b></li>'
        for n, v in [("Balayages et intrusions", 642), ("Domaines malveillants", 412), ("Force brute", 151),
                     ("Exploits connus", 37), ("Objets au comportement anormal", 23), ("Commande et contrôle", 19)]
    )
    mp = f"""<div class="rs-geo" data-geo="{a(json.dumps(data, ensure_ascii=False))}">
      <svg class="rs-geo-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Carte du monde : provenance des attaques bloquées vers la maison, à Saint-Hyacinthe">
        <path class="rs-geo-dots" d=""/><g class="rs-geo-arcs"></g><g class="rs-geo-home"></g>
      </svg>
      <div class="rs-geo-hud"><span><i class="rs-dot is-ok"></i>Bouclier actif</span><span><b data-live="blocked">1 284</b> blocages · 24 h</span></div>
    </div>"""
    return (
        head("Menaces", "Ce qui frappe à la porte, d’où ça vient, et ce que la passerelle a fait.",
             [("Bloqués · 24 h", '<span data-live="blocked">1 284</span>', "", ""), ("Intrusions", "37", "", ""),
              ("Adresses bannies", "9", "", ""), ("Passés", "0", "is-ok", "")])
        + card("Provenance en direct", mp, "rs-c-geo", '<span class="rs-tag-live"><i></i>En direct</span>')
        + '<div class="rs-g2 rs-g2-w">'
        + card("Journal", f'<ol class="rs-feed" aria-live="off">{feed}</ol>')
        + card("Par catégorie · 24 h", f'<ul class="rs-cats">{cats}</ul><p class="rs-note">Adresses d’exemple réservées à la documentation. Aucune donnée de vos appareils ne quitte la maison pour cette analyse.</p>')
        + "</div>"
    )


# ---------- VPN ----------
def mod_vpn():
    sess = "".join(
        f'<li><span class="rs-dv">{ic(icn)}<span><b>{n}</b><small>{d}</small></span></span>'
        f'<span class="rs-mono">{where}</span><span class="rs-mono" data-since="{since}">—</span>'
        f'<span class="rs-mono">{tx}</span>{pill(scope, "gold")}</li>'
        for icn, n, d, where, since, tx, scope in [
            ("phone", "Téléphone principal", "Tunnel chiffré · double authentification", "Montréal · LTE", 2780, "184 Mo", "Toute la maison"),
            ("charger", "Véhicule récréatif · routeur 5G", "Site à site · permanent", "Route 132 · 5G", 15120, "2,1 Go", "Caméras + JARVIS"),
            ("laptop", "Technicien · accès temporaire", "Approuvé par vous · expire à 19 h 00", "Granby · fibre", 640, "36 Mo", "Stockage seulement"),
        ]
    )
    prof = "".join(
        f'<li><b>{n}</b><span>{d}</span>{pill(s, t)}</li>'
        for n, d, s, t in [("Ordinateur portable", "Toute la maison · clé renouvelée il y a 12 j", "Hors ligne", ""),
                           ("Tablette · enfants", "Internet par la maison seulement · filtres actifs", "Hors ligne", ""),
                           ("Téléphone · adolescent", "Internet par la maison seulement", "Hors ligne", ""),
                           ("Ancien téléphone", "Révoqué le 3 nov. · clé détruite", "Révoqué", "bad")]
    )
    sec = "".join(
        f'<li>{ic("check", "rs-ic is-ok")}<span><b>{t}</b><small>{d}</small></span></li>'
        for t, d in [("Aucun port ouvert, sauf le tunnel", "Un seul port UDP, invisible aux balayages : il ne répond qu’aux clés connues."),
                     ("Double authentification", "Chaque nouvelle connexion demande une confirmation sur le téléphone principal."),
                     ("Accès au plus juste", "Chaque profil ne voit que ce dont il a besoin : le technicien n’atteint que le stockage."),
                     ("Tout est journalisé", "Qui, quand, d’où et vers quoi. Rien du contenu.")]
    )
    return (
        head("VPN · accès à distance", "Joindre la maison de partout, sans rien exposer sur Internet.",
             [("Sessions actives", "3", "", ""), ("Profils", "7", "", ""), ("Ports ouverts", "1", "", ""),
              ("Tentatives refusées · 24 h", "212", "", "")])
        + card("Sessions en cours", f'<ul class="rs-sess">{sess}</ul>', "", '<span class="rs-tag-live"><i></i>En direct</span>')
        + '<div class="rs-g2">'
        + card("Profils autorisés", f'<ul class="rs-ssid">{prof}</ul>')
        + card("Comment c’est protégé", f'<ul class="rs-checks">{sec}</ul>')
        + "</div>"
    )


# ---------- Contrôles parentaux et invités ----------
def _sched(blocks):
    seg = "".join(
        f'<i class="is-{k}" style="left:{s / 24 * 100:.2f}%;width:{(e - s) / 24 * 100:.2f}%"></i>' for s, e, k in blocks
    )
    return f'<span class="rs-sched">{seg}<b class="rs-now" style="left:{17.8 / 24 * 100:.2f}%"></b></span>'


def mod_controles():
    prof = []
    for name, devs, used, cap, sched, blocked, pid in [
        ("Enfants", "Tablette · console", 130, 180, [(0, 7, "off"), (7, 8, "on"), (15.5, 21, "on"), (21, 24, "off")],
         "Contenu adulte, jeux d’argent, réseaux sociaux, achats intégrés", "enf"),
        ("Adolescent", "Téléphone · ordinateur", 214, 300, [(0, 6.5, "off"), (6.5, 23, "on"), (23, 24, "off")],
         "Contenu adulte, jeux d’argent", "ado"),
    ]:
        prof.append(f"""<div class="rs-prof" data-prof="{pid}">
          <div class="rs-prof-h"><span class="rs-av">{name[0]}</span><span><b>{name}</b><small>{devs}</small></span>
            <button type="button" class="rs-switch" role="switch" aria-checked="false" data-pause="{pid}"><i></i><span>Mettre Internet en pause</span></button></div>
          <div class="rs-prof-row"><span class="rs-dim">Temps d’écran aujourd’hui</span><span class="rs-mono">{used // 60} h {used % 60:02d} / {cap // 60} h</span></div>
          <span class="rs-meter" style="--v:{used / cap * 100:.0f}%"><i></i></span>
          <div class="rs-prof-row"><span class="rs-dim">Horaire · Internet permis</span><span class="rs-mono">0 h — 12 h — 24 h</span></div>
          {_sched(sched)}
          <p class="rs-prof-b"><span class="rs-dim">Bloqué :</span> {blocked}</p>
          <p class="rs-paused">Internet en pause pour ce profil. Les appels et les messages à la famille restent permis.</p>
        </div>""")
    guest = f"""<div class="rs-guest">
      <div class="rs-guest-h"><span><b>Maison · Invités</b><small>WPA3 · VLAN 20 · appareils isolés entre eux</small></span>
        <button type="button" class="rs-switch is-on" role="switch" aria-checked="true" data-guest><i></i><span>Réseau invités</span></button></div>
      <ul class="rs-kv">
        <li><span>Mot de passe</span><b class="rs-mono" data-gpass>soleil-érable-42</b></li>
        <li><span>Renouvelé</span><b>chaque lundi · automatiquement</b></li>
        <li><span>Limite par appareil</span><b class="rs-mono">50 Mb/s</b></li>
        <li><span>Accès</span><b>Internet seulement · rien de la maison</b></li>
        <li><span>Connectés</span><b class="rs-mono" data-gcount>3 appareils</b></li>
      </ul>
      <div class="rs-acts"><button type="button" class="rs-btn" data-gnew>Générer un nouveau mot de passe</button></div>
    </div>"""
    return (
        head("Contrôles", "Des règles simples pour les enfants et les invités, sans fouiller le contenu de personne.",
             [("Profils", "2", "", ""), ("Pages bloquées · 7 j", "318", "", ""), ("Invités connectés", '<span data-gk>3</span>', "", ""),
              ("Coucher des enfants", "21 h", "", "")])
        + f'<div class="rs-g2">{"".join(card("Profil", p) for p in prof)}</div>'
        + '<div class="rs-g2">'
        + card("Réseau invités", guest)
        + card("Ce que voit chaque profil", '<ul class="rs-checks">' + "".join(
            f'<li>{ic("check", "rs-ic is-ok")}<span><b>{t}</b><small>{d}</small></span></li>' for t, d in [
                ("Filtrage par catégorie", "Au niveau du nom de domaine : aucune application à installer, rien à contourner sur l’appareil."),
                ("Recherche sécurisée forcée", "Sur les moteurs de recherche et les sites de vidéos des profils Enfants."),
                ("Aucun contenu lu", "JARVIS voit qu’un site est bloqué, jamais ce qui est écrit ou regardé."),
            ]) + "</ul>")
        + "</div>"
    )


# ---------- Continuité ----------
def mod_continuite():
    links = "".join(
        f"""<div class="rs-wan{" is-on" if k == "fibre" else ""}" data-wan="{k}">
          <div class="rs-wan-h"><span class="rs-wan-n">{p}</span><span><b>{n}</b><small>{d}</small></span>{pill(s, t)}</div>
          <svg class="rs-spark" viewBox="0 0 200 40" preserveAspectRatio="none" aria-hidden="true"><path class="rs-spark-a" d=""/><path class="rs-spark-l" d=""/></svg>
          <div class="rs-wan-f"><span><small>Latence</small><b class="rs-mono" data-lat="{k}">{l} ms</b></span><span><small>Perte</small><b class="rs-mono">{loss}</b></span><span><small>Débit max</small><b class="rs-mono">{bw}</b></span></div>
        </div>"""
        for k, p, n, d, s, t, l, loss, bw in [
            ("fibre", "1", "Fibre", "Principal · symétrique", "Actif", "ok", 9, "0 %", "1 Gb/s"),
            ("g5", "2", "Routeur 5G", "Secours · forfait 100 Go", "En veille", "", 31, "0 %", "420 Mb/s"),
            ("star", "3", "Satellite", "Secours · dernier recours", "En veille", "", 38, "0,1 %", "220 Mb/s"),
        ]
    )
    tl = "".join(
        f'<li data-t="{i}"><time>{t}</time><span><b>{h}</b><small>{d}</small></span></li>'
        for i, (t, h, d) in enumerate([
            ("18:03:00.0", "Fibre muette", "3 sondes sur 3 sans réponse en 1,2 s"),
            ("18:03:01.4", "Bascule décidée", "Règle approuvée à l’installation · aucun clic requis"),
            ("18:03:02.1", "5G active", "Nouvelle adresse publique · DNS dynamique mis à jour"),
            ("18:03:03.0", "Tout est reconnecté", "VPN, appels et caméras à distance · coupure ressentie : 2,1 s"),
            ("18:41:27.5", "Fibre de retour", "Stable depuis 5 min : retour automatique, sans coupure"),
        ])
    )
    power = "".join(
        f'<li><span>{n}</span><b class="rs-mono">{v}</b></li>'
        for n, v in [("Onduleur · armoire réseau", "100 % · 41 min"), ("Consommation", "86 W"),
                     ("Dernier test de la batterie", "1er nov. · réussi"), ("Arrêt propre programmé", "à 10 % de batterie")]
    )
    return (
        head("Continuité", "Si la fibre tombe, la maison bascule seule et vous le dit après.",
             [("Lien actif", '<span data-live="wan">Fibre · 9 ms</span>', "", ""), ("Disponibilité · 30 j", "99,998 %", "", ""),
              ("Bascules · 30 j", "1", "", ""), ("Coupure ressentie", "2,1 s", "", "")])
        + f'<div class="rs-wans">{links}</div>'
        + '<div class="rs-g2 rs-g2-w">'
        + card("Dernière bascule · 28 oct.", f'<ol class="rs-tl">{tl}</ol><div class="rs-acts"><button type="button" class="rs-btn rs-btn-pri" data-failover>Simuler une coupure de la fibre</button></div>', "rs-c-tl")
        + card("Électricité", f'<ul class="rs-kv">{power}</ul><p class="rs-note">Passerelle, commutateurs, points d’accès et JARVIS sont sur l’onduleur : une panne de courant n’éteint pas le réseau.</p>')
        + "</div>"
    )


# ---------- Sauvegardes ----------
def mod_sauvegardes():
    copies = "".join(
        f'<div class="rs-copy"><span class="rs-copy-n">{n}</span><b>{t}</b><small>{d}</small>'
        f'<span class="rs-copy-f"><span class="rs-mono">{s}</span>{pill(st, "ok")}</span></div>'
        for n, t, d, s, st in [
            ("1", "Stockage local", "Dans la maison · 4 disques en miroir", "2,1 To · il y a 2 h", "À jour"),
            ("2", "Hors site, chiffré", "Centre de données au Québec · clé gardée chez vous", "2,1 To · il y a 2 h", "À jour"),
            ("3", "Copie immuable", "Impossible à effacer ou chiffrer pendant 30 jours", "30 versions", "Protégée"),
        ]
    )
    jobs = "".join(
        f'<tr><td><b>{n}</b><small>{d}</small></td><td class="rs-mono">{f}</td><td class="rs-mono">{l}</td><td class="rs-mono rs-r">{s}</td><td>{pill("Réussie", "ok")}</td></tr>'
        for n, d, f, l, s in [
            ("Configuration du réseau", "Passerelle, commutateurs, points d’accès, règles", "Chaque jour · 3 h", "Aujourd’hui 3 h 00", "4,2 Mo"),
            ("JARVIS", "Automatisations, réglages, historique", "Chaque heure", "Aujourd’hui 15 h 00", "1,8 Go"),
            ("Enregistrements des caméras", "30 jours glissants · 6 caméras", "En continu", "Il y a 4 min", "1,6 To"),
            ("Ordinateurs de la famille", "Documents et photos", "Chaque nuit", "Aujourd’hui 1 h 12", "412 Go"),
            ("Téléphones", "Photos et contacts", "En recharge, sur le Wi-Fi", "Hier 23 h 40", "96 Go"),
        ]
    )
    test = f"""<div class="rs-restore">
      <p class="rs-kick"><i class="rs-dot is-ok"></i>Dernier test de restauration · 2 nov.</p>
      <b>Configuration de la passerelle restaurée sur un appareil de test en 4 min 12 s.</b>
      <span>Une sauvegarde qu’on n’a jamais restaurée n’est qu’un espoir : JARVIS en teste une chaque mois, automatiquement, sans toucher au réseau en service.</span>
      <ol class="rs-flowl rs-rflow" aria-live="polite">
        <li><i></i><span>Copie hors site téléchargée et déchiffrée</span></li>
        <li><i></i><span>Empreinte vérifiée · identique à l’original</span></li>
        <li><i></i><span>Restaurée dans un environnement isolé</span></li>
        <li><i></i><span>Réussi en 3 min 58 s · rapport ajouté au journal</span></li>
      </ol>
      <div class="rs-acts"><button type="button" class="rs-btn rs-btn-pri" data-restore>Lancer un test maintenant</button></div>
    </div>"""
    return (
        head("Sauvegardes", "Trois copies, deux endroits, une qui ne peut pas être effacée. Et on vérifie qu’elles marchent.",
             [("Dernière sauvegarde", "Il y a 2 h", "", ""), ("Copies", "3", "", ""), ("Dernier test", "2 nov. · réussi", "is-ok", ""),
              ("Prochain test", "2 déc.", "", "")])
        + f'<div class="rs-copies">{copies}</div>'
        + card("Test de restauration", test, "rs-c-restore")
        + card("Tâches", f'<div class="rs-tablew"><table class="rs-table rs-t-sm"><thead><tr><th>Quoi</th><th>Fréquence</th><th>Dernière</th><th class="rs-r">Taille</th><th></th></tr></thead><tbody>{jobs}</tbody></table></div>')
    )


# ---------- Mises à jour ----------
PATCHES = [
    ("Passerelle pare-feu", "4.1.13", "4.1.15", 9.8, "Contournement de l’authentification à distance", "crit"),
    ("Caméra · garage", "2.8.4", "2.8.6", 7.5, "Accès au flux vidéo sans mot de passe", "plan"),
    ("Point d’accès · extérieur", "7.0.66", "7.0.76", 5.3, "Déni de service sur le Wi-Fi invités", "plan"),
    ("Commutateur PoE", "6.6.61", "6.6.65", 4.3, "Correctifs de stabilité", "plan"),
    ("Commutateur cœur", "7.1.26", "7.1.26", 0, "À jour", "ok"),
    ("Points d’accès · salon et étage", "7.0.76", "7.0.76", 0, "À jour", "ok"),
    ("JARVIS", "2026.11.2", "2026.11.2", 0, "À jour", "ok"),
    ("Ancienne caméra · cabanon", "1.9.2", "—", 8.1, "Fin de support : plus aucune mise à jour", "eol"),
]


def mod_maj():
    def sev(s):
        if s >= 9:
            return "crit", "Critique"
        if s >= 7:
            return "high", "Élevée"
        if s >= 4:
            return "med", "Moyenne"
        return "none", "—"
    rows = []
    for name, cur, new, score, what, st in PATCHES:
        k, lab = sev(score)
        sc = f'<span class="rs-cvss is-{k}"><b>{str(score).replace(".", ",")}</b>{lab}</span>' if score else '<span class="rs-cvss is-none"><b>—</b>Aucune</span>'
        state = {"crit": pill("Votre accord requis", "bad"), "plan": pill("Planifiée · cette nuit 3 h", "gold"),
                 "ok": pill("À jour", "ok"), "eol": pill("À remplacer · isolée", "warn")}[st]
        rows.append(
            f'<tr class="is-{st}"><td><b>{name}</b><small>{what}</small></td><td class="rs-mono">{cur}</td>'
            f'<td class="rs-mono">{new}</td><td>{sc}</td><td data-pstate>{state}</td></tr>'
        )
    crit = f"""<div class="rs-crit">
      <div class="rs-crit-s"><b>9,8</b><small>CVSS · critique</small></div>
      <div class="rs-crit-t">
        <p class="rs-kick"><i class="rs-dot is-bad"></i>Faille critique · passerelle pare-feu</p>
        <b>Un correctif ferme une faille connue depuis hier.</b>
        <span>Elle permettrait de se connecter à la console de la passerelle sans mot de passe. Chez vous, la console n’est pas exposée à Internet : le risque réel est faible, mais la règle est claire, on corrige.</span>
        {proposal("Installer cette nuit à 3 h 00 (coupure de 90 s)",
                  "Configuration sauvegardée avant, retour automatique à la version précédente si un test échoue.",
                  ["Planifié pour cette nuit · 3 h 00", "Sauvegarde de la configuration prévue juste avant", "Confirmé : le résultat des 14 tests vous attendra demain matin."],
                  "Mis de côté. JARVIS vous le redemandera demain matin.", ok="Approuver pour cette nuit")}
      </div></div>"""
    return (
        head("Mises à jour", "Chaque équipement, sa version, ses failles connues et quand on les corrige.",
             [("Équipements", "21", "", ""), ("À jour", "17", "is-ok", ""), ("Planifiées", "3", "", ""),
              ("Critiques", '<span data-crit>1</span>', "is-bad", "")])
        + crit
        + card("Micrologiciels", f'<div class="rs-tablew"><table class="rs-table"><thead><tr><th>Équipement</th><th>Version</th><th>Disponible</th><th>Gravité (CVSS)</th><th>État</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
               '<p class="rs-foot">Gravité selon l’échelle CVSS de 0 à 10. L’ancienne caméra du cabanon ne recevra plus de correctifs : elle est isolée en attendant son remplacement.</p>')
    )


# ---------- Segmentation ----------
SEG_Z = [("perso", "Personnel"), ("invites", "Invités"), ("objets", "Objets"), ("cameras", "Caméras"),
         ("serveurs", "Serveurs"), ("internet", "Internet")]
# (source, destination) : (verdict, texte court, explication, blocages 24 h)
SEG = {
    ("perso", "objets"): ("lim", "Limité", "Vos appareils peuvent commander le téléviseur et l’imprimante, rien d’autre.", 0),
    ("perso", "cameras"): ("lim", "Limité", "Voir les caméras par JARVIS seulement, jamais directement.", 0),
    ("perso", "serveurs"): ("ok", "Permis", "Ordinateurs et téléphones joignent JARVIS et le stockage.", 0),
    ("perso", "invites"): ("no", "Bloqué", "Les invités ne sont jamais joignables depuis la maison.", 0),
    ("perso", "internet"): ("ok", "Permis", "Filtré selon le profil (enfants, adolescent).", 0),
    ("invites", "internet"): ("ok", "Permis", "Internet seulement, 50 Mb/s par appareil.", 0),
    ("objets", "serveurs"): ("lim", "JARVIS seul.", "Les objets ne parlent qu’à JARVIS, sur un seul port chiffré.", 0),
    ("objets", "internet"): ("lim", "Liste blanche", "Seulement les services prévus par le fabricant; tout le reste est bloqué.", 23),
    ("objets", "perso"): ("no", "Bloqué", "Une ampoule ou une prise ne peut jamais joindre un ordinateur.", 41),
    ("cameras", "serveurs"): ("lim", "Enregistrement", "Les caméras envoient leur image à JARVIS, rien d’autre.", 0),
    ("cameras", "internet"): ("no", "Bloqué", "Aucune caméra ne parle à Internet : pas de nuage, pas de fuite.", 6),
    ("serveurs", "internet"): ("lim", "Sauvegardes", "Sauvegardes hors site et mises à jour seulement.", 0),
    ("serveurs", "objets"): ("ok", "Permis", "JARVIS commande les objets connectés.", 0),
    ("serveurs", "cameras"): ("ok", "Permis", "JARVIS reçoit et enregistre les caméras.", 0),
    ("internet", "perso"): ("no", "Bloqué", "Rien n’entre sans avoir été demandé de l’intérieur.", 642),
    ("internet", "serveurs"): ("vpn", "VPN seul.", "Seulement par le tunnel, avec une clé connue.", 212),
}


def mod_segmentation():
    hdr = "".join(f'<th scope="col"><span>{n}</span></th>' for _, n in SEG_Z)
    body = []
    for s, sn in SEG_Z:
        cells = []
        for d, dn in SEG_Z:
            if s == d:
                cells.append('<td class="is-self"><span>—</span></td>')
                continue
            v, short, why, hits = SEG.get((s, d), ("no", "Bloqué", "Refusé par défaut : tout ce qui n’est pas permis est bloqué.", 0))
            cells.append(
                f'<td class="is-{v}"><button type="button" data-seg="{a(sn + " → " + dn)}" data-why="{a(why)}" data-hits="{hits}" data-v="{v}">'
                f'<span>{short}</span>{f"<small>{hits}</small>" if hits else ""}</button></td>'
            )
        body.append(f'<tr><th scope="row">{sn}</th>{"".join(cells)}</tr>')
    detail = """<div class="rs-segd" aria-live="polite"><p class="rs-kick">Règle sélectionnée</p><b data-sd-t>Objets → Personnel</b>
      <span class="rs-segd-v" data-sd-v>Bloqué</span><p data-sd-w>Une ampoule ou une prise ne peut jamais joindre un ordinateur.</p>
      <p class="rs-mono rs-dim" data-sd-h>41 tentatives bloquées · 24 h</p></div>"""
    return (
        head("Segmentation", "Qui a le droit de parler à qui. Tout ce qui n’est pas permis est bloqué.",
             [("Zones", "5 + Internet", "", ""), ("Règles", "18", "", ""), ("Bloqué par défaut", "Oui", "is-ok", ""),
              ("Tentatives bloquées · 24 h", "924", "", "")])
        + '<div class="rs-g2 rs-g2-seg">'
        + card("Matrice des règles · source → destination",
               f'<div class="rs-tablew"><table class="rs-matrix"><thead><tr><th><small>De ↓ · vers →</small></th>{hdr}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
               '<ul class="rs-mleg"><li><i class="is-ok"></i>Permis</li><li><i class="is-lim"></i>Limité</li><li><i class="is-vpn"></i>VPN seulement</li><li><i class="is-no"></i>Bloqué</li></ul>')
        + card("", detail, "rs-c-segd")
        + "</div>"
    )


# ---------- Score ----------
FACTORS = [
    ("Exposition à Internet", 15, 15, "ok", "Un seul port ouvert (le VPN), invisible aux balayages."),
    ("Segmentation", 15, 15, "ok", "5 zones séparées, blocage par défaut, aucune exception risquée."),
    ("Sauvegardes", 15, 15, "ok", "3 copies, dont une immuable; test de restauration réussi le 2 nov."),
    ("Wi-Fi", 10, 9, "ok", "WPA3 partout sauf le réseau des objets (WPA2/WPA3, pour les vieux appareils)."),
    ("Accès et mots de passe", 15, 14, "ok", "Double authentification partout; un compte de technicien expire ce soir."),
    ("Mises à jour", 15, 9, "bad", "Une faille critique sur la passerelle attend votre accord pour cette nuit."),
    ("Appareils", 10, 6, "warn", "Une ancienne caméra sans support; une prise en quarantaine à valider."),
    ("Surveillance", 5, 3, "warn", "Les journaux sont gardés 30 jours; 90 jours serait mieux pour une enquête."),
]
WEEKS = [71, 74, 74, 78, 80, 79, 82, 86]


def mod_score():
    total = sum(f[2] for f in FACTORS)
    facts = "".join(
        f'<li class="is-{t}"><div><b>{n}</b><span class="rs-mono">{g} / {m}</span></div>'
        f'<span class="rs-meter is-{t}" style="--v:{g / m * 100:.0f}%"><i></i></span><small>{why}</small></li>'
        for n, m, g, t, why in FACTORS
    )
    bars = "".join(
        f'<li style="--v:{(v - 60) / 40 * 100:.0f}%"{" class=is-now" if i == len(WEEKS) - 1 else ""}><i></i><b>{v}</b><small>S{37 + i}</small></li>'
        for i, v in enumerate(WEEKS)
    )
    gain = "".join(
        f'<li><span class="rs-gain">+{p}</span><span><b>{t}</b><small>{d}</small></span></li>'
        for p, t, d in [(6, "Approuver le correctif de la passerelle", "Module Mises à jour · coupure de 90 s cette nuit"),
                        (3, "Remplacer l’ancienne caméra du cabanon", "Un modèle compatible coûte environ 180 $"),
                        (2, "Garder les journaux 90 jours", "Un clic · 14 Go de plus sur le stockage")]
    )
    C = 2 * 3.14159 * 70
    gauge = f"""<div class="rs-gauge" style="--v:{total}">
      <svg viewBox="0 0 180 180" aria-hidden="true"><circle class="rs-g-bg" cx="90" cy="90" r="70"/>
        <circle class="rs-g-fg" cx="90" cy="90" r="70" style="stroke-dasharray:{C * total / 100:.1f} {C:.1f}"/></svg>
      <div><b>{total}</b><small>sur 100</small><em>+4 en une semaine</em></div></div>"""
    return (
        head("Score de la semaine", "Une note simple, expliquée ligne par ligne, et ce qui la ferait monter.",
             [("Score", f"{total} / 100", "", ""), ("Tendance · 8 sem.", "+15", "is-ok", ""), ("Points à gagner", "11", "", ""),
              ("Rapport", "Chaque lundi · 8 h", "", "")])
        + '<div class="rs-g2 rs-g2-score">'
        + card("", gauge + f'<ol class="rs-weeks" aria-label="Score des 8 dernières semaines">{bars}</ol>'
               f'<div><p class="rs-kick">Pour gagner des points cette semaine</p><ul class="rs-gains">{gain}</ul></div>', "rs-c-gauge")
        + card("Ce qui compose la note", f'<ul class="rs-facts2">{facts}</ul>')
        + "</div>"
    )


BUILDERS = {"topo": mod_topo, "appareils": mod_appareils, "wifi": mod_wifi, "trafic": mod_trafic,
            "menaces": mod_menaces, "vpn": mod_vpn, "controles": mod_controles, "continuite": mod_continuite,
            "sauvegardes": mod_sauvegardes, "maj": mod_maj, "segmentation": mod_segmentation, "score": mod_score}

LINKS = [
    ("Sécurité", "/solutions/securite-intelligente/#jarvis", "Les 6 caméras vivent seules sur le VLAN 40 : elles enregistrent chez JARVIS et ne voient ni Internet ni vos ordinateurs."),
    ("Environnements", "/solutions/environnements-intelligents/#jarvis", "Thermostats, lumières et prises restent sur le VLAN 30 et ne parlent qu’à JARVIS, même quand Internet tombe."),
    ("Mobilité", "/solutions/mobilite/#jarvis", "Le routeur 5G du véhicule récréatif rejoint la maison par un tunnel VPN site à site : caméras et réglages, en route."),
]


def build():
    tabs = "".join(
        f'<button type="button" class="rs-tab{" is-warn" if k in WARN else ""}" data-mod="{k}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'{ic(MOD_IC[k])}<span><b>{n}</b><small data-mstate="{k}">{s}</small></span></button>'
        for i, (k, n, s) in enumerate(MODULES)
    )
    panels = "".join(
        f'<section class="rs-mod" data-panel="{k}" aria-label="{a(n)}"{"" if k == "topo" else " hidden"}>{BUILDERS[k]()}</section>'
        for k, n, _ in MODULES
    )
    links = "".join(
        f'<li><a href="{h}">{ic("link")}<b>{n}</b></a><span>{t}</span></li>' for n, h, t in LINKS
    )
    status = "".join(
        f'<div class="rs-s{" " + c if c else ""}"><dt>{t}</dt><dd>{v}</dd></div>'
        for t, v, c in [
            ("Internet", '<i class="rs-dot is-ok"></i><span data-live="wan">Fibre · 9 ms</span>', ""),
            ("En direct", '<span data-live="down">312</span> ↓ <span class="rs-dim">·</span> <span data-live="up">41</span> ↑ <small>Mb/s</small>', ""),
            ("Appareils", '44 <small class="rs-warn-t">· 1 nouveau</small>', ""),
            ("Bloqués · 24 h", '<span data-live="blocked">1 284</span>', ""),
            ("Score", '86<small> / 100</small>', "is-score"),
        ]
    )
    return f"""<div class="demo-shell" data-demo="reseau">
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Réseau et cybersécurité</b><span class="rs-site">Résidence · Saint-Hyacinthe</span><span class="rs-clock" data-clock>17:52:04</span><span class="tag tag-sim">Démo · données d’exemple</span></div>
  <div class="demo-body">
    <dl class="rs-status">{status}</dl>
    <nav class="rs-tabs" aria-label="Modules du réseau">{tabs}</nav>
    <div class="rs-panels">{panels}</div>
    <div class="rs-links"><p class="rs-kick">Relié aux autres extensions</p><ul>{links}</ul></div>
  </div>
</div>
<p class="demo-hint">Douze modules · choisissez une situation sur la carte · rien n’est appliqué sans votre accord</p>"""


HTML = nb(build())
