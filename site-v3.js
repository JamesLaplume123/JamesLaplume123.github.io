(() => {
  const body = document.body;
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');

  toggle?.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    body.classList.remove('nav-open');
    toggle?.setAttribute('aria-expanded', 'false');
  }));

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape' || !body.classList.contains('nav-open')) return;
    body.classList.remove('nav-open');
    toggle?.setAttribute('aria-expanded', 'false');
    toggle?.focus();
  });

  const reveal = [...document.querySelectorAll('[data-reveal]')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    reveal.forEach((node) => observer.observe(node));
  } else {
    reveal.forEach((node) => node.classList.add('visible'));
  }

  const form = document.querySelector('[data-contact-form]');
  if (form) {
    const status = form.querySelector('[data-form-status]');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      button.disabled = true;
      status.textContent = 'Envoi en cours...';

      try {
        const response = await fetch('https://formsubmit.co/ajax/laplumejames@gmail.com', {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: new FormData(form),
        });
        if (!response.ok) throw new Error('Form unavailable');
        form.reset();
        status.textContent = 'Merci. Votre message a bien été transmis.';
      } catch {
        status.innerHTML = 'L’envoi automatique est indisponible. Écrivez directement à <a href="mailto:laplumejames@gmail.com">laplumejames@gmail.com</a>.';
      } finally {
        button.disabled = false;
      }
    });
  }

  const counter = document.querySelector('[data-visitor-count]');
  if (counter) {
    const cacheKey = 'jl-public-visitor-count';
    const cached = Number(sessionStorage.getItem(cacheKey));
    const show = (count) => {
      counter.textContent = new Intl.NumberFormat(document.documentElement.lang || 'fr-CA').format(count);
    };
    if (Number.isFinite(cached) && cached > 0) {
      show(cached);
    } else {
      fetch('https://counterapi.com/api/jameslaplume.ca/view/site?unique=true', { cache: 'no-store' })
        .then((response) => response.ok ? response.json() : Promise.reject())
        .then((data) => {
          const count = Number(data.value ?? data.count ?? data.data?.value);
          if (!Number.isFinite(count)) throw new Error('Invalid count');
          show(count);
          sessionStorage.setItem(cacheKey, String(count));
        })
        .catch(() => counter.closest('.visitor-counter')?.remove());
    }
  }
})();
