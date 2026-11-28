# Règles de travail — site JARVIS (jarvisprivatesystems.com)

Ces règles s'appliquent à toute session et à tout agent dans ce dépôt. Elles reprennent la méthode
du logiciel JARVIS, adaptée à un site.

## Qui est qui

- **James** est le propriétaire du produit. Il ne lit pas le code. Il décide du *quoi* ; il
  approuve ce qui va en ligne et tout changement de la loi du site.
- **La session principale est le chef.** Elle reçoit les demandes, les classe, les découpe,
  délègue aux agents de `.claude/agents/` et fait rapport à James. Pour un changement de contenu
  ou de structure, le chef ne fait pas le travail lui-même : il le confie aux agents.

## À lire avant toute tâche

1. `docs/SITE.md` — la loi du site : le plan, le style, la façon de vendre.
2. `docs/plan_du_site.json` — la liste fermée des pages et leur statut.
3. `docs/FEUILLE_DE_ROUTE.md` — l'étape en cours. On ne travaille que sur elle.
4. `docs/OFFRE.md` — si la demande touche l'offre, les appareils ou les forfaits.

## Au début de chaque session : l'essai témoin

La session doit être ouverte sur le dossier du site : sinon les garde-fous ne tournent pas.
Avant toute autre commande, le chef lance dans le terminal :

    : site-temoin

Cette commande ne fait rien. Attendu : le garde-fou du terminal la refuse avec le mot « Témoin ».
Si elle passe, les garde-fous ne sont pas chargés : le chef n'écrit rien, ne lance aucune commande
Git ou GitHub, et dit à James, en une ligne, de rouvrir la session sur le dossier du site.

## Le chemin de chaque demande

1. **Classer** la demande :
   - *Visuel* : apparence seulement, une seule page. Risque faible.
   - *Contenu* : textes, images, chiffres, exemples. Risque moyen.
   - *Structure* : plan du site, menu, nouvelle page, gabarit, offre, formulaires. Risque élevé.
2. **Situer** avec l'agent `architecte` : la place de la demande dans le plan, et tout ce qu'elle
   touche ailleurs (menu, pied de page, accueil, pages sœurs, version anglaise).
3. **Si la loi du site ou le plan doit changer**, arrêter et demander à James. La documentation
   change avant le code.
4. **Écrire** avec l'agent `redacteur` : les textes, au budget de la loi, chaque chiffre avec sa
   source vérifiée.
5. **Bâtir** avec l'agent `developpeur`, sur une branche dédiée, avec les gabarits communs.
6. **Vérifier** : `scripts/check.sh` doit passer en entier.
7. **Réviser** avec l'agent `reviseur`, qui fait le tour de tout le site, pas seulement de la page
   changée. Ajouter l'agent `securite` pour tout ce qui touche formulaires, page d'administration,
   Worker, secrets ou données personnelles.
8. **Montrer à James** les captures (`scripts/captures.py`) et un rapport en français simple,
   5 lignes au maximum :
   - Ce que tu as demandé
   - Ce qui a changé
   - Ce qui est touché ailleurs
   - Résultat des vérifications
   - Quoi regarder à l'écran
9. **Mettre en ligne** seulement sur le « mets en ligne » ou « fusionne » explicite de James.

Une correction de faute ou de couleur peut sauter les étapes 2 et 4. Les étapes 6, 8 et 9 ne se
sautent jamais.

**Fichiers de règles** (`CLAUDE.md`, `docs/SITE.md`, `docs/plan_du_site.json`, `docs/OFFRE.md`,
`.claude/`, `.github/`, `.githooks/`, `scripts/check.sh`, `scripts/verifier_*`) : le chef les
modifie lui-même, seulement avec l'accord de James, en nommant chaque fichier en clair (outils Edit
et Write). Les agents ne les modifient jamais.

## Règles absolues

- **Ne rien perdre.** Une page retirée garde son adresse par une redirection. Le contenu remplacé
  est vérifié : chaque lien et chaque information de l'ancienne version existe dans la nouvelle.
- **Remplacer, jamais empiler.** Une nouvelle version d'une section remplace l'ancienne dans le même
  changement. Pas de doublon, pas de code ni de style mort.
- **Un seul style.** Jamais l'ancien et le nouveau style dans la même page une fois qu'elle est
  « fait » dans le plan.
- **Rien d'inventé.** Chaque chiffre a sa source, chaque comparaison est vraie, l'état du projet
  (en conception) est dit honnêtement.
- **Aucun secret dans le code ni dans Git.** Jamais de mot de passe ou de jeton tapé par un agent.
- **Le vrai logiciel ne va jamais en ligne** : seulement des démonstrations avec des données
  d'exemple.
- **Forfaits et prix : James décide.** Aucune inclusion ni aucun prix inventé.
- **Une idée nouvelle n'est pas une tâche.** Elle va dans `docs/IDEES.md` jusqu'à ce que James la
  choisisse.
- **Une question sur un choix incertain se pose avant de bâtir**, pas après.

## Git

- Une branche par changement. Petits commits, messages en français.
- `main` reçoit seulement du travail vérifié et révisé, par une demande de fusion. La fusion est
  faite par James (bouton « Merge ») ou, sur son « mets en ligne » ou « fusionne » explicite, par
  le chef. Après une fusion, `main` locale se remet sur `origin/main`.
- Personne ne pousse sur `main`, ne force un envoi ni ne commet sur `main`. Le verrou d'envoi
  (`.githooks/pre-push`) et le garde-fou du terminal arrêtent les formes ordinaires.
- Le site publié est bâti par `python3 tools/build.py` : les fichiers bâtis sont commis avec leur
  source, dans le même changement.
- **Audit de dérive toutes les 10 fusions :** l'agent `reviseur` compare tout le site à
  `docs/SITE.md` et signale les écarts à James.

## Communication avec James

Court, concret, sans jargon. Les termes techniques sont expliqués en une phrase. Quand quelque
chose bloque, le dire tout de suite avec ce qu'il faut pour avancer.
