
import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries before they are imported
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Mock Resolve for benchmark
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
import resolve_proxy

class SlowClip:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def GetName(self):
        # Simulate a slightly slow API call
        time.sleep(0.001)
        return self.name

def benchmark_add_clips():
    import editor_actions
    from unittest.mock import patch

    # Create 1000 slow clips
    all_clips = [SlowClip(f"clip_{i}.mp4", f"/path/to/clip_{i}.mp4") for i in range(1000)]
    clip_names = [f"clip_{i}.mp4" for i in range(900, 910)] # 10 clips to find

    with patch('editor_actions.list_clips_in_media_pool', return_value=all_clips):
        with patch('editor_actions.is_api_available', return_value=True):
            with patch('editor_actions.get_resolve') as mock_get_resolve:
                # Setup mock project/media pool
                mock_project = mock_get_resolve.return_value.GetProjectManager.return_value.GetCurrentProject.return_value
                mock_project.GetCurrentTimeline.return_value = True # Already has timeline

                start_time = time.time()
                editor_actions.add_clips_to_timeline(clip_names)
                end_time = time.time()

                print(f"Time taken for add_clips_to_timeline: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
