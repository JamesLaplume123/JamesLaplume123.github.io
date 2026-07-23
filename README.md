# jameslaplume.ca

Site personnel premium de James Laplume.

Cette version sert de base publique pour le domaine `jameslaplume.ca`: une page
rapide, statique, prête pour GitHub Pages, avec une direction visuelle plus
haut de gamme et une première interface de laboratoire Jarvis.

## Structure

- `index.html`: contenu de la page
- `styles.css`: direction visuelle, responsive et animations
- `script.js`: interactions du panneau Jarvis, horloge, animations et canvas
- `assets/hero-workspace.png`: image principale
- `CNAME`: domaine personnalisé pour GitHub Pages

## Direction

Le site présente James comme un atelier numérique personnel:

- serveur privé
- automatisation
- vision, caméras et sécurité locale
- van tech
- futur assistant Jarvis

## DNS WHC pour GitHub Pages

Le domaine racine utilise les quatre adresses `A` officielles de GitHub Pages:

```text
@ -> 185.199.108.153
@ -> 185.199.109.153
@ -> 185.199.110.153
@ -> 185.199.111.153
```

Le sous-domaine `www` pointe vers GitHub Pages:

```text
www -> CNAME -> JamesLaplume123.github.io
```

Le courriel reste isolé du site:

```text
mail -> A -> 54.39.226.237
@ -> MX -> mail.jameslaplume.ca.
```

## Plus tard

Quand Jarvis devient une vraie application, migrer vers une structure React ou
un backend privé sera logique. Pour l'instant, la page reste volontairement
statique pour charger vite et se déployer simplement sur GitHub Pages.
