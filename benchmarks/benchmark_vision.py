import time
import sys
import os
from unittest.mock import MagicMock
import cv2
import numpy as np

# Mock ImageGrab before importing vision
sys.modules['pyautogui'] = MagicMock()
from PIL import Image

def mock_grab():
    return Image.open('benchmarks/dummy_screen.png')

import PIL.ImageGrab
PIL.ImageGrab.grab = mock_grab

# Add src to path
sys.path.append(os.path.abspath('src'))
import vision

def benchmark_vision():
    template_path = 'assets/templates/dummy.png'
    iterations = 50

    print(f"Benchmarking find_image_on_screen with {iterations} iterations...")

    start_time = time.time()
    for _ in range(iterations):
        vision.find_image_on_screen(template_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per call: {avg_time:.4f} seconds")
    return avg_time

if __name__ == "__main__":
    benchmark_vision()
