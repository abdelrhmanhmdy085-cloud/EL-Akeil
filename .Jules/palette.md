## 2025-05-14 - [Splash Screen Control & i18n Accessibility]
**Learning:** A long splash screen (5s) without user control can be frustrating. Adding a "Skip" button improves perceived performance. Also, many existing apps have incomplete i18n support for accessibility attributes like 'aria-label', which can be easily fixed by enhancing the i18n utility to support 'data-i18n-aria-label'.
**Action:** Always provide a skip option for intrusive animations and ensure the i18n system covers all user-facing strings including ARIA labels.

## 2025-05-14 - [Naming Conflict in Flask/Python]
**Learning:** Having a directory and a file with the same name (e.g., 'chef/' and 'chef.py') in the same package can cause import confusion in Python, where the package (directory) might be prioritized over the module (file).
**Action:** Avoid naming directories and files identically within the same namespace to prevent import errors.
