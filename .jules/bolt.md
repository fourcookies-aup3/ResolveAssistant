## 2025-05-15 - Optimize Clip Selection Bottleneck
**Learning:** The `add_clips_to_timeline` function used a nested loop for clip matching, resulting in $O(N \times M)$ complexity. In environments with many media pool items, this causes significant lag. Additionally, relying on `clip.path` without null checks can lead to `TypeError`.
**Action:** Always prefer hash map (dictionary) lookups for matching operations against large collections. Ensure attributes used in path operations (like `clip.path`) are verified as non-null before use.
