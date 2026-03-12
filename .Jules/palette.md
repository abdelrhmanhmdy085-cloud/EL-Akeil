## 2026-03-12 - Dynamic i18n Re-application
**Learning:** When refactoring page logic to avoid reloads (e.g., toggling Login/Register modes), simply updating `data-i18n` attributes is insufficient if the translation script only runs on page load. The `applyTranslations(lang)` function must be explicitly called after DOM updates to ensure the new state is correctly localized.
**Action:** Always call the global translation applicator after dynamic UI updates that involve localized strings.

## 2026-03-12 - Semantic Form Labels and Password Visibility
**Learning:** Converting `div` based labels to semantic `<label>` elements significantly improves accessibility. Additionally, providing a password visibility toggle with localized ARIA labels and RTL/LTR aware positioning enhances the user experience for multi-lingual authentication forms.
**Action:** Use `<label for="...">` for all form inputs and provide visibility toggles for password fields by default.
