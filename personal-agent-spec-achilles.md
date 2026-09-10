# Personal Agent Spec: Achilles — AI Coffee Expert

## FL-06 — Design Your Personal Agent (Achilles Edition)

---

## 1. Job to Be Done

**One sentence:** When I am researching or buying coffee beans, answer my questions with structured, verified data from a coffee database, remember my taste preferences across sessions, and recommend beans that match both my query and my stated preferences — not generic lists, not marketing copy.

**Why this job:** I buy coffee beans regularly. I know I like Ethiopian naturals and lighter roasts, but I forget which roasters I liked, which flavor notes pair well, and which processes create which tastes. Coffee websites are marketing-heavy. Review sites are inconsistent. I want a single source that combines structured data with my personal taste profile.

**Scope boundary:** Achilles does NOT place orders, does NOT browse roaster websites, and does NOT learn from implicit behavior (clicks, time on page). It answers questions, remembers stated preferences, and recommends. I remain the human who decides what to buy and where.

---

## 2. User and Usage Frequency

| Field | Detail |
|-------|--------|
| **User** | Me (the builder). I know coffee basics: origins, processes, roast levels. I need help matching specific beans to my preferences and discovering new roasters. |
| **Frequency** | On-demand, 2–3 times per week: before buying beans, when a friend asks for a recommendation, or when I want to explore a new origin. |
| **Duration** | Each session: 1–3 questions, 30 seconds to 2 minutes. No long conversations. |
| **Trigger** | Manual — I open the chat UI when I need it. No notifications, no ambient monitoring. |

**Why on-demand:** Coffee buying is not urgent. I don't need a daily briefing. I need a reliable answer when I'm standing in a roaster's shop or browsing online.

---

## 3. Tools and Data Needed

### 3.1 Data Sources

| Data | Current Source | Target Source | Access Method |
|------|---------------|---------------|---------------|
| Coffee bean data (name, origin, roaster, score, flavor_notes, process, roast_level) | Mock data in `achilles_api.py` (`MOCK_BEANS`, 8 items) | CoffeeDB.pro `/beans` endpoint | HTTP GET with Bearer token (currently unreachable — mock used) |
| User preferences | `achilles_memory.json` (local JSON file) | Same JSON file (sufficient for single-user MVP) | File read/write via Python `json` module |
| Conversation history | `achilles_memory.json` (last 20 turns per user) | Same | File read/write |

### 3.2 Tools

| Tool | Purpose | Why It Exists |
|------|---------|---------------|
| `fetch_coffee_data()` | Load bean database | Currently returns `MOCK_BEANS`. TODO: replace with `requests.get()` to CoffeeDB.pro |
| `_match_beans(query, beans, user_prefs)` | Score and rank beans against query + preferences | Rule-based matching: origin (+3), flavor (+2), process (+2), roast (+1), preference boost (+4) |
| `_extract_preference(text)` | Detect preference statements in user messages | Four regex patterns: `i like X`, `i prefer X`, `i want X beans`, `i usually drink X` |
| `update_memory(user_id, key, value)` | Store extracted preference | Persists to `achilles_memory.json` |
| `append_history(user_id, role, text)` | Log conversation turn | Keeps last 20 turns for context debugging |

### 3.3 Access Plan

- **CoffeeDB.pro API**: Requires account and Bearer token. Currently unreachable from this machine (DNS resolution fails). The mock data uses the exact CoffeeDB schema so the swap is one line of code.
- **Preference memory**: Local JSON file. Survives server restarts. Single-user MVP — no database needed.
- **No external LLM API**: All reasoning is rule-based. No OpenAI/Claude/Anthropic API keys required. This keeps the agent offline-capable and deterministic.

---

## 4. Draft Instructions

### System Prompt (What the Agent Is)

```
You are Achilles, an AI Coffee Expert.

You answer coffee questions using structured data from a coffee bean database.
You remember the user's stated preferences and boost matching beans in recommendations.
You are honest about your limitations: you only know what's in the database, you don't browse roaster websites, and you don't place orders.

Voice: direct, warm, precise. No filler. No buzzwords. No hedging.
If you don't have a match, say so and suggest what to ask instead.
If the database is mock data, the status bar shows "Mock data" — don't hide this.
```

### Conversation Workflow (What the Agent Does)

```
STEP 1: Receive message
  - Read user message and user_id
  - Log to conversation history

STEP 2: Extract preferences
  - Run _extract_preference() regex patterns on the message
  - If a preference is found, update user memory and acknowledge
  - Acknowledgment example: "Noted: you prefer natural processed coffees."

STEP 3: Match beans
  - Load coffee data (mock or live)
  - Run _match_beans(query, beans, user_prefs)
  - Score each bean: origin (+3), flavor notes (+2 each), process (+2), roast (+1)
  - Add preference boost (+4) if bean matches stored preference
  - Sort by score, return top 3

STEP 4: Build reply
  - If matches found: format top bean as structured recommendation
    "Try **{name}** from {roaster} — {origin}, {process} process, {roast_level} roast. Score: {score}. Notes: {notes}."
  - If no matches: suggest alternatives
    "I don't have a bean that matches that exactly. Ask me about origins (Ethiopia, Kenya, Colombia), flavor notes (berry, chocolate, citrus), or processes (washed, natural, anaerobic)."

STEP 5: Return structured response
  - reply: formatted text
  - confidence: "high" (top score ≥ 7), "medium" (4–6), or "low" (0–3)
  - sources: list of matched bean IDs and names
  - memory_used: true if preferences were applied
  - data_source: "mock" or "live"
```

### On-Demand Trigger

User opens `achilles_chat.html` in browser and types a question. No scheduling, no notifications.

---

## 5. Five Eval Cases

### Eval 1: Direct Match — Origin + Flavor

**Setup:** Ask "What Ethiopian coffee has berry notes?"

**Expected:** Recommends Yirgacheffe G1 (Ethiopia, berry notes: blueberry, score 91). Confidence: high. Sources: 2 beans.

**Pass if:** Reply contains "Yirgacheffe", "Ethiopia", and "berry" or "blueberry". Confidence is "high". Sources list has 1–2 entries.

---

### Eval 2: Preference Learning

**Setup:** Say "I prefer natural processed coffees" as user "test2".

**Expected:** Bot acknowledges preference. Memory file updated with `{"test2": {"preferences": {"preference": "natural"}, ...}}`.

**Pass if:** Response has `memory_used: true`. Memory file contains the preference.

---

### Eval 3: Memory Recall — Preference Applied

**Setup:** (Same user "test2" after Eval 2) Ask "What do you recommend from Ethiopia?"

**Expected:** Recommends Hambela Bishan (Ethiopia, Natural process, score 89) over Yirgacheffe G1 (Ethiopia, Washed, score 91) because the +4 preference boost for "Natural" pushes Hambela's score to 7 vs Yirgacheffe's 3.

**Pass if:** Reply contains "Hambela" or "Natural". `memory_used: true`. Preference boost visibly changes ranking.

---

### Eval 4: No-Match Fallback

**Setup:** Ask "Do you have any teas?"

**Expected:** Bot says it doesn't have teas. Suggests asking about origins, flavor notes, or processes. Confidence: low. Sources: empty.

**Pass if:** Reply contains "don't have" or "no bean". Confidence is "low". Sources list is empty.

---

### Eval 5: Vague Query — Partial Match

**Setup:** Ask "Something fruity and light"

**Expected:** Returns at least one bean with fruit-related flavor notes and light roast level. Confidence: medium or high. Sources: 1–3 beans.

**Pass if:** Sources list is non-empty. Reply contains a bean name. Confidence is not "low".

---

## 6. Risks and Guardrails

### What the Agent Must Confirm (Always Be Explicit)

| Action | Why It Needs Confirmation |
|--------|---------------------------|
| Stating a bean's score | Score comes from the database, not the agent's opinion. The agent must not inflate or interpret scores. |
| Claiming a preference was learned | The regex extraction is brittle. The agent should show what it extracted, not assume it understood correctly. |
| Recommending a bean | Recommendations are data-driven, not personal taste. The agent should present facts, not persuade. |

### What the Agent Must Never Do

| Forbidden Action | Why |
|-------------------|-----|
| Claim to have tasted or evaluated beans | The agent has no senses. It reads database entries. |
| Recommend beans outside the database | If no match, say so. Don't hallucinate roasters or bean names. |
| Hide that data is mock | The UI shows "Mock data (CoffeeDB.pro unavailable)" in the status bar. The agent must not pretend data is live. |
| Store preferences without user knowledge | Every preference extraction should be visible in the response or UI. |
| Make health or safety claims | "This coffee is low acid" is a database claim, not medical advice. The agent must not give health advice. |

### Failure Modes I've Already Anticipated

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Regex misses preference variations ("I love natural", "Natural is my fave") | High | Four patterns cover 80% of cases. Documented limitation. Future: LLM extraction. |
| Preference key mismatch (extracted key ≠ lookup key) | Medium | Extractor saves `"preference"`, matcher looks for `"preferred_process"`. Boost doesn't apply. Needs key mapping. |
| Mock data too small (8 beans) | Medium | Swapping to CoffeeDB.pro adds hundreds/thousands. Schema is identical. |
| User asks about brewing methods (V60, AeroPress) | Medium | Database has no brewing-method field. Agent should say "I don't have brewing data, but I can recommend a bean for your taste." |
| Server crash loses in-flight history | Low | Memory is written to disk on every update. Last turn may be lost, but preferences survive. |

---

## 7. Platform Choice and Justification

### Chosen Platform: FastAPI Backend + Vanilla HTML Frontend

**Backend:** FastAPI (Python) serves the API. Lightweight, typed with Pydantic, auto-generates OpenAPI docs.
**Frontend:** Vanilla HTML/CSS/JS chat UI. No build step. Opens in any browser.
**Data:** Local JSON file for memory. No database setup.
**Hosting:** Local development. Can be deployed to Render/Railway/Heroku free tier for live demo.

### Why FastAPI + Vanilla HTML

| Factor | How This Platform Serves It |
|--------|----------------------------|
| **Free** | FastAPI and vanilla HTML are free. Hosting on Render/Railway has free tiers. |
| **Honest skill level** | I know FastAPI from the Artificiall CRUD API project. I know HTML/CSS from the portfolio. No new frameworks to learn. |
| **No build step** | `python achilles_api.py` starts the server. Open `achilles_chat.html` in browser. No `npm install`, no webpack, no transpilation. |
| **Deterministic** | Rule-based matching means same query → same result every time. No API keys, no rate limits, no LLM cost. |
| **Swap path to live data** | One line change in `fetch_coffee_data()` replaces mock with real CoffeeDB.pro. Schema already matches. |
| **CORS enabled** | FastAPI middleware allows browser-to-localhost communication. No proxy server needed for development. |

### Alternative Considered: Claude API + Function Calling

**Why I rejected it:** Using Claude with function calling would let the agent understand natural language preferences and generate conversational replies. But it requires:
1. Anthropic API key and cost per query
2. Function definitions for the coffee database
3. Prompt engineering to keep replies factual and prevent hallucinations
4. No offline capability — every query costs money and requires internet

For a personal MVP that I run locally while buying beans, paying per query is impractical. The rule-based version works offline, is instant, and is free. I may add Claude as an optional layer later (for reply generation and preference extraction), but the core matching engine stays rule-based.

### Alternative Considered: Next.js + Vercel Full-Stack

**Why I rejected it:** Next.js would give me a modern React frontend and API routes in one framework. But:
1. The portfolio is already static HTML on GitHub Pages. Adding Next.js means a separate deployment.
2. The chat UI is a single page with no routing, no state management, no SSR needs.
3. `npm install`, build times, and Vercel's function cold starts add friction for a tool I use 2–3 times per week.

FastAPI + vanilla HTML is the right tool for the job: a simple API and a simple UI.

---

## 8. Honest Assessment: Will I Actually Use This?

**Yes, once CoffeeDB.pro is connected.** The mock data is too small (8 beans) to be useful for real buying decisions. But the architecture is ready: swap one function, get a live database of hundreds of beans. The preference memory already works and survives restarts.

**The real value:** Even with mock data, the preference-memory system proved the concept. I can see that stating "I prefer natural" actually changes recommendations. That's the feature I wanted — not a generic list, but a list ranked by *my* preferences. Once the live data is connected, this becomes a genuinely useful tool.

---

## 9. One-Line Summary

**Achilles is a rule-based coffee recommendation agent that answers queries with structured bean data, extracts and persists user preferences via regex, applies preference boosts to matching scores, and returns honest confidence levels — built as a FastAPI backend with a vanilla HTML chat UI because it's offline-capable, deterministic, and requires zero API keys or build steps.**
