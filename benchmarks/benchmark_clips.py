import sys
from unittest.mock import MagicMock

# Mock GUI dependencies before importing src
sys.modules["pyautogui"] = MagicMock()
sys.modules["cv2"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.ImageGrab"] = MagicMock()

import os
import time

# Add src to path
sys.path.append(os.path.abspath("src"))

# Mock Resolve environment
os.environ["USE_MOCK_RESOLVE"] = "true"

from editor_actions import add_clips_to_timeline, get_resolve

def setup_mock_clips(num_clips):
    resolve = get_resolve()
    ms = resolve.GetMediaStorage()
    paths = [f"/path/to/clip_{i}.mov" for i in range(num_clips)]
    ms.AddItemListToMediaPool(paths)
    return [f"clip_{i}.mov" for i in range(num_clips)]

def benchmark_add_clips(num_total, num_to_add):
    # Clear previous clips if any
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("BenchProject")

    clip_names = setup_mock_clips(num_total)
    to_add = clip_names[:num_to_add]

    start_time = time.time()
    add_clips_to_timeline(to_add)
    end_time = time.time()

    print(f"Time to add {num_to_add} clips out of {num_total}: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    benchmark_add_clips(10000, 2000)
