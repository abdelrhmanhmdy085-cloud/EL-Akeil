## 2025-05-10 - Accessible Dish Cards in Category View
**Learning:** Dynamic card elements rendered via JS that trigger navigation/clicks must use semantic `<button type="button">` elements with CSS resets and explicit `aria-label` text describing key item attributes (e.g. name, chef, price, rating) to provide screen readers complete context while keeping decorative icons hidden via `aria-hidden="true"`.
**Action:** Always convert interactive card wrappers into semantic `<button type="button">` tags with `:focus-visible` styling and descriptive `aria-label` content.
