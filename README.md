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
  - Posts asynchronously via JavaScript to Formspree (`https://formspree.io/f/mgvalvjr`)
  - No page reload; instant success/error feedback
  - Submissions forwarded to `pawel.pikulik@velans.com`
  - Free tier (50 submissions/month)
  - See [`backend-explainer.md`](backend-explainer.md) for full data-flow explanation

## Post-deployment checklist

- [x] Site loads over HTTPS with padlock
- [x] Rename URL from random slug to `pawelpikulik`
- [x] Contact form present and styled
- [ ] Test contact form submission reaches inbox
- [ ] Test in private/incognito window
- [ ] Test on phone
- [ ] LinkedIn profile links to this site
- [ ] CV links to this site
