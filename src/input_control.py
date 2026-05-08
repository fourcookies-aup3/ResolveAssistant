import pyautogui
import subprocess
import os
import sys
import time

# Safety features
pyautogui.FAILSAFE = True
# Slow down actions for live viewing
pyautogui.PAUSE = 1.0 # Significant pause between actions for visibility

def click(x, y):
    """
    Moves to and clicks at the specified coordinates.
    """
    move_to(x, y)
    pyautogui.click()

def type_text(text):
    """
    Types the specified text slowly for visibility.
    """
    pyautogui.write(text, interval=0.15)

def press_key(key):
    """
    Presses a specific key.
    """
    pyautogui.press(key)

def hotkey(*args):
    """
    Presses a combination of keys.
    """
    pyautogui.hotkey(*args)

def move_to(x, y):
    """
    Moves the mouse to specified coordinates with a visible duration.
    """
    pyautogui.moveTo(x, y, duration=0.8)

def launch_resolve(executable_path=None):
    """
    Launches DaVinci Resolve based on provided path or default OS paths.
    """
    if not executable_path:
        if sys.platform == 'win32':
            executable_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
        elif sys.platform == 'darwin':
            executable_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve"
        elif sys.platform == 'linux':
            executable_path = "/opt/resolve/bin/resolve"

    if executable_path and os.path.exists(executable_path):
        print(f"Launching DaVinci Resolve from {executable_path}...")
        subprocess.Popen([executable_path])
        return True
    else:
        print(f"Error: Could not find Resolve executable at {executable_path}.")
        return False

def wait_for_window(window_title_part="DaVinci Resolve", timeout=60):
    """
    Waits for a window with the given title to appear.
    """
    print(f"Waiting for {window_title_part} to open...")
    time.sleep(10) # Give it some initial time
    return True

def focus_window():
    """
    Attempts to bring DaVinci Resolve to the foreground.
    """
    print("Focusing DaVinci Resolve...")
    if sys.platform == 'win32':
        hotkey('alt', 'tab')
    elif sys.platform == 'darwin':
        hotkey('command', 'tab')
    time.sleep(1)
