## 2025-05-14 - Optimized clip lookup in add_clips_to_timeline
**Learning:** Nested loops in API calls can cause significant performance degradation when handling large media pools. Switching from $O(N \times M)$ to $O(N + M)$ using a hash map provides a measurable and substantial speedup.
**Action:** Always look for opportunities to replace nested search loops with hash map lookups, especially when dealing with lists that can grow large.

## 2025-05-14 - Headless environment test isolation
**Learning:** Running multiple tests that mock the same GUI libraries in a single `pytest` session can lead to cross-test pollution and unexpected failures in a headless environment.
**Action:** Run tests individually or ensure rigorous cleanup/reset of mocked modules between test runs when working in headless environments without a `DISPLAY`.
