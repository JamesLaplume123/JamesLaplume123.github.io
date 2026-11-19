# Ce que JARVIS sait par cœur (fiche de connaissances)
Mise à jour automatique à partir du catalogue du site. Tous les prix sont en dollars canadiens, taxes en sus, et sont des points de départ : chaque soumission est confirmée par écrit, ligne par ligne, avant tout achat. Rien ne se paie sur le site.
## Qui nous sommes
- JARVIS Private Systems : technologies de sécurité et intelligence privée. Nous concevons et installons JARVIS, un système privé qui gère et protège les maisons, les fermes, les entreprises et les véhicules. Fondateur : James Laplume.
- En phase de lancement : nous prenons les noms des personnes intéressées et nous choisissons quelques premiers projets.
- Aucune zone desservie n’est publiée et aucun lieu n’est nommé (ni ville, ni région, ni province). Pour savoir si un projet est possible à un endroit donné, la réponse se donne par la page Contact.
- L’entreprise parle toujours au « nous ». JARVIS, l’assistant, parle au « je » seulement de lui-même.
- Tout tourne chez le client, dans un Hub. Les données restent sur place. Un relais chiffré sert à l’accès de partout et à relier plusieurs lieux; il ne garde rien. En option seulement : une sauvegarde chiffrée et une copie des vidéos hors du lieu.
- JARVIS continue de fonctionner sans Internet (règles, IA locale, caméras, journal). Les mises à jour sont signées, la nuit, avec retour arrière.
- Le logiciel est en construction : le site montre des démonstrations; le premier JARVIS tourne dans le laboratoire mobile (une ambulance convertie). La démo et la visite sont offertes dès maintenant.
## Les pages du site (donner le lien complet quand c’est utile)
- Menu du site : Solutions (les sept, puis Maison, Ferme, Entreprise) · Le logiciel · L’offre · À propos (Laboratoire mobile, Vision, Le Hub, Confiance, Questions, Contact) · bouton doré « Composer mon forfait ».
- Parcours conseillé : voir (accueil, solutions) → tester (le logiciel, la démonstration de chaque solution) → comprendre (l’offre, le Hub, les questions) → composer son forfait (le configurateur), puis « Recevoir ma soumission ».
- Le forfait se bâtit en chemin : « Ajouter à mon forfait » sur chaque page de solution; le compteur de la barre mène au configurateur, où tout est déjà coché.
- https://jarvisprivatesystems.com/ : Accueil
- https://jarvisprivatesystems.com/solutions/ : Les sept solutions
- https://jarvisprivatesystems.com/logiciel/ : Le logiciel en démonstration
- https://jarvisprivatesystems.com/plateforme/ : Le Hub : le boîtier, son IA privée, le noyau
- https://jarvisprivatesystems.com/offre/ : L’offre : trois niveaux tout compris (Base, Signature, Platinum), des options, le projet sur mesure
- https://jarvisprivatesystems.com/offre/#composer : Composer mon JARVIS : pour qui, le lieu, le guide de trois questions, le niveau, les options, le projet, la soumission
- https://jarvisprivatesystems.com/solutions/maison-intelligente-cle-en-main/ : Maison intelligente clé en main
- https://jarvisprivatesystems.com/solutions/domotique-ferme-agricole/ : Domotique pour ferme
- https://jarvisprivatesystems.com/solutions/ia-privee-entreprise/ : IA privée pour entreprise
- https://jarvisprivatesystems.com/a-propos/ : À propos de James
- https://jarvisprivatesystems.com/vision-roadmap/ : Vision et feuille de route
- https://jarvisprivatesystems.com/laboratoire-mobile/ : Laboratoire mobile (ambulance)
- https://jarvisprivatesystems.com/confiance/ : Confiance
- https://jarvisprivatesystems.com/recherche/ : Recherche : la méthode
- https://jarvisprivatesystems.com/questions/ : Questions fréquentes
- https://jarvisprivatesystems.com/contact/ : Contact : démo, visite, soumission
- https://jarvisprivatesystems.com/confidentialite/ : Confidentialité (Loi 25)
- https://jarvisprivatesystems.com/mentions-legales/ : Mentions légales
- https://jarvisprivatesystems.com/plan-du-site/ : Plan du site : toutes les pages
- Chaque solution a sa page : https://jarvisprivatesystems.com/solutions/<nom>/ avec environnements-intelligents, ia-privee-connaissances, securite-intelligente, automatisation-operations, reseau-resilience, diagnostic-care, mobilite
## Pour chez moi, pour mon entreprise, ou les deux
- Le site demande d’abord pour qui : « Pour chez moi », « Pour mon entreprise » ou « Les deux ». Côté « Pour chez moi », il ne montre pas ce qui est propre à l’entreprise.
- Propre à l’entreprise : Automatisation d’entreprise (réceptionniste IA, lignes téléphoniques, automatisations), les services professionnels, les rapports et la base de données du Hub Platinum, et les lieux d’entreprise (bureau ou commerce, atelier, entrepôt ou usine, ferme, garage ou hangar, flotte de véhicules).
- Les six autres solutions servent aux deux publics.
- Un propriétaire d’entreprise a souvent aussi une maison : un seul compte, une seule application, plusieurs lieux personnels et d’entreprise possibles. La soumission se fait ensemble ou séparément pour l’entreprise (au nom de l’entreprise), au choix. Ne donner aucun conseil fiscal.
## Les trois règles de l’offre (à dire simplement)
- 1. Un cerveau par lieu : un lieu reçoit un Hub, un véhicule reçoit un boîtier. JARVIS le choisit selon la taille du lieu.
- 2. Un seul niveau pour tout : Base, Signature ou Platinum s’applique à tous les lieux du client. Il décide des extensions incluses, d’où vit l’IA et du soutien. Le lieu principal porte le niveau; les plus petits s’appuient sur lui.
- 3. L’équipement suit le lieu : chaque type de lieu a son ensemble de départ (boîtier, capteurs). Le reste est sur mesure, et ce qui existe déjà est réutilisé.
- Le client ne décide donc que deux choses : ses lieux et son niveau. Le reste est proposé, puis ajusté.
## Entrer par son lieu : cinq familles (même source que le site : src/lieux.py)
### Chez vous
- Maison : Hub Signature. L’IA tourne dans le Hub, sans Internet, et relie jusqu’à 100 appareils. Solutions qui comptent : Environnements intelligents (Lumières, chauffage et énergie sur un seul écran); Sécurité intelligente (Caméras, portes et alarme dans un seul fil); Réseau et cybersécurité (Un Wi-Fi solide dans toute la maison).
- Condo : Hub Base. Un lieu simple : quelques appareils, une fuite ou une porte à surveiller. Solutions qui comptent : Environnements intelligents (Chauffage et éclairage réglés selon votre journée); Diagnostic & continuité (Une fuite d’eau repérée avant le dégât).
- Chalet : Hub Base. Il veille sur un lieu fermé : gel, fuite, porte, batterie. Solutions qui comptent : Diagnostic & continuité (Gel, fuite, panne : prévenu avant le dégât); Sécurité intelligente (Une porte ouverte ou un mouvement, vous le savez); Environnements intelligents (Le chauffage monté avant votre arrivée).
- Domaine : Hub Platinum. Plusieurs bâtiments, beaucoup de caméras, rien ne doit s’arrêter. Solutions qui comptent : Sécurité intelligente (Caméras, plaques et accès de toute la propriété); Environnements intelligents (Maison, garage et dépendances sur un seul écran); Réseau et cybersécurité (Un réseau qui relie chaque bâtiment); Diagnostic & continuité (Eau, énergie et équipements suivis jour après jour).
### Votre entreprise
- Bureau ou commerce : Hub Signature. Réceptionniste IA et jusqu’à dix automatisations, traitées sur place. Solutions qui comptent : Automatisation d’entreprise (La réception ne manque plus un appel); IA privée et connaissances (Vos documents répondent aux questions de l’équipe); Réseau et cybersécurité (Un réseau séparé pour les clients, les postes et les caméras).
- Atelier, entrepôt ou usine : Hub Signature. Accès, caméras et machines suivis au même endroit. Solutions qui comptent : Sécurité intelligente (Qui entre, quand, et par quelle porte); Diagnostic & continuité (Une machine qui dérive se voit avant le bris); Réseau et cybersécurité (Un réseau séparé pour les machines); Automatisation d’entreprise (Commandes et bons qui circulent sans ressaisie).
- Ferme : Hub Platinum. Des bâtiments et des animaux qui ne peuvent pas attendre : batterie et Internet de secours. Solutions qui comptent : Diagnostic & continuité (Température, courant, eau : l’alerte avant la perte); Environnements intelligents (Tous les bâtiments sur un seul écran); Réseau et cybersécurité (Internet dans chaque bâtiment); Sécurité intelligente (Portes, barrières et visiteurs).
- Garage ou hangar : Hub Signature. Des biens de valeur : caméras analysées sur place, accès contrôlés. Solutions qui comptent : Sécurité intelligente (Chaque entrée et chaque sortie, avec l’image); Environnements intelligents (Portes, humidité et température du bâtiment); Diagnostic & continuité (Batteries et équipements suivis).
### Lieux mobiles
- VR : Hub Signature + Boîtier VR. Une maison qui roule : le Hub et le Boîtier VR gèrent batteries, eau, chauffage et sécurité. Solutions qui comptent : Environnements intelligents (Batteries, eau, chauffage et lumières à bord); Mobilité (Un copilote qui propose le bon arrêt); Sécurité intelligente (Le véhicule surveillé quand vous êtes ailleurs); Diagnostic & continuité (Une batterie ou une pompe qui faiblit se voit tôt).
- Roulotte : Hub Base + Boîtier VR. Batteries, réservoirs, gel et porte : l’essentiel d’un petit lieu mobile. Solutions qui comptent : Environnements intelligents (Batteries et réservoirs d’un coup d’œil); Diagnostic & continuité (Le gel et les fuites signalés); Mobilité (Le trajet et les arrêts gardés sur la carte).
- Bateau ou yacht : Hub Base + Boîtier VR. À quai comme en route : énergie, cale et accès surveillés. Solutions qui comptent : Environnements intelligents (Énergie, réservoirs et confort à bord); Diagnostic & continuité (Pompe de cale et batteries suivies); Sécurité intelligente (Une présence à bord, vous le savez).
### Véhicules
- Auto ou camion : Boîtier Mobilité. Aucun Hub à bord : le Boîtier Mobilité donne la position, le diagnostic et l’antivol. Solutions qui comptent : Mobilité (Position, diagnostic et antivol, de partout).
- Moto : Boîtier Mobilité. Aucun Hub à bord : le Boîtier Mobilité suffit. Solutions qui comptent : Mobilité (Position et antivol, de partout).
- Flotte de véhicules : Boîtier Mobilité. Un Boîtier Mobilité par véhicule : position, diagnostic et antivol pour toute la flotte. Solutions qui comptent : Mobilité (Chaque véhicule, son état et ses trajets au même endroit); Diagnostic & continuité (L’entretien prévu avant la panne).
### Aérien
- Avion ou hélicoptère : Boîtier Mobilité. Suivi au sol par son boîtier : position, batterie, alertes. Le hangar, lui, reçoit un Hub. JARVIS ne touche jamais à l’avionique. Solutions qui comptent : Mobilité (L’appareil, sa position et son état au sol, au même endroit).
- Un lieu mobile (VR, roulotte, bateau, yacht) se traite comme une maison qui roule : Hub et Boîtier VR. Un véhicule (auto, camion, moto) ou un appareil (avion, hélicoptère) reçoit un Boîtier Mobilité, sans Hub à bord. Une flotte : un boîtier par véhicule, le tableau de la flotte au bureau.
- Aérien : suivi au sol seulement (position, batterie, alertes, hangar). JARVIS ne touche jamais aux commandes ni à l’avionique.
## L’offre : trois niveaux tout compris (même source que la page L’offre)
- Le client choisit un niveau : Base, Signature ou Platinum. Le niveau dit ce que JARVIS fait et le soutien inclus. Chaque niveau comprend tout le précédent.
- Base : lumières, chauffage, serrures et énergie; alertes : fuites, pannes, entretien; l’app JARVIS, de partout; soutien par courriel. Solutions incluses : Environnements intelligents, Diagnostic & continuité.
- Signature : Tout Base, plus : caméras qui comprennent ce qu’elles voient; une IA privée qui reste chez vous; assistant vocal et réceptionniste; soutien par courriel et téléphone. Solutions incluses : Environnements intelligents, Diagnostic & continuité, Sécurité intelligente, IA privée et connaissances.
- Platinum : Tout Signature, plus : réseau et cybersécurité; plusieurs lieux reliés, sans limite; batterie et Internet de secours; soutien prioritaire, une personne dédiée. Solutions incluses : Environnements intelligents, Diagnostic & continuité, Sécurité intelligente, IA privée et connaissances, Réseau et cybersécurité.
- Le projet (le matériel du lieu et l’installation) est sur mesure : chaque lieu est différent. On réutilise ce qui existe déjà (Victron, UniFi, caméras ONVIF, NAS, Starlink).
- Les options s’ajoutent au mois, annulables en tout temps : ce qui n’est pas déjà dans le niveau (par exemple Mobilité pour un véhicule, ou l’Entreprise).
- La page L’offre se fait en trois étapes : 1) vos lieux (l’écosystème se dessine, un cerveau par lieu), 2) votre niveau (trois questions conseillent si on hésite), 3) votre projet (extensions, ensemble de départ de chaque lieu, données, installation), puis « Recevoir ma soumission ».
- Où vit l’IA : Base : L’IA passe par Internet, avec votre accord. Signature : L’IA tourne dans votre Hub, même sans Internet. Platinum : IA renforcée, 100 % chez vous : elle continue pendant une panne.
- Extensions : cinq viennent avec le niveau (Base 2, Signature 4, Platinum 5). Mobilité s’ajoute avec chaque véhicule. Entreprise s’ajoute pour un lieu d’entreprise, dès le niveau Signature.
- Règle simple : un Hub plus puissant peut toujours faire un niveau plus bas, jamais l’inverse.
## Monter ou descendre de niveau
- Monter : si le Hub suffit, on active le niveau à distance, le jour même. S’il faut plus de puissance, on échange le Hub avec un crédit; la configuration est restaurée telle quelle.
- Un autre lieu : l’ancien Hub part au chalet ou dans le VR, relié au nouveau.
- Redescendre : le client garde son Hub; on retire des fonctions et il paie moins.
- Le matériel installé reste toujours. Rien ne se perd.
## Bâtir son écosystème (plusieurs lieux, une seule app)
- Un écosystème JARVIS, c’est tous les lieux d’une personne ou d’une entreprise reliés : maison, chalet, VR, bateau, garage, bureau, ferme, et les véhicules.
- Méthode à proposer, une question à la fois : 1) quels sont vos lieux; 2) lequel est le principal (il reçoit le plus gros Hub, qui prête son IA aux autres); 3) pour chaque autre lieu, un Hub plus petit suffit souvent; 4) les véhicules reçoivent un Boîtier Mobilité, sans Hub; 5) une seule app et un seul compte pour tout, une soumission pour l’ensemble.
- Les lieux se parlent par un lien privé et chiffré. Si Internet tombe, chaque lieu continue seul.
## Le nuage : seulement ce qui est utile
- Tout tourne chez le client. La sauvegarde chiffrée est incluse (illisible pour nous). L’accès de partout passe par un relais chiffré qui ne garde rien. En option seulement, et sur accord explicite : une copie chiffrée des vidéos hors du lieu (au cas où le Hub serait volé ou détruit) et un renfort d’IA par le nuage pour les grosses tâches.
## Quel Hub pour quel niveau (en mots de tous les jours)
- Hub Base — Un petit lieu à surveiller (Chalet, condo, petit VR). Savoir que tout va bien, et agir à distance. Vous pouvez : être prévenu d’une fuite, du gel ou d’une porte ouverte; régler le chauffage et les lumières de partout; voir jusqu’à deux caméras. À savoir : L’assistant passe par Internet. Idéal comme deuxième lieu, relié à votre maison.
- Hub Signature — La maison où vous vivez (Maison, VR complet, petite entreprise). Tout le lieu, et une IA qui reste chez vous. Vous pouvez : tout gérer dans une seule application; parler à JARVIS, même sans Internet; relier jusqu’à trois lieux : maison, chalet, VR. À savoir : Jusqu’à six caméras analysées.
- Hub Platinum — Un lieu qui ne doit jamais s’arrêter (Domaine, ferme, entreprise). Plusieurs bâtiments, beaucoup de caméras, aucune coupure. Vous pouvez : continuer pendant une panne de courant ou d’Internet; suivre tous vos bâtiments et vos lieux, sans limite; recevoir des rapports et automatiser le travail. À savoir : Pensé pour les grands lieux : trop pour une maison ordinaire.
- Pour aider quelqu’un qui hésite, poser les trois questions de la page L’offre : combien de caméras; l’intelligence doit-elle rester chez vous, même sans Internet; une coupure serait-elle grave. Platinum si une coupure serait grave ou 7 caméras et plus; Signature si l’IA doit rester chez soi ou 3 à 6 caméras; sinon Base.
## Les trois Hubs
### Hub Base. Pour : Chalet, condo, petit VR.
- Pour veiller sur un lieu simple : fuite, gel, porte, batterie. L’IA passe par Internet. A : Jusqu’à 30 appareils; 2 caméras analysées, 7 jours d’enregistrement; IA par Internet seulement; Wi-Fi, Bluetooth, Zigbee; Garantie 1 an, soutien par courriel. Manque : Pas d’IA dans le Hub; Pas d’assistant vocal ni de réceptionniste; Pas d’automatisations d’entreprise; Pas de batterie de secours.
### Hub Signature. Pour : Maison, VR complet, PME.
- L’IA tourne chez vous, sans Internet : assistant vocal, caméras analysées sur place, réceptionniste. A : Jusqu’à 100 appareils; 6 caméras analysées, 30 jours d’enregistrement; IA locale, dans le Hub; Assistant vocal « Jarvis » et réceptionniste IA; Z-Wave et Matter, 3 lieux reliés; Garantie 2 ans, soutien téléphone. Manque : Pas de base de données ni de rapports; Pas de batterie de secours; Automatisations limitées à 10.
### Hub Platinum. Pour : Domaine, entreprise, ferme.
- Pour un lieu qui ne doit jamais s’arrêter : carte IA dédiée, batterie, Internet de secours, rapports. A : Appareils illimités; 16 caméras et plus, 90 jours d’enregistrement; IA forte, 100 % locale, carte IA dédiée; Base de données, rapports, automatisations illimitées; Batterie interne 2 h, Internet de secours intégré; Hub principal de tous vos lieux; Garantie 3 ans, remplacement express, personne dédiée.
### Comparatif précis (Base | Signature | Platinum)
- Appareils reliés : 30 | 100 | Illimité
- Caméras analysées par l’IA : 2 | 6 | 16 et plus
- Enregistrement vidéo : 7 jours | 30 jours | 90 jours et plus
- IA privée : Par Internet seulement | Locale, dans le Hub | Forte, 100 % locale
- Assistant vocal « Jarvis » : non | Oui | Oui, plusieurs pièces
- Réceptionniste IA : non | Oui | Oui, plusieurs lignes
- Automatisations d’entreprise : non | Jusqu’à 10 | Illimitées
- Base de données et rapports : non | non | Oui
- Lieux reliés (multi-Hubs) : Suit un Hub principal | Jusqu’à 3 | Illimité
- Dans chaque Hub : Environnements intelligents, l’app JARVIS, les comptes et droits, les mises à jour signées, les sauvegardes chiffrées.
## Les solutions (incluses selon le niveau, ou en option au mois)
- Environnements intelligents : incluse avec chaque Hub. Inclus avec chaque Hub : c’est la base de JARVIS.
- Diagnostic & continuité. Un dégât d’eau coûte en moyenne. Ici, vous êtes prévenu à la première goutte.
- Sécurité intelligente. Vos caméras comprennent ce qu’elles voient. Une alerte utile, pas cent notifications.
- IA privée et connaissances. Posez une question sur votre lieu ou vos documents. La réponse ne sort jamais de chez vous.
- Réseau et cybersécurité. Un appareil inconnu sur votre réseau est bloqué avant de faire des dégâts.
- Mobilité par véhicule. Position, diagnostic et antivol de chaque véhicule. Les données cellulaires sont comprises.
- Chaque solution payante inclut l’accès de partout et les alertes sur le téléphone. Sans solution payante, JARVIS fonctionne quand même chez le client, sur place.
## Pour une entreprise (à la carte, par mois; demande un Hub Signature ou Platinum)
- Socle Entreprise, obligatoire pour toute automatisation. Comptes employés, journal de tout ce que JARVIS fait, rapport hebdomadaire, connexions à vos outils (courriel, texto, calendrier, comptabilité). 300 textos par mois compris.
- Réceptionniste IA par ligne. Répond 24/7 à votre nom, prend les messages et les rendez-vous, transfère les urgences. 300 minutes par ligne comprises.
- Toutes les automatisations. Toute la bibliothèque, activée au besoin. Hub Platinum recommandé.
- Automatisation sur mesure. Vous décrivez le besoin, nous la construisons et la testons.,.
- Au-delà : minute d’appel · texto · ligne supplémentaire = une réceptionniste de plus.
- Prix des automatisations (un déclencheur, une action) (reliée à un outil du client) (veille 24/7 avec escalade). Hub Signature : jusqu’à 10 automatisations; Platinum : illimité.
### Bibliothèque d’automatisations
- Réception : Prendre et confirmer un rendez-vous; Texter le rappel la veille; Transférer un appel urgent au bon employé; Répondre aux questions fréquentes; Prendre les messages et vous les résumer.
- Ventes : Envoyer une soumission à partir d’un gabarit; Relancer une soumission sans réponse après 3 jours; Créer la fiche client; Prévenir le vendeur quand un client rappelle.
- Facturation : Relancer une facture impayée (7, 14, 30 jours); Envoyer le reçu après paiement; Comptes à recevoir chaque lundi.
- Opérations : Créer un bon de travail à partir d’une demande; Assigner au technicien disponible; Escalader à la personne de garde; Alerte si un équipement critique tombe.
- Direction : Rapport du matin : appels, ventes, alertes; Résumé de la semaine le vendredi; Approbation par texto : « OK » ou « Non ».
- Ferme et commerce : Alerte de température : frigo, réservoir à lait, étable; Journal automatique des livraisons; Commande de moulée quand le silo est bas; Alerte si une porte reste ouverte; Veille d’une pompe ou d’un abreuvoir.
## Le matériel (payé une fois, prêt à brancher)
- Boîtiers JARVIS : Boîtier VR Base; Boîtier VR Signature; Boîtier VR Platinum; Boîtier Mobilité; Écran JARVIS 10 po; Écran JARVIS 7 po; Boîtier Secours.
- Capteurs : Fuite d’eau; Vanne d’eau automatique; Température et humidité; Porte et fenêtre; Présence (radar); Fumée et CO; Propane; Niveau de réservoir; Pression des pneus (4); Compteur d’énergie; Capteur universel.
- Caméras et accès : Caméra extérieure; Caméra intérieure; Caméra 360° (dôme); Sonnette vidéo; Lecteur de plaques; Serrure intelligente; Clavier et lecteur de badges; Interphone vidéo; Sirène et stroboscope; Bouton d’urgence.
- Confort et réseau : Thermostat intelligent; Interrupteur ou gradateur; Prise intelligente; Ampoule couleur; Bande DEL (2 m); Moteur de store; Relais foyer ou garage; Switch PoE 8 ports; Routeur 4G/5G; Starlink Mini; Téléphone IP.
- Les caméras s’enregistrent dans le Hub, jamais dans le nuage. Le Boîtier VR va dans un VR, une roulotte ou un bateau; le Boîtier Mobilité dans une voiture ou un camion. Le Hub Base n’a pas d’IA locale : les caméras y sont analysées par Internet.
## Ouvrir un plan tout composé (un seul lien)
- Adresse : https://jarvisprivatesystems.com/offre/?lieux=<lieux>&niveau=<niveau>&ens=tout#composer. La page s’ouvre avec l’écosystème dessiné, le niveau choisi et l’ensemble de départ de chaque lieu ajouté. Le visiteur ajuste, puis demande sa soumission.
- lieux : identifiants séparés par des virgules, parmi : maison (Maison), condo (Condo), chalet (Chalet), domaine (Domaine), bureau (Bureau ou commerce), atelier (Atelier, entrepôt ou usine), ferme (Ferme), garage (Garage ou hangar), vr (VR), roulotte (Roulotte), bateau (Bateau ou yacht), auto (Auto ou camion), moto (Moto), flotte (Flotte de véhicules), avion (Avion ou hélicoptère).
- niveau : base, signature ou platinum. Sans niveau, la page prend le niveau conseillé pour ces lieux.
- Exemple : maison, chalet et une auto, niveau Signature : https://jarvisprivatesystems.com/offre/?lieux=maison,chalet,auto&niveau=signature&ens=tout#composer
- Un lieu ne se met qu’une fois dans le lien; le nombre de véhicules ou de pièces s’ajuste sur la page.
## Les ensembles de départ (un par lieu, ajustables pièce par pièce)
- Maison : 3 × Fuite d’eau, 1 × Vanne d’eau automatique, 3 × Porte et fenêtre, 2 × Présence (radar), 1 × Sonnette vidéo, 1 × Thermostat intelligent. L’eau coupée toute seule, la sonnette qui reconnaît, le chauffage par pièce.
- Condo : 2 × Fuite d’eau, 1 × Porte et fenêtre, 1 × Présence (radar), 1 × Thermostat intelligent. L’essentiel d’un condo : l’eau, la porte, le chauffage.
- Chalet : 3 × Température et humidité, 2 × Fuite d’eau, 2 × Porte et fenêtre, 1 × Routeur 4G/5G, 1 × Prise intelligente. Gel, fuite, intrusion : prévenu avant que le plancher lève au printemps.
- Domaine : 6 × Caméra extérieure, 1 × Lecteur de plaques, 2 × Serrure intelligente, 1 × Interphone vidéo, 4 × Fuite d’eau, 1 × Vanne d’eau automatique, 1 × Switch PoE 8 ports, 1 × Boîtier Secours, 1 × Écran JARVIS 10 po. Caméras, plaques, serrures, eau et secours : rien n’entre, rien ne coule, rien ne s’arrête.
- Bureau ou commerce : 2 × Téléphone IP, 2 × Caméra extérieure, 1 × Caméra intérieure, 1 × Switch PoE 8 ports, 1 × Clavier et lecteur de badges, réceptionniste IA, 3 automatisations pour commencer. Une réceptionniste qui ne manque aucun appel, et trois automatisations pour commencer.
- Atelier, entrepôt ou usine : 2 × Caméra extérieure, 1 × Caméra 360° (dôme), 1 × Clavier et lecteur de badges, 2 × Porte et fenêtre, 2 × Capteur universel, 1 × Switch PoE 8 ports. Qui entre et par quelle porte; une machine qui dérive se voit avant le bris.
- Ferme : 1 × Routeur 4G/5G, 4 × Caméra extérieure, 6 × Température et humidité, 4 × Capteur universel, 1 × Boîtier Secours, 1 × Compteur d’énergie, 3 automatisations pour commencer. Frigo, réservoir à lait, pompes, silo : les alertes qui sauvent une récolte ou un troupeau.
- Garage ou hangar : 2 × Caméra extérieure, 1 × Clavier et lecteur de badges, 2 × Porte et fenêtre, 1 × Température et humidité, 1 × Switch PoE 8 ports. Chaque entrée avec l’image; l’humidité et la température du bâtiment suivies.
- VR : 1 × Boîtier VR (celui du niveau), 4 × Température et humidité, 2 × Porte et fenêtre, 1 × Fuite d’eau, 1 × Propane, 1 × Caméra intérieure, 1 × Écran JARVIS 7 po. Le VR au complet dans la poche : batteries, réservoirs, propane, caméra et écran à bord.
- Roulotte : 1 × Boîtier VR (celui du niveau), 2 × Température et humidité, 1 × Porte et fenêtre, 1 × Fuite d’eau. Batteries, réservoirs, gel et porte : les quatre choses qui gâchent un voyage.
- Bateau ou yacht : 1 × Boîtier VR (celui du niveau), 2 × Température et humidité, 1 × Porte et fenêtre, 1 × Fuite d’eau. Batteries, cale et accès : l’essentiel, à quai comme en route.
- Auto ou camion : 1 × Boîtier Mobilité. Position, diagnostic et antivol, sans Hub à bord.
- Moto : 1 × Boîtier Mobilité. Position et antivol, sans Hub à bord.
- Flotte de véhicules : 2 × Boîtier Mobilité. Un boîtier par véhicule : ajustez le nombre à votre flotte.
- Avion ou hélicoptère : 1 × Boîtier Mobilité. Suivi au sol : position, batterie et alertes. Jamais l’avionique.
- Ce sont des points de départ proposés à l’étape 3 de la page L’offre. Le Boîtier VR suit le niveau choisi.
## Services professionnels (payés une fois)
- Vérifier · Vérification de vos systèmes (résidence). Caméras, accès, réseau, Wi-Fi, sauvegardes, habitudes : le tour complet de la maison ou du chalet. Rapport écrit avec priorités.
- Vérifier · Vérification de vos systèmes (entreprise). Accès, caméras, réseau, postes, sauvegardes, comptes employés. Rapport pour la direction et plan sur 90 jours.
- Vérifier · Test d’intrusion réseau. Attaque autorisée de votre réseau et de vos services, puis correction avec vous. Rapport et nouvelle vérification.
- Vérifier · Revue de votre exposition en ligne. Ce qu’Internet dit de vous et de votre entreprise, à partir de sources publiques. Rapport et nettoyage.
- Protéger · Accompagnement Loi 25. Registre, politiques, incidents, consentements : votre entreprise conforme, avec JARVIS comme preuve.
- Protéger · Mise à niveau du réseau. Zones séparées, mots de passe, mises à jour, sauvegardes testées, caméras isolées. Une journée, puis vérification.
- Former · Formation d’équipe (demi-journée). Vos employés apprennent JARVIS, la réceptionniste et les bons réflexes : hameçonnage, mots de passe, accès.
- Former · Prise en main à la maison (2 h). Toute la famille apprend JARVIS : scènes, alertes, caméras, codes invités.
- Nous vérifions et protégeons des systèmes; nous ne sommes pas une agence de gardiennage ni d’enquête.
### Entretien et veille (entreprise, par mois)
- Entretien et veille PME. Mises à jour vérifiées, surveillance du réseau et des caméras, rapport mensuel, 2 heures de soutien par mois, réponse le jour ouvrable suivant.
- Entretien et veille Pro. PME + réponse en 4 heures, 6 heures de soutien par mois, revue trimestrielle sur place, personne dédiée.
## Installation
- Je l’installe moi-même : Inclus. Prises identifiées, aucun fil à couper. Plan, vidéo et mise en service à distance (30 min).
- Mise en service guidée. Un technicien vous accompagne en vidéo pendant l’installation.
- JARVIS s’en occupe :. Sur place, minimum 3 h. Déplacement en sus. Le panier compte 3 h.
- Visite de planification : Gratuite. Domaine, entreprise, ferme : inventaire, plan écrit, soumission ligne par ligne.
- Toujours inclus : Configuration pour votre lieu (Vos appareils déjà jumelés, vos scènes de base prêtes); Test d’une heure (Chaque kit tourne une heure sur banc avant l’envoi); Mises à jour automatiques (Signées, la nuit, avec retour arrière); Sauvegarde chiffrée (Si le Hub brise, le nouveau repart comme avant); Garantie (1 an Base, 2 ans Signature, 3 ans Platinum. Garantie légale en plus); Retour 30 jours (Matériel non installé : remboursé, moins la configuration).
## Plusieurs lieux
- Un Hub par lieu (maison, chalet, VR, bateau, entreprise, ferme, garage, hangar). Les lieux se parlent par un lien privé et chiffré; les petits lieux empruntent l’IA du plus gros Hub. Les solutions sont à −30 % dès le deuxième lieu; l’Entreprise et le matériel ne sont pas réduits.
- Un Hub Base suit un Hub principal; un Signature relie jusqu’à 3 lieux; un Platinum, sans limite.
## Chiffres utiles (sources : Bureau d’assurance du Canada, Chubb)
- 47 % des réclamations d’assurance habitation sont des dégâts d’eau en moyenne. Seulement 9 % des gens ont un système qui détecte les fuites. Diagnostic & continuité coûte; un capteur de fuite; la vanne d’eau automatique.
## Ce qu’on ne promet pas
- Pas de téléphone à donner : le contact passe par la page Contact. Pas de délai de livraison précis. Pas de « sans engagement » : les solutions sont annulables en tout temps, le matériel non installé est remboursable 30 jours, moins la configuration.
- Les capacités des Hubs sont des repères; elles dépendent aussi des caméras et des solutions actives. Les prix sont confirmés par écrit avant tout achat.