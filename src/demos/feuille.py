# Feuille de route réelle du logiciel JARVIS (assets/demos/feuille.css et .js).
# Source : docs/FEUILLE_DE_ROUTE.md du dépôt jarvis — étape en cours : 1, Noyau,
# comptes et interfaces. À mettre à jour ici quand l'étape en cours change.
# Deux vues : la piste des chantiers (haut) et le tableau filtrable par solution et par
# état (Existe · En construction · À venir). Données réelles : aucune mention « démo ».

import re

from demos.vision import SOL, SOL_ORDER, chip, icon

NBSP = " "
CURRENT, TOTAL = 1, 20  # étape en cours, dernière étape avant la vente


def fr(s):
    """Espaces insécables de la typographie française."""
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NBSP}\2", s)
    s = re.sub(r"(\d) (h|Ah|W|jours|%)\b", rf"\1{NBSP}\2", s)
    s = re.sub(r" ([:;?!»])", rf"{NBSP}\1", s)
    return s


# (étapes, titre, texte, état) — état : done · now · next · vision
STAGES = [
    ("Étape 0", "Fondations",
     "Règles, garde-fous et vérifications automatiques à chaque changement.", "done"),
    ("Étapes 1 à 14", "Le logiciel",
     "En cours : noyau, comptes et interfaces — invitations, connexion sécurisée, rôles, journal, "
     "coffre des secrets, sauvegardes dont la restauration est prouvée.", "now"),
    ("Étape 15", "Mise en service",
     "Le logiciel installé sur le Hub du laboratoire mobile, à côté de l’ancien système.", "next"),
    ("Étapes 16 à 19", "Environnements intelligents",
     "Appareils, éclairage, tableau du véhicule, puis 14 jours en parallèle avant d’arrêter l’ancien.", "next"),
    ("Étape 20", "Prêt à vendre",
     "Revue de sécurité par un expert externe, test d’intrusion, Loi 25, guide et support.", "next"),
    ("Ensuite", "Les extensions",
     "Entreprise, IA et connaissances, puis les autres : une à la fois, chacune prouvée.", "vision"),
]
STATE = {"done": "Terminée", "now": f"En cours · étape {CURRENT}", "next": "À venir", "vision": "Vision"}

# Tableau : (solution, état, repère, titre, texte) — état : existe · construit · avenir
ETATS = [("existe", "Existe"), ("construit", "En construction"), ("avenir", "À venir")]
ITEMS = [
    ("hub", "existe", "Étape 0", "Fondations et garde-fous",
     "Un changement qui brise une règle d’architecture est refusé automatiquement."),
    ("env", "existe", "Laboratoire mobile", "Les lumières du véhicule, pilotées",
     "Le premier JARVIS, sur Home Assistant, garde déjà l’éclairage du laboratoire mobile."),
    ("mob", "existe", "Laboratoire mobile", "Un véhicule réel sur la route",
     "Une Ford 2017 V10 convertie : 560 Ah LiFePO₄ et 500 W solaires."),
    ("diag", "existe", "Laboratoire mobile", "Des batteries mesurées en vrai",
     "Charge, tension et température réelles, suivies au quotidien."),
    ("ia", "existe", "Ce site", "Démonstration : vos documents, avec la source",
     "Le fonctionnement visé, montré avec des données d’exemple."),
    ("secu", "existe", "Ce site", "Démonstration : un seul fil pour la sécurité",
     "Caméras, accès et alarmes réunis, montrés avec des données d’exemple."),
    ("res", "existe", "Ce site", "Démonstration : la carte du réseau",
     "Douze modules en mots simples, montrés avec des données d’exemple."),
    ("hub", "construit", "Étape 1", "Noyau, comptes et interfaces",
     "Premier démarrage, compte propriétaire, invitation par lien, code à usage unique et codes de secours."),
    ("hub", "construit", "Étape 1", "Journal, rôles et coffre des secrets",
     "Chaque accès tracé, chaque secret rangé à part, chaque compte suspendu aussitôt."),
    ("hub", "construit", "Étape 1", "Les deux interfaces Signature",
     "Côté personne et côté admin, avec une sauvegarde dont la restauration est prouvée."),
    ("hub", "avenir", "Étape 2", "Les prises des extensions",
     "Paquets signés, approbation, attribution et retrait des plugins et des extensions."),
    ("hub", "avenir", "Étape 3", "Le Hub au complet",
     "Mises à jour signées avec retour en arrière, accès à distance par un relais qui ne garde rien."),
    ("secu", "avenir", "Étape 4", "Personnes, accès et sécurité",
     "Groupes, droits effectifs, sessions, clés d’accès, export et suppression de ses données."),
    ("ia", "avenir", "Étapes 9 et 10", "Documents et recherche",
     "Documents rangés sur le Hub; un droit retiré fait disparaître le résultat partout."),
    ("auto", "avenir", "Étape 12", "Règles et automatisations",
     "Une règle simulée sans effet, puis activée, ne se déclenche qu’une seule fois."),
    ("ia", "avenir", "Étape 13", "Assistant IA local",
     "Local par défaut; un envoi vers un fournisseur distant est refusé sans accord."),
    ("mob", "avenir", "Étape 15", "Mise en service sur le laboratoire mobile",
     "Le nouveau logiciel sur le Hub du véhicule, à côté de l’ancien."),
    ("env", "avenir", "Étapes 16 et 17", "Appareils et éclairage",
     "Valeurs réelles mises à jour en moins d’une seconde, ambiances avec des états honnêtes."),
    ("diag", "avenir", "Étape 18", "Tableau du véhicule",
     "Énergie, confort, eau, Internet et équipements, avec leurs vraies données."),
    ("env", "avenir", "Étape 19", "Arrêt de l’ancien JARVIS",
     "14 jours en parallèle, puis un retour en arrière essayé en moins d’une heure."),
    ("secu", "avenir", "Étape 20", "Revue de sécurité externe",
     "Test d’intrusion, Loi 25, guide et support : rien ne se vend avant."),
    ("auto", "avenir", "Étape 21", "Extension Entreprise",
     "Réception, bons de travail et approbations, d’après des entrevues avec des entreprises."),
    ("res", "avenir", "Après la vente", "Plusieurs Hubs reliés",
     "Maison, chalet, entreprise et véhicule coordonnés, chacun avec ses propres règles."),
    ("secu", "avenir", "Vision", "Firme de sécurité privée",
     "Permis d’agence, assurance et analystes vérifiés avant toute mission réelle."),
]


def _board():
    counts = {k: sum(1 for it in ITEMS if it[1] == k) for k, _ in ETATS}
    sols = '<button type="button" class="fr-f is-on" data-sol="all" aria-pressed="true"><b>Toutes</b></button>' + "".join(
        f'<button type="button" class="fr-f" data-sol="{k}" aria-pressed="false" style="--x:{SOL[k][4]}">'
        f'{icon(k)}<b>{SOL[k][2]}</b></button>'
        for k in SOL_ORDER
    )
    sts = "".join(
        f'<button type="button" class="fr-s fr-s-{k} is-on" data-st="{k}" aria-pressed="true">'
        f'<i aria-hidden="true"></i>{lab}<em>{counts[k]}</em></button>'
        for k, lab in ETATS
    )
    lab = dict(ETATS)
    cards = "".join(
        f'<li class="fr-c fr-c-{st}" data-sol="{sol}" data-st="{st}" style="--x:{SOL[sol][4]}">'
        f'<div class="fr-c-top">{chip(sol)}<span class="fr-c-st"><i aria-hidden="true"></i>{lab[st]}</span></div>'
        f'<p class="fr-c-k">{rep}</p><h4>{fr(t)}</h4><p class="fr-c-t">{fr(x)}</p></li>'
        for sol, st, rep, t, x in ITEMS
    )
    return f"""<div class="fr-board">
    <div class="fr-tools">
      <div class="fr-fs" role="group" aria-label="Filtrer par solution">{sols}</div>
      <div class="fr-ss" role="group" aria-label="Filtrer par état">{sts}</div>
    </div>
    <p class="fr-count" aria-live="polite"><b>{len(ITEMS)}</b> jalons affichés</p>
    <ul class="fr-grid">{cards}</ul>
    <p class="fr-empty" hidden>Aucun jalon pour ce filtre. Essayez un autre état.</p>
  </div>"""


def html():
    items = "".join(
        f'<li class="fr-{st}" style="--i:{i}"><span class="fr-seg" aria-hidden="true"><i class="fr-fill"></i></span>'
        f'<span class="fr-dot" aria-hidden="true"></span>'
        f'<p class="fr-k">{steps}</p><h3>{title}</h3><p class="fr-t">{fr(text)}</p>'
        f'<span class="fr-chip">{STATE[st]}</span></li>'
        for i, (steps, title, text, st) in enumerate(STAGES)
    )
    return f"""<div class="fr" data-demo="feuille" data-rev>
  <div class="fr-head">
    <p><b>Étape {CURRENT}</b> sur {TOTAL} avant la mise en vente · une étape n’est terminée que lorsqu’elle est vérifiée à l’écran</p>
  </div>
  <ol class="fr-track">{items}</ol>
  {_board()}
</div>"""
