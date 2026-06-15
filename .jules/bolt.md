## 2025-05-15 - [Vision: Grayscale Template Matching and Caching]
**Learning:** Grayscale conversion of both screen and template images in `src/vision.py` significantly improves `cv2.matchTemplate` performance (e.g., from ~1.2s to ~0.08s for a 1080p screen) by reducing channel processing. Implementing a module-level template cache avoids redundant disk I/O.
**Action:** Always prefer grayscale matching for UI elements unless color is a critical differentiator. Use caching for static assets like UI templates to eliminate repeated I/O.
