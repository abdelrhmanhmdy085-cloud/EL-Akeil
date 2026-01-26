## 2025-05-14 - [i18n Attribute Support & Splash Skip]
**Learning:** Standard translation systems often miss ARIA labels and title attributes, which are vital for screen reader accessibility. Also, non-interactive splash screens are a common UX friction point for returning users.
**Action:** Enhance the i18n logic to support `data-i18n-aria-label` and `data-i18n-title` consistently across the app. Always ensure splash screens can be dismissed via click or a skip button.
