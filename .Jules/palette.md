## 2025-08-23 - Form Label-Input Association in Checkout
**Learning:** Form controls in static or server-rendered HTML forms that rely only on nesting `<input>` inside or adjacent to `<label>` without explicit `for` and `id` attributes can break screen reader context and prevent label-click focusing/selection across different browsers.
**Action:** Always ensure explicit `for` attributes on `<label>` elements matching unique `id` attributes on form inputs (`<input>`, `<select>`, `<textarea>`, radio/checkbox controls).
