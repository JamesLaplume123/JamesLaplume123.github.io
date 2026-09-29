# jameslaplume.ca

Site statique multipage de James Laplume et du projet JARVIS.

## Structure publique

- `/solutions/` présente les six familles de solutions.
- `/plateforme/` explique comment JARVIS App, JARVIS Core et JARVIS Hub forment une même plateforme.
- `/ambulance-lab/` documente le laboratoire physique.
- `/recherche/` sépare les hypothèses, essais et preuves.
- `/vision-roadmap/` contient uniquement la vision et les horizons futurs.
- `/confiance/`, `/a-propos/` et `/contact/` complètent le parcours.

## Reconstruction

Le contenu commun et les routes sont générés par `tools/build-site.mjs`.

```powershell
node tools/build-site.mjs
```

Les pages générées restent du HTML statique compatible avec GitHub Pages. Les détails sensibles de recherche, les secrets, les données personnelles et les configurations exploitables ne doivent jamais être ajoutés à ce dépôt public.

## Fonctionnement

- `site-v3.css` contient le système visuel responsive commun.
- `site-v3.js` contrôle le menu, les animations, le formulaire et le compteur public.
- Le formulaire utilise FormSubmit pour transmettre les demandes à `laplumejames@gmail.com`.
- `/en/` fournit un aperçu anglais; l’édition détaillée est maintenue en français.
- Les anciennes pages redirigent vers les nouvelles sections correspondantes.
- `CNAME` conserve le domaine `jameslaplume.ca`.
- `.nojekyll` permet à GitHub Pages de servir tous les actifs tels quels.
- `sitemap.xml`, `robots.txt` et `og.png` assurent le référencement et le partage social.

## Telemetrie batteries

GitHub Pages reste l'hébergement statique du site. Pour du presque temps réel, Home Assistant OS doit pousser les mesures vers une petite passerelle publique sécurisée, puis le site lit cette passerelle toutes les 30 secondes.

- Worker Cloudflare: `integrations/cloudflare-worker/`
- Exemple Home Assistant avec Worker: `integrations/home-assistant/battery-telemetry.yaml`
- Option rapide Home Assistant vers GitHub Gist: `integrations/home-assistant/battery-telemetry-github-gist.yaml`
- Configuration publique du site: `data/battery-public-config.json`

Le site compare les sources publiques disponibles et garde la plus recente. Si HAOS n'a pas encore pousse de nouvelle mesure, l'instantane local sert seulement de secours et reste indique comme vieux par l'interface.

Ne jamais publier de jeton Home Assistant, adresse IP privée, identifiant Bluetooth/MAC ou commande de contrôle dans le JSON public.

## Déploiement

- Dépôt : `JamesLaplume123/JamesLaplume123.github.io`
- Branche publiée : `main`
- Domaine : `jameslaplume.ca`
