import unittest
from unittest.mock import MagicMock
import sys
import os

# Mocking necessary modules
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

# Mocking resolve_proxy
sys.modules['resolve_proxy'] = MagicMock()
import resolve_proxy
resolve_proxy.is_api_available.return_value = True

# Mocking GetResolve
mock_resolve = MagicMock()
resolve_proxy.get_resolve.return_value = mock_resolve

# Set up mock project and media pool
mock_project = MagicMock()
mock_resolve.GetProjectManager().GetCurrentProject.return_value = mock_project
mock_mp = MagicMock()
mock_project.GetMediaPool.return_value = mock_mp

# Add src to path
sys.path.append(os.path.abspath('src'))

import editor_actions

class TestBoltOptimization(unittest.TestCase):

    def setUp(self):
        mock_mp.AppendToTimeline.reset_mock()

    def test_add_clips_to_timeline_optimization(self):
        # Create mock clips
        clip1 = MagicMock()
        clip1.GetName.return_value = "clip1.mp4"
        clip1.path = "/path/to/clip1.mp4"

        clip2 = MagicMock()
        clip2.GetName.return_value = "clip2.mp4"
        clip2.path = "/path/to/clip2.mp4"

        # Second clip with same name but different path (to test first-match)
        clip1_duplicate = MagicMock()
        clip1_duplicate.GetName.return_value = "clip1.mp4"
        clip1_duplicate.path = "/other/path/clip1.mp4"

        all_clips = [clip1, clip2, clip1_duplicate]

        # Mock list_clips_in_media_pool
        editor_actions.list_clips_in_media_pool = lambda: all_clips

        # Target names
        target_names = ["clip1.mp4", "clip2.mp4"]

        # Run the optimized function
        editor_actions.add_clips_to_timeline(target_names)

        # Verify AppendToTimeline was called with the correct clips
        # It should pick the FIRST clip1, not the duplicate.
        mock_mp.AppendToTimeline.assert_called_once()
        clips_added = mock_mp.AppendToTimeline.call_args[0][0]

        self.assertEqual(len(clips_added), 2)
        self.assertEqual(clips_added[0], clip1)
        self.assertEqual(clips_added[1], clip2)

    def test_add_clips_to_timeline_by_path(self):
        # Test finding by basename of path
        clip = MagicMock()
        clip.GetName.return_value = "DifferentName"
        clip.path = "/path/to/my_video.mov"

        editor_actions.list_clips_in_media_pool = lambda: [clip]

        editor_actions.add_clips_to_timeline(["my_video.mov"])

        mock_mp.AppendToTimeline.assert_called_once()
        clips_added = mock_mp.AppendToTimeline.call_args[0][0]
        self.assertEqual(clips_added[0], clip)

if __name__ == "__main__":
    unittest.main()
