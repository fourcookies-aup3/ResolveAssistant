import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock GUI libraries
mock_modules = ['pyautogui', 'cv2', 'PIL', 'PIL.ImageGrab']
for module in mock_modules:
    sys.modules[module] = MagicMock()

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import editor_actions
from resolve_proxy import MockMediaPoolItem, get_resolve

class TestBoltOptimization(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ["RESOLVE_API_UNAVAILABLE"] = "false"
        import resolve_proxy
        resolve_proxy._resolve_instance = None

    def test_add_clips_to_timeline_optimization(self):
        # Setup mock data
        all_clips = [
            MockMediaPoolItem("/path/to/clip_1.mp4"),
            MockMediaPoolItem("/path/to/clip_2.mp4"),
            MockMediaPoolItem("/path/to/unique_name.mp4")
        ]
        # Assign a different name to clip_2 to test Name vs Path
        all_clips[1].GetName = lambda: "Second Clip"

        target_names = ["clip_1.mp4", "Second Clip", "unique_name.mp4", "non_existent.mp4"]

        # Mock list_clips_in_media_pool
        with unittest.mock.patch('editor_actions.list_clips_in_media_pool') as mock_list:
            mock_list.return_value = all_clips

            # Setup resolve and project
            resolve = get_resolve()
            pm = resolve.GetProjectManager()
            project = pm.CreateProject("Test Bolt")
            project.GetMediaPool().CreateEmptyTimeline("Timeline 1")

            with unittest.mock.patch.object(project.GetMediaPool(), 'AppendToTimeline') as mock_append:
                editor_actions.add_clips_to_timeline(target_names)

                # Verify AppendToTimeline was called with the correct clips
                self.assertTrue(mock_append.called)
                clips_added = mock_append.call_args[0][0]
                self.assertEqual(len(clips_added), 3)
                self.assertEqual(clips_added[0].path, "/path/to/clip_1.mp4")
                self.assertEqual(clips_added[1].path, "/path/to/clip_2.mp4")
                self.assertEqual(clips_added[2].path, "/path/to/unique_name.mp4")

    def test_first_match_behavior(self):
        # Resolve usually takes the first match if multiple clips have same name
        all_clips = [
            MockMediaPoolItem("/path/to/v1/clip.mp4"),
            MockMediaPoolItem("/path/to/v2/clip.mp4")
        ]
        target_names = ["clip.mp4"]

        with unittest.mock.patch('editor_actions.list_clips_in_media_pool') as mock_list:
            mock_list.return_value = all_clips

            resolve = get_resolve()
            pm = resolve.GetProjectManager()
            project = pm.CreateProject("Test Match")
            project.GetMediaPool().CreateEmptyTimeline("Timeline 1")

            with unittest.mock.patch.object(project.GetMediaPool(), 'AppendToTimeline') as mock_append:
                editor_actions.add_clips_to_timeline(target_names)

                clips_added = mock_append.call_args[0][0]
                self.assertEqual(len(clips_added), 1)
                # Should be the first one
                self.assertEqual(clips_added[0].path, "/path/to/v1/clip.mp4")

if __name__ == "__main__":
    unittest.main()
