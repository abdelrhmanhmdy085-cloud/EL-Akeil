## 2026-03-02 - Accessible Password Toggle for Bi-directional Forms
**Learning:** Bi-directional (RTL/LTR) authentication forms require relative input wrappers with CSS logical properties (`inset-inline-end`, `padding-inline-end`) and explicit `type="button"` on password toggle triggers to prevent accidental form submission while maintaining visual alignment across languages.
**Action:** When adding password visibility toggles, wrap the input in a relative container using logical inline end positioning and apply dynamic `aria-label` and `title` updates with language fallbacks.
