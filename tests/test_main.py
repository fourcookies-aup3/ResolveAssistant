import sys
from unittest.mock import MagicMock, patch

# Only set mocks if not already set
for _mod in ['pyautogui', 'PIL', 'PIL.ImageGrab', 'cv2']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import resolve_proxy


class TestMain(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        os.environ.pop("RESOLVE_API_UNAVAILABLE", None)
        resolve_proxy._resolve_instance = None

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    def test_main_exit(self, mock_print, mock_input):
        from main import main
        main()
        mock_print.assert_any_call(
            "Welcome to ResolveAssistant! Your AI-powered video editing companion."
        )

    @patch('builtins.input', side_effect=['quit'])
    @patch('builtins.print')
    def test_main_quit(self, mock_print, mock_input):
        from main import main
        main()
        mock_print.assert_any_call(
            "Welcome to ResolveAssistant! Your AI-powered video editing companion."
        )

    @patch('builtins.input', side_effect=['save project', 'exit'])
    @patch('builtins.print')
    def test_main_command_then_exit(self, mock_print, mock_input):
        from main import main
        main()
        calls = [str(c) for c in mock_print.call_args_list]
        found_save = any("Saving project" in c for c in calls)
        self.assertTrue(found_save)

    @patch('builtins.input', side_effect=EOFError)
    @patch('builtins.print')
    def test_main_eof(self, mock_print, mock_input):
        from main import main
        main()  # Should not raise

    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('builtins.print')
    def test_main_keyboard_interrupt(self, mock_print, mock_input):
        from main import main
        main()  # Should not raise

    @patch('builtins.input', side_effect=['do something unknown', 'exit'])
    @patch('builtins.print')
    def test_main_unknown_command(self, mock_print, mock_input):
        from main import main
        main()
        calls = [str(c) for c in mock_print.call_args_list]
        found_sorry = any("sorry" in c.lower() for c in calls)
        self.assertTrue(found_sorry)

    def tearDown(self):
        resolve_proxy._resolve_instance = None


if __name__ == "__main__":
    unittest.main()
