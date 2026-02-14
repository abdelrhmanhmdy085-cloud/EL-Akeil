## 2025-01-30 - Semantic Role Selection Buttons
**Learning:** Using `<div>` for interactive role-selection cards prevents keyboard accessibility and fails screen reader identification. Converting them to `<button>` elements with `appearance: none` and `focus-visible` styles preserves the design while meeting core accessibility standards.
**Action:** Always prefer `<button>` for card-like interactive elements and use `:focus-visible` to provide distinct visual feedback for keyboard users without affecting mouse users.
