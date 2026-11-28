# Gabarit commun des pages de solution.
# Chaque module fournit un dict DATA ; solution_page() le transforme en page :
# bande (fil d'Ariane, une phrase, « Ajouter à mon forfait ») → « En clair », bâti comme l'offre (la
# promesse, « Imaginez », le chiffre, la différence avec un produit ordinaire, ce que JARVIS fait,
# l'équipement) → démonstration interactive → sur le terrain (photos) → déploiement responsable →
# questions (ajoutées par partials.document) → prochain pas. On comprend d'abord, on essaie ensuite.
# Les pages sur mesure (Environnements, IA privée, Mobilité) reprennent la même bande par bande().
# Refonte « trois divisions » (novembre 2026) : la bande dit à quelle division appartient la solution,
# et « En clair » ouvre sur un chiffre réel et sourcé qui montre que le problème existe.

from config import CAPABILITIES
from pages import catalogue as CAT

PRIX = {s["slug"]: ("Inclus à tous les niveaux" if s["prix"] == 0 else f"{s['prix']} $ par mois" + (" par véhicule" if s.get("unite") else "")) for s in CAT.SOLUTIONS}
PRIX["automatisation-operations"] = f"Dès {CAT.ENT_SOCLE['prix']} $ par mois, puis 9 à 29 $ par automatisation"
from demos import coquille
import galerie
import pro

_CAP = {c["slug"]: c for c in CAPABILITIES}

# La division de chaque solution (src/divisions.py) : les cinq solutions des lieux servent les deux.
_PRIVE = '<a href="/solutions/#prive">JARVIS Privé</a>'
_ENTREPRISE = '<a href="/solutions/entreprise/">JARVIS Entreprise</a>'
DIVISION = {
    "reseau-resilience": f"{_PRIVE} et {_ENTREPRISE}",
    "securite-intelligente": f"{_PRIVE} et {_ENTREPRISE}",
    "diagnostic-care": f"{_PRIVE} et {_ENTREPRISE}",
    "environnements-intelligents": f"{_PRIVE} et {_ENTREPRISE}",
    "mobilite": f"{_PRIVE} et {_ENTREPRISE}",
    "ia-privee-connaissances": _PRIVE,
    "automatisation-operations": _ENTREPRISE,
}

# Le problème, en un chiffre réel (vérifiés le 27 novembre 2026) : (chiffre, ce qu'il dit, source, lien).
CHIFFRES = {
    "securite-intelligente": ("6 139", "entrées par effraction à Montréal en 2025, en hausse de 6 % sur 2024.",
                              "données du SPVM, Narcity",
                              "https://www.narcity.com/fr/montreal/montreal-introductions-effraction-janvier-2026"),
    "reseau-resilience": ("29", "attaques par jour contre une maison connectée, en moyenne, en 2025.",
                          "Bitdefender et NETGEAR",
                          "https://www.bitdefender.com/en-gb/news/new-bitdefender-and-netgear-report-reveals-rising-threats-across-the-connected-home-landscape"),
    "diagnostic-care": ("47 %", "des réclamations d’assurance habitation au Québec sont liées à des dégâts d’eau.",
                        "Bureau d’assurance du Canada",
                        "https://www.protegez-vous.ca/partenaires/bureau-dassurance-du-canada/degats-d-eau-mieux-connaitre-les-couvertures-d-assurance-grace-a-une-maison-interactive"),
    "environnements-intelligents": ("55 %", "de l’électricité d’une maison au Québec sert au chauffage.",
                                    "Hydro-Québec, Transition énergétique Québec",
                                    "https://transitionenergetique.gouv.qc.ca/fileadmin/medias/pdf/residentiel/Brochure-soyons-ecoenergetiques-habitation.pdf"),
    "mobilite": ("7 742", "véhicules volés au Québec en 2025. Environ la moitié n’est jamais retrouvée.",
                 "Équité Association, Protégez-Vous",
                 "https://www.protegez-vous.ca/nouvelles/automobile/vol-auto-statistiques"),
    "automatisation-operations": ("37 %", "des appels aux salons et aux spas restent sans réponse.",
                                  "Zenoti", "https://www.zenoti.com/fr/thecheckin/how-track-salon-call-conversion-rate"),
    "ia-privee-connaissances": ("83 %", "des Canadiens sont préoccupés par leur vie privée quand ils utilisent des outils d’IA.",
                                "Commissariat à la protection de la vie privée du Canada, sondage 2024-2025",
                                "https://www.priv.gc.ca/fr/pour-les-institutions-federales/bulletins-sur-la-lprp/pab_20250605/"),
}


def chiffre(slug):
    """Le chiffre réel du problème, en tête de « En clair »."""
    if slug not in CHIFFRES:
        return ""
    n, texte, source, url = CHIFFRES[slug]
    return (f'<p class="clair-chiffre"><b>{n}</b><span>{texte}'
            f'<small>Source : <a href="{url}" rel="noopener">{source}</a></small></span></p>')


# Image d'aperçu, utilisée tant qu'une solution n'a pas sa démo interactive (DATA["demo_html"]).
FRAME = """<figure class="frame" data-rev>
    <img src="{img}" alt="Aperçu conceptuel — {title}" loading="lazy">
    <figcaption>
      <span>JARVIS App · {up}</span>
      <strong>{cap}</strong>
    </figcaption>
  </figure>"""


def prix_ligne(slug):
    """Le prix de la solution; sur soumission tant que les prix ne sont pas publics (SITE["prix_publics"])."""
    if not pro.PRIX:
        return pro.SOUMISSION
    return PRIX.get(slug, "Voir le configurateur")


def forfait_bouton(slug):
    """« Ajouter à mon forfait » : le choix suit le visiteur jusqu'au configurateur (assets/js/wow.js).
    Environnements intelligents vient avec tous les niveaux : rien à ajouter, on va composer."""
    if slug == "environnements-intelligents":
        return '<a class="pill" href="/offre/#composer">Inclus à tous les niveaux · composer mon forfait</a>'
    return (f'<button type="button" class="pill" data-forfait-add="{slug}" aria-pressed="false">'
            '<span data-forfait-off>Ajouter à mon forfait</span><span data-forfait-on hidden>Dans mon forfait ✓</span></button>')


def bande(slug, h1, lead, image, pour):
    """Ouverture commune : fil d'Ariane, le titre, une phrase, le forfait, pour qui, le prix."""
    return f"""
<section class="band top">
  <div class="bg"><img src="{image}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil(f"/solutions/{slug}/")}
    <h1 data-rev>{h1}</h1>
    <p class="lead" data-rev>{lead}</p>
    <div class="acts" data-rev>
      {forfait_bouton(slug)}
      <a class="pill ghost" href="#essayer">Essayer la démonstration</a>
    </div>
    <p class="for-line" data-rev><span>Division</span> {DIVISION[slug]}</p>
    <p class="for-line" data-rev><span>Pour</span> {pour}</p>
    <p class="for-line" data-rev><span>Prix</span> {prix_ligne(slug)}</p>
  </div>
</section>
"""


def avec_bande(contenu, slug, h1, lead, image, pour):
    """Pages sur mesure : remplace leur première section (l'ancienne bande) par la bande commune."""
    fin = contenu.index("</section>") + len("</section>")
    return bande(slug, h1, lead, image, pour) + contenu[fin:]


def fin(titre):
    return f"""<section class="cta">
  <h2 data-rev>{titre}</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
"""


def clair_section(c, slug=""):
    """Bloc « En clair », bâti comme l'offre : la promesse, « Imaginez », le chiffre réel, la différence avec
    un produit ordinaire (rangée par rangée, photos en tête), les six choses que JARVIS fait, l'équipement."""
    if not c:
        return ""
    ph_avant, ph_apres = galerie.avant_apres_photos(slug)
    titre_duel, ordinaire, lignes = c["duel"]
    avant = "".join(f"<li>{o}</li>" for o, _ in lignes)
    apres = "".join(f"<li>{j}</li>" for _, j in lignes)
    rangees = len(lignes) + 2  # la photo, l'étiquette, puis une rangée par différence
    lien = ('<a class="clair-lien" href="/pourquoi-jarvis/">Pourquoi JARVIS plutôt que Google, Amazon ou Apple ›</a>'
            if c.get("pourquoi", True) else "")
    capacites = "".join(
        f"""<article class="card" data-rev><small>{i + 1:02d}</small><h3>{t}</h3><p>{p}</p></article>"""
        for i, (t, p) in enumerate(c["capacites"])
    )
    eq_titre, eq, eq_note = c["equipement"]
    puces = "".join(f'<span class="chip">{x}</span>' for x in eq)
    note = f"<small>{eq_note}</small>" if eq_note else ""
    return f"""
<section class="clair" id="en-clair" data-toc="En clair" aria-labelledby="clair-titre">
  <div class="clair-head" data-rev>
    <p class="eyebrow">En clair</p>
    <h2 id="clair-titre">{c['titre']}</h2>
    <p class="clair-sub">{c['quoi']}</p>
    <p class="clair-ex"><b>Imaginez :</b> {c['imaginez']}</p>
    {chiffre(slug)}
  </div>
  <div class="clair-bloc" data-rev>
    <p class="eyebrow">La différence</p>
    <h3 class="clair-t">{titre_duel}</h3>
    {lien}
  </div>
  <div class="vs duel" style="--r:{rangees}" data-rev>
    <div class="vs-col vs-before">{ph_avant}<p class="vs-k">{ordinaire}</p><ul>{avant}</ul></div>
    <div class="vs-arrow" aria-hidden="true"><span></span></div>
    <div class="vs-col vs-after">{ph_apres}<p class="vs-k">Avec JARVIS</p><ul>{apres}</ul></div>
  </div>
  <p class="eyebrow clair-k" data-rev>Ce que JARVIS fait</p>
  <div class="cards">{capacites}</div>
  <div class="clair-eq" data-rev><p class="eyebrow">{eq_titre}</p>{puces}{note}</div>
</section>"""


def solution_page(d):
    compat = "".join(f'<span class="chip">{c}</span>' for c in d["compat"])
    return {
        "url": f"/solutions/{d['slug']}/",
        "v2": True,
        "title": f"{d['title']} | Solutions JARVIS",
        "description": d["description"],
        "og_image": d["image"],
        "assets": ["coquille", *d.get("assets", []), "galerie"],
        "content": bande(d["slug"], d["h1"], d["lead"], d["image"], d["for"]) + f"""
{clair_section(d.get('clair'), d['slug'])}
<section class="sect sol-demo" id="essayer" data-toc="Essayer">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez · démonstration interactive</p>
      <h2>{d['demo_title']}</h2>
    </div>
    <p data-rev>{d['demo_copy']}</p>
  </div>
  {coquille.html(d['slug'], d.get('demo_html') or FRAME.format(img=d.get('demo_image', d['image']), title=d['title'], up=d['title'].upper(), cap=d.get('demo_caption', 'Prototype interactif — données simulées.')))}
  {d.get('extra', '')}
</section>
{galerie.terrain(d['slug']) if d['slug'] in galerie.SOLUTIONS else ''}

<section class="sect sol-trust" id="deploiement" data-toc="Déploiement">
  <div class="trust" data-rev>
    <div>
      <p class="eyebrow">Déploiement responsable</p>
      <h2>{d['deploy_title']}</h2>
      <p>{d['deploy_copy']}</p>
    </div>
    <dl>
      <div><dt>Accord humain</dt><dd>Les actions sensibles exigent une validation adaptée au risque.</dd></div>
      <div><dt>Limite publiée</dt><dd>{d['limit']}</dd></div>
      <div><dt>Compatibilités possibles</dt><dd class="chips">{compat}</dd></div>
    </dl>
  </div>
</section>

""" + fin(d["cta_title"]) + """""",
    }
