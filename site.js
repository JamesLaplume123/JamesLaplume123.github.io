(() => {
  const root = document.documentElement;
  const body = document.body;
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");

  if (toggle && nav) {
    const closeNav = () => {
      nav.classList.remove("open");
      body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
    };

    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      body.classList.toggle("nav-open", isOpen);
      toggle.setAttribute("aria-expanded", String(isOpen));
    });

    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeNav));
    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) closeNav();
    });
  }

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const revealItems = document.querySelectorAll(".reveal");
  if (reducedMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("visible"));
  } else {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealItems.forEach((item) => observer.observe(item));
  }

  const productStage = document.querySelector(".product-stage");
  if (productStage) {
    const viewport = productStage.querySelector("[data-product-stage]");
    const image = productStage.querySelector("[data-product-image]");
    const title = productStage.querySelector("[data-product-title]");
    const description = productStage.querySelector("[data-product-copy]");
    const buttons = [...productStage.querySelectorAll("[data-product-view]")];
    const views = {
      assistant: {
        src: "/media/jarvis/jarvis-showcase.webp",
        fr: {
          title: "Une demande devient une mission prête à valider.",
          description: "JARVIS rassemble les sources autorisées, prépare le travail et attend votre approbation avant toute action externe."
        },
        en: {
          title: "A request becomes a mission ready for review.",
          description: "JARVIS gathers approved sources, prepares the work and waits for human approval before any external action."
        }
      },
      modules: {
        src: "/media/jarvis/jarvis-modules.webp",
        fr: {
          title: "Une plateforme modulaire, livrée par étapes.",
          description: "Control, Knowledge, Agents, Vision, Automation et Diagnostics avancent avec des statuts honnêtes."
        },
        en: {
          title: "A modular platform, delivered in stages.",
          description: "Control, Knowledge, Agents, Vision, Automation and Diagnostics progress with honest status labels."
        }
      }
    };

    const locale = root.lang.startsWith("en") ? "en" : "fr";
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const key = button.dataset.productView;
        const view = views[key];
        if (!view || button.classList.contains("active")) return;
        buttons.forEach((item) => {
          const active = item === button;
          item.classList.toggle("active", active);
          item.setAttribute("aria-selected", String(active));
        });
        viewport.classList.add("is-switching");
        window.setTimeout(() => {
          image.src = view.src;
          image.alt = view[locale].title;
          title.textContent = view[locale].title;
          description.textContent = view[locale].description;
          image.addEventListener("load", () => viewport.classList.remove("is-switching"), { once: true });
        }, 170);
      });
    });
  }

  const architecture = document.querySelector(".architecture-layout:has([data-architecture-node])");
  if (architecture) {
    const title = architecture.querySelector("[data-architecture-title]");
    const bodyCopy = architecture.querySelector("[data-architecture-body]");
    const proof = architecture.querySelector("[data-architecture-proof]");
    const nodes = [...architecture.querySelectorAll("[data-architecture-node]")];
    nodes.forEach((node) => {
      node.addEventListener("click", () => {
        nodes.forEach((item) => item.classList.toggle("active", item === node));
        title.textContent = node.dataset.title;
        bodyCopy.textContent = node.dataset.body;
        proof.textContent = node.dataset.proof;
      });
    });
  }

  const form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const name = String(data.get("name") || "").trim();
      const email = String(data.get("email") || "").trim();
      const company = String(data.get("organization") || "").trim();
      const service = String(data.get("projectType") || "").trim();
      const message = String(data.get("message") || "").trim();
      const isEnglish = root.lang.startsWith("en");
      const subject = isEnglish
        ? `Project inquiry - ${service || "JARVIS"}`
        : `Demande de projet - ${service || "JARVIS"}`;
      const lines = isEnglish
        ? [`Name: ${name}`, `Email: ${email}`, `Company: ${company}`, `Service: ${service}`, "", message]
        : [`Nom : ${name}`, `Courriel : ${email}`, `Entreprise : ${company}`, `Service : ${service}`, "", message];
      window.location.href = `mailto:laplumejames@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
    });
  }

  const footerBottom = document.querySelector(".footer-bottom");
  if (footerBottom) {
    const isEnglish = root.lang.startsWith("en");
    const counter = document.createElement("span");
    counter.className = "visitor-counter";
    counter.innerHTML = `<i aria-hidden="true"></i>${isEnglish ? "Visitors" : "Visiteurs"} <b data-visitor-count aria-live="polite">—</b>`;
    footerBottom.append(counter);

    const value = counter.querySelector("[data-visitor-count]");
    const sessionKey = "jl-visit-count";
    const cachedCount = Number(sessionStorage.getItem(sessionKey));
    const endpoint = new URL("https://counterapi.com/api/jameslaplume.ca/view/site");
    endpoint.searchParams.set("unique", "true");

    const showCount = (count) => {
      value.textContent = new Intl.NumberFormat(isEnglish ? "en-CA" : "fr-CA").format(count);
    };

    if (Number.isFinite(cachedCount) && cachedCount > 0) {
      showCount(cachedCount);
      return;
    }

    fetch(endpoint, { mode: "cors", cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error("Counter unavailable");
        return response.json();
      })
      .then((data) => {
        const count = Number(data.value ?? data.count ?? data.data?.value);
        if (!Number.isFinite(count)) throw new Error("Invalid counter response");
        showCount(count);
        sessionStorage.setItem(sessionKey, String(count));
      })
      .catch(() => {
        counter.hidden = true;
      });
  }
})();
