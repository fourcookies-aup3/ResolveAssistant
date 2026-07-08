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

class MockClip:
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
    def GetName(self):
        return self.name

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        # Reset resolve_proxy state
        resolve_proxy._resolve_instance = None
        if "RESOLVE_API_UNAVAILABLE" in os.environ:
            del os.environ["RESOLVE_API_UNAVAILABLE"]
        os.environ["USE_MOCK_RESOLVE"] = "true"

        self.resolve = resolve_proxy.get_resolve()
        # Create a project so it's not None
        import uuid
        self.project = self.resolve.GetProjectManager().CreateProject(str(uuid.uuid4()))

        # Mock GetClipList to return nothing by default
        self.project.GetMediaPool().GetRootFolder().clips = []

    def test_add_clips_to_timeline_success(self):
        # Setup mock pool
        clips = [
            MockClip("clip1", "/path/to/clip1.mp4"),
            MockClip("clip2", "/path/to/clip2.mp4"),
            MockClip("clip3", "/path/to/clip3.mp4")
        ]
        self.project.GetMediaPool().GetRootFolder().clips = clips

        # Patch AppendToTimeline
        with patch.object(self.project.GetMediaPool(), 'AppendToTimeline', return_value=True) as mock_append:
            # Call function
            editor_actions.add_clips_to_timeline(["clip1", "clip3.mp4"])

            # Verify
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(len(args), 2)
            self.assertEqual(args[0], clips[0])
            self.assertEqual(args[1], clips[2])

    def test_first_match_preservation(self):
        # Setup mock pool with duplicate names
        # We expect the FIRST one in the list to be picked
        clips = [
            MockClip("duplicate", "/path/1"),
            MockClip("duplicate", "/path/2"),
        ]
        self.project.GetMediaPool().GetRootFolder().clips = clips

        # Patch AppendToTimeline
        with patch.object(self.project.GetMediaPool(), 'AppendToTimeline', return_value=True) as mock_append:
            # Call function
            editor_actions.add_clips_to_timeline(["duplicate"])

            # Verify
            mock_append.assert_called_once()
            args = mock_append.call_args[0][0]
            self.assertEqual(args[0], clips[0]) # Should be the first one

    def test_no_match(self):
        self.project.GetMediaPool().GetRootFolder().clips = []

        # Patch AppendToTimeline
        with patch.object(self.project.GetMediaPool(), 'AppendToTimeline', return_value=True) as mock_append:
            # Should not call AppendToTimeline if no clips found
            editor_actions.add_clips_to_timeline(["nonexistent"])
            mock_append.assert_not_called()

if __name__ == "__main__":
    unittest.main()
