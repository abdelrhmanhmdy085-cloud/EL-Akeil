## 2025-05-15 - [Accessibility and I18n Integrity]
**Learning:** In projects with dynamic internationalization, using `innerHTML` to inject language controls can inadvertently destroy other interactive elements (like notification bells or login links) in the same container. Semantic HTML conversion (div/span to button) must be paired with CSS resets to maintain the visual design while improving accessibility.
**Action:** Use `prepend` or `appendChild` for dynamic UI injection instead of `innerHTML`. Always add focus-visible styles when introducing keyboard-accessible elements.
