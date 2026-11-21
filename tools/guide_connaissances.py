# Fiche de connaissances du JARVIS du site (le portier sur la tour la lit comme guide-connaissances.md).
# Générée à partir du catalogue (src/pages/catalogue.py) : une seule source de vérité pour les prix.
# Sortie : assets/guide/connaissances.md (publique, sans règle de comportement : seulement des faits).
# Appelé par tools/build.py; peut aussi être lancé seul : python3 tools/guide_connaissances.py

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path[:0] = [os.path.join(RACINE, "src"), os.path.join(RACINE, "src", "pages")]

import catalogue as C  # noqa: E402
from config import SITE, CAPABILITIES  # noqa: E402
import lieux  # noqa: E402

D = SITE["domain"].rstrip("/")


def p(n):
    return f"{n:,}".replace(",", " ") + " $"


def fiche(complet=True):
    L = []
    a = L.append
    a("# Ce que JARVIS sait par cœur (fiche de connaissances)")
    a(f"Mise à jour automatique à partir du catalogue du site. Tous les prix sont en dollars canadiens, taxes en sus, et sont des points de départ : chaque soumission est confirmée par écrit, ligne par ligne, avant tout achat. Rien ne se paie sur le site.")
    a("")
    a("## Qui nous sommes")
    a("- JARVIS Private Systems : technologies de sécurité et intelligence privée. Nous concevons et installons JARVIS, un système privé qui gère et protège les maisons, les fermes, les entreprises et les véhicules. Fondateur : James Laplume.")
    a("- En phase de lancement : nous prenons les noms des personnes intéressées et nous choisissons quelques premiers projets.")
    a("- Aucune zone desservie n’est publiée et aucun lieu n’est nommé (ni ville, ni région, ni province). Pour savoir si un projet est possible à un endroit donné, la réponse se donne par la page Contact.")
    a("- L’entreprise parle toujours au « nous ». JARVIS, l’assistant, parle au « je » seulement de lui-même.")
    a("- Tout tourne chez le client, dans un JARVIS. Les données restent sur place. Un relais chiffré sert à l’accès de partout et à relier plusieurs lieux; il ne garde rien. En option seulement : une sauvegarde chiffrée et une copie des vidéos hors du lieu.")
    a("- JARVIS continue de fonctionner sans Internet (règles, IA locale, caméras, journal). Les mises à jour sont signées, la nuit, avec retour arrière.")
    a("- Le logiciel est en construction : le site montre des démonstrations; le premier JARVIS tourne dans le laboratoire mobile (une ambulance convertie). La démo et la visite sont offertes dès maintenant.")
    a("")
    a("## Les pages du site (donner le lien complet quand c’est utile)")
    pages = [
        ("/", "Accueil"), ("/solutions/", "Les sept solutions"), ("/logiciel/", "Le logiciel en démonstration"),
        ("/plateforme/", "L’appareil JARVIS : son IA privée, le noyau"),
        ("/offre/", "L’offre : trois niveaux tout compris (Base, Signature, Platinum), des options, le projet sur mesure"),
        ("/offre/#composer", "Composer mon JARVIS : pour qui, le lieu, le guide de trois questions, le niveau, les options, le projet, la soumission"),
        ("/solutions/maison-intelligente-cle-en-main/", "Maison intelligente clé en main"),
        ("/solutions/domotique-ferme-agricole/", "Domotique pour ferme"), ("/solutions/ia-privee-entreprise/", "IA privée pour entreprise"),
        ("/a-propos/", "À propos de James"), ("/vision-roadmap/", "Vision et feuille de route"), ("/laboratoire-mobile/", "Laboratoire mobile (ambulance)"),
        ("/confiance/", "Confiance"), ("/recherche/", "Recherche : la méthode"), ("/questions/", "Questions fréquentes"),
        ("/contact/", "Contact : démo, visite, soumission"), ("/confidentialite/", "Confidentialité (Loi 25)"),
        ("/mentions-legales/", "Mentions légales"), ("/plan-du-site/", "Plan du site : toutes les pages"),
    ]
    a("- Menu du site : Solutions (les sept, puis Maison, Ferme, Entreprise) · Le logiciel · L’offre · À propos (Laboratoire mobile, Vision, L’appareil, Confiance, Questions, Contact) · bouton doré « Composer mon forfait ».")
    a("- Parcours conseillé : voir (accueil, solutions) → tester (le logiciel, la démonstration de chaque solution) → comprendre (l’offre, l’appareil, les questions) → composer son forfait (le configurateur), puis « Recevoir ma soumission ».")
    a("- Le forfait se bâtit en chemin : « Ajouter à mon forfait » sur chaque page de solution; le compteur de la barre mène au configurateur, où tout est déjà coché.")
    for u, t in pages:
        a(f"- {D}{u} : {t}")
    if complet:
        for c in CAPABILITIES:
            a(f"- {D}/solutions/{c['slug']}/ : {c['title']} ({c['label']})")
    else:
        a("- Chaque solution a sa page : " + D + "/solutions/<nom>/ avec " + ", ".join(c["slug"] for c in CAPABILITIES))
    a("")
    a("## Pour chez moi, pour mon entreprise, ou les deux")
    a("- Le site demande d’abord pour qui : « Pour chez moi », « Pour mon entreprise » ou « Les deux ». Côté « Pour chez moi », il ne montre pas ce qui est propre à l’entreprise.")
    a("- Propre à l’entreprise : " + ", ".join(lieux._TITRE[s] for s in lieux.SOLUTIONS_PUBLIC) + " (réceptionniste IA, lignes téléphoniques, automatisations), les services professionnels, les rapports et la base de données du JARVIS Pro, et les lieux d’entreprise (" + ", ".join(l["nom"].lower() for l in lieux.LIEUX if l["public"] == "entreprise") + ").")
    a("- Les six autres solutions servent aux deux publics.")
    a("- Un propriétaire d’entreprise a souvent aussi une maison : un seul compte, une seule application, plusieurs lieux personnels et d’entreprise possibles. La soumission se fait ensemble ou séparément pour l’entreprise (au nom de l’entreprise), au choix. Ne donner aucun conseil fiscal.")
    a("")
    a("## Les trois règles de l’offre (à dire simplement)")
    a("- 1. Un cerveau par lieu : un lieu reçoit un JARVIS (JARVIS Mini, JARVIS ou JARVIS Pro), un véhicule reçoit un boîtier. Nous le choisissons selon la taille du lieu et le niveau.")
    a("- 2. Un seul niveau pour tout : Base, Signature ou Platinum s’applique à tous les lieux du client. Il décide des extensions incluses, d’où vit l’IA et du soutien. Le lieu principal porte le niveau; les plus petits s’appuient sur lui.")
    a("- 3. L’équipement suit le lieu : chaque type de lieu a son ensemble de départ (boîtier, capteurs). Le reste est sur mesure, et ce qui existe déjà est réutilisé.")
    a("- Le client ne décide donc que deux choses : ses lieux et son niveau. Le reste est proposé, puis ajusté.")
    a("")
    a("## Entrer par son lieu : cinq familles (même source que le site : src/lieux.py)")
    for fid, fnom in lieux.FAMILLES:
        a(f"### {fnom}")
        for l in lieux.LIEUX:
            if l["famille"] != fid:
                continue
            quoi = " + ".join(x for x in (lieux.HUB_NOM.get(l["hub"]), l.get("boitier")) if x)
            sols = "; ".join(f"{lieux._TITRE[s]} ({r.rstrip('.')})" for s, r in l["solutions"])
            a(f"- {l['nom']} : {quoi}. {l['raison']} Solutions qui comptent : {sols}.")
    a("- Un lieu mobile (VR, roulotte, bateau, yacht) se traite comme une maison qui roule : JARVIS et Boîtier VR. Un véhicule (auto, camion, moto) ou un appareil (avion, hélicoptère) reçoit un Boîtier Mobilité, sans JARVIS à bord. Une flotte : un boîtier par véhicule, le tableau de la flotte au bureau.")
    a("- Aérien : suivi au sol seulement (position, batterie, alertes, hangar). JARVIS ne touche jamais aux commandes ni à l’avionique.")
    a("")
    a("## L’offre : trois niveaux tout compris (même source que la page L’offre)")
    a("- Le client choisit un niveau : Base, Signature ou Platinum. Le niveau dit ce que JARVIS fait et le soutien inclus. Chaque niveau comprend tout le précédent.")
    for k, nom in (("base", "Base"), ("signature", "Signature"), ("platinum", "Platinum")):
        n = C.NIVEAUX[k]
        a(f"- {nom} : " + (n["plus"] + " " if n["plus"] else "") + "; ".join(x[0].lower() + x[1:] for x in n["inclus"]) + ". Solutions incluses : " + ", ".join({s["id"]: s["nom"] for s in C.SOLUTIONS}[x] for x in n["sols"]) + ".")
    a("- Le projet (le matériel du lieu et l’installation) est sur mesure : chaque lieu est différent. On réutilise ce qui existe déjà (Victron, UniFi, caméras ONVIF, NAS, Starlink).")
    a("- Les options s’ajoutent au mois, annulables en tout temps : ce qui n’est pas déjà dans le niveau (par exemple Mobilité pour un véhicule, ou l’Entreprise).")
    a("- La page L’offre se fait en trois étapes : 1) vos lieux (l’écosystème se dessine, un cerveau par lieu), 2) votre niveau (trois questions conseillent si on hésite), 3) votre projet (extensions, ensemble de départ de chaque lieu, données, installation), puis « Recevoir ma soumission ».")
    a("- Où vit l’IA : " + " ".join(f"{nom} : {C.NIVEAUX[k]['ia']}" for k, nom in (("base", "Base"), ("signature", "Signature"), ("platinum", "Platinum"))))
    a("- Extensions : cinq viennent avec le niveau (Base 2, Signature 4, Platinum 5). Mobilité s’ajoute avec chaque véhicule. Entreprise s’ajoute pour un lieu d’entreprise, dès le niveau Signature.")
    a("- Règle simple : un JARVIS plus puissant peut toujours faire un niveau plus bas, jamais l’inverse.")
    a("")
    a("## Monter ou descendre de niveau")
    a("- Monter : si le JARVIS suffit, on active le niveau à distance, le jour même. S’il faut plus de puissance, on échange le JARVIS avec un crédit; la configuration est restaurée telle quelle.")
    a("- Un autre lieu : l’ancien JARVIS part au chalet ou dans le VR, relié au nouveau.")
    a("- Redescendre : le client garde son JARVIS; on retire des fonctions et il paie moins.")
    a("- Le matériel installé reste toujours. Rien ne se perd.")
    a("")
    a("## Bâtir son écosystème (plusieurs lieux, une seule app)")
    a("- Un écosystème JARVIS, c’est tous les lieux d’une personne ou d’une entreprise reliés : maison, chalet, VR, bateau, garage, bureau, ferme, et les véhicules.")
    a("- Méthode à proposer, une question à la fois : 1) quels sont vos lieux; 2) lequel est le principal (il reçoit le plus gros JARVIS, qui prête son IA aux autres); 3) pour chaque autre lieu, un JARVIS plus petit suffit souvent; 4) les véhicules reçoivent un Boîtier Mobilité, sans JARVIS; 5) une seule app et un seul compte pour tout, une soumission pour l’ensemble.")
    a("- Les lieux se parlent par un lien privé et chiffré. Si Internet tombe, chaque lieu continue seul.")
    a("")
    a("## Le nuage : seulement ce qui est utile")
    a("- Tout tourne chez le client. La sauvegarde chiffrée est incluse (illisible pour nous). L’accès de partout passe par un relais chiffré qui ne garde rien. En option seulement, et sur accord explicite : une copie chiffrée des vidéos hors du lieu (au cas où le JARVIS serait volé ou détruit) et un renfort d’IA par le nuage pour les grosses tâches.")
    a("")
    a("## Quel appareil pour quel niveau (en mots de tous les jours)")
    for h in C.HUBS:
        c = lieux.HUBS_CHOIX[h["id"]]
        a(f"- {h['nom']} — {c['situation']} ({c['pour']}). {c['promesse']} Vous pouvez : " + "; ".join(x[0].lower() + x[1:] for x in c["peut"]) + f". À savoir : {c['savoir']}")
    a("- Pour aider quelqu’un qui hésite, poser les trois questions de la page L’offre : combien de caméras; l’intelligence doit-elle rester chez vous, même sans Internet; une coupure serait-elle grave. Platinum si une coupure serait grave ou 7 caméras et plus; Signature si l’IA doit rester chez soi ou 3 à 6 caméras; sinon Base.")
    a("")
    a("## Les trois appareils : JARVIS Mini, JARVIS, JARVIS Pro")
    a("- N’écris jamais le mot « Hub » : c’est un ancien nom, retiré du site. Si un visiteur le dit, il parle de l’appareil JARVIS : réponds « JARVIS Mini », « JARVIS », « JARVIS Pro » ou « l’appareil ».")
    for h in C.HUBS:
        a(f"### {h['nom']} : {p(h['prix'])}, une fois. Pour : {h['pour']}.")
        if not complet:
            a(f"- {h['pourquoi']} A : " + "; ".join(h["pts"]) + ("." if not h["manque"] else ". Manque : " + "; ".join(h["manque"]) + "."))
            continue
        a(f"- Pourquoi : {h['pourquoi']}")
        a("- Ce qu’il a : " + "; ".join(h["pts"]) + ".")
        if h["manque"]:
            a("- Ce qui lui manque : " + "; ".join(h["manque"]) + ".")
    a("")
    a("### Comparatif précis (Base | Signature | Platinum)")
    for lab, *v in (C.COMPARE if complet else C.COMPARE[3:12]):
        a(f"- {lab} : " + " | ".join("non" if x == "—" else x for x in v))
    a("- Dans chaque JARVIS : Environnements intelligents, l’app JARVIS, les comptes et droits, les mises à jour signées, les sauvegardes chiffrées.")
    a("")
    a("## Les solutions (incluses selon le niveau, ou en option au mois)")
    for s in C.SOLUTIONS:
        prix = "incluse avec chaque JARVIS" if s["prix"] == 0 else f"{s['prix']} $ par mois" + (f" {s['unite']}" if s.get("unite") else "")
        a(f"- {s['nom']} : {prix}. {s['pourquoi']}" + (" Comprend : " + "; ".join(s["pts"]) + "." if complet else ""))
    a("- Chaque solution payante inclut l’accès de partout et les alertes sur le téléphone. Sans solution payante, JARVIS fonctionne quand même chez le client, sur place.")
    a("")
    a("## Pour une entreprise (à la carte, par mois; demande le niveau Signature ou Platinum)")
    a(f"- {C.ENT_SOCLE['nom']} : {C.ENT_SOCLE['prix']} $ par mois, obligatoire pour toute automatisation. {C.ENT_SOCLE['d']}")
    a(f"- {C.ENT_RECEP['nom']} : {C.ENT_RECEP['prix']} $ par mois {C.ENT_RECEP['unite']}. {C.ENT_RECEP['d']}")
    a(f"- {C.ENT_TOUTES['nom']} : {C.ENT_TOUTES['prix']} $ par mois. {C.ENT_TOUTES['pourquoi']}")
    a(f"- {C.ENT_MESURE['nom']} : {C.ENT_MESURE['prix']} $ une fois puis {C.ENT_MESURE['mois']} $ par mois. {C.ENT_MESURE['d']}")
    a(f"- {C.ENT_USAGE}")
    a("- Prix des automatisations : 9 $ (un déclencheur, une action), 19 $ (reliée à un outil du client), 29 $ (veille 24/7 avec escalade). Niveau Signature : jusqu’à 10 automatisations; niveau Platinum : illimité.")
    a("### Bibliothèque d’automatisations")
    for cat, items in C.AUTOMATISATIONS:
        a(f"- {cat} : " + "; ".join(f"{n} ({pr} $/mois)" + (f" — {w}" if complet else "") for _, n, pr, w in items) + ".")
    a("")
    a("## Le matériel (payé une fois, prêt à brancher)")
    for cat, items in C.MATERIEL:
        if complet:
            a(f"### {cat}")
            for _, n, pr, d, w in items:
                a(f"- {n} : {p(pr)}. {d} Pourquoi : {w}")
        else:
            a(f"- {cat} : " + "; ".join(f"{n} {p(pr)}" for _, n, pr, _, _ in items) + ".")
    a("- Les caméras s’enregistrent dans le JARVIS, jamais dans le nuage. Le Boîtier VR va dans un VR, une roulotte ou un bateau; le Boîtier Mobilité dans une voiture ou un camion. Le JARVIS Mini n’a pas d’IA locale : les caméras y sont analysées par Internet.")
    a("")
    a("## Ouvrir un plan tout composé (un seul lien)")
    a(f"- Adresse : {D}/offre/?lieux=<lieux>&niveau=<niveau>&ens=tout#composer. La page s’ouvre avec l’écosystème dessiné, le niveau choisi et l’ensemble de départ de chaque lieu ajouté. Le visiteur ajuste, puis demande sa soumission.")
    a("- lieux : identifiants séparés par des virgules, parmi : " + ", ".join(f"{l['id']} ({l['nom']})" for l in lieux.LIEUX) + ".")
    a("- niveau : base, signature ou platinum. Sans niveau, la page prend le niveau conseillé pour ces lieux.")
    a(f"- Exemple : maison, chalet et une auto, niveau Signature : {D}/offre/?lieux=maison,chalet,auto&niveau=signature&ens=tout#composer")
    a("- Un lieu ne se met qu’une fois dans le lien; le nombre de véhicules ou de pièces s’ajuste sur la page.")
    a(f"- Liste sur mesure : un paramètre par lieu, « pièce:quantité » séparés par des virgules, remplace l’ensemble de départ de ce lieu. Exemple, deux caméras et deux capteurs de fuite à la maison, trois capteurs de gel au chalet : {D}/offre/?lieux=maison,chalet&niveau=signature&ens=tout&maison=camext:2,fuite:2,vanne:1&chalet=temp:3,fuite:2,porte:2#composer")
    a("- Les codes de pièces, pour composer cette liste :")
    for cat, items in C.MATERIEL:
        a(f"  - {cat} : " + "; ".join(f"{i} = {n}" for i, n, _, _, _ in items) + ".")
    a("- Un code qui n’est pas dans cette liste est ignoré par la page. Les quantités sont des nombres entiers. Le Boîtier VR s’écrit vr* : la page met celui du niveau choisi.")
    a("")
    a("## Les ensembles de départ (un par lieu, ajustables pièce par pièce)")
    for l in lieux.LIEUX:
        e = C.ENSEMBLES[l["id"]]
        pieces = ", ".join(f"{q} × " + ("Boîtier VR (celui du niveau)" if i == "vr*" else C.MAT_BY_ID[i][1]) for i, q in e["mat"].items())
        ent = e.get("ent") or {}
        plus = (", réceptionniste IA" if ent.get("recep") else "") + (f", {len(ent['autos'])} automatisations pour commencer" if ent.get("autos") else "")
        a(f"- {l['nom']} : {pieces}{plus}. {e['pourquoi']}")
    a("- Ce sont des points de départ proposés à l’étape 3 de la page L’offre. Le Boîtier VR suit le niveau choisi.")
    a("")
    a("## Services professionnels (payés une fois)")
    for fam, items in C.SERVICES:
        for _, n, pr, d, w in items:
            a(f"- {fam} · {n} : {p(pr)}. {d}" + (f" {w}" if complet else ""))
    a("- Nous vérifions et protégeons des systèmes; nous ne sommes pas une agence de gardiennage ni d’enquête.")
    a("### Entretien et veille (entreprise, par mois)")
    for _, n, pr, d, w in C.ENT_VEILLE:
        a(f"- {n} : {pr} $ par mois. {d}")
    a("")
    a("## Installation")
    for _, n, pr, aff, d in C.INSTALL:
        a(f"- {n} : {aff}. {d}")
    a("- Toujours inclus : " + "; ".join(f"{n} ({d.rstrip('.')})" for n, d in C.INCLUS) + ".")
    a("")
    a("## Plusieurs lieux")
    a("- Un JARVIS par lieu (maison, chalet, VR, bateau, entreprise, ferme, garage, hangar). Les lieux se parlent par un lien privé et chiffré; les petits lieux empruntent l’IA du plus gros JARVIS. Les solutions sont à −30 % dès le deuxième lieu; l’Entreprise et le matériel ne sont pas réduits.")
    a("- Niveau Base : chaque lieu veille seul. Niveau Signature : jusqu’à 3 lieux reliés entre eux. Niveau Platinum : sans limite.")
    a("")
    a("## Chiffres utiles (sources : Bureau d’assurance du Canada, Chubb)")
    a("- 47 % des réclamations d’assurance habitation sont des dégâts d’eau, 12 000 $ en moyenne. Seulement 9 % des gens ont un système qui détecte les fuites. Diagnostic & continuité coûte 15 $ par mois; un capteur de fuite, 59 $; la vanne d’eau automatique, 349 $.")
    a("")
    a("## Ce qu’on ne promet pas")
    a("- Pas de téléphone à donner : le contact passe par la page Contact. Pas de délai de livraison précis. Pas de « sans engagement » : les solutions sont annulables en tout temps, le matériel non installé est remboursable 30 jours, moins la configuration.")
    a("- Les capacités des JARVIS sont des repères; elles dépendent aussi des caméras et des solutions actives. Les prix sont confirmés par écrit avant tout achat.")
    texte = "\n".join(L) + "\n"
    return texte if SITE["prix_publics"] else sans_prix(texte)


def sans_prix(texte):
    """Prix non publics (SITE["prix_publics"] = False) : la fiche garde tout (JARVIS, différences, solutions,
    ce que chacune ne fait pas) mais aucun montant. Une phrase dit pourquoi."""
    import re
    m = r"\d[\d\u00a0\u202f ]*[,.]?\d*\s?\$"
    unite = r"(?:\s?/\s?mois|\spar mois|,?\sune fois|\sl’heure)?"
    lignes = []
    for l in texte.split("\n"):
        if "$" in l:
            l = re.sub(r"\s*\((?:[^()]*?)" + m + r"[^()]*\)", "", l)                 # (valeur à la carte 75 $)
            l = re.sub(r"\s*(?::|,|\+|puis|dès|à|au lieu de)?\s*" + m + unite, "", l)   # : 590 $, une fois
            l = l.replace(" la minute ensuite", "")
            l = re.sub(r"\s+([.;,])", r"\1", l).replace("..", ".").replace(" .", ".")
        if "$" in l or not l.strip("-# .;,:"):
            continue
        lignes.append(l)
    out = "\n".join(lignes)
    return out.replace(
        "## L’offre en quatre étapes",
        "## Les prix\n- Les prix ne sont pas publiés pendant le lancement : chaque projet reçoit une soumission écrite. "
        "Ne donner aucun montant, même approximatif.\n\n## L’offre en quatre étapes", 1)


def ecrire():
    dossier = os.path.join(RACINE, "assets", "guide")
    os.makedirs(dossier, exist_ok=True)
    # connaissances.md : version courte, celle que le modèle lit (tient dans son contexte);
    # connaissances-complete.md : tout, avec descriptions et pourquoi (référence, et pour un modèle à grand contexte).
    chemin = os.path.join(dossier, "connaissances.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(fiche(complet=False))
    with open(os.path.join(dossier, "connaissances-complete.md"), "w", encoding="utf-8") as f:
        f.write(fiche(complet=True))
    return chemin


if __name__ == "__main__":
    print(ecrire())
