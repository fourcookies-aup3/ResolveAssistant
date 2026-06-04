import sys
import os
import unittest
from unittest.mock import MagicMock

# Mock GUI dependencies
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

os.environ["USE_MOCK_RESOLVE"] = "true"
import editor_actions
from resolve_proxy import get_resolve, MockMediaPoolItem

class TestBoltOptimization(unittest.TestCase):
    def test_add_clips_to_timeline_functionality(self):
        resolve = get_resolve()
        # Reset mock state
        resolve.GetProjectManager().projects = {}
        project = resolve.GetProjectManager().CreateProject("Test Optimization")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()

        # Setup clips with and without paths
        clip1 = MockMediaPoolItem("/path/to/video1.mp4")
        clip2 = MockMediaPoolItem("/path/to/video2.mov")
        clip3 = MockMediaPoolItem("") # No path
        clip3.GetName = MagicMock(return_value="audio_only")

        root_folder.clips = [clip1, clip2, clip3]

        # Test finding by full name (basename for file clips)
        with unittest.mock.patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video1.mp4", "audio_only"])

            # Check if correct clips were added
            self.assertEqual(mock_append.call_count, 1)
            added_clips = mock_append.call_args[0][0]
            self.assertEqual(len(added_clips), 2)
            self.assertIn(clip1, added_clips)
            self.assertIn(clip3, added_clips)

    def test_add_clips_to_timeline_no_match(self):
        resolve = get_resolve()
        resolve.GetProjectManager().projects = {}
        project = resolve.GetProjectManager().CreateProject("Test No Match")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()
        root_folder.clips = [MockMediaPoolItem("/path/to/v1.mp4")]

        with unittest.mock.patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["nonexistent.mp4"])
            mock_append.assert_not_called()

if __name__ == "__main__":
    unittest.main()
