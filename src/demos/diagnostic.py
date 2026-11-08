# Démo « Diagnostic & continuité » : du symptôme à la remise en service, avec preuves.
# Deux cas simulés (chambre froide d'un commerce, réfrigérateur d'un VR). Une seule
# source pour les chiffres : la simulation ci-dessous produit les courbes ET les
# valeurs citées dans le texte (heures, températures, tensions), qui restent donc
# cohérentes. Le script assets/demos/diagnostic.js trace et anime; sans lui, les
# cinq étapes du premier cas se lisent l'une sous l'autre.

import json
import math
from html import escape

STEP = 3          # une mesure aux 3 minutes
END = 27 * 60     # minutes depuis « hier 12 h » jusqu'à « aujourd'hui 15 h »
NOW = 24 * 60 + 10     # aujourd'hui 12 h 10 : ouverture de l'enquête
APPROVE = NOW + 4      # 12 h 14 : accord donné
VERIFY = 26 * 60 + 32  # 14 h 32 : remise en service vérifiée
NB = " "


def hm(m):
    """Minutes depuis hier 12 h → « 14 h 32 » (espaces insécables)."""
    h, mn = divmod(int(round(m + 720)) % 1440, 60)
    return f"{h}{NB}h{NB}{mn:02d}" if mn else f"{h}{NB}h"


def dur(m):
    h, mn = divmod(int(round(m)), 60)
    return f"{h}{NB}h{NB}{mn:02d}" if h else f"{mn}{NB}min"


def fr(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def deg(v, d=1):
    return f"{fr(v, d)}{NB}°C"


# ---------------------------------------------------------------------------
# Cas A — chambre froide d'une épicerie (ventilateur du condenseur arrêté)
# ---------------------------------------------------------------------------
def sim_froid():
    t_now, cut_in, cut_out = 6.4, 3.8, 2.2
    doors = [22, 61, 118, 175, 236, 290, 352, 411, 470, 528, 1158, 1236, 1311, 1392]
    base, on, fail, fix = 3.0, False, None, None
    r_fail = r_fix = None
    temp, sec, comp, start = [], [], [], None
    over4 = alert = None
    for m in range(END + 1):
        if fail is None and m >= 18 * 60 + 35 and not on and base >= cut_in:
            fail = m                                  # le ventilateur lâche au démarrage
            r_fail = (t_now - base) / (NOW - fail)
        if fail is not None and fix is None and m == 25 * 60 + 48:
            fix = m                                   # 13 h 48 : moteur remplacé
            r_fix = (base - 3.0) / (VERIFY - fix)
        broken = fail is not None and fix is None
        if broken:
            on = True
        elif on and base <= cut_out:
            on = False
        elif not on and base >= cut_in:
            on = True
        if on and start is None:
            start = m
        if not on and start is not None:
            comp.append([start, m]); start = None
        if m % STEP == 0:
            spike = sum(.55 * math.exp(-(m - d) / 5) for d in doors if 0 <= m - d < 40)
            temp.append(round(base + spike, 2))
            sec.append(round(1.18 + .04 * math.sin(m * 1.7), 2) if on and not broken else 0)
        if broken:
            base += r_fail
            if over4 is None and base >= 4.0:
                over4 = m
            if alert is None and base >= 5.0:
                alert = m
        elif on:
            base -= r_fix if fix is not None else .105
        else:
            base += .052
    if start is not None:
        comp.append([start, END])
    in24 = [d for d in doors if NOW - 1440 <= d <= NOW]
    return dict(temp=temp, sec=sec, comp=comp, doors=doors, fail=fail, fix=fix, alert=alert,
                over4=over4, t_now=t_now, n_doors=len(in24), t_fix=round(3.0 + r_fix * (VERIFY - fix), 1))


# ---------------------------------------------------------------------------
# Cas B — réfrigérateur 12 V d'un VR (batterie trop basse, coupure de protection)
# ---------------------------------------------------------------------------
def sim_vr():
    t_now, cut_in, cut_out = 9.1, 4.8, 2.6
    doors = [40, 355, 390, 465, 610, 1185, 1220, 1430]
    tries = [(1280, 1287), (1330, 1336), (1375, 1382), (1415, 1421)]
    restart = APPROVE + 2
    base, on, cut = 3.4, False, None
    r_warm = r_cool = None
    temp, sec, comp, start, cuts = [], [], [], None, []
    over5 = alert = None
    att = sum(b - a for a, b in tries)

    def volt(m):
        if cut is None:
            v = 13.5 if m < 300 else 13.05 - (13.05 - 11.9) * (m - 300) / (15 * 60 - 300)
            return v - (.22 if on else 0)
        if m < cut + 3:
            return 11.62 - .24 * (m - cut) / 2
        if m < 1200:
            return 11.92 - .12 * (m - cut) / (1200 - cut)
        if m >= restart:
            return 13.9 + .2 * (1 - math.exp(-(m - restart) / 10)) - (.08 if on else 0)
        prev_end = 1200
        for a, b in tries:
            if a <= m < b:
                return 12.4 - .97 * (m - a) / (b - a - 1)
            if m < a:
                lo = 11.8 if prev_end == 1200 else 11.75
                return lo + (12.4 - lo) * (m - prev_end) / (a - prev_end)
            prev_end = b
        return 11.75 + .35 * min(1, (m - prev_end) / 60)

    for m in range(END + 1):
        if cut is None and m >= 15 * 60 + 5 and not on and base >= cut_in:
            cut = m                                   # le compresseur veut démarrer… et tombe
            off_min = (NOW - cut - 3) - att
            r_warm = (t_now - base + .07 * att) / off_min
        if m == restart:
            r_cool = (base - 4.0) / (VERIFY - restart)
        if cut is None or m >= restart:
            if m >= restart and base > cut_out and (on or m == restart):
                on = True
            elif on and base <= cut_out:
                on = False
            elif not on and base >= cut_in:
                on = True
        else:
            was = on
            on = m < cut + 3 or any(a <= m < b for a, b in tries)
            if was and not on:
                cuts.append(m)
        if on and start is None:
            start = m
        if not on and start is not None:
            comp.append([start, m]); start = None
        if m % STEP == 0:
            spike = sum(.6 * math.exp(-(m - d) / 6) for d in doors if 0 <= m - d < 40)
            temp.append(round(base + spike, 2))
            sec.append(round(volt(m), 2))
        if cut is None:
            base += -.07 if on else .03
        elif m < restart:
            base += -.07 if on and m >= cut + 3 else (0 if on else r_warm)
            if over5 is None and base >= 5.0:
                over5 = m
            if alert is None and base >= 6.0:
                alert = m
        else:
            base += -r_cool if on and r_cool else (-.07 if on else .03)
    if start is not None:
        comp.append([start, END])
    in24 = [d for d in doors if NOW - 1440 <= d <= NOW]
    vmin = min(sec[cut // STEP: NOW // STEP + 1])
    return dict(temp=temp, sec=sec, comp=comp, doors=doors, cut=cut, cuts=cuts, restart=restart,
                alert=alert, over5=over5, t_now=t_now, n_doors=len(in24), vmin=vmin, n_tries=len(tries))


F, V = sim_froid(), sim_vr()


# ---------------------------------------------------------------------------
# Textes des cinq étapes, construits à partir des valeurs simulées
# ---------------------------------------------------------------------------
CASES = {
    "froid": {
        "tab": ("Commerce", "Chambre froide"),
        "hero": dict(k="Chambre froide · maintenant", v=F["t_now"], lo=2, hi=4, max=10, start=3.0,
                     s=f"Consigne 3{NB}°C · plage normale 2 à 4{NB}°C",
                     since=f"Au-dessus de 4{NB}°C depuis {hm(F['over4'])}"),
        "legend": [("line", "Température"), ("band", f"Plage normale 2 à 4{NB}°C"), ("set", f"Consigne 3{NB}°C"), ("bar", "Compresseur en marche"),
                   ("dot", "Porte ouverte"), ("sec", "Courant du ventilateur")],
        "steps": [
            dict(h=f"La chambre froide n’atteint plus 3{NB}°C.",
                 p=(f"Il est {hm(NOW)}. Le thermomètre indique {deg(F['t_now'])} au lieu de 3{NB}°C. "
                    f"JARVIS a donné l’alerte à {hm(F['alert'])} et a ouvert une enquête, au lieu de vous laisser deviner."),
                 notif=(f"Chambre froide au-dessus de 5{NB}°C. J’ai commencé l’enquête.", hm(F["alert"]))),
            dict(h="Vingt-quatre heures de mesures, lues pour vous.",
                 p=(f"Jusqu’à {hm(F['fail'])}, tout est normal : le compresseur part et s’arrête, la température "
                    f"reste entre 2 et 4{NB}°C. Depuis, il tourne sans arrêt et la température monte quand même."),
                 take="le froid est produit, mais la chaleur ne sort plus."),
            dict(h="Quatre causes vérifiées. Une seule reste.",
                 checks=[
                     ("power", "ok", "Alimentation électrique", f"Tension stable à 240{NB}V, aucune coupure.", "Normale"),
                     ("doors", "ok", "Porte", f"{F['n_doors']} ouvertures, toutes refermées en moins de 40{NB}secondes.", "Fermée"),
                     ("set", "ok", "Thermostat", f"Consigne de 3{NB}°C, inchangée depuis 41{NB}jours.", "Réglé"),
                     ("sec", "bad", "Ventilateur du condenseur", f"Aucun courant depuis {hm(F['fail'])}; normalement 1,2{NB}A.", "Arrêté"),
                 ],
                 concl=("le ventilateur du condenseur est arrêté. Sans lui, la chaleur reste coincée "
                        "et le compresseur force pour rien.")),
            dict(sheet=("CF-0412", hm(NOW + 2), [
                ("Symptôme", f"Chambre froide à {deg(F['t_now'])} au lieu de 3{NB}°C."),
                ("Preuves", f"Courbe de 24{NB}h · compresseur en marche continue depuis {dur(NOW - F['fail'])} · ventilateur à 0{NB}A."),
                ("Causes écartées", "Alimentation, porte, thermostat."),
                ("Cause probable", "Moteur du ventilateur du condenseur."),
                ("Pièces à prévoir", "Moteur de ventilateur et condensateur (modèle à confirmer sur la plaque)."),
                ("Urgence", "Aujourd’hui · marchandise à surveiller."),
            ], [("Courbe de 24 h", "line"), ("Journal du compresseur", "comp"), ("Courant du ventilateur", "sec")]),
                 p="Le frigoriste arrive avec la bonne pièce, sans refaire l’enquête."),
            dict(h="JARVIS propose. Vous décidez.",
                 p="JARVIS propose d’envoyer le dossier à votre frigoriste, puis de vérifier la remise en service sur les mesures.",
                 flow=[("sent", f"Envoyé au frigoriste · {hm(APPROVE)}"),
                       ("work", f"Intervention : moteur du ventilateur remplacé à {hm(F['fix'])}"),
                       ("read", f"Relecture des mesures : retour à 3{NB}°C, cycles normaux"),
                       ("ok", f"Vérifié à {hm(VERIFY)}")],
                 done="Preuve jointe au dossier : la courbe revenue dans la plage normale."),
        ],
    },
    "vr": {
        "tab": ("Véhicule aménagé", "Réfrigérateur du VR"),
        "hero": dict(k="Réfrigérateur du VR · maintenant", v=V["t_now"], lo=2, hi=5, max=10, start=4.0,
                     s=f"Réglé sur 4{NB}°C · plage normale 2 à 5{NB}°C",
                     since=f"Au-dessus de 5{NB}°C depuis {hm(V['over5'])}"),
        "legend": [("line", "Température"), ("band", f"Plage normale 2 à 5{NB}°C"), ("set", f"Réglage 4{NB}°C"), ("bar", "Compresseur en marche"),
                   ("dot", "Porte ouverte"), ("sec", "Tension de la batterie")],
        "steps": [
            dict(h="Le réfrigérateur du VR ne refroidit plus.",
                 p=(f"Il est {hm(NOW)}. Le réfrigérateur indique {deg(V['t_now'])} au lieu de 4{NB}°C. "
                    f"JARVIS a donné l’alerte à {hm(V['alert'])}, pendant que les aliments étaient encore récupérables."),
                 notif=(f"Réfrigérateur du VR au-dessus de 6{NB}°C. J’ai commencé l’enquête.", hm(V["alert"]))),
            dict(h="Une nuit de mesures, lue pour vous.",
                 p=(f"À {hm(V['cut'])}, quand le compresseur a voulu démarrer, la batterie est descendue sous 11,6{NB}V. "
                    f"Le réfrigérateur s’est coupé pour la protéger. Au matin, il a tenté de repartir "
                    f"{['zéro', 'une', 'deux', 'trois', 'quatre', 'cinq'][V['n_tries']]} fois."),
                 take="le réfrigérateur n’est pas brisé, il manque d’énergie."),
            dict(h="Quatre causes vérifiées. Une seule reste.",
                 checks=[
                     ("power", "ok", "Fusible et câblage", "Le courant passe dès que la tension le permet.", "Intacts"),
                     ("doors", "ok", "Porte", f"{V['n_doors']} ouvertures courtes en 24{NB}h, bien refermée.", "Fermée"),
                     ("set", "ok", "Thermostat", f"Réglé sur 4{NB}°C, inchangé depuis le départ.", "Réglé"),
                     ("sec", "bad", "Tension de la batterie",
                      f"{fr(V['vmin'])}{NB}V au démarrage du compresseur; il coupe sous 11,6{NB}V.", "Trop basse"),
                 ],
                 concl=("la batterie est trop déchargée. Le réfrigérateur se coupe pour la protéger, "
                        "puis ne peut plus repartir.")),
            dict(sheet=("VR-0207", hm(NOW + 2), [
                ("Symptôme", f"Réfrigérateur à {deg(V['t_now'])}, coupé depuis {hm(V['cut'])}."),
                ("Preuves", f"Tension minimale {fr(V['vmin'])}{NB}V · {len(V['cuts'])} coupures pour basse tension · aucune recharge la nuit."),
                ("Causes écartées", "Fusible, porte, thermostat."),
                ("Cause probable", "Batterie trop déchargée, peut-être en fin de vie."),
                ("À prévoir", f"Recharge complète et test de capacité; batterie 12{NB}V 100{NB}Ah si le test échoue."),
                ("Urgence", "Aujourd’hui · aliments à surveiller."),
            ], [("Courbe de 24 h", "line"), ("Journal de la batterie", "sec"), ("Coupures du réfrigérateur", "comp")]),
                 p="Le technicien sait quoi tester en premier, sans refaire l’enquête."),
            dict(h="JARVIS propose. Vous décidez.",
                 p="JARVIS propose de démarrer la génératrice pour recharger la batterie, puis de vérifier que le réfrigérateur repart.",
                 flow=[("sent", f"Envoyé : démarrage de la génératrice · {hm(APPROVE)}"),
                       ("work", f"Batterie à 14,1{NB}V, réfrigérateur relancé à {hm(V['restart'])}"),
                       ("read", f"Relecture des mesures : retour à 4{NB}°C, tension stable"),
                       ("ok", f"Vérifié à {hm(VERIFY)}")],
                 done="Preuve jointe au dossier : la courbe revenue dans la plage normale."),
        ],
    },
}

RAIL = ["Symptôme", "Preuves", "Causes éliminées", "Dossier technicien", "Remise en service vérifiée"]


def series(sim, case):
    """Données du graphique (JSON) : les nombres, plus quelques étiquettes."""
    common = dict(end=END, now=NOW, approve=APPROVE, verify=VERIFY, step=STEP,
                  t=sim["temp"], s=sim["sec"], comp=sim["comp"], doors=sim["doors"])
    if case == "froid":
        return dict(common, y=[0, 8], band=[2, 4], set=3, anom=[sim["fail"], NOW], fix=sim["fix"],
                    sy=[0, 1.6], sunit="A", sname="Ventilateur du condenseur", sdec=1, cuts=[], sthr=None,
                    lab=dict(anom="Le compresseur ne s’arrête plus", set=f"Consigne 3{NB}°C",
                             band="Plage normale", verify=f"Vérifié à {hm(VERIFY)}", now="Maintenant",
                             comp="Compresseur", sec="Ventilateur du condenseur · A", thr="",
                             on="en marche", off="arrêté", cut="Coupure"))
    return dict(common, y=[0, 10], band=[2, 5], set=4, anom=[sim["cut"], NOW], fix=sim["restart"],
                sy=[11, 14.4], sunit="V", sname="Batterie", sdec=2, cuts=sim["cuts"], sthr=11.6,
                lab=dict(anom="Réfrigérateur coupé : batterie trop basse", set=f"Réglage 4{NB}°C",
                         band="Plage normale", verify=f"Vérifié à {hm(VERIFY)}", now="Maintenant",
                         comp="Compresseur", sec="Tension de la batterie · V", thr=f"Coupure 11,6{NB}V",
                         on="en marche", off="arrêté", cut="Coupure"))


DATA = {"froid": series(F, "froid"), "vr": series(V, "vr")}


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
def hero(case, c):
    h = c["hero"]
    pct = lambda v: f"{100 * v / h['max']:.1f}%"
    return f"""<div class="dg-hero" data-case="{case}"{'' if case == 'froid' else ' hidden'}>
      <p class="dg-hk"><i aria-hidden="true"></i>{h['k']}</p>
      <p class="dg-big"><b data-to="{h['v']}" data-from="{h['start']}">{fr(h['v'])}</b><span>°C</span></p>
      <div class="dg-gauge" style="--lo:{pct(h['lo'])};--hi:{pct(h['hi'])};--v:{pct(h['v'])};--v0:{pct(h['start'])}" aria-hidden="true">
        <i class="dg-gband"></i><i class="dg-gmark"></i>
      </div>
      <div class="dg-gscale" aria-hidden="true"><span>0{NB}°C</span><span>{h['max']}{NB}°C</span></div>
      <p class="dg-hs">{h['s']}</p>
      <p class="dg-since">{h['since']}</p>
    </div>"""


def legend(case, c):
    items = "".join(f'<li><i class="lg-{k}" aria-hidden="true"></i>{escape(t)}</li>' for k, t in c["legend"])
    return f'<ul class="dg-legend" data-case="{case}"{"" if case == "froid" else " hidden"}>{items}</ul>'


def step_html(case, n, s):
    hid = "" if case == "froid" else " hidden"
    head = f'<p class="dg-k">Étape {n} · {RAIL[n - 1]}</p>'
    if n == 1:
        msg, when = s["notif"]
        body = f"""<h3>{s['h']}</h3><p>{s['p']}</p>
        <div class="dg-notif"><i aria-hidden="true"></i><div><b>JARVIS</b><span>{msg}</span><small>Notification · {when}</small></div></div>"""
    elif n == 2:
        body = f"""<h3>{s['h']}</h3><p>{s['p']}</p><p class="dg-take"><b>Ce que ça veut dire :</b> {s['take']}</p>"""
    elif n == 3:
        lis = "".join(
            f'<li data-hl="{hl}" data-res="{res}"><i aria-hidden="true"></i><div><b>{t}</b><span>{d}</span></div>'
            f'<em><s>Vérification…</s><u>{r}</u></em></li>'
            for hl, res, t, d, r in s["checks"]
        )
        body = f"""<h3>{s['h']}</h3><ul class="dg-checks">{lis}</ul>
        <p class="dg-concl"><b>Cause probable :</b> {s['concl']}</p>"""
    elif n == 4:
        ref, when, rows, att = s["sheet"]
        dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
        chips = "".join(f'<span class="dg-att" data-from="{lane}">{a}</span>' for a, lane in att)
        body = f"""<div class="dg-sheet">
          <header><b>Dossier technicien · {ref}</b><small>Préparé par JARVIS · {when}</small></header>
          <dl>{dl}</dl>
          <footer><div class="dg-atts">{chips}</div><span class="dg-ready">Prêt à transmettre</span></footer>
        </div><p class="dg-after">{s['p']}</p>"""
    else:
        fl = "".join(f'<li data-k="{k}"><i aria-hidden="true"></i><span>{v}</span></li>' for k, v in s["flow"])
        body = f"""<h3>{s['h']}</h3><p>{s['p']}</p>
        <div class="dg-prop">
          <button type="button" class="dg-approve" data-act="approve">Approuver l’intervention</button>
          <p class="dg-wait">En attente de votre accord : rien n’est envoyé.</p>
          <ol class="dg-flow" aria-live="polite">{fl}</ol>
        </div>
        <div class="dg-done"><b>Remise en service vérifiée</b><span>{s['done']}</span></div>"""
    return f'<section class="dg-step" data-case="{case}" data-step="{n}"{hid}>{head}{body}</section>'


TABS = "".join(
    f'<button type="button" data-case="{k}" aria-pressed="{"true" if k == "froid" else "false"}">'
    f'<small>{c["tab"][0]}</small><b>{c["tab"][1]}</b></button>'
    for k, c in CASES.items()
)
RAIL_HTML = "".join(
    f'<li data-step="{i + 1}"><button type="button" data-go="{i + 1}"><i>{i + 1}</i><span>{t}</span></button></li>'
    for i, t in enumerate(RAIL)
)
PANELS = "".join(step_html(k, i + 1, s) for k, c in CASES.items() for i, s in enumerate(c["steps"]))
HEROES = "".join(hero(k, c) for k, c in CASES.items())
LEGENDS = "".join(legend(k, c) for k, c in CASES.items())
JSON = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))

HTML = f"""<div class="demo-shell" data-demo="diagnostic" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Diagnostic &amp; continuité</b><span class="tag tag-sim">Démo · données simulées</span></div>
  <div class="demo-body">
    <div class="dg-head">
      <div class="dg-cases" role="group" aria-label="Choisir un cas">{TABS}</div>
      <div class="dg-ctrl">
        <button type="button" data-nav="prev" aria-label="Étape précédente"><span aria-hidden="true">←</span></button>
        <button type="button" data-nav="play" aria-pressed="true"><i class="dg-pp" aria-hidden="true"></i><span class="dg-pl-on">Lecture auto</span><span class="dg-pl-off">En pause</span></button>
        <button type="button" data-nav="next" aria-label="Étape suivante"><span aria-hidden="true">→</span></button>
        <button type="button" data-nav="replay"><span aria-hidden="true">↻</span> Rejouer</button>
      </div>
    </div>
    <ol class="dg-rail" aria-label="Les cinq étapes de l’enquête">{RAIL_HTML}</ol>
    <div class="dg-stage">
      <div class="dg-viz">
        {HEROES}
        <div class="dg-chart" role="img" aria-label="Courbe de température des 24 dernières heures, avec les cycles du compresseur, les ouvertures de porte et une deuxième mesure (données simulées)">
          <svg class="dg-svg" xmlns="http://www.w3.org/2000/svg"></svg>
          <div class="dg-sweep" aria-hidden="true"><i></i></div>
          <div class="dg-tip" aria-hidden="true" hidden></div>
        </div>
        {LEGENDS}
      </div>
      <div class="dg-panels" aria-live="polite">{PANELS}</div>
    </div>
  </div>
  <script type="application/json" class="dg-data">{JSON}</script>
</div>
<p class="demo-hint">Lecture automatique · flèches pour avancer · survolez la courbe · rien n’est envoyé sans « Approuver »</p>"""


# ===========================================================================
# Partie 2 — Ce que l'extension mesure vraiment (sous la démo, sur la page)
#   1. Bibliothèque : 22 diagnostics précis et mesurables, par environnement.
#   2. La boucle complète : trois cas vedettes animés, de la mesure au rapport.
#   3. Santé des équipements : score, durée de vie restante, prochain entretien.
# Toutes les valeurs sont des données d'exemple. Les courbes sont produites ici
# (bloc JSON) et tracées par assets/demos/diagnostic.js à la taille réelle.
# ===========================================================================
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _nz(i, seed):
    """Bruit déterministe entre −0,5 et 0,5 (mêmes courbes à chaque build)."""
    v = math.sin(i * 12.9898 + seed * 78.233) * 43758.5453
    return v - math.floor(v) - .5


def _ser(n, f, seed, amp, d=2):
    return [round(f(i) + amp * _nz(i, seed), d) for i in range(n)]


def _smooth(k):
    k = max(0.0, min(1.0, k))
    return k * k * (3 - 2 * k)


def _rise(i, a, b, v0, v1):
    """v0 jusqu'à l'index a, puis montée douce vers v1 à l'index b."""
    return v0 + (v1 - v0) * _smooth((i - a) / max(1, b - a))


ENVS = [
    ("maison", "Maison"),
    ("ferme", "Ferme"),
    ("commerce", "Commerce"),
    ("vehicule", "Véhicule"),
    ("energie", "Énergie"),
    ("ti", "Réseau et TI"),
]
ENV_LAB = dict(ENVS)

# Méthodes de détection (étiquettes)
M_SEUIL, M_TEND, M_REF, M_CORR = "Seuil", "Tendance", "Écart à la référence", "Corrélation"


def C(kind, unit, y, pts, x, band=None, thr=None, thr_lab="", ref=None, ref_lab="", anom=None, dec=1, name=""):
    return dict(k=kind, u=unit, y=y, p=pts, x=x, band=band, thr=thr, tl=thr_lab, ref=ref, rl=ref_lab,
                a=anom, d=dec, n=name)


# Chaque diagnostic : id, environnement, nom, équipement, mesure, plage normale,
# signature, méthodes, détail de détection, test automatique, résultat, bon de travail, courbe.
DIAGS = [
    dict(id="puits", env="ferme", t="Pompe de puits", e="Pompe submersible 1 HP · puits artésien",
         mes=f"Courant du moteur (A) par pince sur le circuit, démarrages par heure, pression du réservoir (psi).",
         norm=f"8,5 à 9,5{NB}A en marche · 1 à 3 démarrages par heure la nuit · 40 à 60{NB}psi.",
         sig=f"La nuit, sans eau consommée, la pompe démarre 9 fois par heure au lieu de 2.",
         m=[M_REF, M_CORR],
         how=f"Démarrages nocturnes comparés à la moyenne des 30 dernières nuits (+{NB}290{NB}%), croisés avec le compteur d’eau : 0{NB}L consommé.",
         test=f"À 2 h, la vanne motorisée de la maison se ferme 15{NB}minutes et JARVIS mesure la chute de pression du réservoir.",
         res=f"La pression baisse de 2,8{NB}psi/min même vanne fermée : l’eau retourne au puits. Clapet de pied ou conduite.",
         bon=("Puisatier", "Remplacer le clapet de pied, vérifier la conduite."),
         c=C("bars", "/h", [0, 10], _ser(21, lambda i: _rise(i, 9, 15, 2.3, 9.0), 1, .7), ("Il y a 21 nuits", "Cette nuit"),
             band=[1, 3.5], thr=5, thr_lab="Référence + 100 %", anom=10, name="Démarrages par heure, la nuit")),
    dict(id="tank", env="ferme", t="Tank à lait", e="Réservoir réfrigéré 6 000 L",
         mes=f"Température du lait (°C) aux 30{NB}secondes, courant du compresseur (A), température de l’air au condenseur.",
         norm=f"De 35 à 4{NB}°C en moins de 2{NB}h après la traite · pente de départ d’environ −0,25{NB}°C/min.",
         sig=f"La pente tombe à −0,12{NB}°C/min : 3{NB}h{NB}35 pour passer sous 4{NB}°C.",
         m=[M_TEND, M_REF],
         how="Durée de refroidissement de chaque traite comparée aux 20 traites précédentes; alerte quand trois traites de suite dépassent l’objectif.",
         test=f"À la traite suivante, JARVIS mesure le courant du compresseur et l’écart de température à travers le condenseur.",
         res=f"Courant normal (11,2{NB}A), mais écart de 6{NB}°C au condenseur au lieu de 14{NB}°C : condenseur encrassé.",
         bon=("Frigoriste agricole", "Nettoyer le condenseur, vérifier le ventilateur et la charge."),
         c=C("line", "min", [0, 240], _ser(24, lambda i: _rise(i, 12, 23, 102, 215), 2, 9, 0), ("Il y a 12 jours", "Dernière traite"),
             band=[80, 120], thr=120, thr_lab="Objectif 2 h", anom=13, dec=0, name="Minutes pour passer sous 4 °C")),
    dict(id="etable", env="ferme", t="Ventilation d’étable", e="Ventilateurs de 50 po à vitesse variable",
         mes=f"Vitesse réelle des ventilateurs (tr/min, en % de la consigne), ammoniac NH₃ (ppm), température intérieure.",
         norm=f"Vitesse égale à la consigne à ±5{NB}% · NH₃ sous 10{NB}ppm.",
         sig=f"Le ventilateur 3 tourne à 62{NB}% de la consigne; le NH₃ de sa zone monte à 18{NB}ppm.",
         m=[M_REF, M_CORR],
         how="Vitesse mesurée comparée à la consigne envoyée, et hausse de NH₃ localisée près du même ventilateur.",
         test=f"Le ventilateur 3 est commandé à 100{NB}% pendant 2{NB}minutes; JARVIS mesure vitesse et courant.",
         res=f"Courant normal, vitesse plafonnée à 61{NB}% : la courroie glisse.",
         bon=("Électromécanicien agricole", "Remplacer la courroie, vérifier la poulie."),
         c=C("line", "%", [0, 100], _ser(48, lambda i: (60 + 18 * math.sin(i / 7.6)) * (1 if i < 30 else .62), 3, 2.5, 0), ("Avant-hier", "Maintenant"),
             ref=[round(60 + 18 * math.sin(i / 7.6)) for i in range(48)], ref_lab="Consigne", anom=30, dec=0, name="Vitesse du ventilateur 3")),
    dict(id="abreuvoir", env="ferme", t="Abreuvoirs chauffants", e="Conduite d’eau de l’étable, groupe A",
         mes="Débit d’eau (L/h) par groupe d’animaux, température de la conduite (°C).",
         norm=f"Débit du groupe A proche de celui du groupe B (±10{NB}%) · conduite au-dessus de 4{NB}°C.",
         sig=f"La nuit froide, le débit du groupe A chute de 35{NB}%; sa conduite descend à 1{NB}°C.",
         m=[M_REF, M_CORR],
         how="Débit du groupe A comparé à celui du groupe B, corrélé à la température de la conduite et à la météo.",
         test=f"JARVIS met le câble chauffant en marche forcée 20{NB}minutes et mesure son courant et la température de la conduite.",
         res=f"Aucun courant dans le câble chauffant (0{NB}A au lieu de 2,4{NB}A) : câble ou thermostat hors service.",
         bon=("Électricien agricole", "Remplacer le câble chauffant avant la prochaine nuit froide."),
         c=C("line", "L/h", [0, 160], _ser(48, lambda i: (95 + 30 * math.sin(i / 3.8)) * (1 if i < 30 else .64), 4, 6, 0), ("Avant-hier", "Maintenant"),
             ref=[round(95 + 30 * math.sin(i / 3.8)) for i in range(48)], ref_lab="Groupe B", anom=30, dec=0, name="Débit du groupe A")),
    dict(id="chauffe", env="maison", t="Chauffe-eau", e="Réservoir électrique 60 gal · deux éléments 4 500 W",
         mes=f"Temps de réchauffe (min) après un gros tirage, courant de chaque élément (A), température à la sortie.",
         norm=f"Réchauffe complète en 45 à 55{NB}min · élément du haut, puis celui du bas, à 18,7{NB}A chacun.",
         sig=f"La réchauffe passe d’un coup de 48 à 95{NB}min; l’élément du bas ne s’allume plus.",
         m=[M_REF, M_SEUIL],
         how="Profil du courant de chaque réchauffe comparé à la référence : la deuxième marche de 18,7 A a disparu.",
         test="Au prochain tirage, JARVIS suit la séquence des éléments et la température de sortie minute par minute.",
         res=f"Élément du haut 18,7{NB}A, élément du bas 0{NB}A : élément inférieur ou son thermostat hors service.",
         bon=("Plombier ou électricien", "Remplacer l’élément inférieur et son thermostat."),
         c=C("bars", "min", [0, 110], _ser(20, lambda i: 48 if i < 13 else 95, 5, 5, 0), ("Il y a 20 jours", "Hier"),
             band=[35, 55], thr=60, thr_lab="Seuil 60 min", anom=13, dec=0, name="Temps de réchauffe")),
    dict(id="thermopompe", env="maison", t="Thermopompe", e="Thermopompe centrale 3 tonnes",
         mes="Écart de température entre l’air de retour et l’air soufflé (ΔT, °C), durée des cycles, démarrages par heure.",
         norm=f"ΔT de 10 à 14{NB}°C en chauffage · cycles d’au moins 10{NB}min · 2 à 4 démarrages par heure.",
         sig=f"Cycles courts de 3 à 4{NB}min, 11 démarrages par heure, ΔT de 6{NB}°C.",
         m=[M_SEUIL, M_TEND],
         how="Seuil sur le nombre de démarrages par heure, et tendance du ΔT sur 14 jours à température extérieure égale.",
         test=f"JARVIS force 15{NB}minutes de marche continue et mesure le ΔT stabilisé et la perte de charge du filtre.",
         res=f"Filtre propre, ΔT stable à 6{NB}°C : charge de réfrigérant basse probable.",
         bon=("Technicien en chauffage et climatisation", "Rechercher la fuite, recharger le réfrigérant."),
         c=C("bars", "/h", [0, 14], _ser(24, lambda i: _rise(i, 12, 16, 2.6, 11), 6, .8), ("Hier 8 h", "Maintenant"),
             band=[1, 4], thr=6, thr_lab="Seuil 6 / h", anom=13, name="Démarrages par heure")),
    dict(id="garage", env="maison", t="Porte de garage", e="Ouvre-porte à courroie ½ HP",
         mes="Temps de course (s), courant du moteur (A) tout au long de la course, fins de course.",
         norm=f"Course de 12 à 13{NB}s · courant sous 4{NB}A, sans pic.",
         sig=f"Course de 15,8{NB}s; pic de 6,1{NB}A toujours au même endroit, à 70{NB}% de la course.",
         m=[M_REF],
         how="Profil de courant de chaque ouverture comparé, point par point, au profil enregistré à l’installation.",
         test="À la prochaine ouverture, JARVIS enregistre le profil complet et vérifie l’inversion de sécurité.",
         res="Frottement localisé à 70 % de la course : roulette ou rail; inversion de sécurité fonctionnelle.",
         bon=("Technicien de portes de garage", "Remplacer les roulettes, aligner le rail, vérifier les ressorts."),
         c=C("line", "A", [0, 7], _ser(50, lambda i: 2.6 + .6 * math.sin(i / 8) + 3.3 * math.exp(-((i - 35) / 3.2) ** 2), 7, .15), ("Fermée", "Ouverte"),
             ref=[round(2.6 + .6 * math.sin(i / 8), 2) for i in range(50)], ref_lab="Profil de référence", anom=31, name="Courant pendant la course")),
    dict(id="puisard", env="maison", t="Pompe de puisard", e="Pompe submersible ⅓ HP · sous-sol",
         mes="Niveau d’eau dans la fosse (cm), temps de pompage par cycle (s), courant (A).",
         norm=f"Pompage de 12 à 20{NB}s par cycle · niveau sous 30{NB}cm · courant de 5,5 à 6{NB}A.",
         sig=f"Le temps de pompage double (42{NB}s) et le courant baisse de 30{NB}%.",
         m=[M_TEND, M_REF],
         how="Temps de pompage comparé aux 60 derniers cycles; vitesse de baisse du niveau (cm/s) comparée à la référence.",
         test=f"Au prochain cycle, JARVIS mesure la baisse du niveau seconde par seconde : débit réel contre débit de référence.",
         res=f"Débit à 45{NB}% de la référence : crépine bouchée ou turbine usée. Pompe de secours vérifiée, prête.",
         bon=("Plombier", "Nettoyer la crépine, vérifier le clapet; remplacer la pompe si l’usure est confirmée."),
         c=C("bars", "s", [0, 50], _ser(20, lambda i: _rise(i, 9, 16, 17, 43), 8, 2.2, 0), ("Il y a 20 cycles", "Dernier cycle"),
             band=[12, 20], thr=30, thr_lab="Seuil 30 s", anom=11, dec=0, name="Temps de pompage")),
    dict(id="fumee", env="maison", t="Détecteurs de fumée", e="Neuf détecteurs reliés",
         mes="Tension de la pile (V), résultat de l’auto-test hebdomadaire, âge du détecteur, communication.",
         norm=f"Pile au-dessus de 2,8{NB}V · auto-test réussi chaque semaine · moins de 10 ans.",
         sig=f"Corridor : pile à 2,62{NB}V. Cuisine : fabriqué il y a 10 ans et 2 mois.",
         m=[M_SEUIL, M_TEND],
         how="Seuil sur la tension, tendance de décharge (date prévue sous le seuil) et calendrier de fin de vie du fabricant.",
         test="Auto-test hebdomadaire déclenché à distance (sirène silencieuse quand le modèle le permet) et contrôle de la liaison.",
         res="Une pile à changer cette semaine, un détecteur à remplacer; les sept autres réussissent l’auto-test.",
         bon=("Responsable du bâtiment", "Changer la pile du corridor, remplacer le détecteur de la cuisine."),
         c=C("line", "V", [2.4, 3.2], _ser(52, lambda i: 3.06 - .0018 * i - (.0004 * max(0, i - 30) ** 1.6), 9, .012, 2), ("Il y a 1 an", "Cette semaine"),
             band=[2.8, 3.2], thr=2.8, thr_lab="Seuil bas 2,8 V", anom=40, dec=2, name="Pile du détecteur du corridor")),
    dict(id="congel", env="commerce", t="Congélateur commercial", e="Congélateur vertical à deux portes · dépanneur",
         mes="Température intérieure (°C), contact de porte (secondes ouvertes), courant du compresseur.",
         norm=f"−22 à −18{NB}°C · retour sous −18{NB}°C en moins de 10{NB}min après une ouverture.",
         sig=f"Remontées jusqu’à −11{NB}°C, retour en 38{NB}min; la température monte même porte fermée.",
         m=[M_CORR, M_REF],
         how="Corrélation porte et température : la remontée ne suit plus les ouvertures. Temps de marche du compresseur porte fermée.",
         test=f"La nuit, porte fermée 2{NB}h : JARVIS mesure la part de marche du compresseur contre la référence.",
         res=f"Compresseur en marche 78{NB}% du temps au lieu de 45{NB}% : joint de porte usé, infiltration d’air chaud.",
         bon=("Frigoriste commercial", "Remplacer le joint de la porte droite, vérifier le dégivrage."),
         c=C("line", "°C", [-24, -8], _ser(60, lambda i: (-20 if i < 34 else _rise(i, 34, 44, -20, -15.5)) + sum(
             (3.2 if j < 34 else 5.5) * math.exp(-max(0, i - j) / (2 if j < 34 else 6)) * (i >= j) for j in (6, 17, 27, 38, 49)), 10, .4), ("Il y a 12 h", "Maintenant"),
             band=[-22, -18], thr=-15, thr_lab="Seuil −15 °C", anom=34, name="Température intérieure")),
    dict(id="air", env="commerce", t="Compresseur d’air", e="Compresseur à vis 15 HP · atelier",
         mes="Pression du réservoir (kPa), chute de pression la nuit (kPa/min), démarrages par heure, courant.",
         norm=f"Chute sous 5{NB}kPa/min hors production · 6 démarrages par heure au plus.",
         sig=f"La nuit, machines arrêtées : chute de 22{NB}kPa/min et 14 démarrages par heure.",
         m=[M_REF, M_SEUIL],
         how="Chute de pression des nuits sans production comparée à la référence de l’installation.",
         test=f"Dimanche 3 h, JARVIS isole chaque zone avec ses vannes motorisées et mesure la chute zone par zone.",
         res=f"Zone B (peinture) : 18{NB}kPa/min. Fuite à un raccord rapide; environ 1,1{NB}kW perdus en continu.",
         bon=("Mécanicien d’entretien", "Remplacer les raccords rapides de la zone B, refaire l’essai."),
         c=C("bars", "kPa/min", [0, 26], _ser(14, lambda i: _rise(i, 6, 11, 3.6, 22), 11, 1.4), ("Il y a 14 nuits", "Cette nuit"),
             band=[0, 5], thr=8, thr_lab="Seuil 8 kPa/min", anom=7, name="Chute de pression la nuit")),
    dict(id="vaisselle", env="commerce", t="Lave-vaisselle commercial", e="Lave-vaisselle à capot · restaurant",
         mes="Température du rinçage final (°C) à chaque cycle, courant du surchauffeur (A).",
         norm=f"Rinçage final d’au moins 82{NB}°C, à chaque cycle.",
         sig=f"Pendant le coup de feu du soir, le rinçage descend à 76{NB}°C.",
         m=[M_SEUIL, M_CORR],
         how="Seuil bas sur chaque cycle, corrélé à la cadence : la chute apparaît au-delà de 40 cycles à l’heure.",
         test="JARVIS mesure le courant du surchauffeur pendant trois cycles de suite.",
         res=f"Un des trois éléments du surchauffeur ne tire plus de courant : capacité réduite d’un tiers.",
         bon=("Technicien d’équipement de cuisine", "Remplacer l’élément du surchauffeur."),
         c=C("bars", "°C", [70, 90], _ser(30, lambda i: 84.5 - (7.5 * math.exp(-((i - 23) / 3.5) ** 2) if i > 15 else 0), 12, .8), ("17 h", "21 h"),
             band=[82, 90], thr=82, thr_lab="Minimum 82 °C", anom=18, name="Rinçage final")),
    dict(id="moteur", env="vehicule", t="Moteur du VR", e="Classe C · moteur V8 essence",
         mes="Lecteur OBD-II : codes, température du liquide de refroidissement (°C), correction de carburant à long terme (%).",
         norm=f"88 à 98{NB}°C · correction de carburant entre −5 et +5{NB}%.",
         sig=f"Correction à +14{NB}% au ralenti, code P0171 en attente, 104{NB}°C en montée.",
         m=[M_TEND, M_SEUIL],
         how="Tendance de la correction de carburant sur 15 trajets, seuil sur la température et lecture des codes en attente.",
         test=f"À l’arrêt, JARVIS compare la correction au ralenti et à 2 500{NB}tr/min (moteur chaud, avec votre accord).",
         res=f"+14{NB}% au ralenti, +4{NB}% à 2 500{NB}tr/min : prise d’air probable, pas l’injection.",
         bon=("Mécanicien de véhicules récréatifs", "Rechercher la prise d’air (test à la fumée), vérifier le thermostat."),
         c=C("line", "%", [-6, 18], _ser(15, lambda i: _rise(i, 6, 13, .5, 14), 13, 1.3), ("Il y a 15 trajets", "Aujourd’hui"),
             band=[-5, 5], thr=10, thr_lab="Seuil +10 %", anom=8, name="Correction de carburant")),
    dict(id="pneus", env="vehicule", t="Pneus", e="Six pneus · roues jumelées à l’arrière",
         mes="Capteurs de pression et de température de chaque pneu (psi, °C).",
         norm=f"80{NB}psi à froid ±3 · pneus jumelés à moins de 5{NB}°C l’un de l’autre.",
         sig=f"Arrière gauche intérieur : −1,4{NB}psi par jour; 9{NB}°C plus chaud que son jumeau en roulant.",
         m=[M_REF, M_TEND],
         how="Pneu comparé à son jumeau (même charge, même route), et tendance de la pression à froid jour après jour.",
         test=f"Au matin, après 8{NB}h de stationnement, JARVIS compare les pressions à froid pour écarter l’effet de la chaleur.",
         res=f"Fuite lente confirmée : 1,4{NB}psi en 24{NB}h. Rouler sous 72{NB}psi abîmerait le pneu.",
         bon=("Atelier de pneus", "Réparer ou remplacer le pneu arrière gauche intérieur."),
         c=C("line", "psi", [60, 86], _ser(10, lambda i: 80 - 1.45 * i, 14, .5), ("Il y a 10 jours", "Ce matin"),
             band=[77, 83], thr=75, thr_lab="Seuil 75 psi", ref=[80] * 10, ref_lab="Pneu jumeau", anom=3, name="Pression à froid")),
    dict(id="lifepo4", env="vehicule", t="Batteries LiFePO₄", e="Banc 12 V 560 Ah · véhicule aménagé",
         mes="Tension de chaque cellule (mV) lue par le BMS, résistance interne (mΩ), température des cellules.",
         norm=f"Écart entre cellules sous 30{NB}mV en fin de charge · résistance d’environ 0,25{NB}mΩ par cellule.",
         sig=f"Écart de 140{NB}mV en fin de charge : la cellule 3 monte toujours la première.",
         m=[M_REF, M_TEND],
         how="Chaque cellule comparée à ses voisines à chaque fin de charge; tendance de l’écart sur 30 charges.",
         test=f"Impulsion de charge de 50{NB}A pendant 10{NB}s : JARVIS calcule la résistance de chaque cellule.",
         res=f"Cellule 3 à 0,41{NB}mΩ (+64{NB}%), capacité estimée à −18{NB}% : cellule faible.",
         bon=("Technicien 12 V", "Équilibrage actif, puis remplacement de la cellule 3 si l’écart revient."),
         c=C("line", "mV", [0, 160], _ser(30, lambda i: _rise(i, 15, 29, 16, 140), 15, 5, 0), ("Il y a 30 charges", "Dernière charge"),
             band=[0, 30], thr=50, thr_lab="Seuil 50 mV", anom=17, dec=0, name="Écart entre cellules")),
    dict(id="generatrice", env="energie", t="Génératrice de secours", e="Génératrice au propane 22 kW",
         mes="Temps de démarrage (s), tension (V) et fréquence (Hz) pendant l’essai en charge, température du moteur.",
         norm=f"Démarrage en moins de 10{NB}s · 240{NB}V ±5{NB}% · 60{NB}Hz ±0,5.",
         sig=f"Démarrage de 8 à 18{NB}s en trois semaines; 58,7{NB}Hz sous 70{NB}% de charge.",
         m=[M_TEND, M_SEUIL],
         how="Tendance du temps de démarrage d’un essai à l’autre, et seuil sur la fréquence pendant l’essai en charge.",
         test=f"Essai en charge automatique chaque mardi à 10{NB}h, 20{NB}minutes sur des charges non essentielles.",
         res="La fréquence chute sous la charge : alimentation en carburant ou régulateur à vérifier.",
         bon=("Mécanicien de génératrices", "Vérifier le régulateur de propane et le filtre; refaire l’essai en charge."),
         c=C("bars", "s", [0, 20], _ser(12, lambda i: _rise(i, 7, 11, 8, 18), 16, .7), ("Il y a 12 semaines", "Mardi"),
             band=[5, 10], thr=10, thr_lab="Seuil 10 s", anom=9, name="Temps de démarrage à l’essai")),
    dict(id="solaire", env="energie", t="Panneaux solaires", e="Toiture 9,6 kW · deux chaînes",
         mes="Production réelle (kWh) contre production attendue selon l’ensoleillement prévu (W/m²), tension de chaque chaîne.",
         norm=f"Production réelle de 90 à 105{NB}% de l’attendu, par temps clair.",
         sig=f"La chaîne 2 glisse à 78{NB}% de l’attendu, environ −1{NB}% par semaine; la chaîne 1 reste à 98{NB}%.",
         m=[M_REF, M_CORR],
         how="Production comparée à la prévision d’ensoleillement, et chaîne 2 comparée à la chaîne 1 sous le même soleil.",
         test="À midi, par temps clair, l’onduleur mesure la tension à vide et la courbe courant-tension de chaque chaîne.",
         res=f"Chaîne 2 : tension 12{NB}% sous la chaîne 1. Un panneau ou sa diode de dérivation est défaillant.",
         bon=("Installateur solaire", "Inspecter la chaîne 2 à la caméra thermique, remplacer le panneau ou la diode."),
         c=C("line", "%", [60, 110], _ser(30, lambda i: _rise(i, 8, 29, 97, 78), 17, 1.6, 0), ("Il y a 30 jours", "Hier"),
             band=[90, 105], thr=88, thr_lab="Seuil 88 %", ref=_ser(30, lambda i: 98, 27, 1.2, 0), ref_lab="Chaîne 1", anom=12, dec=0, name="Rendement de la chaîne 2")),
    dict(id="panneau", env="energie", t="Panneau électrique", e="Panneau 200 A · capteurs thermiques",
         mes="Température de chaque borne (°C), courant de chaque circuit (A).",
         norm=f"Bornes sous 45{NB}°C · échauffement proportionnel au courant, comme les voisines.",
         sig=f"Disjoncteur 14 : 61{NB}°C à 18{NB}A, quand ses voisines restent à 32{NB}°C.",
         m=[M_CORR, M_REF],
         how="Température corrélée au courant sur 24 h : la borne 14 chauffe deux fois plus que ses voisines pour la même charge.",
         test="JARVIS compare la montée de température à trois paliers de charge (cuisinière, sécheuse, les deux).",
         res="Échauffement anormal à chaque palier : connexion desserrée ou disjoncteur usé. Risque d’incendie.",
         bon=("Maître électricien", "Resserrer ou remplacer le disjoncteur 14; vérifier le conducteur."),
         c=C("line", "°C", [20, 70], _ser(48, lambda i: 33 + (28 if i >= 20 else 6) * max(0, math.sin((i - 14) / 6.5)) ** 2, 18, 1.2, 0), ("Hier 8 h", "Maintenant"),
             band=[20, 45], thr=50, thr_lab="Seuil 50 °C", ref=_ser(48, lambda i: 31 + 3 * max(0, math.sin((i - 14) / 6.5)) ** 2, 28, .8, 0),
             ref_lab="Bornes voisines", anom=24, dec=0, name="Borne du disjoncteur 14")),
    dict(id="onduleur", env="ti", t="Onduleur", e="Onduleur 1 500 VA · baie du serveur",
         mes="Charge (%), autonomie annoncée (min), état et température des batteries.",
         norm=f"Charge sous 60{NB}% · autonomie de plus de 20{NB}min.",
         sig=f"À charge égale (38{NB}%), l’autonomie passe de 24 à 9{NB}min en trois mois.",
         m=[M_TEND],
         how="Tendance de l’autonomie à charge comparable; date projetée sous le seuil de 15 minutes.",
         test=f"Autotest de 30{NB}s sur batterie chaque mois, puis essai d’autonomie mesuré hors des heures d’ouverture.",
         res=f"Batteries à 41{NB}% de leur capacité d’origine : remplacement nécessaire.",
         bon=("Technicien TI", "Remplacer les batteries de l’onduleur, refaire l’essai."),
         c=C("line", "min", [0, 30], _ser(13, lambda i: _rise(i, 3, 12, 24, 9), 19, .8), ("Il y a 13 semaines", "Cette semaine"),
             band=[20, 30], thr=15, thr_lab="Seuil 15 min", anom=6, name="Autonomie annoncée")),
    dict(id="disques", env="ti", t="Disques du serveur", e="Serveur de fichiers · quatre disques en miroir",
         mes="Données SMART : secteurs réalloués, secteurs en attente, erreurs de lecture, température (°C).",
         norm=f"Aucun secteur réalloué ni en attente · moins de 45{NB}°C.",
         sig=f"Disque 2 : de 0 à 56 secteurs réalloués en 10 jours, 4 en attente.",
         m=[M_TEND, M_SEUIL],
         how="Croissance des secteurs réalloués d’un jour à l’autre : c’est la vitesse, pas le nombre, qui annonce la panne.",
         test=f"Autotest SMART long la nuit (environ 6{NB}h), puis vérification complète du volume.",
         res="L’autotest échoue; trois erreurs de lecture. Le miroir protège encore les données.",
         bon=("Technicien TI", "Remplacer le disque 2 et reconstruire le miroir; vérifier la sauvegarde."),
         c=C("bars", "", [0, 60], [0, 0, 0, 0, 0, 2, 8, 8, 19, 26, 33, 41, 49, 56], ("Il y a 14 jours", "Aujourd’hui"),
             band=[0, 1], thr=10, thr_lab="Seuil 10", anom=5, dec=0, name="Secteurs réalloués, disque 2")),
    dict(id="wifi", env="ti", t="Réseau Wi-Fi", e="Trois bornes maillées · maison",
         mes="Perte de paquets (%), latence (ms), force du signal (dBm), occupation des canaux.",
         norm=f"Perte sous 0,5{NB}% · latence locale sous 10{NB}ms.",
         sig=f"Chaque soir de 19 h à 22 h, 6 à 9{NB}% de pertes sur la borne 2.",
         m=[M_CORR],
         how="Pertes corrélées à l’heure et à l’occupation du canal : elles reviennent aux mêmes heures, sur la même borne.",
         test=f"Mesure aux 5{NB}s vers la borne 2 et balayage des canaux pendant la plage touchée.",
         res=f"Canal 6 occupé à 82{NB}% par un réseau voisin. Aucune panne : de l’interférence.",
         bon=("Aucun technicien", "JARVIS propose de changer la borne 2 de canal, avec votre accord."),
         c=C("line", "%", [0, 10], _ser(72, lambda i: .2 + (7 * max(0, math.sin(math.pi * ((i % 24) - 19) / 3)) if 19 <= i % 24 <= 22 else 0), 20, .3), ("Il y a 3 jours", "Maintenant"),
             band=[0, .5], thr=2, thr_lab="Seuil 2 %", anom=19, name="Perte de paquets, borne 2")),
    dict(id="piscine", env="maison", t="Filtre de piscine", e="Pompe et filtre au sable · piscine creusée",
         mes="Pression à l’entrée du filtre (psi), débit (L/min), courant de la pompe.",
         norm=f"10 à 15{NB}psi après un lavage à contre-courant.",
         sig=f"La pression monte de 11 à 19{NB}psi en un mois; le débit baisse de 25{NB}%.",
         m=[M_TEND, M_SEUIL],
         how="Tendance de la pression depuis le dernier lavage, seuil à +6 psi au-dessus de la pression propre.",
         test="Après le lavage à contre-courant, JARVIS vérifie que la pression revient près de 11 psi.",
         res="Pression revenue à 16 psi seulement : sable colmaté, à remplacer.",
         bon=("Entretien de piscine", "Remplacer le sable du filtre, vérifier le panier de la pompe."),
         c=C("line", "psi", [6, 22], _ser(30, lambda i: 11 + 8 * (i / 29) ** 1.4, 21, .4), ("Il y a 30 jours", "Aujourd’hui"),
             band=[8, 15], thr=17, thr_lab="Seuil 17 psi", anom=20, name="Pression du filtre")),
]

# ---------------------------------------------------------------------------
# Les trois cas vedettes : la boucle complète, de la mesure au rapport
# ---------------------------------------------------------------------------
LOOP = ["Mesure", "Écart détecté", "Test automatique", "Diagnostic", "Bon de travail",
        "Intervention", "Retour à la normale", "Rapport"]

# Courbes : points avant l'intervention, puis après (retour à la normale)
_P_PUITS = _ser(28, lambda i: _rise(i, 8, 15, 2.3, 9) if i < 18 else 2.3, 31, .6)
_P_TANK = _ser(30, lambda i: _rise(i, 9, 19, 101, 212) if i < 22 else 100, 32, 7, 0)
_P_LFP = _ser(30, lambda i: _rise(i, 6, 18, 16, 141) if i < 22 else (60 if i == 22 else 16), 33, 4, 0)

CASES2 = [
    dict(id="puits", env="Ferme", t="Pompe de puits", photo="pompe-puits", ph="Pompe submersible et réservoir sous pression",
         c=C("bars", "/h", [0, 10], _P_PUITS, ("Il y a 4 semaines", "Aujourd’hui"), band=[1, 3.5], thr=5, thr_lab="Référence + 100 %",
             anom=10, name="Démarrages par heure, la nuit"),
         # index de chaque étape sur la courbe : montré jusqu'à…, test, intervention
         at=dict(meas=8, dev=13, test=15, fix=17, back=24),
         st=[
             ("Courant du moteur et pression lus aux 2 secondes.",
              f"Pince ampèremétrique sur le circuit de la pompe, capteur de pression sur le réservoir. Chaque nuit, entre 0 h et 5 h, la pompe démarre en moyenne 2,3 fois par heure : c’est la référence de ce puits."),
             ("Les démarrages nocturnes triplent.",
              f"Neuf démarrages par heure la nuit, sans eau consommée au compteur. Écart de +{NB}290{NB}% contre la référence des 30 nuits : JARVIS ouvre une enquête."),
             ("Vanne de la maison fermée 15 minutes.",
              f"À 2 h, JARVIS ferme la vanne motorisée et suit la pression : de 58 à 16{NB}psi en 15{NB}minutes. Avec la maison isolée, l’eau ne peut repartir que vers le puits."),
             ("Clapet de pied qui fuit.", "Le retour d’eau vers le puits explique les démarrages répétés. Fuite dans la maison écartée par le test."),
             ("Bon de travail envoyé au puisatier.", ""),
             ("Clapet remplacé le lendemain.", f"Le puisatier arrive avec la pièce et le dossier. Intervention de 2{NB}h{NB}10, notée au journal par l’extension Entreprise."),
             ("2,2 démarrages par heure, comme avant.",
              f"Sept nuits de suite dans la plage normale; la vanne fermée, la pression ne bouge plus (0,1{NB}psi/min). JARVIS ferme le dossier."),
             ("Rapport joint au dossier du puits.", ""),
         ],
         conf=87, why=[("Démarrages nocturnes", "+ 290 % contre la référence", 34), ("Compteur d’eau", "0 L consommé", 22),
                       ("Test vanne fermée", "−2,8 psi/min", 31)],
         alt=[("Fuite dans la maison", "écartée par le test"), ("Pressostat déréglé", "consigne inchangée")],
         bon=dict(ref="BT-2611-031", to="Puisatier", role="Fournisseur no 4 · zone rurale", task="Remplacer le clapet de pied, vérifier la conduite de descente.",
                  pieces="Clapet de pied 1¼ po, raccords", when="Demain 8 h · confirmé", rule="Règle approuvée : envoi automatique si la confiance dépasse 80 %"),
         rep=[("Durée de l’enquête", "11 min, de l’alerte au bon"), ("Temps d’arrêt", "Aucun"), ("Retour vérifié", "7 nuits dans la plage"),
              ("Pièces", "Clapet de pied")],
         cost=[("Pompe usée prématurément (démarrages ×4)", 1800), ("Appel d’urgence de fin de semaine évité", 350), ("Électricité gaspillée, 1 an", 160)]),
    dict(id="tank", env="Ferme", t="Tank à lait", photo="tank-lait", ph="Réservoir à lait réfrigéré et son groupe compresseur",
         c=C("line", "min", [0, 240], _P_TANK, ("Il y a 15 jours", "Aujourd’hui"), band=[80, 120], thr=120, thr_lab="Objectif 2 h",
             anom=11, dec=0, name="Minutes pour passer sous 4 °C"),
         at=dict(meas=8, dev=15, test=18, fix=21, back=27),
         st=[
             ("La température du lait, aux 30 secondes.",
              f"Sonde dans le tank, pince sur le compresseur, deux sondes au condenseur. Après chaque traite, le lait passe de 35 à 4{NB}°C en 1{NB}h{NB}40 environ."),
             ("Trois traites de suite au-dessus de 2 h.",
              f"La pente de refroidissement s’adoucit traite après traite : −0,12{NB}°C/min au lieu de −0,25. Tendance confirmée sur 20 traites."),
             ("Mesure du condenseur à la traite suivante.",
              f"Compresseur à 11,2{NB}A, normal. Écart d’air à travers le condenseur : 6{NB}°C au lieu de 14{NB}°C. La chaleur sort mal."),
             ("Condenseur encrassé.", "Le compresseur travaille bien; c’est l’échange de chaleur qui faiblit. Poussière et paille, fréquent en automne."),
             ("Bon de travail envoyé au frigoriste.", ""),
             ("Condenseur nettoyé entre deux traites.", f"Intervention de 50{NB}min, sans interrompre la production. Photos avant et après jointes au bon."),
             ("1 h 40 de nouveau sous 4 °C.",
              f"Six traites de suite sous l’objectif; écart au condenseur revenu à 14{NB}°C. JARVIS ferme le dossier."),
             ("Rapport joint au carnet du tank.", ""),
         ],
         conf=82, why=[("Durée de refroidissement", "+ 110 % en 15 jours", 30), ("Écart au condenseur", "6 °C au lieu de 14 °C", 36),
                       ("Courant du compresseur", "normal : 11,2 A", 16)],
         alt=[("Compresseur faible", "courant normal"), ("Charge de réfrigérant", "pressions à confirmer sur place")],
         bon=dict(ref="BT-2611-044", to="Frigoriste agricole", role="Fournisseur no 2 · contrat d’entretien", task="Nettoyer le condenseur, vérifier le ventilateur et la charge de réfrigérant.",
                  pieces="Aucune prévue · nettoyant à condenseur", when="Aujourd’hui 14 h · entre deux traites", rule="Règle approuvée : priorité haute pour le tank à lait"),
         rep=[("Durée de l’enquête", "2 traites"), ("Lait perdu", "Aucun"), ("Retour vérifié", "6 traites sous 2 h"), ("Énergie", "−22 % par traite")],
         cost=[("Lait déclassé si la tendance continuait (1 tank)", 5100), ("Compresseur surmené, usure évitée", 1500), ("Électricité gaspillée, 1 an", 420)]),
    dict(id="lfp", env="Véhicule", t="Batteries LiFePO₄", photo="batteries-lifepo4", ph="Banc de batteries LiFePO₄ et son BMS",
         c=C("line", "mV", [0, 160], _P_LFP, ("Il y a 30 charges", "Aujourd’hui"), band=[0, 30], thr=50, thr_lab="Seuil 50 mV",
             anom=9, dec=0, name="Écart entre cellules en fin de charge"),
         at=dict(meas=6, dev=13, test=17, fix=21, back=27),
         st=[
             ("Chaque cellule, lue par le BMS.",
              f"Seize cellules, quatre batteries de 12{NB}V. À chaque fin de charge, JARVIS note l’écart entre la plus haute et la plus basse : 16{NB}mV en moyenne."),
             ("L’écart dépasse 50 mV et grandit.",
              f"La cellule 3 monte toujours la première. Écart de 141{NB}mV à la dernière charge, en hausse depuis 12 charges."),
             ("Impulsion de 50 A pendant 10 secondes.",
              f"Moteur arrêté, à l’arrêt, JARVIS demande au chargeur une impulsion et mesure la chute de tension de chaque cellule : résistance interne calculée."),
             ("Cellule 3 affaiblie.", f"Résistance de 0,41{NB}mΩ, contre 0,25{NB}mΩ pour ses voisines. Capacité estimée à −18{NB}%."),
             ("Bon de travail envoyé au technicien 12 V.", ""),
             ("Équilibrage, puis cellule remplacée.", "Équilibrage actif d’abord : l’écart revient en deux charges. Le technicien remplace la cellule 3 à l’atelier."),
             ("Écart de 16 mV, comme avant.",
              f"Six charges de suite sous 30{NB}mV; résistance de la nouvelle cellule : 0,24{NB}mΩ. JARVIS ferme le dossier."),
             ("Rapport joint au carnet du véhicule.", ""),
         ],
         conf=91, why=[("Écart entre cellules", "141 mV, en hausse", 32), ("Toujours la même cellule", "cellule 3, 12 charges sur 12", 25),
                       ("Résistance interne", "+ 64 % contre ses voisines", 34)],
         alt=[("Capteur du BMS", "lecture vérifiée par le chargeur"), ("Connexion desserrée", "écart présent sans courant")],
         bon=dict(ref="BT-2611-052", to="Technicien 12 V", role="Fournisseur no 7 · atelier mobile", task="Équilibrage actif; remplacer la cellule 3 si l’écart revient.",
                  pieces="Cellule LiFePO₄ 3,2 V 280 Ah, barres de liaison", when="Jeudi 9 h · au camping", rule="Règle approuvée : vous confirmez tout bon de plus de 200 $"),
         rep=[("Durée de l’enquête", "3 charges"), ("Panne en voyage", "Évitée"), ("Retour vérifié", "6 charges sous 30 mV"), ("Pièces", "1 cellule")],
         cost=[("Banc complet remplacé au lieu d’une cellule", 2960), ("Remorquage et nuit d’hôtel en panne", 650), ("Aliments perdus au réfrigérateur", 180)]),
]

# ---------------------------------------------------------------------------
# Santé des équipements : score, durée de vie restante, prochain entretien
# ---------------------------------------------------------------------------
# nom, lieu, score, tendance (12 mois), durée de vie restante, prochain entretien, source (type, détail), facteurs
ASSETS = [
    ("Disque 2 du serveur", "Bureau · baie TI", 18, [96, 96, 95, 95, 94, 94, 93, 92, 80, 52, 31, 18], "2 à 6 semaines",
     "Remplacer · cette semaine", ("Mesure", "SMART : 56 secteurs réalloués"), "Vitesse de réallocation, autotest échoué"),
    ("Batteries LiFePO₄", "Véhicule aménagé", 64, [94, 93, 93, 92, 91, 90, 88, 84, 78, 70, 66, 64], "6 à 8 ans",
     "Équilibrage · jeudi 12 nov.", ("Mesure", "Écart de cellules, résistance interne"), "Cellule 3 : +64 % de résistance"),
    ("Tank à lait", "Ferme · laiterie", 71, [90, 90, 89, 89, 88, 88, 87, 86, 83, 79, 74, 71], "9 à 12 ans",
     "Nettoyage du condenseur · aujourd’hui", ("Mesure", "Courbe de refroidissement"), "Pente de refroidissement −52 %"),
    ("Pompe de puits", "Ferme · puits", 76, [88, 88, 87, 87, 86, 86, 85, 84, 80, 74, 75, 76], "5 à 8 ans",
     "Clapet de pied · lundi 9 nov.", ("Mesure", "Démarrages nocturnes, chute de pression"), "Démarrages ×4 depuis 3 semaines"),
    ("Onduleur de la baie", "Bureau · baie TI", 58, [92, 90, 88, 85, 82, 79, 75, 71, 67, 63, 60, 58], "Batteries : 1 à 2 mois",
     "Batteries · 20 nov.", ("Mesure", "Autonomie 9 min à 38 % de charge"), "Autonomie −63 % en trois mois"),
    ("Génératrice 22 kW", "Maison · extérieur", 83, [94, 94, 93, 93, 92, 92, 91, 90, 89, 87, 85, 83], "12 à 15 ans",
     "Entretien 200 h · 4 déc.", ("Fabricant", "Aux 200 h ou chaque année"), "Démarrage plus lent : 18 s"),
    ("Thermopompe centrale", "Maison · sous-sol", 79, [91, 91, 90, 90, 89, 89, 88, 87, 86, 84, 81, 79], "8 à 11 ans",
     "Recherche de fuite · 16 nov.", ("Mesure", "ΔT et cycles courts"), "ΔT de 6 °C au lieu de 12 °C"),
    ("Chambre froide", "Épicerie · arrière-boutique", 92, [90, 90, 91, 90, 91, 64, 88, 91, 92, 92, 92, 92], "10 à 14 ans",
     "Inspection annuelle · 15 janv.", ("Calendrier", "Contrat d’entretien annuel"), "Ventilateur remplacé, cycles normaux"),
    ("Ventilation de l’étable", "Ferme · étable", 74, [89, 89, 88, 88, 87, 87, 86, 85, 84, 80, 76, 74], "Courroie : 2 semaines",
     "Courroie du ventilateur 3 · 13 nov.", ("Mesure", "Vitesse contre consigne"), "Ventilateur 3 à 62 % de la consigne"),
    ("Pneus du VR", "Véhicule aménagé", 69, [86, 86, 85, 84, 84, 83, 82, 80, 79, 77, 73, 69], "3 ans · 28 000 km",
     "Réparation arrière gauche · 10 nov.", ("Mesure", "Pression à froid, pneu jumeau"), "Fuite lente de 1,4 psi par jour"),
    ("Détecteurs de fumée", "Maison · 9 détecteurs", 88, [97, 97, 96, 96, 96, 95, 95, 94, 93, 92, 90, 88], "Cuisine : à remplacer",
     "Pile du corridor · 14 nov.", ("Règlement", "Fin de vie : 10 ans"), "Une pile basse, un détecteur de 10 ans"),
    ("Panneaux solaires", "Maison · toiture", 81, [97, 97, 96, 96, 95, 94, 92, 90, 88, 86, 83, 81], "20 ans et plus",
     "Inspection chaîne 2 · 24 nov.", ("Mesure", "Rendement contre ensoleillement prévu"), "Chaîne 2 à 78 % de l’attendu"),
    ("Compresseur d’air", "Atelier", 85, [93, 93, 92, 92, 91, 91, 90, 89, 88, 87, 86, 85], "7 à 9 ans",
     "Huile et filtres · 2 000 h, 30 nov.", ("Fabricant", "Aux 2 000 h de marche"), "Fuite zone B réparée"),
    ("Porte de garage", "Maison · garage", 77, [90, 90, 89, 89, 88, 87, 86, 85, 83, 81, 79, 77], "Roulettes : 1 à 3 mois",
     "Roulettes et rail · 21 nov.", ("Mesure", "Profil de courant de la course"), "Pic de 6,1 A à 70 % de la course"),
]

SOURCE_INFO = {
    "Mesure": "Calculé à partir des mesures de l’équipement",
    "Fabricant": "Intervalle recommandé par le fabricant",
    "Calendrier": "Contrat ou calendrier d’entretien",
    "Règlement": "Exigence réglementaire ou de sécurité",
}


def _photo(name, alt):
    rel = f"media/diagnostic/{name}.webp"
    if os.path.exists(os.path.join(_ROOT, rel)):
        return f'<img class="dgx-ph" src="/{rel}" alt="{alt}" loading="lazy" decoding="async">'
    return (f'<span class="dgx-ph dgx-noph" role="img" aria-label="{alt} · photo à venir">'
            f'<i aria-hidden="true"></i><small>Photo à venir</small></span>')


def _money(v):
    return f"{v:,}".replace(",", NB) + f"{NB}$"


def _health_cls(s):
    return "ok" if s >= 80 else ("warn" if s >= 60 else "bad")


def _lib_html():
    count = {k: sum(1 for d in DIAGS if d["env"] == k) for k, _ in ENVS}
    chips = (f'<button type="button" data-env="all" aria-pressed="true">Tous <small>{len(DIAGS)}</small></button>'
             + "".join(f'<button type="button" data-env="{k}" aria-pressed="false">{lab} <small>{count[k]}</small></button>'
                       for k, lab in ENVS))
    items = "".join(
        f'<li data-env="{d["env"]}"><button type="button" data-diag="{d["id"]}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'<span class="dgl-i-env">{ENV_LAB[d["env"]]}</span><b>{d["t"]}</b>'
        f'<span class="dgl-i-m">{escape(d["c"]["n"])}{" · " + d["c"]["u"] if d["c"]["u"] else ""}</span></button></li>'
        for i, d in enumerate(DIAGS)
    )

    def card(i, d):
        tags = "".join(f'<span class="dgl-tag">{m}</span>' for m in d["m"])
        rows = [
            ("mes", "Ce qui est mesuré", d["mes"]),
            ("norm", "Plage normale", d["norm"]),
            ("sig", "Signature de l’anomalie", d["sig"]),
            ("how", "Comment JARVIS le détecte", f'<span class="dgl-tags">{tags}</span>{d["how"]}'),
            ("test", "Test automatique de confirmation", d["test"]),
            ("res", "Résultat", d["res"]),
        ]
        dl = "".join(f'<div class="dgl-r dgl-r-{k}"><dt>{t}</dt><dd>{v}</dd></div>' for k, t, v in rows)
        to, task = d["bon"]
        return f"""<article class="dgl-card" data-diag="{d['id']}"{'' if i == 0 else ' data-off'}>
        <header><p class="dgl-env">{ENV_LAB[d['env']]} · diagnostic {i + 1:02d}</p><h4>{d['t']}</h4><p class="dgl-eq">{d['e']}</p></header>
        <div class="dgl-chart" role="img" aria-label="{escape(d['c']['n'])} : courbe d’exemple, plage normale et signature de l’anomalie"><svg class="dgx-svg" xmlns="http://www.w3.org/2000/svg"></svg></div>
        <dl class="dgl-spec">{dl}</dl>
        <footer class="dgl-bon"><span class="dgl-bon-k">Bon de travail</span><b>{to}</b><span>{task}</span></footer>
      </article>"""

    cards = "".join(card(i, d) for i, d in enumerate(DIAGS))
    methods = "".join(
        f'<li><b>{m}</b><span>{t}</span></li>' for m, t in [
            (M_SEUIL, "La mesure franchit une limite fixe : 82 °C, 2,8 V, 50 mV."),
            (M_TEND, "La mesure glisse jour après jour; JARVIS projette quand elle franchira la limite."),
            (M_REF, "La mesure s’éloigne de l’historique de cet équipement, ou de son jumeau."),
            (M_CORR, "Deux mesures qui devraient bouger ensemble se séparent."),
        ])
    return f"""<div class="dgx-sect dgl" data-rev>
    <div class="dgx-head">
      <p class="eyebrow">La bibliothèque</p>
      <h3>{len(DIAGS)} diagnostics précis, <em>chacun avec ses chiffres.</em></h3>
      <p>Pour chaque équipement : le capteur et son unité, la plage normale, la signature d’une panne, la façon dont JARVIS la repère,
      le test qu’il lance pour la confirmer et la personne qui reçoit le bon de travail.</p>
    </div>
    <ul class="dgl-methods" aria-label="Les quatre façons de détecter un écart">{methods}</ul>
    <div class="dgl-filters" role="group" aria-label="Filtrer par environnement">{chips}</div>
    <div class="dgl-body">
      <ul class="dgl-list" aria-label="Diagnostics">{items}</ul>
      <div class="dgl-cards" aria-live="polite">{cards}</div>
    </div>
    <p class="dgx-note">Données d’exemple · valeurs typiques, à ajuster à chaque équipement pendant la mise en service.</p>
  </div>"""


def _loop_html():
    tabs = "".join(
        f'<button type="button" data-loop="{c["id"]}" aria-pressed="{"true" if i == 0 else "false"}"><small>{c["env"]}</small><b>{c["t"]}</b></button>'
        for i, c in enumerate(CASES2))
    rail = "".join(f'<li data-i="{i}"><button type="button" data-st="{i}"><i>{i + 1}</i><span>{t}</span></button></li>'
                   for i, t in enumerate(LOOP))

    def case(i, c):
        hid = "" if i == 0 else " hidden"
        panes = []
        for j, (h, p) in enumerate(c["st"]):
            extra = ""
            if j == 3:
                why = "".join(f'<li style="--w:{w}"><span>{a}</span><b>{b}</b><i aria-hidden="true"></i></li>' for a, b, w in c["why"])
                alt = "".join(f'<li><s>{a}</s><span>{b}</span></li>' for a, b in c["alt"])
                extra = f"""<div class="dgo-conf">
                  <div class="dgo-ring" style="--c:{c['conf']}" role="img" aria-label="Niveau de confiance {c['conf']} %"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="t" cx="60" cy="60" r="52"/><circle class="v" cx="60" cy="60" r="52" pathLength="100"/></svg><b data-n="{c['conf']}">{c['conf']}</b><small>% de confiance</small></div>
                  <div><p class="dgo-mini">Ce qui pèse dans la balance</p><ul class="dgo-why">{why}</ul>
                  <p class="dgo-mini">Hypothèses écartées</p><ul class="dgo-alt">{alt}</ul></div></div>"""
            elif j == 4:
                b = c["bon"]
                extra = f"""<div class="dgo-wo">
                  <div class="dgo-wo-route" aria-hidden="true"><span class="n">JARVIS</span><i class="w"><i></i></i><span class="n">Entreprise</span><i class="w"><i></i></i><span class="n">{b['to']}</span></div>
                  <div class="dgo-wo-card">
                    <header><b>Bon de travail · {b['ref']}</b><small>Envoyé par l’extension Entreprise</small></header>
                    <dl><div><dt>Destinataire</dt><dd>{b['to']} · {b['role']}</dd></div><div><dt>Travail</dt><dd>{b['task']}</dd></div>
                    <div><dt>Pièces à apporter</dt><dd>{b['pieces']}</dd></div><div><dt>Rendez-vous</dt><dd>{b['when']}</dd></div></dl>
                    <footer><span class="dgo-wo-ok">Reçu et accepté</span><small>{b['rule']}</small></footer>
                  </div></div>"""
            elif j == 7:
                rep = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in c["rep"])
                tot = sum(v for _, v in c["cost"])
                cost = "".join(f'<li><span>{a}</span><b>{_money(v)}</b></li>' for a, v in c["cost"])
                extra = f"""<div class="dgo-rep">
                  <dl class="dgo-rep-dl">{rep}</dl>
                  <div class="dgo-cost"><p class="dgo-mini">Coûts évités <em>estimation</em></p><ul>{cost}</ul>
                  <p class="dgo-tot"><span>Total estimé</span><b data-n="{tot}">{_money(tot)}</b></p>
                  <p class="dgo-est">Estimation à partir de prix typiques du marché, données d’exemple. Ce n’est pas une garantie.</p></div></div>"""
            panes.append(f'<section class="dgo-pane" data-i="{j}"{"" if j == 0 else " data-off"}><p class="dgo-k">Étape {j + 1} sur 8 · {LOOP[j]}</p>'
                         f'<h4>{h}</h4>{f"<p>{p}</p>" if p else ""}{extra}</section>')
        return f"""<div class="dgo-case" data-loop="{c['id']}"{hid}>
        <div class="dgo-viz">
          <div class="dgo-media">{_photo(c['photo'], c['ph'])}<div class="dgo-media-t"><small>{c['env']} · données d’exemple</small><b>{c['t']}</b></div></div>
          <div class="dgo-chart" role="img" aria-label="{escape(c['c']['n'])} : de la mesure au retour à la normale"><svg class="dgx-svg" xmlns="http://www.w3.org/2000/svg"></svg></div>
        </div>
        <div class="dgo-panes">{''.join(panes)}</div>
      </div>"""

    cases = "".join(case(i, c) for i, c in enumerate(CASES2))
    return f"""<div class="dgx-sect dgo" data-rev>
    <div class="dgx-head">
      <p class="eyebrow">La boucle complète</p>
      <h3>De la mesure au rapport, <em>sans maillon manquant.</em></h3>
      <p>Trois cas réels de terrain, rejoués étape par étape : JARVIS mesure, repère l’écart, le confirme par un test,
      chiffre sa confiance, envoie le bon de travail au bon technicien par l’extension Entreprise, puis prouve le retour à la normale.</p>
    </div>
    <div class="dgo-shell">
      <div class="dgo-top">
        <div class="dgo-tabs" role="group" aria-label="Choisir un cas">{tabs}</div>
        <div class="dgo-ctrl"><button type="button" data-lp="play" aria-pressed="true"><i class="dg-pp" aria-hidden="true"></i><span class="on">Lecture auto</span><span class="off">En pause</span></button>
        <button type="button" data-lp="replay"><span aria-hidden="true">↻</span> Rejouer</button></div>
      </div>
      <ol class="dgo-rail" aria-label="Les huit étapes de la boucle">{rail}</ol>
      {cases}
    </div>
    <p class="dgx-note">Données d’exemple · les coûts évités sont des estimations, pas des garanties.</p>
  </div>"""


def _health_html():
    n = len(ASSETS)
    bad = sum(1 for a in ASSETS if a[2] < 60)
    warn = sum(1 for a in ASSETS if 60 <= a[2] < 80)
    month = 9
    saved = sum(v for c in CASES2 for _, v in c["cost"])
    kpis = [("Équipements suivis", str(n), "dans 6 lieux"), ("À remplacer", str(bad), "score sous 60"),
            ("À surveiller", str(warn), "score de 60 à 79"), ("Entretiens ce mois-ci", str(month), "planifiés automatiquement"),
            ("Coûts évités cette année", _money(saved), "estimation")]
    kp = "".join(f'<div class="dgh-kpi"><small>{a}</small><b>{b}</b><span>{c}</span></div>' for a, b, c in kpis)
    rows = []
    for i, (name, place, s, tr, rul, nxt, (src, srcd), why) in enumerate(sorted(ASSETS, key=lambda a: a[2])):
        cls = _health_cls(s)
        lo, hi = min(min(tr) - 6, 50), 100
        pts = " ".join(f"{k * 100 / (len(tr) - 1):.1f},{28 - (v - lo) * 26 / (hi - lo):.1f}" for k, v in enumerate(tr))
        rows.append(f"""<tr data-score="{s}" class="is-{cls}">
          <th scope="row"><b>{name}</b><small>{place}</small></th>
          <td class="dgh-score"><span class="dgh-ring" style="--s:{s}" aria-label="Score de santé {s} sur 100"><b>{s}</b></span>
            <svg class="dgh-spark" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true"><polyline points="{pts}"/></svg></td>
          <td class="dgh-rul"><b>{rul}</b><small>{why}</small></td>
          <td class="dgh-next"><b>{nxt}</b></td>
          <td class="dgh-src"><span class="dgh-badge" data-src="{src}" title="{SOURCE_INFO[src]}">{src}</span><small>{srcd}</small></td>
        </tr>""")
    legend = "".join(f'<li><span class="dgh-badge" data-src="{k}">{k}</span>{v}</li>' for k, v in SOURCE_INFO.items())
    return f"""<div class="dgx-sect dgh" data-rev>
    <div class="dgx-head">
      <p class="eyebrow">Santé des équipements</p>
      <h3>Chaque équipement a un score, <em>une durée de vie et une date.</em></h3>
      <p>Le score combine l’âge, les mesures et l’historique des pannes. La durée de vie restante est une estimation qui se resserre
      avec les mois de mesures; la source de chaque entretien est toujours indiquée.</p>
    </div>
    <div class="dgh-board">
      <div class="dgh-kpis">{kp}</div>
      <div class="dgh-tools" role="group" aria-label="Trier">
        <span>Trier par</span><button type="button" data-sort="score" aria-pressed="true">Santé</button><button type="button" data-sort="name" aria-pressed="false">Nom</button>
      </div>
      <div class="dgh-wrap"><table class="dgh-t">
        <thead><tr><th scope="col">Équipement</th><th scope="col">Santé · 12 mois</th><th scope="col">Durée de vie restante</th><th scope="col">Prochain entretien</th><th scope="col">Source</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table></div>
      <ul class="dgh-legend">{legend}</ul>
    </div>
    <p class="dgx-note">Données d’exemple · scores et durées de vie estimés, mis à jour à chaque nouvelle mesure.</p>
  </div>"""


XDATA = json.dumps({"lib": {d["id"]: d["c"] for d in DIAGS},
                    "loop": {c["id"]: dict(c["c"], at=c["at"]) for c in CASES2}},
                   ensure_ascii=False, separators=(",", ":"))

EXTRA = f"""<div class="dgx" data-dgx>
  {_lib_html()}
  {_loop_html()}
  {_health_html()}
  <script type="application/json" class="dgx-data">{XDATA}</script>
</div>"""
