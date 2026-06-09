## 2025-05-15 - [O(N*M) lookup in add_clips_to_timeline]
**Learning:** Found a nested loop in `add_clips_to_timeline` that compared every target clip name against every clip in the media pool. This scales poorly as projects grow (e.g., 10,000 clips in pool and 5,000 targets took ~1.64s).
**Action:** Always prefer hash map (dictionary) lookups for matching sets of items, reducing complexity from O(N*M) to O(N+M). Verified ~432x speedup with benchmark.
