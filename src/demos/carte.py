# « Radar en direct » : carte sombre (OpenFreeMap) + radar d'Environnement Canada (GeoMet),
# animé sur la dernière heure et demie. BouLance est placée à Saint-Hyacinthe (lieu de base,
# choix de James : aucune position GPS en direct). La bibliothèque de carte (MapLibre) est
# hébergée sur le site et chargée seulement quand la carte approche de l'écran.


def html():
    return """<div class="demo-shell ct" data-demo="carte" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Radar en direct</b>
    <span class="ct-time" data-ct="time">—</span>
    <span class="tag tag-real">Données réelles</span></div>
  <div class="demo-body ct-body">
    <div class="ct-map" data-ct="map" role="img" aria-label="Carte radar des précipitations autour de Saint-Hyacinthe">
      <p class="ct-wait" data-ct="wait">Chargement de la carte…</p>
    </div>
    <div class="ct-card">
      <p class="ct-k">BouLance · lieu de base</p>
      <h3>Saint-Hyacinthe</h3>
      <p class="ct-now"><b data-ct="temp">—</b><span data-ct="cond">Conditions actuelles</span></p>
      <p class="ct-note">Position fixe, choisie par le propriétaire : aucune position en direct n’est publiée.</p>
    </div>
    <div class="ct-legend" aria-hidden="true"><span>Faible</span><i></i><span>Forte</span><em>Pluie · neige</em></div>
  </div>
  <div class="ct-bar">
    <button type="button" class="ct-play" data-ct="play" aria-label="Mettre en pause l’animation">❚❚</button>
    <div class="ct-track" data-ct="track"></div>
    <span class="ct-src">Radar : Environnement et Changement climatique Canada · carte : OpenFreeMap, © OpenMapTiles, © contributeurs OpenStreetMap</span>
  </div>
</div>"""
