// Test local des conversations avec JARVIS : fausse KV en mémoire, aucun réseau.
// Lancer : node integrations/site-api/test/conversations.mjs
// Adresses IP de documentation seulement (203.0.113.x), jamais de vraies.
import assert from "node:assert/strict";
const W = (await import(new URL("../src/index.js", import.meta.url))).default;
const store = new Map();
const KV = {
  async get(k) { return store.has(k) ? store.get(k).v : null; },
  async put(k, v, o = {}) { store.set(k, { v, ttl: o.expirationTtl }); },
  async delete(k) { store.delete(k); },
  async list({ prefix, limit = 1000 }) {
    const keys = [...store.keys()].filter((k) => k.startsWith(prefix)).sort().slice(0, limit).map((name) => ({ name }));
    return { keys, list_complete: true };
  },
};
const env = { SITE_KV: KV, LEADS_TOKEN: "jeton-de-test", ALLOWED_ORIGINS: "https://jarvisprivatesystems.com,http://localhost:4173" };
const waits = [];
const ctx = { waitUntil: (p) => waits.push(p) };
const MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15";
function req(path, method, body, headers = {}) {
  const r = new Request("https://api.test" + path, { method, body, headers: { "CF-Connecting-IP": "203.0.113.9",
    "Origin": "https://jarvisprivatesystems.com", "User-Agent": MAC, "Content-Type": "application/json", ...headers } });
  Object.defineProperty(r, "cf", { value: { country: "CA", region: "Quebec", city: "Exempleville" } });
  return r;
}
const call = async (r) => { const res = await W.fetch(r, env, ctx); await Promise.all(waits); return res; };
const envoi = (o, h) => call(req("/chat/log", "POST", JSON.stringify(o), h));
const chats = (h = { Authorization: "Bearer jeton-de-test" }) => call(req("/chats", "GET", undefined, h));

// 1. Un échange venant du site est gardé 24 mois, avec l'adresse (comme le journal des visites).
assert.equal((await envoi({ s: "abc-123", q: "Combien coûte un Hub?", r: "Sur soumission.", page: "/offre/?x=1", lang: "fr" })).status, 200);
const cles = [...store.keys()].filter((k) => k.startsWith("chat:"));
assert.equal(cles.length, 1);
const e = JSON.parse(store.get(cles[0]).v);
assert.equal(e.q, "Combien coûte un Hub?");
assert.equal(e.r, "Sur soumission.");
assert.equal(e.s, "abc-123");
assert.equal(e.page, "/offre/");                       // chemin seulement, sans paramètres
assert.equal(e.ville, "Exempleville");
assert.equal(e.ip, "203.0.113.9");
assert.equal(store.get(cles[0]).ttl, 730 * 24 * 3600);

// 2. Rien d'écrit : autre origine, robot, question vide.
await envoi({ q: "x", r: "y" }, { Origin: "https://ailleurs.example" });
await envoi({ q: "x", r: "y" }, { "User-Agent": "curl/8.0" });
await envoi({ q: "", r: "y" });
assert.equal([...store.keys()].filter((k) => k.startsWith("chat:")).length, 1);

// 3. Lecture : seulement avec le jeton.
assert.equal((await chats({})).status, 401);
assert.equal((await chats({ Authorization: "Bearer mauvais" })).status, 401);
const lu = await (await chats()).json();
assert.equal(lu.ok, true);
assert.equal(lu.echanges.length, 1);
assert.equal(lu.echanges[0].q, "Combien coûte un Hub?");

// 4. Les textes trop longs sont coupés.
await envoi({ s: "long", q: "q".repeat(5000), r: "r".repeat(20000) });
const long = (await (await chats()).json()).echanges.find((x) => x.s === "long");
assert.equal(long.q.length, 2000);
assert.equal(long.r.length, 8000);

console.log("Conversations : tout est correct.");
