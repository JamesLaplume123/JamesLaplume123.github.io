# Catalogue — l'offre complète, à la façon d'une boutique (novembre 2026).
# Quatre étapes : 1) le Hub (Base, Signature, Platinum), 2) les solutions (par mois),
# 3) le matériel du lieu (une fois), 4) plusieurs lieux. Un configurateur fait le total.
# Les prix sont des points de départ (voir docs) et vivent tous dans CATALOGUE ci-dessous.
# Styles : assets/demos/catalogue.css · Script : assets/demos/catalogue.js

from html import escape
import json

HUBS = [
    {"id": "base", "nom": "Hub Base", "prix": 590, "pour": "Chalet, condo, petit VR",
     "tag": "",
     "pts": ["Jusqu’à 30 appareils", "2 caméras analysées, 7 jours d’enregistrement", "IA par Internet seulement",
             "Wi-Fi, Bluetooth, Zigbee", "Garantie 1 an, soutien par courriel"],
     "manque": ["Pas d’IA dans le Hub", "Pas d’assistant vocal ni de réceptionniste", "Pas de batterie de secours"]},
    {"id": "signature", "nom": "Hub Signature", "prix": 1290, "pour": "Maison, VR complet, PME",
     "tag": "Le plus choisi",
     "pts": ["Jusqu’à 100 appareils", "6 caméras analysées, 30 jours d’enregistrement", "IA locale, dans le Hub",
             "Assistant vocal « Jarvis » et réceptionniste IA", "Z-Wave et Matter, 3 lieux reliés",
             "Garantie 2 ans, soutien téléphone"],
     "manque": ["Pas de base de données ni de rapports", "Pas de batterie de secours", "Automatisations limitées à 10"]},
    {"id": "platinum", "nom": "Hub Platinum", "prix": 2490, "pour": "Domaine, entreprise, ferme",
     "tag": "Rien ne manque",
     "pts": ["Appareils illimités", "16 caméras et plus, 90 jours d’enregistrement", "IA forte, 100 % locale, carte IA dédiée",
             "Base de données, rapports, automatisations illimitées", "Batterie interne 2 h, Internet de secours intégré",
             "Hub principal de tous vos lieux", "Garantie 3 ans, remplacement express, personne dédiée"],
     "manque": []},
]

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
    ("Boîtier", "Plastique", "Aluminium", "Aluminium, sans ventilateur"),
    ("Garantie", "1 an", "2 ans", "3 ans + remplacement express"),
    ("Soutien", "Courriel", "Courriel et téléphone", "Prioritaire, personne dédiée"),
]

SOLUTIONS = [
    {"id": "env", "nom": "Environnements intelligents", "prix": 0, "slug": "environnements-intelligents",
     "pts": ["Lumières, chauffage, stores, foyer, serrures", "Scènes : Matin, Soir, Nuit, Absent", "Énergie pièce par pièce", "Fonctionne sans Internet"]},
    {"id": "diag", "nom": "Diagnostic et continuité", "prix": 15, "slug": "diagnostic-care",
     "pts": ["Veille 24/7 : fuite, gel, batterie, panne", "Alertes de partout, avec la cause probable", "Dossier prêt pour le technicien", "Rapport mensuel de santé du lieu"]},
    {"id": "secu", "nom": "Sécurité intelligente", "prix": 20, "slug": "securite-intelligente",
     "pts": ["Enregistrement local, rien dans le nuage", "Reconnaît personne, véhicule, animal, colis", "Alertes regroupées en une phrase", "Mode urgence et accès temporaires"]},
    {"id": "ia", "nom": "IA privée et connaissances", "prix": 15, "slug": "ia-privee-connaissances",
     "pts": ["Assistant qui connaît votre lieu", "Répond à partir de vos documents, source citée", "Assistant vocal (Signature et Platinum)", "Option IA par Internet avec votre clé"]},
    {"id": "res", "nom": "Réseau et cybersécurité", "prix": 10, "slug": "reseau-resilience",
     "pts": ["Carte du réseau en direct", "Appareils inconnus détectés et bloqués", "Zones séparées : invités, caméras, travail", "Lien de secours géré automatiquement"]},
    {"id": "mob", "nom": "Mobilité", "prix": 10, "slug": "mobilite", "unite": "par véhicule",
     "pts": ["Position en direct, historique des trajets", "Diagnostic moteur, pression des pneus", "Alerte de mouvement (antivol)", "Données cellulaires incluses"]},
]
COMPLET = {"id": "complet", "nom": "JARVIS Complet", "prix": 49, "valeur": 70}

ENTREPRISE = [
    {"id": "ent1", "nom": "Entreprise Départ", "prix": 49, "hub": "signature",
     "d": "Réceptionniste IA (1 ligne), 10 automatisations actives, 200 minutes, 500 actions par mois."},
    {"id": "ent2", "nom": "Entreprise Croissance", "prix": 149, "hub": "signature",
     "d": "2 lignes, 30 automatisations, 600 minutes, 2 000 actions, rapports hebdomadaires."},
    {"id": "ent3", "nom": "Entreprise Illimité", "prix": 349, "hub": "platinum",
     "d": "Lignes et automatisations illimitées, 2 000 minutes, base de données, tableau de bord direction."},
]
ENT_USAGE = "Au-delà du forfait : minute d’appel 0,10 $ · 1 000 actions 10 $ · ligne supplémentaire 15 $/mois · automatisation sur mesure dès 295 $."
AUTOMATISATIONS = [
    ("Réception", ["Répondre 24/7 et prendre les messages", "Prendre et confirmer un rendez-vous", "Texter le rappel la veille",
                   "Transférer un appel urgent au bon employé", "Répondre aux questions fréquentes"]),
    ("Ventes", ["Envoyer une soumission à partir d’un gabarit", "Relancer une soumission sans réponse après 3 jours",
                "Créer la fiche client", "Prévenir le vendeur quand un client rappelle"]),
    ("Facturation", ["Relancer une facture impayée (7, 14, 30 jours)", "Envoyer le reçu après paiement", "Comptes à recevoir chaque lundi"]),
    ("Opérations", ["Créer un bon de travail à partir d’une demande", "Assigner au technicien disponible",
                    "Escalader à la personne de garde", "Alerte si un équipement critique tombe"]),
    ("Direction", ["Rapport du matin : appels, ventes, alertes", "Résumé de la semaine le vendredi", "Approbation par texto : « OK » ou « Non »"]),
    ("Ferme et commerce", ["Alerte de température : frigo, réservoir à lait, étable", "Journal automatique des livraisons", "Commande de moulée quand le silo est bas"]),
]

# Matériel : (catégorie, [(id, nom, prix, description)])
MATERIEL = [
    ("Boîtiers JARVIS", [
        ("vrb", "Boîtier VR Base", 490, "12 V. Batteries (shunt), 2 réservoirs, batterie moteur. VR, roulotte, bateau."),
        ("vrs", "Boîtier VR Signature", 890, "Base + 16 sorties (lumières, pompe, chauffage) + 3e réservoir + 4G et GPS."),
        ("vrp", "Boîtier VR Platinum", 1290, "Signature + 2 ports caméras + bus du véhicule (RV-C, NMEA 2000) + secours."),
        ("mobb", "Boîtier Mobilité", 249, "Port OBD-II, GPS, LTE. Pour voiture ou camion, sans Hub dans l’auto."),
        ("ecr10", "Écran JARVIS 10 po", 549, "Tactile, micro et haut-parleur : contrôle sur place, assistant vocal, interphone."),
        ("ecr7", "Écran JARVIS 7 po", 349, "Version compacte pour une chambre, un VR ou un bureau."),
        ("sec", "Boîtier Secours", 299, "Garde le Hub et le routeur allumés 8 h pendant une panne."),
    ]),
    ("Capteurs", [
        ("fuite", "Fuite d’eau", 59, "Sous l’évier, près du chauffe-eau, au sous-sol. À pile."),
        ("vanne", "Vanne d’eau automatique", 449, "Ferme l’entrée d’eau à distance ou dès qu’une fuite est détectée."),
        ("temp", "Température et humidité", 39, "Intérieur, extérieur, soute, frigo. Alerte de gel. À pile."),
        ("porte", "Porte et fenêtre", 49, "Ouvert ou fermé, alerte en votre absence. À pile."),
        ("radar", "Présence (radar)", 79, "Détecte une personne même immobile."),
        ("fumee", "Fumée et CO", 129, "Relié à JARVIS : alerte partout, lumières, sirène."),
        ("propane", "Propane", 149, "Niveau de la bonbonne et détection de fuite."),
        ("reserv", "Niveau de réservoir", 120, "Eau potable, grise, noire, carburant. Collé sous le réservoir."),
        ("pneus", "Pression des pneus (4)", 399, "Alerte de crevaison et de surchauffe."),
        ("energie", "Compteur d’énergie", 189, "Consommation en direct, par circuit ou pour tout le lieu."),
        ("univ", "Capteur universel", 89, "Pince ampèremétrique, pression, débit, vibration. Pour une pompe, un silo."),
    ]),
    ("Caméras et accès", [
        ("camext", "Caméra extérieure", 299, "4K, vision de nuit couleur, alimentée par câble réseau."),
        ("camint", "Caméra intérieure", 179, "2K, discrète, micro, obturateur de confidentialité."),
        ("cam360", "Caméra 360° (dôme)", 449, "Stationnement, entrepôt, cour."),
        ("sonnette", "Sonnette vidéo", 249, "Reconnaît visiteurs et colis, répond de partout."),
        ("plaques", "Lecteur de plaques", 599, "Véhicule connu, inconnu, refusé. Ouvre la barrière aux connus."),
        ("serrure", "Serrure intelligente", 349, "Déverrouiller par cellulaire, codes invités."),
        ("clavier", "Clavier et lecteur de badges", 249, "Entrée d’entreprise ou de garage, badges et codes QR."),
        ("inter", "Interphone vidéo", 399, "Parler au visiteur et ouvrir de partout."),
        ("sirene", "Sirène et stroboscope", 99, "Pour le mode urgence."),
        ("urgence", "Bouton d’urgence", 49, "Lumières, sirène, enregistrement, appel aux contacts."),
    ]),
    ("Confort et réseau", [
        ("thermo", "Thermostat intelligent", 149, "Chauffage ou climatisation par pièce."),
        ("inter2", "Interrupteur ou gradateur", 69, "Remplace l’interrupteur existant. Par électricien."),
        ("prise", "Prise intelligente", 35, "Lampe, pompe, chauffe-moteur."),
        ("ampoule", "Ampoule couleur", 29, "Scènes et ambiances."),
        ("del", "Bande DEL (2 m)", 59, "Ambiance, escalier, comptoir."),
        ("store", "Moteur de store", 199, "Selon l’heure et le soleil."),
        ("relais", "Relais foyer ou garage", 89, "Allumer le foyer ou ouvrir le garage, avec confirmation."),
        ("poe", "Switch PoE 8 ports", 249, "Alimente caméras et téléphones par câble réseau."),
        ("r4g", "Routeur 4G/5G", 399, "Internet cellulaire : chalet, VR, ferme."),
        ("starlink", "Starlink Mini", 599, "Internet par satellite, partout."),
        ("telip", "Téléphone IP", 149, "Pour la réceptionniste IA et les transferts."),
    ]),
]

KITS = [
    ("Kit VR Essentiel", 1290, "Hub Base + Boîtier VR Base + 2 températures + 1 porte", "Diagnostic + Mobilité · 25 $/mois",
     {"hub": "base", "mat": {"vrb": 1, "temp": 2, "porte": 1}, "sol": ["diag", "mob"]}),
    ("Kit VR Complet", 2490, "Hub Signature + Boîtier VR Signature + 4 températures + 2 portes + fuite + propane", "JARVIS Complet · 49 $/mois",
     {"hub": "signature", "mat": {"vrs": 1, "temp": 4, "porte": 2, "fuite": 1, "propane": 1}, "sol": ["complet"]}),
    ("Kit Chalet", 1190, "Hub Base + 3 températures + 2 fuites + 2 portes + routeur 4G", "Diagnostic · 15 $/mois",
     {"hub": "base", "mat": {"temp": 3, "fuite": 2, "porte": 2, "r4g": 1}, "sol": ["diag"]}),
    ("Kit Maison", 1890, "Hub Signature + 3 fuites + 3 portes + 2 présences + sonnette vidéo", "JARVIS Complet · 49 $/mois",
     {"hub": "signature", "mat": {"fuite": 3, "porte": 3, "radar": 2, "sonnette": 1}, "sol": ["complet"]}),
    ("Kit Maison Sécurité", 2990, "Kit Maison + 3 caméras extérieures + switch PoE + sirène", "JARVIS Complet · 49 $/mois",
     {"hub": "signature", "mat": {"fuite": 3, "porte": 3, "radar": 2, "sonnette": 1, "camext": 3, "poe": 1, "sirene": 1}, "sol": ["complet"]}),
    ("Kit PME", 2190, "Hub Signature + 2 téléphones IP + 2 caméras + switch PoE + clavier", "Entreprise Départ + Réseau · 59 $/mois",
     {"hub": "signature", "mat": {"telip": 2, "camext": 2, "poe": 1, "clavier": 1}, "sol": ["res"], "ent": "ent1"}),
    ("Kit Domaine", 5990, "Hub Platinum + 6 caméras + lecteur de plaques + 2 serrures + interphone + 4 fuites + vanne d’eau + switch PoE", "JARVIS Complet · 49 $/mois",
     {"hub": "platinum", "mat": {"camext": 6, "plaques": 1, "serrure": 2, "inter": 1, "fuite": 4, "vanne": 1, "poe": 1}, "sol": ["complet"]}),
    ("Kit Ferme", 4490, "Hub Platinum + routeur 4G + 4 caméras + 6 températures + 4 capteurs universels + Boîtier Secours", "Complet + Entreprise Départ · 98 $/mois",
     {"hub": "platinum", "mat": {"r4g": 1, "camext": 4, "temp": 6, "univ": 4, "sec": 1}, "sol": ["complet"], "ent": "ent1"}),
]

INSTALL = [
    ("Je l’installe moi-même", "Inclus", "Prises identifiées, aucun fil à couper. Plan, vidéo et mise en service à distance (30 min)."),
    ("Mise en service guidée", "149 $", "Un technicien vous accompagne en vidéo pendant l’installation."),
    ("JARVIS s’en occupe", "110 $/h", "Installation, configuration et formation sur place. Déplacement en sus."),
    ("Visite de planification", "Gratuite", "Domaine, entreprise, ferme : inventaire, plan écrit, soumission ligne par ligne."),
]
INCLUS = [
    ("Configuration pour votre lieu", "Vos appareils déjà jumelés, vos scènes de base prêtes."),
    ("Test d’une heure", "Chaque kit tourne une heure sur banc avant l’envoi."),
    ("Mises à jour automatiques", "Signées, la nuit, avec retour arrière."),
    ("Sauvegarde chiffrée", "Si le Hub brise, le nouveau repart comme avant."),
    ("Garantie", "1 an Base, 2 ans Signature, 3 ans Platinum. Garantie légale du Québec en plus."),
    ("Retour 30 jours", "Matériel non installé : remboursé, moins la configuration."),
]


def _p(n):
    return f"{n:,}".replace(",", " ") + " $"


def _hubs():
    out = []
    for h in HUBS:
        pts = "".join(f"<li>{escape(p)}</li>" for p in h["pts"])
        manque = "".join(f"<li>{escape(p)}</li>" for p in h["manque"])
        manque_html = f'<p class="ct-k ct-k-no">Ce qui manque</p><ul class="ct-no">{manque}</ul>' if manque else ""
        tag = f'<span class="ct-tag">{escape(h["tag"])}</span>' if h["tag"] else ""
        out.append(f"""<label class="ct-hub" data-rev data-hub="{h['id']}">
      <input type="radio" name="hub" value="{h['id']}" data-prix="{h['prix']}"{' checked' if h['id'] == 'signature' else ''}>
      <span class="ct-check" aria-hidden="true"></span>
      {tag}
      <figure class="ct-hub-ph"><img src="/media/product/jarvis-hub-v1.webp" alt="" loading="lazy" decoding="async"></figure>
      <h3>{escape(h['nom'])}</h3>
      <p class="ct-prix">{_p(h['prix'])}<small>une fois</small></p>
      <p class="ct-pour">{escape(h['pour'])}</p>
      <p class="ct-k">Ce que vous avez</p>
      <ul class="ct-oui">{pts}</ul>
      {manque_html}
    </label>""")
    return "".join(out)


def _compare():
    rows = []
    for i, (lab, *vals) in enumerate(COMPARE):
        cells = "".join(
            '<td><i class="ct-dot" aria-label="Non disponible"></i></td>' if v == "—" else f"<td>{escape(v)}</td>"
            for v in vals
        )
        rows.append(f"<tr><th scope=\"row\">{escape(lab)}</th>{cells}</tr>")
    return f"""<div class="ct-cmp-w"><table class="ct-cmp">
      <thead><tr><th></th><th>Hub Base<small>{_p(590)}</small></th><th class="is-mid">Hub Signature<small>{_p(1290)}</small></th><th>Hub Platinum<small>{_p(2490)}</small></th></tr></thead>
      <tbody>{"".join(rows)}</tbody></table></div>
    <p class="ct-note"><i class="ct-dot"></i> Non disponible sur ce Hub. Les capacités sont des repères; elles dépendent aussi des caméras et des solutions actives.</p>"""


def _solutions():
    out = []
    for s in SOLUTIONS:
        pts = "".join(f"<li>{escape(p)}</li>" for p in s["pts"])
        inclus = s["prix"] == 0
        prix = "Inclus" if inclus else f"{s['prix']} $<small>/mois{' ' + s['unite'] if s.get('unite') else ''}</small>"
        inp = f'<input type="checkbox" name="sol" value="{s["id"]}" data-prix="{s["prix"]}"{" checked disabled" if inclus else ""}>'
        out.append(f"""<label class="ct-sol{' is-inclus' if inclus else ''}" data-rev>
      {inp}<span class="ct-check" aria-hidden="true"></span>
      <div class="ct-sol-h"><h3>{escape(s['nom'])}</h3><p class="ct-prix">{prix}</p></div>
      <ul class="ct-oui">{pts}</ul>
      <a href="/solutions/{s['slug']}/">Voir la solution <i aria-hidden="true">→</i></a>
    </label>""")
    return "".join(out)


def _entreprise():
    cards = "".join(f"""<label class="ct-ent" data-rev>
      <input type="radio" name="ent" value="{e['id']}" data-prix="{e['prix']}"><span class="ct-check" aria-hidden="true"></span>
      <h3>{escape(e['nom'])}</h3><p class="ct-prix">{e['prix']} $<small>/mois</small></p>
      <p class="ct-pour">Hub {e['hub'].capitalize()} ou plus</p><p class="ct-d">{escape(e['d'])}</p>
    </label>""" for e in ENTREPRISE)
    cards += """<label class="ct-ent is-none" data-rev><input type="radio" name="ent" value="" data-prix="0" checked><span class="ct-check" aria-hidden="true"></span><h3>Sans Entreprise</h3><p class="ct-d">Pour une maison, un chalet, un VR.</p></label>"""
    biblio = "".join(
        f'<div class="ct-auto" data-rev><h4>{escape(cat)}</h4><ul>{"".join(f"<li>{escape(i)}</li>" for i in items)}</ul></div>'
        for cat, items in AUTOMATISATIONS
    )
    return f"""<div class="ct-ents">{cards}</div>
    <p class="ct-note">{escape(ENT_USAGE)}</p>
    <h3 class="ct-sub" data-rev>La bibliothèque d’automatisations <em>· toutes incluses, activez d’un clic</em></h3>
    <div class="ct-autos">{biblio}</div>"""


def _materiel():
    out = []
    for cat, items in MATERIEL:
        rows = "".join(f"""<div class="ct-item" data-id="{i}" data-prix="{p}">
        <div class="ct-item-t"><b>{escape(n)}</b><span>{escape(d)}</span></div>
        <div class="ct-item-p">{_p(p)}</div>
        <div class="ct-qty"><button type="button" data-q="-1" aria-label="Retirer">−</button><output>0</output><button type="button" data-q="1" aria-label="Ajouter">+</button></div>
      </div>""" for i, n, p, d in items)
        out.append(f'<section class="ct-cat" data-rev><h3>{escape(cat)}</h3>{rows}</section>')
    return "".join(out)


def _kits():
    return "".join(f"""<article class="ct-kit" data-rev>
      <h3>{escape(n)}</h3><p class="ct-prix">{_p(p)}</p>
      <p class="ct-d">{escape(d)}</p><p class="ct-mois">{escape(m)}</p>
      <button type="button" class="pill" data-kit='{json.dumps(cfg, ensure_ascii=False)}'>Partir de ce kit</button>
    </article>""" for n, p, d, m, cfg in KITS)


def _install():
    return "".join(f'<article class="card" data-rev><small>{escape(p)}</small><h3>{escape(n)}</h3><p>{escape(d)}</p></article>' for n, p, d in INSTALL)


def _inclus():
    return "".join(f'<li data-rev><b>{escape(n)}</b><span>{escape(d)}</span></li>' for n, d in INCLUS)


PAGE = {
    "url": "/catalogue/",
    "v2": True,
    "title": "Catalogue JARVIS | Hubs, solutions, matériel et prix",
    "description": "Choisissez votre Hub, vos solutions et le matériel de votre lieu. Prix clairs, total en direct, kits prêts à partir.",
    "og_image": "/media/offre/maison.webp",
    "assets": ["catalogue"],
    "content": f"""
<section class="band top ct-top">
  <div class="bg"><img src="/media/solutions/jarvis-spaces-property-v3.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Catalogue</p>
    <h1 data-rev>Un Hub. Vos solutions.<br><em>Rien de plus.</em></h1>
    <p class="lead" data-rev>Composez votre JARVIS en quatre étapes. Le total se calcule en direct. Vos données restent chez vous.</p>
    <ol class="of-trois" data-rev>
      <li><a href="#hub"><i>1</i>Le Hub</a></li>
      <li><a href="#solutions"><i>2</i>Vos solutions</a></li>
      <li><a href="#materiel"><i>3</i>Le matériel</a></li>
      <li><a href="#lieux"><i>4</i>Plusieurs lieux</a></li>
    </ol>
  </div>
</section>

<form id="ct" class="ct" novalidate>

<section class="sect" id="hub" data-toc="1 · Le Hub" aria-labelledby="hub-t">
  <div class="sect-head"><div data-rev><p class="of-num"><i>1</i><span>Étape 1 sur 4</span></p>
    <h2 id="hub-t">Choisissez votre Hub.<br><em>Selon la taille de votre lieu.</em></h2></div>
    <p data-rev>Même logiciel, même app, mêmes solutions. Ce qui change : la puissance, le nombre d’appareils, l’IA et la sécurité. Payé une fois.</p></div>
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
    <div><h3>{COMPLET['nom']} · {COMPLET['prix']} $/mois</h3><p>Les six solutions ci-dessus. Valeur à la carte : {COMPLET['valeur']} $/mois.</p></div>
  </label>
  <h3 class="ct-sub" data-rev>Automatisation d’entreprise <em>· une réceptionniste IA et des automatisations prêtes</em></h3>
  {_entreprise()}
</section>

<section class="sect" id="materiel" data-toc="3 · Le matériel" aria-labelledby="mat-t">
  <div class="sect-head"><div data-rev><p class="of-num"><i>3</i><span>Étape 3 sur 4</span></p>
    <h2 id="mat-t">Ajoutez le matériel<br><em>de votre lieu.</em></h2></div>
    <p data-rev>Payé une fois. Prêt à brancher : chaque appareil apparaît tout seul dans l’app. Déjà du Victron, de l’UniFi, des caméras ONVIF, un NAS ou Starlink? JARVIS s’y branche au lieu de les remplacer.</p></div>
  <div class="ct-kits-h" data-rev><h3 class="ct-sub">Pressé? <em>Partez d’un kit, puis ajustez.</em></h3></div>
  <div class="ct-kits">{_kits()}</div>
  <div class="ct-mats">{_materiel()}</div>
</section>

<section class="sect alt" id="lieux" data-toc="4 · Plusieurs lieux" aria-labelledby="lieux-t">
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

<aside class="ct-total" aria-live="polite">
  <div class="ct-total-in">
    <div class="ct-total-l"><small>Votre JARVIS</small><b data-total-nom>Hub Signature</b><span data-total-detail>0 solution · 0 appareil</span></div>
    <div class="ct-total-r">
      <div><small>Une fois</small><b data-total-once>1 290 $</b></div>
      <div><small>Par mois</small><b data-total-month>0 $</b></div>
      <a class="pill" href="/contact/" data-total-link>Obtenir ma soumission</a>
    </div>
  </div>
</aside>
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
