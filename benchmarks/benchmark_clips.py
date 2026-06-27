import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI dependencies
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['pynput'] = MagicMock()

# Ensure src is in the path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from editor_actions import add_clips_to_timeline
from resolve_proxy import MockMediaPoolItem, get_resolve

def benchmark_add_clips():
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Setup: 10000 clips in media pool
    num_pool_clips = 10000
    pool_clips = [MockMediaPoolItem(f"clip_{i}.mp4") for i in range(num_pool_clips)]
    root_folder.clips.extend(pool_clips)

    # Targets: 500 clips to add
    num_targets = 500
    target_names = [f"clip_{i}.mp4" for i in range(0, num_targets * 10, 10)]

    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} pool clips and {num_targets} targets...")

    start_time = time.perf_counter()
    add_clips_to_timeline(target_names)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Duration: {duration:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
