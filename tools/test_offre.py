# Essai de la page /offre/ dans un vrai navigateur (règles de docs/OFFRE.md).
# Demande Playwright et le site servi sur http://localhost:4173 :
#   python3 tools/build.py && python3 -m http.server 4173 &   puis   python3 tools/test_offre.py
# Sort avec le code 1 si une règle n'est pas respectée.
import asyncio, json, os, sys
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import lieux
from demos import hub as page_appareil
ok=True
def verifie(nom, cond, detail=""):
    global ok
    print(("OK  " if cond else "ÉCHEC ")+nom, "" if cond else detail)
    ok = ok and cond
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:4173/offre/'); await pg.wait_for_timeout(800)
        F="JSON.parse(localStorage.getItem('jarvis-forfait')||'{}')"
        q=lambda id: f"+document.querySelector('.ct-item[data-id={id}] output').value"
        lieu=lambda l: pg.evaluate(f"document.querySelector('#lieu .lx-b[data-lieu={l}]').click()")
        # 1. VR + roulotte : niveau conseillé Signature; ensemble VR = boîtier Signature
        await lieu('vr'); await lieu('roulotte'); await pg.wait_for_timeout(200)
        verifie("niveau conseillé = signature", await pg.evaluate(f"{F}.hub")=="signature")
        await pg.evaluate("document.querySelector('[data-ens=vr]').click()")
        verifie("ensemble VR : Boîtier VR Signature", await pg.evaluate(q('vrs'))==1 and await pg.evaluate(q('vrb'))==0)
        # 2. passer à Platinum : le boîtier suit
        await pg.evaluate("document.querySelector('input[name=hub][value=platinum]').click()"); await pg.wait_for_timeout(200)
        verifie("niveau Platinum : Boîtier VR Platinum", await pg.evaluate(q('vrp'))==1 and await pg.evaluate(q('vrs'))==0)
        verifie("Platinum : 5 extensions incluses", await pg.evaluate("document.querySelectorAll('.ct-sol.is-niveau').length")==5)
        eco=await pg.evaluate("document.querySelector('.eco').innerText")
        verifie("écosystème : niveau Platinum, VR principal JARVIS Pro", "NIVEAU PLATINUM" in eco.upper() and "Lieu principal · JARVIS Pro + Boîtier VR" in eco, eco[:300])
        verifie("roulotte : JARVIS Mini relié", "JARVIS Mini + Boîtier VR · relié au principal" in eco, eco[:400])
        # 3. redescendre à Base : aucun appareil ne dépasse le niveau; extensions 2; option ajoutée reste possible
        await pg.evaluate("document.querySelector('input[name=hub][value=base]').click()"); await pg.wait_for_timeout(200)
        eco=await pg.evaluate("document.querySelector('.eco').innerText")
        verifie("Base : VR principal JARVIS Mini", "Lieu principal · JARVIS Mini + Boîtier VR" in eco, eco[:300])
        verifie("Base : 2 extensions incluses", await pg.evaluate("document.querySelectorAll('.ct-sol.is-niveau').length")==2)
        verifie("Base : Boîtier VR Base", await pg.evaluate(q('vrb'))==1 and await pg.evaluate(q('vrp'))==0)
        await pg.evaluate("document.querySelector('.ct-sol[data-sol=secu] input').click()"); await pg.wait_for_timeout(100)
        verifie("option Sécurité ajoutée au forfait", await pg.evaluate(f"{F}.sols")==["securite-intelligente"], str(await pg.evaluate(f"{F}.sols")))
        # 4. retirer le VR : son ensemble part avec lui
        await pg.evaluate("document.querySelector('.eco-x[data-lieu=vr]').click()"); await pg.wait_for_timeout(200)
        verifie("VR retiré : ensemble retiré", await pg.evaluate(q('vrb'))==0 and await pg.evaluate(q('temp'))==0 and await pg.evaluate(f"Object.keys({F}.etat.e).length")==0)
        # 5. entreprise : bureau -> bloc entreprise visible, ensemble avec réceptionniste
        await lieu('bureau'); await pg.wait_for_timeout(200)
        verifie("bureau : public entreprise/deux", await pg.evaluate("document.documentElement.dataset.public") in ("deux","entreprise"))
        verifie("bloc Entreprise visible", await pg.evaluate("getComputedStyle(document.querySelector('#entreprise')).display")!="none")
        await pg.evaluate("document.querySelector('[data-ens=bureau]').click()"); await pg.wait_for_timeout(150)
        verifie("ensemble bureau : socle, 1 ligne, 3 automatisations", await pg.evaluate("[document.querySelector('input[name=socle]').checked, +document.querySelector('.ct-ent-recep output').value, document.querySelectorAll('input[name=auto]:checked').length]")==[True,1,3])
        tips=await pg.evaluate("document.querySelector('[data-cart-tips]').innerText")
        verifie("À prévoir : entreprise demande Signature (niveau manuel Base)", "Signature ou Platinum" in tips, tips)
        await pg.evaluate("document.querySelector('[data-cart-tips] [data-up]').click()"); await pg.wait_for_timeout(200)
        verifie("bouton « Passer au niveau Signature »", await pg.evaluate(f"{F}.hub")=="signature")
        # 6. flotte : Mobilité suit (2 véhicules)
        await lieu('flotte'); await pg.wait_for_timeout(150)
        verifie("flotte : Mobilité × 2", await pg.evaluate("+document.querySelector('.ct-sol[data-sol=mob] output').value")==2)
        # 7. nuage + lien de soumission
        await pg.evaluate("document.querySelector('input[name=nuage][value=n_video]').click()"); await pg.wait_for_timeout(100)
        await pg.evaluate("document.querySelector('[data-cart-open]').click()"); await pg.wait_for_timeout(500)
        lien=await pg.evaluate("decodeURIComponent((document.querySelector('.fo-go')||{}).href||'')")
        print("   soumission :", lien.split('config=')[-1][:400])
        verifie("soumission : niveau, lieux, option nuage", "Niveau Signature" in lien and "Bureau ou commerce (JARVIS)" in lien and "Copie des vidéos hors du lieu" in lien, lien)
        # 8. rechargement : tout revient tel quel
        avant=await pg.evaluate(f"JSON.stringify([{F}.hub,{F}.lieux,{F}.sols,{F}.etat])")
        await pg.reload(); await pg.wait_for_timeout(900)
        apres=await pg.evaluate(f"JSON.stringify([{F}.hub,{F}.lieux,{F}.sols,{F}.etat])")
        verifie("rechargement : état identique", avant==apres, avant+"\n"+apres)
        # 9. guide
        await pg.evaluate("document.querySelector('[data-gq=coupure] button[data-v=\"2\"]').click()")
        verifie("guide : coupure grave -> Platinum conseillé", await pg.evaluate("document.querySelector('.ct-nvc.is-reco').dataset.hub")=="platinum")
        # 10. tout retirer
        await pg.evaluate("window.JarvisCatalogue.vider()"); await pg.wait_for_timeout(200)
        verifie("tout retirer : forfait vide", await pg.evaluate(f"[{F}.lieux.length,{F}.sols.length,{F}.autres.length,{F}.hub]")==[0,0,0,""], str(await pg.evaluate(f"{F}")))
        # 11. plan tout composé (lien donné par JARVIS)
        await pg.goto('http://localhost:4173/offre/?lieux=maison,chalet,auto,inconnu&niveau=platinum&ens=tout#composer'); await pg.wait_for_timeout(900)
        plan=await pg.evaluate(f"[{F}.lieux, {F}.hub, {F}.manuel, Object.keys({F}.etat.e).sort(), +document.querySelector('.ct-sol[data-sol=mob] output').value, location.search, {F}.autres.some(a=>a.id==='mobb')]")
        verifie("plan : lieux, niveau, ensembles, Mobilité, adresse nettoyée", plan==[["maison","chalet","auto"],"platinum",True,["auto","chalet","maison"],1,"",True], str(plan))
        await pg.goto('http://localhost:4173/offre/?lieux=ferme&ens=tout'); await pg.wait_for_timeout(900)
        plan=await pg.evaluate(f"[{F}.hub, {F}.manuel, document.documentElement.dataset.public, document.querySelector('input[name=socle]').checked]")
        verifie("plan sans niveau : niveau conseillé (ferme -> platinum), entreprise", plan==["platinum",False,"entreprise",True], str(plan))
        # 12. plusieurs lieux : le niveau dit combien se relient
        await pg.goto('http://localhost:4173/offre/?lieux=maison,condo,chalet,garage&niveau=signature'); await pg.wait_for_timeout(900)
        tips=await pg.evaluate("document.querySelector('[data-cart-tips]').innerText")
        verifie("4 lieux au niveau Signature : À prévoir, passer à Platinum", "jusqu’à trois lieux; vous en avez 4" in tips, tips)
        await pg.goto('http://localhost:4173/offre/?lieux=condo,chalet&niveau=base'); await pg.wait_for_timeout(900)
        tips=await pg.evaluate("document.querySelector('[data-cart-tips]').innerText"); eco=await pg.evaluate("document.querySelector('.eco-note').innerText")
        verifie("2 lieux au niveau Base : chacun veille seul", "chaque lieu veille seul" in tips and "chaque lieu veille seul" in eco, tips+" | "+eco)
        verifie("aucune erreur JavaScript", not errs, str(errs))
        # 13. sur un téléphone (écran tactile) et avec « réduire les animations » : le forfait doit tourner aussi.
        #     (Le 19 novembre 2026, deux sorties hâtives de wow.js coupaient tout le forfait sur les téléphones.)
        for nom, options in (("téléphone tactile", dict(p.devices["iPhone 13"])), ("animations réduites", dict(viewport={"width": 1280, "height": 800}, reduced_motion="reduce"))):
            ctx = await b.new_context(**options); pm = await ctx.new_page(); em = []
            pm.on('pageerror', lambda e: em.append(str(e)))
            await pm.goto('http://localhost:4173/offre/?lieux=maison,chalet,auto&niveau=signature&ens=tout#composer'); await pm.wait_for_timeout(1200)
            etat = await pm.evaluate(f"[!!window.JarvisForfait, ({F}.lieux||[]).length, {F}.hub, !!document.querySelector('.eco'), location.search]")
            verifie(f"{nom} : le plan s'ouvre et l'écosystème se dessine", etat == [True, 3, "signature", True, ""], str(etat))
            el = pm.locator('#lieu .lx-b[data-lieu="vr"]')
            await el.scroll_into_view_if_needed()
            await (el.tap() if options.get("has_touch") else el.click()); await pm.wait_for_timeout(300)
            verifie(f"{nom} : toucher un lieu l'ajoute", "vr" in await pm.evaluate(f"{F}.lieux"))
            verifie(f"{nom} : aucune erreur JavaScript", not em, str(em))
            await ctx.close()
        # 14. une seule règle, deux endroits : cerveaux() du site (wow.js) et de la construction (src/lieux.py)
        #     doivent donner le même appareil à chaque lieu; la page /plateforme/ affiche ce résultat.
        await pg.goto('http://localhost:4173/offre/'); await pg.wait_for_timeout(600)
        cas = [(["maison", "chalet", "garage", "ferme", "bateau", "vr"], ""), (["maison", "chalet", "auto"], "signature"), (["condo", "chalet"], "base"),
               (["vr", "roulotte"], "platinum"), (["auto", "moto"], ""), (["chalet", "maison", "domaine"], ""), (["ferme", "maison"], "base"), (["bureau", "avion", "flotte"], "")]
        for ids, niv in cas:
            js = await pg.evaluate("o => window.JarvisForfait.cerveaux(o)", {"lieux": ids, "hub": niv})
            n, prin, app = lieux.cerveaux(ids, niv or None)
            py = {"niveau": n or "", "principal": prin or "", "hub": {i: app[i] or "" for i in ids}}
            verifie(f"même règle des deux côtés : {', '.join(ids)}" + (f" au niveau {niv}" if niv else ""), js == py, f"site {js} | construction {py}")
        ids = [l[1] for l in page_appareil.LIEUX]
        js = await pg.evaluate("o => window.JarvisForfait.cerveaux(o)", {"lieux": ids, "hub": ""})
        await pg.goto('http://localhost:4173/plateforme/'); await pg.wait_for_timeout(600)
        vus = await pg.evaluate("[...document.querySelectorAll('.hb-lx-t')].map(t => [...t.querySelectorAll('.hb-lx-hub')].map(x => x.textContent.trim()))")
        attendu = [[lieux.HUB_NOM[js["hub"][i]]] + ([lieux.PAR_ID[i]["boitier"]] if lieux.PAR_ID[i].get("boitier") else []) + (["Lieu principal"] if i == js["principal"] else []) for i in ids]
        verifie("page L'appareil : chaque lieu d'exemple porte l'appareil que donne la règle", vus == attendu, f"{vus} | {attendu}")
        verifie("page L'appareil : aucune erreur JavaScript", not errs, str(errs))
        # 15. les trois niveaux côte à côte : chaque colonne nomme son appareil, et ce qu'elle dit « incluse »
        #     est exactement ce que le niveau coche à l'étape 3 (une seule source : NIVEAUX).
        await pg.goto('http://localhost:4173/offre/'); await pg.wait_for_timeout(700)
        cols = await pg.evaluate("[...document.querySelectorAll('.ct-nvc')].map(c => [c.dataset.hub, c.querySelector('strong').textContent, c.querySelector('em').textContent, c.querySelectorAll('.ct-nv-c.is-oui').length, c.querySelectorAll('.ct-nv-c').length])")
        verifie("niveaux : trois colonnes, chacune avec son appareil", [c[:3] for c in cols] == [["base", "Base", "JARVIS Mini"], ["signature", "Signature", "JARVIS"], ["platinum", "Platinum", "JARVIS Pro"]], str(cols))
        verifie("niveaux : même nombre de lignes dans chaque colonne", len({c[4] for c in cols}) == 1 and cols[0][4] >= 10, str(cols))
        for hub, _, _, incluses, _ in cols:
            await pg.evaluate(f"document.querySelector('input[name=hub][value={hub}]').click()"); await pg.wait_for_timeout(200)
            coche = await pg.evaluate("document.querySelectorAll('.ct-sol.is-niveau').length")
            verifie(f"niveau {hub} : la colonne annonce {incluses} extensions incluses, l'étape 3 en coche autant", incluses == coche, f"{incluses} contre {coche}")
        ctx = await b.new_context(**p.devices["iPhone 13"]); pm = await ctx.new_page()
        await pm.goto('http://localhost:4173/offre/'); await pm.wait_for_timeout(900)
        col = pm.locator('.ct-nvc[data-hub="platinum"] .ct-nv-c').nth(6)
        await col.scroll_into_view_if_needed(); await col.tap(); await pm.wait_for_timeout(300)
        verifie("téléphone : toucher n'importe où dans une colonne choisit ce niveau", await pm.evaluate(f"{F}.hub") == "platinum")
        large = await pm.evaluate("[document.documentElement.scrollWidth, window.innerWidth, [...document.querySelectorAll('.ct-nvc')].every(c => { const r = c.getBoundingClientRect(); return r.left >= 0 && r.right <= window.innerWidth; })]")
        verifie("téléphone : les trois colonnes tiennent dans l'écran", large[0] <= large[1] and large[2], str(large))
        hauts = await pm.evaluate("[...document.querySelectorAll('.ct-nvc')].map(c => [...c.querySelectorAll('.ct-nv-c')].map(x => Math.round(x.getBoundingClientRect().top)))")
        verifie("téléphone : les lignes s'alignent d'une colonne à l'autre", hauts[0] == hauts[1] == hauts[2], str(hauts))
        await ctx.close()
        await b.close()
    print("RÉSULTAT :", "tout passe" if ok else "à corriger")
asyncio.run(main())
raise SystemExit(0 if ok else 1)
