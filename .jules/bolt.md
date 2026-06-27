## 2025-05-15 - [O(N*M) lookup in Media Pool]
**Learning:** Using nested loops for clip lookups in `add_clips_to_timeline` creates a significant bottleneck ($O(N \cdot M)$) as the Media Pool grows. In professional editing, media pools can easily contain thousands of clips.
**Action:** Always prefer hash map (dictionary) lookups for media pool operations. Use `reversed()` iteration when building the map to preserve the "first match" behavior expected by the original implementation.
