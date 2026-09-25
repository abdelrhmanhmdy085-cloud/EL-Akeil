## 2025-05-18 - Accessible Category Cards

**Learning:** Category card containers dynamically rendered in JavaScript (`categories.html`) required conversion from `<div>` to `<button type="button">` with CSS resets (`border: none`, `padding: 0`, `width: 100%`, `text-align: inherit`, `font-family: inherit`) and `:focus-visible` outline indicators to ensure full keyboard navigation and screen reader support without breaking card flex layouts.
**Action:** When converting clickable card containers into semantic `<button>` elements, apply explicit CSS resets and set `aria-label` attributes combining name and item count while using `aria-hidden="true"` on decorative icons and arrows.
