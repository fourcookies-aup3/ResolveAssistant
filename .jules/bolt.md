# Bolt Performance Journal

## 2025-05-15 - Optimize clip lookup in add_clips_to_timeline
**Learning:** Replacing an $O(N \times M)$ nested loop with an $O(N+M)$ hash map lookup provides a massive speedup (~171x) when dealing with large media pools (10,000+ clips).
**Action:** Always prefer dictionary-based lookups for linear searches in large datasets. To preserve "first-match" behavior when building the map, iterate the source list in reverse so that the first occurrence in the original list overwrites later ones and remains as the final value.
