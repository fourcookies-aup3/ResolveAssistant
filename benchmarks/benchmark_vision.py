import time
import os
import sys
import numpy as np
from unittest.mock import MagicMock

# Mock GUI modules to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
# We need real cv2 for benchmarking the matching logic if possible,
# but we can mock the screen capture.
import cv2

sys.path.append(os.path.abspath("src"))
import vision

def run_vision_benchmark():
    print("Starting benchmark for find_image_on_screen...")

    # Create dummy images
    screen_np = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
    template_np = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)

    # Place template in screen
    screen_np[500:550, 600:650] = template_np

    cv2.imwrite("benchmarks/dummy_screen.png", screen_np)
    os.makedirs("assets/templates", exist_ok=True)
    cv2.imwrite("assets/templates/dummy.png", template_np)

    # Mock capture_screen to return our dummy screen
    vision.capture_screen = MagicMock(return_value=screen_np)

    start_time = time.time()
    for _ in range(10):
        vision.find_image_on_screen("assets/templates/dummy.png")
    end_time = time.time()

    print(f"Time taken for 10 iterations: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    run_vision_benchmark()
