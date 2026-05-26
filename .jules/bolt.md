## 2025-05-26 - Vision Template Caching
**Learning:** Template matching in `src/vision.py` was re-reading the template image from disk on every single call. While `cv2.matchTemplate` is the dominant CPU bottleneck, redundant disk I/O adds unnecessary latency and OS overhead, especially in tight automation loops.
**Action:** Implement module-level dictionary caching for templates. This reduced template acquisition time from ~85μs to effectively zero. Always check for redundant I/O in frequently called vision/looping functions.
