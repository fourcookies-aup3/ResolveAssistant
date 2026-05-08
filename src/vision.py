import cv2
import numpy as np
from PIL import ImageGrab
import os

def capture_screen(region=None):
    """
    Captures a region of the screen for faster processing.
    region: (left, top, width, height)
    """
    try:
        screenshot = ImageGrab.grab(bbox=region)
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        return screenshot_bgr
    except Exception as e:
        return None

def find_image_on_screen(template_path, threshold=0.8, region=None):
    """
    Finds a template image on the screen, optionally within a region.
    """
    if not os.path.exists(template_path):
        return None

    screen = capture_screen(region)
    if screen is None:
        return None

    template = cv2.imread(template_path)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2

        # Adjust for region offset
        if region:
            center_x += region[0]
            center_y += region[1]

        return (center_x, center_y)

    return None

def analyze_frame():
    """
    Optimized frame analysis: samples every 10th pixel for speed.
    """
    screen = capture_screen()
    if screen is None:
        return {"brightness": 0, "dominant_color": "unknown", "movement_score": 0}

    # Subsample for speed
    small_screen = screen[::10, ::10]
    avg_color = np.average(np.average(small_screen, axis=0), axis=0)
    brightness = np.average(avg_color)

    b, g, r = avg_color
    dominant = "blue" if b > g and b > r else "green" if g > b and g > r else "red"

    return {
        "brightness": float(brightness),
        "dominant_color": dominant,
        "avg_bgr": [float(b), float(g), float(r)]
    }
