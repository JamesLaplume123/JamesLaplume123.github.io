# English overview — one page; the detailed edition stays in French. Wow version.

import galerie

PAGE = {
    "url": "/en/",
    "assets": ["galerie"],
    "v2": True,
    "lang": "en",
    "title": "JARVIS Private Systems | Private intelligence and connected systems",
    "description": (
        "JARVIS connects private AI, automation, networks and physical environments "
        "while keeping humans in control."
    ),
    "content": """
<section class="band top">
  <div class="bg"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt="" fetchpriority="high"></div>
  <div class="band-inner">
    <p class="eyebrow" data-rev>JARVIS · Private intelligent systems</p>
    <h1 data-rev>Connect what exists.<br><em>Make the whole system act.</em></h1>
    <p class="lead" data-rev>JARVIS connects information, software, devices and physical
    environments through a private architecture built around context, explicit permissions
    and human approval.</p>
    <div class="acts" data-rev>
      <a class="pill" href="/contact/">Book a demo</a>
      <a class="pill ghost" href="/solutions/">Explore the seven solutions</a>
    </div>
    <div class="meta" data-rev>
      <span class="chip">Development and real-world lab</span>
      <span class="chip">Québec, Canada</span>
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
  <div class="acts" data-rev><a class="pill" href="/contact/">Book a demo</a></div>
</section>
""",
}
