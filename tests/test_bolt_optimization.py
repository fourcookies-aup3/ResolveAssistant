import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
import resolve_proxy

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        # Reset mock instance
        resolve_proxy._resolve_instance = None
        self.resolve = resolve_proxy.get_resolve()
        self.pm = self.resolve.GetProjectManager()
        self.project = self.pm.CreateProject("TestOptimizationProject")

    def test_add_clips_to_timeline_performance_logic(self):
        # Create a pool with duplicate names to verify first-match behavior
        ms = self.resolve.GetMediaStorage()

        # We need to mock the clips to have different 'identities' but same names
        clip1 = resolve_proxy.MockMediaPoolItem("path/to/clip_a.mp4")
        clip2 = resolve_proxy.MockMediaPoolItem("other/path/to/clip_a.mp4")

        # Manually inject them into the mock media pool
        root = self.project.GetMediaPool().GetRootFolder()
        root.clips = [clip1, clip2]

        # Test finding by name
        with patch.object(self.project.GetMediaPool(), 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["clip_a.mp4"])

            # Should have appended clip1 (the first match)
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(len(args), 1)
            self.assertEqual(args[0], clip1)

    def test_add_clips_to_timeline_basename_matching(self):
        # Test matching by basename when GetName() might be different or for path-based matching
        clip = resolve_proxy.MockMediaPoolItem("absolute/path/video.mp4")
        # In our mock, GetName returns basename, but let's ensure it works via the hasattr(clip, 'path') logic

        root = self.project.GetMediaPool().GetRootFolder()
        root.clips = [clip]

        with patch.object(self.project.GetMediaPool(), 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video.mp4"])
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(args[0], clip)

    def test_multiple_clips_selection(self):
        ms = self.resolve.GetMediaStorage()
        clips = ms.AddItemListToMediaPool(["c1.mp4", "c2.mp4", "c3.mp4"])

        with patch.object(self.project.GetMediaPool(), 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["c1.mp4", "c3.mp4"])
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(len(args), 2)
            self.assertEqual(args[0].GetName(), "c1.mp4")
            self.assertEqual(args[1].GetName(), "c3.mp4")

if __name__ == "__main__":
    unittest.main()
