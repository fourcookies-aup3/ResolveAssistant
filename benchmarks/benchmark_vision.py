import time
import sys
import os
import numpy as np

# Mocking necessary modules for headless environment
from unittest.mock import MagicMock

sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath('src'))

import vision

def benchmark_vision():
    print("Running Vision Benchmarks...")

    # Create a dummy screen and template
    screen = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
    template = screen[500:550, 500:550].copy()

    template_path = "benchmarks/dummy_template.png"
    os.makedirs("benchmarks", exist_ok=True)
    import cv2
    cv2.imwrite(template_path, template)

    # Monkeypatch capture_screen to return our dummy screen
    original_capture = vision.capture_screen
    vision.capture_screen = lambda: screen

    iterations = 10
    start_time = time.time()
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for find_image_on_screen: {avg_time:.4f}s")

    vision.capture_screen = original_capture
    return avg_time

if __name__ == "__main__":
    benchmark_vision()
