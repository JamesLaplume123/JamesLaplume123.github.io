// Test local du Worker : fausse KV en mémoire, aucun réseau. Lancer : node integrations/site-api/test/visites.mjs
import assert from "node:assert/strict";
const mod = await import(new URL("../src/index.js", import.meta.url));
const W = mod.default;
const store = new Map();
const KV = {
  async get(k) { return store.has(k) ? store.get(k).v : null; },
  async put(k, v, o = {}) { store.set(k, { v, m: o.metadata, ttl: o.expirationTtl }); },
  async list({ prefix, limit }) {
    const keys = [...store.keys()].filter((k) => k.startsWith(prefix)).sort().slice(0, limit)
      .map((name) => ({ name, metadata: store.get(name).m }));
    return { keys, list_complete: true };
  },
};
const env = { SITE_KV: KV, LEADS_TOKEN: "jeton-de-test", ALLOWED_ORIGINS: "https://jameslaplume.ca" };
const waits = [];
const ctx = { waitUntil: (p) => waits.push(p) };
function req(path, method, body, headers = {}, cf) {
  const r = new Request("https://api.test" + path, { method, body, headers: { "CF-Connecting-IP": "203.0.113.7", "Origin": "https://jameslaplume.ca",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1", ...headers } });
  Object.defineProperty(r, "cf", { value: cf || { country: "CA", region: "Quebec", city: "Saint-Hyacinthe", latitude: "45.63", longitude: "-72.95", timezone: "America/Toronto", asn: 577, asOrganization: "Bell Canada" } });
  return r;
}
let r = await W.fetch(req("/visits/hit", "POST", JSON.stringify({ path: "/solutions/?q=secret#x", ref: "https://www.google.com/search?q=james" })), env, ctx);
assert.equal((await r.json()).value, 1);
await new Promise((res) => setTimeout(res, 5));
r = await W.fetch(req("/visits/view", "POST", JSON.stringify({ path: "/contact/", ref: "" })), env, ctx);
await Promise.all(waits);
await new Promise((res) => setTimeout(res, 5));
await W.fetch(req("/visits/hit", "POST", "pas du json", { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0 Safari/537.36 Edg/130.0" }, { country: "FR", city: "Paris" }), env, ctx);
await Promise.all(waits);
assert.equal(store.get("visits").v, "2", "compteur : 2 arrivées, la vue ne compte pas");
// refus sans jeton / mauvais jeton
r = await W.fetch(req("/visits/log", "GET"), env, ctx); assert.equal(r.status, 401);
r = await W.fetch(req("/visits/log", "GET", undefined, { Authorization: "Bearer faux" }), env, ctx); assert.equal(r.status, 401);
r = await W.fetch(req("/visits/log", "GET"), { ...env, LEADS_TOKEN: "" }, ctx); assert.equal(r.status, 401);
// avec jeton
r = await W.fetch(req("/visits/log?limit=200", "GET", undefined, { Authorization: "Bearer jeton-de-test" }), env, ctx);
assert.equal(r.status, 200);
const j = await r.json();
assert.equal(j.visits.length, 3);
const [last, mid, first] = j.visits;
assert.equal(last.pays, "FR"); assert.equal(last.navigateur, "Edge"); assert.equal(last.appareil, "Ordinateur"); assert.equal(last.page, "");
assert.equal(mid.type, "page"); assert.equal(mid.page, "/contact/");
assert.equal(first.page, "/solutions/"); assert.equal(first.ref, "www.google.com");
assert.equal(first.ville, "Saint-Hyacinthe"); assert.equal(first.fournisseur, "Bell Canada"); assert.equal(first.asn, 577);
assert.equal(first.ip, "203.0.113.7"); assert.equal(first.appareil, "Mobile"); assert.equal(first.systeme, "iOS"); assert.equal(first.navigateur, "Safari");
assert.equal(first.lat, 45.63);
for (const [k, v] of store) if (k.startsWith("visit:")) assert.equal(v.ttl, 30 * 24 * 3600);
// limite par adresse : au-delà de 60 inscriptions par heure, plus rien n'est journalisé (le compteur continue)
for (let i = 0; i < 70; i++) await W.fetch(req("/visits/view", "POST", "{}"), env, ctx);
await Promise.all(waits);
const n = [...store.keys()].filter((k) => k.startsWith("visit:")).length;
assert.equal(n, 60, "plafond par adresse et par heure");
r = await W.fetch(req("/visits/log?limit=5", "GET", undefined, { Authorization: "Bearer jeton-de-test" }), env, ctx);
assert.equal((await r.json()).visits.length, 5);
// le formulaire garde sa propre limite
assert.ok(![...store.keys()].some((k) => k.startsWith("rate:")));
// préalable CORS : Authorization permis
r = await W.fetch(req("/visits/log", "OPTIONS"), env, ctx);
assert.match(r.headers.get("Access-Control-Allow-Headers"), /Authorization/);
// /leads garde le même contrôle
r = await W.fetch(req("/leads", "GET"), env, ctx); assert.equal(r.status, 401);
r = await W.fetch(req("/leads", "GET", undefined, { Authorization: "Bearer jeton-de-test" }), env, ctx); assert.equal(r.status, 200);
console.log("Tous les tests du Worker passent.");
