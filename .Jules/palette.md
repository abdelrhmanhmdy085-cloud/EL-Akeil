## 2026-02-09 - [Splash Screen Accessibility & Control]
**Learning:** Long splash screen animations (5s+) without a skip option can frustrate returning users. Additionally, splash screens often lack basic accessibility roles, making them invisible or confusing to screen reader users.
**Action:** Always provide a skip button for splash screens and use `role="dialog"`, `aria-modal="true"`, and `aria-hidden="true"` (when closed) to manage focus and visibility for assistive technologies.
