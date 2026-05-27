import time
import os
import sys
from unittest.mock import MagicMock

# Mocking GUI dependencies for headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Ensure we can import from src
sys.path.append(os.path.abspath('src'))

from editor_actions import add_clips_to_timeline
import resolve_proxy

def benchmark_add_clips():
    # Setup mock clips
    num_clips = 1000
    mock_clips = []
    for i in range(num_clips):
        clip = MagicMock()
        clip.GetName.return_value = f"clip_{i}.mp4"
        clip.path = f"/path/to/clip_{i}.mp4"
        mock_clips.append(clip)

    # Inject mock clips into the mock resolve
    resolve = resolve_proxy.get_resolve()
    project = resolve.GetProjectManager().CreateProject("Test Project")
    project.GetMediaPool().GetRootFolder().clips = mock_clips

    # List of clips to add (worst case: all of them in reverse order)
    clip_names_to_add = [f"clip_{i}.mp4" for i in range(num_clips)][::-1]

    start_time = time.time()
    add_clips_to_timeline(clip_names_to_add)
    end_time = time.time()

    print(f"Time taken to add {num_clips} clips: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_add_clips()
