/* Guide JARVIS — bulle de discussion du site.
   Parle uniquement au portier public (data-guide sur <html>), qui ne donne accès
   qu'à l'agent d'accueil hébergé par JARVIS. Aucun témoin; la conversation reste
   dans l'onglet (sessionStorage) et disparaît à sa fermeture. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var URL_GUIDE = (doc.getAttribute("data-guide") || "").replace(/\/$/, "");
  if (!URL_GUIDE || document.getElementById("jg-root")) return;

  var EN = (doc.lang || "").slice(0, 2) === "en";
  var T = EN ? {
    open: "Talk to JARVIS", live: "Online now", title: "JARVIS", sub: "Online · JARVIS Private Systems",
    hello: (new Date().getHours() < 17 ? "Good day." : "Good evening.") + " I'm JARVIS. Tell me about your home, cottage or business, and what you'd like me to take care of.",
    teaser: (new Date().getHours() < 17 ? "Good day." : "Good evening.") + " I'm JARVIS. Anything I can take care of for your home or business?",
    ph: "Talk to JARVIS…", send: "Send", think: "JARVIS is thinking…",
    note: "JARVIS is an artificial intelligence and can make mistakes. Don't share sensitive information.",
    err: "JARVIS is unavailable right now. You can reach the team at", contact: "/en/contact/",
    close: "Close", reset: "New conversation",
    chips: ["What is the Hub?", "Security for my business", "How much does it cost?"]
  } : {
    open: "Parler à JARVIS", live: "En ligne maintenant", title: "JARVIS", sub: "En ligne · JARVIS Private Systems",
    hello: (new Date().getHours() < 17 ? "Bonjour." : "Bonsoir.") + " Je suis JARVIS. Parlez-moi de votre maison, de votre chalet ou de votre entreprise, et de ce que vous aimeriez que je prenne en charge.",
    teaser: (new Date().getHours() < 17 ? "Bonjour." : "Bonsoir.") + " Je suis JARVIS. Je peux m’occuper de quelque chose pour votre maison ou votre entreprise?",
    ph: "Parlez à JARVIS…", send: "Envoyer", think: "JARVIS réfléchit…",
    note: "JARVIS est une intelligence artificielle : ses réponses peuvent contenir des erreurs. Ne partagez pas d’information sensible.",
    err: "JARVIS est indisponible pour le moment. Écrivez à l’équipe :", contact: "/contact/",
    close: "Fermer", reset: "Nouvelle conversation",
    chips: ["C’est quoi le Hub?", "Sécurité pour mon entreprise", "Combien ça coûte?"]
  };

  var KEY = "jg-conversation";
  var msgs = [];
  try { msgs = JSON.parse(sessionStorage.getItem(KEY) || "[]") || []; } catch (e) { msgs = []; }
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(msgs.slice(-20))); } catch (e) {} }

  var css = [
    "#jg-root{position:fixed;right:1.1rem;bottom:1.1rem;z-index:85;font-family:var(--sans,system-ui,sans-serif);color:var(--ink,#f5f5f7)}",
    "#jg-root *{box-sizing:border-box}",
    ".jg-fab{position:relative;display:flex;align-items:center;gap:.8rem;border:1px solid var(--mode-line,#d3bc9455);cursor:pointer;padding:.55rem 1.25rem .55rem .55rem;border-radius:999px;background:var(--mode-panel-solid,#0b0b0dfa);color:var(--ink,#f5f5f7);text-align:left;box-shadow:var(--mode-spec,none),0 0 0 1px #0006,0 14px 40px #000b,0 0 32px color-mix(in srgb,var(--mode-glow,#c9a35c) 35%,transparent);transition:transform .35s var(--ease,ease),box-shadow .35s}",
    ".jg-fab:hover{transform:translateY(-3px);box-shadow:var(--mode-spec,none),0 18px 48px #000c,0 0 44px color-mix(in srgb,var(--mode-glow,#c9a35c) 55%,transparent)}",
    ".jg-orb{position:relative;flex:none;width:48px;height:48px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#fff 0 9%,var(--gold-soft,#e9c98c) 10% 22%,transparent 23%),radial-gradient(circle,color-mix(in srgb,var(--mode-glow,#c9a35c) 45%,transparent) 0 55%,transparent 56%),#000;border:1.5px solid var(--gold-soft,#e9c98c);box-shadow:0 0 18px color-mix(in srgb,var(--mode-glow,#c9a35c) 70%,transparent),inset 0 0 12px color-mix(in srgb,var(--mode-glow,#c9a35c) 60%,transparent)}",
    ".jg-orb::before,.jg-orb::after{content:\"\";position:absolute;inset:-7px;border-radius:50%;border:1.5px solid var(--gold-soft,#e9c98c);opacity:0;animation:jg-ping 2.6s var(--ease,ease-out) infinite}",
    ".jg-orb::after{animation-delay:1.3s}",
    ".jg-orb i{position:absolute;inset:6px;border-radius:50%;border:1.5px dashed color-mix(in srgb,var(--gold-soft,#e9c98c) 70%,transparent);animation:jg-spin 9s linear infinite}",
    "@keyframes jg-ping{0%{transform:scale(.85);opacity:.7}100%{transform:scale(1.55);opacity:0}}",
    ".jg-txt b{display:block;font:600 1.02rem/1.15 var(--sans);background:var(--mode-display,#e7c888);-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".jg-txt small{display:flex;align-items:center;gap:.35rem;margin-top:.2rem;font:500 .66rem/1 var(--mono,monospace);letter-spacing:.12em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jg-live{width:7px;height:7px;border-radius:50%;background:#3ddc84;box-shadow:0 0 8px #3ddc84}",
    ".jg-dot{width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#fff 0 18%,transparent 19%),conic-gradient(from 0deg,#0000,#0008,#0000);border:2px solid currentColor;animation:jg-spin 6s linear infinite}",
    "@keyframes jg-spin{to{transform:rotate(1turn)}}",
    ".jg-teaser{position:absolute;right:0;bottom:calc(100% + .8rem);width:min(300px,calc(100vw - 2.2rem));padding:.85rem 2.1rem .85rem 1rem;border-radius:16px 16px 4px 16px;background:var(--mode-panel-solid,#0b0b0dfa);border:1px solid var(--mode-line,#d3bc9455);box-shadow:0 18px 50px #000c;font-size:.9rem;line-height:1.45;cursor:pointer;opacity:0;transform:translateY(8px);transition:opacity .5s,transform .5s var(--ease,ease);pointer-events:none}",
    ".jg-teaser.is-on{opacity:1;transform:none;pointer-events:auto}",
    ".jg-teaser button{position:absolute;top:.35rem;right:.35rem;border:0;background:none;color:var(--dim,#a8a8b0);cursor:pointer;font-size:.9rem;padding:.25rem .4rem;border-radius:6px}",
    "#jg-root.is-open .jg-teaser{display:none}",
    ".jg-panel{position:absolute;right:0;bottom:0;width:min(380px,calc(100vw - 2.2rem));height:min(560px,calc(100vh - 6rem));display:none;flex-direction:column;border-radius:var(--radius,16px);background:var(--mode-panel-solid,#0b0b0dfa);border:1px solid var(--mode-line,#d3bc9433);box-shadow:var(--mode-spec,none),0 24px 70px #000c;overflow:hidden;backdrop-filter:blur(18px)}",
    "#jg-root.is-open .jg-panel{display:flex}#jg-root.is-open .jg-fab{display:none}",
    ".jg-head{display:flex;align-items:center;gap:.7rem;padding:.9rem 1rem;border-bottom:1px solid var(--mode-line,#ffffff1a)}",
    ".jg-head b{display:block;font:600 .98rem/1.2 var(--sans);background:var(--mode-display,#e7c888);-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".jg-head small{display:block;font:500 .62rem/1.4 var(--mono,monospace);letter-spacing:.12em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jg-head .jg-dot{color:var(--gold-soft,#e9c98c);flex:none}",
    ".jg-head small::before{content:\"\";display:inline-block;width:6px;height:6px;margin-right:.4rem;border-radius:50%;background:#3ddc84;box-shadow:0 0 6px #3ddc84;vertical-align:1px}",
    ".jg-sp{flex:1}",
    ".jg-ic{border:0;background:none;color:var(--dim,#a8a8b0);cursor:pointer;font-size:1.05rem;padding:.3rem .45rem;border-radius:8px}",
    ".jg-ic:hover{color:var(--ink,#fff);background:#ffffff12}",
    ".jg-log{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.7rem;scroll-behavior:smooth}",
    ".jg-m{max-width:88%;padding:.65rem .85rem;border-radius:14px;font-size:.9rem;line-height:1.5;white-space:pre-wrap;word-wrap:break-word}",
    ".jg-m a{color:var(--gold-soft,#e9c98c)}",
    ".jg-a{align-self:flex-start;background:#ffffff0d;border:1px solid #ffffff14;border-bottom-left-radius:4px}",
    ".jg-u{align-self:flex-end;background:var(--mode-action,#cfa45b);color:var(--mode-on-action,#1c1408);border-bottom-right-radius:4px}",
    ".jg-t{color:var(--dim,#a8a8b0);font-style:italic}",
    ".jg-chips{display:flex;flex-wrap:wrap;gap:.4rem}",
    ".jg-chip{border:1px solid var(--mode-line,#ffffff26);background:none;color:var(--gold-soft,#e9c98c);border-radius:999px;padding:.4rem .7rem;font:500 .78rem/1 var(--sans);cursor:pointer}",
    ".jg-chip:hover{background:#ffffff0f}",
    ".jg-form{display:flex;gap:.5rem;padding:.75rem;border-top:1px solid var(--mode-line,#ffffff1a)}",
    ".jg-in{flex:1;min-width:0;background:#ffffff0d;border:1px solid #ffffff1f;color:var(--ink,#fff);border-radius:12px;padding:.65rem .8rem;font:400 .9rem/1.3 var(--sans);resize:none;max-height:7rem}",
    ".jg-in:focus{outline:none;border-color:var(--gold-soft,#e9c98c)}",
    ".jg-send{border:0;border-radius:12px;padding:0 .95rem;cursor:pointer;background:var(--mode-action,#cfa45b);color:var(--mode-on-action,#1c1408);font:600 .85rem/1 var(--sans)}",
    ".jg-send:disabled{opacity:.5;cursor:default}",
    ".jg-note{margin:0;padding:0 .9rem .7rem;font-size:.68rem;line-height:1.4;color:var(--dim,#a8a8b0)}",
    "@media (max-width:560px){#jg-root{right:.7rem;bottom:.7rem}.jg-fab{padding:.45rem 1rem .45rem .45rem;gap:.6rem}.jg-orb{width:42px;height:42px}.jg-txt b{font-size:.92rem}.jg-panel{width:calc(100vw - 1.4rem);height:calc(100vh - 5rem)}}",
    "@media (prefers-reduced-motion:reduce){.jg-dot,.jg-orb i,.jg-orb::before,.jg-orb::after{animation:none}}"
  ].join("");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var root = document.createElement("div");
  root.id = "jg-root";
  root.innerHTML =
    '<div class="jg-teaser" role="status"><span></span><button type="button" class="jg-tx">✕</button></div>' +
    '<button class="jg-fab" type="button" aria-expanded="false"><span class="jg-orb" aria-hidden="true"><i></i></span>' +
      '<span class="jg-txt"><b></b><small><i class="jg-live" aria-hidden="true"></i><span></span></small></span></button>' +
    '<section class="jg-panel" role="dialog" aria-modal="false">' +
      '<header class="jg-head"><i class="jg-dot" aria-hidden="true"></i><div><b></b><small></small></div><div class="jg-sp"></div>' +
        '<button class="jg-ic jg-reset" type="button">↺</button><button class="jg-ic jg-close" type="button">✕</button></header>' +
      '<div class="jg-log" aria-live="polite"></div>' +
      '<form class="jg-form"><textarea class="jg-in" rows="1" maxlength="1000"></textarea><button class="jg-send" type="submit"></button></form>' +
      '<p class="jg-note"></p>' +
    '</section>';
  document.body.appendChild(root);

  var fab = root.querySelector(".jg-fab"), panel = root.querySelector(".jg-panel");
  var log = root.querySelector(".jg-log"), form = root.querySelector(".jg-form");
  var input = root.querySelector(".jg-in"), send = root.querySelector(".jg-send");
  fab.querySelector(".jg-txt b").textContent = T.open;
  fab.querySelector(".jg-txt small span").textContent = T.live;
  var teaser = root.querySelector(".jg-teaser");
  teaser.querySelector("span").textContent = T.teaser;
  teaser.querySelector(".jg-tx").setAttribute("aria-label", T.close);
  fab.setAttribute("aria-label", T.open);
  panel.setAttribute("aria-label", T.title);
  root.querySelector(".jg-head b").textContent = T.title;
  root.querySelector(".jg-head small").textContent = T.sub;
  root.querySelector(".jg-close").setAttribute("aria-label", T.close);
  root.querySelector(".jg-close").title = T.close;
  root.querySelector(".jg-reset").setAttribute("aria-label", T.reset);
  root.querySelector(".jg-reset").title = T.reset;
  input.placeholder = T.ph; send.textContent = T.send;
  root.querySelector(".jg-note").textContent = T.note;

  /* Texte sûr : on échappe tout, puis on rend cliquables les liens http(s) et [texte](lien). */
  function esc(s) { return s.replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function rich(s) {
    var h = esc(s).replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, function (m, t, u) { return '<a href="' + u + '" rel="noopener">' + t + "</a>"; });
    h = h.replace(/(^|[\s(])(https?:\/\/[^\s<)]+[^\s<).,!?;:])/g, function (m, p, u) { return p + '<a href="' + u + '" rel="noopener">' + u + "</a>"; });
    return h;
  }
  function bubble(role, text, extra) {
    var d = document.createElement("div");
    d.className = "jg-m " + (role === "user" ? "jg-u" : "jg-a") + (extra ? " " + extra : "");
    if (role === "user") d.textContent = text; else d.innerHTML = rich(text);
    log.appendChild(d); log.scrollTop = log.scrollHeight;
    return d;
  }
  function chips() {
    var w = document.createElement("div"); w.className = "jg-chips";
    T.chips.forEach(function (c) {
      var b = document.createElement("button"); b.type = "button"; b.className = "jg-chip"; b.textContent = c;
      b.addEventListener("click", function () { w.remove(); ask(c); });
      w.appendChild(b);
    });
    log.appendChild(w);
  }
  function render() {
    log.innerHTML = "";
    bubble("assistant", T.hello);
    msgs.forEach(function (m) { bubble(m.role, m.content); });
    if (!msgs.length) chips();
  }

  var busy = false;
  function ask(q) {
    q = (q || "").trim().slice(0, 1000);
    if (!q || busy) return;
    busy = true; send.disabled = true;
    msgs.push({ role: "user", content: q }); save();
    var c = log.querySelector(".jg-chips"); if (c) c.remove();
    bubble("user", q);
    var wait = bubble("assistant", T.think, "jg-t");
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 130000);
    var txt = "", live = null;
    /* Affiche la réponse mot par mot dès qu'elle arrive. */
    function ajoute(morceau) {
      txt += morceau;
      if (!live) { wait.remove(); live = bubble("assistant", ""); }
      live.innerHTML = rich(txt);
      log.scrollTop = log.scrollHeight;
    }
    fetch(URL_GUIDE + "/chat", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: msgs.slice(-10), stream: true, lang: EN ? "en" : "fr" }),
      signal: ctl ? ctl.signal : undefined
    }).then(function (r) {
      var type = r.headers.get("Content-Type") || "";
      if (type.indexOf("text/event-stream") === -1 || !r.body || !r.body.getReader) {
        return r.json().catch(function () { return {}; }).then(function (d) { if (d && d.reply) ajoute(d.reply); });
      }
      var lecteur = r.body.getReader(), dec = new TextDecoder(), tampon = "";
      function lis() {
        return lecteur.read().then(function (res) {
          if (res.done) return;
          tampon += dec.decode(res.value, { stream: true });
          var blocs = tampon.split("\n\n"); tampon = blocs.pop();
          blocs.forEach(function (b) {
            if (b.indexOf("data: ") !== 0) return;
            try { var j = JSON.parse(b.slice(6)); if (j.d) ajoute(j.d); } catch (e) {}
          });
          return lis();
        });
      }
      return lis();
    }).then(function () {
      if (!txt.trim()) throw new Error("vide");
      msgs.push({ role: "assistant", content: txt.trim() }); save();
    }).catch(function () {
      if (txt.trim()) { msgs.push({ role: "assistant", content: txt.trim() }); save(); return; }
      wait.remove();
      bubble("assistant", T.err + " " + location.origin + T.contact);
      msgs.pop(); save();
    }).then(function () { clearTimeout(timer); busy = false; send.disabled = false; input.focus(); });
  }

  function open(on) {
    hideTeaser();
    root.classList.toggle("is-open", on);
    fab.setAttribute("aria-expanded", on ? "true" : "false");
    if (on) { if (!log.children.length) render(); setTimeout(function () { input.focus(); }, 50); }
    else fab.focus();
  }
  var TKEY = "jg-teaser-vu";
  function hideTeaser() { teaser.classList.remove("is-on"); try { sessionStorage.setItem(TKEY, "1"); } catch (e) {} }
  var dejaVu = false; try { dejaVu = !!sessionStorage.getItem(TKEY); } catch (e) {}
  if (!dejaVu && !msgs.length) setTimeout(function () { if (!root.classList.contains("is-open")) teaser.classList.add("is-on"); }, 5000);
  teaser.addEventListener("click", function (e) { if (e.target.closest(".jg-tx")) { hideTeaser(); return; } open(true); });
  /* Tout élément [data-jarvis] de la page ouvre aussi la conversation. */
  document.addEventListener("click", function (e) { var t = e.target.closest && e.target.closest("[data-jarvis]"); if (t) { e.preventDefault(); open(true); } });
  window.JARVIS = { ouvrir: function () { open(true); } };
  fab.addEventListener("click", function () { open(true); });
  root.querySelector(".jg-close").addEventListener("click", function () { open(false); });
  root.querySelector(".jg-reset").addEventListener("click", function () { msgs = []; save(); render(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; ask(q); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit")); }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.classList.contains("is-open")) open(false); });
})();
