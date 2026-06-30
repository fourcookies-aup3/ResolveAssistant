## 2026-06-30 - Vision Matching Optimization
**Learning:** Grayscale conversion and template caching significantly reduce vision processing latency. Grayscale reduces the data size for cv2.matchTemplate, while caching avoids repeated disk I/O for the same templates. In this environment, it reduced latency from ~0.96s to ~0.08s per call.
**Action:** Always prefer grayscale for UI element matching when color isn't a distinguishing factor, and implement caching for frequently used template assets.
