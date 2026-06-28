## 2026-06-28 - Optimized Media Pool Clip Lookup
**Learning:** Nested loops for matching media pool items by name/path scale poorly ($O(N \times M)$). Large projects with thousands of clips experience noticeable lag during timeline assembly.
**Action:** Always use hash map indexing ($O(N+M)$) when looking up clips in the Media Pool, even if the initial pool size seems small.
