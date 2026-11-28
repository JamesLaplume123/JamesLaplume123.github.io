#!/usr/bin/env python3
"""Captures de tout le site, pour le réviseur et pour James (étape 8 du chemin de chaque demande).

Chaque page du plan (docs/plan_du_site.json) est photographiée en entier, à l'ordinateur et au
téléphone, puis réunie sur une planche par page. Rien n'est écrit dans le projet.

    python3 scripts/captures.py                  # tout le site
    python3 scripts/captures.py / /solutions/    # seulement ces pages
Sortie : /tmp/captures-site/ (ou --sortie DOSSIER).
"""

import argparse
import asyncio
import http.server
import json
import socketserver
import threading
from functools import partial
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PLAN = json.loads((RACINE / "docs" / "plan_du_site.json").read_text(encoding="utf-8"))
TAILLES = {"ordinateur": (1440, 900), "telephone": (390, 844)}


class Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serveur():
    srv = socketserver.TCPServer(("127.0.0.1", 0), partial(Silencieux, directory=str(RACINE)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


async def photographier(urls, sortie, port):
    from playwright.async_api import async_playwright
    from PIL import Image

    erreurs = {}
    async with async_playwright() as p:
        navigateur = await p.chromium.launch()
        for genre, (w, h) in TAILLES.items():
            page = await navigateur.new_page(viewport={"width": w, "height": h})
            await page.add_init_script("try{localStorage.setItem('jv-teaser-vu','1')}catch(e){}")
            await page.route("**/*workers.dev/**", lambda r: r.abort())
            page.on("pageerror", lambda e, g=genre: erreurs.setdefault(page.url, []).append(str(e)[:120]))
            for url in urls:
                await page.goto(f"http://127.0.0.1:{port}{url}", wait_until="load")
                await page.add_style_tag(content="[data-rev]{opacity:1!important;transform:none!important}"
                                                 ".jv-teaser{display:none!important}")
                hauteur = await page.evaluate("document.body.scrollHeight")
                for y in range(0, hauteur, 700):
                    await page.evaluate(f"window.scrollTo(0,{y})")
                    await page.wait_for_timeout(40)
                await page.evaluate("window.scrollTo(0,0)")
                await page.wait_for_timeout(300)
                deborde = await page.evaluate("document.documentElement.scrollWidth > innerWidth")
                if deborde:
                    erreurs.setdefault(url, []).append(f"déborde à l'horizontale ({genre})")
                nom = (url.strip("/").replace("/", "_") or "accueil").replace(".html", "")
                fichier = sortie / f"{nom}-{genre}.jpg"
                await page.screenshot(path=str(fichier), full_page=True, type="jpeg", quality=60)
            await page.close()
        await navigateur.close()

    # Une planche par page : l'ordinateur à gauche, le téléphone à droite, réduits.
    for url in urls:
        nom = (url.strip("/").replace("/", "_") or "accueil").replace(".html", "")
        a, b = Image.open(sortie / f"{nom}-ordinateur.jpg"), Image.open(sortie / f"{nom}-telephone.jpg")
        a = a.resize((720, int(a.height * 720 / a.width)))
        b = b.resize((260, int(b.height * 260 / b.width)))
        planche = Image.new("RGB", (720 + 40 + 260, max(a.height, b.height)), (24, 24, 24))
        planche.paste(a, (0, 0))
        planche.paste(b, (760, 0))
        planche.save(sortie / f"planche-{nom}.jpg", quality=62)
    return erreurs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--sortie", default="/tmp/captures-site")
    args = ap.parse_args()
    urls = args.urls or [p["url"] for p in PLAN["pages"] if p["statut"] != "a_creer"]
    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    srv, port = serveur()
    try:
        erreurs = asyncio.run(photographier(urls, sortie, port))
    finally:
        srv.shutdown()
    print(f"{len(urls)} pages photographiées dans {sortie} (planche-*.jpg pour James).")
    for url, liste in erreurs.items():
        for e in liste:
            print(f"  à regarder : {url} : {e}")


if __name__ == "__main__":
    main()
