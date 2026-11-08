# Démo interactive « Automatisation d'entreprise » (assets/demos/automatisation.css et .js).
# Scénario vedette : la réception téléphonique IA — JARVIS répond sur la ligne
# IP de l'entreprise, suit la procédure de l'équipe (validée étape par étape)
# et s'arrête dès qu'un humain est requis. Trois autres scénarios : une demande
# traverse cinq étapes (reçue → lue → règle → votre approbation → exécutée).
# L'état statique (lisible sans JavaScript) montre l'appel terminé; les
# gabarits <template> sont animés par le script. Données entièrement fictives.

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
    "phone": '<path d="M7.4 3.6c.6 0 1.1.4 1.3 1l.9 2.5c.2.6 0 1.2-.5 1.6l-1.1 1a12.6 12.6 0 0 0 6.3 6.3l1-1.1c.4-.5 1-.7 1.6-.5l2.5.9c.6.2 1 .7 1 1.3v2c0 1-.8 1.8-1.8 1.7C10.8 19.7 4.3 13.2 3.7 5.4c-.1-1 .7-1.8 1.7-1.8z"/>',
    "bell": '<path d="M18.2 16.5H5.8c1.3-1.4 1.9-2.6 1.9-4.9V9.4A4.3 4.3 0 0 1 12 5.1a4.3 4.3 0 0 1 4.3 4.3v2.2c0 2.3.6 3.5 1.9 4.9z"/><path d="M10.2 19.4a1.9 1.9 0 0 0 3.6 0"/>',
    "swap": '<path d="M4 7.5h12M13 4l3.5 3.5L13 11"/><path d="M20 16.5H8M11 13l-3.5 3.5L11 20"/>',
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
             "fields": [("Fournisseur", "Outillage Rive-Sud", "", "devis-2231.pdf"),
                        ("Montant", "1 284,50 $", "", "devis-2231.pdf"),
                        ("Projet", "Chantier Lavoie", "", "Chantier Lavoie"),
                        ("Date requise", "14 novembre", "", "14 novembre")],
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
             "fields": [("Cliente", "Nadia Côté · nouvelle", "", "Nadia Côté"),
                        ("Besoin", "Sécurité · 4 caméras", "", "Caméras extérieures"),
                        ("Échéance", "Avant le 1er décembre", "", "avant décembre"),
                        ("Responsable", "Équipe des ventes", "", "")],
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
             "fields": [("Article", "Compresseur 60 gal.", "ok", "BC-0418"), ("Quantité", "1 = 1", "ok", "F-88214.pdf"),
                        ("Prix", "1 284,50 $ = 1 284,50 $", "ok", "F-88214.pdf"),
                        ("Livraison", "0 $ ≠ 58,00 $", "bad", "F-88214.pdf")],
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

# ---------- Scénario vedette : réception téléphonique IA ----------
# JARVIS répond sur la ligne IP de l'entreprise (fictive : Les Entreprises
# Delorme), suit la procédure écrite avec l'équipe — chaque étape se valide,
# une à la fois — et s'arrête pour le remboursement : la procédure exige un
# humain. L'escalade est toujours possible : « Je veux parler à quelqu'un ».

TEL = {
    "tab": "Réception téléphonique",
    "lead": (
        "Une cliente appelle pour déplacer son rendez-vous. JARVIS répond sur la ligne "
        "de l'entreprise, suit la procédure de votre équipe et ne décide rien de "
        "sensible sans un humain."
    ),
    "line": "Ligne principale · Les Entreprises Delorme (fictif)",
    "number": "450 555-0184",
    "caller": ("MT", "Marie-Claude Tessier", "Cliente · dossier CL-2284"),
    "duration": "2:05",
    # (id, libellé, détail une fois validée, ligne de journal, humain?)
    "steps": [
        ("s1", "Identifier la cliente", "Dossier CL-2284 · cliente depuis 2024", "Cliente identifiée · dossier CL-2284", False),
        ("s2", "Comprendre la demande", "Déplacer le rendez-vous du 13 novembre", "Intention comprise : déplacer le rendez-vous", False),
        ("s3", "Vérifier l’agenda", "Deux techniciens libres la semaine prochaine", "Agenda vérifié · deux techniciens libres", False),
        ("s4", "Proposer deux créneaux", "Mardi 17 à 13 h · jeudi 19 à 13 h 30", "Deux créneaux proposés à la cliente", False),
        ("s5", "Confirmer le choix", "Jeudi 19 novembre à 13 h 30", "Rendez-vous confirmé · jeudi 19 novembre, 13 h 30", False),
        ("s6", "Rembourser le dépôt (45 $)", "45 $ remboursés · approuvé par vous (gérant)", "Dépôt de 45 $ remboursé · approuvé par vous", True),
        ("s7", "Mettre le dossier à jour", "Rendez-vous déplacé · dépôt traité", "Dossier CL-2284 mis à jour", False),
        ("s8", "Envoyer la confirmation", "Courriel et SMS envoyés à la cliente", "Confirmation envoyée · courriel et SMS", False),
        ("s9", "Résumé à l’équipe", "Appel consigné · réf. AP-3121", "Résumé envoyé à l’équipe · appel consigné (AP-3121)", False),
    ],
    "no_detail": "Refusé par vous · un responsable rappelle la cliente",
    "no_log": "Remboursement refusé par vous · un responsable rappellera",
    # Transcription : qui parle, texte, étape activée au début (act), validée à
    # la fin (done), narration (say). ask : l'accord humain est demandé après.
    "script": [
        {"who": "jarvis", "text": "Les Entreprises Delorme, bonjour. Vous parlez à JARVIS, l’assistant de l’équipe. Comment puis-je vous aider ?",
         "say": "JARVIS répond au téléphone de l’entreprise. Personne n’a été interrompu."},
        {"who": "client", "text": "Bonjour, c’est Marie-Claude Tessier. J’ai un rendez-vous vendredi pour l’installation des caméras, mais je dois le déplacer.",
         "act": "s1,s2"},
        {"who": "jarvis", "text": "Bonjour madame Tessier, je retrouve votre dossier. Installation de quatre caméras, vendredi 13 novembre à 9 h. Quelles disponibilités vous conviendraient ?",
         "done": "s1,s2", "act": "s3",
         "say": "Il suit la procédure écrite avec votre équipe : chaque étape se valide, une à la fois."},
        {"who": "client", "text": "Plutôt la semaine prochaine, en après-midi si possible.", "done": "s3"},
        {"who": "jarvis", "text": "Je peux vous proposer mardi 17 novembre à 13 h ou jeudi 19 novembre à 13 h 30, avec le même technicien.",
         "act": "s4", "done": "s4"},
        {"who": "client", "text": "Jeudi 13 h 30, c’est parfait. J’avais aussi versé un dépôt de 45 $ pour vendredi : est-ce qu’il peut être remboursé ?",
         "act": "s5"},
        {"who": "jarvis", "text": "Le rendez-vous est déplacé au jeudi 19 novembre, 13 h 30. Pour le remboursement du dépôt, la procédure demande l’accord d’un membre de l’équipe : un instant, je vérifie avec lui.",
         "done": "s5", "ask": "s6",
         "say": "Un remboursement ? La procédure exige un humain. JARVIS attend votre accord."},
        {"who": "jarvis", "variant": True,
         "ok": "C’est accordé : le dépôt de 45 $ vous sera remboursé d’ici deux jours ouvrables. Vous recevrez la confirmation par courriel et par texto.",
         "no": "Un responsable doit revoir ce remboursement : il vous rappelle aujourd’hui même. Votre nouveau rendez-vous, lui, est bien confirmé.",
         "act": "s7", "done": "s7,s8",
         "say": "Votre décision est prise : JARVIS termine le travail et consigne tout."},
        {"who": "client", "text": "Merci beaucoup, c’est très clair."},
        {"who": "jarvis", "text": "Avec plaisir, madame Tessier. Bonne journée !", "act": "s9", "done": "s9"},
    ],
    "ask": "Rembourser le dépôt de <b>45 $</b> à Mme Tessier (dossier CL-2284) ?",
    "ask_log": "Remboursement de 45 $ · en attente de votre accord",
    "ok_btn": ("Approuver le remboursement", "Remboursement approuvé par vous (gérant)"),
    "no_btn": ("Refuser", "Remboursement refusé par vous · un responsable rappellera"),
    # Escalade : à tout moment, la cliente peut demander une personne.
    "esc": [
        {"who": "client", "text": "En fait, je préférerais parler à quelqu’un, s’il vous plaît."},
        {"who": "jarvis", "text": "Bien sûr, je vous transfère tout de suite. La personne qui prend l’appel a déjà tout le dossier sous les yeux."},
    ],
    "esc_say": "« Je veux parler à quelqu’un » : transfert immédiat, avec tout le contexte.",
    "hand": [
        ("Qui", "Marie-Claude Tessier · cliente depuis 2024 · dossier CL-2284"),
        ("Pourquoi", "Souhaite parler à une personne (déplacement de rendez-vous, dépôt de 45 $)"),
        ("Historique", "Rendez-vous du 13 novembre à déplacer · installation de quatre caméras"),
        ("L’appel en est à", ""),  # rempli selon les étapes déjà validées
    ],
    "end": {
        "ok": ("Client satisfait · rendez-vous déplacé · personne n’a été interrompu",
               "Appel consigné avec enregistrement et transcription · réf. AP-3121"),
        "no": ("Rendez-vous déplacé · le remboursement attend un responsable",
               "Appel consigné avec enregistrement et transcription · réf. AP-3121"),
        "esc": ("Transfert réussi · l’employé a l’appel, avec tout le contexte",
                "La cliente n’a rien eu à répéter · appel consigné · réf. AP-3121"),
    },
    "end_say": "Client satisfait · rendez-vous déplacé · personne n’a été interrompu.",
    "before": [(6, "appels manqués"), (4, "rappels à faire"), (15, "minutes perdues")],
    "after": [(0, "appel manqué"), (1, "accord humain")],
}

TEL_TIMES = ["10:02:11", "10:02:14", "10:02:31", "10:02:49", "10:03:02", "10:03:11",
             "10:03:26", "10:03:27", "10:03:41", "10:03:52", "10:04:02", "10:04:16"]


def tel_wave():
    return '<div class="au-wave" data-wave aria-hidden="true">' + "<i></i>" * 28 + "</div>"


def tel_steps(done=False):
    items = []
    for sid, label, detail, log_line, human in TEL["steps"]:
        cls = " is-done" if done else ""
        badge = '<em class="au-ps-h">Validation humaine</em>' if human else ""
        notif = ""
        if human:
            ok, ok_log = TEL["ok_btn"]
            no, no_log = TEL["no_btn"]
            notif = f"""<div class="au-notif au-x{' on' if done else ''}" data-notif {'' if done else 'hidden'}>
    <p class="au-notif-t">{icon('bell')}Notification · à vous (gérant)</p>
    <p class="au-ask">{fr(TEL['ask'])}</p>
    <div class="au-btns" data-ok-log="{fr(ok_log)}" data-no-log="{fr(no_log)}" {'hidden' if done else ''}>
      <button type="button" class="au-ok" data-do="ok">{fr(ok)}</button>
      <button type="button" class="au-no" data-do="no">{fr(no)}</button>
    </div>
    <p class="au-wait" {'hidden' if done else ''}><i class="au-pulse" aria-hidden="true"></i>La cliente patiente · <span data-timer>0:00</span></p>
    <p class="au-decided{' is-ok' if done else ''}" role="status">{icon('user') + fr(ok_log) if done else ''}</p>
  </div>"""
        items.append(f"""<li class="au-ps{cls}{' is-human' if human else ''}" data-ps="{sid}" data-d="{fr(detail)}"
  data-dn="{fr(TEL['no_detail']) if human else ''}" data-log="{fr(log_line)}">
  <i class="au-ps-i" aria-hidden="true"></i>
  <div class="au-ps-c"><b>{fr(label)}</b>{badge}<small class="au-ps-d">{fr(detail) if done else ''}</small>{notif}</div>
</li>""")
    return f'<ol class="au-steps" aria-label="Procédure de l’équipe">{"".join(items)}</ol>'


def tel_script(done=False):
    lines = []
    for ln in TEL["script"]:
        who = ln["who"]
        name = "JARVIS" if who == "jarvis" else "Mme Tessier"
        if ln.get("variant"):
            text = fr(ln["ok"]) if done else ""
            extra = f' data-ok-text="{fr(ln["ok"])}" data-no-text="{fr(ln["no"])}" data-variant'
        else:
            text = fr(ln["text"])
            extra = ""
        attrs = "".join(
            f' data-{k}="{fr(ln[k]) if k == "say" else ln[k]}"' for k in ("act", "done", "ask", "say") if ln.get(k)
        )
        lines.append(f'<li class="au-line au-x{" on" if done else ""}" data-who="{who}"{extra}{attrs}>'
                     f'<span class="au-who">{name}</span><p>{text}</p></li>')
    esc = "".join(
        f'<li class="au-line" data-who="{ln["who"]}" data-esc-line hidden>'
        f'<span class="au-who">{"JARVIS" if ln["who"] == "jarvis" else "Mme Tessier"}</span><p>{fr(ln["text"])}</p></li>'
        for ln in TEL["esc"]
    )
    return f'<ol class="au-script" data-script aria-label="Transcription de l’appel">{"".join(lines)}{esc}</ol>'


def tel_hand():
    rows = "".join(
        f'<div class="au-hand-r"><span>{fr(k)}</span><b{" data-hand-at" if not v else ""}>{fr(v)}</b></div>'
        for k, v in TEL["hand"]
    )
    return f"""<div class="au-hand" data-hand hidden>
  <p class="au-hand-t">{icon('swap')}Transfert à l’employé · tout le contexte suit</p>
  {rows}
</div>"""


def tel_end(done=False):
    ok_t, ok_s = TEL["end"]["ok"]
    no_t, no_s = TEL["end"]["no"]
    esc_t, esc_s = TEL["end"]["esc"]
    return (f'<div class="au-telend au-x{" on is-ok" if done else ""}" data-telend'
            f' data-ok-t="{fr(ok_t)}" data-ok-s="{fr(ok_s)}" data-no-t="{fr(no_t)}" data-no-s="{fr(no_s)}"'
            f' data-esc-t="{fr(esc_t)}" data-esc-s="{fr(esc_s)}" {"" if done else "hidden"}>'
            f'<b data-telend-t>{fr(ok_t) if done else ""}</b><span data-telend-s>{fr(ok_s) if done else ""}</span></div>')


def tel_stage(done=False):
    ini, name, meta = TEL["caller"]
    status = "Terminé · appel consigné" if done else "Appel entrant"
    timer = TEL["duration"] if done else "0:00"
    return f"""<div class="au-tel{' is-done' if done else ''}" data-tel>
  <div class="au-call">
    <p class="au-call-line"><span class="au-call-i">{icon('phone')}</span><span><b>{fr(TEL['line'])}</b><small>Téléphonie IP · {TEL['number']}</small></span>
      <em class="au-cstat{' is-end' if done else ' is-ring'}" data-cstat>{status}</em></p>
    <p class="au-caller"><span class="au-ava" aria-hidden="true">{ini}</span><span><b>{fr(name)}</b><small>{fr(meta)}</small></span>
      <span class="au-ctimer" data-ctimer>{timer}</span></p>
    {tel_wave()}
    {tel_script(done)}
    <div class="au-esc-bar">
      <p>À tout moment : «{NBSP}Je veux parler à quelqu’un{NBSP}» → transfert avec tout le contexte à l’écran de l’employé.</p>
      <button type="button" class="au-esc-btn" data-esc {'disabled' if done else ''}>Essayer le transfert</button>
    </div>
    {tel_hand()}
  </div>
  <aside class="au-play">
    <p class="au-k">Procédure de l’équipe · validée étape par étape</p>
    {tel_steps(done)}
    {tel_end(done)}
  </aside>
</div>"""


def tel_journal_static():
    lines = ["Appel entrant · ligne principale", "JARVIS a répondu avant la deuxième sonnerie"]
    for sid, _label, _d, log_line, human in TEL["steps"]:
        if human:
            lines.append(TEL["ask_log"])
        lines.append(log_line)
    lines = lines[:len(TEL_TIMES)]
    return "".join(f"<li><time>{TEL_TIMES[i]}</time><span>{fr(t)}</span></li>" for i, t in enumerate(lines))


STATIC_TIMES = ["9:12:04", "9:12:05", "9:12:06", "9:12:06", "9:12:41", "9:12:42", "9:12:44"]
# Signature manuscrite du gérant, tracée sur le document approuvé
SIGN = ('<svg class="au-sig" viewBox="0 0 132 30" aria-hidden="true"><path pathLength="1" d="M9 21C4 25 3 16 13 7'
        'c6-5 9-3 5 5-3 6-7 12-5 13 3 1 7-8 10-11 2-2 3 0 2 3-1 3-1 6 1 5 3-1 5-7 8-8 2 0 1 4 1 6 0 2 2 2 4 0 '
        '3-3 5-7 8-7 2 0 0 5 2 6 3 1 6-4 9-6 2-1 3 1 3 3 0 3 3 3 6 0 4-4 9-10 14-10M20 27c26-2 60-6 104-10"/></svg>')


def sources(sc):
    """Passages du message d'origine que JARVIS lit à l'étape 2 (sans doublon, dans l'ordre)."""
    out = []
    for f in sc["stages"][1]["fields"]:
        if f[3] and f[3] not in out:
            out.append(f[3])
    return out


def marked(text, srcs):
    """Texte du message, avec un <mark> sur chaque passage lu par JARVIS."""
    s = fr(text)
    for i, src in enumerate(srcs):
        if fr(src) in s:
            s = s.replace(fr(src), f'<mark class="au-m" data-m="{i}">{fr(src)}</mark>', 1)
    return s


def card(st, done, srcs):
    k = st["k"]
    if k == "mail":
        ini, name, meta = st["from"]
        return f"""<div class="au-mail au-x">
  <p class="au-from"><span class="au-ava" aria-hidden="true">{ini}</span><span><b>{fr(name)}</b><small>{marked(meta, srcs)}</small></span></p>
  <p class="au-subj">{marked(st['subj'], srcs)}</p>
  <p class="au-body">{marked(st['body'], srcs)}</p>
  <span class="au-att">{icon('doc')}{marked(st['att'], srcs)}</span>
</div>"""
    if k == "form":
        rows = "".join(f'<li><span>{fr(a)}</span><b>{marked(b, srcs)}</b></li>' for a, b in st["rows"])
        return f"""<div class="au-form au-x">
  <p class="au-cap">Formulaire du site web</p>
  <ul>{rows}</ul>
  <p class="au-body">{marked(st['msg'], srcs)}</p>
</div>"""
    if k == "fields":
        def field(a, b, flag, src):
            cls = f" is-{flag}" if flag else ""
            ref = f' data-src="{srcs.index(src)}"' if src else ""
            mark = {"ok": "<i>✓</i>", "bad": "<i>✕</i>"}.get(flag, "")
            return (f'<li class="au-f au-x{cls}"{ref}><span>{fr(a)}</span>'
                    f'<b class="au-v"><span class="au-t">{fr(b)}</span>{mark}</b></li>')
        rows = "".join(field(*f) for f in st["fields"])
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
    sign = f'<p class="au-sign">{SIGN}</p>' if st["icon"] == "doc" else ""
    return f"""<div class="au-doc au-x"><small>{fr(kick)}</small><b>{fr(title)}</b><span>{fr(line)}</span>{sign}
  <em class="au-stamp" aria-hidden="true">Confirmé</em></div>
<ol class="au-track au-x" aria-label="Suivi de l’action" style="--tk:{1 if done else 0}">{track}</ol>
<p class="au-res" data-sent="{fr(st['sent'])}" data-conf="{fr(st['conf'])}" data-skip="{fr(st['skip'])}">{fr(st['conf']) + '.' if done else ''}</p>"""


def pipe(sc, done=False):
    items = []
    n = len(sc["stages"])
    srcs = sources(sc)
    for i, st in enumerate(sc["stages"]):
        state = ""
        if done:
            state = " is-done" + (" is-linked" if i < n - 1 else " is-conf")
            if st["k"] == "approve":
                state += " is-decided"
        log = st.get("log", "")
        summary = st.get("sum") or (st["ok"][1] if done and st["k"] == "approve" else "")
        link = (
            '<span class="au-link" aria-hidden="true"><i></i></span>' if i < n - 1 else ""
        )
        items.append(f"""<li class="au-st{state}" data-k="{st['k']}" data-say="{fr(st['say'])}" data-log="{fr(log)}">
  <div class="au-node">{icon(st['icon'])}</div>{link}
  <p class="au-lab"><small>{i + 1:02d}</small>{fr(st['label'])}</p>
  <p class="au-sum">{fr(summary)}</p>
  <div class="au-card">{card(st, done, srcs)}</div>
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


def tel_stats():
    sc = {"before": TEL["before"], "after": TEL["after"]}
    return stats(sc)


def tabs():
    out = [f'<button type="button" class="au-tab is-on" data-sc="tel" aria-pressed="true">'
           f'<small>01</small>{fr(TEL["tab"])}</button>']
    out += [
        f'<button type="button" class="au-tab" data-sc="{i}" aria-pressed="false">'
        f'<small>{i + 2:02d}</small>{fr(sc["tab"])}</button>'
        for i, sc in enumerate(SCENARIOS)
    ]
    return "".join(out)


def templates():
    tel = (f'<template data-au-tel>'
           f'<p data-part="lead">{fr(TEL["lead"])}</p>'
           f'<div data-part="pipe">{tel_stage()}</div>'
           f'<div data-part="stats">{tel_stats()}</div>'
           "</template>")
    return tel + "".join(
        f'<template data-au-sc="{i}">'
        f'<p data-part="lead">{fr(sc["lead"])}</p>'
        f'<div data-part="pipe">{pipe(sc)}</div>'
        f'<div data-part="stats">{stats(sc)}</div>'
        "</template>"
        for i, sc in enumerate(SCENARIOS)
    )


def render():
    return f"""<div class="demo-shell" data-demo="automatisation" data-rev>
  <div class="demo-top">
    <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
    <b>JARVIS · Automatisation</b>
    <span class="au-role">{icon('user')}Votre rôle : gérant</span>
    <span class="tag tag-sim">Simulation · données d’exemple</span>
  </div>
  <div class="demo-body au">
    <div class="au-bar">
      <div class="au-tabs" role="group" aria-label="Scénarios">{tabs()}</div>
      <button type="button" class="au-replay" data-replay>{REPLAY}Rejouer</button>
    </div>
    <div class="au-intro">
      <p class="au-lead" data-lead>{fr(TEL['lead'])}</p>
      <p class="au-say" data-say aria-live="polite"><span data-step>Terminé</span><b data-say-text>{fr(TEL['end_say'])}</b></p>
    </div>
    <div class="au-stage" data-stage>{tel_stage(done=True)}</div>
    <div class="au-foot">
      <div class="au-journal">
        <p class="au-k">Journal · chaque étape laisse une trace</p>
        <ol data-journal>{tel_journal_static()}</ol>
      </div>
      <div class="au-vs">
        <div class="au-vs-row" data-stats>{tel_stats()}</div>
        <p class="au-vs-note">Exemple illustratif, pas une mesure réelle</p>
      </div>
    </div>
    {templates()}
  </div>
</div>
<p class="demo-hint">Vous jouez le gérant : approuvez quand JARVIS vous le demande, ou essayez « Je veux parler à quelqu’un » · Exemple illustratif, données fictives</p>"""


HTML = render()


# =============================================================================
# « Votre secteur » — explorateur des besoins réels, secteur par secteur.
# Chaque secteur : 3 à 5 problèmes concrets du quotidien, et pour chacun
# l'automatisation JARVIS qui le règle (déclencheur → étapes → validation
# humaine au besoin → résultat), le gain estimé et les extensions touchées.
# Photos : media/secteurs/<slug>.webp dès que le fichier existe au build
# (aucun changement de code), sinon une photo du site qui convient, sinon un
# panneau noir « Photo à venir ». Données d'exemple, gains = estimations.
# =============================================================================

import os
import unicodedata

_MEDIA_SECT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "media", "secteurs")

# Extensions JARVIS : clé → (nom court, page)
EXT = {
    "E": ("Entreprise", "automatisation-operations"),
    "V": ("Environnements", "environnements-intelligents"),
    "I": ("IA privée", "ia-privee-connaissances"),
    "S": ("Sécurité", "securite-intelligente"),
    "R": ("Réseau", "reseau-resilience"),
    "D": ("Diagnostic", "diagnostic-care"),
    "M": ("Mobilité", "mobilite"),
}


def P(p, d, a, trig, steps, h, r, g, x):
    """Un problème réel et son automatisation.
    p problème · d la situation vécue · a nom de l'automatisation · trig déclencheur ·
    steps étapes de JARVIS · h validation humaine (ou None) · r résultat ·
    g gain estimé (sorte « t » temps ou « r » risque, chiffre, précision) · x extensions."""
    return {"p": p, "d": d, "a": a, "trig": trig, "steps": steps, "h": h, "r": r, "g": g, "x": x}


# (slug, nom, métiers, mots-clés de recherche, photo existante du site qui convient, phrase d'accroche, problèmes)
SECTEURS = [
    ("fermes", "Fermes et agriculture", "Laitière · porcine · avicole · érablière · cultures",
     "ferme fermier agriculteur agricole producteur laitier lait vache vaches bovin porc porcs porcherie porcine volaille poulailler avicole poulet poules oeufs érablière cabane à sucre acériculteur sirop grandes cultures serre serriculteur maraîcher bleuets pomiculteur verger",
     None, "Les animaux ne prennent pas congé, et une alarme ratée la nuit peut coûter un troupeau.", [
        P("La ventilation qui tombe en panne la nuit dans le poulailler",
          "Une panne de ventilation ou de chauffage en bâtiment avicole ou porcin peut tuer des milliers de bêtes en moins d’une heure. L’alarme sonne dans un bâtiment vide.",
          "Garde de nuit des bâtiments d’élevage", "Bâtiment 3 à 32 °C, ventilateur 2 arrêté",
          ["Capteurs et automate du bâtiment lus en continu", "Appel vocal au producteur, puis à la personne de garde s’il ne répond pas", "Génératrice démarrée et vérifiée"],
          "Le producteur confirme au téléphone qu’il prend la situation en main", "Intervention en 9 minutes · événement consigné pour l’assureur",
          ("r", "Troupeau protégé", "une seule nuit sans alarme peut coûter des dizaines de milliers de dollars"), "EVDR"),
        P("Le réservoir à lait qui refroidit mal",
          "Un compresseur qui faiblit, et c’est tout un réservoir déclassé, découvert seulement au passage du camion.",
          "Surveillance du refroidissement du lait", "La courbe de refroidissement s’écarte de la normale",
          ["Température comparée aux traites précédentes", "Alerte au producteur, avec la courbe", "Rendez-vous proposé au frigoriste"],
          "Le producteur approuve l’appel de service", "Compresseur réparé avant la traite suivante",
          ("r", "Réservoir sauvé", "plutôt qu’une cargaison de lait jetée"), "EDV"),
        P("Les registres de traitements tenus sur le calendrier du mur",
          "Antibiotiques, délais d’attente, vaccins : tout est noté à la main, puis recopié pour la vérification ou le vétérinaire.",
          "Registre de troupeau dicté", "Le producteur dicte : « Vache 412, mammite, traitement commencé »",
          ["Traitement inscrit au registre de la bête", "Délai d’attente calculé, lait de la vache retiré au tableau", "Rappel de fin de traitement programmé"],
          None, "Registre prêt pour la vérification · aucun lait livré trop tôt",
          ("t", "≈ 3 h", "par semaine de paperasse en moins"), "EI"),
        P("Les fuites dans la tubulure de l’érablière",
          "En pleine coulée, une fuite dans le système sous vide fait perdre de l’eau d’érable chaque heure, et il faut marcher des kilomètres pour la trouver.",
          "Vigie du vide en érablière", "Le vide baisse sur la ligne principale 4",
          ["Capteurs de vide comparés ligne par ligne", "Section fautive située sur la carte de l’érablière", "Itinéraire envoyé au téléphone de l’équipe"],
          None, "Fuite trouvée en 20 minutes plutôt qu’en une demi-journée",
          ("t", "≈ 4 h", "gagnées par fuite, en pleine coulée"), "EVM"),
        P("La moulée et le propane commandés trop tard",
          "Le silo se vide un vendredi soir; le réservoir de propane, en plein froid.",
          "Réapprovisionnement des intrants", "Silo de moulée à 18 %",
          ["Consommation prévue selon le troupeau et la météo", "Commande préparée chez le fournisseur habituel"],
          "Le producteur approuve la commande", "Livraison confirmée pour mardi",
          ("r", "Aucune rupture", "de moulée ni de chauffage"), "EV"),
    ]),
    ("construction", "Construction et entrepreneurs", "Général · spécialisés · rénovation",
     "construction entrepreneur entrepreneur général rénovation rénovateur chantier charpentier menuisier coffreur maçon briqueteur couvreur toiture plâtrier gypse peintre béton cimentier ébéniste armoires portes et fenêtres soudeur",
     "/media/solutions/automatisation-operations.webp", "Le chantier avance vite; la paperasse, elle, se perd entre la camionnette et le bureau.", [
        P("Les bons de travail papier perdus sur les chantiers",
          "Les feuilles de temps et les bons de travail reviennent froissés, en retard ou jamais. La facturation attend.",
          "Bons de travail dictés sur le chantier", "Le contremaître dicte sa journée en fin de quart",
          ["Heures, tâches et matériaux extraits de la dictée", "Bon de travail rattaché au bon projet, avec photos", "Heures envoyées à la paie"],
          "Le contremaître relit et signe sur son téléphone", "Bon de travail au bureau le soir même",
          ("t", "≈ 6 h", "par semaine de saisie et de relances"), "EIM"),
        P("Les extras faits sans ordre de changement signé",
          "Le client demande « une petite affaire de plus »; elle est faite, jamais signée, puis contestée à la facturation.",
          "Ordre de changement en direct", "Un ouvrier signale un travail hors contrat",
          ["Ordre de changement préparé avec vos prix", "Envoyé au client pour signature électronique", "Ajouté à la prochaine facture"],
          "Le chargé de projet approuve le prix avant l’envoi", "Extra signé avant d’être fait",
          ("r", "Extras payés", "plutôt que perdus en discussions à la fin du chantier"), "E"),
        P("Les sous-traitants qui arrivent pour rien",
          "Une livraison est repoussée, tout se décale, mais l’électricien arrive quand même lundi matin.",
          "Échéancier qui prévient tout le monde", "Le fournisseur repousse la livraison des fermes de toit",
          ["Échéancier recalculé", "Sous-traitants touchés repérés", "Nouveaux créneaux proposés à chacun par texto"],
          "Le chargé de projet confirme le nouvel échéancier", "Personne ne se déplace pour rien",
          ("t", "≈ 1 jour", "de main-d’œuvre sauvé à chaque décalage"), "EM"),
        P("La paperasse de sécurité du chantier",
          "Inspections quotidiennes, pauses sécurité, fiches de données de sécurité : tout doit être prouvé lors d’une visite de la CNESST.",
          "Registre de sécurité du chantier", "Début de quart sur le chantier Lavoie",
          ["Liste d’inspection envoyée au responsable", "Photos et réponses classées par chantier", "Non-conformité ouverte si un point échoue"],
          "Le responsable corrige et ferme la non-conformité", "Registre complet, prêt à présenter",
          ("r", "Constat évité", "dossier présenté en deux minutes lors d’une visite"), "ES"),
        P("Les soumissions qui partent trop tard",
          "Les demandes arrivent par courriel, texto et téléphone; la soumission part une semaine plus tard, quand le client a signé ailleurs.",
          "Soumission préparée en 24 heures", "Demande de soumission reçue avec photos",
          ["Mesures et besoins extraits", "Brouillon chiffré avec vos prix unitaires", "Relance automatique après trois jours"],
          "L’estimateur révise et approuve le prix", "Soumission envoyée le lendemain",
          ("t", "≈ 2 h", "par soumission"), "EI"),
    ]),
    ("transport", "Transport et logistique", "Camionnage · livraison · entreposage",
     "transport transporteur camionnage camion camions camionneur chauffeur livraison livreur logistique entrepôt entreposage distribution flotte répartiteur répartition messagerie courrier déménagement déménageur autobus remorquage",
     "/media/solutions/security-enterprise-delivery-v1.webp", "Chaque camion immobilisé coûte cher, et chaque livraison doit être prouvée.", [
        P("Les rondes de sécurité sur papier",
          "La vérification avant départ est obligatoire; les feuilles se perdent dans les cabines et une défectuosité majeure peut passer inaperçue.",
          "Ronde de sécurité numérique", "Le chauffeur commence son quart",
          ["Liste de vérification sur le téléphone, avec photos", "Défectuosité mineure envoyée à l’atelier", "Défectuosité majeure : camion bloqué au tableau"],
          "Le mécanicien confirme la réparation avant le départ", "Rapport conservé, prêt pour un contrôle routier",
          ("r", "Amende évitée", "et aucun camion parti avec un défaut majeur"), "EMD"),
        P("« Où est mon camion? » au téléphone toute la journée",
          "Les clients appellent le répartiteur pour connaître l’heure de livraison; chaque appel interrompt la planification.",
          "Avis de livraison automatiques", "Le camion quitte l’entrepôt",
          ["Heure d’arrivée calculée selon la position et la circulation", "Texto au client avec l’heure prévue", "Nouvel avis si le retard dépasse 20 minutes"],
          None, "Le client sait, sans appeler",
          ("t", "≈ 40", "appels de moins par jour au répartiteur"), "EM"),
        P("Les preuves de livraison introuvables",
          "Une marchandise est contestée trois semaines plus tard; le bon signé est quelque part dans un camion.",
          "Preuve de livraison classée", "Livraison terminée chez le client",
          ["Photo, signature et position enregistrées", "Bon de livraison joint à la facture", "Facture envoyée au client le jour même"],
          None, "Litige réglé en une minute",
          ("t", "≈ 15 min", "par litige, et la facture part le jour même"), "EM"),
        P("L’entretien préventif fait en retard",
          "Le programme d’entretien de la flotte vit dans un chiffrier; un camion dépasse son échéance sans que personne le voie.",
          "Entretien de flotte au kilomètre", "Le camion 12 approche des 25 000 km depuis son dernier entretien",
          ["Kilométrage lu dans le véhicule", "Rendez-vous proposé à l’atelier un jour creux", "Pièces commandées d’avance"],
          "Le gestionnaire de flotte approuve la date", "Entretien fait sans perdre un voyage",
          ("r", "Panne évitée", "un camion en panne sur la route coûte des milliers de dollars"), "EMD"),
        P("Les heures de conduite qui frôlent la limite",
          "Un chauffeur approche de sa limite d’heures de conduite, et la répartition l’envoie quand même sur un long trajet.",
          "Répartition qui respecte les heures", "Nouvelle livraison à assigner",
          ["Heures restantes de chaque chauffeur lues", "Chauffeur conforme le plus proche proposé"],
          "Le répartiteur confirme l’assignation", "Livraison assignée sans infraction",
          ("r", "Infraction évitée", "et dossier de l’exploitant protégé"), "EM"),
    ]),
    ("garages", "Garages et concessionnaires", "Mécanique · carrosserie · pneus · concessions",
     "garage mécanicien mécanique auto automobile voiture carrosserie carrossier débosselage pneus pneu changement de pneus concessionnaire concession vendeur d'autos véhicules usagés esthétique automobile lave-auto vitres d'auto silencieux",
     "/media/solutions/diagnostic-care.webp", "Le téléphone sonne pendant que les mains sont sous un capot.", [
        P("« Est-ce que mon auto est prête? » vingt fois par jour",
          "Le comptoir passe la journée au téléphone au lieu de servir les clients en personne.",
          "Suivi des réparations en direct", "Le technicien ferme le bon de travail",
          ["Statut mis à jour au dossier", "Texto au client avec le total et l’heure de cueillette", "Le client qui appelle quand même entend le statut exact"],
          None, "Le client vient chercher son auto, informé",
          ("t", "≈ 2 h", "par jour au comptoir"), "E"),
        P("Les travaux supplémentaires en attente d’approbation",
          "Le technicien trouve des plaquettes usées; le client ne rappelle pas, et l’auto bloque un pont élévateur tout l’après-midi.",
          "Approbation par texto, avec photo", "Le technicien signale un travail supplémentaire",
          ["Photo et explication en mots simples", "Prix calculé selon vos taux", "Envoyé au client : approuver ou refuser"],
          "Le client approuve sur son téléphone", "Travail ajouté au bon, pont libéré",
          ("t", "≈ 1 h", "de pont élévateur libérée par véhicule"), "ED"),
        P("La saison des pneus qui sature le téléphone",
          "Au printemps et à l’automne, tout le monde appelle la même semaine pour ses pneus.",
          "Rendez-vous de pneus en libre-service", "Première neige annoncée dans la région",
          ["Clients avec pneus entreposés repérés", "Invitations avec créneaux libres envoyées par vagues", "Pneus sortis de l’entrepôt la veille"],
          None, "Agenda rempli sans un seul appel",
          ("t", "≈ 25 h", "de téléphone épargnées par saison"), "EV"),
        P("Les rappels d’entretien jamais envoyés",
          "Les clients oublient leur vidange; ils vont chez le concurrent quand le voyant s’allume.",
          "Rappels d’entretien personnalisés", "Le kilométrage estimé du client atteint l’échéance",
          ["Historique du véhicule lu", "Rappel envoyé avec un créneau proposé"],
          None, "Client de retour au bon moment",
          ("r", "Clients fidèles", "plus de visites, sans relances à la main"), "EM"),
        P("Les pistes de vente qui refroidissent",
          "Une demande d’essai routier arrive samedi soir; le vendeur la voit lundi.",
          "Pistes de vente suivies à la minute", "Demande reçue sur le site ou par téléphone",
          ["Véhicule demandé vérifié en inventaire", "Réponse immédiate avec créneaux d’essai", "Piste assignée au vendeur de garde"],
          "Le vendeur confirme l’essai routier", "Essai planifié avant que le client magasine ailleurs",
          ("r", "Ventes sauvées", "une piste répondue en cinq minutes se conclut bien plus souvent"), "E"),
    ]),
    ("cliniques", "Cliniques et santé", "Dentaire · physiothérapie · vétérinaire · médicale",
     "clinique santé dentiste dentaire hygiéniste denturologiste physiothérapeute physiothérapie physio ostéopathe chiropraticien massothérapeute vétérinaire vétérinaires animaux hôpital vétérinaire optométriste opticien médecin clinique médicale psychologue ergothérapeute orthophoniste podiatre audiologiste",
     None, "La réception jongle entre le patient au comptoir, le téléphone et l’urgence.", [
        P("Les appels manqués pendant les urgences en clinique vétérinaire",
          "Un animal arrive en urgence, toute l’équipe est mobilisée; pendant ce temps, le téléphone sonne dans le vide.",
          "Réception d’urgence", "Appel entrant, personne de libre",
          ["JARVIS répond et suit le protocole de triage de la clinique", "Urgence réelle : vétérinaire avisé, client attendu", "Autres appels : rendez-vous pris ou rappel planifié"],
          "Le vétérinaire décide de l’urgence", "Aucun appel perdu, aucune urgence ignorée",
          ("r", "Aucun appel perdu", "même pendant une chirurgie"), "EI"),
        P("Les rendez-vous manqués et les trous dans l’horaire",
          "Un patient oublie son rendez-vous; la plage reste vide et le professionnel est payé à attendre.",
          "Confirmation et liste d’attente", "48 heures avant chaque rendez-vous",
          ["Rappel avec confirmation par texto", "Annulation : premier patient de la liste d’attente invité", "Plage comblée à l’horaire"],
          None, "Plage remplie plutôt que perdue",
          ("t", "≈ 4 h", "de plages récupérées par semaine"), "E"),
        P("Les formulaires d’assurance et les réclamations",
          "Chaque traitement exige des reçus, des codes et parfois un rapport pour l’assureur ou la CNESST.",
          "Réclamations préparées", "Fin du traitement au dossier",
          ["Reçu et codes de traitement préparés", "Réclamation transmise à l’assureur du patient", "Refus ou pièce manquante signalé"],
          "Le professionnel signe le rapport", "Réclamation envoyée le jour même",
          ("t", "≈ 5 h", "par semaine à la réception"), "EI"),
        P("Les rappels de vaccins et de suivis",
          "Vaccins annuels, nettoyages aux six mois, suivi postopératoire : les rappels dépendent de la mémoire de quelqu’un.",
          "Rappels de soins", "Échéance au dossier du patient",
          ["Rappel personnalisé (nom de l’animal, soin dû)", "Créneau proposé, réservé en un clic"],
          None, "Patient revu à temps",
          ("r", "Soins à jour", "et revenus récurrents protégés"), "E"),
        P("Les renseignements de patients qui circulent sans contrôle",
          "Notes, radiographies, courriels : des renseignements sensibles circulent partout, alors que la Loi 25 exige de les protéger.",
          "Dossier protégé et journalisé", "Une personne consulte un dossier",
          ["Droits de la personne vérifiés", "Consultation inscrite au journal (sans le contenu)", "Accès inhabituel signalé au responsable"],
          "Le responsable de la protection des renseignements tranche", "Chaque accès est traçable",
          ("r", "Conformité", "à la Loi 25, démontrable en tout temps"), "EIRS"),
    ]),
    ("pharmacies", "Pharmacies", "Officine · laboratoire · comptoir",
     "pharmacie pharmacien pharmacienne officine assistant technique en pharmacie ATP médicament médicaments ordonnance ordonnances prescription renouvellement vaccination",
     None, "Le pharmacien est là pour conseiller, pas pour répéter « pas encore prête » au téléphone.", [
        P("« Est-ce que ma prescription est prête? » au téléphone",
          "Une grande part des appels demandent un simple statut; chacun interrompt une vérification au laboratoire.",
          "Statut d’ordonnance sans attente", "Appel d’un patient",
          ["Patient identifié (date de naissance)", "Statut lu dans le système de la pharmacie", "Texto envoyé quand c’est prêt"],
          None, "Le laboratoire n’est pas interrompu",
          ("t", "≈ 3 h", "par jour au téléphone"), "E"),
        P("Les demandes de renouvellement aux médecins",
          "Les renouvellements dépendent de télécopies et de relances aux cliniques; le patient tombe à court.",
          "Renouvellements suivis", "Plus que 7 jours de médicament au dossier",
          ["Demande de renouvellement préparée", "Envoyée à la clinique, relancée après 48 heures", "Patient informé du statut"],
          "Le pharmacien valide la demande", "Aucun patient à court de médicament",
          ("r", "Traitement continu", "aucune interruption pour un papier oublié"), "E"),
        P("Les ruptures de stock découvertes au comptoir",
          "Le patient arrive, le produit manque; il faut appeler trois grossistes.",
          "Stock et substitutions", "Seuil bas, ou rupture annoncée par le grossiste",
          ["Patients touchés repérés", "Commande ou substitution proposée"],
          "Le pharmacien approuve la substitution", "Patient prévenu avant de se déplacer",
          ("t", "≈ 30 min", "par rupture"), "E"),
        P("La température du réfrigérateur à vaccins",
          "Une nuit au-dessus de 8 °C et les vaccins sont perdus, souvent sans que personne le sache.",
          "Chaîne de froid surveillée", "Réfrigérateur à 8,4 °C depuis 15 minutes",
          ["Alerte au pharmacien de garde", "Registre de température tenu automatiquement", "Rapport d’écart prêt pour l’inspection"],
          "Le pharmacien décide si les doses sont conservées", "Vaccins sauvés, registre complet",
          ("r", "Lot sauvé", "des milliers de dollars de vaccins"), "EVD"),
    ]),
    ("restauration", "Restauration", "Restaurants · cafés · traiteurs · bars",
     "restaurant restauration resto café bistro bar brasserie microbrasserie traiteur cuisine cuisinier chef cantine casse-croûte boulangerie pâtisserie pizzeria camion de cuisine de rue cafétéria",
     None, "Le service du soir n’attend pas, et l’inspecteur non plus.", [
        P("La conformité MAPAQ des températures",
          "Les relevés des frigos et des chambres froides se font sur une feuille… quand quelqu’un y pense.",
          "Relevés de températures automatiques", "Chambre froide à 6 °C depuis 20 minutes",
          ["Capteurs relevés toutes les 5 minutes", "Alerte au gérant avec l’historique", "Registre conservé pour l’inspecteur"],
          "Le gérant décide du sort des aliments", "Registre MAPAQ toujours complet",
          ("r", "Inventaire sauvé", "et dossier prêt pour l’inspecteur"), "EVD"),
        P("Les réservations qui ne se présentent pas",
          "Une table de huit ne vient pas un samedi : c’est le profit de la soirée qui disparaît.",
          "Réservations confirmées", "Réservation demandée par téléphone, même en plein service",
          ["JARVIS répond et réserve selon le plan de salle", "Confirmation la veille, annulation facile", "Table libérée offerte à la liste d’attente"],
          None, "Moins de tables vides",
          ("t", "≈ 6 h", "de téléphone par semaine en salle"), "E"),
        P("Le coût des aliments qui dérape",
          "Les prix des fournisseurs changent chaque semaine; la marge d’un plat disparaît sans qu’on le voie.",
          "Coût de recette toujours à jour", "Facture de fournisseur reçue",
          ["Prix lus et comparés à la semaine précédente", "Coût de chaque recette recalculé", "Plat sous la marge visée signalé"],
          "Le chef ajuste la recette ou le prix", "Marge protégée, plat par plat",
          ("r", "Marge suivie", "plutôt qu’une surprise à la fin du mois"), "EI"),
        P("Les remplacements de dernière minute",
          "Un serveur se dit malade à 15 h; le gérant passe une heure à texter tout le monde.",
          "Remplacement en un message", "Absence signalée",
          ["Employés disponibles et qualifiés repérés", "Offre envoyée à tous : le premier qui accepte a le quart"],
          "Le gérant confirme le remplacement", "Quart couvert en 15 minutes",
          ("t", "≈ 1 h", "par absence"), "E"),
        P("Les commandes de traiteur et les allergies",
          "Une commande d’événement arrive par courriel avec trois allergies glissées au milieu du texte.",
          "Commande d’événement structurée", "Courriel de commande reçu",
          ["Quantités, date et allergies extraites", "Fiche de production pour la cuisine", "Allergies surlignées sur chaque étiquette"],
          "Le chef valide la fiche", "Aucune allergie oubliée",
          ("r", "Allergies maîtrisées", "à chaque commande, sans exception"), "EI"),
    ]),
    ("hotellerie", "Hôtellerie, gîtes et campings", "Hôtels · gîtes · chalets locatifs · campings",
     "hôtel hotel hôtellerie motel auberge gîte gite chalet chalets locatifs location à court terme courte durée camping pourvoirie tourisme spa nordique centre de villégiature",
     "/media/solutions/jarvis-enterprise-operations-v1.webp", "Les clients arrivent à 23 h, partent à 7 h, et les questions arrivent à toute heure.", [
        P("Les arrivées tardives sans personne à l’accueil",
          "Un client arrive à minuit, la réception est fermée; il appelle le propriétaire, qui dort.",
          "Arrivée autonome", "Réservation confirmée, arrivée prévue après 21 h",
          ["Code d’accès unique créé pour la durée du séjour", "Instructions d’arrivée envoyées", "Chauffage réglé avant l’arrivée"],
          None, "Client installé sans réveiller personne",
          ("t", "≈ 5", "appels de nuit de moins par semaine"), "ESV"),
        P("Le ménage entre deux séjours",
          "Un départ tardif, une arrivée hâtive : l’équipe de ménage ne sait pas par où commencer.",
          "Planification du ménage", "Client parti : porte verrouillée, thermostat en veille",
          ["Chambre placée en tête de liste", "Préposée avisée avec la liste de la chambre", "Chambre marquée prête, avec photos"],
          "La gouvernante vérifie", "Chambre prête avant l’arrivée suivante",
          ("t", "≈ 1 h", "de coordination par jour"), "EVS"),
        P("Les mêmes questions des clients, jour et nuit",
          "Wi-Fi, heure de départ, restaurants, sentiers : les mêmes questions par texto, à toute heure.",
          "Conciergerie par texto", "Message d’un client",
          ["Réponse tirée de votre guide de l’établissement", "Demande spéciale (lit d’appoint) transmise à l’équipe"],
          "Une personne prend le relais si la demande est nouvelle", "Réponse en moins d’une minute, en français ou en anglais",
          ("t", "≈ 8 h", "par semaine"), "EI"),
        P("Le bruit et les dégâts découverts trop tard",
          "Une fête dans un chalet, les voisins se plaignent; le propriétaire l’apprend par un mauvais commentaire.",
          "Veille du bruit, respectueuse", "Niveau sonore élevé après 23 h (aucune voix enregistrée)",
          ["Message courtois au client", "Si le bruit continue : avis au propriétaire"],
          "Le propriétaire décide d’intervenir", "Voisins tranquilles, réputation intacte",
          ("r", "Réputation protégée", "et permis municipal préservé"), "ESV"),
    ]),
    ("commerce", "Commerce de détail", "Boutiques · quincailleries · épiceries",
     "commerce boutique magasin détaillant détail quincaillerie épicerie dépanneur fleuriste librairie animalerie vêtements meubles électronique bijouterie sport vélo commerce en ligne boutique en ligne",
     None, "Les clients veulent une réponse tout de suite, même quand la boutique est pleine.", [
        P("« L’avez-vous en stock? » au téléphone et en message",
          "Le commis laisse un client en magasin pour aller vérifier une tablette pour quelqu’un au téléphone.",
          "Réponse d’inventaire instantanée", "Question d’un client par téléphone, texto ou site",
          ["Article reconnu, même mal nommé", "Quantité lue dans la caisse", "Mise de côté proposée pour 24 heures"],
          None, "Client servi sans déranger l’équipe",
          ("t", "≈ 2 h", "par jour"), "E"),
        P("L’inventaire en magasin et en ligne qui ne concorde pas",
          "Un article vendu en ligne était déjà parti en magasin; il faut rembourser et s’excuser.",
          "Inventaire synchronisé", "Vente à la caisse",
          ["Quantité retirée de la boutique en ligne", "Seuil atteint : bon de commande préparé"],
          "Le gérant approuve la commande", "Plus aucune vente fantôme",
          ("r", "Remboursements évités", "et clients en ligne satisfaits"), "E"),
        P("Les pertes et le vol à l’étalage",
          "Les écarts d’inventaire s’accumulent; impossible de savoir où, quand ni comment.",
          "Écarts d’inventaire expliqués", "Écart entre l’inventaire et les ventes",
          ["Rayon et période de l’écart repérés", "Extraits vidéo de la période regroupés pour le gérant"],
          "Le gérant revoit et décide", "Écart compris, mesure ciblée",
          ("r", "Pertes réduites", "sans surveiller les employés au quotidien"), "ES"),
        P("Les commandes spéciales qui ne reviennent jamais",
          "Aucune trace de qui attend quoi; impossible de prévenir un client que son produit est arrivé.",
          "Relance personnalisée", "Commande spéciale reçue ou produit de nouveau en stock",
          ["Clients intéressés retrouvés", "Texto personnel avec mise de côté"],
          None, "Client de retour en boutique",
          ("r", "Ventes récupérées", "sur chaque commande spéciale"), "E"),
    ]),
    ("manufacturier", "Manufacturier et ateliers", "Usinage · transformation alimentaire · production",
     "manufacturier manufacture usine production atelier usinage machiniste soudure fabrication métal métallique plastique transformation alimentaire agroalimentaire imprimerie ébénisterie assemblage machinerie emballage",
     "/media/solutions/reseau-resilience.webp", "Une machine arrêtée, c’est toute la chaîne qui attend.", [
        P("Les bris de machine imprévus",
          "Un roulement chauffe depuis des jours; personne ne le voit avant l’arrêt complet de la ligne.",
          "Maintenance prédictive", "Vibration de la presse 3 en hausse de 30 %",
          ["Tendance comparée à l’historique de la machine", "Bon de travail préventif créé", "Pièce vérifiée en magasin, commandée au besoin"],
          "Le responsable de la maintenance planifie l’arrêt", "Réparation faite pendant un arrêt prévu",
          ("r", "Arrêt évité", "une heure d’arrêt de ligne coûte souvent des milliers de dollars"), "EDV"),
        P("Le cadenassage et les registres de santé et sécurité",
          "Les fiches de cadenassage et les inspections sont sur papier; après un accident, il faut tout prouver.",
          "Cadenassage guidé", "Intervention sur une machine",
          ["Fiche de cadenassage de cette machine affichée", "Chaque étape confirmée avec photo", "Registre signé et conservé"],
          "Le superviseur autorise la remise en marche", "Procédure respectée et prouvée",
          ("r", "Accident évité", "et conformité démontrable à la CNESST"), "ES"),
        P("La traçabilité des lots",
          "Un client signale un défaut; retrouver la matière, la machine et le quart qui ont produit ce lot prend des jours.",
          "Traçabilité en un clic", "Plainte d’un client sur le lot 24-1187",
          ["Matières premières, machine et quart retrouvés", "Lots semblables repérés", "Rapport préparé pour le client"],
          "Le responsable de la qualité approuve le rapport", "Réponse au client le jour même",
          ("t", "≈ 2 jours", "d’enquête ramenés à une heure"), "EI"),
        P("Les commandes clients retapées à la main",
          "Les bons de commande arrivent en PDF; quelqu’un les retape dans le système de production.",
          "Commandes lues et planifiées", "Bon de commande reçu par courriel",
          ["Articles, quantités et dates extraits", "Capacité de production vérifiée", "Date de livraison proposée au client"],
          "Le planificateur confirme la date", "Commande en production sans saisie",
          ("t", "≈ 10 h", "de saisie par semaine"), "EI"),
    ]),
    ("professionnels", "Services professionnels", "Comptables · notaires · avocats · assurances",
     "comptable comptabilité CPA tenue de livres teneur de livres notaire avocat avocate cabinet juridique droit courtier d'assurance assurances courtier hypothécaire conseiller financier planificateur financier fiscaliste impôts architecte ingénieur arpenteur-géomètre traducteur consultant",
     "/media/solutions/ia-privee-connaissances.webp", "Le temps facturable fond dans les relances, les pièces manquantes et les échéances.", [
        P("Les documents manquants en saison des impôts",
          "Feuillets, reçus, relevés : il manque toujours une pièce, et il faut relancer chaque client à la main.",
          "Collecte de documents guidée", "Dossier du client ouvert pour l’année",
          ["Liste personnalisée selon l’an dernier", "Dépôt sécurisé : chaque pièce reconnue et classée", "Relance polie pour ce qui manque"],
          "Le comptable confirme que le dossier est complet", "Dossier complet sans un seul appel",
          ("t", "≈ 45 min", "par dossier"), "EIR"),
        P("Les échéances qui ne doivent jamais être manquées",
          "Un délai de procédure, de prescription ou de production oublié, et c’est la responsabilité professionnelle qui est en jeu.",
          "Échéancier protégé", "Nouveau document au dossier",
          ["Dates et délais repérés dans le document", "Échéances inscrites avec rappels à 30, 7 et 1 jour", "Rappel au remplaçant si le responsable est absent"],
          "Le professionnel valide chaque échéance", "Aucune échéance manquée",
          ("r", "Faute évitée", "et assurance responsabilité protégée"), "EI"),
        P("Les conflits d’intérêts et l’ouverture de dossier",
          "Chaque nouveau mandat demande de chercher le nom dans tous les dossiers, puis de remplir les mêmes formulaires.",
          "Ouverture de dossier en deux minutes", "Nouveau client au formulaire",
          ["Recherche de conflits dans tous les dossiers", "Identité vérifiée selon vos règles", "Lettre de mandat préparée"],
          "L’associé approuve l’ouverture", "Mandat ouvert, conforme",
          ("t", "≈ 30 min", "par nouveau dossier"), "EI"),
        P("Le temps jamais facturé",
          "Courriels, appels de six minutes : le temps passé n’est jamais entré, donc jamais facturé.",
          "Temps capté automatiquement", "Appel ou courriel lié à un dossier",
          ["Durée et dossier repérés", "Entrée de temps proposée"],
          "Le professionnel accepte ou corrige", "Temps facturé plutôt qu’oublié",
          ("t", "≈ 3 h", "facturables récupérées par semaine"), "EI"),
    ]),
    ("immobilier", "Immobilier et gestion locative", "Courtiers · gestionnaires · propriétaires de plex",
     "immobilier courtier immobilier agent immobilier gestion locative gestionnaire immeuble immeubles propriétaire plex duplex triplex logement logements locataire locataires syndicat de copropriété copropriété condo concierge conciergerie",
     "/media/solutions/security-enterprise-parking-v1.webp", "Un dégât d’eau à 2 h du matin et un bail à renouveler : tout arrive en même temps.", [
        P("Les demandes d’entretien des locataires éparpillées",
          "Textos, appels, notes dans la porte : une fuite signalée en mars est oubliée jusqu’au dégât.",
          "Demandes d’entretien suivies", "Un locataire signale un robinet qui coule, avec photo",
          ["Urgence évaluée selon vos critères", "Bon de travail envoyé au bon fournisseur", "Locataire informé de la date de visite"],
          "Le gestionnaire approuve au-delà de 300 $", "Réparation faite et documentée",
          ("t", "≈ 4 h", "de coordination par semaine"), "E"),
        P("Les dégâts d’eau découverts trop tard",
          "Un chauffe-eau qui fuit dans un logement vacant, découvert par le locataire du dessous.",
          "Détection de fuite et intervention", "Capteur de fuite sous le chauffe-eau du 302",
          ["Valve d’eau fermée automatiquement", "Plombier de garde appelé", "Assureur et locataires touchés avisés"],
          "Le gestionnaire confirme l’intervention", "Dégât contenu à un seul logement",
          ("r", "Sinistre évité", "des dizaines de milliers de dollars"), "EVS"),
        P("Les avis de modification de bail hors délai",
          "Les avis de renouvellement doivent partir dans des délais précis; un oubli, et l’augmentation est perdue.",
          "Calendrier des baux", "Le bail du 4B entre dans sa période d’avis",
          ["Délai calculé selon la durée du bail", "Avis préparé avec l’augmentation proposée", "Envoi et preuve de réception conservés"],
          "Le propriétaire approuve le montant", "Avis envoyé à temps, preuve à l’appui",
          ("r", "Augmentation préservée", "et dossier solide devant le Tribunal administratif du logement"), "EI"),
        P("Les visites et les candidatures",
          "Vingt personnes écrivent pour un logement; il faut répondre à chacune, planifier, puis vérifier les candidatures.",
          "Location accompagnée", "Annonce publiée",
          ["Réponses aux questions fréquentes", "Visites regroupées en plages", "Candidatures complètes classées"],
          "Le propriétaire choisit son locataire", "Logement loué sans y passer ses soirées",
          ("t", "≈ 6 h", "par logement à louer"), "E"),
    ]),
    ("domicile", "Entretien et services à domicile", "Plombiers · électriciens · paysagistes · thermopompes",
     "plombier plomberie électricien électricité paysagiste paysagement aménagement paysager entretien ménager ménage femme de ménage frigoriste réfrigération climatisation thermopompe chauffage ventilation calfeutrage exterminateur gestion parasitaire ramoneur piscinier piscine nettoyage de vitres gouttières homme à tout faire",
     "/media/solutions/environnements-intelligents.webp", "Impossible de répondre au téléphone dans un vide sanitaire.", [
        P("Les appels manqués pendant qu’on est chez un client",
          "Chaque appel qui tombe dans la boîte vocale est un contrat qui part chez le concurrent.",
          "Réception pour les équipes terrain", "Appel entrant, le technicien est sous un évier",
          ["JARVIS répond, comprend le problème et note l’adresse", "Urgence (refoulement, panne) : technicien de garde avisé", "Sinon : rendez-vous pris dans l’horaire"],
          "Le technicien accepte l’urgence", "Contrat pris, pas perdu",
          ("r", "Contrats gardés", "plutôt que perdus dans la boîte vocale"), "EM"),
        P("L’horaire de la journée qui ne tient plus",
          "Trois appels de dernière minute, et l’horaire du matin est à refaire.",
          "Horaire et routes optimisés", "Nouvel appel de service ajouté",
          ["Routes recalculées pour l’équipe", "Clients avisés de leur nouvelle heure d’arrivée"],
          "Le répartiteur approuve les changements", "Moins de route, plus d’appels par jour",
          ("t", "≈ 1 h", "de route par technicien, par jour"), "EM"),
        P("Les factures faites le soir, à la maison",
          "Le technicien finit à 17 h, puis passe la soirée à faire ses factures et ses soumissions.",
          "Facture prête avant de quitter le client", "Le technicien dicte : « remplacé la valve, 1 h 30 »",
          ["Facture préparée avec pièces et main-d’œuvre", "Paiement sur place par lien", "Photos jointes au dossier du client"],
          "Le technicien relit et envoie", "Payé avant de reprendre la route",
          ("t", "≈ 5 h", "par semaine, et paiement reçu des semaines plus tôt"), "EIM"),
        P("Les entretiens saisonniers oubliés",
          "Thermopompes, ouverture de piscine, aération de pelouse : les clients oublient, et l’équipe a des semaines creuses.",
          "Contrats saisonniers renouvelés", "Mars : saison d’ouverture des piscines",
          ["Clients de l’an dernier repérés", "Créneaux offerts par quartier", "Agenda rempli d’avance"],
          None, "Saison remplie avant de commencer",
          ("r", "Revenu récurrent", "et semaines creuses comblées"), "EM"),
    ]),
    ("esthetique", "Salons, esthétique et soins", "Coiffure · esthétique · ongles · massothérapie",
     "salon salon de coiffure coiffure coiffeur coiffeuse barbier barbershop esthétique esthéticienne ongles manucure pédicure spa massothérapie massage tatouage tatoueur bronzage cils sourcils électrolyse épilation",
     None, "Les mains sont occupées toute la journée; le téléphone, lui, sonne quand même.", [
        P("Les rendez-vous oubliés et les absences",
          "Une cliente ne se présente pas : c’est une heure payée à attendre et une autre cliente refusée.",
          "Rappels et dépôt", "Rendez-vous pris",
          ["Dépôt demandé selon votre politique", "Rappel 24 heures avant", "Absence : liste d’attente avisée tout de suite"],
          None, "Moins d’absences, plages remplies",
          ("t", "≈ 3 h", "récupérées par semaine"), "E"),
        P("Les réservations prises entre deux clientes",
          "La coiffeuse répond au téléphone les mains pleines de teinture.",
          "Réservation au téléphone et par message", "Appel ou message",
          ["Service, durée et professionnelle compris", "Créneau proposé et confirmé"],
          None, "La coiffeuse ne lâche jamais sa cliente",
          ("t", "≈ 1 h", "par jour"), "E"),
        P("La prochaine visite jamais réservée",
          "La cliente part sans prendre rendez-vous; elle revient dans quatre mois plutôt que six semaines.",
          "Prochaine visite proposée", "Six semaines après la dernière visite",
          ["Rappel personnalisé avec sa professionnelle", "Deux créneaux proposés"],
          None, "Cliente de retour au bon moment",
          ("r", "Visites régulières", "et revenu plus stable"), "E"),
        P("Les produits de revente en rupture",
          "Le shampoing que tout le monde demande est en rupture depuis deux semaines.",
          "Commande de produits", "Seuil bas à la caisse",
          ["Quantité à commander calculée", "Bon de commande préparé"],
          "La propriétaire approuve", "Toujours en stock",
          ("r", "Ventes protégées", "sur les produits de revente"), "E"),
    ]),
    ("municipalites", "Organismes et municipalités", "Municipalités · OBNL · coopératives",
     "municipalité municipalités ville mairie MRC municipal travaux publics conseil municipal organisme OBNL organisme communautaire organisme sans but lucratif coopérative association fondation bénévoles bénévolat loisirs bibliothèque fabrique paroisse",
     None, "Beaucoup de demandes, peu de mains, et chaque dollar doit être justifié.", [
        P("Les requêtes citoyennes perdues entre les services",
          "Un nid-de-poule signalé par téléphone, un lampadaire par courriel : personne ne sait qui s’en occupe.",
          "Requêtes citoyennes suivies", "Un citoyen signale un lampadaire brisé, avec photo",
          ["Requête située sur la carte", "Envoyée au bon service avec un numéro de suivi", "Citoyen avisé quand c’est réglé"],
          "Le contremaître assigne l’équipe", "Requête réglée, et le citoyen le sait",
          ("t", "≈ 6 h", "par semaine au comptoir"), "EM"),
        P("Les avis urgents aux citoyens",
          "Avis d’ébullition, fermeture de rue, déneigement : il faut prévenir tout le monde, vite, et pas seulement sur les réseaux sociaux.",
          "Avis aux citoyens en quelques minutes", "Bris d’aqueduc sur la rue Principale",
          ["Secteur touché tracé sur la carte", "Message préparé en français et en anglais", "Envoyé par texto, appel et courriel aux résidents du secteur"],
          "La direction générale approuve le message", "Résidents avisés en 10 minutes",
          ("r", "Santé publique protégée", "et preuve d’envoi conservée"), "EM"),
        P("Les redditions de comptes de subventions",
          "Chaque subvention exige un rapport : heures, participants, dépenses. Tout est à compiler à la main.",
          "Rapport de subvention compilé", "Fin du trimestre",
          ["Heures, présences et dépenses regroupées", "Rapport rempli selon le gabarit du bailleur de fonds"],
          "La direction relit et signe", "Rapport déposé à temps",
          ("t", "≈ 2 jours", "par rapport"), "EI"),
        P("Les horaires de bénévoles",
          "Les disponibilités changent chaque semaine; les trous apparaissent la veille.",
          "Bénévoles coordonnés", "Quart sans bénévole, à 48 heures d’avis",
          ["Bénévoles disponibles invités", "Confirmation, puis rappel la veille"],
          None, "Quart couvert",
          ("t", "≈ 4 h", "de coordination par semaine"), "E"),
    ]),
    ("ecoles", "Écoles, garderies et CPE", "Garderies · CPE · écoles privées · camps de jour",
     "école écoles garderie garderies CPE centre de la petite enfance service de garde milieu familial camp de jour éducatrice éducateur enseignant enseignante école privée centre de formation tutorat école de conduite école de musique",
     None, "Les parents veulent savoir; la direction veut que tout soit en règle.", [
        P("Les absences signalées au téléphone le matin",
          "Entre 7 h et 9 h, le téléphone ne dérougit pas; une absence non signalée doit être vérifiée.",
          "Absences et retards à la minute", "Un parent appelle ou écrit : « Léa est malade »",
          ["Enfant identifié, absence inscrite", "Éducatrice avisée", "Enfant absent non signalé : parent joint"],
          None, "Chaque enfant est localisé",
          ("r", "Sécurité des enfants", "aucune absence inexpliquée"), "E"),
        P("Les ratios et les présences à rapporter",
          "Les ratios éducatrice-enfants se respectent à chaque heure, et les fiches d’assiduité financent le service.",
          "Présences et ratios en direct", "Arrivées et départs à la tablette de l’entrée",
          ["Ratio calculé par groupe, en temps réel", "Alerte si un groupe dépasse", "Fiches d’assiduité produites à la fin du mois"],
          "La direction déplace une éducatrice", "Ratios respectés, rapport prêt",
          ("t", "≈ 6 h", "de compilation par mois"), "E"),
        P("Le journal de bord aux parents écrit le soir",
          "Repas, siestes, activités, photos : l’éducatrice écrit le soir plutôt que d’être avec les enfants.",
          "Journal de la journée assisté", "Fin de la journée",
          ["Repas, siestes et activités notés au fil de la journée", "Résumé rédigé pour chaque parent"],
          "L’éducatrice relit avant l’envoi", "Parents informés, éducatrice libérée",
          ("t", "≈ 30 min", "par éducatrice, par jour"), "EI"),
        P("La liste d’attente et les inscriptions",
          "Des centaines de familles en attente; une place se libère et personne ne sait qui appeler en premier.",
          "Liste d’attente tenue à jour", "Une place se libère dans le groupe des 18 mois",
          ["Famille prioritaire repérée selon vos critères", "Offre envoyée, délai de réponse suivi", "Dossier d’inscription préparé"],
          "La direction confirme l’offre", "Place comblée en 48 heures",
          ("t", "≈ 5 h", "par place à combler"), "E"),
    ]),
    ("residences", "Résidences pour aînés et soins", "RPA · soins à domicile · ressources intermédiaires",
     "résidence pour aînés résidences RPA résidence pour personnes âgées aînés CHSLD privé ressource intermédiaire soins à domicile maison de retraite préposé aux bénéficiaires infirmière infirmière auxiliaire soins infirmiers soutien à domicile",
     None, "La nuit, une seule personne veille parfois sur des dizaines de résidents.", [
        P("Les chutes de nuit découvertes à la ronde",
          "Un résident tombe en se rendant à la salle de bain; il attend au sol jusqu’à la ronde suivante.",
          "Veille de nuit discrète", "Sortie du lit sans retour depuis 10 minutes (capteur, aucune caméra dans la chambre)",
          ["Préposée de nuit avisée avec le numéro de chambre", "Infirmière avisée si personne ne répond en 3 minutes", "Événement consigné au dossier"],
          "La préposée confirme son arrivée", "Résident aidé en quelques minutes",
          ("r", "Chute prise à temps", "plutôt qu’une longue attente au sol"), "EVS"),
        P("Les appels des familles",
          "Les familles appellent pour avoir des nouvelles; chaque appel interrompt les soins.",
          "Nouvelles aux familles", "Appel d’un proche autorisé",
          ["Proche identifié, autorisation vérifiée", "Nouvelles non médicales partagées (activités, repas)", "Question de santé : rappel planifié par l’infirmière"],
          "L’infirmière rappelle pour la santé", "Familles rassurées, soins non interrompus",
          ("t", "≈ 1 h 30", "par jour"), "EI"),
        P("Les registres de distribution des médicaments",
          "Chaque dose doit être consignée; une feuille oubliée est un risque pour le résident et pour la certification.",
          "Distribution de médicaments guidée", "Tournée de 8 h",
          ["Liste par résident, dose par dose", "Dose manquée signalée tout de suite", "Registre complet pour la visite de certification"],
          "L’infirmière valide chaque écart", "Aucune dose oubliée",
          ("r", "Erreur évitée", "et certification protégée"), "EI"),
    ]),
    ("deneigement", "Déneigement et excavation", "Déneigement · excavation · terrassement",
     "déneigement déneigeur souffleuse neige tracteur excavation excavatrice terrassement pavage asphalte drainage transport de neige épandage abrasif sel entrepreneur en déneigement",
     None, "Une tempête à 3 h du matin, 400 entrées à dégager et autant de clients impatients.", [
        P("« Vous n’êtes pas encore passés! » au téléphone",
          "Après chaque tempête, le bureau est submergé d’appels de clients qui attendent leur passage.",
          "Avis de passage automatiques", "Le tracteur termine une entrée",
          ["Passage confirmé par la position du véhicule", "Texto au client avec l’heure", "Client qui appelle : sa place dans la tournée"],
          None, "Moins d’appels, clients rassurés",
          ("t", "≈ 70", "appels de moins par tempête"), "EM"),
        P("Les preuves de passage contestées",
          "Un client commercial conteste un passage; une chute sur son terrain, et c’est votre assurance qui est visée.",
          "Preuve de passage horodatée", "Passage ou épandage d’abrasif terminé",
          ["Photo, heure et position enregistrées", "Registre par client conservé toute la saison"],
          None, "Preuve fournie en 10 secondes",
          ("r", "Réclamation évitée", "et dossier solide devant l’assureur"), "EMS"),
        P("Le départ des équipes selon la météo",
          "Faut-il réveiller les opérateurs à 2 h? Le patron se lève toutes les heures pour regarder le radar.",
          "Veille météo et rappel des équipes", "Prévision : 8 cm d’ici 5 h",
          ["Seuil de vos contrats atteint", "Opérateurs appelés selon leurs tournées", "Abrasif et carburant vérifiés"],
          "Le patron confirme le départ", "Équipes sur la route au bon moment",
          ("r", "Départ à temps", "et des nuits complètes pour le patron"), "EMV"),
        P("Les contrats saisonniers à renouveler",
          "Chaque automne, il faut relancer 400 clients, recueillir les signatures et les paiements.",
          "Renouvellement en un clic", "1er septembre",
          ["Contrat de l’an dernier reconduit au nouveau tarif", "Signature et paiement en ligne", "Relance des retardataires"],
          "Le patron approuve les tarifs", "Saison vendue avant la première neige",
          ("t", "≈ 40 h", "par automne"), "E"),
    ]),
    ("sport", "Centres sportifs et loisirs", "Gyms · studios · arénas · clubs",
     "gym gymnase centre de conditionnement physique entraînement entraîneur yoga pilates studio crossfit aréna club sportif piscine escalade golf curling ski centre de ski loisirs centre récréatif arts martiaux danse",
     None, "Les membres veulent de la souplesse; l’équipe veut moins de paperasse.", [
        P("L’accès en dehors des heures de personnel",
          "Les membres veulent s’entraîner à 5 h; impossible d’avoir quelqu’un à l’accueil.",
          "Accès membre sécurisé", "Un membre présente son téléphone à la porte",
          ["Abonnement actif vérifié", "Porte déverrouillée, entrée consignée", "Bouton d’aide relié à une personne de garde"],
          None, "Ouvert plus longtemps, sans accueil",
          ("r", "Heures prolongées", "sans ajouter de quarts de travail"), "ESV"),
        P("Les paiements refusés et les abonnements échus",
          "Une carte expire, le paiement est refusé, et personne ne relance pendant des mois.",
          "Relance de paiement courtoise", "Paiement refusé",
          ["Message au membre avec un lien de mise à jour", "Deuxième rappel après trois jours"],
          "Le gérant décide de suspendre ou non", "Paiement régularisé",
          ("r", "Revenus récupérés", "sur les paiements échoués"), "E"),
        P("Les réservations de cours, de glaces et de terrains",
          "Cours complets, listes d’attente, heures de glace : tout se gère au téléphone et au chiffrier.",
          "Réservations et liste d’attente", "Désistement à un cours complet",
          ["Première personne de la liste avisée", "Place confirmée en un clic"],
          None, "Cours plein, sans intervention",
          ("t", "≈ 5 h", "par semaine"), "E"),
    ]),
]


def fr2(s):
    """fr() + espaces insécables avant les unités courantes."""
    s = fr(s)
    return re.sub(r"(\d) (°C|%|km|cm|min|jours?\b)", rf"\1{NBSP}\2", s)


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("’", "'")


PHOTOS_SECTEURS = []  # (fichier, description) : photos que James peut générer


def _sect_photo(slug, repli):
    PHOTOS_SECTEURS.append(slug)
    if os.path.exists(os.path.join(_MEDIA_SECT, slug + ".webp")):
        return "/media/secteurs/" + slug + ".webp"
    return repli


SE_ICONS = {
    "trig": '<path d="M13 3 5 13.5h6L10 21l8-10.5h-6z"/>',
    "step": '<circle cx="12" cy="12" r="3.2"/><path d="M12 3.5v2.3M12 18.2v2.3M3.5 12h2.3M18.2 12h2.3M6 6l1.6 1.6M16.4 16.4 18 18M6 18l1.6-1.6M16.4 7.6 18 6"/>',
    "hum": '<circle cx="10" cy="8" r="3.6"/><path d="M3.5 20c.4-3.6 3.1-6 6.5-6 1.3 0 2.4.3 3.4.8"/><path d="m15 18 2 2 4-4.2"/>',
    "res": '<circle cx="12" cy="12" r="8.5"/><path d="m8.2 12.3 2.5 2.5 5.1-5.3"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    "photo": '<rect x="3" y="5.5" width="18" height="14" rx="2.5"/><circle cx="12" cy="12.5" r="3.4"/><path d="M8.5 5.5 10 3.5h4l1.5 2"/>',
    "time": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "shield": '<path d="M12 3.5 19 6v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="m9 11.8 2.2 2.2 3.8-4"/>',
}


def se_icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#se-i-{name}"/></svg>'


def _sprite():
    syms = "".join(f'<symbol id="se-i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in SE_ICONS.items())
    return f'<svg class="se-sprite" aria-hidden="true" focusable="false">{syms}</svg>'


def _photo_html(src, name, cls):
    if src:
        return f'<span class="{cls}"><img src="{src}" alt="" loading="lazy" decoding="async"></span>'
    return (f'<span class="{cls} is-none" role="img" aria-label="{name} · photo à venir">'
            f'{se_icon("photo")}<small>Photo à venir</small></span>')


def _ext_chips(keys):
    return "".join(
        f'<a class="se-ext{" is-main" if k == "E" else ""}" href="/solutions/{EXT[k][1]}/">{EXT[k][0]}</a>' for k in keys
    )


def _flow(pn, sid, i):
    nodes = [("trig", "Déclencheur", pn["trig"])]
    nodes += [("step", f"JARVIS · étape {j + 1}", s) for j, s in enumerate(pn["steps"])]
    if pn["h"]:
        nodes.append(("hum", "Validation humaine", pn["h"]))
    nodes.append(("res", "Résultat", pn["r"]))
    items = "".join(
        f'<li class="se-n is-on" data-kind="{k}"><span class="se-ni">{se_icon(k)}</span>'
        f'<span class="se-nc"><small>{lab}</small><b>{fr2(t)}</b>'
        + ('<em class="se-hs" data-hs>Validé</em>' if k == "hum" else "")
        + '</span></li>'
        for k, lab, t in nodes
    )
    return f'<ol class="se-flow" aria-label="Déroulement de l’automatisation">{items}</ol>'


def _detail(pn, sid, i):
    kind, big, small = pn["g"]
    glab = "Temps gagné" if kind == "t" else "Risque évité"
    return f"""<div class="se-det" data-paind="{i}" id="se-{sid}-{i}" role="tabpanel"{'' if i == 0 else ' hidden'}>
      <div class="se-ba">
        <div class="se-before"><small>Aujourd’hui</small><b>{fr2(pn['p'])}</b><p>{fr2(pn['d'])}</p></div>
        <span class="se-arrow" aria-hidden="true"></span>
        <div class="se-after"><small>Avec JARVIS</small><b>{fr2(pn['a'])}</b><p>{fr2(pn['r'])}.</p></div>
      </div>
      {_flow(pn, sid, i)}
      <div class="se-foot">
        <div class="se-gain is-{kind}">{se_icon('time' if kind == 't' else 'shield')}<span><small>{glab} · estimation</small><b>{fr2(big)}</b><em>{fr2(small)}</em></span></div>
        <div class="se-exts"><small>Extensions</small><span>{_ext_chips(pn['x'])}</span></div>
      </div>
    </div>"""


def _view(sec, first):
    slug, name, sub, _k, repli, intro, pains = sec
    src = _sect_photo(slug, repli)
    keys = []
    for pn in pains:
        for k in pn["x"]:
            if k not in keys:
                keys.append(k)
    keys.sort(key=lambda k: "EVISRDM".index(k))
    tabs = "".join(
        f'<li><button type="button" class="se-pain{" is-on" if i == 0 else ""}" data-pain="{i}" role="tab" '
        f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="se-{slug}-{i}">'
        f'<small>{i + 1:02d}</small><span><b>{fr2(pn["p"])}</b><em>{fr2(pn["a"])}</em></span></button></li>'
        for i, pn in enumerate(pains)
    )
    details = "".join(_detail(pn, slug, i) for i, pn in enumerate(pains))
    return f"""<article class="se-view" data-secp="{slug}" id="secteur-{slug}"{'' if first else ' hidden'}>
    <header class="se-vhead">
      {_photo_html(src, name, 'se-vph')}
      <div class="se-vcap">
        <p class="se-kick">Votre secteur · {len(pains)} automatisations</p>
        <h4>{fr2(name)}</h4>
        <p class="se-sub">{fr2(sub)}</p>
        <p class="se-intro">{fr2(intro)}</p>
        <p class="se-vexts">{_ext_chips(keys)}</p>
      </div>
    </header>
    <div class="se-vbody">
      <div class="se-side">
        <p class="se-k">Les vrais problèmes du métier</p>
        <ol class="se-pains" role="tablist" aria-label="Problèmes du secteur {fr2(name)}">{tabs}</ol>
      </div>
      <div class="se-main">
        <div class="se-mbar"><p class="se-k">L’automatisation · du déclencheur au résultat</p>
          <button type="button" class="se-replay" data-se-replay>{REPLAY}Rejouer</button></div>
        {details}
      </div>
    </div>
  </article>"""


def secteurs_html():
    PHOTOS_SECTEURS.clear()
    n_auto = sum(len(s[6]) for s in SECTEURS)
    cards = []
    for i, sec in enumerate(SECTEURS):
        slug, name, sub, kw, repli, _intro, pains = sec
        src = repli
        if os.path.exists(os.path.join(_MEDIA_SECT, slug + ".webp")):
            src = "/media/secteurs/" + slug + ".webp"
        k = _norm(" ".join([name, sub, kw] + [p["p"] + " " + p["a"] for p in pains]))
        cards.append(
            f'<li><button type="button" class="se-card{" is-on" if i == 0 else ""}" data-sec="{slug}" '
            f'aria-pressed="{"true" if i == 0 else "false"}" aria-controls="secteur-{slug}" data-k="{k}">'
            f'{_photo_html(src, name, "se-ph")}'
            f'<span class="se-cap"><b>{fr2(name)}</b><small>{fr2(sub)}</small></span>'
            f'<em class="se-cnt">{len(pains)}</em></button></li>'
        )
    views = "".join(_view(sec, i == 0) for i, sec in enumerate(SECTEURS))
    sugg = ["vétérinaire", "plombier", "ferme laitière", "restaurant", "garage", "notaire", "garderie", "déneigement"]
    chips = "".join(f'<button type="button" class="se-sug" data-sug="{s}">{s}</button>' for s in sugg)
    return f"""<div class="au-sect se" data-secteurs data-rev id="votre-secteur">
  {_sprite()}
  <div class="se-head">
    <p class="eyebrow">Votre secteur</p>
    <h3>Votre métier a ses casse-têtes. <em>JARVIS les connaît.</em></h3>
    <p>{len(SECTEURS)} secteurs du Québec, {n_auto} problèmes bien réels — et pour chacun, l’automatisation qui le règle,
    étape par étape, avec un humain aux commandes quand il le faut. Choisissez votre secteur ou tapez votre métier.</p>
  </div>
  <div class="se-search">
    <label class="se-field">{se_icon('search')}<span class="se-vh">Tapez votre métier</span>
      <input type="search" data-se-q placeholder="Tapez votre métier : vétérinaire, couvreur, érablière…" autocomplete="off" spellcheck="false"></label>
    <p class="se-sugs"><span>Essayez :</span>{chips}</p>
    <p class="se-count" data-se-count aria-live="polite">{len(SECTEURS)} secteurs · {n_auto} automatisations</p>
  </div>
  <ul class="se-cards" data-se-cards>{''.join(cards)}</ul>
  <p class="se-empty" data-se-empty hidden>Votre métier n’est pas encore dans la liste? <a href="/contact/">Décrivez-nous votre journée</a> :
  s’il y a des appels, des papiers ou des vérifications qui se répètent, ça s’automatise.</p>
  <div class="se-stage" data-se-stage>{views}</div>
  <p class="se-note">Données d’exemple · les gains sont des estimations, pas des mesures réelles · chaque automatisation est conçue et validée avec vous</p>
</div>"""


SECTEURS_HTML = secteurs_html()
