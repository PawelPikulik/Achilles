# Prompt Ladder: CoffeeDB API Integration

## Baseline: The Weak Prompt

**Prompt:**
```
Write Python code to connect to the CoffeeDB API.
```

**Output:**
```python
import requests

def get_coffee_data():
    response = requests.get("https://api.coffeedb.pro")
    return response.json()

if __name__ == "__main__":
    print(get_coffee_data())
```

**Embarrassment check:** This is genuinely weak. No error handling, no authentication, no specific endpoint, no context about what CoffeeDB returns, no structure. It assumes the API is public, returns JSON, and never fails. It wouldn't survive a code review or a production deploy.

---

## Version 1: Clearer Goal

**What changed in the prompt:** Added a specific endpoint (/beans) and a specific data structure (name, origin, roaster, score, flavor_notes). Changed "connect to" to "fetch and parse."

**Prompt:**
```
Write Python code to fetch coffee bean data from the CoffeeDB API /beans endpoint, parse the response, and return structured JSON with fields: name, origin, roaster, score, and flavor_notes.
```

**Output:**
```python
import requests

def fetch_beans():
    url = "https://api.coffeedb.pro/beans"
    response = requests.get(url)
    data = response.json()
    
    beans = []
    for item in data:
        beans.append({
            "name": item.get("name"),
            "origin": item.get("origin"),
            "roaster": item.get("roaster"),
            "score": item.get("score"),
            "flavor_notes": item.get("flavor_notes")
        })
    return beans

print(fetch_beans())
```

**What improved in the output:** The endpoint is specific. The field mapping is explicit. The function has a real name. It's no longer just "get_coffee_data" — it's "fetch_beans" with a known schema. A reader can see what the API returns without guessing.

**What still failed:** Still no authentication (CoffeeDB requires a Bearer token). Still no error handling (what if the API is down? What if the response is malformed?). Still no production context (env vars, timeouts, logging). The code would crash in production on the first 500 error.

**What to try next:** The biggest gap is that the model doesn't know CoffeeDB requires auth or has error states. I need to add the real API context.

---

## Version 2: Defined Audience

**What changed in the prompt:** Added audience: "for a backend developer who will review this in a production Flask app."

**Prompt:**
```
Write Python code for a backend developer who will review this in a production Flask application. Fetch coffee bean data from the CoffeeDB API /beans endpoint, parse the response, and return structured JSON with fields: name, origin, roaster, score, and flavor_notes.
```

**Output:**
```python
from flask import Flask, jsonify
from abc import ABC, abstractmethod
import requests

app = Flask(__name__)

class CoffeeRepository(ABC):
    @abstractmethod
    def fetch_beans(self):
        pass

class CoffeeDBRepository(CoffeeRepository):
    def __init__(self, base_url: str = "https://api.coffeedb.pro"):
        self.base_url = base_url
    
    def fetch_beans(self):
        response = requests.get(f"{self.base_url}/beans")
        return response.json()

class CoffeeService:
    def __init__(self, repository: CoffeeRepository):
        self.repository = repository
    
    def get_all_beans(self):
        data = self.repository.fetch_beans()
        return [self._map_bean(item) for item in data]
    
    def _map_bean(self, item):
        return {
            "name": item.get("name"),
            "origin": item.get("origin"),
            "roaster": item.get("roaster"),
            "score": item.get("score"),
            "flavor_notes": item.get("flavor_notes")
        }

service = CoffeeService(CoffeeDBRepository())

@app.route("/beans")
def get_beans():
    return jsonify(service.get_all_beans())

if __name__ == "__main__":
    app.run(debug=True)
```

**What improved in the output:** It added Flask scaffolding. It abstracted the repository pattern. It separated service logic from route logic. It's structured like something a backend developer might recognize.

**What still failed:** This is the "didn't help" moment. The audience constraint made the model over-engineer. It added abstract classes, dependency injection, and service layers that solve a problem I don't have. The code is 3x longer but not 3x better. It still has no auth, no error handling, and no production context. The abstractions are generic boilerplate, not specific to CoffeeDB. A backend developer would probably refactor this back to a simpler function on first review.

**What to try next:** The audience layer was too abstract. I need to ground the model in the actual CoffeeDB API constraints — auth, rate limits, error codes — rather than asking for generic "production-ready patterns."

---

## Version 3: Real Context

**What changed in the prompt:** Added real CoffeeDB API context: base URL, Bearer token auth, rate limit (100/min), specific endpoint fields, and specific error codes to handle (429, 500, timeout). Removed the audience constraint.

**Prompt:**
```
Write Python code for a Flask app. The CoffeeDB API base URL is https://api.coffeedb.pro/v1. Authentication is via Bearer token in the Authorization header. Rate limit: 100 requests/minute. The /beans endpoint returns JSON with fields: name, origin, roaster, score, flavor_notes. Handle HTTP 429, 500, and timeout errors explicitly.
```

**Output:**
```python
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

COFFEEDB_BASE_URL = "https://api.coffeedb.pro/v1"
COFFEEDB_API_KEY = os.getenv("COFFEEDB_API_KEY")

def fetch_beans():
    headers = {"Authorization": f"Bearer {COFFEEDB_API_KEY}"}
    
    try:
        response = requests.get(
            f"{COFFEEDB_BASE_URL}/beans",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 429:
            return {"error": "Rate limit exceeded. Retry after 60 seconds."}
        elif response.status_code == 500:
            return {"error": "CoffeeDB server error. Please retry."}
        elif response.status_code != 200:
            return {"error": f"Unexpected status: {response.status_code}"}
        
        data = response.json()
        return [
            {
                "name": item.get("name"),
                "origin": item.get("origin"),
                "roaster": item.get("roaster"),
                "score": item.get("score"),
                "flavor_notes": item.get("flavor_notes")
            }
            for item in data
        ]
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please retry."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@app.route("/beans")
def get_beans():
    result = fetch_beans()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
```

**What improved in the output:** Massive improvement. Auth is handled via env var. Rate limit (429) and server errors (500) are caught. Timeout is handled. The endpoint and fields are specific. The code is grounded in reality. It would actually work (or fail gracefully) in production.

**What still failed:** Error handling is passive — it returns error dicts but doesn't log them, doesn't retry, and doesn't surface the right HTTP status to the client. The response parsing has no type safety. There's no docstring explaining the contract. The code works but isn't maintainable.

**What to try next:** I need structure — docstrings, type hints, a clear output format, and better error handling patterns. I want the code to be readable and auditable.

---

## Version 4: Specified Output Format

**What changed in the prompt:** Added explicit output format requirements: docstring, auth check, structured error logging, Pydantic model, main block, inline comments.

**Prompt:**
```
Write Python code for a Flask app. The CoffeeDB API base URL is https://api.coffeedb.pro/v1. Authentication is via Bearer token in the Authorization header. Rate limit: 100 requests/minute. The /beans endpoint returns JSON with fields: name, origin, roaster, score, flavor_notes. Handle HTTP 429, 500, and timeout errors explicitly.

Output format requirements:
1. Docstring explaining the function's purpose, parameters, and return type.
2. Auth header setup with environment variable validation.
3. Explicit error handling for 429, 500, and timeout with structured logging.
4. JSON response parsing using a Pydantic model for type safety.
5. A main block for local testing.
6. Inline comments explaining each architectural decision.
```

**Output:**
```python
import os
import logging
from typing import List, Union
import requests
from flask import Flask, jsonify
from pydantic import BaseModel, Field

# Configure logging for production visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Configuration ---
# Load API key from environment to avoid hardcoding secrets
COFFEEDB_BASE_URL = "https://api.coffeedb.pro/v1"
COFFEEDB_API_KEY = os.getenv("COFFEEDB_API_KEY")
if not COFFEEDB_API_KEY:
    raise ValueError("COFFEEDB_API_KEY environment variable is required")

# --- Pydantic Model for Type Safety ---
# Validates response structure at runtime; fails fast if API changes schema
class CoffeeBean(BaseModel):
    """Represents a single coffee bean from CoffeeDB.pro."""
    name: str
    origin: str
    roaster: str
    score: float = Field(..., ge=0, le=100)
    flavor_notes: List[str]

# --- Core Function ---
def fetch_beans() -> Union[List[CoffeeBean], dict]:
    """
    Fetch coffee beans from CoffeeDB.pro API with error handling.
    
    Returns:
        List[CoffeeBean]: Parsed and validated coffee beans on success.
        dict: Error information with user-friendly message on failure.
    """
    headers = {"Authorization": f"Bearer {COFFEEDB_API_KEY}"}
    
    try:
        # Send request with 10s timeout to avoid hanging connections
        response = requests.get(
            f"{COFFEEDB_BASE_URL}/beans",
            headers=headers,
            timeout=10
        )
        
        # Handle rate limit (429) — client should back off
        if response.status_code == 429:
            logger.warning("Rate limit hit (429)")
            return {"error": "Rate limit exceeded", "retry_after": 60}
        
        # Handle server error (500) — transient, retryable
        if response.status_code == 500:
            logger.error("CoffeeDB server error (500)")
            return {"error": "CoffeeDB server error", "retry": True}
        
        # Handle unexpected status codes
        if response.status_code != 200:
            logger.error(f"Unexpected status: {response.status_code}")
            return {"error": f"Unexpected status: {response.status_code}"}
        
        # Parse and validate response using Pydantic
        data = response.json()
        beans = [CoffeeBean(**item) for item in data]
        logger.info(f"Fetched {len(beans)} beans successfully")
        return beans
        
    except requests.exceptions.Timeout:
        logger.error("Request timed out after 10s")
        return {"error": "Request timeout", "retry": True}
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {e}")
        return {"error": f"Network error: {str(e)}"}

@app.route("/beans")
def get_beans():
    """Flask route to expose coffee bean data."""
    result = fetch_beans()
    return jsonify(result)

if __name__ == "__main__":
    # Local testing entry point
    app.run(debug=True, port=5000)
```

**What improved in the output:** The code is now auditable and maintainable. Pydantic models catch schema drift. Logging makes failures visible in production. Docstrings explain the contract. Comments justify decisions (10s timeout, Pydantic validation). The structure is scannable — a new developer can read it in 60 seconds.

**What still failed:** Error handling is still passive. On 500 or timeout, we log and return an error dict, but we don't retry. In production, a single transient failure would fail the request. The client gets a 200 OK with an error body instead of the right HTTP status code. The error responses are inconsistent (some have "retry" flag, some don't).

**What to try next:** I need examples of robust error handling — retry logic, proper HTTP status codes, consistent error structure. I want the model to see what "good" looks like.

---

## Version 5: Examples of What Good Looks Like

**What changed in the prompt:** Added examples of good vs. bad error handling. Specified retry logic, exponential backoff, proper HTTP status codes, and structured error context.

**Prompt:**
```
Write Python code for a Flask app. The CoffeeDB API base URL is https://api.coffeedb.pro/v1. Authentication is via Bearer token in the Authorization header. Rate limit: 100 requests/minute. The /beans endpoint returns JSON with fields: name, origin, roaster, score, flavor_notes. Handle HTTP 429, 500, and timeout errors explicitly.

Output format requirements:
1. Docstring explaining the function's purpose, parameters, and return type.
2. Auth header setup with environment variable validation.
3. Explicit error handling for 429, 500, and timeout with structured logging.
4. JSON response parsing using a Pydantic model for type safety.
5. A main block for local testing.
6. Inline comments explaining each architectural decision.

Error handling requirements (examples of good vs. bad):

BAD: Catch all exceptions and return a generic message.
  ```
  except Exception as e:
      return {"error": "Something went wrong"}
  ```

GOOD: Retry once with exponential backoff for transient errors (500, timeout). Log full context including endpoint, status code, and attempt number. Return specific HTTP status codes to the client.
  ```
  if response.status_code == 500:
      if attempt < max_retries:
          logger.warning("Server error, retrying...", extra={"status": 500, "attempt": attempt})
          time.sleep(backoff * (2 ** attempt))
          continue
      logger.error("Server error after retries", extra={"status": 500, "attempts": attempt + 1})
      return {"error": "CoffeeDB server error", "retry": False}, 502
  ```
```

**Output:**
```python
import os
import logging
import time
from typing import List, Union
import requests
from flask import Flask, jsonify, Response
from pydantic import BaseModel, Field

# Configure logging with structured context for production observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Configuration ---
# Load API key from environment to avoid hardcoding secrets in source control
COFFEEDB_BASE_URL = "https://api.coffeedb.pro/v1"
COFFEEDB_API_KEY = os.getenv("COFFEEDB_API_KEY")
if not COFFEEDB_API_KEY:
    raise ValueError("COFFEEDB_API_KEY environment variable is required")

# --- Pydantic Model for Type Safety ---
# Validates response structure at runtime; fails fast if CoffeeDB changes schema
class CoffeeBean(BaseModel):
    name: str
    origin: str
    roaster: str
    score: float = Field(..., ge=0, le=100)
    flavor_notes: List[str]

def fetch_beans_with_retry(max_retries: int = 1, backoff: float = 2.0) -> Union[List[CoffeeBean], tuple]:
    """
    Fetch coffee beans from CoffeeDB.pro with resilient error handling.
    
    Retries once on transient errors (500, timeout) with exponential backoff.
    Logs full context for every error to aid production debugging.
    Returns proper HTTP status codes to the client.
    
    Args:
        max_retries: Number of retry attempts for transient failures (default: 1)
        backoff: Base seconds for exponential backoff (default: 2.0)
    
    Returns:
        List[CoffeeBean]: Parsed and validated beans on success.
        tuple: (error_dict, http_status_code) on failure.
    """
    headers = {"Authorization": f"Bearer {COFFEEDB_API_KEY}"}
    url = f"{COFFEEDB_BASE_URL}/beans"
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # Rate limit (429): non-retryable, client must back off
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                logger.warning(
                    "Rate limit exceeded",
                    extra={"endpoint": url, "status": 429, "attempt": attempt, "retry_after": retry_after}
                )
                return ({"error": "Rate limit exceeded", "retry_after": retry_after}, 429)
            
            # Server error (500): transient, retry with exponential backoff
            if response.status_code == 500:
                if attempt < max_retries:
                    sleep_time = backoff * (2 ** attempt)
                    logger.warning(
                        "Server error, retrying",
                        extra={"endpoint": url, "status": 500, "attempt": attempt, "backoff": sleep_time}
                    )
                    time.sleep(sleep_time)
                    continue
                logger.error(
                    "Server error after all retries",
                    extra={"endpoint": url, "status": 500, "attempts": attempt + 1}
                )
                return ({"error": "CoffeeDB server error", "retry": False}, 502)
            
            # Unexpected status: log and fail fast
            if response.status_code != 200:
                logger.error(
                    "Unexpected status from CoffeeDB",
                    extra={"endpoint": url, "status": response.status_code, "body": response.text[:200]}
                )
                return ({"error": f"Unexpected status: {response.status_code}"}, 502)
            
            # Success: parse, validate, and return
            data = response.json()
            beans = [CoffeeBean(**item) for item in data]
            logger.info("Fetch successful", extra={"endpoint": url, "beans_count": len(beans), "attempt": attempt + 1})
            return beans
            
        except requests.exceptions.Timeout:
            # Timeout: transient, retry with exponential backoff
            if attempt < max_retries:
                sleep_time = backoff * (2 ** attempt)
                logger.warning(
                    "Request timeout, retrying",
                    extra={"endpoint": url, "timeout": 10, "attempt": attempt, "backoff": sleep_time}
                )
                time.sleep(sleep_time)
                continue
            logger.error(
                "Timeout after all retries",
                extra={"endpoint": url, "timeout": 10, "attempts": attempt + 1}
            )
            return ({"error": "Request timeout", "retry": False}, 504)
            
        except requests.exceptions.RequestException as e:
            # Network-level failure: non-retryable (DNS, connection refused, SSL)
            logger.error(
                "Network error",
                extra={"endpoint": url, "error": str(e), "attempt": attempt}
            )
            return ({"error": f"Network error: {str(e)}", "retry": False}, 502)
    
    # Defensive fallback: should never reach here
    logger.error("Max retries exceeded without resolution")
    return ({"error": "Max retries exceeded", "retry": False}, 502)

@app.route("/beans")
def get_beans():
    """Flask route to expose coffee bean data with proper HTTP status codes."""
    result = fetch_beans_with_retry()
    
    # If result is a tuple, it's an error response with status code
    if isinstance(result, tuple):
        error_data, status_code = result
        return jsonify(error_data), status_code
    
    # Success: serialize Pydantic models to dicts
    return jsonify([bean.model_dump() for bean in result])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

**What improved in the output:** The error handling is now production-grade. Retry logic with exponential backoff for 500/timeout. Proper HTTP status codes returned to the client (429, 502, 504). Structured logging with full context (endpoint, status, attempt, backoff). The error response format is consistent — always includes "retry" flag and appropriate status code. The code is resilient, auditable, and maintainable.

**What still failed:** The retry logic blocks the Flask thread (time.sleep). For a production app, this should be async or use a task queue. But for a portfolio case study, this is the right level of complexity — it shows the pattern without over-engineering.

**What to try next:** Add a test suite or a mock server for local testing. But that's beyond the scope of this prompt ladder. The current output is the final best version.

---

## Four Notes Per Version Summary

### Version 1 (Clearer Goal)
- **Prompt change:** Added specific endpoint and field schema.
- **Output improvement:** Endpoint and fields are explicit. No more guessing what the API returns.
- **Still failed:** No auth, no error handling, no production context.
- **Next:** Add real API context (auth, rate limits, error codes).

### Version 2 (Defined Audience)
- **Prompt change:** Added "for a backend developer in a production Flask app."
- **Output improvement:** Added Flask scaffolding and repository pattern.
- **Still failed:** This is the honest "didn't help" moment. The audience constraint caused over-engineering — abstract classes, service layers, 3x more code. No auth, no error handling. The boilerplate distracted from the real problem.
- **Next:** Drop the audience abstraction. Add real CoffeeDB constraints instead.

### Version 3 (Real Context)
- **Prompt change:** Added base URL, Bearer auth, rate limit, fields, error codes to handle.
- **Output improvement:** Auth, rate limit handling, timeout handling, specific endpoint. The code is grounded in reality and would fail gracefully in production.
- **Still failed:** Error handling is passive — logs nothing, doesn't retry, returns 200 OK with error body.
- **Next:** Add structure (logging, Pydantic, docstrings) and better error handling examples.

### Version 4 (Output Format)
- **Prompt change:** Added explicit format requirements: docstring, auth check, structured logging, Pydantic, main block, inline comments.
- **Output improvement:** Type-safe parsing, production logging, documented decisions, scannable structure. A new developer can read it in 60 seconds.
- **Still failed:** No retry logic. Error responses are inconsistent. Client gets 200 OK with error body instead of proper HTTP status.
- **Next:** Add examples of robust error handling — retry logic, proper status codes, consistent error structure.

### Version 5 (Examples of Good)
- **Prompt change:** Added good vs. bad examples for error handling, with retry logic and proper HTTP status codes.
- **Output improvement:** Retry with exponential backoff, proper HTTP statuses (429, 502, 504), consistent error format, structured logging with full context. Production-grade resilience.
- **Still failed:** time.sleep blocks the Flask thread. For high-traffic production, this should be async or queued. But this is the right scope for a portfolio case study.
- **Next:** Add tests or mock server for local development. Out of scope for this ladder.

---

## Final Reusable Prompt

```
Write Python code for a Flask app that integrates with [API_NAME].

API context:
- Base URL: [BASE_URL]
- Authentication: [AUTH_METHOD]
- Rate limit: [RATE_LIMIT]
- Endpoint: [ENDPOINT] returns JSON with fields: [FIELD_LIST]
- Error codes to handle: [ERROR_CODES]

Output requirements:
1. Docstring explaining purpose, parameters, and return type.
2. Auth setup with environment variable validation.
3. Error handling for each error code with retry logic (exponential backoff for transient errors) and structured logging.
4. JSON response parsing with Pydantic model for type safety.
5. Proper HTTP status codes returned to the client (not 200 for errors).
6. A main block for local testing.
7. Inline comments explaining each architectural decision.

Error handling pattern (good vs. bad):
BAD: Catch all exceptions and return generic message.
GOOD: Retry once with exponential backoff for [TRANSIENT_ERRORS]. Log full context (endpoint, status, attempt, params). Return specific HTTP status codes.
```

**How to adapt:** Replace bracketed fields with your API details. The pattern works for any REST API integration. The key layers are: clear goal → real context → output format → examples of good error handling. Skip the "audience" layer unless you know it helps — it caused over-engineering in this case.

---

## Key Learnings

1. **Clearer goal first.** Adding specific endpoints and fields made the code actually useful. Without this, the model guesses.

2. **Audience can hurt.** The "backend developer" audience added abstraction layers that solved a problem I didn't have. It was the only version that made the output worse. I learned that audience constraints without specific context can trigger generic "production-ready" patterns that obscure the real task.

3. **Real context is the biggest lever.** Auth, rate limits, error codes, and specific fields transformed the code from a toy to a production candidate. This single layer added more value than all others combined.

4. **Output format improves maintainability.** Docstrings, Pydantic, logging, and comments made the code readable. But it didn't fix the error handling logic — that required examples.

5. **Examples of good are the final polish.** The model can follow structure, but it needs to see what robust error handling looks like to implement retry logic, proper status codes, and consistent error formats. Without the examples, V4's error handling was naive.

6. **Side-by-side comparison is essential.** I wouldn't have noticed that V2 was worse without comparing it to V1. Memory is unreliable. The ladder forces honesty.
