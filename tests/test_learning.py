import sys
from unittest.mock import MagicMock, patch

# Global Setup Mocks
mock_pyautogui = MagicMock()
mock_pil = MagicMock()
mock_cv2 = MagicMock()
mock_tesseract = MagicMock()

# Ensure cv2 functions return valid shapes
import numpy as np
mock_cv2.threshold.return_value = (None, np.zeros((10,10)))
mock_cv2.cvtColor.return_value = np.zeros((10,10))
mock_tesseract.image_to_string.return_value = "Advanced Edit Mode"

sys.modules['pyautogui'] = mock_pyautogui
sys.modules['PIL'] = mock_pil
sys.modules['PIL.ImageGrab'] = mock_pil.ImageGrab
sys.modules['cv2'] = mock_cv2
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()
sys.modules['pytesseract'] = mock_tesseract

import os
import unittest
import time
from sqlalchemy import create_engine

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import database
import trainer
import observer
from ai_agent import AIAgent

class TestLearningFeatures(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=database.StaticPool)
        database.init_db(self.engine)
        self.agent = AIAgent()

    @patch('vision.analyze_frame')
    def test_training_cycle(self, mock_analyze):
        mock_analyze.return_value = {"brightness": 150, "dominant_color": "teal"}

        trainer.start_video_training()
        self.assertTrue(trainer._training_active)

        time.sleep(4)

        trainer.stop_video_training()
        self.assertFalse(trainer._training_active)

        session = database.get_session()
        knowledge = session.query(database.EditingKnowledge).first()
        session.close()

        self.assertIsNotNone(knowledge, "Knowledge should have been recorded in training loop")

    @patch('vision.analyze_frame')
    def test_observer_recording(self, mock_analyze):
        mock_analyze.return_value = {"brightness": 100}
        obs = observer.Observer()
        obs.is_observing = True
        obs.on_click(100, 200, "left", True)

        session = database.get_session()
        action = session.query(database.ObservedAction).first()
        session.close()

        self.assertIsNotNone(action)
        self.assertEqual(action.action_type, 'click')

if __name__ == "__main__":
    unittest.main()
