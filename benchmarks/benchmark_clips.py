import time
import sys
import os
from unittest.mock import MagicMock

# Mock GUI modules before importing src modules
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath("src"))

# Set environment variable for mock resolve
os.environ["USE_MOCK_RESOLVE"] = "true"

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve, MockMediaPoolItem

def benchmark_add_clips():
    # Increase scale to see the difference more clearly
    pool_size = 5000
    to_add_count = 1000

    resolve = get_resolve()
    project = resolve.GetProjectManager().CreateProject("Test Project")
    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()

    # Fill media pool
    all_clips = [MockMediaPoolItem(f"/path/to/clip_{i}.mp4") for i in range(pool_size)]
    root_folder.clips = all_clips

    clip_names = [f"clip_{i}.mp4" for i in range(0, pool_size, pool_size // to_add_count)]

    start_time = time.time()
    add_clips_to_timeline(clip_names)
    end_time = time.time()

    print(f"Time taken to add {len(clip_names)} clips from {pool_size} pool: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_add_clips()
