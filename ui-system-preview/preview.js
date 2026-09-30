(() => {
  window.lucide?.createIcons();

  const toast = document.querySelector('[data-toast]');
  let toastTimer;
  const announce = (title, detail) => {
    if (!toast) return;
    toast.querySelector('strong').textContent = title;
    toast.querySelector('small').textContent = detail;
    toast.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('visible'), 2200);
  };

  document.querySelectorAll('.primary-nav button').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.primary-nav button').forEach((item) => item.classList.toggle('active', item === button));
      announce(button.dataset.section, 'La navigation conserve une seule structure dans toutes les capacités.');
    });
  });

  document.querySelectorAll('[data-scene]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-scene]').forEach((item) => item.classList.toggle('active', item === button));
      document.querySelector('[data-scene-name]').textContent = button.dataset.scene;
      document.querySelector('[data-scene-copy]').textContent = button.dataset.copy;
      announce(`Ambiance ${button.dataset.scene}`, 'Les systèmes concernés préparent leur action de façon coordonnée.');
    });
  });

  document.querySelectorAll('[data-control]').forEach((button) => {
    button.addEventListener('click', () => {
      const enabled = button.classList.toggle('is-on');
      announce(button.dataset.control, enabled ? 'Commande activée dans cet aperçu.' : 'Commande désactivée dans cet aperçu.');
    });
  });

  document.querySelectorAll('[data-temp-step]').forEach((button) => {
    button.addEventListener('click', () => {
      const output = document.querySelector('[data-temperature]');
      const next = Math.min(27, Math.max(16, Number(output.textContent) + Number(button.dataset.tempStep)));
      output.textContent = String(next);
      announce('Climat du salon', `Consigne ajustée à ${next} °C.`);
    });
  });

  document.querySelectorAll('.mode-switch button').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.mode-switch button').forEach((item) => item.classList.toggle('active', item === button));
      announce(`Mode ${button.textContent}`, 'La consigne et les priorités énergétiques seront ajustées.');
    });
  });

  document.querySelectorAll('[data-room]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-room]').forEach((item) => item.classList.toggle('selected', item === button));
      announce(button.dataset.room, button.dataset.roomState);
    });
  });

  const refreshTime = () => {
    const now = new Date();
    const time = new Intl.DateTimeFormat('fr-CA', { hour: '2-digit', minute: '2-digit' }).format(now);
    const date = new Intl.DateTimeFormat('fr-CA', { weekday: 'long', day: 'numeric', month: 'long' }).format(now);
    const clock = document.querySelector('[data-clock]');
    const dateNode = document.querySelector('[data-date]');
    if (clock) clock.textContent = time;
    if (dateNode) dateNode.textContent = date.charAt(0).toUpperCase() + date.slice(1);
  };
  refreshTime();
  setInterval(refreshTime, 30000);
})();
