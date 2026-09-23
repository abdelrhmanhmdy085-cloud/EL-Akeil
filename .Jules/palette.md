# Palette's Journal - UX & Accessibility Learnings

## 2026-09-23 - Dynamic Category Filter Button Group Accessibility
**Learning:** Dynamic category filter buttons rendered via JavaScript missing explicit `type="button"`, `:focus-visible` focus outlines, and `aria-pressed` toggle state leave keyboard and screen-reader users without interactive context.
**Action:** Always ensure dynamically rendered filter button containers feature `role="group"` with descriptive `aria-label`, button elements set explicit `type="button"`, `:focus-visible` ring/outline styles, and toggle `aria-pressed="true|false"` when filter selection changes.
