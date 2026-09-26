import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const baseUrl = 'https://jameslaplume.ca';

const solutions = [
  {
    index: '01', slug: 'environnements-intelligents', title: 'Espaces et véhicules intelligents',
    short: 'Faire travailler ensemble les technologies d’un lieu, sans rendre son utilisation compliquée.',
    promise: 'Un environnement qui comprend son état, s’adapte au contexte et demeure contrôlable simplement.',
    image: '/media/solutions/environnements-intelligents.webp', status: 'Laboratoire · futurs projets pilotes',
    problemTitle: 'Les appareils sont intelligents. Le lieu, lui, reste souvent fragmenté.',
    problem: 'Éclairage, chauffage, énergie, accès, audio, capteurs et sécurité vivent dans des applications séparées. JARVIS construit une couche commune qui les observe et les coordonne sans remplacer ce qui fonctionne déjà.',
    features: [
      ['01', 'Une seule lecture du lieu', 'Voir les états importants, les anomalies et les actions possibles dans une expérience cohérente.'],
      ['02', 'Des automatisations contextuelles', 'Adapter le confort et l’énergie selon la présence, l’heure, la météo et les priorités choisies.'],
      ['03', 'Un contrôle qui reste local', 'Conserver les fonctions essentielles même lorsqu’Internet ou un service externe devient indisponible.'],
      ['04', 'Des modes manuels clairs', 'Chaque automatisation sensible peut être expliquée, suspendue ou reprise manuellement.'],
      ['05', 'Un historique utile', 'Comprendre ce qui s’est passé avant une anomalie plutôt que consulter une suite de journaux techniques.'],
      ['06', 'Une base extensible', 'Ajouter progressivement de nouveaux appareils sans reconstruire tout l’environnement.'],
    ],
    scenarioTitle: 'Une soirée froide, une seule expérience.',
    scenario: [
      ['Comprendre', 'Le système observe la présence, la température, l’état de l’énergie et les préférences autorisées.'],
      ['Proposer', 'Il prépare le lieu avant l’arrivée et explique l’effet prévu sur le confort et l’énergie.'],
      ['Agir', 'Les actions réversibles sont exécutées; les décisions sensibles restent en attente d’une approbation.'],
      ['Apprendre', 'Le résultat est enregistré pour ajuster les prochaines propositions, sans enfermer l’utilisateur.'],
    ],
    integrations: ['Home Assistant', 'Matter', 'Zigbee', 'Z-Wave', 'KNX', 'ESPHome', 'Modbus', 'MQTT', 'Caméras', 'Énergie'],
    local: 'Les commandes essentielles, les règles et l’historique récent peuvent demeurer sur place. Les services infonuagiques restent optionnels et clairement identifiés.',
    limit: 'JARVIS n’invente pas une nouvelle plateforme domotique. Il relie des systèmes compatibles, documentés et autorisés. Chaque installation exige une analyse technique.',
  },
  {
    index: '02', slug: 'ia-privee-connaissances', title: 'IA privée et connaissances',
    short: 'Parler à ses propres informations, retrouver les bonnes preuves et préparer une action avec permission.',
    promise: 'Un assistant qui travaille à partir de vos sources autorisées et montre d’où vient chaque réponse importante.',
    image: '/media/solutions/ia-privee-connaissances.webp', status: 'En développement',
    problemTitle: 'L’information existe déjà. Le travail consiste à la retrouver et à lui faire confiance.',
    problem: 'Documents, courriels, procédures, photos et historiques sont dispersés. L’interface conversationnelle de JARVIS aide à chercher, comparer et préparer la prochaine étape sans donner un accès illimité à toutes les données.',
    features: [
      ['01', 'Recherche avec provenance', 'Chaque résultat important peut pointer vers les documents ou systèmes qui le soutiennent.'],
      ['02', 'Permissions explicites', 'Les personnes, agents et missions accèdent seulement aux sources nécessaires à leur rôle.'],
      ['03', 'Contexte de mission', 'L’assistant utilise le dossier, le site et l’objectif autorisés plutôt qu’une mémoire sans limites.'],
      ['04', 'Préparation du travail', 'Résumer une demande, comparer des documents et préparer un dossier ou une intervention.'],
      ['05', 'Actions supervisées', 'Les communications et opérations externes importantes attendent une validation humaine.'],
      ['06', 'Déploiement flexible', 'Les données peuvent rester locales, privées ou réparties selon le niveau de sensibilité.'],
    ],
    scenarioTitle: 'Préparer une intervention sans chercher pendant une heure.',
    scenario: [
      ['Demande', 'Une personne décrit le problème et choisit le site ou le dossier concerné.'],
      ['Sources', 'JARVIS consulte uniquement les plans, messages et procédures autorisés.'],
      ['Dossier', 'Il résume la situation, cite ses sources et prépare les prochaines vérifications.'],
      ['Approbation', 'Un humain corrige ou approuve avant qu’une mission ou un message soit créé.'],
    ],
    integrations: ['Documents', 'Courriels', 'Calendriers', 'Photos', 'Procédures', 'Stockage local', 'API métier', 'Bases de connaissances'],
    local: 'Les modèles, index et documents sensibles peuvent être conservés sur une infrastructure privée. Le choix dépend du matériel, du volume et du niveau de confidentialité.',
    limit: 'L’assistant ne reçoit jamais automatiquement toutes les données du réseau. Chaque connecteur, source et permission doit être déclaré, contrôlé et révocable.',
  },
  {
    index: '03', slug: 'securite-intelligente', title: 'Sécurité intelligente',
    short: 'Transformer caméras, accès et alarmes en événements compréhensibles plutôt qu’en notifications isolées.',
    promise: 'Une sécurité qui réunit le contexte, les preuves et les décisions, sans retirer le contrôle humain.',
    image: '/media/solutions/securite-intelligente.webp', status: 'Feuille de route · futurs pilotes',
    problemTitle: 'Une alerte sans contexte crée du bruit. Une preuve organisée permet de décider.',
    problem: 'Les caméras, portes, alarmes et capteurs détectent chacun une partie de l’événement. JARVIS vise à construire une chronologie commune pour expliquer ce qui a été observé et ce qui mérite réellement une attention.',
    features: [
      ['01', 'Chronologie unifiée', 'Rapprocher les événements provenant des caméras, accès, alarmes et capteurs autorisés.'],
      ['02', 'Conservation des preuves', 'Associer les images, états et décisions pertinentes à un incident documenté.'],
      ['03', 'Alertes hiérarchisées', 'Différencier un événement normal, une anomalie et une situation exigeant une vérification.'],
      ['04', 'Présence et périmètres', 'Adapter les règles selon l’occupation, les horaires et les zones réellement concernées.'],
      ['05', 'Respect de la vie privée', 'Limiter l’analyse, la durée de conservation et les personnes pouvant consulter les données.'],
      ['06', 'Réponse supervisée', 'Proposer une procédure et laisser les décisions sensibles à une personne autorisée.'],
    ],
    scenarioTitle: 'Comprendre une ouverture inhabituelle, sans conclure trop vite.',
    scenario: [
      ['Détection', 'Un accès est ouvert à une heure inhabituelle et une caméra confirme un mouvement.'],
      ['Contexte', 'Le système vérifie l’horaire, la présence autorisée et les événements associés.'],
      ['Preuve', 'Une chronologie concise est créée avec les sources disponibles et leur niveau de confiance.'],
      ['Décision', 'La personne responsable choisit l’action; aucune accusation n’est produite automatiquement.'],
    ],
    integrations: ['Frigate', 'ONVIF', 'Contrôle d’accès', 'Alarmes', 'Capteurs', 'Interphones', 'Journaux réseau', 'Stockage local'],
    local: 'L’analyse vidéo et la conservation peuvent être effectuées localement. Les accès distants passent par des mécanismes privés et auditables.',
    limit: 'Le système ne prétend pas identifier les intentions ni déterminer qu’une personne est dangereuse. Les règles, responsabilités et obligations légales doivent être définies avant tout déploiement.',
  },
  {
    index: '04', slug: 'automatisation-operations', title: 'Automatisation des opérations',
    short: 'Faire circuler demandes, documents et approbations entre les outils que l’entreprise utilise déjà.',
    promise: 'Moins de ressaisie et d’oublis, avec des étapes visibles et des validations placées au bon endroit.',
    image: '/media/solutions/automatisation-operations.webp', status: 'Priorité de développement commercial',
    problemTitle: 'Le travail se perd dans les passages entre courriel, formulaire, dossier et logiciel.',
    problem: 'JARVIS ne cherche pas à remplacer le CRM, la comptabilité ou les outils spécialisés. Il prend en charge les étapes répétitives entre eux et conserve une trace de ce qui a été proposé, validé et exécuté.',
    features: [
      ['01', 'Demandes structurées', 'Transformer un courriel ou formulaire en dossier clair avec les informations essentielles.'],
      ['02', 'Documents préparés', 'Créer des brouillons cohérents à partir de modèles et de sources autorisées.'],
      ['03', 'Approbations visibles', 'Placer une validation humaine avant une dépense, un envoi ou une opération sensible.'],
      ['04', 'Missions terrain', 'Préparer les informations nécessaires à une intervention et récupérer les résultats.'],
      ['05', 'Agents limités', 'Confier une mission précise à un agent avec sources, outils et durée clairement délimités.'],
      ['06', 'Journal complet', 'Conserver les preuves, erreurs, décisions et résultats pour comprendre chaque exécution.'],
    ],
    scenarioTitle: 'Une demande client devient un dossier prêt à traiter.',
    scenario: [
      ['Recevoir', 'Une demande arrive par courriel ou formulaire et les éléments utiles sont extraits.'],
      ['Vérifier', 'Les données manquantes, incohérences et documents associés sont signalés.'],
      ['Préparer', 'JARVIS produit le dossier, les tâches et le brouillon de communication.'],
      ['Valider', 'Une personne approuve avant la mise à jour des outils ou l’envoi au client.'],
    ],
    integrations: ['Courriel', 'Formulaires', 'CRM', 'Calendrier', 'Stockage documentaire', 'Comptabilité', 'Gestion de tâches', 'API'],
    local: 'Les règles et informations sensibles peuvent rester dans l’environnement de l’entreprise. Les connecteurs externes sont activés individuellement.',
    limit: 'Une automatisation fiable commence par un processus compris. JARVIS n’automatise pas une décision réglementée ou irréversible sans contrôle approprié.',
  },
  {
    index: '05', slug: 'reseau-resilience', title: 'Réseau et résilience numérique',
    short: 'Comprendre l’infrastructure, surveiller les dépendances et conserver des accès privés fiables.',
    promise: 'Une vue claire du réseau et de ses risques, avant que chaque problème devienne une urgence.',
    image: '/media/solutions/reseau-resilience.webp', status: 'Feuille de route spécialisée',
    problemTitle: 'Le réseau soutient tout le reste, mais il devient visible seulement lorsqu’il tombe.',
    problem: 'Cette solution vise l’inventaire, la topologie, la disponibilité, les liens Internet, la segmentation et les accès privés. Elle joue le rôle d’une couche d’observation et d’assistance pour l’administrateur, sans promettre une cybersécurité magique.',
    features: [
      ['01', 'Inventaire vivant', 'Identifier les équipements autorisés, leur rôle, leur état et leurs dépendances.'],
      ['02', 'Topologie compréhensible', 'Montrer comment les sites, réseaux, passerelles et services essentiels sont reliés.'],
      ['03', 'Disponibilité surveillée', 'Repérer une dégradation de connexion, une perte de service ou un équipement instable.'],
      ['04', 'Accès privé', 'Préparer des accès distants limités, documentés et révocables plutôt qu’exposer les systèmes.'],
      ['05', 'Segmentation progressive', 'Séparer les appareils, utilisateurs et fonctions selon les risques et besoins réels.'],
      ['06', 'Contexte pour le diagnostic', 'Transmettre à Care les événements réseau pertinents lorsqu’une panne touche plusieurs systèmes.'],
    ],
    scenarioTitle: 'Une connexion instable devient une cause vérifiable.',
    scenario: [
      ['Observer', 'Une caméra, un tableau de bord et un service distant deviennent intermittents.'],
      ['Corréler', 'JARVIS rapproche la perte de paquets, l’état de la passerelle et les changements récents.'],
      ['Isoler', 'Le problème probable est limité à un lien ou un équipement au lieu d’accuser chaque application.'],
      ['Escalader', 'Un rapport avec les mesures et prochaines vérifications est remis à la personne responsable.'],
    ],
    integrations: ['Routeurs', 'Commutateurs', 'Wi-Fi', 'VPN', 'DNS', 'Pare-feu', 'LTE', 'Starlink', 'SNMP', 'Journaux'],
    local: 'La supervision et l’inventaire peuvent rester sur place. Les échanges entre sites utilisent des connexions privées et des permissions explicites.',
    limit: 'La surveillance réseau n’est pas un service complet de cybersécurité. Les audits offensifs et interventions spécialisées appartiennent à une future branche Security Pro encadrée.',
  },
  {
    index: '06', slug: 'diagnostic-care', title: 'Diagnostic et continuité — JARVIS Care',
    short: 'Passer d’un symptôme à des preuves, des vérifications et une remise en service documentée.',
    promise: 'Comprendre plus vite ce qui a changé, quoi vérifier et comment transmettre un dossier utile à la bonne personne.',
    image: '/media/solutions/diagnostic-care.webp', status: 'Prototype · futur service récurrent',
    problemTitle: 'Une panne traverse souvent plusieurs systèmes et personne ne possède toute l’histoire.',
    problem: 'Care réunit les états, événements, changements et procédures autorisés pour construire un diagnostic progressif. Il prépare les vérifications, documente le résultat et facilite la continuité après l’installation.',
    features: [
      ['01', 'Détection précoce', 'Repérer les dérives de capteurs, températures, consommations ou communications avant un arrêt complet.'],
      ['02', 'Arbre de vérification', 'Classer les causes possibles et proposer les contrôles les moins risqués en premier.'],
      ['03', 'Contexte des changements', 'Relier le symptôme aux mises à jour, interventions et événements qui l’ont précédé.'],
      ['04', 'Dossier technicien', 'Préparer mesures, photos, historique, pièces possibles et étapes déjà vérifiées.'],
      ['05', 'Sauvegarde et retour', 'Documenter les configurations, mises à jour et options de retour lorsque le système le permet.'],
      ['06', 'Suivi continu', 'Vérifier après l’intervention que le service est réellement stable et que la cause est comprise.'],
    ],
    scenarioTitle: 'Une ventilation arrêtée devient un diagnostic guidé.',
    scenario: [
      ['Symptôme', 'La ventilation ne démarre plus malgré une commande valide.'],
      ['Preuves', 'Le système compare l’énergie disponible, le relais, le capteur et les derniers événements.'],
      ['Hypothèses', 'Il classe les causes possibles, par exemple alimentation, fusible, communication ou moteur.'],
      ['Rapport', 'Les vérifications confirmées et la prochaine action sont préparées pour le propriétaire ou le technicien.'],
    ],
    integrations: ['Capteurs', 'Télémétrie', 'Journaux', 'Manuels', 'Inventaire', 'Sauvegardes', 'Historique de maintenance', 'Rapports PDF'],
    local: 'Le diagnostic utilise d’abord les données disponibles dans le site. Seules les informations approuvées sont ajoutées à un rapport ou partagées avec un intervenant.',
    limit: 'JARVIS peut organiser les preuves et suggérer des vérifications. Il ne remplace pas un technicien qualifié, un mécanicien ni un professionnel lorsqu’une intervention présente un risque.',
  },
];

const navItems = [
  ['solutions', '/solutions/', 'Solutions'],
  ['plateforme', '/plateforme/', 'Plateforme'],
  ['ambulance', '/ambulance-lab/', 'Ambulance Lab'],
  ['recherche', '/recherche/', 'Recherche'],
  ['vision', '/vision-roadmap/', 'Vision'],
  ['about', '/a-propos/', 'À propos'],
];

function header(active = '', lang = 'fr-CA') {
  const english = lang.startsWith('en');
  if (english) return `<a class="skip-link" href="#contenu">Skip to content</a>
  <header class="site-header">
    <a class="brand" href="/en/"><span class="brand-mark">JL</span><span class="brand-copy"><strong>James Laplume</strong><small>Intelligent systems studio</small></span></a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" data-nav-toggle><span></span><span></span></button>
    <nav class="site-nav" aria-label="Main navigation" data-nav><a href="/solutions/">Solutions</a><a href="/plateforme/">Platform</a><a href="/ambulance-lab/">Ambulance Lab</a><a href="/recherche/">Research</a><a href="/vision-roadmap/">Vision</a><a href="/a-propos/">About</a></nav>
    <div class="header-actions"><a class="language-link" href="/">Français</a><a class="header-cta" href="/contact/">Discuss a project</a></div>
  </header>`;
  return `<a class="skip-link" href="#contenu">Aller au contenu</a>
  <header class="site-header">
    <a class="brand" href="/"><span class="brand-mark">JL</span><span class="brand-copy"><strong>James Laplume</strong><small>Intelligent systems studio</small></span></a>
    <button class="nav-toggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false" data-nav-toggle><span></span><span></span></button>
    <nav class="site-nav" aria-label="Navigation principale" data-nav>${navItems.map(([key, href, label]) => `<a${active === key ? ' class="active"' : ''} href="${href}">${label}</a>`).join('')}</nav>
    <div class="header-actions"><a class="language-link" href="/en/" lang="en">English</a><a class="header-cta${active === 'contact' ? ' active' : ''}" href="/contact/">Parler du projet</a></div>
  </header>`;
}

function footer(lang = 'fr-CA') {
  if (lang.startsWith('en')) return `<footer class="site-footer"><div class="footer-main shell">
    <div><a class="brand" href="/en/"><span class="brand-mark">JL</span><span class="brand-copy"><strong>James Laplume</strong><small>Intelligent systems studio</small></span></a><p>Connect what exists. Understand what matters. Act with your approval.</p></div>
    <div><h3>Explore</h3><a href="/solutions/">Solutions</a><a href="/plateforme/">Platform</a><a href="/ambulance-lab/">Ambulance Lab</a><a href="/recherche/">Research</a></div>
    <div><h3>Project</h3><a href="/vision-roadmap/">Vision and roadmap</a><a href="/confiance/">Trust</a><a href="/a-propos/">About</a><a href="/contact/">Contact</a></div>
    <div><h3>Status</h3><span>Platform in development</span><span>Active real-world laboratory</span><span>Open to collaboration</span></div>
  </div><div class="footer-bottom shell"><span>© 2026 James Laplume · Québec, Canada</span><span>Detailed edition available in French</span><span>Private by design</span></div></footer>`;
  return `<footer class="site-footer"><div class="footer-main shell">
    <div><a class="brand" href="/"><span class="brand-mark">JL</span><span class="brand-copy"><strong>James Laplume</strong><small>Intelligent systems studio</small></span></a><p>Relier ce qui existe. Comprendre ce qui compte. Agir avec votre accord.</p></div>
    <div><h3>Explorer</h3><a href="/solutions/">Solutions</a><a href="/plateforme/">Plateforme</a><a href="/ambulance-lab/">Ambulance Lab</a><a href="/recherche/">Recherche</a></div>
    <div><h3>Projet</h3><a href="/vision-roadmap/">Vision et feuille de route</a><a href="/confiance/">Confiance</a><a href="/a-propos/">À propos</a><a href="/contact/">Contact</a></div>
    <div><h3>État</h3><span>Plateforme en développement</span><span>Laboratoire réel actif</span><span>Ouvert aux collaborations</span></div>
  </div><div class="footer-bottom shell"><span>© 2026 James Laplume · Québec, Canada</span><span class="visitor-counter"><i></i> Visiteurs <b data-visitor-count>—</b></span><span>Privé par conception</span></div></footer>`;
}

function documentPage({ title, description, active, pathname, body, image = '/og.png', lang = 'fr-CA' }) {
  const canonical = `${baseUrl}${pathname}`;
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><meta name="description" content="${description}"><link rel="canonical" href="${canonical}"><meta property="og:title" content="${title}"><meta property="og:description" content="${description}"><meta property="og:type" content="website"><meta property="og:url" content="${canonical}"><meta property="og:image" content="${baseUrl}${image}"><meta name="theme-color" content="#0b0e0e"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/site-v3.css?v=20260926b"></head><body>${header(active, lang)}<main id="contenu">${body}</main>${footer(lang)}<script src="/site-v3.js?v=20260926b" defer></script></body></html>`;
}

function hero({ eyebrow, title, lead, image, meta = [], page = false, actions = '' }) {
  return `<section class="hero${page ? ' page-hero' : ''}"><div class="hero-media"><img src="${image}" alt=""></div><div class="hero-inner shell"><div class="hero-copy" data-reveal><p class="eyebrow">${eyebrow}</p><h1 class="display">${title}</h1><p class="lead">${lead}</p>${actions ? `<div class="hero-actions">${actions}</div>` : ''}${meta.length ? `<div class="hero-meta">${meta.map(([a,b]) => `<div><span>${a}</span><b>${b}</b></div>`).join('')}</div>` : ''}</div></div></section>`;
}

function cta(title = 'Commençons par comprendre ce qui doit mieux fonctionner.') {
  return `<section class="cta-band"><div class="cta-inner shell" data-reveal><div><p class="eyebrow">Premier échange</p><h2 class="subhead">${title}</h2></div><div><p>Présentez le problème, le lieu ou le processus. Je vous répondrai clairement sur ce qui est possible aujourd’hui, ce qui exige un pilote et ce qui appartient encore à la recherche.</p><a class="button button-primary" href="/contact/">Discuter du projet <span>↗</span></a></div></div></section>`;
}

function solutionCards() {
  return `<div class="solution-grid">${solutions.map((s) => `<a class="solution-card" href="/solutions/${s.slug}/"><img src="${s.image}" alt=""><div class="solution-card-copy"><span class="solution-index">${s.index} / 06</span><h3>${s.title}</h3><p>${s.short}</p><span class="arrow">↗</span></div></a>`).join('')}</div>`;
}

function homePage() {
  const body = hero({ eyebrow:'JARVIS · Systèmes intelligents privés', title:'Relier ce qui existe.<br><em>Faire agir l’ensemble.</em>', lead:'JARVIS réunit les informations, les logiciels, les appareils et les lieux que vous utilisez déjà pour créer des systèmes plus simples, privés et capables d’agir avec votre accord.', image:'/media/concept/jarvis-hero-architecture-v1.webp', actions:'<a class="button button-primary" href="/solutions/">Explorer les solutions <span>↗</span></a><a class="button button-ghost" href="/ambulance-lab/">Voir le laboratoire réel</a>', meta:[['Approche','Relier avant de remplacer'],['Contrôle','Permissions et approbations'],['État','Développement et laboratoire']] }) +
  `<section class="section section-white"><div class="intro-grid shell" data-reveal><div><p class="eyebrow">La philosophie</p><h2 class="headline">Tout existe déjà.<br>Le vrai défi est de tout faire travailler ensemble.</h2></div><aside class="intro-aside"><p>Nous avons plus d’applications, d’appareils, de données et de formations que jamais. Pourtant, l’information reste dispersée et les décisions demeurent difficiles. JARVIS ajoute les liens qui manquent : contexte, permissions, preuves et coordination.</p><strong>Ne pas remplacer. Comprendre, relier et orchestrer.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="section-heading" data-reveal><div><p class="eyebrow">Six solutions</p><h2 class="headline">Du numérique au réel.</h2></div><p>Chaque solution peut fonctionner seule. Ensemble, elles partagent la même plateforme, les mêmes règles et une lecture commune du contexte.</p></div>${solutionCards()}</div></section>` +
  `<section class="split-media"><div class="split-media-image"><img src="/media/solutions/ia-privee-connaissances.webp" alt="Espace de travail privé et système local"></div><div class="split-media-copy"><p class="eyebrow">La plateforme JARVIS</p><h2 class="headline">Une intelligence qui connaît ses limites.</h2><p>Le chat n’est qu’une interface. Derrière lui, JARVIS sépare l’identité, les permissions, les sources, les agents et les actions. Une réponse importante doit pouvoir être expliquée; une action sensible doit pouvoir être refusée.</p><ul class="detail-list"><li><b>01</b><span>Des sources autorisées et une provenance visible</span></li><li><b>02</b><span>Des missions limitées plutôt qu’un accès général</span></li><li><b>03</b><span>Des actions supervisées et un journal complet</span></li></ul><div class="hero-actions"><a class="button button-primary" href="/plateforme/">Comprendre la plateforme <span>↗</span></a></div></div></section>` +
  `<section class="ambulance-teaser"><img src="/media/ambulance/ambulance-ford-2017-hd.jpg" alt="Ambulance Ford E-Series 2017 verte utilisée comme laboratoire mobile"><div class="ambulance-teaser-copy shell" data-reveal><p class="eyebrow">La preuve dans le réel</p><h2 class="headline">L’Ambulance Lab.</h2><p class="lead">Une Ford 2017 V10 transformée en laboratoire mobile. Énergie, réseau, confort, sécurité, diagnostic et automatisation doivent y fonctionner ensemble, en déplacement comme hors réseau.</p><a class="button button-primary" href="/ambulance-lab/">Découvrir le projet <span>↗</span></a></div></section>` +
  `<section class="section section-white"><div class="intro-grid shell" data-reveal><div><p class="eyebrow">Recherche appliquée</p><h2 class="headline">Construire par hypothèses, preuves et essais réels.</h2></div><aside class="intro-aside"><p>Le site distingue les idées, les prototypes et les systèmes validés. Le journal de recherche documente les questions, les expériences et les limites afin que le projet progresse sur des bases vérifiables.</p><strong><a href="/recherche/">Consulter la méthode et les travaux →</a></strong></aside></div></section>` + cta();
  return documentPage({ title:'JARVIS | Systèmes intelligents privés — James Laplume', description:'JARVIS relie vos outils, vos informations et vos espaces dans une expérience privée, contextuelle et contrôlée.', active:'', pathname:'/', body, image:'/media/concept/jarvis-hero-architecture-v1.png' });
}

function solutionsHub() {
  const body = hero({ eyebrow:'Solutions JARVIS', title:'Six façons de rendre un système <em>plus capable.</em>', lead:'Pour une maison, un véhicule ou une entreprise : comprendre ce qui existe, relier ce qui apporte une vraie valeur et conserver le dernier mot.', image:'/media/solutions/environnements-intelligents.webp', page:true, meta:[['Structure','Six solutions distinctes'],['Interface','Une plateforme commune'],['Maturité','Affichée sur chaque page']] }) +
  `<section class="section section-white"><div class="intro-grid shell" data-reveal><div><p class="eyebrow">Une structure claire</p><h2 class="headline">Des résultats pour le client, des capacités partagées derrière.</h2></div><aside class="intro-aside"><p>Les solutions décrivent ce qu’une personne ou une organisation obtient. JARVIS, la Box, les connecteurs et l’automatisation contextuelle composent la plateforme qui permet de les livrer.</p><strong>Une solution n’est pas une nouvelle application isolée.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell">${solutionCards()}</div></section>` +
  `<section class="section section-dark"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Choisir sans deviner</p><h2 class="headline">Le point de départ est le problème.</h2></div><p>Un premier échange sert à définir le besoin, les systèmes déjà présents, les contraintes et la plus petite validation utile.</p></div><div class="feature-grid"><article class="feature"><span>01</span><h3>Analyser l’existant</h3><p>Équipements, logiciels, données, responsabilités et irritants réels.</p></article><article class="feature"><span>02</span><h3>Choisir une preuve</h3><p>Un scénario limité qui démontre une valeur mesurable sans reconstruire l’ensemble.</p></article><article class="feature"><span>03</span><h3>Décider de la suite</h3><p>Documenter les résultats, les risques et le prochain niveau de maturité.</p></article></div></div></section>` + cta('Quel problème mérite d’être simplifié en premier?');
  return documentPage({ title:'Solutions JARVIS | James Laplume', description:'Six familles de solutions pour les environnements intelligents, l’IA privée, la sécurité, les opérations, le réseau et le diagnostic.', active:'solutions', pathname:'/solutions/', body, image:solutions[0].image });
}

function solutionPage(s) {
  const body = hero({ eyebrow:`Solution ${s.index} / 06`, title:s.title.replace(' — ', '<br><em>') + (s.title.includes(' — ') ? '</em>' : ''), lead:s.promise, image:s.image, page:true, actions:'<a class="button button-primary" href="/contact/">Présenter un besoin <span>↗</span></a><a class="button button-ghost" href="/solutions/">Voir les six solutions</a>', meta:[['État actuel',s.status],['Approche','Intégration sur mesure'],['Principe','Contrôle humain']] }) +
  `<section class="section section-white"><div class="intro-grid shell" data-reveal><div><p class="eyebrow">Le problème</p><h2 class="headline">${s.problemTitle}</h2></div><aside class="intro-aside"><p>${s.problem}</p><strong>Une solution adaptée commence par une cartographie honnête de l’existant.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="section-heading" data-reveal><div><p class="eyebrow">L’expérience recherchée</p><h2 class="subhead">Ce que le système doit rendre plus simple.</h2></div><p>Ces capacités décrivent une cible de conception. Leur disponibilité dépend du niveau de maturité et des intégrations du projet.</p></div><div class="feature-grid">${s.features.map(([n,t,p])=>`<article class="feature" data-reveal><span>${n}</span><h3>${t}</h3><p>${p}</p></article>`).join('')}</div></div></section>` +
  `<section class="section section-white"><div class="scenario shell"><div data-reveal><p class="eyebrow">Scénario illustré</p><h2 class="headline">${s.scenarioTitle}</h2><div class="integration-row">${s.integrations.map(x=>`<span>${x}</span>`).join('')}</div></div><div class="scenario-steps" data-reveal>${s.scenario.map(([t,p])=>`<article class="scenario-step"><div><h3>${t}</h3><p>${p}</p></div></article>`).join('')}</div></div></section>` +
  `<section class="section section-dark"><div class="shell"><div class="intro-grid"><div data-reveal><p class="eyebrow">Déploiement responsable</p><h2 class="headline">Local quand ça compte.<br>Connecté quand c’est utile.</h2></div><aside class="intro-aside" data-reveal><p>${s.local}</p><strong>${s.limit}</strong></aside></div><div class="evidence-band"><div class="evidence"><span>Maturité publiée</span><strong>${s.status}</strong></div><div class="evidence"><span>Décisions sensibles</span><strong>Validation humaine requise</strong></div><div class="evidence"><span>Portée</span><strong>Définie pour chaque projet</strong></div></div></div></section>` + cta();
  return documentPage({ title:`${s.title} | Solutions JARVIS`, description:s.short, active:'solutions', pathname:`/solutions/${s.slug}/`, body, image:s.image });
}

function platformPage() {
  const body = hero({eyebrow:'La plateforme JARVIS',title:'Une couche d’intelligence <em>entre vos systèmes.</em>',lead:'JARVIS n’est ni un chatbot généraliste ni une nouvelle collection d’applications. C’est une architecture privée qui donne du contexte, des permissions et une capacité d’action contrôlée aux systèmes déjà présents.',image:'/media/solutions/ia-privee-connaissances.webp',page:true,meta:[['Interface','Conversation et tableaux de bord'],['Exécution','Missions et automatisations'],['Déploiement','Local, privé ou hybride']]}) +
  `<section class="section section-white"><div class="intro-grid shell"><div><p class="eyebrow">Comment ça fonctionne</p><h2 class="headline">Une demande traverse des couches clairement séparées.</h2></div><aside class="intro-aside"><p>Cette séparation empêche un assistant d’obtenir plus d’autorité simplement parce qu’il possède plus de contexte. Chaque mission garde ses sources, ses outils et ses limites.</p><strong>L’interface ne décide pas des permissions.</strong></aside></div><div class="architecture shell"><div class="arch-node"><span>01 · Personne</span><b>Objectif et accord</b></div><div class="arch-node"><span>02 · Interface</span><b>Application ou assistant</b></div><div class="arch-node"><span>03 · Noyau</span><b>Identité, contexte, règles</b></div><div class="arch-node"><span>04 · Connecteurs</span><b>Données et systèmes</b></div><div class="arch-node"><span>05 · Edge</span><b>Box, appareils, lieux</b></div></div></section>` +
  `<section class="section section-dark"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Capacités partagées</p><h2 class="headline">La même discipline derrière les six solutions.</h2></div><p>Chaque brique peut évoluer sans transformer le site public en catalogue de modules techniques.</p></div><div class="feature-grid"><article class="feature"><span>Identité</span><h3>Qui demande?</h3><p>Personnes, appareils et agents sont reconnus avant d’accéder à une source ou une action.</p></article><article class="feature"><span>Permissions</span><h3>Qu’est-ce qui est permis?</h3><p>La portée est explicite, limitée et révocable.</p></article><article class="feature"><span>Contexte</span><h3>Que se passe-t-il?</h3><p>Le site, le temps, les états et la mission donnent un sens aux données.</p></article><article class="feature"><span>Preuves</span><h3>Pourquoi cette réponse?</h3><p>Les sources et événements utiles sont conservés avec leur provenance.</p></article><article class="feature"><span>Automatisation</span><h3>Que peut-on préparer?</h3><p>Les étapes répétitives sont exécutées selon des règles définies.</p></article><article class="feature"><span>Approbation</span><h3>Qui garde le dernier mot?</h3><p>Les actions sensibles attendent une décision humaine.</p></article></div></div></section>` +
  `<section class="section section-paper"><div class="split-media shell"><div class="split-media-image"><img src="/media/product/systems-lab.png" alt="Matériel local et systèmes connectés"></div><div class="split-media-copy"><p class="eyebrow">JARVIS Box et I/O Edge</p><h2 class="subhead">Le lien avec le monde physique.</h2><p>La Box héberge les services locaux, les connecteurs et les règles nécessaires au site. Les interfaces Edge relient capteurs, relais, équipements et protocoles spécialisés. Le matériel final dépendra des validations et de la productisation.</p><ul class="detail-list"><li><b>01</b><span>Fonctions essentielles disponibles localement</span></li><li><b>02</b><span>Connecteurs documentés et remplaçables</span></li><li><b>03</b><span>Mises à jour, sauvegardes et retour contrôlé</span></li></ul></div></div></section>` + cta('Quelle partie de votre environnement mérite une première preuve?');
  return documentPage({title:'Plateforme JARVIS | Architecture privée et contextuelle',description:'Découvrez comment JARVIS relie identité, permissions, contexte, agents, connecteurs et systèmes physiques.',active:'plateforme',pathname:'/plateforme/',body,image:'/media/solutions/ia-privee-connaissances.webp'});
}

function ambulancePage() {
  const body = hero({eyebrow:'Ambulance Lab · Ford 2017 V10',title:'Le laboratoire où tout doit <em>fonctionner pour vrai.</em>',lead:'Une ancienne ambulance québécoise devient un véhicule habitable et un banc d’essai mobile pour l’énergie, le réseau, les systèmes d’origine, le confort, la sécurité, le diagnostic et l’automatisation.',image:'/media/ambulance/ambulance-ford-2017-hd.jpg',page:true,meta:[['État','Construction active'],['Rôle','Laboratoire physique'],['Objectif','Valider les six solutions']]}) +
  `<section class="section section-white"><div class="intro-grid shell"><div><p class="eyebrow">Le projet concret</p><h2 class="headline">Un véhicule complet. Une architecture commune.</h2></div><aside class="intro-aside"><p>L’Ambulance Lab n’est pas une offre distincte. C’est le premier environnement où JARVIS doit prouver qu’il peut observer, coordonner et diagnostiquer des systèmes numériques et physiques dans des conditions réelles.</p><strong>Chaque capacité sera identifiée comme prévue, installée, mesurée ou validée.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Infrastructure prévue et existante</p><h2 class="subhead">Un véritable véhicule habitable et automatisé.</h2></div><p>Les caractéristiques évolueront avec la construction et seront mises à jour à partir de mesures réelles.</p></div><div class="lab-specs"><div class="lab-spec"><span>Énergie</span><strong>560 Ah LiFePO₄ + extension prévue</strong></div><div class="lab-spec"><span>Recharge</span><strong>500 W solaire · DC-DC 60 A</strong></div><div class="lab-spec"><span>Autonomie</span><strong>Génératrice et gestion de charges</strong></div><div class="lab-spec"><span>Confort</span><strong>Chauffage diesel · climatisation</strong></div><div class="lab-spec"><span>Habitation</span><strong>Eau, chauffe-eau, frigo, douche, TV</strong></div><div class="lab-spec"><span>Ventilation</span><strong>Deux ventilateurs de toit contrôlables</strong></div><div class="lab-spec"><span>Connectivité</span><strong>Starlink, LTE, Wi-Fi et accès privé</strong></div><div class="lab-spec"><span>Véhicule</span><strong>Systèmes Ford et ambulance conservés</strong></div></div></div></section>` +
  `<section class="split-media"><div class="split-media-image"><img src="/media/ambulance/ambulance-garage-lab-v1.webp" alt="Ambulance dans un atelier professionnel"></div><div class="split-media-copy"><p class="eyebrow">Orchestration contextuelle</p><h2 class="subhead">Prévoir, proposer, agir et expliquer.</h2><p>La gestion énergétique combinera l’état des batteries, le solaire prévu, l’historique de consommation, les déplacements probables, les heures permises et les charges prioritaires.</p><ul class="detail-list"><li><b>01</b><span>Délester graduellement les charges non essentielles</span></li><li><b>02</b><span>Proposer ou démarrer la recharge selon les règles autorisées</span></li><li><b>03</b><span>Prévoir l’eau, l’énergie, la connectivité et les arrêts utiles</span></li><li><b>04</b><span>Conserver un mode manuel et expliquer chaque décision</span></li></ul></div></section>` +
  `<section class="section section-white"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Les six solutions dans le véhicule</p><h2 class="headline">Une preuve intégrée, pas six démonstrations isolées.</h2></div><p>Le même noyau doit comprendre les dépendances entre l’habitation, le réseau, le véhicule et les conditions de déplacement.</p></div><div class="feature-grid">${solutions.map(s=>`<article class="feature"><span>${s.index}</span><h3>${s.title}</h3><p>${s.slug==='environnements-intelligents'?'Contrôler confort, énergie et équipements comme un seul environnement.':s.slug==='ia-privee-connaissances'?'Interroger manuels, plans, historiques et procédures autorisés.':s.slug==='securite-intelligente'?'Réunir caméras, accès, présence et événements de sécurité.':s.slug==='automatisation-operations'?'Préparer rapports, listes, entretiens et missions sans ressaisie.':s.slug==='reseau-resilience'?'Maintenir Starlink, LTE, Wi-Fi, VPN et services locaux observables.':'Diagnostiquer capteurs, charges, systèmes mécaniques et pannes progressives.'}</p></article>`).join('')}</div></div></section>` +
  `<section class="section section-dark"><div class="intro-grid shell"><div><p class="eyebrow">Diagnostic mécanique et technique</p><h2 class="headline">Voir les dérives avant le code d’erreur.</h2></div><aside class="intro-aside"><p>Lorsque les interfaces et capteurs autorisés le permettent, JARVIS pourra suivre les tendances, rapprocher un symptôme des événements précédents, classer les causes possibles et préparer un rapport pour le propriétaire ou le mécanicien.</p><strong>Les conclusions demeurent des hypothèses guidées jusqu’à leur vérification.</strong></aside></div></section>` + cta('Vous souhaitez suivre le laboratoire ou contribuer à une validation?');
  return documentPage({title:'Ambulance Lab | Laboratoire mobile JARVIS',description:'Une ambulance Ford 2017 V10 transformée en laboratoire réel pour l’énergie, le réseau, la sécurité, le diagnostic et l’automatisation.',active:'ambulance',pathname:'/ambulance-lab/',body,image:'/media/ambulance/ambulance-ford-2017-hd.jpg'});
}

function researchPage() {
  const body = hero({eyebrow:'Recherche appliquée',title:'Des idées ambitieuses. <em>Des preuves vérifiables.</em>',lead:'Le projet avance par questions, prototypes, mesures et décisions documentées. Cette section devient la mémoire publique de ce qui est testé, appris et corrigé.',image:'/media/solutions/diagnostic-care.webp',page:true,meta:[['Méthode','Hypothèse → essai → preuve'],['Transparence','Limites publiées'],['Sécurité','Détails sensibles privés']]}) +
  `<section class="section section-white"><div class="intro-grid shell"><div><p class="eyebrow">Le cadre</p><h2 class="headline">Le site présente. La recherche démontre.</h2></div><aside class="intro-aside"><p>Chaque sujet public sera relié à une question précise, un protocole, des observations et une conclusion limitée. Les secrets, accès, données personnelles et architectures exploitables restent dans un dépôt privé.</p><strong>Une démonstration n’est pas encore une validation.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Axes actifs</p><h2 class="subhead">Ce que le laboratoire doit apprendre.</h2></div><p>Ces axes structurent les prochains essais; ils ne constituent pas encore des résultats commerciaux.</p></div><div class="research-grid"><article class="research-item"><span>R-01 · Énergie</span><h3>Prévoir l’autonomie utile</h3><p>Comparer état des batteries, production solaire, déplacement, météo et consommation réelle.</p></article><article class="research-item"><span>R-02 · Diagnostic</span><h3>Passer du symptôme à la preuve</h3><p>Évaluer comment les événements et capteurs réduisent progressivement les causes possibles.</p></article><article class="research-item"><span>R-03 · Contexte</span><h3>Automatiser sans surprendre</h3><p>Déterminer quand proposer, agir, demander une approbation ou ne rien faire.</p></article><article class="research-item"><span>R-04 · Résilience</span><h3>Continuer hors réseau</h3><p>Tester les fonctions essentielles lorsque le cloud, Internet ou une liaison deviennent indisponibles.</p></article><article class="research-item"><span>R-05 · Sécurité</span><h3>Réduire le bruit des alertes</h3><p>Mesurer si le contexte améliore la compréhension sans créer d’inférences dangereuses.</p></article><article class="research-item"><span>R-06 · Interaction</span><h3>Expliquer chaque décision</h3><p>Construire des interfaces où les sources, règles et conséquences demeurent compréhensibles.</p></article></div></div></section>` +
  `<section class="section section-dark"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Niveaux de maturité</p><h2 class="headline">Dire précisément où chaque élément se trouve.</h2></div><p>Le même vocabulaire sera utilisé dans le site, les documents de recherche et la feuille de route.</p></div><div class="roadmap"><div class="roadmap-row"><span>01 · Idée</span><h3>Question formulée</h3><p>Aucune preuve fonctionnelle</p></div><div class="roadmap-row"><span>02 · Laboratoire</span><h3>Essai contrôlé</h3><p>Conditions limitées</p></div><div class="roadmap-row"><span>03 · Prototype</span><h3>Parcours fonctionnel</h3><p>Fiabilité incomplète</p></div><div class="roadmap-row"><span>04 · Validé</span><h3>Critères mesurés</h3><p>Résultats documentés</p></div><div class="roadmap-row"><span>05 · Pilote</span><h3>Déploiement supervisé</h3><p>Utilisateur réel</p></div><div class="roadmap-row"><span>06 · Commercial</span><h3>Produit et soutien définis</h3><p>Offre répétable</p></div></div></div></section>` + cta('Vous représentez un centre de recherche, un partenaire ou un terrain d’essai?');
  return documentPage({title:'Recherche JARVIS | Méthode, essais et preuves',description:'Le journal public des hypothèses, expériences, mesures et limites du projet JARVIS.',active:'recherche',pathname:'/recherche/',body,image:'/media/solutions/diagnostic-care.webp'});
}

function visionPage() {
  const body = hero({eyebrow:'Vision et feuille de route',title:'Un écosystème privé qui grandit <em>avec la personne.</em>',lead:'À long terme, JARVIS vise à relier plusieurs environnements autorisés — maison, véhicule, entreprise et vie quotidienne — sans centraliser aveuglément toutes les données.',image:'/media/concept/jarvis-future-ecosystem-v1.webp',page:true,meta:[['Aujourd’hui','Noyau et laboratoires'],['Prochaine étape','Pilotes limités'],['Long terme','Écosystème multi-environnements']]}) +
  `<section class="section section-white"><div class="intro-grid shell"><div><p class="eyebrow">La direction</p><h2 class="headline">Un noyau commun. Plusieurs environnements autonomes.</h2></div><aside class="intro-aside"><p>Chaque lieu conserve ses fonctions locales et ses propres règles. Seul le contexte nécessaire et autorisé circule entre les environnements par une couche future appelée Fabric.</p><strong>La connexion ne doit jamais signifier une perte de contrôle.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Aujourd’hui → demain</p><h2 class="headline">Une progression en trois horizons.</h2></div><p>La vision reste puissante parce qu’elle distingue clairement les fondations actuelles des possibilités futures.</p></div><div class="roadmap"><div class="roadmap-row"><span>Horizon 01</span><h3>Relier un environnement réel</h3><p>Plateforme, Ambulance Lab, premières automatisations et preuves.</p></div><div class="roadmap-row"><span>Horizon 02</span><h3>Déployer des solutions spécialisées</h3><p>IA privée, opérations, réseau, sécurité et Care dans des pilotes encadrés.</p></div><div class="roadmap-row"><span>Horizon 03</span><h3>Relier plusieurs environnements</h3><p>Maison, véhicule et entreprise partagent seulement le contexte autorisé.</p></div><div class="roadmap-row"><span>Horizon 04</span><h3>Intelligence personnelle contextuelle</h3><p>Accompagnement volontaire pour habitudes, santé générale, temps et qualité de vie.</p></div></div></div></section>` +
  `<section class="split-media"><div class="split-media-image"><img src="/media/concept/jarvis-life-context-v3.webp" alt="Personne dans un environnement moderne et connecté"></div><div class="split-media-copy"><p class="eyebrow">Vision très long terme</p><h2 class="subhead">Transformer l’information en accompagnement utile.</h2><p>Montres, sommeil, activité, agenda, habitudes, finances, apprentissage et environnement produisent déjà beaucoup d’informations. Avec un consentement explicite, JARVIS pourrait un jour relier ces signaux pour aider une personne à atteindre ses propres objectifs.</p><ul class="detail-list"><li><b>01</b><span>La personne choisit ses objectifs, ses sources et ses limites</span></li><li><b>02</b><span>Le système cherche les contradictions et les occasions utiles</span></li><li><b>03</b><span>Il propose une prochaine action réaliste au bon moment</span></li><li><b>04</b><span>Il apprend des résultats et des refus, sans retirer la liberté</span></li></ul></div></section>` +
  `<section class="section section-dark"><div class="intro-grid shell"><div><p class="eyebrow">Frontières importantes</p><h2 class="headline">Une vision de qualité de vie, pas une autorité invisible.</h2></div><aside class="intro-aside"><p>Cette intelligence personnelle appartient à la recherche très long terme. Elle exige un consentement continu, une séparation des données sensibles, une explicabilité forte et aucune prétention médicale.</p><strong>Conseiller et coordonner, jamais manipuler ni diagnostiquer.</strong></aside></div></section>` + cta('Vous souhaitez discuter de la vision, de la recherche ou d’un futur partenariat?');
  return documentPage({title:'Vision et feuille de route JARVIS',description:'La vision à long terme de JARVIS : plusieurs environnements privés, une intelligence contextuelle et un contrôle humain durable.',active:'vision',pathname:'/vision-roadmap/',body,image:'/media/concept/jarvis-future-ecosystem-v1.png'});
}

function trustPage() {
  const body = hero({eyebrow:'Confiance et gouvernance',title:'La capacité d’agir exige des <em>limites visibles.</em>',lead:'Vie privée, sécurité, provenance et contrôle humain ne sont pas des options ajoutées après coup. Ils définissent la manière dont JARVIS peut accéder à une source ou agir dans le monde réel.',image:'/media/solutions/securite-intelligente.webp',page:true,meta:[['Données','Accès explicites'],['Actions','Approbations selon le risque'],['Historique','Preuves et journalisation']]}) +
  `<section class="section section-white"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Principes de conception</p><h2 class="headline">Savoir qui peut voir, comprendre et agir.</h2></div><p>Ces principes sont des objectifs d’architecture. Leur mise en œuvre doit être vérifiée pour chaque solution et chaque déploiement.</p></div><div class="trust-grid"><article class="trust-item"><span class="eyebrow">01 · Minimisation</span><h3>Utiliser seulement ce qui est nécessaire.</h3><p>Une mission reçoit les sources, outils et durées utiles à son objectif, pas un accès général par défaut.</p></article><article class="trust-item"><span class="eyebrow">02 · Provenance</span><h3>Montrer d’où vient l’information.</h3><p>Une réponse importante distingue les faits observés, les sources consultées et les hypothèses produites.</p></article><article class="trust-item"><span class="eyebrow">03 · Approbation</span><h3>Adapter le contrôle au risque.</h3><p>Les actions sensibles, irréversibles ou externes demeurent entre les mains d’une personne autorisée.</p></article><article class="trust-item"><span class="eyebrow">04 · Réversibilité</span><h3>Prévoir l’arrêt et le retour.</h3><p>Les automatisations doivent pouvoir être suspendues et les changements importants documentés.</p></article><article class="trust-item"><span class="eyebrow">05 · Localité</span><h3>Garder les fonctions essentielles près du site.</h3><p>Le cloud est utilisé lorsqu’il apporte une valeur comprise, jamais comme dépendance cachée.</p></article><article class="trust-item"><span class="eyebrow">06 · Honnêteté</span><h3>Publier la maturité et les limites.</h3><p>Une idée, un prototype et une solution commerciale ne sont jamais présentés comme équivalents.</p></article></div></div></section>` + cta('Un projet sensible commence par définir les responsabilités.');
  return documentPage({title:'Confiance et gouvernance | JARVIS',description:'Les principes de vie privée, permissions, provenance, contrôle humain et transparence qui guident JARVIS.',active:'',pathname:'/confiance/',body,image:'/media/solutions/securite-intelligente.webp'});
}

function aboutPage() {
  const body = hero({eyebrow:'À propos',title:'Construire le lien entre <em>l’idée et le réel.</em>',lead:'Je m’appelle James Laplume. Je développe JARVIS comme une plateforme d’intégration et de recherche appliquée pour les environnements intelligents, l’IA privée et l’automatisation.',image:'/media/solutions/automatisation-operations.webp',page:true,meta:[['Lieu','Québec, Canada'],['Approche','Prototypes et preuves'],['Collaboration','Technique, recherche, terrain']]}) +
  `<section class="section section-white"><div class="intro-grid shell"><div><p class="eyebrow">Pourquoi ce projet</p><h2 class="headline">La technologie devrait augmenter notre capacité d’agir, pas notre charge mentale.</h2></div><aside class="intro-aside"><p>Les bons appareils, logiciels et modèles existent souvent déjà. Mon travail consiste à comprendre le système complet, construire les liens manquants et vérifier dans le réel que l’ensemble demeure utile, compréhensible et contrôlable.</p><strong>JARVIS est la plateforme. L’Ambulance Lab est le premier grand terrain de preuve.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="feature-grid"><article class="feature"><span>01 · Clarté</span><h3>Dire ce qui est réel.</h3><p>Les concepts, prototypes, validations et offres futures sont identifiés séparément.</p></article><article class="feature"><span>02 · Curiosité</span><h3>Comprendre le système complet.</h3><p>Une panne ou un besoin ne respecte pas les frontières entre logiciel, réseau et matériel.</p></article><article class="feature"><span>03 · Contrôle</span><h3>Laisser le dernier mot.</h3><p>Le système propose et prépare; la personne demeure responsable des décisions sensibles.</p></article></div></div></section>` +
  `<section class="section section-dark"><div class="intro-grid shell"><div><p class="eyebrow">Collaborations recherchées</p><h2 class="headline">Des regards exigeants et des terrains réels.</h2></div><aside class="intro-aside"><p>Le projet peut bénéficier de partenaires en recherche, énergie, véhicules, bâtiment, sécurité, réseau, expérience utilisateur et développement de produit. L’objectif n’est pas de prétendre tout maîtriser seul, mais de construire une architecture cohérente avec les bonnes expertises.</p><strong>Ouvert aux conversations sérieuses, aux critiques et aux collaborations structurées.</strong></aside></div></section>` + cta('Parlons du problème, de l’expertise ou du terrain que vous pourriez apporter.');
  return documentPage({title:'À propos | James Laplume et JARVIS',description:'Découvrez James Laplume, la philosophie de JARVIS et l’approche de recherche appliquée derrière le projet.',active:'about',pathname:'/a-propos/',body,image:'/media/solutions/automatisation-operations.webp'});
}

function contactPage() {
  const body = hero({eyebrow:'Contact',title:'Parlons du problème <em>avant de parler de la solution.</em>',lead:'Client potentiel, partenaire technique, chercheur ou investisseur : décrivez simplement ce que vous cherchez à comprendre, relier ou automatiser.',image:'/media/solutions/ia-privee-connaissances.webp',page:true,meta:[['Réponse','À laplumejames@gmail.com'],['Lieu','Québec, Canada'],['Échanges','Exploratoires et confidentiels']]}) +
  `<section class="section section-white"><div class="contact-layout shell"><div data-reveal><p class="eyebrow">Premier échange</p><h2 class="headline">Une idée claire peut commencer par quelques lignes.</h2><p class="lead">Je vous répondrai sur ce qui semble réalisable, ce qui mérite une première preuve et les informations nécessaires pour aller plus loin.</p><div class="contact-direct"><p>Vous préférez écrire directement?</p><a href="mailto:laplumejames@gmail.com">laplumejames@gmail.com ↗</a></div></div><form class="contact-form" data-contact-form data-reveal><input type="hidden" name="_subject" value="Nouvelle demande depuis jameslaplume.ca"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off"><div class="field"><label for="name">Nom</label><input id="name" name="name" autocomplete="name" required></div><div class="field"><label for="email">Courriel</label><input id="email" name="email" type="email" autocomplete="email" required></div><div class="field full"><label for="organization">Organisation ou projet</label><input id="organization" name="organization" autocomplete="organization"></div><div class="field full"><label for="profile">Vous êtes</label><select id="profile" name="profile"><option>Client potentiel</option><option>Partenaire technique</option><option>Recherche ou institution</option><option>Investisseur ou accompagnateur</option><option>Autre</option></select></div><div class="field full"><label for="interest">Sujet principal</label><select id="interest" name="interest"><option>Environnement intelligent</option><option>IA privée et connaissances</option><option>Sécurité intelligente</option><option>Automatisation des opérations</option><option>Réseau et résilience</option><option>Diagnostic et JARVIS Care</option><option>Ambulance Lab</option><option>Recherche ou partenariat</option></select></div><div class="field full"><label for="message">Votre message</label><textarea id="message" name="message" required placeholder="Le problème actuel, ce que vous aimeriez rendre possible et les systèmes déjà présents."></textarea></div><div class="form-actions"><button class="button button-dark" type="submit">Envoyer le message <span>↗</span></button><p class="form-status" data-form-status aria-live="polite">Votre message sera transmis à James.</p></div></form></div></section>`;
  return documentPage({title:'Contact | Discuter d’un projet JARVIS',description:'Présentez votre projet, votre problème ou une possibilité de collaboration à James Laplume.',active:'contact',pathname:'/contact/',body,image:'/media/solutions/ia-privee-connaissances.webp'});
}

function englishPage() {
  const englishSolutions = [
    ['01','Smart environments','Connect comfort, energy, access and devices without making the environment harder to use.'],
    ['02','Private AI and knowledge','Work with authorized documents and data while keeping provenance and permissions visible.'],
    ['03','Intelligent security','Turn cameras, access and alarms into understandable events and organized evidence.'],
    ['04','Operations automation','Move requests, documents and approvals between the tools a business already uses.'],
    ['05','Network resilience','Understand infrastructure, dependencies, private access and service degradation.'],
    ['06','Diagnostics and JARVIS Care','Move from a symptom to evidence, verification steps and a documented recovery.'],
  ];
  const body = hero({eyebrow:'JARVIS · Private intelligent systems',title:'Connect what exists.<br><em>Make the whole system act.</em>',lead:'JARVIS connects information, software, devices and physical environments through a private architecture built around context, explicit permissions and human approval.',image:'/media/concept/jarvis-hero-architecture-v1.webp',actions:'<a class="button button-primary" href="/solutions/">Explore the six solutions <span>↗</span></a><a class="button button-ghost" href="/contact/">Discuss the project</a>',meta:[['Current stage','Development and real-world lab'],['Location','Québec, Canada'],['Detailed site','Available in French']]}) +
  `<section class="section section-white"><div class="intro-grid shell"><div><p class="eyebrow">English overview</p><h2 class="headline">A clear public map of an ambitious research and product vision.</h2></div><aside class="intro-aside"><p>The project is organized into six solution families: smart environments, private AI and knowledge, intelligent security, business automation, network resilience, and diagnostics with JARVIS Care.</p><strong>The detailed multi-page edition is currently maintained in French.</strong></aside></div></section>` +
  `<section class="section section-paper"><div class="shell"><div class="feature-grid">${englishSolutions.map(([n,t,p])=>`<article class="feature"><span>${n}</span><h3>${t}</h3><p>${p}</p></article>`).join('')}</div><div class="hero-actions"><a class="button button-dark" href="/solutions/">View the detailed French edition <span>↗</span></a></div></div></section>` +
  `<section class="cta-band"><div class="cta-inner shell"><div><p class="eyebrow">First conversation</p><h2 class="subhead">Let’s start with the problem that should work better.</h2></div><div><p>Share the environment, process or research question. I will clearly separate what can be demonstrated now, what needs a pilot and what remains part of the long-term vision.</p><a class="button button-primary" href="/contact/">Discuss the project <span>↗</span></a></div></div></section>`;
  return documentPage({title:'JARVIS | Private intelligent systems',description:'JARVIS connects private AI, automation, networks and physical environments while keeping humans in control.',active:'',pathname:'/en/',body,image:'/media/concept/jarvis-hero-architecture-v1.png',lang:'en-CA'});
}

async function writeRoute(route, html) {
  const dir = route === '/' ? root : path.join(root, route.replace(/^\//,'').replace(/\/$/,''));
  await mkdir(dir, { recursive: true });
  await writeFile(path.join(dir, 'index.html'), html, 'utf8');
}

await writeRoute('/', homePage());
await writeRoute('/solutions/', solutionsHub());
for (const solution of solutions) await writeRoute(`/solutions/${solution.slug}/`, solutionPage(solution));
await writeRoute('/plateforme/', platformPage());
await writeRoute('/ambulance-lab/', ambulancePage());
await writeRoute('/recherche/', researchPage());
await writeRoute('/vision-roadmap/', visionPage());
await writeRoute('/confiance/', trustPage());
await writeRoute('/a-propos/', aboutPage());
await writeRoute('/contact/', contactPage());
await writeRoute('/en/', englishPage());

const redirect = (target) => `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=${target}"><link rel="canonical" href="${baseUrl}${target}"><title>Redirection</title></head><body><p><a href="${target}">Continuer</a></p></body></html>`;
await writeRoute('/services/', redirect('/solutions/'));
await writeRoute('/jarvis-twin/', redirect('/plateforme/'));
await writeRoute('/about/', redirect('/a-propos/'));
await writeRoute('/jarvis-builder/', redirect('/plateforme/'));
await writeRoute('/trading-lab/', redirect('/'));

for (const [file, target] of [
  ['about.html', '/a-propos/'],
  ['contact.html', '/contact/'],
  ['solutions.html', '/solutions/'],
  ['projects.html', '/ambulance-lab/'],
  ['lab.html', '/ambulance-lab/'],
  ['mobile-lab.html', '/ambulance-lab/'],
  ['learn.html', '/recherche/'],
]) await writeFile(path.join(root, file), redirect(target), 'utf8');

const notFound = documentPage({
  title:'Page introuvable | James Laplume',
  description:'Cette page n’existe plus ou a été déplacée.',
  active:'', pathname:'/404.html',
  body:`<section class="hero page-hero"><div class="hero-media"><img src="/media/concept/jarvis-hero-architecture-v1.webp" alt=""></div><div class="hero-inner shell"><div class="hero-copy visible"><p class="eyebrow">Erreur 404</p><h1 class="display">Cette route ne mène <em>nulle part.</em></h1><p class="lead">La page a peut-être été déplacée pendant la réorganisation du site.</p><div class="hero-actions"><a class="button button-primary" href="/">Retour à l’accueil</a><a class="button button-ghost" href="/solutions/">Voir les solutions</a></div></div></div></section>`,
});
await writeFile(path.join(root, '404.html'), notFound, 'utf8');

const urls = ['/', '/solutions/', ...solutions.map((s)=>`/solutions/${s.slug}/`), '/plateforme/', '/ambulance-lab/', '/recherche/', '/vision-roadmap/', '/confiance/', '/a-propos/', '/contact/', '/en/'];
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((url)=>`  <url><loc>${baseUrl}${url}</loc><lastmod>2026-09-26</lastmod></url>`).join('\n')}\n</urlset>\n`;
await writeFile(path.join(root, 'sitemap.xml'), sitemap, 'utf8');
console.log(`Built ${urls.length} public routes.`);
