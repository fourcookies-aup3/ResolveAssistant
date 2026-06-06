import time
import os
import sys

# Mocking resolve_proxy to avoid dependency issues in headless environment
class MockClip:
    def __init__(self, name):
        self.name = name
    def GetName(self):
        return self.name

def benchmark_add_clips():
    # Simulate a large media pool
    pool_size = 5000
    all_clips = [MockClip(f"clip_{i}.mp4") for i in range(pool_size)]

    # Clips we want to add
    clips_to_find = [f"clip_{i}.mp4" for i in range(0, pool_size, 10)] # 500 clips

    print(f"Benchmarking with {pool_size} clips in pool and searching for {len(clips_to_find)} clips.")

    # Current O(N*M) approach
    start_time = time.time()
    clips_to_add = []
    for name in clips_to_find:
        for clip in all_clips:
            if clip.GetName() == name:
                clips_to_add.append(clip)
                break
    end_time = time.time()
    print(f"O(N*M) approach took: {end_time - start_time:.4f} seconds")

    # Proposed O(N+M) approach
    start_time = time.time()
    clips_to_add_optimized = []
    # Build hash map
    clip_map = {clip.GetName(): clip for clip in all_clips}
    for name in clips_to_find:
        if name in clip_map:
            clips_to_add_optimized.append(clip_map[name])
    end_time = time.time()
    print(f"O(N+M) approach took: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
