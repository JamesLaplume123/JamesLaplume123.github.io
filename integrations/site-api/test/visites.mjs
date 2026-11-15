// Test local du Worker : fausse KV en mémoire, aucun réseau. Lancer : node integrations/site-api/test/visites.mjs
// Les adresses IP sont des adresses de documentation (203.0.113.x, 2001:db8::), jamais de vraies.
import assert from "node:assert/strict";
const mod = await import(new URL("../src/index.js", import.meta.url));
const W = mod.default;
const store = new Map();
let writes = 0;
const KV = {
  async get(k) { return store.has(k) ? store.get(k).v : null; },
  async put(k, v, o = {}) {
    writes++;
    const expiration = o.expiration || (o.expirationTtl ? Math.floor(Date.now() / 1000) + o.expirationTtl : undefined);
    store.set(k, { v, m: o.metadata, ttl: o.expirationTtl, expiration });
  },
  async delete(k) { writes++; store.delete(k); },
  // Comme KV : ordre alphabétique des clés, tranche de « limit », curseur opaque pour la suite.
  async list({ prefix, limit = 1000, cursor }) {
    const all = [...store.keys()].filter((k) => k.startsWith(prefix)).sort();
    const from = cursor ? parseInt(Buffer.from(cursor, "base64").toString(), 10) : 0;
    const keys = all.slice(from, from + limit).map((name) => ({ name, metadata: store.get(name).m, expiration: store.get(name).expiration }));
    const done = from + limit >= all.length;
    return done ? { keys, list_complete: true } : { keys, list_complete: false, cursor: Buffer.from(String(from + limit)).toString("base64") };
  },
};
const env = { SITE_KV: KV, LEADS_TOKEN: "jeton-de-test", ALLOWED_ORIGINS: "https://jameslaplume.ca,https://www.jameslaplume.ca,http://localhost:4173" };
const waits = [];
const ctx = { waitUntil: (p) => waits.push(p) };
const IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1";
function req(path, method, body, headers = {}, cf) {
  const r = new Request("https://api.test" + path, { method, body, headers: { "CF-Connecting-IP": "203.0.113.7", "Origin": "https://jameslaplume.ca",
    "User-Agent": IPHONE, ...headers } });
  Object.defineProperty(r, "cf", { value: cf || { country: "CA", region: "Quebec", city: "Saint-Hyacinthe", latitude: "45.63", longitude: "-72.95", timezone: "America/Toronto", asn: 577, asOrganization: "Bell Canada" } });
  return r;
}
const call = async (r, e = env) => { const res = await W.fetch(r, e, ctx); await Promise.all(waits); return res; };
const AUTH = { Authorization: "Bearer jeton-de-test" };
const log = async (q = "") => (await call(req("/visits/log" + q, "GET", undefined, AUTH))).json();
const visitKeys = () => [...store.keys()].filter((k) => k.startsWith("visit:"));
const pause = () => new Promise((res) => setTimeout(res, 3));
const today = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Toronto", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());

// L'ancien compteur public (avant les compteurs par jour) sert de point de départ.
store.set("visits", { v: "57" });
let r = await call(req("/visits", "GET"));
assert.equal((await r.json()).value, 57);

// ---------- Requêtes ignorées : réponse 200, aucune écriture ----------
const HIT = JSON.stringify({ path: "/solutions/?q=secret#x", ref: "https://www.google.com/search?q=james" });
for (const [nom, headers] of [
  ["origine inconnue", { Origin: "https://ailleurs.example" }],
  ["poste local, même s'il est permis pour le formulaire", { Origin: "http://localhost:4173" }],
  ["robot", { "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" }],
  ["navigateur sans écran", { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) HeadlessChrome/130.0 Safari/537.36" }],
  ["aperçu de lien", { "User-Agent": "facebookexternalhit/1.1" }],
  ["sans User-Agent", { "User-Agent": "" }],
]) {
  for (const path of ["/visits/hit", "/visits/view"]) {
    r = await call(req(path, "POST", HIT, headers));
    assert.equal(r.status, 200, nom);
    if (path === "/visits/hit") assert.equal((await r.json()).value, 57, nom + " : le compteur ne bouge pas");
  }
}
r = await W.fetch(new Request("https://api.test/visits/hit", { method: "POST", body: HIT, headers: { "User-Agent": IPHONE } }), env, ctx); // sans Origin
assert.equal(r.status, 200);
assert.equal(writes, 0, "requêtes ignorées : aucune écriture KV");
assert.equal(visitKeys().length, 0);

// ---------- Une arrivée : 2 écritures (+ 1 fois par jour : vjour) ----------
r = await call(req("/visits/hit", "POST", HIT));
assert.equal((await r.json()).value, 58, "le compteur public continue après l'ancien");
assert.equal(writes, 3, "première arrivée du jour : visite + compteur du jour + vjour");
assert.equal(store.get("vjour").v, today);
await pause();
writes = 0;
r = await call(req("/visits/view", "POST", JSON.stringify({ path: "/contact/", ref: "" })));
assert.equal(writes, 2, "page suivante : visite + compteur du jour");
await pause();
writes = 0;
r = await call(req("/visits/hit", "POST", "pas du json", { Origin: "https://www.jameslaplume.ca", "CF-Connecting-IP": "2001:db8::42",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0 Safari/537.36 Edg/130.0" }, { country: "FR", city: "Paris" }));
assert.equal((await r.json()).value, 59);
assert.equal(writes, 2, "arrivée : visite + compteur du jour");
assert.equal(store.get("visits").v, "57", "l'ancienne clé n'est plus écrite");
assert.deepEqual(JSON.parse(store.get("vstat:" + today).v), { visites: 2, pages: 3, total: 59, pagesTotal: 3 });
r = await call(req("/visits", "GET"));
assert.equal((await r.json()).value, 59);

// ---------- Refus sans jeton / mauvais jeton ----------
r = await call(req("/visits/log", "GET")); assert.equal(r.status, 401);
r = await call(req("/visits/log", "GET", undefined, { Authorization: "Bearer faux" })); assert.equal(r.status, 401);
r = await call(req("/visits/log", "GET"), { ...env, LEADS_TOKEN: "" }); assert.equal(r.status, 401);
r = await call(req("/visits/log", "GET", undefined, { Authorization: "Bearer " }), { ...env, LEADS_TOKEN: "" }); assert.equal(r.status, 401);

// ---------- Avec jeton ----------
let j = await log("?limit=200");
assert.equal(j.conservation_jours, 730);
assert.equal(j.visits.length, 3);
assert.equal(j.cursor, null);
const [last, mid, first] = j.visits;
assert.equal(last.pays, "FR"); assert.equal(last.navigateur, "Edge"); assert.equal(last.appareil, "Ordinateur"); assert.equal(last.page, "");
assert.equal(last.ip, "2001:db8::42");
assert.equal(mid.type, "page"); assert.equal(mid.page, "/contact/");
assert.equal(first.page, "/solutions/"); assert.equal(first.ref, "www.google.com");
assert.equal(first.ville, "Saint-Hyacinthe"); assert.equal(first.fournisseur, "Bell Canada"); assert.equal(first.asn, 577);
assert.equal(first.ip, "203.0.113.7"); assert.equal(first.appareil, "Mobile"); assert.equal(first.systeme, "iOS"); assert.equal(first.navigateur, "Safari");
assert.equal(first.lat, 45.63);
// Durée : 24 mois
for (const k of visitKeys()) assert.equal(store.get(k).ttl, 730 * 24 * 3600, "chaque visite est gardée 24 mois");
// Compteurs par jour et totaux
assert.deepEqual(j.jours, [{ jour: today, visites: 2, pages: 3 }]);
assert.deepEqual(j.totaux, { visites: 59, pages: 3 });
assert.deepEqual(j.archives, []);
// Les limites de taille restent
r = await call(req("/visits/view", "POST", JSON.stringify({ path: "/" + "a".repeat(900), ref: "https://" + "b".repeat(300) + ".example/" }),
  { "CF-Connecting-IP": "203.0.113.9" }, { country: "CANADA", city: "v".repeat(300), asOrganization: "f".repeat(300) }));
j = await log();
assert.equal(j.visits[0].page.length, 200); assert.equal(j.visits[0].ref, ""); assert.equal(j.visits[0].pays, "CA");
assert.equal(j.visits[0].ville.length, 80); assert.equal(j.visits[0].fournisseur.length, 100);

// ---------- Compteurs des jours passés, année précédente comprise ----------
const stat = (d, visites, pages) => store.set("vstat:" + d, { v: JSON.stringify({ visites, pages, total: 0, pagesTotal: 0 }), m: { visites, pages, total: 0, pagesTotal: 0 } });
const Y = +today.slice(0, 4), avant = (Y - 1) + "-12-31", debut = Y + "-01-01";
stat(avant, 4, 9); if (debut !== today) stat(debut, 1, 2);
store.set("vstat:" + (Y - 2) + "-06-01", { v: "{}" }); // deux années plus tôt : hors des listes
j = await log();
assert.deepEqual(j.jours.map((d) => d.jour), [...new Set([avant, debut, today])].sort());
assert.deepEqual(j.jours[0], { jour: avant, visites: 4, pages: 9 });
for (let i = 0; i < 420; i++) stat((Y - 1) + "-" + String(1 + Math.floor(i / 28)).padStart(2, "0") + "-" + String(1 + (i % 28)).padStart(2, "0"), 1, 1);
j = await log();
assert.equal(j.jours.length, 400, "au plus 400 jours de compteurs");
assert.equal(j.jours[399].jour, today);
for (const k of [...store.keys()]) if (k.startsWith("vstat:") && k !== "vstat:" + today) store.delete(k);

// ---------- Plafond par adresse et par heure : en mémoire, sans écriture ----------
for (let i = 0; i < 70; i++) await W.fetch(req("/visits/view", "POST", "{}", { "CF-Connecting-IP": "203.0.113.60" }), env, ctx);
await Promise.all(waits);
assert.equal(visitKeys().length, 4 + 60, "plafond par adresse et par heure");
assert.ok(![...store.keys()].some((k) => k.startsWith("vrate:") || k.startsWith("rate:")), "aucune clé de limite pour le journal");

// ---------- Pagination : les plus récentes d'abord, sans doublon ni trou ----------
// 450 visites datées, écrites comme le fait le Worker (horodatage inversé).
for (const k of visitKeys()) store.delete(k);
const base = Date.parse("2026-11-10T12:00:00Z");
for (let i = 0; i < 450; i++) {
  const t = base + i * 60000;
  const v = { t: new Date(t).toISOString(), type: "arrivee", page: "/p" + i, ip: "203.0.113." + (i % 250), appareil: "Mobile" };
  store.set("visit:" + String(9999999999999 - t).padStart(13, "0") + ":" + String(i).padStart(8, "0"), { v: JSON.stringify(v), m: i % 7 ? v : undefined });
}
const p1 = await log();
assert.equal(p1.visits.length, 200, "200 par défaut");
assert.ok(p1.cursor, "un curseur pour la suite");
assert.equal(p1.visits[0].page, "/p449", "la plus récente d'abord");
assert.ok(Array.isArray(p1.jours) && Array.isArray(p1.archives));
const p2 = await log("?cursor=" + encodeURIComponent(p1.cursor));
assert.equal(p2.visits.length, 200);
assert.equal(p2.jours, undefined, "les totaux ne voyagent qu'avec la première tranche");
assert.equal(p2.archives, undefined);
const p3 = await log("?cursor=" + encodeURIComponent(p2.cursor));
assert.equal(p3.visits.length, 50); assert.equal(p3.cursor, null);
const pages = [...p1.visits, ...p2.visits, ...p3.visits].map((v) => v.page);
assert.deepEqual(pages, Array.from({ length: 450 }, (_, i) => "/p" + (449 - i)));
assert.equal((await log("?limit=5")).visits.length, 5);
assert.equal((await log("?limit=9999")).visits.length, 450);
for (let i = 450; i < 520; i++) store.set("visit:" + String(9999999999999 - base - i * 60000).padStart(13, "0") + ":x", { v: JSON.stringify({ t: new Date(base + i * 60000).toISOString() }) });
assert.equal((await log("?limit=9999")).visits.length, 500, "500 au plus par tranche");
assert.equal((await log("?limit=abc")).visits.length, 200);

// ---------- Visites de l'ancien régime (30 jours) : prolongées à 24 mois après la visite ----------
for (const k of visitKeys()) store.delete(k);
const t0 = Date.now() - 5 * 86400000;
for (let i = 0; i < 30; i++) {
  const t = t0 + i * 1000, v = { t: new Date(t).toISOString(), type: "arrivee", page: "/vieux" + i };
  store.set("visit:" + String(9999999999999 - t).padStart(13, "0") + ":" + i, { v: JSON.stringify(v), m: v, expiration: Math.floor(t / 1000) + 30 * 86400 });
}
writes = 0;
await log();
assert.equal(writes, 20, "au plus 20 prolongations par lecture");
await log();
assert.equal(writes, 30, "le reste à la lecture suivante");
await log();
assert.equal(writes, 30, "ensuite la lecture n'écrit plus rien");
for (const k of visitKeys()) {
  const e = store.get(k);
  assert.equal(e.expiration, Math.floor(Date.parse(e.m.t) / 1000) + 730 * 86400);
  assert.ok(JSON.parse(e.v).page.startsWith("/vieux"), "le contenu est intact");
}

// ---------- Archives : relevés d'avant la mise en service ----------
const releve = { periode: "du 8 au 15 novembre 2026", note: "Appels au service, pas des visites.",
  lignes: [{ pays: "CA", region: "QC", ville: "Saint-Hyacinthe", fournisseur: "Fournisseur d'essai", ip: "203.0.113.20", appels: 12 },
    { pays: "US", ville: "Columbus", fournisseur: "Robot d'essai", ip: "2001:db8::1", appels: 40, robot: true }] };
store.set("archive:2026-11-08", { v: JSON.stringify(releve) });
store.set("archive:abime", { v: "pas du json" });
store.set("archive:2020-01-01", { v: JSON.stringify({ lignes: [] }) }); // plus vieux que 24 mois : effacé, jamais servi
j = await log();
assert.deepEqual(j.archives, [{ cle: "archive:2026-11-08", contenu: releve }]);
assert.ok(!store.has("archive:2020-01-01"), "un relevé de plus de 24 mois est effacé");
r = await call(req("/visits/log", "GET")); assert.equal(r.status, 401, "les archives restent derrière le jeton");

// ---------- Plafond du jour : le quota KV reste pour le formulaire ----------
store.set("vstat:" + today, { v: JSON.stringify({ visites: 100, pages: 450, total: 900, pagesTotal: 2000 }) });
writes = 0;
r = await call(req("/visits/hit", "POST", HIT, { "CF-Connecting-IP": "203.0.113.99" }));
assert.equal((await r.json()).value, 900);
assert.equal(writes, 0, "plafond du jour atteint : plus aucune écriture");

// ---------- Le reste du service ----------
r = await call(req("/visits/log", "OPTIONS"));
assert.match(r.headers.get("Access-Control-Allow-Headers"), /Authorization/);
r = await call(req("/leads", "GET")); assert.equal(r.status, 401);
r = await call(req("/leads", "GET", undefined, AUTH)); assert.equal(r.status, 200);
console.log("Tous les tests du Worker passent.");
