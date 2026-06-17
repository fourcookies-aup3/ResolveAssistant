import os
import sys
import time
from unittest.mock import MagicMock, patch

# Mock GUI modules before importing src
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import editor_actions
import resolve_proxy
from resolve_proxy import MockMediaPoolItem

def benchmark_add_clips():
    print("Benchmarking add_clips_to_timeline...")

    # Setup many mock clips
    num_pool_clips = 10000
    num_target_clips = 500

    pool_clips = []
    for i in range(num_pool_clips):
        clip = MockMediaPoolItem(f"/path/to/clip_{i}.mp4")
        pool_clips.append(clip)

    target_names = [f"clip_{i}.mp4" for i in range(0, num_target_clips * 2, 2)]

    # Mock other API calls to avoid side effects
    with patch('editor_actions.is_api_available', return_value=True), \
         patch('editor_actions.get_resolve') as mock_get_resolve, \
         patch('editor_actions.list_clips_in_media_pool', return_value=pool_clips):

        mock_resolve = MagicMock()
        mock_get_resolve.return_value = mock_resolve
        mock_project = mock_resolve.GetProjectManager.return_value.GetCurrentProject.return_value
        mock_project.GetCurrentTimeline.return_value = MagicMock()
        mock_project.GetMediaPool.return_value.AppendToTimeline = MagicMock()

        start_time = time.time()
        editor_actions.add_clips_to_timeline(target_names)
        end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken for {num_target_clips} targets in {num_pool_clips} clips: {duration:.4f}s")
    return duration

if __name__ == "__main__":
    benchmark_add_clips()
