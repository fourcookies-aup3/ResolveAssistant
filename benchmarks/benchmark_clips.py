import time
import os
import sys
from unittest.mock import MagicMock

# Mock pyautogui and vision before importing editor_actions
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['vision'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath("src"))

# Set environment variables for MockResolve
os.environ["USE_MOCK_RESOLVE"] = "true"

import editor_actions
from resolve_proxy import get_resolve

def benchmark_add_clips_to_timeline(num_clips_in_pool, num_clips_to_add):
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(f"Benchmark_{num_clips_in_pool}")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Fill media pool with many clips
    print(f"Preparing media pool with {num_clips_in_pool} clips...")
    for i in range(num_clips_in_pool):
        clip = MagicMock()
        clip.GetName.return_value = f"clip_{i}.mp4"
        clip.path = f"/path/to/clip_{i}.mp4"
        root_folder.clips.append(clip)

    clip_names_to_add = [f"clip_{i}.mp4" for i in range(num_clips_to_add)]

    print(f"Adding {num_clips_to_add} clips to timeline...")
    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    # Test with 1000 clips in pool and 100 to add
    benchmark_add_clips_to_timeline(1000, 100)
    # Test with 5000 clips in pool and 500 to add
    benchmark_add_clips_to_timeline(5000, 500)
    # Test with 10000 clips in pool and 1000 to add
    benchmark_add_clips_to_timeline(10000, 1000)
