## 2025-05-15 - Grayscale Template Matching and Memory Caching
**Learning:** Performing template matching on color images (BGR) is significantly slower than grayscale as it processes three channels instead of one. Additionally, repeated disk I/O for loading templates in a loop is a major bottleneck.
**Action:** Always convert both screen captures and templates to grayscale before matching. Implement a memory cache for templates to avoid redundant disk I/O and pre-process them into grayscale.
