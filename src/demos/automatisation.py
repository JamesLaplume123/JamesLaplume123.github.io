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
