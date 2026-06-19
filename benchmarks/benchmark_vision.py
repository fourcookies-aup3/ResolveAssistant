import time
import os
import cv2
import numpy as np
from src.vision import find_image_on_screen

def create_dummy_assets():
    os.makedirs('assets/templates', exist_ok=True)
    template = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(template, (25, 25), (75, 75), (0, 255, 0), -1)
    cv2.imwrite('assets/templates/dummy.png', template)

    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
    screen[500:600, 500:600] = template
    cv2.imwrite('benchmarks/dummy_screen.png', screen)
    return 'assets/templates/dummy.png', 'benchmarks/dummy_screen.png'

def benchmark_vision():
    template_path, screen_path = create_dummy_assets()

    # Mock capture_screen to use our dummy screen
    import src.vision
    original_capture = src.vision.capture_screen
    dummy_screen = cv2.imread(screen_path)
    src.vision.capture_screen = lambda: dummy_screen

    print("Benchmarking find_image_on_screen...")
    start_time = time.time()
    iterations = 20
    for _ in range(iterations):
        find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time over {iterations} iterations: {avg_time:.4f}s")

    src.vision.capture_screen = original_capture

if __name__ == "__main__":
    benchmark_vision()
