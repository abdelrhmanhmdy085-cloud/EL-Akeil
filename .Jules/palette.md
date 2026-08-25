## 2026-08-25 - Modal Close Button Accessibility and Keyboard Navigation
**Learning:** Modal close controls implemented as non-semantic `<span>` tags lack built-in keyboard focusability, screen reader role announcement, and Escape key handling. Using semantic `<button type="button">` with `aria-label`, CSS `:focus-visible` outlines, and explicit `Escape` event listeners provides an intuitive and accessible experience.
**Action:** Always convert modal close triggers to semantic `<button type="button">` with localized ARIA labels, focus-visible styles, and Escape key dismissal listeners.
