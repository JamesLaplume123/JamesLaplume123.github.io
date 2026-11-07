# Module « Éclairage » des Environnements intelligents (dossier « JARVIS accueil lumières », 13 pages).
# Une seule source de vérité pour les huit environnements : zones, lumières, plans, ambiances et
# configurations, transmises au script (assets/demos/lumieres.js) par un bloc JSON unique.
#
# Coordonnées : en pixels du plan de chaque environnement (photo ou dessin SVG).
#   fx = points lumineux (x, y, portée[, couleur imposée]);  st = bandes (x1, y1, x2, y2);
#   dk = zones à assombrir sur une photo où la lumière est déjà présente (x, y, rx, ry).
# Les photos ne sont jamais retouchées : la lumière est une couche posée dessus.
# Le contrat de comportement (page 13 du dossier) est appliqué par le script :
# aperçu et brouillon n'envoient rien, le précédent est protégé avant la première commande,
# chaque lumière confirme son propre résultat, une sauvegarde est toujours explicite.

import json

from demos.maison import H as MZ_H, LUMIERE as MZ_LUMIERE, ROOMS as MZ_ROOMS, W as MZ_W

# ---------------------------------------------------------------------------------------------
# Ambiances : un style, jamais une configuration. Couleur des bandes RGB, température des
# lumières blanches (K) et niveau par défaut. « cats » sert aux filtres de la Bibliothèque.
# ---------------------------------------------------------------------------------------------
AMBIANCES = [
    {"k": "heure-doree", "name": "Heure dorée", "desc": "Un soir tout en chaleur.", "cats": ["chaleureuses"],
     "c": "#ffb35c", "kv": 2400, "lvl": 70, "word": "chaleur",
     "title": "Le soir, tout simplement.", "cap": "Une lumière chaude pour ralentir."},
    {"k": "ocean", "name": "Océan", "desc": "Une touche de fraîcheur.", "cats": ["colorees"],
     "c": "#3d9bff", "kv": 6200, "lvl": 54, "word": "Bleu",
     "title": "Comme au bord de l’eau.", "cap": "Un bleu calme, sans éblouir."},
    {"k": "aurore", "name": "Aurore", "desc": "Un peu de couleur, beaucoup de douceur.", "cats": ["colorees", "douces"],
     "c": "#38e0c4", "c2": "#b169ff", "kv": 4200, "lvl": 60, "word": "Aurore",
     "title": "Le ciel du Nord, à l’intérieur.", "cap": "Turquoise et violet, tout en douceur."},
    {"k": "lecture", "name": "Lecture", "desc": "Pour rester encore un chapitre.", "cats": ["chaleureuses"],
     "c": "#ffe7c2", "kv": 3600, "lvl": 90, "word": "chaleur",
     "title": "Encore une page.", "cap": "Une lumière franche, juste assez chaude."},
    {"k": "cinema", "name": "Cinéma", "desc": "La lumière se fait discrète.", "cats": ["colorees", "douces"],
     "c": "#8f5cff", "kv": 2700, "lvl": 25, "word": "Violet",
     "title": "L’écran d’abord.", "cap": "Une lueur violette, en retrait."},
    {"k": "nuit-douce", "name": "Nuit douce", "desc": "Juste assez pour vous accompagner.", "cats": ["douces", "chaleureuses"],
     "c": "#ff9440", "kv": 2000, "lvl": 15, "word": "Nuit",
     "title": "Le passage, sans éblouir.", "cap": "Une veilleuse ambrée au ras du sol."},
    # Style global : une seule teinte ambrée pour tout l’environnement, là où c’est allumé.
    {"k": "signature", "name": "Signature", "desc": "Une lumière ambrée, partout où c’est allumé.", "cats": ["chaleureuses"],
     "c": "#ffa94d", "kv": 2300, "lvl": 70, "word": "Signature", "style": True, "tone": "ambre",
     "title": "Signature", "cap": "Une lumière ambrée, partout où c’est allumé."},
]
# Photos du dossier (couloir de BouLance dans chaque ambiance); Signature reprend la photo ambrée.
AMB_PHOTO = {a["k"]: a["k"] for a in AMBIANCES if a["k"] != "signature"}
AMB_PHOTO["signature"] = "heure-doree"


# ---------------------------------------------------------------------------------------------
# Dessins des plans (SVG) : plan d’architecte de luxe, fond presque noir, murs dorés fins,
# mobilier esquissé. Les couleurs viennent des variables du mode (assets/demos/lumieres.css).
# ---------------------------------------------------------------------------------------------
def _r(x, y, w, h, c="fu", rx=0):
    return f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}"{f" rx={chr(34)}{rx}{chr(34)}" if rx else ""}/>'


def _l(x1, y1, x2, y2, c="w2"):
    return f'<line class="{c}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def _c(x, y, r, c="fu"):
    return f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}"/>'


def _p(d, c="fu"):
    return f'<path class="{c}" d="{d}"/>'


def _t(x, y, s, a="start"):
    return f'<text class="tx" x="{x}" y="{y}" text-anchor="{a}">{s}</text>'


def _walls(*segs):
    """Murs porteurs : une suite de segments (x1, y1, x2, y2)."""
    return "".join(_l(*s, c="w") for s in segs)


def _bed(x, y, w, h, vertical=True):
    if vertical:
        pw = (w - 18) / 2
        return (_r(x, y, w, h, rx=4) + _r(x + 6, y + 6, pw, 16, "fu2", 3) + _r(x + 12 + pw, y + 6, pw, 16, "fu2", 3)
                + _l(x + 3, y + h * .42, x + w - 3, y + h * .42, "fu2"))
    ph = (h - 18) / 2
    return (_r(x, y, w, h, rx=4) + _r(x + 6, y + 6, 16, ph, "fu2", 3) + _r(x + 6, y + 12 + ph, 16, ph, "fu2", 3)
            + _l(x + w * .42, y + 3, x + w * .42, y + h - 3, "fu2"))


def _tree(x, y, r):
    return _c(x, y, r, "tr") + _c(x, y, r * .45, "fu2")


def _car(x, y, w, h, sport=False):
    """Voiture vue de haut, capot vers le bas (vers la porte)."""
    r = w * (.42 if sport else .32)
    s = _r(x, y, w, h, rx=r)
    s += _p(f"M{x + w * .14},{y + h * .62} Q{x + w / 2},{y + h * .54} {x + w * .86},{y + h * .62} "
            f"L{x + w * .8},{y + h * .72} Q{x + w / 2},{y + h * .67} {x + w * .2},{y + h * .72} Z", "fu2")
    s += _p(f"M{x + w * .18},{y + h * .3} Q{x + w / 2},{y + h * .24} {x + w * .82},{y + h * .3} "
            f"L{x + w * .84},{y + h * .38} Q{x + w / 2},{y + h * .33} {x + w * .16},{y + h * .38} Z", "fu2")
    for wx in (x - 5, x + w - 3):
        for wy in (y + h * .18, y + h * .7):
            s += _r(wx, wy, 8, h * .13, "fu", 2)
    return s


def _frame(body, title, w=1000, h=600):
    """Fond, trame, règle et cartouche communs à tous les plans dessinés."""
    grid = _p("".join(f"M{x} 0V{h}" for x in range(40, w, 40)) + "".join(f"M0 {y}H{w}" for y in range(40, h, 40)), "gr")
    ticks = _p("".join(f"M{x} 4V12" for x in range(40, w, 40)) + "".join(f"M4 {y}H12" for y in range(40, h, 40)), "tk")
    north = (f'<g class="nn" transform="translate({w - 34} 34)">{_c(0, 0, 13, "fu2")}'
             f'{_p("M0,-10 L4,4 L0,1 L-4,4 Z", "nr")}<text class="tx" x="0" y="-17" text-anchor="middle">N</text></g>')
    scale = (f'<g transform="translate({w - 150} {h - 18})">{_l(0, 0, 100, 0, "tk")}{_l(0, -4, 0, 4, "tk")}'
             f'{_l(50, -3, 50, 3, "tk")}{_l(100, -4, 100, 4, "tk")}{_t(0, -8, "0")}{_t(100, -8, "5 m", "end")}</g>')
    return (f'<svg class="lu-art" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<rect class="bg" width="{w}" height="{h}"/>{grid}{ticks}{body}{north}{scale}'
            f'{_t(18, h - 14, "JARVIS · PLAN · " + title)}</svg>')


def _plan_chalet():
    b = ""
    b += "".join(_tree(*t) for t in [(62, 110, 30), (56, 300, 34), (74, 520, 26), (972, 92, 26), (948, 522, 30),
                                      (860, 566, 22), (252, 566, 24), (690, 574, 20), (40, 420, 22)])
    # Terrasse et sentier
    b += _r(178, 468, 560, 52, "fu2", 6) + _l(440, 520, 432, 598, "fu2") + _l(482, 520, 492, 598, "fu2")
    for x in range(198, 738, 40):
        b += _l(x, 468, x, 520, "fu3")
    # Planchers
    b += _r(130, 80, 640, 380, "fl")
    # Spa : terrasse de bois et bain à remous
    b += _r(770, 150, 180, 270, "fl")
    for y in range(164, 420, 14):
        b += _l(774, y, 946, y, "fu3")
    b += _c(860, 285, 64, "fu") + _c(860, 285, 50, "fu2") + _r(912, 270, 30, 30, "fu2", 4)
    # Salon : foyer de pierre, sofas, tapis, escalier vers la mezzanine
    b += _r(130, 212, 28, 96, "fu") + _r(134, 238, 14, 44, "fu2") + _r(158, 222, 22, 76, "fu2")
    b += _r(178, 176, 172, 196, "fu2 dash", 8) + _r(232, 244, 56, 56, "fu", 10)
    b += _r(306, 192, 30, 134, "fu", 6) + _r(192, 334, 144, 30, "fu", 6) + _r(192, 182, 36, 36, "fu", 8)
    b += _r(392, 316, 62, 132, "fu")
    for y in range(328, 448, 12):
        b += _l(392, y, 454, y, "fu2")
    b += _r(392, 104, 44, 44, "fu", 10) + _c(448, 100, 8, "fu2")
    b += _r(160, 74, 280, 8, "gl")
    # Cuisine
    b += _r(480, 88, 282, 28, "fu") + _r(556, 92, 40, 20, "fu2", 3) + _r(656, 92, 40, 20, "fu2", 3)
    b += "".join(_c(666 + dx, 102, 4, "fu2") for dx in (0, 20)) + _r(736, 122, 28, 44, "fu")
    b += _r(540, 158, 162, 46, "fu", 6) + "".join(_c(x, 220, 8, "fu2") for x in (560, 600, 640, 680))
    # Chambres
    b += _bed(504, 316, 92, 112) + _r(486, 318, 16, 16, "fu2") + _r(598, 318, 16, 16, "fu2")
    b += _bed(660, 338, 72, 100) + _r(740, 340, 16, 16, "fu2")
    b += _r(500, 456, 90, 6, "gl") + _r(650, 456, 90, 6, "gl")
    # Murs (avec ouvertures)
    b += _walls((130, 80, 770, 80), (130, 80, 130, 460), (130, 460, 410, 460), (450, 460, 770, 460),
                (770, 80, 770, 296), (770, 342, 770, 460))
    b += "".join(_l(*s) for s in [(470, 80, 470, 150), (470, 204, 470, 318), (470, 372, 470, 460),
                                  (470, 250, 540, 250), (580, 250, 690, 250), (730, 250, 770, 250), (620, 250, 620, 460)])
    b += _t(150, 450, "SALON · 6,8 × 7,6 M") + _t(786, 410, "SPA")
    return _frame(b, "CHALET")


def _plan_entreprise():
    b = ""
    # Stationnement
    b += _r(40, 430, 920, 155, "fl")
    for x in range(80, 941, 54):
        b += _l(x, 440, x, 500, "fu2")
    b += _l(60, 545, 940, 545, "fu3 dash")
    for x, y in [(94, 450), (202, 450), (256, 450), (418, 450), (580, 450), (742, 450), (850, 450)]:
        b += _r(x, y, 32, 44, "fu", 10)
    b += "".join(_c(x, 515, 5, "fu") for x in (150, 380, 610, 840))
    # Bâtiment
    b += _r(60, 50, 880, 360, "fl")
    # Accueil : comptoir courbe, salon d’attente, portes vitrées
    b += _p("M140,178 Q190,110 240,178", "fu thick") + _c(110, 88, 14, "fu") + _c(150, 88, 14, "fu") + _r(98, 106, 66, 18, "fu2", 6)
    b += _c(270, 76, 12, "tr") + _r(56, 108, 8, 64, "gl")
    # Salle de réunion
    b += _r(100, 292, 160, 60, "fu", 22) + _r(64, 300, 6, 44, "gl")
    b += "".join(_c(x, 282, 7, "fu2") + _c(x, 362, 7, "fu2") for x in range(118, 248, 26))
    # Bureaux : deux rangées
    for y0 in (96, 276):
        for x in range(330, 620, 48):
            b += _r(x, y0, 40, 24, "fu", 3) + _r(x, y0 + 30, 40, 24, "fu", 3) + _c(x + 20, y0 - 8, 6, "fu2") + _c(x + 20, y0 + 62, 6, "fu2")
    b += _l(320, 214, 630, 214, "fu3 dash")
    # Entrepôt : rayonnages et quais de chargement
    for i in range(5):
        b += _r(676, 80 + i * 66, 234, 22, "fu")
        b += "".join(_l(x, 80 + i * 66, x, 102 + i * 66, "fu2") for x in range(704, 910, 30))
    for y in (110, 220, 330):
        b += _r(940, y, 16, 48, "fu2 dash")
    # Murs
    b += _walls((60, 50, 940, 50), (60, 50, 60, 106), (60, 174, 60, 410), (60, 410, 456, 410), (504, 410, 940, 410),
                (940, 50, 940, 106), (940, 162, 940, 216), (940, 272, 940, 326), (940, 382, 940, 410))
    b += "".join(_l(*s) for s in [(300, 50, 300, 120), (300, 166, 300, 296), (300, 342, 300, 410), (60, 230, 196, 230),
                                  (244, 230, 300, 230), (650, 50, 650, 226), (650, 296, 650, 410)])
    # Issues de secours (pictogrammes)
    b += "".join(_r(x - 7, y - 4, 14, 8, "ex", 2) for x, y in [(68, 140), (932, 392), (480, 404)])
    b += _t(80, 425, "ISSUES DE SECOURS : ÉCLAIRAGE PERMANENT") + _t(670, 400, "ENTREPÔT · 9 M SOUS PLAFOND")
    return _frame(b, "ENTREPRISE")


def _plan_garage():
    b = ""
    b += _r(40, 460, 920, 125, "fl")
    for x in range(100, 580, 40):
        b += _l(x, 462, x - 30, 585, "fu3")
    b += _tree(900, 520, 26) + _tree(820, 560, 18) + _r(620, 486, 150, 36, "fu2", 8)
    b += _r(70, 60, 860, 390, "fl")
    # Baies et voitures
    b += _l(330, 70, 330, 440, "fu3 dash")
    b += _car(150, 112, 104, 250) + _car(410, 112, 100, 250, sport=True)
    # Atelier : servantes, pont élévateur, plafonniers hexagonaux
    b += "".join(_r(x, 68, 50, 30, "fu", 3) for x in range(600, 900, 58))
    b += _r(640, 150, 12, 120, "fu") + _r(830, 150, 12, 120, "fu") + _l(652, 180, 830, 180, "fu2") + _l(652, 240, 830, 240, "fu2")
    for cx, cy in [(680, 140), (800, 140), (740, 240), (860, 240)]:
        pts = " ".join(f"{cx + 34 * dx},{cy + 34 * dy}" for dx, dy in
                       [(1, 0), (.5, .866), (-.5, .866), (-1, 0), (-.5, -.866), (.5, -.866)])
        b += f'<polygon class="lp" points="{pts}"/>'
    b += _l(590, 320, 930, 320, "fu3 dash")
    # Établi
    b += _r(608, 404, 304, 34, "fu", 3) + _r(608, 444, 304, 4, "gl") + _c(650, 378, 10, "fu2") + _r(860, 408, 26, 26, "fu2", 4)
    # Murs et portes de garage
    b += _walls((70, 60, 930, 60), (70, 60, 70, 450), (930, 60, 930, 450), (70, 450, 96, 450), (304, 450, 356, 450),
                (564, 450, 930, 450))
    b += _l(96, 452, 304, 452, "fu2 dash") + _l(356, 452, 564, 452, "fu2 dash")
    b += _l(590, 60, 590, 196, "w2") + _l(590, 262, 590, 450, "w2")
    b += _t(90, 80, "BAIE 1") + _t(350, 80, "BAIE 2") + _t(612, 312, "ATELIER · 4,5 M")
    return _frame(b, "GARAGE")


def _plan_ferme():
    b = ""
    # Cour : gravier, abreuvoir, silos, arbres
    b += _r(320, 318, 640, 266, "fl")
    b += _p("M330,560 Q560,300 940,340", "fu3 dash") + _r(520, 520, 90, 20, "fu", 6)
    b += _c(900, 380, 30, "fu") + _c(900, 380, 22, "fu2") + _c(900, 460, 30, "fu") + _c(900, 460, 22, "fu2")
    b += _tree(380, 360, 26) + _tree(760, 560, 22) + _tree(40, 300, 22) + _tree(980, 560, 18)
    # Maison
    b += _r(60, 60, 240, 190, "fl") + _r(60, 250, 240, 26, "fu2 dash")
    b += _r(84, 90, 90, 56, "fu", 6) + "".join(_c(x, 82, 6, "fu2") + _c(x, 154, 6, "fu2") for x in (100, 128, 156))
    b += _bed(214, 170, 68, 66) + _r(196, 74, 92, 22, "fu")
    # Étable : allée centrale et stalles
    b += _r(370, 60, 320, 240, "fl")
    b += "".join(_l(x, 64, x, 160, "fu2") + _l(x, 200, x, 296, "fu2") for x in range(410, 690, 40))
    b += _l(372, 172, 688, 172, "fu3 dash") + _l(372, 188, 688, 188, "fu3 dash")
    # Grange : balles de foin, grandes portes
    b += _r(720, 60, 220, 240, "fl")
    b += "".join(_r(x, y, 46, 30, "fu", 10) for x in (740, 792, 844) for y in (80, 116))
    b += _r(740, 196, 100, 70, "fu2", 6) + _l(760, 300, 900, 300, "fu2 dash")
    # Serre : vitrage et planches de culture
    b += _r(60, 330, 240, 230, "fl")
    b += "".join(_l(x, 332, x, 558, "gl2") for x in range(80, 300, 20))
    b += "".join(_r(78, y, 204, 18, "fu", 3) for y in (350, 392, 434, 476, 518))
    # Murs
    b += _walls((60, 60, 300, 60), (60, 60, 60, 250), (300, 60, 300, 250), (60, 250, 160, 250), (200, 250, 300, 250),
                (370, 60, 690, 60), (370, 60, 370, 300), (690, 60, 690, 300), (370, 300, 500, 300), (560, 300, 690, 300),
                (720, 60, 940, 60), (720, 60, 720, 300), (940, 60, 940, 300), (720, 300, 760, 300), (900, 300, 940, 300))
    b += f'<rect class="w" x="60" y="330" width="240" height="230" fill="none"/>' + _l(180, 60, 180, 160, "w2")
    b += _t(384, 314, "ÉTABLE · 24 STALLES") + _t(76, 574, "SERRE · CYCLE 16 H")
    return _frame(b, "FERME")


def _plan_bateau():
    b = ""
    # Eau : quelques rides
    for y, x0 in [(90, 120), (130, 520), (510, 200), (540, 640), (470, 860), (110, 840)]:
        b += _p(f"M{x0},{y} q20,-8 40,0 t40,0 t40,0", "wv")
    hull = "M80,175 L600,160 C760,160 880,220 940,300 C880,380 760,440 600,440 L80,425 Q66,300 80,175 Z"
    b += _p(hull, "fl") + _p(hull, "w")
    b += _p("M100,192 L600,180 C745,180 850,232 905,300 C850,368 745,420 600,420 L100,408 Q90,300 100,192 Z", "w2")
    b += _r(54, 232, 26, 136, "fu2", 4)
    for y in range(240, 368, 12):
        b += _l(56, y, 78, y, "fu3")
    # Cockpit : barre à roue, banquettes en U
    b += _p("M112,214 L290,212 L290,236 L136,238 L136,362 L290,364 L290,388 L112,386 Z", "fu")
    b += _c(250, 300, 28, "fu2") + "".join(_l(250, 300, 250 + 28 * dx, 300 + 28 * dy, "fu2")
                                         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    # Rouf : carré et cabine avant
    b += _p("M300,215 L700,210 C760,215 805,255 820,300 C805,345 760,385 700,390 L300,385 Z", "w2")
    b += _r(400, 270, 92, 60, "fu", 12) + _p("M360,236 L380,236 L380,364 L540,364 L540,348 L396,348 L396,252 L540,252 L540,236", "fu")
    b += _r(320, 222, 34, 40, "fu") + _r(326, 230, 22, 16, "fu2", 3)
    b += _l(600, 214, 600, 386, "w2")
    b += _p("M620,244 L752,252 C786,268 798,290 798,300 C798,310 786,332 752,348 L620,356 Z", "fu")
    b += _r(628, 262, 30, 28, "fu2", 6) + _r(628, 310, 30, 28, "fu2", 6)
    # Mât et bôme
    b += _c(560, 300, 9, "fu") + _l(560, 300, 270, 300, "fu2 dash")
    b += _t(110, 452, "LONGUEUR 13,7 M · BAU 4,2 M") + _t(780, 470, "TRIBORD", "middle") + _t(780, 140, "BÂBORD", "middle")
    return _frame(b, "VOILIER")


def _plan_avion():
    b = ""
    b += _r(40, 40, 920, 520, "fl")
    # Marquage au sol et équipements du hangar
    b += _l(100, 300, 960, 300, "fu3 dash") + _c(860, 300, 60, "fu3 dash")
    b += "".join(_r(x, 52, 70, 26, "fu", 3) for x in (90, 180, 270)) + _r(820, 470, 80, 46, "fu", 6) + _r(90, 480, 110, 40, "fu2", 4)
    # Avion d’affaires, nez vers la droite
    b += _p("M500,282 L432,92 L470,92 L604,280 Z", "fu") + _p("M500,318 L432,508 L470,508 L604,320 Z", "fu")
    b += _p("M236,286 L190,210 L216,210 L296,285 Z", "fu") + _p("M236,314 L190,390 L216,390 L296,315 Z", "fu")
    b += _r(268, 256, 74, 22, "fu", 11) + _r(268, 322, 74, 22, "fu", 11)
    fus = ("M210,282 L800,278 C850,280 885,290 905,300 C885,310 850,320 800,322 L210,318 "
           "C190,312 182,306 180,300 C182,294 190,288 210,282 Z")
    b += _p(fus, "fl2") + _p(fus, "w2")
    b += "".join(_r(x, 285, 18, 11, "fu2", 3) + _r(x, 304, 18, 11, "fu2", 3) for x in range(400, 760, 44))
    b += _l(780, 281, 780, 319, "fu2") + _r(800, 290, 26, 8, "fu2", 2) + _r(800, 302, 26, 8, "fu2", 2)
    # Murs et portes du hangar
    b += _walls((40, 40, 960, 40), (40, 40, 40, 560), (960, 40, 960, 560), (40, 560, 90, 560), (910, 560, 960, 560))
    b += _l(90, 562, 910, 562, "fu2 dash")
    b += _t(60, 548, "HANGAR 2 · PORTES 34 M") + _t(470, 84, "BÂBORD", "middle") + _t(470, 528, "TRIBORD", "middle")
    return _frame(b, "HANGAR")


# ---------------------------------------------------------------------------------------------
# Environnements
#   zones : k, name, ic (icône), lab (étiquette sur le plan), poly, tag (sous-titre), out (rangée
#           extérieure sur l’accueil), group (libellés quand la zone a plusieurs lumières).
#   lights : k, name, zone, kind (rgb = couleur, blanc = blanc réglable, fixe = blanc fixe,
#            regl = réglementaire, jamais touché), fx/st/dk, cap (plafond, raison), fixed (raison).
#   state : lumière → [allumée, ambiance, niveau %]
# ---------------------------------------------------------------------------------------------
def _box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


GROUP_BANDES = {"together": "Les deux bandes ensemble", "same": "Même lumière, des deux côtés.",
                "apart": "Les deux bandes sont indépendantes.", "short": "2 bandes"}


def _group(n_word, noun, same, short=None):
    return {"together": f"Les {n_word} {noun} ensemble", "same": same,
            "apart": f"Les {n_word} {noun} sont indépendantes.", "short": short or "2 lumières"}


BOULANCE = {
    "name": "BouLance", "kind": "VR", "word": "le VR", "main": "couloir",
    "plan": {"type": "vr", "w": 1536, "h": 1024, "view": [0, 196, 1536, 620],
             "imgs": {"chaleur": "/media/vr/plan-chaleur.webp", "ocean": "/media/vr/plan-ocean.webp",
                      "signature": "/media/vr/plan-signature.webp"},
             # Couleur déjà présente dans chaque photo du plan, par lumière
             "baked": {"chaleur": {"couloir-g": "ambre", "couloir-d": "ambre", "cuisine": "ambre", "chambre": "violet"},
                       "ocean": {"couloir-g": "bleu", "couloir-d": "bleu", "cuisine": "ambre", "chambre": "violet"},
                       "signature": {"couloir-g": "ambre", "couloir-d": "ambre", "cuisine": "ambre", "chambre": "ambre"}}},
    "zones": [
        {"k": "couloir", "name": "Couloir", "ic": "strip", "lab": [818, 488], "poly": _box(540, 420, 1075, 570),
         "tag": "Votre passage en douceur", "tagApart": "Chaque côté, à votre façon", "group": GROUP_BANDES,
         "photo": "amb", "titleApart": "Deux côtés. Votre équilibre.", "capApart": "Un peu plus ici, un peu moins là."},
        {"k": "cuisine", "name": "Cuisine", "ic": "cook", "lab": [760, 360], "poly": _box(515, 250, 985, 435),
         "tag": "Le plan de travail, bien éclairé", "photo": "cuisine", "baked": "ambre",
         "ov": [[36, 18, 100, 30]]},
        {"k": "chambre", "name": "Chambre", "ic": "bed", "lab": [1236, 470], "poly": _box(1085, 262, 1390, 668),
         "tag": "Le repos, à votre rythme", "photo": "chambre", "baked": "violet", "ov": [[10, 16, 60, 28]]},
        {"k": "exterieur", "name": "Extérieur", "ic": "out", "lab": [1250, 742], "poly": _box(380, 690, 1420, 790),
         "tag": "À la belle étoile", "photo": "exterieur", "baked": "off", "out": True, "ov": [[12, 66, 70, 96]]},
    ],
    "lights": [
        {"k": "couloir-g", "name": "Couloir · gauche", "short": "Bande gauche", "zone": "couloir", "kind": "rgb",
         "st": [[574, 447, 1054, 447]], "dk": [[815, 447, 260, 26]], "fl": [[815, 470, 250, 34]]},
        {"k": "couloir-d", "name": "Couloir · droite", "short": "Bande droite", "zone": "couloir", "kind": "rgb",
         "st": [[566, 540, 1054, 540]], "dk": [[812, 540, 265, 26]], "fl": [[812, 518, 250, 34]]},
        {"k": "cuisine", "name": "Cuisine", "zone": "cuisine", "kind": "rgb",
         "st": [[540, 296, 850, 296]], "fx": [[883, 303, 46], [640, 330, 110], [790, 320, 90]],
         "dk": [[740, 330, 250, 95]]},
        {"k": "chambre", "name": "Chambre", "zone": "chambre", "kind": "rgb",
         "st": [[1100, 288, 1372, 288], [1100, 652, 1372, 652], [1100, 300, 1100, 640]], "fx": [[1236, 470, 150]],
         "dk": [[1236, 465, 170, 215]]},
        {"k": "exterieur", "name": "Extérieur", "zone": "exterieur", "kind": "blanc",
         "fx": [[600, 742, 130], [860, 748, 140], [1120, 742, 120], [1395, 712, 60]]},
    ],
    "state": {"couloir-g": [1, "heure-doree", 70], "couloir-d": [1, "heure-doree", 35], "cuisine": [1, "lecture", 90],
              "chambre": [1, "cinema", 25], "exterieur": [0, "heure-doree", 60]},
    "configs": [
        {"k": "soiree-douce", "name": "Soirée douce", "fav": True,
         "lights": {"couloir-g": [1, "ocean", 54], "couloir-d": [1, "ocean", 54], "cuisine": [1, "lecture", 90],
                    "chambre": [1, "cinema", 15], "exterieur": [0, "heure-doree", 60]}},
        {"k": "au-chaud", "name": "Au chaud", "fav": True,
         "lights": {"couloir-g": [1, "heure-doree", 70], "couloir-d": [1, "heure-doree", 70], "cuisine": [1, "heure-doree", 60],
                    "chambre": [1, "heure-doree", 40], "exterieur": [0, "heure-doree", 60]}},
        {"k": "passage-nuit", "name": "Le passage de nuit", "fav": False,
         "lights": {"couloir-g": [1, "nuit-douce", 15], "couloir-d": [1, "nuit-douce", 15], "cuisine": [0, "lecture", 90],
                    "chambre": [1, "nuit-douce", 10], "exterieur": [0, "heure-doree", 60]}},
    ],
    # Cas de connexion interrompue du dossier (page 12) : la première application de Signature
    # laisse la bande droite sans confirmation; « Réessayer » réussit.
    "failOnce": {"amb": "signature", "light": "couloir-d"},
}


def _maison():
    labels = {"chambre": (900, 292), "sdb": (1078, 392)}
    icons = {"salon": "sofa", "cuisine": "cook", "chambre": "bed", "sdb": "bath", "bureau": "desk", "entree": "door",
             "garage": "car", "terrasse": "fire", "piscine": "pool", "exterieur": "out"}
    tags = {"salon": "Le cœur de la maison", "cuisine": "Le plan de travail, bien éclairé", "chambre": "Le repos, à votre rythme",
            "sdb": "Une lumière franche le matin", "bureau": "Concentré, sans fatigue", "entree": "L’accueil, dès la porte",
            "garage": "Pratique avant tout", "terrasse": "Les soirées dehors", "piscine": "L’eau, la nuit",
            "exterieur": "Le jardin et les allées"}
    kinds = {"salon": "rgb", "cuisine": "blanc", "chambre": "rgb", "sdb": "blanc", "bureau": "blanc", "entree": "blanc",
             "garage": "fixe", "terrasse": "blanc", "piscine": "rgb", "exterieur": "blanc"}
    zones, lights = [], []
    for k, n, poly, _w, _e in MZ_ROOMS:
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        lab = labels.get(k, ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
        zones.append({"k": k, "name": n, "ic": icons[k], "lab": list(lab), "poly": poly, "tag": tags[k],
                      "out": k in ("terrasse", "piscine", "exterieur")})
        light = {"k": k, "name": n, "zone": k, "kind": kinds[k], "fx": [[f[0], f[1], f[2]] for f in MZ_LUMIERE[k]["f"] if f[3] != 3]}
        if k == "garage":
            light["kv"] = 4000
        lights.append(light)
    state = {"salon": [1, "heure-doree", 60], "cuisine": [1, "lecture", 70], "chambre": [0, "nuit-douce", 20],
             "sdb": [0, "lecture", 80], "bureau": [1, "lecture", 80], "entree": [1, "heure-doree", 40],
             "garage": [0, "lecture", 100], "terrasse": [1, "heure-doree", 70], "piscine": [1, "ocean", 80],
             "exterieur": [1, "heure-doree", 55]}
    return {
        "name": "Ma maison", "kind": "Maison", "word": "la maison", "main": "salon",
        "plan": {"type": "photo", "w": MZ_W, "h": MZ_H, "view": [0, 0, MZ_W, MZ_H],
                 "img": "/media/solutions/jarvis-spaces-property-v3.webp"},
        "zones": zones, "lights": lights, "state": state,
        "configs": [
            {"k": "souper", "name": "Souper entre amis", "fav": True,
             "lights": {**{k: [0, "lecture", 60] for k in state}, "salon": [1, "heure-doree", 55], "cuisine": [1, "heure-doree", 70],
                        "entree": [1, "heure-doree", 40], "terrasse": [1, "heure-doree", 70], "piscine": [1, "ocean", 70],
                        "exterieur": [1, "heure-doree", 55]}},
            {"k": "film", "name": "Soirée film", "fav": False,
             "lights": {**{k: [0, "lecture", 60] for k in state}, "salon": [1, "cinema", 20], "entree": [1, "nuit-douce", 10],
                        "exterieur": [1, "nuit-douce", 20]}},
        ],
    }


def _env(name, kind, word, main, svg, zones, lights, state, configs):
    return {"name": name, "kind": kind, "word": word, "main": main,
            "plan": {"type": "svg", "w": 1000, "h": 600, "view": [0, 0, 1000, 600], "svg": svg},
            "zones": zones, "lights": lights, "state": state, "configs": configs}


def _off(state, **on):
    """Configuration : tout éteint sauf les lumières nommées (clés avec « _ » pour « - »)."""
    out = {k: [0, v[1], v[2]] for k, v in state.items()}
    for k, v in on.items():
        out[k.replace("_", "-")] = v
    return out


CHALET_STATE = {"salon": [1, "heure-doree", 65], "foyer": [1, "heure-doree", 80], "cuisine": [1, "lecture", 85],
                "ch-1": [0, "nuit-douce", 20], "ch-2": [0, "nuit-douce", 20], "spa": [1, "ocean", 70],
                "terrasse": [1, "heure-doree", 50]}
CHALET = _env(
    "Le chalet", "Chalet", "le chalet", "salon", _plan_chalet(),
    [
        {"k": "salon", "name": "Grand salon et foyer", "short": "Grand salon", "ic": "fire", "lab": [300, 136],
         "poly": _box(130, 80, 470, 460), "tag": "Le feu, la vue, la soirée",
         "group": _group("deux", "lumières", "Même ambiance au plafond et autour du foyer.")},
        {"k": "cuisine", "name": "Cuisine", "ic": "cook", "lab": [620, 140], "poly": _box(470, 80, 770, 250),
         "tag": "Le plan de travail, bien éclairé"},
        {"k": "chambres", "name": "Chambres", "ic": "bed", "lab": [620, 290], "poly": _box(470, 250, 770, 460),
         "tag": "Le repos, chacun à son rythme", "group": _group("deux", "chambres", "Même lumière dans les deux chambres.")},
        {"k": "spa", "name": "Spa", "ic": "spa", "lab": [860, 196], "poly": _box(770, 150, 950, 420),
         "tag": "L’eau chaude sous les étoiles", "out": True},
        {"k": "exterieur", "name": "Extérieur", "ic": "out", "lab": [620, 540], "poly": _box(40, 462, 960, 580),
         "tag": "La terrasse et le sentier", "out": True},
    ],
    [
        {"k": "salon", "name": "Grand salon", "zone": "salon", "kind": "blanc",
         "fx": [[300, 180, 150], [250, 330, 130], [410, 380, 90]]},
        {"k": "foyer", "name": "Foyer · accent", "short": "Foyer", "zone": "salon", "kind": "rgb",
         "st": [[160, 220, 160, 300]], "fx": [[176, 260, 70]]},
        {"k": "cuisine", "name": "Cuisine", "zone": "cuisine", "kind": "rgb",
         "st": [[486, 118, 758, 118]], "fx": [[580, 182, 60], [662, 182, 60]]},
        {"k": "ch-1", "name": "Chambre principale", "short": "Principale", "zone": "chambres", "kind": "rgb",
         "st": [[504, 312, 596, 312]], "fx": [[548, 360, 80]]},
        {"k": "ch-2", "name": "Chambre d’amis", "short": "Amis", "zone": "chambres", "kind": "blanc",
         "fx": [[696, 380, 72]]},
        {"k": "spa", "name": "Spa", "zone": "spa", "kind": "rgb", "fx": [[860, 285, 70], [860, 285, 40]]},
        {"k": "terrasse", "name": "Terrasse et sentier", "short": "Terrasse", "zone": "exterieur", "kind": "blanc",
         "fx": [[200, 494, 46], [330, 494, 46], [460, 494, 46], [600, 494, 46], [730, 494, 46], [462, 548, 30], [484, 588, 28]]},
    ],
    CHALET_STATE,
    [
        {"k": "apres-ski", "name": "Après-ski", "fav": True,
         "lights": {**CHALET_STATE, "salon": [1, "heure-doree", 55], "foyer": [1, "heure-doree", 90], "spa": [1, "aurore", 70]}},
        {"k": "nuit-chalet", "name": "Bonne nuit au chalet", "fav": False,
         "lights": _off(CHALET_STATE, foyer=[1, "nuit-douce", 15], terrasse=[1, "nuit-douce", 15])},
    ],
)

ENTREPRISE_STATE = {"accueil": [1, "heure-doree", 70], "issues": [1, "secours", 100], "reunion": [0, "lecture", 90],
                    "bureaux-n": [1, "lecture", 85], "bureaux-s": [1, "lecture", 85], "entrepot": [1, "lecture", 80],
                    "parking": [1, "lecture", 70]}
ENTREPRISE = _env(
    "Les bureaux", "Entreprise", "l’entreprise", "bureaux", _plan_entreprise(),
    [
        {"k": "bureaux", "name": "Bureaux", "ic": "desk", "lab": [476, 214], "poly": _box(300, 50, 650, 410),
         "tag": "Concentré, sans fatigue", "group": _group("deux", "rangées", "Même lumière sur les deux rangées.", "2 rangées")},
        {"k": "accueil", "name": "Accueil", "ic": "door", "lab": [180, 206], "poly": _box(60, 50, 300, 230),
         "tag": "La première impression"},
        {"k": "reunion", "name": "Salle de réunion", "short": "Réunion", "ic": "meet", "lab": [180, 260],
         "poly": _box(60, 230, 300, 410), "tag": "Des visages bien éclairés"},
        {"k": "entrepot", "name": "Entrepôt", "ic": "box", "lab": [796, 230], "poly": _box(650, 50, 940, 410),
         "tag": "Sécurité et visibilité"},
        {"k": "stationnement", "name": "Stationnement", "ic": "park", "lab": [500, 545], "poly": _box(40, 430, 960, 585),
         "tag": "Du coucher au lever du soleil", "out": True},
    ],
    [
        {"k": "bureaux-n", "name": "Bureaux · nord", "short": "Rangée nord", "zone": "bureaux", "kind": "blanc",
         "fx": [[400, 126, 96], [560, 126, 96]]},
        {"k": "bureaux-s", "name": "Bureaux · sud", "short": "Rangée sud", "zone": "bureaux", "kind": "blanc",
         "fx": [[400, 306, 96], [560, 306, 96]]},
        {"k": "accueil", "name": "Accueil", "zone": "accueil", "kind": "rgb",
         "st": [[146, 172, 236, 172]], "fx": [[190, 140, 110]]},
        {"k": "issues", "name": "Issues de secours", "zone": "accueil", "kind": "regl",
         "fx": [[68, 140, 24, "#39d98a"], [932, 392, 24, "#39d98a"], [480, 404, 24, "#39d98a"]],
         "mode": "Permanent",
         "fixed": "Éclairage de sécurité exigé par le Code : toujours allumé, jamais modifié par une ambiance ni par « Tout éteindre »."},
        {"k": "reunion", "name": "Salle de réunion", "short": "Réunion", "zone": "reunion", "kind": "blanc",
         "st": [[110, 322, 250, 322]], "fx": [[180, 322, 110]]},
        {"k": "entrepot", "name": "Entrepôt", "zone": "entrepot", "kind": "fixe", "kv": 5000,
         "fx": [[730, 110, 80], [860, 110, 80], [730, 240, 80], [860, 240, 80], [730, 370, 70], [860, 370, 70]]},
        {"k": "parking", "name": "Stationnement", "zone": "stationnement", "kind": "fixe", "kv": 4000,
         "fx": [[150, 515, 80], [380, 515, 80], [610, 515, 80], [840, 515, 80]]},
    ],
    ENTREPRISE_STATE,
    [
        {"k": "ouverture", "name": "Ouverture des bureaux", "fav": True,
         "lights": {**ENTREPRISE_STATE, "reunion": [1, "lecture", 90]}},
        {"k": "fermeture", "name": "Fermeture", "fav": False,
         "lights": _off(ENTREPRISE_STATE, accueil=[1, "nuit-douce", 20], parking=[1, "lecture", 70])},
    ],
)

GARAGE_STATE = {"atelier": [1, "lecture", 90], "etabli": [1, "lecture", 100], "baie-1": [1, "signature", 70],
                "baie-2": [1, "ocean", 60], "exterieur": [0, "heure-doree", 60]}
GARAGE = _env(
    "Le garage", "Garage", "le garage", "atelier", _plan_garage(),
    [
        {"k": "atelier", "name": "Atelier", "ic": "tool", "lab": [760, 290], "poly": _box(590, 60, 930, 320),
         "tag": "Voir chaque détail"},
        {"k": "etabli", "name": "Établi", "ic": "tool", "lab": [760, 372], "poly": _box(590, 320, 930, 450),
         "tag": "Une lumière franche, sans ombre"},
        {"k": "baie-1", "name": "Baie 1", "ic": "car", "lab": [200, 400], "poly": _box(70, 60, 330, 450),
         "tag": "La voiture en vitrine"},
        {"k": "baie-2", "name": "Baie 2", "ic": "car", "lab": [460, 400], "poly": _box(330, 60, 590, 450),
         "tag": "La voiture en vitrine"},
        {"k": "exterieur", "name": "Extérieur", "ic": "out", "lab": [330, 530], "poly": _box(40, 460, 960, 585),
         "tag": "L’entrée et l’allée", "out": True},
    ],
    [
        {"k": "atelier", "name": "Atelier", "zone": "atelier", "kind": "blanc",
         "fx": [[680, 140, 90], [800, 140, 90], [740, 240, 90], [860, 240, 90]]},
        {"k": "etabli", "name": "Établi", "zone": "etabli", "kind": "blanc", "st": [[612, 400, 908, 400]], "fx": [[760, 404, 70]]},
        {"k": "baie-1", "name": "Baie 1", "zone": "baie-1", "kind": "rgb",
         "st": [[100, 90, 100, 420], [300, 90, 300, 420]], "fx": [[200, 240, 120]]},
        {"k": "baie-2", "name": "Baie 2", "zone": "baie-2", "kind": "rgb",
         "st": [[360, 90, 360, 420], [560, 90, 560, 420]], "fx": [[460, 240, 120]]},
        {"k": "exterieur", "name": "Extérieur", "zone": "exterieur", "kind": "blanc",
         "fx": [[120, 472, 56], [330, 472, 56], [560, 472, 56], [760, 472, 56]]},
    ],
    GARAGE_STATE,
    [
        {"k": "vitrine", "name": "Vitrine du soir", "fav": True,
         "lights": {**GARAGE_STATE, "atelier": [0, "lecture", 90], "etabli": [0, "lecture", 100], "baie-1": [1, "aurore", 70],
                    "baie-2": [1, "aurore", 70], "exterieur": [1, "heure-doree", 50]}},
        {"k": "travail", "name": "Travail mécanique", "fav": False,
         "lights": {**GARAGE_STATE, "baie-1": [1, "lecture", 100], "baie-2": [1, "lecture", 100]}},
    ],
)

FERME_STATE = {"maison": [1, "heure-doree", 70], "etable": [1, "heure-doree", 30], "grange": [0, "lecture", 80],
               "serre": [1, "culture", 100], "cour": [1, "heure-doree", 60]}
FERME = _env(
    "La ferme", "Ferme", "la ferme", "maison", _plan_ferme(),
    [
        {"k": "maison", "name": "Maison", "ic": "sofa", "lab": [180, 220], "poly": _box(60, 60, 300, 250),
         "tag": "La maison de ferme"},
        {"k": "etable", "name": "Étable", "ic": "barn", "lab": [530, 270], "poly": _box(370, 60, 690, 300),
         "tag": "Le calme pour les animaux"},
        {"k": "grange", "name": "Grange", "ic": "barn", "lab": [830, 270], "poly": _box(720, 60, 940, 300),
         "tag": "Le foin et la machinerie"},
        {"k": "serre", "name": "Serre", "ic": "plant", "lab": [180, 336], "poly": _box(60, 330, 300, 560),
         "tag": "Le cycle de croissance"},
        {"k": "cour", "name": "Cour", "ic": "out", "lab": [640, 420], "poly": _box(320, 318, 960, 584),
         "tag": "Les allées et la cour", "out": True},
    ],
    [
        {"k": "maison", "name": "Maison", "zone": "maison", "kind": "rgb", "fx": [[130, 130, 90], [240, 160, 70]]},
        {"k": "etable", "name": "Étable", "zone": "etable", "kind": "blanc",
         "fx": [[430, 180, 70], [530, 180, 70], [630, 180, 70]],
         "cap": [40, "Animaux au repos : 40 % au maximum le soir et la nuit."]},
        {"k": "grange", "name": "Grange", "zone": "grange", "kind": "fixe", "kv": 3500, "fx": [[830, 170, 110]]},
        {"k": "serre", "name": "Serre", "zone": "serre", "kind": "regl", "fx": [[180, 445, 130, "#ff5cd6"], [180, 445, 70, "#ff5cd6"]],
         "mode": "Programme de culture",
         "fixed": "Lampes de croissance commandées par le programme de culture (16 h par jour) : une ambiance ne les change jamais."},
        {"k": "cour", "name": "Cour", "zone": "cour", "kind": "blanc", "fx": [[450, 400, 90], [640, 470, 90], [820, 520, 80]]},
    ],
    FERME_STATE,
    [
        {"k": "traite", "name": "Traite du matin", "fav": True,
         "lights": {**FERME_STATE, "etable": [1, "lecture", 40], "grange": [1, "lecture", 80], "cour": [1, "lecture", 80]}},
        {"k": "nuit-ferme", "name": "Nuit à la ferme", "fav": False,
         "lights": {**FERME_STATE, "maison": [0, "heure-doree", 70], "etable": [1, "nuit-douce", 10], "cour": [1, "nuit-douce", 20]}},
    ],
)

BATEAU_STATE = {"carre": [1, "heure-doree", 60], "cabine": [0, "nuit-douce", 20], "cockpit": [1, "heure-doree", 40],
                "pont": [0, "heure-doree", 40], "feux": [1, "navigation", 100]}
BATEAU = _env(
    "Le voilier", "Bateau", "le bateau", "carre", _plan_bateau(),
    [
        {"k": "carre", "name": "Carré", "ic": "sofa", "lab": [446, 240], "poly": _box(300, 212, 600, 388),
         "tag": "La table et la cuisine de bord"},
        {"k": "cabine", "name": "Cabine avant", "ic": "bed", "lab": [702, 300], "poly": _box(600, 230, 820, 370),
         "tag": "La couchette, à l’avant"},
        {"k": "cockpit", "name": "Cockpit", "ic": "wheel", "lab": [196, 300], "poly": _box(100, 205, 300, 395),
         "tag": "La barre et les banquettes"},
        {"k": "pont", "name": "Pont", "ic": "boat", "lab": [450, 158], "poly": _box(80, 160, 940, 440),
         "tag": "Circuler à bord, la nuit", "out": True},
        {"k": "feux", "name": "Feux de navigation", "ic": "nav", "lab": [830, 470], "poly": _box(720, 180, 950, 420),
         "tag": "Réglementaires · jamais modifiés", "out": True},
    ],
    [
        {"k": "carre", "name": "Carré", "zone": "carre", "kind": "rgb",
         "st": [[310, 226, 590, 224], [310, 376, 590, 378]], "fx": [[446, 300, 100]]},
        {"k": "cabine", "name": "Cabine avant", "zone": "cabine", "kind": "rgb", "st": [[630, 248, 750, 255]], "fx": [[700, 300, 80]]},
        {"k": "cockpit", "name": "Cockpit", "zone": "cockpit", "kind": "blanc", "fx": [[200, 300, 90]]},
        {"k": "pont", "name": "Pont", "zone": "pont", "kind": "blanc",
         "fx": [[150, 194, 26], [300, 189, 26], [450, 185, 26], [600, 181, 26], [150, 406, 26], [300, 410, 26],
                [450, 414, 26], [600, 418, 26]]},
        {"k": "feux", "name": "Feux de navigation", "zone": "feux", "kind": "regl",
         "fx": [[842, 214, 40, "#ff3b3b"], [842, 386, 40, "#2fe07a"], [74, 300, 34, "#ffffff"], [560, 300, 28, "#ffffff"]],
         "mode": "Navigation",
         "fixed": "Ils montrent votre position et votre route aux autres bateaux (règlement sur les abordages) : "
                  "seul le tableau de navigation les commande, jamais une ambiance."},
    ],
    BATEAU_STATE,
    [
        {"k": "mouillage", "name": "Soirée au mouillage", "fav": True,
         "lights": {**BATEAU_STATE, "carre": [1, "heure-doree", 50], "cockpit": [1, "heure-doree", 35], "pont": [1, "nuit-douce", 15]}},
        {"k": "quart", "name": "Quart de nuit", "fav": False,
         "lights": {**BATEAU_STATE, "carre": [1, "nuit-douce", 10], "cabine": [0, "nuit-douce", 10], "cockpit": [1, "nuit-douce", 10],
                    "pont": [0, "heure-doree", 40]}},
    ],
)

AVION_STATE = {"cabine": [1, "heure-doree", 60], "cockpit": [1, "lecture", 40], "hangar": [1, "lecture", 80],
               "anticol": [1, "anticollision", 100]}
AVION = _env(
    "L’avion", "Avion", "l’avion", "cabine", _plan_avion(),
    [
        {"k": "cabine", "name": "Cabine", "ic": "plane", "lab": [580, 252], "poly": _box(330, 276, 780, 324),
         "tag": "Le voyage, en douceur"},
        {"k": "cockpit", "name": "Poste de pilotage", "short": "Pilotage", "ic": "wheel", "lab": [860, 252],
         "poly": [(780, 276), (906, 300), (780, 324)], "tag": "Des instruments lisibles"},
        {"k": "hangar", "name": "Hangar", "ic": "box", "lab": [200, 150], "poly": _box(40, 40, 960, 560),
         "tag": "Préparer le vol"},
        {"k": "feux", "name": "Feux anticollision", "ic": "nav", "lab": [452, 540], "poly": _box(170, 80, 620, 520),
         "tag": "Réglementaires · non modifiables", "out": True},
    ],
    [
        {"k": "cabine", "name": "Cabine", "zone": "cabine", "kind": "rgb",
         "st": [[340, 289, 774, 287], [340, 311, 774, 313]], "fx": [[560, 300, 70]]},
        {"k": "cockpit", "name": "Poste de pilotage", "short": "Pilotage", "zone": "cockpit", "kind": "blanc",
         "fx": [[842, 300, 46]], "cap": [50, "Limité à 50 % : aucun éblouissement aux commandes."]},
        {"k": "hangar", "name": "Hangar", "zone": "hangar", "kind": "fixe", "kv": 5000,
         "fx": [[200, 140, 100], [500, 140, 100], [800, 140, 100], [200, 460, 100], [500, 460, 100], [800, 460, 100]]},
        {"k": "anticol", "name": "Feux anticollision", "zone": "feux", "kind": "regl", "strobe": True,
         "fx": [[451, 92, 44, "#ff3b3b"], [451, 508, 44, "#2fe07a"], [180, 300, 36, "#ffffff"], [560, 300, 30, "#ff3b3b"]],
         "mode": "Anticollision",
         "fixed": "Réglementaires : seul l’interrupteur du poste de pilotage les commande. Une ambiance ne les touche jamais."},
    ],
    AVION_STATE,
    [
        {"k": "embarquement", "name": "Embarquement", "fav": True,
         "lights": {**AVION_STATE, "cabine": [1, "lecture", 80], "hangar": [1, "lecture", 100]}},
        {"k": "vol-de-nuit", "name": "Vol de nuit", "fav": False,
         "lights": {**AVION_STATE, "cabine": [1, "nuit-douce", 15], "cockpit": [1, "cinema", 20], "hangar": [0, "lecture", 80]}},
    ],
)

ENVS = {
    "boulance": BOULANCE, "maison": _maison(), "chalet": CHALET, "entreprise": ENTREPRISE, "garage": GARAGE,
    "ferme": FERME, "bateau": BATEAU, "avion": AVION,
}


# Grammaire des phrases générées (« Océan dans le couloir. », « La bande droite ne répond pas. ») :
# article, préposition et genre (m, f, mp, fp) de chaque zone, puis des lumières qui ne portent pas
# le nom de leur zone.
ALL = {"boulance": "tout le VR", "maison": "toute la maison", "chalet": "tout le chalet", "entreprise": "toute l’entreprise",
       "garage": "tout le garage", "ferme": "toute la ferme", "bateau": "tout le bateau", "avion": "tout l’avion"}
ZTXT = {
    "boulance": {"couloir": ("le couloir", "dans le couloir", "m"), "cuisine": ("la cuisine", "en cuisine", "f"),
                 "chambre": ("la chambre", "dans la chambre", "f"), "exterieur": ("l’extérieur", "à l’extérieur", "m")},
    "maison": {"salon": ("le salon", "au salon", "m"), "cuisine": ("la cuisine", "en cuisine", "f"),
               "chambre": ("la chambre", "dans la chambre", "f"), "sdb": ("la salle de bain", "dans la salle de bain", "f"),
               "bureau": ("le bureau", "au bureau", "m"), "entree": ("l’entrée", "à l’entrée", "f"),
               "garage": ("le garage", "au garage", "m"), "terrasse": ("la terrasse", "sur la terrasse", "f"),
               "piscine": ("la piscine", "à la piscine", "f"), "exterieur": ("l’extérieur", "à l’extérieur", "m")},
    "chalet": {"salon": ("le grand salon", "au grand salon", "m"), "cuisine": ("la cuisine", "en cuisine", "f"),
               "chambres": ("les chambres", "dans les chambres", "fp"), "spa": ("le spa", "au spa", "m"),
               "exterieur": ("l’extérieur", "à l’extérieur", "m")},
    "entreprise": {"bureaux": ("les bureaux", "dans les bureaux", "mp"), "accueil": ("l’accueil", "à l’accueil", "m"),
                   "reunion": ("la salle de réunion", "en salle de réunion", "f"), "entrepot": ("l’entrepôt", "dans l’entrepôt", "m"),
                   "stationnement": ("le stationnement", "au stationnement", "m")},
    "garage": {"atelier": ("l’atelier", "à l’atelier", "m"), "etabli": ("l’établi", "à l’établi", "m"),
               "baie-1": ("la baie 1", "dans la baie 1", "f"), "baie-2": ("la baie 2", "dans la baie 2", "f"),
               "exterieur": ("l’extérieur", "à l’extérieur", "m")},
    "ferme": {"maison": ("la maison", "à la maison", "f"), "etable": ("l’étable", "à l’étable", "f"),
              "grange": ("la grange", "à la grange", "f"), "serre": ("la serre", "dans la serre", "f"),
              "cour": ("la cour", "dans la cour", "f")},
    "bateau": {"carre": ("le carré", "au carré", "m"), "cabine": ("la cabine avant", "dans la cabine avant", "f"),
               "cockpit": ("le cockpit", "au cockpit", "m"), "pont": ("le pont", "sur le pont", "m"),
               "feux": ("les feux de navigation", "aux feux de navigation", "mp")},
    "avion": {"cabine": ("la cabine", "en cabine", "f"), "cockpit": ("le poste de pilotage", "au poste de pilotage", "m"),
              "hangar": ("le hangar", "dans le hangar", "m"), "feux": ("les feux anticollision", "aux feux anticollision", "mp")},
}
LTXT = {
    "boulance": {"couloir-g": ("la bande gauche", "f"), "couloir-d": ("la bande droite", "f")},
    "chalet": {"salon": ("le grand salon", "m"), "foyer": ("le foyer", "m"), "ch-1": ("la chambre principale", "f"),
               "ch-2": ("la chambre d’amis", "f"), "terrasse": ("la terrasse", "f")},
    "entreprise": {"bureaux-n": ("la rangée nord", "f"), "bureaux-s": ("la rangée sud", "f"),
                   "issues": ("les issues de secours", "fp"), "parking": ("le stationnement", "m")},
    "avion": {"anticol": ("les feux anticollision", "mp")},
}


def _data():
    envs = {}
    for k, e in ENVS.items():
        e = dict(e)
        e["all"] = ALL[k]
        zt, lt = ZTXT[k], LTXT.get(k, {})
        e["zones"] = [{**z, "the": zt[z["k"]][0], "in": zt[z["k"]][1], "g": zt[z["k"]][2]} for z in e["zones"]]
        e["lights"] = [{**l, "the": (lt.get(l["k"]) or zt[l["zone"]])[0], "g": (lt.get(l["k"]) or (None, zt[l["zone"]][2]))[1]}
                       for l in e["lights"]]
        # Polygones et points en listes simples (JSON compact)
        e["zones"] = [{**z, "poly": [list(p) for p in z["poly"]]} for z in e["zones"]]
        envs[k] = e
    return {"v": 1, "user": "James", "ambiances": AMBIANCES, "photos": AMB_PHOTO, "envs": envs}


def html():
    """Bloc de données unique du module Éclairage (inclus une seule fois par le cadre Environnements)."""
    raw = json.dumps(_data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="lum-data">{raw}</script>'
