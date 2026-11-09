# Le Hub et l'IA privée (/plateforme/) — ce qu'il y a sous le capot (refonte « clarté », novembre 2026).
# Rôle de la page face aux deux autres : /logiciel/ montre l'application; /offre/ dit comment ça se
# compose et comment commencer; ici, ce qui fait tourner JARVIS : le Hub, son IA, les extensions qui
# travaillent ensemble, le noyau en Rust, les comptes et les droits. #offre devient un court renvoi.
# Ce que prévoit l'App (58 vues) vit maintenant sur /logiciel/#prevu.

from demos import hub, rust
import parcours

PAGE = {
    "url": "/plateforme/",
    "v2": True,
    "title": "Le Hub et l’IA privée | Sous le capot de JARVIS",
    "description": (
        "Le Hub installé chez vous, son IA locale en français et sept extensions qui "
        "travaillent ensemble : un système privé, local et contrôlé."
    ),
    "og_image": "/media/product/user/accueil-og.jpg",
    "assets": ["rust", "hub", "parcours"],
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Sous le capot · le Hub et l’IA privée</p>
    <h1 data-rev>Votre système privé.<br><em>Un seul point d’entrée.</em></h1>
    <p class="lead" data-rev>Parlez à JARVIS App. JARVIS Core comprend le contexte et applique
    vos règles. JARVIS Hub garde l’intelligence près de vos systèmes.</p>
    <div class="acts" data-rev>
      <a class="pill" href="#hub">Découvrir le Hub</a>
      <a class="pill ghost" href="/logiciel/">Essayer le logiciel</a>
      <a class="pill ghost" href="/offre/">L’offre</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip">Interface · JARVIS App</span>
      <span class="chip">Intelligence · JARVIS Core</span>
      <span class="chip">Sur place · JARVIS Hub</span>
    </div>
  </div>
</section>

<section class="sect hb-sect" id="hub" data-toc="Le Hub" aria-label="Le Hub, cœur de JARVIS">
  """ + hub.coeur() + """
</section>

<section class="sect alt hb-sect" id="ia" data-toc="L’IA" aria-labelledby="ia-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">L’IA au cœur</p>
      <h2 id="ia-titre">Une IA qui comprend.<br><em>Et qui vous laisse décider.</em></h2>
    </div>
    <p data-rev>Une seule IA, sur le Hub. Vous lui parlez normalement; elle propose un plan, explique
    pourquoi et attend votre accord.</p>
  </div>
  """ + hub.ia() + """
</section>

<section class="sect hb-sect" id="ensemble" data-toc="Les extensions ensemble" aria-labelledby="ensemble-titre">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Comment les extensions travaillent ensemble</p>
      <h2 id="ensemble-titre">Chacune son rôle.<br><em>Toutes reliées par le Hub.</em></h2>
    </div>
    <p data-rev>Chaque extension garde son domaine et partage ce qu’elle observe. Le Hub fait respecter
    les droits et garde la trace.</p>
  </div>
  """ + hub.ensemble() + """
</section>

<section class="sect rust-sect" id="rust" data-toc="Rust" aria-labelledby="rust-titre">
  <div class="head shead" data-rev>
    <p class="eyebrow">Le logiciel · écrit en Rust</p>
    <h2 id="rust-titre">Sûr par construction. <em>Pas par promesse.</em></h2>
    <p>Le noyau qui garde vos comptes, vos droits et vos secrets est écrit en Rust, le langage que
    recommandent les agences de cybersécurité pour le logiciel critique.</p>
  </div>
  """ + rust.html() + """
</section>

<section class="sect alt" id="experience" data-toc="Comptes et droits">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Comptes, droits et services</p>
      <h2>Votre identité. Vos règles.<br><em>Votre point d’entrée.</em></h2>
    </div>
    <p data-rev>Avant toute solution, JARVIS connaît seulement les personnes, les rôles et les
    limites que vous avez définis. Rien d’autre n’est relié par défaut, et les utilisateurs n’ont
    jamais de serveur à gérer.</p>
  </div>
  <div class="cards two">
    <article class="card" data-rev>
      <small>Identités configurées</small>
      <h3>Une seule interface, des responsabilités différentes.</h3>
      <p>Chaque personne possède son propre accès.</p>
      <ul>
        <li>Profil principal — administration et décisions sensibles</li>
        <li>Utilisateur autorisé — usage quotidien, actions permises seulement</li>
        <li>Invité temporaire — accès limité dans le temps et révocable</li>
      </ul>
    </article>
    <article class="card" data-rev>
      <small>Contrôle des actions</small>
      <h3>Voir, proposer, approuver et exécuter ne sont pas le même pouvoir.</h3>
      <p>Chaque capacité déclare ses sources, ses actions possibles et la personne qui doit
      approuver. Activer une capacité ne donne pas accès aux autres.</p>
    </article>
    <article class="card" data-rev>
      <small>Où tout fonctionne</small>
      <h3>Hub, vos machines, fournisseurs — affichés séparément.</h3>
      <p>L’administrateur voit où chaque logiciel fonctionne et ce que chaque connexion autorise.
      On teste la connexion, puis on accorde seulement le nécessaire.</p>
    </article>
    <article class="card" data-rev>
      <small>Réparer sans perdre</small>
      <h3>Déconnecter ne veut pas dire supprimer.</h3>
      <p>Une connexion interrompue ne veut pas dire logiciel arrêté. Les données et les
      sauvegardes restent séparées et protégées.</p>
    </article>
  </div>
</section>



""" + parcours.offre_bref(classe="ob ob-sect", toc="L’offre") + """

<section class="cta">
  <h2 data-rev>Quel environnement devrait recevoir<br><span>son propre JARVIS?</span></h2>
  <p data-rev>Présentez le lieu, les systèmes existants et le premier problème que vous
  souhaitez résoudre.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
