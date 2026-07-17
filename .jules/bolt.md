## 2025-02-15 - Grayscale conversion and memory caching for cv2 template matching
**Learning:** Performing cv2.matchTemplate on full color (RGB/BGR) screens with repeated disk I/O introduces a massive overhead (~0.23s per call). Converting templates and screen captures to grayscale reduces channel processing by 3x and using in-memory caches avoids redundant disk reads, delivering a ~4x speedup on template search latency (~0.06s).
**Action:** Always implement a module-level template cache and grayscale conversion for computer-vision template searches.

## 2025-02-15 - Hash map lookup for large collections of media pool clips
**Learning:** Searching through a large number of clips (e.g., 10,000 in media pool) using nested loops to match target files introduces an O(N * M) performance bottleneck (taking ~0.23s for 500 targets). Replacing this with an O(N + M) pre-built dictionary lookup cuts lookup time to ~0.017s (~13x speedup).
**Action:** When mapping elements from list structures to a set of targets, pre-build a lookup table (dictionary/hash map) instead of performing nested loops.
