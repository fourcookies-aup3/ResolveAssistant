## 2025-05-14 - [Hash Map optimization for clip lookup]
**Learning:** Replacing an O(N*M) nested loop with an O(N+M) hash map lookup in `add_clips_to_timeline` yields significant performance gains as the media pool grows. Using `reversed()` when building the map is a clean way to maintain "first-match" semantics.
**Action:** Always check for nested loops in search/filter operations involving large lists and consider hash map optimizations.
