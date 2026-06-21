import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI dependencies that fail in headless
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui
sys.modules["cv2"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["vision"] = MagicMock()

# Now import our modules
sys.path.append('src')
import resolve_proxy
import editor_actions

def run_benchmark():
    # Prepare mock clips
    num_pool_clips = 100000
    num_targets = 1000

    mock_clips = []
    for i in range(num_pool_clips):
        clip = resolve_proxy.MockMediaPoolItem(f"/path/to/clip_{i}.mp4")
        mock_clips.append(clip)

    # Inject mock clips into the mock resolve environment
    resolve = resolve_proxy.get_resolve()
    resolve.GetProjectManager().CreateProject("BenchProject")
    project = resolve.GetProjectManager().GetCurrentProject()
    project.GetMediaPool().GetRootFolder().clips = mock_clips

    target_names = [f"clip_{i}.mp4" for i in range(0, num_targets)]

    print(f"Benchmarking add_clips_to_timeline with {num_pool_clips} pool clips and {num_targets} targets...")

    # Measure time for add_clips_to_timeline
    start_time = time.time()
    editor_actions.add_clips_to_timeline(target_names)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")

if __name__ == "__main__":
    os.environ["USE_MOCK_RESOLVE"] = "true"
    run_benchmark()
