import sys
from unittest.mock import MagicMock

# Global Setup Mocks
mock_pyautogui = MagicMock()
mock_pil = MagicMock()
mock_cv2 = MagicMock()
mock_tesseract = MagicMock()

# Ensure cv2 functions return valid shapes
import numpy as np
mock_cv2.threshold.return_value = (None, np.zeros((10,10)))
mock_cv2.cvtColor.return_value = np.zeros((10,10))

sys.modules['pyautogui'] = mock_pyautogui
sys.modules['PIL'] = mock_pil
sys.modules['PIL.ImageGrab'] = mock_pil.ImageGrab
sys.modules['cv2'] = mock_cv2
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()
sys.modules['pytesseract'] = mock_tesseract

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions
from ai_agent import AIAgent

class TestResolveAssistant(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_create_project(self):
        # Setup OCR mock to return 'Project Manager' so wait_for_ui_text passes
        mock_tesseract.image_to_string.return_value = "Project Manager"
        result = editor_actions.create_new_project("Test Project")
        self.assertTrue(result)

        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ["RESOLVE_API_UNAVAILABLE"] = "false"
        result_fail = editor_actions.create_new_project("Test Project")
        self.assertFalse(result_fail)

    def test_ai_process_command(self):
        mock_tesseract.image_to_string.return_value = "video.mp4"
        response = self.agent.process_command("create project AI Project")
        self.assertIn("Created project: AI Project", response)

        response = self.agent.process_command("import /path/to/video.mp4")
        self.assertIn("Imported: /path/to/video.mp4", response)

    def test_execute_plan(self):
        import json
        plan = json.dumps([
            {"function": "create_new_project", "args": ["Plan Project"]},
            {"function": "switch_to_page", "args": ["edit"]}
        ])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")

if __name__ == "__main__":
    unittest.main()
