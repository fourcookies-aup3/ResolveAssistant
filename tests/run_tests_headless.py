import unittest
import sys
from unittest.mock import MagicMock

# Mock GUI dependencies
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui
sys.modules["cv2"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["vision"] = MagicMock()

# Mock resolve_proxy to avoid actual API calls
sys.path.append('src')
import resolve_proxy
os_environ = {"USE_MOCK_RESOLVE": "true"}

if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["tests"]))
