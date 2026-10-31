---
title: Séparer les objets connectés du réseau principal
category: Réseaux
status: Architecture
---

Les objets connectés ne devraient pas tous avoir le même niveau de confiance qu'un ordinateur personnel ou qu'un serveur.

La séparation peut être simple ou avancée selon l'environnement: réseau invité, VLAN, règles de pare-feu, accès limité vers Home Assistant et blocage de ce qui n'est pas nécessaire.

Objectifs:

- limiter les risques
- rendre le dépannage plus clair
- garder les services importants stables
- éviter qu'un appareil faible compromette tout le réseau

La sécurité pratique commence souvent par une bonne organisation.
