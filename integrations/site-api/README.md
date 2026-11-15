# Service du site (formulaire, compteur, journal des visites, demandes pour JARVIS)

Petit Worker Cloudflare qui remplace les services externes du site :

- **Formulaire** : `POST /contact` garde la demande dans KV, puis l'envoie par Resend
  à `laplumejames@gmail.com` (réponse directe au visiteur avec « Répondre »).
- **Compteur** : `GET /visits` (lecture) et `POST /visits/hit` (une visite par session,
  sans témoin).
- **Journal des visites** :
  - `POST /visits/hit` inscrit aussi la première page de la session au journal;
  - `POST /visits/view` inscrit les pages suivantes, sans toucher au compteur;
  - `GET /visits/log?limit=200&cursor=…` (jeton `LEADS_TOKEN`, en-tête
    `Authorization: Bearer …`) renvoie les visites les plus récentes d'abord, par tranches
    (200 par défaut, 500 au plus). La réponse donne `cursor` : le repasser pour la tranche
    suivante; `null` quand tout est lu. La première tranche donne aussi `jours` (compteurs des
    400 derniers jours), `totaux` (depuis le début) et `archives`. C'est ce que lit la page
    privée `/admin/visites/`.

  Chaque visite contient : heure, page (chemin seulement, sans paramètres), domaine du site
  d'origine, pays, région, ville, latitude et longitude approximatives, fuseau horaire, numéro
  et nom du fournisseur Internet (tirés de l'adresse IP par Cloudflare), type d'appareil,
  système, navigateur et adresse IP. Aucun témoin, aucun identifiant dans le navigateur.

  **Conservation : 24 mois**, puis KV efface chaque visite tout seul (`expirationTtl`). La durée
  est la constante `RETENTION_JOURS = 730`, en tête de `src/index.js` : une ligne à changer
  (avec `/confidentialite/`, `/admin/visites/` et les README). Les visites écrites quand la durée
  était de 30 jours sont prolongées à 24 mois quand James ouvre le journal (20 par lecture).

  **Ce qui est compté.** Seulement les requêtes dont l'en-tête `Origin` est dans
  `ALLOWED_ORIGINS` et n'est pas un poste local (`localhost`), et dont le `User-Agent` n'est pas
  un robot évident (bot, crawler, spider, HeadlessChrome, facebookexternalhit, curl…). Les
  autres reçoivent une réponse 200 normale, mais rien n'est écrit ni compté.

  **Clés KV.**

  | Clé | Contenu | Durée |
  | --- | --- | --- |
  | `visit:<horodatage inversé>:<8 car.>` | une visite; l'horodatage inversé fait sortir les plus récentes en premier | 24 mois |
  | `vstat:AAAA-MM-JJ` | compteurs du jour (heure de Toronto) : `visites`, `pages`, et les cumuls `total` (compteur public) et `pagesTotal` | gardés (aucun renseignement personnel) |
  | `vjour` | dernier jour qui a un compteur | — |
  | `visits` | ancien compteur public : point de départ du cumul, plus écrit | — |
  | `archive:AAAA-MM-JJ` | relevé d'avant la mise en service, créé à la main dans le tableau de bord (JSON : `periode`, `source`, `note`, `lignes`); plus servi et effacé 24 mois après sa date | 24 mois |

  **Écritures KV (quota gratuit : 1 000 par jour).**

  | Événement | Écritures |
  | --- | --- |
  | Arrivée (`/visits/hit`) | 2 : la visite et le compteur du jour (qui porte aussi le compteur public) |
  | Page suivante (`/visits/view`) | 2 : la visite et le compteur du jour |
  | Première visite de chaque jour | 1 de plus (`vjour`) |
  | Requête ignorée (autre origine, robot, plafond atteint) | 0 |
  | Lecture du journal | 0 (sauf la prolongation des anciennes visites, une seule fois chacune) |

  Deux plafonds protègent le quota : 60 inscriptions par heure pour une même adresse (tenu en
  mémoire, sans écriture, donc approximatif), et 450 inscriptions par jour au total
  (`JOURNAL_MAX_PAR_JOUR`, soit 900 écritures) : au-delà, plus rien n'est compté ni inscrit ce
  jour-là, et il reste de la place pour le formulaire. Avec plus de 450 pages vues par jour, il
  faudra passer au forfait payant de Workers ou alléger le journal.
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

Relevé d'avant la mise en service : dans le tableau de bord Cloudflare, espace KV du service,
ajouter la clé `archive:2026-11-08` avec le relevé en JSON. Ce relevé contient des adresses IP :
il ne va jamais dans ce dépôt.

Ne jamais mettre une clé ou un jeton dans ce dépôt : il est public.
