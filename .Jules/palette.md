## 2026-02-25 - [Semantic Buttons & Accessible I18n]
**Learning:** Many interactive elements in this app were implemented as divs/spans with onclick, making them inaccessible to keyboard users. Converting them to semantic buttons requires CSS resets (background, border, padding, font-family) to preserve the design.
**Action:** Always prefer <button> for actions. Use data-i18n-aria-label with updated i18n.js to ensure screen readers receive localized context.

## 2026-02-25 - [I18n Initialization Integrity]
**Learning:** Using .innerHTML to inject language toggles can accidentally destroy other navigation elements (like Login/Register) within the same container.
**Action:** Use .insertAdjacentHTML('afterbegin', ...) or .prepend() to add the language toggle while preserving existing navbar items.

## 2026-02-25 - [HTML Nesting Restrictions]
**Learning:** <button> elements only permit phrasing content. Nesting headings (h3), paragraphs (p), or divs inside a button is invalid HTML and can cause CI/deployment failures or rendering issues.
**Action:** Use <span> with display: block and appropriate styling (classes like .h3-equivalent) to replicate heading/block styles inside a button while maintaining HTML validity.
