import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        # Reset the resolve instance to get a fresh mock project
        import resolve_proxy
        resolve_proxy._resolve_instance = None

    def test_add_clips_to_timeline_optimized(self):
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject("Test Project")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()

        # Setup clips with names and paths
        clip1 = MockMediaPoolItem("path/to/video1.mp4")
        clip2 = MockMediaPoolItem("path/to/video2.mp4")
        root_folder.clips.extend([clip1, clip2])

        # Test finding by name
        with unittest.mock.patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video1.mp4"])
            mock_append.assert_called_once()
            added_clips = mock_append.call_args[0][0]
            self.assertEqual(len(added_clips), 1)
            self.assertEqual(added_clips[0].GetName(), "video1.mp4")

    def test_add_clips_to_timeline_multiple(self):
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject("Test Project Multiple")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()

        clip1 = MockMediaPoolItem("path/to/video1.mp4")
        clip2 = MockMediaPoolItem("path/to/video2.mp4")
        clip3 = MockMediaPoolItem("path/to/video3.mp4")
        root_folder.clips.extend([clip1, clip2, clip3])

        with unittest.mock.patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video1.mp4", "video3.mp4"])
            mock_append.assert_called_once()
            added_clips = mock_append.call_args[0][0]
            self.assertEqual(len(added_clips), 2)
            self.assertIn(clip1, added_clips)
            self.assertIn(clip3, added_clips)

if __name__ == "__main__":
    unittest.main()
