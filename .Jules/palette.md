## 2025-05-22 - [Accessibility & i18n Optimization]
**Learning:** Standardizing i18n for non-textual elements (like ARIA labels and titles) significantly improves accessibility for screen reader users in multi-lingual apps. Also, using `prepend()` instead of `innerHTML` in dynamic UI initialization prevents accidental destruction of other UI components.
**Action:** Use `data-i18n-aria-label` and `data-i18n-title` patterns in all future components. Always prefer `prepend()`/`append()` or DOM manipulation over `innerHTML` for partial UI updates.
