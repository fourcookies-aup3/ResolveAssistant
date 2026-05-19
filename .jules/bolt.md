## 2025-05-15 - Optimize clip addition performance
**Learning:** The previous implementation of `add_clips_to_timeline` used a nested loop (O(N*M)) to match clip names against the media pool, which caused significant slowdowns when dealing with thousands of clips.
**Action:** Replaced the nested loop with a hash map lookup (O(N+M)), achieving over 700x speedup for 10,000 clips (from ~6.86s to ~0.009s). Always look for nested loops over large datasets that can be optimized with dictionaries.
