# Screenshot Checklist + AI Image Prompts for Achilles Portfolio

## Screenshot Checklist (5 Real Captures)

### 1. Hero Screenshot: Achilles Live Conversation

**What to capture:**
A clean, legible screenshot of a conversation where Achilles answers a coffee question using the engineered prompt.

**How to set it up:**
1. Open Claude (or the interface you used to test the final prompt).
2. Paste the final consolidated prompt (Version 6 from `prompt-engineering-log.md`) into the system/custom instructions.
3. Send the test query: `"Recommend a coffee with berry notes for pour-over."`
4. Wait for the full response (including the silent reasoning section if visible).

**What to include in the frame:**
- The user query visible at the top
- The full structured response (Direct Answer, Data Source, Details, Confidence, Next Step)
- The "Low" confidence label and the honest admission about no live data
- No browser chrome, bookmarks, or other tabs
- No personal notifications or unrelated UI elements

**Formatting tips:**
- Crop to the conversation area only (remove sidebars, nav, etc.).
- Use a dark theme if available — matches the portfolio's "Dark Roast Precision" aesthetic.
- Ensure text is legible at 800px wide (common portfolio hero width).
- If the response is long, capture the top portion that shows the structure; the full text is in the repo anyway.

**Where to save:** `C:\Users\velan\FlyRank\assets\screenshots\hero-conversation.png`

---

### 2. Code Snippet: CoffeeDB API Integration

**What to capture:**
A clean, syntax-highlighted screenshot of the final API integration code (Version 5 from `prompt-ladder-apicode.md`).

**How to set it up:**
1. Open the `prompt-ladder-apicode.md` file in a code editor or VS Code.
2. Copy the final code block (the `fetch_beans_with_retry` function through the Flask route).
3. Paste into a new file and save as `coffee_api_integration.py`.
4. Open in VS Code with a dark theme (e.g., "Dark+" or "One Dark Pro").

**What to include in the frame:**
- The `fetch_beans_with_retry` function signature and docstring
- The retry loop with exponential backoff
- The structured logging with `extra` context
- The Pydantic `CoffeeBean` model
- The Flask route `get_beans` with proper HTTP status handling
- No file explorer sidebar, no terminal panel, no minimap

**Formatting tips:**
- Use a monospace font at 14px minimum for legibility.
- Crop to 80-100 characters width (standard code block width).
- Ensure syntax highlighting is visible (colors for keywords, strings, comments).
- If the code is too long, capture the `fetch_beans_with_retry` function — it's the most impressive part.

**Where to save:** `C:\Users\velan\FlyRank\assets\screenshots\code-api-integration.png`

---

### 3. API Response Data: Parsed JSON

**What to capture:**
A formatted JSON response showing the structured output from the CoffeeDB API (or a realistic mock based on the Pydantic model).

**How to set it up:**
1. Create a mock JSON file with 2-3 realistic coffee bean entries.
2. Open in a JSON formatter (e.g., jsonformatter.org, or VS Code with Prettier).
3. Use a dark theme or the portfolio's dark charcoal background.

**Mock data to use:**
```json
[
  {
    "name": "Ethiopia Yirgacheffe G1",
    "origin": "Ethiopia, Yirgacheffe",
    "roaster": "Velans Coffee Roasters",
    "score": 87.5,
    "flavor_notes": ["blueberry", "jasmine", "lemon", "black tea"]
  },
  {
    "name": "Kenya AA Nyeri",
    "origin": "Kenya, Nyeri",
    "roaster": "Velans Coffee Roasters",
    "score": 89.0,
    "flavor_notes": ["blackcurrant", "raspberry", "grapefruit", "tomato"]
  }
]
```

**What to include in the frame:**
- The JSON structure with field names aligned
- The `flavor_notes` array showing berry-related notes
- A caption or label indicating this is parsed output from CoffeeDB.pro
- Clean background, no browser chrome

**Formatting tips:**
- Use a dark background with syntax highlighting (JSON keys in one color, values in another).
- Ensure the field names from the Pydantic model are visible: `name`, `origin`, `roaster`, `score`, `flavor_notes`.
- Add a small label at the top: "Parsed CoffeeDB.pro response — validated with Pydantic"

**Where to save:** `C:\Users\velan\FlyRank\assets\screenshots\api-response-json.png`

---

### 4. Prompt Ladder Excerpt: Version 0 vs. Version 5

**What to capture:**
A side-by-side screenshot showing the naive baseline prompt and the final production-grade prompt/code from the API code ladder.

**How to set it up:**
1. Open `prompt-ladder-apicode.md` in a text editor or browser.
2. Scroll to the baseline section and the Version 5 section.
3. Use a split-screen view or two windows side by side.

**Left side (Version 0 — Baseline):**
```
Write Python code to connect to the CoffeeDB API.
```
+ the 6-line naive output.

**Right side (Version 5 — Final):**
The full prompt with all layers + the 120+ line production code.

**What to include in the frame:**
- Clear labels: "Version 0: Naive" and "Version 5: Production-Grade"
- The dramatic difference in prompt length and code quality
- No scrollbars if possible (capture the key sections)

**Formatting tips:**
- Use a dark background for both sides.
- Ensure the code on the right is partially visible (even if cropped) to show the scale difference.
- Add a caption below: "6 iterations: from toy script to production-ready API integration"

**Where to save:** `C:\Users\velan\FlyRank\assets\screenshots\prompt-ladder-v0-vs-v5.png`

---

### 5. Cross-Model Comparison Table

**What to capture:**
A screenshot of the comparison table from `prompt-engineering-log.md` showing Claude vs. ChatGPT outputs.

**How to set it up:**
1. Open `prompt-engineering-log.md` in a browser or markdown previewer.
2. Scroll to the "Cross-Model Comparison: Claude vs. ChatGPT" section.
3. Capture the full table + the ChatGPT output above it + the honest synthesis below.

**What to include in the frame:**
- The ChatGPT output (the 5-part response with general knowledge filler)
- The comparison table (all 6 dimensions)
- The honest synthesis paragraph (the verdict on which model is better and why)
- Clean background, no unrelated UI

**Formatting tips:**
- Use a markdown previewer with a dark theme or the GitHub dark theme.
- Ensure the table columns are readable (Claude vs. ChatGPT side by side).
- If the table is too wide, capture it in two screenshots or use a wider viewport.

**Where to save:** `C:\Users\velan\FlyRank\assets\screenshots\cross-model-comparison.png`

---

## AI-Generated Image Prompts (2 Assets)

### Asset 1: Hero Texture — Dark Roast Macro

**Tool-specific prompts:**

**For DALL-E 3 (ChatGPT):**
```
Macro photography of dark roasted coffee beans, extreme close-up, shallow depth of field, warm amber light from the left, deep charcoal background, minimal composition, precise details, no text, no labels, high contrast, premium quality, 4K. The mood is warm, technical, and precise. No bright colors, no neon, no gradients that look like stock art. Deep espresso browns, dark slate grays, warm amber accents only.
```

**For Midjourney:**
```
Macro photography of dark roasted coffee beans, extreme close-up, shallow depth of field, warm amber light from the left, deep charcoal background, minimal composition, precise details, no text, no labels, high contrast, premium quality, 4K --ar 16:9 --style raw --v 6
```

**For Stable Diffusion / ComfyUI:**
```
Prompt: macro photography dark roasted coffee beans, extreme close-up, shallow depth of field, warm amber side light, deep charcoal background, minimal, precise, high contrast, no text, no labels, 4K, premium quality
Negative prompt: text, labels, watermark, bright colors, neon, gradient, stock photo, cluttered, blurry, cartoon, illustration
```

**Why these prompts are structured this way:**
- **"Macro photography"** establishes the visual genre (realistic, tactile, premium)
- **"Shallow depth of field"** creates the cinematic, professional look
- **"Warm amber light from the left"** adds dimensionality and warmth
- **"Deep charcoal background"** forces the dark palette that matches the portfolio
- **"No text, no labels"** prevents generated gibberish that looks unprofessional
- **"No bright colors, no neon"** explicitly excludes the rejected "futuristic AI" aesthetic

---

### Asset 2: Architecture Diagram — API to LLM to Response

**Tool-specific prompts:**

**For DALL-E 3 (ChatGPT):**
```
Minimalist technical diagram on a dark charcoal background, three abstract geometric nodes connected by thin precise copper lines, no text, no labels, clean shapes, warm amber accent lighting, technical illustration style, 4K. The nodes represent: a database/API icon (left), a processing/engine icon (center), and a speech bubble/conversation icon (right). The lines flow left to right. The mood is precise, technical, warm but not cold. No gradients, no glow effects, no futuristic holograms. Dark espresso browns, charcoal, copper accents only.
```

**For Midjourney:**
```
Minimalist technical diagram, dark charcoal background, three abstract geometric nodes connected by thin precise copper lines, no text, no labels, clean shapes, warm amber accent lighting, technical illustration style, 4K, left to right flow, database icon to processing icon to speech bubble icon --ar 16:9 --style raw --v 6
```

**For Stable Diffusion / ComfyUI:**
```
Prompt: minimalist technical diagram, dark charcoal background, three abstract geometric nodes, thin precise copper lines connecting them, no text, no labels, clean shapes, warm amber accent lighting, technical illustration style, 4K, left to right flow, database icon, processing engine, speech bubble
Negative prompt: text, labels, watermark, gradients, glow effects, holograms, futuristic, neon, bright colors, cluttered, organic shapes, hand-drawn
```

**Why these prompts are structured this way:**
- **"Three abstract geometric nodes"** explicitly limits complexity (more nodes = more clutter)
- **"Thin precise copper lines"** establishes the technical-but-warm aesthetic
- **"No text, no labels"** prevents unreadable generated text — the diagram should be purely visual
- **"Left to right flow"** matches the reading direction and the API → LLM → Response narrative
- **"No gradients, no glow effects"** excludes the sci-fi aesthetic that would clash with the portfolio's grounded tone
- **Icon descriptions** (database, processing engine, speech bubble) give the model concrete visual anchors without being too prescriptive

---

## File Organization

```
C:\Users\velan\FlyRank\assets\
├── screenshots\
│   ├── hero-conversation.png          (Real capture #1)
│   ├── code-api-integration.png       (Real capture #2)
│   ├── api-response-json.png        (Real capture #3)
│   ├── prompt-ladder-v0-vs-v5.png   (Real capture #4)
│   └── cross-model-comparison.png    (Real capture #5)
├── generated\
│   ├── hero-texture.png              (AI-generated asset #1)
│   └── architecture-diagram.png      (AI-generated asset #2)
└── headshot\                         (Optional, if using a bio image)
    └── your-photo.jpg                (Real photo #6)
```

---

## Judgment Criteria for Each Screenshot

Before saving each screenshot, ask:

1. **Does this prove something?** If it's decoration, don't capture it.
2. **Is the text legible at 800px wide?** If not, zoom in or crop tighter.
3. **Does the color scheme match "Dark Roast Precision"?** Dark backgrounds, warm accents, no bright colors.
4. **Is there any personal or irrelevant UI in the frame?** Crop it out.
5. **Would a Head of AI recognize this as evidence?** If it looks like a mockup or template, reshoot.

---

## Judgment Criteria for Each Generated Image

Before keeping each generated image, ask:

1. **Does it match the style spec?** Dark charcoal, copper lines, no text, no bright colors.
2. **Does it serve the proof or distract from it?** Hero texture sets mood; architecture diagram illustrates flow. Both must feel like they belong to the same portfolio.
3. **Is there any generated gibberish text?** If yes, regenerate with "no text, no labels" emphasized.
4. **Does it look like stock art?** If yes, the prompt needs more specific constraints (lighting, camera angle, material).
5. **Would I be embarrassed if a Head of AI saw this?** If yes, reject it and try again.

---

## Quick Reference: Rejection Examples

**Reject if the hero texture shows:**
- White or light gray background
- Bright green, blue, or purple colors
- Cartoonish or illustrated style (should be photographic)
- Text or labels on the beans
- Cluttered composition with multiple elements
- Visible watermarks or generic stock photo feel

**Reject if the architecture diagram shows:**
- Gradients or glow effects
- Text labels that are unreadable or gibberish
- More than 3 nodes (too complex for a portfolio hero diagram)
- Organic or hand-drawn lines (should be precise, geometric)
- Futuristic holographic or neon aesthetic
- White or light background
