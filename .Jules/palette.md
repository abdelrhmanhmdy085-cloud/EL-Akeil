## 2026-09-04 - Category Filter Toggle Class Preservation
**Learning:** When adding `aria-pressed` toggle behavior to button groups with utility classes (such as `.btn` and `.btn-outline`), resetting classes in JS must strictly preserve the primary base button class (`.btn`) so interactive elements do not lose layout styling (padding, line-height) when toggled.
**Action:** In JS reset handlers, explicitly target buttons with `.classList.add('btn', 'btn-outline')` and `.classList.remove('active-filter')` instead of removing `.btn`.
