import unittest
import os
import sys
from unittest.mock import MagicMock

# Mocking
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from editor_actions import add_clips_to_timeline
from resolve_proxy import get_resolve, MockMediaPoolItem

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.resolve = get_resolve()
        self.pm = self.resolve.GetProjectManager()
        # Use a unique name for each test
        import uuid
        self.project = self.pm.CreateProject(f"Test Project {uuid.uuid4()}")
        self.mp = self.project.GetMediaPool()
        self.root = self.mp.GetRootFolder()

    def test_add_clips_multiple_matches(self):
        # Create clips with same name but different paths
        clip1 = MockMediaPoolItem("path1/clip.mp4")
        clip2 = MockMediaPoolItem("path2/clip.mp4")

        # In the media pool: clip1 (first), clip2 (second)
        self.root.clips = [clip1, clip2]

        # We want to add "clip.mp4". It should pick clip1 (the first match).
        with unittest.mock.patch.object(self.mp, 'AppendToTimeline') as mock_append:
            add_clips_to_timeline(["clip.mp4"])
            mock_append.assert_called_once()
            added_clips = mock_append.call_args[0][0]
            self.assertEqual(len(added_clips), 1)
            self.assertEqual(added_clips[0].path, "path1/clip.mp4")

    def test_add_clips_by_basename(self):
        clip = MockMediaPoolItem("absolute/path/to/video.mov")
        self.root.clips = [clip]

        with unittest.mock.patch.object(self.mp, 'AppendToTimeline') as mock_append:
            add_clips_to_timeline(["video.mov"])
            mock_append.assert_called_once()
            added_clips = mock_append.call_args[0][0]
            self.assertEqual(added_clips[0].path, "absolute/path/to/video.mov")

    def test_add_clips_not_found(self):
        clip = MockMediaPoolItem("path/to/clip.mp4")
        self.root.clips = [clip]

        with unittest.mock.patch.object(self.mp, 'AppendToTimeline') as mock_append:
            add_clips_to_timeline(["nonexistent.mp4"])
            mock_append.assert_not_called()

if __name__ == "__main__":
    unittest.main()
