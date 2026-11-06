# Service du site (formulaire, compteur, demandes pour JARVIS)

Petit Worker Cloudflare qui remplace les services externes du site :

- **Formulaire** : `POST /contact` garde la demande dans KV, puis l'envoie par Resend
  à `laplumejames@gmail.com` (réponse directe au visiteur avec « Répondre »).
- **Compteur** : `GET /visits` et `POST /visits/hit`, sans témoin ni pistage.
- **JARVIS** : `GET /leads` (jeton `LEADS_TOKEN`) liste les demandes reçues, pour
  que JARVIS Private Systems les importe plus tard.

## Mise en service

1. Créer un espace KV `jarvis-site` et le lier sous le nom `SITE_KV`.
2. Déployer `src/index.js` (tableau de bord Cloudflare ou `npx wrangler deploy`).
3. Ajouter les secrets `RESEND_API_KEY` (clé Resend, domaine jarvisprivatesystems.com
   vérifié) et `LEADS_TOKEN` (longue chaîne aléatoire).
4. Relier un domaine, par exemple `api.jarvisprivatesystems.com`.
5. Dans `src/config.py` du site, mettre `"api": "https://api.jarvisprivatesystems.com"`,
   puis `python3 tools/build.py`. Le formulaire l'utilise alors en premier
   (FormSubmit reste en secours).

Ne jamais mettre une clé ou un jeton dans ce dépôt : il est public.
