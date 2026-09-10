# Explain It Like You Built It: Achilles Preference Memory

## The Friend Question

> "Okay, so your coffee bot remembers what I like. But I just typed 'I prefer natural processed coffees' in a chat box. How does it know that's a *preference* and not just part of a normal question? And how does it actually *use* that preference the next time I ask for a recommendation?"

---

## The Short Answer

Achilles doesn't "understand" preferences like a human does. It runs a set of regex patterns — literal text searches — over every message you send. If your message matches a pattern like `I prefer [something]`, the bot extracts that something, stores it in a JSON file on disk, and adds a hidden score boost to beans that match it next time it searches.

It's not intelligence. It's a filing cabinet with a very fast clerk.

---

## The Four Moving Parts

### Part 1: The Regex Patterns (The Clerk's Script)

When you send a message, Achilles runs four regex patterns:

```python
patterns = [
    (r"i\s+like\s+(\w+)", "flavor_like"),
    (r"i\s+prefer\s+(\w+)", "preference"),
    (r"i\s+want\s+([\w\s]+)\s+beans", "bean_type"),
    (r"i\s+usually\s+drink\s+(\w+)", "usual_drink"),
]
```

Each pattern looks for a specific sentence structure. `i prefer natural` matches the second pattern. The `\w+` captures the word after "prefer" — in this case, "natural". That word gets stored under the key "preference".

### Part 2: The JSON File (The Filing Cabinet)

Preferences are stored in a file called `achilles_memory.json`:

```json
{
  "demo_user": {
    "preferences": {
      "preference": "natural"
    },
    "history": [
      {"role": "user", "text": "I prefer natural processed coffees", "ts": "2026-09-10T16:22:00"},
      {"role": "achilles", "text": "Try Hambela Bishan...", "ts": "2026-09-10T16:22:01"}
    ]
  }
}
```

Every user gets their own entry. The history array keeps the last 20 conversation turns (so the file doesn't grow forever). The preferences dictionary stores extracted keywords.

The file is read when the server starts and written every time a preference changes. If the server crashes, preferences survive. If you delete the file, everyone starts fresh.

### Part 3: The Score Boost (The Clerk's Hidden Work)

When you ask "What do you recommend from Ethiopia?", Achilles doesn't just look for Ethiopian beans. It gives every bean a score:

- Origin match: +3 points
- Flavor note match: +2 points per note
- Process match: +2 points
- Roast level match: +1 point
- **Preference boost: +4 points if the bean's process matches your stored preference**

So if you previously said "I prefer natural" and now ask about Ethiopia, the Natural-processed Ethiopian bean (Hambela Bishan) gets +3 for "Ethiopia" plus +4 for "Natural" — a total of 7 points. The Washed-processed Ethiopian bean (Yirgacheffe) only gets +3. Hambela wins.

This is the entire "memory" mechanism. No neural network. No embeddings. Just addition.

### Part 4: The Matching Engine (The Search)

The matching engine loops through all beans in the database and checks whether your query words appear in each bean's fields:

```python
for bean in beans:
    score = 0
    if bean["origin"].lower() in query:  # "ethiopia" → +3
        score += 3
    for note in bean["flavor_notes"]:
        if note.lower() in query:        # "berry" → +2
            score += 2
    if bean["process"].lower() in query:  # "natural" → +2
        score += 2
    if bean["roast_level"].lower() in query:  # "light" → +1
        score += 1
    # ... preference boost applied here
```

After scoring, beans are sorted by score (highest first) and the top 3 are returned. The reply is a template string filled with the top bean's data:

> "Try **Hambela Bishan** from Tim Wendelboe — Ethiopia, Natural process, Light-Medium roast. Score: 89. Notes: strawberry, peach, chocolate, floral."

---

## The "Wait, Really?" Moment

The first time I tested this, I typed "I prefer natural processed coffees" and then asked "What do you recommend from Ethiopia?" I expected the bot to recommend the Natural Ethiopian bean. It did. But I didn't understand *why* it worked until I added print statements to the scoring function.

Hambela Bishan scored 7. Yirgacheffe G1 scored 3. The +4 preference boost was the difference. Without it, both would have scored 3 (origin match only) and Yirgacheffe would have won because it has a higher base score (91 vs 89).

The preference boost doesn't just change the recommendation — it *overrides* the default ranking. That's the whole point of memory: your stated preferences matter more than the database's quality scores.

---

## Why This Isn't "Real" AI

A real recommendation system would use:
- **Embeddings**: convert "I like fruity coffees" into a vector and find beans with similar vectors
- **Collaborative filtering**: look at what other users with similar tastes liked
- **An LLM**: let a language model interpret the query and generate a recommendation

Achilles uses none of these. It uses:
- **Keyword matching**: exact word matches only
- **Regex extraction**: only catches four specific sentence patterns
- **Additive scoring**: simple arithmetic, no learning from feedback

This is a feature, not a bug, for an MVP. It works offline, runs in milliseconds, and produces deterministic, explainable results. When it recommends a bean, I can tell you exactly why: +3 for origin, +4 for preference, +2 for process match. No black box.

---

## The Limitation I Found

The regex patterns are brittle. If you type "I love natural coffees" or "Natural is my favorite process", the bot doesn't catch it. Only exact matches to the four patterns work. I could add more patterns, but each one is a manual addition — the system doesn't learn new patterns from conversation.

A real version would use an LLM for preference extraction: "Extract any preferences about origin, process, or flavor from this message." But that requires an API key, rate limits, and cost. For this MVP, the four regex patterns cover 80% of typical preference statements.

---

## In One Sentence

**Achilles remembers your preferences by running four regex patterns over every message, storing matched keywords in a JSON file, and adding a hidden +4 score boost to beans that match those keywords the next time it searches — a filing clerk with a calculator, not a mind reader.**
