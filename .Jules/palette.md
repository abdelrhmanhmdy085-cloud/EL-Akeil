## 2026-09-20 - Mode Toggles on Authentication Forms
**Learning:** Mode toggles in authentication forms (such as switching between login and registration in `driver_auth.html`) implemented using anchor elements (`<a>`) without `href` attributes lack keyboard focusability and screen reader semantics.
**Action:** Always use semantic `<button type="button">` elements with CSS resets and `:focus-visible` outline indicators for in-page mode toggles to guarantee full keyboard accessibility and screen reader support.
