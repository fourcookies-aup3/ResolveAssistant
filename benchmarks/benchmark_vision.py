import time
import os
import sys
import numpy as np
import cv2
from unittest.mock import MagicMock

# Mocking GUI dependencies for headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Ensure we can import from src
sys.path.append(os.path.abspath('src'))

import vision

def benchmark_vision():
    # Create a dummy screen and template
    screen_np = np.zeros((1080, 1920, 3), dtype=np.uint8)
    template_np = np.zeros((100, 100, 3), dtype=np.uint8)

    # Put the template somewhere in the screen
    screen_np[500:600, 500:600] = template_np

    template_path = 'benchmarks/dummy_template.png'
    os.makedirs('benchmarks', exist_ok=True)
    cv2.imwrite(template_path, template_np)

    # Mock capture_screen to return our dummy screen
    vision.capture_screen = MagicMock(return_value=screen_np)

    num_iterations = 100
    start_time = time.time()
    for _ in range(num_iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    print(f"Time taken for {num_iterations} vision lookups: {end_time - start_time:.4f} seconds")
    print(f"Average time per lookup: {(end_time - start_time) / num_iterations:.4f} seconds")

if __name__ == "__main__":
    benchmark_vision()
