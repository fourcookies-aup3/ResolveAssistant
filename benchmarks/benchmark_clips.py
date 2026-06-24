import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libs
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class MockClip:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

def benchmark_add_clips():
    import editor_actions

    # Setup mock clips
    num_pool_clips = 5000
    num_targets = 200

    all_clips = [MockClip(f"clip_{i}", f"/path/to/clip_{i}.mp4") for i in range(num_pool_clips)]
    # Search for clips that are at the end of the pool to trigger worst case for O(N*M)
    clip_names = [f"clip_{i}" for i in range(num_pool_clips - num_targets, num_pool_clips)]

    # Mock the necessary parts of editor_actions/resolve_proxy
    editor_actions.is_api_available = MagicMock(return_value=True)
    mock_resolve = MagicMock()
    editor_actions.get_resolve = MagicMock(return_value=mock_resolve)

    mock_project = mock_resolve.GetProjectManager().GetCurrentProject()
    mock_project.GetCurrentTimeline.return_value = MagicMock()
    mock_project.GetMediaPool().GetRootFolder().GetClipList.return_value = all_clips

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names)
    end_time = time.time()

    print(f"Time taken to add {num_targets} clips from the END of a pool of {num_pool_clips}: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
