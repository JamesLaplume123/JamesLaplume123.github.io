# jameslaplume.ca

Première version statique du site personnel de James Laplume.

## Structure

- `index.html`: contenu de la page
- `styles.css`: apparence du site
- `script.js`: petite interaction du panneau Jarvis
- `assets/hero-workspace.png`: image principale
- `CNAME`: domaine personnalisé pour GitHub Pages

## Publier avec GitHub Pages

1. Créer un dépôt GitHub public nommé `jameslaplume.ca` ou `JamesLaplume123.github.io`.
2. Ajouter tous les fichiers de ce dossier à la racine du dépôt.
3. Aller dans `Settings` > `Pages`.
4. Choisir `Deploy from a branch`, branche `main`, dossier `/root`.
5. Dans `Custom domain`, entrer `jameslaplume.ca`.
6. Dans WHC, configurer les DNS pour GitHub Pages.

## DNS WHC pour GitHub Pages

Ajouter quatre enregistrements `A` pour le domaine racine:

```text
@ -> 185.199.108.153
@ -> 185.199.109.153
@ -> 185.199.110.153
@ -> 185.199.111.153
```

Ajouter aussi le sous-domaine `www`:

```text
www -> CNAME -> JamesLaplume123.github.io
```

Quand GitHub confirme le domaine, activer `Enforce HTTPS`.

## Plus tard sur ton serveur

Ce site peut être servi tel quel avec Caddy ou nginx. Exemple de dossier:

```text
/var/www/jameslaplume.ca
```

Le futur assistant Jarvis demandera un backend séparé pour gérer les appels API,
les données privées, les permissions et les automatisations.
