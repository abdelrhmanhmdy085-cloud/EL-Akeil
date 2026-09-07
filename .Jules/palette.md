## 2026-01-07 - Accessible Form Labels in Auth Forms
**Learning:** In static HTML forms, using non-semantic `<div>` elements as field headers prevents screen readers from properly associating label text with form inputs and eliminates tap/click-to-focus behavior.
**Action:** Always wrap form input headers in semantic `<label for="[input_id]">` tags with `display: block` to ensure proper WCAG 1.3.1 compliance and touch accessibility.
