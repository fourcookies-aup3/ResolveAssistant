## 2025-05-15 - Hash Map Optimization for Clip Lookup
**Learning:** In scenarios with large media pools (10k+ clips), $O(N \cdot M)$ nested loops for name/path matching become a significant bottleneck, causing multi-second delays for batch operations.
**Action:** Always prefer dictionary-based lookups ($O(N+M)$) when matching items between two lists in the editor actions layer.
