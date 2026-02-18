## 2025-05-14 - [Dynamic ARIA Labels with i18n]
**Learning:** Using 'data-i18n-aria-label' in a global i18n script allows for accessible, multi-lingual icon buttons without manual JavaScript for each button.
**Action:** Always implement 'data-i18n-aria-label' support in the core i18n utility to ensure icon-only buttons remain accessible across all supported languages.

## 2025-05-14 - [DOM Persistence vs i18n Initialization]
**Learning:** Components that need to persist state (like notification badges) should be placed outside of containers that are dynamically overwritten by i18n scripts (e.g., using `.innerHTML`).
**Action:** When auditing UI bugs where elements "disappear" after a language switch, check if they are nested inside an i18n-managed container.
