## 2026-03-29 - Password Visibility Toggles Logical Positioning
**Learning:** For password visibility toggles across bi-directional (RTL/LTR) layouts, using absolute positioning with CSS logical property `inset-inline-end: 12px` inside a relative wrapper automatically ensures flawless alignment without requiring direction-specific overrides.
**Action:** Always wrap password inputs in a `.password-wrapper` and position toggle buttons with `inset-inline-end` and `padding-inline-end` on the input.
