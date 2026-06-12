import sys
import os
import unittest
from unittest.mock import MagicMock

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
import resolve_proxy

class MockClip:
    def __init__(self, name, path=None):
        self._name = name
        self.path = path
    def GetName(self):
        return self._name

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        # Reset mock resolve state if necessary (though it's fresh per import here)

    def test_add_clips_to_timeline_matching(self):
        # Setup mock resolve
        resolve = resolve_proxy.get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject("Test Match Project")
        mp = project.GetMediaPool()

        # Setup pool with various clips
        clips = [
            MockClip("clip1.mp4", "/path/to/clip1.mp4"),
            MockClip("clip2.mp4"), # No path
            MockClip("other.mov", "/path/to/other.mov")
        ]
        project.GetMediaPool().GetRootFolder().clips = clips

        # Mock AppendToTimeline to verify what it receives
        mp.AppendToTimeline = MagicMock(return_value=True)

        # Test matching by name
        editor_actions.add_clips_to_timeline(["clip1.mp4"])
        mp.AppendToTimeline.assert_called_once()
        matched_clips = mp.AppendToTimeline.call_args[0][0]
        self.assertEqual(len(matched_clips), 1)
        self.assertEqual(matched_clips[0].GetName(), "clip1.mp4")

        mp.AppendToTimeline.reset_mock()

        # Test matching by basename
        editor_actions.add_clips_to_timeline(["other.mov"])
        matched_clips = mp.AppendToTimeline.call_args[0][0]
        self.assertEqual(len(matched_clips), 1)
        self.assertEqual(matched_clips[0].GetName(), "other.mov")

        mp.AppendToTimeline.reset_mock()

        # Test matching multiple
        editor_actions.add_clips_to_timeline(["clip1.mp4", "clip2.mp4", "nonexistent.mp4"])
        matched_clips = mp.AppendToTimeline.call_args[0][0]
        self.assertEqual(len(matched_clips), 2)
        names = [c.GetName() for c in matched_clips]
        self.assertIn("clip1.mp4", names)
        self.assertIn("clip2.mp4", names)

if __name__ == "__main__":
    unittest.main()
