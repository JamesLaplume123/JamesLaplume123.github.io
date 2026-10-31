# Gabarits partagés : <head>, en-tête, pied de page et enveloppe de document.
# Chaque page de src/pages/ fournit un dict PAGE ; document() produit le HTML final.

from config import SITE, NAV, CTA_V2, FOOTER_COLUMNS


def head(page):
    url = SITE["domain"] + page["url"]
    title = page["title"]
    desc = page["description"]
    og = SITE["domain"] + page.get("og_image", SITE["og_image"])
    v = SITE["asset_version"]
    robots = '<meta name="robots" content="noindex">' if page.get("noindex") else ""
    assets = (
        '<link rel="preload" href="/assets/fonts/geist/geist-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
        f'<link rel="stylesheet" href="/assets/css/wow.css?v={v}">'
    )
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
{assets}"""


NAV_EN_LABELS = {
    "/solutions/": "Solutions",
    "/plateforme/": "JARVIS",
    "/laboratoire-mobile/": "Mobile lab",
    "/vision-roadmap/": "Vision",
}


def header_v2(page):
    """En-tête des pages wow : barre fixe fine + menu mobile plein écran."""
    en = page.get("lang") == "en"
    links = "".join(
        '<a href="{u}"{active}>{l}</a>'.format(
            u=item["url"],
            l=NAV_EN_LABELS.get(item["url"], item["label"]) if en else item["label"],
            active=' aria-current="page"' if page["url"].startswith(item["url"]) else "",
        )
        for item in NAV
    )
    cta_label = "Book a demo" if en else CTA_V2["label"]
    nav_label = "Main navigation" if en else "Navigation principale"
    menu_label = "Open menu" if en else "Ouvrir le menu"
    lang_link = (
        '<a class="sheet-lang" href="/" lang="fr">Français</a>'
        if en
        else '<a class="sheet-lang" href="/en/" lang="en">English</a>'
    )
    return f"""<header class="bar" data-bar>
  <a class="bar-brand" href="{'/en/' if en else '/'}"><b>JARVIS</b> <span>Private Systems</span></a>
  <nav class="bar-nav" aria-label="{nav_label}">{links}</nav>
  <div class="bar-actions">
    <a class="bar-cta" href="{CTA_V2['url']}">{cta_label}</a>
    <button class="bar-menu" type="button" aria-expanded="false" aria-label="{menu_label}" data-menu>
      <span></span><span></span>
    </button>
  </div>
</header>
<nav class="sheet" aria-label="Menu">
  {links}
  <a class="sheet-cta" href="{CTA_V2['url']}">{cta_label}</a>
  {lang_link}
</nav>"""


def footer_v2(page):
    cols = "".join(
        "<div><h2>{t}</h2><nav>{links}</nav></div>".format(
            t=col["title"],
            links="".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in col["links"]),
        )
        for col in FOOTER_COLUMNS
    )
    return f"""<footer class="foot">
  <div class="foot-grid">
    <div class="foot-brand">
      <b>JARVIS <span>Private Systems</span></b>
      <p>Relier ce qui existe. Faire agir l’ensemble.</p>
    </div>
    {cols}
  </div>
  <p class="foot-line"><span>{SITE['copyright']}</span><span>Privé par conception</span></p>
</footer>"""


def document(page):
    """Enveloppe une page complète : doctype, head, header, contenu, footer."""
    v = SITE["asset_version"]
    lang = "fr-CA" if page.get("lang", "fr") == "fr" else "en"
    skip = "Aller au contenu" if page.get("lang", "fr") == "fr" else "Skip to content"
    body_class = page.get("body_class", "")
    top, bottom = header_v2(page), footer_v2(page)
    script = f'<script src="/assets/js/wow.js?v={v}" defer></script>'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{head(page)}
</head>
<body class="{body_class}">
<a class="skip-link" href="#contenu">{skip}</a>
{top}
<main id="contenu">
{page['content']}
</main>
{bottom}
{script}
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
