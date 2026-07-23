# jameslaplume.ca

Premium multi-page static website for **James Laplume - Intelligent Systems Lab**.

Positioning:

```text
Tout connecter. Tout contrôler.
Everything connected. Everything under your control.
```

## Pages

- `index.html`: cinematic home page with interactive smart home, dashboard, security, route atlas, Jarvis Lab and service sections
- `solutions.html`: solutions organized by customer outcomes
- `lab.html`: technical lab, stack and honest status labels
- `mobile-lab.html`: flagship connected ambulance project, Ford 2017 V10
- `projects.html`: project and case-study system
- `learn.html`: article index with filters and Markdown reader
- `about.html`: James background and learning roadmap
- `contact.html`: detailed contact form that prepares a mailto email

## Content System

Most repeatable content lives in:

```text
data/site-data.js
```

Update that file to change:

- services
- solution categories
- smart home scenarios
- dashboard actions
- security demo modes
- mobile ambulance systems
- route atlas entries
- process steps
- lab status items
- certification roadmap
- stack chips
- project cards
- article metadata

Technical articles live in:

```text
articles/*.md
```

To add an article:

1. Create a new Markdown file in `articles/`.
2. Add its metadata to `data/site-data.js` under `articles`.
3. Use the same `slug` as the Markdown filename without `.md`.

## Assets

Main images:

- `assets/smart-home-architecture.png`
- `assets/systems-lab.png`
- `assets/ambulance-quebec-garage.png`

The ambulance image is intentionally Quebec-style and based on the requested Ford 2017 V10 project direction.

## Deployment

This site is intentionally static and fast for GitHub Pages.

Required repository settings:

- Repository: `JamesLaplume123/JamesLaplume123.github.io`
- Branch: `main`
- Source: `/`
- Custom domain: `jameslaplume.ca`

Important files:

- `CNAME`: custom domain
- `.nojekyll`: serve static files directly

## DNS

Authoritative nameservers:

```text
parking1.whc.ca
parking2.whc.ca
```

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

## Future Private App

Public website:

```text
jameslaplume.ca
```

Future private system:

```text
app.jameslaplume.ca
```

The private system should remain behind authentication or VPN and must not expose real Home Assistant tokens, camera streams, private URLs, IP addresses or infrastructure credentials.
