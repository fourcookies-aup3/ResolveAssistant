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

def benchmark_add_clips_to_timeline(num_pool_clips=1000, num_targets=500):
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    ms = resolve.GetMediaStorage()

    # Create a large number of clips in the media pool
    clip_paths = [f"/path/to/clip_{i}.mp4" for i in range(num_pool_clips)]
    ms.AddItemListToMediaPool(clip_paths)

    # Names we want to add to timeline
    target_names = [f"clip_{i}.mp4" for i in range(num_targets)]

    start_time = time.time()
    editor_actions.add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken to add {num_targets} clips from a pool of {num_pool_clips}: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    benchmark_add_clips_to_timeline(10000, 5000)
