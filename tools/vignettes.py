#!/usr/bin/env python3
"""Vignettes du forfait (tiroir « Mon forfait ») : petites images carrées, légères.

Pour chaque lieu, chaque solution et chaque Hub, prend la photo dédiée si elle existe
(media/forfait/lieu-<id>.webp, media/forfait/sol-<clé>.webp, media/hubs/hub-<id>.webp),
sinon la photo de repli, et écrit media/forfait/v-<nom>.webp (240 px). À relancer quand une
photo change : python3 tools/vignettes.py
"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import lieux  # noqa: E402


def vignette(src, dest, taille=240):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    c = min(w, h)
    im = im.crop(((w - c) // 2, (h - c) // 2, (w - c) // 2 + c, (h - c) // 2 + c)).resize((taille, taille), Image.LANCZOS)
    im.save(dest, "WEBP", quality=78, method=6)


def main():
    n = 0
    for nom, source in lieux.sources_vignettes():
        src = ROOT / source.lstrip("/")
        if not src.exists():
            print("  photo absente :", source)
            continue
        vignette(src, ROOT / "media" / "forfait" / f"v-{nom}.webp")
        n += 1
    print(n, "vignettes")


if __name__ == "__main__":
    main()
