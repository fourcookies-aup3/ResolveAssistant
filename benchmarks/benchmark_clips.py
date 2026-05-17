import sys
import os
import time
from unittest.mock import MagicMock

# Mock GUI libraries BEFORE importing editor_actions
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
from editor_actions import add_clips_to_timeline

def benchmark():
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    ms = resolve.GetMediaStorage()

    # Create 5000 mock clips
    num_total_clips = 5000
    clip_paths = [f"path/to/clip_{i}.mp4" for i in range(num_total_clips)]
    ms.AddItemListToMediaPool(clip_paths)

    # Clip names to add
    num_to_add = 500
    clip_names_to_add = [f"clip_{i}.mp4" for i in range(num_total_clips - num_to_add, num_total_clips)]

    start_time = time.time()
    add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    print(f"Time taken to add {num_to_add} clips out of {num_total_clips}: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark()
