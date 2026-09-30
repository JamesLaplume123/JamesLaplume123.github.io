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

  const demoApprove = document.querySelector('[data-demo-approve]');
  if (demoApprove) {
    const demo = demoApprove.closest('.platform-chat');
    const status = demo?.querySelector('[data-demo-status]');
    demoApprove.addEventListener('click', () => {
      demo?.classList.add('approved');
      demoApprove.disabled = true;
      demoApprove.textContent = 'Plan approuve';
      if (status) status.textContent = 'Plan approuve · execution planifiee';
    });
  }

  document.querySelectorAll('[data-demo-tabs]').forEach((demo) => {
    const buttons = [...demo.querySelectorAll('[data-demo-tab]')];
    const panels = [...demo.querySelectorAll('[data-demo-panel]')];
    buttons.forEach((button) => button.addEventListener('click', () => {
      const target = button.dataset.demoTab;
      buttons.forEach((item) => {
        const selected = item === button;
        item.classList.toggle('active', selected);
        item.setAttribute('aria-selected', selected ? 'true' : 'false');
      });
      panels.forEach((panel) => panel.hidden = panel.dataset.demoPanel !== target);
    }));
  });

  document.querySelectorAll('[data-personal-opportunities]').forEach((demo) => {
    const buttons = [...demo.querySelectorAll('[data-personal-opportunity]')];
    const cases = [...demo.querySelectorAll('[data-personal-case]')];
    buttons.forEach((button) => button.addEventListener('click', () => {
      const selected = button.dataset.personalOpportunity;
      buttons.forEach((item) => item.classList.toggle('active', item === button));
      cases.forEach((item) => item.hidden = item.dataset.personalCase !== selected);
    }));
  });

  const makeButtonLike = (elements, onActivate) => {
    elements.forEach((element, index) => {
      element.tabIndex = 0;
      element.setAttribute('role', 'button');
      element.setAttribute('aria-pressed', String(element.classList.contains('active')));
      const activate = () => onActivate(element, index, elements);
      element.addEventListener('click', activate);
      element.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') return;
        event.preventDefault();
        activate();
      });
    });
  };

  const selectCard = (elements, selected) => {
    elements.forEach((element) => {
      const active = element === selected;
      element.classList.toggle('active', active);
      element.setAttribute('aria-pressed', String(active));
    });
  };

  const setConsoleStatus = (root, message) => {
    const status = root.querySelector('[data-preview-status]');
    if (status) status.textContent = message;
  };

  const ensureFeedback = (root, label = 'Simulation') => {
    let feedback = root.querySelector('.concept-feedback');
    if (feedback) return feedback;
    feedback = document.createElement('div');
    feedback.className = 'concept-feedback';
    feedback.hidden = true;
    feedback.setAttribute('role', 'status');
    feedback.setAttribute('aria-live', 'polite');
    feedback.innerHTML = `<i></i><div><span>${label}</span><strong data-concept-feedback></strong></div>`;
    root.append(feedback);
    return feedback;
  };

  const showFeedback = (root, message, label) => {
    const feedback = ensureFeedback(root, label);
    const copy = feedback.querySelector('[data-concept-feedback]');
    if (copy) copy.textContent = message;
    feedback.hidden = false;
    feedback.classList.remove('visible');
    requestAnimationFrame(() => feedback.classList.add('visible'));
    clearTimeout(feedback.hideTimer);
    clearTimeout(feedback.cleanupTimer);
    feedback.hideTimer = setTimeout(() => {
      feedback.classList.remove('visible');
      feedback.cleanupTimer = setTimeout(() => { feedback.hidden = true; }, 220);
    }, 2400);
  };

  document.querySelectorAll('.cap-console').forEach((console) => {
    const roomCards = [...console.querySelectorAll('.space-room-grid article')];
    if (roomCards.length) {
      const roomStates = [
        ['Salon', '20,8 °C · occupé', 'Éclairage doux · air stable', 'Passer en mode lecture'],
        ['Cuisine', '21,1 °C · inoccupée', 'Deux prises surveillées', 'Éteindre les prises non essentielles'],
        ['Garage', 'Porte ouverte', 'Ouverte depuis 12 minutes', 'Fermer la porte du garage'],
        ['Extérieur', '4 °C · pluie prévue', 'Éclairage au coucher du soleil', 'Avancer l’éclairage de 15 minutes']
      ];
      const inspector = document.createElement('div');
      inspector.className = 'concept-inspector';
      inspector.innerHTML = '<div><span>Espace sélectionné</span><strong data-room-title>Salon</strong><small data-room-copy>20,8 °C · occupé</small></div><button type="button" data-room-action>Passer en mode lecture</button>';
      console.querySelector('.space-room-grid')?.after(inspector);
      makeButtonLike(roomCards, (card, index) => {
        selectCard(roomCards, card);
        inspector.querySelector('[data-room-title]').textContent = roomStates[index][0];
        inspector.querySelector('[data-room-copy]').textContent = `${roomStates[index][1]} · ${roomStates[index][2]}`;
        inspector.querySelector('[data-room-action]').textContent = roomStates[index][3];
      });
      inspector.querySelector('[data-room-action]')?.addEventListener('click', (event) => {
        event.currentTarget.textContent = 'Action appliquée dans la simulation';
        event.currentTarget.disabled = true;
        showFeedback(console, 'L’état de l’espace, la commande et l’heure ont été ajoutés au journal.', 'Environnement');
      });

      const sceneCards = [...console.querySelectorAll('.scene-library article')];
      makeButtonLike(sceneCards, (card) => {
        selectCard(sceneCards, card);
        const name = card.querySelector('span')?.textContent || 'Scène';
        setConsoleStatus(console, `${name} · aperçu prêt`);
        showFeedback(console, `La scène ${name} est sélectionnée. Ses actions restent modifiables avant activation.`, 'Scène');
      });

      const energyRows = [...console.querySelectorAll('.space-energy-plan article')];
      makeButtonLike(energyRows, (card) => {
        selectCard(energyRows, card);
        const period = card.querySelector('span')?.textContent || 'Période';
        showFeedback(console, `${period} : charge sélectionnée pour comparer son coût, sa priorité et son effet sur la réserve.`, 'Énergie');
      });
    }

    const knowledgeConversation = console.querySelector('.knowledge-conversation');
    if (knowledgeConversation) {
      const evidenceCards = [...console.querySelectorAll('[data-evidence]')];
      const evidencePanels = [...console.querySelectorAll('[data-evidence-panel]')];
      evidenceCards.forEach((card) => card.addEventListener('click', () => {
        const selected = card.dataset.evidence;
        evidenceCards.forEach((item) => item.classList.toggle('active', item === card));
        evidencePanels.forEach((panel) => { panel.hidden = panel.dataset.evidencePanel !== selected; });
        const fileName = card.querySelector('em')?.textContent || 'Source';
        showFeedback(console, `${fileName} ouvert avec son passage, ses métadonnées et sa limite d’utilisation.`, 'Preuve consultée');
      }));

      const caseButtons = [...console.querySelectorAll('[data-knowledge-case]')];
      const mission = console.querySelector('[data-knowledge-mission]');
      const folder = console.querySelector('[data-knowledge-folder]');
      const access = console.querySelector('[data-knowledge-access]');
      const internet = console.querySelector('[data-knowledge-internet]');
      const question = console.querySelector('[data-knowledge-question]');
      const conclusion = console.querySelector('[data-knowledge-conclusion]');
      const confidence = console.querySelector('[data-knowledge-confidence]');
      const summary = console.querySelector('[data-knowledge-summary]');
      const facts = console.querySelector('[data-knowledge-facts]');
      const evidenceGrid = console.querySelector('[data-knowledge-evidence-grid]');
      const evidencePreview = console.querySelector('[data-knowledge-evidence-preview]');
      const nextLabel = console.querySelector('[data-knowledge-next-label]');
      const nextStep = console.querySelector('[data-knowledge-next]');
      const technicalSnapshot = {
        mission: mission?.textContent, folder: folder?.textContent, access: access?.textContent,
        internet: internet?.textContent, question: question?.textContent, conclusion: conclusion?.textContent,
        confidence: confidence?.textContent, summary: summary?.textContent, facts: facts?.innerHTML,
        evidenceGrid: evidenceGrid?.innerHTML, evidencePreview: evidencePreview?.innerHTML,
        nextLabel: nextLabel?.textContent, nextStep: nextStep?.textContent
      };
      const knowledgeCases = {
        personal: {
          mission:'Retrouver et organiser des souvenirs', folder:'PR-012 · Voyage en Floride', access:'Ordinateur · NAS · photos · vidéos · courriels', internet:'Fermé',
          question:'Retrouve mes photos et vidéos du voyage en Floride, classe-les par journée et prépare une sélection sans déplacer les originaux.',
          conclusion:'JARVIS a retrouvé 286 médias et reconstitué huit journées; douze fichiers restent sans date ou lieu fiable.', confidence:'Confiance · 95 %',
          summary:'JARVIS interroge l’index local des dossiers autorisés, rapproche les dates, lieux, réservations et métadonnées des appareils, puis prépare une sélection. Les photos et films originaux restent sur l’ordinateur et le NAS.',
          facts:[['Retrouvé','214 photos · 72 vidéos','Ordinateur et NAS autorisés'],['Reconstitué','8 journées · 11 lieux','Métadonnées + réservations'],['À vérifier','12 fichiers sans repère fiable','Aucune date inventée']],
          nextLabel:'Album personnel proposé', next:'Créer une sélection par journée, isoler les doublons et demander où classer les douze fichiers incertains.', followup:'Montre-moi seulement les photos prises près de Miami avec les vidéos de la même journée.',
          sources:[
            ['IMG','214','photos','Photos_2025_Floride.album','Photothèque personnelle','Dates, lieux et appareils conservés','La photothèque fournit les images originales et leurs métadonnées sans créer de copies inutiles.',['214 photos dans la période autorisée','9 lieux confirmés par GPS','7 fichiers sans emplacement']],
            ['VID','72','vidéos','Videos_Voyage.index','Vidéos et séquences','Ordinateur + NAS · lecture seulement','L’index vidéo utilise les dates, miniatures et transcriptions disponibles pour relier les séquences au voyage.',['72 vidéos retrouvées','18 séquences près de Miami','5 vidéos sans date fiable']],
            ['MSG','8','réservations','Reservations_Floride.msg','Courriels de réservation','Dossier Voyages seulement','Les confirmations servent de repères de date et de lieu sans ouvrir toute la boîte courriel.',['Vol aller et retour retrouvés','Trois hôtels confirmés','Deux locations de voiture']],
            ['MED','1','film personnel','Montage_Floride_4K.mov','Bibliothèque de médias','NAS familial · fichier original','Le film déjà monté est relié aux mêmes événements et peut être retrouvé ou lu depuis sa source.',['Durée : 18 min 42 s','Créé le 14 mars 2025','Original conservé sur le NAS']]
          ]
        },
        crm: {
          mission:'Préparer une rencontre client', folder:'CRM-218 · Groupe Atlas', access:'CRM · courriels · contrat · calendrier', internet:'Fermé',
          question:'Prépare-moi un portrait clair de ce client avant la rencontre de demain.',
          conclusion:'Le renouvellement et deux demandes restées sans suivi doivent être abordés en priorité.', confidence:'Confiance · 91 %',
          summary:'JARVIS rapproche la fiche CRM, les derniers courriels, le contrat actif et les rendez-vous. Il distingue les faits enregistrés des intentions commerciales et prépare un briefing sans modifier le CRM.',
          facts:[['Confirmé','Renouvellement le 15 novembre','Contrat signé · section 8'],['À traiter','Deux demandes sans suivi','Courriels des 18 et 24 septembre'],['Occasion','Extension vers un second site','Note CRM · à valider avec le client']],
          nextLabel:'Brief proposé', next:'Préparer une page avec les engagements, les demandes ouvertes et cinq questions pour la rencontre.', followup:'Montre-moi les deux demandes qui n’ont pas reçu de suivi.',
          sources:[
            ['CRM','12 ans','dans le CRM','Groupe_Atlas.crm','Historique du compte','Compte, contacts, occasions et activités','Le CRM confirme la relation et les dossiers ouverts.',['Compte actif depuis 2014','4 contacts autorisés','Occasion « Site Est » ouverte']],
            ['MSG','2','suivis manquants','Courriels_Atlas.msg','Demandes récentes','18 et 24 septembre · boîte Ventes','Les messages montrent les demandes exactes et leurs dates.',['Demande de calendrier d’installation','Question sur le support prolongé','Aucune réponse finale archivée']],
            ['PDF','15 nov.','renouvellement','Contrat_Atlas_2024.pdf','Échéance et portée','Contrat signé · version finale','Le contrat fixe la date et les services réellement inclus.',['Renouvellement automatique','Préavis de 30 jours','Un seul site actuellement couvert']],
            ['CAL','45 min','demain · 10 h','Rencontre_Atlas.cal','Contexte du rendez-vous','Calendrier de la direction','Le calendrier précise les participants et le temps disponible.',['Direction générale invitée','Responsable technique présent','Aucun ordre du jour joint']]
          ]
        },
        contract: {
          mission:'Comparer un contrat et ses annexes', folder:'CT-086 · Renouvellement fournisseur', access:'Contrats · annexes · courriels juridiques', internet:'Fermé',
          question:'Qu’est-ce qui change dans cette nouvelle version et quelles clauses exigent une décision?',
          conclusion:'Trois changements ont un impact opérationnel; la responsabilité sur les sauvegardes demeure ambiguë.', confidence:'Confiance · 94 %',
          summary:'JARVIS compare la version signée, la proposition reçue et les annexes. Il cite chaque différence, sépare les changements de prix des obligations et ne formule aucun avis juridique.',
          facts:[['Modifié','Hausse de 8 %','Proposition v3 · page 4'],['Nouveau','Préavis porté à 90 jours','Clause 11.2'],['Ambigu','Responsabilité des sauvegardes','Annexe B et courriel contradictoires']],
          nextLabel:'Décision préparée', next:'Créer un tableau avant/après et soumettre les trois clauses sensibles au responsable autorisé.', followup:'Affiche-moi mot pour mot les clauses qui ont changé.',
          sources:[
            ['PDF','V2','contrat signé','Contrat_2025_signe.pdf','Référence contractuelle','42 pages · signature vérifiée','Cette version constitue le point de comparaison.',['Prix annuel actuel','Préavis de 60 jours','Sauvegardes incluses à l’annexe B']],
            ['PDF','V3','proposition','Renouvellement_2026_v3.pdf','Nouvelle version','45 pages · reçue le 27 septembre','La proposition contient les modifications à décider.',['Prix augmenté de 8 %','Préavis de 90 jours','Nouvelle limite de responsabilité']],
            ['DOC','B','annexe technique','Annexe_B_services.docx','Portée technique','Services et exclusions','L’annexe décrit qui opère les sauvegardes.',['Rétention de 30 jours','Test annuel mentionné','Responsabilité non attribuée clairement']],
            ['MSG','3','échanges juridiques','Courriels_juridiques.msg','Contexte des négociations','Fil autorisé · lecture seulement','Les échanges expliquent l’intention, sans modifier le texte signé.',['Demande de clarification envoyée','Réponse partielle reçue','Aucune acceptation donnée']]
          ]
        },
        finance: {
          mission:'Expliquer un écart de facture', folder:'FI-144 · Fournisseur Nord', access:'Facture · bon de commande · réception', internet:'Fermé',
          question:'Pourquoi cette facture est-elle plus élevée que le bon de commande?',
          conclusion:'L’écart provient de frais de transport ajoutés et d’une quantité reçue non confirmée.', confidence:'Confiance · 96 %',
          summary:'JARVIS compare la facture, la commande, la réception et l’entente fournisseur. Il calcule l’écart, montre son origine et prépare les questions à envoyer sans approuver le paiement.',
          facts:[['Écart total','1 284 $','Facture moins bon de commande'],['Expliqué','684 $ de transport','Non prévu sur la commande'],['À confirmer','600 $ de quantité','Réception partielle non signée']],
          nextLabel:'Contrôle proposé', next:'Bloquer l’approbation, demander la preuve de livraison et préparer un courriel au fournisseur.', followup:'Montre-moi chaque ligne qui ne correspond pas à la commande.',
          sources:[
            ['PDF','18 420 $','facturé','Facture_FN-8841.pdf','Facture fournisseur','Reçue le 28 septembre','La facture fournit les montants réellement demandés.',['12 lignes facturées','Transport ajouté séparément','Taxes calculées après frais']],
            ['PO','17 136 $','commandé','BC-2026-441.po','Bon de commande','Approuvé le 4 septembre','La commande constitue la limite approuvée.',['11 lignes approuvées','Transport inclus au devis','Quantité de câble : 800 m']],
            ['REC','620 m','reçus','Reception_441.rec','Réception physique','Entrée d’inventaire provisoire','La réception ne confirme pas toute la quantité facturée.',['620 m comptés','Bon de livraison non signé','180 m encore à confirmer']],
            ['MSG','1','réponse attendue','Echange_fournisseur.msg','Entente commerciale','Boîte Comptabilité · lecture','Le fournisseur mentionne une surcharge, sans approbation jointe.',['Surcharge évoquée le 26 septembre','Aucun accord interne retrouvé','Brouillon de contestation prêt']]
          ]
        },
        hr: {
          mission:'Préparer l’arrivée d’un employé', folder:'RH-031 · Technicien terrain', access:'Politiques · rôle · formations · calendrier', internet:'Fermé',
          question:'Prépare l’accueil du nouveau technicien et montre ce qui manque avant sa première journée.',
          conclusion:'Le plan d’accueil est presque complet; deux accès et une formation sécurité restent à confirmer.', confidence:'Confiance · 89 %',
          summary:'JARVIS lit uniquement le dossier d’accueil autorisé, le profil de rôle, les politiques et le calendrier de formation. Les données personnelles non nécessaires demeurent exclues.',
          facts:[['Prêt','Matériel et horaire','Demande TI + calendrier'],['Manquant','Accès CRM et inventaire','Aucune approbation jointe'],['Obligatoire','Formation sécurité terrain','À planifier avant la première mission']],
          nextLabel:'Plan d’accueil proposé', next:'Préparer la liste du jour 1 et demander les deux approbations manquantes aux responsables.', followup:'Quels accès doivent être approuvés avant sa première mission?',
          sources:[
            ['DOC','Rôle','technicien','Profil_Technicien.docx','Responsabilités du poste','Version RH approuvée','Le profil définit les outils et formations nécessaires.',['Interventions terrain','Accès CRM limité','Formation sécurité obligatoire']],
            ['POL','6','politiques','Politiques_Accueil.pdf','Règles d’intégration','Corpus RH autorisé','Les politiques encadrent les étapes obligatoires.',['Confidentialité signée','Sécurité avant terrain','Accès selon le rôle']],
            ['CAL','3','séances prévues','Calendrier_Accueil.cal','Horaire de la première semaine','Calendrier du gestionnaire','Le calendrier confirme ce qui est déjà réservé.',['Accueil lundi 9 h','Formation produit mardi','Sécurité non planifiée']],
            ['TKT','2','accès en attente','Demandes_TI.tkt','État des accès','Portail TI · lecture seulement','Les billets montrent les permissions qui attendent un accord.',['Courriel créé','CRM en attente','Inventaire en attente']]
          ]
        }
      };
      const renderFacts = (items) => items.map(([label, value, note]) => `<article><span>${label}</span><strong>${value}</strong><small>${note}</small></article>`).join('');
      const renderEvidence = (key, items) => {
        evidenceGrid.innerHTML = items.map(([kind, metric, metricNote, file, title, meta], index) => `<button class="knowledge-evidence-card${index === 0 ? ' active' : ''}" type="button" data-evidence="${key}-${index}"><span class="knowledge-evidence-thumb doc"><i>${kind}</i><b>${metric}</b><small>${metricNote}</small></span><span><em>${file}</em><strong>${title}</strong><small>${meta}</small></span></button>`).join('');
        evidencePreview.innerHTML = items.map(([kind, metric, metricNote, file, title, meta, why, details], index) => `<article data-evidence-panel="${key}-${index}"${index ? ' hidden' : ''}><div class="knowledge-preview-record"><span>${kind} · ${file}</span><h4>${title}</h4><ul>${details.map((detail) => `<li>${detail}</li>`).join('')}</ul><small>${meta}</small></div><div class="knowledge-preview-copy"><span>Pourquoi cette source compte</span><h4>${why}</h4><dl><div><dt>Fichier</dt><dd>${file}</dd></div><div><dt>Repère</dt><dd>${metric} · ${metricNote}</dd></div><div><dt>Accès</dt><dd>Lecture autorisée pour ce dossier</dd></div><div><dt>Action</dt><dd>Aucune modification automatique</dd></div></dl></div></article>`).join('');
      };
      const renderKnowledgeCase = (key) => {
        const selectedCase = key === 'technical' ? technicalSnapshot : knowledgeCases[key];
        if (!selectedCase) return;
        mission.textContent = selectedCase.mission;
        folder.textContent = selectedCase.folder;
        access.textContent = selectedCase.access;
        internet.textContent = selectedCase.internet;
        question.textContent = selectedCase.question;
        conclusion.textContent = selectedCase.conclusion;
        confidence.textContent = selectedCase.confidence;
        summary.textContent = selectedCase.summary;
        facts.innerHTML = key === 'technical' ? selectedCase.facts : renderFacts(selectedCase.facts);
        if (key === 'technical') {
          evidenceGrid.innerHTML = selectedCase.evidenceGrid;
          evidencePreview.innerHTML = selectedCase.evidencePreview;
        } else {
          renderEvidence(key, selectedCase.sources);
        }
        nextLabel.textContent = selectedCase.nextLabel;
        nextStep.textContent = selectedCase.nextStep || selectedCase.next;
        const input = console.querySelector('#knowledge-question');
        if (input) input.value = selectedCase.followup || 'Quels documents appuient cette conclusion?';
        caseButtons.forEach((button) => button.classList.toggle('active', button.dataset.knowledgeCase === key));
        showFeedback(console, `${folder.textContent} ouvert avec ses sources et ses limites d’accès.`, 'Dossier ouvert');
      };
      caseButtons.forEach((button) => button.addEventListener('click', () => renderKnowledgeCase(button.dataset.knowledgeCase)));

      const form = document.createElement('form');
      form.className = 'knowledge-live-form';
      form.innerHTML = '<label for="knowledge-question">Poser une question aux sources autorisées</label><div><input id="knowledge-question" value="Quels documents appuient cette conclusion?" autocomplete="off"><button type="submit">Interroger</button></div><small>La réponse simulée conserve les citations et le niveau de confiance.</small>';
      knowledgeConversation.after(form);
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const question = form.querySelector('input').value.trim();
        const response = console.querySelector('.knowledge-response>p');
        if (!question || !response) return;
        response.textContent = question.toLowerCase().includes('document')
          ? 'Deux documents primaires et un rapport d’entretien appuient la conclusion. Le point encore incertain est la circulation d’air, qui exige une vérification physique.'
          : 'JARVIS a rapproché la question des sources actuellement autorisées. Les faits confirmés, les limites et la prochaine vérification restent séparés.';
        showFeedback(console, 'Question analysée localement; trois citations sont reliées à la réponse.', 'Connaissances');
      });

      const sourceCards = [...console.querySelectorAll('.knowledge-source-list article')];
      makeButtonLike(sourceCards, (card) => {
        const state = card.querySelector(':scope > span');
        const enabled = !card.classList.toggle('disabled');
        if (state) {
          state.textContent = enabled ? 'Autorisé' : 'Fermé';
          state.classList.toggle('off', !enabled);
        }
        card.setAttribute('aria-pressed', String(enabled));
        showFeedback(console, `${card.querySelector('b')?.textContent || 'Source'} : ${enabled ? 'lecture autorisée pour cette mission' : 'accès retiré de cette mission'}.`, 'Permissions');
      });

      const fileCards = [...console.querySelectorAll('.knowledge-files article')];
      makeButtonLike(fileCards, (card) => {
        selectCard(fileCards, card);
        showFeedback(console, `${card.querySelector('h4')?.textContent || 'Dossier'} ouvert avec ses sources, décisions et limites.`, 'Dossier');
      });

      const matrix = console.querySelector('.permission-matrix');
      if (matrix) {
        const roles = document.createElement('div');
        roles.className = 'permission-profiles';
        roles.innerHTML = '<span>Profil simulé</span><button class="active" type="button">Utilisateur</button><button type="button">Technicien</button><button type="button">Direction</button>';
        matrix.before(roles);
        const roleMessages = {
          Utilisateur: 'Lecture de ses dossiers et préparation de brouillons seulement.',
          Technicien: 'Documentation technique, état des systèmes et rapports d’intervention.',
          Direction: 'Synthèses transversales; toute action opérationnelle exige une approbation.'
        };
        roles.querySelectorAll('button').forEach((button) => button.addEventListener('click', () => {
          roles.querySelectorAll('button').forEach((item) => item.classList.toggle('active', item === button));
          showFeedback(console, roleMessages[button.textContent], 'Profil d’accès');
        }));
      }
    }

    const visionRail = console.querySelector('[data-vision-camera-rail]');
    if (visionRail) {
      const visionData = {
        residential: {
          label: 'Résidence', site: 'Résidence principale', system: 'Surveillance locale active',
          detail: 'Famille, invités, personnel de service, véhicules et appareils autorisés.',
          ruleProfile: 'Résidence · Protection contextuelle', ruleSummary: 'Priorité à la sécurité des occupants, aux accès privés et aux zones extérieures.',
          identities: [
            ['R1', 'Résident autorisé', 'Téléphone · véhicule · code personnel', 'Tous les accès', 'good'],
            ['R2', 'Résidente autorisée', 'Téléphone · montre · code personnel', 'Tous les accès', 'good'],
            ['INV', 'Invitation temporaire', 'Lien mobile · mardi 18 h à 23 h', 'Entrée avant', 'guest'],
            ['?', 'Identité inconnue', 'Aucun facteur autorisé associé', 'Aucun accès', 'unknown']
          ],
          rules: [
            ['Accès principal', 'Deux facteurs contextuels concordants', 'Appareil + code, ou appareil + plaque', 'Active'],
            ['Visiteur inconnu', 'Toujours demander une confirmation', 'Aucun déverrouillage automatique', 'Active'],
            ['Piscine et spa', 'Vérifier que le bassin est libre', 'Confirmation visuelle avant la toile', 'Active'],
            ['Mode nuit', 'Afficher la caméra avant toute alerte', 'Présence extérieure prolongée · 22 h à 06 h', 'Active']
          ],
          cameras: {
            entry: {
              label: 'Entrée avant', meta: '20 h 41', src: '/media/solutions/camera-front-entry-v1.webp', alt: 'Entrée avant de la résidence', state: 'Vérification requise', type: 'Événement prioritaire', confidence: 'Confiance contextuelle · 87 %', detection: '3 éléments rapprochés',
              headline: 'Une personne inconnue accompagne une résidente autorisée.', explanation: 'JARVIS rapproche la caméra, l’accès, les appareils reconnus et l’horaire. Il ne déverrouille rien tant que le contexte demeure incomplet.',
              factors: [['R2', 'Résidente autorisée', 'Téléphone + horaire habituel', 'Confirmé', 'good'], ['V1', 'Véhicule autorisé', 'Plaque + entrée principale', 'Confirmé', 'good'], ['?', 'Visiteur non reconnu', 'Aucun profil ou invitation', 'À vérifier', 'warning']],
              proposal: 'Afficher l’interphone et demander à la résidente de confirmer le visiteur. Aucun accès automatique.', guardrail: 'Une confirmation humaine est requise.', action: 'Demander confirmation',
              summary: 'Un accès autorisé et une présence inconnue ont été observés presque simultanément.',
              timeline: [['20:40:58', 'Véhicule autorisé observé', 'Plaque reconnue · confiance élevée', 'Caméra', 'good'], ['20:41:04', 'Téléphone de la résidente présent', 'Proximité locale · profil R2', 'Appareil', 'good'], ['20:41:08', 'Accès principal en attente', 'Contexte incomplet · aucun déverrouillage', 'Accès', 'attention'], ['20:41:12', 'Visiteur distinct observé', 'Aucune invitation associée', 'Vision', 'attention']]
            },
            driveway: {
              label: 'Allée et garage', meta: '20 h 43', src: '/media/solutions/camera-driveway-garage-v1.webp', alt: 'Allée et porte de garage de la résidence', state: 'Accès préparé', type: 'Arrivée reconnue', confidence: 'Confiance contextuelle · 96 %', detection: 'Plaque + téléphone + horaire',
              headline: 'Un véhicule reconnu arrive à la porte qui lui est attribuée.', explanation: 'La plaque, le téléphone local et l’horaire concordent. L’accès intérieur demeure séparé de la porte du garage.',
              factors: [['V1', 'Véhicule autorisé', 'Plaque reconnue dans l’allée', 'Confirmé', 'good'], ['R1', 'Profil résident', 'Téléphone détecté à proximité', 'Confirmé', 'good'], ['G2', 'Porte attribuée', 'Aucun obstacle observé', 'Prête', 'good']],
              proposal: 'Ouvrir uniquement la porte G2, allumer le passage intérieur et conserver la porte vers la maison verrouillée.', guardrail: 'L’accès à la maison reste distinct.', action: 'Préparer l’arrivée',
              summary: 'Trois facteurs concordants permettent de préparer le garage sans ouvrir l’accès intérieur.',
              timeline: [['20:42:47', 'Plaque V1 reconnue', 'Approche par l’allée principale', 'Caméra', 'good'], ['20:42:51', 'Téléphone R1 présent', 'Signal local confirmé', 'Appareil', 'good'], ['20:42:56', 'Porte G2 vérifiée', 'Zone libre · moteur disponible', 'Garage', 'good'], ['20:43:02', 'Scène d’arrivée préparée', 'En attente de confirmation', 'JARVIS', 'attention']]
            },
            garage: {
              label: 'Garage intérieur', meta: '20 h 44', src: '/media/solutions/camera-garage-supercars-v1.webp', alt: 'Garage intérieur avec véhicules', state: 'Situation normale', type: 'Surveillance passive', confidence: 'Confiance contextuelle · 99 %', detection: 'Aucune anomalie détectée',
              headline: 'Deux véhicules autorisés sont présents. Aucun mouvement inattendu.', explanation: 'Les portes, les véhicules, la présence intérieure et la liaison réseau correspondent à l’état attendu du garage.',
              factors: [['V1', 'Véhicule principal', 'Position habituelle', 'Présent', 'good'], ['V2', 'Véhicule secondaire', 'Position habituelle', 'Présent', 'good'], ['P1', 'Porte vers la maison', 'Verrouillée · aucun passage', 'Sûre', 'good']],
              proposal: 'Maintenir la surveillance passive et conserver l’enregistrement local selon la durée choisie.', guardrail: 'Aucune intervention n’est nécessaire.', action: 'Voir le journal',
              summary: 'L’état du garage correspond aux habitudes et aux règles du site.',
              timeline: [['20:43:11', 'Porte G2 refermée', 'Fin de course confirmée', 'Garage', 'good'], ['20:43:28', 'Véhicule V1 immobilisé', 'Position habituelle', 'Vision', 'good'], ['20:43:44', 'Passage intérieur verrouillé', 'Aucune ouverture enregistrée', 'Accès', 'good'], ['20:44:00', 'Surveillance passive reprise', 'Aucune anomalie', 'JARVIS', 'good']]
            },
            terrace: {
              label: 'Terrasse arrière', meta: '22 h 18', src: '/media/solutions/camera-rear-terrace-v1.webp', alt: 'Terrasse arrière de la résidence', state: 'Présence à confirmer', type: 'Mode nuit', confidence: 'Confiance contextuelle · 71 %', detection: 'Mouvement + chaleur extérieure',
              headline: 'Une présence demeure près du foyer après le passage en mode nuit.', explanation: 'Le mouvement est réel, mais aucun appareil reconnu ne permet encore de l’associer à un occupant ou à un invité.',
              factors: [['TH', 'Signature thermique', 'Présence près du foyer', 'Détectée', 'warning'], ['D3', 'Porte patio', 'Fermée depuis 21 h 52', 'Confirmé', 'good'], ['RF', 'Appareil reconnu', 'Aucun signal à proximité', 'Absent', 'warning']],
              proposal: 'Allumer l’éclairage discret, afficher la caméra et attendre une confirmation avant de déclencher une alerte.', guardrail: 'Aucune sirène sur un signal unique.', action: 'Vérifier la terrasse',
              summary: 'La caméra et le capteur thermique concordent, mais l’identité demeure inconnue.',
              timeline: [['22:17:41', 'Mode nuit activé', 'Périmètre extérieur surveillé', 'Scène', 'good'], ['22:18:03', 'Mouvement sur la terrasse', 'Zone du foyer', 'Caméra', 'attention'], ['22:18:05', 'Chaleur confirmée', 'Signature de taille humaine', 'Capteur', 'attention'], ['22:18:09', 'Aucun appareil reconnu', 'Vérification proposée', 'JARVIS', 'attention']]
            },
            pool: {
              label: 'Piscine et spa', meta: '22 h 21', src: '/media/solutions/camera-pool-spa-v1.webp', alt: 'Piscine et spa de la résidence', state: 'Bassin libre', type: 'Fermeture du soir', confidence: 'Confiance contextuelle · 98 %', detection: 'Vision + eau + accès',
              headline: 'Le périmètre piscine est calme. La toile peut être fermée.', explanation: 'La caméra ne voit personne, les portes extérieures sont fermées et aucun mouvement n’est détecté dans l’eau.',
              factors: [['CV', 'Vue du bassin', 'Aucune personne détectée', 'Libre', 'good'], ['AQ', 'Activité de l’eau', 'Aucun mouvement récent', 'Calme', 'good'], ['PX', 'Accès extérieurs', 'Portes et portail fermés', 'Sécurisés', 'good']],
              proposal: 'Fermer la toile après une dernière confirmation visuelle et activer la règle de surveillance nocturne.', guardrail: 'La fermeture exige une validation explicite.', action: 'Confirmer et fermer',
              summary: 'Les trois sources nécessaires à la fermeture sécuritaire sont concordantes.',
              timeline: [['22:20:32', 'Dernier mouvement terminé', 'Aucune activité dans l’eau', 'Capteur', 'good'], ['22:20:41', 'Portes extérieures fermées', 'Deux contacts confirmés', 'Accès', 'good'], ['22:20:56', 'Bassin libre vérifié', 'Analyse visuelle locale', 'Vision', 'good'], ['22:21:02', 'Fermeture proposée', 'Validation humaine requise', 'JARVIS', 'attention']]
            }
          }
        },
        enterprise: {
          label: 'Entreprise', site: 'Siège social · environnement simulé', system: 'Poste de sécurité local actif',
          detail: 'Employés, visiteurs, fournisseurs, véhicules, zones restreintes et équipements critiques.',
          ruleProfile: 'Entreprise · Accès par rôle et zone', ruleSummary: 'Priorité aux responsabilités, aux horaires, à la traçabilité et aux zones sensibles.',
          identities: [
            ['EMP', 'Employé autorisé', 'Badge · appareil géré · horaire', 'Zones de travail', 'good'],
            ['VIS', 'Visiteur attendu', 'Invitation · hôte · fenêtre horaire', 'Accueil seulement', 'guest'],
            ['FOU', 'Fournisseur planifié', 'Commande · plaque · quai attribué', 'Zone de livraison', 'guest'],
            ['?', 'Présence non associée', 'Aucun badge, mandat ou hôte', 'Aucun accès', 'unknown']
          ],
          rules: [
            ['Entrée des employés', 'Badge et appareil géré concordants', 'Horaire et site autorisés', 'Active'],
            ['Visiteurs', 'Invitation, pièce d’identité et hôte', 'Accès limité à l’accueil', 'Active'],
            ['Zones restreintes', 'Rôle, formation et approbation valides', 'Jamais sur reconnaissance visuelle seule', 'Active'],
            ['Livraisons', 'Commande et quai attribué', 'Aucun accès aux bureaux', 'Active']
          ],
          cameras: {
            lobby: {
              label: 'Entrée principale', meta: '08 h 12', src: '/media/solutions/securite-intelligente.webp', alt: 'Entrée principale d’une entreprise', state: 'Visiteur attendu', type: 'Accueil et accès', confidence: 'Confiance contextuelle · 95 %', detection: 'Invitation + hôte + heure',
              headline: 'Un visiteur attendu arrive dans sa fenêtre d’accueil.', explanation: 'L’invitation, l’identité présentée, l’horaire et l’hôte concordent. L’accès reste limité au parcours prévu.',
              factors: [['VIS', 'Invitation valide', 'Réunion à 08 h 30 · accueil', 'Confirmé', 'good'], ['H1', 'Hôte disponible', 'Présent au siège social', 'Confirmé', 'good'], ['Z1', 'Zone autorisée', 'Accueil + salle 3 seulement', 'Limitée', 'good']],
              proposal: 'Imprimer un laissez-passer temporaire et aviser l’hôte. Aucun accès aux zones opérationnelles.', guardrail: 'Le laissez-passer expire automatiquement.', action: 'Admettre à l’accueil',
              summary: 'L’identité, le rendez-vous et l’hôte concordent; le périmètre reste limité.',
              timeline: [['08:11:46', 'Invitation retrouvée', 'Calendrier de l’hôte', 'Agenda', 'good'], ['08:11:53', 'Identité présentée', 'Correspondance avec l’invitation', 'Accueil', 'good'], ['08:12:01', 'Hôte présent sur le site', 'Appareil d’entreprise actif', 'Réseau', 'good'], ['08:12:07', 'Laissez-passer préparé', 'En attente du responsable', 'JARVIS', 'attention']]
            },
            perimeter: {
              label: 'Périmètre et stationnement', meta: '18 h 47', src: '/media/solutions/security-enterprise-parking-v1.webp', alt: 'Stationnement et accès de service d’un siège social', state: 'Véhicule à vérifier', type: 'Après les heures', confidence: 'Confiance contextuelle · 68 %', detection: 'Plaque inconnue + zone sensible',
              headline: 'Un véhicule non associé demeure près de l’accès de service.', explanation: 'Aucune livraison, visite ou plaque autorisée ne correspond. JARVIS rassemble les faits sans conclure à une menace.',
              factors: [['V?', 'Plaque non reconnue', 'Aucun véhicule enregistré', 'Inconnue', 'warning'], ['CAL', 'Calendrier des livraisons', 'Aucun créneau actif', 'Vide', 'warning'], ['P2', 'Zone de service', 'Fermée depuis 18 h', 'Sécurisée', 'good']],
              proposal: 'Afficher les vues voisines, aviser le responsable et conserver l’accès de service verrouillé.', guardrail: 'Aucune confrontation automatique.', action: 'Ouvrir la vérification',
              summary: 'La présence est inhabituelle, mais aucune tentative d’accès n’a été observée.',
              timeline: [['18:46:31', 'Véhicule observé', 'Stationnement de service', 'Caméra', 'attention'], ['18:46:39', 'Plaque sans correspondance', 'Listes locales consultées', 'Vision', 'attention'], ['18:46:48', 'Aucune livraison planifiée', 'Calendrier vérifié', 'Opérations', 'attention'], ['18:47:02', 'Accès maintenu verrouillé', 'Responsable à aviser', 'JARVIS', 'good']]
            },
            loading: {
              label: 'Réception sécurisée', meta: '10 h 04', src: '/media/solutions/security-enterprise-delivery-v1.webp', alt: 'Entrée logistique sécurisée d’un siège social', state: 'Livraison concordante', type: 'Fournisseur', confidence: 'Confiance contextuelle · 97 %', detection: 'Commande + plaque + accès',
              headline: 'La livraison correspond à la commande et à l’accès réservé.', explanation: 'JARVIS rapproche la commande, le fournisseur, le véhicule déclaré et la fenêtre d’arrivée avant de proposer un accès limité.',
              factors: [['PO', 'Commande active', 'PO-1842 · matériel attendu', 'Confirmé', 'good'], ['TR', 'Fournisseur attendu', 'Véhicule et entreprise concordants', 'Confirmé', 'good'], ['SAS', 'Entrée de service', 'Réservée pendant 35 minutes', 'Prête', 'good']],
              proposal: 'Déverrouiller le sas de réception, aviser le responsable et refermer automatiquement à la fin du créneau.', guardrail: 'L’accès demeure limité à la zone de réception.', action: 'Autoriser la réception',
              summary: 'Les informations physiques et opérationnelles concordent avec la livraison prévue.',
              timeline: [['10:03:32', 'Véhicule arrivé', 'Plaque déclarée reconnue', 'Caméra', 'good'], ['10:03:41', 'Commande PO-1842 active', 'Réception prévue aujourd’hui', 'ERP', 'good'], ['10:03:50', 'Sas de réception libre', 'Aucun conflit de réservation', 'Accès', 'good'], ['10:04:03', 'Accès temporaire préparé', 'Validation du responsable requise', 'JARVIS', 'attention']]
            },
            executive: {
              label: 'Étage direction', meta: '21 h 16', src: '/media/solutions/automatisation-operations.webp', alt: 'Étage de direction après les heures', state: 'Accès hors horaire', type: 'Zone restreinte', confidence: 'Confiance contextuelle · 91 %', detection: 'Badge valide + horaire inhabituel',
              headline: 'Un badge valide demande un accès inhabituel après les heures.', explanation: 'L’identité est autorisée, mais l’horaire et la zone ne correspondent pas au profil habituel. Une exception doit être expliquée et approuvée.',
              factors: [['EMP', 'Employé reconnu', 'Badge et appareil concordants', 'Confirmé', 'good'], ['HR', 'Horaire inhabituel', 'Aucune présence prévue', 'Écart', 'warning'], ['ZD', 'Zone direction', 'Accès sensible', 'Approbation', 'warning']],
              proposal: 'Contacter le responsable de garde, demander le motif et créer un accès exceptionnel limité dans le temps.', guardrail: 'Le badge valide ne suffit pas hors politique.', action: 'Demander une exception',
              summary: 'L’identité est certaine, mais le contexte ne respecte pas la politique d’accès.',
              timeline: [['21:15:42', 'Badge EMP reconnu', 'Identité et appareil concordants', 'Accès', 'good'], ['21:15:48', 'Horaire hors politique', 'Aucune présence prévue', 'Règle', 'attention'], ['21:15:55', 'Porte maintenue verrouillée', 'Aucun passage', 'Accès', 'good'], ['21:16:04', 'Exception proposée', 'Responsable de garde requis', 'JARVIS', 'attention']]
            },
            technical: {
              label: 'Local technique', meta: '14 h 23', src: '/media/solutions/reseau-resilience.webp', alt: 'Local technique sécurisé', state: 'Porte ouverte trop longtemps', type: 'Infrastructure critique', confidence: 'Confiance contextuelle · 93 %', detection: 'Accès + durée + équipement',
              headline: 'La porte du local technique demeure ouverte après le départ du technicien.', explanation: 'Le badge est valide et la maintenance est autorisée, mais la durée d’ouverture dépasse la politique de la zone critique.',
              factors: [['TEC', 'Technicien autorisé', 'Mandat M-228 actif', 'Confirmé', 'good'], ['D4', 'Porte technique', 'Ouverte depuis 6 min 42 s', 'Anomalie', 'warning'], ['ENV', 'Environnement', 'Température et réseau normaux', 'Stable', 'good']],
              proposal: 'Aviser le technicien et le responsable, afficher la caméra et fermer l’incident après confirmation de la porte.', guardrail: 'Aucun verrouillage si une personne est détectée dans la zone.', action: 'Lancer la vérification',
              summary: 'L’accès était légitime; seule la durée d’ouverture est anormale.',
              timeline: [['14:16:04', 'Badge technicien accepté', 'Mandat M-228 validé', 'Accès', 'good'], ['14:18:31', 'Technicien observé en sortie', 'Caméra intérieure', 'Vision', 'good'], ['14:22:46', 'Porte toujours ouverte', 'Seuil de 5 minutes dépassé', 'Capteur', 'attention'], ['14:23:01', 'Vérification préparée', 'Aucune fermeture automatique', 'JARVIS', 'attention']]
            }
          }
        }
      };

      let activeProfile = 'residential';
      let activeCamera = 'entry';
      const $ = (selector) => console.querySelector(selector);

      const renderIdentities = (profile) => {
        const target = $('[data-vision-identities]');
        if (!target) return;
        target.innerHTML = profile.identities.map(([code, title, copy, access, tone]) => `<article tabindex="0"><div class="identity-avatar ${tone}">${code}</div><h4>${title}</h4><p>${copy}</p><span>${access}</span></article>`).join('');
        const cards = [...target.querySelectorAll('article')];
        makeButtonLike(cards, (card) => {
          selectCard(cards, card);
          showFeedback(console, `${card.querySelector('h4')?.textContent} : facteurs et permissions affichés.`, 'Profil d’accès');
        });
      };

      const renderRules = (profile) => {
        const target = $('[data-vision-rules]');
        if (!target) return;
        target.innerHTML = profile.rules.map(([scope, title, copy, state]) => `<article tabindex="0" role="button" aria-pressed="true"><div><span>${scope}</span><b>${title}</b><small>${copy}</small></div><em>${state}</em></article>`).join('');
        target.querySelectorAll('article').forEach((card) => card.addEventListener('click', () => {
          const state = card.querySelector('em');
          const active = !card.classList.toggle('disabled');
          if (state) state.textContent = active ? 'Active' : 'En pause';
          card.setAttribute('aria-pressed', String(active));
          showFeedback(console, `${card.querySelector('b')?.textContent} : ${active ? 'règle active' : 'simulation mise en pause'}.`, 'Politique');
        }));
      };

      const renderTimeline = (camera, profile) => {
        const target = $('[data-vision-timeline]');
        if (!target) return;
        target.innerHTML = camera.timeline.map(([time, title, copy, source, tone]) => `<article tabindex="0"><time>${time}</time><i class="${tone}"></i><div><b>${title}</b><small>${copy}</small></div><span>${source}</span></article>`).join('');
        $('[data-vision-timeline-camera]').textContent = `${camera.label} · ${profile.label}`;
        $('[data-vision-timeline-summary]').textContent = camera.summary;
        const events = [...target.querySelectorAll('article')];
        makeButtonLike(events, (card) => {
          selectCard(events, card);
          showFeedback(console, `${card.querySelector('b')?.textContent} : source, preuve et règle associée ouvertes.`, 'Chronologie');
        });
      };

      const renderCamera = (key, announce = false) => {
        const profile = visionData[activeProfile];
        const camera = profile.cameras[key];
        if (!camera) return;
        activeCamera = key;
        visionRail.querySelectorAll('button').forEach((button) => button.classList.toggle('active', button.dataset.visionCamera === key));
        const image = $('[data-vision-image]');
        image.src = camera.src;
        image.alt = camera.alt;
        $('[data-vision-camera-label]').textContent = `${camera.label} · ${camera.meta}`;
        $('[data-vision-camera-state]').textContent = camera.state;
        $('[data-vision-event-type]').textContent = camera.type;
        $('[data-vision-headline]').textContent = camera.headline;
        $('[data-vision-explanation]').textContent = camera.explanation;
        $('[data-vision-confidence]').textContent = camera.confidence;
        $('[data-vision-detection-label]').textContent = camera.detection;
        $('[data-vision-site-label]').textContent = profile.site;
        $('[data-vision-proposal]').textContent = camera.proposal;
        $('[data-vision-guardrail]').textContent = camera.guardrail;
        const action = $('[data-vision-action]');
        action.textContent = camera.action;
        action.disabled = false;
        $('[data-vision-factors]').innerHTML = camera.factors.map(([code, title, copy, status, tone]) => `<article class="${tone}" tabindex="0"><i>${code}</i><div><b>${title}</b><small>${copy}</small></div><strong>${status}</strong></article>`).join('');
        renderTimeline(camera, profile);
        if (announce) showFeedback(console, `${camera.label} affichée. Image, contexte, preuves et chronologie sont maintenant synchronisés.`, 'JARVIS Vision');
      };

      const renderProfile = (profileKey, announce = false) => {
        activeProfile = profileKey;
        const profile = visionData[profileKey];
        const firstCamera = Object.keys(profile.cameras)[0];
        document.querySelectorAll('[data-vision-profile]').forEach((button) => button.classList.toggle('active', button.dataset.visionProfile === profileKey));
        $('[data-vision-system-state]').textContent = profile.system;
        $('[data-vision-profile-label]').textContent = profile.label;
        $('[data-vision-profile-detail]').textContent = profile.detail;
        $('[data-vision-rule-profile]').textContent = profile.ruleProfile;
        $('[data-vision-rule-summary]').textContent = profile.ruleSummary;
        visionRail.innerHTML = Object.entries(profile.cameras).map(([key, camera], index) => `<button class="${index === 0 ? 'active' : ''}" type="button" data-vision-camera="${key}"><img src="${camera.src}" alt=""><span><strong>${camera.label}</strong><small>${camera.meta} · ${camera.state}</small></span></button>`).join('');
        visionRail.querySelectorAll('button').forEach((button) => button.addEventListener('click', () => renderCamera(button.dataset.visionCamera, true)));
        renderIdentities(profile);
        renderRules(profile);
        renderCamera(firstCamera);
        if (announce) showFeedback(console, `Profil ${profile.label} chargé avec ses caméras, identités, règles et événements propres.`, 'Environnement');
      };

      console.querySelectorAll('[data-vision-profile]').forEach((button) => button.addEventListener('click', () => renderProfile(button.dataset.visionProfile, true)));
      $('[data-vision-action]')?.addEventListener('click', (event) => {
        const camera = visionData[activeProfile].cameras[activeCamera];
        event.currentTarget.textContent = 'Décision enregistrée';
        event.currentTarget.disabled = true;
        showFeedback(console, `${camera.action} : décision simulée et ajoutée au journal. Aucune action réelle n’a été exécutée.`, 'Action supervisée');
      });
      renderProfile('residential');
    }

    const networkMap = console.querySelector('[data-network-demo]');
    if (networkMap) {
      const recommendationButton = console.querySelector('.network-recommendation button');
      recommendationButton?.addEventListener('click', () => console.querySelector('[data-demo-tab="topology"]')?.click());
      const insight = networkMap.querySelector('.network-insight');
      if (insight) {
        const diagnose = document.createElement('button');
        diagnose.type = 'button';
        diagnose.className = 'network-diagnose';
        diagnose.textContent = 'Lancer les vérifications';
        insight.append(diagnose);
        diagnose.addEventListener('click', async () => {
          diagnose.disabled = true;
          const stages = ['Test de disponibilité...', 'Vérification du port et du VLAN...', 'Comparaison avec les changements récents...', 'Cause probable isolée'];
          for (const stage of stages) {
            diagnose.textContent = stage;
            await new Promise((resolve) => setTimeout(resolve, 350));
          }
          const action = networkMap.querySelector('[data-network-action]');
          if (action) action.textContent = 'Port 18 instable. Tester le câble avant tout remplacement.';
          showFeedback(console, 'Diagnostic terminé : le service global reste disponible et l’intervention est limitée au secteur Est.', 'Réseau');
          diagnose.textContent = 'Vérifications terminées';
        });
      }
      const devices = [...console.querySelectorAll('.network-device-table article')];
      makeButtonLike(devices, (card) => {
        selectCard(devices, card);
        showFeedback(console, `${card.querySelector('b')?.textContent || 'Appareil'} : identité, segment, port, historique et politiques affichés.`, 'Inventaire');
      });
      const changes = [...console.querySelectorAll('.network-change-list article')];
      makeButtonLike(changes, (card) => {
        selectCard(changes, card);
        showFeedback(console, `${card.querySelector('b')?.textContent || 'Changement'} relié aux métriques observées avant et après.`, 'Changement');
      });
    }

    const careIncidents = [...console.querySelectorAll('.care-incident-grid article')];
    if (careIncidents.length) {
      const cases = [
        {
          label: 'Dossier C-118 · ventilation cabine', title: 'La commande arrive, mais le ventilateur ne démarre pas.', result: 'Les mesures convergent vers F4. La confirmation physique reste requise avant de remplacer une pièce.',
          steps: [['Commande','Ordre reçu par le contrôleur','La scène et l’interface répondent.','Confirmé'],['Énergie','Batterie à 93 % · tension normale','Aucun délestage actif.','Confirmé'],['Circuit','Aucun courant après le fusible F4','Mesure locale horodatée.','Cause probable'],['Prochaine vérification','Inspecter F4 avant le relais et le moteur','Intervention physique requise.','À faire']],
          report: ['Ventilation cabine · diagnostic préliminaire','Commande valide, aucun démarrage du moteur.','Tension normale avant F4, absence de courant après F4.','Fusible F4 ouvert ou contact défectueux, à confirmer physiquement.','Aucune pièce remplacée et moteur non testé directement.']
        },
        {
          label: 'Dossier C-119 · caméra Est', title: 'La caméra alterne entre disponible et hors ligne depuis 14 h 22.', result: 'La perte se concentre sur le port 18 et son câble. La caméra demeure fonctionnelle lorsqu’elle est reliée ailleurs.',
          steps: [['Service','Flux vidéo disponible par intermittence','Le service de vision redémarre sans erreur.','Confirmé'],['Énergie','Alimentation PoE stable','Aucune coupure électrique observée.','Confirmé'],['Réseau','18 % de perte sur le port 18','Les autres ports du commutateur sont stables.','Cause probable'],['Prochaine vérification','Tester le câble puis déplacer le port','Aucun remplacement de caméra proposé.','À faire']],
          report: ['Caméra Est · diagnostic préliminaire','Flux vidéo intermittent depuis 14 h 22.','PoE stable; perte de paquets limitée au port 18.','Câble ou port réseau instable, à confirmer par permutation contrôlée.','Aucune configuration ni caméra remplacée.']
        },
        {
          label: 'Dossier C-120 · transmission', title: 'La température augmente plus vite que son historique lors des montées.', result: 'La dérive est préventive : charge et pente n’expliquent pas entièrement l’écart. Une inspection du niveau et du refroidissement est proposée.',
          steps: [['Capteur','Température confirmée par lectures successives','Aucun saut ni valeur impossible.','Confirmé'],['Contexte','Pente, charge et température extérieure comparées','Le trajet est comparable à six trajets précédents.','Confirmé'],['Tendance','Hausse de 14 °C au-dessus de la référence','Aucun code moteur enregistré.','À surveiller'],['Prochaine vérification','Contrôler le niveau et le circuit de refroidissement','Inspection avant le prochain long trajet.','À faire']],
          report: ['Transmission · observation préventive','Température plus élevée que l’historique lors des montées.','Lectures cohérentes; écart de 14 °C à contexte comparable.','Dérive thermique à investiguer avant apparition d’un code.','Aucun diagnostic mécanique définitif sans inspection.']
        }
      ];
      let activeCareCase = 0;
      makeButtonLike(careIncidents, (card, index) => {
        selectCard(careIncidents, card);
        activeCareCase = index;
        const panelTitle = console.querySelector('.care-diagnosis-head span');
        const panelCopy = console.querySelector('.care-diagnosis-head h3');
        if (panelTitle) panelTitle.textContent = cases[index].label;
        if (panelCopy) panelCopy.textContent = cases[index].title;
        console.querySelectorAll('.care-diagnostic-flow article').forEach((step, stepIndex) => {
          const values = cases[index].steps[stepIndex];
          if (!values) return;
          const kind = step.querySelector('span');
          const title = step.querySelector('strong');
          const copy = step.querySelector('small');
          const state = step.querySelector('em');
          if (kind) kind.textContent = values[0];
          if (title) title.textContent = values[1];
          if (copy) copy.textContent = values[2];
          if (state) state.textContent = values[3];
        });
        const reportTitle = console.querySelector('.care-report h4');
        if (reportTitle) reportTitle.textContent = cases[index].report[0];
        console.querySelectorAll('.care-report article p').forEach((paragraph, paragraphIndex) => paragraph.textContent = cases[index].report[paragraphIndex + 1]);
        console.querySelector('[data-demo-tab="diagnosis"]')?.click();
      });
      const flow = console.querySelector('.care-diagnostic-flow');
      if (flow) {
        const run = document.createElement('button');
        run.type = 'button';
        run.className = 'care-run-diagnostic';
        run.textContent = 'Rejouer le diagnostic';
        flow.before(run);
        run.addEventListener('click', async () => {
          const steps = [...flow.querySelectorAll('article')];
          steps.forEach((step) => step.classList.remove('passed', 'current'));
          run.disabled = true;
          for (const step of steps) {
            step.classList.add('current');
            await new Promise((resolve) => setTimeout(resolve, 420));
            step.classList.remove('current');
            step.classList.add('passed');
          }
          run.disabled = false;
          run.textContent = 'Diagnostic rejoué';
          showFeedback(console, cases[activeCareCase].result, 'Diagnostic');
        });
      }
      const equipment = [...console.querySelectorAll('.care-equipment-grid article')];
      makeButtonLike(equipment, (card) => {
        selectCard(equipment, card);
        showFeedback(console, `${card.querySelector('b')?.textContent || 'Équipement'} : dépendances, télémétrie, documentation et historique ouverts.`, 'Équipement');
      });
      const report = console.querySelector('.care-report');
      if (report) {
        const exportButton = document.createElement('button');
        exportButton.type = 'button';
        exportButton.className = 'care-export-report';
        exportButton.textContent = 'Préparer le partage';
        report.append(exportButton);
        exportButton.addEventListener('click', () => {
          exportButton.textContent = 'Rapport prêt · destinataire à choisir';
          showFeedback(console, 'Le rapport sépare les faits, les hypothèses, les limites et les actions exécutées.', 'Rapport');
        });
      }
    }
  });

  document.querySelectorAll('.fabric-console').forEach((console) => {
    const panels = [...console.querySelectorAll('[data-demo-panel]')];
    panels.forEach((panel) => {
      const cards = [...panel.querySelectorAll('.fabric-signal-row article, .fabric-event-flow article')];
      makeButtonLike(cards, (card) => {
        selectCard(cards, card);
        const label = card.querySelector('span')?.textContent || 'Signal';
        const value = card.querySelector('b')?.textContent || '';
        showFeedback(console, `${label} : ${value}. Source et permission ouvertes dans la simulation.`, 'Fabric');
      });
      const action = panel.querySelector('[data-preview-action]');
      action?.addEventListener('click', () => {
        panel.classList.add('simulation-complete');
        const title = panel.querySelector('h3')?.textContent || 'Plan coordonné';
        showFeedback(console, `${title} Le plan a été transmis uniquement aux environnements autorisés; chacun conserve son autonomie.`, 'Coordination');
      });
    });
  });

  document.querySelectorAll('.personal-console').forEach((console) => {
    console.querySelectorAll('[data-preview-action]').forEach((button) => button.addEventListener('click', () => {
      const action = button.closest('.personal-case-action')?.querySelector('strong')?.textContent || 'La proposition a été ajoutée au plan personnel.';
      showFeedback(console, `${action} Vous pouvez la modifier ou la retirer.`, 'Plan personnel');
    }));
    const goalCards = [...console.querySelectorAll('.impact-goals article')];
    makeButtonLike(goalCards, (card) => {
      const enabled = !card.classList.toggle('disabled');
      card.setAttribute('aria-pressed', String(enabled));
      const state = card.querySelector('strong');
      if (state) state.textContent = enabled ? 'Actif' : 'En pause';
      showFeedback(console, `${card.querySelector('h4')?.textContent || 'Objectif'} : ${enabled ? 'suivi actif' : 'suivi mis en pause'}.`, 'Objectif');
    });
    const habitCards = [...console.querySelectorAll('.impact-habits article')];
    makeButtonLike(habitCards, (card) => {
      selectCard(habitCards, card);
      showFeedback(console, `${card.querySelector('h4')?.textContent || 'Habitude'} : tendance, contexte et prochaine petite action affichés.`, 'Habitude');
    });
    console.querySelectorAll('.impact-money button').forEach((button) => button.addEventListener('click', () => {
      button.disabled = true;
      button.textContent = 'Plan préparé';
      showFeedback(console, 'Le scénario compare l’intention, la tendance et la prochaine décision sans effectuer de transaction.', 'Dépenses');
    }));
    console.querySelector('.impact-learning button')?.addEventListener('click', (event) => {
      event.currentTarget.disabled = true;
      event.currentTarget.textContent = 'Parcours préparé';
      showFeedback(console, 'Le contenu autorisé est découpé en prochaines étapes, avec rappel et mesure du progrès.', 'Progression');
    });
    console.querySelectorAll('.personal-source-grid article').forEach((card) => {
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.addEventListener('click', () => {
        const disabled = card.classList.toggle('disabled');
        card.setAttribute('aria-pressed', String(!disabled));
        showFeedback(console, `${card.querySelector('b')?.textContent || 'Source'} : ${disabled ? 'retirée' : 'autorisée'} pour les recommandations futures.`, 'Contrôle');
      });
    });
  });

  document.querySelectorAll('.sp-console').forEach((console) => {
    const osintPanel = console.querySelector('[data-demo-panel="osint"]');
    if (osintPanel) {
      const controls = document.createElement('div');
      controls.className = 'sp-interactive-controls';
      controls.innerHTML = '<span>Explorer les preuves publiques</span><button class="active" type="button">Domaines</button><button type="button">Identités</button><button type="button">Fournisseurs</button>';
      osintPanel.querySelector('.sp-panel-head')?.after(controls);
      controls.querySelectorAll('button').forEach((button) => button.addEventListener('click', () => {
        controls.querySelectorAll('button').forEach((item) => item.classList.toggle('active', item === button));
        const messages = {
          Domaines: 'Domaines, sous-domaines, certificats et services publics corrélés avec leur source.',
          Identités: 'Mentions publiques et rôles professionnels séparés des hypothèses non confirmées.',
          Fournisseurs: 'Dépendances externes visibles, propriété à confirmer avant toute conclusion.'
        };
        showFeedback(console, messages[button.textContent], 'OSINT');
      }));
      const assets = [...osintPanel.querySelectorAll('.sp-source-stack article, .sp-asset-map button, .sp-asset-map article')];
      makeButtonLike(assets, (card) => {
        selectCard(assets, card);
        showFeedback(console, 'Élément sélectionné : source, horodatage, relation et niveau de confiance affichés.', 'Preuve publique');
      });
    }

    const surfacePanel = console.querySelector('[data-demo-panel="surface"]');
    if (surfacePanel) {
      const findings = [...surfacePanel.querySelectorAll('.sp-exposure-list article, .sp-finding')];
      makeButtonLike(findings, (card) => {
        selectCard(findings, card);
        const title = card.querySelector('strong, b')?.textContent || 'Constat';
        showFeedback(console, `${title} : actif, preuve, impact possible et propriétaire à confirmer sont séparés.`, 'Surface exposée');
      });
    }

    const pentestPanel = console.querySelector('[data-demo-panel="pentest"]');
    if (pentestPanel) {
      const run = document.createElement('button');
      run.type = 'button';
      run.className = 'sp-run-validation';
      run.textContent = 'Autoriser et simuler la validation';
      pentestPanel.querySelector('.sp-test-summary')?.append(run);
      run.addEventListener('click', async () => {
        const steps = [...pentestPanel.querySelectorAll('.sp-test-sequence article')];
        run.disabled = true;
        for (const step of steps) {
          step.classList.add('running');
          await new Promise((resolve) => setTimeout(resolve, 420));
          step.classList.remove('running');
          step.classList.add('passed');
        }
        run.textContent = 'Validation terminée · aucune donnée modifiée';
        setConsoleStatus(console, 'Test autorisé terminé · preuves conservées');
        showFeedback(console, 'Le contrôle approuvé a été exécuté dans ses limites; le résultat est prêt pour remédiation et retest.', 'Pentest autorisé');
      });
    }

    const reportPanel = console.querySelector('[data-demo-panel="report"]');
    if (reportPanel) {
      const actionArea = reportPanel.querySelector('.sp-report-actions') || reportPanel.querySelector('.sp-report');
      if (actionArea) {
        const prepare = document.createElement('button');
        prepare.type = 'button';
        prepare.className = 'sp-prepare-report';
        prepare.textContent = 'Préparer le dossier exécutif';
        actionArea.append(prepare);
        prepare.addEventListener('click', () => {
          prepare.textContent = 'Dossier prêt · diffusion non autorisée';
          showFeedback(console, 'Résumé exécutif, preuves techniques, plan de correction et retest sont réunis sans envoi externe.', 'Rapport');
        });
      }
    }
  });

  document.querySelectorAll('[data-ops-console]').forEach((console) => {
    console.querySelectorAll('[data-ops-go]').forEach((button) => {
      button.addEventListener('click', () => {
        console.querySelector(`[data-demo-tab="${button.dataset.opsGo}"]`)?.click();
      });
    });

    console.querySelectorAll('[data-ops-toggle]').forEach((button) => {
      button.setAttribute('aria-pressed', String(button.classList.contains('active')));
      button.addEventListener('click', () => {
        const active = button.classList.toggle('active');
        button.setAttribute('aria-pressed', String(active));
        button.textContent = active ? 'Actif' : 'En pause';
      });
    });

    console.querySelector('[data-preview-action]')?.addEventListener('click', () => {
      const approvalCount = console.querySelector('.ops-sidebar .attention');
      const approvalShortcut = console.querySelector('.ops-topbar [data-ops-go="approvals"]');
      if (approvalCount) approvalCount.textContent = '1';
      if (approvalShortcut) approvalShortcut.textContent = '1 à approuver';
    });
  });

  document.querySelectorAll('[data-automation-studio]').forEach((studio) => {
    const flows = {
      service: {
        name: 'Traiter une demande de service',
        goal: 'Une demande devient une mission complète, planifiable et prête à être approuvée.',
        process: 'Comprendre la demande et vérifier le client',
        processCopy: 'Le client, le lieu, l’urgence et les doublons sont vérifiés dans le CRM.',
        description: 'Transformer un courriel ou un formulaire en dossier prêt à planifier, sans recopier les informations.',
        health: 'Actif · 98 % de réussite',
        version: 'Version publiée · v6',
        input: 'Boîte demandes@ · formulaire Web',
        output: 'CRM · calendrier · brouillon courriel',
        guard: 'Aucun envoi sans validation humaine',
        nodes: [
          ['EM','Déclencheur','Courriel reçu','Microsoft 365 / IMAP','Le flux démarre lorsqu’un nouveau message arrive dans la boîte autorisée et correspond aux règles de tri.','Microsoft 365 ou serveur IMAP','Expéditeur, objet, corps et pièces jointes','Un événement horodaté avec le message original','Lecture de la boîte choisie seulement'],
          ['IA','Comprendre','Extraire la demande','Texte + pièces jointes','JARVIS extrait le client, le lieu, le besoin, l’urgence et les documents sans modifier le message original.','Message original et pièces jointes','Texte, PDF, images et métadonnées','Champs structurés avec niveau de confiance','Traitement local; Internet désactivé par défaut'],
          ['RG','Vérifier','Client et doublon','CRM + règles','Les champs obligatoires, le client existant, les doublons et le niveau de service sont vérifiés avant de continuer.','CRM et règles de l’entreprise','Identité, adresse, demandes récentes, contrat','Dossier validé ou exception dirigée vers la file','Lecture CRM; aucune fusion automatique'],
          ['OK','Décider','Approbation','Avant communication','Une personne voit le message, la mission proposée et les preuves avant toute communication externe.','Dossier préparé par les étapes précédentes','Mission, horaire, destinataire et brouillon','Décision horodatée avec commentaire','Approbateur autorisé seulement'],
          ['MS','Destination','Créer la mission','CRM + calendrier','Après approbation, JARVIS crée la mission, réserve la plage et envoie le message approuvé.','Décision humaine approuvée','Dossier, date, équipe et message final','Mission CRM, événement calendrier et courriel','Écriture limitée aux objets du flux']
        ]
      },
      invoice: {
        name: 'Traiter une facture fournisseur',
        goal: 'Une facture vérifiée devient un brouillon comptable, sans déclencher de paiement.',
        process: 'Lire la facture et la rapprocher de la commande',
        processCopy: 'Le fournisseur, les montants, les taxes, la commande et les écarts sont vérifiés.',
        description: 'Lire la facture, vérifier le fournisseur et le bon de commande, puis préparer l’écriture comptable.',
        health: 'Actif · 96 % de réussite',
        version: 'Version publiée · v3',
        input: 'Boîte factures@ · dépôt PDF',
        output: 'Comptabilité · dossier fournisseur',
        guard: 'Approbation si exception ou montant supérieur à 2 500 $',
        nodes: [
          ['PDF','Déclencheur','Facture reçue','Courriel / dépôt','Le flux démarre lorsqu’un PDF est reçu dans une source autorisée.','Boîte factures ou dossier surveillé','Message, PDF et identité de la source','Document original horodaté','Lecture de la source choisie'],
          ['OCR','Comprendre','Lire les champs','OCR + extraction','Le fournisseur, les lignes, les taxes, le total, la date et le numéro de facture sont extraits.','Document PDF original','Texte et structure de la facture','Champs comptables avec confiance','Traitement local lorsque possible'],
          ['3V','Vérifier','Rapprochement','Fournisseur + commande','Le fournisseur, les doublons, le bon de commande et les écarts de montant sont contrôlés.','Comptabilité et commandes','Fournisseur, historique, commande, réception','Facture conforme ou exception expliquée','Lecture financière limitée au rapprochement'],
          ['OK','Décider','Approbation financière','Seuils + exceptions','Les factures hors tolérance ou au-dessus du seuil attendent la personne responsable.','Facture et preuves de rapprochement','Montant, écarts et pièces justificatives','Décision avec commentaire','Rôle financier autorisé'],
          ['ACC','Destination','Créer le brouillon','Comptabilité','Une écriture en brouillon et le dossier de preuve sont créés après validation.','Facture validée et approbation','Comptes, taxes, fournisseur et échéance','Écriture brouillon; aucun paiement','Création de brouillon seulement']
        ]
      },
      lead: {
        name: 'Qualifier et assigner un prospect',
        goal: 'Une nouvelle demande devient un suivi commercial attribué à la bonne personne.',
        process: 'Qualifier la demande et vérifier le contact',
        processCopy: 'Le besoin, le territoire, le consentement et les doublons sont vérifiés dans le CRM.',
        description: 'Réunir les demandes Web et courriel, éliminer les doublons et assigner le bon suivi.',
        health: 'Actif · 99 % de réussite',
        version: 'Version publiée · v4',
        input: 'Formulaire Web · boîte ventes@',
        output: 'CRM · tâche commerciale · brouillon',
        guard: 'Aucun contact automatique sans consentement valide',
        nodes: [
          ['WEB','Déclencheur','Nouvelle demande','Formulaire / courriel','Le flux démarre avec une demande soumise ou un courriel adressé aux ventes.','Site Web ou messagerie','Coordonnées, message et consentement','Demande normalisée','Lecture du canal de vente seulement'],
          ['IA','Comprendre','Qualifier le besoin','Classification','JARVIS classe le besoin, le secteur, l’échéance et les informations manquantes.','Demande originale','Texte et champs du formulaire','Résumé, catégorie et questions manquantes','IA locale ou service explicitement autorisé'],
          ['CRM','Vérifier','Contact et doublon','CRM','Le contact et l’organisation sont recherchés avant de créer une nouvelle fiche.','CRM commercial','Courriel, téléphone et organisation','Contact existant ou fiche proposée','Lecture et proposition; aucune fusion'],
          ['RT','Décider','Routage','Territoire + charge','Les règles choisissent l’équipe selon le besoin, le territoire et la disponibilité.','Règles commerciales et calendrier','Catégorie, région et capacité','Responsable proposé et délai cible','Routage automatique réversible'],
          ['CRM','Destination','Créer le suivi','CRM + tâches','Le prospect, la tâche et un brouillon personnalisé sont créés pour le responsable.','Demande qualifiée','Résumé, propriétaire et échéance','Prospect CRM et tâche de rappel','Aucun envoi sans consentement']
        ]
      },
      onboarding: {
        name: 'Préparer l’arrivée d’un employé',
        goal: 'Une embauche confirmée devient un plan d’arrivée coordonné et contrôlé.',
        process: 'Préparer le plan et séparer les accès',
        processCopy: 'Les tâches, le matériel et chaque demande d’accès sont dirigés vers leur responsable.',
        description: 'Coordonner les tâches RH, les accès, le matériel et l’accueil à partir d’une date confirmée.',
        health: 'Brouillon · connexions à terminer',
        version: 'Brouillon · v1',
        input: 'Dossier RH approuvé',
        output: 'Répertoire · TI · tâches · calendrier',
        guard: 'Les accès sensibles exigent le propriétaire du système',
        nodes: [
          ['RH','Déclencheur','Embauche confirmée','Système RH','Le flux démarre uniquement après la confirmation du dossier par une personne autorisée.','Système RH','Nom, rôle, équipe, gestionnaire et date','Événement d’arrivée confirmé','Lecture des champs nécessaires seulement'],
          ['PL','Comprendre','Préparer le plan','Rôle + politiques','JARVIS sélectionne la liste de tâches correspondant au rôle et au site.','Modèles internes autorisés','Rôle, site et date de début','Plan d’arrivée détaillé','Aucune décision RH autonome'],
          ['RG','Vérifier','Séparer les accès','Moindre privilège','Chaque accès est comparé au rôle et dirigé vers son propriétaire.','Répertoire et catalogue d’accès','Groupes, licences et matériel requis','Demandes d’accès distinctes','Lecture du catalogue; aucune élévation'],
          ['OK','Décider','Approbations ciblées','RH + TI + gestionnaire','Les responsables approuvent uniquement les éléments dont ils sont propriétaires.','Plan et demandes séparées','Accès, matériel et communications','Décisions par responsable','Validation selon le système'],
          ['ON','Destination','Orchestrer l’arrivée','Tâches + calendrier','Les tâches, rendez-vous et demandes approuvées sont créés avec suivi des retards.','Décisions approuvées','Responsables, dates et instructions','Plan d’accueil et journal complet','Écriture limitée aux éléments approuvés']
        ]
      },
      direction: {
        name: 'Coordonner un renouvellement client',
        goal: 'Une échéance contractuelle devient un suivi commercial complet, attribué et supervisé.',
        process: 'Vérifier le contrat, le compte et les actions requises',
        processCopy: 'JARVIS rassemble uniquement les données nécessaires avant de proposer le parcours de renouvellement.',
        description: 'Détecter une échéance, vérifier le dossier client, créer les tâches et préparer le message de renouvellement.',
        health: 'Actif · 97 % de réussite',
        version: 'Version publiée · v3',
        input: 'CRM · contrats · calendrier',
        output: 'CRM · tâches · calendrier · brouillon courriel',
        guard: 'Aucun engagement ni message externe sans approbation',
        nodes: [
          ['EC','Déclencheur','Échéance à 60 jours','CRM + contrats','Le flux démarre lorsqu’un contrat actif entre dans la fenêtre de renouvellement définie.','CRM et registre contractuel','Client, contrat, date et responsable','Événement de renouvellement horodaté','Lecture des contrats actifs seulement'],
          ['IA','Comprendre','Préparer le contexte','Compte + historique','JARVIS résume les engagements, demandes ouvertes et changements pertinents pour ce renouvellement.','CRM et base de connaissances','Contrat, activités et demandes liées','Contexte sourcé pour le responsable','Lecture limitée au compte concerné'],
          ['RG','Vérifier','Contrôler le parcours','Règles commerciales','Le propriétaire du compte, les tâches obligatoires, les délais et les doublons sont vérifiés.','CRM, calendrier et règles','Responsable, disponibilité et étapes','Parcours conforme ou exception','Aucune modification à cette étape'],
          ['OK','Décider','Valider le suivi','Avant communication','Le responsable approuve l’approche, l’échéancier et le brouillon avant tout contact externe.','Dossier de renouvellement','Message, tâches et dates proposées','Décision horodatée','Responsable du compte seulement'],
          ['CRM','Destination','Lancer le renouvellement','CRM + calendrier','Après approbation, JARVIS crée les tâches, réserve le suivi et enregistre le brouillon approuvé.','Décision approuvée','Responsable, échéances et message','Tâches et suivi CRM créés','Écriture limitée au compte concerné']
        ]
      },
      incident: {
        name: 'Coordonner un incident opérationnel',
        goal: 'Une anomalie devient une réponse structurée, supervisée et documentée.',
        process: 'Rassembler le contexte et proposer la réponse',
        processCopy: 'Les alertes, changements récents, procédures et responsables sont réunis avant toute action.',
        description: 'Détecter une anomalie, comprendre son impact et guider une réponse sans improvisation.',
        health: 'Actif · surveillance continue',
        version: 'Version pilote · v2',
        input: 'Alertes · opérations · procédures · calendrier',
        output: 'Dossier incident · tâches · communications préparées',
        guard: 'Aucun arrêt de service ni message externe sans autorisation',
        nodes: [
          ['AL','Déclencheur','Anomalie détectée','Système autorisé','Le flux démarre lorsqu’une alerte dépasse le seuil défini ou qu’un responsable signale un incident.','Supervision et formulaires','Alerte, heure, site et service touché','Événement incident horodaté','Lecture des systèmes concernés'],
          ['IA','Comprendre','Évaluer l’impact','Services + contexte','JARVIS relie l’incident aux dépendances, aux activités en cours et aux changements récents.','Événement et inventaire','Impact, dépendances et historique','Périmètre probable et confiance','Les hypothèses restent visibles'],
          ['RG','Vérifier','Préparer la réponse','Procédures + responsables','Les procédures autorisées et les personnes responsables sont sélectionnées selon la situation.','Documentation interne','Procédures, astreinte et contraintes','Plan de réponse proposé','Aucune procédure improvisée'],
          ['OK','Décider','Autoriser l’action','Impact expliqué','La personne responsable voit les conséquences avant un arrêt, une correction ou une communication.','Plan et preuves','Action, portée et retour arrière','Décision horodatée','Approbateur du service seulement'],
          ['IR','Destination','Exécuter et suivre','Tâches + journal','Les actions approuvées sont lancées, suivies puis ajoutées au rapport d’incident.','Décision approuvée','Tâches, messages et état du service','Incident suivi et documenté','Écriture limitée au plan approuvé']
        ]
      }
    };

    const cases = {
      service: {
        request: '« Le client demande une intervention urgente demain matin pour le système du site de Montréal. »',
        confidence: '96 %',
        facts: [['Client','Groupe Atlas'],['Priorité','Élevée'],['Site','Montréal'],['Contrat','Actif'],['Technicien','Disponible à 08 h 30'],['Source','Courriel + 3 photos']],
        prepares: ['Mission dans le CRM','Plage au calendrier','Technicien proposé','Brouillon au client','Documents associés'],
        decision: 'Autoriser la mission et l’envoi du message',
        results: ['Mission créée','Calendrier mis à jour','CRM mis à jour','Courriel envoyé','Journal d’audit enregistré']
      },
      invoice: {
        request: '« Facture de 8 420 $ reçue. Le montant dépasse la commande approuvée de 640 $. »',
        confidence: '99 %',
        facts: [['Fournisseur','Nordex Services'],['Montant','8 420 $'],['Commande','PO-2841'],['Écart','+ 640 $'],['Réception','Confirmée'],['Échéance','18 octobre']],
        prepares: ['Champs comptables','Rapprochement de commande','Exception documentée','Brouillon comptable','Dossier de preuve'],
        decision: 'Accepter l’écart ou retourner la facture au fournisseur',
        results: ['Décision enregistrée','Brouillon créé','Pièces associées','Échéance planifiée','Journal d’audit enregistré']
      },
      lead: {
        request: '« Nous cherchons à automatiser trois sites et souhaitons une rencontre cette semaine. »',
        confidence: '93 %',
        facts: [['Organisation','Groupe Meridian'],['Besoin','Automatisation multi-sites'],['Territoire','Québec'],['Échéance','Cette semaine'],['Doublon','Aucun'],['Consentement','Confirmé']],
        prepares: ['Fiche CRM','Résumé du besoin','Priorité commerciale','Responsable proposé','Brouillon de suivi'],
        decision: 'Assigner le prospect et autoriser le premier contact',
        results: ['Prospect créé','Responsable assigné','Tâche planifiée','Brouillon approuvé','Journal d’audit enregistré']
      },
      onboarding: {
        request: '« L’arrivée de la nouvelle responsable des opérations est confirmée pour lundi. »',
        confidence: '100 %',
        facts: [['Rôle','Responsable des opérations'],['Début','Lundi · 08 h 30'],['Site','Siège social'],['Gestionnaire','Direction générale'],['Matériel','Portable + téléphone'],['Accès','6 demandes ciblées']],
        prepares: ['Plan d’accueil','Demandes d’accès','Matériel réservé','Rencontres au calendrier','Tâches aux responsables'],
        decision: 'Approuver séparément les accès et le plan d’arrivée',
        results: ['Plan publié','Matériel réservé','Tâches distribuées','Calendrier préparé','Journal d’audit enregistré']
      },
      direction: {
        request: '« Le contrat du Groupe Horizon arrive à échéance dans 60 jours. »',
        confidence: '98 %',
        facts: [['Client','Groupe Horizon'],['Échéance','28 novembre'],['Responsable','Compte Entreprise'],['Demandes ouvertes','2'],['Renouvellement','Approbation requise'],['Dernier contact','Il y a 21 jours']],
        prepares: ['Dossier de renouvellement','Tâches du responsable','Plage de suivi','Brouillon au client','Échéances dans le CRM'],
        decision: 'Approuver le parcours et le premier message au client',
        results: ['Tâches créées','Suivi planifié','Brouillon approuvé','CRM mis à jour','Journal d’audit enregistré']
      },
      incident: {
        request: '« Le traitement des commandes ralentit depuis 14 h 08 et deux équipes sont touchées. »',
        confidence: '91 %',
        facts: [['Impact','2 équipes'],['Service','Traitement des commandes'],['Début','14 h 08'],['Changement récent','Connecteur mis à jour'],['Contournement','Disponible'],['Responsable','Opérations TI']],
        prepares: ['Dossier incident','Chronologie des événements','Cause probable','Plan de contournement','Message interne préparé'],
        decision: 'Autoriser le contournement et informer les équipes',
        results: ['Contournement activé','Service stabilisé','Équipes informées','Analyse planifiée','Rapport d’incident créé']
      }
    };

    const viewButtons = [...studio.querySelectorAll('[data-ops-view]')];
    const navButtons = [...studio.querySelectorAll('.automation-studio-nav [data-ops-view]')];
    const viewPanels = [...studio.querySelectorAll('[data-ops-view-panel]')];
    const nodeButtons = [...studio.querySelectorAll('[data-flow-node]')];
    const flowModeButtons = [...studio.querySelectorAll('[data-flow-mode]')];
    const flowModePanels = [...studio.querySelectorAll('[data-flow-mode-panel]')];
    const flowLayout = studio.querySelector('[data-flow-layout]');
    let currentFlow = 'service';

    const showView = (view) => {
      navButtons.forEach((button) => button.classList.toggle('active', button.dataset.opsView === view));
      viewPanels.forEach((panel) => panel.hidden = panel.dataset.opsViewPanel !== view);
    };

    const showNode = (index) => {
      const node = flows[currentFlow].nodes[index];
      if (!node) return;
      nodeButtons.forEach((button, buttonIndex) => button.classList.toggle('selected', buttonIndex === index));
      const values = {
        '[data-inspector-step]': `${String(index + 1).padStart(2, '0')} / 05`,
        '[data-inspector-code]': node[0],
        '[data-inspector-kind]': node[1],
        '[data-inspector-title]': node[2],
        '[data-inspector-description]': node[4],
        '[data-inspector-source]': node[5],
        '[data-inspector-input]': node[6],
        '[data-inspector-output]': node[7],
        '[data-inspector-permission]': node[8]
      };
      Object.entries(values).forEach(([selector, value]) => {
        const element = studio.querySelector(selector);
        if (element) element.textContent = value;
      });
    };

    const showFlowMode = (mode) => {
      flowModeButtons.forEach((button) => button.classList.toggle('active', button.dataset.flowMode === mode));
      flowModePanels.forEach((panel) => panel.hidden = panel.dataset.flowModePanel !== mode);
      flowLayout?.classList.toggle('design-mode', mode === 'design');
    };

    const renderFlow = (flowKey) => {
      const flow = flows[flowKey];
      if (!flow) return;
      const caseStudy = cases[flowKey];
      currentFlow = flowKey;
      const values = {
        '[data-flow-name]': flow.name,
        '[data-flow-description]': flow.description,
        '[data-flow-health]': flow.health,
        '[data-flow-version]': flow.version,
        '[data-flow-input]': flow.input,
        '[data-flow-output]': flow.output,
        '[data-flow-guard]': flow.guard,
        '[data-summary-goal]': flow.goal,
        '[data-summary-source-code]': flow.nodes[0][0],
        '[data-summary-source]': flow.nodes[0][2],
        '[data-summary-source-meta]': flow.nodes[0][3],
        '[data-summary-process]': flow.process,
        '[data-summary-process-meta]': flow.processCopy,
        '[data-summary-approval]': flow.nodes[3][2],
        '[data-summary-approval-meta]': flow.nodes[3][4],
        '[data-summary-result-code]': flow.nodes[4][0],
        '[data-summary-result]': flow.nodes[4][2],
        '[data-summary-result-meta]': flow.nodes[4][4],
        '[data-summary-read]': flow.input,
        '[data-summary-write]': flow.output,
        '[data-summary-guard]': flow.guard,
        '[data-summary-health]': flow.health.replace('Actif · ', '')
      };
      Object.entries(values).forEach(([selector, value]) => {
        const element = studio.querySelector(selector);
        if (element) element.textContent = value;
      });
      if (caseStudy) {
        const request = studio.querySelector('[data-case-request]');
        const confidence = studio.querySelector('[data-case-confidence]');
        const decision = studio.querySelector('[data-case-decision]');
        if (request) request.textContent = caseStudy.request;
        if (confidence) confidence.textContent = caseStudy.confidence;
        if (decision) decision.textContent = caseStudy.decision;
        caseStudy.facts.forEach(([label, value], index) => {
          const labelElement = studio.querySelector(`[data-fact-label="${index}"]`);
          const valueElement = studio.querySelector(`[data-fact-value="${index}"]`);
          if (labelElement) labelElement.textContent = label;
          if (valueElement) valueElement.textContent = value;
        });
        caseStudy.prepares.forEach((item, index) => {
          const element = studio.querySelector(`[data-prepare-item="${index}"]`);
          if (element) element.textContent = item;
        });
        caseStudy.results.forEach((item, index) => {
          const element = studio.querySelector(`[data-result-item="${index}"]`);
          if (element) element.textContent = item;
        });
      }
      nodeButtons.forEach((button, index) => {
        const node = flow.nodes[index];
        button.querySelector('[data-node-code]').textContent = node[0];
        button.querySelector('[data-node-kind]').textContent = node[1];
        button.querySelector('[data-node-title]').textContent = node[2];
        button.querySelector('[data-node-meta]').textContent = node[3];
        button.classList.remove('running', 'passed');
      });
      studio.querySelectorAll('.automation-flow-library [data-flow-select]').forEach((button) => button.classList.toggle('active', button.dataset.flowSelect === flowKey));
      const result = studio.querySelector('[data-test-result]');
      if (result) result.hidden = true;
      const caseResult = studio.querySelector('[data-case-result]');
      const caseApprove = studio.querySelector('[data-case-approve]');
      if (caseResult) caseResult.hidden = true;
      if (caseApprove) {
        caseApprove.disabled = false;
        caseApprove.textContent = 'Autoriser l’exécution';
      }
      showNode(0);
      showFlowMode('overview');
    };

    viewButtons.forEach((button) => button.addEventListener('click', () => showView(button.dataset.opsView)));
    studio.querySelectorAll('[data-flow-select]').forEach((button) => button.addEventListener('click', () => {
      renderFlow(button.dataset.flowSelect);
      showView('automations');
    }));
    nodeButtons.forEach((button, index) => button.addEventListener('click', () => showNode(index)));
    flowModeButtons.forEach((button) => button.addEventListener('click', () => showFlowMode(button.dataset.flowMode)));
    studio.querySelectorAll('[data-open-flow]').forEach((button) => button.addEventListener('click', () => {
      renderFlow(button.dataset.openFlow);
      showView('automations');
    }));

    const testButton = studio.querySelector('[data-run-test]');
    testButton?.addEventListener('click', async () => {
      testButton.disabled = true;
      testButton.textContent = 'Test en cours...';
      nodeButtons.forEach((node) => node.classList.remove('running', 'passed'));
      for (const node of nodeButtons) {
        node.classList.add('running');
        await new Promise((resolve) => setTimeout(resolve, 280));
        node.classList.remove('running');
        node.classList.add('passed');
      }
      const result = studio.querySelector('[data-test-result]');
      if (result) result.hidden = false;
      testButton.disabled = false;
      testButton.textContent = 'Tester de nouveau';
    });

    const chatForm = studio.querySelector('[data-automation-chat-form]');
    chatForm?.addEventListener('submit', (event) => {
      event.preventDefault();
      const input = chatForm.querySelector('input');
      const answer = studio.querySelector('[data-automation-chat-answer]');
      if (!input.value.trim() || !answer) return;
      answer.querySelector('strong').textContent = 'J’ai compris le résultat recherché.';
      answer.querySelector('p').textContent = 'Je préparerais d’abord un brouillon avec le déclencheur, les données nécessaires, les exceptions, les approbations et les systèmes de destination. Rien ne serait activé avant un test avec des données contrôlées.';
      input.value = '';
    });

    const approveButton = studio.querySelector('[data-automation-approve]');
    approveButton?.addEventListener('click', () => {
      approveButton.disabled = true;
      approveButton.textContent = 'Exécution autorisée';
      const state = studio.querySelector('[data-approval-state]');
      if (state) state.textContent = 'Décision enregistrée · mission en cours de création';
    });

    const caseApprove = studio.querySelector('[data-case-approve]');
    caseApprove?.addEventListener('click', () => {
      caseApprove.disabled = true;
      caseApprove.textContent = 'Exécution autorisée';
      const result = studio.querySelector('[data-case-result]');
      if (result) result.hidden = false;
    });

    const configureButton = studio.querySelector('[data-inspector-config]');
    configureButton?.addEventListener('click', () => {
      configureButton.textContent = configureButton.getAttribute('aria-pressed') === 'true' ? 'Configurer cette étape' : 'Configuration affichée';
      configureButton.setAttribute('aria-pressed', String(configureButton.getAttribute('aria-pressed') !== 'true'));
    });

    document.querySelectorAll('[data-jump-flow]').forEach((button) => button.addEventListener('click', () => {
      renderFlow(button.dataset.jumpFlow);
      showView('automations');
    }));
    document.querySelectorAll('[data-jump-assistant]').forEach((button) => button.addEventListener('click', () => {
      showView('assistant');
      document.querySelector('#operations-center')?.scrollIntoView({ behavior:'smooth', block:'start' });
    }));

    renderFlow(currentFlow);
  });

  document.querySelectorAll('[data-preview-action]').forEach((button) => {
    button.addEventListener('click', () => {
      const preview = button.closest('[data-preview-root]') || button.closest('section') || button.parentElement;
      const status = preview?.querySelector('[data-preview-status]');
      button.disabled = true;
      button.textContent = button.dataset.doneLabel || 'Action confirmée';
      preview?.classList.add('action-complete');
      if (status && button.dataset.doneStatus) status.textContent = button.dataset.doneStatus;
    });
  });

  document.querySelectorAll('[data-platform-decision]').forEach((panel) => {
    const modify = panel.querySelector('[data-platform-modify]');
    const status = panel.querySelector('[data-preview-status]');
    modify?.addEventListener('click', () => {
      const editing = panel.classList.toggle('is-editing');
      modify.textContent = editing ? 'Terminer' : 'Modifier';
      if (status) status.textContent = editing ? 'Plan ouvert à la modification' : 'Aucune action exécutée';
    });
  });

  document.querySelectorAll('[data-residence-console]').forEach((console) => {
    const roomPins = [...console.querySelectorAll('[data-residence-room]')];
    const floorplan = console.querySelector('.residence-floorplan-canvas');
    const lightLayers = [...console.querySelectorAll('[data-room-layer]')];
    const viewPanels = [...console.querySelectorAll('[data-residence-view-panel]')];
    const shadeEffect = console.querySelector('.shade-effect');
    const fireplaceEffect = console.querySelector('.fireplace-effect');
    const poolCoverEffect = console.querySelector('.pool-cover-effect');
    const residenceShell = console.closest('.cap-console') || console;
    const roomName = console.querySelector('[data-residence-room-name]');
    const roomStatus = console.querySelector('[data-residence-room-status]');
    const temperature = console.querySelector('[data-residence-temp]');
    const temperatureLabel = console.querySelector('[data-temperature-label]');
    const lighting = console.querySelector('[data-residence-light]');
    const lightingRange = console.querySelector('[data-residence-light-range]');
    const hvacState = console.querySelector('[data-hvac-state]');
    const hvacButtons = [...console.querySelectorAll('[data-hvac-mode]')];
    const deviceButtons = [...console.querySelectorAll('[data-room-toggle]')];
    const recommendation = console.querySelector('[data-residence-recommendation]');
    let selectedRoom = roomPins[0];

    const setRoomLight = (room, level) => {
      const safeLevel = Math.max(0, Math.min(100, Number(level) || 0));
      const layer = lightLayers.find((item) => item.dataset.roomLayer === room);
      const pin = roomPins.find((item) => item.dataset.residenceRoom === room);
      if (layer) layer.style.setProperty('--light-level', String(safeLevel / 100));
      if (pin) pin.dataset.light = String(safeLevel);
    };

    const deviceType = (name) => {
      const normalized = name.toLowerCase();
      if (/éclairage|plafonnier|suspension|lampe/.test(normalized)) return 'light';
      if (/store|toile/.test(normalized)) return 'shade';
      if (/audio|télévision|écran/.test(normalized)) return 'media';
      if (/foyer|chauffage/.test(normalized)) return 'heat';
      if (/porte/.test(normalized)) return 'door';
      return 'generic';
    };

    const renderClimate = (mode) => {
      const labels = { auto:'Automatique', heat:'Chauffage', cool:'Climatisation', off:'Arrêt' };
      hvacButtons.forEach((button) => button.classList.toggle('active', button.dataset.hvacMode === mode));
      if (hvacState) hvacState.textContent = labels[mode] || labels.auto;
      if (floorplan) {
        floorplan.dataset.hvac = mode;
        floorplan.style.setProperty('--zone-color', mode === 'heat' ? '230,110,73' : mode === 'cool' ? '63,157,220' : '218,185,112');
      }
      console.style.setProperty('--zone-color', mode === 'heat' ? '230,110,73' : mode === 'cool' ? '63,157,220' : '218,185,112');
    };

    const updatePhysicalEffects = () => {
      const shadeButton = deviceButtons.find((button) => button.dataset.device === 'shade');
      const heatButton = deviceButtons.find((button) => button.dataset.device === 'heat');
      const shadeName = shadeButton?.querySelector('span')?.textContent.toLowerCase() || '';
      const isPoolCover = shadeName.includes('piscine');
      shadeEffect?.classList.toggle('visible', Boolean(shadeButton) && !isPoolCover);
      poolCoverEffect?.classList.toggle('closed', Boolean(isPoolCover && shadeButton?.classList.contains('active')));
      if (floorplan && shadeButton && !isPoolCover) {
        floorplan.dataset.coverState = shadeName.includes('toile')
          ? (shadeButton.classList.contains('active') ? 'deployed' : 'retracted')
          : (shadeButton.classList.contains('active') ? 'closed' : 'open');
      }
      fireplaceEffect?.classList.toggle('active', Boolean(heatButton?.classList.contains('active') && heatButton?.querySelector('span')?.textContent.toLowerCase().includes('foyer')));
    };

    const selectRoom = (pin) => {
      selectedRoom = pin;
      roomPins.forEach((item) => item.classList.toggle('active', item === pin));
      if (roomName) roomName.textContent = pin.dataset.residenceRoom;
      if (roomStatus) roomStatus.textContent = pin.dataset.status;
      if (temperature) temperature.textContent = pin.dataset.temp;
      if (temperatureLabel) temperatureLabel.textContent = pin.dataset.tempLabel || 'Température';
      if (lighting) lighting.textContent = `${pin.dataset.light} %`;
      if (lightingRange) lightingRange.value = pin.dataset.light;
      if (recommendation) recommendation.textContent = pin.dataset.recommendation || 'Aucune action requise.';
      const devices = (pin.dataset.devices || '').split(';;').map((device) => device.split('|'));
      deviceButtons.forEach((button, index) => {
        const [name = 'Appareil', state = 'Arrêté', enabled = '0'] = devices[index] || [];
        const icon = button.querySelector('i');
        const label = button.querySelector('span');
        const value = button.querySelector('b');
        button.dataset.device = deviceType(name);
        button.classList.toggle('active', enabled === '1');
        if (icon) icon.textContent = name.split(/\s+/).map((word) => word[0]).join('').slice(0, 2).toUpperCase();
        if (label) label.textContent = name;
        if (value) value.textContent = state;
      });
      if (floorplan) {
        floorplan.style.setProperty('--zone-x', pin.dataset.zoneX);
        floorplan.style.setProperty('--zone-y', pin.dataset.zoneY);
        floorplan.style.setProperty('--zone-light', String(Number(pin.dataset.light) / 100));
        floorplan.style.setProperty('--zone-dark', String(1 - (Number(pin.dataset.light) / 100)));
      }
      renderClimate(pin.dataset.hvac || 'auto');
      updatePhysicalEffects();
    };

    roomPins.forEach((pin) => pin.addEventListener('click', () => selectRoom(pin)));

    console.querySelectorAll('[data-temp-adjust]').forEach((button) => button.addEventListener('click', () => {
      const next = Math.max(16, Math.min(25, Number(temperature?.textContent || 21) + Number(button.dataset.tempAdjust)));
      if (temperature) temperature.textContent = next;
      if (selectedRoom) {
        selectedRoom.dataset.temp = String(next);
        const value = selectedRoom.querySelector('b');
        if (value && /°C/.test(value.textContent)) value.textContent = `${next} °C`;
      }
    }));

    lightingRange?.addEventListener('input', () => {
      if (lighting) lighting.textContent = `${lightingRange.value} %`;
      if (selectedRoom) setRoomLight(selectedRoom.dataset.residenceRoom, lightingRange.value);
      floorplan?.style.setProperty('--zone-light', String(Number(lightingRange.value) / 100));
      floorplan?.style.setProperty('--zone-dark', String(1 - (Number(lightingRange.value) / 100)));
      const lightButton = deviceButtons.find((button) => button.dataset.device === 'light');
      if (lightButton) {
        lightButton.classList.toggle('active', Number(lightingRange.value) > 0);
        const state = lightButton.querySelector('b');
        if (state) state.textContent = Number(lightingRange.value) > 0 ? `${lightingRange.value} %` : 'Éteint';
      }
    });

    hvacButtons.forEach((button) => button.addEventListener('click', () => {
      const mode = button.dataset.hvacMode;
      if (selectedRoom) selectedRoom.dataset.hvac = mode;
      renderClimate(mode);
    }));

    deviceButtons.forEach((button) => button.addEventListener('click', () => {
      const active = button.classList.toggle('active');
      const label = button.querySelector('span')?.textContent || '';
      const state = button.querySelector('b');
      if (!state) return;
      if (button.dataset.device === 'light') {
        state.textContent = active ? 'Allumé' : 'Éteint';
        const level = active ? Math.max(35, Number(selectedRoom?.dataset.light || 68)) : 0;
        if (lightingRange) lightingRange.value = String(level);
        if (lighting) lighting.textContent = `${level} %`;
        if (selectedRoom) setRoomLight(selectedRoom.dataset.residenceRoom, level);
        floorplan?.style.setProperty('--zone-light', String(level / 100));
        floorplan?.style.setProperty('--zone-dark', String(1 - (level / 100)));
      }
      if (button.dataset.device === 'shade') {
        const normalizedLabel = label.toLowerCase();
        state.textContent = normalizedLabel.includes('piscine') ? (active ? 'Fermée' : 'Ouverte') : normalizedLabel.includes('toile') ? (active ? 'Déployée' : 'Repliée') : (active ? 'Fermés' : 'Ouverts');
      }
      if (button.dataset.device === 'media') state.textContent = active ? 'En lecture' : 'Arrêtés';
      if (button.dataset.device === 'heat') state.textContent = active ? 'Allumé' : 'Arrêté';
      if (button.dataset.device === 'door') state.textContent = active ? 'Fermée' : 'Ouverte';
      if (button.dataset.device === 'generic') state.textContent = active ? 'Actif' : 'Arrêté';
      updatePhysicalEffects();
    }));

    const sceneButtons = [...console.querySelectorAll('[data-residence-scene]')];
    const sceneLevels = {
      home: { 'Salon':68, 'Cuisine et salle à manger':82, 'Suite principale':24, 'Bureau':46, 'Terrasse arrière':45, 'Piscine et spa':42, 'Garage intégré':36 },
      away: { 'Salon':0, 'Cuisine et salle à manger':0, 'Suite principale':0, 'Bureau':0, 'Terrasse arrière':0, 'Piscine et spa':14, 'Garage intégré':0 },
      evening: { 'Salon':62, 'Cuisine et salle à manger':38, 'Suite principale':16, 'Bureau':0, 'Terrasse arrière':58, 'Piscine et spa':52, 'Garage intégré':12 },
      night: { 'Salon':0, 'Cuisine et salle à manger':8, 'Suite principale':12, 'Bureau':0, 'Terrasse arrière':10, 'Piscine et spa':22, 'Garage intégré':8 }
    };
    const sceneDetails = {
      home:['Selon les pièces','Selon l’usage','Confort','Surveillés'],
      away:['Tout éteint','Fermés','Réduit','Protégés'],
      evening:['Ambiance chaude','Terrasse ouverte','Confort','Surveillés'],
      night:['Passages · 10 %','Fermés','Suite · 19 °C','Périmètre actif']
    };
    const applyScene = (key, sourceButton) => {
      Object.entries(sceneLevels[key] || sceneLevels.home).forEach(([room, level]) => setRoomLight(room, level));
      const matchingQuickButton = sceneButtons.find((item) => item.dataset.sceneKey === key);
      sceneButtons.forEach((item) => item.classList.toggle('active', item === matchingQuickButton));
      const name = console.querySelector('[data-residence-scene-name]');
      const copy = console.querySelector('[data-residence-scene-copy]');
      if (name) name.textContent = matchingQuickButton?.dataset.residenceScene || sourceButton?.dataset.sceneTitle || 'Maison';
      if (copy) copy.textContent = matchingQuickButton?.dataset.residenceMessage || sourceButton?.dataset.sceneImpact || '';
      if (selectedRoom) selectRoom(selectedRoom);
      const currentShade = deviceButtons.find((button) => button.dataset.device === 'shade');
      if (currentShade) {
        const currentShadeName = currentShade.querySelector('span')?.textContent.toLowerCase() || '';
        const isPoolCover = currentShadeName.includes('piscine');
        const isAwning = currentShadeName.includes('toile') && !isPoolCover;
        const closed = key === 'away' || key === 'night';
        const active = isPoolCover ? closed : isAwning ? key === 'evening' : closed;
        currentShade.classList.toggle('active', active);
        const state = currentShade.querySelector('b');
        if (state) state.textContent = isPoolCover ? (active ? 'Fermée' : 'Ouverte') : isAwning ? (active ? 'Déployée' : 'Repliée') : (active ? 'Fermés' : 'Ouverts');
      }
      updatePhysicalEffects();
      fireplaceEffect?.classList.toggle('active', key === 'evening');
      showFeedback(residenceShell, `Le mode ${name?.textContent || 'sélectionné'} a reconfiguré l’éclairage, le confort et les accès de cette démonstration.`, 'Mode appliqué');
    };
    sceneButtons.forEach((button) => button.addEventListener('click', () => applyScene(button.dataset.sceneKey, button)));

    residenceShell.querySelectorAll('[data-apply-scene]').forEach((button) => button.addEventListener('click', () => {
      const key = button.dataset.applyScene;
      residenceShell.querySelectorAll('[data-apply-scene]').forEach((item) => item.classList.toggle('active', item === button));
      const title = residenceShell.querySelector('[data-scene-preview-title]');
      const copy = residenceShell.querySelector('[data-scene-preview-copy]');
      if (title) title.textContent = button.dataset.sceneTitle;
      if (copy) copy.textContent = button.dataset.sceneImpact;
      ['lighting','covers','climate','access'].forEach((name, index) => {
        const target = residenceShell.querySelector(`[data-scene-${name}]`);
        if (target) target.textContent = (sceneDetails[key] || sceneDetails.home)[index];
      });
      applyScene(key, button);
    }));

    const viewButtons = [...console.querySelectorAll('.residence-console-head nav button')];
    viewButtons.forEach((button) => button.addEventListener('click', () => {
      viewButtons.forEach((item) => item.classList.toggle('active', item === button));
      viewPanels.forEach((panel) => { panel.hidden = panel.dataset.residenceViewPanel !== button.dataset.residenceView; });
    }));

    residenceShell.querySelector('[data-open-residence]')?.addEventListener('click', () => {
      const overview = residenceShell.querySelector('[data-demo-tab="overview"]');
      overview?.click();
      setTimeout(() => console.scrollIntoView({ behavior:'smooth', block:'start' }), 50);
    });

    residenceShell.querySelectorAll('[data-space-select]').forEach((button) => button.addEventListener('click', () => {
      residenceShell.querySelectorAll('[data-space-select]').forEach((item) => item.classList.toggle('active', item === button));
      ['name','summary','temp','air','presence','light'].forEach((field) => {
        const target = residenceShell.querySelector(`[data-space-${field}]:not(button)`);
        if (target) target.textContent = button.dataset[`space${field[0].toUpperCase()}${field.slice(1)}`];
      });
      const systems = residenceShell.querySelector('[data-space-systems]:not([data-space-select])');
      if (systems) systems.innerHTML = (button.dataset.spaceSystems || '').split(';;').map((item) => {
        const [label, value] = item.split('|');
        return `<article><span>${label}</span><b>${value}</b></article>`;
      }).join('');
    }));

    console.querySelector('[data-residence-assistant]')?.addEventListener('click', () => {
      showFeedback(console.closest('.cap-console') || console, `JARVIS a ouvert le contexte de la pièce ${roomName?.textContent || 'sélectionnée'} sans quitter le tableau de bord.`, 'Assistant résidentiel');
    });

    selectRoom(selectedRoom);
  });

  document.querySelectorAll('[data-home-control]').forEach((control) => {
    const buttons = [...control.querySelectorAll('[data-home-scene]')];
    const mode = control.querySelector('[data-home-mode]');
    const temp = control.querySelector('[data-home-temp]');
    const light = control.querySelector('[data-home-light]');
    buttons.forEach((button) => button.addEventListener('click', () => {
      buttons.forEach((item) => item.classList.toggle('active', item === button));
      if (mode) mode.textContent = `Ambiance ${button.dataset.homeScene.toLowerCase()} active`;
      if (temp) temp.textContent = button.dataset.temp;
      if (light) light.textContent = button.dataset.light;
    }));
  });

  document.querySelectorAll('[data-setup-demo]').forEach((demo) => {
    const steps = [...demo.querySelectorAll('[data-setup-step]')];
    const progress = [...demo.querySelectorAll('.jarvis-setup-progress i')];
    const complete = demo.querySelector('[data-setup-complete]');
    const next = demo.querySelector('[data-setup-next]');
    const back = demo.querySelector('[data-setup-back]');
    let current = 0;

    const render = () => {
      steps.forEach((step, index) => step.hidden = index !== current);
      progress.forEach((item, index) => item.classList.toggle('active', index <= current));
      back.disabled = current === 0;
      next.textContent = current === steps.length - 1 ? 'Créer mon JARVIS' : 'Continuer';
    };

    demo.querySelectorAll('[data-setup-choice]').forEach((choice) => choice.addEventListener('click', () => {
      const group = choice.parentElement;
      group.querySelectorAll('[data-setup-choice]').forEach((item) => item.classList.toggle('selected', item === choice));
    }));

    next.addEventListener('click', () => {
      if (current < steps.length - 1) {
        current += 1;
        render();
        return;
      }
      steps.forEach((step) => step.hidden = true);
      complete.hidden = false;
      demo.classList.add('setup-done');
      next.textContent = 'Ouvrir JARVIS';
      progress.forEach((item) => item.classList.add('active'));
    });

    back.addEventListener('click', () => {
      if (complete && !complete.hidden) {
        complete.hidden = true;
        demo.classList.remove('setup-done');
        current = steps.length - 1;
      } else if (current > 0) {
        current -= 1;
      }
      render();
    });
    render();
  });

  document.querySelectorAll('[data-network-demo]').forEach((demo) => {
    const nodes = [...demo.querySelectorAll('[data-network-node]')];
    const title = demo.querySelector('[data-network-title]');
    const copy = demo.querySelector('[data-network-copy]');
    const action = demo.querySelector('[data-network-action]');
    nodes.forEach((node) => node.addEventListener('click', () => {
      nodes.forEach((item) => item.classList.toggle('selected', item === node));
      if (title) title.textContent = node.dataset.title;
      if (copy) copy.textContent = node.dataset.copy;
      if (action) action.textContent = node.dataset.action;
    }));
  });

  document.addEventListener('click', (event) => {
    const card = event.target.closest('[data-evidence]');
    if (!card) return;
    const root = card.closest('.cap-console');
    if (!root) return;
    const selected = card.dataset.evidence;
    root.querySelectorAll('[data-evidence]').forEach((item) => item.classList.toggle('active', item === card));
    root.querySelectorAll('[data-evidence-panel]').forEach((panel) => { panel.hidden = panel.dataset.evidencePanel !== selected; });
  });

  document.querySelectorAll('[data-ambulance-console]').forEach((consoleElement) => {
    const modeButtons = [...consoleElement.querySelectorAll('[data-ambulance-mode]')];
    const modeLabel = consoleElement.querySelector('[data-ambulance-mode-label]');
    const modeCopy = consoleElement.querySelector('[data-ambulance-mode-copy]');
    const recommendation = consoleElement.querySelector('[data-ambulance-recommendation]');
    const recommendations = {
      route: 'Le DC-DC recharge la réserve pendant le déplacement; les charges de confort restent stabilisées.',
      camp: 'Maintenir le chauffe-eau reporté et profiter du prochain trajet avant d’envisager la génératrice.',
      night: 'Réduire l’éclairage, maintenir le chauffage silencieux et conserver le périmètre actif.',
      away: 'Réduire les charges non essentielles, verrouiller les accès et conserver la surveillance locale.'
    };

    modeButtons.forEach((button) => button.addEventListener('click', () => {
      modeButtons.forEach((item) => item.classList.toggle('active', item === button));
      if (modeLabel) modeLabel.textContent = button.dataset.label;
      if (modeCopy) modeCopy.textContent = button.dataset.copy;
      if (recommendation) recommendation.textContent = recommendations[button.dataset.ambulanceMode] || '';
    }));

    consoleElement.querySelectorAll('[data-vehicle-toggle]').forEach((button) => {
      button.dataset.defaultLabel = button.textContent.trim();
      button.addEventListener('click', () => {
        button.classList.toggle('active');
        button.textContent = button.classList.contains('active') ? 'Commande prête' : button.dataset.defaultLabel;
      });
    });
  });

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
