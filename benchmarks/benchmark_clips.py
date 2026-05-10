import sys
import os
import time
from unittest.mock import MagicMock

# Mock GUI and other libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
# cv2 mock to return a dummy image
cv2_mock = MagicMock()
cv2_mock.imread.return_value = MagicMock()
cv2_mock.matchTemplate.return_value = MagicMock()
cv2_mock.minMaxLoc.return_value = (0, 0.9, (0,0), (100,100))
sys.modules['cv2'] = cv2_mock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
import resolve_proxy

def benchmark_add_clips_to_timeline(num_clips):
    # Force fresh mock
    resolve_proxy._resolve_instance = None
    os.environ["USE_MOCK_RESOLVE"] = "true"
    resolve = resolve_proxy.get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(f"Bench Project {num_clips}")
    mp = project.GetMediaPool()
    root = mp.GetRootFolder()

    clip_names = [f"clip_{i}.mp4" for i in range(num_clips)]
    # Populate media pool
    from resolve_proxy import MockMediaPoolItem
    root.clips = [MockMediaPoolItem(name) for name in clip_names]

    start_time = time.time()
    editor_actions.add_clips_to_timeline(clip_names)
    end_time = time.time()

    print(f"Time to add {num_clips} clips: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips_to_timeline(100)
    benchmark_add_clips_to_timeline(500)
    benchmark_add_clips_to_timeline(1000)
    benchmark_add_clips_to_timeline(2000)
