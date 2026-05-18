## 2024-05-18 - [Optimized clip lookup in add_clips_to_timeline]
**Learning:** Found an O(N*M) nested loop in `add_clips_to_timeline` where N is the number of clips in the media pool and M is the number of clips to add. For a media pool with 10,000 clips, adding 10,000 clips took ~64.7s.
**Action:** Replaced the nested loop with a hash map (dictionary) for clip lookup, reducing complexity to O(N+M). This improved performance for 10,000 clips to ~0.027s, a >2000x speedup.
