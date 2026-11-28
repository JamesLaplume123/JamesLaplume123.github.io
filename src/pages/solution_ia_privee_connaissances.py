# Solution 02 — IA privée et connaissances. PAGE VEDETTE (sur mesure).
# Contenu tiré du Guide visuel « IA et connaissances » (conception à valider) :
# en clair, démo interactive, trois autorisations, réponses vérifiables,
# périmètres, contrôle.

from demos import coquille
from demos.ia import HTML as DEMO
from pages._solution import clair_section, fiche_section, avec_bande
import galerie

# « En clair », bâti comme l'offre (voir pages/_solution.py, clair_section). Solution de JARVIS Privé :
# l'exemple est celui d'une famille; la version entreprise est « Savoir de l'entreprise ».
CLAIR = {
    "titre": "Posez une question à vos documents. <em>La source est montrée.</em>",
    "quoi": "Vos garanties, contrats et manuels répondent. Avec la page qui le prouve.",
    "moments": [
        ("Samedi", "Le lave-vaisselle fuit."),
        ("Samedi", "« Est-il encore garanti? »"),
        ("Samedi", "JARVIS montre la ligne qui le prouve."),
    ],
    "message": "Oui, garanti jusqu’au 14 mars. Source : garantie, page 2.",
    "duel": ("Plus qu’un assistant IA en ligne.", "Un assistant IA en ligne", [
        ("Vos documents partent en ligne.", "Ils restent chez vous."),
        ("Une réponse sans preuve.", "La source, à chaque réponse."),
        ("Il invente parfois.", "Il dit quand il ne sait pas."),
        ("Il ne connaît pas vos papiers.", "Vos papiers, déjà classés."),
    ]),
    "capacites": [
        ("Vos papiers répondent", "Garanties, contrats, factures, manuels."),
        ("Des réponses vérifiables", "Le passage exact, d’un toucher."),
        ("Aucune invention", "Pas de source? Il le dit."),
        ("Chez vous", "L’IA tourne dans votre JARVIS."),
        ("Chacun son espace", "Vos papiers restent les vôtres."),
        ("Rien sans vous", "Chaque action attend votre accord."),
    ],
    "equipement": ("Ce qu’il faut", [
        "Votre appareil JARVIS : l’IA tourne dedans",
        "Vos dossiers, courriels et numérisations, reliés avec votre accord"], ""),
}

POUR = "Particuliers et familles"

PAGE = {
    "url": "/solutions/ia-privee-connaissances/",
    "v2": True,
    "title": "IA privée et connaissances | Solutions JARVIS",
    "description": "Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.",
    "og_image": "/media/product/outils/ia.jpg",
    "assets": ["coquille", "ia", "galerie"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/solutions/ia-privee-connaissances.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution 02 / 07</p>
    <h1 data-rev>IA privée et <em>connaissances.</em></h1>
    <p class="lead" data-rev>Vos documents restent à leur place. L’IA vous aide à les
    comprendre — et montre toujours d’où vient sa réponse.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="#outil">Voir l’outil</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> Particuliers · PME · équipes</p>
  </div>
</section>

""" + clair_section(CLAIR, "ia-privee-connaissances") + """

<section class="sect sol-demo" id="essayer" data-toc="Essayer">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez-le · données simulées</p>
      <h2>Parlez à vos propres documents. <em>Chaque réponse montre sa
      preuve.</em></h2>
    </div>
    <p data-rev>Choisissez une question : JARVIS répond en citant le passage exact, puis propose
    une action qui attend votre « Approuver ». Rien ne quitte votre JARVIS.</p>
  </div>
  """ + coquille.html("ia-privee-connaissances", DEMO) + """
</section>

<section class="sect alt" id="controle" data-toc="Le contrôle">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le contrôle, en trois crans</p>
      <h2>Trois autorisations <em>différentes.</em></h2>
    </div>
    <p data-rev>Une connexion n’active ni la lecture par l’IA, ni les commandes, ni le
    partage externe. Chaque pouvoir se donne séparément — et se retire séparément.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>01 · Connecter</small>
      <h3>JARVIS peut joindre un compte ou un service précis.</h3>
      <p>Relier votre agenda ou votre stockage ne donne encore aucun droit de lecture à
      l’IA.</p>
    </article>
    <article class="card" data-rev>
      <small>02 · Autoriser à lire</small>
      <h3>Vous choisissez les dossiers, les usages et la destination du traitement.</h3>
      <p>Dossier par dossier, avec le lieu de traitement — local ou externe — toujours
      affiché avant votre accord.</p>
    </article>
    <article class="card" data-rev>
      <small>03 · Autoriser une action</small>
      <h3>Créer un rappel ou envoyer un message exige son propre droit.</h3>
      <p>L’IA prépare, vous confirmez, l’outil autorisé exécute — et rapporte le résultat
      réel.</p>
    </article>
  </div>
</section>

<section class="sect alt" id="perimetres" data-toc="Périmètres">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">À qui appartient quoi</p>
      <h2>Personnel, partagé <em>ou professionnel.</em></h2>
    </div>
    <p data-rev>Ces périmètres indiquent à qui le contenu est ouvert — pas où se trouve son
    serveur. Le rôle d’administrateur est une permission de gestion, jamais un passe-partout
    sur vos contenus.</p>
  </div>
  <div class="rows">
    <div class="row" data-rev>
      <i>Personnel</i>
      <div><h3>Moi uniquement.</h3>
      <p>Mes notes, mes factures, mes documents choisis.</p></div>
    </div>
    <div class="row" data-rev>
      <i>Partagé</i>
      <div><h3>Les personnes choisies.</h3>
      <p>Maison, famille ou projet — chaque partage est explicite : la notice du
      chauffe-eau, pas tout votre dossier personnel.</p></div>
    </div>
    <div class="row" data-rev>
      <i>Professionnel</i>
      <div><h3>Mon organisation.</h3>
      <p>Procédures et dossiers ouverts à mon rôle — et le serveur vérifie les droits
      avant la recherche, à l’ouverture et avant chaque action.</p></div>
    </div>
  </div>
</section>

""" + galerie.terrain("ia-privee-connaissances") + """

""" + fiche_section(CLAIR, "ia-privee-connaissances", POUR) + """
<section class="sect sol-trust" id="deploiement" data-toc="Déploiement">
  <div class="trust" data-rev>
    <div>
      <p class="eyebrow">Déploiement responsable</p>
      <h2>« Privé » se vérifie, <em>il ne se décrète pas.</em></h2>
      <p>Qui peut consulter? Où sont les données? Où sont-elles traitées? Trois
      questions, trois réponses affichées avant chaque autorisation.</p>
    </div>
    <dl>
      <div><dt>Accord humain</dt><dd>Les actions sensibles exigent une validation adaptée au risque.</dd></div>
      <div><dt>Vos données</dt><dd>Retirer un accès bloque aussitôt tout nouvel usage. Original, copie, index,
      conversation et mémoire se suppriment chacun selon leur règle, et vous pouvez exporter vos contenus.</dd></div>
      <div><dt>Limite publiée</dt><dd>« Local » ne prouve pas, à lui seul, qu’aucun service externe ne reçoit
      de données : chaque flux se vérifie. L’IA lit seulement les sources autorisées, et une instruction trouvée
      dans un document ne déclenche jamais un accès ni une action.</dd></div>
    </dl>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Quelle information mérite enfin<br><span>d’être retrouvable?</span></h2>
  <p data-rev>Décrivez vos documents, vos outils actuels et ce que vous cherchez trop
  souvent sans le trouver.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}

PAGE["content"] = avec_bande(PAGE["content"], "ia-privee-connaissances", "IA privée et connaissances", CLAIR, "/media/solutions/ia-privee-connaissances.webp")

