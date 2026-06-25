import sys
from unittest.mock import MagicMock, patch
import unittest.mock

# Only set mocks if not already set
for _mod in ['pyautogui', 'PIL', 'PIL.ImageGrab', 'cv2']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import os
import json
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
from ai_agent import AIAgent


class TestAIAgentProcessCommand(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_create_project(self):
        response = self.agent.process_command("create project TestProject")
        self.assertIn("Created project: TestProject", response)
        self.assertIn("(via API)", response)

    def test_import_media(self):
        response = self.agent.process_command("import /videos/clip.mp4")
        self.assertIn("Imported media from: /videos/clip.mp4", response)
        self.assertIn("(via API)", response)

    def test_create_timeline(self):
        response = self.agent.process_command("create timeline My Timeline")
        self.assertIn("Created timeline: My Timeline", response)
        self.assertIn("(via API)", response)

    def test_add_to_timeline(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("AddClipProj")
        ms = resolve.GetMediaStorage()
        ms.AddItemListToMediaPool(["/path/clip1.mp4"])
        project = pm.GetCurrentProject()
        project.GetMediaPool().CreateEmptyTimeline("TL1")

        response = self.agent.process_command("add clip1.mp4 to timeline")
        self.assertIn("to timeline", response)

    def test_add_to_timeline_fallback_when_clip_not_found(self):
        # When clips aren't found via API, it falls through to UI automation
        resolve_proxy._resolve_instance = None
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("EmptyProj")
        project = pm.GetCurrentProject()
        project.GetMediaPool().CreateEmptyTimeline("TL1")

        response = self.agent.process_command("add nonexistent.mp4 to timeline")
        self.assertIn("to timeline", response)

    def test_switch_to_page(self):
        response = self.agent.process_command("switch to edit page")
        self.assertIn("Switched to edit page", response)

    def test_switch_to_color_page(self):
        response = self.agent.process_command("switch to color page")
        self.assertIn("Switched to color page", response)

    def test_save_project(self):
        response = self.agent.process_command("save project")
        self.assertIn("Saving project", response)

    @patch('editor_actions.click_ui_element')
    def test_click_command_success(self, mock_click):
        mock_click.return_value = True
        response = self.agent.process_command("click play_button")
        self.assertIn("Clicked play_button", response)
        mock_click.assert_called_once_with("play_button")

    @patch('editor_actions.click_ui_element')
    def test_click_command_failure(self, mock_click):
        mock_click.return_value = False
        response = self.agent.process_command("click nonexistent_button")
        self.assertIn("Failed to find or click", response)

    @patch('editor_actions.render_project')
    def test_render(self, mock_render):
        mock_render.return_value = True
        response = self.agent.process_command("render")
        self.assertIn("Starting render process", response)
        mock_render.assert_called_once()

    def test_unknown_command(self):
        response = self.agent.process_command("do something random")
        self.assertIn("I'm sorry", response)
        self.assertIn("create project", response)

    def test_case_insensitive_commands(self):
        response = self.agent.process_command("CREATE PROJECT UpperCase")
        self.assertIn("Created project: UpperCase", response)

        response = self.agent.process_command("SAVE PROJECT")
        self.assertIn("Saving project", response)

    def tearDown(self):
        resolve_proxy._resolve_instance = None


class TestAIAgentProcessCommandFreeVersion(unittest.TestCase):
    def setUp(self):
        os.environ["RESOLVE_API_UNAVAILABLE"] = "true"
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_create_project_ui_automation(self):
        with patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            response = self.agent.process_command("create project FreeProject")
            self.assertIn("(via UI Automation)", response)

    def test_import_media_ui_automation(self):
        response = self.agent.process_command("import /path/to/video.mp4")
        self.assertIn("(via UI Automation)", response)

    def test_create_timeline_ui_automation(self):
        response = self.agent.process_command("create timeline FreeTL")
        self.assertIn("(via UI Automation)", response)

    def tearDown(self):
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        os.environ["USE_MOCK_RESOLVE"] = "true"
        resolve_proxy._resolve_instance = None


class TestAIAgentExecutePlan(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None
        self.agent = AIAgent()

    def test_execute_plan_success(self):
        plan = json.dumps([
            {"function": "create_new_project", "args": ["PlanProject"]},
            {"function": "create_timeline", "args": ["PlanTimeline"]},
        ])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(results[1]["status"], "success")

    def test_execute_plan_function_not_found(self):
        plan = json.dumps([
            {"function": "nonexistent_function", "args": []},
        ])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "failed")
        self.assertIn("not found", results[0]["error"])

    def test_execute_plan_mixed(self):
        plan = json.dumps([
            {"function": "create_new_project", "args": ["MixedProject"]},
            {"function": "fake_function", "args": []},
            {"function": "save_project", "args": []},
        ])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(results[1]["status"], "failed")
        self.assertEqual(results[2]["status"], "success")

    def test_execute_plan_with_kwargs(self):
        plan = json.dumps([
            {"function": "switch_to_page", "args": ["edit"], "kwargs": {}},
        ])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "success")

    def test_execute_plan_empty(self):
        plan = json.dumps([])
        results = self.agent.execute_plan(plan)
        self.assertEqual(len(results), 0)

    def tearDown(self):
        resolve_proxy._resolve_instance = None


if __name__ == "__main__":
    unittest.main()
