import time
import os
import sys
from unittest.mock import MagicMock

# Mocking GUI dependencies to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()
sys.modules['pygetwindow'] = MagicMock()

# Mocking Resolve API
class MockClip:
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

def benchmark_add_clips():
    print("Running Clips Benchmark...")
    sys.path.append(os.path.abspath('src'))
    import editor_actions
    import resolve_proxy

    # Mock is_api_available to return True
    resolve_proxy.is_api_available = lambda: True

    # Mock Resolve object and its hierarchy
    mock_resolve = MagicMock()
    mock_project_manager = mock_resolve.GetProjectManager.return_value
    mock_project = mock_project_manager.GetCurrentProject.return_value
    mock_media_pool = mock_project.GetMediaPool.return_value

    editor_actions.get_resolve = lambda: mock_resolve

    # Create a large list of clips in media pool
    num_clips = 20000 # Increased to show bottleneck better
    all_clips = [MockClip(f"clip_{i}.mp4", f"/path/to/clip_{i}.mp4") for i in range(num_clips)]

    # Mock list_clips_in_media_pool
    editor_actions.list_clips_in_media_pool = lambda: all_clips

    # Names to search for (some exist, some don't)
    clip_names_to_add = [f"clip_{i}.mp4" for i in range(0, num_clips, 40)] # 500 clips

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time to add {len(clip_names_to_add)} clips from a pool of {num_clips}: {duration:.4f}s")
    return duration

if __name__ == "__main__":
    benchmark_add_clips()
