import test_helpers  # noqa: F401 — shared mock setup for GUI libs and src path

import os
import unittest

import resolve_proxy
import editor_actions
from ai_agent import AIAgent

class TestFreeVersionSupport(unittest.TestCase):
    def setUp(self):
        # Force API Unavailable for these tests
        os.environ["RESOLVE_API_UNAVAILABLE"] = "true"
        # Reset the resolve instance
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_api_unavailable_detection(self):
        self.assertFalse(resolve_proxy.is_api_available())

    def test_create_project_fallback(self):
        import pyautogui
        # We need to mock click_ui_element because it tries to find an image
        with unittest.mock.patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            result = editor_actions.create_new_project("Free Project")
            self.assertTrue(result)
            # Verify hotkey was called (Shift+1 to open project manager)
            pyautogui.hotkey.assert_any_call('shift', '1')

    def test_ai_agent_feedback(self):
        with unittest.mock.patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            response = self.agent.process_command("create project Free Project")
            self.assertIn("(via UI Automation)", response)

if __name__ == "__main__":
    unittest.main()
