import pyautogui

# Safety features
pyautogui.FAILSAFE = True

def click(x, y):
    """Clicks at the specified coordinates."""
    try:
        pyautogui.click(x, y)
        return True
    except Exception as e:
        print(f"Error clicking at ({x}, {y}): {e}")
        return False

def type_text(text):
    """Types the specified text."""
    try:
        pyautogui.write(text, interval=0.1)
        return True
    except Exception as e:
        print(f"Error typing text: {e}")
        return False

def press_key(key):
    """Presses a specific key (e.g., 'enter', 'esc', 'space')."""
    try:
        pyautogui.press(key)
        return True
    except Exception as e:
        print(f"Error pressing key '{key}': {e}")
        return False

def hotkey(*args):
    """Presses a combination of keys (e.g., 'ctrl', 's')."""
    try:
        pyautogui.hotkey(*args)
        return True
    except Exception as e:
        print(f"Error pressing hotkey {'+'.join(args)}: {e}")
        return False

def move_to(x, y):
    """Moves the mouse to specified coordinates."""
    try:
        pyautogui.moveTo(x, y, duration=0.2)
        return True
    except Exception as e:
        print(f"Error moving to ({x}, {y}): {e}")
        return False
