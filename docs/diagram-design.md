# NextRole Diagram Design System

## Design Philosophy

**Modern AI Infrastructure + Enterprise SaaS**

The style should communicate:

* AI-native
* Professional
* Technical but approachable
* Premium SaaS
* Clean GitHub README aesthetic
* Documentation-first
* Not cyberpunk
* Not dark mode
* Not overly colorful

Think:

* OpenAI docs
* Vercel diagrams
* Stripe architecture illustrations
* Linear UI aesthetics
* Modern cloud architecture graphics

---

# Color Palette

Derived from the NextRole logo.

### Primary Gradient

Used for logos, headers, key arrows, highlights.

```css
Blue:  #1565D8
Azure: #1D9BF0
Teal:  #19B8A5
Mint:  #56D98A
```

Gradient:

```css
linear-gradient(
  90deg,
  #1565D8 0%,
  #1D9BF0 35%,
  #19B8A5 70%,
  #56D98A 100%
)
```

---

### Secondary Colors

#### Deep Blue

Used for:

* Titles
* Stage labels
* Main arrows

```css
#1A4FA3
```

---

#### Teal Green

Used for:

* Success paths
* Shared context
* Iteration loops

```css
#16B887
```

---

### Background

Always:

```css
#FFFFFF
```

Avoid:

* Dark backgrounds
* Black containers
* Heavy gradients behind content

The white background is what makes it README-friendly.

---

# Layout Structure

## Vertical Pipeline Layout

Preferred for workflows.

```text
Stage 1
   ↓
Stage 2
   ↓
Stage 3
   ↓
 Parallel
 ↙     ↘
 A       B
 ↘     ↙
   Join
    ↓
Stage 5
    ↓
Stage 6
```

Characteristics:

* Strong vertical flow
* Plenty of whitespace
* Equal spacing between stages
* Perfect alignment

---

## Architecture Layout

Preferred for system diagrams.

```text
Users
   ↓

Supervisor Layer

 ┌───────────────┐
 │ Main Agent    │
 └───────────────┘

      ↓

Subagents Layer

 ┌───┐ ┌───┐ ┌───┐
 │ A │ │ B │ │ C │
 └───┘ └───┘ └───┘

      ↓

Outputs Layer
```

Layers are always visually separated.

---

# Container Style

## Main Cards

Shape:

```text
Rounded Rectangle
```

Radius:

```text
20-28px
```

Style:

```text
White fill
Soft shadow
Thin blue border
```

Border:

```css
1.5px solid #D7E8FF
```

---

### Header Cards

Used for:

* Main Agent
* Supervisor
* Stage banners

Style:

```text
Pill shape
Blue → Green gradient
White text
```

Example:

```text
[ MAIN AGENT • SUPERVISOR ]
```

---

# Icon Style

## Preferred

Use:

* Outline icons
* Thin stroke icons
* Modern SaaS icon packs

Examples:

### Stage 1

📋 intake

### Stage 2

📄 processing

### Stage 3

🔍 research

### Resume

📄✨

### Interview

💬

### Battlecard

🛡️

### Updates

🔄

---

Avoid:

* 3D icons
* Cartoon icons
* Emoji style icons
* Photorealistic illustrations

---

# Stage Number System

Each stage gets:

```text
①
②
③
④
⑤
⑥
```

Style:

* Circular badge
* Blue gradient
* White number

Example:

```text
 ○1
```

Position:

Top-left corner of the card.

---

# Connection Style

## Primary Flow

Use:

```text
Solid blue arrows
```

Color:

```css
#1565D8
```

Thickness:

```text
2-3px
```

---

## Context Flow

Use:

```text
Dashed green arrows
```

Color:

```css
#16B887
```

Purpose:

* Shared context
* Feedback loops
* Iteration

---

## Parallel Branches

Left branch:

```css
#16B887
```

Right branch:

```css
#1565D8
```

This creates visual balance.

---

# Typography

## Font Family

Use:

```text
Inter
```

Alternatives:

```text
Geist
IBM Plex Sans
Manrope
```

---

## Hierarchy

### Titles

```text
28-36px
SemiBold
```

Color:

```css
#1A4FA3
```

---

### Stage Titles

```text
20-24px
SemiBold
```

---

### Description Text

```text
16-18px
Regular
```

---

# Shadows

Very important.

Use:

```css
box-shadow:
0 8px 24px rgba(21,101,216,0.08);
```

Not:

```css
0 20px 60px rgba(...)
```

The style should feel lightweight.

---

# README Optimization Rules

Always generate diagrams with:

### Canvas

```text
16:9 landscape
```

or

```text
4:5 portrait
```

---

### Margins

```text
Large whitespace
```

---

### Export

```text
PNG
Transparent-safe
High resolution
```

---

# Signature NextRole Elements

Every diagram should contain at least 3 of these:

### 1. Logo in top-left

The N + Rocket mark.

### 2. Blue→Green Gradient

Used somewhere prominent.

### 3. Rounded SaaS Cards

White cards with soft borders.

### 4. Circular Stage Badges

Numbered workflow indicators.

### 5. Dashed Context Lines

Green dashed lines for shared context.

### 6. Thin Outline Icons

Modern documentation aesthetic.

---

# Reusable Prompt Template

For future image generation:

> Create a premium SaaS architecture diagram in the NextRole design system. Use a pure white background, large whitespace, rounded white cards with subtle blue borders and soft shadows, blue-to-teal-to-green gradients derived from the NextRole logo (#1565D8 → #1D9BF0 → #19B8A5 → #56D98A), thin modern outline icons, Inter typography, circular numbered stage badges, solid blue directional arrows, dashed green context-flow arrows, clean GitHub README style, Vercel/Stripe/OpenAI documentation aesthetics, high information density while maintaining clarity, professional enterprise AI platform branding, vector-style infographic quality.
