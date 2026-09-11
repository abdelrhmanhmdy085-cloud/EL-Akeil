## 2026-09-11 - Accessible Toggle Switch Pattern

**Learning:** Custom UI toggle switches implemented using non-interactive container elements (`<div>`) with `onclick` handlers prevent screen reader users and keyboard navigation users from discovering or toggling states using Space or Enter keys.
**Action:** Convert toggle containers into semantic `<button type="button" role="switch" aria-checked="true|false">` elements with CSS resets (`border: none`, `width: 100%`, `font-family: inherit`), explicit `:focus-visible` outline indicators, and dynamic JavaScript updates to `aria-checked` upon state changes.
