# Le parcours du visiteur (refonte « clarté », novembre 2026) : comprendre en dix secondes
# ce que JARVIS vend et comment commencer.
#   offre_bref()  : l'offre en trois étapes, court renvoi vers /offre/ (/plateforme/#offre).
# Styles : assets/demos/parcours.css.

ETAPES = [
    ("1", "Le Hub · dès 590 $", "Un petit boîtier silencieux, payé une fois. Base, Signature ou Platinum selon la taille du lieu. Un par lieu, une seule application, même sans Internet."),
    ("2", "Vos solutions · dès 10 $/mois", "Comme des apps : sécurité, diagnostic, IA privée, réseau, mobilité, entreprise. Environnements intelligents est inclus. Annulables en tout temps."),
    ("3", "Le matériel et l’installation", "Capteurs, caméras, boîtiers payés une fois. Vous installez vous-même (inclus), guidé en vidéo, ou on s’en occupe."),
]


def offre_bref(ident="offre", titre_id="offre-titre", classe="ob", toc=""):
    etapes = "".join(
        f'<li class="ob-step" data-rev><i>{n}</i><b>{t}</b><span>{d}</span></li>' for n, t, d in ETAPES
    )
    toc_attr = f' data-toc="{toc}"' if toc else ""
    return f"""<section class="{classe}" id="{ident}"{toc_attr} aria-labelledby="{titre_id}">
  <div class="ob-head" data-rev>
    <p class="eyebrow">L’offre, en bref</p>
    <h2 id="{titre_id}">Un Hub, vos solutions, le matériel. <em>Le total en direct.</em></h2>
  </div>
  <ol class="ob-steps">{etapes}</ol>
  <p class="ob-acts" data-rev><a class="pill" href="/catalogue/">Composer mon JARVIS</a>
  <a class="pill ghost" href="/offre/">Comment ça se compose</a></p>
  <p class="ob-note" data-rev>Prix en dollars canadiens, points de départ : chaque soumission est confirmée par écrit, ligne par ligne.</p>
</section>"""
