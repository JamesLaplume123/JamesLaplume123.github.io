# Architecture d'information du site JARVIS

Statut: proposition de phase 1 à approuver avant toute modification de la
navigation publique.

## 1. Objectif

Le site doit permettre à une personne non technique de répondre rapidement à
quatre questions:

1. Qu'est-ce que JARVIS?
2. Quel problème peut-il résoudre pour moi?
3. Qu'est-ce qui existe réellement aujourd'hui?
4. Comment puis-je discuter du projet?

Chaque page reçoit un seul rôle principal. Une idée expliquée en détail sur une
page ne doit apparaître ailleurs que sous forme de résumé ou de lien.

## 2. Navigation principale proposée

Le logo ramène à l'accueil. La navigation visible contient seulement:

1. Solutions
2. JARVIS
3. Laboratoire mobile
4. Vision
5. À propos
6. Parler du projet

La langue demeure une commande séparée.

### Changements par rapport au menu actuel

- "Plateforme" devient "JARVIS" dans le menu. L'URL `/plateforme/` peut être
  conservée pour éviter une migration inutile.
- "Recherche" quitte le menu principal et reste accessible depuis le
  Laboratoire mobile, Vision, À propos et le pied de page.
- "Confiance" quitte le menu principal et reste accessible depuis JARVIS,
  toutes les démonstrations, le pied de page et les mentions de permissions.
- "Contact" reste présenté comme la commande principale "Parler du projet".

Cette navigation réduit la concurrence entre des pages institutionnelles et le
parcours commercial principal.

## 3. Rôle exclusif de chaque page

### Accueil

Rôle: comprendre l'ensemble en moins d'une minute.

L'accueil doit contenir:

1. La promesse centrale.
2. Une vue simple de JARVIS App, Core et Hub.
3. Les six capacités sous forme de choix visuels.
4. Le Laboratoire mobile comme preuve dans le réel.
5. Une seule ouverture vers la Vision.
6. Un appel à discuter du projet.

L'accueil ne doit pas expliquer en détail les permissions, la recherche, la
feuille de route, Personal Intelligence ou Security Pro.

### Solutions

Rôle: aider un visiteur à reconnaître son problème et choisir la bonne capacité.

La page compare les six capacités selon:

- le problème observé;
- le résultat recherché;
- les systèmes typiquement concernés;
- les personnes ou organisations concernées;
- un exemple concret;
- le lien vers la démonstration détaillée.

La page ne doit pas répéter toute l'architecture App, Core et Hub.

### Pages de solution

Rôle: démontrer une capacité à travers une situation réelle et une interface
JARVIS cohérente.

Chaque page suit la même structure:

1. Problème clair.
2. Résultat obtenu.
3. Personnes ou environnements concernés.
4. Démonstration interactive.
5. Sources et systèmes reliés.
6. Permissions et limites propres à cette capacité.
7. Appel à discuter d'un projet semblable.

Chaque page explique seulement ce qui la distingue. Les règles communes
renvoient vers JARVIS ou Confiance.

### JARVIS

Rôle: expliquer le produit commun derrière toutes les solutions.

La page présente:

1. JARVIS App.
2. JARVIS Core.
3. JARVIS Hub.
4. Le parcours d'une demande, de l'intention à la preuve.
5. L'expérience de base avant l'ajout d'une capacité.
6. Le fonctionnement local et l'autonomie.

Les détails complets sur les rôles, permissions et journaux appartiennent à la
page Confiance.

### Laboratoire mobile

Rôle: montrer où les idées sont intégrées et testées dans le monde réel.

La page présente:

1. Le véhicule réel et sa transformation.
2. Les systèmes d'habitation et les systèmes Ford d'origine.
3. Le tableau de bord du véhicule.
4. Les automatisations contextuelles.
5. Les essais, mesures et diagnostics.
6. Les étapes de construction.

La page ne doit pas devenir une seconde page Solutions ou une seconde feuille
de route générale.

### Vision

Rôle: présenter clairement ce que les fondations pourraient permettre plus
tard.

La page contient quatre blocs distincts:

1. JARVIS Multi-Site.
2. Personal Intelligence.
3. Security Pro.
4. Feuille de route.

Chaque bloc possède une promesse, un exemple interactif, sa dépendance aux
fondations et son niveau de maturité. La page ne réexplique pas les six
capacités actuelles.

### Recherche

Rôle: expliquer la méthode de validation.

La page montre comment une hypothèse devient un essai, une mesure, une limite,
une preuve et une prochaine décision. Elle couvre toutes les capacités, pas
seulement le Laboratoire mobile.

### Confiance

Rôle: expliquer les règles communes de gouvernance.

La page possède les informations de référence sur:

- les identités et rôles;
- les permissions de lecture et d'action;
- les approbations humaines;
- les journaux et preuves;
- le fonctionnement local;
- l'accès Internet contrôlé;
- la révocation et les limites.

Les autres pages résument ces règles en une phrase et renvoient ici.

### À propos

Rôle: présenter James, sa démarche et le type de collaborations recherchées.

Cette page ne doit pas devenir un CV exhaustif ni une nouvelle explication de
JARVIS.

### Contact

Rôle: transformer l'intérêt en conversation utile.

Le formulaire demande le contexte, le problème, les systèmes déjà présents et
le type de collaboration. Il confirme clairement comment le message sera
transmis.

## 4. Propriétaire de chaque message

| Sujet | Page propriétaire |
| --- | --- |
| Promesse générale | Accueil |
| Comparaison des six capacités | Solutions |
| App, Core et Hub | JARVIS |
| Rôles, permissions et audit | Confiance |
| Preuve physique et intégration | Laboratoire mobile |
| Méthode d'expérimentation | Recherche |
| Multi-Site, Personal Intelligence et Security Pro | Vision |
| État actuel et prochaines étapes | Vision - Feuille de route |
| Histoire du fondateur et collaborations | À propos |
| Prise de contact | Contact |

## 5. Parcours principaux

### Client potentiel

Accueil → Solutions → Solution concernée → JARVIS → Parler du projet

Le client reconnaît d'abord son problème. Il découvre ensuite la capacité, puis
la fondation commune qui permet de la livrer.

### Investisseur ou accompagnateur

Accueil → JARVIS → Laboratoire mobile → Vision → À propos → Parler du projet

Le visiteur comprend le produit, voit une preuve d'exécution, découvre
l'ambition et rencontre le porteur du projet.

### Partenaire technique ou centre de recherche

Accueil → Laboratoire mobile → Recherche → Vision → Confiance → Parler du projet

Le partenaire voit le terrain, la méthode, les travaux futurs et le cadre de
gouvernance.

## 6. Réduction prévue de l'accueil

Les sections actuelles seront regroupées ainsi:

1. Hero et promesse.
2. JARVIS en une vue: App, Core, Hub et expérience de base.
3. Six capacités.
4. Laboratoire mobile et méthode de preuve dans un seul ensemble.
5. Vision à long terme en un seul aperçu.
6. Appel à discuter.

À déplacer ou réduire:

- les rôles détaillés vont dans Confiance;
- la philosophie devient une courte transition, pas une pleine section;
- Recherche ne possède plus une grande destination indépendante sur l'accueil;
- la Vision n'apparaît qu'une fois;
- les explications techniques détaillées vont dans JARVIS.

## 7. Règles de liaison

- Une page contient au maximum un appel principal et un appel secondaire par
  grande section.
- Un concept détaillé renvoie vers sa page propriétaire au lieu d'être répété.
- Les liens utilisent toujours le même nom pour une même destination.
- La navigation d'une interface JARVIS ne remplace jamais la navigation du site.
- Les sous-menus sont réservés aux pages longues et ne répètent pas un second
  menu à l'intérieur de la démonstration.
- Le pied de page conserve les destinations secondaires: Recherche, Confiance,
  Contact et version anglaise.

## 8. Critère d'approbation de la phase 1

La phase est approuvée lorsque:

1. Le menu principal est compris sans explication.
2. Chaque page possède une seule responsabilité.
3. Les trois parcours mènent naturellement au contact.
4. Recherche et Confiance restent accessibles sans encombrer la navigation.
5. Aucun contenu important n'est supprimé; il est placé au bon endroit.
