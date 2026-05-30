## 2025-05-14 - Initial UI Vision Assessment
**Learning:** The `find_image_on_screen` function in `src/vision.py` performs redundant disk I/O by reading templates on every call and performs template matching on 3-channel BGR images, which is significantly slower than grayscale matching.
**Action:** Implement template caching and grayscale conversion to reduce overhead and improve matching speed.
