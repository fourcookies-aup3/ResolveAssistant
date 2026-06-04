import sys
import os
import time
from unittest.mock import MagicMock

# Mock pyautogui before importing anything else
sys.modules['pyautogui'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath('src'))

# Mock resolve_proxy before importing editor_actions
os.environ["USE_MOCK_RESOLVE"] = "true"
import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

def run_benchmark(num_clips_in_pool=1000, num_clips_to_add=500):
    resolve = get_resolve()
    project = resolve.GetProjectManager().CreateProject(f"Benchmark Project {num_clips_in_pool}")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Fill media pool
    pool_clips = []
    for i in range(num_clips_in_pool):
        clip = MockMediaPoolItem(f"clip_{i}.mp4")
        pool_clips.append(clip)
    root_folder.clips = pool_clips

    # Clip names to add
    clip_names_to_add = [f"clip_{i}.mp4" for i in range(num_clips_to_add)]

    print(f"Benchmarking add_clips_to_timeline with {num_clips_in_pool} clips in pool and {num_clips_to_add} to add...")

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Duration: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    # Warm up
    run_benchmark(100, 50)
    # Real test
    run_benchmark(10000, 2000)
