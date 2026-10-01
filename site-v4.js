(() => {
  const environmentData = {
    home: {
      image: '/media/concept/jarvis-hero-architecture-v1.webp',
      kicker: 'JARVIS · INTELLIGENCE PRIVÉE · RÉSIDENCE',
      lead: 'Une intelligence privée qui comprend vos règles, coordonne les systèmes autorisés et vous laisse les décisions importantes.',
      title: 'Retour prévu dans 32 minutes.',
      copy: 'La maison peut préparer l’éclairage d’arrivée et maintenir la recharge après 21 h.',
      signals: ['Absence confirmée', 'Réserve 74 %', 'Votre accord'],
      link: '/solutions/environnements-intelligents/'
    },
    business: {
      image: '/media/solutions/jarvis-enterprise-operations-v1.webp',
      kicker: 'JARVIS · INTELLIGENCE OPÉRATIONNELLE · ENTREPRISE',
      lead: 'JARVIS relie les demandes, les documents et les outils autorisés pour préparer un travail complet, explicable et vérifiable.',
      title: 'Une demande urgente est prête.',
      copy: 'Le client, le contrat, la disponibilité et les documents ont été rapprochés. La mission attend une décision.',
      signals: ['Client reconnu', 'Confiance 96 %', 'Approbation'],
      link: '/solutions/automatisation-operations/'
    },
    vehicle: {
      image: '/media/ambulance/ambulance-cutaway-control-v1.webp',
      kicker: 'JARVIS · LABORATOIRE MOBILE · CONDITIONS RÉELLES',
      lead: 'Énergie, eau, confort, réseau et sécurité deviennent un environnement mobile compréhensible et contrôlable.',
      title: 'L’autonomie couvre le prochain arrêt.',
      copy: 'Le trajet recharge les batteries. Le chauffe-eau peut rester reporté et le confort sera prêt à l’arrivée.',
      signals: ['Trajet 2 h 18', 'Batteries 74 %', 'Plan proposé'],
      link: '/laboratoire-mobile/'
    }
  };

  const capabilityData = {
    'environnements-intelligents': ['/media/solutions/jarvis-spaces-property-v3.webp', 'ENVIRONNEMENTS INTELLIGENTS', 'Le lieu répond à la situation, pas à une suite de commandes.', 'Éclairage, climat, sécurité et énergie se coordonnent dans une interface unique.', 'Mode arrivée prêt à confirmer'],
    'ia-privee-connaissances': ['/media/solutions/ia-privee-connaissances.webp', 'IA PRIVÉE ET CONNAISSANCES', 'Une réponse utile montre ce qu’elle sait et d’où elle le sait.', 'Documents, photos, courriels et dossiers autorisés deviennent interrogeables sans perdre leurs sources.', '3 sources rapprochées'],
    'securite-intelligente': ['/media/solutions/securite-intelligente.webp', 'SÉCURITÉ INTELLIGENTE', 'Comprendre l’événement avant de décider quoi faire.', 'Caméras, accès, personnes, appareils et règles expliquent ensemble ce qui mérite votre attention.', 'Événement expliqué localement'],
    'automatisation-operations': ['/media/solutions/jarvis-enterprise-operations-v1.webp', 'AUTOMATISATION D’ENTREPRISE', 'La demande devient un travail complet, prêt à approuver.', 'JARVIS consulte les outils autorisés, prépare les actions et conserve chaque décision dans le journal.', 'Mission prête à autoriser'],
    'reseau-resilience': ['/media/solutions/reseau-resilience.webp', 'RÉSEAU ET CYBERSÉCURITÉ', 'Voir l’infrastructure comme un système vivant.', 'Topologie, appareils et changements permettent de comprendre une anomalie avant qu’elle devienne une panne.', 'Caméra Est à vérifier'],
    'diagnostic-care': ['/media/solutions/diagnostic-care.webp', 'DIAGNOSTIC ET CONTINUITÉ', 'Passer du symptôme aux prochaines vérifications utiles.', 'JARVIS rapproche l’état réel, l’historique et la documentation pour guider une reprise structurée.', 'Deux causes probables classées']
  };

  const hero = document.querySelector('[data-v4-hero]');
  if (hero) {
    const environmentButtons = [...hero.querySelectorAll('[data-v4-environment]')];
    environmentButtons.forEach((button) => button.addEventListener('click', () => {
      const data = environmentData[button.dataset.v4Environment];
      if (!data) return;
      environmentButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-selected', String(active));
      });
      hero.querySelector('[data-v4-hero-image]').src = data.image;
      hero.querySelector('[data-v4-hero-kicker]').textContent = data.kicker;
      hero.querySelector('[data-v4-hero-lead]').textContent = data.lead;
      hero.querySelector('[data-v4-console-title]').textContent = data.title;
      hero.querySelector('[data-v4-console-copy]').textContent = data.copy;
      hero.querySelector('[data-v4-signal-one]').textContent = data.signals[0];
      hero.querySelector('[data-v4-signal-two]').textContent = data.signals[1];
      hero.querySelector('[data-v4-signal-three]').textContent = data.signals[2];
      hero.querySelector('[data-v4-console-link]').href = data.link;
    }));
  }

  const capabilityButtons = [...document.querySelectorAll('[data-v4-capability]')];
  if (capabilityButtons.length) {
    const image = document.querySelector('[data-v4-capability-image]');
    const kicker = document.querySelector('[data-v4-capability-kicker]');
    const title = document.querySelector('[data-v4-capability-title]');
    const copy = document.querySelector('[data-v4-capability-copy]');
    const link = document.querySelector('[data-v4-capability-link]');
    const status = document.querySelector('[data-v4-capability-status]');
    capabilityButtons.forEach((button) => button.addEventListener('click', () => {
      const slug = button.dataset.v4Capability;
      const data = capabilityData[slug];
      if (!data) return;
      capabilityButtons.forEach((item) => item.classList.toggle('active', item === button));
      image.src = data[0];
      image.alt = `Aperçu de la capacité ${data[1].toLowerCase()}`;
      kicker.textContent = data[1];
      title.textContent = data[2];
      copy.textContent = data[3];
      link.href = `/solutions/${slug}/`;
      status.textContent = data[4];
    }));
  }

  const legacyContactForm = document.querySelector('[data-contact-form]');
  if (legacyContactForm) {
    const form = legacyContactForm.cloneNode(true);
    legacyContactForm.replaceWith(form);

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      const status = form.querySelector('[data-form-status]');
      const payload = Object.fromEntries(new FormData(form).entries());
      payload._url = window.location.href;
      button.disabled = true;
      status.textContent = 'Envoi en cours...';

      try {
        const response = await fetch('https://formsubmit.co/ajax/laplumejames@gmail.com', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || result.success === false) throw new Error('Form unavailable');
        form.reset();
        status.textContent = 'Merci. Votre message a bien été transmis.';
      } catch {
        const subject = encodeURIComponent(`Demande depuis jameslaplume.ca · ${payload.name || 'Nouveau projet'}`);
        const body = encodeURIComponent([
          `Nom: ${payload.name || ''}`,
          `Courriel: ${payload.email || ''}`,
          `Organisation: ${payload.organization || ''}`,
          `Profil: ${payload.profile || ''}`,
          `Sujet: ${payload.interest || ''}`,
          '',
          payload.message || ''
        ].join('\n'));
        const fallback = document.createElement('a');
        fallback.href = `mailto:laplumejames@gmail.com?subject=${subject}&body=${body}`;
        fallback.textContent = 'Ouvrir votre courriel prérempli';
        status.replaceChildren('L’envoi automatique est temporairement indisponible. ', fallback, '.');
      } finally {
        button.disabled = false;
      }
    });
  }
})();
