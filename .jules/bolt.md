## 2026-06-23 - [Optimize clip lookup in add_clips_to_timeline]
**Learning:** Nested loops for looking up media items in a large pool create an $O(N \times M)$ bottleneck that becomes noticeable as project complexity grows.
**Action:** Use hash map (dictionary) lookups to achieve $O(N+M)$ complexity. Ensure 'first-match' behavior by only populating the map with the first encounter of a key.
