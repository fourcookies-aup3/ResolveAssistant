## 2025-05-15 - Hash Map Optimization for Media Pool Clip Matching
**Learning:** In scenarios involving matching a list of items (M) against a large collection (N), the default nested loop approach O(N*M) becomes a significant bottleneck as the collection grows. Using a hash map to pre-index the collection reduces complexity to O(N+M).
**Action:** Always check for nested loops in data matching tasks, especially when dealing with potentially large collections like media pools or file lists, and consider pre-indexing with dictionaries.
