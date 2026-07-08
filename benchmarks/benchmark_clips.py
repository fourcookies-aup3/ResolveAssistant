import sys
import os
import time
import statistics
from unittest.mock import MagicMock

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()
sys.modules['pyscreeze'] = MagicMock()
sys.modules['pygetwindow'] = MagicMock()

# Mock resolve_proxy
mock_resolve = MagicMock()
sys.modules['resolve_proxy'] = MagicMock()
import resolve_proxy
resolve_proxy.is_api_available.return_value = True
resolve_proxy.get_resolve.return_value = mock_resolve

sys.path.append('src')
import editor_actions

class MockClip:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

def run_benchmark(num_pool_clips=1000, num_target_clips=100):
    pool_clips = [MockClip(f"clip_{i}.mp4", f"/path/to/clip_{i}.mp4") for i in range(num_pool_clips)]
    target_names = [f"clip_{i}.mp4" for i in range(num_target_clips)]

    editor_actions.list_clips_in_media_pool = MagicMock(return_value=pool_clips)

    project = mock_resolve.GetProjectManager().GetCurrentProject()
    project.GetCurrentTimeline.return_value = MagicMock()
    project.GetMediaPool().AppendToTimeline.return_value = True

    start_time = time.perf_counter()
    editor_actions.add_clips_to_timeline(target_names)
    end_time = time.perf_counter()

    return end_time - start_time

if __name__ == "__main__":
    run_benchmark(100, 10)

    durations = []
    for _ in range(5):
        durations.append(run_benchmark(100000, 1000))

    avg = statistics.mean(durations)
    print(f"Average execution time for 100,000 pool clips and 1,000 target clips: {avg:.6f}s")
