## 2025-05-14 - [Optimize clip lookup in add_clips_to_timeline]
**Learning:** Nested loops for matching items in large collections (like the Media Pool) can lead to significant performance degradation as the project grows. A hash map (dictionary) provides O(1) lookup and drastically improves responsiveness.
**Action:** Always prefer hash maps over nested loops when searching for multiple items in a list, especially when dealing with potentially large data structures from the Resolve API.
