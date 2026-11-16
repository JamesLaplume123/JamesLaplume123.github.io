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
    a("- Tout tourne chez le client, dans un Hub. Les données restent sur place; aucun stockage dans le nuage. Un relais chiffré sert seulement à l’accès de partout et à relier plusieurs lieux; il ne garde rien.")
    a("- JARVIS continue de fonctionner sans Internet (règles, IA locale, caméras, journal). Les mises à jour sont signées, la nuit, avec retour arrière.")
    a("- Le logiciel est en construction : le site montre des démonstrations; le premier JARVIS tourne dans le laboratoire mobile (une ambulance convertie). La démo et la visite sont offertes dès maintenant.")
    a("")
    a("## Les pages du site (donner le lien complet quand c’est utile)")
    pages = [
        ("/", "Accueil"), ("/solutions/", "Les sept solutions"), ("/logiciel/", "Le logiciel en démonstration"),
        ("/plateforme/", "Le Hub : le boîtier, son IA privée, le noyau"),
        ("/offre/", "L’offre : un Hub payé une fois (Base, Signature, Platinum), des solutions par mois, le matériel"),
        ("/catalogue/", "Composer mon forfait : le configurateur (lieu, Hub conseillé, solutions, matériel, récapitulatif, soumission)"),
        ("/solutions/maison-intelligente-cle-en-main/", "Maison intelligente clé en main"),
        ("/solutions/domotique-ferme-agricole/", "Domotique pour ferme"), ("/solutions/ia-privee-entreprise/", "IA privée pour entreprise"),
        ("/a-propos/", "À propos de James"), ("/vision-roadmap/", "Vision et feuille de route"), ("/laboratoire-mobile/", "Laboratoire mobile (ambulance)"),
        ("/confiance/", "Confiance"), ("/recherche/", "Recherche : la méthode"), ("/questions/", "Questions fréquentes"),
        ("/contact/", "Contact : démo, visite, soumission"), ("/confidentialite/", "Confidentialité (Loi 25)"),
        ("/mentions-legales/", "Mentions légales"), ("/plan-du-site/", "Plan du site : toutes les pages"),
    ]
    a("- Menu du site : Solutions (les sept, puis Maison, Ferme, Entreprise) · Le logiciel · L’offre · À propos (Laboratoire mobile, Vision, Le Hub, Confiance, Questions, Contact) · bouton doré « Composer mon forfait ».")
    a("- Parcours conseillé : voir (accueil, solutions) → tester (le logiciel, la démonstration de chaque solution) → comprendre (l’offre, le Hub, les questions) → composer son forfait (le configurateur), puis « Recevoir ma soumission ».")
    a("- Le forfait se bâtit en chemin : « Ajouter à mon forfait » sur chaque page de solution; le compteur de la barre mène au configurateur, où tout est déjà coché.")
    for u, t in pages:
        a(f"- {D}{u} : {t}")
    if complet:
        for c in CAPABILITIES:
            a(f"- {D}/solutions/{c['slug']}/ : {c['title']} ({c['label']})")
    else:
        a("- Chaque solution a sa page : " + D + "/solutions/<nom>/ avec " + ", ".join(c["slug"] for c in CAPABILITIES))
    a("")
    a("## Entrer par son lieu (même source que le site : src/lieux.py)")
    for fid, fnom in lieux.FAMILLES:
        a(f"### {fnom}")
        for l in lieux.LIEUX:
            if l["famille"] != fid:
                continue
            quoi = " + ".join(x for x in (lieux.HUB_NOM.get(l["hub"]), l.get("boitier")) if x)
            sols = "; ".join(f"{lieux._TITRE[s]} ({r.rstrip('.')})" for s, r in l["solutions"])
            a(f"- {l['nom']}" + (f" ({l['sorte'].lower()})" if l.get("sorte") else "") + f" : {quoi}. {l['raison']} Solutions qui comptent : {sols}.")
    a("- Un lieu mobile (VR, roulotte, bateau habitable) se traite comme une maison qui roule : Hub et Boîtier VR. Un véhicule (auto, camion, moto, avion) reçoit un Boîtier Mobilité, sans Hub à bord.")
    a("")
    a("## L’offre en quatre étapes")
    a("1. Le Hub, payé une fois : Base, Signature ou Platinum selon la taille du lieu. Même logiciel, même app; ce qui change, c’est la puissance, le nombre d’appareils, l’IA et la sécurité.")
    a("2. Les solutions, par mois, annulables en tout temps : comme des apps. Environnements intelligents est inclus avec chaque Hub.")
    a("3. Le matériel du lieu, payé une fois : capteurs, caméras, boîtiers, prêt à brancher. On réutilise ce qui existe déjà (Victron, UniFi, caméras ONVIF, NAS, Starlink).")
    a("4. Plusieurs lieux : un Hub par lieu, une seule app, −30 % sur les solutions dès le deuxième lieu. Installation au choix.")
    a("")
    a("## Les trois Hubs")
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
    a("- Dans chaque Hub : Environnements intelligents, l’app JARVIS, les comptes et droits, les mises à jour signées, les sauvegardes chiffrées.")
    a("")
    a("## Les solutions (par mois)")
    for s in C.SOLUTIONS:
        prix = "incluse avec chaque Hub" if s["prix"] == 0 else f"{s['prix']} $ par mois" + (f" {s['unite']}" if s.get("unite") else "")
        a(f"- {s['nom']} : {prix}. {s['pourquoi']}" + (" Comprend : " + "; ".join(s["pts"]) + "." if complet else ""))
    a(f"- {C.COMPLET['nom']} : {C.COMPLET['prix']} $ par mois pour les cinq solutions payantes, Mobilité pour un véhicule comprise (valeur à la carte {C.COMPLET['valeur']} $).")
    a("- Chaque solution payante inclut l’accès de partout et les alertes sur le téléphone. Sans solution payante, JARVIS fonctionne quand même chez le client, sur place.")
    a("")
    a("## Pour une entreprise (à la carte, par mois; demande un Hub Signature ou Platinum)")
    a(f"- {C.ENT_SOCLE['nom']} : {C.ENT_SOCLE['prix']} $ par mois, obligatoire pour toute automatisation. {C.ENT_SOCLE['d']}")
    a(f"- {C.ENT_RECEP['nom']} : {C.ENT_RECEP['prix']} $ par mois {C.ENT_RECEP['unite']}. {C.ENT_RECEP['d']}")
    a(f"- {C.ENT_TOUTES['nom']} : {C.ENT_TOUTES['prix']} $ par mois. {C.ENT_TOUTES['pourquoi']}")
    a(f"- {C.ENT_MESURE['nom']} : {C.ENT_MESURE['prix']} $ une fois puis {C.ENT_MESURE['mois']} $ par mois. {C.ENT_MESURE['d']}")
    a(f"- {C.ENT_USAGE}")
    a("- Prix des automatisations : 9 $ (un déclencheur, une action), 19 $ (reliée à un outil du client), 29 $ (veille 24/7 avec escalade). Hub Signature : jusqu’à 10 automatisations; Platinum : illimité.")
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
    a("- Les caméras s’enregistrent dans le Hub, jamais dans le nuage. Le Boîtier VR va dans un VR, une roulotte ou un bateau; le Boîtier Mobilité dans une voiture ou un camion. Le Hub Base n’a pas d’IA locale : les caméras y sont analysées par Internet.")
    a("")
    a("## Les kits (prix des pièces moins 8 %, ajustables pièce par pièce)")
    for i, k in enumerate(C.KITS, 1):
        plein, once, mois = C._kit_totaux(k)
        hub = C.HUB_BY_ID[k["hub"]]["nom"]
        pieces = ", ".join(f"{q} × {C.MAT_BY_ID[m][1]}" for m, q in k["mat"].items())
        if complet:
            a(f"- {k['nom']} : {p(once)} une fois (au lieu de {p(plein)}) + {mois} $ par mois. Pour : {k['pour']}. Contenu : {hub}, {pieces}. {k['pourquoi']} Lien : {D}/catalogue/?kit={i}")
        else:
            a(f"- {k['nom']} : {p(once)} + {mois} $/mois, {hub}, {1 + sum(k['mat'].values())} pièces. Pour : {k['pour']}. {D}/catalogue/?kit={i}")
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
    a("- Un Hub par lieu (maison, chalet, VR, bateau, entreprise, ferme, garage, hangar). Les lieux se parlent par un lien privé et chiffré; les petits lieux empruntent l’IA du plus gros Hub. Les solutions sont à −30 % dès le deuxième lieu; l’Entreprise et le matériel ne sont pas réduits.")
    a("- Un Hub Base suit un Hub principal; un Signature relie jusqu’à 3 lieux; un Platinum, sans limite.")
    a("")
    a("## Chiffres utiles (sources : Bureau d’assurance du Canada, Chubb)")
    a("- 47 % des réclamations d’assurance habitation sont des dégâts d’eau, 12 000 $ en moyenne. Seulement 9 % des gens ont un système qui détecte les fuites. Diagnostic & continuité coûte 15 $ par mois; un capteur de fuite, 59 $; la vanne d’eau automatique, 349 $.")
    a("")
    a("## Ce qu’on ne promet pas")
    a("- Pas de téléphone à donner : le contact passe par la page Contact. Pas de délai de livraison précis. Pas de « sans engagement » : les solutions sont annulables en tout temps, le matériel non installé est remboursable 30 jours, moins la configuration.")
    a("- Les capacités des Hubs sont des repères; elles dépendent aussi des caméras et des solutions actives. Les prix sont confirmés par écrit avant tout achat.")
    texte = "\n".join(L) + "\n"
    return texte if SITE["prix_publics"] else sans_prix(texte)


def sans_prix(texte):
    """Prix non publics (SITE["prix_publics"] = False) : la fiche garde tout (Hubs, différences, solutions,
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
