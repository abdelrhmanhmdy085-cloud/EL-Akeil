## 2026-06-05 - [Icon-to-Button conversion for Accessibility]
**Learning:** Decorative icons used for interactions (like a location pin in a search bar) should always be converted to semantic <button> elements with explicit aria-label and title for keyboard and screen reader support. Global :focus-visible styles ensure these new buttons are navigable without affecting mouse users.
**Action:** Always check for non-semantic interactive elements (divs/spans with click handlers) and convert them to buttons.

## 2026-06-05 - [Encoding issues in JSON localization]
**Learning:** Writing to JSON files with emojis can easily trigger mojibake (e.g., âœ… for ✅) if encoding isn't strictly UTF-8 throughout the read/write/parse cycle.
**Action:** Use Python with 'encoding="utf-8"' and 'ensure_ascii=False' for surgical JSON updates to prevent character corruption.
