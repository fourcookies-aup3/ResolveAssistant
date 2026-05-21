## 2025-05-15 - Optimize clip lookup in add_clips_to_timeline
**Learning:** Nested loops for matching items between two lists (Media Pool and target clips) lead to O(N*M) complexity, which causes significant lag as the media pool grows. Using a hash map reduces this to O(N+M).
**Action:** Always prefer hash map lookups when matching items from large collections.
