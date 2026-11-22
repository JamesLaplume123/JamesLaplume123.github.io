# L'offre JARVIS : les règles

Source de vérité de l'offre (19 novembre 2026). La page `/offre/`, la fiche de connaissances de
JARVIS (`assets/guide/connaissances.md`) et le tiroir « Mon forfait » suivent ces règles. Si une
règle change, on change ce document d'abord, puis le code.

Aucun prix ici. Les prix vivent dans `src/pages/catalogue.py` et restent cachés tant que
`SITE["prix_publics"]` est faux.

## Les trois règles

1. **Un cerveau par lieu.** Un lieu (fixe ou habitable) reçoit un appareil JARVIS. Un véhicule reçoit un
   boîtier, rien d'autre à bord. JARVIS choisit le cerveau selon la taille du lieu.
2. **Un seul niveau pour tout.** Base, Signature ou Platinum s'applique à tous les lieux du client.
   Le niveau décide des extensions incluses, d'où vit l'IA et du soutien.
3. **L'équipement suit le lieu.** Chaque type de lieu a son ensemble de départ (boîtier, capteurs).
   Le reste est sur mesure; ce qui existe déjà chez le client est réutilisé.

Conséquence : **le client ne décide que deux choses, ses lieux et son niveau.** Tout le reste est
proposé par JARVIS, puis ajusté.

## Ce qui se déduit, et comment

| Chose | Règle | Où c'est écrit |
|---|---|---|
| Le cerveau d'un lieu | Appareil conseillé du lieu; le lieu principal (le plus gros appareil conseillé) porte le niveau; aucun autre appareil ne dépasse le niveau | `cerveaux()` dans `assets/js/wow.js` et dans `src/lieux.py` |
| Le Boîtier VR | Lieux mobiles (VR, roulotte, bateau) : il suit le niveau (Base, Signature, Platinum) | `BOITIER_VR` dans `assets/demos/catalogue.js` |
| Les extensions incluses | Base : 2 · Signature : 4 · Platinum : 5 | `NIVEAUX` dans `src/pages/catalogue.py` |
| Mobilité | S'ajoute avec chaque véhicule (une par véhicule) | `catalogue.js`, familles `vehicules` et `aerien` |
| Entreprise | Proposée dès qu'il y a un lieu d'entreprise; demande Signature ou Platinum | `data-public="entreprise"`, « À prévoir » |
| Où vit l'IA | Base : par Internet, avec accord · Signature : dans l'appareil · Platinum : dans l'appareil, renforcée | `NIVEAUX[...]["ia"]` |
| L'équipement proposé | Un ensemble de départ par lieu, ajouté d'un geste | `ENSEMBLES` dans `src/pages/catalogue.py` |
| Pour qui (particulier, entreprise) | Déduit des lieux choisis; il n'y a plus de question « pour qui » | `basculeLieu()` dans `wow.js` |

## Les pièces de l'offre, et leur place

- **Les lieux** : cinq familles, quinze lieux (`src/lieux.py`). Chez vous · Votre entreprise ·
  Lieux mobiles · Véhicules · Aérien.
- **Les appareils** : JARVIS Mini, JARVIS, JARVIS Pro (`HUBS`, fiche technique `COMPARE`; dans le
  code, la clé reste `base`, `signature`, `platinum`). Ils ne portent plus le nom des niveaux
  (décision de James, 19 novembre 2026) : le client choisit un niveau, JARVIS choisit l'appareil.
  Un appareil plus puissant peut toujours faire un niveau plus bas, jamais l'inverse.
- **Les niveaux** : Base, Signature, Platinum (`NIVEAUX`). Chacun comprend le précédent.
- **Les sept extensions** : Environnements, Diagnostic, Sécurité, IA privée, Réseau (avec le niveau);
  Mobilité (avec les véhicules); Entreprise (avec un lieu d'entreprise).
- **L'équipement** : boîtiers, capteurs, caméras et accès, confort et réseau (`MATERIEL`).
- **Les données** : tout reste chez le client. Sauvegarde chiffrée incluse. Accès de partout par un
  relais chiffré qui ne garde rien. En option, sur accord explicite : copie chiffrée des vidéos hors
  du lieu, renfort d'IA par le nuage.
- **L'aérien** : suivi au sol seulement (position, batterie, alertes, hangar). JARVIS ne touche
  jamais aux commandes ni à l'avionique.

## La page `/offre/` : trois étapes

1. **Vos lieux.** On choisit; « Votre écosystème » se dessine, un cerveau par lieu.
2. **Votre niveau.** Les trois niveaux côte à côte, même sur un téléphone. Chaque colonne est un choix
   et porte le nom de son appareil (Base : JARVIS Mini; Signature : JARVIS; Platinum : JARVIS Pro). Les
   lignes s'alignent d'une colonne à l'autre, dans cet ordre : les cinq extensions (« incluse » ou « en
   option »), où vit l'IA, caméras, appareils, lieux reliés, secours, soutien, garantie. Repliés :
   « Vous hésitez? », la fiche technique, changer de niveau plus tard.
3. **Votre projet.** Les extensions, l'ensemble de départ de chaque lieu, les données, l'installation,
   puis « Recevoir ma soumission ».

## Changer de niveau

- Monter : si l'appareil suffit, activation à distance. Sinon, échange de l'appareil avec un crédit.
- Un autre lieu : l'ancien appareil part dans le nouveau lieu, relié au principal.
- Redescendre : le client garde son appareil; on retire des fonctions.
- Le matériel installé reste toujours.

## Vérifié automatiquement

- `src/pages/catalogue.py` refuse de se bâtir s'il manque un ensemble de départ pour un lieu, ou si
  un ensemble nomme une pièce ou une automatisation qui n'existe pas.
- `tools/test_offre.py` joue le parcours dans un vrai navigateur : niveau conseillé, Boîtier VR qui
  suit le niveau, aucun appareil au-dessus du niveau, ensembles ajoutés et retirés, entreprise, flotte,
  nuage, soumission, rechargement.
- Le même essai vérifie les niveaux côte à côte : chaque colonne nomme son appareil, ce qu'elle dit
  « incluse » est ce que le niveau coche à l'étape 3, et sur un téléphone les trois colonnes tiennent
  dans l'écran, alignées.
- `tools/verifier_seo.py` refuse la publication si l'ancien nom « Hub » revient dans ce qu'un visiteur
  peut lire, sur n'importe quelle page (retiré de tout le site le 19 novembre 2026).
- La page `/plateforme/` ne nomme aucun appareil à la main : ses lieux d'exemple passent par
  `cerveaux()` (`src/lieux.py`), la même règle que la page L'offre.

## À décider par James

- Le montant du crédit quand on échange un appareil (rien n'est chiffré sur le site d'ici là).
- Les prix : le niveau par mois, le coût d'un lieu de plus (auparavant −30 % sur les solutions dès
  le deuxième lieu), un rabais sur les ensembles de départ (auparavant −8 % sur les kits).
- Le nom « JARVIS » sur un appareil : à faire vérifier par un agent de marques.
