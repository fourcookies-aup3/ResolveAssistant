import cv2
import numpy as np
from PIL import ImageGrab
import os

# BOLT OPTIMIZATION: Module-level cache for template images to avoid
# repeated disk I/O.
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
    if not os.path.exists(template_path):
        print(f"Template image not found: {template_path}")
        return None

    screen = capture_screen()
    if screen is None:
        return None

    # BOLT OPTIMIZATION: Convert screen to grayscale for significantly faster
    # matching. UI elements usually have distinct shapes that are well-captured
    # in grayscale.
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # BOLT OPTIMIZATION: Use cached template if available to eliminate
    # redundant disk I/O.
    if template_path in _template_cache:
        template_gray, (h, w) = _template_cache[template_path]
    else:
        template = cv2.imread(template_path)
        if template is None:
            return None
        # Pre-process template to grayscale and cache it along with its
        # dimensions.
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        h, w = template_gray.shape[:2]
        _template_cache[template_path] = (template_gray, (h, w))

    # Perform template matching on grayscale images for optimal performance.
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None
