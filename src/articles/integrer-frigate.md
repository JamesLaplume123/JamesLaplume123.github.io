---
title: Intégrer Frigate dans un système local
category: Sécurité
status: Lab note
---

Frigate sert à analyser les flux caméra localement et à reconnaître des objets comme une personne ou un véhicule.

Dans une architecture intelligente, Frigate ne remplace pas Home Assistant. Il lui envoie des événements utiles. Home Assistant peut ensuite décider quoi faire: allumer une lumière, marquer une timeline, envoyer une notification ou ignorer l'événement.

Les points à planifier:

- position des caméras
- zones de détection
- stockage
- performance matérielle
- réseau filaire
- accès distant privé

Une bonne configuration réduit les fausses alertes au lieu d'ajouter du bruit.
