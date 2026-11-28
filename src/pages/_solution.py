# Gabarit commun des pages de solution, façon Apple : une idée par écran, peu de mots, les preuves en
# petites notes en bas. Chaque module fournit un dict DATA (et son CLAIR) ; solution_page() en fait :
#   ouverture (le nom, la promesse, une phrase, « Ajouter à mon forfait ») →
#   « Imaginez » (un moment réel, minute par minute, et le seul message que JARVIS envoie) →
#   le chiffre (le problème existe, source en note) → la différence (un produit ordinaire, rangée par
#   rangée, contre JARVIS) → ce que JARVIS fait (six tuiles) → démonstration → sur le terrain →
#   en détail (division, pour qui, équipement, prix, notes) → déploiement → questions → prochain pas.
# Les pages sur mesure (Environnements, IA privée, Mobilité) prennent la même ouverture par avec_bande(),
# les mêmes sections par clair_section() et fiche_section().

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


def _note_source(slug):
    n, texte, source, url = CHIFFRES[slug]
    return f'Source du chiffre : <a href="{url}" rel="noopener">{source}</a>.'


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


def bande(slug, nom, c, image):
    """L'ouverture : le nom en petit, la promesse en grand, une phrase, deux gestes."""
    return f"""
<section class="band top ap-hero">
  <div class="bg"><img src="{image}" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil(f"/solutions/{slug}/")}
    <h1 data-rev><span class="ap-nom">{nom}</span>{c['titre']}</h1>
    <p class="lead" data-rev>{c['quoi']}</p>
    <div class="acts" data-rev>
      {forfait_bouton(slug)}
      <a class="ap-lien" href="#essayer">Voir la démonstration ›</a>
    </div>
  </div>
</section>
"""


def avec_bande(contenu, slug, nom, c, image):
    """Pages sur mesure : remplace leur première section (l'ancienne bande) par l'ouverture commune."""
    fin_ = contenu.index("</section>") + len("</section>")
    return bande(slug, nom, c, image) + contenu[fin_:]


def fin(titre):
    return f"""<section class="cta">
  <h2 data-rev>{titre}</h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
"""


def clair_section(c, slug):
    """Le cœur de la page, en quatre écrans : Imaginez, le chiffre, la différence, ce que JARVIS fait."""
    if not c:
        return ""
    moments = "".join(f'<li data-rev><time>{h}</time><span>{x}</span></li>' for h, x in c["moments"])
    n, texte, _, _ = CHIFFRES[slug]
    titre_duel, ordinaire, lignes = c["duel"]
    rangees = "".join(f'<div class="ap-tr" role="row"><span role="cell">{o}</span><span role="cell">{j}</span></div>'
                      for o, j in lignes)
    lien = ('<p class="ap-suite" data-rev><a class="ap-lien" href="/pourquoi-jarvis/">'
            'Pourquoi JARVIS plutôt que Google, Amazon ou Apple ›</a></p>' if c.get("pourquoi", True) else "")
    tuiles = "".join(f'<article class="ap-tuile" data-rev><h3>{t}</h3><p>{p}</p></article>'
                     for t, p in c["capacites"])
    return f"""
<section class="ap ap-moment" id="en-clair" data-toc="Aperçu" aria-labelledby="moment-titre">
  <div class="ap-moment-ph" aria-hidden="true">{galerie.moment_photo(slug)}</div>
  <div class="ap-moment-in">
    <h2 class="ap-h" id="moment-titre" data-rev>Imaginez.</h2>
    <ol class="ap-temps">{moments}</ol>
    <div class="ap-notif" data-rev>
      <p class="ap-notif-t"><b>JARVIS</b><small>maintenant</small></p>
      <p>{c['message']}</p>
    </div>
  </div>
</section>

<section class="ap ap-chiffre" aria-label="Le problème, en un chiffre">
  <p class="ap-n" data-rev>{n}<sup><a href="#notes" aria-label="Note 1">1</a></sup></p>
  <p class="ap-nt" data-rev>{texte}</p>
</section>

<section class="ap ap-duel" aria-labelledby="duel-titre">
  <h2 class="ap-h" id="duel-titre" data-rev>{titre_duel}</h2>
  <div class="ap-tab" role="table" data-rev>
    <div class="ap-tr ap-th" role="row"><span role="columnheader">{ordinaire}</span><span role="columnheader">Avec JARVIS</span></div>
    {rangees}
  </div>
  {lien}
</section>

<section class="ap ap-fait" aria-labelledby="fait-titre">
  <h2 class="ap-h" id="fait-titre" data-rev>Ce que JARVIS fait.</h2>
  <div class="ap-bento">{tuiles}</div>
</section>
"""


def fiche_section(c, slug, pour):
    """En détail, comme une fiche technique : division, pour qui, équipement, prix, puis les notes."""
    eq_titre, eq, eq_note = c["equipement"]
    sup = '<sup><a href="#notes" aria-label="Note 2">2</a></sup>' if eq_note else ""
    notes = f"<li>{_note_source(slug)}</li>" + (f"<li>{eq_note}</li>" if eq_note else "")
    return f"""
<section class="ap ap-fiche" id="en-detail" data-toc="En détail" aria-labelledby="fiche-titre">
  <h2 class="ap-h" id="fiche-titre" data-rev>En détail.</h2>
  <dl class="ap-dl" data-rev>
    <div><dt>Division</dt><dd>{DIVISION[slug]}</dd></div>
    <div><dt>Pour</dt><dd>{pour}</dd></div>
    <div><dt>{eq_titre}{sup}</dt><dd>{" · ".join(eq)}</dd></div>
    <div><dt>Prix</dt><dd>{prix_ligne(slug)}</dd></div>
  </dl>
  <ol class="ap-notes" id="notes">{notes}</ol>
</section>
"""


def solution_page(d):
    compat = "".join(f'<span class="chip">{c}</span>' for c in d["compat"])
    c = d["clair"]
    return {
        "url": f"/solutions/{d['slug']}/",
        "v2": True,
        "title": f"{d['title']} | Solutions JARVIS",
        "description": d["description"],
        "og_image": d["image"],
        "assets": ["coquille", *d.get("assets", []), "galerie"],
        "content": bande(d["slug"], d["title"], c, d["image"]) + clair_section(c, d["slug"]) + f"""
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
{fiche_section(c, d['slug'], d['for'])}
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

""" + fin(d["cta_title"]),
    }
