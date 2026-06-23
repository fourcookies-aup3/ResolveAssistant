import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries before they are imported
mock_modules = ['pyautogui', 'cv2', 'PIL', 'PIL.ImageGrab']
for module in mock_modules:
    sys.modules[module] = MagicMock()

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import editor_actions
from resolve_proxy import MockMediaPoolItem, get_resolve

def run_benchmark(num_pool_clips=1000, num_targets=100):
    print(f"\nBenchmarking add_clips_to_timeline with {num_pool_clips} pool clips and {num_targets} targets...")

    # Setup mock data
    all_clips = [MockMediaPoolItem(f"/path/to/clip_{i}.mp4") for i in range(num_pool_clips)]
    target_names = [f"clip_{i}.mp4" for i in range(num_targets)]

    # Mock list_clips_in_media_pool
    original_list_clips = editor_actions.list_clips_in_media_pool
    editor_actions.list_clips_in_media_pool = lambda: all_clips

    # Force API mode
    os.environ["USE_MOCK_RESOLVE"] = "true"
    os.environ["RESOLVE_API_UNAVAILABLE"] = "false"

    # Reset resolve proxy instance to pick up env changes
    import resolve_proxy
    resolve_proxy._resolve_instance = None

    resolve = get_resolve()
    print(f"API Available: {resolve.is_api_available}")

    # Make sure we have a project and timeline
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Test Project")
    project.GetMediaPool().CreateEmptyTimeline("Timeline 1")

    start_time = time.time()
    editor_actions.add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Duration: {duration:.4f} seconds")

    # Restore
    editor_actions.list_clips_in_media_pool = original_list_clips
    return duration

if __name__ == "__main__":
    # Baseline
    run_benchmark(1000, 100)
    run_benchmark(5000, 200)
    run_benchmark(10000, 500)
    run_benchmark(100000, 1000)
