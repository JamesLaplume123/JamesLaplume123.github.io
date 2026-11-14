# Gabarits partagés : <head>, en-tête, pied de page et enveloppe de document.
# Chaque page de src/pages/ fournit un dict PAGE ; document() produit le HTML final.

import re

from config import SITE, NAV, CTA_V2, CAPABILITIES, FOOTER_COLUMNS, SEO
from demos.app import EXT_ICON, ICONS


def head(page):
    url = SITE["domain"] + page["url"]
    title, desc = SEO.get(page["url"], (page["title"], page["description"]))
    og_path = page.get("og_image", SITE["og_image"])
    og = SITE["domain"] + og_path
    og_size = (
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        if og_path == SITE["og_image"] else ""
    )
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
{lang_alt}<meta property="og:locale" content="{'en_CA' if page.get('lang') == 'en' else 'fr_CA'}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
{og_size}<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="CA-QC">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="theme-color" content="{SITE['theme_color']}">
<link rel="icon" href="/favicon.svg?v={v}">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{MODE_SCRIPT}
{assets}"""


MODE_SCRIPT = (
    '<script>try{var m=new URLSearchParams(location.search).get("mode")'
    '||localStorage.getItem("jarvis-mode");'
    'if(m==="base"||m==="signature"||m==="platinum")'
    'document.documentElement.dataset.mode=m}catch(e){}</script>'
)

NAV_EN_LABELS = {
    "/logiciel/": "The software",
    "/solutions/": "Solutions",
    "/offre/": "The offer",
    "/a-propos/": "About",
}


def ext_icon(slug):
    """Icône d'une extension : la même que dans JARVIS App (src/demos/app.py, lecture seule)."""
    return f'<svg class="mm-i" viewBox="0 0 24 24" aria-hidden="true">{ICONS[EXT_ICON[slug]]}</svg>'


def ext_links(cls):
    """Les sept extensions : icône, nom et une ligne. Sert au menu déroulant et au menu mobile."""
    return "".join(
        f'<a class="{cls}" href="/solutions/{c["slug"]}/">{ext_icon(c["slug"])}'
        f'<span><b>{c["title"]}</b><small>{c["menu"]}</small></span></a>'
        for c in CAPABILITIES
    )


def mega_menu(en):
    """Les sept solutions, une phrase chacune. Rien d'autre."""
    return f"""<div class="mega" data-mega-panel>
      <p class="mega-k">{'Seven solutions · one system' if en else 'Sept solutions · un seul système'}</p>
      <div class="mega-grid">{ext_links("mega-a")}</div>
    </div>"""


SUB_EN = {
    "/logiciel/": ("The software, live", "The app, screen by screen (in French)."),
    "/plateforme/": ("The Hub and private AI", "Under the hood: Hub, AI, core, accounts."),
    "/a-propos/": ("Who is behind JARVIS", "James, his approach and the field."),
    "/vision-roadmap/": ("Our vision", "Where JARVIS is going, and where it truly stands."),
    "/laboratoire-mobile/": ("Mobile lab", "The converted ambulance, live batteries."),
    "/confiance/": ("Trust and security", "How your data and access are protected."),
    "/recherche/": ("Research", "The method behind every proof."),
}


def sub_links(item, cls, en):
    """Sous-menu d'une entrée (Le logiciel, À propos) : icône, titre et une ligne."""
    out = []
    for url, lab, desc, ic in item["sub"]:
        if en and url in SUB_EN:
            lab, desc = SUB_EN[url]
        out.append(f'<a class="{cls}" href="{url}"><svg class="mm-i" viewBox="0 0 24 24" aria-hidden="true">{ICONS[ic]}</svg>'
                   f'<span><b>{lab}</b><small>{desc}</small></span></a>')
    return "".join(out)


def header_v2(page):
    """En-tête des pages wow : barre fixe fine, menu des extensions, menu mobile plein écran."""
    en = page.get("lang") == "en"

    def label(item):
        return NAV_EN_LABELS.get(item["url"], item["label"]) if en else item["label"]

    def current(item):
        urls = [item["url"]] + [u for u, *_ in item.get("sub", [])]
        return any("#" not in u and page["url"].startswith(u) for u in urls)

    bar_links = []
    for item in NAV:
        cur = ' aria-current="page"' if current(item) else ""
        if item.get("menu") or item.get("sub"):
            panel = mega_menu(en) if item.get("menu") else (
                f'<div class="mega mega-s" data-mega-panel><div class="mega-grid">{sub_links(item, "mega-a", en)}</div></div>')
            what = label(item)
            bar_links.append(
                f'<div class="bar-dd" data-mega><a href="{item["url"]}"{cur}>{what}</a>'
                f'<button class="bar-dd-t" type="button" aria-expanded="false" '
                f'aria-label="{"Show the menu " + what if en else "Afficher le menu " + what}" data-mega-t>'
                f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9.5 6 6 6-6"/></svg></button>'
                f'{panel}</div>'
            )
        else:
            bar_links.append(f'<a href="{item["url"]}"{cur}>{label(item)}</a>')

    def sheet_sub(item):
        if item.get("menu"):
            return f'<div class="sheet-exts">{ext_links("sheet-x")}</div>'
        if item.get("sub"):
            return f'<div class="sheet-exts">{sub_links(item, "sheet-x", en)}</div>'
        return ""

    sheet_links = "".join(
        f'<a class="sheet-main" href="{item["url"]}"{" aria-current=" + chr(34) + "page" + chr(34) if current(item) else ""}>{label(item)}</a>'
        + sheet_sub(item)
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
    bar_lang = (
        '<a class="bar-lang" href="/" lang="fr">FR</a>'
        if en
        else '<a class="bar-lang" href="/en/" lang="en">EN</a>'
    )
    return f"""<header class="bar" data-bar>
  <a class="bar-brand" href="{'/en/' if en else '/'}"><b>JARVIS</b> <span>Private Systems</span></a>
  <nav class="bar-nav" aria-label="{nav_label}">{"".join(bar_links)}</nav>
  <div class="bar-actions">
    {bar_lang}
    <a class="bar-cta" href="{CTA_V2['url']}">{cta_label}</a>
    <button class="bar-menu" type="button" aria-expanded="false" aria-label="{menu_label}" data-menu>
      <span></span><span></span>
    </button>
  </div>
</header>
<nav class="sheet" aria-label="Menu">
  <div class="sheet-in">
    {sheet_links}
    <a class="sheet-cta" href="{CTA_V2['url']}">{cta_label}</a>
    {lang_link}
  </div>
</nav>"""


def autres_extensions(page):
    """Bas des pages de solution : les six autres extensions, pour ne jamais finir dans un cul-de-sac."""
    slugs = [c["slug"] for c in CAPABILITIES]
    here = page["url"].strip("/").split("/")[-1]
    if not page["url"].startswith("/solutions/") or here not in slugs:
        return ""
    liens = "".join(
        f'<a href="/solutions/{c["slug"]}/#jarvis">{ext_icon(c["slug"])}<span>{c["title"]}</span></a>'
        for c in CAPABILITIES if c["slug"] != here
    )
    return f"""<nav class="ext-next" aria-labelledby="ext-next-t">
  <p class="eyebrow" id="ext-next-t">Les autres extensions</p>
  <div class="ext-next-row">{liens}</div>
  <p class="ext-next-all"><a href="/solutions/">Comparer les sept solutions <i aria-hidden="true">→</i></a></p>
</nav>
"""


def toc(page):
    """Menu de sections collant : construit à partir des <section id="…" data-toc="Libellé">.
    Affiché seulement quand la page en compte au moins trois."""
    items = []
    for tag in re.findall(r"<section\b[^>]*>", page["content"]):
        sid, lab = re.search(r'\bid="([^"]+)"', tag), re.search(r'\bdata-toc="([^"]+)"', tag)
        if sid and lab:
            items.append((sid.group(1), lab.group(1)))
    if len(items) < 3:
        return ""
    links = "".join(f'<a href="#{i}">{l}</a>' for i, l in items)
    cta = "" if page["url"].startswith("/contact") else f'<a class="toc-cta" href="{CTA_V2["url"]}">{CTA_V2["label"]}</a>'
    return f'<nav class="toc" aria-label="Sections de la page" data-toc-nav><div class="toc-in">{links}</div>{cta}</nav>'


def footer_v2(page):
    cols = "".join(
        "<div><h2>{t}</h2><nav>{links}</nav></div>".format(
            t=col["title"],
            links="".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in col["links"]),
        )
        for col in FOOTER_COLUMNS
    )
    exts = "".join(f'<a href="/solutions/{c["slug"]}/">{c["title"]}</a>' for c in CAPABILITIES)
    cols = f"<div><h2>Extensions</h2><nav>{exts}</nav></div>" + cols
    return f"""<footer class="foot">
  <div class="foot-grid">
    <div class="foot-brand">
      <b>JARVIS <span>Private Systems</span></b>
      <p>La liberté, par la technologie.<br>Sécurité privée, domotique et IA — Québec.</p>
      <p class="foot-count" hidden><i class="dot" aria-hidden="true"></i>Visites du site <b data-live="visits-foot">—</b></p>
    </div>
    {cols}
  </div>
  <div class="foot-modes" role="group" aria-label="Mode d’affichage">
    <span>Mode</span>
    <button type="button" data-mode-set="base" aria-pressed="false">Base</button>
    <button type="button" class="is-on" data-mode-set="signature" aria-pressed="true">Signature</button>
    <button type="button" data-mode-set="platinum" aria-pressed="false">Platinum</button>
  </div>
  <p class="foot-line"><span>{SITE['copyright']}</span><span>Privé par conception</span></p>
</footer>"""


def document(page):
    """Enveloppe une page complète : doctype, head, header, contenu, footer."""
    v = SITE["asset_version"]
    lang = "fr-CA" if page.get("lang", "fr") == "fr" else "en"
    skip = "Aller au contenu" if page.get("lang", "fr") == "fr" else "Skip to content"
    body_class = page.get("body_class", "")
    demo_css = "".join(
        f'\n<link rel="stylesheet" href="/assets/demos/{name}.css?v={v}">' for name in page.get("assets", [])
    )
    top, bottom = header_v2(page), footer_v2(page)
    content = page["content"]
    nav = toc(page)
    if nav:
        # Juste après la première section (la bande d'ouverture) : il colle ensuite sous la barre.
        cut = content.index("</section>") + len("</section>")
        content = content[:cut] + "\n" + nav + content[cut:]
    autres = autres_extensions(page)
    if autres:
        cut = content.rfind('<section class="cta">')
        content = content[:cut] + autres + "\n" + content[cut:]
    script = f'<script src="/assets/js/wow.js?v={v}" defer></script>'
    # Démos propres à une page : assets/demos/<nom>.css et .js, chargés seulement là.
    for name in page.get("assets", []):
        script += f'\n<script src="/assets/demos/{name}.js?v={v}" defer></script>'
    api = SITE.get("api", "").rstrip("/")
    api_attr = f' data-api="{api}"' if api else ""
    guide = SITE.get("guide", "").rstrip("/")
    if guide:
        api_attr += f' data-guide="{guide}"'
        script += f'\n<script src="/assets/js/guide.js?v={v}" defer></script>'
    return f"""<!doctype html>
<html lang="{lang}"{api_attr}>
<head>
{head(page)}{demo_css}
</head>
<body class="{body_class}">
<a class="skip-link" href="#contenu">{skip}</a>
{top}
<main id="contenu">
{content}
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
