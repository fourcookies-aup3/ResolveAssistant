## 2025-05-15 - Optimized Clip Addition Performance
**Learning:** The previous implementation of `add_clips_to_timeline` used an $O(N \times M)$ nested loop to match target names against the media pool. In projects with thousands of clips, this caused a significant and measurable lag (up to 16 seconds for 10k clips).
**Action:** Replaced the linear search with an $O(N+M)$ hash map lookup. Always index large collections before performing multiple lookups.

## 2025-05-15 - Test Pollution in Headless Environment
**Learning:** Running the entire test suite via `pytest` in this headless environment caused cross-test pollution because multiple tests were modifying `sys.modules` to mock GUI libraries. This led to intermittent assertion failures in `tests/test_advanced.py`.
**Action:** Run performance-sensitive or mock-heavy tests in isolation using `python3 tests/test_file.py` or ensure clean state reset between test runs.
