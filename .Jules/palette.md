# Palette's Journal - Critical UX & Accessibility Learnings

## 2025-03-05 - Explicit Label-Input Associations in Dynamic HTML Forms
**Learning:** In static HTML forms as well as dynamically injected form sections (e.g., adding dishes or line items via JavaScript), screen readers require explicit `for` and `id` linking between `<label>` elements and form controls (`<input>`, `<textarea>`, `<select>`) to properly announce form inputs when focused.
**Action:** Always generate unique `id`s and matching `for` attributes when dynamically rendering form fields in JavaScript template strings.
