## 2025-05-15 - Hash map optimization for clip lookups
**Learning:** Nested O(N*M) loops for matching target clips against the Media Pool cause massive slowdowns as the project grows. Aプロジェクト with 5000 clips can take nearly a minute just to identify 200 clips for addition.
**Action:** Always use a hash map (dictionary) for clip lookups by name or path. Iterating in reverse when building the dictionary preserves 'first-match' behavior if duplicate names exist.

## 2025-05-15 - Global mock pollution in tests
**Learning:** Tests that mock `sys.modules` (like `pyautogui`) can pollute the global state, causing failures when multiple test files are run in the same process via `pytest`.
**Action:** Run tests individually or ensure absolute isolation when mocking global modules in a headless environment.
