/* JARVIS — la présence du site.
   Parle uniquement au portier public (data-guide sur <html>), qui ne donne accès qu'à
   l'intelligence hébergée par JARVIS Private Systems. Aucun témoin : la conversation
   vit dans l'onglet (sessionStorage) et disparaît avec lui.
   L'habillage suit les modes Signature, Platinum et Base de wow.css. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var URL_GUIDE = (doc.getAttribute("data-guide") || "").replace(/\/$/, "");
  var PONT = "https://jameslaplume.ca/pont-guide.html", PONT_ORIGINE = "https://jameslaplume.ca", pontP = null;
  function pontPret() {
    if (pontP) return pontP;
    pontP = new Promise(function (resolve, reject) {
      var f = document.createElement("iframe");
      f.src = PONT; f.setAttribute("aria-hidden", "true"); f.tabIndex = -1;
      f.style.cssText = "position:absolute;width:0;height:0;border:0;opacity:0;pointer-events:none";
      var ok = false;
      function h(e) { if (e.origin === PONT_ORIGINE && e.data && e.data.jv === "pont-pret") { ok = true; window.removeEventListener("message", h); resolve(f); } }
      window.addEventListener("message", h);
      f.onerror = function () { reject(new Error("pont")); };
      document.body.appendChild(f);
      setTimeout(function () { if (!ok) { pontP = null; reject(new Error("pont : pas de réponse")); } }, 15000);
    });
    return pontP;
  }
  if (!URL_GUIDE || document.getElementById("jv-root")) return;

  var EN = (doc.lang || "").slice(0, 2) === "en";
  var soir = new Date().getHours() >= 17;
  var T = EN ? {
    open: "Talk to JARVIS", state: "Online", title: "JARVIS",
    sub: "Private intelligence",
    hello: (soir ? "Good evening." : "Good day.") + " I'm JARVIS. Tell me about your home, your cottage or your business, and what you'd like me to take care of.",
    teaser: (soir ? "Good evening." : "Good day.") + " I'm JARVIS. Anything I can look after for you?",
    ph: "Talk to JARVIS…", send: "Send", think: "Analysing",
    note: "JARVIS is an artificial intelligence and can be wrong. Please don't share sensitive information.",
    err: "I can't reach my node right now. The team is here:", contact: "/en/contact/",
    close: "Close", reset: "New conversation", openPage: "Open the page",
    chips: ["What is the Hub?", "How much does it cost?", "What do I need for my RV?", "Security for my business"]
  } : {
    open: "Parler à JARVIS", state: "En ligne", title: "JARVIS",
    sub: "Intelligence privée",
    hello: (soir ? "Bonsoir." : "Bonjour.") + " Je suis JARVIS. Parlez-moi de votre maison, de votre chalet ou de votre entreprise, et de ce que vous aimeriez me confier.",
    teaser: (soir ? "Bonsoir." : "Bonjour.") + " Je suis JARVIS. Je peux veiller sur quelque chose pour vous?",
    ph: "Parlez à JARVIS…", send: "Envoyer", think: "Analyse",
    note: "JARVIS est une intelligence artificielle : il peut se tromper. Ne partagez pas d'information sensible.",
    err: "Je n'arrive pas à joindre mon nœud en ce moment. L'équipe, elle, est joignable :", contact: "/contact/",
    close: "Fermer", reset: "Nouvelle conversation", openPage: "Ouvrir la page",
    chips: ["C'est quoi le Hub?", "Combien ça coûte?", "Qu'est-ce qu'il me faut pour mon VR?", "Une réceptionniste pour mon entreprise"]
  };

  var KEY = "jv-conversation", TKEY = "jv-teaser-vu";
  var msgs = [];
  try { msgs = JSON.parse(sessionStorage.getItem(KEY) || "[]") || []; } catch (e) { msgs = []; }
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(msgs.slice(-20))); } catch (e) {} }

  var css = [
    "#jv-root{position:fixed;right:1.1rem;bottom:1.1rem;z-index:86;font-family:var(--sans,system-ui,sans-serif);color:var(--ink,#f5f5f7)}",
    "#jv-root *{box-sizing:border-box}",
    "#jv-root ::selection{background:color-mix(in srgb,var(--mode-glow,#c9a35c) 45%,transparent)}",
    /* lanceur : une orbe de particules en trois dimensions (WebGL) et son étiquette holographique */
    ".jv-fab{position:relative;display:flex;flex-direction:row-reverse;align-items:center;border:0;padding:0;background:none;color:var(--ink,#f5f5f7);cursor:pointer;text-align:left;-webkit-tap-highlight-color:transparent}",
    ".jv-fab:focus-visible{outline:none}",
    ".jv-fab:focus-visible .jv-orb{outline:2px solid var(--gold-soft,#e9c98c);outline-offset:2px}",
    ".jv-orb{position:relative;flex:none;display:block;width:96px;height:96px;border-radius:50%;transition:transform .5s var(--ease,cubic-bezier(.2,.8,.2,1))}",
    ".jv-orb::before{content:\"\";position:absolute;left:14%;right:14%;bottom:-2%;height:16%;border-radius:50%;background:radial-gradient(ellipse,#000c,transparent 70%);filter:blur(4px)}",
    ".jv-orb::after{content:\"\";position:absolute;inset:20%;border-radius:50%;background:radial-gradient(circle,#fff 0 5%,color-mix(in srgb,var(--mode-glow,#c9a35c) 92%,#fff) 11%,color-mix(in srgb,var(--mode-glow,#c9a35c) 55%,transparent) 30%,color-mix(in srgb,var(--mode-glow,#c9a35c) 14%,transparent) 58%,transparent 74%);filter:blur(2.5px);animation:jv-souffle 4.4s ease-in-out infinite}",
    ".jv-gl{position:absolute;inset:0;width:100%;height:100%;z-index:1}",
    ".jv-hud{position:absolute;inset:0;width:100%;height:100%;z-index:2;overflow:visible;pointer-events:none}",
    ".jv-hud circle{fill:none;stroke:var(--gold-soft,#e9c98c);transform-origin:50px 50px}",
    ".jv-hud .a{stroke-width:.7;stroke-dasharray:.7 4.3;opacity:.6;animation:jv-spin 40s linear infinite}",
    ".jv-hud .b{stroke-width:1.2;stroke-dasharray:46 240;stroke-linecap:round;animation:jv-spin 6.5s linear infinite reverse}",
    ".jv-hud .c{stroke-width:.5;stroke-dasharray:20 9 3 58;opacity:.55;animation:jv-spin 16s linear infinite}",
    ".jv-orb.no-gl::after{inset:30%;filter:none;background:radial-gradient(circle,#fff 0 18%,var(--gold-soft,#e9c98c) 22% 46%,transparent 72%)}",
    ".jv-fab:hover .jv-orb{transform:scale(1.08)}",
    ".jv-fab.is-go .jv-orb{transform:scale(1.3);transition-duration:.22s}",
    "@keyframes jv-souffle{0%,100%{opacity:.75;transform:scale(.92)}50%{opacity:1;transform:scale(1.1)}}",
    ".jv-lab-w{margin-right:-20px;filter:drop-shadow(0 0 .6px var(--gold-soft,#e9c98c)) drop-shadow(0 0 .6px var(--gold-soft,#e9c98c)) drop-shadow(0 12px 26px #000d)}",
    ".jv-lab{position:relative;display:flex;flex-direction:column;justify-content:center;gap:.28rem;height:56px;max-width:0;padding:0;opacity:0;overflow:hidden;white-space:nowrap;background:linear-gradient(90deg,#07070cf7,#0a0a10e6);clip-path:polygon(13px 0,100% 0,100% 100%,0 100%,0 13px);transition:max-width .75s var(--ease,cubic-bezier(.2,.8,.2,1)),padding .75s var(--ease,cubic-bezier(.2,.8,.2,1)),opacity .3s}",
    ".jv-fab:hover .jv-lab,.jv-fab:focus-visible .jv-lab,.jv-fab.is-dit .jv-lab{max-width:270px;padding:0 38px 0 20px;opacity:1}",
    ".jv-lab::after{content:\"\";position:absolute;top:0;bottom:0;left:-60px;width:60px;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--mode-glow,#c9a35c) 30%,transparent),transparent);animation:jv-balaye 3.2s ease-in-out infinite}",
    "@keyframes jv-balaye{0%,35%{transform:translateX(0)}100%{transform:translateX(420px)}}",
    ".jv-lab b{display:block;font:650 .98rem/1 var(--sans,system-ui);letter-spacing:.06em;text-transform:uppercase;background:var(--mode-display,#e7c888);-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".jv-lab b.is-code{font:500 .82rem/1.2 var(--mono,monospace);letter-spacing:.04em;text-transform:none}",
    ".jv-lab small{display:flex;align-items:center;gap:.45rem;font:500 .6rem/1 var(--mono,monospace);letter-spacing:.2em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jv-eq{flex:none;display:inline-flex;align-items:flex-end;gap:2px;height:9px;margin-left:.3rem}",
    "#jv-root .jv-eq{display:inline-flex}#jv-root .jv-eq i{display:block;flex:none;width:2px;height:100%;background:var(--gold-soft,#e9c98c);transform-origin:50% 100%;animation:jv-eq 1.1s ease-in-out infinite}",
    ".jv-eq i:nth-child(2){animation-delay:.18s}.jv-eq i:nth-child(3){animation-delay:.36s}.jv-eq i:nth-child(4){animation-delay:.54s}",
    ".jv-head .jv-orb{width:50px;height:50px;margin:-6px -4px -6px -8px}",
    ".jv-head .jv-hud .a{display:none}",
    ".jv-live{width:6px;height:6px;border-radius:50%;background:#3ddc84;box-shadow:0 0 8px #3ddc84;animation:jv-beat 2.4s ease-in-out infinite}",
    "@keyframes jv-beat{0%,100%{opacity:1}50%{opacity:.35}}",
    /* orbe */
    "@keyframes jv-spin{to{transform:rotate(1turn)}}",
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
    "@media (max-width:560px){#jv-root{right:.5rem;bottom:.5rem}.jv-orb{width:76px;height:76px}.jv-lab{height:48px}.jv-lab b{font-size:.86rem}.jv-fab:hover .jv-lab{max-width:0;padding:0;opacity:0}.jv-fab.is-dit .jv-lab{max-width:230px;padding:0 32px 0 16px;opacity:1}.jv-panel{width:calc(100vw - 1.4rem);height:calc(100vh - 4.8rem)}.jv-teaser{bottom:calc(100% + .4rem)}}",
    "@media (prefers-reduced-motion:reduce){.jv-orb::after,.jv-hud circle,.jv-lab::after,.jv-eq i,.jv-scan,.jv-live,.jv-think em i{animation:none}.jv-m,.jv-fig{animation:none}.jv-lab{transition:none}}"
  ].join("");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  function orbe() {
    return '<span class="jv-orb" aria-hidden="true"><canvas class="jv-gl"></canvas>' +
      '<svg class="jv-hud" viewBox="0 0 100 100"><circle class="a" cx="50" cy="50" r="47.5"/><circle class="b" cx="50" cy="50" r="44"/><circle class="c" cx="50" cy="50" r="40.5"/></svg></span>';
  }
  var root = document.createElement("div");
  root.id = "jv-root";
  root.innerHTML =
    '<div class="jv-teaser" role="status"><span></span><button type="button" class="jv-tx">✕</button></div>' +
    '<button class="jv-fab" type="button" aria-expanded="false">' + orbe() +
      '<span class="jv-lab-w"><span class="jv-lab"><b></b><small><i class="jv-live"></i><span class="jv-st"></span><span class="jv-eq" aria-hidden="true"><i></i><i></i><i></i><i></i></span></small></span></span></button>' +
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


  /* ------------------------------------------------------------------ L'orbe vivante
     Une sphère de verre avec une hélice d'ADN à l'intérieur, rendue en WebGL : le reflet suit le
     pointeur, l'hélice accélère quand on approche et quand JARVIS réfléchit, et ondule quand il répond. Couleurs : celles du mode (Base, Signature, Platinum).
     Sans WebGL : un noyau fixe. Mouvement réduit : une seule image. En pause hors écran. */
  var ORBES = [], etatOrbe = "repos", souris = { x: -9999, y: -9999 }, calme = false;
  try { calme = matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  function teinte() {
    var t = document.createElement("span"); t.style.cssText = "position:absolute;visibility:hidden;color:var(--mode-glow,#c9a35c)";
    root.appendChild(t); var c = getComputedStyle(t).color, m = c.match(/[\d.]+/g); t.remove();
    if (!m || m.length < 3) return [0.79, 0.64, 0.36];
    var k = c.indexOf("color(") === 0 ? 1 : 255;
    return [m[0] / k, m[1] / k, m[2] / k];
  }
  /* Une sphère de verre, calculée pixel par pixel (un seul fragment shader, sans bibliothèque) :
     verre fumé luisant, point de lumière net qui suit le pointeur, reflet de fenêtre, bord irisé, et,
     vue à travers la lentille, une double hélice d'ADN lumineuse qui tourne. */
  var VS = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  var FS = [
    "precision highp float;uniform vec2 res;uniform float t,e,w;uniform vec2 tilt;uniform vec3 ca;",
    "vec3 iri(float x){return .5+.5*cos(6.2832*(x+vec3(0.,.33,.67)));}",
    "void main(){vec2 p=(gl_FragCoord.xy-.5*res)/(.5*res.y);float R=.8,d=length(p);vec3 col=vec3(0.);float al=0.;",
    " float halo=exp(-max(d-R,0.)*10.)*(.16+.3*e);",
    " if(d<R){vec3 n=vec3(p/R,sqrt(max(0.,1.-dot(p,p)/(R*R))));",
    "  vec2 q=p/R*(.6+.4*n.z)-tilt*.14*(1.-n.z);",
    "  vec2 h=vec2(q.x*.914-q.y*.407,q.x*.407+q.y*.914);",
    "  float ph=h.y*5.4+t*(1.+1.7*e),amp=.3*(1.+.2*w*sin(h.y*9.-t*6.)),env=smoothstep(1.,.5,abs(h.y));",
    "  float x1=amp*sin(ph),z=cos(ph)*.5+.5;",
    "  float s1=exp(-(h.x-x1)*(h.x-x1)/(.0014+.0026*z))*(.4+.6*z);",
    "  float s2=exp(-(h.x+x1)*(h.x+x1)/(.0014+.0026*(1.-z)))*(.4+.6*(1.-z));",
    "  float fr=abs(fract(h.y*8.)-.5);",
    "  float rung=smoothstep(.13,.02,fr)*step(abs(h.x),abs(x1))*.4;",
    "  float dna=((s1+s2)*(.55+.45*smoothstep(.3,0.,fr))+rung)*env;",
    "  vec3 hot=mix(ca,vec3(1.),.78);",
    "  vec3 inner=ca*dna*1.25+hot*dna*dna*dna*.9+ca*(.1+.3*e)*exp(-dot(q,q)*3.2);",
    "  col=mix(vec3(.012,.014,.02),ca*.1,.5)*(.55+.45*n.z)+inner;",
    "  vec3 V=vec3(0.,0.,1.),L=normalize(vec3(-.55+tilt.x*.9,.62-tilt.y*.9,.75));",
    "  float sp=pow(max(dot(n,normalize(L+V)),0.),110.);",
    "  float sp2=pow(max(dot(n,normalize(vec3(.5,-.62,.6)+V)),0.),20.)*.2;",
    "  vec3 r=reflect(-V,n);float rx=r.x+tilt.x*.35;",
    "  float win=smoothstep(.5,.7,r.y)*smoothstep(.97,.82,r.y)*smoothstep(-.75,-.2,rx)*smoothstep(.7,.15,rx);",
    "  float fres=pow(1.-n.z,3.);",
    "  col+=vec3(1.)*sp*1.4+hot*sp2+vec3(1.)*win*(.2+.25*fres);",
    "  col+=mix(ca,iri(n.z*.9+t*.04+atan(p.y,p.x)*.09),.5)*fres*.95;",
    "  col+=hot*pow(max(dot(n,normalize(vec3(.35,-.78,.5))),0.),7.)*.2*(1.+e);",
    "  al=smoothstep(R,R-.025,d);}",
    " gl_FragColor=vec4(col*al+ca*halo*(1.-al),al+(1.-al)*halo*.75);}"
  ].join("\n");
  function Orbe(el) {
    var cv = el.querySelector("canvas"), gl = null;
    try { gl = cv.getContext("webgl", { alpha: true, premultipliedAlpha: true, antialias: false, powerPreference: "low-power" }); } catch (e) { gl = null; }
    if (!gl) { el.classList.add("no-gl"); return; }
    function sh(type, src) { var o = gl.createShader(type); gl.shaderSource(o, src); gl.compileShader(o); return o; }
    var pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { el.classList.add("no-gl"); return; }
    gl.useProgram(pr);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var ap = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(ap); gl.vertexAttribPointer(ap, 2, gl.FLOAT, false, 0, 0);
    gl.disable(gl.DEPTH_TEST); gl.disable(gl.BLEND); gl.clearColor(0, 0, 0, 0);
    var U = {}; ["t", "e", "w", "tilt", "ca", "res"].forEach(function (u) { U[u] = gl.getUniformLocation(pr, u); });
    var me = { el: el, e: 0.1, w: 0, tx: 0, ty: 0, t: Math.random() * 40, taille: 0, coup: 0 };
    me.couleur = function () { var c = teinte(); gl.uniform3f(U.ca, c[0], c[1], c[2]); };
    me.dessine = function (dt) {
      if (el.offsetParent === null) return;
      var css = el.clientWidth, dpr = Math.min(window.devicePixelRatio || 1, 2), px = Math.round(css * dpr);
      if (px !== me.taille) { me.taille = px; cv.width = cv.height = px; gl.viewport(0, 0, px, px); gl.uniform2f(U.res, px, px); }
      var b = el.getBoundingClientRect(), dx = souris.x - (b.left + b.width / 2), dy = souris.y - (b.top + b.height / 2), dist = Math.sqrt(dx * dx + dy * dy);
      var pres = Math.max(0, 1 - dist / 320), cible = etatOrbe === "pense" ? 1 : etatOrbe === "parle" ? 0.55 : 0.08 + 0.55 * pres * pres + (el.parentNode.matches && el.parentNode.matches(":hover") ? 0.3 : 0);
      if (me.coup > 0) { cible = 1.6; me.coup -= dt; }
      me.e += (cible - me.e) * Math.min(1, dt * 4); me.w += ((etatOrbe === "parle" ? 1 : 0) - me.w) * Math.min(1, dt * 3);
      me.tx += (Math.max(-1, Math.min(1, dx / 420)) - me.tx) * Math.min(1, dt * 3); me.ty += (Math.max(-1, Math.min(1, dy / 420)) - me.ty) * Math.min(1, dt * 3);
      me.t += dt * (0.8 + 1.2 * me.e);
      gl.uniform1f(U.t, me.t); gl.uniform1f(U.e, me.e); gl.uniform1f(U.w, me.w); gl.uniform2f(U.tilt, me.tx, me.ty);
      gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    };
    me.couleur(); ORBES.push(me);
  }
  Orbe(root.querySelector(".jv-fab .jv-orb"));
  Orbe(root.querySelector(".jv-head .jv-orb"));
  function orbeEtat(x) { etatOrbe = x; }
  if (ORBES.length) {
    var avant = 0;
    (function boucle(now) {
      var dt = Math.min(0.05, (now - avant) / 1000 || 0.016); avant = now;
      if (!document.hidden) ORBES.forEach(function (o) { o.dessine(calme ? 0 : dt); });
      if (!calme) requestAnimationFrame(boucle);
    })(0);
    window.addEventListener("pointermove", function (e) { souris.x = e.clientX; souris.y = e.clientY; }, { passive: true });
    if (window.MutationObserver) new MutationObserver(function () { ORBES.forEach(function (o) { o.couleur(); }); if (calme) ORBES.forEach(function (o) { o.dessine(0); }); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ["data-mode"] });
  }
  /* L'étiquette se déchiffre lettre par lettre quand elle se déplie. */
  var etiq = fab.querySelector(".jv-lab b"), dechT = 0;
  function dechiffre(tout) {
    clearInterval(dechT); etiq.classList.remove("is-code");
    if (calme) { etiq.textContent = T.open; return; }
    var txt = T.open, code = EN ? "jarvis.listen()" : "jarvis.ecoute()", hexa = "4A 41 52 56 49 53", i = 0, phase = tout ? 0 : 2, pause = 0;
    etiq.classList.add("is-code");
    dechT = setInterval(function () {
      if (pause > 0) { pause--; return; }
      i++;
      if (phase === 0) {            /* une vraie ligne de code s'écrit */
        etiq.textContent = "> " + code.slice(0, i) + (i < code.length ? "_" : "");
        if (i >= code.length) { phase = 1; i = 0; pause = 9; }
      } else if (phase === 1) {     /* le mot JARVIS en code machine (hexadécimal) */
        etiq.textContent = hexa.slice(0, i * 2);
        if (i * 2 >= hexa.length) { phase = 2; i = 0; pause = 9; }
      } else {                      /* il se déchiffre en clair */
        if (i === 1) etiq.classList.remove("is-code");
        var g = "01<>/\\#+=-", o = "";
        for (var k = 0; k < txt.length; k++) o += k < i || txt[k] === " " ? txt[k] : g[(Math.random() * g.length) | 0];
        etiq.textContent = o; if (i >= txt.length) clearInterval(dechT);
      }
    }, 34);
  }
  fab.addEventListener("pointerenter", function (e) { if (e.pointerType !== "touch") dechiffre(false); });
  fab.addEventListener("focus", function () { dechiffre(false); });
  /* À l'arrivée, l'étiquette se présente quelques secondes, puis laisse l'orbe seule. */
  setTimeout(function () { if (root.classList.contains("is-open")) return; fab.classList.add("is-dit"); dechiffre(true); setTimeout(function () { fab.classList.remove("is-dit"); }, 6400); }, 1400);

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
    occupe = true; send.disabled = true; orbeEtat("pense");
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
      if (!live) { attente.remove(); live = bulle("assistant", ""); live.classList.add("jv-cursor"); orbeEtat("parle"); }
      live.innerHTML = rich(txt); bas();
    }
    var ctl = window.AbortController ? new AbortController() : null;
    var minuteur = setTimeout(function () { if (ctl) ctl.abort(); }, 130000);

    var corps = { messages: msgs.slice(-10).map(function (m) { return { role: m.role, content: m.content }; }), stream: true, lang: EN ? "en" : "fr" };
    function traiteSSE(ligne) {
      try { var j = JSON.parse(ligne); if (j.d) ajoute(j.d); if (j.g) gestes.push(j.g); } catch (e) {}
    }
    function directe() {
      return fetch(URL_GUIDE + "/chat", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corps),
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
            blocs.forEach(function (b) { if (b.indexOf("data: ") === 0) traiteSSE(b.slice(6)); });
            return lis();
          });
        }
        return lis();
      });
    }
    /* Pont : quand le portier refuse l'origine de cette page (autre domaine), la requête part
       d'un cadre hébergé sur jameslaplume.ca, que le portier accepte. */
    function parPont() {
      return pontPret().then(function (cadre) {
        return new Promise(function (resolve, reject) {
          var id = String(Date.now()) + Math.random().toString(36).slice(2);
          function fin() { window.removeEventListener("message", h); }
          function h(e) {
            if (e.origin !== PONT_ORIGINE || !e.data || e.data.jv !== "pont" || e.data.id !== id) return;
            if (e.data.sse) traiteSSE(e.data.sse);
            else if (e.data.json) { var d = e.data.json; if (d && d.reply) ajoute(d.reply); if (d && d.gestes) gestes = d.gestes; }
            else if (e.data.fin) { fin(); resolve(); }
            else if (e.data.err) { fin(); reject(new Error(e.data.err)); }
          }
          window.addEventListener("message", h);
          cadre.contentWindow.postMessage({ jv: "chat", id: id, body: corps }, PONT_ORIGINE);
          setTimeout(function () { fin(); reject(new Error("pont : délai")); }, 130000);
        });
      });
    }
    (PONT && location.origin !== PONT_ORIGINE ? directe().catch(function (e) { if (txt.trim()) throw e; return parPont(); }) : directe())
      .then(function () {
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
      clearTimeout(minuteur); occupe = false; send.disabled = false; orbeEtat("repos");
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
  fab.addEventListener("click", function () {
    if (calme || !ORBES.length) { ouvrir(true); return; }
    fab.classList.add("is-go"); ORBES[0].coup = 0.3;
    setTimeout(function () { fab.classList.remove("is-go"); ouvrir(true); }, 240);
  });
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
