## 2026-07-06 - [Initial Audit]
**Learning:** Found O(N*M) nested loop in `add_clips_to_timeline` and redundant disk I/O / full-color matching in `find_image_on_screen`.
**Action:** Prioritize hash map optimization for clip lookup and grayscale/caching for vision logic.

## 2026-07-06 - [Hash Map Optimization for Clip Lookup]
**Learning:** Replacing O(N*M) nested loops with an O(N+M) hash map in `add_clips_to_timeline` significantly improves performance when dealing with large media pools (e.g., 10,000+ clips). Reversing the list during map construction preserves the "first-match" behavior of the original loop.
**Action:** Use hash maps for element lookups in collections that can grow significantly.
