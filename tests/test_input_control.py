import sys
from unittest.mock import MagicMock

# Only set mocks if not already set (avoids conflicts when running all tests)
for _mod in ['pyautogui', 'PIL', 'PIL.ImageGrab', 'cv2']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import input_control


class TestInputControl(unittest.TestCase):
    def setUp(self):
        # Use the pyautogui mock that input_control actually references
        self.mock_pyautogui = input_control.pyautogui
        self.mock_pyautogui.reset_mock()

    def test_click(self):
        input_control.click(100, 200)
        self.mock_pyautogui.click.assert_called_once_with(100, 200)

    def test_click_origin(self):
        input_control.click(0, 0)
        self.mock_pyautogui.click.assert_called_once_with(0, 0)

    def test_type_text(self):
        input_control.type_text("hello world")
        self.mock_pyautogui.write.assert_called_once_with("hello world", interval=0.1)

    def test_type_text_empty(self):
        input_control.type_text("")
        self.mock_pyautogui.write.assert_called_once_with("", interval=0.1)

    def test_press_key_enter(self):
        input_control.press_key('enter')
        self.mock_pyautogui.press.assert_called_once_with('enter')

    def test_press_key_escape(self):
        input_control.press_key('esc')
        self.mock_pyautogui.press.assert_called_once_with('esc')

    def test_press_key_space(self):
        input_control.press_key('space')
        self.mock_pyautogui.press.assert_called_once_with('space')

    def test_hotkey_single(self):
        input_control.hotkey('enter')
        self.mock_pyautogui.hotkey.assert_called_once_with('enter')

    def test_hotkey_two_keys(self):
        input_control.hotkey('ctrl', 's')
        self.mock_pyautogui.hotkey.assert_called_once_with('ctrl', 's')

    def test_hotkey_three_keys(self):
        input_control.hotkey('ctrl', 'shift', 'z')
        self.mock_pyautogui.hotkey.assert_called_once_with('ctrl', 'shift', 'z')

    def test_move_to(self):
        input_control.move_to(50, 75)
        self.mock_pyautogui.moveTo.assert_called_once_with(50, 75, duration=0.2)

    def test_move_to_origin(self):
        input_control.move_to(0, 0)
        self.mock_pyautogui.moveTo.assert_called_once_with(0, 0, duration=0.2)

    def test_failsafe_enabled(self):
        self.assertTrue(self.mock_pyautogui.FAILSAFE)


if __name__ == "__main__":
    unittest.main()
