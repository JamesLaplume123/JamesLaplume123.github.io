#!/usr/bin/env python3
"""Générateur du site jameslaplume.ca.

Usage :  python3 tools/build.py

Lit les pages de src/pages/, les enveloppe avec les gabarits de src/partials.py
et écrit le HTML final à la racine du dépôt (servie par GitHub Pages).
Produit aussi sitemap.xml et les redirections des anciennes URL.
Aucune dépendance extérieure : Python 3 standard seulement.
"""

import importlib
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from config import SITE, REDIRECTS  # noqa: E402
from partials import document, redirect_document  # noqa: E402

# Ordre de référence des pages (sert aussi au sitemap).
PAGE_MODULES = [
    "accueil",
    "solutions",
    "solution_environnements_intelligents",
    "solution_ia_privee_connaissances",
    "solution_securite_intelligente",
    "solution_automatisation_operations",
    "solution_reseau_resilience",
    "solution_diagnostic_care",
    "plateforme",
    "laboratoire_mobile",
    "vision_roadmap",
    "recherche",
    "confiance",
    "a_propos",
    "contact",
    "merci",
    "confidentialite",
    "english",
    "page_404",
]


def out_path(url):
    """'/solutions/' → solutions/index.html ; '/404.html' → 404.html"""
    if url.endswith(".html"):
        return ROOT / url.lstrip("/")
    return ROOT / url.strip("/") / "index.html" if url != "/" else ROOT / "index.html"


def build():
    written = []
    pages = []
    for name in PAGE_MODULES:
        try:
            mod = importlib.import_module(f"pages.{name}")
        except ModuleNotFoundError:
            print(f"  (page absente, ignorée : {name})")
            continue
        page = mod.PAGE
        path = out_path(page["url"])
        path.parent.mkdir(parents=True, exist_ok=True)
        # Décodage asynchrone des images : évite de bloquer le rendu.
        html = document(page).replace("<img src", '<img decoding="async" src')
        path.write_text(html, encoding="utf-8")
        written.append(path.relative_to(ROOT))
        pages.append(page)

    # Redirections des anciennes URL.
    for old, target in REDIRECTS.items():
        path = ROOT / old
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(redirect_document(target), encoding="utf-8")
        written.append(Path(old))

    # Sitemap (pages indexables seulement).
    today = date.today().isoformat()
    entries = "".join(
        f"  <url><loc>{SITE['domain']}{p['url']}</loc><lastmod>{today}</lastmod></url>\n"
        for p in pages
        if not p.get("noindex") and not p["url"].endswith(".html")
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n",
        encoding="utf-8",
    )
    written.append(Path("sitemap.xml"))

    print(f"{len(written)} fichiers générés :")
    for w in written:
        print(f"  {w}")


if __name__ == "__main__":
    build()
