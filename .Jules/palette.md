## 2026-01-30 - Splash Screen Accessibility and I18n
**Learning:** Adding ARIA roles (dialog, modal) to splash screens and properly handling its dismissal with aria-hidden is crucial for a compliant UX. Also, using prepend() for i18n-injected elements avoids overwriting existing navigation items.
**Action:** Always check if i18n script overwrites the entire navbar and use semantic elements (button instead of div) for interactive icons.
