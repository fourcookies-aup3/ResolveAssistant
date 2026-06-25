import sys
from unittest.mock import MagicMock, patch
import unittest.mock

# Only set mocks if not already set
for _mod in ['pyautogui', 'PIL', 'PIL.ImageGrab', 'cv2']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
import editor_actions
import input_control


class TestEditorActionsAPI(unittest.TestCase):
    """Tests for editor_actions with API available (Studio mode)."""

    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None
        self.mock_pyautogui = input_control.pyautogui
        self.mock_pyautogui.reset_mock()

    def test_create_new_project_api(self):
        result = editor_actions.create_new_project("APIProject")
        self.assertTrue(result)

    def test_import_media_api(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("ImportProject")

        result = editor_actions.import_media(["/path/to/video.mp4"])
        self.assertIsNotNone(result)

    def test_import_media_multiple_files(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("MultiImport")

        result = editor_actions.import_media(["/path/a.mp4", "/path/b.mp4"])
        self.assertIsNotNone(result)

    def test_create_timeline_api(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("TimelineProj")

        result = editor_actions.create_timeline("MyTimeline")
        self.assertIsNotNone(result)

    def test_list_clips_in_media_pool_empty(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("EmptyPool")

        clips = editor_actions.list_clips_in_media_pool()
        self.assertEqual(clips, [])

    def test_list_clips_in_media_pool_with_clips(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("ClipPool")
        ms = resolve.GetMediaStorage()
        ms.AddItemListToMediaPool(["/path/clip1.mp4"])

        clips = editor_actions.list_clips_in_media_pool()
        self.assertEqual(len(clips), 1)

    def test_add_clips_to_timeline_api(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("AddClipsProj")
        ms = resolve.GetMediaStorage()
        ms.AddItemListToMediaPool(["/path/clip1.mp4"])
        project = pm.GetCurrentProject()
        project.GetMediaPool().CreateEmptyTimeline("TL1")

        result = editor_actions.add_clips_to_timeline(["clip1.mp4"])
        self.assertTrue(result)

    def test_add_clips_to_timeline_creates_timeline_if_missing(self):
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("NoTLProj")
        ms = resolve.GetMediaStorage()
        ms.AddItemListToMediaPool(["/path/clip1.mp4"])

        result = editor_actions.add_clips_to_timeline(["clip1.mp4"])
        self.assertTrue(result)

    def test_switch_to_page_api(self):
        result = editor_actions.switch_to_page("edit")
        self.assertTrue(result)
        self.mock_pyautogui.hotkey.assert_called()

    def test_switch_to_page_all_pages(self):
        pages = ['media', 'cut', 'edit', 'fusion', 'color', 'fairlight', 'deliver']
        for page in pages:
            self.mock_pyautogui.reset_mock()
            resolve_proxy._resolve_instance = None
            result = editor_actions.switch_to_page(page)
            self.assertTrue(result)
            self.mock_pyautogui.hotkey.assert_called()

    def test_switch_to_page_unknown(self):
        self.mock_pyautogui.reset_mock()
        result = editor_actions.switch_to_page("unknown_page")
        self.assertTrue(result)
        self.mock_pyautogui.hotkey.assert_not_called()

    def test_save_project(self):
        result = editor_actions.save_project()
        self.assertTrue(result)
        self.mock_pyautogui.hotkey.assert_called()

    def test_render_project(self):
        with patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            result = editor_actions.render_project()
            self.assertTrue(result)
            mock_click.assert_called_once_with('start_render')

    def test_render_project_button_not_found(self):
        with patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = False
            result = editor_actions.render_project()
            self.assertFalse(result)

    def test_click_ui_element_found(self):
        with patch('vision.find_image_on_screen') as mock_find:
            mock_find.return_value = (100, 200)
            result = editor_actions.click_ui_element('save_button')
            self.assertTrue(result)
            self.mock_pyautogui.click.assert_called_with(100, 200)

    def test_click_ui_element_not_found(self):
        with patch('vision.find_image_on_screen') as mock_find:
            mock_find.return_value = None
            result = editor_actions.click_ui_element('missing_button')
            self.assertFalse(result)

    def tearDown(self):
        resolve_proxy._resolve_instance = None


class TestEditorActionsFallback(unittest.TestCase):
    """Tests for editor_actions with API unavailable (Free version fallback)."""

    def setUp(self):
        os.environ["RESOLVE_API_UNAVAILABLE"] = "true"
        resolve_proxy._resolve_instance = None
        self.mock_pyautogui = input_control.pyautogui
        self.mock_pyautogui.reset_mock()

    def test_create_new_project_fallback(self):
        with patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = True
            result = editor_actions.create_new_project("FreeProject")
            self.assertTrue(result)
            self.mock_pyautogui.hotkey.assert_any_call('shift', '1')

    def test_create_new_project_fallback_click_fails(self):
        with patch('editor_actions.click_ui_element') as mock_click:
            mock_click.return_value = False
            result = editor_actions.create_new_project("FailProject")
            self.assertFalse(result)

    def test_import_media_fallback_linux(self):
        with patch.object(editor_actions, 'sys') as mock_sys:
            mock_sys.platform = 'linux'
            self.mock_pyautogui.reset_mock()
            result = editor_actions.import_media(["/path/to/video.mp4"])
            self.assertTrue(result)
            self.mock_pyautogui.hotkey.assert_any_call('ctrl', 'i')

    def test_import_media_fallback_mac(self):
        with patch.object(editor_actions, 'sys') as mock_sys:
            mock_sys.platform = 'darwin'
            self.mock_pyautogui.reset_mock()
            result = editor_actions.import_media(["/path/to/video.mp4"])
            self.assertTrue(result)
            self.mock_pyautogui.hotkey.assert_any_call('command', 'i')

    def test_create_timeline_fallback_linux(self):
        with patch.object(editor_actions, 'sys') as mock_sys:
            mock_sys.platform = 'linux'
            self.mock_pyautogui.reset_mock()
            result = editor_actions.create_timeline("FreeTL")
            self.assertTrue(result)
            self.mock_pyautogui.hotkey.assert_any_call('ctrl', 'n')

    def test_create_timeline_fallback_mac(self):
        with patch.object(editor_actions, 'sys') as mock_sys:
            mock_sys.platform = 'darwin'
            self.mock_pyautogui.reset_mock()
            result = editor_actions.create_timeline("FreeTL")
            self.assertTrue(result)
            self.mock_pyautogui.hotkey.assert_any_call('command', 'n')

    def test_add_clips_to_timeline_fallback(self):
        result = editor_actions.add_clips_to_timeline(["clip1.mp4"])
        self.assertTrue(result)
        self.mock_pyautogui.press.assert_any_call('f12')

    def test_list_clips_no_api(self):
        clips = editor_actions.list_clips_in_media_pool()
        self.assertEqual(clips, [])

    def tearDown(self):
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        os.environ["USE_MOCK_RESOLVE"] = "true"
        resolve_proxy._resolve_instance = None


if __name__ == "__main__":
    unittest.main()
