"""Règles communes aux garde-fous du site JARVIS (repris du logiciel JARVIS, ADR-007 et ADR-009).

Ce module est lu par les scripts de .claude/hooks/. Il ne fait rien seul.
- La décision porte sur la cible réelle du chemin (`..`, liens symboliques et majuscules résolus).
- En cas d'entrée inutilisable ou d'erreur, on refuse par prudence.
"""

import fnmatch
import json
import os
import sys

# Fichiers de règles : un agent peut proposer, mais seul le chef les écrit, avec l'accord de James.
FICHIERS_DE_REGLES = {"claude.md", "docs/site.md", "docs/plan_du_site.json", "docs/offre.md", "scripts/check.sh"}
DOSSIERS_DE_REGLES = (".claude/", ".github/", ".githooks/")
PREFIXES_DE_REGLES = ("scripts/verifier_",)

# Secrets : jamais écrits ni lus par un agent.
MOTIFS_DE_SECRETS = (".env", ".env.*", "*.pem", "*.key", ".dev.vars", "wrangler.toml", "secrets.*",
                     "id_rsa*", "id_ed25519*", "*.p12", ".npmrc")
EXCEPTIONS_DE_SECRETS = ("wrangler.toml.example", ".env.example")


class EntreeInutilisable(Exception):
    """L'entrée JSON du hook est absente, invalide ou mal formée."""


def lire_entree():
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as e:
        raise EntreeInutilisable(f"entrée JSON invalide ({e})") from None
    if not isinstance(donnees, dict):
        raise EntreeInutilisable("l'entrée n'est pas un objet JSON")
    entree = donnees.get("tool_input")
    if entree is not None and not isinstance(entree, dict):
        raise EntreeInutilisable("tool_input n'est pas un objet")
    return donnees


def racine_du_projet(donnees):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or donnees.get("cwd") or os.getcwd())


def chemin_vise(donnees):
    """(relatif, dans_le_projet, réel) du fichier visé par Edit/Write ; ('', True, '') s'il n'y en a pas."""
    entree = donnees.get("tool_input") or {}
    brut = entree.get("file_path") or entree.get("notebook_path") or ""
    if not brut:
        return "", True, ""
    if not isinstance(brut, str):
        raise EntreeInutilisable("file_path n'est pas du texte")
    racine = racine_du_projet(donnees)
    brut = os.path.expanduser(brut.strip())
    if not os.path.isabs(brut):
        base = donnees.get("cwd") if isinstance(donnees.get("cwd"), str) else racine
        brut = os.path.join(base, brut)
    reel = os.path.realpath(brut)
    if reel == racine:
        return "", True, reel
    if reel.startswith(racine + os.sep):
        return reel[len(racine) + 1:].replace(os.sep, "/"), True, reel
    return reel, False, reel


def est_regle(chemin):
    c = chemin.casefold()
    return (c in FICHIERS_DE_REGLES or c.startswith(DOSSIERS_DE_REGLES)
            or any(c.startswith(p) for p in PREFIXES_DE_REGLES))


def est_secret(chemin):
    nom = os.path.basename(chemin).casefold()
    if nom in EXCEPTIONS_DE_SECRETS:
        return False
    return any(fnmatch.fnmatch(nom, m) for m in MOTIFS_DE_SECRETS) or "/secrets/" in "/" + chemin.casefold()


def decision(genre, raison):
    """Rend la décision à Claude Code : deny (bloqué) ou ask (demander à James)."""
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": genre,
                                             "permissionDecisionReason": raison}}, ensure_ascii=False))
    sys.exit(0)


def executer(corps):
    try:
        corps()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 — un garde-fou en erreur refuse
        print(f"Garde-fou en erreur ({type(e).__name__}: {e}) : refus par prudence.", file=sys.stderr)
        sys.exit(2)
