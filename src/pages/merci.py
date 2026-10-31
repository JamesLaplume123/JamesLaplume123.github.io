# Page de remerciement après l'envoi du formulaire de contact.
# FormSubmit redirige ici grâce au champ caché _next du formulaire.

PAGE = {
    "url": "/merci/",
    "v2": True,
    "noindex": True,
    "title": "Message reçu | JARVIS Private Systems",
    "description": "Votre message a bien été transmis à James Laplume.",
    "content": """
<section class="notfound">
  <div>
    <p class="eyebrow">Message reçu</p>
    <h1 style="font-size:clamp(2.4rem,6vw,4.2rem);margin-top:1.2rem">Merci.<br><em>C’est entre
    bonnes mains.</em></h1>
    <p>Votre message a été transmis. Je vous réponds personnellement.</p>
    <div class="acts" style="justify-content:center">
      <a class="pill" href="/">Retour à l’accueil</a>
      <a class="pill ghost" href="/solutions/">Explorer les solutions</a>
    </div>
  </div>
</section>
""",
}
