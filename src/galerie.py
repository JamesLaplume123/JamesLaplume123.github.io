# Galeries photo du site : grandes images premium (cadre en cristal doré, cartes noires).
#
# Chaque emplacement prend automatiquement media/vitrine/<dossier>/<nom>.webp s'il existe au
# moment du build (déposer le fichier puis reconstruire, aucun changement de code). Sinon, il
# affiche un panneau noir sobre « Photo à venir » — jamais un dessin. Même mécanique que
# photo_ou_attente des démos. Les photos ne sont jamais recolorées : superpositions seulement.
#
# Une forme reste en usage : avant_apres(), deux images 3:2 côte à côte (laboratoire mobile).

import os
from html import escape

_RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Registre des emplacements (rempli au build) : fichier, page, texte de remplacement, format.
PHOTOS = []

FORMATS = {
    "vedette": "4:3 · 2400 × 1800",
    "carte": "4:3 · 1600 × 1200",
    "panorama": "21:9 · 2560 × 1100",
    "paire": "3:2 · 1800 × 1200",
}


def _src(cle, page, alt, forme):
    """Chemin public de la photo si le fichier existe, sinon None. Note l'emplacement au registre."""
    fichier = "media/vitrine/" + cle + ".webp"
    if not any(p["fichier"] == fichier for p in PHOTOS):
        PHOTOS.append({"fichier": fichier, "page": page, "alt": alt, "format": FORMATS[forme]})
    if os.path.exists(os.path.join(_RACINE, fichier)):
        return "/" + fichier
    return None


def _visuel(cle, page, alt, forme, pos="50% 50%", attente="Photo à venir", eager=False):
    src = _src(cle, page, alt, forme)
    if src:
        lazy = "" if eager else ' loading="lazy"'
        return f'<img src="{src}" alt="{escape(alt)}"{lazy} style="object-position:{pos}">', False
    return (
        f'<div class="gl-ph" role="img" aria-label="{escape(alt)}">'
        f'<span class="gl-ph-f" aria-hidden="true"></span>'
        f'<span class="gl-ph-n">{attente}</span></div>'
    ), True


def _figure(c, page, forme, classes="", attente="Photo à venir"):
    vis, ph = _visuel(c["f"], page, c["alt"], forme, c.get("pos", "50% 50%"), attente)
    cls = " ".join(x for x in ("gl-fig", classes, "is-ph" if ph else "") if x)
    cap = ""
    k, t = _typo(c.get("k", "")), _typo(c.get("t", ""))
    if k or t:
        cap = "<figcaption>" + (f"<span>{k}</span>" if k else "") + (f"<b>{t}</b>" if t else "") + "</figcaption>"
    badge = f'<i class="gl-badge{" is-on" if c.get("on") else ""}">{c["badge"]}</i>' if c.get("badge") else ""
    return f'<figure class="{cls}" data-rev>{vis}{badge}{cap}</figure>'


def _typo(s):
    """Apostrophe typographique dans les textes visibles."""
    return s.replace("'", "’")


def _tete(eyebrow, titre, intro):
    return f"""<div class="sect-head">
    <div data-rev>
      <p class="eyebrow">{eyebrow}</p>
      <h2 style="margin-top:1rem">{titre}</h2>
    </div>
    <p data-rev>{intro}</p>
  </div>"""


def avant_apres(page, avant, apres, eyebrow, titre, intro, ident="", toc="", alt=False, attente="Photo à venir",
                libelles=("Avant", "Avec JARVIS")):
    """Deux grandes images côte à côte : la situation d'aujourd'hui, puis la même avec JARVIS."""
    # La pastille dit déjà « Avant » / « Avec JARVIS » : la légende garde seulement la phrase.
    a = dict(avant, badge=libelles[0], k="")
    b = dict(apres, badge=libelles[1], on=True, k="")
    id_attr = f' id="{ident}"' if ident else ""
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""
<section class="sect gl-sect{' alt' if alt else ''}"{id_attr}{toc_attr}>
  {_tete(eyebrow, titre, intro)}
  <div class="gl-va">{_figure(a, page, "paire", "", attente)}<span class="gl-va-arrow" aria-hidden="true"></span>{_figure(b, page, "paire", "", attente)}</div>
</section>"""


def laboratoire_visuels():
    return avant_apres(
        "/laboratoire-mobile/",
        {"f": "laboratoire/ambulance-avant", "alt": "Intérieur médical d'origine d'une ambulance Ford : civière, armoires blanches, éclairage froid",
         "k": "À l’achat", "t": "Une ambulance retirée du service"},
        {"f": "laboratoire/ambulance-apres", "alt": "Le même intérieur transformé : banquette, cuisinette en bois sombre, éclairage doré indirect",
         "k": "Aujourd’hui", "t": "Habitation, atelier et banc d’essai"},
        "Avant · après", "La même ambulance.<br><em>Une autre vie.</em>",
        "", ident="transformation", libelles=("Avant", "Après"))
