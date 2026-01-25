## 2025-05-14 - [i18n Container Safety]
**Learning:** Overwriting a global container like `#langControls` to inject a language toggle can destroy other critical UI elements (notifications, login buttons) that are added dynamically or reside in the same container.
**Action:** Always use `prepend()` or `append()` or target a specific sub-container for dynamically injected UI elements to ensure coexistence with other features.

## 2025-05-14 - [Loading States with Visual Feedback]
**Learning:** Pure text "Loading..." states are less engaging and can be missed by users. A visual spinner combined with text provides better feedback.
**Action:** Use a reusable CSS-based spinner pattern for all async data loading containers.

## 2025-05-14 - [Semantic Buttons for Accessibility]
**Learning:** Using `div` or `span` with `onclick` for interactive elements like language toggles or location icons breaks keyboard navigation and screen reader support.
**Action:** Always use semantic `<button>` elements for interactive actions and ensure they have descriptive `aria-label` or `title` attributes.
