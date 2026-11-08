# Solution 02 — IA privée et connaissances. PAGE VEDETTE (sur mesure).
# Contenu tiré du Guide visuel « IA et connaissances » (conception à valider) :
# en clair, démo interactive, trois autorisations, réponses vérifiables,
# périmètres, contrôle.

from demos import coquille
from demos.ia import HTML as DEMO
from pages._solution import clair_section

CLAIR = {
    "quoi": "Posez une question à vos propres documents. <em>La réponse arrive avec sa preuve.</em>",
    "exemple": (
        "Un employé demande : « Comment ferme-t-on l’atelier le vendredi? ». JARVIS cherche dans "
        "vos procédures, vos courriels et vos registres, répond en quatre étapes et montre la page "
        "exacte d’où vient chacune. Si l’information n’existe nulle part, il le dit au lieu d’inventer."
    ),
    "avant": [
        "L’information existe, mais elle est éparpillée entre dossiers, courriels et classeurs.",
        "On dérange la personne qui « sait » à chaque question.",
        "Une IA publique peut inventer une réponse avec beaucoup d’assurance.",
        "Envoyer vos documents à un service externe pose un risque pour la confidentialité.",
    ],
    "apres": [
        "Une question en mots simples, une réponse en quelques secondes.",
        "Chaque réponse montre sa source : le document et le passage exact.",
        "Pas de source fiable? JARVIS le dit clairement, sans rien inventer.",
        "En mode local, tout se passe sur votre Hub : vos documents restent chez vous.",
    ],
    "obtenez": [
        ("Des réponses vérifiables", "Un clic sur le numéro de la source affiche le passage qui justifie la réponse."),
        ("Vos documents restent chez vous", "Traitement local sur le Hub, ou externe seulement si vous l’autorisez, et toujours affiché."),
        ("Des actions avec permission", "JARVIS peut préparer une liste de tâches ou un message. Rien ne part sans votre « Approuver »."),
    ],
}

PAGE = {
    "url": "/solutions/ia-privee-connaissances/",
    "v2": True,
    "title": "IA privée et connaissances | Solutions JARVIS",
    "description": "Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.",
    "og_image": "/media/product/outils/ia.jpg",
    "assets": ["coquille", "ia"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/solutions/ia-privee-connaissances.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution 02 / 07</p>
    <h1 data-rev>IA privée et <em>connaissances.</em></h1>
    <p class="lead" data-rev>Vos documents restent à leur place. L’IA vous aide à les
    comprendre — et montre toujours d’où vient sa réponse.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="#outil">Voir l’outil</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> Particuliers · PME · équipes</p>
  </div>
</section>

<section class="sect sol-demo" id="outil">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez-le · données simulées</p>
      <h2>Parlez à vos propres documents. <em>Chaque réponse montre sa
      preuve.</em></h2>
    </div>
    <p data-rev>Choisissez une question. JARVIS fouille les six documents d’un atelier fictif,
    répond en citant ses sources et vous montre le passage exact. Puis il propose une action :
    elle attend votre « Approuver ». Rien ne quitte le Hub.</p>
  </div>
  """ + coquille.html("ia-privee-connaissances", DEMO) + """
</section>

""" + clair_section(CLAIR) + """

<section class="sect alt">
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

<section class="sect alt">
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

<section class="sect sol-trust">
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
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
