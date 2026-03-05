# Palette's UX Journal

## 2025-03-05 - [Accessibility & Navigation Conflicts]
**Learning:** Overwriting shared navigation containers (like `#langControls`) using `innerHTML` can destroy other interactive elements such as notification badges. Additionally, using `div` for form labels prevents screen readers from associating text with inputs.
**Action:** Use `prepend()` or `appendChild()` instead of `innerHTML` for dynamic UI injections. Always use semantic `<label htmlFor="...">` and matching `id`s for form accessibility.
