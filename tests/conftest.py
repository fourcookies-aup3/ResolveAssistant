import sys
from unittest.mock import MagicMock
import os

# Mock GUI dependencies that fail in headless environment
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui

mock_cv2 = MagicMock()
sys.modules["cv2"] = mock_cv2

mock_pil = MagicMock()
sys.modules["PIL"] = mock_pil
sys.modules["PIL.ImageGrab"] = MagicMock()

# Ensure we use mock resolve
os.environ["USE_MOCK_RESOLVE"] = "true"
