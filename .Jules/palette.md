# Palette Journal

## 2025-05-18 - Tab Control Accessibility & Keyboard Navigation
**Learning:** Replacing non-semantic `<div>` tab controls with `<button type="button" class="tab" role="tab">` elements and explicit `:focus-visible` styling dramatically improves keyboard navigation and screen reader support without breaking existing CSS rules or tab layout.
**Action:** Always convert custom tab controls into semantic `<button>` elements with `role="tab"`, `role="tablist"`, `aria-selected`, and `aria-controls` for accessible tabbed interfaces.
