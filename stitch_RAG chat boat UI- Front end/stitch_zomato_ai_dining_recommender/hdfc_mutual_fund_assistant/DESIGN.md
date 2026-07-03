---
name: HDFC Mutual Fund Assistant
colors:
  surface: '#10131a'
  surface-dim: '#10131a'
  surface-bright: '#363941'
  surface-container-lowest: '#0b0e15'
  surface-container-low: '#191b23'
  surface-container: '#1d2027'
  surface-container-high: '#272a31'
  surface-container-highest: '#32353c'
  on-surface: '#e1e2ec'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#e1e2ec'
  inverse-on-surface: '#2e3038'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#bec6e0'
  on-secondary: '#283044'
  secondary-container: '#3f465c'
  on-secondary-container: '#adb4ce'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00a572'
  on-tertiary-container: '#00311f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#10131a'
  on-background: '#e1e2ec'
  surface-variant: '#32353c'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  title-md:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '500'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  code:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 20px
  lg: 32px
  xl: 64px
  container-max: 1200px
  gutter: 24px
---

## Brand & Style
The design system is engineered for high-stakes financial environments where precision and trust are paramount. It adopts a **Corporate Modern** aesthetic influenced by the clarity of developer-centric platforms like Stripe and Vercel, but infused with the sophisticated depth of high-end fintech.

The atmosphere is "Safe-Certainty"—it feels like a secure vault that is also a cutting-edge laboratory. The visual language balances high-density data presentation with a serene, uncluttered interface. We utilize a dark-mode default to reduce eye strain during prolonged analysis and to make primary data points and accent colors pop with surgical precision.

## Colors
The palette is rooted in a spectrum of deep, obsidian blues to establish a foundation of stability. 

- **Primary Blue (#3B82F6):** Used for primary actions, interactive elements, and user chat bubbles. It signifies "Action" and "Intelligence."
- **Secondary Navy (#0F172A):** The core container color, providing a softer contrast than pure black.
- **Teal Accent (#10B981):** Reserved for "Success" states, positive market trends, and growth indicators.
- **Gold Accent (#F59E0B):** Used sparingly for premium features, warnings, or "Facts-only" highlights to ensure immediate visual hierarchy.
- **Neutral Grays:** We use a range of cool-toned slates for secondary text and disabled states to maintain the cold, professional atmosphere.

## Typography
This design system utilizes a dual-font strategy. **Outfit** is used for headlines and titles; its geometric construction adds a modern, tech-forward feel. **Inter** is used for all body copy, data tables, and labels to ensure maximum legibility and a systematic, utilitarian appearance.

For Markdown support:
- **Bold Text:** Use `fontWeight: 600` for emphasis.
- **Blockquotes:** Rendered with a `2px` left border in `primary_color_hex` and an italicized `Inter` font.
- **Links:** Primary blue with an underline on hover.

## Layout & Spacing
The layout follows a 12-column grid for desktop, a 6-column grid for tablet, and a 4-column grid for mobile. We prioritize a "Dense but Clear" rhythm, using 20px (md) as the standard padding for cards and containers.

The chat interface is centered within the `container-max` to ensure focus. For data-heavy views, the system uses a fluid layout that allows charts to expand to the full width of the screen while maintaining consistent side margins of 24px (gutter).

## Elevation & Depth
We employ a **Glassmorphic** approach to depth. Rather than traditional shadows, elevation is communicated through backdrop blurs and varying opacity of surface fills.

- **Level 1 (Base):** Solid `#020617`.
- **Level 2 (Cards):** Surface color at 60% opacity with a `16px` backdrop blur and a `1px` border of `rgba(255, 255, 255, 0.08)`.
- **Level 3 (Modals/Overlays):** Surface color at 80% opacity with a `32px` backdrop blur and a soft, wide-spread shadow (`0 20px 40px rgba(0,0,0,0.4)`).

This creates a sense of light passing through the interface, reminiscent of high-end dashboard hardware.

## Shapes
The shape language is "Soft-Precision." We use a standard 8px (0.5rem) radius for most UI elements. This avoids the playfulness of fully pill-shaped components while moving away from the aggressive sharpness of pure industrial design.

- **Small elements (Checkboxes, Tooltips):** 4px.
- **Standard elements (Buttons, Input fields):** 8px.
- **Large elements (Cards, Chat Bubbles):** 16px.

## Components

### Chat Bubbles
- **User Bubble:** Right-aligned. Background: `#2563EB`. Text: White. Shape: `rounded-lg` with a sharper corner on the bottom right.
- **AI Bubble:** Left-aligned. Background: `rgba(255, 255, 255, 0.05)`. Border: `1px solid rgba(255, 255, 255, 0.1)`. Text: Slate-200. Shape: `rounded-lg` with a sharper corner on the bottom left.

### Facts-Only Disclaimer (Warning)
- **Style:** A thin, horizontal banner or card with a subtle `accent_gold` glow.
- **Background:** `rgba(245, 158, 11, 0.05)`. 
- **Border:** `1px solid rgba(245, 158, 11, 0.3)`.
- **Icon:** Use a solid "shield" or "info" icon in gold.

### Buttons
- **Primary:** Solid blue gradient (`#3B82F6` to `#2563EB`) with a subtle white inner-glow at the top.
- **Ghost:** Transparent background with a `1px` white border at 10% opacity.

### Input Fields
- Dark backgrounds (`#020617`) with a persistent `1px` border. On focus, the border glows blue and the background remains dark to maintain focus on the text.

### Cards & Data Tables
- Use the Glassmorphic level 2 styling. Data headers should use the `label-caps` typography style for a professional, institutional feel.