/* JARVIS — la présence du site.
   Parle uniquement au portier public (data-guide sur <html>), qui ne donne accès qu'à
   l'intelligence hébergée par JARVIS Private Systems. Aucun témoin : la conversation
   vit dans l'onglet (sessionStorage) et disparaît avec lui.
   L'habillage suit les modes Signature, Platinum et Base de wow.css. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var URL_GUIDE = (doc.getAttribute("data-guide") || "").replace(/\/$/, "");
  if (!URL_GUIDE || document.getElementById("jv-root")) return;

  var EN = (doc.lang || "").slice(0, 2) === "en";
  var soir = new Date().getHours() >= 17;
  var T = EN ? {
    open: "Talk to JARVIS", state: "Online", title: "JARVIS",
    sub: "Private systems · Québec node",
    hello: (soir ? "Good evening." : "Good day.") + " I'm JARVIS. Tell me about your home, your cottage or your business, and what you'd like me to take care of.",
    teaser: (soir ? "Good evening." : "Good day.") + " I'm JARVIS. Anything I can look after for you?",
    ph: "Talk to JARVIS…", send: "Send", think: "Analysing",
    note: "JARVIS is an artificial intelligence and can be wrong. Please don't share sensitive information.",
    err: "I can't reach my node right now. The team is here:", contact: "/en/contact/",
    close: "Close", reset: "New conversation", openPage: "Open the page",
    chips: ["What is the Hub?", "Show me what it looks like", "Security for my business"]
  } : {
    open: "Parler à JARVIS", state: "En ligne", title: "JARVIS",
    sub: "Systèmes privés · nœud Québec",
    hello: (soir ? "Bonsoir." : "Bonjour.") + " Je suis JARVIS. Parlez-moi de votre maison, de votre chalet ou de votre entreprise, et de ce que vous aimeriez me confier.",
    teaser: (soir ? "Bonsoir." : "Bonjour.") + " Je suis JARVIS. Je peux veiller sur quelque chose pour vous?",
    ph: "Parlez à JARVIS…", send: "Envoyer", think: "Analyse",
    note: "JARVIS est une intelligence artificielle : il peut se tromper. Ne partagez pas d'information sensible.",
    err: "Je n'arrive pas à joindre mon nœud en ce moment. L'équipe, elle, est joignable :", contact: "/contact/",
    close: "Fermer", reset: "Nouvelle conversation", openPage: "Ouvrir la page",
    chips: ["C'est quoi le Hub?", "Montre-moi à quoi ça ressemble", "La sécurité pour mon entreprise"]
  };

  var KEY = "jv-conversation", TKEY = "jv-teaser-vu";
  var msgs = [];
  try { msgs = JSON.parse(sessionStorage.getItem(KEY) || "[]") || []; } catch (e) { msgs = []; }
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(msgs.slice(-20))); } catch (e) {} }

  var css = [
    "#jv-root{position:fixed;right:1.1rem;bottom:1.1rem;z-index:86;font-family:var(--sans,system-ui,sans-serif);color:var(--ink,#f5f5f7)}",
    "#jv-root *{box-sizing:border-box}",
    "#jv-root ::selection{background:color-mix(in srgb,var(--mode-glow,#c9a35c) 45%,transparent)}",
    /* lanceur */
    ".jv-fab{position:relative;display:flex;align-items:center;gap:.8rem;border:1px solid var(--mode-line,#d3bc9455);cursor:pointer;padding:.5rem 1.3rem .5rem .5rem;border-radius:999px;background:var(--mode-panel-solid,#0b0b0dfa);color:var(--ink,#f5f5f7);text-align:left;box-shadow:var(--mode-spec,none),0 14px 40px #000b,0 0 30px color-mix(in srgb,var(--mode-glow,#c9a35c) 28%,transparent);transition:transform .4s var(--ease,ease),box-shadow .4s}",
    ".jv-fab:hover{transform:translateY(-3px);box-shadow:var(--mode-spec,none),0 18px 48px #000c,0 0 46px color-mix(in srgb,var(--mode-glow,#c9a35c) 52%,transparent)}",
    ".jv-fab b{display:block;font:600 1.02rem/1.15 var(--sans);background:var(--mode-display,#e7c888);-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".jv-fab small{display:flex;align-items:center;gap:.4rem;margin-top:.18rem;font:500 .62rem/1 var(--mono,monospace);letter-spacing:.18em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jv-live{width:6px;height:6px;border-radius:50%;background:#3ddc84;box-shadow:0 0 8px #3ddc84;animation:jv-beat 2.4s ease-in-out infinite}",
    "@keyframes jv-beat{0%,100%{opacity:1}50%{opacity:.35}}",
    /* orbe */
    ".jv-orb{position:relative;flex:none;width:46px;height:46px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#fff 0 7%,var(--gold-soft,#e9c98c) 8% 17%,transparent 18%),radial-gradient(circle,color-mix(in srgb,var(--mode-glow,#c9a35c) 42%,transparent) 0 52%,transparent 53%),#05050a;border:1.5px solid var(--gold-soft,#e9c98c);box-shadow:0 0 16px color-mix(in srgb,var(--mode-glow,#c9a35c) 65%,transparent),inset 0 0 14px color-mix(in srgb,var(--mode-glow,#c9a35c) 55%,transparent)}",
    ".jv-orb i{position:absolute;border-radius:50%;border:1px solid color-mix(in srgb,var(--gold-soft,#e9c98c) 65%,transparent)}",
    ".jv-orb i:nth-child(1){inset:5px;border-style:dashed;animation:jv-spin 11s linear infinite}",
    ".jv-orb i:nth-child(2){inset:10px;border-top-color:transparent;border-bottom-color:transparent;animation:jv-spin 5s linear infinite reverse}",
    ".jv-orb::before,.jv-orb::after{content:\"\";position:absolute;inset:-7px;border-radius:50%;border:1.5px solid var(--gold-soft,#e9c98c);opacity:0;animation:jv-ping 2.8s var(--ease,ease-out) infinite}",
    ".jv-orb::after{animation-delay:1.4s}",
    "@keyframes jv-spin{to{transform:rotate(1turn)}}",
    "@keyframes jv-ping{0%{transform:scale(.86);opacity:.65}100%{transform:scale(1.6);opacity:0}}",
    /* invitation */
    ".jv-teaser{position:absolute;right:0;bottom:calc(100% + .8rem);width:min(304px,calc(100vw - 2.2rem));padding:.9rem 2.2rem .9rem 1rem;border-radius:14px 14px 3px 14px;background:var(--mode-panel-solid,#0b0b0dfa);border:1px solid var(--mode-line,#d3bc9455);box-shadow:0 18px 50px #000c;font-size:.9rem;line-height:1.5;cursor:pointer;opacity:0;transform:translateY(10px);transition:opacity .6s,transform .6s var(--ease,ease);pointer-events:none}",
    ".jv-teaser.is-on{opacity:1;transform:none;pointer-events:auto}",
    ".jv-teaser button{position:absolute;top:.3rem;right:.3rem;border:0;background:none;color:var(--dim,#a8a8b0);cursor:pointer;font-size:.85rem;padding:.3rem .4rem;border-radius:6px;line-height:1}",
    "#jv-root.is-open .jv-teaser{display:none}",
    /* panneau */
    ".jv-panel{position:absolute;right:0;bottom:0;width:min(408px,calc(100vw - 2rem));height:min(600px,calc(100vh - 5.5rem));display:none;flex-direction:column;border-radius:18px;background:var(--mode-panel-solid,#07070afa);border:1px solid var(--mode-line,#d3bc9455);box-shadow:var(--mode-spec,none),0 30px 80px #000d,0 0 60px color-mix(in srgb,var(--mode-glow,#c9a35c) 16%,transparent);overflow:hidden;backdrop-filter:blur(20px)}",
    "#jv-root.is-open .jv-panel{display:flex;animation:jv-in .45s var(--ease,ease) both}",
    "#jv-root.is-open .jv-fab{display:none}",
    "@keyframes jv-in{from{opacity:0;transform:translateY(14px) scale(.985)}}",
    /* coins et balayage */
    ".jv-panel::before{content:\"\";position:absolute;inset:9px;border-radius:12px;pointer-events:none;background:linear-gradient(var(--gold-soft,#e9c98c) 0 0) 0 0/14px 1px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 0 0/1px 14px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 100% 0/14px 1px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 100% 0/1px 14px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 0 100%/14px 1px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 0 100%/1px 14px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 100% 100%/14px 1px no-repeat,linear-gradient(var(--gold-soft,#e9c98c) 0 0) 100% 100%/1px 14px no-repeat;opacity:.5;z-index:3}",
    ".jv-scan{position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,transparent,var(--gold-soft,#e9c98c),transparent);opacity:.45;z-index:4;animation:jv-scan 7s linear infinite;pointer-events:none}",
    "@keyframes jv-scan{0%{transform:translateY(0)}100%{transform:translateY(600px)}}",
    /* en-tête */
    ".jv-head{position:relative;z-index:5;display:flex;align-items:center;gap:.75rem;padding:1rem 1rem .85rem;border-bottom:1px solid var(--mode-line,#ffffff1a)}",
    ".jv-head .jv-orb{width:34px;height:34px}",
    ".jv-head .jv-orb::before,.jv-head .jv-orb::after{display:none}",
    ".jv-id b{display:block;font:600 1rem/1.1 var(--sans);letter-spacing:.22em;background:var(--mode-display,#e7c888);-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".jv-id small{display:flex;align-items:center;gap:.4rem;margin-top:.22rem;font:500 .58rem/1 var(--mono,monospace);letter-spacing:.16em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jv-sp{flex:1}",
    ".jv-ic{border:1px solid transparent;background:none;color:var(--dim,#a8a8b0);cursor:pointer;font-size:.95rem;padding:.3rem .45rem;border-radius:8px;line-height:1}",
    ".jv-ic:hover{color:var(--ink,#fff);border-color:var(--mode-line,#ffffff26);background:#ffffff0d}",
    /* journal */
    ".jv-log{position:relative;z-index:5;flex:1;overflow-y:auto;overscroll-behavior:contain;padding:1.1rem 1rem;display:flex;flex-direction:column;gap:.85rem;scroll-behavior:smooth}",
    ".jv-log::-webkit-scrollbar{width:4px}.jv-log::-webkit-scrollbar-thumb{background:var(--mode-line,#ffffff26);border-radius:4px}",
    ".jv-m{max-width:90%;font-size:.92rem;line-height:1.58;white-space:pre-wrap;word-wrap:break-word;animation:jv-up .4s var(--ease,ease) both}",
    "@keyframes jv-up{from{opacity:0;transform:translateY(6px)}}",
    ".jv-m a{color:var(--gold-soft,#e9c98c);text-underline-offset:3px}",
    ".jv-a{align-self:flex-start;padding:.1rem 0 .1rem .85rem;border-left:1.5px solid color-mix(in srgb,var(--mode-glow,#c9a35c) 60%,transparent)}",
    ".jv-u{align-self:flex-end;padding:.6rem .9rem;border-radius:13px 13px 3px 13px;background:var(--mode-action,#cfa45b);color:var(--mode-on-action,#1c1408);box-shadow:var(--mode-action-edge,none);font-weight:500}",
    ".jv-cursor::after{content:\"\";display:inline-block;width:7px;height:1em;margin-left:2px;background:var(--gold-soft,#e9c98c);vertical-align:-2px;animation:jv-blink 1s steps(2) infinite}",
    "@keyframes jv-blink{50%{opacity:0}}",
    /* analyse */
    ".jv-think{align-self:flex-start;display:flex;align-items:center;gap:.5rem;font:500 .6rem/1 var(--mono,monospace);letter-spacing:.2em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jv-think em{display:flex;gap:3px}",
    ".jv-think em i{width:3px;height:11px;background:var(--gold-soft,#e9c98c);animation:jv-eq .9s ease-in-out infinite}",
    ".jv-think em i:nth-child(2){animation-delay:.15s}.jv-think em i:nth-child(3){animation-delay:.3s}.jv-think em i:nth-child(4){animation-delay:.45s}",
    "@keyframes jv-eq{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}",
    /* gestes */
    ".jv-act{align-self:flex-start;max-width:90%;display:flex;align-items:center;gap:.6rem;width:100%;padding:.62rem .8rem;border-radius:11px;border:1px solid var(--mode-line,#ffffff26);background:#ffffff0a;color:var(--ink,#f5f5f7);text-decoration:none;font-size:.86rem;cursor:pointer;transition:border-color .3s,background .3s,transform .3s}",
    ".jv-act:hover{border-color:var(--gold-soft,#e9c98c);background:#ffffff14;transform:translateX(2px)}",
    ".jv-act u{flex:none;width:22px;height:22px;border-radius:50%;border:1px solid var(--gold-soft,#e9c98c);display:flex;align-items:center;justify-content:center;font-size:.7rem;text-decoration:none;color:var(--gold-soft,#e9c98c)}",
    ".jv-lab{flex:1;min-width:0}",
    ".jv-act b{display:block;font-weight:500;line-height:1.3}",
    ".jv-lab span{display:block;font:500 .55rem/1.3 var(--mono,monospace);letter-spacing:.18em;text-transform:uppercase;color:var(--dim,#a8a8b0);margin-top:.15rem}",
    ".jv-fig{align-self:flex-start;width:100%;margin:0;border-radius:12px;overflow:hidden;border:1px solid var(--mode-line,#ffffff26);background:#000;animation:jv-up .5s var(--ease,ease) both}",
    ".jv-fig img{display:block;width:100%;height:160px;object-fit:cover;opacity:0;transition:opacity .6s}",
    ".jv-fig img.is-on{opacity:1}",
    ".jv-fig figcaption{padding:.5rem .75rem;font:500 .6rem/1.4 var(--mono,monospace);letter-spacing:.12em;text-transform:uppercase;color:var(--dim,#a8a8b0);border-top:1px solid var(--mode-line,#ffffff1a)}",
    /* suggestions */
    ".jv-chips{display:flex;flex-wrap:wrap;gap:.4rem;align-self:flex-start}",
    ".jv-chip{border:1px solid var(--mode-line,#ffffff26);background:none;color:var(--gold-soft,#e9c98c);border-radius:999px;padding:.42rem .75rem;font:500 .78rem/1 var(--sans);cursor:pointer;transition:background .3s,border-color .3s}",
    ".jv-chip:hover{background:#ffffff12;border-color:var(--gold-soft,#e9c98c)}",
    /* saisie */
    ".jv-form{position:relative;z-index:5;display:flex;gap:.5rem;padding:.75rem;border-top:1px solid var(--mode-line,#ffffff1a)}",
    ".jv-in{flex:1;min-width:0;background:#ffffff0a;border:1px solid var(--mode-line,#ffffff1f);color:var(--ink,#fff);border-radius:11px;padding:.68rem .85rem;font:400 .9rem/1.35 var(--sans);resize:none;max-height:7rem}",
    ".jv-in:focus{outline:none;border-color:var(--gold-soft,#e9c98c);box-shadow:0 0 0 3px color-mix(in srgb,var(--mode-glow,#c9a35c) 14%,transparent)}",
    ".jv-send{border:0;border-radius:11px;padding:0 1rem;cursor:pointer;background:var(--mode-action,#cfa45b);color:var(--mode-on-action,#1c1408);font:600 .85rem/1 var(--sans);box-shadow:var(--mode-action-edge,none)}",
    ".jv-send:disabled{opacity:.45;cursor:default}",
    ".jv-note{position:relative;z-index:5;margin:0;padding:0 .9rem .75rem;font-size:.66rem;line-height:1.45;color:var(--dim,#a8a8b0)}",
    "@media (max-width:560px){#jv-root{right:.7rem;bottom:.7rem}.jv-fab{padding:.42rem 1rem .42rem .42rem;gap:.6rem}.jv-orb{width:40px;height:40px}.jv-fab b{font-size:.92rem}.jv-panel{width:calc(100vw - 1.4rem);height:calc(100vh - 4.8rem)}.jv-teaser{bottom:calc(100% + .6rem)}}",
    "@media (prefers-reduced-motion:reduce){.jv-orb i,.jv-orb::before,.jv-orb::after,.jv-scan,.jv-live,.jv-think em i{animation:none}.jv-m,.jv-fig{animation:none}}"
  ].join("");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  function orbe() { return '<span class="jv-orb" aria-hidden="true"><i></i><i></i></span>'; }
  var root = document.createElement("div");
  root.id = "jv-root";
  root.innerHTML =
    '<div class="jv-teaser" role="status"><span></span><button type="button" class="jv-tx">✕</button></div>' +
    '<button class="jv-fab" type="button" aria-expanded="false">' + orbe() +
      '<span><b></b><small><i class="jv-live"></i><span class="jv-st"></span></small></span></button>' +
    '<section class="jv-panel" role="dialog" aria-modal="false">' +
      '<i class="jv-scan" aria-hidden="true"></i>' +
      '<header class="jv-head">' + orbe() +
        '<span class="jv-id"><b></b><small><i class="jv-live"></i><span class="jv-sub"></span></small></span>' +
        '<span class="jv-sp"></span>' +
        '<button class="jv-ic jv-reset" type="button">↺</button>' +
        '<button class="jv-ic jv-close" type="button">✕</button></header>' +
      '<div class="jv-log" role="log" aria-live="polite"></div>' +
      '<form class="jv-form"><textarea class="jv-in" rows="1" maxlength="1000"></textarea>' +
        '<button class="jv-send" type="submit"></button></form>' +
      '<p class="jv-note"></p>' +
    '</section>';
  document.body.appendChild(root);

  var fab = root.querySelector(".jv-fab"), panel = root.querySelector(".jv-panel");
  var log = root.querySelector(".jv-log"), form = root.querySelector(".jv-form");
  var input = root.querySelector(".jv-in"), send = root.querySelector(".jv-send");
  var teaser = root.querySelector(".jv-teaser");
  fab.querySelector("b").textContent = T.open;
  fab.querySelector(".jv-st").textContent = T.state;
  fab.setAttribute("aria-label", T.open);
  panel.setAttribute("aria-label", T.title);
  root.querySelector(".jv-id b").textContent = T.title;
  root.querySelector(".jv-sub").textContent = T.sub;
  teaser.querySelector("span").textContent = T.teaser;
  teaser.querySelector(".jv-tx").setAttribute("aria-label", T.close);
  var bClose = root.querySelector(".jv-close"), bReset = root.querySelector(".jv-reset");
  bClose.setAttribute("aria-label", T.close); bClose.title = T.close;
  bReset.setAttribute("aria-label", T.reset); bReset.title = T.reset;
  input.placeholder = T.ph; send.textContent = T.send;
  root.querySelector(".jv-note").textContent = T.note;

  /* Texte sûr : on échappe tout, puis on rend cliquables les liens et [texte](lien). */
  function esc(s) { return s.replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function rich(s) {
    var h = esc(s).replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, function (m, t, u) { return '<a href="' + u + '" rel="noopener">' + t + "</a>"; });
    h = h.replace(/(^|[\s(])(https?:\/\/[^\s<)]+[^\s<).,!?;:])/g, function (m, p, u) { return p + '<a href="' + u + '" rel="noopener">' + u + "</a>"; });
    return h;
  }
  function bas() { log.scrollTop = log.scrollHeight; }
  function bulle(role, texte) {
    var d = document.createElement("div");
    d.className = "jv-m " + (role === "user" ? "jv-u" : "jv-a");
    if (role === "user") d.textContent = texte; else d.innerHTML = rich(texte);
    log.appendChild(d); bas();
    return d;
  }
  /* Un geste : ouvrir une page du site, ou montrer une image. */
  function geste(g) {
    if (!g || !g.url || g.url.charAt(0) !== "/") return;
    if (g.type === "image") {
      var f = document.createElement("figure");
      f.className = "jv-fig";
      var im = new Image();
      im.alt = g.nom || ""; im.loading = "lazy"; im.src = g.url;
      im.addEventListener("load", function () { im.classList.add("is-on"); bas(); });
      f.appendChild(im);
      if (g.nom) { var c = document.createElement("figcaption"); c.textContent = g.nom; f.appendChild(c); }
      log.appendChild(f);
    } else {
      var a = document.createElement("a");
      a.className = "jv-act"; a.href = g.url;
      a.innerHTML = '<u aria-hidden="true">→</u><span class="jv-lab"><b></b><span></span></span>';
      a.querySelector("b").textContent = g.nom || g.url;
      a.querySelector(".jv-lab span").textContent = T.openPage;
      log.appendChild(a);
    }
    bas();
  }
  function chips() {
    var w = document.createElement("div"); w.className = "jv-chips";
    T.chips.forEach(function (c) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "jv-chip"; b.textContent = c;
      b.addEventListener("click", function () { w.remove(); demande(c); });
      w.appendChild(b);
    });
    log.appendChild(w); bas();
  }
  function rendre() {
    log.innerHTML = "";
    bulle("assistant", T.hello);
    msgs.forEach(function (m) {
      bulle(m.role, m.content);
      if (m.role === "assistant" && m.gestes) m.gestes.forEach(geste);
    });
    if (!msgs.length) chips();
  }

  var occupe = false;
  function demande(q) {
    q = (q || "").trim().slice(0, 1000);
    if (!q || occupe) return;
    occupe = true; send.disabled = true;
    msgs.push({ role: "user", content: q }); save();
    var c = log.querySelector(".jv-chips"); if (c) c.remove();
    bulle("user", q);

    var attente = document.createElement("div");
    attente.className = "jv-think";
    attente.innerHTML = '<em><i></i><i></i><i></i><i></i></em><span></span>';
    attente.querySelector("span").textContent = T.think;
    log.appendChild(attente); bas();

    var txt = "", live = null, gestes = [];
    function ajoute(bout) {
      txt += bout;
      if (!live) { attente.remove(); live = bulle("assistant", ""); live.classList.add("jv-cursor"); }
      live.innerHTML = rich(txt); bas();
    }
    var ctl = window.AbortController ? new AbortController() : null;
    var minuteur = setTimeout(function () { if (ctl) ctl.abort(); }, 130000);

    fetch(URL_GUIDE + "/chat", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: msgs.slice(-10).map(function (m) { return { role: m.role, content: m.content }; }), stream: true, lang: EN ? "en" : "fr" }),
      signal: ctl ? ctl.signal : undefined
    }).then(function (r) {
      var type = r.headers.get("Content-Type") || "";
      if (type.indexOf("text/event-stream") === -1 || !r.body || !r.body.getReader) {
        return r.json().catch(function () { return {}; }).then(function (d) {
          if (d && d.reply) ajoute(d.reply);
          if (d && d.gestes) gestes = d.gestes;
        });
      }
      var lecteur = r.body.getReader(), dec = new TextDecoder(), tampon = "";
      function lis() {
        return lecteur.read().then(function (res) {
          if (res.done) return;
          tampon += dec.decode(res.value, { stream: true });
          var blocs = tampon.split("\n\n"); tampon = blocs.pop();
          blocs.forEach(function (b) {
            if (b.indexOf("data: ") !== 0) return;
            try {
              var j = JSON.parse(b.slice(6));
              if (j.d) ajoute(j.d);
              if (j.g) gestes.push(j.g);
            } catch (e) {}
          });
          return lis();
        });
      }
      return lis();
    }).then(function () {
      if (!txt.trim()) throw new Error("vide");
      if (live) { live.classList.remove("jv-cursor"); live.innerHTML = rich(txt.trim()); }
      gestes.forEach(geste);
      msgs.push({ role: "assistant", content: txt.trim(), gestes: gestes }); save();
    }).catch(function () {
      if (txt.trim()) {
        if (live) live.classList.remove("jv-cursor");
        msgs.push({ role: "assistant", content: txt.trim(), gestes: gestes }); save();
        return;
      }
      attente.remove();
      bulle("assistant", T.err + " " + location.origin + T.contact);
      msgs.pop(); save();
    }).then(function () {
      clearTimeout(minuteur); occupe = false; send.disabled = false;
      if (panel.offsetParent !== null) input.focus();
    });
  }

  function cacheTeaser() { teaser.classList.remove("is-on"); try { sessionStorage.setItem(TKEY, "1"); } catch (e) {} }
  function ouvrir(on) {
    cacheTeaser();
    root.classList.toggle("is-open", on);
    fab.setAttribute("aria-expanded", on ? "true" : "false");
    if (on) { if (!log.children.length) rendre(); setTimeout(function () { input.focus(); bas(); }, 60); }
    else fab.focus();
  }
  var vu = false; try { vu = !!sessionStorage.getItem(TKEY); } catch (e) {}
  if (!vu && !msgs.length) setTimeout(function () {
    if (!root.classList.contains("is-open")) teaser.classList.add("is-on");
  }, 5000);

  teaser.addEventListener("click", function (e) { if (e.target.closest(".jv-tx")) { cacheTeaser(); return; } ouvrir(true); });
  fab.addEventListener("click", function () { ouvrir(true); });
  bClose.addEventListener("click", function () { ouvrir(false); });
  bReset.addEventListener("click", function () { msgs = []; save(); rendre(); input.focus(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; demande(q); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit")); }
  });
  input.addEventListener("input", function () { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 112) + "px"; });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.classList.contains("is-open")) ouvrir(false); });
  /* Tout élément [data-jarvis] de la page ouvre la conversation. */
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-jarvis]");
    if (t) { e.preventDefault(); ouvrir(true); var q = t.getAttribute("data-jarvis"); if (q) setTimeout(function () { demande(q); }, 300); }
  });
  window.JARVIS = { ouvrir: function (q) { ouvrir(true); if (q) demande(q); } };
})();
