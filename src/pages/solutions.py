# Solutions — reconnaître son problème et choisir la bonne capacité. Version wow.

from config import CAPABILITIES
import galerie

GUIDE = [
    ("environnements-intelligents", "Votre lieu dépend de plusieurs applications qui ne se parlent pas?"),
    ("ia-privee-connaissances", "Vos documents, courriels et connaissances sont difficiles à retrouver?"),
    ("securite-intelligente", "Vos caméras, accès et alarmes produisent des alertes sans contexte?"),
    ("automatisation-operations", "Votre équipe ressaisit les mêmes informations entre plusieurs outils?"),
    ("reseau-resilience", "Votre infrastructure devient visible seulement lorsqu’un service tombe?"),
    ("diagnostic-care", "Une panne traverse plusieurs systèmes et personne ne possède toute l’histoire?"),
]

STORIES = {
    "environnements-intelligents": {
        "result": "Un seul environnement pour comprendre et contrôler le confort, l’énergie, les accès et les équipements.",
        "points": ["Contrôle simple du lieu", "Automatisations selon le contexte", "Fonctions essentielles disponibles localement"],
        "for": "Résidences, bâtiments, ateliers et véhicules aménagés",
    },
    "ia-privee-connaissances": {
        "result": "Un assistant privé qui cherche dans les sources autorisées, cite ses preuves et prépare la prochaine action.",
        "points": ["Conversation sur vos propres informations", "Documents, courriels, photos et procédures", "Accès Internet optionnel avec permissions strictes"],
        "for": "Particuliers, PME et équipes qui travaillent avec beaucoup d’information",
    },
    "securite-intelligente": {
        "result": "Une chronologie claire qui distingue les présences autorisées, les anomalies et les événements à vérifier.",
        "points": ["Caméras, accès et capteurs réunis", "Personnes, appareils ou plaques autorisés selon le cadre", "Preuves locales et réponse supervisée"],
        "for": "Résidences, entreprises et propriétés réparties sur plusieurs sites",
    },
    "automatisation-operations": {
        "result": "Des demandes, documents et approbations qui avancent entre vos systèmes sans perdre leur contexte.",
        "points": ["Courriel transformé en dossier", "Documents et tâches préparés", "Approbation avant chaque action sensible"],
        "for": "PME, entreprises de services et équipes terrain",
    },
    "reseau-resilience": {
        "result": "Une vue vivante du réseau, de ses dépendances, de ses accès privés et des risques à traiter.",
        "points": ["Inventaire, topologie et disponibilité", "Wi-Fi, VPN, LTE, Starlink et multi-sites", "Assistance à la surveillance réseau"],
        "for": "Maisons connectées, PME et petits multi-sites qui dépendent de leur réseau",
    },
    "diagnostic-care": {
        "result": "Un diagnostic progressif qui relie les symptômes aux preuves et prépare un dossier utile pour intervenir.",
        "points": ["Pannes physiques, logicielles ou mécaniques", "Hypothèses et vérifications guidées", "Rapport technicien et suivi après intervention"],
        "for": "Tous les environnements équipés, du bâtiment au véhicule",
    },
}

STORIES["mobilite"] = {
    "result": "Un copilote de route qui propose le bon arrêt au bon moment, et un journal qui garde chaque voyage sur la carte.",
    "points": ["Suggestions selon la distance, l’ouverture, le soleil et le véhicule", "Photos et arrêts géolocalisés automatiquement", "VR, voitures et vélos électriques connectés"],
    "for": "VR, voitures, véhicules électriques et vélos électriques",
}
GUIDE.append(("mobilite", "Vous voyagez et passez plus de temps à chercher qu’à profiter de la route?"))

GUIDE_HTML = "".join(
    f"""<a class="row" href="#{slug}" data-rev>
      <i>Question {i + 1:02d}</i>
      <span>{q}
      <em class="go">{next(c['title'] for c in CAPABILITIES if c['slug'] == slug)} ↓</em></span>
    </a>"""
    for i, (slug, q) in enumerate(GUIDE)
)

STORIES_HTML = "".join(
    f"""<article class="frow{' flip' if i % 2 else ''}" id="{c['slug']}">
      <figure class="media" data-rev>
        <img src="{c['image']}" alt="Aperçu de la solution {c['title']}" loading="lazy">
      </figure>
      <div data-rev>
        <p class="num">{c['num']} / 07</p>
        <h3>{c['title']}</h3>
        <p class="res">{STORIES[c['slug']]['result']}</p>
        <ul>{''.join(f'<li>{p}</li>' for p in STORIES[c['slug']]['points'])}</ul>
        <p class="for">Particulièrement utile pour
        <b>{STORIES[c['slug']]['for']}</b></p>
        <a class="pill ghost" href="/solutions/{c['slug']}/#jarvis">Explorer cette solution</a>
      </div>
    </article>"""
    for i, c in enumerate(CAPABILITIES)
)

PAGE = {
    "url": "/solutions/",
    "assets": ["galerie"],
    "v2": True,
    "title": "Solutions | JARVIS Private Systems",
    "description": (
        "Sept familles de solutions pour les environnements intelligents, l’IA privée, "
        "la sécurité, les opérations, le réseau et le diagnostic."
    ),
    "og_image": "/media/solutions/environnements-intelligents.webp",
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/solutions/environnements-intelligents.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Solutions JARVIS</p>
    <h1 data-rev>Sept solutions.<br><em>Une architecture commune.</em></h1>
    <p class="lead" data-rev>Commencez par un problème concret. Chaque solution peut fonctionner
    seule; JARVIS permet ensuite de les relier sans tout reconstruire.</p>
    <div class="meta" data-rev>
      <span class="chip">Un besoin réel</span>
      <span class="chip">Local, privé ou hybride</span>
      <span class="chip">Maison · véhicule · entreprise</span>
    </div>
  </div>
</section>

<section class="sect">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Trouver le bon point d’entrée</p>
      <h2 style="margin-top:1rem">Qu’est-ce qui vous ralentit <em>aujourd’hui?</em></h2>
    </div>
    <p data-rev>Vous n’avez pas à choisir une technologie ni à comprendre toute l’architecture.
    Identifiez simplement le problème qui revient le plus souvent.</p>
  </div>
  <div class="rows">
    {GUIDE_HTML}
  </div>
</section>

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Les sept solutions</p>
      <h2 style="margin-top:1rem">Des résultats distincts.<br><em>Une expérience cohérente.</em></h2>
    </div>
    <p data-rev>Sept points d’entrée, selon le problème à résoudre.</p>
  </div>
  {STORIES_HTML}
</section>
{galerie.solutions_clients()}

<section class="statement">
  <p class="eyebrow" data-rev>Une fondation commune</p>
  <h2 data-rev style="margin-top:1.2rem">Une plateforme,<br><em>pas six systèmes isolés.</em></h2>
  <p data-rev>Les six capacités partagent la même identité, les mêmes permissions et la
  même trace. Elles s’activent selon le besoin.</p>
  <div class="acts" data-rev style="justify-content:center">
    <a class="pill ghost" href="/plateforme/">Comprendre la plateforme</a>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Quel problème mérite<br><span>une première preuve?</span></h2>
  <p data-rev>Décrivez le problème et son contexte. La première preuve utile sera clairement définie.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Réserver une démo</a></div>
</section>
""",
}
