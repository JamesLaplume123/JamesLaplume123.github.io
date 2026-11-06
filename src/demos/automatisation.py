# Démo interactive « Automatisation d'entreprise » (assets/demos/automatisation.css et .js).
# Une demande traverse cinq étapes : reçue → lue → règle → votre approbation →
# exécutée et journalisée. Les scénarios ci-dessous produisent l'état statique
# (lisible sans JavaScript : la demande d'achat déjà approuvée) et les gabarits
# <template> que le script anime. Données entièrement fictives.

import re

NBSP = " "


def fr(s):
    """Espaces insécables de la typographie française (montants, heures, deux-points)."""
    s = re.sub(r"(\d) (\d{3})", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) (\$|h\b|gal\.)", rf"\1{NBSP}\2", s)
    return s.replace(" :", NBSP + ":").replace(" ?", NBSP + "?")


ICONS = {
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "form": '<rect x="4.5" y="3" width="15" height="18" rx="2.5"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4"/>',
    "scan": '<path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><path d="M7.5 12h9"/>',
    "rule": '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    "warn": '<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.5M12 17v.01"/>',
    "user": '<circle cx="10" cy="8" r="3.6"/><path d="M3.5 20c.4-3.6 3.1-6 6.5-6 1.3 0 2.4.3 3.4.8"/><path d="m15 18 2 2 4-4.2"/>',
    "doc": '<path d="M14 3H7.5A2.5 2.5 0 0 0 5 5.5v13A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V8z"/><path d="M14 3v5h5"/><path d="m9 14.5 2 2 4-4"/>',
    "send": '<path d="M21 3 10 14"/><path d="M21 3 14.5 21 10 14 3 9.5z"/>',
}
REPLAY = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 8a5.5 5.5 0 1 0 1.7-4"/><path d="M2.5 2.5v3h3"/></svg>'


def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


SCENARIOS = [
    {
        "tab": "Demande d’achat",
        "lead": "Luc, sur le chantier, demande un compresseur par courriel. Suivez sa demande jusqu’au bon de commande.",
        "stages": [
            {"k": "mail", "icon": "mail", "label": "Courriel reçu",
             "say": "Un courriel arrive dans la boîte des achats.",
             "log": "Courriel reçu · boîte des achats", "sum": "Courriel de Luc, devis joint",
             "from": ("LB", "Luc Bérubé", "Chantier Lavoie · 9 h 12"),
             "subj": "Besoin d’un compresseur 60 gallons",
             "body": "Le nôtre a lâché. Peux-tu commander celui du devis joint? Il nous le faut pour le 14 novembre.",
             "att": "devis-2231.pdf"},
            {"k": "fields", "icon": "scan", "label": "JARVIS lit et extrait",
             "say": "JARVIS lit le courriel et le devis, puis remplit la demande. Personne ne recopie rien.",
             "log": "4 champs extraits du courriel et du devis", "sum": "4 champs remplis",
             "fields": [("Fournisseur", "Outillage Rive-Sud", ""), ("Montant", "1 284,50 $", ""),
                        ("Projet", "Chantier Lavoie", ""), ("Date requise", "14 novembre", "")],
             "note": "Lu dans le courriel et devis-2231.pdf"},
            {"k": "rule", "icon": "rule", "label": "Règle appliquée",
             "say": "Votre règle s’applique : au-delà de 500 $, le gérant doit approuver.",
             "log": "Règle « achat de plus de 500 $ » → approbation du gérant", "sum": "Plus de 500 $ → gérant",
             "rule": "Achat de plus de 500 $ → approbation du gérant",
             "eval": ("1 284,50 $", ">", "500 $"), "verdict": ("ask", "Approbation requise")},
            {"k": "approve", "icon": "user", "label": "Votre approbation",
             "say": "À vous : vous êtes le gérant. Rien ne part sans votre clic.",
             "log": "En attente de l’approbation du gérant",
             "ask": "Approuver l’achat de <b>1 284,50 $</b> chez Outillage Rive-Sud?",
             "ok": ("Approuver", "Approuvé par vous (gérant)"),
             "no": ("Refuser", "Refusé par vous (gérant) · aucune action")},
            {"k": "result", "icon": "doc", "label": "Bon de commande",
             "say": "Le bon de commande part au fournisseur, qui confirme. Tout est inscrit au journal.",
             "sum": "BC-0418 · confirmé",
             "doc": ("Bon de commande", "BC-0418", "Outillage Rive-Sud · 1 284,50 $ · livraison le 14 novembre"),
             "track": ("Créé", "Envoyé", "Confirmé"),
             "sent": "BC-0418 créé et envoyé à Outillage Rive-Sud",
             "conf": "Commande confirmée par le fournisseur",
             "skip": "Rien n’est commandé. La demande reste au dossier, avec votre refus."},
        ],
        "before": [(4, "outils"), (11, "clics"), (2, "jours")],
        "after": [(1, "approbation"), (40, "secondes")],
    },
    {
        "tab": "Nouveau client",
        "lead": "Une cliente remplit le formulaire de votre site. JARVIS crée sa fiche et prépare un courriel de bienvenue, que vous approuvez.",
        "stages": [
            {"k": "form", "icon": "form", "label": "Formulaire reçu",
             "say": "Une demande arrive par le formulaire de votre site web.",
             "log": "Formulaire reçu · site web", "sum": "Nadia Côté · caméras extérieures",
             "rows": [("Nom", "Nadia Côté"), ("Besoin", "Caméras extérieures"), ("Ville", "Saint-Hyacinthe")],
             "msg": "« Une soumission avant décembre, si possible. »"},
            {"k": "fields", "icon": "scan", "label": "Fiche client créée",
             "say": "JARVIS vérifie qu’elle n’est pas déjà cliente, puis crée sa fiche dans votre logiciel clients.",
             "log": "Nouvelle fiche client créée", "sum": "Fiche client créée",
             "fields": [("Cliente", "Nadia Côté · nouvelle", ""), ("Besoin", "Sécurité · 4 caméras", ""),
                        ("Échéance", "Avant le 1er décembre", ""), ("Responsable", "Équipe des ventes", "")],
             "note": "Aucune fiche existante à ce nom"},
            {"k": "rule", "icon": "rule", "label": "Règle appliquée",
             "say": "Votre règle : chaque nouveau client reçoit un mot de bienvenue, approuvé par une personne.",
             "log": "Règle « nouveau client » → courriel de bienvenue à approuver", "sum": "Bienvenue à approuver",
             "rule": "Nouveau client → courriel de bienvenue, après approbation",
             "eval": ("Déjà cliente?", "→", "Non"), "verdict": ("ask", "Courriel préparé")},
            {"k": "approve", "icon": "user", "label": "Courriel à approuver",
             "say": "Le courriel est prêt. Lisez-le, puis approuvez l’envoi.",
             "log": "Courriel de bienvenue en attente d’approbation",
             "draft": ("Merci, Nadia : votre demande est bien reçue",
                       "Bonjour Nadia, merci pour votre demande. Nous vous appelons d’ici 24 h pour planifier la visite."),
             "ok": ("Approuver l’envoi", "Envoi approuvé par vous"),
             "no": ("Ignorer", "Envoi ignoré par vous · rien n’est parti")},
            {"k": "result", "icon": "send", "label": "Envoyé et suivi",
             "say": "Le courriel part, sa réception est confirmée, et un rappel d’appel est ajouté.",
             "sum": "Envoyé · rappel demain 10 h",
             "doc": ("Courriel de bienvenue", "À Nadia Côté", "Rappel d’appel ajouté : demain, 10 h"),
             "track": ("Prêt", "Envoyé", "Confirmé"),
             "sent": "Courriel de bienvenue envoyé à Nadia Côté",
             "conf": "Courriel remis · rappel d’appel ajouté pour demain 10 h",
             "skip": "Rien n’est parti. La fiche client existe; le courriel reste en brouillon."},
        ],
        "before": [(3, "logiciels"), (9, "copier-coller"), (1, "jour")],
        "after": [(1, "approbation"), (30, "secondes")],
    },
    {
        "tab": "Facture fournisseur",
        "lead": "Une facture arrive. JARVIS la compare au bon de commande, trouve un écart et vous pose la question.",
        "stages": [
            {"k": "mail", "icon": "mail", "label": "Facture reçue",
             "say": "Le fournisseur envoie sa facture par courriel.",
             "log": "Facture F-88214 reçue · Outillage Rive-Sud", "sum": "Facture F-88214",
             "from": ("OR", "Outillage Rive-Sud", "Comptes clients · 8 h 47"),
             "subj": "Facture F-88214",
             "body": "Bonjour, voici la facture de votre commande BC-0418. Merci de votre confiance.",
             "att": "F-88214.pdf"},
            {"k": "fields", "icon": "scan", "label": "Rapprochement",
             "say": "JARVIS compare la facture au bon de commande BC-0418, ligne par ligne.",
             "log": "Facture comparée au BC-0418 · 3 lignes conformes, 1 écart", "sum": "1 écart sur 4 lignes",
             "fields": [("Article", "Compresseur 60 gal.", "ok"), ("Quantité", "1 = 1", "ok"),
                        ("Prix", "1 284,50 $ = 1 284,50 $", "ok"), ("Livraison", "0 $ ≠ 58,00 $", "bad")],
             "note": "Bon de commande BC-0418 · facture F-88214"},
            {"k": "rule", "icon": "warn", "label": "Écart détecté",
             "say": "Votre règle : tout écart avec la commande va à une personne. Le paiement attend.",
             "log": "Règle « écart de facture » → question au gérant · paiement suspendu", "sum": "Écart de 58 $ · paiement suspendu",
             "rule": "Tout écart avec la commande → question à une personne",
             "eval": ("Écart", "=", "58,00 $"), "verdict": ("warn", "Paiement suspendu")},
            {"k": "approve", "icon": "user", "label": "Question à l’humain",
             "say": "JARVIS ne décide pas à votre place : acceptez-vous ces frais de livraison?",
             "log": "Question posée au gérant · paiement en attente",
             "ask": "Accepter les frais de livraison de <b>58,00 $</b>, absents du bon de commande?",
             "ok": ("Accepter", "Frais de livraison acceptés par vous (gérant)"),
             "no": ("Contester", "Écart contesté par vous · paiement toujours suspendu")},
            {"k": "result", "icon": "doc", "label": "Facture approuvée",
             "say": "La facture approuvée part à la comptabilité, qui confirme sa réception.",
             "sum": "Transmise · confirmée",
             "doc": ("Facture approuvée", "F-88214", "1 342,50 $ · note ajoutée au dossier du fournisseur"),
             "track": ("Approuvée", "Envoyée", "Confirmée"),
             "sent": "Facture F-88214 transmise à la comptabilité",
             "conf": "Réception confirmée · paiement planifié",
             "skip": "Paiement suspendu. Un message de contestation peut être préparé, à approuver lui aussi."},
        ],
        "before": [(3, "documents"), (4, "lignes à vérifier"), (20, "minutes")],
        "after": [(1, "décision"), (20, "secondes")],
    },
]

STATIC_TIMES = ["9:12:04", "9:12:05", "9:12:06", "9:12:06", "9:12:41", "9:12:42", "9:12:44"]


def card(st, done):
    k = st["k"]
    if k == "mail":
        ini, name, meta = st["from"]
        return f"""<div class="au-mail au-x">
  <p class="au-from"><span class="au-ava" aria-hidden="true">{ini}</span><span><b>{fr(name)}</b><small>{fr(meta)}</small></span></p>
  <p class="au-subj">{fr(st['subj'])}</p>
  <p class="au-body">{fr(st['body'])}</p>
  <span class="au-att">{icon('doc')}{st['att']}</span>
</div>"""
    if k == "form":
        rows = "".join(f'<li><span>{fr(a)}</span><b>{fr(b)}</b></li>' for a, b in st["rows"])
        return f"""<div class="au-form au-x">
  <p class="au-cap">Formulaire du site web</p>
  <ul>{rows}</ul>
  <p class="au-body">{fr(st['msg'])}</p>
</div>"""
    if k == "fields":
        rows = "".join(
            f'<li class="au-f au-x{" is-" + flag if flag else ""}"><span>{fr(a)}</span>'
            f'<b class="au-v">{fr(b)}{"<i>✓</i>" if flag == "ok" else "<i>✕</i>" if flag == "bad" else ""}</b></li>'
            for a, b, flag in st["fields"]
        )
        return f"""<ul class="au-fields">{rows}</ul>
<p class="au-note au-x">{fr(st['note'])}</p>"""
    if k == "rule":
        l, op, r = st["eval"]
        kind, verdict = st["verdict"]
        return f"""<div class="au-rule au-x"><small>Votre règle</small><b>{fr(st['rule'])}</b></div>
<p class="au-eval au-x"><span>{fr(l)}</span><i>{op}</i><span>{fr(r)}</span></p>
<p class="au-verdict au-x is-{kind}">{fr(verdict)}</p>"""
    if k == "approve":
        ok, ok_log = st["ok"]
        no, no_log = st["no"]
        if "draft" in st:
            subj, body = st["draft"]
            ask = f'<div class="au-draft au-x"><small>Objet</small><b>{fr(subj)}</b><p>{fr(body)}</p></div>'
        else:
            ask = f'<p class="au-ask au-x">{fr(st["ask"])}</p>'
        decided = f'<p class="au-decided is-ok">{icon("user")}{fr(ok_log)}</p>' if done else '<p class="au-decided" role="status"></p>'
        return f"""{ask}
<div class="au-btns au-x" data-ok-log="{fr(ok_log)}" data-no-log="{fr(no_log)}">
  <button type="button" class="au-ok" data-do="ok">{fr(ok)}</button>
  <button type="button" class="au-no" data-do="no">{fr(no)}</button>
</div>
<p class="au-wait au-x"><i class="au-pulse" aria-hidden="true"></i>En attente de vous · <span data-timer>0:00</span></p>
{decided}"""
    # result
    kick, title, line = st["doc"]
    on = ' class="on"' if done else ""
    track = "".join(f"<li{on}>{fr(t)}</li>" for t in st["track"])
    return f"""<div class="au-doc au-x"><small>{fr(kick)}</small><b>{fr(title)}</b><span>{fr(line)}</span>
  <em class="au-stamp" aria-hidden="true">Confirmé</em></div>
<ol class="au-track au-x" aria-label="Suivi de l’action">{track}</ol>
<p class="au-res" data-sent="{fr(st['sent'])}" data-conf="{fr(st['conf'])}" data-skip="{fr(st['skip'])}">{fr(st['conf']) + '.' if done else ''}</p>"""


def pipe(sc, done=False):
    items = []
    n = len(sc["stages"])
    for i, st in enumerate(sc["stages"]):
        state = ""
        if done:
            state = " is-done" + (" is-linked" if i < n - 1 else " is-conf")
            if st["k"] == "approve":
                state += " is-decided"
        log = st.get("log", "")
        summary = st.get("sum") or (st["ok"][1] if done and st["k"] == "approve" else "")
        link = (
            '<span class="au-link" aria-hidden="true"><i></i><b></b><b></b><b></b></span>' if i < n - 1 else ""
        )
        items.append(f"""<li class="au-st{state}" data-k="{st['k']}" data-say="{fr(st['say'])}" data-log="{fr(log)}">
  <div class="au-node">{icon(st['icon'])}</div>{link}
  <p class="au-lab"><small>{i + 1:02d}</small>{fr(st['label'])}</p>
  <p class="au-sum">{fr(summary)}</p>
  <div class="au-card">{card(st, done)}</div>
</li>""")
    return f'<ol class="au-pipe">{"".join(items)}</ol>'


def stats(sc):
    def group(items):
        return "".join(
            f'<span class="au-num"><b data-count="{n}">{n}</b><small>{fr(u)}</small></span>' for n, u in items
        )
    return f"""<div class="au-vs-col is-before"><p class="au-k">Avant</p><div class="au-nums">{group(sc['before'])}<i class="au-strike" aria-hidden="true"></i></div></div>
<span class="au-vs-arrow" aria-hidden="true"></span>
<div class="au-vs-col is-after"><p class="au-k">Avec JARVIS</p><div class="au-nums">{group(sc['after'])}</div></div>"""


def journal_static(sc):
    lines = []
    for st in sc["stages"]:
        if st["k"] == "approve":
            lines.append(st["ok"][1])
        elif st["k"] == "result":
            lines += [st["sent"], st["conf"]]
        else:
            lines.append(st["log"])
    return "".join(f"<li><time>{STATIC_TIMES[i]}</time><span>{fr(t)}</span></li>" for i, t in enumerate(lines))


def tabs():
    return "".join(
        f'<button type="button" class="au-tab{" is-on" if i == 0 else ""}" data-sc="{i}" '
        f'aria-pressed="{"true" if i == 0 else "false"}"><small>{i + 1:02d}</small>{fr(sc["tab"])}</button>'
        for i, sc in enumerate(SCENARIOS)
    )


def templates():
    return "".join(
        f'<template data-au-sc="{i}">'
        f'<p data-part="lead">{fr(sc["lead"])}</p>'
        f'<div data-part="pipe">{pipe(sc)}</div>'
        f'<div data-part="stats">{stats(sc)}</div>'
        "</template>"
        for i, sc in enumerate(SCENARIOS)
    )


def render():
    first = SCENARIOS[0]
    return f"""<div class="demo-shell" data-demo="automatisation" data-rev>
  <div class="demo-top">
    <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
    <b>JARVIS · Automatisation</b>
    <span class="au-role">{icon('user')}Votre rôle : gérant</span>
    <span class="tag tag-sim">Démo · données simulées</span>
  </div>
  <div class="demo-body au">
    <div class="au-bar">
      <div class="au-tabs" role="group" aria-label="Scénarios">{tabs()}</div>
      <button type="button" class="au-replay" data-replay>{REPLAY}Rejouer</button>
    </div>
    <div class="au-intro">
      <p class="au-lead" data-lead>{fr(first['lead'])}</p>
      <p class="au-say" data-say aria-live="polite"><span data-step>Terminé</span><b data-say-text>{fr(first['stages'][-1]['say'])}</b></p>
    </div>
    <div class="au-stage" data-stage>{pipe(first, done=True)}</div>
    <div class="au-foot">
      <div class="au-journal">
        <p class="au-k">Journal · chaque étape laisse une trace</p>
        <ol data-journal>{journal_static(first)}</ol>
      </div>
      <div class="au-vs">
        <div class="au-vs-row" data-stats>{stats(first)}</div>
        <p class="au-vs-note">Exemple illustratif, pas une mesure réelle</p>
      </div>
    </div>
    {templates()}
  </div>
</div>
<p class="demo-hint">Vous jouez le gérant : cliquez sur « Approuver » quand JARVIS vous le demande · Exemple illustratif</p>"""


HTML = render()
