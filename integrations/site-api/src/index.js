// Service du site jameslaplume.ca — Worker Cloudflare.

// Durée de conservation du journal des visites, en jours (24 mois). Une seule ligne à changer;
// penser alors à /confidentialite/, à /admin/visites/ et aux README.
const RETENTION_JOURS = 730;

//
//   POST /contact      reçoit le formulaire, l'envoie par Resend et le garde pour JARVIS
//   GET  /visits       renvoie le nombre de visites
//   POST /visits/hit   ajoute une visite (une par session, décidé par le navigateur) et l'inscrit au journal
//   POST /visits/view  inscrit au journal une page vue de plus dans la même session (sans toucher au compteur)
//   GET  /visits/log   journal des visites, par tranches (réservé à James, jeton LEADS_TOKEN requis)
//   POST /chat/log     copie d'un échange avec JARVIS (envoyée par la bulle du site)
//   GET  /chats        conversations avec JARVIS, les plus récentes d'abord (jeton LEADS_TOKEN requis,
//                      page /admin/visites/)
//   GET  /leads        liste les demandes gardées (réservé à JARVIS, jeton requis)
//   GET  /live         batteries de l'ambulance (BouLance) en direct, lues dans Home Assistant
//   GET  /history      énergie stockée des dernières 24 h (Home Assistant)
//
// Liaisons attendues (voir wrangler.toml.example) :
//   SITE_KV        espace KV : demandes, compteur, journal des visites, limites d'envoi
//   RESEND_API_KEY secret : clé Resend (jamais dans le code ni dans Git)
//   LEADS_TOKEN    secret : jeton que JARVIS (demandes) et la page /admin/visites/ (journal) présentent
//   HA_TOKEN       secret : jeton longue durée Home Assistant (lecture seulement par ce service)
//   HA_URL, MAIL_FROM, MAIL_TO, ALLOWED_ORIGINS : variables simples
//
// Journal des visites : chaque visite est gardée 24 mois (RETENTION_JOURS), puis KV l'efface tout
// seul (expirationTtl). Seules les requêtes venant du site (en-tête Origin dans ALLOWED_ORIGINS, hors
// localhost) et qui ne sont pas des robots évidents sont comptées et inscrites. Il contient l'adresse IP, la localisation approximative que Cloudflare tire de cette adresse, le
// fournisseur Internet, la page, le domaine du site d'où vient le visiteur et le type d'appareil.
// Aucun témoin, aucun identifiant posé dans le navigateur. Annoncé dans /confidentialite/ (Loi 25).
//
// Clés KV du journal :
//   visit:<horodatage inversé>:<8 car.>  une visite (les plus récentes sortent en premier), 24 mois
//   vstat:AAAA-MM-JJ                     compteurs du jour (heure de Toronto) : visites, pages, et les
//                                        cumuls depuis le début; aucun renseignement personnel, gardés
//   vjour                                dernier jour qui a un compteur (écrit une fois par jour)
//   visits                               ancien compteur public : lu comme point de départ, plus écrit
//   archive:AAAA-MM-JJ                   relevé d'avant la mise en service, créé à la main par James
// Écritures KV (quota gratuit : 1 000 par jour) : 2 par visite ou par page vue (la visite et le
// compteur du jour), plus 1 par jour (vjour). Rien pour une requête ignorée.
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
    "Access-Control-Allow-Headers": "Content-Type, Accept, Authorization",
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
  // Formulaire : 5 envois par heure et par adresse, assez pour un humain, trop peu pour un robot.
  // (Le journal des visites a son propre plafond, en mémoire : voir tooMany.)
  const key = "rate:" + ip + ":" + Math.floor(Date.now() / 3600000);
  const n = parseInt((await env.SITE_KV.get(key)) || "0", 10);
  if (n >= 5) return true;
  await env.SITE_KV.put(key, String(n + 1), { expirationTtl: 3700 });
  return false;
}

// Même contrôle pour tout ce qui est réservé : « Authorization: Bearer <LEADS_TOKEN> ».
function authorized(request, env) {
  const auth = request.headers.get("Authorization") || "";
  return Boolean(env.LEADS_TOKEN) && auth === "Bearer " + env.LEADS_TOKEN;
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

  if (!env.RESEND_API_KEY) {
    // Demande gardée, mais pas encore de courriel : le site passe au service de secours.
    return json({ ok: false, stored: true, message: "Envoi par courriel non configuré." }, 503, h);
  }
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
    // Demande gardée; le site tente aussi le service de secours pour que James la reçoive.
    return json({ ok: false, stored: true, message: "Le courriel n’est pas parti." }, 502, h);
  }
  return json({ ok: true, id: lead.id }, 200, h);
}

// Compteur public : le cumul voyage dans le compteur du jour (vstat), pour ne pas payer une
// écriture de plus par visite. L'ancienne clé « visits » sert de point de départ.
async function visits(env, h) {
  return json({ value: await readTotal(env) }, 200, h);
}

// ---------- Journal des visites ----------
const VISIT_TTL = RETENTION_JOURS * 24 * 3600; // 24 mois, puis effacement automatique par KV
const VISITS_PER_IP_HOUR = 60;   // au-delà, l'adresse est ignorée pour l'heure (mémoire du Worker, sans écriture)
const JOURNAL_MAX_PAR_JOUR = 450; // au-delà, plus rien n'est écrit ce jour-là : le quota KV reste pour le formulaire
const KEY_MAX = 9999999999999;   // horodatage inversé : les clés les plus récentes sortent en premier
const TZ = "America/Toronto";    // les jours des compteurs suivent l'heure du Québec
const STAT_JOURS = 400;          // nombre de jours de compteurs renvoyés à la page privée
const PROLONGER_MAX = 20;        // visites de l'ancien régime (30 jours) prolongées par lecture du journal

// Robots évidents : jamais comptés ni inscrits.
const ROBOT_UA = /bot|crawl|spider|slurp|headless|facebookexternalhit|preview|lighthouse|pagespeed|monitor|uptime|pingdom|scrapy|curl|wget|python|httpclient|go-http|okhttp|java\/|libwww|phantom|puppeteer|playwright|selenium/i;
function isRobot(ua) { return !ua || ROBOT_UA.test(ua); }

// Vient-elle du vrai site ? Origin doit être dans ALLOWED_ORIGINS, et jamais un poste local
// (localhost reste permis pour les essais du formulaire, mais ne compte pas comme visite).
function fromSite(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (!origin || !allowed.includes(origin)) return false;
  try { return !/^(localhost|127\.\d+\.\d+\.\d+|\[::1\]|.*\.localhost)$/.test(new URL(origin).hostname); } catch { return false; }
}

// Plafond par adresse et par heure, tenu en mémoire : aucune écriture KV. Approximatif (chaque
// instance du Worker a sa mémoire); le plafond du jour ci-dessus est le vrai filet.
const recent = new Map();
function tooMany(ip, now) {
  const hour = Math.floor(now / 3600000);
  if (recent.size > 5000) recent.clear();
  const r = recent.get(ip);
  if (!r || r.h !== hour) { recent.set(ip, { h: hour, n: 1 }); return false; }
  r.n += 1;
  return r.n > VISITS_PER_IP_HOUR;
}

const dayFmt = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" });
function dayOf(ms) { return dayFmt.format(new Date(ms)); } // « 2026-11-15 »

function parseStat(v) {
  try {
    const s = typeof v === "string" ? JSON.parse(v) : v;
    if (!s || typeof s !== "object") return null;
    const n = (x) => (Number.isFinite(+x) && +x >= 0 ? Math.floor(+x) : 0);
    return { visites: n(s.visites), pages: n(s.pages), total: n(s.total), pagesTotal: n(s.pagesTotal) };
  } catch { return null; }
}

// Cumuls au dernier jour connu (ou l'ancien compteur, avant le premier compteur du jour).
async function lastTotals(env) {
  const last = await env.SITE_KV.get("vjour");
  const s = last ? parseStat(await env.SITE_KV.get("vstat:" + last)) : null;
  if (s) return s;
  return { visites: 0, pages: 0, total: parseInt((await env.SITE_KV.get("visits")) || "0", 10) || 0, pagesTotal: 0 };
}

async function readTotal(env) {
  const today = parseStat(await env.SITE_KV.get("vstat:" + dayOf(Date.now())));
  return today ? today.total : (await lastTotals(env)).total;
}

// Chemin de la page seulement (« /solutions/ »), sans paramètres ni fragment, 200 caractères au plus.
function cleanPath(v) {
  let p = clean(v, 400);
  if (!p) return "";
  try { p = new URL(p, "https://jameslaplume.ca").pathname; } catch { return ""; }
  try { p = decodeURIComponent(p); } catch {}
  p = p.replace(/[^\p{L}\p{N}\/._~-]/gu, "");
  return p.startsWith("/") ? p.slice(0, 200) : "";
}

// Domaine seulement (« www.google.com ») : jamais l'adresse complète, qui peut contenir une recherche.
function cleanRef(v) {
  const r = clean(v, 500);
  if (!r) return "";
  try {
    const host = new URL(r).hostname.toLowerCase();
    return /^[a-z0-9.-]{1,100}$/.test(host) ? host : "";
  } catch { return ""; }
}

// Type d'appareil, système et navigateur, en mots simples, à partir du User-Agent.
function device(ua) {
  const u = ua || "";
  let appareil = "Ordinateur";
  if (isRobot(u)) appareil = "Robot";
  else if (/iPad|Tablet|PlayBook|Silk|Android(?!.*Mobile)/i.test(u)) appareil = "Tablette";
  else if (/Mobi|iPhone|iPod|Android.*Mobile|Windows Phone/i.test(u)) appareil = "Mobile";
  const systeme =
    /iPhone|iPad|iPod/.test(u) ? "iOS" :
    /Android/.test(u) ? "Android" :
    /CrOS/.test(u) ? "ChromeOS" :
    /Windows/.test(u) ? "Windows" :
    /Mac OS X|Macintosh/.test(u) ? "macOS" :
    /Linux/.test(u) ? "Linux" : "Autre";
  const navigateur =
    /Edg\//.test(u) ? "Edge" :
    /OPR\/|Opera/.test(u) ? "Opera" :
    /SamsungBrowser/.test(u) ? "Samsung Internet" :
    /Firefox\/|FxiOS/.test(u) ? "Firefox" :
    /Chrome\/|CriOS/.test(u) ? "Chrome" :
    /Safari\//.test(u) ? "Safari" : "Autre";
  return { appareil, systeme, navigateur };
}

async function readBody(request) {
  // Le site envoie du texte brut (JSON) pour éviter une requête préalable CORS.
  try { return JSON.parse((await request.text()) || "{}") || {}; } catch { return {}; }
}

// Compte et inscrit une visite (« arrivee ») ou une page suivante (« page »). Renvoie le compteur
// public. Deux écritures KV : le compteur du jour (attendu) et la visite (« later », sans faire attendre).
async function record(request, env, data, kind, later) {
  const ua = clean(request.headers.get("User-Agent"), 400);
  const ip = request.headers.get("CF-Connecting-IP") || "inconnue";
  const now = Date.now();
  if (!fromSite(request, env) || isRobot(ua) || tooMany(ip, now)) return readTotal(env);

  const day = dayOf(now);
  let stat = parseStat(await env.SITE_KV.get("vstat:" + day));
  let firstOfDay = false;
  if (!stat) {
    const prev = await lastTotals(env);
    stat = { visites: 0, pages: 0, total: prev.total, pagesTotal: prev.pagesTotal };
    firstOfDay = true;
  }
  if (stat.pages >= JOURNAL_MAX_PAR_JOUR) return stat.total;
  stat.pages += 1;
  stat.pagesTotal += 1;
  if (kind === "arrivee") { stat.visites += 1; stat.total += 1; }
  // Les compteurs voyagent aussi dans les métadonnées : la page privée les lit en une seule liste.
  await env.SITE_KV.put("vstat:" + day, JSON.stringify(stat), { metadata: stat });
  if (firstOfDay) await env.SITE_KV.put("vjour", day);

  const cf = request.cf || {};
  const num = (v) => (v == null || v === "" || !isFinite(+v) ? null : Math.round(+v * 1000) / 1000);
  const visit = {
    t: new Date(now).toISOString(),
    type: kind,                                    // « arrivee » (première page) ou « page » (suivantes)
    page: cleanPath(data.path),
    ref: cleanRef(data.ref),
    pays: clean(cf.country, 2).toUpperCase(),      // code ISO à deux lettres (CA, US, FR…)
    region: clean(cf.region, 80),
    ville: clean(cf.city, 80),
    lat: num(cf.latitude),
    lon: num(cf.longitude),
    fuseau: clean(cf.timezone, 60),
    asn: cf.asn ? Number(cf.asn) || null : null,
    fournisseur: clean(cf.asOrganization, 100),
    ip: clean(ip, 45),
    ...device(ua),
  };
  const key = "visit:" + String(KEY_MAX - now).padStart(13, "0") + ":" + crypto.randomUUID().slice(0, 8);
  const body = JSON.stringify(visit);
  // La visite voyage aussi dans les métadonnées de la clé (1 024 octets au plus) : le journal se lit
  // alors en une seule requête à KV, sans relire chaque visite.
  const small = new TextEncoder().encode(body).length <= 1000;
  later(env.SITE_KV.put(key, body, small ? { expirationTtl: VISIT_TTL, metadata: visit } : { expirationTtl: VISIT_TTL }).catch(() => {}));
  return stat.total;
}

function defer(ctx, jobs) {
  return (p) => { if (ctx && ctx.waitUntil) ctx.waitUntil(p); else jobs.push(p); };
}

async function hit(request, env, h, ctx) {
  const data = await readBody(request);
  const jobs = [];
  const value = await record(request, env, data, "arrivee", defer(ctx, jobs));
  await Promise.all(jobs);
  return json({ value }, 200, h);
}

async function view(request, env, h, ctx) {
  const data = await readBody(request);
  const jobs = [];
  // Le journal ne fait jamais échouer la page : une erreur de KV reste silencieuse.
  await record(request, env, data, "page", defer(ctx, jobs)).catch(() => {});
  await Promise.all(jobs);
  return json({ ok: true }, 200, h);
}

// Compteurs par jour : une liste par année (métadonnées), sans lire chaque clé.
async function dayStats(env) {
  const year = +dayOf(Date.now()).slice(0, 4);
  const jours = [];
  for (const y of [year - 1, year]) {
    let cursor;
    do {
      const list = await env.SITE_KV.list({ prefix: "vstat:" + y + "-", limit: 1000, cursor });
      for (const k of list.keys) {
        const s = parseStat(k.metadata) || parseStat(await env.SITE_KV.get(k.name));
        if (s) jours.push({ jour: k.name.slice(6), visites: s.visites, pages: s.pages });
      }
      cursor = list.list_complete ? undefined : list.cursor;
    } while (cursor);
  }
  jours.sort((a, b) => (a.jour < b.jour ? -1 : 1));
  const t = await lastTotals(env);
  return { jours: jours.slice(-STAT_JOURS), totaux: { visites: t.total, pages: t.pagesTotal } };
}

// Relevés d'avant la mise en service (clés « archive:AAAA-MM-JJ », créées à la main). Un relevé
// plus vieux que la durée de conservation n'est plus servi et est effacé.
async function archives(env, later) {
  const list = await env.SITE_KV.list({ prefix: "archive:", limit: 20 });
  const out = [];
  for (const k of list.keys) {
    const since = Date.parse(k.name.slice(8) + "T00:00:00Z");
    if (isFinite(since) && Date.now() - since > VISIT_TTL * 1000) { later(env.SITE_KV.delete(k.name).catch(() => {})); continue; }
    const v = await env.SITE_KV.get(k.name);
    if (!v) continue;
    try { out.push({ cle: k.name, contenu: JSON.parse(v) }); } catch {}
  }
  return out;
}

async function visitLog(request, env, h, ctx) {
  if (!authorized(request, env)) return json({ ok: false }, 401, h);
  const q = new URL(request.url).searchParams;
  const asked = parseInt(q.get("limit") || "200", 10);
  const limit = Math.max(1, Math.min(500, isFinite(asked) ? asked : 200));
  const cursor = clean(q.get("cursor"), 2000) || undefined;
  const jobs = [];
  const later = defer(ctx, jobs);
  // Les clés « visit: » sortent de KV dans l'ordre alphabétique; l'horodatage inversé met donc les
  // plus récentes en premier, et le curseur de KV donne la tranche suivante.
  const list = await env.SITE_KV.list({ prefix: "visit:", limit, cursor });
  const out = [];
  let prolonged = 0;
  for (const k of list.keys) {
    let v = k.metadata && k.metadata.t ? k.metadata : null;
    let raw = null;
    if (!v) {
      raw = await env.SITE_KV.get(k.name);
      if (raw) { try { v = JSON.parse(raw); } catch {} }
    }
    if (!v) continue;
    out.push(v);
    // Visites écrites sous l'ancien régime (30 jours) : on repousse leur échéance à 24 mois après
    // la visite, quelques-unes par lecture, pour qu'elles ne s'effacent pas avant.
    const wanted = Math.floor(Date.parse(v.t) / 1000) + VISIT_TTL;
    if (k.expiration && isFinite(wanted) && k.expiration < wanted - 86400 && prolonged < PROLONGER_MAX) {
      prolonged += 1;
      const small = Boolean(k.metadata && k.metadata.t);
      later(env.SITE_KV.put(k.name, raw || JSON.stringify(v), small ? { expiration: wanted, metadata: v } : { expiration: wanted }).catch(() => {}));
    }
  }
  const body = { ok: true, conservation_jours: RETENTION_JOURS, visits: out, cursor: list.list_complete ? null : list.cursor || null };
  if (!cursor) {
    // Première tranche seulement : les totaux et les relevés d'archive.
    Object.assign(body, await dayStats(env));
    body.archives = await archives(env, later);
  }
  await Promise.all(jobs);
  return json(body, 200, h);
}


// ---------- Conversations avec JARVIS (la bulle du site) ----------
// Demande de James (18 novembre 2026) : voir ce que les visiteurs demandent à JARVIS. La bulle envoie
// une copie de chaque échange terminé (POST /chat/log). Gardé 24 mois comme le journal, lu seulement
// avec le jeton (GET /chats), dans la page privée /admin/visites/ (section Conversations). Contient
// l'adresse IP, comme le journal, pour relier une conversation à un visiteur. Annoncé sous la bulle
// et dans /confidentialite/ (Loi 25).
//   chat:<horodatage inversé>:<8 car.>   un échange (question, réponse, conversation, page)
const CHAT_MAX = { q: 2000, r: 8000, s: 40, page: 200 };
const CHAT_MAX_PAR_JOUR = 300;    // filet du quota KV (1 écriture par échange)
const chatJour = { d: "", n: 0 };  // compteur en mémoire de l'instance (approximatif, sans écriture)

async function chatLog(request, env, h, ctx) {
  const data = await readBody(request);
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const ua = request.headers.get("User-Agent") || "";
  const now = Date.now();
  if (!fromSite(request, env) || isRobot(ua) || tooMany("chat:" + ip, now)) return json({ ok: true }, 200, h);
  const jour = dayOf(now);
  if (chatJour.d !== jour) { chatJour.d = jour; chatJour.n = 0; }
  if (++chatJour.n > CHAT_MAX_PAR_JOUR) return json({ ok: true }, 200, h);
  const q = clean(data.q, CHAT_MAX.q), r = clean(data.r, CHAT_MAX.r);
  if (!q) return json({ ok: true }, 200, h);
  // La bulle envoie la question dès qu'elle part (r vide : en attente), puis la même entrée avec la
  // réponse : même identifiant (i) et même heure de départ (t0), donc la même clé, réécrite.
  const t0 = Number(data.t0);
  const depart = Number.isFinite(t0) && Math.abs(now - t0) < 3 * 3600000 ? Math.floor(t0) : now;
  const id = /^[a-z0-9]{8}$/i.test(String(data.i || "")) ? String(data.i) : crypto.randomUUID().slice(0, 8);
  const cf = request.cf || {};
  const echange = {
    t: new Date(depart).toISOString(),
    s: clean(data.s, CHAT_MAX.s).replace(/[^a-z0-9-]/gi, ""),   // conversation (onglet), au hasard
    q, r,
    page: cleanPath(data.page),
    lang: data.lang === "en" ? "en" : "fr",
    pays: clean(cf.country, 2).toUpperCase(),
    region: clean(cf.region, 80),
    ville: clean(cf.city, 80),
    fournisseur: clean(cf.asOrganization, 100),
    ip: clean(ip, 45),
    ...device(ua),
  };
  const key = "chat:" + String(KEY_MAX - depart).padStart(13, "0") + ":" + id;
  const jobs = [];
  defer(ctx, jobs)(env.SITE_KV.put(key, JSON.stringify(echange), { expirationTtl: VISIT_TTL }).catch(() => {}));
  await Promise.all(jobs);
  return json({ ok: true }, 200, h);
}

async function chats(request, env, h) {
  if (!authorized(request, env)) return json({ ok: false }, 401, h);
  const url = new URL(request.url);
  const limit = Math.min(500, Math.max(1, parseInt(url.searchParams.get("limit") || "200", 10) || 200));
  const list = await env.SITE_KV.list({ prefix: "chat:", limit, cursor: url.searchParams.get("cursor") || undefined });
  const out = [];
  for (const k of list.keys) {
    const v = await env.SITE_KV.get(k.name);
    if (v) { try { out.push(JSON.parse(v)); } catch { /* entrée abîmée : ignorée */ } }
  }
  return json({ ok: true, echanges: out, cursor: list.list_complete ? null : list.cursor }, 200, h);
}

async function leads(request, env, h) {
  if (!authorized(request, env)) return json({ ok: false }, 401, h);
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
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const h = cors(request.headers.get("Origin") || "", env);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
    try {
      if (url.pathname === "/contact" && request.method === "POST") return await contact(request, env, h);
      if (url.pathname === "/visits" && request.method === "GET") return await visits(env, h);
      if (url.pathname === "/visits/hit" && request.method === "POST") return await hit(request, env, h, ctx);
      if (url.pathname === "/visits/view" && request.method === "POST") return await view(request, env, h, ctx);
      if (url.pathname === "/visits/log" && request.method === "GET") return await visitLog(request, env, h, ctx);
      if (url.pathname === "/leads" && request.method === "GET") return await leads(request, env, h);
      if (url.pathname === "/chat/log" && request.method === "POST") return await chatLog(request, env, h, ctx);
      if (url.pathname === "/chats" && request.method === "GET") return await chats(request, env, h);
      if (url.pathname === "/live" && request.method === "GET") return await live(request, env, h);
      if (url.pathname === "/history" && request.method === "GET") return await history(request, env, h);
      return json({ ok: true, service: "jameslaplume.ca" }, 200, h);
    } catch (e) {
      return json({ ok: false, message: "Erreur du service." }, 500, h);
    }
  },
};
