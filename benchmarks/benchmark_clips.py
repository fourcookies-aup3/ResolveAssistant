import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['pynput'] = MagicMock()

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import editor_actions
import resolve_proxy

def benchmark_add_clips():
    print("Benchmarking add_clips_to_timeline...")

    # Setup mock clips
    num_clips = 1000
    clip_names = [f"clip_{i}.mp4" for i in range(num_clips)]

    # Configure mock resolve
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    ms = resolve.GetMediaStorage()

    # Pre-populate media pool
    ms.AddItemListToMediaPool(clip_names)

    # We want to add 500 of these clips to the timeline
    to_add = [f"clip_{i}.mp4" for i in range(0, 1000, 2)]

    start_time = time.time()
    editor_actions.add_clips_to_timeline(to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken to add {len(to_add)} clips out of {num_clips} total: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    benchmark_add_clips()
