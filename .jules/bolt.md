# Bolt Performance Journal

## 2025-05-22 - Optimized clip lookup in add_clips_to_timeline
**Learning:** The previous (N \times M)$ implementation of clip lookup in `add_clips_to_timeline` was a significant bottleneck when dealing with large media pools (e.g., 100,000 clips). Replacing the nested loop with a hash map (dictionary) pre-indexed by name and filename reduces the complexity to (N + M)$.
**Impact:**
- For 100,000 pool clips and 1,000 target clips, execution time dropped from ~0.478s to ~0.180s (~2.6x speedup).
- Note: The speedup is more pronounced as the number of target clips ($) or pool clips ($) increases, as the complexity changed from multiplicative to additive.
**Action:** Always prefer hash map indexing for lookups in collections where $ and $ can be large. Preserved 'first-match' behavior by iterating through the original list in reverse when building the map.
