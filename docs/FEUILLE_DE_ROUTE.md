# Feuille de route du site JARVIS

On ne travaille que sur l'étape en cours. Tout le travail de la refonte se fait sur des branches ;
la refonte complète est montrée à James avant d'être mise en ligne (sauf ce qu'il demande de
publier avant).

## Refonte « un seul site » (novembre 2026)

But : un site cohérent du début à la fin, du général au détail, dans un seul style (docs/SITE.md).

| Étape | Contenu | État |
|---|---|---|
| 1. Les fondations | La loi du site, le plan fermé, les agents, les garde-fous, les vérifications et les captures | **En cours** |
| 2. Le cadre | Le menu, le pied de page et les gabarits communs (accueil, division, solution, page simple) | À faire |
| 3. L'accueil | Ce qu'est JARVIS → les trois divisions → l'appareil → la preuve (laboratoire) → contact | À faire |
| 4. Les divisions | Page Solutions, nouvelle page JARVIS Privé, JARVIS Entreprise, JARVIS Cyber | À faire |
| 5. Les solutions | Les 8 pages de solution au complet dans le gabarit, exemple maison ou entreprise selon le visiteur ; les 2 pages d'exemple | À faire |
| 6. Les autres pages | L'appareil, le logiciel, Pourquoi JARVIS, à propos, vision, confiance, laboratoire, recherche, questions, contact | À faire |
| 7. Composer mon forfait | Le configurateur au nouveau modèle (division → lieux → solutions → appareil par lieu), prix sur soumission ; inclusions décidées par James | À faire, avec James |
| 8. La révision complète | Tour de tout le site par le réviseur, captures à James, mise en ligne sur son accord | À faire |
| 9. La version anglaise | /en/ refait page pour page selon la même loi | Après la refonte |

Une page passe au statut « fait » dans `docs/plan_du_site.json` seulement quand elle respecte la loi
au complet : à ce moment, `scripts/verifier_site.py` applique le budget de texte.
