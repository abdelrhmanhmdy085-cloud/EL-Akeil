## 2026-02-16 - [Modal Keyboard Accessibility]
**Learning:** Using non-semantic elements like 'div' or 'span' for interactive components (like cards or close buttons) breaks keyboard navigation. Converting them to semantic 'button' elements automatically provides them with the 'button' role and makes them focusable.
**Action:** Always prioritize semantic elements ('button', 'a') for interactive components. If using a non-semantic element is unavoidable, ensure 'role="button"' and 'tabindex="0"' are added, along with keyboard event listeners for 'Enter' and 'Space'.

## 2026-02-16 - [Global Focus Visibility]
**Learning:** Many projects lack explicit focus styles, leaving keyboard users without visual feedback. A simple ':focus-visible' global style can significantly improve accessibility without affecting mouse users.
**Action:** Add a high-contrast ':focus-visible' outline to the global stylesheet in every project to ensure baseline keyboard accessibility.
