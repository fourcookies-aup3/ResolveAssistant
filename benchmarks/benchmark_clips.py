import time
import os
import sys
from unittest.mock import MagicMock

# Mocking modules for headless environment
mock_cv2 = MagicMock()
mock_numpy = MagicMock()
mock_pil = MagicMock()
mock_pyautogui = MagicMock()

sys.modules["cv2"] = mock_cv2
sys.modules["numpy"] = mock_numpy
sys.modules["PIL"] = mock_pil
sys.modules["PIL.ImageGrab"] = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve

def benchmark_add_clips(num_pool_items=10000, num_targets=500):
    resolve = get_resolve()
    # Reset project/media pool if necessary, but MockResolve creates fresh ones
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(f"Benchmark Project {num_pool_items}")

    # Fill media pool with many items
    pool_paths = [f"path/to/clip_{i}.mp4" for i in range(num_pool_items)]
    resolve.GetMediaStorage().AddItemListToMediaPool(pool_paths)

    target_names = [f"clip_{i}.mp4" for i in range(num_targets)]

    start_time = time.time()
    add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time to add {num_targets} clips from pool of {num_pool_items}: {duration:.4f}s")
    return duration

if __name__ == "__main__":
    benchmark_add_clips(10000, 500)
