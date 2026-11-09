# Le logiciel (/logiciel/) — JARVIS App en grand, « comme un vrai produit » (refonte « clarté »,
# novembre 2026). La démo complète (src/demos/app.py) dans un cadre d'ordinateur, avec une visite
# guidée : chaque étape ouvre l'écran correspondant et dit ce que le client y gagne. Plein écran et
# aperçu téléphone. Puis ce que l'app prévoit (déplacé de /plateforme/), ce qui est vrai aujourd'hui,
# et l'appel à l'action. Les liens /logiciel/#ecran-<clé> ouvrent directement un écran.
# Styles et script : assets/demos/logiciel.css et logiciel.js (l'app : assets/demos/app.*).

from demos import app
from demos.app import SCREENS, TITLE, fr, icon

# Ce que le client gagne à chaque écran (une phrase simple)
GAIN = {
    "accueil": "Vous savez en un coup d’œil où en sont la maison, vos messages et vos extensions.",
    "assistant": "Vous demandez en mots simples; rien ne se fait sans votre accord.",
    "espace": "Tout ce qui vous concerne est rangé au même endroit, en personnel comme en professionnel.",
    "journee": "Plus besoin d’ouvrir cinq applications pour savoir ce qui s’en vient.",
    "partage": "Vous gardez la main sur qui voit quoi, et jusqu’à quand.",
    "messages": "Vos conversations restent chez vous, sur votre Hub.",
    "appels": "Les numéros inconnus sont filtrés; vous ne manquez plus un appel important.",
    "carte": "Tous vos lieux et vos véhicules en direct, d’un seul regard.",
    "outils": "Chaque extension s’ouvre d’un clic, dans la même application.",
}
NOM = {"carte": "Carte de vos lieux", "assistant": "Assistant", "journee": "Ma journée", "partage": "Partages",
       "messages": "Messages", "appels": "Appels"}


def _etapes():
    out = []
    for i, (k, _n, _d, titre, texte) in enumerate(SCREENS):
        on = i == 0
        out.append(f"""<li><button type="button" class="lg-step{" is-on" if on else ""}" data-step="{k}" aria-pressed="{"true" if on else "false"}">
        <i>{i + 1:02d}</i><span class="lg-step-n">{NOM.get(k, TITLE[k])}</span>
        <span class="lg-step-d"><b>{fr(titre)}</b><span>{fr(texte)}</span><em>{icon("check")}{fr(GAIN[k])}</em></span>
      </button></li>""")
    return "".join(out)


def _maintenant():
    """Légende de l'étape ouverte (tablette et téléphone, sous la rangée d'étapes)."""
    k, _n, _d, titre, texte = SCREENS[0]
    return f'<b>{fr(titre)}</b><span>{fr(texte)}</span><em>{icon("check")}{fr(GAIN[k])}</em>'


PREVU = """<ul class="feats">
    <li data-rev><small>Accès</small><h3>Sur invitation seulement.</h3><p>Aucune inscription publique : chaque compte est créé par l’administrateur du Hub. Clés d’accès prévues — votre biométrie reste sur votre appareil.</p></li>
    <li data-rev><small>Ma journée</small><h3>Agenda et tâches, enfin ensemble.</h3><p>Tous vos calendriers et vos listes, de toutes vos sources, dans une seule vue. Un calendrier en lecture seule le reste.</p></li>
    <li data-rev><small>Messages</small><h3>Vos conversations, chez vous.</h3><p>Texte, photos, documents, vocaux et appels sur le Hub. Micro et caméra ne s’activent jamais sans votre permission.</p></li>
    <li data-rev><small>Assistant</small><h3>Il propose. Vous décidez.</h3><p>En texte ou en voix, il prépare l’action puis attend votre confirmation. Jamais de succès affiché sans résultat réel.</p></li>
    <li data-rev><small>Recommandations</small><h3>Chaque suggestion montre d’où elle vient.</h3><p>Provenance et raison visibles. Une suggestion n’agit jamais à votre place.</p></li>
    <li data-rev><small>Partage</small><h3>Je choisis ce que je partage.</h3><p>Avec qui, pour combien de temps, révocable en tout temps. Un accès retiré disparaît partout.</p></li>
    <li data-rev><small>Carte</small><h3>Voir votre monde, pas celui des autres.</h3><p>Le Hub, vos appareils, et seulement les personnes qui ont choisi de partager. Jamais de fausse position.</p></li>
    <li data-rev><small>Personnalisation</small><h3>Votre accueil vous ressemble.</h3><p>Affichez, ordonnez et dimensionnez vos cartes. Vos préférences suivent votre compte, sans changer vos droits.</p></li>
  </ul>"""

# Ce que vous voyez est vrai : cohérent avec la feuille de route réelle (src/demos/feuille.py).
VRAI = [
    ("existe", "Existe aujourd’hui", [
        "Cette démonstration : les écrans prévus, avec des données d’exemple. Rien n’est commandé.",
        "Le premier JARVIS, sur Home Assistant, dans le laboratoire mobile : lumières et batteries réelles.",
        "Les fondations : un changement qui brise une règle d’architecture est refusé automatiquement.",
    ]),
    ("construit", "En construction · étape 1", [
        "Le noyau : premier démarrage, compte propriétaire, invitation par lien et connexion sécurisée.",
        "Le journal, les rôles et le coffre des secrets.",
        "Les deux interfaces Signature, côté personne et côté administrateur.",
    ]),
    ("avenir", "À venir", [
        "Les extensions branchées sur vos vrais appareils, une à la fois, chacune prouvée.",
        "Les documents et la recherche (étapes 9 et 10), puis l’assistant IA local (étape 13).",
        "Une revue de sécurité par un expert externe avant toute vente (étape 20).",
    ]),
]


def _vrai():
    return "".join(
        f'<article class="lg-v lg-v-{k}" data-rev><p class="lg-v-k"><i></i>{t}</p>'
        f'<ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></article>'
        for k, t, items in VRAI
    )


PAGE = {
    "url": "/logiciel/",
    "v2": True,
    "title": "Le logiciel JARVIS | Démonstration de JARVIS App",
    "description": (
        "JARVIS App en grand : accueil, assistant, messages, appels, carte de vos lieux et extensions. "
        "Une visite guidée, écran par écran."
    ),
    "og_image": "/media/product/user/accueil-og.jpg",
    "assets": ["app", "logiciel"],
    "content": f"""
<section class="lg-hero" aria-labelledby="lg-titre">
  <div class="lg-hero-in" data-rev>
    <p class="eyebrow">Le logiciel · JARVIS App</p>
    <h1 id="lg-titre">Le logiciel JARVIS.<br><em>Voyez-le comme si vous l’aviez.</em></h1>
    <p class="lead">L’application que vous et vos proches utiliseriez chaque jour. Choisissez une étape :
    l’écran s’ouvre. Tout est cliquable.</p>
  </div>
</section>

<section class="lg-tour" id="visite" aria-label="Visite guidée de JARVIS App">
  <div class="lg-tour-in">
    <aside class="lg-guide">
      <p class="lg-guide-k">Visite guidée <span>{len(SCREENS)} étapes</span></p>
      <ol class="lg-steps">{_etapes()}</ol>
      <div class="lg-now" aria-live="polite">{_maintenant()}</div>
      <div class="lg-tools">
        <button type="button" class="lg-tool" data-lg="full">{icon("expand")}<span>Plein écran</span></button>
        <button type="button" class="lg-tool" data-lg="phone" aria-pressed="false">{icon("phone")}<span>Aperçu téléphone</span></button>
      </div>
      <p class="lg-guide-n">Données d’exemple · aucun appareil commandé</p>
    </aside>
    <div class="lg-stage" data-lg-stage>
      <button type="button" class="lg-exit" data-lg="exit">{icon("x")}<span>Quitter le plein écran</span></button>
      <div class="lg-host" data-lg-host><div class="lg-app" data-lg-app>{app.html()}</div></div>
    </div>
  </div>
</section>

<section class="sect alt" id="prevu" aria-labelledby="prevu-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ce que l’app prévoit · 58 vues conçues</p>
      <h2 id="prevu-titre">Tout votre quotidien. <em>Aucune surprise.</em></h2>
    </div>
    <p data-rev>Le parcours complet du compte personnel est dessiné, écran par écran. C’est la direction
    de conception : chaque fonction sera confirmée seulement une fois construite et prouvée.</p>
  </div>
  {PREVU}
</section>

<section class="sect" id="vrai" aria-labelledby="vrai-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Ce que vous voyez est vrai</p>
      <h2 id="vrai-titre">Ce qui existe.<br><em>Ce qui s’en vient.</em></h2>
    </div>
    <div class="side" data-rev>
      <p>Pas de promesse floue : voici où en est vraiment JARVIS. La démo montre les écrans prévus; le
      noyau du logiciel est en construction.</p>
      <a class="pill ghost" href="/vision-roadmap/#feuille-de-route">Voir la feuille de route complète</a>
    </div>
  </div>
  <div class="lg-vs">{_vrai()}</div>
  <p class="lg-under" data-rev>Envie de voir ce qui fait tourner l’application?
  <a href="/plateforme/">Le Hub et l’IA privée, sous le capot <i aria-hidden="true">→</i></a></p>
</section>

<section class="cta">
  <h2 data-rev>Voyez JARVIS<br><span>chez vous.</span></h2>
  <p data-rev>Une rencontre, vos besoins réels, et ce qui fonctionne déjà aujourd’hui.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/" data-magnet>Réserver une démo</a>
  <a class="pill ghost" href="/offre/">Voir l’offre</a></div>
</section>
""",
}
