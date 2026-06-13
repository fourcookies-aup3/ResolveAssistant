import time
import os
import sys

# Mocking modules for headless environment
from unittest.mock import MagicMock

# Mock GUI modules to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Ensure src is in PYTHONPATH
sys.path.append(os.path.abspath("src"))

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve, MockMediaPoolItem

def run_benchmark():
    print("Starting benchmark for add_clips_to_timeline...")

    # Setup mock environment
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    mp = project.GetMediaPool()

    # Create a large number of clips in the media pool
    num_pool_clips = 10000
    pool_clips = []
    for i in range(num_pool_clips):
        clip = MockMediaPoolItem(f"/path/to/clip_{i}.mp4")
        pool_clips.append(clip)

    mp.GetRootFolder().clips = pool_clips

    # List of clip names to add
    num_target_clips = 5000
    target_names = [f"clip_{i}.mp4" for i in range(num_target_clips)]

    # Measure time
    start_time = time.time()
    add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken to add {num_target_clips} clips from a pool of {num_pool_clips}: {duration:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
