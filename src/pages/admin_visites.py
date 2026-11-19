# Page privée « Visites du site » : le journal des visites, réservé à James.
# Hors menu, hors sitemap, robots noindex/nofollow, /admin/ refusé dans robots.txt.
# Le jeton LEADS_TOKEN est collé par James et gardé seulement dans sessionStorage (onglet ouvert);
# il n'est envoyé qu'au service du site (GET /visits/log, GET /chats). Rien de secret n'est écrit ici.
# Trois vues : Visiteurs (une ligne par adresse IP), Conversations avec JARVIS (GET /chats, même jeton)
# et Journal (chaque page vue). Un clic sur un visiteur ou une adresse ouvre sa fiche : son parcours
# et ses questions à JARVIS dans un seul fil.
# Les chiffres viennent des compteurs par jour du service; le journal se charge par tranches
# (« Charger plus »); le relevé d'avant la mise en service vient d'une clé d'archive du service,
# jamais du dépôt (il contient des adresses IP).
# Cartes noires : monde en points (demos/reseau_geo.py) et sud du Québec (demos/app_geo.py),
# toutes deux tirées de Natural Earth, sans tuiles externes. Code : assets/demos/visites.css et .js.

import json
import math
from html import escape

from demos import reseau_geo as WORLD
from demos.app_geo import BOX, GEO

# Même projection que la Carte de l'app (kilomètres, origine Saint-Hyacinthe).
QC_LAT0, QC_LON0 = 45.630, -72.957
QC_KX = 111.32 * math.cos(math.radians(47.0))
QC_KY = 111.13


def _world_dots():
    """Les terres en points (un point tous les 2°), en un seul tracé SVG."""
    d = []
    for j, row in enumerate(WORLD.ROWS.split(",")):
        for c, ch in enumerate(row):
            v = int(ch, 16)
            for b in range(4):
                i = c * 4 + b
                if v & (8 >> b) and i < WORLD.COLS:
                    d.append(f"M{i * WORLD.U + WORLD.U / 2:g} {j * WORLD.U + WORLD.U / 2:g}h0")
    return "".join(d)


def _maps():
    W, H = WORLD.SIZE
    x, y, w, h = BOX
    proj = {
        "world": {"lat0": WORLD.LAT0, "lon0": WORLD.LON0, "step": WORLD.STEP, "u": WORLD.U, "w": W, "h": H},
        "qc": {"lat0": QC_LAT0, "lon0": QC_LON0, "kx": round(QC_KX, 4), "ky": QC_KY, "box": list(BOX)},
    }
    return f"""<div class="av-maps" data-proj="{escape(json.dumps(proj), quote=True)}">
      <figure class="av-card av-map">
        <figcaption><span>Monde</span><b data-av="world-n">—</b></figcaption>
        <svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Carte du monde : un point par visite">
          <path class="av-dots" d="{_world_dots()}"/>
          <g class="av-pts" data-av="world"></g>
        </svg>
      </figure>
      <figure class="av-card av-map">
        <figcaption><span>Sud du Québec</span><b data-av="qc-n">—</b></figcaption>
        <svg viewBox="{x} {y} {w} {h}" preserveAspectRatio="xMidYMax slice" role="img" aria-label="Carte du sud du Québec : un point par visite">
          <rect x="{x - 400}" y="{y - 400}" width="{w + 800}" height="{h + 800}" class="av-qc-sea"/>
          <path class="av-qc-land" d="{GEO["land"]}"/>
          <path class="av-qc-lakes" d="{GEO["lakes"]}"/>
          <path class="av-qc-border" d="{GEO["border"]}"/>
          <path class="av-qc-hw" d="{GEO["hw"]}"/>
          <g class="av-pts" data-av="qc"></g>
        </svg>
      </figure>
    </div>"""


PAGE = {
    "url": "/admin/visites/",
    "v2": True,
    "noindex": True,
    "robots": "noindex,nofollow",
    "assets": ["visites"],
    "title": "Visites du site | JARVIS Private Systems",
    "description": "Page privée : journal des visites du site.",
    "content": f"""
<section class="plain-top av-top">
  <p class="eyebrow">Privé · réservé à James</p>
  <h1>Visites du site.</h1>
  <p class="lead">D’où viennent les visiteurs, ce qu’ils regardent et avec quel appareil.
  Chaque visite est gardée 24 mois, puis effacée automatiquement.</p>
</section>

<section class="av" data-av-root>
  <div class="av-card av-access">
    <form class="av-token" data-av="form" autocomplete="off">
      <label for="av-jeton">Jeton d’accès du service</label>
      <div class="av-token-row">
        <input id="av-jeton" name="jeton" type="password" spellcheck="false" autocomplete="off"
          placeholder="Coller le jeton LEADS_TOKEN">
        <button class="pill" type="submit">Ouvrir le journal</button>
      </div>
      <p class="av-hint">Gardé seulement dans cet onglet, le temps de la session, et envoyé
      uniquement au service du site.</p>
    </form>
    <div class="av-tools">
      <button type="button" class="pill ghost" data-av="refresh">Actualiser</button>
      <button type="button" class="pill ghost" data-av="csv">Exporter en CSV</button>
      <button type="button" class="pill ghost" data-av="forget">Oublier le jeton</button>
      <button type="button" class="pill ghost" data-av="me">Ne pas compter mes visites sur cet appareil</button>
    </div>
    <p class="av-status" data-av="status" role="status" aria-live="polite">Collez le jeton pour afficher le journal.</p>
  </div>

  <div class="av-kpis">
    <div class="av-card av-kpi"><span>Aujourd’hui</span><b data-av="k-day">—</b><small data-av="k-day-p">pages vues —</small></div>
    <div class="av-card av-kpi"><span>7 jours</span><b data-av="k-7">—</b><small data-av="k-7-p">pages vues —</small></div>
    <div class="av-card av-kpi"><span>30 jours</span><b data-av="k-30">—</b><small data-av="k-30-p">pages vues —</small></div>
    <div class="av-card av-kpi"><span>Depuis le début</span><b data-av="k-all">—</b><small data-av="k-all-p">pages vues —</small></div>
  </div>

  <nav class="av-nav" aria-label="Vues">
    <div class="av-tabs" role="tablist">
      <button type="button" role="tab" class="av-tab is-on" data-tab="visiteurs" aria-selected="true">Visiteurs <b data-av="n-visiteurs">—</b></button>
      <button type="button" role="tab" class="av-tab" data-tab="conversations" aria-selected="false">Conversations <b data-av="n-conversations">—</b></button>
      <button type="button" role="tab" class="av-tab" data-tab="journal" aria-selected="false">Journal <b data-av="n-journal">—</b></button>
      <button type="button" role="tab" class="av-tab" data-tab="carte" aria-selected="false">Carte</button>
    </div>
    <input type="search" class="av-search" data-av="q" placeholder="Chercher une adresse IP, une ville, un mot…" aria-label="Chercher dans les visiteurs, les conversations et le journal">
    <label class="av-check"><input type="checkbox" data-av="f-bots" checked><span>Masquer les robots</span></label>
  </nav>

  <div class="av-card av-log av-pane" data-pane="visiteurs">
    <div class="av-log-head">
      <h2>Visiteurs</h2>
      <label class="av-check"><input type="checkbox" data-av="f-parle"><span>Seulement ceux qui ont parlé à JARVIS</span></label>
      <p class="av-count" data-av="v-count">—</p>
    </div>
    <div class="av-table" role="table" aria-label="Visiteurs, du plus récent au plus ancien">
      <div class="av-row av-vrow av-th" role="row">
        <span role="columnheader">Visiteur</span><span role="columnheader">Adresse IP</span>
        <span role="columnheader">Appareil</span><span role="columnheader">Visites</span>
        <span role="columnheader">Pages</span><span role="columnheader">JARVIS</span>
        <span role="columnheader">Dernière visite</span>
      </div>
      <div data-av="v-rows" role="rowgroup"></div>
    </div>
    <p class="av-empty" data-av="v-empty">Aucun visiteur à afficher.</p>
  </div>

  <div class="av-card av-log av-pane" data-pane="conversations" hidden>
    <div class="av-log-head">
      <h2>Conversations avec JARVIS</h2>
      <p class="av-count" data-av="c-count">—</p>
    </div>
    <p class="av-hint av-cstate" data-av="c-state"></p>
    <div class="cv-liste" data-av="c-rows"></div>
    <div class="av-more"><button type="button" class="pill ghost" data-av="c-more" hidden>Charger plus</button></div>
  </div>

  <div class="av-card av-log av-pane" data-pane="journal" hidden>
    <div class="av-log-head">
      <h2>Journal</h2>
      <div class="av-filters">
        <label><span>Pays</span><select data-av="f-pays"><option value="">Tous les pays</option></select></label>
        <label><span>Page</span><select data-av="f-page"><option value="">Toutes les pages</option></select></label>
      </div>
      <p class="av-count" data-av="count">0 visite</p>
    </div>
    <div class="av-table" role="table" aria-label="Visites, les plus récentes d’abord">
      <div class="av-row av-th" role="row">
        <span role="columnheader">Heure (Toronto)</span><span role="columnheader">Lieu</span>
        <span role="columnheader">Fournisseur</span><span role="columnheader">Adresse IP</span>
        <span role="columnheader">Page</span><span role="columnheader">Appareil</span>
        <span role="columnheader">Provenance</span>
      </div>
      <div data-av="rows" role="rowgroup"></div>
    </div>
    <p class="av-empty" data-av="empty">Aucune visite à afficher.</p>
    <div class="av-more"><button type="button" class="pill ghost" data-av="more" hidden>Charger plus</button></div>
  </div>

  <div class="av-pane" data-pane="carte" hidden>
  {_maps()}
  </div>

  <div class="av-card av-log av-archive av-pane-extra" data-av="archive" hidden>
    <div class="av-log-head">
      <h2>Avant le 15 novembre 2026</h2>
      <p class="av-count" data-av="a-count">—</p>
    </div>
    <p class="av-hint" data-av="a-lead"></p>
    <div class="av-table" role="table" aria-label="Relevé d’avant la mise en service du journal">
      <div class="av-row av-arow av-th" role="row">
        <span role="columnheader">Lieu</span><span role="columnheader">Fournisseur</span>
        <span role="columnheader">Adresse IP</span><span role="columnheader">Appels</span>
      </div>
      <div data-av="a-rows" role="rowgroup"></div>
    </div>
    <p class="av-note" data-av="a-note"></p>
  </div>

  <div class="av-voile" data-av="voile" hidden></div>
  <aside class="av-fiche" data-av="fiche" aria-label="Fiche du visiteur" hidden>
    <button type="button" class="av-fermer" data-av="fermer" aria-label="Fermer la fiche">×</button>
    <div data-av="fiche-corps"></div>
  </aside>
</section>
""",
}
