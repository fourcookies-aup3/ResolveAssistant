import sys
from unittest.mock import MagicMock

# Mock GUI and input libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import vision
import input_control
import editor_actions
from ai_agent import AIAgent

class TestAdvancedFeatures(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.agent = AIAgent()

    def test_vision_capture(self):
        import numpy as np
        import PIL.ImageGrab
        mock_img = MagicMock()
        mock_img.__array__ = MagicMock(return_value=np.zeros((100, 100, 3), dtype=np.uint8))
        PIL.ImageGrab.grab.return_value = mock_img

        import cv2
        cv2.cvtColor.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

        img = vision.capture_screen()
        self.assertIsNotNone(img)
        self.assertEqual(img.shape, (100, 100, 3))

    def test_input_click(self):
        import pyautogui
        input_control.click(10, 20)
        pyautogui.moveTo.assert_called_once_with(10, 20, duration=unittest.mock.ANY)
        pyautogui.click.assert_called_once()

    def test_ai_click_command(self):
        with unittest.mock.patch('editor_actions.click_ui_element') as mock_click_ui:
            mock_click_ui.return_value = True
            response = self.agent.process_command("click save_button")
            self.assertIn("Clicked save_button", response)
            mock_click_ui.assert_called_once_with("save_button")

    def test_save_project_action(self):
        import pyautogui
        editor_actions.save_project()
        pyautogui.hotkey.assert_called()

if __name__ == "__main__":
    unittest.main()
