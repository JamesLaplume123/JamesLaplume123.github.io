# English overview — one page; the detailed edition stays in French.
# « Essentiel » (November 2026): one sentence, the seven solutions, one button. No location.

SOLUTIONS = [
    ("Smart environments", "Lights, heating, locks and energy on one screen."),
    ("Private AI and knowledge", "Ask your own documents; the source is always shown."),
    ("Intelligent security", "Cameras and alarms turned into clear events."),
    ("Business automation", "Reception, requests and approvals that move on their own."),
    ("Network and cybersecurity", "A map of your network and its risks, in plain words."),
    ("Diagnostics & continuity", "From a symptom to the cause, with a file ready to hand over."),
    ("Mobility", "A road copilot for the RV, the car or the bike."),
]

CARTES = "".join(
    f'<article class="card" data-rev><small>{i + 1:02d}</small><h3>{t}</h3><p>{p}</p></article>'
    for i, (t, p) in enumerate(SOLUTIONS)
)

PAGE = {
    "url": "/en/",
    "v2": True,
    "lang": "en",
    "title": "JARVIS Private Systems | Security technology and private AI",
    "description": (
        "We design and install JARVIS, a private system that runs and protects homes, farms, "
        "businesses and vehicles. Home automation, networking and private AI, on site."
    ),
    "content": f"""
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Security technology and private AI</p>
    <h1 data-rev>Smart, secure places.<br><em>One system, on site.</em></h1>
    <p class="lead" data-rev>We design and install JARVIS, a private system that runs and protects
    homes, farms, businesses and vehicles.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Let’s talk about your project</a>
      <a class="pill ghost" href="/logiciel/" hreflang="fr">Try the software (French)</a>
    </div>
  </div>
</section>

<section class="sect" aria-labelledby="en-sept">
  <div class="sect-head">
    <div data-rev>
      <h2 id="en-sept">Seven solutions. <em>One system.</em></h2>
    </div>
  </div>
  <div class="cards">{CARTES}</div>
  <p class="pro-suite" data-rev><a href="/solutions/" hreflang="fr">The detailed edition, in French <i aria-hidden="true">→</i></a></p>
</section>

<section class="cta">
  <h2 data-rev>See JARVIS<br><span>with your own eyes.</span></h2>
  <div class="acts" data-rev><a class="pill" href="/contact/">Let’s talk about your project</a></div>
</section>
""",
}
