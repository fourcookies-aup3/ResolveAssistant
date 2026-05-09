import sys
from unittest.mock import MagicMock, patch

# Mock libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()

import os
import unittest
import time
from sqlalchemy import create_engine

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import database
import watcher
import autonomous_engine

class TestAutonomousSystem(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=database.StaticPool)
        database.init_db(self.engine)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_watcher_detection(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["video1.mp4", "video2.mov"]

        # Test finding new files
        processed = ["video1.mp4"]
        new = watcher.get_new_files(processed)
        self.assertEqual(len(new), 1)
        self.assertIn("video2.mov", new[0])

    @patch('watcher.get_new_files')
    @patch('editor_actions.professional_auto_edit')
    @patch('editor_actions.render_project')
    def test_autonomous_loop_one_cycle(self, mock_render, mock_edit, mock_watcher):
        mock_edit.return_value = True
        # Path with filename
        filepath = os.path.join(watcher.SOURCE_DIR, "new.mp4")
        mock_watcher.side_effect = [[filepath], KeyboardInterrupt]

        # This will run one iteration and then stop due to mock side effect
        with patch('watcher.wait_for_file_ready', return_value=True):
            autonomous_engine.start_fully_autonomous_mode()

        # Verify it attempted to edit and record
        mock_edit.assert_called_once()
        session = database.get_session()
        entry = session.query(database.ProcessedFile).first()
        self.assertEqual(os.path.basename(entry.filename), "new.mp4")

if __name__ == "__main__":
    unittest.main()
