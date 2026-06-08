## 2026-06-08 - Optimized clip addition to timeline
**Learning:** Found a critical $O(N \times M)$ bottleneck in `add_clips_to_timeline` where every target clip was searched linearly through the entire media pool.
**Action:** Always use hash maps (dictionaries) when matching a list of target items against a large pool to achieve $O(N + M)$ complexity. Ensure to preserve the original "first-match" behavior by checking if the key already exists before insertion if needed.
