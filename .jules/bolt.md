## 2025-05-15 - [O(N*M) Bottleneck in Clip Lookup]
**Learning:** The original `add_clips_to_timeline` implementation used a nested loop to match requested clip names against the media pool, resulting in O(N*M) complexity. This becomes a severe bottleneck in projects with thousands of clips (e.g., 10,000 clips taking ~68s).
**Action:** Use a hash map (dictionary) to index the media pool clips by name and path basename. This reduces lookup time to O(1) per clip, bringing total complexity to O(N+M). Ensure "first-wins" behavior by only adding to the dictionary if the key is not already present.

## 2025-05-15 - [Test Mocking and sys.modules]
**Learning:** Running multiple test suites in the same process can cause failures if they all mock `sys.modules['pyautogui']` differently, as the first mock might persist.
**Action:** Run tests individually or ensure mocks are properly reset/managed if executing in a single session. In this environment, `python3 -m pytest tests/test_filename.py` is safer.
