# Contact — transformer l'intérêt en conversation utile. Version wow.
# Le formulaire passe par FormSubmit vers laplumejames@gmail.com (comme avant).

PAGE = {
    "url": "/contact/",
    "v2": True,
    "title": "Contact | Réserver une démonstration JARVIS",
    "description": (
        "Réservez une démonstration de JARVIS ou présentez votre projet, votre problème "
        "ou une possibilité de collaboration à James Laplume."
    ),
    "og_image": "/media/product/jarvis-command-center-preview-og.jpg",
    "content": """
<section class="plain-top">
  <p class="eyebrow" data-rev>Contact</p>
  <h1 data-rev>Voyez JARVIS <em>de vos yeux.</em></h1>
  <p class="lead" data-rev>Client potentiel, partenaire technique, chercheur ou investisseur :
  décrivez ce que vous cherchez à comprendre, relier ou automatiser, et réservez une
  démonstration en direct.</p>
</section>

<section class="sect" style="padding-top:2rem">
  <div class="sect-head" style="align-items:start">
    <div data-rev>
      <p class="eyebrow">Premier échange</p>
      <h2 style="margin-top:1rem">Une idée claire peut commencer par <em>quelques
      lignes.</em></h2>
      <p style="color:var(--dim);margin-top:1.2rem">Je vous répondrai sur ce qui semble
      réalisable, ce qui mérite une première preuve et les informations nécessaires pour
      aller plus loin.</p>
      <p style="margin-top:1.6rem"><a class="pill ghost" href="mailto:laplumejames@gmail.com">laplumejames@gmail.com</a></p>
      <div class="meta" style="display:flex;gap:.7rem;flex-wrap:wrap;margin-top:2rem">
        <span class="chip">Réponse personnelle</span>
        <span class="chip">Québec, Canada</span>
        <span class="chip">Échanges confidentiels</span>
      </div>
    </div>
    <form class="form-card" data-rev action="https://formsubmit.co/laplumejames@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="Nouveau message — jameslaplume.ca">
      <input type="hidden" name="_next" value="https://jameslaplume.ca/merci/">
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
          <label for="f-org">Organisation ou projet</label>
          <input id="f-org" name="organisation" type="text">
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
            <option>Démonstration JARVIS</option>
            <option>Environnement intelligent</option>
            <option>IA privée et connaissances</option>
            <option>Sécurité intelligente</option>
            <option>Automatisation d’entreprise</option>
            <option>Réseau et cybersécurité</option>
            <option>Diagnostic & continuité</option>
            <option>Laboratoire mobile JARVIS</option>
            <option>Recherche ou partenariat</option>
          </select>
        </div>
        <div class="field full">
          <label for="f-message">Votre message</label>
          <textarea id="f-message" name="message" required
            placeholder="Le contexte, le problème, les systèmes déjà présents et le type de collaboration recherché."></textarea>
        </div>
      </div>
      <p class="form-note">Votre message sera transmis directement à James. Aucune liste
      d’envoi, aucun suivi publicitaire.</p>
      <button class="pill" type="submit">Envoyer le message</button>
    </form>
  </div>
</section>
""",
}
