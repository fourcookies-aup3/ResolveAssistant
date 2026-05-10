## 2026-05-10 - [O(N^2) to O(N) Clip Lookup & Instant Input]
**Learning:** The clip lookup in `add_clips_to_timeline` was a major bottleneck for large projects (1000+ clips). Using a hash map for lookups reduced execution time from ~0.6s to ~0.0015s for 1000 clips. Additionally, reducing `moveTo` duration to 0 and explicitly setting `PAUSE` significantly improves automation "snappiness".
**Action:** Always check for nested loops in media management logic and use hash maps for indexing where possible.
