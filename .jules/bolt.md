# Bolt Journal - Critical Learnings

## 2025-05-15 - [Clip Lookup Optimization]
**Learning:** Nested loops $O(N \times M)$ for matching targets against a large media pool (10k+ clips) caused significant latency (~3.5s). Using a hash map (dictionary) for lookup reduces this to $O(N+M)$, achieving ~100x speedup.
**Action:** Always prefer hash map lookups for matching names/paths in large collections.

## 2025-05-15 - [Vision Performance]
**Learning:** `cv2.matchTemplate` is substantially faster (approx. 4x in this environment) when processing single-channel grayscale images compared to 3-channel BGR. Additionally, redundant disk I/O from reloading templates on every call is a major bottleneck.
**Action:** Implement memory caching for templates and convert both screen and templates to grayscale before matching.

## 2025-05-15 - [Mock Pollution in Headless Tests]
**Learning:** Running multiple tests that mock global `sys.modules` (like `pyautogui` or `cv2`) in a single process can lead to state pollution and assertion failures.
**Action:** Isolate tests by running them individually or ensure thorough state reset between test cases.
