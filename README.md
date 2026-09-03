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
- `static-runtime.js` charge aussi la télémétrie publique des batteries, avec `data/battery-public-config.json` comme configuration et `data/battery-status.json` comme instantané de secours.
- Le formulaire prépare un courriel structuré vers `contact@jameslaplume.ca` parce que GitHub Pages ne fournit pas de serveur applicatif.
- `CNAME` conserve le domaine `jameslaplume.ca`.
- `.nojekyll` permet à GitHub Pages de servir tous les actifs tels quels.
- `sitemap.xml`, `robots.txt` et `og.png` assurent le référencement et le partage social.

## Telemetrie batteries

GitHub Pages reste l'hébergement statique du site. Pour du presque temps réel, Home Assistant OS doit pousser les mesures vers une petite passerelle publique sécurisée, puis le site lit cette passerelle toutes les 30 secondes.

- Worker Cloudflare: `integrations/cloudflare-worker/`
- Exemple Home Assistant avec Worker: `integrations/home-assistant/battery-telemetry.yaml`
- Option rapide Home Assistant vers GitHub Gist: `integrations/home-assistant/battery-telemetry-github-gist.yaml`
- Configuration publique du site: `data/battery-public-config.json`

Ne jamais publier de jeton Home Assistant, adresse IP privée, identifiant Bluetooth/MAC ou commande de contrôle dans le JSON public.

## Déploiement

- Dépôt : `JamesLaplume123/JamesLaplume123.github.io`
- Branche publiée : `main`
- Domaine : `jameslaplume.ca`
