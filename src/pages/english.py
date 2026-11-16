# English overview — one page; the detailed edition stays in French. Wow version.

import galerie

PAGE = {
    "url": "/en/",
    "assets": ["galerie"],
    "v2": True,
    "lang": "en",
    "title": "JARVIS Private Systems | Technology and security, Québec",
    "description": (
        "We design and install JARVIS, a private system that runs and protects homes, farms, "
        "businesses and vehicles in Montérégie, Québec. Your data stays on site."
    ),
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>Security technology and private AI · Montérégie, Québec</p>
    <h1 data-rev>Smart, secure places.<br><em>One system, on site.</em></h1>
    <p class="lead" data-rev>JARVIS Private Systems is a technology and security company. We design
    and install JARVIS, a private system that runs and protects homes, farms, businesses and
    vehicles in Montérégie, Québec. It brings together home automation, networking and
    cybersecurity, connected cameras and locks, and a private AI. Your data stays with you, and
    you keep the final say. We are in our launch phase: we are taking the names of interested people and
    choosing a few first projects.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Let’s talk about your project</a>
      <a class="pill ghost" href="/en/contact/" data-jarvis>Talk to JARVIS</a>
      <a class="pill ghost" href="/solutions/">Explore the seven solutions</a>
      <a class="pill ghost" href="/logiciel/" hreflang="fr">Try the software (French)</a>
      <a class="pill ghost" href="/offre/" hreflang="fr">The offer (French)</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip">Launch phase</span>
      <span class="chip">Based near Saint-Hyacinthe, Québec</span>
      <span class="chip">Detailed site in French</span>
    </div>
  </div>
</section>

""" + galerie.clients_en() + """

<section class="sect alt">
  <div class="sect-head">
    <div data-rev>
      <p class="eyebrow">Seven extensions · one system</p>
      <h2 style="margin-top:1rem">Add only <em>what you need.</em></h2>
    </div>
    <p data-rev>Each extension does one precise job in the same app. The detailed multi-page
    edition is maintained in French.</p>
  </div>
  <div class="cards">
    <article class="card" data-rev>
      <small>01</small>
      <h3>Smart environments</h3>
      <p>Connect comfort, energy, access and devices without making the environment harder
      to use.</p>
    </article>
    <article class="card" data-rev>
      <small>02</small>
      <h3>Private AI and knowledge</h3>
      <p>Work with authorized documents and data while keeping provenance and permissions
      visible.</p>
    </article>
    <article class="card" data-rev>
      <small>03</small>
      <h3>Intelligent security</h3>
      <p>Turn cameras, access and alarms into understandable events and organized
      evidence.</p>
    </article>
    <article class="card" data-rev>
      <small>04</small>
      <h3>Operations automation</h3>
      <p>Move requests, documents and approvals between the tools a business already
      uses.</p>
    </article>
    <article class="card" data-rev>
      <small>05</small>
      <h3>Network resilience</h3>
      <p>Understand infrastructure, dependencies, private access and service
      degradation.</p>
    </article>
    <article class="card" data-rev>
      <small>06</small>
      <h3>Diagnostics &amp; continuity</h3>
      <p>Move from a symptom to evidence, verification steps and a documented recovery.</p>
    </article>
    <article class="card" data-rev>
      <small>07</small>
      <h3>Mobility</h3>
      <p>A road copilot for RVs and vehicles: the right stop at the right time, energy and
      weather included.</p>
    </article>
  </div>
  <div class="chiprow" data-rev>
    <a class="pill ghost" href="/solutions/">View the detailed French edition</a>
  </div>
</section>

<section class="cta">
  <h2 data-rev>See JARVIS<br><span>with your own eyes.</span></h2>
  <p data-rev>Share the environment, process or research question. I will clearly separate
  what can be demonstrated now, what needs a pilot and what remains part of the long-term
  vision.</p>
  <div class="acts" data-rev><a class="pill" href="/contact/">Let’s talk about your project</a></div>
</section>
""",
}
