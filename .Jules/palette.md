## 2026-03-01 - Accessible Password Toggle with RTL Support

**Learning:** When adding password visibility toggles in multi-language (LTR & RTL) interfaces, use CSS logical property `inset-inline-end: 12px` and `padding-inline-end` for input fields instead of `right` or `left` to ensure seamless alignment across layout directions. Always update both `data-i18n-aria-label` / `data-i18n-title` and dynamic `aria-label` / `title` fallback attributes upon toggling so screen reader users receive immediate accessible feedback.

**Action:** Wrap password inputs in `.password-wrapper` with relative positioning, position toggle buttons using `inset-inline-end`, and dynamically update ARIA attributes and tooltips on toggle interaction.
