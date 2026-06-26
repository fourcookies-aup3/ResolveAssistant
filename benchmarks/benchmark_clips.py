import sys
from unittest.mock import MagicMock

# Mock GUI libraries for headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

import os
import time

# Add src to path
sys.path.append(os.path.abspath("src"))

from editor_actions import add_clips_to_timeline
from resolve_proxy import MockMediaPoolItem, get_resolve

def run_benchmark(num_pool_clips=1000, num_targets=100):
    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} clips in pool and {num_targets} targets...")

    # Prepare mock data
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(f"BenchmarkProject_{num_pool_clips}_{num_targets}")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Fill media pool
    pool_clips = []
    for i in range(num_pool_clips):
        clip = MockMediaPoolItem(f"/path/to/clip_{i}.mp4")
        pool_clips.append(clip)
    root_folder.clips = pool_clips

    # Target names to add
    target_names = [f"clip_{i}.mp4" for i in range(0, num_pool_clips, num_pool_clips // num_targets)]

    # Measure
    start_time = time.time()
    add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    # Small test
    run_benchmark(100, 10)

    # Larger test to see the bottleneck
    run_benchmark(5000, 200)
