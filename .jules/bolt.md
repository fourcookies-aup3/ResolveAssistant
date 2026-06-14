## 2025-05-14 - Isolate GUI Mocks in Tests
**Learning:** Running all tests in a single `pytest` session can lead to cross-test pollution when mocking core GUI libraries like `pyautogui` or `cv2` via `sys.modules`. This causes unexpected assertion failures in later tests because the mock state is shared.
**Action:** Execute tests individually (e.g., `python3 tests/test_file.py`) or ensure thorough mock resets between test cases to maintain isolation in headless environments.

## 2025-05-14 - Significant Speedup with Hash Map Lookup
**Learning:** Replacing a nested loop ($O(N \times M)$) with a hash map ($O(N + M)$) for media pool clip lookups resulted in a ~180x performance improvement for a pool of 10,000 clips. Even simple dictionary lookups can be massive wins in automation scripts handling large datasets.
**Action:** Always prefer hash map lookups over repeated linear scans when dealing with potentially large collections in the Media Pool.
