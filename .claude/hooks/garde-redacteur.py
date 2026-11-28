#!/usr/bin/env python3
"""Garde-fou de l'agent rédacteur : il écrit seulement les textes, dans src/ (pages, divisions,
configuration des textes, articles). Le style, les scripts, la documentation et les règles lui sont
fermés."""

import os
import sys

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from regles import chemin_vise, decision, est_regle, est_secret, executer, lire_entree  # noqa: E402
except Exception as e:  # noqa: BLE001
    print(f"Garde-fou en panne ({type(e).__name__}: {e}) : refus par prudence.", file=sys.stderr)
    sys.exit(2)


def corps():
    chemin, dans_le_projet, reel = chemin_vise(lire_entree())
    if not reel:
        return
    if not dans_le_projet or est_secret(chemin) or est_regle(chemin):
        decision("deny", f"Bloqué : {chemin} n'est pas un fichier de textes. Le rédacteur écrit seulement dans src/.")
    if not chemin.casefold().startswith("src/") or not chemin.endswith((".py", ".md")):
        decision("deny", f"Bloqué : {chemin} n'est pas un fichier de textes du site (src/*.py ou src/*.md). "
                         "Le style et les gabarits vont au développeur.")


executer(corps)
