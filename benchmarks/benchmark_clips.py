import time
import os
import sys

# Mock GUI libraries for headless environment
from unittest.mock import MagicMock
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Mock Resolve API
os.environ["USE_MOCK_RESOLVE"] = "true"
sys.path.append('src')

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve

def benchmark_add_clips():
    resolve = get_resolve()
    # Reset mock state if needed
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")

    # Pre-populate media pool
    num_clips = 2000
    paths = [f"clip_{i}.mp4" for i in range(num_clips)]
    resolve.GetMediaStorage().AddItemListToMediaPool(paths)

    # Clips to add to timeline (e.g., search for 1000 clips)
    clips_to_add = [f"clip_{i}.mp4" for i in range(0, num_clips, 2)]

    start_time = time.time()
    add_clips_to_timeline(clips_to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"BENCHMARK_RESULT: {duration:.4f} seconds for {len(clips_to_add)} clips in pool of {num_clips}")

if __name__ == "__main__":
    benchmark_add_clips()
