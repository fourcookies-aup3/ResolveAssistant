## 2025-05-14 - Optimize clip addition with hash map
**Learning:** The previous implementation of `add_clips_to_timeline` used a nested loop to match clip names against the media pool, resulting in O(N*M) complexity. For large projects with thousands of clips, this became a significant bottleneck.
**Action:** Always use hash maps (dictionaries in Python) for looking up items in large collections by property (like name or path) to achieve O(1) lookup time.
