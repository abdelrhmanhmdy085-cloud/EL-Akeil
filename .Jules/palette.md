## 2026-03-11 - Semantic Interactive Elements
**Learning:** Using non-semantic elements like <div> for buttons (e.g., language toggles, notification icons) breaks keyboard accessibility as they are not focusable or interactive by default.
**Action:** Always use semantic <button> elements for interactive controls and provide localized ARIA labels via the i18n system.

## 2026-03-11 - Safe UI Injection
**Learning:** Using innerHTML to inject UI elements into shared containers (like #langControls) can unintentionally overwrite existing features like notification badges or login buttons.
**Action:** Use prepend() or appendChild() to inject new UI elements into existing containers to maintain DOM stability.
