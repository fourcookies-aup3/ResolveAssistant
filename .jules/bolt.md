## 2025-05-15 - Hash Map Optimization for Clip Lookups
**Learning:** Replacing O(N*M) nested loops with O(N+M) hash map lookups provides a massive performance boost (50x+) in media-heavy projects.
**Action:** Always look for nested loops where the inner loop is performing a lookup that can be pre-indexed into a dictionary. Ensure 'first-match' behavior is preserved by checking if a key already exists before inserting.
