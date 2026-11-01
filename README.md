# jameslaplume.ca — JARVIS Private Systems

Site public de JARVIS Private Systems, fondé par James Laplume (Québec, Canada).
Site statique multipage, hébergé sur GitHub Pages avec le domaine `jameslaplume.ca`.

## Structure du dépôt

```
src/                  Source du site (la seule chose à modifier)
├── config.py         Identité, navigation, capacités, redirections
├── partials.py       Gabarits <head>, en-tête, pied de page
├── pages/            Une page = un module Python (contenu HTML)
│   └── _solution.py  Gabarit commun des six pages de solution
└── articles/         Brouillons d'articles (non publiés pour l'instant)

tools/build.py        Générateur (Python 3 standard, aucune dépendance)

assets/
├── css/wow.css       L'unique feuille de style (design « WOW », esprit Apple/Tesla)
├── js/wow.js         L'unique script (barre, menu, scènes, modes, compteurs)
├── fonts/            Geist et Geist Mono auto-hébergées (variables)
└── *.js, *_vinext_*  Build figé de /sudo-bonne-fete/ (carte QR) — ne pas toucher

media/                Images du site (webp/png)
data/                 Configurations publiques (télémétrie batterie)
integrations/         Worker Cloudflare + exemples Home Assistant (télémétrie)
docs/                 Références : source de vérité, architecture, UI, audits

index.html, */index.html, sitemap.xml, <anciennes-urls>
                      FICHIERS GÉNÉRÉS — ne pas éditer à la main
```

## Modifier le site

1. Éditer le contenu dans `src/pages/`, les gabarits dans `src/partials.py`
   ou le style dans `assets/css/site.css`.
2. Regénérer :

```bash
python3 tools/build.py
```

3. Prévisualiser localement :

```bash
python3 -m http.server 4173
```

4. Commiter et pousser sur `main` : GitHub Pages publie automatiquement.

Les modes Base, Signature et Platinum sont définis en tête de `wow.css`, et leurs
images sont dans `media/modes/`. Ajouter `?mode=platinum` à une adresse force un mode.

Pour invalider le cache navigateur après un changement de CSS/JS, incrémenter
`asset_version` dans `src/config.py` puis regénérer.

## Règles éditoriales

- L'architecture des pages suit `docs/SITE_INFORMATION_ARCHITECTURE.md` ;
  le vocabulaire produit suit `docs/JARVIS_SITE_SOURCE_OF_TRUTH.md` ;
  le système visuel suit `docs/JARVIS_UI_SYSTEM.md`.
- Ne jamais publier de secret, jeton, adresse IP privée, identifiant matériel
  ou configuration exploitable : le dépôt est public.
- Ne jamais inventer de client, certification, résultat commercial ou capacité
  déjà disponible. Chaque démonstration est marquée « données simulées ».

## Déploiement

- Dépôt : `JamesLaplume123/JamesLaplume123.github.io`
- Branche publiée : `main` (racine)
- Domaine : `jameslaplume.ca` (fichier `CNAME`)
- `.nojekyll` : GitHub Pages sert les fichiers tels quels
- Branche `ancien-site` : le site tel qu'il était en ligne avant la refonte (conservé, non publié)

## Formulaire de contact

Le formulaire de `/contact/` passe par FormSubmit et transmet les messages à
`laplumejames@gmail.com`. Aucun service de suivi n'est utilisé.

## Télémétrie batteries (optionnel, non branché au site actuellement)

L'interface publique de télémétrie a été retirée du site lors de la refonte
d'octobre 2026; les intégrations restent prêtes dans `integrations/` :

- Worker Cloudflare : `integrations/cloudflare-worker/`
- Home Assistant : `integrations/home-assistant/`
- Configuration publique : `data/battery-public-config.json`

Ne jamais publier de jeton Home Assistant, adresse IP privée ou identifiant
Bluetooth/MAC dans le JSON public.
