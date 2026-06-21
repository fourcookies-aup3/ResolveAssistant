import unittest
from unittest.mock import MagicMock
import os
import sys

# Mock GUI dependencies
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui
sys.modules["cv2"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["vision"] = MagicMock()

# Add src to path
sys.path.append('src')

class TestBoltOptimization(unittest.TestCase):
    def test_add_clips_to_timeline_logic(self):
        # Mock dependencies
        import resolve_proxy
        from editor_actions import add_clips_to_timeline

        # Setup mock project and media pool
        resolve = resolve_proxy.get_resolve()
        resolve.GetProjectManager().CreateProject("TestProject")
        project = resolve.GetProjectManager().GetCurrentProject()

        # Create mock clips
        clip1 = resolve_proxy.MockMediaPoolItem("/path/to/video1.mp4")
        clip2 = resolve_proxy.MockMediaPoolItem("/path/to/video2.mp4")
        clip3 = resolve_proxy.MockMediaPoolItem("/path/to/other.mov")

        # Manually set clips in mock folder
        project.GetMediaPool().GetRootFolder().clips = [clip1, clip2, clip3]

        # Test finding clips by name
        target_names = ["video1.mp4", "video2.mp4", "nonexistent.mp4"]

        # We need to mock mp.AppendToTimeline to verify what was added
        mp = project.GetMediaPool()
        mp.AppendToTimeline = MagicMock(return_value=True)

        add_clips_to_timeline(target_names)

        # Verify AppendToTimeline was called with [clip1, clip2]
        args, kwargs = mp.AppendToTimeline.call_args
        self.assertEqual(len(args[0]), 2)
        self.assertIn(clip1, args[0])
        self.assertIn(clip2, args[0])
        self.assertNotIn(clip3, args[0])

    def test_add_clips_to_timeline_preserves_first_match(self):
        # Test that if two clips have the same name, the first one found is used
        import resolve_proxy
        from editor_actions import add_clips_to_timeline

        resolve = resolve_proxy.get_resolve()
        resolve.GetProjectManager().CreateProject("TestProjectDuplicate")
        project = resolve.GetProjectManager().GetCurrentProject()

        clip_a = resolve_proxy.MockMediaPoolItem("/path/a/clip.mp4")
        clip_b = resolve_proxy.MockMediaPoolItem("/path/b/clip.mp4")

        project.GetMediaPool().GetRootFolder().clips = [clip_a, clip_b]

        mp = project.GetMediaPool()
        mp.AppendToTimeline = MagicMock(return_value=True)

        add_clips_to_timeline(["clip.mp4"])

        args, kwargs = mp.AppendToTimeline.call_args
        self.assertEqual(args[0][0], clip_a)

if __name__ == "__main__":
    os.environ["USE_MOCK_RESOLVE"] = "true"
    unittest.main()
