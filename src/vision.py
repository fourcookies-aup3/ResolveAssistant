import cv2
import numpy as np
from PIL import ImageGrab, Image
import os
import pytesseract

# Configure tesseract path if necessary (standard paths checked by default)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen(region=None):
    try:
        screenshot = ImageGrab.grab(bbox=region)
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        return screenshot_bgr
    except Exception as e:
        return None

def find_image_on_screen(template_path, threshold=0.8, region=None):
    if not os.path.exists(template_path):
        return None

    screen = capture_screen(region)
    if screen is None:
        return None

    template = cv2.imread(template_path)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        if region:
            center_x += region[0]
            center_y += region[1]
        return (center_x, center_y)
    return None

def read_text_from_screen(region=None):
    """
    Uses OCR to read text from a specific region or the whole screen.
    High precision for reading menu items and labels.
    """
    screen = capture_screen(region)
    if screen is None:
        return ""

    # Pre-process for OCR: grayscale and threshold
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    text = pytesseract.image_to_string(thresh)
    return text.strip()

def detect_ui_state():
    """
    Analyzes multiple UI indicators to determine the current state.
    Returns: {"page": "edit", "dialog": "none", "is_ready": True}
    """
    screen_text = read_text_from_screen()

    # Identify page based on OCR of common menu/tab items
    pages = ["Media", "Cut", "Edit", "Fusion", "Color", "Fairlight", "Deliver"]
    current_page = "unknown"
    for p in pages:
        if p.lower() in screen_text.lower():
            current_page = p.lower()
            break

    # Check for modal dialogs (e.g., Save, Import)
    dialog = "none"
    if "save" in screen_text.lower() and "project" in screen_text.lower():
        dialog = "save_project"
    elif "import" in screen_text.lower():
        dialog = "import_media"

    return {
        "page": current_page,
        "dialog": dialog,
        "is_ready": current_page != "unknown",
        "raw_vision": screen_text[:100] # For debugging
    }

def analyze_frame():
    screen = capture_screen()
    if screen is None:
        return {"brightness": 0, "dominant_color": "unknown"}

    small_screen = screen[::10, ::10]
    avg_color = np.average(np.average(small_screen, axis=0), axis=0)
    brightness = np.average(avg_color)

    b, g, r = avg_color
    dominant = "blue" if b > g and b > r else "green" if g > b and g > r else "red"

    # Advanced: Histogram analysis for precision grading
    hist = cv2.calcHist([screen], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    return {
        "brightness": float(brightness),
        "dominant_color": dominant,
        "ui_state": detect_ui_state(),
        "is_dark": brightness < 60,
        "is_high_contrast": np.std(small_screen) > 50
    }
