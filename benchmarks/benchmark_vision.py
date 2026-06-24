import time
import os
import sys
from unittest.mock import MagicMock
import numpy as np

# Mock GUI libs
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def benchmark_vision():
    import vision
    import cv2

    # Create a dummy screen and template
    screen_w, screen_h = 1920, 1080
    template_w, template_h = 100, 50

    dummy_screen = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
    dummy_template = np.zeros((template_h, template_w, 3), dtype=np.uint8)

    # Put the template somewhere in the screen
    x, y = 500, 400
    dummy_screen[y:y+template_h, x:x+template_w] = 255
    dummy_template[:] = 255

    # Mock capture_screen to return our dummy screen
    vision.capture_screen = MagicMock(return_value=dummy_screen)

    # Mock cv2.imread to return our dummy template
    cv2.imread = MagicMock(return_value=dummy_template)
    os.path.exists = MagicMock(return_value=True)

    template_path = "assets/templates/test.png"

    # Warm up
    vision.find_image_on_screen(template_path)

    start_time = time.time()
    iterations = 20
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    print(f"Average time for find_image_on_screen: {(end_time - start_time) / iterations:.4f} seconds")

if __name__ == "__main__":
    benchmark_vision()
