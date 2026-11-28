# JARVIS Cyber — la troisième division (refonte « trois divisions », novembre 2026).
# Elle présente les services « Vérifier, protéger, former » déjà offerts dans le configurateur
# (catalogue.SERVICES) : on vérifie les systèmes du client lui-même, sur mandat écrit, puis on corrige
# avec lui. Security Pro (OSINT poussé, enquêtes) reste une vision sous permis : /vision-roadmap/.
# Jamais présenté comme une agence de gardiennage, d'enquête ou de sécurité privée (src/pro.py).
# Aucun prix ici : les prix vivent dans le configurateur (SITE["prix_publics"]).

import divisions
import pro

SERVICES = "".join(
    f'<div class="svc-c" data-rev><em>{k}</em><b>{n}</b><span>{l}</span></div>' for k, n, l in divisions.CYBER
)

ETAPES = [
    ("01", "Le mandat écrit", "Ce qu’on vérifie, quand et comment, signé avant de commencer."),
    ("02", "La vérification", "Vos caméras, votre réseau, vos accès et vos sauvegardes, comme un pirate les verrait."),
    ("03", "La correction, avec vous", "Les failles classées par gravité, et un plan clair pour les fermer."),
    ("04", "La nouvelle vérification", "On reteste pour prouver que c’est réglé."),
]

PAGE = {
    "url": "/solutions/cyber/",
    "v2": True,
    "title": "JARVIS Cyber | Solutions JARVIS",
    "description": (
        "Vérification de vos systèmes, test d’intrusion réseau sur mandat écrit, revue de votre "
        "exposition en ligne, Loi 25 et formation, pour maisons et entreprises."
    ),
    "og_image": "/media/vision/securite-centre.webp",
    "assets": ["divisions"],
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/vision/securite-centre.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    {pro.fil("/solutions/cyber/")}
    <h1 data-rev>JARVIS <em>Cyber.</em></h1>
    <p class="lead" data-rev>Nous vérifions vos systèmes comme un pirate le ferait, puis nous corrigeons avec vous. Toujours sur mandat écrit, pour vos propres systèmes.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Parlons de votre projet</a>
      <a class="pill ghost" href="#services">Voir les services</a>
    </div>
    <p class="for-line" data-rev><span>Pour</span> Toute maison ou entreprise, cliente de JARVIS ou non</p>
  </div>
</section>

<section class="sect" id="pourquoi" aria-labelledby="cy-pq">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Pourquoi maintenant</p>
      <h2 id="cy-pq">Une entreprise sur six <em>a été touchée en 2025.</em></h2>
    </div>
    <div class="side" data-rev>
      <p>Au Canada, environ une entreprise sur six (16 %) a subi un incident de cybersécurité en 2025. Source : Statistique Canada.</p>
    </div>
  </div>
</section>

<section class="sect alt" id="services" aria-labelledby="cy-svc">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Vérifier · protéger · former</p>
      <h2 id="cy-svc">Les services <em>de JARVIS Cyber.</em></h2>
    </div>
    <div class="side" data-rev><p>Chaque service se fait une fois, sur soumission confirmée.</p></div>
  </div>
  <div class="svc">{SERVICES}</div>
</section>

<section class="sect" id="deroulement" aria-labelledby="cy-der">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Comment ça se passe</p>
      <h2 id="cy-der">Quatre étapes, <em>toujours dans cet ordre.</em></h2>
    </div>
  </div>
  <div class="svc">{"".join(f'<div class="svc-c" data-rev><em>{n}</em><b>{t}</b><span>{d}</span></div>' for n, t, d in ETAPES)}</div>
  <div class="dv-suite" data-rev>
    <p class="form-note" style="margin:0">Nous vérifions et protégeons vos systèmes; nous ne sommes pas une agence de gardiennage ni d’enquête. Security Pro, la version plus poussée, reste une vision : elle demandera un permis avant toute mission réelle.</p>
    <a class="dv-lien" href="/vision-roadmap/">Voir la vision ›</a>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Quel système voulez-vous <em>faire vérifier?</em></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
