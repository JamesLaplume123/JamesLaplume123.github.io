#!/usr/bin/env python3
"""Garde-fou global, pour tous (outils Edit, Write, MultiEdit, NotebookEdit).

- Bloque toute écriture d'un secret.
- Demande l'accord de James avant de modifier un fichier de règles ou d'écrire hors du projet.
"""

import os
import sys

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from regles import chemin_vise, decision, est_regle, est_secret, executer, lire_entree  # noqa: E402
except Exception as e:  # noqa: BLE001 — un garde-fou sans ses règles refuse tout
    print(f"Garde-fou en panne ({type(e).__name__}: {e}) : refus par prudence.", file=sys.stderr)
    sys.exit(2)


def corps():
    chemin, dans_le_projet, reel = chemin_vise(lire_entree())
    if not reel:
        return
    if est_secret(chemin):
        decision("deny", f"Bloqué : {chemin} est un fichier secret. Les secrets ne passent jamais par un agent.")
    if not dans_le_projet:
        decision("ask", f"Écriture hors du projet ({reel}). James doit approuver.")
    if est_regle(chemin):
        decision("ask", f"{chemin} est un fichier de règles du site. James doit approuver ce changement.")


executer(corps)
