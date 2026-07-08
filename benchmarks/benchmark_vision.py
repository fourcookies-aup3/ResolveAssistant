import sys
import os
import time
import statistics
import numpy as np
from unittest.mock import MagicMock

# Mock GUI and other deps
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
import PIL.ImageGrab

# Mock screen capture
mock_screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
PIL.ImageGrab.grab.return_value = MagicMock()
# We need to mock the conversion or ensure it works with the mock
# Actually let's just mock capture_screen in vision

sys.path.append('src')
import vision

def run_benchmark(iterations=10):
    # Create a dummy template
    template_path = 'dummy_template.png'
    template = np.zeros((100, 100, 3), dtype=np.uint8)
    import cv2
    cv2.imwrite(template_path, template)

    # Mock capture_screen to return a fixed image
    vision.capture_screen = MagicMock(return_value=np.zeros((1080, 1920, 3), dtype=np.uint8))

    durations = []
    for _ in range(iterations):
        start = time.perf_counter()
        vision.find_image_on_screen(template_path)
        end = time.perf_counter()
        durations.append(end - start)

    os.remove(template_path)
    return durations

if __name__ == "__main__":
    durations = run_benchmark(20)
    avg = statistics.mean(durations)
    print(f"Average execution time for find_image_on_screen: {avg:.6f}s")
