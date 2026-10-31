# Solution 02 — IA privée et connaissances.

from pages._solution import solution_page

# Vitrine : une question devient une réponse sourcée, avec ses preuves.
SHOWCASE = """
<div class="qa-stage" data-reveal>
  <div class="qa-thread">
    <div class="qa-user">
      <small>VOUS</small>
      <p>Pourquoi la génératrice s’arrête-t-elle après quelques minutes, et que puis-je vérifier sans risque?</p>
    </div>
    <div class="qa-answer">
      <header><span>JARVIS · SYNTHÈSE SOURCÉE</span><small>Confiance · 74 %</small></header>
      <strong>La surchauffe liée à la circulation d’air est la piste la mieux appuyée.</strong>
      <p>Le manuel relie le code E-17 à une température d’huile élevée et le technicien recommande
      un dégagement de 30 cm. Le dernier entretien confirme l’huile et le filtre remplacés. La photo
      jointe identifie le véhicule, mais ne montre pas l’entrée d’air : elle ne peut donc pas
      confirmer l’hypothèse.</p>
      <footer>
        <span class="status status-real"><i></i>Confirmé · code E-17 observé</span>
        <span class="status status-building"><i></i>Probable · ventilation à contrôler</span>
        <span class="status status-proto"><i></i>Preuve manquante · entrée d’air</span>
      </footer>
    </div>
  </div>
  <div class="qa-sources">
    <p class="eyebrow">Preuves rapprochées</p>
    <article class="card">
      <p class="eyebrow">PDF · page 48</p>
      <h3>Manuel_Generatrice.pdf</h3>
      <p>Code d’arrêt E-17 et procédure de vérification. Document primaire, cité dans la réponse.</p>
    </article>
    <article class="card">
      <p class="eyebrow">DOC · 41 h depuis l’entretien</p>
      <h3>Entretien_2026.docx</h3>
      <p>Huile et filtre remplacés. Écarte un entretien oublié, mais aucune preuve thermique jointe.</p>
    </article>
    <article class="card">
      <p class="eyebrow">IMG · preuve insuffisante</p>
      <h3>IMG_1842_Vue_vehicule.jpg</h3>
      <p>Le véhicule est identifié, mais l’entrée d’air est hors cadre. JARVIS refuse d’en déduire une obstruction.</p>
    </article>
  </div>
</div>
"""

DATA = {
    "slug": "ia-privee-connaissances",
    "title": "IA privée et connaissances",
    "description": "Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.",
    "image": "/media/solutions/ia-privee-connaissances.webp",
    "h1": "IA privée et <em>connaissances.</em>",
    "lead": "Un assistant qui travaille à partir de vos sources autorisées et montre d’où vient chaque réponse importante.",
    "for": "Particuliers, PME et équipes qui travaillent avec beaucoup d’information",
    "problem_title": "L’information existe déjà. <em>Le travail consiste à la retrouver.</em>",
    "problem_copy": (
        "Documents, courriels, procédures, photos et historiques sont dispersés. "
        "L’interface conversationnelle de JARVIS aide à chercher, comparer et préparer la prochaine "
        "étape sans donner un accès illimité à toutes les données."
    ),
    "change_title": "Une réponse utile commence par une source vérifiable.",
    "change_copy": (
        "Chaque réponse relie la demande aux sources consultées, aux permissions utilisées "
        "et à la prochaine action proposée."
    ),
    "features": [
        ("Recherche avec provenance", "Chaque résultat important peut pointer vers les documents ou systèmes qui le soutiennent."),
        ("Permissions explicites", "Les personnes, agents et missions accèdent seulement aux sources nécessaires à leur rôle."),
        ("Contexte de mission", "L’assistant utilise le dossier, le site et l’objectif autorisés plutôt qu’une mémoire sans limites."),
        ("Préparation du travail", "Résumer une demande, comparer des documents et préparer un dossier ou une intervention."),
        ("Actions supervisées", "Les communications et opérations externes importantes attendent une validation humaine."),
        ("Déploiement flexible", "Les données peuvent rester locales, privées ou réparties selon le niveau de sensibilité."),
    ],
    "demo_title": "Poser une question. <em>Voir les preuves.</em>",
    "demo_copy": (
        "L’aperçu montre comment une question devient une réponse sourcée, puis un travail "
        "préparé — sans accès général aux données."
    ),
    "showcase": SHOWCASE,
    "compat": ["Documents", "Courriels", "Calendriers", "Photos", "Procédures", "Stockage local", "API métier"],
    "deploy_title": "Vos informations restent là où vous les avez autorisées.",
    "deploy_copy": (
        "Les modèles, index et documents sensibles peuvent être conservés sur une infrastructure "
        "privée. Le choix dépend du matériel, du volume et du niveau de confidentialité."
    ),
    "limit": (
        "L’assistant ne reçoit jamais automatiquement toutes les données du réseau. Chaque "
        "connecteur, source et permission doit être déclaré, contrôlé et révocable."
    ),
    "cta_title": "Quelle information devrait devenir <em>facile à retrouver?</em>",
    "cta_copy": (
        "Présentez les sources concernées, les personnes qui doivent y accéder et le résultat "
        "concret que l’assistant devrait préparer."
    ),
}

DATA["demo_image"] = "/media/product/user/assistant.jpg"
DATA["demo_caption"] = "Assistant JARVIS — il propose, vous décidez. Conception en validation."

PAGE = solution_page(DATA)
