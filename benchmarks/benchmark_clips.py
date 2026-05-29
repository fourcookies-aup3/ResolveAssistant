import sys
import os
import time
from unittest.mock import MagicMock

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
import resolve_proxy

def benchmark_add_clips():
    print("Benchmarking add_clips_to_timeline...")

    # Setup mock with many clips
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    mp = project.GetMediaPool()
    root = mp.GetRootFolder()

    num_total_clips = 5000
    num_to_add = 2500
    print(f"Generating {num_total_clips} mock clips...")
    for i in range(num_total_clips):
        root.clips.append(resolve_proxy.MockMediaPoolItem(f"clip_{i}.mp4"))

    clips_to_find = [f"clip_{i}.mp4" for i in range(0, num_to_add)]

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clips_to_find)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken to add {len(clips_to_find)} clips out of {num_total_clips}: {duration:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
