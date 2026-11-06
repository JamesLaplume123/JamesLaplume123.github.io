# Feuille de route réelle du logiciel JARVIS (assets/demos/feuille.css et .js).
# Source : docs/FEUILLE_DE_ROUTE.md du dépôt jarvis — étape en cours : 1, Noyau,
# comptes et interfaces. À mettre à jour ici quand l'étape en cours change.
# Données réelles : aucune mention « démo ».

import re

NBSP = " "
CURRENT, TOTAL = 1, 20  # étape en cours, dernière étape avant la vente


def fr(s):
    """Espaces insécables de la typographie française."""
    s = re.sub(r"(\d) (\d{3})\b", rf"\1{NBSP}\2", s)
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
     "IA et connaissances, Personal Intelligence, Security Pro, Multi-Site : une à la fois, chacune prouvée.", "vision"),
]
STATE = {"done": "Terminée", "now": f"En cours · étape {CURRENT}", "next": "À venir", "vision": "Vision"}


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
</div>"""
