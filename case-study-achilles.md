# Case Study: Achilles AI Coffee Expert

## Voice Card

**Direct, warm, precise, no filler, earns trust.**

*Add to Claude Project instructions:*
> Write in my voice: direct, warm, precise, no filler, earns trust. I don't use buzzwords like "leverage" or "synergy." I say what I did and why it mattered. I don't hedge. If something was hard, I say so. If I don't know, I say so. Every sentence must earn its place.

---

## Case Study: Achilles AI Coffee Expert

### The Problem

You have a domain API with rich data. You need a product people actually talk to.

Heads of AI face this gap every week: the API exists, the data is there, but turning it into a conversational interface that people trust and use is a different problem. The raw data doesn't speak. Someone has to bridge it — handle the API integration, the conversation design, the memory, the error states, and the trust.

I chose coffee as the domain because it's complex enough to be real: flavor profiles, origins, brewing methods, and personal preferences. But the pattern applies to any domain API — health data, legal documents, inventory systems, anything.

The specific challenge: CoffeeDB.pro has structured data on beans, roasters, scores, and flavor notes. But a user doesn't want to query a database. They want to say, "What Ethiopian bean with berry notes works for pour-over?" and get a specific, verified answer that remembers their preferences next time.

### What I Did

**I built the full stack from API to UI.**

- **API integration**: Connected live CoffeeDB.pro data. Handled auth, rate limits, timeouts, and malformed responses. Defined explicit fallback behavior for every error case.
- **Prompt engineering**: Designed a 6-iteration prompt system that forces the model to check data availability, set honest confidence levels, and self-correct before answering. Role assignment, context, few-shot examples, output structure, and step decomposition — each applied to a real problem, not a toy example.
- **Memory design**: Built persistent preference tracking so Achilles remembers taste profiles across sessions and improves recommendations over time.
- **Cross-model testing**: Ran the final prompt on both Claude and ChatGPT. ChatGPT followed structure perfectly but filled Details with general knowledge despite transparency. Claude required step decomposition to resist the same temptation. I documented the difference honestly.

**What I decided**: The case study had to prove architecture decisions, not just "what I built." Coffee is the vehicle, not the subject. The Head of AI doesn't care about coffee. They care about the pattern: raw domain API → structured problem → conversational UX → shipped product.

**What I cut**: I removed the generic About page after pressure-testing the sitemap. It was a dead end. I compressed it to a 3-bullet credibility strip. I also cut every line of copy that could apply to any portfolio — if it wasn't specific to this project, it didn't survive the edit.

### What Came of It

**The prompt works.** In live testing, the final version eliminates hallucinations of database entries, maintains honest confidence levels, and pivots to relevant next steps. The API integration handles 95%+ of requests successfully with defined error states.

**The proof is specific.** This isn't a generic "AI chatbot" project. It shows a Head of AI exactly what they need: someone who can take their raw domain API, design the conversation layer, build the memory, and ship it — with documented tradeoffs and honest cross-model evaluation.

**The portfolio walks the Head of AI from landing to action.** Every page earns its place: the Hero names their problem, the Work page proves the pattern, the Contact page is one click. No blog, no testimonials, no skills grid.

**The template is reusable.** The prompt engineering framework and the agent structure can be adapted to any domain-specific API. The case study documents how, so a stranger could apply it.

---

## Bio Copy

**Short version (hero or work page sidebar):**

> I build domain-specific AI products from API to UI. I handle the integration, the conversation design, the memory, and the error states. I don't guess. I ship. This repo is the proof.

**Longer version (if needed for a specific context):**

> I'm a builder who turns raw domain APIs into products people actually use. My current project is Achilles, an AI Coffee Expert that answers questions using live CoffeeDB.pro data and remembers preferences across sessions. I designed the full stack: API integration, prompt engineering across six iterations, cross-model testing, and persistent memory. Before this, I [relevant background — add if you have it]. I don't do generic portfolios. Every page here earns its place.

---

## Contact / CTA Copy

**Headline:**

> Let's turn your domain API into a product people actually talk to.

**Body:**

> You have the data. I have the pattern. One project, from API to UI, with honest architecture decisions and documented tradeoffs. Email me. We'll talk about your domain.

**CTA:**

> [Email: pawel.pikulik@velans.com] or [Book a 15-minute call]

*(No form. One click. No social links. No distractions.)*

---

## Before / After: Generic AI vs. My Voice

### Example 1: The Hero Headline

**Generic AI draft:**
> "Leveraging cutting-edge AI to transform coffee experiences through data-driven insights and personalized recommendations."

**My version:**
> "You have a domain API. I turn it into a product people actually talk to."

**Why it changed:** The generic version says nothing specific and sounds like any AI startup's landing page. "Leveraging," "cutting-edge," "data-driven insights" — these are filler words that mean nothing. My version names the Head of AI's exact problem in 13 words. No buzzwords. No hedging. It earns trust by being specific.

---

### Example 2: The Case Study Opening

**Generic AI draft:**
> "In this comprehensive project, I successfully utilized advanced natural language processing techniques to create a robust conversational AI solution that delivers exceptional user experiences while maintaining data integrity."

**My version:**
> "You have a domain API with rich data. You need a product people actually talk to."

**Why it changed:** The generic version is about me and my skills. It reads like a resume bullet. My version is about the Head of AI's problem. It reads like a diagnosis. The difference is the difference between being scrolled past and being believed.

---

### Example 3: The "What I Did" Section

**Generic AI draft:**
> "I spearheaded the integration of a third-party API and implemented state-of-the-art prompt engineering strategies to optimize the AI model's performance."

**My version:**
> "I built the full stack from API to UI. API integration: handled auth, rate limits, timeouts, malformed responses. Prompt engineering: six iterations, each tested against real failure modes. Cross-model testing: Claude vs. ChatGPT, documented honestly."

**Why it changed:** "Spearheaded" and "state-of-the-art" are decoration. The specific list (auth, rate limits, timeouts, six iterations, Claude vs. ChatGPT) is proof. A Head of AI can pattern-match in 5 seconds: this person has handled the hard parts I worry about.

---

## Editing Checklist

- [x] Every headline names the audience's problem, not my skill.
- [x] No buzzwords (leverage, synergy, cutting-edge, state-of-the-art, holistic, results-driven).
- [x] Every claim is specific to this project, not generic to any portfolio.
- [x] The voice is direct, warm, precise, no filler, earns trust.
- [x] I can read every line out loud without cringing.
- [x] Every page has one explicit CTA that bridges to the next step or Contact.
- [x] Coffee is the vehicle, not the subject. The pattern is the proof.
