# Palette's Journal - Critical UX/Accessibility Learnings

## 2026-02-11 - [Splash Screen Skip Pattern]
**Learning:** For apps with cinematic or long-duration splash screens (e.g., 5s+), providing an immediate "Skip" option is crucial for returning users and usability. Managing multiple phase-based timeouts is essential to prevent state conflicts when the skip action is triggered.
**Action:** Always store timeout IDs in accessible variables and implement a cleanup function that clears all pending transitions before immediate dismissal. Use 'aria-hidden' to ensure hidden splash screens are ignored by screen readers.

## 2026-02-11 - [Handling Repository Hygiene in UX PRs]
**Learning:** When running backend servers for frontend verification, ensure that auto-generated files like '__pycache__' and local databases ('data.db') are NOT committed. These files can significantly clutter PR diffs and violate line-count constraints.
**Action:** Always run 'git status' before submitting and restore any accidentally modified or deleted binary files that were already in the repository.
