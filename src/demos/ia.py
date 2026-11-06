# Démo interactive « IA privée et connaissances » (assets/demos/ia.css et ia.js).
# Une seule source de vérité : les scénarios ci-dessous produisent à la fois
# l'état statique (lisible sans JavaScript : la première question déjà répondue)
# et les gabarits <template> que le script anime. Données entièrement fictives.

import re

NBSP = " "


def fr(s):
    """Espaces insécables de la typographie française (montants, heures, deux-points)."""
    s = re.sub(r"(\d) (\d{3})", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) (\$|h\b|%|s\b|minutes|ans\b|pages?\b)", rf"\1{NBSP}\2", s)
    return s.replace(" :", NBSP + ":").replace(" —", NBSP + "—")


# Les six documents fictifs de l'atelier : (id, type, nom, détail, passages indexés)
DOCS = [
    ("d1", "pdf", "Procédure de fermeture.pdf", "Atelier · 4 pages", 48),
    ("d2", "xls", "Registre des alarmes.xlsx", "Codes et zones", 64),
    ("d3", "mail", "Courriels de l’équipe", "Boîte partagée · 2026", 1180),
    ("d4", "pdf", "Contrat thermopompe.pdf", "Installation · garantie", 36),
    ("d5", "xls", "Carnet d’entretien.xlsx", "Bâtiment · 2019 à 2025", 52),
    ("d6", "pdf", "Soumission Tremblay.pdf", "S-2026-031 · 2 pages", 18),
]
TYPE_LABEL = {"pdf": "PDF", "xls": "XLSX", "mail": "Courriel"}
TYPE_ICON = {"pdf": "PDF", "xls": "XLS", "mail": "@"}
DOC = {d[0]: d for d in DOCS}

SCENARIOS = [
    {
        "chip": "Fermeture du vendredi",
        "q": "Quelle est la procédure de fermeture de l’atelier le vendredi?",
        "blocks": [
            ("p", "Le vendredi, la fermeture se fait en quatre étapes :"),
            ("ol", [
                "Couper l’alimentation des compresseurs et des chargeurs [1].",
                "Ranger les outils portatifs dans l’armoire verrouillée [1].",
                "Armer l’alarme en zone B — la zone A est réservée aux fins de semaine de garde [2].",
                "Envoyer à Marie une photo du tableau électrique avant 17 h [3].",
            ]),
        ],
        "sources": [
            {"n": 1, "doc": "d1", "loc": "page 2", "head": "4. Fermeture de fin de semaine",
             "text": "Le vendredi, couper l’alimentation des compresseurs et des chargeurs, puis ranger les outils portatifs dans l’armoire verrouillée."},
            {"n": 2, "doc": "d2", "loc": "onglet Zones", "head": "Zones d’alarme du bâtiment",
             "text": "Zone B : fermeture de semaine, y compris le vendredi. Zone A : réservée aux fins de semaine de garde."},
            {"n": 3, "doc": "d3", "loc": "courriel du 12 septembre", "head": "De : Marie · Objet : Fermeture du vendredi",
             "text": "À partir de maintenant, envoyez-moi une photo du tableau électrique avant 17 h chaque vendredi."},
        ],
        "secs": "1,2 s",
        "action": {
            "title": "Créer la liste de tâches de vendredi",
            "sub": "4 tâches pour l’équipe atelier, dans votre outil Tâches.",
            "items": ["Couper compresseurs et chargeurs", "Ranger les outils portatifs",
                      "Armer l’alarme en zone B", "Photo du tableau à Marie avant 17 h"],
            "done": "4 tâches créées pour l’équipe atelier.",
        },
    },
    {
        "chip": "Garantie de la thermopompe",
        "q": "Quand expire la garantie de la thermopompe?",
        "blocks": [
            ("p", "La garantie des pièces expire le 14 juin 2029 : elle couvre 10 ans à partir de l’installation du 14 juin 2019 [1]."),
            ("p", "Une condition : un entretien annuel par un technicien certifié, sinon la garantie tombe [1]. Le dernier entretien inscrit date du 3 décembre 2025 [2] : le prochain est à faire avant le 3 décembre 2026."),
        ],
        "sources": [
            {"n": 1, "doc": "d4", "loc": "page 3", "head": "Article 7 — Garantie",
             "text": "Installation : 14 juin 2019. Pièces garanties 10 ans, à condition d’un entretien annuel par un technicien certifié."},
            {"n": 2, "doc": "d5", "loc": "ligne 14", "head": "Thermopompe — historique des entretiens",
             "text": "3 décembre 2025 · Entretien annuel complet · Technicien certifié · Prochain : décembre 2026."},
        ],
        "secs": "0,9 s",
        "action": {
            "title": "Ajouter un rappel d’entretien",
            "sub": "Le 19 novembre, deux semaines avant l’échéance, dans le calendrier de l’atelier.",
            "items": [],
            "done": "Rappel ajouté au calendrier pour le 19 novembre.",
        },
    },
    {
        "chip": "Promesses au client Tremblay",
        "q": "Qu’a-t-on promis au client Tremblay?",
        "blocks": [
            ("p", "Trois engagements, tous écrits :"),
            ("ol", [
                "Installer 4 caméras extérieures et un enregistreur local, pour 3 480 $ avant taxes [1].",
                "Terminer les travaux au plus tard le 21 novembre [2].",
                "Offrir une formation de 30 minutes sur l’application, sans frais [2].",
            ]),
        ],
        "sources": [
            {"n": 1, "doc": "d6", "loc": "page 1", "head": "Soumission S-2026-031 — M. Tremblay",
             "text": "4 caméras extérieures et 1 enregistreur local, installation comprise : 3 480 $ avant taxes."},
            {"n": 2, "doc": "d3", "loc": "courriel du 22 octobre", "head": "À : M. Tremblay · Objet : Confirmation des travaux",
             "text": "Nous terminerons au plus tard le 21 novembre et vous offrons une formation de 30 minutes sur l’application, sans frais."},
        ],
        "secs": "1,0 s",
        "action": {
            "title": "Envoyer à M. Tremblay le rappel des engagements",
            "sub": "Courriel préparé à partir des 2 sources. Il part seulement si vous approuvez.",
            "items": [],
            "done": "Courriel remis à M. Tremblay.",
        },
    },
    {
        "chip": "Remboursement sans reçu",
        "trap": True,
        "q": "Peut-on rembourser un client qui n’a pas de reçu?",
        "blocks": [
            ("warn", "Je ne trouve pas de source fiable pour répondre."),
            ("p", "Aucun de vos 6 documents ne parle de remboursement sans reçu. Plutôt que d’inventer une règle, je peux poser la question à la bonne personne."),
        ],
        "sources": [],
        "secs": "1,1 s",
        "action": {
            "title": "Demander la règle à Marie, la gérante",
            "sub": "Message interne préparé. Sa réponse pourra devenir une procédure écrite.",
            "items": [],
            "done": "Question transmise à Marie.",
        },
    },
]

SKELETON = [(94, 86, 72), (90, 64), (97, 82, 58), (88, 70)]

ICON_LOCK = (
    '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="2"/>'
    '<path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>'
)
ICON_SEND = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5"/></svg>'
ICON_SPARK = (
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5 9.4 6.6 14.5 8 9.4 9.4 8 14.5 6.6 9.4 1.5 8 6.6 6.6z"/></svg>'
)
ICON_REPLAY = (
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 8a5.5 5.5 0 1 0 1.7-4"/><path d="M2.5 2.5v3h3"/></svg>'
)
ICON_WARN ='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2 15 14H1z"/><path d="M8 6.5v3.5M8 12v.01"/></svg>'


def cites(text):
    """« [1] » devient un bouton de citation cliquable."""
    return re.sub(
        r" ?\[(\d)\]",
        r' <button type="button" class="ia-cite" data-c="\1" aria-label="Voir la source \1">\1</button>',
        fr(text),
    )


def answer(sc):
    out = []
    for kind, body in sc["blocks"]:
        if kind == "ol":
            out.append("<ol>" + "".join(f"<li>{cites(t)}</li>" for t in body) + "</ol>")
        elif kind == "warn":
            out.append(f'<p class="ia-warn">{ICON_WARN}<strong>{fr(body)}</strong></p>')
        else:
            out.append(f"<p>{cites(body)}</p>")
    return "".join(out)


def meta(sc):
    n = len(sc["sources"])
    src = (
        f'<span class="ia-badge is-src">{n} source{"s" if n > 1 else ""} · {sc["secs"]}</span>'
        if n else f'<span class="ia-badge is-warn">0 source fiable · rien d’inventé</span>'
    )
    return (
        f'<div class="ia-meta"><span class="ia-badge is-ok">{ICON_LOCK}Modèle local · aucune donnée envoyée à l’extérieur</span>'
        f'{src}</div>'
    )


def action(sc, i):
    a = sc["action"]
    items = "".join(f"<li>{fr(t)}</li>" for t in a["items"])
    items = f'<ul class="ia-act-list">{items}</ul>' if items else ""
    return f"""<div class="ia-act" data-act>
  <p class="ia-act-k">{ICON_SPARK}JARVIS propose · en attente de votre accord</p>
  <h4>{fr(a['title'])}</h4>
  <p class="ia-act-sub">{fr(a['sub'])}</p>
  {items}
  <div class="ia-act-btns">
    <button type="button" class="ia-ok" data-do="ok">Approuver</button>
    <button type="button" class="ia-no" data-do="no">Ignorer</button>
    <span class="ia-act-note">Rien ne part sans votre accord.</span>
  </div>
  <ol class="ia-track" aria-label="Suivi de l’action">
    <li data-s="1">Approuvé</li><li data-s="2">Envoyé</li><li data-s="3">Confirmé</li>
  </ol>
  <p class="ia-act-done" data-done="{fr(a['done'])}" role="status"></p>
</div>"""


def chat(sc, i):
    return f"""<div class="ia-msg is-me"><p class="ia-bub">{fr(sc['q'])}</p></div>
<div class="ia-msg is-bot">
  <span class="ia-av" aria-hidden="true"></span>
  <div class="ia-bub">
    <div class="ia-think" aria-hidden="true">
      <p><span>Recherche dans vos documents</span><i></i><i></i><i></i></p>
      <span class="ia-think-bar"></span>
      <small><b data-read>0</b> passages lus · 6 documents</small>
    </div>
    <div class="ia-ans">{answer(sc)}</div>
    {meta(sc)}
    <p class="ia-quote" hidden></p>
  </div>
</div>
{action(sc, i)}"""


def page(src, k):
    d = DOC[src["doc"]]
    sk = SKELETON[k % len(SKELETON)]
    before = "".join(f'<i class="ia-sk" style="--w:{w}%"></i>' for w in sk)
    after = "".join(f'<i class="ia-sk" style="--w:{w}%"></i>' for w in SKELETON[(k + 1) % len(SKELETON)] + SKELETON[(k + 2) % len(SKELETON)])
    return f"""<article class="ia-page" data-c="{src['n']}" data-doc="{src['doc']}">
  <header><span class="ia-ty is-{d[1]}">{TYPE_LABEL[d[1]]}</span><b>{fr(d[2])}</b><small>{fr(src['loc'])}</small></header>
  <h4>{fr(src['head'])}</h4>
  {before}
  <p class="ia-pass"><span>{fr(src['text'])}</span></p>
  {after}
</article>"""


def pages(sc):
    if not sc["sources"]:
        return """<article class="ia-page is-none">
  <p><b>Aucun passage fiable.</b> Aucun document ne répond à cette question : JARVIS ne cite rien plutôt que d’inventer.</p>
</article>"""
    return "".join(page(s, k) for k, s in enumerate(sc["sources"]))


def tabs(sc):
    return "".join(
        f'<button type="button" class="ia-tab" data-c="{s["n"]}"><span>{s["n"]}</span>'
        f'{fr(DOC[s["doc"]][2].rsplit(".", 1)[0])} · {fr(s["loc"])}</button>'
        for s in sc["sources"]
    )


def hits(sc):
    by = {}
    for s in sc["sources"]:
        by.setdefault(s["doc"], []).append(str(s["n"]))
    return "|".join(f"{d}:{','.join(n)}" for d, n in by.items())


def docs(sc=None):
    h = dict(x.split(":") for x in hits(sc).split("|")) if sc and sc["sources"] else {}
    out = []
    for d in DOCS:
        state = (" is-hit" if d[0] in h else " is-miss") if sc else ""
        out.append(
            f'<li class="ia-doc{state}" data-doc="{d[0]}" data-pass="{d[4]}">'
            f'<span class="ia-ty is-{d[1]}" aria-hidden="true">{TYPE_ICON[d[1]]}</span>'
            f'<span class="ia-doc-t"><b>{fr(d[2])}</b><small>{fr(d[3])}</small></span>'
            f'<em class="ia-hit">{h.get(d[0], "").replace(",", " ")}</em></li>'
        )
    return "".join(out)


def chips():
    out = []
    for i, sc in enumerate(SCENARIOS):
        trap = '<em>question piège</em>' if sc.get("trap") else ""
        on = " is-on" if i == 0 else ""
        out.append(
            f'<button type="button" class="ia-chip{on}" data-sc="{i}" aria-pressed="{"true" if i == 0 else "false"}">'
            f'{fr(sc["chip"])}{trap}</button>'
        )
    return "".join(out)


TOTAL = sum(d[4] for d in DOCS)

WELCOME = fr("""<div class="ia-msg is-bot" data-keep>
  <span class="ia-av" aria-hidden="true"></span>
  <p class="ia-bub">Bonjour. Je connais les 6 documents de l’atelier Démo. Choisissez une question :
  je réponds seulement avec ce que je peux prouver.</p>
</div>""")


def templates():
    return "".join(
        f'<template data-ia-sc="{i}" data-q="{fr(sc["q"])}" data-hits="{hits(sc)}">'
        f'<div data-part="chat">{chat(sc, i)}</div>'
        f'<div data-part="pages">{pages(sc)}</div>'
        f'<div data-part="tabs">{tabs(sc)}</div>'
        "</template>"
        for i, sc in enumerate(SCENARIOS)
    )


def render():
    first = SCENARIOS[0]
    total = f"{TOTAL:,}".replace(",", NBSP)
    return f"""<div class="demo-shell" data-demo="ia" data-rev>
  <div class="demo-top">
    <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
    <b>JARVIS · IA privée</b>
    <span class="ia-state"><i class="dot" aria-hidden="true"></i>Modèle local actif</span>
    <span class="tag tag-sim">Démo · données simulées</span>
  </div>
  <div class="demo-body ia">
    <div class="ia-chat">
      <div class="ia-head">
        <p class="ia-k">Conversation<span> · Atelier Démo</span></p>
        <p class="ia-lock">{ICON_LOCK}Rien ne quitte le Hub</p>
      </div>
      <div class="ia-log" data-log>
        {WELCOME}
        {chat(first, 0).replace('class="ia-think"', 'class="ia-think" hidden')}
      </div>
      <div class="ia-compose">
        <div class="ia-compose-top">
          <p class="ia-k">Choisissez une question</p>
          <button type="button" class="ia-replay" data-replay>{ICON_REPLAY}Rejouer</button>
        </div>
        <div class="ia-chips" role="group" aria-label="Questions proposées">{chips()}</div>
        <div class="ia-input">
          <span class="ia-typed" data-typed></span><span class="ia-ph" data-ph>Posez une question sur vos documents…</span>
          <span class="ia-send" aria-hidden="true">{ICON_SEND}</span>
        </div>
      </div>
      <p class="ia-sr" aria-live="polite" data-sr></p>
    </div>
    <div class="ia-src">
      <div class="ia-head">
        <p class="ia-k">Vos documents · 6</p>
        <p class="ia-count"><b data-count>{total}</b> passages lus</p>
      </div>
      <ul class="ia-docs" data-docs>{docs(first)}</ul>
      <div class="ia-prev">
        <p class="ia-k">Preuve · passage exact</p>
        <div class="ia-tabs" data-tabs>{tabs(first)}</div>
        <div class="ia-stack" data-stack>{pages(first).replace('class="ia-page" data-c="1"', 'class="ia-page is-on" data-c="1"', 1).replace('class="ia-pass"', 'class="ia-pass is-on"', 1)}</div>
      </div>
    </div>
    {templates()}
  </div>
</div>
<p class="demo-hint">Cliquez sur un numéro de source pour voir le passage exact · Documents et réponses fictifs</p>"""


HTML = render()
