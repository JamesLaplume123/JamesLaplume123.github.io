# Catalogue — l'offre complète, à la façon d'une boutique (novembre 2026).
# Quatre étapes : 1) le Hub (Base, Signature, Platinum), 2) les solutions (par mois) et
# l'Entreprise à la carte, 3) le matériel du lieu (une fois), 4) lieux et installation.
# Un panier collant à droite détaille chaque ligne et fait le total.
# Tous les prix vivent ici. Les kits sont calculés à partir de leurs pièces (−8 %).
# Styles : assets/demos/catalogue.css · Script : assets/demos/catalogue.js

from html import escape
import json

HUBS = [
    {"id": "base", "nom": "Hub Base", "prix": 590, "pour": "Chalet, condo, petit VR",
     "tag": "", "cam": 2, "app": 30, "autos": 0,
     "pourquoi": "Pour veiller sur un lieu simple : fuite, gel, porte, batterie. L’IA passe par Internet.",
     "pts": ["Jusqu’à 30 appareils", "2 caméras analysées, 7 jours d’enregistrement", "IA par Internet seulement",
             "Wi-Fi, Bluetooth, Zigbee", "Garantie 1 an, soutien par courriel"],
     "manque": ["Pas d’IA dans le Hub", "Pas d’assistant vocal ni de réceptionniste", "Pas d’automatisations d’entreprise", "Pas de batterie de secours"]},
    {"id": "signature", "nom": "Hub Signature", "prix": 1290, "pour": "Maison, VR complet, PME",
     "tag": "Le plus choisi", "cam": 6, "app": 100, "autos": 10,
     "pourquoi": "L’IA tourne chez vous, sans Internet : assistant vocal, caméras analysées sur place, réceptionniste.",
     "pts": ["Jusqu’à 100 appareils", "6 caméras analysées, 30 jours d’enregistrement", "IA locale, dans le Hub",
             "Assistant vocal « Jarvis » et réceptionniste IA", "Z-Wave et Matter, 3 lieux reliés",
             "Garantie 2 ans, soutien téléphone"],
     "manque": ["Pas de base de données ni de rapports", "Pas de batterie de secours", "Automatisations limitées à 10"]},
    {"id": "platinum", "nom": "Hub Platinum", "prix": 3490, "pour": "Domaine, entreprise, ferme",
     "tag": "Rien ne manque", "cam": 16, "app": 10 ** 6, "autos": 10 ** 6,
     "pourquoi": "Pour un lieu qui ne doit jamais s’arrêter : carte IA dédiée, batterie, Internet de secours, rapports.",
     "pts": ["Appareils illimités", "16 caméras et plus, 90 jours d’enregistrement", "IA forte, 100 % locale, carte IA dédiée",
             "Base de données, rapports, automatisations illimitées", "Batterie interne 2 h, Internet de secours intégré",
             "Hub principal de tous vos lieux", "Garantie 3 ans, remplacement express, personne dédiée"],
     "manque": []},
]
HUB_BY_ID = {h["id"]: h for h in HUBS}

# Tableau comparatif détaillé : (ligne, base, signature, platinum). "—" = manque (point rouge).
COMPARE = [
    ("Processeur", "Standard", "4× plus rapide", "16× plus rapide + carte IA"),
    ("Mémoire", "8 Go", "16 Go", "32 Go"),
    ("Stockage", "128 Go SSD", "512 Go SSD", "2 To SSD"),
    ("Appareils reliés", "30", "100", "Illimité"),
    ("Caméras analysées par l’IA", "2", "6", "16 et plus"),
    ("Enregistrement vidéo", "7 jours", "30 jours", "90 jours et plus"),
    ("IA privée", "Par Internet seulement", "Locale, dans le Hub", "Forte, 100 % locale"),
    ("Assistant vocal « Jarvis »", "—", "Oui", "Oui, plusieurs pièces"),
    ("Réceptionniste IA", "—", "Oui", "Oui, plusieurs lignes"),
    ("Automatisations d’entreprise", "—", "Jusqu’à 10", "Illimitées"),
    ("Base de données et rapports", "—", "—", "Oui"),
    ("Lieux reliés (multi-Hubs)", "Suit un Hub principal", "Jusqu’à 3", "Illimité"),
    ("Réseau", "Wi-Fi, Bluetooth, Zigbee", "+ Z-Wave, Matter", "+ 2 ports 2,5 Gb"),
    ("Internet de secours", "—", "Prêt pour 4G", "4G ou Starlink intégré"),
    ("Alimentation de secours", "—", "—", "Batterie interne 2 h"),
    ("Puce de sécurité", "—", "Oui", "Oui, certifiée"),
    ("Boîtier", "Plastique", "Aluminium", "Aluminium, refroidissement silencieux"),
    ("Garantie", "1 an", "2 ans", "3 ans + remplacement express"),
    ("Soutien", "Courriel", "Courriel et téléphone", "Prioritaire, personne dédiée"),
]

SOLUTIONS = [
    {"id": "env", "nom": "Environnements intelligents", "prix": 0, "slug": "environnements-intelligents",
     "pourquoi": "Inclus avec chaque Hub : c’est la base de JARVIS.",
     "pts": ["Lumières, chauffage, stores, foyer, serrures", "Scènes : Matin, Soir, Nuit, Absent", "Énergie pièce par pièce", "Fonctionne sans Internet"]},
    {"id": "diag", "nom": "Diagnostic et continuité", "prix": 15, "slug": "diagnostic-care",
     "pourquoi": "Un dégât d’eau coûte 12 000 $ en moyenne. Ici, vous êtes prévenu à la première goutte.",
     "pts": ["Veille 24/7 : fuite, gel, batterie, panne", "Alertes de partout, avec la cause probable", "Dossier prêt pour le technicien", "Rapport mensuel de santé du lieu"]},
    {"id": "secu", "nom": "Sécurité intelligente", "prix": 20, "slug": "securite-intelligente",
     "pourquoi": "Vos caméras comprennent ce qu’elles voient. Une alerte utile, pas cent notifications.",
     "pts": ["Enregistrement local, rien dans le nuage", "Reconnaît personne, véhicule, animal, colis", "Alertes regroupées en une phrase", "Mode urgence et accès temporaires"]},
    {"id": "ia", "nom": "IA privée et connaissances", "prix": 15, "slug": "ia-privee-connaissances",
     "pourquoi": "Posez une question sur votre lieu ou vos documents. La réponse ne sort jamais de chez vous.",
     "pts": ["Assistant qui connaît votre lieu", "Répond à partir de vos documents, source citée", "Assistant vocal (Signature et Platinum)", "Option IA par Internet avec votre clé"]},
    {"id": "res", "nom": "Réseau et cybersécurité", "prix": 10, "slug": "reseau-resilience",
     "pourquoi": "Un appareil inconnu sur votre réseau est bloqué avant de faire des dégâts.",
     "pts": ["Carte du réseau en direct", "Appareils inconnus détectés et bloqués", "Zones séparées : invités, caméras, travail", "Lien de secours géré automatiquement"]},
    {"id": "mob", "nom": "Mobilité", "prix": 15, "slug": "mobilite", "unite": "par véhicule",
     "pourquoi": "Position, diagnostic et antivol de chaque véhicule. Les données cellulaires sont comprises.",
     "pts": ["Position en direct, historique des trajets", "Diagnostic moteur, pression des pneus", "Alerte de mouvement (antivol)", "Données cellulaires incluses"]},
]
COMPLET = {"id": "complet", "nom": "JARVIS Complet", "prix": 49, "valeur": sum(s["prix"] for s in SOLUTIONS)}

# Entreprise à la carte : socle, réceptionniste par ligne, automatisations une par une.
ENT_SOCLE = {"id": "socle", "nom": "Socle Entreprise", "prix": 29,
             "d": "Comptes employés, journal de tout ce que JARVIS fait, rapport hebdomadaire, connexions à vos outils (courriel, texto, calendrier, comptabilité). 300 textos par mois compris.",
             "pourquoi": "Obligatoire pour toute automatisation : c’est ce qui relie JARVIS à votre entreprise."}
ENT_RECEP = {"id": "recep", "nom": "Réceptionniste IA", "prix": 59, "unite": "par ligne",
             "d": "Répond 24/7 à votre nom, prend les messages et les rendez-vous, transfère les urgences. 300 minutes par ligne comprises, 0,15 $ la minute ensuite.",
             "pourquoi": "Un appel manqué est souvent un client perdu. Elle ne manque jamais un appel."}
ENT_TOUTES = {"id": "toutes", "nom": "Toutes les automatisations", "prix": 149,
              "pourquoi": "Toute la bibliothèque, activée au besoin. Hub Platinum recommandé."}
ENT_MESURE = {"id": "mesure", "nom": "Automatisation sur mesure", "prix": 295, "mois": 19,
              "d": "Vous décrivez le besoin, nous la construisons et la testons. 295 $ une fois, puis 19 $ par mois."}
ENT_USAGE = "Au-delà : minute d’appel 0,15 $ · texto 0,05 $ · ligne supplémentaire = une réceptionniste de plus."
# Trois niveaux de prix : simple 9 $ (un déclencheur, une action), reliée 19 $ (parle à un outil externe), critique 29 $ (veille 24/7, escalade).
AUTOMATISATIONS = [
    ("Réception", [
        ("a_rdv", "Prendre et confirmer un rendez-vous", 19, "Pris dans votre calendrier, confirmé par texto. Fini les doubles réservations."),
        ("a_rappel", "Texter le rappel la veille", 9, "Un rendez-vous manqué, c’est une heure perdue. Le rappel les réduit de moitié."),
        ("a_urgent", "Transférer un appel urgent au bon employé", 19, "Le client en panne tombe sur quelqu’un, pas sur une boîte vocale."),
        ("a_faq", "Répondre aux questions fréquentes", 9, "Heures, prix, adresse : réglé sans vous déranger."),
        ("a_msg", "Prendre les messages et vous les résumer", 9, "Un texto clair au lieu de dix boîtes vocales."),
    ]),
    ("Ventes", [
        ("a_soum", "Envoyer une soumission à partir d’un gabarit", 19, "La soumission part dans l’heure, pendant que le client est chaud."),
        ("a_relance", "Relancer une soumission sans réponse après 3 jours", 9, "Une relance polie ferme une vente sur cinq."),
        ("a_fiche", "Créer la fiche client", 19, "Chaque appel devient un client dans votre outil, sans retaper."),
        ("a_rappelv", "Prévenir le vendeur quand un client rappelle", 9, "Le vendeur rappelle avec le dossier déjà ouvert."),
    ]),
    ("Facturation", [
        ("a_impayee", "Relancer une facture impayée (7, 14, 30 jours)", 19, "Vous êtes payé plus vite sans jouer au mauvais flic."),
        ("a_recu", "Envoyer le reçu après paiement", 9, "Le client a sa preuve, vous n’avez rien fait."),
        ("a_ar", "Comptes à recevoir chaque lundi", 19, "Vous savez qui vous doit quoi avant le café."),
    ]),
    ("Opérations", [
        ("a_bon", "Créer un bon de travail à partir d’une demande", 19, "La demande devient une tâche assignée, avec adresse et photos."),
        ("a_assign", "Assigner au technicien disponible", 19, "Le bon tombe sur la bonne personne, au bon moment."),
        ("a_garde", "Escalader à la personne de garde", 29, "Si personne ne répond en 10 minutes, JARVIS monte d’un niveau."),
        ("a_equip", "Alerte si un équipement critique tombe", 29, "Compresseur, frigo, serveur : vous le savez avant les clients."),
    ]),
    ("Direction", [
        ("a_matin", "Rapport du matin : appels, ventes, alertes", 9, "Une page, à 7 h, et vous savez où en est l’entreprise."),
        ("a_semaine", "Résumé de la semaine le vendredi", 9, "Ce qui a marché, ce qui traîne, ce qui coûte."),
        ("a_ok", "Approbation par texto : « OK » ou « Non »", 19, "Approuvez une dépense ou un congé depuis le chantier."),
    ]),
    ("Ferme et commerce", [
        ("a_frigo", "Alerte de température : frigo, réservoir à lait, étable", 29, "Une chambre froide qui lâche la nuit, c’est des milliers de dollars."),
        ("a_livr", "Journal automatique des livraisons", 9, "Qui est venu, quand, combien de temps : écrit tout seul."),
        ("a_silo", "Commande de moulée quand le silo est bas", 19, "Le fournisseur reçoit la commande avant que ça manque."),
        ("a_porte", "Alerte si une porte reste ouverte", 9, "Entrepôt, étable, garage : fermé quand ça doit l’être."),
        ("a_pompe", "Veille d’une pompe ou d’un abreuvoir", 29, "Débit, courant, vibration : la panne est vue avant le dégât."),
    ]),
]
AUTOS_BY_ID = {a[0]: a for _, items in AUTOMATISATIONS for a in items}

# Matériel : (catégorie, [(id, nom, prix, description, pourquoi, compte_camera)])
MATERIEL = [
    ("Boîtiers JARVIS", [
        ("vrb", "Boîtier VR Base", 490, "12 V. Batteries (shunt), 2 réservoirs, batterie moteur. VR, roulotte, bateau.", "Sans lui, le Hub ne voit ni vos batteries ni vos réservoirs."),
        ("vrs", "Boîtier VR Signature", 890, "Base + 16 sorties (lumières, pompe, chauffage) + 3e réservoir + 4G et GPS.", "Contrôlez le VR de partout, même sur la route."),
        ("vrp", "Boîtier VR Platinum", 1290, "Signature + 2 ports caméras + bus du véhicule (RV-C, NMEA 2000) + secours.", "Le VR ou le bateau au complet, jusqu’au moteur."),
        ("mobb", "Boîtier Mobilité", 249, "Port OBD-II, GPS, LTE. Pour voiture ou camion, sans Hub dans l’auto.", "Position, antivol et diagnostic de chaque véhicule."),
        ("ecr10", "Écran JARVIS 10 po", 549, "Tactile, micro et haut-parleur : contrôle sur place, assistant vocal, interphone.", "Pour la famille ou les employés, sans sortir le téléphone."),
        ("ecr7", "Écran JARVIS 7 po", 349, "Version compacte pour une chambre, un VR ou un bureau.", "Le même contrôle, dans un petit espace."),
        ("sec", "Boîtier Secours", 299, "Garde le Hub et le routeur allumés 8 h pendant une panne.", "Pendant la panne, c’est là que vous avez besoin d’alertes."),
    ]),
    ("Capteurs", [
        ("fuite", "Fuite d’eau", 59, "Sous l’évier, près du chauffe-eau, au sous-sol. À pile.", "47 % des réclamations habitation au Québec sont des dégâts d’eau."),
        ("vanne", "Vanne d’eau automatique", 349, "Se pose sur votre vanne d’entrée. Ferme l’eau dès qu’une fuite est détectée.", "Fermer l’eau en 10 secondes, c’est la différence entre une serviette et un sous-sol."),
        ("temp", "Température et humidité", 39, "Intérieur, extérieur, soute, frigo. Alerte de gel. À pile.", "Un tuyau gelé au chalet se découvre au printemps. Trop tard."),
        ("porte", "Porte et fenêtre", 49, "Ouvert ou fermé, alerte en votre absence. À pile.", "Savoir que la porte du garage est restée ouverte."),
        ("radar", "Présence (radar)", 79, "Détecte une personne même immobile.", "Les lumières ne s’éteignent plus quand vous lisez."),
        ("fumee", "Fumée et CO", 129, "Relié à JARVIS : alerte partout, lumières, sirène.", "Un détecteur qui sonne dans une maison vide ne sert à rien."),
        ("propane", "Propane", 149, "Niveau de la bonbonne et détection de fuite.", "Plus jamais de bonbonne vide un samedi soir."),
        ("reserv", "Niveau de réservoir", 120, "Eau potable, grise, noire, carburant. Collé sous le réservoir.", "Le niveau exact, pas « à peu près la moitié »."),
        ("pneus", "Pression des pneus (4)", 249, "Alerte de crevaison et de surchauffe.", "Un pneu de VR qui éclate à 100 km/h."),
        ("energie", "Compteur d’énergie", 189, "Consommation en direct, par circuit ou pour tout le lieu.", "Voir ce qui coûte cher avant la facture d’Hydro."),
        ("univ", "Capteur universel", 89, "Pince ampèremétrique, pression, débit, vibration. Pour une pompe, un silo.", "Surveiller n’importe quoi qui tourne, chauffe ou coule."),
    ]),
    ("Caméras et accès", [
        ("camext", "Caméra extérieure", 299, "4K, vision de nuit couleur, alimentée par câble réseau.", "Voir qui est là, de nuit, en couleur. Enregistré chez vous."),
        ("camint", "Caméra intérieure", 179, "2K, discrète, micro, obturateur de confidentialité.", "Un œil à l’intérieur, que vous fermez quand vous êtes là."),
        ("cam360", "Caméra 360° (dôme)", 399, "Stationnement, entrepôt, cour.", "Une caméra au lieu de quatre."),
        ("sonnette", "Sonnette vidéo", 249, "Reconnaît visiteurs et colis, répond de partout.", "Le colis est livré, le livreur est parti : vous le savez."),
        ("plaques", "Lecteur de plaques", 599, "Véhicule connu, inconnu, refusé. Ouvre la barrière aux connus.", "La barrière s’ouvre pour vous, pas pour les autres."),
        ("serrure", "Serrure intelligente", 349, "Déverrouiller par cellulaire, codes invités.", "Un code pour le locataire, effacé quand il part."),
        ("clavier", "Clavier et lecteur de badges", 249, "Entrée d’entreprise ou de garage, badges et codes QR.", "Qui est entré, à quelle heure, avec quel badge."),
        ("inter", "Interphone vidéo", 399, "Parler au visiteur et ouvrir de partout.", "Le livreur est reçu même si vous êtes à Montréal."),
        ("sirene", "Sirène et stroboscope", 99, "Pour le mode urgence.", "Faire fuir avant que ça entre."),
        ("urgence", "Bouton d’urgence", 49, "Lumières, sirène, enregistrement, appel aux contacts.", "Un geste, et tout le lieu réagit."),
    ]),
    ("Confort et réseau", [
        ("thermo", "Thermostat intelligent", 189, "Chauffage ou climatisation par pièce. Compatible plinthes du Québec.", "Chauffer les pièces où vous êtes, pas la maison entière."),
        ("inter2", "Interrupteur ou gradateur", 89, "Remplace l’interrupteur existant. Par électricien.", "Vos lumières existantes deviennent intelligentes."),
        ("prise", "Prise intelligente", 35, "Lampe, pompe, chauffe-moteur.", "Le chauffe-moteur part à 5 h, pas toute la nuit."),
        ("ampoule", "Ampoule couleur", 29, "Scènes et ambiances.", "La scène Soir, d’un mot."),
        ("del", "Bande DEL (2 m)", 59, "Ambiance, escalier, comptoir.", "L’escalier s’allume doucement la nuit."),
        ("store", "Moteur de store", 199, "Selon l’heure et le soleil.", "Le store descend quand le soleil tape."),
        ("relais", "Relais foyer ou garage", 89, "Allumer le foyer ou ouvrir le garage, avec confirmation.", "Le foyer est allumé quand vous arrivez au chalet."),
        ("poe", "Switch PoE 8 ports", 249, "Alimente caméras et téléphones par câble réseau.", "Un seul câble par caméra : courant et réseau."),
        ("r4g", "Routeur 4G/5G", 399, "Internet cellulaire : chalet, VR, ferme.", "Internet là où il n’y en a pas."),
        ("starlink", "Starlink Mini", 549, "Internet par satellite, partout. Prix du fabricant plus l’intégration.", "Le VR connecté au fond du bois."),
        ("telip", "Téléphone IP", 149, "Pour la réceptionniste IA et les transferts.", "La réceptionniste vous passe l’appel sur un vrai téléphone."),
    ]),
]
MAT_BY_ID = {m[0]: m for _, items in MATERIEL for m in items}
CAMERAS = {"camext", "camint", "cam360", "sonnette", "plaques", "inter"}

INSTALL = [
    ("auto", "Je l’installe moi-même", 0, "Inclus", "Prises identifiées, aucun fil à couper. Plan, vidéo et mise en service à distance (30 min)."),
    ("guide", "Mise en service guidée", 149, "149 $", "Un technicien vous accompagne en vidéo pendant l’installation."),
    ("place", "JARVIS s’en occupe", 330, "dès 330 $", "Sur place : 110 $ l’heure, minimum 3 h. Déplacement en sus. Le panier compte 3 h."),
    ("visite", "Visite de planification", 0, "Gratuite", "Domaine, entreprise, ferme : inventaire, plan écrit, soumission ligne par ligne."),
]
INCLUS = [
    ("Configuration pour votre lieu", "Vos appareils déjà jumelés, vos scènes de base prêtes."),
    ("Test d’une heure", "Chaque kit tourne une heure sur banc avant l’envoi."),
    ("Mises à jour automatiques", "Signées, la nuit, avec retour arrière."),
    ("Sauvegarde chiffrée", "Si le Hub brise, le nouveau repart comme avant."),
    ("Garantie", "1 an Base, 2 ans Signature, 3 ans Platinum. Garantie légale du Québec en plus."),
    ("Retour 30 jours", "Matériel non installé : remboursé, moins la configuration."),
]

# Kits : prix calculé à partir des pièces, moins 8 %. "sol" = solutions ; "ent" = socle, recep (nb lignes), autos.
KIT_RABAIS = 0.08
KITS = [
    {"nom": "Kit VR Essentiel", "pour": "Roulotte, petit VR, bateau de 25 pi", "pourquoi": "Batteries, réservoirs, gel et porte : les quatre choses qui gâchent un voyage.",
     "hub": "base", "mat": {"vrb": 1, "temp": 2, "porte": 1, "fuite": 1}, "sol": ["diag", "mob"]},
    {"nom": "Kit VR Complet", "pour": "VR de classe A ou C, cinquième roue", "pourquoi": "Le VR au complet dans la poche : contrôle, caméra, écran, propane, et JARVIS Complet.",
     "hub": "signature", "mat": {"vrs": 1, "temp": 4, "porte": 2, "fuite": 1, "propane": 1, "camint": 1, "ecr7": 1}, "sol": ["complet"]},
    {"nom": "Kit Chalet", "pour": "Chalet fermé l’hiver, sans Internet", "pourquoi": "Gel, fuite, intrusion : prévenu avant que le plancher lève au printemps.",
     "hub": "base", "mat": {"temp": 3, "fuite": 2, "porte": 2, "r4g": 1, "prise": 1}, "sol": ["diag"]},
    {"nom": "Kit Maison", "pour": "Maison familiale, condo", "pourquoi": "L’eau coupée toute seule, la sonnette qui reconnaît, l’IA chez vous.",
     "hub": "signature", "mat": {"fuite": 3, "vanne": 1, "porte": 3, "radar": 2, "sonnette": 1, "thermo": 1}, "sol": ["complet"]},
    {"nom": "Kit Maison Sécurité", "pour": "Maison en coin de rue, absences fréquentes", "pourquoi": "Le Kit Maison, plus trois caméras qui comprennent ce qu’elles voient et une serrure.",
     "hub": "signature", "mat": {"fuite": 3, "vanne": 1, "porte": 3, "radar": 2, "sonnette": 1, "thermo": 1, "camext": 3, "poe": 1, "sirene": 1, "serrure": 1}, "sol": ["complet"]},
    {"nom": "Kit PME", "pour": "Garage, clinique, bureau de 2 à 10 employés", "pourquoi": "Une réceptionniste qui ne manque aucun appel et trois automatisations qui font gagner une heure par jour.",
     "hub": "signature", "mat": {"telip": 2, "camext": 2, "camint": 1, "poe": 1, "clavier": 1}, "sol": ["res"],
     "ent": {"socle": True, "recep": 1, "autos": ["a_rdv", "a_rappel", "a_faq"]}},
    {"nom": "Kit Domaine", "pour": "Grande propriété, terrain, dépendances", "pourquoi": "Caméras, plaques, serrures, eau et secours : rien n’entre, rien ne coule, rien ne s’arrête.",
     "hub": "platinum", "mat": {"camext": 6, "plaques": 1, "serrure": 2, "inter": 1, "fuite": 4, "vanne": 1, "poe": 1, "sec": 1, "ecr10": 1}, "sol": ["complet"]},
    {"nom": "Kit Ferme", "pour": "Ferme laitière, érablière, serre", "pourquoi": "Frigo, réservoir à lait, pompes, silo : les alertes qui sauvent une récolte ou un troupeau.",
     "hub": "platinum", "mat": {"r4g": 1, "camext": 4, "temp": 6, "univ": 4, "sec": 1, "energie": 1}, "sol": ["complet"],
     "ent": {"socle": True, "autos": ["a_frigo", "a_silo", "a_pompe"]}},
]


def _p(n):
    return f"{n:,}".replace(",", " ") + " $"


def _kit_totaux(k):
    once_plein = HUB_BY_ID[k["hub"]]["prix"] + sum(MAT_BY_ID[i][2] * q for i, q in k["mat"].items())
    once = int(round(once_plein * (1 - KIT_RABAIS) / 10.0) * 10)
    mois = 0
    if "complet" in k["sol"]:
        mois += COMPLET["prix"]
    else:
        mois += sum(s["prix"] for s in SOLUTIONS if s["id"] in k["sol"])
    e = k.get("ent") or {}
    if e.get("socle"):
        mois += ENT_SOCLE["prix"]
    mois += ENT_RECEP["prix"] * e.get("recep", 0)
    mois += sum(AUTOS_BY_ID[a][2] for a in e.get("autos", []))
    return once_plein, once, mois


def _hubs():
    out = []
    for h in HUBS:
        pts = "".join(f"<li>{escape(p)}</li>" for p in h["pts"])
        manque = "".join(f"<li>{escape(p)}</li>" for p in h["manque"])
        manque_html = f'<p class="ct-k ct-k-no">Ce qui manque</p><ul class="ct-no">{manque}</ul>' if manque else ""
        tag = f'<span class="ct-tag">{escape(h["tag"])}</span>' if h["tag"] else ""
        out.append(f"""<label class="ct-hub" data-rev data-hub="{h['id']}">
      <input type="radio" name="hub" value="{h['id']}" data-prix="{h['prix']}" data-cam="{h['cam']}" data-app="{h['app']}" data-autos="{h['autos']}"{' checked' if h['id'] == 'signature' else ''}>
      <span class="ct-check" aria-hidden="true"></span>
      {tag}
      <figure class="ct-hub-ph"><img src="/media/product/jarvis-hub-v1.webp" alt="" loading="lazy" decoding="async"></figure>
      <h3>{escape(h['nom'])}</h3>
      <p class="ct-prix">{_p(h['prix'])}<small>une fois</small></p>
      <p class="ct-pour">{escape(h['pour'])}</p>
      <p class="ct-why">{escape(h['pourquoi'])}</p>
      <p class="ct-k">Ce que vous avez</p>
      <ul class="ct-oui">{pts}</ul>
      {manque_html}
    </label>""")
    return "".join(out)


def _compare():
    rows = []
    for lab, *vals in COMPARE:
        cells = "".join(
            '<td><i class="ct-dot" aria-label="Non disponible"></i></td>' if v == "—" else f"<td>{escape(v)}</td>"
            for v in vals
        )
        rows.append(f"<tr><th scope=\"row\">{escape(lab)}</th>{cells}</tr>")
    heads = "".join(f'<th{" class=is-mid" if h["id"] == "signature" else ""}>{escape(h["nom"])}<small>{_p(h["prix"])}</small></th>' for h in HUBS)
    return f"""<div class="ct-cmp-w"><table class="ct-cmp">
      <thead><tr><th></th>{heads}</tr></thead>
      <tbody>{"".join(rows)}</tbody></table></div>
    <p class="ct-note"><i class="ct-dot"></i> Non disponible sur ce Hub. Les capacités sont des repères; elles dépendent aussi des caméras et des solutions actives.</p>"""


def _solutions():
    out = []
    for s in SOLUTIONS:
        pts = "".join(f"<li>{escape(p)}</li>" for p in s["pts"])
        inclus = s["prix"] == 0
        prix = "Inclus" if inclus else f"{s['prix']} $<small>/mois{' ' + s['unite'] if s.get('unite') else ''}</small>"
        if s.get("unite"):
            inp = f'<input type="checkbox" name="sol" value="{s["id"]}" data-prix="{s["prix"]}" data-qty="1">'
            qty = '<div class="ct-qty ct-qty-sol"><button type="button" data-q="-1" aria-label="Un véhicule de moins">−</button><output>0</output><button type="button" data-q="1" aria-label="Un véhicule de plus">+</button><span>véhicule(s)</span></div>'
        else:
            inp = f'<input type="checkbox" name="sol" value="{s["id"]}" data-prix="{s["prix"]}"{" checked disabled" if inclus else ""}>'
            qty = ""
        out.append(f"""<label class="ct-sol{' is-inclus' if inclus else ''}" data-rev data-sol="{s['id']}">
      {inp}<span class="ct-check" aria-hidden="true"></span>
      <div class="ct-sol-h"><h3>{escape(s['nom'])}</h3><p class="ct-prix">{prix}</p></div>
      <p class="ct-why">{escape(s['pourquoi'])}</p>
      <ul class="ct-oui">{pts}</ul>
      {qty}
      <a href="/solutions/{s['slug']}/">Voir la solution <i aria-hidden="true">→</i></a>
    </label>""")
    return "".join(out)


def _entreprise():
    socle = f"""<label class="ct-ent ct-ent-socle" data-rev>
      <input type="checkbox" name="socle" value="socle" data-prix="{ENT_SOCLE['prix']}"><span class="ct-check" aria-hidden="true"></span>
      <h3>{escape(ENT_SOCLE['nom'])}</h3><p class="ct-prix">{ENT_SOCLE['prix']} $<small>/mois</small></p>
      <p class="ct-why">{escape(ENT_SOCLE['pourquoi'])}</p><p class="ct-d">{escape(ENT_SOCLE['d'])}</p>
    </label>"""
    recep = f"""<div class="ct-ent ct-ent-recep" data-rev data-id="recep" data-prix="{ENT_RECEP['prix']}">
      <h3>{escape(ENT_RECEP['nom'])}</h3><p class="ct-prix">{ENT_RECEP['prix']} $<small>/mois {ENT_RECEP['unite']}</small></p>
      <p class="ct-why">{escape(ENT_RECEP['pourquoi'])}</p><p class="ct-d">{escape(ENT_RECEP['d'])}</p>
      <div class="ct-qty"><button type="button" data-q="-1" aria-label="Une ligne de moins">−</button><output>0</output><button type="button" data-q="1" aria-label="Une ligne de plus">+</button><span>ligne(s)</span></div>
    </div>"""
    toutes = f"""<label class="ct-ent ct-ent-toutes" data-rev>
      <input type="checkbox" name="toutes" value="toutes" data-prix="{ENT_TOUTES['prix']}"><span class="ct-check" aria-hidden="true"></span>
      <span class="ct-tag">Tout inclus</span>
      <h3>{escape(ENT_TOUTES['nom'])}</h3><p class="ct-prix">{ENT_TOUTES['prix']} $<small>/mois</small></p>
      <p class="ct-why">{escape(ENT_TOUTES['pourquoi'])}</p><p class="ct-d">Les {len(AUTOS_BY_ID)} automatisations de la bibliothèque, plus celles qui s’ajoutent chaque mois.</p>
    </label>"""
    mesure = f"""<div class="ct-ent ct-ent-mesure" data-rev data-id="mesure" data-prix="{ENT_MESURE['prix']}" data-mois="{ENT_MESURE['mois']}">
      <h3>{escape(ENT_MESURE['nom'])}</h3><p class="ct-prix">{ENT_MESURE['prix']} $<small>une fois + {ENT_MESURE['mois']} $/mois</small></p>
      <p class="ct-d">{escape(ENT_MESURE['d'])}</p>
      <div class="ct-qty"><button type="button" data-q="-1" aria-label="Une de moins">−</button><output>0</output><button type="button" data-q="1" aria-label="Une de plus">+</button></div>
    </div>"""
    cats = []
    for cat, items in AUTOMATISATIONS:
        rows = "".join(f"""<label class="ct-auto" data-id="{i}">
          <input type="checkbox" name="auto" value="{i}" data-prix="{p}"><span class="ct-check ct-check-sm" aria-hidden="true"></span>
          <span class="ct-auto-t"><b>{escape(n)}</b><em>{escape(w)}</em></span>
          <span class="ct-auto-p">{p} $<small>/mois</small></span>
        </label>""" for i, n, p, w in items)
        cats.append(f'<section class="ct-autocat" data-rev><h4>{escape(cat)}</h4>{rows}</section>')
    return f"""<div class="ct-ents">{socle}{recep}{toutes}</div>
    <h3 class="ct-sub" data-rev>La bibliothèque d’automatisations <em>· cochez celles qu’il vous faut, elles s’ajoutent au panier</em></h3>
    <p class="ct-note ct-note-prix" data-rev><b>9 $</b> un déclencheur, une action · <b>19 $</b> reliée à un de vos outils · <b>29 $</b> veille 24/7 avec escalade. Toutes demandent le Socle Entreprise et un Hub Signature ou Platinum.</p>
    <div class="ct-autos">{"".join(cats)}</div>
    <div class="ct-ents ct-ents-bas">{mesure}</div>
    <p class="ct-note">{escape(ENT_USAGE)}</p>"""


def _materiel():
    out = []
    for cat, items in MATERIEL:
        rows = "".join(f"""<div class="ct-item" data-id="{i}" data-prix="{p}"{' data-cam="1"' if i in CAMERAS else ''}>
        <div class="ct-item-t"><b>{escape(n)}</b><span>{escape(d)}</span><em>{escape(w)}</em></div>
        <div class="ct-item-p">{_p(p)}</div>
        <div class="ct-qty"><button type="button" data-q="-1" aria-label="Retirer">−</button><output>0</output><button type="button" data-q="1" aria-label="Ajouter">+</button></div>
      </div>""" for i, n, p, d, w in items)
        out.append(f'<section class="ct-cat" data-rev><h3>{escape(cat)}</h3>{rows}</section>')
    return "".join(out)


def _kits():
    out = []
    for k in KITS:
        plein, once, mois = _kit_totaux(k)
        hub = HUB_BY_ID[k["hub"]]
        pieces = [f"<li><b>1×</b> {escape(hub['nom'])}</li>"] + [
            f"<li><b>{q}×</b> {escape(MAT_BY_ID[i][1])}</li>" for i, q in k["mat"].items()]
        mens = []
        if "complet" in k["sol"]:
            mens.append(f"JARVIS Complet ({COMPLET['prix']} $)")
        else:
            mens += [f"{s['nom']} ({s['prix']} $)" for s in SOLUTIONS if s["id"] in k["sol"]]
        e = k.get("ent") or {}
        if e.get("socle"):
            mens.append(f"Socle Entreprise ({ENT_SOCLE['prix']} $)")
        if e.get("recep"):
            mens.append(f"Réceptionniste IA × {e['recep']} ({ENT_RECEP['prix'] * e['recep']} $)")
        for a in e.get("autos", []):
            mens.append(f"{AUTOS_BY_ID[a][1]} ({AUTOS_BY_ID[a][2]} $)")
        cfg = {"nom": k["nom"], "rabais": plein - once, "hub": k["hub"], "mat": k["mat"], "sol": k["sol"], "ent": e}
        out.append(f"""<article class="ct-kit" data-rev>
      <div class="ct-kit-h"><h3>{escape(k['nom'])}</h3><p class="ct-pour">{escape(k['pour'])}</p></div>
      <p class="ct-prix">{_p(once)}<small>une fois</small></p>
      <p class="ct-econ"><s>{_p(plein)}</s> à la pièce · vous économisez {_p(plein - once)}</p>
      <p class="ct-mois">{mois} $/mois<small> · {escape(" + ".join(mens))}</small></p>
      <p class="ct-why">{escape(k['pourquoi'])}</p>
      <details class="ct-kit-d"><summary>Ce qu’il y a dans la boîte ({1 + sum(k['mat'].values())} pièces)</summary><ul>{"".join(pieces)}</ul></details>
      <button type="button" class="pill" data-kit='{json.dumps(cfg, ensure_ascii=False)}'>Partir de ce kit</button>
    </article>""")
    return "".join(out)


def _install():
    return "".join(f"""<label class="ct-inst card" data-rev>
      <input type="radio" name="install" value="{i}" data-prix="{p}"{' checked' if i == 'auto' else ''}><span class="ct-check" aria-hidden="true"></span>
      <small>{escape(aff)}</small><h3>{escape(n)}</h3><p>{escape(d)}</p>
    </label>""" for i, n, p, aff, d in INSTALL)


def _inclus():
    return "".join(f'<li data-rev><b>{escape(n)}</b><span>{escape(d)}</span></li>' for n, d in INCLUS)


PAGE = {
    "url": "/catalogue/",
    "v2": True,
    "title": "Catalogue JARVIS | Hubs, solutions, matériel et prix",
    "description": "Choisissez votre Hub, vos solutions et le matériel de votre lieu. Prix clairs, panier détaillé, kits prêts à partir.",
    "og_image": "/media/offre/maison.webp",
    "assets": ["catalogue"],
    "content": f"""
<section class="band top ct-top">
  <div class="bg"><img src="/media/solutions/jarvis-spaces-property-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Catalogue</p>
    <h1 data-rev>Un Hub. Vos solutions.<br><em>Rien de plus.</em></h1>
    <p class="lead" data-rev>Composez votre JARVIS en quatre étapes. Chaque ligne s’ajoute au panier, à droite. Vos données restent chez vous.</p>
    <ol class="of-trois" data-rev>
      <li><a href="#hub"><i>1</i>Le Hub</a></li>
      <li><a href="#solutions"><i>2</i>Vos solutions</a></li>
      <li><a href="#materiel"><i>3</i>Le matériel</a></li>
      <li><a href="#lieux"><i>4</i>Lieux et installation</a></li>
    </ol>
  </div>
</section>

<form id="ct" class="ct" novalidate>
<div class="ct-wrap">
<div class="ct-main">

<section class="sect" id="hub" data-toc="1 · Le Hub" aria-labelledby="hub-t">
  <div class="sect-head"><div data-rev><p class="of-num"><i>1</i><span>Étape 1 sur 4</span></p>
    <h2 id="hub-t">Choisissez votre Hub.<br><em>Selon la taille de votre lieu.</em></h2></div>
    <p data-rev>Même logiciel, même app, mêmes solutions. Ce qui change : la puissance, le nombre d’appareils, l’IA et la sécurité. Payé une fois. Le panier vous dira si votre Hub devient trop petit.</p></div>
  <div class="ct-hubs">{_hubs()}</div>
  <details class="ct-details" data-rev><summary>Comparer les trois Hubs en détail</summary>{_compare()}</details>
  <div class="ct-inclus-hub" data-rev><b>Dans chaque Hub :</b> la solution Environnements intelligents, l’app JARVIS, les comptes et droits, les mises à jour signées, les sauvegardes chiffrées.</div>
</section>

<section class="sect alt" id="solutions" data-toc="2 · Vos solutions" aria-labelledby="sol-t">
  <div class="sect-head"><div data-rev><p class="of-num"><i>2</i><span>Étape 2 sur 4</span></p>
    <h2 id="sol-t">Choisissez vos solutions.<br><em>Comme des apps.</em></h2></div>
    <p data-rev>Par mois, annulables en tout temps. Chaque solution payante inclut l’accès de partout et les alertes sur votre téléphone. Sans elles, JARVIS fonctionne quand même chez vous.</p></div>
  <div class="ct-sols">{_solutions()}</div>
  <label class="ct-complet" data-rev>
    <input type="checkbox" name="complet" value="complet" data-prix="{COMPLET['prix']}"><span class="ct-check" aria-hidden="true"></span>
    <span class="ct-tag">Meilleure valeur</span>
    <div><h3>{COMPLET['nom']} · {COMPLET['prix']} $/mois</h3><p>Les cinq solutions payantes, Mobilité pour un véhicule comprise. Valeur à la carte : {COMPLET['valeur']} $/mois.</p></div>
  </label>
  <h3 class="ct-sub" id="entreprise" data-rev>Pour une entreprise <em>· une réceptionniste IA et des automatisations à la carte</em></h3>
  <p class="ct-intro" data-rev>Tout est à l’unité et payable par mois. Vous commencez avec le Socle et une automatisation; vous en ajoutez quand vous en voyez le gain. Demande un Hub Signature ou Platinum.</p>
  {_entreprise()}
</section>

<section class="sect" id="materiel" data-toc="3 · Le matériel" aria-labelledby="mat-t">
  <div class="sect-head"><div data-rev><p class="of-num"><i>3</i><span>Étape 3 sur 4</span></p>
    <h2 id="mat-t">Ajoutez le matériel<br><em>de votre lieu.</em></h2></div>
    <p data-rev>Payé une fois. Prêt à brancher : chaque appareil apparaît tout seul dans l’app. Déjà du Victron, de l’UniFi, des caméras ONVIF, un NAS ou Starlink? JARVIS s’y branche au lieu de les remplacer.</p></div>
  <div class="ct-kits-h" data-rev><h3 class="ct-sub">Pressé? <em>Partez d’un kit (−8 %), puis ajustez pièce par pièce.</em></h3></div>
  <div class="ct-kits">{_kits()}</div>
  <h3 class="ct-sub" data-rev>À la pièce <em>· la raison d’être de chaque appareil est écrite dessous</em></h3>
  <div class="ct-mats">{_materiel()}</div>
</section>

<section class="sect alt" id="lieux" data-toc="4 · Lieux et installation" aria-labelledby="lieux-t">
  <div class="sect-head"><div data-rev><p class="of-num"><i>4</i><span>Étape 4 sur 4</span></p>
    <h2 id="lieux-t">Plusieurs lieux?<br><em>Une seule app.</em></h2></div>
    <p data-rev>Un Hub par lieu. Les lieux se parlent par un lien privé et chiffré. Les petits lieux empruntent l’IA de votre plus gros Hub. Les solutions sont à 30 % de rabais dès le deuxième lieu.</p></div>
  <div class="ct-lieux" data-rev>
    <label>Ce lieu est mon <select name="rang"><option value="1">premier lieu JARVIS</option><option value="2">deuxième lieu ou plus (−30 % sur les solutions)</option></select></label>
  </div>
  <h3 class="ct-sub" data-rev>Installation <em>· à vous de choisir</em></h3>
  <div class="cards ct-install">{_install()}</div>
  <h3 class="ct-sub" data-rev>Toujours inclus</h3>
  <ul class="ct-inclus">{_inclus()}</ul>
</section>

</div>

<aside class="ct-cart" aria-label="Votre panier">
  <div class="ct-cart-in">
    <div class="ct-cart-h"><small>Votre JARVIS</small><b data-cart-nom>Hub Signature</b><button type="button" class="ct-cart-x" data-cart-close aria-label="Fermer le détail">×</button></div>
    <div class="ct-cart-body">
      <section class="ct-cart-g"><h4>Une fois <span data-cart-once-sub></span></h4><ul data-cart-once></ul></section>
      <section class="ct-cart-g"><h4>Par mois <span data-cart-month-sub></span></h4><ul data-cart-month></ul></section>
      <div class="ct-cart-tips" data-cart-tips hidden></div>
    </div>
    <div class="ct-cart-tot">
      <div><small>Aujourd’hui</small><b data-total-once>1 290 $</b></div>
      <div><small>Par mois</small><b data-total-month>0 $</b></div>
      <div class="ct-cart-an"><small>Première année</small><b data-total-year>1 290 $</b></div>
    </div>
    <a class="pill" href="/contact/" data-total-link>Obtenir ma soumission</a>
    <p class="ct-cart-note">Dollars canadiens, taxes en sus. Soumission confirmée par écrit, ligne par ligne. Rien à payer ici.</p>
  </div>
</aside>

<div class="ct-bar" aria-live="polite">
  <div><small>Aujourd’hui</small><b data-total-once>1 290 $</b></div>
  <div><small>Par mois</small><b data-total-month>0 $</b></div>
  <button type="button" class="pill ghost" data-cart-open>Voir le panier<span data-cart-count></span></button>
</div>
</div>
</form>

<section class="sect" id="pourquoi" data-toc="Pourquoi" aria-labelledby="pq-t">
  <div class="sect-head"><div data-rev><p class="eyebrow">Pourquoi JARVIS</p>
    <h2 id="pq-t">Vous prévient<br><em>avant que ça coûte cher.</em></h2></div>
    <p data-rev>Au Québec, 47 % des réclamations d’assurance habitation sont des dégâts d’eau, à 12 000 $ en moyenne. Seulement 9 % des gens ont un système qui les prévient. JARVIS Diagnostic : 15 $ par mois.</p></div>
  <div class="cards ct-faits">
    <article class="card" data-rev><b class="ct-big">47 %</b><p>des réclamations d’assurance habitation au Québec sont des dégâts d’eau. (BAC)</p></article>
    <article class="card" data-rev><b class="ct-big">12 000 $</b><p>coût moyen d’une réclamation pour dégât d’eau. (BAC)</p></article>
    <article class="card" data-rev><b class="ct-big">9 %</b><p>des gens ont un système qui détecte les fuites et les prévient. (Chubb)</p></article>
  </div>
  <p class="ct-legal" data-rev>Prix en dollars canadiens, taxes en sus. Points de départ : chaque soumission est confirmée par écrit, ligne par ligne. Les capacités des Hubs sont des repères.</p>
</section>
""",
}
