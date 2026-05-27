## 2026-05-27 - Optimize clip lookup in add_clips_to_timeline
**Learning:** Nested loops (O(N*M)) for matching requested clip names against a media pool are a major bottleneck as projects scale. A hash map (O(N+M)) provides a massive speedup (480x in benchmarks) while still allowing for "first-match" priority if implemented carefully.
**Action:** Use dictionary-based indexing for any multi-item lookup operations involving lists or media pools.
