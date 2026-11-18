# Les cartes de Hub « est-ce pour moi? » et le comparatif, partagés par l'accueil et la page /offre/
# (src/pages/catalogue.py : explication et configurateur réunis sur une seule page, décision de James,
# novembre 2026 : « une étape de trop »). Textes : src/lieux.py (HUBS_CHOIX). Aucun montant tant que
# SITE["prix_publics"] est False (src/pro.py). Styles : assets/demos/offre.css.

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
    """La photo du boîtier, si elle existe : media/hubs/hub-<id>.webp. Sinon rien (jamais un dessin)."""
    chemin = f"/media/hubs/hub-{hid}.webp"
    if os.path.exists(os.path.join(_RACINE, chemin.lstrip("/"))):
        return f'<img class="of-h-ph" src="{chemin}" alt="" loading="lazy" decoding="async">'
    return ""


def hubs(guide=True):
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
      <p class="of-h-lieu" data-hub-pour hidden aria-live="polite"></p>
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
    hesite = f"""<div class="of-hes" data-rev>
    <p class="of-hes-t">Vous hésitez?</p>
    <div class="of-qs">{questions}</div>
    <p class="of-hes-r" data-of-raison hidden aria-live="polite"></p>
    <script type="application/json" data-of-raisons>{raisons}</script>
  </div>""" if guide else '<p class="of-h-note" data-hub-note hidden aria-live="polite"></p>'
    return f"""<div class="of-choix" data-of-choix{"" if guide else " data-of-lieux"}>
  <div class="of-hs">{"".join(tuiles)}</div>
  {hesite}
  <p class="of-deux" data-rev>Le Hub s’achète une fois. Les solutions se prennent au mois, et s’annulent quand vous voulez.</p>
  {"" if pro.PRIX else '<p class="of-soum" data-rev>Prix sur soumission, confirmé par écrit.</p>'}
</div>"""
