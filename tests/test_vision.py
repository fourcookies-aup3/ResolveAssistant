import sys
from unittest.mock import MagicMock, patch

# Only set mocks if not already set
for _mod in ['pyautogui', 'PIL', 'PIL.ImageGrab', 'cv2']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import os
import unittest
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import vision


class TestCaptureScreen(unittest.TestCase):
    def test_capture_screen_success(self):
        mock_img = MagicMock()
        fake_rgb = np.zeros((100, 200, 3), dtype=np.uint8)
        mock_img.__array__ = MagicMock(return_value=fake_rgb)
        fake_bgr = np.ones((100, 200, 3), dtype=np.uint8)

        with patch.object(vision, 'ImageGrab') as mock_ig, \
             patch.object(vision, 'cv2') as mock_cv:
            mock_ig.grab.return_value = mock_img
            mock_cv.cvtColor.return_value = fake_bgr
            mock_cv.COLOR_RGB2BGR = 4

            result = vision.capture_screen()
            self.assertIsNotNone(result)
            self.assertEqual(result.shape, (100, 200, 3))
            mock_cv.cvtColor.assert_called_once()

    def test_capture_screen_exception(self):
        with patch.object(vision, 'ImageGrab') as mock_ig:
            mock_ig.grab.side_effect = Exception("Display not available")
            result = vision.capture_screen()
            self.assertIsNone(result)


class TestFindImageOnScreen(unittest.TestCase):
    def test_template_not_found(self):
        result = vision.find_image_on_screen("/nonexistent/template.png")
        self.assertIsNone(result)

    @patch('vision.capture_screen')
    @patch('os.path.exists')
    def test_screen_capture_fails(self, mock_exists, mock_capture):
        mock_exists.return_value = True
        mock_capture.return_value = None

        result = vision.find_image_on_screen("template.png")
        self.assertIsNone(result)

    @patch('vision.capture_screen')
    @patch('os.path.exists')
    def test_match_found_above_threshold(self, mock_exists, mock_capture):
        mock_exists.return_value = True
        screen = np.zeros((500, 500, 3), dtype=np.uint8)
        mock_capture.return_value = screen

        template = np.zeros((50, 60, 3), dtype=np.uint8)

        with patch.object(vision, 'cv2') as mock_cv:
            mock_cv.imread.return_value = template
            mock_result = MagicMock()
            mock_cv.matchTemplate.return_value = mock_result
            mock_cv.TM_CCOEFF_NORMED = 5
            # max_val=0.9 (above default threshold 0.8), max_loc=(100, 150)
            mock_cv.minMaxLoc.return_value = (0.0, 0.9, (0, 0), (100, 150))

            result = vision.find_image_on_screen("template.png")
            self.assertIsNotNone(result)
            # Center: (100 + 60//2, 150 + 50//2) = (130, 175)
            self.assertEqual(result, (130, 175))

    @patch('vision.capture_screen')
    @patch('os.path.exists')
    def test_match_below_threshold(self, mock_exists, mock_capture):
        mock_exists.return_value = True
        screen = np.zeros((500, 500, 3), dtype=np.uint8)
        mock_capture.return_value = screen

        template = np.zeros((50, 60, 3), dtype=np.uint8)

        with patch.object(vision, 'cv2') as mock_cv:
            mock_cv.imread.return_value = template
            mock_result = MagicMock()
            mock_cv.matchTemplate.return_value = mock_result
            mock_cv.TM_CCOEFF_NORMED = 5
            # max_val=0.5 (below default threshold 0.8)
            mock_cv.minMaxLoc.return_value = (0.0, 0.5, (0, 0), (100, 150))

            result = vision.find_image_on_screen("template.png")
            self.assertIsNone(result)

    @patch('vision.capture_screen')
    @patch('os.path.exists')
    def test_custom_threshold(self, mock_exists, mock_capture):
        mock_exists.return_value = True
        screen = np.zeros((500, 500, 3), dtype=np.uint8)
        mock_capture.return_value = screen

        template = np.zeros((40, 40, 3), dtype=np.uint8)

        with patch.object(vision, 'cv2') as mock_cv:
            mock_cv.imread.return_value = template
            mock_result = MagicMock()
            mock_cv.matchTemplate.return_value = mock_result
            mock_cv.TM_CCOEFF_NORMED = 5
            # max_val=0.6, above custom threshold 0.5
            mock_cv.minMaxLoc.return_value = (0.0, 0.6, (0, 0), (200, 200))

            result = vision.find_image_on_screen("template.png", threshold=0.5)
            self.assertIsNotNone(result)
            # Center: (200 + 40//2, 200 + 40//2) = (220, 220)
            self.assertEqual(result, (220, 220))


if __name__ == "__main__":
    unittest.main()
