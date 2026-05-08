import sys
from unittest.mock import MagicMock, patch

# Mock GUI and other libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import editor_actions
import media_manager
from ai_agent import AIAgent

class TestProfessionalFeatures(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.agent = AIAgent()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_smart_media_selection(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["upbeat_track.mp3", "dark_mood.wav", "normal.mp3"]

        # Test bright context (should pick upbeat)
        context = {"brightness": 200, "dominant_color": "red"}
        selection = media_manager.get_smart_media_selection("music", context)
        self.assertEqual(selection, "upbeat_track.mp3")

        # Test dark context (should pick dark)
        context = {"brightness": 50, "dominant_color": "blue"}
        selection = media_manager.get_smart_media_selection("music", context)
        self.assertEqual(selection, "dark_mood.wav")

    def test_auto_edit_command(self):
        with patch('editor_actions.professional_auto_edit') as mock_auto:
            response = self.agent.process_command("auto edit Wedding Video")
            self.assertIn("Professional Auto-Edit for 'Wedding Video'", response)
            mock_auto.assert_called_once()

    def test_color_grade_command(self):
        with patch('editor_actions.apply_color_grade') as mock_grade:
            response = self.agent.process_command("color grade cinematic")
            self.assertIn("Applying cinematic color grade", response)
            mock_grade.assert_called_once_with("cinematic")

if __name__ == "__main__":
    unittest.main()
