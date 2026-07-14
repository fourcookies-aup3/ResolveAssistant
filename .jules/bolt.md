## 2025-05-15 - Grayscale template matching and memory caching
**Learning:** Grayscale conversion of both screen and template images significantly improves `cv2.matchTemplate` performance by reducing channel processing. Module-level caching for templates avoids redundant disk I/O, which is a common bottleneck in UI automation.
**Action:** Always prefer grayscale matching for UI elements that don't rely on color for identification. Implement memory caching for frequently used assets.
