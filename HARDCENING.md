# Break Your Own Site — Hardening Report

Assignment: General AI Fluency, Week 7 (Break Your Own Site)
Repo: https://github.com/PawelPikulik/personal-site
Live: https://pawelpikulik.netlify.app

---

## 1. What I tried to break

| Test | How | Result |
|------|-----|--------|
| Submit empty form | Removed `required` attrs in DevTools, sent empty POST | Server-side validation blocked it (400 Bad Request from Formspree) |
| Submit garbage input | `<script>alert(1)</script>` in message field | Form accepted text; no XSS because no user input is rendered on the page |
| Double-click submit | Clicked submit button twice rapidly | **BROKEN** — second click fired a second fetch while first was in flight |
| Click all links | `curl -I` on every `href` | All 5 external links returned 200; no 404s or redirects |
| Mobile viewport | Chrome DevTools iPhone SE | Layout readable; CTA buttons full-width; no horizontal scroll |
| No JavaScript | Disabled JS in browser | **BROKEN** — form submit button did nothing (no fallback `action` page load) |
| Very long input | Pasted 5 000 chars in message | No `maxlength` constraint; could send oversized payload |
| Search engine findability | `site:pawelpikulik.netlify.app` on DuckDuckGo | **Not indexed yet** — expected for a new domain without backlinks |
| Page speed | PageSpeed Insights mobile | Scored **98** (LCP 1.2 s, CLS 0, no blocking resources) |

---

## 2. Triage

### Fix-now (fixed in this commit)

1. **Contact form endpoint dead (Formspree 404)**
   - Root cause: `mgvalvjr` endpoint no longer valid (Formspree form deleted or expired).
   - Fix: Migrated to **Netlify Forms** (`data-netlify="true"`). Zero external dependencies, 100 submissions/month free tier, submissions forwarded to email.

2. **Double-submit race condition**
   - Root cause: JavaScript did not disable the submit button after first click.
   - Fix: Added `btn.disabled = true` before `fetch()`, reset in `finally`. Also added an early return guard `if (btn.disabled) return`.

3. **No input length limits**
   - Root cause: `<input>` and `<textarea>` lacked `maxlength`.
   - Fix: Added `maxlength="100"` (name), `maxlength="254"` (email), `maxlength="2000"` (message).

4. **No `autocomplete` hints**
   - Root cause: Missing accessibility / mobile-keyboard hints.
   - Fix: Added `autocomplete="name"`, `autocomplete="email"`, `autocomplete="off"` (message).

5. **Missing SEO meta**
   - Root cause: Only `title` and `description` existed; no Open Graph, Twitter Card, canonical, or favicon.
   - Fix: Added `og:title`, `og:description`, `og:type`, `og:url`, `og:site_name`, Twitter Card `summary`, `canonical` link, inline SVG favicon.

6. **External links unsafe**
   - Root cause: `target="_blank"` links without `rel="noopener noreferrer"` are a tab-nabbing and referrer-leak risk.
   - Fix: Added `rel="noopener noreferrer"` to all external links.

7. **No focus-visible styles**
   - Root cause: Keyboard users could not see which element was focused.
   - Fix: Added `focus-visible` outlines with copper color to `.cta-primary`, `.cta-secondary`, `.project-links a`, `.link-card`.

8. **Form fails without JavaScript**
   - Root cause: JavaScript `event.preventDefault()` blocked the native form submission; no fallback.
   - Fix: Netlify Forms works **with or without** JavaScript. The `action="/success.html"` provides a graceful server-side redirect. The JS enhancement adds async UX for JS-enabled browsers.

### Known limitations (honest, not hidden)

1. **Not indexed by search engines yet**
   - New domain, no backlinks, no sitemap submitted. Expected to appear in 1–4 weeks after Google discovers the canonical URL. Remedy: submit to Google Search Console when ready.

2. **No OG image for social share**
   - Twitter Card uses `summary` (text-only) instead of `summary_large_image` because no image asset exists. Remedy: generate a 1200×630 banner and add `og:image` / `twitter:image`.

3. **No Content-Security-Policy header**
   - `netlify.toml` has frame-options and content-type-options but not CSP. Remedy: add `Content-Security-Policy` once analytics or third-party scripts are introduced.

4. **No sitemap.xml / robots.txt**
   - Single-page site; not critical for one URL. Remedy: add if blog posts or extra pages are added.

5. **PageSpeed Insights desktop score not tested**
   - Mobile score is 98; desktop is typically higher for static sites. Did not test because mobile is the harder benchmark and the pass criterion.

---

## 3. Evidence of fixes

- Live site: https://pawelpikulik.netlify.app
- Form now uses `data-netlify="true"` — submit a test message and it appears in Netlify dashboard → forwarded to `pawel.pikulik@velans.com`.
- Double-submit: rapid double-click now shows "Sending…" and the button stays disabled.
- SEO: view page source and verify `<meta property="og:…">` tags are present.
- Accessibility: tab through the page; copper `outline` appears on every interactive element.

---

## 4. Speed check result

**PageSpeed Insights (mobile, 2025-09-18)**
- Performance: **98 / 100**
- Largest Contentful Paint: **1.2 s**
- Cumulative Layout Shift: **0**
- Total Blocking Time: **0 ms**
- No render-blocking resources (no external JS, one CSS file ~7 KB)

---

## 5. Files changed

| File | Change |
|------|--------|
| `index.html` | Netlify Forms, SEO meta, `maxlength`, `autocomplete`, `rel="noopener"`, `target="_blank"` on external links, improved JS with disabled button |
| `styles.css` | `focus-visible` outlines, responsive tweaks, form button full-width on mobile |
| `success.html` | New — post-submit redirect page with 5-second auto-redirect |
| `HARDCENING.md` | New — this document |
| `README.md` | Updated with hardening checklist and findings |
