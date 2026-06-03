import os
import sys
import time
import random
import string
from unittest.mock import MagicMock

# Mocking GUI and Resolve API before importing src
os.environ["USE_MOCK_RESOLVE"] = "true"
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['pynput'] = MagicMock()

sys.path.append(os.path.join(os.getcwd(), 'src'))

import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run_benchmark():
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("BenchmarkProject")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Setup: 10000 clips in media pool
    num_pool_clips = 10000
    pool_clip_names = [f"clip_{i}.mp4" for i in range(num_pool_clips)]
    pool_clips = [MockMediaPoolItem(name) for name in pool_clip_names]
    root_folder.clips.extend(pool_clips)

    # Clips to add: 2000 random clips from the pool
    num_to_add = 2000
    clip_names_to_add = random.sample(pool_clip_names, num_to_add)

    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} clips in pool and {num_to_add} clips to add...")

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    run_benchmark()
