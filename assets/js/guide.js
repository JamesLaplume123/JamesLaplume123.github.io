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
    open: "Ask the JARVIS Guide", title: "JARVIS Guide", sub: "Private AI · hosted by JARVIS",
    hello: "Hi! I'm the JARVIS Guide. Tell me about your place (home, cottage, business, farm, RV…) and what you'd like to improve. I'll point you to the right solution.",
    ph: "Your question…", send: "Send", think: "The Guide is thinking…",
    note: "AI answers can be wrong. Don't share personal or sensitive information.",
    err: "The Guide is unavailable right now. You can reach us at", contact: "/en/contact/",
    close: "Close", reset: "New conversation",
    chips: ["What is the Hub?", "Security for my business", "How much does it cost?"]
  } : {
    open: "Parler au Guide JARVIS", title: "Guide JARVIS", sub: "IA privée · hébergée par JARVIS",
    hello: "Bonjour! Je suis le Guide JARVIS. Parlez-moi de votre lieu (maison, chalet, entreprise, ferme, VR…) et de ce que vous aimeriez améliorer : je vous oriente vers la bonne solution.",
    ph: "Votre question…", send: "Envoyer", think: "Le Guide réfléchit…",
    note: "Réponses générées par IA, elles peuvent contenir des erreurs. Ne partagez pas d’information personnelle ou sensible.",
    err: "Le Guide est indisponible pour le moment. Écrivez-nous :", contact: "/contact/",
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
    ".jg-fab{display:flex;align-items:center;gap:.6rem;border:0;cursor:pointer;padding:.7rem 1.05rem .7rem .75rem;border-radius:999px;background:var(--mode-action,linear-gradient(135deg,#f6e2b5,#cfa45b));color:var(--mode-on-action,#1c1408);font:600 .9rem/1 var(--sans,system-ui);box-shadow:var(--mode-action-edge,none),0 12px 34px #0009;transition:transform .35s var(--ease,ease)}",
    ".jg-fab:hover{transform:translateY(-2px)}",
    ".jg-dot{width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#fff 0 18%,transparent 19%),conic-gradient(from 0deg,#0000,#0008,#0000);border:2px solid currentColor;animation:jg-spin 6s linear infinite}",
    "@keyframes jg-spin{to{transform:rotate(1turn)}}",
    ".jg-panel{position:absolute;right:0;bottom:0;width:min(380px,calc(100vw - 2.2rem));height:min(560px,calc(100vh - 6rem));display:none;flex-direction:column;border-radius:var(--radius,16px);background:var(--mode-panel-solid,#0b0b0dfa);border:1px solid var(--mode-line,#d3bc9433);box-shadow:var(--mode-spec,none),0 24px 70px #000c;overflow:hidden;backdrop-filter:blur(18px)}",
    "#jg-root.is-open .jg-panel{display:flex}#jg-root.is-open .jg-fab{display:none}",
    ".jg-head{display:flex;align-items:center;gap:.7rem;padding:.9rem 1rem;border-bottom:1px solid var(--mode-line,#ffffff1a)}",
    ".jg-head b{display:block;font:600 .98rem/1.2 var(--sans);background:var(--mode-display,#e7c888);-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".jg-head small{display:block;font:500 .62rem/1.4 var(--mono,monospace);letter-spacing:.12em;text-transform:uppercase;color:var(--dim,#a8a8b0)}",
    ".jg-head .jg-dot{color:var(--gold-soft,#e9c98c);flex:none}",
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
    "@media (max-width:560px){#jg-root{right:.7rem;bottom:.7rem}.jg-fab span{display:none}.jg-fab{padding:.65rem}.jg-panel{width:calc(100vw - 1.4rem);height:calc(100vh - 5rem)}}",
    "@media (prefers-reduced-motion:reduce){.jg-dot{animation:none}}"
  ].join("");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var root = document.createElement("div");
  root.id = "jg-root";
  root.innerHTML =
    '<button class="jg-fab" type="button" aria-expanded="false"><i class="jg-dot" aria-hidden="true"></i><span></span></button>' +
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
  fab.querySelector("span").textContent = T.open;
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
    root.classList.toggle("is-open", on);
    fab.setAttribute("aria-expanded", on ? "true" : "false");
    if (on) { if (!log.children.length) render(); setTimeout(function () { input.focus(); }, 50); }
    else fab.focus();
  }
  fab.addEventListener("click", function () { open(true); });
  root.querySelector(".jg-close").addEventListener("click", function () { open(false); });
  root.querySelector(".jg-reset").addEventListener("click", function () { msgs = []; save(); render(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; ask(q); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit")); }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.classList.contains("is-open")) open(false); });
})();
