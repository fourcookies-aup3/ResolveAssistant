## 2025-05-14 - Optimized clip lookup in add_clips_to_timeline
**Learning:** Nested loops $O(N \times M)$ for matching clips in large media pools create significant latency. Using a hash map $O(N+M)$ reduces lookup time from seconds to milliseconds.
**Action:** Always prefer hash map lookups over nested loops when matching items between two collections, especially for media asset management.

## 2025-05-14 - Isolate tests in headless environments
**Learning:** Running multiple tests that mock global modules (like `sys.modules['pyautogui']`) can lead to mock pollution and unexpected assertion failures if state is not reset or tests are run together.
**Action:** Run tests individually or ensure rigorous cleanup when mocking global state to prevent side effects between test suites.
