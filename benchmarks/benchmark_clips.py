import sys
from unittest.mock import MagicMock

# Mock GUI libraries before they are imported
mock_pyautogui = MagicMock()
mock_cv2 = MagicMock()
mock_pil = MagicMock()

sys.modules["pyautogui"] = mock_pyautogui
sys.modules["cv2"] = mock_cv2
sys.modules["PIL"] = mock_pil
sys.modules["PIL.ImageGrab"] = MagicMock()

import time
import os

# Setup path to include src
sys.path.append(os.path.join(os.getcwd(), 'src'))

from editor_actions import add_clips_to_timeline
from resolve_proxy import MockMediaPoolItem, get_resolve

def run_benchmark(num_pool_clips=10000, num_targets=500):
    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} pool clips and {num_targets} targets...")

    # Setup mock data
    resolve = get_resolve()
    # Reset instance to avoid accumulation if called multiple times
    import resolve_proxy
    resolve_proxy._resolve_instance = None
    resolve = get_resolve()

    project = resolve.GetProjectManager().CreateProject("BenchmarkProject")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Add many clips to the pool
    all_clips = []
    for i in range(num_pool_clips):
        clip = MockMediaPoolItem(f"/path/to/clip_{i}.mp4")
        all_clips.append(clip)
    root_folder.clips = all_clips

    # Targets to find
    target_names = [f"clip_{i}.mp4" for i in range(0, num_targets)]

    # Measure
    start_time = time.perf_counter()
    add_clips_to_timeline(target_names)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    os.environ["USE_MOCK_RESOLVE"] = "true"
    run_benchmark()
