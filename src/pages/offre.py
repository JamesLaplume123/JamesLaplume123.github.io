# L'offre — comment se compose un JARVIS (refonte « essentiel », novembre 2026).
# Avec les prix du catalogue : 1) le Hub (Base, Signature, Platinum), 2) les solutions par mois;
# 3) le matériel, les kits et le total en direct vivent dans /catalogue/.
# Tous les prix viennent de src/pages/catalogue.py (source unique).
# Styles : assets/demos/parcours.css + assets/demos/offre.css.

from html import escape

from config import CAPABILITIES
from pages import catalogue as CAT
import pro

# Prix affiché sur chaque carte de solution (slug du site → texte)
PRIX_SOL = {s["slug"]: ("Inclus avec le Hub" if s["prix"] == 0 else f"{s['prix']} $/mois" + (" par véhicule" if s.get("unite") else ""))
            for s in CAT.SOLUTIONS}
PRIX_SOL["automatisation-operations"] = f"dès {CAT.ENT_SOCLE['prix']} $/mois + 9 $ par automatisation"


def _p(n):
    return f"{n:,}".replace(",", " ") + " $"


def _hub():
    tuiles = []
    for h in CAT.HUBS:
        tag = f'<span class="of-h-tag">{escape(h["tag"])}</span>' if h["tag"] else ""
        tuiles.append(f"""<a class="of-h" href="/catalogue/#hub" data-rev>
      {tag}<p class="of-h-k">{escape(h['pour'])}</p>
      <h3>{escape(h['nom'])}</h3>
      <p class="of-h-prix">{_p(h['prix'])}<small>une fois</small></p>
    </a>""")
    return f'<div class="of-hs">{"".join(tuiles)}</div>'


def _solutions():
    return "".join(
        f'<a class="card" href="/solutions/{c["slug"]}/" data-rev><small>{escape(PRIX_SOL[c["slug"]])}</small>'
        f'<h3>{c["title"]}</h3><p>{c["menu"]}</p></a>'
        for c in CAPABILITIES
    )


FAQ = [
    ("Dois-je prendre toutes les solutions?",
     "Non. Environnements intelligents vient avec chaque Hub. Les autres s’ajoutent par mois, une à la fois, "
     f"et s’annulent en tout temps. {CAT.COMPLET['nom']} les regroupe à {CAT.COMPLET['prix']} $ par mois si vous en voulez plusieurs."),
    ("Est-ce que je peux l’installer moi-même?",
     "Oui : prises identifiées, aucun fil à couper, plan et vidéo, mise en service à distance. "
     "Si vous préférez, un technicien vous guide en vidéo ou vient sur place."),
    ("Les prix sont-ils définitifs?",
     "Ce sont des points de départ, en dollars canadiens, taxes en sus. Chaque soumission est confirmée par écrit, "
     "ligne par ligne, avant que vous payiez quoi que ce soit."),
]

FAQ_HTML = pro.faq_items(FAQ)


PAGE = {
    "url": "/offre/",
    "v2": True,
    "title": "L’offre JARVIS | Un Hub, vos solutions, le matériel de votre lieu",
    "schema": [pro.ld_faq(FAQ)],
    "description": (
        "Un Hub payé une fois (dès 590 $), des solutions par mois (dès 10 $), le matériel qu’il vous faut. "
        "Composez votre JARVIS et voyez le total dans le catalogue."
    ),
    "og_image": "/media/offre/maison.webp",
    "assets": ["parcours", "offre"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/jarvis-spaces-property-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <h1 data-rev>Un Hub. Vos solutions.<br><em>Rien de plus.</em></h1>
    <p class="lead" data-rev>Un Hub payé une fois, des solutions par mois, le matériel de votre lieu.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/catalogue/">Composer mon JARVIS</a>
    </div>
  </div>
</section>

<section class="sect" id="hub" aria-labelledby="hub-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">1 · Le Hub</p>
      <h2 id="hub-titre">Trois tailles,<br><em>un seul logiciel.</em></h2>
    </div>
  </div>
  {_hub()}
</section>

<section class="sect alt" id="solutions" aria-labelledby="ext-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">2 · Vos solutions</p>
      <h2 id="ext-titre">Par mois,<br><em>comme des apps.</em></h2>
    </div>
  </div>
  <div class="cards">{_solutions()}</div>
  <p class="pro-suite" data-rev><a href="/catalogue/#materiel">3 · Le matériel et l’installation, dans le catalogue <i aria-hidden="true">→</i></a></p>
</section>

<section class="faq" id="questions" aria-labelledby="faq-titre">
  <div class="head" data-rev>
    <p class="eyebrow">L’offre</p>
    <h2 id="faq-titre">Questions fréquentes</h2>
  </div>
  <div class="faq-list">{FAQ_HTML}</div>
</section>

<section class="cta">
  <h2 data-rev>Voyons ce qu’il vous faut.</h2>
  <div class="acts" data-rev><a class="pill" href="/catalogue/">Composer mon JARVIS</a>
  <a class="pill ghost" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
