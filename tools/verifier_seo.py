#!/usr/bin/env python3
"""Vérification du référencement après le build.

Usage :  python3 tools/verifier_seo.py     (code de sortie 1 s'il y a une erreur)

Pour chaque page du sitemap : un seul <h1>, un <title> et une description uniques et de
longueur raisonnable, une adresse canonique sur le bon domaine, des données structurées
lisibles, aucune image sans attribut alt, aucun identifiant en double, aucun lien interne
cassé. Vérifie aussi que le sitemap n'expose aucune page privée et que robots.txt le cite, et
qu'aucun ancien nom (« Hub ») ne revient dans ce qu'un visiteur peut lire (docs/OFFRE.md).
Aucune dépendance extérieure.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from config import SITE  # noqa: E402

D = SITE["domain"]
TITRE = (25, 65)
DESC = (90, 170)
PRIVE = ("/admin/", "/labo-cartes/", "/merci/")
# Anciens noms retirés du site (19 novembre 2026) : l'appareil s'appelle JARVIS Mini, JARVIS ou JARVIS Pro.
ANCIENS = re.compile(r"(?<![-/#._\w])hubs?(?![-/_\w]|\"\s*:)", re.I)
LISIBLE = re.compile(r'(?:alt|title|aria-label|content|placeholder|data-toast|data-toc)="([^"]*)"')


def ancien_nom(h):
    """Le premier ancien nom qu'un visiteur pourrait lire dans la page (texte, attributs lisibles,
    données JSON), ou None. Les clés, les identifiants et les chemins internes ne comptent pas."""
    h = re.sub(r"<style\b.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<script(?![^>]*application/(?:ld\+)?json)[^>]*>.*?</script>", " ", h, flags=re.S)
    texte = re.sub(r"<[^>]+>", " ", h) + " " + " ".join(LISIBLE.findall(h))
    for m in ANCIENS.finditer(texte):
        autour = texte[max(0, m.start() - 3): m.end() + 4].lower()
        if "github" in autour or "hublot" in autour:
            continue
        if m.group(0) == "hub" and texte[m.start() - 1: m.start()] == '"' and texte[m.end(): m.end() + 1] == '"':
            continue   # identifiant interne dans des données ("hub"), jamais affiché
        return " ".join(texte[max(0, m.start() - 30): m.end() + 30].split())
    return None


def fichier(url):
    url = url.split("#")[0].split("?")[0]
    if url.endswith("/"):
        return ROOT / url.strip("/") / "index.html" if url != "/" else ROOT / "index.html"
    return ROOT / url.lstrip("/")


def main():
    err, avert = [], []
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    urls = [u[len(D):] for u in re.findall(r"<loc>([^<]+)</loc>", sitemap)]
    for u in urls:
        if u.startswith(PRIVE):
            err.append(f"sitemap : page privée exposée {u}")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {D}/sitemap.xml" not in robots:
        err.append("robots.txt : ligne Sitemap absente ou sur un autre domaine")

    titres, descs = defaultdict(list), defaultdict(list)
    for u in urls:
        f = fichier(u)
        if not f.exists():
            err.append(f"{u} : fichier absent")
            continue
        h = f.read_text(encoding="utf-8")
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        t = t.group(1).strip() if t else ""
        d = d.group(1).strip() if d else ""
        titres[t].append(u)
        descs[d].append(u)
        vieux = ancien_nom(h)
        if vieux:
            err.append(f"{u} : ancien nom visible « {vieux} »")
        if not TITRE[0] <= len(t) <= TITRE[1]:
            avert.append(f"{u} : titre de {len(t)} caractères")
        if not DESC[0] <= len(d) <= DESC[1]:
            avert.append(f"{u} : description de {len(d)} caractères")
        n = len(re.findall(r"<h1[\s>]", h))
        if n != 1:
            err.append(f"{u} : {n} balises h1")
        if f'<link rel="canonical" href="{D}{u}">' not in h:
            err.append(f"{u} : adresse canonique absente ou incorrecte")
        if 'name="robots" content="noindex' in h:
            err.append(f"{u} : page du sitemap marquée noindex")
        for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                json.loads(bloc)
            except ValueError as e:
                err.append(f"{u} : données structurées illisibles ({e})")
        if u != "/" and "BreadcrumbList" not in h and not u.startswith("/en/"):
            err.append(f"{u} : fil d’Ariane (BreadcrumbList) absent")
        for img in re.findall(r"<img\b[^>]*>", h):
            if " alt=" not in img:
                err.append(f"{u} : image sans attribut alt ({img[:70]})")
        ids = re.findall(r'\sid="([^"]+)"', re.sub(r"<script\b.*?</script>", "", h, flags=re.S))
        for i in sorted({i for i in ids if ids.count(i) > 1}):
            err.append(f"{u} : identifiant en double #{i}")
        niveaux = [int(x) for x in re.findall(r"<h([1-6])[\s>]", h.split("<main", 1)[-1].split("</main>")[0])]
        if niveaux and niveaux[0] != 1:
            avert.append(f"{u} : le premier titre du contenu n’est pas un h1")
        for lien in set(re.findall(r'href="(/[^"#?]*)', h)):
            if lien.startswith("//"):
                continue
            cible = fichier(lien)
            if not cible.exists():
                err.append(f"{u} : lien interne cassé {lien}")
        for ancre in set(re.findall(r'href="(/[^"?]*#[^"]+)"', h)):
            chemin, _, frag = ancre.partition("#")
            cible = fichier(chemin)
            if cible.exists() and not re.search(rf'\sid="{re.escape(frag)}"', cible.read_text(encoding="utf-8")):
                avert.append(f"{u} : ancre introuvable {ancre}")

    for t, us in titres.items():
        if len(us) > 1:
            err.append(f"titre en double « {t} » : {', '.join(us)}")
    for d, us in descs.items():
        if len(us) > 1:
            err.append(f"description en double : {', '.join(us)}")

    print(f"{len(urls)} pages vérifiées.")
    for a in avert:
        print("  avertissement :", a)
    for e in err:
        print("  ERREUR :", e)
    print("Référencement : " + ("ÉCHEC" if err else "tout est correct") + f" ({len(err)} erreurs, {len(avert)} avertissements)")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
