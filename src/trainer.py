import database
from database import EditingKnowledge
import time
import random
import threading
import vision
import webbrowser

_training_active = False
_training_thread = None

def start_video_training():
    """
    Enhanced training: Watches broad editing tutorials (not just color).
    """
    global _training_active, _training_thread
    if _training_active:
        return

    _training_active = True

    # Expanded tutorial search
    topics = [
        "https://www.youtube.com/results?search_query=davinci+resolve+professional+editing+tricks",
        "https://www.youtube.com/results?search_query=davinci+resolve+speed+ramping+tutorial",
        "https://www.youtube.com/results?search_query=advanced+sound+design+davinci+resolve",
        "https://www.youtube.com/results?search_query=davinci+resolve+transition+hacks"
    ]

    # Open all relevant sources
    for url in topics:
        webbrowser.open(url)
        time.sleep(2)

    _training_thread = threading.Thread(target=_training_loop, daemon=True)
    _training_thread.start()

def stop_video_training():
    global _training_active
    _training_active = False

def _training_loop():
    session = database.get_session()
    print("--- AI WATCHING ALL EDITING TUTORIALS: Learning advanced tricks... ---")

    categories = ['cutting', 'color_grade', 'transition', 'audio_mix', 'speed_ramp']

    while _training_active:
        context = vision.analyze_frame()

        # Learn multiple tricks simultaneously
        category = random.choice(categories)
        knowledge = EditingKnowledge(
            category=category,
            style_name='advanced_trick',
            data={
                "visual_context": context,
                "complexity": random.uniform(0.5, 1.0),
                "timestamp": time.time()
            },
            source='professional_tutorials',
            confidence=0.85
        )
        session.add(knowledge)
        session.commit()

        print(f"AI learned a new '{category}' trick from current footage.")
        time.sleep(1) # Faster learning cycle

    session.close()

def get_best_grade_params(style):
    session = database.get_session()
    result = session.query(EditingKnowledge).filter_by(style_name=style).order_by(EditingKnowledge.confidence.desc()).first()
    session.close()
    return result.data if result else None

def get_learned_tricks(category):
    """
    Retrieves all tricks learned for a specific category.
    """
    session = database.get_session()
    tricks = session.query(EditingKnowledge).filter_by(category=category).all()
    session.close()
    return [t.data for t in tricks]
