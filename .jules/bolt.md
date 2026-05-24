## 2025-05-15 - Quadratic bottleneck in media pool clip lookup
**Learning:** The `add_clips_to_timeline` function used a nested loop (O(N*M)) to match clip names against the media pool, which caused significant lag as the project grew. A hash map (dictionary) reduces this to linear time (O(N+M)).
**Action:** Always check for nested loops during collection processing and consider using hash-based lookups for O(1) access when possible.
