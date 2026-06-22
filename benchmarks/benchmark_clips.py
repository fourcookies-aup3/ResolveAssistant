import time
import sys
import os

# Mocking necessary modules
from unittest.mock import MagicMock

sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Mocking resolve_proxy since it might try to connect to a real Resolve instance
sys.modules['resolve_proxy'] = MagicMock()
import resolve_proxy
resolve_proxy.is_api_available.return_value = True

# Mocking GetResolve
mock_resolve = MagicMock()
resolve_proxy.get_resolve.return_value = mock_resolve

# Set up mock project and media pool
mock_project = MagicMock()
mock_resolve.GetProjectManager().GetCurrentProject.return_value = mock_project
mock_mp = MagicMock()
mock_project.GetMediaPool.return_value = mock_mp

# Add src to path
sys.path.append(os.path.abspath('src'))

import editor_actions

def benchmark_clips():
    print("Running Clips Benchmarks...")

    num_pool_clips = 1000
    num_targets = 100

    # Create many mock clips
    all_clips = []
    for i in range(num_pool_clips):
        clip = MagicMock()
        clip.GetName.return_value = f"clip_{i}.mp4"
        clip.path = f"/path/to/clip_{i}.mp4"
        all_clips.append(clip)

    # Mock list_clips_in_media_pool
    editor_actions.list_clips_in_media_pool = lambda: all_clips

    target_names = [f"clip_{i}.mp4" for i in range(0, num_pool_clips, num_pool_clips // num_targets)]

    iterations = 5
    start_time = time.time()
    for _ in range(iterations):
        editor_actions.add_clips_to_timeline(target_names)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for add_clips_to_timeline ({num_pool_clips} pool clips, {num_targets} targets): {avg_time:.4f}s")
    return avg_time

if __name__ == "__main__":
    benchmark_clips()
