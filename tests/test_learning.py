import sys
from unittest.mock import MagicMock, patch

# Mock libraries
sys.modules['pyautogui'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.ImageGrab'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.mouse'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()

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
        # Shared in-memory engine for multithreaded test
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=database.StaticPool)
        database.init_db(self.engine)
        self.agent = AIAgent()

    @patch('vision.analyze_frame')
    def test_training_cycle(self, mock_analyze):
        mock_analyze.return_value = {"brightness": 150, "dominant_color": "teal"}

        trainer.start_video_training()
        self.assertTrue(trainer._training_active)

        # Increase wait time and ensure at least one loop iteration
        time.sleep(4)

        trainer.stop_video_training()
        self.assertFalse(trainer._training_active)

        session = database.get_session()
        knowledge = session.query(database.EditingKnowledge).first()
        session.close()

        self.assertIsNotNone(knowledge, "Knowledge should have been recorded during training loop")
        self.assertEqual(knowledge.source, 'video_stream')

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
