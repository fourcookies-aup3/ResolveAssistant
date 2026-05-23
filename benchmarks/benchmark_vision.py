import time
import sys
import os
from unittest.mock import MagicMock

# Mocking GUI dependencies to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()

# Mocking cv2 for capture_screen if needed, but we want to benchmark the real cv2 matchTemplate
import cv2
import numpy as np

# Add src to path
sys.path.append(os.path.abspath('src'))
import vision

def benchmark_vision():
    print("Running Vision Benchmarks...")

    # Create a dummy screen and template
    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    template = np.zeros((100, 100, 3), dtype=np.uint8)

    # Put some data in template and screen
    cv2.rectangle(template, (10, 10), (90, 90), (255, 255, 255), -1)
    cv2.rectangle(screen, (500, 500), (600, 600), (255, 255, 255), -1)

    template_path = 'benchmarks/template.png'
    cv2.imwrite(template_path, template)

    # Mock capture_screen to return our screen
    original_capture = vision.capture_screen
    vision.capture_screen = lambda: screen

    start_time = time.time()
    iterations = 10
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for find_image_on_screen: {avg_time:.4f}s")

    # Cleanup
    os.remove(template_path)
    vision.capture_screen = original_capture
    return avg_time

if __name__ == "__main__":
    benchmark_vision()
