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
            ], ["Courbe de 24 h", "Journal du compresseur", "Courant du ventilateur"]),
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
            ], ["Courbe de 24 h", "Journal de la batterie", "Coupures du réfrigérateur"]),
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
        chips = "".join(f'<span class="dg-att">{a}</span>' for a in att)
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
