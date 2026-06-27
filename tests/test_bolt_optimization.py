import sys
import os
import unittest
from unittest.mock import MagicMock

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# Mock GUI dependencies to avoid DISPLAY errors
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()

import editor_actions
from resolve_proxy import MockMediaPoolItem, get_resolve

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        # Reset the mock resolve instance to get a fresh project
        import resolve_proxy
        resolve_proxy._resolve_instance = None
        self.resolve = get_resolve()

    def test_add_clips_to_timeline_functionality(self):
        pm = self.resolve.GetProjectManager()
        project = pm.CreateProject("Test Project")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()

        # Add some clips to media pool
        clip1 = MockMediaPoolItem("clip1.mp4")
        clip2 = MockMediaPoolItem("/path/to/clip2.mp4")
        clip3 = MockMediaPoolItem("clip1.mp4") # Duplicate name

        root_folder.clips.extend([clip1, clip2, clip3])

        # Test adding by name
        result = editor_actions.add_clips_to_timeline(["clip1.mp4", "clip2.mp4"])
        self.assertTrue(result)

        # Test adding by basename
        result = editor_actions.add_clips_to_timeline(["clip2.mp4"])
        self.assertTrue(result)

    def test_add_clips_to_timeline_first_match(self):
        # Verify it picks the first match in the list
        pm = self.resolve.GetProjectManager()
        project = pm.CreateProject("First Match Project")
        mp = project.GetMediaPool()
        root_folder = mp.GetRootFolder()

        clip_a1 = MockMediaPoolItem("clipA.mp4")
        clip_a2 = MockMediaPoolItem("clipA.mp4")

        # Manually set something to distinguish them if possible,
        # or just check that it's the exact object
        root_folder.clips.extend([clip_a1, clip_a2])

        # We need to capture what's passed to AppendToTimeline
        with unittest.mock.patch.object(mp, 'AppendToTimeline') as mock_append:
            editor_actions.add_clips_to_timeline(["clipA.mp4"])
            mock_append.assert_called_once()
            added_clips = mock_append.call_args[0][0]
            self.assertEqual(len(added_clips), 1)
            self.assertIs(added_clips[0], clip_a1)

if __name__ == "__main__":
    unittest.main()
