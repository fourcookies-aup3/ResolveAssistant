import sys
from unittest.mock import MagicMock

# Mock GUI libraries
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui

mock_cv2 = MagicMock()
sys.modules["cv2"] = mock_cv2

mock_pil = MagicMock()
sys.modules["PIL"] = mock_pil
sys.modules["PIL.ImageGrab"] = MagicMock()

import time
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

from editor_actions import add_clips_to_timeline
import resolve_proxy

def benchmark_add_clips():
    # Setup mock environment
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    ms = resolve.GetMediaStorage()

    # Create a large number of clips
    num_clips = 1000
    clip_paths = [f"/path/to/clip_{i}.mp4" for i in range(num_clips)]
    ms.AddItemListToMediaPool(clip_paths)

    # Names to search for (all of them)
    clip_names = [f"clip_{i}.mp4" for i in range(num_clips)]

    # Warm up
    add_clips_to_timeline(["clip_0.mp4"])

    start_time = time.time()
    add_clips_to_timeline(clip_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"BENCHMARK_RESULT: {duration:.6f}")
    return duration

if __name__ == "__main__":
    benchmark_add_clips()
