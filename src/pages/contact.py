# Contact — transformer l'intérêt en conversation utile.
# Le formulaire passe par FormSubmit vers laplumejames@gmail.com (comme avant).

PAGE = {
    "url": "/contact/",
    "title": "Contact | Discuter d’un projet JARVIS",
    "description": (
        "Présentez votre projet, votre problème ou une possibilité de collaboration "
        "à James Laplume."
    ),
    "og_image": "/media/solutions/ia-privee-connaissances.webp",
    "content": """
<section class="hero page-hero">
  <div class="hero-media">
    <img src="/media/solutions/ia-privee-connaissances.webp" alt="" fetchpriority="high">
  </div>
  <div class="shell hero-inner">
    <div>
      <p class="eyebrow">Contact</p>
      <h1>Parlons du problème <em>avant de parler de la solution.</em></h1>
      <p class="lead">Client potentiel, partenaire technique, chercheur ou investisseur :
      décrivez simplement ce que vous cherchez à comprendre, relier ou automatiser.</p>
      <div class="hero-meta">
        <div><span>Réponse</span><b>À laplumejames@gmail.com</b></div>
        <div><span>Lieu</span><b>Québec, Canada</b></div>
        <div><span>Échanges</span><b>Exploratoires et confidentiels</b></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div data-reveal>
      <p class="eyebrow">Premier échange</p>
      <h2>Une idée claire peut commencer par <em>quelques lignes.</em></h2>
      <p>Je vous répondrai sur ce qui semble réalisable, ce qui mérite une première preuve et
      les informations nécessaires pour aller plus loin.</p>
      <p>Vous préférez écrire directement?<br>
      <a class="link-arrow" href="mailto:laplumejames@gmail.com">laplumejames@gmail.com <span>↗</span></a></p>
    </div>
    <form class="form-card" data-reveal action="https://formsubmit.co/laplumejames@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="Nouveau message — jameslaplume.ca">
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
      <button class="button button-fill" type="submit" style="margin-top:0.8rem;">
        Envoyer le message <span>↗</span>
      </button>
    </form>
  </div>
</section>
""",
}
