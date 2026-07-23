const year = document.querySelector("#year");
const form = document.querySelector("#assistant-form");
const input = document.querySelector("#assistant-input");
const log = document.querySelector("#assistant-log");
const clock = document.querySelector("[data-clock]");
const header = document.querySelector("[data-site-header]");
const canvas = document.querySelector("[data-signal-canvas]");
const commands = document.querySelectorAll("[data-command]");

const responses = {
  serveur:
    "Plan serveur: Caddy pour le SSL, Docker pour isoler les services, sauvegardes automatiques et un dashboard simple pour voir ce qui roule.",
  vision:
    "Plan vision: caméras locales, détection avec Frigate, alertes propres et accès privé. L'idée est de voir clair sans dépendre d'un cloud inutile.",
  roadmap:
    "Roadmap: site public maintenant, serveur perso ensuite, puis mémoire Jarvis, automatisations et tableau de bord vivant."
};

year.textContent = new Date().getFullYear();

if (window.lucide) {
  window.lucide.createIcons();
} else {
  window.addEventListener("load", () => window.lucide?.createIcons());
}

updateClock();
setInterval(updateClock, 30000);

document.addEventListener("scroll", () => {
  header.classList.toggle("is-scrolled", window.scrollY > 16);
});

commands.forEach((button) => {
  button.addEventListener("click", () => {
    const command = button.dataset.command;
    appendEntry("James", button.textContent.trim());
    appendEntry("Jarvis", responses[command]);
  });
});

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message) {
    input.focus();
    return;
  }

  appendEntry("James", message);
  appendEntry("Jarvis", buildResponse(message));

  input.value = "";
  input.focus();
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.14 }
);

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));

setupSignalCanvas();

function updateClock() {
  if (!clock) return;
  clock.textContent = new Intl.DateTimeFormat("fr-CA", {
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date());
}

function buildResponse(message) {
  const normalized = message.toLowerCase();

  if (normalized.includes("serveur") || normalized.includes("docker")) {
    return responses.serveur;
  }

  if (
    normalized.includes("camera") ||
    normalized.includes("caméra") ||
    normalized.includes("frigate") ||
    normalized.includes("vision")
  ) {
    return responses.vision;
  }

  if (normalized.includes("jarvis") || normalized.includes("assistant")) {
    return "Jarvis va devenir le cerveau tranquille du site: interface publique ici, logique privée sur ton serveur, permissions limitées et actions claires.";
  }

  return "Je garde ça en note pour la suite. Pour agir réellement, il faudra me brancher à un backend privé, puis décider quelles commandes ont le droit de toucher au serveur.";
}

function appendEntry(name, text) {
  const entry = document.createElement("p");
  const speaker = document.createElement("strong");
  speaker.textContent = name;
  entry.appendChild(speaker);
  entry.append(document.createTextNode(text));
  log.appendChild(entry);
  log.scrollTop = log.scrollHeight;
}

function setupSignalCanvas() {
  if (!canvas || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const context = canvas.getContext("2d", { alpha: true });
  const points = [];
  const pointCount = 72;
  let width = 0;
  let height = 0;
  let animationFrame = 0;

  const resize = () => {
    const ratio = window.devicePixelRatio || 1;
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    points.length = 0;
    for (let index = 0; index < pointCount; index += 1) {
      points.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.22,
        vy: (Math.random() - 0.5) * 0.22
      });
    }
  };

  const draw = () => {
    context.clearRect(0, 0, width, height);
    context.lineWidth = 1;

    points.forEach((point) => {
      point.x += point.vx;
      point.y += point.vy;

      if (point.x < 0 || point.x > width) point.vx *= -1;
      if (point.y < 0 || point.y > height) point.vy *= -1;
    });

    for (let index = 0; index < points.length; index += 1) {
      for (let next = index + 1; next < points.length; next += 1) {
        const first = points[index];
        const second = points[next];
        const distance = Math.hypot(first.x - second.x, first.y - second.y);

        if (distance < 132) {
          const opacity = (1 - distance / 132) * 0.22;
          context.strokeStyle = `rgba(109, 217, 255, ${opacity})`;
          context.beginPath();
          context.moveTo(first.x, first.y);
          context.lineTo(second.x, second.y);
          context.stroke();
        }
      }
    }

    points.forEach((point) => {
      context.fillStyle = "rgba(255, 255, 255, 0.45)";
      context.fillRect(point.x, point.y, 1.4, 1.4);
    });

    animationFrame = requestAnimationFrame(draw);
  };

  resize();
  draw();

  window.addEventListener("resize", () => {
    cancelAnimationFrame(animationFrame);
    resize();
    draw();
  });
}
