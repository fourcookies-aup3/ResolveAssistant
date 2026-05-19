import time
import sys
import os
from unittest.mock import MagicMock
import numpy as np

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions

class MockClip:
    def __init__(self, name):
        self.name = name
    def GetName(self):
        return self.name

def benchmark_add_clips(num_clips=1000):
    # Setup
    all_clips = [MockClip(f"clip_{i}") for i in range(num_clips)]
    clip_names_to_add = [f"clip_{i}" for i in range(num_clips)]

    # Mock the necessary parts of editor_actions/resolve_proxy
    import editor_actions
    editor_actions.is_api_available = lambda: True

    mock_resolve = MagicMock()
    mock_project = MagicMock()
    mock_timeline = MagicMock()
    mock_media_pool = MagicMock()

    editor_actions.get_resolve = lambda: mock_resolve
    mock_resolve.GetProjectManager().GetCurrentProject.return_value = mock_project
    mock_project.GetCurrentTimeline.return_value = mock_timeline
    mock_project.GetMediaPool.return_value = mock_media_pool

    # Mock list_clips_in_media_pool to return our large list
    editor_actions.list_clips_in_media_pool = lambda: all_clips

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":
    for n in [100, 500, 1000, 5000, 10000]:
        t = benchmark_add_clips(n)
        print(f"Time taken to add {n} clips: {t:.4f} seconds")
