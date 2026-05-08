import sys
from unittest.mock import MagicMock

# Mock everything related to GUI/OS before any imports
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

import resolve_proxy
import editor_actions
# We must mock AIAgent dependencies inside ai_agent if they fail at import time
# For testing, we can patch the whole module if needed, but here we'll fix the source
from ai_agent import AIAgent

class TestResolveAssistant(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_create_project(self):
        result = editor_actions.create_new_project("Test Project")
        self.assertTrue(result)

        # API fail test
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ["RESOLVE_API_UNAVAILABLE"] = "false"
        result_fail = editor_actions.create_new_project("Test Project")
        self.assertFalse(result_fail)

    def test_ai_process_command(self):
        response = self.agent.process_command("create project AI Project")
        self.assertIn("Created and opened project: AI Project", response)

        response = self.agent.process_command("import /path/to/video.mp4")
        self.assertIn("Imported media from: /path/to/video.mp4", response)

    def test_execute_plan(self):
        import json
        plan = json.dumps([
            {"function": "create_new_project", "args": ["Plan Project"]},
            {"function": "create_timeline", "args": ["Plan Timeline"]}
        ])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(results[1]["status"], "success")

if __name__ == "__main__":
    unittest.main()
