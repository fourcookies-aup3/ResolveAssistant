import time
import os
import sys

# Mocking the environment
from unittest.mock import MagicMock
sys.modules['resolve_proxy'] = MagicMock()
sys.modules['vision'] = MagicMock()
sys.modules['input_control'] = MagicMock()

# Mock clip object
class MockClip:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

def benchmark_clips():
    # Setup mock data for a larger scale
    num_all_clips = 10000
    num_clips_to_add = 1000

    all_clips = [MockClip(f"clip_{i}.mp4", f"/path/to/clip_{i}.mp4") for i in range(num_all_clips)]
    clip_names_to_find = [f"clip_{j}.mp4" for j in range(0, num_clips_to_add)]

    # Current implementation logic
    start_time = time.time()

    clips_to_add = []
    for name in clip_names_to_find:
        for clip in all_clips:
            if clip.GetName() == name or (hasattr(clip, 'path') and os.path.basename(clip.path) == name):
                clips_to_add.append(clip)
                break

    end_time = time.time()
    print(f"Current O(N*M) logic ({num_all_clips} clips, {num_clips_to_add} to add): {end_time - start_time:.6f} seconds")

    # Hash map implementation logic
    start_time = time.time()

    # Pre-index clips
    clip_map = {}
    for clip in all_clips:
        name = clip.GetName()
        if name not in clip_map:
            clip_map[name] = clip
        path = getattr(clip, 'path', None)
        if path:
            base_name = os.path.basename(path)
            if base_name not in clip_map:
                clip_map[base_name] = clip

    clips_to_add_fast = []
    for name in clip_names_to_find:
        if name in clip_map:
            clips_to_add_fast.append(clip_map[name])

    end_time = time.time()
    print(f"Optimized Hash Map logic ({num_all_clips} clips, {num_clips_to_add} to add): {end_time - start_time:.6f} seconds")

    assert len(clips_to_add) == len(clips_to_add_fast)

if __name__ == "__main__":
    benchmark_clips()
