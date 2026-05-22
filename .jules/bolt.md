## 2026-05-22 - Nested loop optimization in clip addition
**Learning:** For functions like `add_clips_to_timeline` that interact with a large media pool (potentially thousands of clips), an O(N*M) search is a significant bottleneck. Using a hash map to index media pool items by name/path reduces the lookup time dramatically.
**Action:** Always prefer indexing large collections into a hash map when performing multiple lookups by key, especially in performance-critical editor actions.
