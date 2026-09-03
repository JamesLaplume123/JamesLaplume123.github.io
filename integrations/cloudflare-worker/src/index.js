const STATUS_KEY = "battery-status";
const MAX_BATTERY_COUNT = 4;

const DEFAULT_ALLOWED_ORIGINS = [
  "https://jameslaplume.ca",
  "https://www.jameslaplume.ca",
];

const numberFields = [
  "soc",
  "capacityAh",
  "remainingAh",
  "voltage",
  "current",
  "power",
  "temperature",
  "energy",
  "highestCell",
  "lowestCell",
  "cellDelta",
  "cycles",
];

const booleanFields = [
  "connected",
  "balancing",
  "chargingAllowed",
  "dischargingAllowed",
  "alarm",
];

function allowedOrigins(env) {
  return String(env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean)
    .concat(DEFAULT_ALLOWED_ORIGINS);
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin");
  const allowed = [...new Set(allowedOrigins(env))];
  const selectedOrigin = origin && allowed.includes(origin) ? origin : allowed[0];

  return {
    "Access-Control-Allow-Origin": selectedOrigin,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "authorization, content-type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function jsonResponse(request, env, body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders(request, env),
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store, max-age=0",
      ...extraHeaders,
    },
  });
}

function cleanString(value, fallback = "") {
  return String(value ?? fallback)
    .replace(/[\u0000-\u001F\u007F]/g, "")
    .trim()
    .slice(0, 120);
}

function finiteNumber(value, fallback = null) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : fallback;
}

function clamp(value, min, max, fallback = null) {
  const numeric = finiteNumber(value, fallback);
  if (numeric == null) return fallback;
  return Math.min(max, Math.max(min, numeric));
}

function cleanBoolean(value) {
  return value === true || value === "true" || value === 1 || value === "1" || value === "on";
}

function sanitizeBattery(input, index) {
  const source = input && typeof input === "object" ? input : {};
  const battery = {
    name: cleanString(source.name, `BMS JBD ${index + 1}`),
    model: cleanString(source.model, "LiFePO4"),
  };

  for (const field of numberFields) {
    battery[field] = finiteNumber(source[field], null);
  }

  battery.soc = clamp(source.soc, 0, 100, battery.soc);
  battery.capacityAh = clamp(source.capacityAh, 0, 2000, battery.capacityAh);
  battery.remainingAh = clamp(source.remainingAh, 0, 2000, battery.remainingAh);
  battery.voltage = clamp(source.voltage, 0, 100, battery.voltage);
  battery.temperature = clamp(source.temperature, -60, 120, battery.temperature);
  battery.highestCell = clamp(source.highestCell, 0, 5, battery.highestCell);
  battery.lowestCell = clamp(source.lowestCell, 0, 5, battery.lowestCell);
  battery.cellDelta = clamp(source.cellDelta, 0, 5, battery.cellDelta);
  battery.cycles = clamp(source.cycles, 0, 100000, battery.cycles);

  if (battery.remainingAh == null && battery.capacityAh != null && battery.soc != null) {
    battery.remainingAh = Number((battery.capacityAh * battery.soc / 100).toFixed(2));
  }

  if (battery.power == null && battery.voltage != null && battery.current != null) {
    battery.power = Number((battery.voltage * battery.current).toFixed(2));
  }

  if (battery.energy == null && battery.remainingAh != null && battery.voltage != null) {
    battery.energy = Number((battery.remainingAh * battery.voltage).toFixed(2));
  }

  if (battery.cellDelta == null && battery.highestCell != null && battery.lowestCell != null) {
    battery.cellDelta = Number(Math.abs(battery.highestCell - battery.lowestCell).toFixed(3));
  }

  for (const field of booleanFields) {
    battery[field] = cleanBoolean(source[field]);
  }

  return battery;
}

function sanitizePayload(payload) {
  if (!payload || typeof payload !== "object" || !Array.isArray(payload.batteries)) {
    throw new Error("Invalid telemetry payload");
  }

  const batteries = payload.batteries
    .slice(0, MAX_BATTERY_COUNT)
    .map((battery, index) => sanitizeBattery(battery, index));

  if (!batteries.length) throw new Error("Telemetry payload has no batteries");

  return {
    updatedAt: new Date().toISOString(),
    sourceUpdatedAt: cleanString(payload.updatedAt, ""),
    gateway: cleanString(payload.gateway, "Home Assistant OS · lecture publique"),
    privacy: "public-readonly",
    batteries,
  };
}

function hasWriteAccess(request, env) {
  const expected = env.WRITE_TOKEN;
  const authorization = request.headers.get("Authorization") || "";
  return Boolean(expected && authorization === `Bearer ${expected}`);
}

async function readStatus(request, env) {
  if (!env.BATTERY_KV) {
    return jsonResponse(request, env, { error: "BATTERY_KV binding missing" }, 500);
  }

  const status = await env.BATTERY_KV.get(STATUS_KEY, "json");
  if (!status) {
    return jsonResponse(request, env, { error: "No battery telemetry published yet" }, 404);
  }

  return jsonResponse(request, env, status);
}

async function writeStatus(request, env) {
  if (!env.BATTERY_KV) {
    return jsonResponse(request, env, { error: "BATTERY_KV binding missing" }, 500);
  }

  if (!hasWriteAccess(request, env)) {
    return jsonResponse(request, env, { error: "Unauthorized" }, 401);
  }

  let status;
  try {
    status = sanitizePayload(await request.json());
  } catch (error) {
    return jsonResponse(request, env, { error: "Invalid battery telemetry payload" }, 400);
  }

  await env.BATTERY_KV.put(STATUS_KEY, JSON.stringify(status), {
    expirationTtl: 60 * 60 * 24 * 14,
  });

  return jsonResponse(request, env, { ok: true, updatedAt: status.updatedAt }, 202);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request, env) });
    }

    if (url.pathname === "/health") {
      return jsonResponse(request, env, { ok: true });
    }

    if (url.pathname === "/" || url.pathname === "/battery-status") {
      if (request.method === "GET") return readStatus(request, env);
      if (request.method === "POST") return writeStatus(request, env);
    }

    return jsonResponse(request, env, { error: "Not found" }, 404);
  },
};
