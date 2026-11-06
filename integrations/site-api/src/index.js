// Service du site jameslaplume.ca — Worker Cloudflare.
//
//   POST /contact      reçoit le formulaire, l'envoie par Resend et le garde pour JARVIS
//   GET  /visits       renvoie le nombre de visites
//   POST /visits/hit   ajoute une visite (une par session, décidé par le navigateur)
//   GET  /leads        liste les demandes gardées (réservé à JARVIS, jeton requis)
//   GET  /live         batteries de l'ambulance (BouLance) en direct, lues dans Home Assistant
//   GET  /history      énergie stockée des dernières 24 h (Home Assistant)
//
// Liaisons attendues (voir wrangler.toml.example) :
//   SITE_KV        espace KV : demandes, compteur, limites d'envoi
//   RESEND_API_KEY secret : clé Resend (jamais dans le code ni dans Git)
//   LEADS_TOKEN    secret : jeton que JARVIS présentera pour lire les demandes
//   HA_TOKEN       secret : jeton longue durée Home Assistant (lecture seulement par ce service)
//   HA_URL, MAIL_FROM, MAIL_TO, ALLOWED_ORIGINS : variables simples
//
// Sécurité : le jeton Home Assistant ne sort jamais du Worker. Le service ne lit qu'une liste
// fermée d'entités (gabarit ci-dessous), ne commande rien, et met la réponse en cache 4 s pour
// qu'un afflux de visiteurs ne charge pas Home Assistant.

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

// Gabarit Jinja rendu par Home Assistant (POST /api/template) : une seule requête, une réponse
// minuscule, et seulement les valeurs publiques des batteries. Aucune position, aucun identifiant.
const BAT = (s) => `{"soc": {{ states('sensor.dp04s007l4s200a_batterie${s}') | float(-1) }},
 "v": {{ states('sensor.dp04s007l4s200a_tension${s}') | float(-1) }},
 "a": {{ states('sensor.dp04s007l4s200a_courant${s}') | float(0) }},
 "w": {{ states('sensor.dp04s007l4s200a_puissance${s}') | float(0) }},
 "t": {{ states('sensor.dp04s007l4s200a_temperature${s}') | float(-99) }},
 "wh": {{ states('sensor.dp04s007l4s200a_energie_stockee${s}') | float(-1) }},
 "cap": {{ states('sensor.dp04s007l4s200a_design_capacity${s}') | float(0) }},
 "cycles": {{ states('sensor.dp04s007l4s200a_cycles${s}') | int(-1) }},
 "hi": {{ states('sensor.dp04s007l4s200a_highest_cell_voltage${s}') | float(-1) }},
 "lo": {{ states('sensor.dp04s007l4s200a_lowest_cell_voltage${s}') | float(-1) }},
 "delta": {{ states('sensor.dp04s007l4s200a_delta_cell_voltage${s}') | float(-1) }},
 "charging": {{ is_state('binary_sensor.dp04s007l4s200a_en_charge${s}', 'on') | tojson }},
 "balancing": {{ is_state('binary_sensor.dp04s007l4s200a_balancer${s}', 'on') | tojson }},
 "chg": {{ is_state('binary_sensor.dp04s007l4s200a_charge_mosfet${s}', 'on') | tojson }},
 "dsg": {{ is_state('binary_sensor.dp04s007l4s200a_discharge_mosfet${s}', 'on') | tojson }},
 "problem": {{ is_state('binary_sensor.dp04s007l4s200a_probleme${s}', 'on') | tojson }},
 "online": {{ (states('sensor.dp04s007l4s200a_tension${s}') not in ['unavailable','unknown']) | tojson }},
 "seen": {{ as_timestamp(states.sensor.dp04s007l4s200a_tension${s}.last_reported or states.sensor.dp04s007l4s200a_tension${s}.last_updated, 0) | int }}}`;
const LIVE_TEMPLATE = `{"batteries": [${BAT("")}, ${BAT("_2")}],
 "total": {"ah": {{ states('sensor.batteries_capacite_restante_totale') | float(-1) }},
  "kwh": {{ states('sensor.batteries_energie_totale') | float(-1) }},
  "w": {{ states('sensor.batteries_puissance_totale') | float(0) }},
  "a": {{ states('sensor.batteries_courant_total') | float(0) }},
  "hours": {{ states('sensor.batteries_autonomie_estimee') | float(-1) }},
  "delta24": {{ states('sensor.batteries_ecart_cellules_maximum_24_h') | float(-1) }},
  "alarm": {{ is_state('binary_sensor.batteries_alarme_generale', 'on') | tojson }}},
 "now": {{ as_timestamp(now()) | int }}}`;

async function ha(env, path, init) {
  const r = await fetch(env.HA_URL.replace(/\/$/, "") + path, {
    ...init,
    headers: { Authorization: "Bearer " + env.HA_TOKEN, "Content-Type": "application/json" },
  });
  if (!r.ok) throw new Error("Home Assistant " + r.status);
  return r;
}

async function cached(request, ttl, h, produce) {
  const cache = caches.default;
  const key = new Request(new URL(request.url).origin + new URL(request.url).pathname, { method: "GET" });
  let hit = await cache.match(key);
  if (hit) {
    const body = await hit.text();
    return new Response(body, { status: 200, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...h } });
  }
  const body = JSON.stringify(await produce());
  await cache.put(key, new Response(body, { headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=" + ttl } }));
  return new Response(body, { status: 200, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...h } });
}

async function live(request, env, h) {
  if (!env.HA_TOKEN || !env.HA_URL) return json({ ok: false, message: "Liaison non configurée." }, 503, h);
  try {
    return await cached(request, 4, h, async () => {
      const r = await ha(env, "/api/template", { method: "POST", body: JSON.stringify({ template: LIVE_TEMPLATE }) });
      const data = JSON.parse(await r.text());
      return { ok: true, ...data };
    });
  } catch (e) {
    return json({ ok: false, message: "Home Assistant ne répond pas." }, 502, h);
  }
}

async function history(request, env, h) {
  if (!env.HA_TOKEN || !env.HA_URL) return json({ ok: false }, 503, h);
  try {
    return await cached(request, 300, h, async () => {
      const start = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
      const r = await ha(env, "/api/history/period/" + encodeURIComponent(start) +
        "?filter_entity_id=sensor.batteries_energie_totale&minimal_response&no_attributes", { method: "GET" });
      const raw = (await r.json())[0] || [];
      const pts = raw.map((p) => [Date.parse(p.last_changed || p.lu * 1000), parseFloat(p.state ?? p.s)])
        .filter((p) => isFinite(p[0]) && isFinite(p[1]));
      // Au plus 96 points (un toutes les 15 min), pour une courbe légère.
      const out = [];
      const step = 15 * 60 * 1000;
      let next = 0;
      for (const p of pts) { if (p[0] >= next) { out.push([Math.round(p[0] / 1000), Math.round(p[1] * 1000) / 1000]); next = p[0] + step; } }
      if (pts.length) out.push([Math.round(pts[pts.length - 1][0] / 1000), pts[pts.length - 1][1]]);
      return { ok: true, unit: "kWh", points: out };
    });
  } catch (e) {
    return json({ ok: false }, 502, h);
  }
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
      if (url.pathname === "/live" && request.method === "GET") return await live(request, env, h);
      if (url.pathname === "/history" && request.method === "GET") return await history(request, env, h);
      return json({ ok: true, service: "jameslaplume.ca" }, 200, h);
    } catch (e) {
      return json({ ok: false, message: "Erreur du service." }, 500, h);
    }
  },
};
