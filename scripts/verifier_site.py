#!/usr/bin/env python3
"""Vérifie que le site bâti respecte la loi du site (docs/SITE.md) et son plan (docs/plan_du_site.json).

Refuse (code 1) :
  - une page bâtie qui n'est pas dans le plan ;
  - une page du plan absente (sauf statut « a_creer ») ;
  - une redirection qui ne redirige pas, ou une page privée indexable ;
  - un lien du menu ou du pied de page vers une page hors du plan ;
  - une page du plan qu'aucune autre page ne relie ;
  - sur une page « fait », un texte qui dépasse le budget de la loi (section 4).
Lancé par scripts/check.sh. La version anglaise (/en/) sera vérifiée à son étape.
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PLAN = json.loads((RACINE / "docs" / "plan_du_site.json").read_text(encoding="utf-8"))
HORS_SITE = {".git", ".claude", ".githooks", ".github", "assets", "media", "integrations", "node_modules",
             "docs", "tools", "scripts", "src", "data", "en", "tmp", "__pycache__"}
VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

BUDGET = {"h1": 14, "h2": 10, "phrase": 20, "paragraphe": 40, "tuile": 15, "rangee": 20}
EXCLUS = re.compile(r"\b(ap-notes|coquille|demo-shell|sol-demo|fil|faq)\b")  # notes, démos, fil d'Ariane, questions

erreurs, avertissements = [], []


def pages_baties():
    trouvees = {}
    for f in RACINE.rglob("index.html"):
        rel = f.relative_to(RACINE)
        if rel.parts[0] in HORS_SITE:
            continue
        url = "/" + "/".join(rel.parts[:-1]) + ("/" if len(rel.parts) > 1 else "")
        trouvees[url] = f
    for f in RACINE.glob("*.html"):
        if f.name != "index.html":
            trouvees["/" + f.name] = f
    return trouvees


def mots(texte):
    return len(re.findall(r"[\w’'-]+", texte))


class Lecteur(HTMLParser):
    """Recueille les liens, et les textes soumis au budget (hors nav, pied, notes et démos)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pile = []          # (balise, exclu)
        self.liens = []
        self.zone = []          # « nav » ou « footer » en cours
        self.liens_zone = {"nav": [], "footer": []}
        self.textes = []        # (genre, texte)
        self.courant = None     # [genre, morceaux, profondeur]

    def _exclu(self):
        return any(e for _, e in self.pile)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        exclu = tag in ("nav", "footer", "header", "script", "style", "noscript") or bool(EXCLUS.search(cls)) \
            or "data-demo" in a
        if tag == "a" and a.get("href"):
            self.liens.append(a["href"])
            for z in self.zone:
                self.liens_zone[z].append(a["href"])
        if tag in VIDES:
            return
        if tag in ("nav", "footer"):
            self.zone.append(tag)
        self.pile.append((tag, exclu))
        if self.courant is None and not self._exclu():
            genre = None
            if tag in ("h1", "h2"):
                genre = tag
            elif tag == "p":
                genre = "paragraphe"
            elif re.search(r"\bap-tuile\b", cls):
                genre = "tuile"
            elif re.search(r"\bap-tr\b", cls) and "ap-th" not in cls:
                genre = "rangee"
            if genre:
                self.courant = [genre, [], len(self.pile)]

    def handle_endtag(self, tag):
        if tag in VIDES:
            return
        while self.pile:
            t, _ = self.pile.pop()
            if t in ("nav", "footer") and self.zone:
                self.zone.pop()
            if self.courant and len(self.pile) < self.courant[2]:
                genre, morceaux, _ = self.courant
                texte = " ".join("".join(morceaux).split())
                if texte:
                    self.textes.append((genre, texte))
                self.courant = None
            if t == tag:
                break

    def handle_data(self, data):
        if self.courant is not None:
            self.courant[1].append(data)


def lire(f):
    lecteur = Lecteur()
    lecteur.feed(f.read_text(encoding="utf-8", errors="replace"))
    return lecteur


def chemin(href):
    if not href.startswith("/") or href.startswith("//"):
        return None
    return href.split("#")[0].split("?")[0] or "/"


def main():
    baties = pages_baties()
    plan = {p["url"]: p for p in PLAN["pages"]}
    connues = set(plan) | set(PLAN["utilitaires"]) | set(PLAN["prives"]) | set(PLAN["redirections"])

    # 1. Rien hors du plan, rien de manquant.
    for url in sorted(baties):
        if url not in connues:
            erreurs.append(f"Page hors du plan : {url}. Ajoute-la à docs/plan_du_site.json (accord de James) "
                           "ou retire-la en gardant son adresse par une redirection.")
    for url, p in plan.items():
        if url not in baties and p["statut"] != "a_creer":
            erreurs.append(f"Page du plan absente : {url} ({p['nom']}).")
        if url in baties and p["statut"] == "a_creer":
            avertissements.append(f"{url} existe : passe son statut de « a_creer » à « a_refaire » ou « fait ».")
    for url in PLAN["utilitaires"]:
        if url not in baties:
            erreurs.append(f"Page utilitaire absente : {url}.")

    # 2. Redirections et pages privées.
    for url in PLAN["redirections"]:
        if url in baties:
            t = baties[url].read_text(encoding="utf-8", errors="replace")
            if 'http-equiv="refresh"' not in t:
                erreurs.append(f"{url} devait être une redirection : elle ne redirige pas.")
    for url in PLAN["prives"]:
        if url in baties:
            t = baties[url].read_text(encoding="utf-8", errors="replace")
            if not re.search(r'<meta name="robots" content="[^"]*noindex', t):
                erreurs.append(f"Page privée indexable par Google : {url}. Ajoute noindex.")

    # 3. Menu et pied de page : seulement des pages du plan.
    permis = set(plan) | set(PLAN["utilitaires"])
    accueil = lire(baties["/"]) if "/" in baties else None
    if accueil:
        for zone, liens in accueil.liens_zone.items():
            for href in liens:
                c = chemin(href)
                if c and c not in permis and not c.startswith(("/assets/", "/media/", "/en/")):
                    erreurs.append(f"Le {'menu' if zone == 'nav' else 'pied de page'} mène hors du plan : {href}.")

    # 4. Chaque page du plan est reliée par au moins une autre page.
    lecteurs = {url: lire(f) for url, f in baties.items() if url in permis}
    for url, p in plan.items():
        if url not in baties or url == "/":
            continue
        if not any(url in {chemin(h) for h in l.liens} for u, l in lecteurs.items() if u != url):
            erreurs.append(f"Aucune page ne mène à {url} ({p['nom']}).")

    # 5. Le budget de texte, sur les pages faites.
    for url, p in plan.items():
        if p["statut"] != "fait" or url not in lecteurs:
            continue
        for genre, texte in lecteurs[url].textes:
            n = mots(texte)
            if genre in ("h1", "h2", "tuile", "rangee") and n > BUDGET[genre]:
                erreurs.append(f"{url} : {genre} de {n} mots (maximum {BUDGET[genre]}) : « {texte[:70]}… »")
            if genre == "paragraphe":
                if n > BUDGET["paragraphe"]:
                    erreurs.append(f"{url} : paragraphe de {n} mots (maximum {BUDGET['paragraphe']}) : « {texte[:70]}… »")
                for phrase in re.split(r"(?<=[.!?])\s+", texte):
                    if mots(phrase) > BUDGET["phrase"]:
                        erreurs.append(f"{url} : phrase de {mots(phrase)} mots (maximum {BUDGET['phrase']}) : "
                                       f"« {phrase[:70]}… »")

    statuts = {}
    for p in plan.values():
        statuts[p["statut"]] = statuts.get(p["statut"], 0) + 1
    print(f"Plan : {len(plan)} pages · {statuts.get('fait', 0)} faites · {statuts.get('a_refaire', 0)} à refaire · "
          f"{statuts.get('a_creer', 0)} à créer")
    for a in avertissements:
        print("  avertissement :", a)
    for e in erreurs:
        print("  ERREUR :", e)
    if erreurs:
        print(f"Loi du site : {len(erreurs)} erreur(s).")
        return 1
    print("Loi du site : tout est conforme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
