# L'offre JARVIS (page /offre/) : trois étapes, selon docs/OFFRE.md.
#   1) Vos lieux : cinq familles (src/lieux.py); « Votre écosystème » montre un cerveau par lieu.
#   2) Votre niveau : Base, Signature ou Platinum, un seul pour tous les lieux (NIVEAUX).
#   3) Votre projet : les extensions, l'équipement proposé par lieu (ENSEMBLES), les données, l'installation.
# Le client ne décide que ses lieux et son niveau; le reste est proposé, puis ajusté.
# Tous les prix vivent ici (cachés tant que SITE["prix_publics"] est faux).
# Styles : assets/demos/catalogue.css · Script : assets/demos/catalogue.js

from html import escape
import os
import lieux
import pro
import json

HUBS = [
    {"id": "base", "nom": "Hub Base", "prix": 590, "pour": "Chalet, condo, petit VR",
     "tag": "", "cam": 2, "app": 30, "autos": 0,
     "pourquoi": "Pour veiller sur un lieu simple : fuite, gel, porte, batterie. L’IA passe par Internet.",
     "pts": ["Jusqu’à 30 appareils", "2 caméras analysées, 7 jours d’enregistrement", "IA par Internet seulement",
             "Wi-Fi, Bluetooth, Zigbee", "Garantie 1 an, soutien par courriel"],
     "manque": ["Pas d’IA dans le Hub", "Pas d’assistant vocal ni de réceptionniste", "Pas d’automatisations d’entreprise", "Pas de batterie de secours"]},
    {"id": "signature", "nom": "Hub Signature", "prix": 1290, "pour": "Maison, VR complet, PME",
     "tag": "Pour la plupart des maisons", "cam": 6, "app": 100, "autos": 10,
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
     "pts": ["Lumières, chauffage, stores, foyer, serrures", "Scènes : Matin, Soir, Nuit, Absent", "Énergie pièce par pièce", "Fonctionne sans Internet"],
     "non": ["Pas d’accès de partout ni d’alertes sans une solution payante"]},
    {"id": "diag", "nom": "Diagnostic & continuité", "prix": 15, "slug": "diagnostic-care",
     "pourquoi": "Un dégât d’eau coûte 12 000 $ en moyenne. Ici, vous êtes prévenu à la première goutte.",
     "pts": ["Veille 24/7 : fuite, gel, batterie, panne", "Alertes de partout, avec la cause probable", "Dossier prêt pour le technicien", "Rapport mensuel de santé du lieu"],
     "non": ["Ne ferme pas l’eau sans la vanne automatique", "Ne remplace pas un plombier ou un électricien"]},
    {"id": "secu", "nom": "Sécurité intelligente", "prix": 20, "slug": "securite-intelligente",
     "pourquoi": "Vos caméras comprennent ce qu’elles voient. Une alerte utile, pas cent notifications.",
     "pts": ["Enregistrement local, rien dans le nuage", "Reconnaît personne, véhicule, animal, colis", "Alertes regroupées en une phrase", "Mode urgence et accès temporaires"],
     "non": ["Pas de centrale d’alarme ni d’agents : c’est vous qu’on prévient", "Demande au moins une caméra ou une sonnette"]},
    {"id": "ia", "nom": "IA privée et connaissances", "prix": 15, "slug": "ia-privee-connaissances",
     "pourquoi": "Posez une question sur votre lieu ou vos documents. La réponse ne sort jamais de chez vous.",
     "pts": ["Assistant qui connaît votre lieu", "Répond à partir de vos documents, source citée", "Assistant vocal (Signature et Platinum)", "Option IA par Internet avec votre clé"],
     "non": ["Sur un Hub Base, l’IA passe par Internet", "N’envoie jamais vos documents à un service externe sans votre clé"]},
    {"id": "res", "nom": "Réseau et cybersécurité", "prix": 10, "slug": "reseau-resilience",
     "pourquoi": "Un appareil inconnu sur votre réseau est bloqué avant de faire des dégâts.",
     "pts": ["Carte du réseau en direct", "Appareils inconnus détectés et bloqués", "Zones séparées : invités, caméras, travail", "Lien de secours géré automatiquement"],
     "non": ["Ne fournit pas Internet : routeur 4G ou Starlink à part", "Pas un antivirus pour vos ordinateurs"]},
    {"id": "mob", "nom": "Mobilité", "prix": 15, "slug": "mobilite", "unite": "par véhicule",
     "pourquoi": "Position, diagnostic et antivol de chaque véhicule. Les données cellulaires sont comprises.",
     "pts": ["Position en direct, historique des trajets", "Diagnostic moteur, pression des pneus", "Alerte de mouvement (antivol)", "Données cellulaires incluses"],
     "non": ["Demande un Boîtier Mobilité ou un Boîtier VR Signature/Platinum", "Ne bloque pas le véhicule à distance"]},
]

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
# Entretien et veille : le contrat mensuel des entreprises (mises à jour, surveillance, soutien, rapport).
ENT_VEILLE = [
    ("veille_pme", "Entretien et veille PME", 149, "Mises à jour vérifiées, surveillance du réseau et des caméras, rapport mensuel, 2 heures de soutien par mois, réponse le jour ouvrable suivant.", "Un système qu’on n’entretient pas finit par ne plus protéger."),
    ("veille_pro", "Entretien et veille Pro", 349, "PME + réponse en 4 heures, 6 heures de soutien par mois, revue trimestrielle sur place, personne dédiée.", "Pour une entreprise qui ne peut pas attendre à demain."),
]
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
        ("fuite", "Fuite d’eau", 59, "Sous l’évier, près du chauffe-eau, au sous-sol. À pile.", "Les dégâts d’eau sont la première cause de réclamation en habitation."),
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
        ("inter", "Interphone vidéo", 399, "Parler au visiteur et ouvrir de partout.", "Le livreur est reçu même si vous êtes au travail."),
        ("sirene", "Sirène et stroboscope", 99, "Pour le mode urgence.", "Faire fuir avant que ça entre."),
        ("urgence", "Bouton d’urgence", 49, "Lumières, sirène, enregistrement, appel aux contacts.", "Un geste, et tout le lieu réagit."),
    ]),
    ("Confort et réseau", [
        ("thermo", "Thermostat intelligent", 189, "Chauffage ou climatisation par pièce. Compatible plinthes électriques.", "Chauffer les pièces où vous êtes, pas la maison entière."),
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

# Services professionnels (une fois) : sécurité privée, audits, formation. Sur place ou à distance.
SERVICES = [
    ("Vérifier", [
        ("audit_res", "Vérification de vos systèmes (résidence)", 349, "Caméras, accès, réseau, Wi-Fi, sauvegardes, habitudes : le tour complet de la maison ou du chalet. Rapport écrit avec priorités.", "Savoir ce qui est faible avant que quelqu’un d’autre le trouve."),
        ("audit_ent", "Vérification de vos systèmes (entreprise)", 1490, "Accès, caméras, réseau, postes, sauvegardes, comptes employés. Rapport pour la direction et plan sur 90 jours.", "Une journée de vérification coûte moins qu’une seule panne."),
        ("pentest", "Test d’intrusion réseau", 2990, "Attaque autorisée de votre réseau et de vos services, puis correction avec vous. Rapport et nouvelle vérification.", "La seule façon de savoir si ça tient, c’est d’essayer."),
        ("osint", "Revue de votre exposition en ligne", 890, "Ce qu’Internet dit de vous et de votre entreprise, à partir de sources publiques. Rapport et nettoyage.", "Ce qu’un fraudeur trouverait en une heure, retiré avant lui."),
    ]),
    ("Protéger", [
        ("loi25", "Accompagnement Loi 25", 1990, "Registre, politiques, incidents, consentements : votre entreprise conforme, avec JARVIS comme preuve.", "Les amendes montent à 25 M$. La conformité coûte 1 990 $."),
        ("durcir", "Mise à niveau du réseau", 790, "Zones séparées, mots de passe, mises à jour, sauvegardes testées, caméras isolées. Une journée, puis vérification.", "Le gros des intrusions passe par ce qui n’a jamais été réglé."),
    ]),
    ("Former", [
        ("formation", "Formation d’équipe (demi-journée)", 490, "Vos employés apprennent JARVIS, la réceptionniste et les bons réflexes : hameçonnage, mots de passe, accès.", "Un outil que personne n’utilise ne protège personne."),
        ("formation_fam", "Prise en main à la maison (2 h)", 190, "Toute la famille apprend JARVIS : scènes, alertes, caméras, codes invités.", "Le système sert seulement si tout le monde s’en sert."),
    ]),
]
SERVICES_PLATS = [x for _, items in SERVICES for x in items]

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
    ("Garantie", "1 an Base, 2 ans Signature, 3 ans Platinum. Garantie légale en plus."),
    ("Retour 30 jours", "Matériel non installé : remboursé, moins la configuration."),
]

# Ensembles de départ : ce que JARVIS propose pour chaque lieu (règle 3 de docs/OFFRE.md). Une clé par lieu
# de src/lieux.py. "mat" = pièces du matériel; "ent" = ce qui s'active pour un lieu d'entreprise.
# « vr* » : le Boîtier VR suit le niveau choisi (Base, Signature ou Platinum); résolu par catalogue.js.
# Ce sont des points de départ : chaque pièce s'ajuste, et ce qui existe déjà est réutilisé.
ENSEMBLES = {
    "maison": {"mat": {"fuite": 3, "vanne": 1, "porte": 3, "radar": 2, "sonnette": 1, "thermo": 1},
               "pourquoi": "L’eau coupée toute seule, la sonnette qui reconnaît, le chauffage par pièce."},
    "condo": {"mat": {"fuite": 2, "porte": 1, "radar": 1, "thermo": 1},
              "pourquoi": "L’essentiel d’un condo : l’eau, la porte, le chauffage."},
    "chalet": {"mat": {"temp": 3, "fuite": 2, "porte": 2, "r4g": 1, "prise": 1},
               "pourquoi": "Gel, fuite, intrusion : prévenu avant que le plancher lève au printemps."},
    "domaine": {"mat": {"camext": 6, "plaques": 1, "serrure": 2, "inter": 1, "fuite": 4, "vanne": 1, "poe": 1, "sec": 1, "ecr10": 1},
                "pourquoi": "Caméras, plaques, serrures, eau et secours : rien n’entre, rien ne coule, rien ne s’arrête."},
    "bureau": {"mat": {"telip": 2, "camext": 2, "camint": 1, "poe": 1, "clavier": 1},
               "ent": {"socle": True, "recep": 1, "autos": ["a_rdv", "a_rappel", "a_faq"]},
               "pourquoi": "Une réceptionniste qui ne manque aucun appel, et trois automatisations pour commencer."},
    "atelier": {"mat": {"camext": 2, "cam360": 1, "clavier": 1, "porte": 2, "univ": 2, "poe": 1},
                "pourquoi": "Qui entre et par quelle porte; une machine qui dérive se voit avant le bris."},
    "ferme": {"mat": {"r4g": 1, "camext": 4, "temp": 6, "univ": 4, "sec": 1, "energie": 1},
              "ent": {"socle": True, "autos": ["a_frigo", "a_silo", "a_pompe"]},
              "pourquoi": "Frigo, réservoir à lait, pompes, silo : les alertes qui sauvent une récolte ou un troupeau."},
    "garage": {"mat": {"camext": 2, "clavier": 1, "porte": 2, "temp": 1, "poe": 1},
               "pourquoi": "Chaque entrée avec l’image; l’humidité et la température du bâtiment suivies."},
    "vr": {"mat": {"vr*": 1, "temp": 4, "porte": 2, "fuite": 1, "propane": 1, "camint": 1, "ecr7": 1},
           "pourquoi": "Le VR au complet dans la poche : batteries, réservoirs, propane, caméra et écran à bord."},
    "roulotte": {"mat": {"vr*": 1, "temp": 2, "porte": 1, "fuite": 1},
                 "pourquoi": "Batteries, réservoirs, gel et porte : les quatre choses qui gâchent un voyage."},
    "bateau": {"mat": {"vr*": 1, "temp": 2, "porte": 1, "fuite": 1},
               "pourquoi": "Batteries, cale et accès : l’essentiel, à quai comme en route."},
    "auto": {"mat": {"mobb": 1}, "pourquoi": "Position, diagnostic et antivol, sans Hub à bord."},
    "moto": {"mat": {"mobb": 1}, "pourquoi": "Position et antivol, sans Hub à bord."},
    "flotte": {"mat": {"mobb": 2}, "pourquoi": "Un boîtier par véhicule : ajustez le nombre à votre flotte."},
    "avion": {"mat": {"mobb": 1}, "pourquoi": "Suivi au sol : position, batterie et alertes. Jamais l’avionique."},
}
assert set(ENSEMBLES) == {l["id"] for l in lieux.LIEUX}, "Un ensemble de départ par lieu, ni plus ni moins."
for _e in ENSEMBLES.values():
    assert all(i == "vr*" or i in MAT_BY_ID for i in _e["mat"]), "Pièce inconnue dans un ensemble."
    assert all(a in AUTOS_BY_ID for a in (_e.get("ent") or {}).get("autos", [])), "Automatisation inconnue dans un ensemble."


def _p(n):
    return f"{n:,}".replace(",", " ") + " $"


# Les trois niveaux, tout compris (décisions de James, 18 novembre 2026; règles dans docs/OFFRE.md) :
# un seul niveau pour tous les lieux du client. Il dit ce que JARVIS fait (les extensions de SOLS, cochées
# d'office par catalogue.js), où vit l'IA et le soutien. Les autres extensions restent des options.
# Le Hub du lieu principal porte le niveau; un Hub plus puissant peut toujours faire un niveau plus bas.
NIVEAUX = {
    "base": {"sols": ["env", "diag"], "plus": "", "ia_court": "Par Internet",
             "ia": "L’IA passe par Internet, avec votre accord.",
             "inclus": ["Lumières, chauffage, serrures et énergie", "Alertes : fuites, pannes, entretien",
                        "L’app JARVIS, de partout", "Soutien par courriel"]},
    "signature": {"sols": ["env", "diag", "secu", "ia"], "plus": "Tout Base, plus :", "ia_court": "Chez vous",
                  "ia": "L’IA tourne dans votre Hub, même sans Internet.",
                  "inclus": ["Caméras qui comprennent ce qu’elles voient", "Une IA privée qui reste chez vous",
                             "Assistant vocal et réceptionniste", "Soutien par courriel et téléphone"]},
    "platinum": {"sols": ["env", "diag", "secu", "ia", "res"], "plus": "Tout Signature, plus :", "ia_court": "Chez vous, renforcée",
                 "ia": "IA renforcée, 100 % chez vous : elle continue pendant une panne.",
                 "inclus": ["Réseau et cybersécurité", "Plusieurs lieux reliés, sans limite",
                            "Batterie et Internet de secours", "Soutien prioritaire, une personne dédiée"]},
}
EXT_COURT = {"env": "Environnements", "diag": "Diagnostic", "secu": "Sécurité", "ia": "IA privée", "res": "Réseau", "mob": "Mobilité"}


def _stats(h):
    """Les trois repères d'un niveau, tirés des faits du Hub (HUBS) : caméras, appareils, où vit l'IA."""
    cam = f"{h['cam']}+" if h["id"] == "platinum" else str(h["cam"])
    app = "Illimité" if h["app"] >= 10 ** 6 else str(h["app"])
    trio = [(cam, "caméras analysées"), (app, "appareils reliés"), (NIVEAUX[h["id"]]["ia_court"], "où vit l’IA")]
    return '<dl class="ct-stats">' + "".join(f"<div><dd>{escape(v)}</dd><dt>{escape(k)}</dt></div>" for v, k in trio) + "</dl>"


def _hubs():
    """Les trois niveaux : nom, pour qui, trois repères (caméras, appareils, IA), puis, sur le niveau choisi,
    les extensions incluses et ce qu'il apporte. La fiche technique des Hubs est repliée dessous."""
    out = []
    for h in HUBS:
        c, n = lieux.HUBS_CHOIX[h["id"]], NIVEAUX[h["id"]]
        tag = f'<span class="ct-tag">{escape(h["tag"])}</span>' if h["tag"] else ""
        ext = " · ".join(EXT_COURT[x] for x in n["sols"])
        out.append(f"""<label class="ct-hub" data-rev data-hub="{h['id']}">
      <input type="radio" name="hub" value="{h['id']}" data-prix="{h['prix']}" data-cam="{h['cam']}" data-app="{h['app']}" data-autos="{h['autos']}">
      <span class="ct-check" aria-hidden="true"></span>
      {tag}
      <figure class="ct-hub-ph"><img src="/media/hubs/hub-{h['id']}.webp" alt="Hub JARVIS {escape(h['nom'])}" loading="lazy" decoding="async"></figure>
      <h3>{escape(h['nom'].replace("Hub ", ""))}</h3>
      <p class="ct-prix">{_p(h['prix'])}<small>une fois</small></p>
      <p class="ct-pour">{c['situation']} · {c['pour']}</p>
      {_stats(h)}
      <div class="ct-niv">
        <p class="ct-niv-ext"><b>{len(n["sols"])} extensions incluses</b>{ext}</p>
        <ul>{f'<li class="ct-niv-plus">{n["plus"]}</li>' if n["plus"] else ''}{"".join(f"<li>{x}</li>" for x in n["inclus"])}</ul>
        <p class="ct-niv-ia">{n["ia"]}</p>
      </div>
      <span class="ct-reco" aria-hidden="true">Conseillé pour vous</span>
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
        inclus = s["prix"] == 0
        prix = "Inclus" if inclus else f"{s['prix']} $<small>/mois{' ' + s['unite'] if s.get('unite') else ''}</small>"
        if s.get("unite"):
            inp = f'<input type="checkbox" name="sol" value="{s["id"]}" data-slug="{s["slug"]}" data-prix="{s["prix"]}" data-qty="1">'
            qty = '<div class="ct-qty ct-qty-sol"><button type="button" data-q="-1" aria-label="Un véhicule de moins">−</button><output>0</output><button type="button" data-q="1" aria-label="Un véhicule de plus">+</button><span>véhicule(s)</span></div>'
        else:
            inp = f'<input type="checkbox" name="sol" value="{s["id"]}" data-slug="{s["slug"]}" data-prix="{s["prix"]}"{" checked disabled" if inclus else ""}>'
            qty = ""
        out.append(f"""<label class="ct-sol{' is-inclus' if inclus else ''}" data-rev data-sol="{s['id']}">
      {inp}<span class="ct-check" aria-hidden="true"></span>
      <div class="ct-sol-h"><h3>{escape(s['nom'])}</h3><p class="ct-prix">{prix}</p></div>
      <p class="ct-why">{escape(s['pourquoi'])}</p>
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
    veille = "".join(f"""<label class="ct-ent ct-ent-veille" data-rev>
      <input type="checkbox" name="veille" value="{i}" data-prix="{p}"><span class="ct-check" aria-hidden="true"></span>
      <h3>{escape(n)}</h3><p class="ct-prix">{p} $<small>/mois</small></p>
      <p class="ct-why">{escape(w)}</p><p class="ct-d">{escape(d)}</p>
    </label>""" for i, n, p, d, w in ENT_VEILLE)
    cats = []
    for cat, items in AUTOMATISATIONS:
        rows = "".join(f"""<label class="ct-auto" data-id="{i}">
          <input type="checkbox" name="auto" value="{i}" data-prix="{p}"><span class="ct-check ct-check-sm" aria-hidden="true"></span>
          <span class="ct-auto-t"><b>{escape(n)}</b><em>{escape(w)}</em></span>
          <span class="ct-auto-p">{p} $<small>/mois</small></span>
        </label>""" for i, n, p, w in items)
        cats.append(f'<section class="ct-autocat" data-rev><h4>{escape(cat)}</h4>{rows}</section>')
    return f"""<div class="ct-ents">{socle}{recep}{toutes}</div>
    <h3 class="ct-sub" data-rev>La bibliothèque d’automatisations <em>cochez celles qu’il vous faut, elles s’ajoutent au panier</em></h3>
    <p class="ct-note ct-note-prix" data-rev><b>9 $</b> un déclencheur, une action · <b>19 $</b> reliée à un de vos outils · <b>29 $</b> veille 24/7 avec escalade. Toutes demandent le Socle Entreprise et un Hub Signature ou Platinum.</p>
    <div class="ct-autos">{"".join(cats)}</div>
    <div class="ct-ents ct-ents-bas">{mesure}</div>
    <p class="ct-note">{escape(ENT_USAGE)}</p>
    <h3 class="ct-sub" data-rev>Entretien et veille <em>pour que ça continue de protéger, mois après mois</em></h3>
    <div class="ct-ents ct-ents-veille">{veille}</div>"""


def _img_mat(i):
    """Vignette d'un article, si sa photo existe (media/forfait/mat-<id>.webp)."""
    chemin = f"/media/forfait/mat-{i}.webp"
    return f' data-img="{chemin}"' if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", chemin.lstrip("/"))) else ""


def _materiel():
    out = []
    for cat, items in MATERIEL:
        rows = "".join(f"""<div class="ct-item" data-id="{i}" data-prix="{p}"{' data-cam="1"' if i in CAMERAS else ''}{_img_mat(i)}>
        {f'<img class="ct-item-ph" src="/media/forfait/mat-{i}.webp" alt="" loading="lazy" decoding="async">' if _img_mat(i) else '<span class="ct-item-ph ct-item-ph-vide" aria-hidden="true"></span>'}
        <div class="ct-item-t"><b>{escape(n)}</b><span>{escape(d)}</span><em>{escape(w)}</em></div>
        <div class="ct-item-p">{_p(p)}</div>
        <div class="ct-qty"><button type="button" data-q="-1" aria-label="Retirer">−</button><output>0</output><button type="button" data-q="1" aria-label="Ajouter">+</button></div>
      </div>""" for i, n, p, d, w in items)
        out.append(f'<section class="ct-cat" data-rev><h3>{escape(cat)}</h3>{rows}</section>')
    return "".join(out)


def _services():
    cats = []
    for fam, items in SERVICES:
        rows = "".join(f"""<div class="ct-item" data-id="{i}" data-prix="{p}" data-svc="1">
        <div class="ct-item-t"><b>{escape(n)}</b><span>{escape(d)}</span><em>{escape(w)}</em></div>
        <div class="ct-item-p">{_p(p)}</div>
        <div class="ct-qty"><button type="button" data-q="-1" aria-label="Retirer">−</button><output>0</output><button type="button" data-q="1" aria-label="Ajouter">+</button></div>
      </div>""" for i, n, p, d, w in items)
        cats.append(f'<section class="ct-cat ct-cat-svc" data-rev><h3>{escape(fam)}</h3>{rows}</section>')
    return f'<div class="ct-mats ct-svcs">{"".join(cats)}</div><p class="ct-note">Payés une fois, sur soumission confirmée. Déplacement selon la distance. Nous vérifions et protégeons vos systèmes; nous ne sommes pas une agence de gardiennage ni d’enquête.</p>'


def _install():
    return "".join(f"""<label class="ct-inst card" data-rev>
      <input type="radio" name="install" value="{i}" data-prix="{p}"{' checked' if i == 'auto' else ''}><span class="ct-check" aria-hidden="true"></span>
      <small>{escape(aff)}</small><h3>{escape(n)}</h3><p>{escape(d)}</p>
    </label>""" for i, n, p, aff, d in INSTALL)


def _inclus():
    return "".join(f'<li data-rev><b>{escape(n)}</b><span>{escape(d)}</span></li>' for n, d in INCLUS)


def _donnees_offre():
    """Ce que catalogue.js lit : les extensions de chaque niveau et l'ensemble de départ de chaque lieu."""
    return json.dumps({"niveaux": {k: v["sols"] for k, v in NIVEAUX.items()}, "ensembles": ENSEMBLES},
                      ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


PAGE = {
    "url": "/offre/",
    "v2": True,
    "title": "L’offre JARVIS | Vos lieux, votre niveau, votre projet",
    "description": "Composez votre JARVIS en trois étapes : choisissez vos lieux, puis votre niveau. JARVIS propose le cerveau de chaque lieu et l’équipement; vous recevez une soumission écrite.",
    "og_image": "/media/hubs/hub-trio.webp",
    "assets": ["catalogue"],
    "content": f"""
<section class="ct-tete" aria-labelledby="ct-titre">
  {pro.fil("/offre/")}
  <h1 id="ct-titre" data-rev>Composez<br><span>votre JARVIS.</span></h1>
  <p data-rev>Dites-nous vos lieux et choisissez un niveau. JARVIS propose le reste : le cerveau de chaque lieu et son équipement.</p>
  <ol class="ct-pas" data-rev>
    <li><a href="#composer"><i>1</i><b>Vos lieux</b><span>Maison, entreprise, véhicules</span></a></li>
    <li><a href="#hub"><i>2</i><b>Votre niveau</b><span>Un seul, pour tout</span></a></li>
    <li><a href="#projet"><i>3</i><b>Votre projet</b><span>Proposé, puis ajusté</span></a></li>
  </ol>
</section>

<form id="ct" class="ct" novalidate>
<script type="application/json" data-offre>{_donnees_offre()}</script>
<section class="ct-lieu-etape" id="composer" data-toc="1 · Vos lieux" aria-label="Vos lieux">
  <p class="ct-etape" data-rev>Étape 1 sur 3</p>
  {lieux.selecteur("Vos lieux.", "Choisissez-en un ou plusieurs. Chaque lieu reçoit son cerveau : un Hub pour un lieu, un boîtier pour un véhicule.", ident="lieu")}
</section>

<div class="ct-wrap">
<div class="ct-vis" data-ct-vis aria-hidden="true">
  <div class="ct-vis-in">
    {"".join(f'<img class="ct-vis-i{" is-on" if h["id"] == "signature" else ""}" data-v="{h["id"]}" src="/media/hubs/hub-{h["id"]}.webp" alt="" loading="lazy" decoding="async">' for h in HUBS)}
    <p class="ct-vis-t"><b data-vis-nom>Hub Signature</b><span data-vis-ligne>{lieux.HUBS_CHOIX["signature"]["promesse"]}</span></p>
  </div>
  <script type="application/json" data-vis-data>{json.dumps({h["id"]: [h["nom"], lieux.HUBS_CHOIX[h["id"]]["promesse"]] for h in HUBS}, ensure_ascii=False)}</script>
</div>
<div class="ct-main">

<section class="sect" id="hub" data-toc="2 · Votre niveau" aria-labelledby="hub-t">
  <div class="sect-head"><div data-rev><p class="ct-etape">Étape 2 sur 3</p>
    <h2 id="hub-t">Votre niveau.<br><em>Un seul, pour tous vos lieux.</em></h2></div>
    <p data-rev>Le niveau dit ce que JARVIS fait, où vit son intelligence et le soutien que vous recevez. Le Hub de chaque lieu suit, tout seul.</p></div>
  <div class="ct-hubs">{_hubs()}</div>
  <details class="ct-details ct-guide" data-guide data-rev>
    <summary>Vous hésitez? <em>· trois questions, et JARVIS conseille</em></summary>
    <div class="ct-details-in">
      <div class="ct-gq" data-gq="cam"><p>Combien de caméras environ?</p>
        <div><button type="button" data-v="0">Aucune à 2</button><button type="button" data-v="1">3 à 6</button><button type="button" data-v="2">7 et plus</button></div></div>
      <div class="ct-gq" data-gq="ia"><p>L’intelligence doit-elle rester chez vous, même sans Internet?</p>
        <div><button type="button" data-v="1">Oui</button><button type="button" data-v="0">Peu importe</button></div></div>
      <div class="ct-gq" data-gq="coupure"><p>Une coupure serait-elle grave? <small>Animaux, entreprise, objets de valeur</small></p>
        <div><button type="button" data-v="2">Oui</button><button type="button" data-v="0">Non</button></div></div>
      <div class="ct-gres" data-guide-res hidden>
        <p><small>Conseillé pour vous</small><b data-guide-nom></b><span data-guide-why></span></p>
        <button type="button" class="pill" data-guide-go>Choisir ce niveau</button>
      </div>
    </div>
  </details>
  <details class="ct-details" data-rev><summary>Fiche technique <em>· les trois Hubs, ligne par ligne</em></summary><img class="ct-trio" src="/media/hubs/hub-trio.webp" alt="Les trois Hubs JARVIS côte à côte" loading="lazy" decoding="async">{_compare()}</details>
  <details class="ct-details" data-rev><summary>Changer de niveau plus tard <em>· rien ne se perd</em></summary>
    <div class="ct-details-in">
    <ul class="ct-grandit">
      <li><b>Monter de niveau</b>Si votre Hub suffit, on l’active à distance, le jour même.</li>
      <li><b>Plus de puissance</b>On échange votre Hub, avec un crédit. Votre lieu est restauré tel quel.</li>
      <li><b>Un autre lieu</b>Votre ancien Hub part au chalet ou dans le VR, relié au nouveau.</li>
      <li><b>Redescendre</b>Vous gardez votre Hub; on retire des fonctions et vous payez moins.</li>
    </ul>
    <p class="ct-note">Un Hub plus puissant peut toujours faire un niveau plus bas, jamais l’inverse. Tout le matériel installé reste.</p>
    </div>
  </details>
</section>

<section class="sect" id="projet" data-toc="3 · Votre projet" aria-labelledby="proj-t">
  <div class="sect-head"><div data-rev><p class="ct-etape">Étape 3 sur 3</p>
    <h2 id="proj-t">Votre projet.<br><em>JARVIS propose, vous ajustez.</em></h2></div>
    <p data-rev>Tout est déjà assorti à vos lieux et à votre niveau. Ajustez ce que vous voulez, ou envoyez tel quel : chaque ligne est confirmée par écrit.</p></div>

  <h3 class="ct-sub" id="solutions" data-rev>Vos extensions <em>ce que JARVIS sait faire</em></h3>
  <p class="ct-intro" data-rev>Celles de votre niveau sont déjà là. Les autres s’ajoutent au mois, annulables en tout temps.</p>
  <div class="ct-sols">{_solutions()}</div>
  <div data-public="entreprise">
  <details class="ct-details" id="entreprise" data-rev><summary>Entreprise <em>· réceptionniste IA et automatisations, à la carte</em></summary>
    <div class="ct-details-in">
    <p class="ct-intro">Tout est à l’unité et payable par mois. Vous commencez avec le Socle et une automatisation; vous en ajoutez quand vous en voyez le gain. Demande le niveau Signature ou Platinum.</p>
    {_entreprise()}
    </div>
  </details>
  </div>

  <h3 class="ct-sub" id="materiel" data-rev>L’équipement de vos lieux <em>un ensemble de départ par lieu</em></h3>
  <div class="ct-ens" data-ensembles aria-live="polite"><p class="ct-ens-vide">Choisissez vos lieux à l’étape 1 : JARVIS propose ici l’ensemble de départ de chacun.</p></div>
  <details class="ct-details ct-piece" data-rev><summary>Ajuster à la pièce <em>· boîtiers, capteurs, caméras, réseau</em></summary>
  <div class="ct-mats">{_materiel()}</div></details>

  <h3 class="ct-sub" id="donnees" data-rev>Vos données et l’IA <em>chez vous d’abord</em></h3>
  <div class="ct-don" data-rev>
    <ul class="ct-don-l">
      <li><b>Chez vous</b>Vos images, vos documents et votre historique restent dans votre Hub.</li>
      <li><b>De partout</b>L’accès à distance passe par un relais chiffré, qui ne garde rien.</li>
      <li><b>Sauvegarde chiffrée</b>Incluse. Illisible pour nous : si le Hub brise, le nouveau repart comme avant.</li>
    </ul>
    <p class="ct-don-t">Le nuage, seulement si vous le voulez :</p>
    <label class="ct-opt"><input type="checkbox" name="nuage" value="n_video"><span class="ct-check ct-check-sm" aria-hidden="true"></span>
      <span><b>Copie des vidéos hors du lieu</b><em>Chiffrée. Si le Hub est volé ou détruit, les images restent.</em></span></label>
    <label class="ct-opt"><input type="checkbox" name="nuage" value="n_ia"><span class="ct-check ct-check-sm" aria-hidden="true"></span>
      <span><b>Renfort d’IA par le nuage</b><em>Pour les grosses tâches seulement, et jamais sans votre accord explicite.</em></span></label>
  </div>

  <h3 class="ct-sub" id="installation" data-rev>L’installation <em>à vous de choisir</em></h3>
  <div class="cards ct-install">{_install()}</div>
  <div data-public="entreprise">
  <details class="ct-details" data-rev><summary>Services professionnels <em>· vérifier, protéger, former</em></summary>
    <div class="ct-details-in">{_services()}</div></details>
  </div>

  <h3 class="ct-sub" data-rev>Toujours inclus</h3>
  <ul class="ct-inclus">{_inclus()}</ul>

  <div class="ct-prevoir" data-cart-tips hidden aria-live="polite"></div>

  <div class="ct-fin" data-rev>
    <h3>Votre JARVIS est prêt.</h3>
    <p>Vous recevez une soumission écrite, ligne par ligne. Rien à payer ici.</p>
    <button type="button" class="pill" data-cart-open>Voir mon JARVIS et recevoir ma soumission</button>
  </div>
</section>

</div>

<div class="ct-bar" aria-live="polite">
  <button type="button" class="ct-jv" data-jv-ouvre><i aria-hidden="true"></i><span>Une question? <b>Demandez à JARVIS</b></span></button>
  <div><small>Aujourd’hui</small><b data-total-once>1 290 $</b></div>
  <div><small>Par mois</small><b data-total-month>0 $</b></div>
  <button type="button" class="pill" data-cart-open>Mon forfait<span data-cart-count></span> · Recevoir ma soumission</button>
</div>
</div>
</form>

""",
}


# ---------------------------------------------------------------------------------------------
# Sans prix publics (SITE["prix_publics"] = False) : le configurateur reste public, mais n'affiche
# aucun montant ni total. Chaque ligne dit « une fois » ou « par mois »; le prix est confirmé dans la
# soumission. Les prix restent dans ce fichier : remettre le drapeau à True les fait tous revenir.
# ---------------------------------------------------------------------------------------------
def _sans_prix(html):
    import re
    M = r"\d[\d\u00a0\u202f ]*[,.]?\d*\s?\$"          # un montant : « 1 290 $ », « 59 $ »
    html = html.replace('<form id="ct" class="ct"', '<form id="ct" class="ct" data-sansprix')
    html = re.sub(r'<p class="ct-note ct-note-prix"[^>]*>.*?</p>', "", html, flags=re.S)
    html = re.sub(M + r"<small>/mois", "<small>par mois", html)
    html = re.sub(M + r"<small>une fois \+ " + M + r"/mois</small>", "<small>une fois, puis par mois</small>", html)
    html = re.sub(M + r"<small>une fois", "<small>une fois", html)
    html = re.sub(r'<div class="ct-item-p">' + M + "</div>", '<div class="ct-item-p">une fois</div>', html)
    html = re.sub(r"<small>" + M + "</small>", "", html)
    html = re.sub(r"(<b data-total-[a-z]+>)" + M + "</b>", r"\1</b>", html)
    html = re.sub(r" \(" + M + r"\)", "", html)
    # Phrases entières qui ne parlent que d'un montant
    html = re.sub(r"[^.<>]*" + M + r"[^.<>]*\.", "", html)
    html = re.sub(r"[^.<>;:]*" + M + r"[^.<>]*(?=<)", "", html)
    html = html.replace("Dollars canadiens, taxes en sus. Soumission confirmée par écrit, ligne par ligne. Rien à payer ici.",
                        "Prix confirmé dans votre soumission, ligne par ligne. Rien à payer ici.")
    html = html.replace("Prix en dollars canadiens, taxes en sus. Points de départ : chaque soumission est confirmée par écrit, ligne par ligne.",
                        "Chaque soumission est confirmée par écrit, ligne par ligne.")
    return html


if not pro.PRIX:
    PAGE["content"] = _sans_prix(PAGE["content"])
    PAGE["title"] = "L’offre JARVIS | Vos lieux, votre niveau, votre projet"

