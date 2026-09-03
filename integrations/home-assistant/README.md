# Home Assistant OS vers jameslaplume.ca

Le fichier `battery-telemetry.yaml` est un exemple de package Home Assistant.

## Ce qui doit etre adapte

- Remplacer `https://ton-worker.workers.dev/battery-status` par l'URL du Worker deploye.
- Remplacer les `sensor.bms_a_*`, `sensor.bms_b_*` et `binary_sensor.bms_*` par les vrais entity_id dans HAOS.
- Ajouter le secret dans `secrets.yaml`:

```yaml
battery_telemetry_authorization: "Bearer TON_LONG_JETON_RANDOM"
```

## Cadence

L'exemple publie toutes les 30 secondes. Pour un site public, c'est assez rapide pour donner une impression temps reel sans transformer le flux en bruit.

## Securite

Home Assistant pousse vers Internet. Internet ne se connecte pas a Home Assistant.

Publier seulement des valeurs d'etat non sensibles: SOC, tension, courant, temperature, Ah, cellules, cycles et alarmes. Garder les IP, MAC, tokens, localisation et commandes de controle hors du flux public.
