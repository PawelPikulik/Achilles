# The Plan to Keep Building

**Week 8 — portfolio maintenance plan.** Purpose: turn this portfolio from a class artifact into a career platform by making the next case study cheap to ship while everything is still fresh.

---

## 1. Where the next case study goes

- **Repo:** this repo (`PawelPikulik/Achilles`) — a new file `case-study-<project>.md` in the repo root, next to [`case-study-achilles.md`](case-study-achilles.md).
- **Index:** one new row in [`DELIVERABLES.md`](DELIVERABLES.md) under a "Post-track case studies" section.
- **Live site:** one new section in `index.html` on the [`personal-site` branch](https://github.com/PawelPikulik/Achilles/tree/personal-site) — copy the existing `.featured` block, swap title/summary/links. Netlify auto-deploys on push.

## 2. Steps to add a case study (5 steps, ~1 hour)

1. **Three beats first.** Copy the skeleton from [`case-study-achilles.md`](case-study-achilles.md): *Problem → What I did → What came of it.* One paragraph per beat. Numbers where possible.
2. **Draft in the Claude Project.** The "Achilles" Claude Project is preserved (instructions in [`claude-project-setup.md`](claude-project-setup.md)) — it already knows my voice, the identity kit, and the stack. First prompt: *"Draft a case study for \<project\> using the three-beat shape. Facts: \<paste bullets\>."*
3. **Edit against the voice card.** Apply the Week 2 editing checklist: cut hedging, one metaphor max, every claim verifiable with a link or a test.
4. **Wire it in.** Add the `DELIVERABLES.md` row and the new site section; push both.
5. **Break-check it.** Re-run the Week 7 checklist from `HARDCENING.md` (personal-site branch): click every new link on phone + desktop, test in incognito.

## 3. The next piece of work (named)

**"Achilles v2 — LLM query layer."** Replace the regex keyword matcher in [`achilles_api.py`](achilles_api.py) with a Groq-powered structured-output call — the exact pattern already exists in `Artificiall/llm.py` (BE-07: retries, timeout, Pydantic schema validation). The rule-based engine stays as the grounding data source; the LLM handles natural-language queries like *"something fruity and bright for pour-over."*

It's a real case study because it has a genuine before/after: the same 10 eval queries in [`test_achilles.py`](test_achilles.py), regex vs. LLM, honestly compared — including whatever the LLM version gets *worse*.

- **Reminder evidence:** [GitHub issue #1](https://github.com/PawelPikulik/Achilles/issues/1) on this repo, attached to milestone "Next case study" **due 2026-10-10**.
- **Calendar nudge:** recurring reminder "Ship next portfolio case study," first occurrence 2026-10-10, repeats second Saturday of each month.

## 4. Build context preserved (cheap future updates)

| Asset | File | Why it makes the next case cheap |
|-------|------|----------------------------------|
| Claude Project instructions | [`claude-project-setup.md`](claude-project-setup.md) | Voice, goals, and role are already set — the next draft is a short conversation, not a rebuild |
| Identity kit | [`identity-kit.md`](identity-kit.md) | Fonts, palette, favicon — no redesign |
| Case study template | [`case-study-achilles.md`](case-study-achilles.md) | Three beats + voice card + editing checklist + before/after examples |
| Break-test checklist | `HARDCENING.md` (personal-site branch) | Re-run after every site change |
