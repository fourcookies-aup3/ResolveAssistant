import cv2
import numpy as np
import time

def benchmark_vision():
    # Create a dummy screen and template
    screen = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
    template = screen[500:550, 800:850].copy()

    # Add some noise to the screen to make it more realistic
    noise = np.random.randint(0, 10, (1080, 1920, 3), dtype=np.uint8)
    screen = cv2.add(screen, noise)

    print("Benchmarking vision matching (1080p screen, 50x50 template)...")

    # Color matching
    start_time = time.time()
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    end_time = time.time()
    print(f"Color matching took: {end_time - start_time:.4f} seconds")

    # Grayscale matching
    start_time = time.time()
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    end_time = time.time()
    print(f"Grayscale matching took: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_vision()
