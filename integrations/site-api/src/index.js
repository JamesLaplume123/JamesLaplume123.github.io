// Service du site jameslaplume.ca — Worker Cloudflare.
//
//   POST /contact      reçoit le formulaire, l'envoie par Resend et le garde pour JARVIS
//   GET  /visits       renvoie le nombre de visites
//   POST /visits/hit   ajoute une visite (une par session, décidé par le navigateur)
//   GET  /leads        liste les demandes gardées (réservé à JARVIS, jeton requis)
//
// Liaisons attendues (voir wrangler.toml.example) :
//   SITE_KV        espace KV : demandes, compteur, limites d'envoi
//   RESEND_API_KEY secret : clé Resend (jamais dans le code ni dans Git)
//   LEADS_TOKEN    secret : jeton que JARVIS présentera pour lire les demandes
//   MAIL_FROM, MAIL_TO, ALLOWED_ORIGINS : variables simples

const MAX = { nom: 120, email: 200, organisation: 160, region: 120, profil: 80, sujet: 120, environnement: 80, message: 5000, page: 200 };

function cors(origin, env) {
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const ok = allowed.includes(origin);
  return {
    "Access-Control-Allow-Origin": ok ? origin : allowed[0] || "https://jameslaplume.ca",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function json(body, status, headers) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...headers },
  });
}

function clean(v, max) {
  return String(v == null ? "" : v).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").trim().slice(0, max);
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function limited(env, ip) {
  // 5 envois par heure et par adresse : assez pour un humain, trop peu pour un robot.
  const key = "rate:" + ip + ":" + Math.floor(Date.now() / 3600000);
  const n = parseInt((await env.SITE_KV.get(key)) || "0", 10);
  if (n >= 5) return true;
  await env.SITE_KV.put(key, String(n + 1), { expirationTtl: 3700 });
  return false;
}

async function contact(request, env, h) {
  let data;
  try { data = await request.json(); } catch { return json({ ok: false, message: "Format invalide." }, 400, h); }
  if (data._honey) return json({ ok: true }, 200, h); // robot : on fait semblant
  const lead = {};
  for (const k of Object.keys(MAX)) lead[k] = clean(data[k], MAX[k]);
  if (!lead.nom || !lead.message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(lead.email)) {
    return json({ ok: false, message: "Nom, courriel valide et message requis." }, 422, h);
  }
  const ip = request.headers.get("CF-Connecting-IP") || "inconnue";
  if (await limited(env, ip)) return json({ ok: false, message: "Trop d’envois. Réessayez dans une heure." }, 429, h);

  lead.recu = new Date().toISOString();
  lead.id = crypto.randomUUID();
  lead.statut = "nouveau";

  // Gardé d'abord : même si le courriel échoue, la demande n'est pas perdue.
  await env.SITE_KV.put("lead:" + lead.recu + ":" + lead.id, JSON.stringify(lead));

  const rows = [
    ["Nom", lead.nom], ["Courriel", lead.email], ["Environnement", lead.environnement],
    ["Organisation", lead.organisation], ["Région", lead.region], ["Profil", lead.profil],
    ["Sujet", lead.sujet], ["Page", lead.page],
  ].filter(([, v]) => v);
  const html =
    '<div style="font-family:system-ui,sans-serif;font-size:15px;color:#111">' +
    "<h2 style=\"margin:0 0 12px\">Nouvelle demande — jameslaplume.ca</h2>" +
    '<table style="border-collapse:collapse">' +
    rows.map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#666">${k}</td><td style="padding:4px 0"><b>${escapeHtml(v)}</b></td></tr>`).join("") +
    "</table>" +
    `<p style="white-space:pre-wrap;margin-top:16px;padding:12px;background:#f5f5f5;border-radius:8px">${escapeHtml(lead.message)}</p>` +
    `<p style="color:#888;font-size:12px">Référence ${lead.id} · reçue ${lead.recu}</p></div>`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: "Bearer " + env.RESEND_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env.MAIL_FROM,
      to: [env.MAIL_TO],
      reply_to: lead.email,
      subject: "Demande — " + (lead.sujet || "JARVIS") + " — " + lead.nom,
      html,
    }),
  });
  if (!r.ok) {
    lead.statut = "courriel-en-echec";
    await env.SITE_KV.put("lead:" + lead.recu + ":" + lead.id, JSON.stringify(lead));
    // La demande est gardée : on confirme au visiteur, James la verra dans JARVIS.
  }
  return json({ ok: true, id: lead.id }, 200, h);
}

async function visits(env, h, hit) {
  let n = parseInt((await env.SITE_KV.get("visits")) || "0", 10);
  if (hit) {
    n += 1;
    await env.SITE_KV.put("visits", String(n));
  }
  return json({ value: n }, 200, h);
}

async function leads(request, env, h) {
  const auth = request.headers.get("Authorization") || "";
  if (!env.LEADS_TOKEN || auth !== "Bearer " + env.LEADS_TOKEN) return json({ ok: false }, 401, h);
  const list = await env.SITE_KV.list({ prefix: "lead:", limit: 1000 });
  const out = [];
  for (const k of list.keys) {
    const v = await env.SITE_KV.get(k.name);
    if (v) out.push(JSON.parse(v));
  }
  return json({ ok: true, leads: out.reverse() }, 200, h);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const h = cors(request.headers.get("Origin") || "", env);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
    try {
      if (url.pathname === "/contact" && request.method === "POST") return await contact(request, env, h);
      if (url.pathname === "/visits" && request.method === "GET") return await visits(env, h, false);
      if (url.pathname === "/visits/hit" && request.method === "POST") return await visits(env, h, true);
      if (url.pathname === "/leads" && request.method === "GET") return await leads(request, env, h);
      return json({ ok: true, service: "jameslaplume.ca" }, 200, h);
    } catch (e) {
      return json({ ok: false, message: "Erreur du service." }, 500, h);
    }
  },
};
