# Retrospective — FlyRank General AI Fluency

**Written for the person I was in Week 1:** someone who could write Python but had never shipped a full-stack product from API to browser, never tested a scraper against a real site, never connected an LLM to a working endpoint, and never published a portfolio that a stranger could actually use.

---

## What I set out to do

Week 1, I claimed one thing: *"I can ship domain-specific AI products from API to UI."* The claim was aspirational. I had written APIs before, but never one with auth, never one that talked to an LLM, never one that survived a broken dependency. I had never built a chat UI that actually sent messages to a backend and showed structured results. I had never written a README a stranger could follow.

The project I chose was Achilles — an AI Coffee Expert. I picked it because coffee is a domain I care about, and because the data source (CoffeeDB.pro) looked real enough to force me to think about schema compatibility, auth, and graceful failure.

## What changed

**Everything I thought would be hard was easy; everything I thought would be easy broke.**

I expected the matching engine to take days. It took an afternoon — regex keyword scoring is crude but fast to build and debug. I expected the UI to be hard. It took two hours — vanilla HTML/CSS/JS with FastAPI's CORS middleware. What I did not expect: CoffeeDB.pro would not resolve. DNS failure on Day 1. I spent more time deciding whether to use mock data than I spent building the entire matching engine.

That decision — mock data with an honest gap documented — became the most important one. It taught me that shipping a working half is better than defending a broken whole. The mock data uses the exact CoffeeDB schema. One line swaps it to live. Every API response says `"data_source": "mock"`. The UI shows a status bar. The README names the limitation in bullet 6. I learned that credibility comes from honesty, not from pretending everything works.

The second thing that changed: I stopped treating AI as a code generator and started treating it as a thinking partner. In Week 1, I would paste a prompt, copy the output, and hope it worked. By Week 5, I was running evals before accepting any change, calibrating scoring weights by watching which beans ranked first, and writing build logs that documented *why* a bug mattered and *how* I fixed it. The AI wrote the scaffold; I decided the thresholds.

The third thing: I learned to break my own work before anyone else could. Week 7, I tested the contact form with empty input, garbage data, double-clicks, and no JavaScript. I found that the Formspree endpoint was dead (404) — a real break, not a hypothetical one. I fixed it by migrating to Netlify Forms, which works with or without JS. That habit — trying to break it, triaging honestly, fixing the fix-nows and naming the known limitations — is the most professional thing I learned.

## What I'd build next

1. **Connect the live data.** CoffeeDB.pro or a real coffee API. The schema is ready; the auth pattern is designed; it's one function swap.
2. **Add an LLM layer.** The rule-based matching is fast and debuggable, but it doesn't understand "something fruity and bright for pour-over." I'd use Groq (already integrated in my Artificiall backend) with structured JSON output, using the matching engine's top-3 results as grounding data.
3. **Persistent memory.** SQLite instead of JSON file. Multi-user support. That's a real deployment, not a demo.

## Three transferable things

**1. Eval-driven iteration.** I don't accept code until it passes tests I wrote myself. This applies to any project: write the test, run it, adjust, repeat. It's faster than hoping.

**2. Honest gap documentation.** Naming what doesn't work — and why — is more credible than hiding it. I used this in the Achilles README, the Artificiall scraper, and the portfolio hardening report. Employers and reviewers trust someone who knows where their own cracks are.

**3. AI as partner, not replacement.** I don't ask AI to ship for me. I ask it to scaffold, suggest, and speed up. The decisions — scoring weights, confidence thresholds, whether to use mock data, how to fix the CORS bug — were mine. The checking was mine. The story I tell about it is mine.

---

**This track was 8 weeks. The product is a repo, a live site, and a way of working I will keep.**
