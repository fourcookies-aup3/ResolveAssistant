import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI modules before importing src modules
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath("src"))

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve, MockMediaPoolItem

def benchmark_add_clips():
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Simulate a large media pool
    pool_size = 10000
    target_count = 500

    print(f"Generating {pool_size} clips in media pool...")
    for i in range(pool_size):
        root_folder.clips.append(MockMediaPoolItem(f"clip_{i}.mp4"))

    target_clip_names = [f"clip_{i}.mp4" for i in range(0, pool_size, pool_size // target_count)]

    print(f"Benchmarking adding {len(target_clip_names)} clips to timeline...")
    start_time = time.time()
    add_clips_to_timeline(target_clip_names)
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
