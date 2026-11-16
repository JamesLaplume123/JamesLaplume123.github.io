# Contact — transformer l'intérêt en conversation utile.
# Envoi sans quitter la page (wow.js) : d'abord le service du site (SITE["api"], le Worker
# Cloudflare qui envoie par Resend et garde la demande pour JARVIS), sinon FormSubmit.
# Si tout échoue, le visiteur reçoit un lien courriel avec son message déjà rédigé.
# Sans JavaScript, le formulaire reste un envoi classique vers FormSubmit.

from config import SITE

API = SITE.get("api", "").rstrip("/")
ENDPOINT = f"{API}/contact" if API else ""

PAGE = {
    "url": "/contact/",
    "v2": True,
    "title": "Contact | Parlons de votre projet",
    "description": (
        "Présentez votre projet, votre problème "
        "ou une possibilité de collaboration à James Laplume."
    ),
    "og_image": "/media/product/jarvis-command-center-preview-og.jpg",
    "content": f"""
<section class="plain-top">
  <p class="eyebrow" data-rev>Contact</p>
  <h1 data-rev>Parlons de <em>votre projet.</em></h1>
  <p class="lead" data-rev>Décrivez votre lieu en quelques lignes, ou laissez simplement votre nom
  pour rester informé. James vous répond personnellement.</p>
</section>

<section class="sect" style="padding-top:2rem" aria-label="Formulaire">
  <div class="contact-form">
    <form class="form-card" data-rev data-contact action="https://formsubmit.co/laplumejames@gmail.com" method="POST"
          data-endpoint="{ENDPOINT}" data-fallback="https://formsubmit.co/ajax/laplumejames@gmail.com">
      <input type="hidden" name="_subject" value="Nouveau message — jarvisprivatesystems.com">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="https://jarvisprivatesystems.com/merci/">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="form-grid">
        <div class="field">
          <label for="f-nom">Nom</label>
          <input id="f-nom" name="nom" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="f-courriel">Courriel</label>
          <input id="f-courriel" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field full">
          <label id="env-label">Environnement visé</label>
          <div class="choices" role="radiogroup" aria-labelledby="env-label">
            <span class="choice"><input type="radio" id="env-res" name="environnement" value="Résidence"><label for="env-res">Résidence</label></span>
            <span class="choice"><input type="radio" id="env-ent" name="environnement" value="Entreprise"><label for="env-ent">Entreprise</label></span>
            <span class="choice"><input type="radio" id="env-mob" name="environnement" value="Mobilité"><label for="env-mob">Mobilité</label></span>
            <span class="choice"><input type="radio" id="env-nsp" name="environnement" value="Je ne sais pas encore" checked><label for="env-nsp">Je ne sais pas encore</label></span>
          </div>
        </div>
        <div class="field">
          <label for="f-org">Organisation ou projet</label>
          <input id="f-org" name="organisation" type="text">
        </div>
        <div class="field">
          <label for="f-region">Ville ou région</label>
          <input id="f-region" name="region" type="text" autocomplete="address-level2">
        </div>
        <div class="field">
          <label for="f-role">Vous êtes</label>
          <select id="f-role" name="profil">
            <option>Client potentiel</option>
            <option>Partenaire technique</option>
            <option>Recherche ou institution</option>
            <option>Investisseur ou accompagnateur</option>
            <option>Autre</option>
          </select>
        </div>
        <div class="field">
          <label for="f-sujet">Sujet principal</label>
          <select id="f-sujet" name="sujet">
            <option>Mon projet</option>
            <option>Rester informé</option>
            <option>Démonstration JARVIS</option>
            <option>Environnements intelligents</option>
            <option>IA privée et connaissances</option>
            <option>Sécurité intelligente</option>
            <option>Automatisation d’entreprise</option>
            <option>Réseau et cybersécurité</option>
            <option>Diagnostic &amp; continuité</option>
            <option>Mobilité</option>
            <option>Laboratoire mobile JARVIS</option>
            <option>Recherche ou partenariat</option>
          </select>
        </div>
        <div class="field full">
          <label for="f-message">Votre message</label>
          <textarea id="f-message" name="message" required
            placeholder="Votre lieu, ce qui vous dérange, ce qui est déjà en place."></textarea>
        </div>
      </div>
      <p class="form-note">Aucune liste d’envoi, aucun suivi publicitaire :
      <a href="/confidentialite/" style="color:#d4d4d8">politique de confidentialité</a>.</p>
      <button class="pill" type="submit"><span class="lbl">Envoyer le message</span><i class="spin" aria-hidden="true"></i></button>
      <p class="form-status" aria-live="polite"></p>
    </form>
    <p class="pro-suite" data-rev><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
  </div>
</section>
""",
}
