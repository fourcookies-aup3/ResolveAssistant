
## 2026-06-21 - O(N+M) lookup for adding clips to timeline
**Learning:** Found a nested loop in `add_clips_to_timeline` that scaled poorly (O(N*M)) with large media pools and multiple target clips. Using a hash map (Python dict) to pre-index the media pool reduced lookup to O(1) per clip.
**Action:** Always check for linear searches inside loops when dealing with collections like media pool clips or project lists. Pre-indexing into a dictionary is a standard Bolt optimization for this codebase.
