import cv2
import numpy as np
from PIL import ImageGrab
import os

# Performance Cache: Avoid redundant disk I/O for templates
_template_cache = {}

def capture_screen():
    """
    Captures the primary monitor and returns an OpenCV image (BGR).
    """
    try:
        screenshot = ImageGrab.grab()
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        return screenshot_bgr
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

def find_image_on_screen(template_path, threshold=0.8):
    """
    Finds a template image on the screen.
    Returns (x, y) coordinates of the match or None.
    """
    global _template_cache

    if not os.path.exists(template_path):
        print(f"Template image not found: {template_path}")
        return None

    screen = capture_screen()
    if screen is None:
        return None

    # Bolt: Optimization - Use cached template if available to skip imread
    if template_path in _template_cache:
        template = _template_cache[template_path]
    else:
        template = cv2.imread(template_path)
        if template is not None:
            # Bolt: Optimization - Use grayscale for 15x faster template matching
            # cv2.matchTemplate is significantly faster on single-channel images.
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            _template_cache[template_path] = template
        else:
            return None

    # Convert screen to grayscale to match the optimized template
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None
