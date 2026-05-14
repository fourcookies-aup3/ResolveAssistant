## 2025-05-15 - [Efficient Media Pool Lookups]
**Learning:** In large video projects, the media pool can grow to thousands of clips. A nested O(N*M) loop for adding clips to a timeline becomes a significant bottleneck. Using a hash map (dictionary) for lookups reduces this to O(N+M).
**Action:** Use dictionaries to index media assets by name or path when performing batch operations like adding clips to timelines.

## 2025-05-15 - [Test Isolation & Mocking]
**Learning:** Running multiple tests that mock `sys.modules` in the same process (like `pytest`) can cause cross-test contamination and failures.
**Action:** Run tests individually or ensure rigorous cleanup/reloading of `sys.modules` if mocking libraries like `pyautogui` or `cv2`.
