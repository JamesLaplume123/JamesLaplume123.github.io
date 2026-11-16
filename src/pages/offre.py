# L'offre — comprendre avant de choisir (décision de James, novembre 2026).
#   1. ce qu'est le Hub, en une phrase et une image;
#   2. comment ça se compose : un Hub par lieu → vos solutions → le matériel du lieu;
#   3. lequel choisir : trois cartes en mots de tous les jours (src/lieux.py, HUBS_CHOIX), le mini-guide
#      « Vous hésitez? » et le comparatif détaillé du catalogue (C.COMPARE), replié;
#   4. trois exemples complets : quel Hub, quelles solutions, pourquoi;
#   5. le prochain pas : composer son forfait.
# Aucun montant tant que SITE["prix_publics"] est False (src/pro.py). Les prix viennent toujours du
# catalogue (src/pages/catalogue.py, source unique). Styles : assets/demos/offre.css.

import json
import os
from html import escape

from config import CAPABILITIES
from pages import catalogue as CAT
import lieux
import pro

_RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
_TITRE = {c["slug"]: c["title"] for c in CAPABILITIES}

def _p(n):
    return f"{n:,}".replace(",", " ") + " $"


def _photo_hub(hid):
    """La photo du boîtier, si elle existe : media/offre/hub-<id>.webp. Sinon rien (jamais un dessin)."""
    chemin = f"/media/offre/hub-{hid}.webp"
    if os.path.exists(os.path.join(_RACINE, chemin.lstrip("/"))):
        return f'<img class="of-h-ph" src="{chemin}" alt="" loading="lazy" decoding="async">'
    return ""


def hubs():
    """Lequel choisir : trois cartes qui répondent à « est-ce pour moi? » (src/lieux.py, HUBS_CHOIX), le
    mini-guide « Vous hésitez? », la phrase en deux temps. Sert à /offre/ et à l'accueil.
    Le prix n'apparaît que si les prix sont publics."""
    tuiles = []
    for h in CAT.HUBS:
        c = lieux.HUBS_CHOIX[h["id"]]
        tag = f'<span class="of-h-tag">{escape(h["tag"])}</span>' if h["tag"] else ""
        moi = c.get("peut_moi", {})
        peut = "".join(
            (f'<li data-public="entreprise">{x}</li><li data-public="particulier">{moi[i]}</li>' if i in moi else f"<li>{x}</li>")
            for i, x in enumerate(c["peut"])
        )
        pour = (f'<span data-public="entreprise">{c["pour"]}</span><span data-public="particulier">{c["pour_moi"]}</span>'
                if c.get("pour_moi") else c["pour"])
        prix = f'<p class="of-h-prix">{_p(h["prix"])}<small>une fois</small></p>' if pro.PRIX else ""
        tuiles.append(f"""<article class="of-h" data-hub="{h['id']}" data-rev>
      {tag}{_photo_hub(h['id'])}<p class="of-h-k">{escape(h['nom'])}</p>
      <h3>{c['situation']}</h3>
      <p class="of-h-pour">{pour}</p>{prix}
      <p class="of-h-pr">{c['promesse']}</p>
      <p class="of-h-v">Vous pouvez</p>
      <ul class="of-h-d">{peut}</ul>
      <p class="of-h-s"><span>À savoir</span> {c['savoir']}</p>
    </article>""")
    questions = "".join(
        f'<div class="of-q" data-q="{k}"><p>{q}</p><div>'
        + "".join(f'<button type="button" data-r="{v}" aria-pressed="false">{lab}</button>' for v, lab in reps)
        + "</div></div>"
        for k, q, reps in lieux.HESITE
    )
    raisons = json.dumps(lieux.HESITE_RAISON, ensure_ascii=False)
    return f"""<div class="of-choix" data-of-choix>
  <div class="of-hs">{"".join(tuiles)}</div>
  <div class="of-hes" data-rev>
    <p class="of-hes-t">Vous hésitez?</p>
    <div class="of-qs">{questions}</div>
    <p class="of-hes-r" data-of-raison hidden aria-live="polite"></p>
    <script type="application/json" data-of-raisons>{raisons}</script>
  </div>
  <p class="of-deux" data-rev>Le Hub s’achète une fois. Les solutions se prennent au mois, et s’annulent quand vous voulez.</p>
  {"" if pro.PRIX else '<p class="of-soum" data-rev>Prix sur soumission, confirmé par écrit.</p>'}
</div>"""


def comparatif():
    """Le comparatif détaillé reste disponible, replié."""
    tete = "".join(f"<th>{escape(h['nom'])}</th>" for h in CAT.HUBS)
    lignes = "".join(
        f"<tr><th>{escape(r[0])}</th>" + "".join(f"<td>{escape(x)}</td>" for x in r[1:]) + "</tr>" for r in CAT.COMPARE
    )
    return (f'<details class="of-cmp" data-rev><summary>Comparer en détail</summary>'
            f'<div class="of-cmp-w"><table><thead><tr><th></th>{tete}</tr></thead><tbody>{lignes}</tbody></table></div></details>')


ETAPES = [
    ("1", "Un Hub par lieu", "Le petit ordinateur installé chez vous. Il fait tourner JARVIS, même sans Internet.",
     "/media/product/jarvis-hub-v1.webp", "62% 55%"),
    ("2", "Les solutions que vous voulez", "Comme des apps : vous prenez seulement ce qui vous sert, et vous annulez quand vous voulez.",
     "/media/accueil/sol-environnements.webp", "32% 50%"),
    ("3", "Le matériel du lieu", "Capteurs, caméras, serrures. Ce que vous avez déjà est réutilisé.",
     "/media/vitrine/plateforme/hub-armoire-technique.webp", "50% 50%"),
]

# Trois exemples complets : (titre, photo, Hub, solutions, pourquoi)
EXEMPLES = [
    ("Un chalet", "/media/vitrine/plateforme/chalet-hiver.webp", "Hub Base",
     ["diagnostic-care", "securite-intelligente"],
     "Fermé une partie de l’année : il vous prévient du gel, d’une fuite ou d’une porte ouverte."),
    ("Une maison et un VR", "/media/offre/vr.webp", "Hub Signature à la maison, Hub Base et Boîtier VR à bord",
     ["environnements-intelligents", "securite-intelligente", "mobilite"],
     "Deux lieux, une seule application : la maison se règle seule pendant que vous roulez."),
    ("Une ferme", "/media/offre/ferme.webp", "Hub Platinum",
     ["diagnostic-care", "reseau-resilience", "environnements-intelligents"],
     "Des bâtiments qui ne peuvent pas attendre : batterie et Internet de secours, alertes jour et nuit."),
]


def _etapes():
    return "".join(
        f"""<article class="of-e" data-rev>
      <img src="{img}" alt="" style="object-position:{pos}">
      <div><i>{n}</i><h3>{t}</h3><p>{p}</p></div>
    </article>"""
        for n, t, p, img, pos in ETAPES
    )


def _exemples():
    return "".join(
        f"""<article class="of-ex"{' data-public="entreprise"' if t == "Une ferme" else ''} data-rev>
      <img src="{img}" alt="">
      <div>
        <h3>{t}</h3>
        <p class="of-ex-h">{hub}</p>
        <p class="of-ex-s">{" · ".join(_TITRE[s] for s in sols)}</p>
        <p>{pourquoi}</p>
      </div>
    </article>"""
        for t, img, hub, sols, pourquoi in EXEMPLES
    )


PAGE = {
    "url": "/offre/",
    "v2": True,
    "title": "L’offre JARVIS | Un Hub, vos solutions, le matériel de votre lieu",
    "description": (
        "Le Hub est le petit ordinateur que nous installons chez vous. Un Hub par lieu, les solutions "
        "que vous voulez, le matériel du lieu. Voyez lequel choisir."
    ),
    "og_image": "/media/offre/maison.webp",
    "assets": ["offre"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/product/jarvis-hub-v1.webp" alt="Le boîtier JARVIS Hub posé sur un meuble, dans un salon" fetchpriority="high"></div>
  <div class="band-inner">
    <h1 data-rev>Un Hub. Vos solutions.<br><em>Rien de plus.</em></h1>
    <p class="lead" data-rev>Le Hub est le petit ordinateur que nous installons chez vous. JARVIS vit dedans; vos données y restent.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/catalogue/">Composer mon forfait</a>
    </div>
  </div>
</section>

<section class="sect" id="comment" aria-labelledby="comment-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Comment ça se compose</p>
      <h2 id="comment-titre">Trois étapes.</h2>
    </div>
  </div>
  <div class="of-es">{_etapes()}</div>
</section>

<section class="sect alt" id="hub" aria-labelledby="hub-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Lequel choisir</p>
      <h2 id="hub-titre">Lequel est<br><em>pour vous?</em></h2>
    </div>
  </div>
  {hubs()}
  {comparatif()}
  <p class="pro-suite" data-rev><a href="/plateforme/">Ce qu’il y a dans le Hub <i aria-hidden="true">→</i></a></p>
</section>

<section class="sect" id="exemples" aria-labelledby="ex-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Trois exemples</p>
      <h2 id="ex-titre">Un Hub, des solutions,<br><em>une raison.</em></h2>
    </div>
  </div>
  <div class="of-exs">{_exemples()}</div>
</section>

<section class="cta">
  <h2 data-rev>À vous de composer.</h2>
  <div class="acts" data-rev><a class="pill" href="/catalogue/">Composer mon forfait</a>
  <a class="pill ghost" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
