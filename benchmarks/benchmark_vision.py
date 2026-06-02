import time
import numpy as np
import cv2
import os
import sys

# Add src to path
sys.path.append(os.path.abspath('src'))

import vision

def benchmark_vision():
    # Create a dummy screen and template
    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    template = np.zeros((100, 100, 3), dtype=np.uint8)
    # Add some "content" to match
    cv2.rectangle(screen, (500, 500), (600, 600), (255, 255, 255), -1)
    cv2.rectangle(template, (0, 0), (100, 100), (255, 255, 255), -1)

    template_path = 'dummy_template.png'
    cv2.imwrite(template_path, template)

    # Mock capture_screen to return our dummy screen
    original_capture = vision.capture_screen
    vision.capture_screen = lambda: screen

    start_time = time.time()
    iterations = 20
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for find_image_on_screen: {avg_time:.4f}s")

    # Cleanup
    os.remove(template_path)
    vision.capture_screen = original_capture

if __name__ == "__main__":
    benchmark_vision()
