## 2025-05-14 - [Navigation Overwrite Pattern]
**Learning:** The i18n system's `initLanguage` function in `i18n.js` overwrites the entire innerHTML of its target container (`#langControls`). This causes any other elements (like notification bells or login buttons) placed inside that container to be deleted upon initialization.
**Action:** Always place the language toggle in its own dedicated, empty container to prevent unintended destruction of neighboring UI elements.
