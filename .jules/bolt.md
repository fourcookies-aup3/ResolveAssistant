## 2026-05-28 - Grayscale Template Matching Speedup
**Learning:** Grayscale template matching with `cv2.matchTemplate` is significantly faster (approx. 12-15x) than multi-channel BGR matching on 1080p screens. Template caching also eliminates redundant disk I/O.
**Action:** Use grayscale conversion for both screen and template images when color information is not critical for identification. Implement module-level caching for frequently used assets.
