# Track Thread Post — Weeks 01–03

*(Copy the content below into your track thread. Replace the repo link if needed.)*

---

**Repo:** https://github.com/PawelPikulik/FlyRank

**Proof statement:** I can ship domain-specific AI products from API to UI. Audience: a Head of AI who needs to turn a raw domain API into a live, conversational product. Action: reach out to me to build theirs.

**Project:** Achilles — an AI Coffee Expert that answers coffee questions and remembers preferences using live data from CoffeeDB.pro.

## Week 01 — Draw the Path + Workflow Audit
- Sitemap (4 sections: Hero, Work, Credibility Strip, Contact): [`sitemap.md`](https://github.com/PawelPikulik/FlyRank/blob/main/sitemap.md)
- Claude Project setup + pressure-test: [`claude-project-setup.md`](https://github.com/PawelPikulik/FlyRank/blob/main/claude-project-setup.md), [`pressure-test-output.md`](https://github.com/PawelPikulik/FlyRank/blob/main/pressure-test-output.md)
- Workflow audit (15 tasks classified) + 3 target tasks: [`workflow-audit.md`](https://github.com/PawelPikulik/FlyRank/blob/main/workflow-audit.md), [`target-tasks.md`](https://github.com/PawelPikulik/FlyRank/blob/main/target-tasks.md)

## Week 02 — Frame It as Cases + Prompt Engineering
- Case study (3 beats, voice card, before/after): [`case-study-achilles.md`](https://github.com/PawelPikulik/FlyRank/blob/main/case-study-achilles.md)
- Prompt engineering log (6 versions, Claude vs. ChatGPT): [`prompt-engineering-log.md`](https://github.com/PawelPikulik/FlyRank/blob/main/prompt-engineering-log.md)
- Prompt ladder (baseline + 5 versions, one honest "didn't help" moment): [`prompt-ladder-apicode.md`](https://github.com/PawelPikulik/FlyRank/blob/main/prompt-ladder-apicode.md)

## Week 03 — Curate Your Images
- Image set + rejection note: [`curated-image-set.md`](https://github.com/PawelPikulik/FlyRank/blob/main/curated-image-set.md)
- Screenshot/prompt guide: [`assets/screenshot-and-prompt-guide.md`](https://github.com/PawelPikulik/FlyRank/blob/main/assets/screenshot-and-prompt-guide.md)

**Rejected image:** A generated "futuristic AI robot barista with holographic data streams" — looked impressive but misrepresented the product (Achilles is text-based, not a robot) and clashed with the grounded, data-driven claim.

**Live site (in progress):** [`index.html`](https://github.com/PawelPikulik/FlyRank/blob/main/index.html) — Dark Roast Precision styling, images pending.

---

## ⚠️ Before Posting: Manual Steps Still Required

These need to be done on your machine before the image set is truly "final" — I cannot do any of these:

1. **Capture 5 screenshots** (exact steps in `assets/screenshot-and-prompt-guide.md`):
   - Hero conversation → save to `assets/screenshots/hero-conversation.png`
   - Code snippet → save to `assets/screenshots/code-api-integration.png`
   - API response JSON → save to `assets/screenshots/api-response-json.png`
   - Prompt ladder V0 vs V5 → save to `assets/screenshots/prompt-ladder-v0-vs-v5.png`
   - Cross-model comparison → save to `assets/screenshots/cross-model-comparison.png`

2. **Generate 2 AI images** using the prompts in the same guide (DALL-E/Midjourney/Stable Diffusion — pick one):
   - Hero texture → save to `assets/generated/hero-texture.png`
   - Architecture diagram → save to `assets/generated/architecture-diagram.png`

3. **Save your headshot** (a real photo, per your own curation criteria) → `assets/headshot/headshot.jpg`

4. **Commit and push** once files are in place:
   ```powershell
   git -C "C:\Users\velan\FlyRank" add assets/
   git -C "C:\Users\velan\FlyRank" commit -m "Add final image assets: screenshots, generated textures, headshot"
   git -C "C:\Users\velan\FlyRank" push origin main
   ```

5. **Open `index.html` in a browser** to verify all images render correctly (placeholders will disappear automatically once files exist at the correct paths).

6. **Post this summary** (top section above) to your track thread.
