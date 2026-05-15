## 2025-05-15 - [Optimize clip lookup in add_clips_to_timeline]
**Learning:** The previous implementation of `add_clips_to_timeline` used an O(N*M) nested loop to match clip names against the entire media pool. For large projects with 1000+ clips, this caused a noticeable delay of ~0.7s per call. Using a hash map (dictionary) for clip indexing reduces this to O(N+M), achieving a >200x speedup in benchmarks (~0.002s).
**Action:** Always consider using hash maps for lookups when dealing with collections that may grow large, especially when the lookup is performed inside a loop.
