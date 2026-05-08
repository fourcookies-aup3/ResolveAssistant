import sys
from unittest.mock import MagicMock, patch

# Mock libraries that require a display or specific OS
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

import database
import trainer
import observer
from ai_agent import AIAgent

class TestLearningFeatures(unittest.TestCase):
    def setUp(self):
        os.environ["USE_MOCK_RESOLVE"] = "true"
        # Use in-memory database for tests
        database.engine = database.create_engine('sqlite:///:memory:')
        database.Session = database.sessionmaker(bind=database.engine)
        database.init_db()
        self.agent = AIAgent()

    def test_training_and_retrieval(self):
        # Initial check
        self.assertIsNone(trainer.get_best_grade_params("cinematic"))

        # Train
        trainer.train_from_internet()

        # Verify retrieval
        params = trainer.get_best_grade_params("cinematic")
        self.assertIsNotNone(params)
        self.assertEqual(params["gain"], 1.2)

    @patch('vision.analyze_frame')
    def test_observer_recording(self, mock_analyze):
        mock_analyze.return_value = {"brightness": 100}
        obs = observer.Observer()
        obs.is_observing = True

        # Simulate a click
        obs.on_click(100, 200, "left", True)

        # Verify database record
        session = database.get_session()
        action = session.query(database.ObservedAction).first()
        session.close()

        self.assertIsNotNone(action)
        self.assertEqual(action.action_type, 'click')
        self.assertIn("100", action.details)

if __name__ == "__main__":
    unittest.main()
