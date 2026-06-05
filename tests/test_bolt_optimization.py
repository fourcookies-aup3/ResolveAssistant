import sys
from unittest.mock import MagicMock, patch

# Mock GUI libraries for tests that don't need them
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Force mock for testing
os.environ["USE_MOCK_RESOLVE"] = "true"

import editor_actions

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        # Reset MockResolve instance
        import resolve_proxy
        resolve_proxy._resolve_instance = None

    def test_add_clips_to_timeline_functionality(self):
        """Verify that the optimized add_clips_to_timeline still correctly identifies and adds clips."""
        resolve = editor_actions.get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject("Test Project")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()

        # Create mock clips
        clip1 = MagicMock()
        clip1.GetName.return_value = "video1.mp4"
        clip1.path = "/path/to/video1.mp4"

        clip2 = MagicMock()
        clip2.GetName.return_value = "video2.mp4"
        clip2.path = "/path/to/video2.mp4"

        root_folder.clips.extend([clip1, clip2])

        # Test adding by name
        with patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video1.mp4"])
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(len(args), 1)
            self.assertEqual(args[0], clip1)

        # Test adding by path basename
        with patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video2.mp4"])
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(len(args), 1)
            self.assertEqual(args[0], clip2)

        # Test adding multiple clips
        with patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["video1.mp4", "video2.mp4"])
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(len(args), 2)
            self.assertIn(clip1, args)
            self.assertIn(clip2, args)

        # Test adding non-existent clip
        with patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["nonexistent.mp4"])
            mock_append.assert_not_called()

if __name__ == "__main__":
    unittest.main()
