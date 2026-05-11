import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries to avoid errors in headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

sys.path.append(os.path.abspath('src'))
import editor_actions
import resolve_proxy

class MockClip:
    def __init__(self, name):
        self.name = name
    def GetName(self):
        return self.name

def benchmark():
    # Setup mock
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject("Bench")

    # Create many clips in media pool
    num_clips = 2000
    clips = [MockClip(f"clip_{i}.mp4") for i in range(num_clips)]
    project.GetMediaPool().GetRootFolder().clips = clips

    # Clip names to find (half of them)
    search_names = [f"clip_{i}.mp4" for i in range(0, num_clips, 2)]

    print(f"Benchmarking add_clips_to_timeline with {len(search_names)} searches in {num_clips} clips...")

    start = time.time()
    editor_actions.add_clips_to_timeline(search_names)
    end = time.time()

    duration = end - start
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    benchmark()
