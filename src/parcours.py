# Le parcours du visiteur (refonte « clarté », novembre 2026) : comprendre en dix secondes
# ce que JARVIS vend, quelle option est pour soi et comment commencer.
#   besoins()     : « Qu'est-ce qu'il vous faut ? », grandes cartes photo par besoin (accueil);
#   offre_bref()  : l'offre en trois étapes, court renvoi vers /offre/ (accueil, /plateforme/#offre).
# Styles : assets/demos/parcours.css.
#
# Photos : chaque carte prend media/vitrine/besoins/<cle>.webp s'il existe au build, sinon une
# photo réelle déjà au site (jamais un dessin).

import os

_RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# (clé, besoin, phrase, solution, photo de repli, position de l'image)
BESOINS = [
    ("proteger", "Protéger ma maison",
     "Caméras, portes et alarme réunies en un seul fil clair.",
     "securite-intelligente", "/media/vitrine/accueil/maison-familiale.webp", "50% 60%",
     ["Caméras qui reconnaissent une personne, un véhicule ou un colis",
      "Serrures, portes et alarme sur un seul écran",
      "Alertes claires, sans fausses alarmes à répétition",
      "Images gardées chez vous, pas dans le nuage"]),
    ("domaine", "Gérer mon domaine et mes véhicules",
     "Lumières, chauffage, garage et énergie sur un seul écran.",
     "environnements-intelligents", "/media/vitrine/accueil/panorama-domaine-crepuscule.webp", "50% 55%",
     ["Résidence, chalet, garage, yacht et hangar au même endroit",
      "Chauffage, éclairage, piscine et énergie automatiques",
      "Voitures de collection surveillées : batterie, humidité, clés",
      "Une règle pour tout le domaine : « je pars », « on arrive »"]),
    ("entreprise", "Automatiser mon entreprise",
     "Réception, demandes et approbations qui avancent seules.",
     "automatisation-operations", "/media/vitrine/accueil/commerce-pme.webp", "50% 50%",
     ["Réceptionniste qui répond au téléphone et prend les rendez-vous",
      "Demandes, soumissions et approbations qui avancent seules",
      "Rapports du matin sans rien compiler à la main",
      "Vos données d’affaires restent dans votre bureau"]),
    ("ferme", "Gérer ma ferme",
     "Bâtiments, équipements et alarmes surveillés jour et nuit.",
     "environnements-intelligents", "/media/env/ferme.webp", "50% 55%",
     ["Étable, poulaillers, porcherie et écurie sur un seul tableau",
      "Température, ventilation, eau et moulée surveillées",
      "Alarme au téléphone si un chauffage ou une pompe lâche",
      "Silos, génératrice et clôtures électriques suivis"]),
    ("ia", "Mon IA privée",
     "Posez une question à vos documents; vos données restent chez vous.",
     "ia-privee-connaissances", "/media/solutions/ia-privee-connaissances.webp", "50% 50%",
     ["Un assistant qui connaît vos documents, contrats et notes",
      "Réponses avec la source, pour vérifier en un clic",
      "Fonctionne sur le Hub, chez vous, même sans Internet",
      "Rien n’est envoyé à une grande entreprise d’IA"]),
    ("route", "Partir sur la route",
     "Un copilote pour le VR, la voiture ou le vélo électrique.",
     "mobilite", "/media/vr/exterieur.webp", "50% 60%",
     ["Batteries, eau, chauffage et portes du VR à distance",
      "Itinéraire, arrêts et recharge planifiés pour vous",
      "Véhicules de tous les jours et de collection au même endroit",
      "La maison se prépare d’elle-même à votre retour"]),
]

TITRES = {
    "environnements-intelligents": "Environnements intelligents",
    "ia-privee-connaissances": "IA privée et connaissances",
    "securite-intelligente": "Sécurité intelligente",
    "automatisation-operations": "Automatisation d’entreprise",
    "reseau-resilience": "Réseau et cybersécurité",
    "diagnostic-care": "Diagnostic & continuité",
    "mobilite": "Mobilité",
}


def photo(cle, repli):
    """media/vitrine/besoins/<cle>.webp s'il existe, sinon la photo réelle de repli."""
    propre = "media/vitrine/besoins/" + cle + ".webp"
    if os.path.exists(os.path.join(_RACINE, propre)):
        return "/" + propre
    return repli


def besoins():
    cartes = "".join(
        f"""<a class="bs-card" href="/solutions/{sol}/" data-rev>
      <span class="bs-ph"><img src="{photo(cle, repli)}" alt="" loading="lazy" decoding="async" style="object-position:{pos}"></span>
      <span class="bs-txt">
        <small>{TITRES[sol]}</small>
        <b>{titre}</b>
        <span>{phrase}</span>
        <ul class="bs-inc" aria-label="Ce que vous obtenez">{"".join(f"<li>{x}</li>" for x in inclus)}</ul>
        <em class="bs-start">Pour commencer : le Hub + {TITRES[sol]}<i aria-hidden="true">→</i></em>
      </span>
    </a>"""
        for cle, titre, phrase, sol, repli, pos, inclus in BESOINS
    )
    return f"""<section class="besoins" id="besoins" aria-labelledby="besoins-titre">
  <div class="bs-head" data-rev>
    <p class="eyebrow">Par où commencer</p>
    <h2 id="besoins-titre">Qu’est-ce qu’il <em>vous faut?</em></h2>
    <p>Choisissez votre besoin : voici, concrètement, ce que JARVIS fait pour vous et par où commencer.</p>
  </div>
  <div class="bs-grid">{cartes}</div>
  <p class="bs-more" data-rev>Pas certain?
    <a href="/solutions/">Comparer les sept solutions</a><span aria-hidden="true">·</span><a href="/offre/">Comprendre l’offre</a></p>
</section>"""


ETAPES = [
    ("1", "Le Hub", "Un petit serveur installé chez vous. Il fait tourner JARVIS, même sans Internet."),
    ("2", "Vos extensions", "Vous ajoutez seulement ce qui vous sert : sécurité, domotique, IA, entreprise, route."),
    ("3", "Installation et soutien", "On installe, on vous forme, puis on reste là pour l’entretien et le soutien."),
]


def offre_bref(ident="offre", titre_id="offre-titre", classe="ob", toc=""):
    etapes = "".join(
        f'<li class="ob-step" data-rev><i>{n}</i><b>{t}</b><span>{d}</span></li>' for n, t, d in ETAPES
    )
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""<section class="{classe}" id="{ident}"{toc_attr} aria-labelledby="{titre_id}">
  <div class="ob-head" data-rev>
    <p class="eyebrow">L’offre, en bref</p>
    <h2 id="{titre_id}">Trois étapes. <em>Rien de compliqué.</em></h2>
  </div>
  <ol class="ob-steps">{etapes}</ol>
  <p class="ob-acts" data-rev><a class="pill" href="/offre/">Voir l’offre en détail</a>
  <a class="pill ghost" href="/contact/">Réserver une démo</a></p>
  <p class="ob-note" data-rev>Soumission gratuite, par écrit, après une visite de votre lieu.</p>
</section>"""
