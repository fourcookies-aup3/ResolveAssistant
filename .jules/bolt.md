## 2026-06-29 - O(N+M) Clip Lookup Optimization
**Learning:** Replacing nested loops with hash map lookups in media pool operations provides massive speedups (~136x in benchmarks). To maintain original "first-match" behavior when using a dictionary, iterating through the source list in reverse ensures the first occurrence takes final precedence in the map.
**Action:** Always consider the order of iteration when converting linear searches to hash maps to preserve deterministic behavior.
