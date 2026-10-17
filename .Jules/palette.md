## 2026-03-29 - Navigation Route Panel Minimize Toggle Micro-UX

**Learning:** When adding collapse/minimize toggle buttons to dynamic overlay panels (e.g. navigation route information panels created in JavaScript), using explicit `<button type="button">` with `aria-label`, `title`, and dynamic `aria-expanded` attributes ensures both screen reader clarity and keyboard accessibility.
**Action:** When creating toggle controls in JS dynamic UI elements, manage `aria-expanded` state along with tooltip (`title`) and `aria-label` updates on user interaction.
