# Gabarits partagés : <head>, en-tête, pied de page et enveloppe de document.
# Chaque page de src/pages/ fournit un dict PAGE ; document() produit le HTML final.

from config import SITE, NAV, CTA, FOOTER_COLUMNS, FOOTER_STATUS

BRAND = (
    '<a class="brand" href="{home}" aria-label="JARVIS Private Systems — accueil">'
    '<span class="brand-word">JARVIS</span>'
    '<span class="brand-sub">Private Systems</span></a>'
)


def head(page):
    url = SITE["domain"] + page["url"]
    title = page["title"]
    desc = page["description"]
    og = SITE["domain"] + page.get("og_image", SITE["og_image"])
    v = SITE["asset_version"]
    robots = '<meta name="robots" content="noindex">' if page.get("noindex") else ""
    lang_alt = (
        f'<link rel="alternate" hreflang="en" href="{SITE["domain"]}/en/">'
        f'<link rel="alternate" hreflang="fr-CA" href="{SITE["domain"]}/">'
        if page["url"] in ("/", "/en/") else ""
    )
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="application-name" content="{SITE['name']}">
{robots}<link rel="canonical" href="{url}">
{lang_alt}<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="theme-color" content="{SITE['theme_color']}">
<link rel="icon" href="/favicon.svg?v={v}">
<link rel="preload" href="/assets/fonts/fraunces/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/geist/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={v}">"""


def header(page):
    lang = page.get("lang", "fr")
    links = "".join(
        '<a href="{u}"{active}>{l}</a>'.format(
            u=item["url"],
            l=item["label"],
            active=' aria-current="page"' if page["url"].startswith(item["url"]) else "",
        )
        for item in NAV
    )
    lang_link = (
        '<a class="lang-link" href="/en/" lang="en">EN</a>'
        if lang == "fr"
        else '<a class="lang-link" href="/" lang="fr">FR</a>'
    )
    cta_label = CTA["label"] if lang == "fr" else "Start a conversation"
    menu_label = "Ouvrir le menu" if lang == "fr" else "Open menu"
    nav_label = "Navigation principale" if lang == "fr" else "Main navigation"
    return f"""<header class="site-head" data-head>
  <div class="head-inner">
    {BRAND.format(home='/' if lang == 'fr' else '/en/')}
    <nav class="head-nav" aria-label="{nav_label}" data-nav>
      {links}
      <div class="head-nav-extra">
        {lang_link}
        <a class="button button-gold" href="{CTA['url']}">{cta_label}</a>
      </div>
    </nav>
    <div class="head-actions">
      {lang_link}
      <a class="button button-gold head-cta" href="{CTA['url']}">{cta_label}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-label="{menu_label}" data-nav-toggle>
        <span></span><span></span>
      </button>
    </div>
  </div>
</header>"""


def footer(page):
    cols = "".join(
        "<div><h2>{t}</h2>{links}</div>".format(
            t=col["title"],
            links="".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in col["links"]),
        )
        for col in FOOTER_COLUMNS
    )
    status = "".join(f"<span>{s}</span>" for s in FOOTER_STATUS)
    return f"""<footer class="site-foot">
  <div class="shell foot-main">
    <div class="foot-brand">
      {BRAND.format(home='/')}
      <p>Relier ce qui existe. Comprendre ce qui compte. Agir avec votre accord.</p>
    </div>
    {cols}
    <div><h2>État</h2>{status}</div>
  </div>
  <div class="shell foot-bottom">
    <span>{SITE['copyright']}</span>
    <span>Privé par conception</span>
  </div>
</footer>"""


def document(page):
    """Enveloppe une page complète : doctype, head, header, contenu, footer."""
    v = SITE["asset_version"]
    lang = "fr-CA" if page.get("lang", "fr") == "fr" else "en"
    skip = "Aller au contenu" if page.get("lang", "fr") == "fr" else "Skip to content"
    body_class = page.get("body_class", "")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{head(page)}
</head>
<body class="{body_class}">
<a class="skip-link" href="#contenu">{skip}</a>
{header(page)}
<main id="contenu">
{page['content']}
</main>
{footer(page)}
<script src="/assets/js/site.js?v={v}" defer></script>
</body>
</html>
"""


def redirect_document(target):
    """Petite page de redirection pour préserver les anciennes URL."""
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex">'
        f'<meta http-equiv="refresh" content="0;url={target}">'
        f'<link rel="canonical" href="{SITE["domain"]}{target}">'
        "<title>Redirection</title></head>"
        f'<body><p><a href="{target}">Continuer</a></p></body></html>\n'
    )
