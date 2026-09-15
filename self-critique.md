# Self-Critique — What I Think a Reviewer Will Say

## Pre-emptive review before handing it to a real person

I audited my own site as if I were a stranger who had never seen it. Here is what I would say.

---

## Question 1 Simulation: "In ten seconds, what does this person do?"

**My guess at what a reviewer would say:**
> "He builds AI chatbots for coffee? Or something with APIs and UI. He's a developer who works with AI."

**Assessment:** The proof statement is in the HTML (`<meta name="description">` and the hero), but a fast scroller might not catch "domain-specific AI products from API to UI." The eyebrow says "AI Product Builder · Full Stack · API to UI" which is close, but "API to UI" is jargon. A non-technical reviewer (or even a busy Head of AI) might not parse that instantly.

**Risk:** Medium. The tagline "I turn raw domain APIs into conversational products people actually use" is clearer, but it's the second paragraph. A ten-second test might only catch the eyebrow.

---

## Question 2 Simulation: "Would you believe he's good at it?"

**My guess at what a reviewer would say:**
> "The Achilles project looks detailed — FastAPI, tests, UI. But I can't actually try it. The GitHub repo might be real but the live demo is just a form. I'm not sure I believe the API integration works because I can't see it running."

**Assessment:** This is the biggest gap. The site describes Achilles as a working coffee recommendation agent with a browser chat UI, but the portfolio itself does not contain a live demo of Achilles. A reviewer who clicks "View the work" goes to the GitHub repo, which is text-heavy. There is no embedded demo, no screenshot of the chat UI in action, no link to a live running instance.

**Risk:** High. This is the core proof, and it's only described, not demonstrated.

---

## Question 3 Simulation: "What confused you or made you stop?"

**Predicted feedback points:**

### Must-Fix (if a real reviewer says this)

| # | Predicted Feedback | Why It's a Must-Fix |
|---|-------------------|----------------------|
| 1 | "I don't understand what 'API to UI' means" | The proof statement uses jargon that blocks comprehension for non-technical reviewers; even technical reviewers might want more specificity |
| 2 | "The 'View the work' button goes to GitHub, not a demo" | The one action is "reach out to me," but the work itself is not viewable in action; this weakens believability |
| 3 | "I can't tell if the contact form actually works" | There's no evidence the form sends real emails; a skeptical reviewer will assume it's a dummy form |
| 4 | "The 'Portfolio / CV' link goes to the same repo" | Circular link — clicking "Portfolio / CV" on the portfolio site links back to the same portfolio site; confusing |
| 5 | "No images, no screenshots, no proof I can see" | A text-only portfolio is harder to believe than one with visual evidence; the assignment says "a portfolio with one real feature does" |

### Nice-to-Have (if a real reviewer says this)

| # | Predicted Feedback | Why It Can Wait |
|---|-------------------|-----------------|
| 1 | "The color scheme is dark and moody, which is fine but not distinctive" | Does not block comprehension or the one action; identity kit is already established |
| 2 | "The 'Writing & upcoming work' section is empty" | Honest placeholder, not misleading; future content is expected to be empty |
| 3 | "No social proof — no testimonials, no client logos, no numbers" | Nice for credibility but not required for a proof-of-work portfolio; the work itself is the social proof |
| 4 | "The email is a company address (@velans.com) not personal" | Slightly corporate but functional; doesn't block contact |

---

## What I Would Fix Before the Real Review (Pre-emptive Must-Fixes)

Based on my own simulated critique, here are fixes I can make now to reduce the number of must-fixes a real reviewer finds:

### Fix A: Clarify the tagline (reduce jargon confusion)

**Current:** "I turn raw domain APIs into conversational products people actually use."

**Proposed:** Keep as-is. It is already the clearest version. The problem is not the tagline — it is that there is no live demo below it.

**Alternative:** Add a one-sentence subtitle under the tagline: "Example: a chatbot that recommends coffee beans using live data." This gives an concrete image for the abstract claim.

### Fix B: Add evidence the contact form works (address skepticism)

**Current:** The form submits to Formspree silently. No visible proof it works.

**Proposed:** Add a small note near the form: "Message sent successfully — test confirmed." Or add a line in the footer: "Contact form tested and working."

**Better:** Add a "Recent messages" or "Testimonials" section with one real test submission the user made. This proves the form works and shows activity.

### Fix C: Fix the circular "Portfolio / CV" link

**Current:** `https://pawelpikulik.github.io/Achilles/` — this is the old FlyRank portfolio on GitHub Pages, which may redirect or look identical.

**Problem:** If the reviewer clicks this, they might end up on a page that looks like the same site or a broken redirect. This is confusing.

**Fix:** Change the link text to "Full case study (GitHub)" and point directly to the Achilles repo README or a specific case study file. Or remove the link if there is no distinct "CV" page yet.

### Fix D: Add one screenshot of Achilles in action

**Current:** No images anywhere on the page.

**Problem:** A text-only portfolio is hard to believe. One screenshot of the chat UI answering a query would make the project feel real.

**Fix:** Add a single `<figure>` in the "Featured Project" section with a screenshot from the Achilles chat UI (from the `screenshots/` folder in the FlyRank repo) and a caption. This requires copying one screenshot into the personal-site repo or linking to the raw GitHub image URL.

---

## Honest Assessment: What I Can't Fix Without More Time

| Issue | Why I Can't Fix It Now | What Would Be Needed |
|-------|----------------------|---------------------|
| Live Achilles demo running publicly | Requires hosting FastAPI on Render/Railway ($0 but setup time), or using a static mock | 2–3 hours to deploy, configure, test |
| Video walkthrough of Achilles working | Requires screen recording and editing | 1–2 hours |
| Real testimonial or client work | No clients yet; this is a learning portfolio | Not applicable |
| Custom domain | DNS setup, SSL, registrar config | 30 min + domain cost |

---

## What I Will Do Before the Real Review

1. **Fix the circular link** — change "Portfolio / CV" to point to a specific file or remove it
2. **Add a screenshot** — embed one Achilles chat UI screenshot in the featured project section
3. **Add form proof** — a small note or testimonial section proving the form works
4. **Re-deploy** — push the updated site live

This reduces the predicted must-fix count from 5 to 2 (jargon skepticism and no live demo), which are deeper issues that require the reviewer's honest reaction.

---

## One-Sentence Summary

**My self-critique predicts a real reviewer will be confused by jargon, skeptical of unproven claims, and blocked by missing visual evidence — so I will fix the circular link, add a screenshot, and add form proof before handing it to them.**
