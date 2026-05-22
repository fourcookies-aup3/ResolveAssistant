import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI dependencies before they are imported
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()

# Mocking and setup
sys.path.append('src')
os.environ['USE_MOCK_RESOLVE'] = 'true'
import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

def benchmark_add_clips(num_pool_clips, num_to_add):
    # Clear previous project/state if necessary
    import resolve_proxy
    resolve_proxy._resolve_instance = None

    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(f"Benchmark Project {num_pool_clips}")
    mp = project.GetMediaPool()
    root = mp.GetRootFolder()

    # Pre-populate media pool
    print(f"Populating pool with {num_pool_clips} clips...")
    for i in range(num_pool_clips):
        name = f"clip_{i}.mp4"
        clip = MockMediaPoolItem(f"/path/to/{name}")
        root.clips.append(clip)

    clip_names = [f"clip_{i}.mp4" for i in range(0, num_pool_clips, num_pool_clips // num_to_add)][:num_to_add]

    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} clips in pool and adding {len(clip_names)} clips.")

    start = time.perf_counter()
    editor_actions.add_clips_to_timeline(clip_names)
    end = time.perf_counter()

    duration = end - start
    print(f"Duration: {duration:.6f} seconds")
    return duration

if __name__ == "__main__":
    benchmark_add_clips(1000, 100)
    benchmark_add_clips(10000, 100)
    benchmark_add_clips(20000, 100)
