import time
import os
import sys

# Mocking for headless environment
from unittest.mock import MagicMock
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve, MockMediaPoolItem

def benchmark_add_clips(num_pool_clips=10000, num_targets=500):
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    mp = project.GetMediaPool()
    root = mp.GetRootFolder()

    # Fill media pool
    pool_clips = []
    for i in range(num_pool_clips):
        clip = MockMediaPoolItem(f"path/to/clip_{i}.mp4")
        pool_clips.append(clip)
    root.clips = pool_clips

    # Targets to add
    target_names = [f"clip_{i}.mp4" for i in range(0, num_pool_clips, num_pool_clips // num_targets)]

    start_time = time.time()
    add_clips_to_timeline(target_names)
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":
    print("Running benchmark for add_clips_to_timeline...")
    duration = benchmark_add_clips()
    print(f"Time taken for 10,000 clips in pool and 500 targets: {duration:.4f}s")
