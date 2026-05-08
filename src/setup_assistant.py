import pyautogui
import os
import time

def capture_template(name):
    """
    Guides the user to capture a UI element template.
    """
    print(f"--- Template Capture: {name} ---")
    print("Move your mouse to the TOP-LEFT corner of the UI element and wait 3 seconds...")
    time.sleep(3)
    x1, y1 = pyautogui.position()
    print(f"Captured: {x1}, {y1}")

    print("Now move your mouse to the BOTTOM-RIGHT corner of the UI element and wait 3 seconds...")
    time.sleep(3)
    x2, y2 = pyautogui.position()
    print(f"Captured: {x2}, {y2}")

    width = x2 - x1
    height = y2 - y1

    if width <= 0 or height <= 0:
        print("Error: Invalid region captured. Please try again.")
        return

    print(f"Capturing region: ({x1}, {y1}, {width}, {height})")
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

    os.makedirs('assets/templates', exist_ok=True)
    save_path = os.path.join('assets/templates', f"{name}.png")
    screenshot.save(save_path)
    print(f"Success! Template saved to {save_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        capture_template(sys.argv[1])
    else:
        print("Usage: python src/setup_assistant.py [template_name]")
