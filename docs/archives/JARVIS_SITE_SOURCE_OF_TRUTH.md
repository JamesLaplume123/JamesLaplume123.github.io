# JARVIS - Source de verite du site

Statut: reference de travail a faire approuver avant la refonte visuelle.

Ce document fixe l'architecture, les noms et les frontieres du projet. Toute
nouvelle page, interface ou correction doit respecter ces regles. Une demande
intermediaire peut enrichir une partie du site, mais ne doit pas modifier cette
architecture sans decision explicite.

## 1. Message central

JARVIS relie les informations, les logiciels, les appareils et les lieux deja
utilises afin de comprendre le contexte, proposer une action et agir selon des
permissions claires.

Promesse courte:

> Relier ce qui existe. Faire agir l'ensemble.

Principe:

> Une seule intelligence privee, plusieurs capacites, toujours sous le controle
> de la personne ou de l'organisation.

## 2. Architecture produit

### JARVIS Private Systems

La marque et le studio qui portent la vision, la recherche appliquee, les
projets pilotes et le developpement du produit. James Laplume en est le fondateur.

### JARVIS

L'ecosysteme et le produit complet. JARVIS n'est ni une simple application de
conversation, ni une box domotique, ni une collection de six logiciels.

### JARVIS App

L'interface utilisateur sur les ecrans autorises: ordinateur, tablette,
telephone ou ecran integre. Elle permet de comprendre, demander, approuver,
controler et consulter les preuves.

### JARVIS Core

Le logiciel central: intelligence, agents specialises, memoire autorisee,
contexte, permissions, evenements, automatisations, orchestration et journal
d'audit.

### JARVIS Hub

L'infrastructure physique locale qui execute JARVIS Core et les services du
site. Le Hub est un equipement professionnel integre au projet. Le mot "Box"
n'est pas utilise dans le marketing public.

### JARVIS Multi-Site

La vision a long terme qui coordonne plusieurs environnements autonomes. Fabric
est le nom technique de la couche de liaison; ce n'est pas un produit public
separe.

## 3. Une plateforme, six capacites

Le menu public peut employer le mot "Solutions", plus naturel pour un client.
Dans l'architecture produit, ce sont six capacites du meme JARVIS.

### 1. Environnements intelligents

Relier et controler les systemes physiques d'un lieu: eclairage, climat,
energie, acces, audio-video, appareils, scenes et confort.

Question client: "Comment faire fonctionner mon lieu comme un seul systeme?"

### 2. IA privee et connaissances

Converser avec des informations autorisees, retrouver des documents, photos,
messages, liens et preuves, puis preparer une reponse avec ses sources.

Question client: "Comment retrouver et comprendre ce que mon organisation ou
ma vie numerique sait deja?"

Cette capacite comprend et retrouve. Elle ne remplace pas l'automatisation des
operations.

### 3. Securite intelligente

Relier cameras, acces, alarmes, identites, appareils et evenements afin de
presenter une situation comprehensible et une action proportionnee.

Question client: "Que se passe-t-il autour de mon site et est-ce important?"

Cette capacite protege un environnement. Elle est distincte de Security Pro,
qui concerne des mandats specialises et explicitement autorises.

### 4. Automatisation d'entreprise

Faire circuler les demandes, documents, validations et actions entre les outils
existants: courriel, CRM, calendrier, comptabilite, RH et operations.

Question client: "Comment enlever le travail repetitif entre mes logiciels sans
perdre le controle?"

Cette capacite fait avancer un processus. IA privee et connaissances lui fournit
du contexte, mais ne constitue pas le processus lui-meme.

### 5. Reseau et cybersecurite

Administrer et surveiller l'infrastructure: topologie, identite des appareils,
Wi-Fi, segmentation, disponibilite, changements, acces et renforcement.

Question client: "Mon infrastructure fonctionne-t-elle correctement et est-elle
administree de facon sure?"

Cette capacite observe et administre le reseau. Elle ne diagnostique pas a elle
seule tous les systemes du lieu.

### 6. Diagnostic et continuite

Partir d'un symptome, rassembler l'historique et les mesures, tester les causes
dans le bon ordre, tenter une recuperation autorisee et produire un rapport.

Question client: "Pourquoi quelque chose ne fonctionne plus et comment le
remettre en service avec des preuves?"

Cette capacite peut traverser le reseau, la domotique, l'energie, un vehicule ou
un service logiciel. Elle repare et explique; elle ne relie pas plusieurs sites.

## 4. Environnements

Les capacites peuvent etre configurees dans plusieurs contextes sans devenir de
nouvelles marques:

- Residence: maison, condo, propriete ou chalet.
- Entreprise: bureau, commerce, atelier, hotel ou equipe terrain.
- Mobilite: vehicule amenage, VR, van ou unite specialisee.
- Multi-Site: coordination future de plusieurs environnements autonomes.

Un utilisateur voit un seul JARVIS. Des agents specialises peuvent travailler
en arriere-plan, mais ne deviennent pas chacun un produit ou une identite.

## 5. Projets et visions

### Laboratoire mobile JARVIS

La Ford 2017 V10 est le premier grand terrain de preuve physique. Elle sert a
tester l'energie, le reseau, le confort, la securite, l'automatisation et le
diagnostic dans des conditions reelles. Ce n'est pas une septieme solution.

### Recherche appliquee

La methode qui transforme une idee en hypothese, essai, observation, preuve,
limite et prochaine decision. Elle couvre les six capacites et le laboratoire.

### Personal Intelligence

Vision a long terme d'un accompagnement contextuel volontaire. JARVIS relie les
applications, appareils et objectifs deja choisis par la personne; il ne recree
pas Garmin, Apple Sante, Runna, les calendriers ou les methodes de formation.

### Security Pro

Vision specialisee pour des mandats ecrits et autorises: OSINT, investigation,
surface d'attaque, audit, hardening, SIEM/EDR et pentest. Elle demeure separee
de la securite quotidienne d'un lieu.

## 6. Gouvernance commune

Toutes les capacites respectent les memes regles:

1. Identite connue et role explicite.
2. Sources et systemes autorises visibles.
3. Permission distincte pour lire, proposer, modifier et communiquer.
4. Approbation humaine pour les actions sensibles.
5. Journal des sources, decisions, actions et resultats.
6. Fonctionnement local prioritaire et Internet seulement lorsqu'il est permis.
7. Possibilite de retirer une permission ou de desactiver une automatisation.

L'assistant peut traverser les six capacites. Son pouvoir depend toujours du
profil actif, du site, de la mission et de la permission accordee.

## 7. Noms a utiliser

- JARVIS Private Systems
- JARVIS
- JARVIS App
- JARVIS Core
- JARVIS Hub
- JARVIS Multi-Site - propulse par Fabric
- Laboratoire mobile JARVIS
- Environnements intelligents
- IA privee et connaissances
- Securite intelligente
- Automatisation d'entreprise
- Reseau et cybersecurite
- Diagnostic et continuite
- Personal Intelligence
- Security Pro

## 8. Noms a retirer des interfaces publiques

- Box JARVIS
- Ambulance Lab
- JARVIS Knowledge
- JARVIS Enterprise
- JARVIS Network
- JARVIS Personal
- JARVIS Everywhere
- JARVIS Care employe comme produit separe

Dans une interface, employer plutot "JARVIS" puis le contexte actif, par
exemple "Residence", "Entreprise", "Securite" ou "Diagnostic".

## 9. Niveaux de maturite

Chaque page utilise un seul statut principal, affiche une seule fois pres de la
demonstration:

- Reel: element physique existant ou mesure verifiable.
- En construction: travail technique actuellement entrepris.
- Prototype interactif: experience fonctionnelle avec donnees simulees.
- Projet pilote: essai limite avec objectif et perimetre definis.
- Vision a long terme: direction future, non presentee comme produit termine.

Ne jamais inventer de client, certification, resultat commercial, integration
terminee ou capacite deja disponible.

## 10. Test de clarte

Une personne doit pouvoir resumer le projet ainsi:

> JARVIS est une intelligence privee qui fonctionne pres de vos systemes. Son
> application vous permet de parler a vos informations, comprendre vos lieux et
> superviser des actions. Les memes fondations peuvent soutenir six capacites,
> d'abord dans un environnement, puis un jour entre plusieurs sites.

Si une page, un nom ou une interface contredit ce resume, la correction doit
etre revue avant d'etre generalisee ou mise en ligne.
