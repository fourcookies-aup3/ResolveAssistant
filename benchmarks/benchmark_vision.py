import time
import numpy as np
import cv2
import os
import sys

# Mocking the environment to avoid issues in headless mode
from unittest.mock import MagicMock
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Import the vision module
# We need to add src to the path
sys.path.append(os.path.join(os.getcwd(), 'src'))
import vision

def benchmark_vision():
    # Create a dummy screen and template
    screen_size = (1080, 1920, 3)
    template_size = (50, 100, 3)

    screen = np.random.randint(0, 256, screen_size, dtype=np.uint8)
    template = np.random.randint(0, 256, template_size, dtype=np.uint8)

    # Place template in screen
    x, y = 500, 500
    screen[y:y+template_size[0], x:x+template_size[1]] = template

    # Save template to disk as vision module reads from disk
    template_path = 'benchmarks/template.png'
    cv2.imwrite(template_path, template)

    # Mock capture_screen to return our dummy screen
    vision.capture_screen = MagicMock(return_value=screen)

    # Measure time for find_image_on_screen
    start_time = time.time()
    iterations = 10
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for find_image_on_screen: {avg_time:.4f} seconds")

    # Cleanup
    if os.path.exists(template_path):
        os.remove(template_path)

if __name__ == "__main__":
    benchmark_vision()
