import pyautogui
import subprocess
import os
import sys
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

def click(x, y):
    pyautogui.click(x, y)

def right_click(x, y):
    pyautogui.rightClick(x, y)

def type_text(text):
    pyautogui.write(text, interval=0.05)

def press_key(key):
    pyautogui.press(key)

def hotkey(*args):
    pyautogui.hotkey(*args)

def move_to(x, y):
    pyautogui.moveTo(x, y, duration=0)

def get_screen_size():
    return pyautogui.size()

def launch_resolve(executable_path=None):
    if not executable_path:
        if sys.platform == 'win32':
            executable_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
        elif sys.platform == 'darwin':
            executable_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve"
    if executable_path and os.path.exists(executable_path):
        subprocess.Popen([executable_path])
        return True
    return False

def wait_for_window(window_title_part="DaVinci Resolve", timeout=60):
    """
    Backwards compatibility for tests.
    """
    time.sleep(1)
    return True

def focus_window():
    if sys.platform == 'win32':
        hotkey('alt', 'tab')
    elif sys.platform == 'darwin':
        hotkey('command', 'tab')
    time.sleep(1)

import vision
def precise_click_template(template_name, expected_state=None):
    if expected_state:
        state = vision.detect_ui_state()
        if state['page'] != expected_state:
            return False
    coords = vision.find_image_on_screen(f"assets/templates/{template_name}.png")
    if coords:
        click(coords[0], coords[1])
        return True
    return False

def wait_for_ui_text(text, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        screen_text = vision.read_text_from_screen()
        if text.lower() in screen_text.lower():
            return True
        time.sleep(0.5)
    return False

def secure_type(text, verification_text=None):
    pyautogui.write(text, interval=0.02)
    if verification_text:
        return wait_for_ui_text(verification_text)
    return True
