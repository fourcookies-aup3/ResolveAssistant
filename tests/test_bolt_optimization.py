import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock GUI modules to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

sys.path.append(os.path.abspath("src"))
import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        # Reset the mock resolve instance to clear state
        import resolve_proxy
        resolve_proxy._resolve_instance = None
        self.resolve = get_resolve()

    def test_add_clips_to_timeline_optimized(self):
        pm = self.resolve.GetProjectManager()
        project = pm.CreateProject("Test Project")
        mp = project.GetMediaPool()

        # Setup clips with different naming scenarios
        clip1 = MockMediaPoolItem("/path/to/video1.mp4") # name: video1.mp4, basename: video1.mp4
        clip2 = MockMediaPoolItem("/other/path/video2.mov") # name: video2.mov, basename: video2.mov

        # Manually set name different from basename if we wanted to test that,
        # but MockMediaPoolItem.GetName() returns basename.

        mp.GetRootFolder().clips = [clip1, clip2]

        # Test finding by name/basename
        with unittest.mock.patch.object(mp, 'AppendToTimeline', return_value=True) as mock_append:
            result = editor_actions.add_clips_to_timeline(["video1.mp4", "video2.mov", "nonexistent.mp4"])
            self.assertTrue(result)

            # Verify correct clips were added
            args, kwargs = mock_append.call_args
            added_clips = args[0]
            self.assertEqual(len(added_clips), 2)
            self.assertIn(clip1, added_clips)
            self.assertIn(clip2, added_clips)

    def test_add_clips_to_timeline_preserves_first_match(self):
        pm = self.resolve.GetProjectManager()
        project = pm.CreateProject("Test Project 2")
        mp = project.GetMediaPool()

        clip1 = MockMediaPoolItem("/path/A/duplicate.mp4")
        clip2 = MockMediaPoolItem("/path/B/duplicate.mp4")

        mp.GetRootFolder().clips = [clip1, clip2]

        with unittest.mock.patch.object(mp, 'AppendToTimeline', return_value=True) as mock_append:
            editor_actions.add_clips_to_timeline(["duplicate.mp4"])

            args, kwargs = mock_append.call_args
            added_clips = args[0]
            self.assertEqual(len(added_clips), 1)
            self.assertIs(added_clips[0], clip1) # Should be the first one found

if __name__ == "__main__":
    unittest.main()
