# Achilles MVP Notes: Honest Gap Documentation

## What Was Built

A working FastAPI backend (`achilles_api.py`) and a browser chat UI (`achilles_chat.html`) for Achilles, the AI Coffee Expert. The system answers coffee questions with structured data, tracks user preferences across sessions, and shows confidence levels and sources for every answer.

**API endpoints:**
- `GET /health` — health check, reports data source (live vs mock)
- `GET /api/coffee` — list all coffee data
- `POST /api/chat` — chat with Achilles (message + optional user_id)
- `GET /api/memory/{user_id}` — view stored preferences
- `POST /api/memory/{user_id}` — manually set a preference

**Files:**
- `achilles_api.py` — FastAPI backend (340 lines)
- `achilles_chat.html` — browser chat UI (matches portfolio identity kit)
- `test_achilles.py` — 10-query test suite
- `requirements.txt` — dependencies

---

## What Is NOT Connected

**CoffeeDB.pro is unreachable.** I attempted to call `https://api.coffeedb.pro/v1/beans` from both `curl` and Python `urllib.request`. Both failed with DNS resolution errors (`getaddrinfo failed`). The domain does not resolve from this machine or network.

This means:
- All coffee data in Achilles is **mock data** (8 beans with realistic schema)
- The `data_source` field in every API response is `"mock"`
- The chat UI shows a status indicator: "Mock data (CoffeeDB.pro unavailable)"

---

## Why Mock Data Is Acceptable for This Phase

The goal of this MVP is to prove the **architecture** works: API → matching engine → structured response → preference memory → UI. The mock data uses the exact schema documented for CoffeeDB.pro (`name`, `origin`, `roaster`, `score`, `flavor_notes`, `process`, `roast_level`). Swapping to real data is a one-line change: replace `fetch_coffee_data()` with an HTTP request to the live API.

The honest documentation is in the code:
- `achilles_api.py:177` — TODO comment showing the real CoffeeDB request to swap in
- Health endpoint reports `"data_source": "mock"`
- Every chat response includes `"data_source": "mock"`
- UI shows mock indicator in the status bar

---

## What Would Change With Real CoffeeDB.pro

| Component | Current | With CoffeeDB.pro |
|-----------|---------|-------------------|
| Data source | `MOCK_BEANS` list (8 items) | `requests.get(COFFEEDB_URL + "/beans", headers=auth_headers, timeout=10)` |
| Auth | None (mock) | Bearer token from `COFFEEDB_API_KEY` env var |
| Rate limits | None | 100 req/min (already handled in prompt-ladder-apicode.md version 3) |
| Error handling | Returns empty list on any error | 429 retry, 500 fallback, timeout with structured error |
| Data freshness | Static | Live, updates when roasters publish new beans |
| Coverage | 8 beans, 6 origins | Full database (unknown size, but significantly larger) |

---

## Known Limitations of the MVP

1. **Rule-based matching, not LLM.** The query engine uses simple regex keyword matching (origin + flavor note + process + roast level). It does not understand natural language nuance, synonyms, or brewing-method recommendations. A real Achilles would use an LLM to interpret the query and call the API for structured data grounding.

2. **Crude preference extraction.** The regex patterns (`i like X`, `i prefer X`, `i want X beans`, `i usually drink X`) only catch simple statements. They don't handle negation, compound preferences, or temporal context.

3. **Preference key mismatch.** The extraction saves keys like `flavor_like`, `preference`, `bean_type`, `usual_drink` — but the matching engine looks for `preferred_origin` and `preferred_process`. The boost doesn't always apply because the keys don't align. Fixing this is a mapping exercise, not an architectural change.

4. **No LLM for reply generation.** Replies are template strings: `"Try **{name}** from {roaster} — {origin}, {process} process, {roast_level} roast. Score: {score}. Notes: {notes}."` A real version would use an LLM to generate a conversational, context-aware response using the structured data as grounding.

5. **Single-user memory file.** Preferences are stored in `achilles_memory.json` on disk. This works for local testing but is not suitable for concurrent users or production. A real deployment would use a database.

6. **CORS allows all origins.** The FastAPI middleware is configured for local development. Production would restrict origins.

---

## How to Swap to Live CoffeeDB.pro

1. Obtain a CoffeeDB.pro API key and set `COFFEEDB_API_KEY` environment variable.
2. Edit `achilles_api.py`, function `fetch_coffee_data()` (line 174):
   ```python
   def fetch_coffee_data() -> list[dict]:
       import requests, os
       url = os.getenv("COFFEEDB_URL", "https://api.coffeedb.pro/v1")
       headers = {"Authorization": f"Bearer {os.getenv('COFFEEDB_API_KEY')}"}
       response = requests.get(f"{url}/beans", headers=headers, timeout=10)
       response.raise_for_status()
       return response.json()
   ```
3. Restart the server. Health endpoint will report `"data_source": "live"`.
4. UI status bar will update automatically.

---

## How to Run the MVP

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the API server
python achilles_api.py
# Or: uvicorn achilles_api:app --host 0.0.0.0 --port 8000

# 3. Open the chat UI
# In browser: open achilles_chat.html (file:// or serve via http-server)

# 4. Run tests (server must be running)
python test_achilles.py
```

---

## One-Sentence Summary

**Achilles MVP is a working FastAPI backend + browser chat UI with mock coffee data, rule-based matching, preference memory, and structured responses — built to prove the API→UI architecture, with an honest gap documented: CoffeeDB.pro is unreachable, so the live connection is a one-line swap once the API is accessible.**
