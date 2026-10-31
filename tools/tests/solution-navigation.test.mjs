import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import vm from 'node:vm';

// Run after `node tools/build-site.mjs`. No npm packages or network are needed.
// The VM exercises the real controller; native navigation/rendering still merits
// a browser smoke check (Tab, Enter, modified click, mouse and touch).
const root = new URL('../../', import.meta.url);
const [html, controller] = await Promise.all([
  readFile(new URL('index.html', root), 'utf8'),
  readFile(new URL('site-v4.js', root), 'utf8'),
]);

const solutions = [
  {
    slug: 'environnements-intelligents', name: 'Environnements intelligents',
    image: '/media/solutions/environnements-intelligents.webp',
    title: 'Le lieu répond à la situation, pas à une suite de commandes.',
  },
  {
    slug: 'ia-privee-connaissances', name: 'IA privée et connaissances',
    image: '/media/solutions/ia-privee-connaissances.webp',
    title: 'Une réponse utile montre ce qu’elle sait et d’où elle le sait.',
  },
  {
    slug: 'securite-intelligente', name: 'Sécurité intelligente',
    image: '/media/solutions/securite-intelligente.webp',
    title: 'Comprendre l’événement avant de décider quoi faire.',
  },
  {
    slug: 'automatisation-operations', name: 'Automatisation d’entreprise',
    image: '/media/solutions/jarvis-enterprise-operations-v1.webp',
    title: 'La demande devient un travail complet, prêt à approuver.',
  },
  {
    slug: 'reseau-resilience', name: 'Réseau et cybersécurité',
    image: '/media/solutions/reseau-resilience.webp',
    title: 'Voir l’infrastructure comme un système vivant.',
  },
  {
    slug: 'diagnostic-care', name: 'Diagnostic & continuité',
    image: '/media/solutions/diagnostic-care.webp',
    title: 'Passer du symptôme aux prochaines vérifications utiles.',
  },
];

function attributes(markup) {
  return Object.fromEntries([...markup.matchAll(/([^\s=<>/]+)(?:="([^"]*)"|='([^']*)')?/g)]
    .map((match) => [match[1], match[2] ?? match[3] ?? '']));
}

function openingTags(attribute) {
  return [...html.matchAll(new RegExp(`<([a-z][\\w-]*)\\b([^>]*\\b${attribute}(?=[\\s=>])[^>]*)>`, 'gi'))]
    .map((match) => ({ tag: match[1].toLowerCase(), attrs: attributes(match[2]) }));
}

const cardMarkup = openingTags('data-v4-capability');

test('the generated homepage exposes exactly six direct solution links', async (t) => {
  assert.equal(cardMarkup.length, 6);
  for (const solution of solutions) {
    await t.test(solution.slug, async () => {
      const cards = cardMarkup.filter(({ attrs }) => attrs['data-v4-capability'] === solution.slug);
      assert.equal(cards.length, 1, 'each solution appears once');
      const { tag, attrs } = cards[0];
      assert.equal(tag, 'a', 'the complete card must navigate without JavaScript');
      assert.equal(attrs.href, `/solutions/${solution.slug}/`);
      assert.ok(attrs.class?.split(/\s+/).includes('v4-solution-link'));
      assert.ok(!('role' in attrs), 'navigation links must retain their native role');
      assert.ok(!('aria-pressed' in attrs), 'a solution link is not a toggle');
      assert.ok(!('aria-selected' in attrs), 'a solution link is not a tab');
      assert.ok(!('tabindex' in attrs) || attrs.tabindex === '0', 'each card stays in keyboard order');
      assert.ok(!('onclick' in attrs), 'navigation must not depend on an inline handler');
      const destination = await readFile(new URL(`solutions/${solution.slug}/index.html`, root), 'utf8');
      assert.match(destination, /<h1\b/, 'the direct destination must exist');
    });
  }
});

test('the initial preview CTA names its solution in a dedicated label', () => {
  const [link] = openingTags('data-v4-capability-link');
  assert.equal(link?.tag, 'a');
  assert.equal(link.attrs.href, '/solutions/environnements-intelligents/');
  const label = html.match(/<span\b[^>]*\bdata-v4-capability-link-label(?=[\s=>])[^>]*>([^<]*)<\/span>/);
  assert.ok(label, 'the preview CTA needs a label that the controller can update');
  assert.equal(label[1].trim(), 'Environnements intelligents');
});

// A small DOM fixture isolates this IIFE from browser services and the unrelated
// contact form. It implements only element/selector/event APIs used on this page.
class Element {
  constructor(document, tagName = 'div', attrs = {}, text = '') {
    this.ownerDocument = document;
    this.tagName = tagName.toUpperCase();
    this.attrs = { ...attrs };
    this.dataset = Object.fromEntries(Object.entries(attrs).filter(([key]) => key.startsWith('data-'))
      .map(([key, value]) => [key.slice(5).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase()), value]));
    this.textContent = text;
    this.children = [];
    this.listeners = new Map();
    this.classList = {
      contains: (name) => this.className.split(/\s+/).includes(name),
      toggle: (name, force) => {
        const names = new Set(this.className.split(/\s+/).filter(Boolean));
        const include = force ?? !names.has(name);
        if (include) names.add(name); else names.delete(name);
        this.className = [...names].join(' ');
        return include;
      },
      add: (...names) => names.forEach((name) => this.classList.toggle(name, true)),
      remove: (...names) => names.forEach((name) => this.classList.toggle(name, false)),
    };
  }
  get className() { return this.attrs.class ?? ''; }
  set className(value) { this.attrs.class = value; }
  get href() { return this.attrs.href ?? ''; }
  set href(value) { this.attrs.href = value; }
  get src() { return this.attrs.src ?? ''; }
  set src(value) { this.attrs.src = value; }
  get alt() { return this.attrs.alt ?? ''; }
  set alt(value) { this.attrs.alt = value; }
  get tabIndex() { return Number(this.attrs.tabindex ?? (this.tagName === 'A' && this.href ? 0 : -1)); }
  set tabIndex(value) { this.attrs.tabindex = String(value); }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) { return this.attrs[name] ?? null; }
  hasAttribute(name) { return name in this.attrs; }
  removeAttribute(name) { delete this.attrs[name]; }
  append(child) { this.children.push(child); child.parentElement = this; return child; }
  matches(selector) {
    if (selector.startsWith('.')) return this.classList.contains(selector.slice(1));
    const attr = selector.match(/^\[([^=\]]+)(?:="([^"]*)")?\]$/);
    return attr ? this.hasAttribute(attr[1]) && (attr[2] === undefined || this.getAttribute(attr[1]) === attr[2])
      : this.tagName.toLowerCase() === selector;
  }
  closest(selector) { return this.matches(selector) ? this : this.parentElement?.closest(selector) ?? null; }
  querySelectorAll(selector) {
    return this.children.flatMap((child) => [...(child.matches(selector) ? [child] : []), ...child.querySelectorAll(selector)]);
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] ?? null; }
  addEventListener(type, listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(listener);
  }
  dispatch(type, options = {}) {
    const event = {
      type, target: this, currentTarget: this, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; },
      stopPropagation() {}, stopImmediatePropagation() {}, ...options,
    };
    for (const listener of this.listeners.get(type) ?? []) listener.call(this, event);
    return event;
  }
  focus() {
    this.ownerDocument.activeElement = this;
    this.dispatch('focus');
    this.dispatch('focusin');
  }
}

function fixture({ finePointer = true, unknownSlug = false } = {}) {
  const document = new Element(null, 'document');
  document.ownerDocument = document;
  const add = (parent, attribute, text = '', attrs = {}, tag = 'div') =>
    parent.append(new Element(document, tag, { [attribute]: '', ...attrs }, text));
  const cards = solutions.map(({ slug }, index) => add(document, 'data-v4-capability', '', {
    class: `v4-solution-link${index === 0 ? ' active' : ''}`,
    'data-v4-capability': slug, href: `/solutions/${slug}/`,
  }, 'a'));
  if (unknownSlug) cards.push(add(document, 'data-v4-capability', '', {
    'data-v4-capability': 'unknown-solution', href: '/solutions/unknown-solution/',
  }, 'a'));
  const preview = document.append(new Element(document, 'article', {
    class: 'v4-capability-preview v4-capability-preview--dashboard',
  }));
  const image = add(preview, 'data-v4-capability-image', '', { src: solutions[0].image }, 'img');
  add(preview, 'data-v4-capability-kicker', 'ENVIRONNEMENTS INTELLIGENTS');
  const title = add(preview, 'data-v4-capability-title', solutions[0].title);
  add(preview, 'data-v4-capability-copy', 'Initial description');
  const link = add(preview, 'data-v4-capability-link', '', { href: '/solutions/environnements-intelligents/' }, 'a');
  const label = add(link, 'data-v4-capability-link-label', solutions[0].name, {}, 'span');
  add(preview, 'data-v4-capability-status', 'Interface conceptuelle JARVIS');
  const hero = add(document, 'data-v4-hero');
  const environments = ['home', 'business', 'vehicle'].map((name, index) => add(hero, 'data-v4-environment', '', {
    'data-v4-environment': name, class: index === 0 ? 'active' : '', 'aria-selected': String(index === 0),
  }, 'button'));
  for (const attribute of ['hero-image', 'hero-kicker', 'hero-lead', 'console-title', 'console-copy', 'signal-one', 'signal-two', 'signal-three', 'console-link']) {
    add(hero, `data-v4-${attribute}`, 'Initial hero', attribute === 'hero-image' ? { src: 'initial-hero.webp' } : {});
  }
  const location = { href: 'https://jameslaplume.ca/' };
  const matchMedia = (media) => ({
    media, matches: finePointer, addEventListener() {}, removeEventListener() {},
  });
  const window = { matchMedia, location };
  vm.runInNewContext(controller, { document, window, matchMedia, console }, { filename: 'site-v4.js' });
  return { document, cards, image, title, link, label, preview, hero, environments, location };
}

function hover(card, pointerType = 'mouse') {
  card.dispatch('pointerenter', { pointerType });
  if (pointerType === 'mouse') card.dispatch('mouseenter');
}

function assertPreview(view, solution) {
  assert.equal(view.image.src, solution.image, 'preview image follows the selected solution');
  assert.equal(view.title.textContent, solution.title, 'preview title follows the selected solution');
  assert.equal(view.link.href, `/solutions/${solution.slug}/`, 'CTA destination follows the preview');
  assert.equal(view.label.textContent, solution.name, 'CTA names the exact visible solution');
}

for (const interaction of ['hover', 'focus']) {
  test(`${interaction} synchronizes preview and CTA for every solution, including returning to the first`, () => {
    const view = fixture();
    for (const solution of [...solutions.slice(1), solutions[0]]) {
      const card = view.cards.find((item) => item.dataset.v4Capability === solution.slug);
      if (interaction === 'focus') card.focus(); else hover(card);
      assertPreview(view, solution);
      assert.equal(view.cards.filter((item) => item.classList.contains('active')).length, 1);
      assert.ok(card.classList.contains('active'));
      if (interaction === 'focus') assert.equal(view.document.activeElement, card, 'updating the preview must preserve keyboard focus');
    }
  });
}

test('solution cards preserve native click, modified-click and Enter behavior', () => {
  const view = fixture();
  for (const card of view.cards) {
    const destination = card.href;
    card.focus();
    for (const options of [{ button: 0 }, { button: 0, ctrlKey: true }, { button: 0, metaKey: true }, { button: 0, shiftKey: true }, { button: 1 }]) {
      assert.equal(card.dispatch('click', options).defaultPrevented, false, 'clicks must not be cancelled');
      assert.equal(card.href, destination);
    }
    for (const type of ['keydown', 'keyup']) {
      assert.equal(card.dispatch(type, { key: 'Enter', code: 'Enter' }).defaultPrevented, false, 'Enter must retain native anchor activation');
    }
    assert.equal(card.tabIndex, 0, 'the controller must not remove a link from keyboard order');
    assert.equal(view.document.activeElement, card);
    assert.equal(card.getAttribute('role'), null);
    assert.equal(card.getAttribute('aria-pressed'), null);
  }
  assert.equal(view.location.href, 'https://jameslaplume.ca/', 'the controller must leave navigation to the browser');
});

test('mouse preview changes do not steal focus, and touch hover does not select another solution', () => {
  const fine = fixture();
  fine.cards[1].focus();
  hover(fine.cards[2]);
  assert.equal(fine.document.activeElement, fine.cards[1]);
  const coarse = fixture({ finePointer: false });
  hover(coarse.cards[2], 'touch');
  assertPreview(coarse, solutions[0]);
});

test('an unknown solution slug is ignored without breaking valid solution previews', () => {
  const view = fixture({ unknownSlug: true });
  view.cards[1].focus();
  const unknown = view.cards.at(-1);
  assert.doesNotThrow(() => { hover(unknown); unknown.focus(); });
  assertPreview(view, solutions[1]);
  assert.equal(unknown.dispatch('click', { button: 0 }).defaultPrevented, false);
  view.cards[4].focus();
  assertPreview(view, solutions[4]);
});

test('solution previews and hero environment controls remain independent', () => {
  const view = fixture();
  const heroImage = view.hero.querySelector('[data-v4-hero-image]');
  hover(view.cards[3]);
  assert.equal(heroImage.src, 'initial-hero.webp');
  for (const [index, destination] of [
    [1, '/solutions/automatisation-operations/'],
    [2, '/laboratoire-mobile/'],
    [0, '/solutions/environnements-intelligents/'],
  ]) {
    view.environments[index].dispatch('click');
    assert.equal(view.hero.querySelector('[data-v4-console-link]').href, destination);
    assert.equal(view.environments[index].getAttribute('aria-selected'), 'true');
    assertPreview(view, solutions[3]);
  }
});
