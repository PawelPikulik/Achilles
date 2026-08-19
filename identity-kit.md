# Identity Kit: Achilles Portfolio

## Fonts

| Role | Font | Source | Why |
|------|------|--------|-----|
| Headings | **Space Grotesk** | [Google Fonts](https://fonts.google.com/specimen/Space+Grotesk) | Geometric, technical, precise. Signals engineering confidence without coldness. |
| Body | **Inter** | [Google Fonts](https://fonts.google.com/specimen/Inter) | Highly legible, modern standard for UI. Neutral, so the content speaks. |
| Code / captions | **SFMono / Consolas** | System monospace | Already in use. Reserved for technical evidence (screenshots, code snippets, data). |

## Palette

| Token | Hex | Usage |
|-------|-----|-------|
| **Charcoal** | `#17130f` | Primary background. Deep, grounded, never pure black. |
| **Cream** | `#f2e9dd` | Primary text. Warm, readable, softer than white. |
| **Copper** | `#c17f3e` | Primary accent. CTAs, labels, key highlights. Warm, metallic, precise. |
| **Muted** | `#a89a86` | Secondary text, captions, borders. Recedes so the work is loudest. |

**Removed from active use:** `espresso` (#241b14) and `amber` (#d9a05b) are now reserved for hover states and image gradients only. The palette is tight: 4 colors do all the work.

## Logo / Favicon

A simple monogram: **"P"** in Space Grotesk, set in copper on a charcoal background. Used as `favicon.svg` and as a small mark in the footer or credibility strip if needed.

```svg
<!-- assets/favicon.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="12" fill="#17130f"/>
  <text x="50" y="68" font-family="Space Grotesk, sans-serif" font-size="60" font-weight="700" fill="#c17f3e" text-anchor="middle">P</text>
</svg>
```

## Two-Line Style Note

> **Dark Roast Precision.** Deep charcoal backgrounds with warm copper accents. Space Grotesk headings for technical confidence; Inter body for clarity. The design frames the work — it never upstages it.

Add this to the Claude Project custom instructions so every build stays consistent.
