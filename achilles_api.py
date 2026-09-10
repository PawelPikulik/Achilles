"""Achilles AI Coffee Expert — MVP Backend

FastAPI backend with:
- /health        health check
- /api/chat      POST {message, user_id?} → {reply, confidence, sources, memory_used}
- /api/memory    GET/POST user preference memory
- /api/coffee    GET coffee data (mock, CoffeeDB-compatible schema)

Mock data simulates CoffeeDB.pro /beans schema:
  name, origin, roaster, score, flavor_notes, process, roast_level

Swap mock_db for real CoffeeDB requests by replacing fetch_coffee_data().
"""

import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("achilles")

# ---------------------------------------------------------------------------
#  Mock CoffeeDB data (beans schema)
# ---------------------------------------------------------------------------

MOCK_BEANS = [
    {
        "id": "b001",
        "name": "Yirgacheffe G1",
        "origin": "Ethiopia",
        "roaster": "Drop Coffee",
        "score": 91,
        "flavor_notes": ["bergamot", "jasmine", "blueberry", "citrus"],
        "process": "Washed",
        "roast_level": "Light",
    },
    {
        "id": "b002",
        "name": "Hambela Bishan",
        "origin": "Ethiopia",
        "roaster": "Tim Wendelboe",
        "score": 89,
        "flavor_notes": ["strawberry", "peach", "chocolate", "floral"],
        "process": "Natural",
        "roast_level": "Light-Medium",
    },
    {
        "id": "b003",
        "name": "Kenya AA Nyeri",
        "origin": "Kenya",
        "roaster": "Intelligentsia",
        "score": 90,
        "flavor_notes": ["blackcurrant", "tomato", "lime", "caramel"],
        "process": "Washed",
        "roast_level": "Medium",
    },
    {
        "id": "b004",
        "name": "Guatemala Huehuetenango",
        "origin": "Guatemala",
        "roaster": "Blue Bottle",
        "score": 87,
        "flavor_notes": ["cocoa", "nut", "apple", "brown sugar"],
        "process": "Washed",
        "roast_level": "Medium",
    },
    {
        "id": "b005",
        "name": "Colombia El Paraiso",
        "origin": "Colombia",
        "roaster": "Square Mile",
        "score": 88,
        "flavor_notes": ["passion fruit", "lychee", "honey", "vanilla"],
        "process": "Anaerobic",
        "roast_level": "Light",
    },
    {
        "id": "b006",
        "name": "Brazil Cerrado",
        "origin": "Brazil",
        "roaster": "Stumptown",
        "score": 84,
        "flavor_notes": ["chocolate", "nut", "caramel", "low acidity"],
        "process": "Natural",
        "roast_level": "Medium-Dark",
    },
    {
        "id": "b007",
        "name": "Sumatra Mandheling",
        "origin": "Indonesia",
        "roaster": "Counter Culture",
        "score": 86,
        "flavor_notes": ["earth", "spice", "cedar", "dark chocolate"],
        "process": "Wet-Hulled",
        "roast_level": "Dark",
    },
    {
        "id": "b008",
        "name": "Panama Geisha Esmeralda",
        "origin": "Panama",
        "roaster": "Ninety Plus",
        "score": 94,
        "flavor_notes": ["jasmine", "mango", "bergamot", "silky"],
        "process": "Washed",
        "roast_level": "Light",
    },
]

# ---------------------------------------------------------------------------
#  In-memory user preferences (survives process lifetime; JSON persists on disk)
# ---------------------------------------------------------------------------

MEMORY_FILE = Path(__file__).with_name("achilles_memory.json")
_user_memory: dict[str, dict] = {}


def _load_memory():
    global _user_memory
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                _user_memory = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load memory: {e}")
            _user_memory = {}
    else:
        _user_memory = {}


def _save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_memory, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Could not save memory: {e}")


def get_memory(user_id: str) -> dict:
    return _user_memory.get(user_id, {"preferences": {}, "history": []})


def update_memory(user_id: str, key: str, value):
    mem = get_memory(user_id)
    mem["preferences"][key] = value
    _user_memory[user_id] = mem
    _save_memory()


def append_history(user_id: str, role: str, text: str):
    mem = get_memory(user_id)
    mem["history"].append({"role": role, "text": text, "ts": datetime.utcnow().isoformat()})
    # Keep last 20 turns
    mem["history"] = mem["history"][-20:]
    _user_memory[user_id] = mem
    _save_memory()


# ---------------------------------------------------------------------------
#  Coffee query engine (mock; replace with real CoffeeDB HTTP client)
# ---------------------------------------------------------------------------

def fetch_coffee_data() -> list[dict]:
    """Return coffee bean data.

    TODO: Replace with real CoffeeDB.pro request:
        response = requests.get(COFFEEDB_URL + "/beans", headers=auth_headers, timeout=10)
        return response.json()
    """
    return MOCK_BEANS


def _match_beans(query: str, beans: list[dict], user_prefs: dict) -> list[dict]:
    """Simple rule-based matching: origin, flavor notes, process, roast."""
    q = query.lower()
    scores = []
    for b in beans:
        score = 0
        # Origin match
        if b["origin"].lower() in q:
            score += 3
        # Flavor note match
        for note in b["flavor_notes"]:
            if note.lower() in q:
                score += 2
        # Process match
        if b["process"].lower() in q:
            score += 2
        # Roast level match
        if b["roast_level"].lower() in q:
            score += 1
        # Preference boost
        preferred_origin = user_prefs.get("preferred_origin", "")
        if preferred_origin and b["origin"].lower() == preferred_origin.lower():
            score += 4
        preferred_process = user_prefs.get("preferred_process", "")
        if preferred_process and b["process"].lower() == preferred_process.lower():
            score += 3
        if score > 0:
            scores.append((score, b))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [b for _, b in scores[:3]]


def _extract_preference(text: str) -> Optional[tuple[str, str]]:
    """Crude preference extraction from user message."""
    patterns = [
        (r"i\s+like\s+(\w+)", "flavor_like"),
        (r"i\s+prefer\s+(\w+)", "preference"),
        (r"i\s+want\s+([\w\s]+)\s+beans", "bean_type"),
        (r"i\s+usually\s+drink\s+(\w+)", "usual_drink"),
    ]
    for pat, key in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return key, m.group(1).strip().lower()
    return None


# ---------------------------------------------------------------------------
#  FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(title="Achilles AI Coffee Expert", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    reply: str
    confidence: str  # "high" | "medium" | "low"
    sources: list[dict]
    memory_used: bool
    data_source: str  # "live" | "mock"


class MemoryUpdate(BaseModel):
    key: str
    value: str


@app.on_event("startup")
def startup():
    _load_memory()
    logger.info("Achilles started. Memory loaded: %d users.", len(_user_memory))


@app.get("/health")
def health():
    return {"status": "ok", "service": "achilles", "data_source": "mock"}


@app.get("/api/coffee")
def get_coffee():
    beans = fetch_coffee_data()
    return {"count": len(beans), "beans": beans}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    start = time.time()
    user_id = req.user_id or "default"
    msg = req.message.strip()
    append_history(user_id, "user", msg)

    mem = get_memory(user_id)
    prefs = mem.get("preferences", {})

    # Extract any new preference
    pref = _extract_preference(msg)
    if pref:
        update_memory(user_id, pref[0], pref[1])
        prefs = get_memory(user_id)["preferences"]

    beans = fetch_coffee_data()
    matches = _match_beans(msg, beans, prefs)

    # Build reply
    if matches:
        top = matches[0]
        reply = (
            f"Try **{top['name']}** from {top['roaster']} — {top['origin']}, "
            f"{top['process']} process, {top['roast_level']} roast. "
            f"Score: {top['score']}. Notes: {', '.join(top['flavor_notes'])}."
        )
        confidence = "high" if len(matches) >= 2 and matches[0]["score"] >= 88 else "medium"
        sources = [{"id": b["id"], "name": b["name"], "score": b["score"]} for b in matches]
    else:
        reply = (
            "I don't have a bean that matches that exactly. "
            "Ask me about origins (Ethiopia, Kenya, Colombia), flavor notes (berry, chocolate, citrus), "
            "or processes (washed, natural, anaerobic)."
        )
        confidence = "low"
        sources = []

    append_history(user_id, "achilles", reply)
    elapsed = time.time() - start
    logger.info("Chat | user=%s | confidence=%s | sources=%d | %.3fs", user_id, confidence, len(sources), elapsed)

    return ChatResponse(
        reply=reply,
        confidence=confidence,
        sources=sources,
        memory_used=bool(prefs),
        data_source="mock",
    )


@app.get("/api/memory/{user_id}")
def get_user_memory(user_id: str):
    return get_memory(user_id)


@app.post("/api/memory/{user_id}")
def set_user_memory(user_id: str, update: MemoryUpdate):
    update_memory(user_id, update.key, update.value)
    return get_memory(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
