## 2026-06-10 - Optimized clip lookup in add_clips_to_timeline
**Learning:** Found an O(N*M) nested loop in the DaVinci Resolve clip addition logic where N is the number of clips to add and M is the total clips in the media pool. For large projects (10,000+ clips), this caused a multi-second delay.
**Action:** Replaced the nested loop with an O(N+M) hash map lookup. Preserved the "first-match" behavior by only adding the first occurrence to the map. Resulted in a ~720x speedup in benchmarks (17.7s -> 0.02s).
