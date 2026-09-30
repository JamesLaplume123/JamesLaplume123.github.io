# Système visuel des interfaces JARVIS

Statut: proposition de phase 2. À approuver avant son application aux pages du
site.

## Intention

L'interface doit ressembler à un produit professionnel installé dans une
résidence, une entreprise ou un véhicule haut de gamme. Elle doit être calme,
immédiatement compréhensible et réellement utilisable.

La référence visuelle oriente la qualité, la hiérarchie et l'ambiance. JARVIS
conserve toutefois sa propre identité et ne reproduit pas une autre marque.

## Identité

- Une seule marque visible: JARVIS.
- Le contexte actif apparaît en second niveau: Résidence, Entreprise, Véhicule,
  Sécurité ou Diagnostic.
- Les codes JK, JE, JP, JN et AL disparaissent des interfaces publiques.
- Un seul monogramme JARVIS est utilisé dans toutes les capacités.
- Les statuts techniques sont secondaires et ne concurrencent jamais le titre.

## Palette

- Fond principal: bleu nuit presque noir.
- Surfaces: graphite bleuté avec profondeur très légère.
- Accent principal: or chaud, réservé à la sélection et aux commandes premium.
- Succès et disponibilité: turquoise.
- Information technique: cyan discret.
- Avertissement: ambre doux.
- Texte principal: blanc cassé, jamais blanc agressif.
- Texte secondaire: gris froid suffisamment contrasté.

Le vert sombre actuel ne doit plus dominer. Le cyan ne doit plus colorer toutes
les bordures et tous les titres.

## Typographie

- Titres d'accueil et d'ambiance: sérif élégante.
- Navigation, données et commandes: sans sérif claire.
- Monospace seulement pour les identifiants, journaux ou valeurs techniques.
- Taille minimale confortable; aucune information importante en microtexte.
- Aucun espacement négatif des lettres.

## Structure commune

Chaque interface complète utilise:

1. Une navigation latérale unique.
2. Une barre supérieure avec contexte, heure, recherche, notifications et
   profil.
3. Une zone visuelle principale montrant le lieu, le dossier ou l'événement.
4. Des contrôles rapides adaptés à la capacité.
5. Des panneaux secondaires limités aux décisions utiles.
6. Un retour d'action discret et temporaire.

Les interfaces intégrées dans une page Web peuvent utiliser une version réduite
de cette structure, mais ne doivent jamais ajouter un deuxième menu concurrent.

## Composants

### Navigation

Icône, libellé court, sélection or et contraste élevé. Aucun badge sans utilité.

### Cartes

Rayon discret, surface sombre, une seule bordure fine et profondeur légère.
Une carte doit permettre une décision ou montrer un état; elle n'est jamais
simplement décorative.

### Photographie

Les images montrent le véritable contexte: pièce, bâtiment, véhicule, personne,
document ou équipement. Elles sont intégrées à l'expérience plutôt qu'ajoutées
comme décoration.

### États

- Or: sélection ou commande active choisie par l'utilisateur.
- Turquoise: système disponible ou état confirmé.
- Cyan: information ou relation technique.
- Ambre: attention requise.
- Rouge: danger réel ou action bloquée, utilisé rarement.

### Actions

Une commande importante indique ce qui changera. Les actions sensibles montrent
l'effet prévu puis demandent une approbation explicite.

### Conversation

La demande de l'utilisateur doit ressortir immédiatement. La réponse JARVIS
sépare clairement la compréhension, les sources, la proposition et l'action.

## Mouvement

- Transitions lentes et précises entre 180 et 350 ms.
- Aucun effet néon, balayage futuriste ou animation décorative continue.
- Les changements réels d'état restent visibles.
- Le mode de mouvement réduit est respecté.

## Règles de densité

- Une vue principale montre au plus six contrôles rapides.
- Une carte possède un titre, un état et au maximum une information secondaire.
- Les détails avancés apparaissent après sélection.
- Les interfaces de démonstration privilégient la vue simple par défaut.
- Un panneau ne répète pas une information déjà visible dans l'en-tête.

## Interdictions

- Robots, circuits imprimés et esthétique cyberpunk générique.
- Racks informatiques utilisés comme image principale d'une expérience client.
- Bordures cyan sur tous les éléments.
- Plusieurs identités JARVIS concurrentes.
- Deux menus contrôlant les mêmes panneaux.
- Texte minuscule pour expliquer une fonction importante.
- Statistiques sans origine ou bénéfices commerciaux inventés.

## Prototype de référence

Le prototype local `/ui-system-preview/` montre la direction visuelle, la
hiérarchie et les interactions de base. Il n'est ni indexé ni relié à la
navigation publique.

Après approbation, ces règles seront appliquées d'abord à la démonstration
Environnements intelligents. Aucune autre interface ne sera convertie avant la
validation de ce premier cas réel.
