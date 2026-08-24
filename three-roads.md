# Three Roads: Stack Rationale

## The Prompt I Gave AI

> I am building a portfolio to prove one claim: I can ship domain-specific AI products from API to UI. The audience is a Head of AI who needs to turn a raw domain API into a live, conversational product. The action I want them to take is to email me.
>
> **My portfolio is currently a single-page HTML site** (index.html + styles.css) with a dark theme, Space Grotesk + Inter fonts, charcoal/copper palette. It has 4 sections: Hero, Work/Case Study, Credibility Strip, Contact. No backend needed for the portfolio itself.
>
> **My constraints:**
> 1. **Free only.** I will not pay for hosting or tools for this portfolio.
> 2. **Honest skill level:** I know Python (FastAPI), HTML/CSS, and basic JavaScript. I am not a frontend specialist. I have built a CRUD API with FastAPI. I have not built a production React app or managed a CI/CD pipeline.
> 3. **What my portfolio needs to do:** Display a case study with text, image galleries (screenshots of code, API responses, architecture diagrams), links to code repos, and a contact email. No blog. No CMS. No testimonials page. No dynamic content for the portfolio itself.
> 4. **How my work must be displayed:** Long-form reading (the case study text), image galleries (screenshots), code repo links, and potentially an embedded demo or iframe if I build Achilles live. The Head of AI must see the proof in 30 seconds and believe it in 3 minutes.
>
> **Backend question:** The portfolio itself does not need a backend. The Achilles AI Coffee Expert (the project in the case study) would need a backend, but that is a separate project, not the portfolio. For the portfolio, static is fine unless the embedded demo requires it.
>
> Give me three stack options, simplest to most powerful, with real trade-offs. For each: how I'd build, where I'd host (free), whether it needs a backend, and the honest trade-off.

---

## The Three Options (AI Response)

### Option 1: Keep What I Have — Static HTML/CSS on GitHub Pages

- **How I'd build:** Pure HTML, CSS, and a tiny bit of vanilla JavaScript. No build step. Just edit files and push.
- **Where I'd host:** GitHub Pages (free, custom domain support, HTTPS out of the box).
- **Backend needed:** No. Zero.
- **Trade-off:** The fastest path to live. What I have now works. I can ship today. But if I ever want to add a live demo of Achilles, I'd need a separate backend or a different stack. Also, no image optimization, no lazy loading, no component reuse. Every page is hand-written.

### Option 2: Vite + React (or Preact) + Netlify

- **How I'd build:** Vite for a fast dev server and build step. React (or Preact, lighter) for component-based sections. Each portfolio section becomes a component. Images handled with Vite's asset handling.
- **Where I'd host:** Netlify (free tier, drag-and-drop or git push, automatic HTTPS, form handling if I ever need it).
- **Backend needed:** No. Still static output. But I could add Netlify Functions (serverless) later if I need a lightweight backend for a demo.
- **Trade-off:** I get component reuse, image optimization, and a modern dev experience. But I have to learn React/Vite, manage `node_modules`, and deal with build failures. For a 4-page portfolio, this is a lot of tooling overhead. The case study text doesn't benefit from React components. The images don't need lazy loading on a page this small. The "future-proofing" is theoretical — I don't have a second case study yet.

### Option 3: Next.js (App Router) + Vercel

- **How I'd build:** Next.js with the App Router. React components, server-side rendering for SEO, image optimization with `next/image`. API routes if I ever want to proxy the CoffeeDB.pro API or serve a live demo from the same domain.
- **Where I'd host:** Vercel (free tier, serverless functions, edge network, automatic preview deployments).
- **Backend needed:** Optional. The portfolio itself is still static. But I can add API routes (serverless) for a live demo, form handling, or a lightweight backend without spinning up a separate server.
- **Trade-off:** The most powerful and most complex. I get SEO, image optimization, the ability to add a live demo later, and a modern framework on my resume. But the learning curve is steep: Next.js App Router, React Server Components, Vercel's deployment model, caching rules. Build times are slow. The "backend" I'd add is serverless, which has cold starts and rate limits on the free tier. For a portfolio that doesn't need a backend today, this is over-engineering. I'd spend 2 weeks learning the framework instead of building the case study proof.

---

## Pressure-Test: What Breaks?

### Option 1 (Static HTML / GitHub Pages)

- **What breaks if I pick the simplest?** Nothing, for the portfolio. But if I build a live Achilles demo, I can't embed it on the same domain without a backend. I'd need a separate hosting solution for the demo (e.g., Vercel for the FastAPI backend, GitHub Pages for the portfolio). Two repos, two deploys. That's fine — the portfolio is the proof, the demo is the extra.
- **What do I maintain?** Almost nothing. HTML and CSS don't break. GitHub Pages is free and stable. If I stop touching it for 6 months, it still works.
- **Can I finish in two weeks?** Yes. It's already built. I just need to replace the placeholder images with real screenshots and a headshot.
- **Does it show my work well?** Yes. The case study text is readable. The screenshots are visible. The code repo links work. The design is intentional and dark. A Head of AI doesn't care about the framework; they care about the proof.

### Option 2 (Vite + React + Netlify)

- **What breaks?** The build step. If I update a dependency and it breaks, I have to debug npm, Vite config, and React version mismatches. For a 4-page site, this is unnecessary stress. Also, React's hydration can cause layout shifts if I'm not careful with images.
- **What do I maintain?** `node_modules`, `package.json`, build scripts, Netlify config. Every update is a potential breakage.
- **Can I finish in two weeks?** Maybe, but half the time would be spent on tooling, not on the content. I'd be learning React instead of writing the case study.
- **Does it show my work well?** No better than Option 1. The images are the same. The text is the same. The Head of AI doesn't see "React" and think "this person is better." They see the proof.

### Option 3 (Next.js + Vercel)

- **What breaks?** Everything, if I'm not careful. Next.js App Router is powerful but complex. Cache invalidation, server component boundaries, image optimization config, Vercel's function limits. The build can fail for reasons I don't understand. Cold starts on serverless functions make a demo feel slow.
- **What do I maintain?** A full React framework, Vercel deployment config, API route code, dependency updates. This is a part-time job.
- **Can I finish in two weeks?** No. I'd spend the first week learning Next.js and fighting the build. The second week would be frantic. The portfolio would be half-baked.
- **Does it show my work well?** Only if I build the live demo. Without the demo, it's a fancy wrapper around the same content. The Head of AI sees the case study, not the framework. And if the demo is slow or broken, it hurts the proof.

---

## The Decision

**I chose Option 1: Static HTML/CSS on GitHub Pages.**

### Why Option 1

It is the right tool for the job. My portfolio is 4 sections, one page, text + images + links. No dynamic content. No user accounts. No database. A static HTML file is exactly what this needs. I can open it in a browser, edit it in any text editor, and push it to GitHub Pages in one command. The design is already intentional (dark theme, custom fonts, copper accents). The content is already written. The only thing missing is the real screenshots and the headshot — not a framework.

### Why I Didn't Choose Option 2

React and Vite are good tools, but they solve problems I don't have. I don't need component reuse for a single page. I don't need a build step for CSS and HTML. I don't need `npm install` for a portfolio that has no interactivity. The overhead — learning React, managing dependencies, debugging build failures — is time I should spend on the case study proof, not on tooling. The case study is what converts the Head of AI, not the tech stack.

### Why I Didn't Choose Option 3

Next.js is overkill. The App Router, server components, and serverless functions are designed for apps with dynamic data, user sessions, and complex routing. My portfolio has none of that. The "future-proofing" argument is a trap: I don't have a second case study, a blog, or a live demo yet. If I build those later, I'll choose the right stack *then*, based on what they actually need. Today, Next.js would be a distraction. I'd spend two weeks learning a framework instead of two weeks making the proof bulletproof.

### Can I Maintain This?

Yes. HTML and CSS are stable. They don't break on update. GitHub Pages is free and requires zero configuration. If I come back in 6 months, the site will still work. If I want to add a new case study, I copy the HTML section and paste a new image. No build step. No dependency hell. This is maintainable because there is almost nothing to maintain.

### Does It Show My Work Well?

Yes. The Head of AI sees the case study first, the design second, the stack never. The proof is in the text (architecture decisions, honest trade-offs, cross-model evaluation) and the images (screenshots of code, API responses, comparison tables). A static HTML site loads instantly, works on any device, and doesn't distract with animations or interactivity. The design is intentional — dark, precise, technical — but it frames the work, it doesn't upstage it. That is exactly what the identity kit says: "The design frames the work — it never upstages it."

### The Honest Backend Answer

The portfolio itself does not need a backend. It is a static site. If I build a live Achilles demo later, I will host it separately (FastAPI on a free tier like Render, Railway, or Vercel's serverless). The portfolio will link to it or embed it via iframe. The two don't need to share a stack. That is the honest answer: the backend is a separate decision for a separate project, not a reason to over-engineer the portfolio today.
