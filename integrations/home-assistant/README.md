# Home Assistant OS vers jameslaplume.ca

Le fichier `battery-telemetry.yaml` est le package Home Assistant pour publier vers un Worker Cloudflare.

Le fichier `battery-telemetry-github-gist.yaml` est l'option rapide si on veut que HAOS pousse directement vers GitHub/Gist. Le site est deja configure pour lire ce Gist avant l'instantane local.

Les entity_id des deux BMS ont ete retrouves dans l'inventaire HA du 2026-08-31.

## Entity IDs utilises

| Mesure | Batterie A | Batterie B |
| --- | --- | --- |
| Charge | `sensor.dp04s007l4s200a_batterie` | `sensor.dp04s007l4s200a_batterie_2` |
| Tension | `sensor.dp04s007l4s200a_tension` | `sensor.dp04s007l4s200a_tension_2` |
| Courant | `sensor.dp04s007l4s200a_courant` | `sensor.dp04s007l4s200a_courant_2` |
| Puissance | `sensor.dp04s007l4s200a_puissance` | `sensor.dp04s007l4s200a_puissance_2` |
| Temperature | `sensor.dp04s007l4s200a_temperature` | `sensor.dp04s007l4s200a_temperature_2` |
| Energie stockee | `sensor.dp04s007l4s200a_energie_stockee` | `sensor.dp04s007l4s200a_energie_stockee_2` |
| Cellule haute | `sensor.dp04s007l4s200a_highest_cell_voltage` | `sensor.dp04s007l4s200a_highest_cell_voltage_2` |
| Cellule basse | `sensor.dp04s007l4s200a_lowest_cell_voltage` | `sensor.dp04s007l4s200a_lowest_cell_voltage_2` |
| Ecart cellules | `sensor.dp04s007l4s200a_delta_cell_voltage` | `sensor.dp04s007l4s200a_delta_cell_voltage_2` |
| Cycles | `sensor.dp04s007l4s200a_cycles` | `sensor.dp04s007l4s200a_cycles_2` |
| Equilibrage | `binary_sensor.dp04s007l4s200a_balancer` | `binary_sensor.dp04s007l4s200a_balancer_2` |
| Charge MOSFET | `binary_sensor.dp04s007l4s200a_charge_mosfet` | `binary_sensor.dp04s007l4s200a_charge_mosfet_2` |
| Decharge MOSFET | `binary_sensor.dp04s007l4s200a_discharge_mosfet` | `binary_sensor.dp04s007l4s200a_discharge_mosfet_2` |
| Alarme BMS | `binary_sensor.dp04s007l4s200a_probleme` | `binary_sensor.dp04s007l4s200a_probleme_2` |

Les valeurs agregees vues dans HA sont:

- `sensor.batteries_capacite_restante_totale`
- `sensor.batteries_courant_total`
- `sensor.batteries_puissance_totale`
- `sensor.batteries_energie_totale`
- `sensor.batteries_ecart_cellules_max`
- `binary_sensor.batteries_alarme_generale`

## Ce qui doit etre configure

- Remplacer `https://ton-worker.workers.dev/battery-status` par l'URL du Worker deploye.
- Ajouter le secret dans `secrets.yaml`:

```yaml
battery_telemetry_authorization: "Bearer TON_LONG_JETON_RANDOM"
```

## Cadence

L'exemple publie toutes les 30 secondes. Pour un site public, c'est assez rapide pour donner une impression temps reel sans transformer le flux en bruit.

L'option GitHub Gist publie toutes les 2 minutes par defaut pour eviter de frapper l'API GitHub inutilement. Pour du 30 secondes plus fiable, utiliser le Worker Cloudflare.

Ton export Home Assistant contenait deja une automation `battery_gist_publish`, mais elle etait a `initial_state: false`; si elle est encore dans HAOS, elle demarre donc desactivee. Le package Gist fourni ici cree une automation active et un `rest_command.publish_battery_gist` avec les bons capteurs.

## Securite

Home Assistant pousse vers Internet. Internet ne se connecte pas a Home Assistant.

Publier seulement des valeurs d'etat non sensibles: SOC, tension, courant, temperature, Ah, cellules, cycles et alarmes. Garder les IP, MAC, tokens, localisation et commandes de controle hors du flux public.
