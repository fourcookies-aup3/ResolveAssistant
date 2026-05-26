import time
import sys
import os
import cv2
import numpy as np
from unittest.mock import patch

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import vision

def benchmark_find_image(iterations=10):
    template_path = 'assets/templates/dummy_template.png'
    dummy_screen = cv2.imread('benchmarks/dummy_screen.png')

    print(f"Benchmarking find_image_on_screen with {iterations} iterations...")

    # Mock capture_screen to isolate template loading and matching
    with patch('vision.capture_screen', return_value=dummy_screen):
        # First call to populate cache
        vision.find_image_on_screen(template_path)

        start_time = time.time()
        for _ in range(iterations):
            vision.find_image_on_screen(template_path)
        end_time = time.time()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Total time: {total_time:.4f}s")
    print(f"Average time per call (Cached): {avg_time:.4f}s")
    return avg_time

if __name__ == "__main__":
    benchmark_find_image()
