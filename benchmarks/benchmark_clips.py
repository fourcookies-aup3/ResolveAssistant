import sys
import os
import time
from unittest.mock import MagicMock, patch

# Mock things before import to avoid DISPLAY errors and missing dependencies
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

os.environ["USE_MOCK_RESOLVE"] = "true"
import resolve_proxy
import editor_actions

def benchmark_add_clips():
    # Force API available in resolve_proxy
    resolve_proxy._resolve_instance = resolve_proxy.MockResolve(is_api_available=True)

    # Setup many mock clips
    num_pool_clips = 500
    num_to_add = 500

    pool_clips = []
    for i in range(num_pool_clips):
        clip = MagicMock()
        name = f"clip_{i}.mp4"
        clip.GetName.return_value = name
        clip.path = f"/path/to/{name}"
        pool_clips.append(clip)

    # Clip names to add
    clip_names_to_add = [f"clip_{i}.mp4" for i in range(num_to_add)]

    # We need to mock list_clips_in_media_pool to return our large list
    # and is_api_available to return True
    with patch('editor_actions.is_api_available', return_value=True),          patch('editor_actions.list_clips_in_media_pool', return_value=pool_clips):

        start_time = time.time()
        editor_actions.add_clips_to_timeline(clip_names_to_add)
        end_time = time.time()

    print(f"Time taken to add {num_to_add} clips from pool of {num_pool_clips}: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_add_clips()
