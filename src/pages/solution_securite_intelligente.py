# Solution 03 — Sécurité intelligente.

from pages._solution import solution_page

# Vitrine : un événement compris avant la réaction.
SHOWCASE = """
<div class="split" data-reveal>
  <figure class="showcase-frame" style="margin:0;">
    <img src="/media/solutions/camera-front-entry-v1.webp"
         alt="Caméra de l’entrée avant pendant un événement à vérifier" loading="lazy">
    <figcaption>
      <span>ENTRÉE AVANT · 20 H 41</span>
      <strong>Vérification requise · 3 éléments rapprochés</strong>
    </figcaption>
  </figure>
  <aside class="console" style="max-width:none;">
    <header class="console-head"><span><i></i>ÉVÉNEMENT PRIORITAIRE</span><small>LOCAL</small></header>
    <div class="console-body">
      <small>CONFIANCE CONTEXTUELLE · 87 %</small>
      <strong>Une personne inconnue accompagne une résidente autorisée.</strong>
      <p>JARVIS rapproche la caméra, l’accès, les appareils reconnus et l’horaire.
      Il ne déverrouille rien tant que le contexte demeure incomplet.</p>
    </div>
    <ul class="console-signals">
      <li><span>CAMÉRA</span><b>Présence double</b></li>
      <li><span>ACCÈS</span><b>Badge reconnu</b></li>
      <li><span>DÉCISION</span><b>Confirmation requise</b></li>
    </ul>
    <div class="console-body" style="border-top:1px solid var(--line);">
      <small>ACTION PROPOSÉE</small>
      <p style="margin-top:0.5rem;">Afficher l’interphone et demander à la résidente de confirmer
      le visiteur. Aucun accès automatique.</p>
    </div>
  </aside>
</div>
"""

DATA = {
    "slug": "securite-intelligente",
    "title": "Sécurité intelligente",
    "description": "Transformer caméras, accès et alarmes en événements compréhensibles plutôt qu’en notifications isolées.",
    "image": "/media/solutions/securite-intelligente.webp",
    "h1": "Sécurité <em>intelligente.</em>",
    "lead": "Une sécurité qui réunit le contexte, les preuves et les décisions, sans retirer le contrôle humain.",
    "for": "Résidences, entreprises et propriétés réparties sur plusieurs sites",
    "problem_title": "Une alerte sans contexte crée du bruit. <em>Une preuve organisée permet de décider.</em>",
    "problem_copy": (
        "Les caméras, portes, alarmes et capteurs détectent chacun une partie de l’événement. "
        "JARVIS vise à construire une chronologie commune pour expliquer ce qui a été observé "
        "et ce qui mérite réellement une attention."
    ),
    "change_title": "Moins d’alertes isolées. Plus de contexte pour décider.",
    "change_copy": (
        "La valeur vient du rapprochement entre présence, accès, image et horaire, "
        "pas d’une multiplication des notifications."
    ),
    "features": [
        ("Chronologie unifiée", "Rapprocher les événements provenant des caméras, accès, alarmes et capteurs autorisés."),
        ("Conservation des preuves", "Associer les images, états et décisions pertinentes à un incident documenté."),
        ("Alertes hiérarchisées", "Différencier un événement normal, une anomalie et une situation exigeant une vérification."),
        ("Présence et périmètres", "Adapter les règles selon l’occupation, les horaires et les zones réellement concernées."),
        ("Respect de la vie privée", "Limiter l’analyse, la durée de conservation et les personnes pouvant consulter les données."),
        ("Réponse supervisée", "Proposer une procédure et laisser les décisions sensibles à une personne autorisée."),
    ],
    "demo_title": "Comprendre un événement <em>avant de réagir.</em>",
    "demo_copy": (
        "Cette scène distingue ce qui est autorisé, ce qui est simplement observé "
        "et ce qui exige une vérification humaine."
    ),
    "showcase": SHOWCASE,
    "compat": ["Frigate", "ONVIF", "Contrôle d’accès", "Alarmes", "Capteurs", "Interphones", "Stockage local"],
    "deploy_title": "Les événements sensibles restent près du site.",
    "deploy_copy": (
        "L’analyse vidéo et la conservation peuvent être effectuées localement. "
        "Les accès distants passent par des mécanismes privés et auditables."
    ),
    "limit": (
        "Le système ne prétend pas identifier les intentions ni déterminer qu’une personne est "
        "dangereuse. Les règles, responsabilités et obligations légales doivent être définies "
        "avant tout déploiement."
    ),
    "cta_title": "Quel événement de sécurité manque aujourd’hui <em>de contexte?</em>",
    "cta_copy": (
        "Décrivez le site, les accès, les caméras et les alertes actuelles. Nous identifierons "
        "les preuves utiles et les limites à respecter."
    ),
}

DATA["demo_image"] = "/media/solutions/security-enterprise-delivery-v1.webp"
DATA["demo_caption"] = "Livraison détectée au quai 2 — contexte attendu. Données simulées."
DATA["extra"] = """
<div class="shots" data-rev style="margin-top:14px">
  <figure>
    <img src="/media/solutions/camera-garage-supercars-v1.webp" alt="Caméra intérieure du garage" loading="lazy">
    <figcaption><b>Garage intérieur</b><span>2 véhicules autorisés</span></figcaption>
  </figure>
  <figure>
    <img src="/media/solutions/security-enterprise-parking-v1.webp" alt="Caméra du stationnement de l’entreprise" loading="lazy">
    <figcaption><b>Stationnement</b><span>Périmètre calme</span></figcaption>
  </figure>
  <figure>
    <img src="/media/solutions/camera-pool-spa-v1.webp" alt="Caméra de la piscine et du spa" loading="lazy">
    <figcaption><b>Piscine et spa</b><span>Périmètre calme</span></figcaption>
  </figure>
</div>
"""

PAGE = solution_page(DATA)
