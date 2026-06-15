import time
import os
import sys
import numpy as np
import cv2

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import vision

def benchmark_vision():
    # Setup dummy images
    template_path = "benchmarks/dummy_template.png"
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")

    # Create a real dummy image (1080p screen)
    dummy_screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    # Add some noise or a pattern so it's not just zeros
    cv2.rectangle(dummy_screen, (500, 500), (600, 600), (255, 255, 255), -1)

    dummy_template = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(dummy_template, (0, 0), (100, 100), (255, 255, 255), -1)

    cv2.imwrite("benchmarks/dummy_screen.png", dummy_screen)
    cv2.imwrite(template_path, dummy_template)

    # Mock capture_screen to return our dummy screen
    vision.capture_screen = lambda: cv2.imread("benchmarks/dummy_screen.png")

    # Warm up
    vision.find_image_on_screen(template_path)

    start_time = time.time()
    iterations = 20
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for vision lookup: {avg_time:.4f}s")
    return avg_time

if __name__ == "__main__":
    benchmark_vision()
