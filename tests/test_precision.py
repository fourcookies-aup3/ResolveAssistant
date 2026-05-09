import sys
from unittest.mock import MagicMock, patch

# Configure Mocks
mock_pyautogui = MagicMock()
mock_pil = MagicMock()
mock_cv2 = MagicMock()
mock_tesseract = MagicMock()

sys.modules['pyautogui'] = mock_pyautogui
sys.modules['PIL'] = mock_pil
sys.modules['PIL.ImageGrab'] = mock_pil.ImageGrab
sys.modules['cv2'] = mock_cv2
sys.modules['pynput'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()
sys.modules['pytesseract'] = mock_tesseract

import os
import unittest
import time
import numpy as np
from sqlalchemy import create_engine

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import vision
import input_control
import database

class TestPrecisionFeatures(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=database.StaticPool)
        database.init_db(self.engine)

    def test_ocr_precision(self):
        # Setup mock return for cv2.threshold and image_to_string
        mock_cv2.threshold.return_value = (None, np.zeros((10,10)))
        mock_tesseract.image_to_string.return_value = "Project Manager"

        text = vision.read_text_from_screen()
        self.assertEqual(text, "Project Manager")

    @patch('vision.detect_ui_state')
    def test_precise_click(self, mock_detect):
        mock_detect.return_value = {"page": "edit", "dialog": "none"}
        # Fail if state mismatch
        result = input_control.precise_click_template("btn", expected_state="color")
        self.assertFalse(result)

    def test_secure_type_verification(self):
        with patch('vision.read_text_from_screen') as mock_read:
            mock_read.return_value = "VerifiedText"
            result = input_control.secure_type("SomeInput", verification_text="VerifiedText")
            self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
