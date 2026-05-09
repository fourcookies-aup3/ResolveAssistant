## 2025-05-15 - [RPC-bound Loop Optimization]
**Learning:** In the DaVinci Resolve API, calls like `clip.GetName()` are likely RPC-based and can be significantly slower than local property access. Using these calls inside nested loops (O(N*M)) causes exponential slowdown as project size grows. Pre-indexing the media pool into a dictionary (O(N+M)) is essential for any bulk media operation.
**Action:** Always prefer indexing large collections (like the Media Pool) into a hash map before performing multi-item searches or matches.
