# Palette's UX Journal

## 2026-05-22 - Semantic Language Toggle
**Learning:** Using `div` with `onclick` for the language toggle makes it inaccessible to keyboard users (no tab focus, no 'Enter' key support).
**Action:** Use a `<button>` element instead of a `div` for interactive controls to ensure they are keyboard-navigable and have the correct role by default.
