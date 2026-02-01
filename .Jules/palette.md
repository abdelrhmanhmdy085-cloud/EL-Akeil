## 2026-05-22 - [Splash Screen Skip Button]
**Learning:** For apps with a splash screen, especially those that last more than 2-3 seconds, providing a 'Skip' button is a essential for UX, as it respects the user's time and prevents frustration.
**Action:** Always include a Skip option for any splash screen or long intro animation.

## 2026-05-22 - [Accessibility via Semantic Elements]
**Learning:** Many interactive elements implemented as `div` or `span` with `onclick` are not keyboard accessible by default. Converting them to `<button>` elements with proper resets is the most robust way to ensure accessibility without complex JS.
**Action:** Prioritize `<button>` for any clickable action that isn't a link.

## 2026-05-22 - [i18n Attribute Support]
**Learning:** Accessibility attributes like `aria-label` and `title` must be part of the internationalization system to ensure a truly inclusive experience for all languages.
**Action:** Enhance any custom i18n system to support attribute translation via `data-i18n-*` pattern.
