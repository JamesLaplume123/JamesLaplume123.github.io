# Coquille « logiciel » des pages de solution : la démonstration s'ouvre dans JARVIS App,
# comme une extension lancée depuis Mes outils (dossier User v25 : barre latérale dorée,
# menu Accueil, Mon espace, Carte, Mes outils, Administration, bannière du lac).
# Le menu mène aux écrans de l'accueil; la liste des extensions mène aux six pages de solution.
# Styles et script : assets/demos/coquille.css et coquille.js.

from config import CAPABILITIES
from demos.app import ADMIN_NOTE, AV_ALEX, BANNER, EXT_ICON, EXT_ON, NAV, NB, WX, face, fr, icon


def html(slug, inner):
    cap = next(c for c in CAPABILITIES if c["slug"] == slug)
    on = slug in EXT_ON
    menu = "".join(
        f'<a class="xs-nav-i{" is-on" if k == "outils" else ""}" href="/#ecran-{k}">{icon(ic)}<span>{lab}</span></a>'
        for (k, lab, _short, ic) in NAV
    )
    exts = "".join(
        f'<a class="xs-ext{" is-on" if c["slug"] == slug else ""}" href="/solutions/{c["slug"]}/#jarvis"'
        f'{" aria-current=\"page\"" if c["slug"] == slug else ""}>{icon(EXT_ICON[c["slug"]])}<span>{c["label"]}</span></a>'
        for c in CAPABILITIES
    )
    return f"""<div class="xs" id="jarvis" data-xs>
  <div class="xs-device">
    <div class="xs-screen">
      <img class="xs-banner" src="{BANNER}" alt="" aria-hidden="true" loading="lazy" decoding="async" width="1990" height="342">
      <nav class="xs-side" aria-label="JARVIS App">
        <div class="xs-brand" aria-hidden="true"><b>JARVIS</b><small>Private Systems</small><em class="xs-mode"></em></div>
        <div class="xs-nav">{menu}</div>
        <div class="xs-exts" aria-label="Extensions">{exts}</div>
        <span class="xs-nav-i xs-admin" title="{fr(ADMIN_NOTE)}">{icon("sliders")}<span>Administration</span></span>
        <p class="xs-motto">Votre espace.<br>À votre image.</p>
      </nav>
      <div class="xs-main">
        <header class="xs-top">
          <a class="xs-search" href="/recherche/">{icon("search")}<span>Que souhaitez-vous faire{NB}?</span></a>
          <span class="xs-wx" title="Saint-Hyacinthe · Environnement Canada">
            <span class="xs-wx-i" aria-hidden="true">{WX}</span>
            <span><b><span data-xs="temp">—</span>{NB}°C</b><small>Saint-Hyacinthe<span class="xs-live"> · en direct</span></small></span>
          </span>
          <span class="xs-pin" title="Emplacement du Hub">{icon("pin")}</span>
          <span class="xs-me">{face(AV_ALEX)}<b>Alex</b>{icon("down")}</span>
        </header>
        <div class="xs-head">
          <p class="xs-crumb"><a href="/#ecran-outils">Mes outils</a><span>/</span><b>{cap["title"]}</b></p>
          <div class="xs-title">
            <span class="xs-title-i">{icon(EXT_ICON[slug])}</span>
            <h3>{cap["title"]}</h3>
            <em class="xs-state{" is-on" if on else ""}">{"Extension activée" if on else "Extension disponible · sur demande"}</em>
          </div>
        </div>
        <div class="xs-body">
{inner}
        </div>
      </div>
    </div>
  </div>
</div>"""
