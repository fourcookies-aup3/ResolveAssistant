import cv2
import numpy as np
from PIL import ImageGrab
import os

# Cache for loaded templates to avoid redundant disk I/O and preprocessing
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
    screen = capture_screen()
    if screen is None:
        return None

    # Performance optimization: Grayscale conversion reduces processing load
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Optimization: Use memory cache for templates
    if template_path in _template_cache:
        template_gray = _template_cache[template_path]
    else:
        if not os.path.exists(template_path):
            print(f"Template image not found: {template_path}")
            return None

        template = cv2.imread(template_path)
        if template is None:
            return None
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        _template_cache[template_path] = template_gray

    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template_gray.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None
