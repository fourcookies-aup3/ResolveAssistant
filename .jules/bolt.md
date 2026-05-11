## 2025-05-15 - Hash map optimization for clip lookup
**Learning:** Nested loops in media management functions can cause significant lag in projects with thousands of clips. Pre-indexing assets into a dictionary reduces lookup time from O(N*M) to O(N+M).
**Action:** Always consider using hash maps when searching for multiple items in a large list, especially for media assets or UI elements.
