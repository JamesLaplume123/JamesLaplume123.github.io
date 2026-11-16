# Questions avant de nous appeler — les réponses franches qu'un client veut avant d'écrire.
# Rien d'inventé : aucun prix, aucun délai, aucun client. Entreprise en phase de lancement.
# Les mêmes questions alimentent les données structurées (FAQPage).

import pro

GROUPES = [
    ("L’entreprise", "entreprise", [
        ("Que fait JARVIS Private Systems, en une phrase?",
         "Nous concevons et installons JARVIS, un système privé qui gère et protège les maisons, les "
         "fermes, les entreprises et les véhicules, en Montérégie. Il réunit la domotique, le réseau "
         "et sa cybersécurité, les caméras et serrures connectées, et une IA privée."),
        ("L’entreprise est-elle nouvelle?",
         "Oui. JARVIS Private Systems est en phase de lancement : nous prenons les noms des personnes "
         "intéressées et choisissons quelques premiers projets. Le logiciel JARVIS est en construction; "
         "son premier terrain d’essai est le <a href=\"/laboratoire-mobile/\">laboratoire mobile</a>, "
         "une ambulance convertie. L’état réel du projet est publié sur la page "
         "<a href=\"/vision-roadmap/#feuille-de-route\">Vision et feuille de route</a>."),
        ("Êtes-vous une agence de sécurité?", pro._PAS_AGENCE),
        ("Qui vais-je rencontrer?",
         "James Laplume, le fondateur. C’est lui qui visite votre lieu, prépare le plan et répond à vos "
         "questions."),
    ]),
    ("Le projet", "projet", [
        ("Par quoi commence-t-on?",
         "Par une visite et une conversation : ce qui est déjà en place, et ce qui vous dérange le plus. "
         "On commence ensuite par une seule chose utile, souvent la domotique ou le réseau. Le détail : "
         "<a href=\"/a-propos/#comment-on-travaille\">comment on travaille</a>."),
        ("Combien ça coûte?",
         "Ça dépend du lieu, de ce qui existe déjà et de ce qu’on relie. Le prix est toujours remis par "
         "écrit, ligne par ligne, après une visite gratuite, et vous décidez ensuite. Le "
         "<a href=\"/catalogue/\">catalogue</a> donne une idée des composantes."),
        ("Combien de temps dure une installation?",
         "Ça dépend de la taille du lieu et des travaux à faire. La durée prévue est écrite dans le plan, "
         "avant de commencer. On ne promet aucun délai avant d’avoir vu les lieux."),
        ("Dois-je remplacer mes appareils?",
         "Généralement non. JARVIS s’appuie sur Home Assistant et sur les standards ouverts Zigbee, "
         "Z-Wave, Matter et MQTT : on commence par ce que vous avez déjà."),
        ("Que dois-je préparer avant de vous écrire?",
         "Trois choses suffisent : le type de lieu (maison, ferme, entreprise, véhicule), le problème "
         "qui vous dérange le plus, et la liste approximative de ce qui est déjà installé (thermostats, "
         "caméras, routeur, applications). Des photos aident, mais ne sont pas nécessaires."),
    ]),
    ("Le système", "systeme", [
        ("Mes données sortent-elles de chez moi?",
         "Pas par défaut. Le système fonctionne sur le Hub, un petit boîtier installé chez vous. Rien "
         "n’est vendu, et rien ne sort sans votre accord. Le détail : "
         "<a href=\"/confiance/\">confiance</a> et <a href=\"/confidentialite/\">confidentialité</a>."),
        ("Est-ce que ça fonctionne sans Internet, ou pendant une panne de courant?",
         "Sans Internet, oui : les règles et l’application tournent sur place. Pendant une panne de "
         "courant, seuls les appareils alimentés par une batterie ou une génératrice continuent; on "
         "choisit avec vous ce qui doit tenir."),
        ("Installez-vous des caméras, des alarmes et des serrures?",
         "JARVIS relie les caméras, les serrures et les capteurs dans la même application que le reste, "
         "et garde les images chez vous. " + pro._PERMIS),
        ("Faut-il un abonnement?",
         "Aucun abonnement au nuage n’est nécessaire pour que le système fonctionne. L’entretien et le "
         "soutien que vous choisissez sont décrits dans la soumission, avant que vous décidiez."),
        ("Et si je veux arrêter, ou changer de fournisseur?",
         "Le système vous est remis avec sa documentation : le plan, la liste des appareils, les règles "
         "et vos accès. Il s’appuie sur des standards ouverts, pas sur un format fermé."),
    ]),
    ("La région", "region", [
        ("Où vous déplacez-vous?",
         "En Montérégie et aux environs, à partir de la région de Saint-Hyacinthe : Saint-Hyacinthe, "
         "Granby, Drummondville, Longueuil et la Rive-Sud, Saint-Jean-sur-Richelieu, Sorel-Tracy, "
         "Beloeil, Mont-Saint-Hilaire et Acton Vale. Chaque ville a sa page : "
         "<a href=\"/regions/\">régions desservies</a>."),
        ("Travaillez-vous avec les fermes et les entreprises?",
         "Oui. Voyez la <a href=\"/solutions/domotique-ferme-agricole/\">domotique pour ferme</a>, "
         "l’<a href=\"/solutions/automatisation-operations/\">automatisation pour PME et commerces</a> "
         "et l’<a href=\"/solutions/ia-privee-entreprise/\">IA privée pour entreprise</a>."),
        ("Comment vous joindre?",
         "Par le <a href=\"/contact/\">formulaire de contact</a> ou par courriel. James répond "
         "personnellement. Vous pouvez aussi simplement laisser votre nom pour rester informé."),
    ]),
]

TOUTES = [qa for _, _, qs in GROUPES for qa in qs]

BLOCS = "".join(
    f"""
<section class="faq{' pro-faq-alt' if i % 2 else ''}" id="{ident}" data-toc="{nom}" aria-labelledby="{ident}-titre">
  <div class="head" data-rev>
    <p class="eyebrow">{i + 1:02d} · {nom}</p>
    <h2 id="{ident}-titre">{nom}</h2>
  </div>
  <div class="faq-list">{pro.faq_items(qs)}</div>
</section>"""
    for i, (nom, ident, qs) in enumerate(GROUPES)
)

PAGE = {
    "url": "/questions/",
    "v2": True,
    "title": "Questions avant de nous appeler | JARVIS Private Systems",
    "description": (
        "Prix, durée, appareils, données, caméras, pannes, régions desservies : les réponses "
        "franches d’une entreprise de technologie et de sécurité en phase de lancement."
    ),
    "og_image": "/media/vitrine/contact/demo-chez-vous.webp",
    "assets": ["pro"],
    "schema": [pro.ld_faq(TOUTES)],
    "content": f"""
<section class="plain-top">
  {pro.fil("/questions/")}
  <p class="eyebrow" data-rev>Questions avant de nous appeler</p>
  <h1 data-rev>Les réponses, <em>avant l’appel.</em></h1>
  <p class="lead" data-rev>Ce qu’on fait, ce que ça coûte, ce qu’on ne fait pas. Des réponses courtes
  et franches, pour que vous sachiez à quoi vous attendre avant de nous écrire.</p>
</section>
{BLOCS}

<section class="cta">
  <h2 data-rev>Une question<br><span>qui n’est pas ici?</span></h2>
  <p data-rev>Écrivez-la en quelques lignes. James répond personnellement, sans pression.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a>
  <a class="pill ghost" href="/logiciel/">Voir le logiciel</a></div>
</section>
""",
}
