## 2025-05-15 - [O(N*M) Clip Lookup in Media Pool]
**Learning:** The `add_clips_to_timeline` function was using a nested loop to find clips in the media pool by name, leading to O(N*M) complexity. This becomes a significant bottleneck as the number of clips in the media pool and the number of clips to be added grow.
**Action:** Always use a hash map (dictionary) to index media pool items when performing multiple lookups by name or path to achieve O(N+M) complexity.
