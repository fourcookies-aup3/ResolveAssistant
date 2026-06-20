## 2025-05-15 - Hash Map Optimization for Clip Lookup
**Learning:** Replacing nested $O(N \times M)$ loops with a dictionary-based $O(N + M)$ lookup provides a massive speedup (>200x) in projects with large media pools (10,000+ items).
**Action:** Always prefer hash maps/dictionaries for multi-target lookups in lists, especially when the source list remains static during the operation.

## 2025-05-15 - Headless GUI Testing Side Effects
**Learning:** Mocking GUI libraries like `pyautogui` or `cv2` using `sys.modules` in a single `pytest` session can lead to cross-test pollution and unexpected assertion failures.
**Action:** Run tests in isolation (separate processes) or carefully reset mocks when testing GUI automation in headless environments.
