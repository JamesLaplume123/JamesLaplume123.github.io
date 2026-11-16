# Le parcours du visiteur (refonte « clarté », novembre 2026) : comprendre en dix secondes
# ce que JARVIS vend et comment commencer.
#   offre_bref()  : l'offre en trois étapes, court renvoi vers /offre/ (/plateforme/#offre).
# Styles : assets/demos/parcours.css.

ETAPES = [
    ("1", "Le Hub", "Un petit boîtier silencieux, installé et entretenu par nous. Un par lieu, une seule application, même sans Internet."),
    ("2", "Vos extensions", "Vous ajoutez seulement ce qui vous sert : sécurité, domotique, IA, entreprise, route."),
    ("3", "Installation et soutien", "On installe, on vous forme, puis on reste là pour l’entretien et le soutien."),
]


def offre_bref(ident="offre", titre_id="offre-titre", classe="ob", toc=""):
    etapes = "".join(
        f'<li class="ob-step" data-rev><i>{n}</i><b>{t}</b><span>{d}</span></li>' for n, t, d in ETAPES
    )
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""<section class="{classe}" id="{ident}"{toc_attr} aria-labelledby="{titre_id}">
  <div class="ob-head" data-rev>
    <p class="eyebrow">L’offre, en bref</p>
    <h2 id="{titre_id}">Trois étapes. <em>Rien de compliqué.</em></h2>
  </div>
  <ol class="ob-steps">{etapes}</ol>
  <p class="ob-acts" data-rev><a class="pill" href="/offre/">Voir l’offre en détail</a>
  <a class="pill ghost" href="/contact/">Parlons de votre projet</a></p>
  <p class="ob-note" data-rev>Soumission gratuite, par écrit, après une visite de votre lieu.</p>
</section>"""
