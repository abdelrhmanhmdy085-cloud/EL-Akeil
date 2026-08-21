## 2026-03-30 - Map Control Accessibility
**Learning:** Icon-only map overlay buttons (like recenter/location pins) frequently lack explicit `aria-label` attributes, relying solely on `title` tooltips which are inaccessible to screen reader users who navigate via touch or key focus.
**Action:** Always provide explicit `aria-label` matching or complementing the `title` attribute for icon-only map controls.
