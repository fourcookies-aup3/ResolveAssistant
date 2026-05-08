import pyautogui
import subprocess
import os
import sys
import time

# Safety features
pyautogui.FAILSAFE = True
# Boosted speed: reduced pause from 1.0 to 0.1
pyautogui.PAUSE = 0.1

def click(x, y):
    """
    Moves to and clicks at the specified coordinates instantly.
    """
    pyautogui.click(x, y)

def right_click(x, y):
    """
    Moves to and right-clicks at the specified coordinates instantly.
    """
    pyautogui.rightClick(x, y)

def type_text(text):
    """
    Types text faster (interval 0.05).
    """
    pyautogui.write(text, interval=0.05)

def press_key(key):
    pyautogui.press(key)

def hotkey(*args):
    pyautogui.hotkey(*args)

def move_to(x, y):
    """
    Instant mouse movement (duration 0).
    """
    pyautogui.moveTo(x, y, duration=0)

def get_screen_size():
    return pyautogui.size()

def launch_resolve(executable_path=None):
    if not executable_path:
        if sys.platform == 'win32':
            executable_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
        elif sys.platform == 'darwin':
            executable_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve"
        elif sys.platform == 'linux':
            executable_path = "/opt/resolve/bin/resolve"

    if executable_path and os.path.exists(executable_path):
        print(f"Launching Resolve (BOOSTED)...")
        subprocess.Popen([executable_path])
        return True
    return False

def wait_for_window(window_title_part="DaVinci Resolve", timeout=60):
    time.sleep(5) # Reduced wait
    return True

def focus_window():
    if sys.platform == 'win32':
        hotkey('alt', 'tab')
    elif sys.platform == 'darwin':
        hotkey('command', 'tab')
