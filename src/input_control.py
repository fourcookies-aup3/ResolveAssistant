import pyautogui

# Safety features
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1 # Reduced pause for faster execution

def click(x, y):
    """
    Clicks at the specified coordinates.
    """
    pyautogui.click(x, y)

def type_text(text):
    """
    Types the specified text.
    """
    pyautogui.write(text, interval=0.1)

def press_key(key):
    """
    Presses a specific key (e.g., 'enter', 'esc', 'space').
    """
    pyautogui.press(key)

def hotkey(*args):
    """
    Presses a combination of keys (e.g., 'ctrl', 's').
    """
    pyautogui.hotkey(*args)

def move_to(x, y):
    """
    Moves the mouse to specified coordinates.
    """
    pyautogui.moveTo(x, y, duration=0) # Instant movement
