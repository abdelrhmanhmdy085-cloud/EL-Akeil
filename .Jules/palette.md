## 2026-03-31 - Hero Search & Location Picker Accessibility Trigger
**Learning:** Icon triggers inside search bars (such as `.location-icon`) rendered as non-semantic `<div>` elements prevent JS event listeners (`document.getElementById('locateBtn')`) from binding and block keyboard accessibility.
**Action:** Always wrap interactive search bar icons in semantic `<button type="button">` elements with matching `id`, localized `aria-label`/`title` attributes, and CSS `:focus-visible` styling.
