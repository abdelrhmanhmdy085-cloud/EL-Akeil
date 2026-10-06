# Palette's UX & Accessibility Journal

## 2026-10-06 - CSS Reset for Converted Interactive Buttons
**Learning:** Converting non-semantic elements (like `<div>` or `<span>`) to semantic `<button type="button">` can introduce default browser button borders and background colors (visual regressions) if CSS resets like `background: transparent; border: none;` are not explicitly defined.
**Action:** Always include clean CSS button resets (`background: transparent; border: none; cursor: pointer;`) when converting non-semantic icon wrappers to semantic `<button>` elements.
