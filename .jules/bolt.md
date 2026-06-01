## 2025-05-15 - $O(N \cdot M)$ Bottleneck in Clip Matching
**Learning:** The `add_clips_to_timeline` function used a nested loop to match a list of clip names against all clips in the media pool. This scales poorly ($O(N \cdot M)$) as projects grow, leading to significant delays (seconds to minutes) in automation tasks.
**Action:** Always use hash maps (dictionaries) for lookups when matching items between two lists in a media-rich environment. This reduced processing time for 2,000 clips in a 10,000-clip pool from ~2.6s to ~0.02s (~130x speedup).
