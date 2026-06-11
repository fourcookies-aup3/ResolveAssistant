## 2025-06-11 - Avoiding Cross-Test Pollution with GUI Mocks
**Learning:** In this codebase, mocking GUI libraries (pyautogui, cv2, PIL) using `sys.modules` in the test setup causes significant cross-test pollution when running with `pytest`. This leads to assertion failures where mocks from previous tests interfere with current ones.
**Action:** Always execute tests individually using `python3 tests/test_file.py` instead of `python3 -m pytest tests/` to ensure a clean process for each test suite, or use a more robust mocking strategy that clears `sys.modules` between runs.

## 2025-06-11 - Clip Selection Performance Bottleneck
**Learning:** The `add_clips_to_timeline` function used a nested loop search ($O(N \times M)$) to find clips by name in the media pool. This scales poorly as media pools grow, leading to multi-second delays for common project sizes.
**Action:** Use hash map lookups ($O(N+M)$) for clip selection. Ensure "first-match" behavior is preserved by checking for key existence before insertion into the map.
