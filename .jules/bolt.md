## 2025-05-15 - [Vision optimization with grayscale and caching]
**Learning:** Grayscale conversion of both screen and template images in 'src/vision.py' significantly improves 'cv2.matchTemplate' performance by reducing channel processing. Combining this with a module-level template cache avoids redundant disk I/O.
**Action:** Use grayscale for template matching whenever color-specific detail is not critical for identification. Always cache templates when multiple lookups are expected.

## 2025-05-15 - [Test isolation in GUI-dependent systems]
**Learning:** Running tests in headless environments often requires mocking GUI-dependent libraries ('pyautogui', 'cv2', 'PIL.ImageGrab'). Global mocking via `sys.modules` can cause mock pollution between test cases if they are run in the same process, leading to intermittent assertion failures.
**Action:** Run tests individually or ensure complete state reset between tests when using extensive `sys.modules` mocking.
