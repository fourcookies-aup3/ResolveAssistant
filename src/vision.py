import cv2
import numpy as np
from PIL import ImageGrab
import os

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

# Module-level template cache for grayscale templates
_template_cache = {}

def find_image_on_screen(template_path, threshold=0.8):
    """
    Finds a template image on the screen.
    Returns (x, y) coordinates of the match or None.
    Optimized: Implements module-level caching and grayscale conversion for cv2.matchTemplate.
    """
    global _template_cache

    # 1. Cache hit check or load from disk (optimized: os.path.exists run only on miss)
    if template_path in _template_cache:
        template_gray, (h, w) = _template_cache[template_path]
    else:
        if not os.path.exists(template_path):
            print(f"Template image not found: {template_path}")
            return None

        template = cv2.imread(template_path)
        if template is None:
            print(f"Failed to read template image: {template_path}")
            return None

        # Convert template to grayscale and cache
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        h, w = template_gray.shape[:2]
        _template_cache[template_path] = (template_gray, (h, w))

    screen = capture_screen()
    if screen is None:
        return None

    # Convert screen capture to grayscale to speed up cv2.matchTemplate
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None
