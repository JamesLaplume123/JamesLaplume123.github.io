# Solutions — reconnaître son problème et choisir la bonne capacité.

from config import CAPABILITIES

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
        "for": "Entreprises, multi-sites et environnements technologiques complexes",
    },
    "diagnostic-care": {
        "result": "Un diagnostic progressif qui relie les symptômes aux preuves et prépare un dossier utile pour intervenir.",
        "points": ["Pannes physiques, logicielles ou mécaniques", "Hypothèses et vérifications guidées", "Rapport technicien et suivi après intervention"],
        "for": "Tous les environnements équipés, du bâtiment au véhicule",
    },
}

GUIDE_HTML = "".join(
    f"""<a href="#{slug}"><span>{q}</span><strong>{next(c['title'] for c in CAPABILITIES if c['slug'] == slug)}</strong></a>"""
    for slug, q in GUIDE
)

STORIES_HTML = "".join(
    f"""<article class="story" id="{c['slug']}">
      <div class="story-media" data-reveal>
        <span class="story-num">{c['num']} / 06</span>
        <img src="{c['image']}" alt="Aperçu de la solution {c['title']}" loading="lazy">
      </div>
      <div data-reveal>
        <h2>{c['title']}</h2>
        <p class="story-result">{STORIES[c['slug']]['result']}</p>
        <ul>{''.join(f'<li>{p}</li>' for p in STORIES[c['slug']]['points'])}</ul>
        <div class="story-foot">
          <div>
            <span>Particulièrement utile pour</span>
            <strong>{STORIES[c['slug']]['for']}</strong>
          </div>
          <a class="link-arrow" href="/solutions/{c['slug']}/">Explorer cette solution <span>↗</span></a>
        </div>
      </div>
    </article>"""
    for c in CAPABILITIES
)

PAGE = {
    "url": "/solutions/",
    "title": "Solutions | JARVIS Private Systems",
    "description": (
        "Six familles de solutions pour les environnements intelligents, l’IA privée, "
        "la sécurité, les opérations, le réseau et le diagnostic."
    ),
    "og_image": "/media/solutions/environnements-intelligents.webp",
    "content": f"""
<section class="hero page-hero">
  <div class="hero-media">
    <img src="/media/solutions/environnements-intelligents.webp" alt="" fetchpriority="high">
  </div>
  <div class="shell hero-inner">
    <div>
      <p class="eyebrow">Solutions JARVIS</p>
      <h1>Six solutions.<br><em>Une architecture commune.</em></h1>
      <p class="lead">Commencez par un problème concret. Chaque solution peut fonctionner seule;
      JARVIS permet ensuite de les relier sans tout reconstruire.</p>
      <div class="hero-meta">
        <div><span>Point de départ</span><b>Un besoin réel</b></div>
        <div><span>Déploiement</span><b>Local, privé ou hybride</b></div>
        <div><span>Environnements</span><b>Maison, véhicule et entreprise</b></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Trouver le bon point d’entrée</p>
        <h2>Qu’est-ce qui vous ralentit <em>aujourd’hui?</em></h2>
      </div>
      <p>Vous n’avez pas à choisir une technologie ni à comprendre toute l’architecture.
      Identifiez simplement le problème qui revient le plus souvent.</p>
    </div>
    <div class="guide-rows" data-reveal>
      {GUIDE_HTML}
    </div>
  </div>
</section>

<section class="section section-raised">
  <div class="shell">
    <div class="section-head" data-reveal>
      <div>
        <p class="eyebrow">Les six solutions</p>
        <h2>Des résultats distincts.<br><em>Une expérience cohérente.</em></h2>
      </div>
      <p>Six points d’entrée, selon le problème à résoudre.</p>
    </div>
    {STORIES_HTML}
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div data-reveal>
      <p class="eyebrow">Une fondation commune</p>
      <h2>Une plateforme, <em>pas six systèmes isolés.</em></h2>
    </div>
    <div data-reveal>
      <p class="lead">Les six capacités partagent la même identité, les mêmes permissions et la
      même trace. Elles s’activent selon le besoin.</p>
      <p style="margin-top:1.6rem;"><a class="link-arrow" href="/plateforme/">Comprendre la plateforme <span>↗</span></a></p>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="shell cta-inner" data-reveal>
    <div>
      <p class="eyebrow">Premier échange</p>
      <h2>Quel problème mérite une première preuve <em>concrète?</em></h2>
    </div>
    <div>
      <p>Décrivez le problème et son contexte. La première preuve utile sera clairement définie.</p>
      <a class="button button-fill" href="/contact/">Discuter du projet <span>↗</span></a>
    </div>
  </div>
</section>
""",
}
