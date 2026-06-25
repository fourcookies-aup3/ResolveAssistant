import time
import os
import cv2
import numpy as np
from src.vision import find_image_on_screen

def benchmark_vision():
    template_path = 'assets/templates/dummy.png'

    # Create a dummy screen
    dummy_screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    # Put the template somewhere
    dummy_screen[500:600, 500:600] = 255
    cv2.imwrite('benchmarks/dummy_screen.png', dummy_screen)

    # We need to mock capture_screen to return our dummy_screen
    import src.vision
    original_capture = src.vision.capture_screen
    src.vision.capture_screen = lambda: cv2.imread('benchmarks/dummy_screen.png')

    start_time = time.time()
    for _ in range(10):
        find_image_on_screen(template_path)
    end_time = time.time()

    print(f"Average time for find_image_on_screen: {(end_time - start_time) / 10:.4f}s")

    src.vision.capture_screen = original_capture

if __name__ == "__main__":
    benchmark_vision()
