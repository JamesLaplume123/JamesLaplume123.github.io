---
title: Créer un réseau de caméras privé
category: Sécurité
status: Guide
---

Un bon réseau de caméras ne commence pas par le nombre de caméras. Il commence par les zones à comprendre: entrée, allée, côté de maison, garage, véhicule, porte secondaire.

L'objectif est de voir ce qui compte sans transformer chaque mouvement en alerte. Les caméras devraient enregistrer localement, être accessibles par VPN et rester isolées du réseau principal lorsque c'est possible.

Architecture typique:

- caméras PoE
- switch PoE
- Frigate pour la détection locale
- Home Assistant pour les notifications et les automatisations
- stockage local
- accès distant privé par Tailscale ou WireGuard

Le point important: la caméra ne doit pas être le système. Elle doit être une source d'information dans une architecture claire.
