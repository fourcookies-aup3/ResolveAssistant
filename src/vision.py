import cv2
import numpy as np
from PIL import ImageGrab
import os

# Module-level cache for template images
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
    Finds a template image on the screen using grayscale matching and caching.
    Returns (x, y) coordinates of the match or None.
    """
    # Performance: Check cache first to avoid syscall
    if template_path in _template_cache:
        template_gray = _template_cache[template_path]
    else:
        if not os.path.exists(template_path):
            print(f"Template image not found: {template_path}")
            return None

        template_img = cv2.imread(template_path)
        if template_img is None:
            return None
        # Performance: Cache template images and store them in grayscale
        template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
        _template_cache[template_path] = template_gray

    screen_bgr = capture_screen()
    if screen_bgr is None:
        return None

    # Performance: Convert screen to grayscale once
    screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)

    # Perform template matching in grayscale
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template_gray.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None
