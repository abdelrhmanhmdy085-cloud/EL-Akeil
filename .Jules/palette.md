# Palette Journal

## 2026-09-30 - Category Detail Dish Card Keyboard Focus & Screen Reader Support
**Learning:** Dynamically rendered dish cards in category listing views (`category.html`) were non-interactive `<div>` containers lacking keyboard focus and screen reader descriptions. Converting them to `<button type="button" class="dish-card">` with explicit CSS resets (`border: none; padding: 0; width: 100%; text-align: inherit; font-family: inherit`), `:focus-visible` outlines, descriptive `aria-label`s, and `aria-hidden="true"` on emoji glyphs provides seamless keyboard accessibility and clean assistive reader output without breaking card flex layouts.
**Action:** When converting dynamic card components to `<button>` elements, ensure CSS resets maintain font inheritance and text alignment, and construct comprehensive `aria-label` strings that summarize card details.
