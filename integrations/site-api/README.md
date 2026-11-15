# Service du site (formulaire, compteur, journal des visites, demandes pour JARVIS)

Petit Worker Cloudflare qui remplace les services externes du site :

- **Formulaire** : `POST /contact` garde la demande dans KV, puis l'envoie par Resend
  à `laplumejames@gmail.com` (réponse directe au visiteur avec « Répondre »).
- **Compteur** : `GET /visits` (lecture) et `POST /visits/hit` (une visite par session,
  sans témoin).
- **Journal des visites** :
  - `POST /visits/hit` inscrit aussi la première page de la session au journal;
  - `POST /visits/view` inscrit les pages suivantes, sans toucher au compteur;
  - `GET /visits/log?limit=200` (jeton `LEADS_TOKEN`, en-tête `Authorization: Bearer …`)
    renvoie les visites les plus récentes d'abord (1 à 1 000). C'est ce que lit la page
    privée `/admin/visites/`.

  Chaque visite contient : heure, page (chemin seulement, sans paramètres), domaine du site
  d'origine, pays, région, ville, latitude et longitude approximatives, fuseau horaire, numéro
  et nom du fournisseur Internet (tirés de l'adresse IP par Cloudflare), type d'appareil,
  système, navigateur et adresse IP. Aucun témoin, aucun identifiant dans le navigateur.
  **Conservation : 30 jours**, puis KV efface chaque visite tout seul (`expirationTtl`).
  Au-delà de 60 inscriptions par heure pour une même adresse, le journal ignore cette adresse
  jusqu'à l'heure suivante (le compteur, lui, continue).
- **JARVIS** : `GET /leads` (même jeton `LEADS_TOKEN`) liste les demandes reçues, pour
  que JARVIS Private Systems les importe plus tard.

Test local, sans réseau : `node integrations/site-api/test/visites.mjs`.

## Mise en service

1. Créer un espace KV `jarvis-site` et le lier sous le nom `SITE_KV`.
2. Déployer `src/index.js` (tableau de bord Cloudflare ou `npx wrangler deploy`).
3. Ajouter les secrets `RESEND_API_KEY` (clé Resend, domaine jarvisprivatesystems.com
   vérifié) et `LEADS_TOKEN` (longue chaîne aléatoire).
4. Relier un domaine, par exemple `api.jarvisprivatesystems.com`.
5. Dans `src/config.py` du site, mettre `"api": "https://api.jarvisprivatesystems.com"`,
   puis `python3 tools/build.py`. Le formulaire l'utilise alors en premier
   (FormSubmit reste en secours).

Pour lire le journal : ouvrir `https://jameslaplume.ca/admin/visites/`, coller le jeton
`LEADS_TOKEN` (gardé seulement le temps de l'onglet), puis « Actualiser ».

Ne jamais mettre une clé ou un jeton dans ce dépôt : il est public.
