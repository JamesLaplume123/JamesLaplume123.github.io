# La loi du site JARVIS

Statut : proposée le 28 novembre 2026, à approuver par James.
Ce document remplace `SITE_INFORMATION_ARCHITECTURE.md`, `JARVIS_SITE_SOURCE_OF_TRUTH.md` et
`JARVIS_UI_SYSTEM.md` (rangés dans `docs/archives/`). Quand il change, la documentation change
avant le code, et seulement avec l'accord de James.

Les règles de l'offre (lieux, appareils, niveaux) restent dans `docs/OFFRE.md`.
La liste fermée des pages est dans `docs/plan_du_site.json` : `scripts/verifier_site.py` la fait
respecter.

## 1. Le message

JARVIS est une IA privée, installée chez vous, qui protège et gère votre maison, votre
entreprise et vos véhicules. La valeur de fond : rendre les gens libres.

Une personne doit comprendre en quelques secondes, dans cet ordre :

1. ce qu'est JARVIS ;
2. les trois divisions ;
3. ce que contient la division qui la concerne ;
4. chaque solution en détail.

On va toujours du général au détail. Une page ne saute jamais une marche.

## 2. Le plan du site

```
Accueil : ce qu'est JARVIS
├── JARVIS Privé : votre maison, votre chalet, vos véhicules
│     L'appareil · Réseau et cybersécurité · Sécurité intelligente · Diagnostic et continuité ·
│     Environnements intelligents · Mobilité · IA privée et connaissances · Intelligence de vie (vision)
├── JARVIS Entreprise : travailleurs autonomes, PME, fermes, commerces
│     Votre travail : Réceptionniste IA · Automatisations · Comptes et accès · Rapport du matin ·
│                     Savoir de l'entreprise
│     Vos bâtiments : tout ce que Privé offre, en version entreprise (réseau, sécurité,
│                     diagnostic, environnements, flotte)
├── JARVIS Cyber : vérification de vos systèmes, sur mandat écrit
│     Vérification · Test d'intrusion · Exposition en ligne · Loi 25 · Mise à niveau · Formation
├── L'appareil : JARVIS Mini, JARVIS, JARVIS Pro, et le logiciel qui tourne dedans
├── Composer mon forfait : le chemin d'achat
└── À propos : Pourquoi JARVIS · Vision · Confiance · Laboratoire · Recherche · Questions · Contact
```

Règles du plan :

- **Une page, un rôle.** Une idée expliquée sur une page n'apparaît ailleurs qu'en résumé ou en lien.
- **Le menu, le pied de page, l'accueil et la page Solutions suivent ce même ordre.**
- **Les solutions communes à Privé et à Entreprise ont une seule page.** Elle montre l'exemple
  « maison » ou l'exemple « entreprise » selon le choix du visiteur (« Pour chez moi » /
  « Pour mon entreprise »).
- **Les pages par contexte** (maison clé en main, ferme, IA pour entreprise) ne sont pas des
  solutions : ce sont des exemples dans leur division. Elles ne sont jamais présentées à côté des
  solutions.
- **Aucune page hors du plan.** Une nouvelle page entre d'abord dans `docs/plan_du_site.json`,
  avec l'accord de James.
- **Ne rien perdre.** Une page retirée garde son adresse par une redirection vers sa nouvelle place.

## 3. Appareils et forfaits

- **L'appareil** (JARVIS Mini, JARVIS, JARVIS Pro) est choisi selon le besoin de chaque lieu. Il
  n'est pas lié au forfait : un client Platinum peut avoir un Mini.
- **Le forfait** (Base, Signature, Platinum) dit ce que JARVIS fait. En Base, l'IA passe par un
  service externe (API) ; l'IA locale est très faible ou absente.
- **Ce qui est inclus dans quel forfait, et les prix, c'est James qui décide.** Tant qu'il n'a
  pas décidé, le site dit « sur soumission » et n'invente aucune inclusion.

## 4. Le style : façon Apple

Un seul style pour tout le site. Une page en ancien style est « à refaire » dans le plan, jamais
mélangée avec le nouveau dans la même section.

- **Une idée par écran.** Un grand titre, une phrase, une image ou une preuve.
- **Fond noir pur, gros titres, beaucoup d'espace.** L'or sert seulement d'accent : la deuxième
  ligne d'un titre, un chiffre, un lien. Pas de cadres dorés sur les nouvelles sections.
- **De grandes photos réelles ou réalistes**, jamais de dessin à la place d'une photo.
- **Les mêmes gabarits partout :** accueil, division, solution, page simple. Une page de
  solution suit toujours : ouverture → Imaginez → le chiffre → la différence → ce que JARVIS fait
  → démonstration → sur le terrain → en détail → déploiement → questions.
- **Les sources et les notes légales vont en petit, en bas** (notes numérotées), jamais dans le
  texte principal.

### Le budget de texte

| Élément | Maximum |
|---|---|
| Grand titre (h1) | 14 mots |
| Titre de section (h2) | 10 mots |
| Phrase | 20 mots |
| Paragraphe | 2 phrases, 40 mots |
| Tuile (titre et ligne) | 15 mots |
| Rangée de comparaison (les deux côtés) | 20 mots |

Les pages légales (confidentialité, mentions légales), les notes en bas de page, les réponses aux
questions fréquentes et les démonstrations sont exemptées.

## 5. La façon de vendre

1. **Le bénéfice d'abord**, jamais la technique d'abord.
2. **Un moment concret** (« Imaginez ») avant toute liste.
3. **Une preuve** : un chiffre réel, avec sa source vérifiée.
4. **La différence** avec un produit ordinaire, rangée par rangée, sans dénigrer de marque.
5. **Le détail ensuite** : la fiche, l'équipement, le prix.
6. **Un seul geste principal par écran.**

Honnêteté, toujours :

- JARVIS est en conception. Le premier lieu réel est le laboratoire mobile (l'ambulance devenue VR).
- Aucun chiffre sans source. Aucune comparaison fausse. Aucune promesse que le projet ne tient pas.
- Les limites légales sont dites : la pose de caméras et d'alarmes par un installateur qui détient
  le permis requis, l'électricité et la plomberie par des entrepreneurs qualifiés, JARVIS Cyber
  seulement sur mandat écrit.

## 6. Ce qui ne va jamais en ligne

- Un secret, un mot de passe ou un jeton.
- Le vrai logiciel : le site montre seulement des démonstrations avec des données d'exemple.
- Les photos et la lettre de Roxanne.
- Une idée que James n'a pas choisie (elle va dans `docs/IDEES.md`).
- Une décision de forfait ou de prix que James n'a pas prise.

## 7. Les langues

Le français d'abord. La version anglaise suit la même loi et le même plan, page pour page, à
l'étape prévue de la feuille de route.
