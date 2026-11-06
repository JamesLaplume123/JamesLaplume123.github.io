# Solution 02 — IA privée et connaissances. PAGE VEDETTE (sur mesure).
# Contenu tiré du Guide visuel « IA et connaissances » (conception à valider) :
# en clair, démo interactive, trois autorisations, réponses vérifiables,
# périmètres, contrôle.

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
    "assets": ["ia"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/solutions/ia-privee-connaissances.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solution 02 / 06</p>
    <h1 data-rev>IA privée et <em>connaissances.</em></h1>
    <p class="lead" data-rev>Vos documents restent à leur place. L’IA vous aide à les
    comprendre — et montre toujours d’où vient sa réponse.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Réserver une démo</a>
      <a class="pill ghost" href="#outil">Voir l’outil</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip chip-sim">Interface conceptuelle · à construire et à tester</span>
      <span class="chip">Particuliers · PME · équipes</span>
      <span class="chip">Traitement local ou autorisé</span>
      <span class="chip">Réponses avec preuves</span>
    </div>
  </div>
</section>

""" + clair_section(CLAIR) + """

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le problème à résoudre</p>
      <h2 style="margin-top:1rem">Vous savez que c’est écrit quelque part. <em>Mais
      où?</em></h2>
    </div>
    <p data-rev>Documents, courriels, photos, procédures : votre information existe, mais
    elle est éparpillée. JARVIS la rend interrogeable — sans la déménager, sans l’exposer,
    et sans jamais inventer de réponse.</p>
  </div>
</section>

<section class="sect" id="outil">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Essayez-le · données simulées</p>
      <h2 style="margin-top:1rem">Parlez à vos propres documents. <em>Chaque réponse montre sa
      preuve.</em></h2>
    </div>
    <p data-rev>Choisissez une question. JARVIS fouille les six documents d’un atelier fictif,
    répond en citant ses sources et vous montre le passage exact. Puis il propose une action :
    elle attend votre « Approuver ». Rien ne quitte le Hub.</p>
  </div>
  """ + DEMO + """
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Le contrôle, en trois crans</p>
      <h2 style="margin-top:1rem">Trois autorisations <em>différentes.</em></h2>
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

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Des réponses honnêtes</p>
      <h2 style="margin-top:1rem">Une réponse utile montre <em>ce qui la justifie.</em></h2>
    </div>
    <p data-rev>Dans la démo, essayez la « question piège » : aucune source ne parle de
    remboursement sans reçu. JARVIS le dit, et propose de demander à la bonne personne au lieu
    d’inventer une règle.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>Règle 01</small>
      <h3>Une source consultable.</h3>
      <p>Nom du document et passage précis — si vous avez toujours le droit de l’ouvrir.</p>
    </article>
    <article class="card" data-rev>
      <small>Règle 02</small>
      <h3>Une version identifiable.</h3>
      <p>Date ou version connue, sans inventer une fraîcheur qui n’a pas été vérifiée.</p>
    </article>
    <article class="card" data-rev>
      <small>Règle 03</small>
      <h3>Une limite explicite.</h3>
      <p>Source ancienne, documents en désaccord ou information manquante : l’IA le dit.</p>
    </article>
  </div>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">À qui appartient quoi</p>
      <h2 style="margin-top:1rem">Personnel, partagé <em>ou professionnel.</em></h2>
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

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Vos données, votre décision</p>
      <h2 style="margin-top:1rem">Reprendre le contrôle, <em>pour vrai.</em></h2>
    </div>
    <p data-rev>Original, copie, index, conversation, mémoire, sauvegarde : chaque trace a
    sa règle, visible et actionnable.</p>
  </div>
  <div class="cards two">
    <article class="card" data-rev>
      <small>Retirer un accès</small>
      <h3>Bloquer les nouveaux usages, immédiatement.</h3>
      <p>Une ancienne autorisation ne suffit plus à chercher ni à agir.</p>
    </article>
    <article class="card" data-rev>
      <small>Supprimer avec précision</small>
      <h3>Original, copie, index, conversation et mémoire se distinguent.</h3>
      <p>Chacun se supprime selon sa propre règle — vérifiée, pas présumée.</p>
    </article>
    <article class="card" data-rev>
      <small>Voir les durées</small>
      <h3>Les délais de conservation sont consultables.</h3>
      <p>Et les options offertes par votre organisation restent visibles.</p>
    </article>
    <article class="card" data-rev>
      <small>Exporter son périmètre</small>
      <h3>Récupérer ses contenus autorisés.</h3>
      <p>Sans embarquer ceux d’une autre personne.</p>
    </article>
  </div>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Déploiement responsable</p>
      <h2 style="margin-top:1rem">« Privé » se vérifie, <em>il ne se décrète pas.</em></h2>
    </div>
    <p data-rev>Qui peut consulter? Où sont les données? Où sont-elles traitées? Trois
    questions, trois réponses affichées avant chaque autorisation.</p>
  </div>
  <div class="cards two">
    <article class="card" data-rev>
      <small>Accord humain</small>
      <h3>Les actions sensibles exigent une validation adaptée au risque.</h3>
    </article>
    <article class="card" data-rev>
      <small>Limite publiée</small>
      <h3 style="font-weight:500;font-size:1rem;color:#b9b9c2;line-height:1.6">« Local » ne
      prouve pas, à lui seul, qu’aucun service externe ne reçoit de données : chaque flux se
      vérifie. L’IA lit seulement les sources autorisées, et une instruction trouvée dans un
      document ne déclenche jamais un accès ni une action.</h3>
    </article>
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
