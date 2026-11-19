# Essai de la page /offre/ dans un vrai navigateur (règles de docs/OFFRE.md).
# Demande Playwright et le site servi sur http://localhost:4173 :
#   python3 tools/build.py && python3 -m http.server 4173 &   puis   python3 tools/test_offre.py
# Sort avec le code 1 si une règle n'est pas respectée.
import asyncio, json
from playwright.async_api import async_playwright
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
        verifie("écosystème : niveau Platinum, VR principal Hub Platinum", "NIVEAU PLATINUM" in eco.upper() and "Lieu principal · Hub Platinum + Boîtier VR" in eco, eco[:300])
        verifie("roulotte : Hub Base relié", "Hub Base + Boîtier VR · relié au principal" in eco, eco[:400])
        # 3. redescendre à Base : aucun Hub ne dépasse le niveau; extensions 2; option ajoutée reste possible
        await pg.evaluate("document.querySelector('input[name=hub][value=base]').click()"); await pg.wait_for_timeout(200)
        eco=await pg.evaluate("document.querySelector('.eco').innerText")
        verifie("Base : VR principal Hub Base", "Lieu principal · Hub Base + Boîtier VR" in eco, eco[:300])
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
        verifie("soumission : niveau, lieux, option nuage", "Niveau Signature" in lien and "Bureau ou commerce (Hub Signature)" in lien and "Copie des vidéos hors du lieu" in lien, lien)
        # 8. rechargement : tout revient tel quel
        avant=await pg.evaluate(f"JSON.stringify([{F}.hub,{F}.lieux,{F}.sols,{F}.etat])")
        await pg.reload(); await pg.wait_for_timeout(900)
        apres=await pg.evaluate(f"JSON.stringify([{F}.hub,{F}.lieux,{F}.sols,{F}.etat])")
        verifie("rechargement : état identique", avant==apres, avant+"\n"+apres)
        # 9. guide
        await pg.evaluate("document.querySelector('[data-gq=coupure] button[data-v=\"2\"]').click()")
        verifie("guide : coupure grave -> Platinum conseillé", await pg.evaluate("document.querySelector('.ct-hub.is-reco').dataset.hub")=="platinum")
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
        verifie("aucune erreur JavaScript", not errs, str(errs))
        await b.close()
    print("RÉSULTAT :", "tout passe" if ok else "à corriger")
asyncio.run(main())
raise SystemExit(0 if ok else 1)
