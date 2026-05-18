import sys
import os
import time
from unittest.mock import MagicMock

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions

def benchmark_add_clips(num_pool_clips, num_requested_clips):
    # Reset singleton for each run
    resolve_proxy._resolve_instance = None

    # Setup mock environment
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(f"Benchmark Project {num_pool_clips}")
    mp = project.GetMediaPool()

    # Fill media pool with many clips
    pool_clips = []
    for i in range(num_pool_clips):
        path = f"/path/to/clip_{i}.mp4"
        clip = resolve_proxy.MockMediaPoolItem(path)
        pool_clips.append(clip)

    # Manually add to mock folder
    mp.GetRootFolder().clips = pool_clips

    # Clips we want to add
    requested_names = [f"clip_{i}.mp4" for i in range(num_requested_clips)]

    start_time = time.time()
    editor_actions.add_clips_to_timeline(requested_names)
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":
    print("Running benchmark...")
    # Small scale
    duration = benchmark_add_clips(100, 100)
    print(f"100 pool clips, 100 requested: {duration:.4f}s")

    # Larger scale
    duration = benchmark_add_clips(1000, 1000)
    print(f"1000 pool clips, 1000 requested: {duration:.4f}s")

    # Even larger scale
    duration = benchmark_add_clips(5000, 5000)
    print(f"5000 pool clips, 5000 requested: {duration:.4f}s")

    # Very large scale to see the O(N*M) impact
    duration = benchmark_add_clips(10000, 10000)
    print(f"10000 pool clips, 10000 requested: {duration:.4f}s")
