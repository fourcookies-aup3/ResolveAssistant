import sys
from unittest.mock import MagicMock

# Mock GUI libraries for tests that don't need them
sys.modules["pyautogui"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.ImageGrab"] = MagicMock()
sys.modules["cv2"] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)

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

        plan = json.dumps(
            [
                {"function": "create_new_project", "args": ["Plan Project"]},
                {"function": "create_timeline", "args": ["Plan Timeline"]},
            ]
        )
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(results[1]["status"], "success")

    def test_add_clips_to_timeline_optimization(self):
        # Create a mock environment
        resolve_proxy._resolve_instance = None
        os.environ["USE_MOCK_RESOLVE"] = "true"

        # Build list of clips with duplicates to assert first-match behavior
        class FakeClip:
            def __init__(self, name, path=None):
                self.name = name
                self.path = path

            def GetName(self):
                return self.name

        clip_first = FakeClip("my_clip", "/path/to/first.mp4")
        clip_second = FakeClip("my_clip", "/path/to/second.mp4")
        clip_no_path = FakeClip("no_path_clip", None)

        mock_clips = [clip_first, clip_second, clip_no_path]

        # Patch list_clips_in_media_pool
        original_list = editor_actions.list_clips_in_media_pool
        editor_actions.list_clips_in_media_pool = lambda: mock_clips

        try:
            # We must set current project & active timeline
            resolve = resolve_proxy.get_resolve()
            pm = resolve.GetProjectManager()
            project = pm.CreateProject("Optimized Project")

            # Let's perform add_clips_to_timeline
            # It should add 'clip_first' because of first-match behavior,
            # and 'clip_no_path' even without a path.
            # Let's intercept AppendToTimeline
            appended_clips = []
            def mock_append(clips):
                appended_clips.extend(clips)
                return True
            project.media_pool.AppendToTimeline = mock_append

            success = editor_actions.add_clips_to_timeline(
                ["my_clip", "no_path_clip"]
            )
            self.assertTrue(success)
            self.assertEqual(len(appended_clips), 2)
            self.assertIs(appended_clips[0], clip_first)
            self.assertIs(appended_clips[1], clip_no_path)

        finally:
            editor_actions.list_clips_in_media_pool = original_list


if __name__ == "__main__":
    unittest.main()
