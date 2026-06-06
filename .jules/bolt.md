## 2025-05-15 - Optimize Vision Matching with Grayscale and Caching
**Learning:** Grayscale conversion of screen captures and template images, combined with module-level caching of loaded templates, reduces `cv2.matchTemplate` execution time from ~2.0s to ~0.1s on a 1080p screen. This is a critical speedup for UI automation tasks that rely on visual feedback.
**Action:** Always prefer grayscale matching for UI elements unless color is the primary distinguishing feature. Implement caching for frequently accessed static assets like UI templates.
