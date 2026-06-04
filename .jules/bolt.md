## 2025-05-15 - Optimized add_clips_to_timeline with hash map
**Learning:** Nested loops for lookup in large datasets (like a media pool with thousands of clips) are a major bottleneck ((N \times M)$). Using a hash map (dictionary) for (1)$ lookups reduces complexity to (N + M)$.
**Action:** Always check for nested loops where one list is being searched for items from another list. Replace with dictionary-based lookups for significant performance gains.

## 2025-05-15 - Headless testing with GUI mocks
**Learning:** Running tests that depend on GUI libraries like `pyautogui` and `cv2` in a headless environment requires careful mocking of `sys.modules` before importing the modules that use them. Furthermore, running all tests in a single `pytest` session can cause mock pollution if different tests mock the same modules differently.
**Action:** Run tests individually or ensure that mocks are correctly reset/isolated when running in a headless environment.
