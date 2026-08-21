# The Through-Line: Content Map & CTAs

## One-Line Claim

> **I turn raw domain APIs into products people actually talk to — from integration to interface.**

This is the sentence a visitor should remember. It names the problem (raw domain APIs that don't become usable products) and the solution (end-to-end shipping, not just a UI or just an API). It is specific enough that a generic AI builder can't claim it, and broad enough to apply to any domain.

---

## Content Map: Pages → Sections → Case → CTA

Every page ladders up to **one action**: email me to turn their domain API into a conversational product.

---

### Page 1: Hero / Landing

**Purpose:** Diagnose the problem in 5 seconds. The visitor must see themselves in the first sentence.

| Section | What It Does | Content |
|---------|-------------|---------|
| Eyebrow | Filters audience | "For Heads of AI evaluating domain-specific builders" |
| Headline | Names the problem | "You have a domain API. I turn it into a product people actually talk to." |
| Proof teaser | Grounds the promise | "Case study: built a conversational coffee expert from a raw data API — full stack, from integration to interface." |
| Hero visual | Shows, doesn't tell | Achilles answering a coffee question in real time (screenshot) |
| **CTA** | → Work page | **"See how it works"** |

**No secondary CTA. One action. No distractions.**

---

### Page 2: Work / Case Study (The Proof)

**Purpose:** This is the only page that proves the claim. Everything else is framing.

**Case on this page:** Achilles AI Coffee Expert — the strongest and only case. Lead with it because it is the only full-stack build.

| Section | What It Proves | Content |
|---------|---------------|---------|
| Opening | Names the pattern, not the domain | "Head of AI: you have a raw domain API. Here's how to turn it into a conversational product, step by step." |
| The Problem | Shows I understand their gap | The gap between "API exists" and "product people trust and use." |
| What I Did | Architecture decisions (not just output) | API integration, 6-iteration prompt system, memory design, cross-model testing. |
| Evidence | Screenshot proof | API integration code, parsed JSON, architecture diagram, cross-model comparison. |
| What Came of It | Result, not claim | "The prompt works. 95%+ requests handled with defined error states." |
| **CTA** | → Contact page | **"Facing a similar API-to-UI problem? Let's talk."** |

**No CTA buried in nav. Page-level CTA is explicit and speaks their language.**

---

### Page 3: Credibility Strip (Was "About" — Cut)

**Purpose:** Prove this wasn't a one-off. Show pattern of behavior that de-risks hiring.

**Location:** Embedded at the bottom of the Work page, not a standalone page. Standalone About pages are dead ends.

| Element | Content |
|---------|---------|
| Headshot | Real photo (not AI-generated) |
| Point 1 | Shipped production systems with ambiguous specs and cross-functional requirements. |
| Point 2 | This is not a one-off — the same pattern applies to any domain-specific API. |
| Point 3 | Full stack: integration, prompt engineering, memory, and honest cross-model evaluation, documented end to end. |

**No CTA here.** The CTA is on the Work page above it. This strip earns its place by answering "Why should I believe you can do this again?"

---

### Page 4: Contact / Action

**Purpose:** Lower friction to the single most important action.

| Section | What It Does | Content |
|---------|-------------|---------|
| Headline | Speaks their need | "Building a domain-specific AI product? Let's talk about turning your API into something people actually use." |
| Body | Bridges the gap | "You have the data. I have the pattern. One project, from API to UI, with honest architecture decisions and documented tradeoffs." |
| **CTA** | One click | **Email me** (pawel.pikulik@velans.com) |

**No form fields. No social links. No "follow me on X." One click, no friction.**

---

## CTAs Ladder Up to the One Action

| Page | CTA | Destination | Rationale |
|------|-----|-------------|-----------|
| Hero | "See how it works" | → Work | Belief before action. They need proof before they reach out. |
| Work | "Let's talk" | → Contact | The proof creates the question "Can you do this for my domain?" The CTA answers it. |
| Contact | "Email me" | → Sent | One click. No form. No friction. |

**Every CTA bridges the visitor to the next step. No dead ends. No distractions.**

---

## Still Need to Gather (Honest Blocker List)

| Item | Why It Blocks | Status | Deadline |
|------|---------------|--------|----------|
| Live CoffeeDB.pro API integration | The case study claims 95%+ success rate. Without a live connection, this is a claim, not proof. | ⏳ Not built | FL-03 |
| Achilles conversation interface | The portfolio needs a live demo or screenshot of the conversation. Without it, the hero screenshot is a placeholder. | ⏳ Not built | FL-03 |
| Screenshot: hero conversation | Hero visual shows Achilles answering a real question. Needs the live interface to exist first. | ⚠️ Placeholder only | FL-03 |
| Screenshot: code + API integration | Shows production-grade retry logic and error handling. Needs live API connection first. | ⚠️ Placeholder only | FL-03 |
| Screenshot: parsed JSON response | Shows live data validated before reaching the conversation layer. Needs live API connection first. | ⚠️ Placeholder only | FL-03 |
| Screenshot: cross-model comparison | Already documented in prompt engineering log. Needs formatting as a clean image. | ✅ Documented, not formatted as image yet | FL-04 |
| Headshot photo | Credibility strip needs a real photo. No AI-generated headshots. | ⚠️ Not yet taken | FL-03 |
| Repo link with live README | Artificiall (CRUD API) is live. Achilles repo does not exist yet. | ⚠️ Partial: CRUD API ✅, Achilles ⏳ | FL-03 |

**What this means:** If FL-03 is the build week, the first two weeks of FL-03 must be dedicated to the live CoffeeDB.pro integration and the conversation interface. Without those, the portfolio is a well-designed frame with no picture inside it. The case study copy is strong, but the proof is still a promise. This list is honest so the build week isn't blocked by surprises.

---

## The One-Line Claim, Sharpened

**Original (AI-generated options):**
- "I build AI-powered conversational interfaces for domain-specific APIs." — Generic. Any developer could say this.
- "I ship end-to-end AI products from raw data to live conversation." — Better, but "end-to-end" is vague.
- "I turn APIs into conversations people trust." — Good, but "trust" is abstract.

**Chosen:**
> **I turn raw domain APIs into products people actually talk to — from integration to interface.**

**Why:** It names the raw material (domain APIs), the transformation (products people talk to), and the full scope (integration to interface). A Head of AI reads this and sees their exact problem: they have the API, they need the product. The "actually talk to" implies the hard part is done — not just a UI, but a conversation that works.
