# Passerelle publique des batteries

Cette passerelle sert de tampon propre entre Home Assistant OS et le site statique `jameslaplume.ca`.

Le flux recommandé est:

1. Home Assistant OS lit les batteries localement.
2. Une automation HAOS envoie un JSON public et nettoyé au Worker avec un jeton secret.
3. Le Worker valide le jeton, garde seulement les champs publics, puis écrit l'instantané dans Workers KV.
4. Le site GitHub Pages lit `GET /battery-status` toutes les 30 secondes.

Cette approche évite d'ouvrir Home Assistant sur Internet, évite d'héberger quelque chose sur le PC, et évite de transformer GitHub en base de données temps réel.

## Deploiement Cloudflare

```powershell
cd integrations/cloudflare-worker
copy wrangler.toml.example wrangler.toml
npm install
npx wrangler kv namespace create BATTERY_KV
```

Copier l'id du namespace dans `wrangler.toml`, puis configurer le secret:

```powershell
npx wrangler secret put WRITE_TOKEN
npx wrangler deploy
```

Après le déploiement, mettre l'URL du Worker dans `data/battery-public-config.json`:

```json
{
  "batteryStatusUrl": "https://ton-worker.workers.dev/battery-status"
}
```

Si tu ajoutes plus tard un sous-domaine comme `telemetry.jameslaplume.ca`, il suffira de remplacer l'URL par `https://telemetry.jameslaplume.ca/battery-status`.

## Donnees publiques permises

Le Worker accepte seulement des données d'état non sensibles:

- nom public de la batterie
- SOC, Ah disponibles, tension, courant, puissance
- température, énergie, plage de cellules
- cycles, équilibrage, permissions BMS, alarme

Ne jamais publier:

- jeton Home Assistant
- adresse IP privée
- identifiant Bluetooth/MAC
- position GPS en direct
- accès de contrôle
