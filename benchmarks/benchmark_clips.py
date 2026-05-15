import time
import sys
import os
from unittest.mock import MagicMock

# Mock GUI libraries for headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions

def benchmark_add_clips():
    # Setup mock clips
    num_clips = 1000
    clip_names = [f"clip_{i}.mp4" for i in range(num_clips)]

    # We need to populate the mock media pool
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    ms = resolve.GetMediaStorage()

    # Pre-populate media pool
    full_paths = [f"/path/to/clip_{i}.mp4" for i in range(num_clips)]
    ms.AddItemListToMediaPool(full_paths)

    # Measure add_clips_to_timeline
    start_time = time.perf_counter()
    editor_actions.add_clips_to_timeline(clip_names)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Time taken to add {num_clips} clips: {duration:.6f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
