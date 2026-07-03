import cv2
import numpy as np
from PIL import ImageGrab
import os

# Module-level cache for grayscale templates to avoid redundant disk I/O
# and grayscale conversions.
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
    Uses grayscale matching and template caching for performance.
    """
    if not os.path.exists(template_path):
        print(f"Template image not found: {template_path}")
        return None

    screen = capture_screen()
    if screen is None:
        return None

    # Performance optimization: Grayscale matching reduces processing
    # time as cv2.matchTemplate only needs to process a single channel.
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Performance optimization: Cache templates in memory to avoid
    # repeated disk I/O and grayscale conversion.
    if template_path in _template_cache:
        template_gray = _template_cache[template_path]
    else:
        # Load directly as grayscale
        template_gray = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template_gray is None:
            print(f"Failed to load template: {template_path}")
            return None
        _template_cache[template_path] = template_gray

    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template_gray.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None
