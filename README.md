# jameslaplume.ca

Site statique bilingue de **James Laplume — Intelligent Systems Lab**, publié avec GitHub Pages.

## Pages

| Français | English |
| --- | --- |
| `/` | `/en/` |
| `/jarvis-builder/` | `/en/jarvis-builder/` |
| `/jarvis-twin/` | `/en/jarvis-twin/` |
| `/ambulance-lab/` | `/en/ambulance-lab/` |
| `/trading-lab/` | `/en/trading-lab/` |
| `/services/` | `/en/services/` |
| `/about/` | `/en/about/` |
| `/contact/` | `/en/contact/` |

Les anciennes pages HTML redirigent vers les nouvelles sections correspondantes.

## Fonctionnement

- `static-runtime.js` contrôle la navigation mobile, l’aperçu JARVIS Builder, le diagnostic JARVIS Twin, l’explorateur de l’ambulance, la télémétrie publique et le formulaire.
- Le formulaire prépare un courriel structuré vers `contact@jameslaplume.ca` parce que GitHub Pages ne fournit pas de serveur applicatif.
- `CNAME` conserve le domaine `jameslaplume.ca`.
- `.nojekyll` permet à GitHub Pages de servir tous les actifs tels quels.
- `sitemap.xml`, `robots.txt` et `og.png` assurent le référencement et le partage social.

## Déploiement

- Dépôt : `JamesLaplume123/JamesLaplume123.github.io`
- Branche publiée : `main`
- Domaine : `jameslaplume.ca`
