# Pourquoi JARVIS — la comparaison avec Google Home, Alexa et Apple Maison (refonte « trois divisions »).
# Règle : chaque affirmation sur un concurrent est vérifiée et sourcée, avec sa date de vérification.
# Aucune affirmation sur les prix de JARVIS ni sur ce qu'un niveau comprend (c'est l'offre qui le dit).
# Styles : assets/demos/divisions.css.

import pro

VERIFIE = "27 novembre 2026"

# (ligne, (point, texte, note) pour JARVIS, Google Home, Alexa, Apple Maison)
# point : o = oui, m = en partie, n = non
LIGNES = [
    ("Installé et réglé pour vous",
     ("o", "Oui", "Nous venons chez vous, tout est réglé"),
     ("n", "Non", "À faire soi-même"), ("n", "Non", "À faire soi-même"), ("n", "Non", "À faire soi-même")),
    ("Fonctionne même sans Internet",
     ("o", "Oui", "Les routines et les alertes tournent dans l’appareil"),
     ("m", "En partie", "La voix et l’IA passent par Internet"),
     ("m", "En partie", "Une panne chez Amazon l’a arrêtée des heures"),
     ("m", "En partie", "Avec un HomePod ou une Apple TV")),
    ("Votre voix et vos images restent chez vous",
     ("o", "Oui", "Analysées et gardées dans l’appareil"),
     ("n", "Non", "Vidéos gardées dans le nuage de Google"),
     ("n", "Non", "Les demandes vocales partent chez Amazon"),
     ("m", "En partie", "Vidéos chiffrées, mais gardées dans iCloud")),
    ("Agit tout seul quand c’est grave",
     ("o", "Oui", "Coupe l’eau, bloque l’intrus, appelle la bonne personne"),
     ("m", "En partie", "Si vous achetez et réglez tout vous-même"),
     ("m", "En partie", "Si vous achetez et réglez tout vous-même"),
     ("m", "En partie", "Si vous achetez et réglez tout vous-même")),
    ("Votre réseau surveillé, les intrus bloqués",
     ("o", "Oui", "Avec Réseau et cybersécurité"),
     ("n", "Non", "Pas compris"), ("n", "Non", "Pas compris"), ("n", "Non", "Pas compris")),
    ("Personne ne peut vous retirer une fonction",
     ("o", "Oui", "Tout tourne chez vous, sur des appareils standards"),
     ("n", "Non", "Ses premiers thermostats Nest, coupés"),
     ("n", "Non", "Une option de confidentialité, retirée"),
     ("m", "En partie", "L’iPad n’est plus accepté comme centre de la maison")),
]

FAITS = [
    ("20 octobre 2025", "Une panne chez Amazon arrête Alexa et les caméras Ring pendant des heures.",
     "Associated Press", "https://www.pbs.org/newshour/nation/amazon-cloud-computing-outage-disrupts-snapchat-ring-and-many-other-online-services"),
    ("28 mars 2025", "Amazon retire l’option qui gardait la voix dans l’appareil : les demandes partent dans son nuage.",
     "TechCrunch", "https://techcrunch.com/2025/03/15/amazons-echo-will-send-all-voice-recordings-to-the-cloud-starting-march-28"),
    ("25 octobre 2025", "Google coupe l’application de ses premiers thermostats Nest.",
     "Google", "https://support.google.com/googlehome/answer/16233096?hl=en"),
]


def _cell(c, j=False):
    p, t, n = c
    cls = ' class="cmp-j"' if j else ""
    texte = f"<b>{t}</b>" if j else t
    return f'<td{cls}><span class="pt pt-{p}" aria-hidden="true"></span>{texte}<small>{n}</small></td>'


TABLE = "".join(
    f'<tr><td class="cmp-k">{k}</td>{_cell(a, True)}{_cell(b)}{_cell(c)}{_cell(d)}</tr>'
    for k, a, b, c, d in LIGNES
)
CARTES = "".join(
    f'<div class="fait" data-rev><em>{d.upper()}</em><p>{t}</p><small>Source : <a href="{u}" rel="noopener">{s}</a></small></div>'
    for d, t, s, u in FAITS
)

PAGE = {
    "url": "/pourquoi-jarvis/",
    "v2": True,
    "title": "Pourquoi JARVIS | JARVIS Private Systems",
    "description": (
        "Installé pour vous, local même sans Internet, vos images chez vous, votre réseau surveillé : "
        "JARVIS face à Google Home, Alexa et Apple Maison, point par point."
    ),
    "og_image": "/media/accueil/film-maison.webp",
    "assets": ["divisions"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/accueil/film-maison.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil("/pourquoi-jarvis/")}
    <h1 data-rev>Pourquoi <em>JARVIS.</em></h1>
    <p class="lead" data-rev>Eux vendent des appareils à brancher soi-même. JARVIS livre une maison qui se protège et se gère toute seule.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/solutions/">Voir les solutions</a>
      <a class="pill ghost" href="#comparaison">Voir la comparaison</a>
    </div>
  </div>
</section>

<section class="sect" id="comparaison" aria-labelledby="pq-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Point par point</p>
      <h2 id="pq-titre">Google Home, Alexa, Apple Maison <em>et JARVIS.</em></h2>
    </div>
    <div class="side" data-rev><p>Ce que vous obtenez, sans le jargon.</p></div>
  </div>
  <div class="cmp-w" data-rev>
    <table class="cmp">
      <thead><tr><th scope="col"><span class="sr-only">Critère</span></th><th scope="col" class="cmp-j">JARVIS</th><th scope="col">Google Home</th><th scope="col">Alexa</th><th scope="col">Apple Maison</th></tr></thead>
      <tbody>{TABLE}</tbody>
    </table>
  </div>
  <div class="cmp-leg"><span><span class="pt pt-o" aria-hidden="true"></span>Oui</span><span><span class="pt pt-m" aria-hidden="true"></span>En partie</span><span><span class="pt pt-n" aria-hidden="true"></span>Non</span></div>
</section>

<section class="sect alt" id="faits" aria-labelledby="pq-faits">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ce qui est vraiment arrivé</p>
      <h2 id="pq-faits">Quand tout dépend <em>du nuage d’un autre.</em></h2>
    </div>
    <div class="side" data-rev><p>Ce qu’ils font bien : c’est peu cher pour commencer. JARVIS s’adresse à ceux qui veulent que tout fonctionne vraiment, tout le temps.</p></div>
  </div>
  <div class="faits">{CARTES}</div>
  <p class="form-note" style="max-width:84rem;margin:2rem auto 0">Comparaison vérifiée le {VERIFIE}. Google Home, Alexa et Apple Maison sont des marques de leurs propriétaires.</p>
</section>

<section class="cta">
  <h2 data-rev>Une maison qui se protège <em>toute seule.</em></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
