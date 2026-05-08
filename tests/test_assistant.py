import sys
import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions
from ai_agent import AIAgent

class TestResolveAssistant(unittest.TestCase):
    def setUp(self):
        # Force mock for testing
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.agent = AIAgent()

    def test_create_project(self):
        result = editor_actions.create_new_project("Test Project")
        self.assertTrue(result)

        # Test creating same project again (should fail in mock)
        result_fail = editor_actions.create_new_project("Test Project")
        self.assertFalse(result_fail)

    def test_ai_process_command(self):
        response = self.agent.process_command("create project AI Project")
        self.assertIn("Created project: AI Project", response)

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
