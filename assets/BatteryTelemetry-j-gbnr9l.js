import { r as reactInterop } from "./rolldown-runtime-S-ySWqyJ.js";
import { a as loadReact, i as loadJsxRuntime } from "./framework-BHiRoOKJ.js";

const React = reactInterop(loadReact(), 1);
const jsxRuntime = loadJsxRuntime();

const CONFIG_URL = "/data/battery-public-config.json";
const DEFAULT_CONFIG = {
  batteryStatusUrl: "",
  batteryGistApiUrl: "",
  batteryGistFile: "battery-status.json",
  batteryFallbackUrl: "/data/battery-status.json",
  batteryPollMs: 30000,
  batteryStaleAfterMs: 300000,
};
const STATUS_STYLE_ID = "battery-feed-state-styles";

async function fetchJson(url) {
  const response = await fetch(url, {
    cache: "no-store",
    headers: { accept: "application/json" },
  });

  if (!response.ok) throw new Error("battery telemetry unavailable");
  return response.json();
}

async function loadPublicConfig() {
  try {
    return { ...DEFAULT_CONFIG, ...(await fetchJson(CONFIG_URL)) };
  } catch {
    return { ...DEFAULT_CONFIG };
  }
}

function validateStatus(status) {
  if (!status || !Array.isArray(status.batteries) || status.batteries.length === 0) {
    throw new Error("battery telemetry is empty");
  }

  return status;
}

async function loadGistStatus(config) {
  const gist = await fetchJson(config.batteryGistApiUrl);
  const content = gist.files?.[config.batteryGistFile]?.content;
  if (!content) throw new Error("battery telemetry gist file unavailable");
  return validateStatus(JSON.parse(content));
}

async function loadBatteryStatus(config) {
  const sources = [
    config.batteryStatusUrl ? () => fetchJson(config.batteryStatusUrl).then(validateStatus) : null,
    config.batteryGistApiUrl ? () => loadGistStatus(config) : null,
    config.batteryFallbackUrl ? () => fetchJson(config.batteryFallbackUrl).then(validateStatus) : null,
  ].filter(Boolean);

  for (const load of sources) {
    try {
      return await load();
    } catch {
      // Try the next safe public source.
    }
  }

  throw new Error("battery telemetry unavailable");
}

function formatMetric(locale, value, unit, fallback) {
  const numeric = Number(value);
  return value == null || !Number.isFinite(numeric)
    ? fallback
    : `${numeric.toLocaleString(locale, { maximumFractionDigits: 3 })} ${unit}`;
}

function formatEnergy(locale, value, fallback) {
  const numeric = Number(value);
  return value == null || !Number.isFinite(numeric)
    ? fallback
    : `${(numeric / 1000).toLocaleString(locale, { maximumFractionDigits: 2 })} kWh`;
}

function formatCells(locale, battery, fallback) {
  if (battery.lowestCell == null || battery.highestCell == null) {
    const delta = Number(battery.cellDelta);
    return Number.isFinite(delta) ? `${Math.round(delta * 1000)} mV` : fallback;
  }

  return `${Number(battery.lowestCell).toLocaleString(locale, { maximumFractionDigits: 3 })}–${Number(battery.highestCell).toLocaleString(locale, { maximumFractionDigits: 3 })} V`;
}

function batteryState(battery, copy) {
  if (battery.alarm) return [copy.alarmState, "alarm"];
  if (Math.abs(Number(battery.current || 0)) > 0.25) {
    return Number(battery.current) > 0 ? [copy.charging, "charging"] : [copy.inService, "charging"];
  }
  return battery.connected ? [copy.online, "online"] : [copy.detected, ""];
}

function ensureStatusStyles() {
  if (document.getElementById(STATUS_STYLE_ID)) return;

  const style = document.createElement("style");
  style.id = STATUS_STYLE_ID;
  style.textContent = ".battery-feed-stale .battery-system-identity>i{background:#ffb86b;box-shadow:0 0 0 .38rem rgba(255,184,107,.1),0 0 1.2rem rgba(255,184,107,.75)}.battery-feed-stale .battery-system-bar>strong{color:#ffcf9c}.battery-feed-error .battery-system-identity>i{background:#ff6f6f;box-shadow:0 0 0 .38rem rgba(255,111,111,.1),0 0 1.2rem rgba(255,111,111,.75)}.battery-feed-error .battery-system-bar>strong{color:#ff9b9b}";
  document.head.appendChild(style);
}

function batteryCopy(locale, variant) {
  const isFrench = locale === "fr";

  return {
    kicker: isFrench ? "Preuve opérationnelle" : "Operational proof",
    heading: isFrench ? "Capacité énergétique en direct." : "Live energy capacity.",
    intro: variant === "ambulance"
      ? isFrench
        ? "Le système énergétique de l'Ambulance Lab publie maintenant une vue sécurisée et en lecture seule des deux batteries LiFePO₄."
        : "The Ambulance Lab energy system now publishes a safe, read-only view of both LiFePO₄ batteries."
      : isFrench
        ? "Deux batteries LiFePO₄ et leurs BMS JBD sont suivis en direct par la passerelle Bluetooth Waveshare."
        : "Two LiFePO₄ batteries and their JBD BMS units are monitored live through the Waveshare Bluetooth gateway.",
    gateway: isFrench ? "Waveshare ESP32 · Bluetooth connecté" : "Waveshare ESP32 · Bluetooth connected",
    initializing: isFrench ? "Télémétrie en initialisation" : "Telemetry initializing",
    calculating: isFrench ? "Calcul de la capacité disponible…" : "Calculating available capacity…",
    privacy: isFrench
      ? "Capacité, mesures électriques, température, santé des cellules et permissions BMS seulement. Aucun jeton Home Assistant, adresse privée, contrôle ou identifiant Bluetooth n'est publié."
      : "Capacity, electrical measurements, temperature, cell health and BMS permissions only. No Home Assistant token, private address, control or Bluetooth identifier is published.",
    waiting: isFrench ? "En attente" : "Pending",
    updated: isFrench ? "Dernière lecture" : "Last reading",
    available: isFrench ? "disponibles" : "available",
    battery: isFrench ? "Batterie" : "Battery",
    capacity: isFrench ? "Capacité disponible" : "Available capacity",
    nominal: isFrench ? "nominaux" : "nominal",
    voltage: isFrench ? "Tension" : "Voltage",
    current: isFrench ? "Courant" : "Current",
    power: isFrench ? "Puissance" : "Power",
    temperature: isFrench ? "Température" : "Temperature",
    energy: isFrench ? "Énergie stockée" : "Stored energy",
    cells: isFrench ? "Plage des cellules" : "Cell range",
    balancing: isFrench ? "Équilibrage actif" : "Balancing active",
    stable: isFrench ? "Cellules stables" : "Cells stable",
    chargeAllowed: isFrench ? "Recharge autorisée" : "Charge enabled",
    chargeProtected: isFrench ? "Recharge protégée" : "Charge protected",
    dischargeAllowed: isFrench ? "Décharge autorisée" : "Discharge enabled",
    dischargeProtected: isFrench ? "Décharge protégée" : "Discharge protected",
    cycle: "cycle",
    cycles: "cycles",
    alarm: isFrench ? "alerte BMS" : "BMS alert",
    alarms: isFrench ? "alertes BMS" : "BMS alerts",
    healthy: isFrench ? "BMS sains" : "BMS healthy",
    online: isFrench ? "En ligne" : "Online",
    detected: isFrench ? "Détectée" : "Detected",
    charging: isFrench ? "En charge" : "Charging",
    inService: isFrench ? "En service" : "In service",
    alarmState: isFrench ? "Alerte BMS" : "BMS alert",
    stale: isFrench ? "flux plus vieux que prévu" : "feed older than expected",
    offline: isFrench ? "Flux public hors ligne" : "Public feed offline",
    error: isFrench
      ? "Les batteries sont détectées; la télémétrie publique est temporairement indisponible."
      : "The batteries are detected; the public telemetry feed is temporarily unavailable.",
  };
}

function BatteryTelemetry({ locale, variant }) {
  const copy = batteryCopy(locale, variant);
  const browserLocale = locale === "fr" ? "fr-CA" : "en-CA";
  const [status, setStatus] = React.useState(null);
  const [config, setConfig] = React.useState(DEFAULT_CONFIG);
  const [failed, setFailed] = React.useState(false);
  const hasRenderedStatus = React.useRef(false);

  React.useEffect(() => {
    let active = true;
    let timer = null;
    ensureStatusStyles();

    const refresh = async (knownConfig = null) => {
      if (document.hidden) return;

      try {
        const nextConfig = knownConfig || await loadPublicConfig();
        const nextStatus = await loadBatteryStatus(nextConfig);
        if (!active) return;
        hasRenderedStatus.current = true;
        setConfig(nextConfig);
        setStatus(nextStatus);
        setFailed(false);
      } catch {
        if (active && !hasRenderedStatus.current) setFailed(true);
      }
    };

    const start = async () => {
      const nextConfig = await loadPublicConfig();
      if (!active) return;
      setConfig(nextConfig);
      await refresh(nextConfig);
      const pollMs = Math.max(10000, Number(nextConfig.batteryPollMs || DEFAULT_CONFIG.batteryPollMs));
      timer = window.setInterval(refresh, pollMs);
    };

    const onVisibilityChange = () => {
      if (!document.hidden) refresh();
    };

    start();
    document.addEventListener("visibilitychange", onVisibilityChange);

    return () => {
      active = false;
      if (timer) window.clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, []);

  const batteries = status?.batteries || [];
  const totalAh = status ? batteries.reduce((total, battery) => total + Number(battery.remainingAh || 0), 0) : null;
  const totalEnergy = status ? batteries.reduce((total, battery) => total + Number(battery.energy || 0), 0) : null;
  const totalCurrent = status ? batteries.reduce((total, battery) => total + Number(battery.current || 0), 0) : null;
  const alarmCount = status ? batteries.filter((battery) => battery.alarm).length : 0;
  const updatedDate = status?.updatedAt ? new Date(status.updatedAt) : null;
  const updatedIsValid = Boolean(updatedDate && !Number.isNaN(updatedDate.getTime()));
  const isStale = Boolean(updatedIsValid && Date.now() - updatedDate.getTime() > Number(config.batteryStaleAfterMs || DEFAULT_CONFIG.batteryStaleAfterMs));
  const sectionClass = [
    "battery-live-section",
    isStale ? "battery-feed-stale" : "",
    failed && !status ? "battery-feed-error" : "",
  ].filter(Boolean).join(" ");
  const heading = status
    ? `${formatMetric(browserLocale, totalAh, "Ah", copy.waiting)} ${locale === "fr" ? "sous surveillance." : "under supervision."}`
    : copy.heading;
  const summary = status
    ? `${formatMetric(browserLocale, totalAh, "Ah", copy.waiting)} ${copy.available} · ${formatEnergy(browserLocale, totalEnergy, copy.waiting)} · ${totalCurrent > 0 ? "+" : ""}${formatMetric(browserLocale, totalCurrent, "A", copy.waiting)} · ${alarmCount ? `${alarmCount} ${alarmCount === 1 ? copy.alarm : copy.alarms}` : copy.healthy}`
    : copy.calculating;
  const updatedLabel = updatedIsValid
    ? `${copy.updated}: ${updatedDate.toLocaleString(browserLocale)}${isStale ? ` · ${copy.stale}` : ""}`
    : failed ? copy.error : copy.initializing;

  return (0, jsxRuntime.jsxs)("section", {
    className: sectionClass,
    id: "batteries",
    children: [
      (0, jsxRuntime.jsxs)("div", {
        className: "battery-live-heading",
        children: [
          (0, jsxRuntime.jsx)("p", { className: "section-label", children: copy.kicker }),
          (0, jsxRuntime.jsx)("h2", { children: heading }),
          (0, jsxRuntime.jsx)("p", { children: copy.intro }),
        ],
      }),
      (0, jsxRuntime.jsxs)("div", {
        className: "battery-system-bar",
        children: [
          (0, jsxRuntime.jsxs)("div", {
            className: "battery-system-identity",
            children: [
              (0, jsxRuntime.jsx)("i", { "aria-hidden": "true" }),
              (0, jsxRuntime.jsxs)("span", {
                children: [
                  (0, jsxRuntime.jsx)("b", { children: failed && !status ? copy.offline : status?.gateway ?? copy.gateway }),
                  (0, jsxRuntime.jsx)("small", { children: updatedLabel }),
                ],
              }),
            ],
          }),
          (0, jsxRuntime.jsx)("strong", { children: summary }),
        ],
      }),
      (0, jsxRuntime.jsxs)("div", {
        className: "battery-live-grid",
        "aria-live": "polite",
        children: [
          failed && !status && (0, jsxRuntime.jsx)("p", { className: "battery-live-error", children: copy.error }),
          batteries.map((battery, index) => {
            const [stateLabel, stateClass] = batteryState(battery, copy);
            const cycleLabel = battery.cycles === 1 ? copy.cycle : copy.cycles;
            const soc = Math.max(0, Math.min(100, Number(battery.soc || 0)));

            return (0, jsxRuntime.jsxs)("article", {
              className: `battery-live-card ${battery.alarm ? "has-alarm" : ""}`,
              children: [
                (0, jsxRuntime.jsxs)("header", {
                  children: [
                    (0, jsxRuntime.jsxs)("div", {
                      children: [
                        (0, jsxRuntime.jsxs)("span", { children: [copy.battery, " 0", index + 1] }),
                        (0, jsxRuntime.jsx)("h3", { children: battery.name }),
                      ],
                    }),
                    (0, jsxRuntime.jsx)("em", { className: `battery-state ${stateClass}`, children: stateLabel }),
                  ],
                }),
                (0, jsxRuntime.jsxs)("div", {
                  className: "battery-primary",
                  children: [
                    (0, jsxRuntime.jsxs)("div", {
                      className: "battery-soc",
                      style: { "--soc": `${soc}%` },
                      children: [
                        (0, jsxRuntime.jsx)("strong", { children: formatMetric(browserLocale, battery.soc, "%", copy.waiting) }),
                        (0, jsxRuntime.jsx)("span", { children: (0, jsxRuntime.jsx)("i", {}) }),
                      ],
                    }),
                    (0, jsxRuntime.jsxs)("div", {
                      className: "battery-ah",
                      children: [
                        (0, jsxRuntime.jsx)("span", { children: copy.capacity }),
                        (0, jsxRuntime.jsx)("strong", { children: formatMetric(browserLocale, battery.remainingAh, "Ah", copy.waiting) }),
                        (0, jsxRuntime.jsxs)("small", {
                          children: [locale === "fr" ? "sur" : "of", " ", formatMetric(browserLocale, battery.capacityAh, "Ah", copy.waiting), " ", copy.nominal],
                        }),
                      ],
                    }),
                  ],
                }),
                (0, jsxRuntime.jsxs)("dl", {
                  className: "battery-metrics",
                  children: [
                    (0, jsxRuntime.jsxs)("div", { children: [(0, jsxRuntime.jsx)("dt", { children: copy.voltage }), (0, jsxRuntime.jsx)("dd", { children: formatMetric(browserLocale, battery.voltage, "V", copy.waiting) })] }),
                    (0, jsxRuntime.jsxs)("div", { children: [(0, jsxRuntime.jsx)("dt", { children: copy.current }), (0, jsxRuntime.jsxs)("dd", { children: [Number(battery.current || 0) > 0 ? "+" : "", formatMetric(browserLocale, battery.current, "A", copy.waiting)] })] }),
                    (0, jsxRuntime.jsxs)("div", { children: [(0, jsxRuntime.jsx)("dt", { children: copy.power }), (0, jsxRuntime.jsx)("dd", { children: formatMetric(browserLocale, battery.power, "W", copy.waiting) })] }),
                    (0, jsxRuntime.jsxs)("div", { children: [(0, jsxRuntime.jsx)("dt", { children: copy.temperature }), (0, jsxRuntime.jsx)("dd", { children: formatMetric(browserLocale, battery.temperature, "°C", copy.waiting) })] }),
                    (0, jsxRuntime.jsxs)("div", { children: [(0, jsxRuntime.jsx)("dt", { children: copy.energy }), (0, jsxRuntime.jsx)("dd", { children: formatEnergy(browserLocale, battery.energy, copy.waiting) })] }),
                    (0, jsxRuntime.jsxs)("div", { children: [(0, jsxRuntime.jsx)("dt", { children: copy.cells }), (0, jsxRuntime.jsx)("dd", { children: formatCells(browserLocale, battery, copy.waiting) })] }),
                  ],
                }),
                (0, jsxRuntime.jsxs)("footer", {
                  className: "battery-card-footer",
                  children: [
                    (0, jsxRuntime.jsxs)("div", {
                      className: "battery-card-statuses",
                      children: [
                        (0, jsxRuntime.jsxs)("span", { className: battery.balancing ? "active" : "", children: [(0, jsxRuntime.jsx)("i", {}), battery.balancing ? copy.balancing : copy.stable] }),
                        (0, jsxRuntime.jsxs)("span", { className: battery.chargingAllowed ? "active" : "warning", children: [(0, jsxRuntime.jsx)("i", {}), battery.chargingAllowed ? copy.chargeAllowed : copy.chargeProtected] }),
                        (0, jsxRuntime.jsxs)("span", { className: battery.dischargingAllowed ? "active" : "warning", children: [(0, jsxRuntime.jsx)("i", {}), battery.dischargingAllowed ? copy.dischargeAllowed : copy.dischargeProtected] }),
                      ],
                    }),
                    (0, jsxRuntime.jsxs)("small", { children: [battery.cycles ?? "—", " ", cycleLabel] }),
                  ],
                }),
              ],
            }, battery.name || index);
          }),
        ],
      }),
      (0, jsxRuntime.jsx)("p", { className: "battery-privacy", children: copy.privacy }),
    ],
  });
}

export { BatteryTelemetry };
