import time
import os
import sys
import numpy as np
import cv2

sys.path.append('src')
import vision

def run_benchmark():
    # Create a dummy screen and template
    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    template = np.zeros((50, 50, 3), dtype=np.uint8)

    # Draw something on both
    cv2.rectangle(screen, (500, 500), (550, 550), (255, 255, 255), -1)
    cv2.rectangle(template, (0, 0), (50, 50), (255, 255, 255), -1)

    os.makedirs('assets/templates', exist_ok=True)
    cv2.imwrite('assets/templates/dummy.png', template)
    cv2.imwrite('benchmarks/dummy_screen.png', screen)

    # Mock capture_screen to return our dummy screen instead of actually grabbing it
    original_capture = vision.capture_screen
    vision.capture_screen = lambda: cv2.imread('benchmarks/dummy_screen.png')

    print("Benchmarking find_image_on_screen...")

    start_time = time.time()
    for _ in range(10):
        vision.find_image_on_screen('assets/templates/dummy.png')
    end_time = time.time()

    duration = (end_time - start_time) / 10
    print(f"Average time taken: {duration:.4f} seconds")

    vision.capture_screen = original_capture

if __name__ == "__main__":
    run_benchmark()
