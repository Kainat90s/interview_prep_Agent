---
name: premium_light_ui_design
description: Guidelines and design principles for building premium, clean, light-themed web interfaces with modern layouts, typography, and SVG icons.
triggers:
  - "improve UI"
  - "make UI premium"
  - "light theme"
  - "website layout"
  - "replace emojis"
---

# Premium Light Theme UI Guidelines

When building or updating user interfaces for web applications, prioritize high-end design aesthetics over raw or AI-generated defaults.

## 1. Color Palette (Light Theme)
Avoid using saturated, basic colors. Rely on HSL or tailored hex values:
- **Base Background:** Slate 50 (`#f8fafc`) or cool grey (`#f3f4f6`) for soft contrast.
- **Card Background:** Pure white (`#ffffff`) to raise content above the base background.
- **Brand Primary:** Indigo 600 (`#4f46e5`) or Blue 600 (`#2563eb`) to convey professionalism.
- **Brand Secondary:** Slate 900 (`#0f172a`) for titles and deep headers.
- **Borders:** Thin, elegant Slate 200 (`#e2e8f0`) or Slate 100 (`#f1f5f9`).
- **Text Hierarchy:**
  - **Headings:** Slate 900 (`#0f172a`)
  - **Body text:** Slate 700 (`#334155`)
  - **Muted text:** Slate 500 (`#64748b`) or Slate 400 (`#94a3b8`)

## 2. Layout Structure & Containers
- **Header (Navbar):** Sticky (`top: 0`), high `z-index`, clean white background with a thin bottom border (`1px solid #e2e8f0`). Apply a subtle blur (`backdrop-filter: blur(16px)`) if using a semi-transparent white background.
- **Page Layout:** Minimum height (`min-height: calc(100vh - 64px)`), standard page padding (`padding: 3rem 1.5rem`), centered max-width content container (`max-width: 1200px`).
- **Footer:** Add a global, professional footer. Align logo, links, copyright, and social indicators with standard grids.
- **Card Styling:**
  - Border radius: `1rem` or `0.75rem` for friendly, modern aesthetics.
  - Border: `1px solid #e2e8f0` (Slate 200).
  - Shadows: Diffused, premium drop shadow (`box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04), 0 8px 10px -6px rgba(0, 0, 0, 0.04)`).
  - Hover micro-animations: Translate Y slightly (`transform: translateY(-4px)`) and increase shadow intensity on hover.

## 3. Icons vs. Emojis
- **Never use raw emojis** for primary UI elements (e.g., in card badges, feature lists, page headings). They look generic and AI-made.
- **Always use SVG icons** (either custom inline SVGs or React icon packages like Lucide).
- Set uniform sizes (e.g., `width: 24px; height: 24px;`) and wrap them in custom circular or square badges with soft primary backgrounds (e.g., `background: rgba(79, 70, 229, 0.08); color: #4f46e5;`).

## 4. Typography
- Import modern typography (e.g., Google Fonts like `Inter`, `Outfit`, `Plus Jakarta Sans`).
- Set `line-height` carefully (`line-height: 1.6` for copy, `line-height: 1.2` for headings).
- Use proper font-weights (`700` or `800` for bold visual impact, `500` for active/medium elements, `400` for regular body).
