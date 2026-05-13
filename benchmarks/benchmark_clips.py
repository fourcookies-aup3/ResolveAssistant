import sys
from unittest.mock import MagicMock
import os
import time

# Mock GUI libraries for headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
import resolve_proxy

def run_benchmark(num_clips=1000):
    print(f"--- Benchmarking add_clips_to_timeline with {num_clips} clips ---")

    # Setup mock data
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Benchmark Project")

    # Create many clips in media pool
    clip_paths = [f"/path/to/clip_{i}.mp4" for i in range(num_clips)]
    editor_actions.import_media(clip_paths)

    # Clip names to add (all of them)
    clip_names = [f"clip_{i}.mp4" for i in range(num_clips)]

    # Measure time
    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    run_benchmark(1000)
