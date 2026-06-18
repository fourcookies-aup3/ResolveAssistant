import time
import sys
import os
from unittest.mock import MagicMock

# Mock GUI modules before importing any src modules
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class MockClip:
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

def benchmark_add_clips_to_timeline():
    # Setup
    num_pool_clips = 5000
    num_targets = 200

    all_clips = [MockClip(f"clip_{i}", f"/path/to/clip_{i}.mp4") for i in range(num_pool_clips)]
    clip_names = [f"clip_{i}" for i in range(num_pool_clips - num_targets, num_pool_clips)]

    import editor_actions
    editor_actions.list_clips_in_media_pool = lambda: all_clips
    editor_actions.is_api_available = lambda: True

    mock_resolve = MagicMock()
    editor_actions.get_resolve = lambda: mock_resolve

    mock_pm = mock_resolve.GetProjectManager()
    mock_project = mock_pm.GetCurrentProject()
    mock_timeline = mock_project.GetCurrentTimeline()
    mock_mp = mock_project.GetMediaPool()

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names)
    end_time = time.time()

    print(f"Time taken for {num_targets} clips in {num_pool_clips} pool: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_add_clips_to_timeline()
