#!/usr/bin/env python3
"""Garde-fou du terminal (outil Bash), pour tous.

Arrête les formes ordinaires, pas une volonté de contourner :
- l'essai témoin « : site-temoin » (refusé avec le mot « Témoin », preuve que les garde-fous tournent) ;
- tout envoi vers main, tout envoi forcé, tout commit sur main ;
- l'écriture d'un fichier de règles par le terminal (le chef les écrit avec Edit ou Write, en clair) ;
- la lecture ou l'écriture d'un secret.
"""

import os
import re
import shlex
import subprocess
import sys

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from regles import decision, est_secret, executer, lire_entree, racine_du_projet  # noqa: E402
except Exception as e:  # noqa: BLE001
    print(f"Garde-fou en panne ({type(e).__name__}: {e}) : refus par prudence.", file=sys.stderr)
    sys.exit(2)

REGLES_DANS_COMMANDE = re.compile(
    r"(?i)(?<![\w/.-])(\./)?(CLAUDE\.md|docs/SITE\.md|docs/plan_du_site\.json|docs/OFFRE\.md|scripts/check\.sh"
    r"|scripts/verifier_[\w.-]*|\.claude/[\w./-]*|\.githooks/[\w./-]*|\.github/[\w./-]*)")
ECRIVAINS = {"tee", "mv", "cp", "rm", "truncate", "chmod", "ln", "install", "touch", "dd"}
REDIRECTION = re.compile(r"(?<![0-9&])>>?\s*['\"]?([^\s'\";|&]+)")


def branche_courante(dossier):
    try:
        r = subprocess.run(["git", "-C", dossier, "symbolic-ref", "--short", "-q", "HEAD"],
                           capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def morceaux(commande):
    """Les commandes simples d'une ligne (séparées par ; && || | et retours de ligne)."""
    for partie in re.split(r"\|\||&&|[;|\n]", commande):
        try:
            mots = shlex.split(partie, comments=True)
        except ValueError:
            mots = partie.split()
        if mots:
            yield mots


def git_sous_commande(mots):
    """Pour « git [-C x] [-c a=b] push … », rend ('push', [arguments]) ; sinon (None, [])."""
    if not mots or os.path.basename(mots[0]) != "git":
        return None, []
    i = 1
    while i < len(mots) and mots[i].startswith("-"):
        i += 2 if mots[i] in ("-C", "-c", "--git-dir", "--work-tree") else 1
    return (mots[i], mots[i + 1:]) if i < len(mots) else (None, [])


def corps():
    donnees = lire_entree()
    commande = (donnees.get("tool_input") or {}).get("command") or ""
    if not isinstance(commande, str):
        decision("deny", "Commande illisible : refus par prudence.")
    dossier = donnees.get("cwd") if isinstance(donnees.get("cwd"), str) else racine_du_projet(donnees)

    if re.search(r"(^|[;&|\s]):\s+site-temoin\b", commande):
        decision("deny", "Témoin : les garde-fous du site sont chargés.")

    for mots in morceaux(commande):
        sous, args = git_sous_commande(mots)
        if sous == "push":
            if any(a in ("-f", "--force", "--force-with-lease", "--force-if-includes", "--mirror", "--delete", "-d")
                   or a.startswith("--force") or (a.startswith("+") and len(a) > 1) for a in args):
                decision("deny", "Envoi forcé ou suppression refusé : l'historique publié ne se réécrit pas.")
            cibles = [a for a in args if not a.startswith("-")][1:]
            if any(re.search(r"(^|:|/)main$", c) for c in cibles):
                decision("deny", "Envoi vers main refusé : main change seulement par une demande de fusion "
                                 "acceptée par James.")
            if not cibles and branche_courante(dossier) == "main":
                decision("deny", "Tu es sur main : crée une branche (git switch -c <nom>) avant d'envoyer.")
        if sous == "commit" and branche_courante(dossier) == "main":
            decision("deny", "Commit sur main refusé : crée une branche (git switch -c <nom>).")
        if sous is None:
            for m in mots[1:]:
                if est_secret(m):
                    decision("deny", f"Bloqué : {m} est un fichier secret. Les secrets ne passent jamais par un agent.")

    refus = ("Un fichier de règles ne s'écrit pas par le terminal : le chef l'écrit avec Edit ou Write, "
             "en le nommant en clair, avec l'accord de James.")
    for cible in REDIRECTION.findall(commande):
        if REGLES_DANS_COMMANDE.fullmatch(cible.lstrip("./") if not cible.startswith(".claude") and not cible.startswith(".git") else cible) \
                or REGLES_DANS_COMMANDE.search(cible):
            decision("deny", refus)
    for mots in morceaux(commande):
        nom = os.path.basename(mots[0])
        if (nom in ECRIVAINS or (nom == "sed" and any(m.startswith("-i") for m in mots[1:]))) \
                and any(REGLES_DANS_COMMANDE.search(m) for m in mots[1:]):
            decision("deny", refus)


executer(corps)
