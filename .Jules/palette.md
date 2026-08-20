## 2025-02-20 - Modal Close Button Accessibility and i18n
**Learning:** Modal close elements built with `<span>` tags lack keyboard focus and screen reader descriptions. Extending `i18n.js` to process `data-i18n-aria-label` and `data-i18n-title` attributes allows icon-only modal close `<button>` elements to remain accessible across language toggles.
**Action:** Always convert modal close `<span>` tags to `<button type="button">` with CSS resets (`background: none`, `border: none`) and `data-i18n-aria-label` attributes.
