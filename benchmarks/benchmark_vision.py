import time
import numpy as np
import cv2
import os
import sys

# Mocking modules that might not be available or need DISPLAY
from unittest.mock import MagicMock
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath('src'))
import vision

def create_dummy_images():
    # Create a dummy screen (1920x1080)
    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    # Draw a rectangle as the template (100x100) at (500, 500)
    cv2.rectangle(screen, (500, 500), (600, 600), (255, 255, 255), -1)

    template = screen[500:600, 500:600].copy()

    cv2.imwrite('benchmarks/dummy_screen.png', screen)
    os.makedirs('assets/templates', exist_ok=True)
    cv2.imwrite('assets/templates/dummy.png', template)
    return screen, template

def benchmark_vision():
    screen_img, template_img = create_dummy_images()

    # Mock vision.capture_screen to return our dummy screen
    vision.capture_screen = MagicMock(return_value=screen_img)

    template_path = 'assets/templates/dummy.png'

    print("Starting benchmark for find_image_on_screen...")
    start_time = time.time()
    iterations = 10
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per call: {avg_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_vision()
