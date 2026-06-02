import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries before they are imported by src modules
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()

# Mocking resolve_proxy
class MockClip:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

class MockMediaPool:
    def AppendToTimeline(self, clips):
        return True

class MockProject:
    def GetCurrentTimeline(self):
        return True
    def GetMediaPool(self):
        return MockMediaPool()

class MockResolve:
    def GetProjectManager(self):
        class PM:
            def GetCurrentProject(self):
                return MockProject()
        return PM()

mock_resolve_proxy = MagicMock()
mock_resolve_proxy.is_api_available.return_value = True
mock_resolve_proxy.get_resolve.return_value = MockResolve()
sys.modules['resolve_proxy'] = mock_resolve_proxy

# Add src to path
sys.path.append(os.path.abspath('src'))

# Now import editor_actions
import editor_actions

def benchmark_add_clips():
    # Setup many clips
    num_total_clips = 10000
    all_clips = [MockClip(f"clip_{i}.mp4", f"/path/to/clip_{i}.mp4") for i in range(num_total_clips)]

    # Mock list_clips_in_media_pool
    editor_actions.list_clips_in_media_pool = lambda: all_clips

    clips_to_add_names = [f"clip_{i}.mp4" for i in range(2000)]

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clips_to_add_names)
    end_time = time.time()

    print(f"Time to add 2000 clips out of 10000: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_add_clips()
