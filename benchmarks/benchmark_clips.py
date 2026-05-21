import sys
import os
import time
from unittest.mock import MagicMock

# Mock Resolve API
sys.modules['DaVinciResolveScript'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions

def benchmark_add_clips():
    # Setup mock environment
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    mp = project.GetMediaPool()

    # Create a large number of clips in the media pool
    num_pool_clips = 10000
    pool_paths = [f"/path/to/clip_{i}.mp4" for i in range(num_pool_clips)]
    resolve.GetMediaStorage().AddItemListToMediaPool(pool_paths)

    # Clips to add to timeline
    num_clips_to_add = 1000
    clip_names_to_add = [f"clip_{i}.mp4" for i in range(0, num_pool_clips, num_pool_clips // num_clips_to_add)]

    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} clips in pool and {len(clip_names_to_add)} to add...")

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Duration: {duration:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
