## 2025-05-15 - Hash Map Optimization for Clip Addition
**Learning:** The previous implementation used a nested loop (O(N*M)) to match requested clip names against the media pool. In DaVinci Resolve projects with large media pools (e.g., 20,000+ clips), this caused a significant bottleneck, taking seconds for even a few hundred additions.
**Action:** Always prefer indexing large collection lists into a hash map (dictionary) before performing multiple lookups. Ensure "first-match" behavior is preserved by checking for key existence before insertion if the source list has a meaningful order.
