## 2025-05-22 - [Enhancing Landing Page UX & Accessibility]
**Learning:** Forcing users to wait through long splash screen animations (5s) without a skip option is a major UX friction point. Additionally, icon-only buttons (like language toggles or location pins) must be semantic buttons with ARIA labels to be accessible.
**Action:** Always include a skip option and click-to-dismiss for intro animations. Use semantic <button> elements with data-i18n-aria-label for icon-only interactive elements.
