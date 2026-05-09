import sys
from unittest.mock import MagicMock

# Mock Setup
mock_pyautogui = MagicMock()
mock_pil = MagicMock()
mock_cv2 = MagicMock()
mock_tesseract = MagicMock()

import numpy as np
mock_cv2.threshold.return_value = (None, np.zeros((10,10)))
mock_cv2.cvtColor.return_value = np.zeros((10,10))
mock_tesseract.image_to_string.return_value = "Project Manager"

sys.modules['pyautogui'] = mock_pyautogui
sys.modules['PIL'] = mock_pil
sys.modules['PIL.ImageGrab'] = mock_pil.ImageGrab
sys.modules['cv2'] = mock_cv2
sys.modules['pynput'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()
sys.modules['pytesseract'] = mock_tesseract

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions
from ai_agent import AIAgent

class TestFreeVersionSupport(unittest.TestCase):
    def setUp(self):
        os.environ["RESOLVE_API_UNAVAILABLE"] = "true"
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_api_unavailable_detection(self):
        self.assertFalse(resolve_proxy.is_api_available())

    def test_create_project_fallback(self):
        with unittest.mock.patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            result = editor_actions.create_new_project("Free Project")
            self.assertTrue(result)
            mock_pyautogui.hotkey.assert_any_call('shift', '1')

    def test_ai_agent_feedback(self):
        with unittest.mock.patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            response = self.agent.process_command("create project Free Project")
            self.assertIn("(via UI Automation)", response)

if __name__ == "__main__":
    unittest.main()
