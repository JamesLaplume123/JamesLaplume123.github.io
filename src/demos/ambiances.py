# Démo « Studio lumière » : six ambiances réelles du module Éclairage de JARVIS.
# Les images viennent du module d'éclairage du logiciel (même pièce, six éclairages).
# Règles montrées : un aperçu n'envoie rien; appliquer → envoyé → confirmé; revenir est toujours possible.
# Les photos ne sont jamais retouchées : le changement d'ambiance passe circuit par circuit
# (assets/demos/ambiances.js) et l'intensité est un voile posé dessus.

AMBIANCES = [
    ("heure-doree", "Heure dorée", "linear-gradient(135deg,#ffd18a,#c77a2b)"),
    ("aurore", "Aurore", "linear-gradient(135deg,#3ee0c8,#8a5cff 60%,#ff5fa8)"),
    ("lecture", "Lecture", "linear-gradient(135deg,#fff3dc,#e8c99a)"),
    ("ocean", "Océan", "linear-gradient(135deg,#4fc3ff,#1f4fd8)"),
    ("cinema", "Cinéma", "linear-gradient(135deg,#b07cff,#4b1fa8)"),
    ("nuit-douce", "Nuit douce", "linear-gradient(135deg,#8a6a3a,#2a1f12)"),
]


def html(piece="Salon"):
    imgs = "".join(
        f'<img class="am-img{" is-on" if i == 0 else ""}" data-k="{k}" src="/media/ambiances/{k}.webp" '
        f'alt="Ambiance {n} : la même pièce éclairée autrement" width="1586" height="992" '
        f'loading="{"eager" if i == 0 else "lazy"}" decoding="async">'
        for i, (k, n, _g) in enumerate(AMBIANCES)
    )
    chips = "".join(
        f'<button type="button" data-k="{k}" data-name="{n}" style="--sw:{g}"'
        f'{" class=" + chr(34) + "is-on is-applied" + chr(34) if i == 0 else ""}><i aria-hidden="true"></i>{n}</button>'
        for i, (k, n, g) in enumerate(AMBIANCES)
    )
    return f"""<div class="demo-shell am" data-demo="ambiances" data-rev>
  <div class="demo-top"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span><b>JARVIS · Studio lumière</b>
    <span class="tag tag-sim">Démo · photos du module Éclairage</span></div>
  <div class="demo-body">
    <div class="am-stage">
      {imgs}
      <i class="am-veil" aria-hidden="true"></i>
      <div class="am-card">
        <p class="am-k">{piece} · ambiance</p>
        <h3 data-am="name">Heure dorée</h3>
        <p class="am-state" data-am="state"><i class="dot" aria-hidden="true"></i><span>Appliquée</span></p>
        <div class="am-acts">
          <button type="button" class="am-apply" data-am="apply" disabled>Appliquer</button>
          <button type="button" class="am-back" data-am="back" hidden>Revenir</button>
        </div>
        <label class="am-dim"><span>Intensité</span><input type="range" min="40" max="115" value="100" data-am="dim" aria-label="Intensité"></label>
      </div>
      <p class="am-auto" data-am="auto"><i class="dot" aria-hidden="true"></i>Démonstration automatique · touchez une ambiance</p>
    </div>
    <div class="am-chips" role="group" aria-label="Choisir une ambiance">{chips}</div>
  </div>
</div>
<p class="demo-hint">Un aperçu n’envoie rien · « Appliquer » envoie, puis JARVIS confirme · démonstration, aucun appareil réel</p>"""
