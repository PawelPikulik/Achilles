# Achilles — AI Coffee Expert

A domain-specific AI product that answers coffee questions using structured bean data, remembers your taste preferences across sessions, and recommends beans that match both your query and your stated tastes.

**Built by:** Pawel Pikulik (with AI as a build partner — see [AI Transparency](#ai-transparency))  
**Track:** FlyRank General AI Fluency (FL-01 through FL-08)  
**Live portfolio:** https://pawelpikulik.netlify.app  
**Backend repo:** https://github.com/PawelPikulik/Artificiall  
**Deliverables index:** [DELIVERABLES.md](DELIVERABLES.md) | [RETROSPECTIVE.md](RETROSPECTIVE.md)

---

## What it does (and for whom)

Achilles is a conversational coffee recommendation system. A user asks a question like *"What Ethiopian coffee has berry notes?"* and Achilles:

1. Parses the query for keywords (origin, flavor notes, process, roast level)
2. Checks the user's stored preferences (e.g. *"I prefer natural processed coffees"*)
3. Scores every bean in the database against the query + preferences
4. Returns the top match with a confidence level and structured source data

**Who it's for:** A Head of AI or Product who needs to see that I can turn a raw domain API into a live, conversational product — from structured data to browser chat.

---

## Quick start

```bash
# 1. Clone and install
git clone https://github.com/PawelPikulik/Achilles.git
cd Achilles
pip install -r requirements.txt

# 2. Start the API
python achilles_api.py
# Or: uvicorn achilles_api:app --host 0.0.0.0 --port 8000

# 3. Open the chat UI
open achilles_chat.html        # macOS
start achilles_chat.html       # Windows
# Or serve via: python -m http.server 8080

# 4. Run tests (server must be running)
python test_achilles.py
```

No API keys required for the MVP — it runs on mock data. To swap to live CoffeeDB.pro data, see [Swap path to production](#swap-path-to-production).

---

## Architecture

```
Browser (achilles_chat.html)
    ↓  HTTP (CORS enabled)
FastAPI (achilles_api.py)
    ↓
┌─────────────────────────────────────────┐
│  Chat endpoint (/api/chat)              │
│  ├── Query parser (regex keywords)      │
│  ├── Preference memory (JSON file)      │
│  ├── Matching engine (rule-based score) │
│  └── Response formatter (structured)    │
├─────────────────────────────────────────┤
│  Memory endpoints (/api/memory)         │
│  ├── GET  — retrieve user prefs        │
│  └── POST — set a preference           │
├─────────────────────────────────────────┤
│  Data layer (fetch_coffee_data)        │
│  └── MOCK_BEANS → CoffeeDB.pro (swap)  │
└─────────────────────────────────────────┘
```

**Key design decisions:**
- **Mock data for MVP:** CoffeeDB.pro was unreachable during build (DNS failure). Mock data uses the exact CoffeeDB schema so swapping to live data is a one-line change.
- **Rule-based matching, not LLM:** The matching engine uses weighted keyword scores rather than an LLM. This is fast, deterministic, and debuggable — but it does not understand natural-language nuance. See [Limitations](#limitations).
- **JSON file memory:** Preferences persist across server restarts via `achilles_memory.json`. Not suitable for concurrent users — see swap path.
- **CORS `*` for dev:** The FastAPI middleware allows all origins so the HTML file can be opened directly. Production would restrict to the deployed domain.

---

## Usage examples

### API (curl)

```bash
# Health check
curl http://localhost:8000/health
# → {"status":"ok","service":"achilles","data_source":"mock"}

# Chat — origin + flavor query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What Ethiopian coffee has berry notes?","user_id":"u1"}'
# → {"reply":"Try Yirgacheffe G1 from Drop Coffee...","confidence":"high",
#     "sources":[{"id":"b001","name":"Yirgacheffe G1","score":91}],
#     "memory_used":false,"data_source":"mock"}

# Store a preference
curl -X POST http://localhost:8000/api/memory/u2 \
  -H "Content-Type: application/json" \
  -d '{"key":"preferred_process","value":"natural"}'

# Recall memory
curl http://localhost:8000/api/memory/u2
# → {"preferences":{"preferred_process":"natural"},"history":[]}
```

### Browser chat

Open `achilles_chat.html` in any browser. The UI:
- Shows a status indicator (live vs. mock data)
- Displays confidence level and source count for every reply
- Remembers your `user_id` across page reloads
- Handles empty input and API errors gracefully

---

## Eval results

| Test | Query | Expected | Result |
|------|-------|----------|--------|
| 1 | "What Ethiopian coffee has berry notes?" | High confidence, Yirgacheffe | ✅ Pass |
| 2 | "I prefer natural processed coffees" | Preference stored | ✅ Pass |
| 3 | "What do you recommend from Ethiopia?" (same user) | Memory recalled | ✅ Pass |
| 4 | "Something with chocolate and nutty flavors" | Brazil or Guatemala | ✅ Pass |
| 5 | "Do you have any teas?" | Low confidence, no-match fallback | ✅ Pass |
| 6 | "I want an anaerobic processed coffee" | Colombia Paraiso | ✅ Pass |
| 7 | "I want a washed coffee from Kenya" | Kenya AA Nyeri | ✅ Pass |
| 8 | "Recommend a dark roast" | Sumatra Mandheling | ✅ Pass |
| 9 | "Any good Colombian beans?" | Colombia El Paraiso | ✅ Pass |
| 10 | "Something fruity and light" | Sources returned | ✅ Pass |

**Score: 10/10 tests pass.**

Run: `python test_achilles.py` (server must be running on `localhost:8000`).

---

## Limitations (honest, not hidden)

1. **Rule-based matching, not LLM.** The query engine uses simple regex keyword matching. It does not understand synonyms, negation, or brewing-method recommendations. A production version would use an LLM to interpret the query and call the API for structured data grounding.

2. **Crude preference extraction.** Regex patterns (`i like X`, `i prefer X`) only catch simple statements. They don't handle compound preferences or temporal context.

3. **Preference key mismatch.** The extraction saves keys like `flavor_like`, but the matching engine looks for `preferred_origin` and `preferred_process`. The boost doesn't always apply. Fixing this is a mapping exercise, not architectural.

4. **No LLM for reply generation.** Replies are template strings. A real version would use an LLM to generate conversational, context-aware responses using structured data as grounding.

5. **Single-user JSON memory.** `achilles_memory.json` works for local testing but is not suitable for concurrent users or production. Swap to SQLite/Redis.

6. **Mock data only.** CoffeeDB.pro was unreachable during build. The mock data uses the exact CoffeeDB schema — swapping to live data is a one-line change documented in `achilles_notes.md`.

7. **CORS allows all origins.** Configured for local development. Production would restrict to the deployed domain.

---

## Swap path to production

| Component | Current | One-line change | Production |
|-----------|---------|-----------------|------------|
| Data source | `MOCK_BEANS` (8 items) | Replace `fetch_coffee_data()` with `requests.get("https://api.coffeedb.pro/v1/beans", headers={"Authorization": "Bearer TOKEN"})` | Live CoffeeDB data |
| Auth | None | Add `COFFEEDB_API_KEY` env var | Bearer token auth |
| Memory | `achilles_memory.json` | Swap `get_memory()` / `update_memory()` to SQLite or Redis calls | Persistent, multi-user |
| CORS | `allow_origins=["*"]` | Change to `allow_origins=["https://pawelpikulik.netlify.app"]` | Secure origin restriction |
| Reply generation | Template strings | Add LLM layer (Claude API / Groq) with structured output | Natural-language replies |

---

## AI Transparency

**I built this with Claude (Anthropic) as my coding partner.**

- **What AI did:** Generated the initial FastAPI scaffold, the regex-based matching engine, the CORS middleware config, the HTML chat UI structure, and the test suite template. Suggested the mock-data fallback when CoffeeDB.pro was unreachable.
- **What I did myself:** Designed the scoring weights (calibrated by running evals), debugged the preference key mismatch (Bug 2 in `build-log-achilles.md`), fixed the CORS issue (Bug 3), added file-lock flushing for the memory race condition (Bug 4), set the confidence thresholds, and wrote the honest gap documentation in `achilles_notes.md`.
- **What I checked:** Every test case was run manually and verified against expected output. The mock data schema was cross-referenced with CoffeeDB.pro documentation. The build log documents 6 bugs found and fixed.

> *Saying "I built this with Claude and here's what I checked myself" reads as credibility, not weakness.* — FlyRank AI Fluency Framework

---

## Files

| File | Purpose |
|------|---------|
| `achilles_api.py` | FastAPI backend: health, chat, memory, coffee data endpoints |
| `achilles_chat.html` | Browser chat UI with identity-kit styling |
| `test_achilles.py` | 10-query automated test suite |
| `achilles_notes.md` | Honest gap documentation: what works, what's mock, how to swap |
| `build-log-achilles.md` | 6 bugs found and fixed with before/after code |
| `requirements.txt` | `fastapi`, `uvicorn`, `pydantic`, `requests` |
| `DELIVERABLES.md` | Full index of every FL-01 through FL-08 deliverable |
| `RETROSPECTIVE.md` | 500–800 word retrospective for the capstone |

---

## License

MIT — built for educational portfolio use.
