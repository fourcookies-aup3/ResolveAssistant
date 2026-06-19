## 2025-05-14 - Optimized Vision Template Matching
**Learning:** Grayscale conversion and template caching drastically reduce overhead in OpenCV-based UI automation. Matching a single-channel grayscale image is significantly faster than a three-channel BGR image, and caching avoids redundant disk I/O for frequently used UI elements.
**Action:** Always prefer grayscale matching and implement a template cache when performing repeated visual searches for static UI elements.
