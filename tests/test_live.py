import sys
from unittest.mock import MagicMock, patch

# Mock GUI libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import input_control
import main

class TestLiveAutomation(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"

    @patch('subprocess.Popen')
    @patch('os.path.exists')
    def test_launch_resolve(self, mock_exists, mock_popen):
        mock_exists.return_value = True
        result = input_control.launch_resolve("/fake/path/resolve")
        self.assertTrue(result)
        mock_popen.assert_called_once()

    @patch('input_control.launch_resolve')
    @patch('input_control.wait_for_window')
    @patch('input_control.focus_window')
    @patch('builtins.input', side_effect=['exit'])
    def test_main_startup_sequence(self, mock_input, mock_focus, mock_wait, mock_launch):
        mock_launch.return_value = True
        main.main()
        mock_launch.assert_called_once()
        mock_wait.assert_called_once()
        mock_focus.assert_called()

if __name__ == "__main__":
    unittest.main()
