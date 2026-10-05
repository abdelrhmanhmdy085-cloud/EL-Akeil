## 2026-10-05 - Semantic FAQ Accordions & Focus Indicators
**Learning:** Replacing non-semantic clickable `<div>` elements with standard `<button type="button">` tags for accordion triggers allows built-in keyboard navigation (Tab, Space, Enter) and screen reader support (`aria-expanded`, `aria-controls`, `aria-labelledby`).
**Action:** When working on accordion or expandable list interfaces, ensure triggers use native `<button type="button">` tags with explicit `:focus-visible` styling and dynamic `aria-expanded` attributes.
