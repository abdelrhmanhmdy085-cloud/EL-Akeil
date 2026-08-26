## 2026-08-26 - Customer Dashboard Tab Accessibility
**Learning:** Tab controls rendered as `div` elements lack keyboard navigation, focus indicators, and screen reader announcements (`role="tab"`, `aria-selected`). Relying on global `event.target` can also cause fragile tab switching.
**Action:** Always replace non-semantic `div` tabs with `<button type="button" class="tab" role="tab">` elements wrapped in a `role="tablist"` container, managing `aria-selected` and `:focus-visible` states explicitly.
