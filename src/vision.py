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

def find_image_on_screen(template_path, threshold=0.8):
    """
    Finds a template image on the screen.
    Returns (x, y) coordinates of the match or None.
    """
    if not os.path.exists(template_path):
        return None

    screen = capture_screen()
    if screen is None:
        return None

    template = cv2.imread(template_path)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)

    return None

def analyze_frame():
    """
    Captures the screen and provides a basic visual summary.
    In a real AI, this would return dominant colors, brightness, and scene type.
    """
    screen = capture_screen()
    if screen is None:
        return {"brightness": 0, "dominant_color": "unknown"}

    avg_color_per_row = np.average(screen, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    brightness = np.average(avg_color)

    # Simple color classification
    b, g, r = avg_color
    dominant = "blue" if b > g and b > r else "green" if g > b and g > r else "red"

    return {
        "brightness": float(brightness),
        "dominant_color": dominant,
        "avg_bgr": [float(b), float(g), float(r)]
    }
