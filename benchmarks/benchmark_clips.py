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

import editor_actions
import resolve_proxy

def run_benchmark(num_pool_clips=10000, num_target_clips=5000):
    # Setup mock environment
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()

    # Reset mock state for clean benchmark
    resolve_proxy._resolve_instance = None
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()

    project = pm.CreateProject("BenchmarkProject")

    # Pre-populate media pool
    ms = resolve.GetMediaStorage()
    paths = [f"clip_{i}.mp4" for i in range(num_pool_clips)]
    ms.AddItemListToMediaPool(paths)

    target_names = [f"clip_{i}.mp4" for i in range(num_target_clips)]

    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} clips in pool and {num_target_clips} targets...")

    start_time = time.time()
    editor_actions.add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Duration: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    run_benchmark(10000, 5000)
