import time
import os
import sys

# Mocking modules before importing editor_actions
from unittest.mock import MagicMock

# Mock DaVinciResolveScript if it doesn't exist
sys.modules['DaVinciResolveScript'] = MagicMock()
# Mock pyautogui and other GUI libs
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

def benchmark_add_clips_to_timeline(num_clips_in_pool, num_clips_to_add):
    resolve = get_resolve()
    # Reset mock state if needed
    resolve.project_manager.projects = {}

    project = resolve.GetProjectManager().CreateProject(f"Benchmark Project {num_clips_in_pool}")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Pre-populate media pool
    clips = [MockMediaPoolItem(f"path/to/clip_{i}.mp4") for i in range(num_clips_in_pool)]
    root_folder.clips.extend(clips)

    clip_names_to_add = [f"clip_{i}.mp4" for i in range(num_clips_to_add)]

    start_time = time.perf_counter()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.perf_counter()

    return end_time - start_time

if __name__ == "__main__":
    # Test with 1000 clips in pool and adding 1000 clips
    duration = benchmark_add_clips_to_timeline(1000, 1000)
    print(f"Time to add 1000 clips with 1000 clips in pool: {duration:.4f} seconds")

    # Test with 5000 clips in pool and adding 5000 clips
    duration = benchmark_add_clips_to_timeline(5000, 5000)
    print(f"Time to add 5000 clips with 5000 clips in pool: {duration:.4f} seconds")

    # Test with 10000 clips in pool and adding 10000 clips
    duration = benchmark_add_clips_to_timeline(10000, 10000)
    print(f"Time to add 10000 clips with 10000 clips in pool: {duration:.4f} seconds")
