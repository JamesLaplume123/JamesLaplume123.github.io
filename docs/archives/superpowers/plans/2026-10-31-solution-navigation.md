# Navigation directe vers les solutions — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for the root integration.

**Goal:** Rendre immédiatement évidente l’ouverture de chacune des six solutions depuis l’accueil.

**Architecture:** Liens HTML natifs vers les six routes existantes. Le survol et le focus enrichissent l’aperçu, sans intercepter la navigation. Un CTA nommé reste visible en tête de l’aperçu. CSS et JavaScript existants, sans dépendance ni routeur.

**Tech Stack:** Générateur Node, HTML statique, CSS responsive, JavaScript navigateur.

**Spec:** Demande de James et capture du31octobre dans ce chat; choix de routine et réalisation délégués par ses consignes persistantes.

## Global Constraints

- Conserver identité noire/or, photographies existantes et pages des six solutions.
- Le clic et Entrée sur chaque carte doivent ouvrir sa propre route, y compris sans JavaScript.
- Aucun formulaire envoyé, équipement commandé ou logiciel privé modifié.
- Préserver un retour arrière Git et vérifier le vrai domaine après publication.

## Review Focus

- Écran court et mobile : aucun lien principal enfoui sous une grande illustration.
- Clavier : Tab garde des liens natifs; focus met l’aperçu à jour sans déplacer le focus.
- Modificateurs : Ctrl/Cmd/clic milieu continuent d’ouvrir les liens normalement.
- Survol rapide : image, titre, lien et libellé décrivent toujours la même solution.
- Réseau/JS indisponible : les six destinations restent accessibles.

## Réalisation

- [x] Tester les six destinations et les événements survol/focus/clic dans tools/tests/solution-navigation.test.mjs.
- [x] Modifier homePage() dans tools/build-site.mjs : six ancres et CTA nommé; reconstruire les pages.
- [x] Modifier uniquement le composant capacités de site-v4.css et site-v4.js : hauteur maîtrisée, photo, actions visibles, aucune interception de clic.
- [x] Vérifier navigateur à320/390/768/1440px, clics réels six routes, clavier, arrière et mouvements réduits.
- [ ] Publier le commit exact puis vérifier le domaine réel (relecture déjà effectuée).
