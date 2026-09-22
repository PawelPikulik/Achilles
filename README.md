# Pawel Pikulik — Personal Site

One-page personal website: who I am, what I build, links to LinkedIn, GitHub, portfolio, and email.

**Live URL:** [pawelpikulik.netlify.app](https://pawelpikulik.netlify.app) ✅ Deployed

## Deploy to Netlify

### Option A: Netlify Drop (fastest — ~2 minutes)

1. Zip the folder contents (`index.html`, `styles.css`, `netlify.toml`).
2. Go to [netlify.com/drop](https://app.netlify.com/drop).
3. Drag the zip onto the page.
4. You get a live HTTPS URL instantly.
5. Go to **Site configuration → Change site name** and rename to `pawelpikulik`.

### Option B: Git deploy (auto-publish on every push)

1. Push this repo to GitHub:
   ```bash
   git remote add origin https://github.com/PawelPikulik/personal-site.git
   git push -u origin main
   ```
2. In Netlify: **Add new site → Import from GitHub** → select `personal-site`.
3. Set build command to `echo 'Static site — no build step'` and publish directory to `.`.
4. Netlify auto-deploys on every push.
5. Rename site to `pawelpikulik` in site settings.

## What is in this repo

| File | Purpose |
|------|---------|
| `index.html` | The page: hero, featured project (Achilles), links, future posts space, **working contact form** |
| `styles.css` | Dark Roast Precision design system (Space Grotesk + Inter) |
| `netlify.toml` | Security headers, publish config |
| `dns-walkthrough.md` | DNS explanation for PF-04 deliverable |
| `backend-explainer.md` | Plain-words explainer: what a backend is, how the contact form data flows, why Formspree (Week 6) |

## Links to update before going live

- `index.html` line 50: LinkedIn URL (`https://linkedin.com/in/pawelpikulik`)
- `index.html` line 54: GitHub profile (`https://github.com/PawelPikulik`)
- `index.html` line 58: Portfolio/CV link
- `index.html` line 62: Booking/email link

## Features

- **Working contact form** (Week 6 — "Make It Do Something")
  - Netlify Forms (no external dependencies, 100 submissions/month free)
  - Works with or without JavaScript (graceful degradation)
  - Disabled-button protection against double-submit
  - Input length limits (`maxlength`), autocomplete hints
  - Submissions forwarded to `pawel.pikulik@velans.com`
  - See [`backend-explainer.md`](backend-explainer.md) for full data-flow explanation

- **SEO / Meta** (Week 7 — "Break Your Own Site")
  - Open Graph tags, Twitter Card, canonical URL, inline SVG favicon
  - Page title and description optimized for search

- **Accessibility**
  - `focus-visible` outlines on all interactive elements
  - Semantic HTML (`<header>`, `<main>`, `<section>`, `<footer>`)
  - Mobile-first responsive layout (no horizontal scroll)

## Post-deployment checklist

- [x] Site loads over HTTPS with padlock
- [x] Rename URL from random slug to `pawelpikulik`
- [x] Contact form present and styled
- [x] Test contact form submission reaches inbox
- [x] Test in private/incognito window
- [x] Test on phone (Chrome DevTools iPhone SE)
- [x] Double-submit race condition fixed
- [x] No-JavaScript fallback works
- [x] SEO meta added
- [ ] LinkedIn profile links to this site
- [ ] CV links to this site
- [ ] Submit to Google Search Console

## Domain + Badge + Analytics (Week 7 — "Plant Your Flag")

- **Domain:** https://pawelpikulik.netlify.app (free Netlify subdomain, HTTPS enforced)
- **Analytics:** Google Analytics 4 installed (replace `G-XXXXXXXXXX` in `index.html` with your real Measurement ID)
- **SEO:** Open Graph, Twitter Card, canonical URL, favicon — verified on live site
- **FlyRank badge:** Placeholder in footer; replace `YOUR_CREDENTIAL_REF` and `YOUR_FIRST_NAME` when credential is issued

## Hardening report

See [`HARDCENING.md`](HARDCENING.md) for the full "Break Your Own Site" findings: what was tested, what broke, what was fixed, and what is an honest known limitation.
