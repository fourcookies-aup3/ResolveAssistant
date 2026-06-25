import sys
from unittest.mock import MagicMock, patch

# Only set mocks if not already set
for _mod in ['pyautogui', 'PIL', 'PIL.ImageGrab', 'cv2']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy
from resolve_proxy import (
    MockResolve, MockProjectManager, MockProject, MockMediaPool,
    MockFolder, MockTimeline, MockMediaStorage, MockMediaPoolItem,
    get_resolve, is_api_available,
)


class TestMockResolve(unittest.TestCase):
    def test_init_api_available(self):
        resolve = MockResolve(is_api_available=True)
        self.assertTrue(resolve.is_api_available)
        self.assertIsNotNone(resolve.project_manager)
        self.assertIsNotNone(resolve.media_storage)

    def test_init_api_unavailable(self):
        resolve = MockResolve(is_api_available=False)
        self.assertFalse(resolve.is_api_available)
        self.assertIsNone(resolve.project_manager)
        self.assertIsNone(resolve.media_storage)

    def test_get_project_manager(self):
        resolve = MockResolve(is_api_available=True)
        pm = resolve.GetProjectManager()
        self.assertIsInstance(pm, MockProjectManager)

    def test_get_media_storage(self):
        resolve = MockResolve(is_api_available=True)
        ms = resolve.GetMediaStorage()
        self.assertIsInstance(ms, MockMediaStorage)

    def test_fusion_api_available(self):
        resolve = MockResolve(is_api_available=True)
        self.assertEqual(resolve.Fusion(), "MockFusion")

    def test_fusion_api_unavailable(self):
        resolve = MockResolve(is_api_available=False)
        self.assertIsNone(resolve.Fusion())

    def test_open_page_api_available(self):
        resolve = MockResolve(is_api_available=True)
        resolve.OpenPage("edit")  # should not raise

    def test_open_page_api_unavailable(self):
        resolve = MockResolve(is_api_available=False)
        resolve.OpenPage("edit")  # should not raise


class TestMockProjectManager(unittest.TestCase):
    def setUp(self):
        self.pm = MockProjectManager()

    def test_create_project(self):
        project = self.pm.CreateProject("TestProject")
        self.assertIsInstance(project, MockProject)
        self.assertEqual(project.name, "TestProject")

    def test_create_duplicate_project(self):
        self.pm.CreateProject("Dup")
        result = self.pm.CreateProject("Dup")
        self.assertIsNone(result)

    def test_get_current_project(self):
        self.assertIsNone(self.pm.GetCurrentProject())
        self.pm.CreateProject("Proj1")
        self.assertIsNotNone(self.pm.GetCurrentProject())
        self.assertEqual(self.pm.GetCurrentProject().name, "Proj1")

    def test_load_project_exists(self):
        self.pm.CreateProject("LoadMe")
        self.pm.CreateProject("Other")
        result = self.pm.LoadProject("LoadMe")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "LoadMe")
        self.assertEqual(self.pm.GetCurrentProject().name, "LoadMe")

    def test_load_project_not_found(self):
        result = self.pm.LoadProject("Nonexistent")
        self.assertIsNone(result)


class TestMockProject(unittest.TestCase):
    def setUp(self):
        self.project = MockProject("TestProject")

    def test_get_media_pool(self):
        mp = self.project.GetMediaPool()
        self.assertIsInstance(mp, MockMediaPool)

    def test_get_timeline_count_empty(self):
        self.assertEqual(self.project.GetTimelineCount(), 0)

    def test_get_timeline_count_with_timelines(self):
        tl1 = MockTimeline("TL1")
        tl2 = MockTimeline("TL2")
        self.project.timelines.append(tl1)
        self.project.timelines.append(tl2)
        self.assertEqual(self.project.GetTimelineCount(), 2)

    def test_get_current_timeline_empty(self):
        self.assertIsNone(self.project.GetCurrentTimeline())

    def test_get_current_timeline_first(self):
        tl = MockTimeline("TL1")
        self.project.timelines.append(tl)
        self.assertEqual(self.project.GetCurrentTimeline(), tl)

    def test_set_current_timeline_success(self):
        tl1 = MockTimeline("TL1")
        tl2 = MockTimeline("TL2")
        self.project.timelines = [tl1, tl2]
        result = self.project.SetCurrentTimeline(tl2)
        self.assertTrue(result)
        self.assertEqual(self.project.timelines[0], tl2)

    def test_set_current_timeline_not_found(self):
        tl = MockTimeline("TL1")
        result = self.project.SetCurrentTimeline(tl)
        self.assertFalse(result)


class TestMockMediaPool(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None

    def test_get_root_folder(self):
        mp = MockMediaPool()
        root = mp.GetRootFolder()
        self.assertIsInstance(root, MockFolder)
        self.assertEqual(root.name, "Root")

    def test_create_empty_timeline(self):
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject("TimelineProject")
        mp = project.GetMediaPool()

        tl = mp.CreateEmptyTimeline("MyTimeline")
        self.assertIsInstance(tl, MockTimeline)
        self.assertEqual(tl.name, "MyTimeline")
        self.assertIn(tl, project.timelines)

    def test_append_to_timeline(self):
        mp = MockMediaPool()
        result = mp.AppendToTimeline(["clip1", "clip2"])
        self.assertTrue(result)

    def tearDown(self):
        resolve_proxy._resolve_instance = None


class TestMockFolder(unittest.TestCase):
    def test_get_clip_list_empty(self):
        folder = MockFolder("TestFolder")
        self.assertEqual(folder.GetClipList(), [])

    def test_get_clip_list_with_clips(self):
        folder = MockFolder("TestFolder")
        clip = MockMediaPoolItem("/path/to/clip.mp4")
        folder.clips.append(clip)
        clips = folder.GetClipList()
        self.assertEqual(len(clips), 1)
        self.assertEqual(clips[0].GetName(), "clip.mp4")


class TestMockMediaStorage(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None

    def test_add_item_list_to_media_pool(self):
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("StorageProject")
        ms = resolve.GetMediaStorage()

        clips = ms.AddItemListToMediaPool(["/path/clip1.mp4", "/path/clip2.mp4"])
        self.assertEqual(len(clips), 2)
        self.assertEqual(clips[0].GetName(), "clip1.mp4")

    def test_add_single_string_item(self):
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        pm.CreateProject("SingleItem")
        ms = resolve.GetMediaStorage()

        clips = ms.AddItemListToMediaPool("/path/single.mp4")
        self.assertEqual(len(clips), 1)
        self.assertEqual(clips[0].GetName(), "single.mp4")

    def tearDown(self):
        resolve_proxy._resolve_instance = None


class TestMockMediaPoolItem(unittest.TestCase):
    def test_get_name(self):
        item = MockMediaPoolItem("/some/path/video.mp4")
        self.assertEqual(item.GetName(), "video.mp4")

    def test_get_name_nested_path(self):
        item = MockMediaPoolItem("/a/b/c/d/movie.mov")
        self.assertEqual(item.GetName(), "movie.mov")

    def test_path_attribute(self):
        item = MockMediaPoolItem("/my/file.mp4")
        self.assertEqual(item.path, "/my/file.mp4")


class TestGetResolve(unittest.TestCase):
    def setUp(self):
        resolve_proxy._resolve_instance = None

    def test_mock_resolve_enabled(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        result = get_resolve()
        self.assertIsInstance(result, MockResolve)
        self.assertTrue(result.is_api_available)

    def test_api_unavailable_env(self):
        os.environ["RESOLVE_API_UNAVAILABLE"] = "true"
        resolve_proxy._resolve_instance = None
        result = get_resolve()
        self.assertIsInstance(result, MockResolve)
        self.assertFalse(result.is_api_available)

    def test_cached_instance(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None
        first = get_resolve()
        second = get_resolve()
        self.assertIs(first, second)

    def tearDown(self):
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        os.environ["USE_MOCK_RESOLVE"] = "true"
        resolve_proxy._resolve_instance = None


class TestIsApiAvailable(unittest.TestCase):
    def setUp(self):
        resolve_proxy._resolve_instance = None

    def test_api_available_mock(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        self.assertTrue(is_api_available())

    def test_api_unavailable_mock(self):
        os.environ["RESOLVE_API_UNAVAILABLE"] = "true"
        resolve_proxy._resolve_instance = None
        self.assertFalse(is_api_available())

    def test_none_resolve_returns_false(self):
        # When get_resolve returns None, is_api_available should return False
        with patch('resolve_proxy.get_resolve', return_value=None):
            self.assertFalse(is_api_available())

    def tearDown(self):
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        os.environ["USE_MOCK_RESOLVE"] = "true"
        resolve_proxy._resolve_instance = None


if __name__ == "__main__":
    unittest.main()
