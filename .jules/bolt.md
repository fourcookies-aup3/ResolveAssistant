## 2025-05-15 - Mock Pollution in Headless Environment
**Learning:** Running multiple tests in a single `pytest` session in a headless environment where GUI libraries are mocked via `sys.modules` can lead to mock pollution. State from one test (like call counts) can bleed into another, causing flaky failures.
**Action:** Run tests individually or ensure a complete state reset of `sys.modules` and mock objects between test cases when GUI mocking is involved.

## 2025-05-15 - Preserving First-Match Behavior in Hash Maps
**Learning:** When converting an $O(N \times M)$ search loop that breaks after the first match to an $O(N+M)$ hash map, iterating through the source list in reverse while building the map ensures that the first occurrence in the original list is the one that remains in the final dictionary.
**Action:** Use `reversed(collection)` when building lookup maps from lists where "first-match" semantics must be preserved.
