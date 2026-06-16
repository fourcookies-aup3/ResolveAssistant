import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['ImageGrab'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath("src"))

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve

class TestBoltOptimization(unittest.TestCase):
    def test_add_clips_to_timeline_optimization(self):
        # Setup mock data
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject("Test Optimization")
        ms = resolve.GetMediaStorage()

        # Create some clips in the media pool
        ms.AddItemListToMediaPool(["/path/to/clip_A.mp4", "/path/to/clip_B.mp4"])

        # Test adding by name
        # We need to mock AppendToTimeline to verify it was called with correct number of clips
        mp = project.GetMediaPool()
        mp.AppendToTimeline = MagicMock(return_value=True)

        result = add_clips_to_timeline(["clip_A.mp4", "clip_B.mp4"])
        self.assertTrue(result)
        mp.AppendToTimeline.assert_called_once()
        args, kwargs = mp.AppendToTimeline.call_args
        self.assertEqual(len(args[0]), 2)

        # Test adding by something that doesn't exist (in API mode)
        mp.AppendToTimeline.reset_mock()
        result = add_clips_to_timeline(["non_existent.mp4"])
        # If no clips found, it shouldn't call AppendToTimeline and return None (due to lack of return if clips_to_add is empty)
        # Wait, looking at the code:
        # if clips_to_add:
        #     return mp.AppendToTimeline(clips_to_add)
        # return None (implicitly)
        self.assertIsNone(result)
        mp.AppendToTimeline.assert_not_called()

if __name__ == "__main__":
    unittest.main()
