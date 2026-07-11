## 2025-05-14 - [Hash Map Optimization for Clip Lookups]
**Learning:** Replacing an (N \times M)$ nested loop with an (N+M)$ hash map lookup in `add_clips_to_timeline` yielded an ~83x speedup (from 1.83s to 0.022s for 10,000 clips). Preservation of "first-match" behavior is achieved by iterating the source list in reverse when populating the dictionary.

**Action:** Always check for nested loops in collection lookups and consider hash maps. Use `reversed()` when building lookups if first-occurrence priority must be maintained.

## 2025-05-14 - [Test Isolation with sys.modules Mocking]
**Learning:** Mocking GUI-dependent libraries via `sys.modules` in a headless environment can cause global state pollution between test files, leading to intermittent failures if tests are run in the same process.

**Action:** Run tests individually or ensure a complete state reset between test suites when using aggressive `sys.modules` mocking.
