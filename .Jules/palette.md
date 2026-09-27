# Palette's UX & Accessibility Journal

## 2026-09-27 - Converting Custom Toggle Switches to Semantic ARIA Switch Buttons
**Learning:** Custom interactive toggle wrappers (like `div.toggle-heatmap`) are invisible to keyboard navigation and screen readers unless built with native button semantics (`<button type="button" role="switch">`) and proper focus styles.
**Action:** When creating toggle switches or interactive card controls, always use a native `<button type="button" role="switch" aria-checked="...">` container with explicit CSS reset, `:focus-visible` outline indicators, and dynamic `aria-checked` JS state updates.
