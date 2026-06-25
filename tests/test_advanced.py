import test_helpers  # noqa: F401 — shared mock setup for GUI libs and src path

import os
import unittest
from unittest.mock import MagicMock

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
        # Setup mock for ImageGrab.grab()
        import PIL.ImageGrab
        mock_img = MagicMock()
        mock_img.__array__ = MagicMock(return_value=np.zeros((100, 100, 3), dtype=np.uint8))
        PIL.ImageGrab.grab.return_value = mock_img

        # Setup cv2.cvtColor mock
        import cv2
        cv2.cvtColor.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

        img = vision.capture_screen()
        self.assertIsNotNone(img)
        self.assertEqual(img.shape, (100, 100, 3))

    def test_input_click(self):
        import pyautogui
        input_control.click(10, 20)
        pyautogui.click.assert_called_once_with(10, 20)

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
