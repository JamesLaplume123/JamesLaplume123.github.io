# Plan du site — toutes les pages, sur une seule page sobre. Le menu et le pied de page vont à
# l'essentiel; c'est cette page qui garde tout le reste accessible.

from config import CAPABILITIES, LIEUX_NAV
import pro

GROUPES = [
    ("Produit", [
        ("/", "Accueil"),
        ("/logiciel/", "Le logiciel"),
        ("/plateforme/", "Le Hub"),
        ("/offre/", "L’offre"),
        ("/catalogue/", "Composer mon forfait"),
    ]),
    ("Solutions", [("/solutions/", "Les sept solutions")]
     + [(f"/solutions/{c['slug']}/", c["title"]) for c in CAPABILITIES]),
    ("Par type de lieu", [(u, n) for u, n, _ in LIEUX_NAV]),
    ("Entreprise", [
        ("/a-propos/", "À propos"),
        ("/vision-roadmap/", "Vision"),
        ("/laboratoire-mobile/", "Laboratoire mobile"),
        ("/confiance/", "Confiance"),
        ("/recherche/", "Recherche"),
    ]),
    ("Aide", [
        ("/questions/", "Questions"),
        ("/contact/", "Contact"),
        ("/confidentialite/", "Confidentialité"),
        ("/mentions-legales/", "Mentions légales"),
        ("/en/", "English"),
    ]),
]

BLOCS = "".join(
    f'<div class="plan-g"><h2>{t}</h2><ul>{"".join(f"""<li><a href="{u}">{n}</a></li>""" for u, n in liens)}</ul></div>'
    for t, liens in GROUPES
)

PAGE = {
    "url": "/plan-du-site/",
    "v2": True,
    "title": "Plan du site | JARVIS Private Systems",
    "description": (
        "Toutes les pages du site JARVIS Private Systems sur une seule page : le logiciel, les "
        "sept solutions, l’offre, l’entreprise et les pages légales."
    ),
    "assets": ["pro"],
    "content": f"""
<section class="plain-top">
  {pro.fil("/plan-du-site/")}
  <h1 data-rev>Plan du site</h1>
</section>

<section class="sect plan-site" aria-label="Toutes les pages">
  <div class="plan-gs">{BLOCS}</div>
</section>
""",
}
