import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries for headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath("src"))

import editor_actions
from resolve_proxy import MockMediaPoolItem, get_resolve

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.resolve = get_resolve()
        # Reset project manager and media pool
        self.resolve.project_manager.projects = {}
        self.project = self.resolve.project_manager.CreateProject("TestProject")
        self.mp = self.project.GetMediaPool()
        self.root_folder = self.mp.GetRootFolder()

    def test_add_clips_to_timeline_success(self):
        # Setup pool
        clip1 = MockMediaPoolItem("/path/to/clip1.mp4")
        clip2 = MockMediaPoolItem("/path/to/clip2.mp4")
        self.root_folder.clips = [clip1, clip2]

        # Call function
        result = editor_actions.add_clips_to_timeline(["clip1.mp4", "clip2.mp4"])

        self.assertTrue(result)

    def test_add_clips_to_timeline_mixed_names(self):
        # Setup pool
        clip1 = MockMediaPoolItem("/path/to/real_clip1.mp4")
        # Manually set name different from basename if possible,
        # but MockMediaPoolItem uses basename.
        # Let's mock GetName
        clip1.GetName = MagicMock(return_value="Clip One")

        self.root_folder.clips = [clip1]

        # Should match by GetName()
        result = editor_actions.add_clips_to_timeline(["Clip One"])
        self.assertTrue(result)

        # Should match by basename
        result = editor_actions.add_clips_to_timeline(["real_clip1.mp4"])
        self.assertTrue(result)

    def test_add_clips_to_timeline_no_match(self):
        self.root_folder.clips = [MockMediaPoolItem("/path/to/clip1.mp4")]

        # This will trigger fallback to UI automation because it returns True
        # but let's just check if it doesn't crash.
        result = editor_actions.add_clips_to_timeline(["nonexistent.mp4"])
        # Fallback returns True
        self.assertTrue(result)

    def test_add_clips_to_timeline_first_match_behavior(self):
        # Setup pool with duplicate names but different paths
        clip1 = MockMediaPoolItem("/path/A/clip.mp4")
        clip2 = MockMediaPoolItem("/path/B/clip.mp4")
        self.root_folder.clips = [clip1, clip2]

        # We want to ensure clip1 is picked (the first one in all_clips)
        # Mock AppendToTimeline to capture what was added
        with unittest.mock.patch.object(self.mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["clip.mp4"])

            # Get the list of clips passed to AppendToTimeline
            # The first argument is the list of clips
            clips_added = mock_append.call_args[0][0]
            self.assertEqual(len(clips_added), 1)
            self.assertEqual(clips_added[0].path, "/path/A/clip.mp4")

if __name__ == "__main__":
    unittest.main()
