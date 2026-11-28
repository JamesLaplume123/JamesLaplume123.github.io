# JARVIS Cyber — la troisième division (refonte « trois divisions », novembre 2026).
# Elle présente les services « Vérifier, protéger, former » déjà offerts dans le configurateur
# (catalogue.SERVICES) : on vérifie les systèmes du client lui-même, sur mandat écrit, puis on corrige
# avec lui. Security Pro (OSINT poussé, enquêtes) reste une vision sous permis : /vision-roadmap/.
# Jamais présenté comme une agence de gardiennage, d'enquête ou de sécurité privée (src/pro.py).
# Aucun prix ici : les prix vivent dans le configurateur (SITE["prix_publics"]).
# Chiffres vérifiés le 27 novembre 2026 : Statistique Canada (Le Quotidien, 21 octobre 2026),
# Bitdefender et NETGEAR (rapport sur la maison connectée, 29 octobre 2025).
# Données : src/divisions.py · Styles : assets/demos/divisions.css.

import divisions
import pro

ETAPES = [
    ("01", "Le mandat écrit", "Ce qu’on vérifie, quand et comment, signé avant de commencer."),
    ("02", "La vérification", "Vos caméras, votre réseau, vos accès et vos sauvegardes, comme un pirate les verrait."),
    ("03", "La correction, avec vous", "Les failles classées par gravité, et un plan clair pour les fermer."),
    ("04", "La nouvelle vérification", "On reteste pour prouver que c’est réglé."),
]
ETAPES_HTML = "".join(
    f'<li><span aria-hidden="true">{n}</span><div><b>{t}</b><p>{d}</p></div></li>' for n, t, d in ETAPES
)

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
      <h2 id="cy-pq">Les attaques visent <em>tout le monde.</em></h2>
    </div>
    <div class="side" data-rev><p>Les grandes entreprises, mais aussi les PME et les maisons connectées.</p></div>
  </div>
  <div class="dv-chiffres">
    <div class="dv-ch" data-rev><b>1 sur 6</b><span>entreprises canadiennes a subi un incident de cybersécurité en 2025.</span><small>Source : <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/261021/dq261021b-fra.htm" rel="noopener">Statistique Canada</a></small></div>
    <div class="dv-ch" data-rev><b>29</b><span>attaques par jour contre une maison connectée, en moyenne, en 2025.</span><small>Source : <a href="https://www.bitdefender.com/en-gb/news/new-bitdefender-and-netgear-report-reveals-rising-threats-across-the-connected-home-landscape" rel="noopener">Bitdefender et NETGEAR</a></small></div>
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
  <div class="gam gam-3">{divisions.cartes(divisions.CYBER)}</div>
</section>

<section class="sect" id="deroulement" aria-labelledby="cy-der">
  <div class="dv-feat">
    <div class="dv-feat-ph" data-rev><img src="/media/vitrine/confiance/approbation-main.webp" alt="" loading="lazy" style="object-position:35% 50%"></div>
    <div data-rev>
      <p class="eyebrow">Comment ça se passe</p>
      <h2 id="cy-der">Quatre étapes, <em>toujours dans cet ordre.</em></h2>
      <ol class="dv-etapes">{ETAPES_HTML}</ol>
      <p class="form-note dv-note">Nous vérifions et protégeons vos systèmes; nous ne sommes pas une agence de gardiennage ni d’enquête. Security Pro, la version plus poussée, reste une vision : elle demandera un permis avant toute mission réelle. <a href="/vision-roadmap/">Voir la vision</a></p>
    </div>
  </div>
</section>

<section class="cta">
  <h2 data-rev>Quel système voulez-vous <em>faire vérifier?</em></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Parlons de votre projet</a></div>
</section>
""",
}
