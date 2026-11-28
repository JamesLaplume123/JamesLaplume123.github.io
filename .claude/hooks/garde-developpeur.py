#!/usr/bin/env python3
"""Garde-fou de l'agent développeur : il bâtit le site, mais ne touche ni à la documentation, ni aux
règles, ni aux secrets, et n'écrit rien hors du projet."""

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
    if not dans_le_projet:
        decision("deny", f"Bloqué : {reel} est hors du projet. Le développeur n'écrit que dans le site.")
    if est_secret(chemin):
        decision("deny", f"Bloqué : {chemin} est un fichier secret.")
    if chemin.casefold().startswith("docs/") or est_regle(chemin):
        decision("deny", f"Bloqué : {chemin} fait partie de la documentation ou des règles. "
                         "Le chef s'en occupe, avec l'accord de James.")


executer(corps)
