# Bolt Performance Journal

⚡ Speed is a feature. Every millisecond counts. ⚡

## 2025-05-15 - Optimize clip lookup in add_clips_to_timeline
**Learning:** Nested loops for looking up items in large collections (like a media pool) create an $O(N \times M)$ bottleneck that scales poorly. Using a hash map (dictionary) for lookup reduces this to $O(N + M)$.
**Action:** Always check for nested loops when matching items between two lists and consider using a dictionary if the lookup key is unique or the first match is sufficient.
