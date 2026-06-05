## 2025-05-15 - Optimizing Media Pool Lookup in DaVinci Resolve API
**Learning:** Linear search in a large media pool ($O(N \times M)$) becomes a major bottleneck as the project grows. While acceptable for a few dozen clips, it scales poorly, taking ~26 seconds for 10,000 clips. Using a hash map ($O(N + M)$) reduces this to < 0.4 seconds.
**Action:** Always use hash maps/dictionaries for lookups when dealing with potentially large lists returned from the DaVinci Resolve API (e.g., Media Pool clips, timelines, or markers) instead of nested loops.
