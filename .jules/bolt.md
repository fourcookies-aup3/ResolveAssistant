# Bolt's Performance Journal - Critical Learnings Only

## 2025-02-15 - [Timeline Clip Hash Map Optimization]
**Learning:** Replacing an $O(N \times M)$ nested loop clip lookup in `add_clips_to_timeline` with a dictionary mapping of name/basename to clip object yields a massive 101.1x speedup (down to ~0.012s from ~1.25s for 10k clips and 500 target names). To preserve the crucial 'first-match' behavior of the original loop, the media pool clips list can be iterated in reverse order when building the hash map, so that the first occurrence in the original list overwrites any subsequent duplicates and remains as the final entry in the dictionary.
**Action:** Always map list items by their unique identifier/name when performing multi-item lookups, and use reversed traversal of lists when creating dictionary lookups if first-match/earliest-match ordering needs to be preserved.
