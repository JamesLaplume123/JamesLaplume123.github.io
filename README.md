# jameslaplume.ca

Premium one-page website for James Laplume — smart systems, private
infrastructure and real automation.

Positioning:

```text
James Laplume — Smart spaces. Private systems. Real automation.
```

## Sections

- Cinematic hero with clear positioning and CTAs
- Four service categories
- Interactive smart-system demonstration
- Featured Connected Ambulance project
- Stylized route map / field atlas
- Five-step working process
- Technical project journal
- Technology stack
- Contact form that prepares a mailto email
- French / English language toggle

## Files

- `index.html`: page structure and French default copy
- `styles.css`: premium dark interface, responsive layout and animations
- `script.js`: language toggle, demo, route map state and contact form
- `assets/hero-studio.png`: generated architectural hero image
- `CNAME`: custom domain for GitHub Pages
- `.nojekyll`: tells GitHub Pages to serve files as a plain static site

## Deployment

This site is intentionally static and fast for GitHub Pages. A React build can be
introduced later if the interactive demo becomes a larger app with real backend
state, dashboards, authentication or API integrations.

## DNS

GitHub Pages apex records:

```text
@ -> 185.199.108.153
@ -> 185.199.109.153
@ -> 185.199.110.153
@ -> 185.199.111.153
```

GitHub Pages `www`:

```text
www -> CNAME -> JamesLaplume123.github.io
```

Mail separation:

```text
mail -> A -> 54.39.226.237
@ -> MX -> mail.jameslaplume.ca.
```
