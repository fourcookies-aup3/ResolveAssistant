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
    Opens a browser to tutorials and starts a continuous frame analysis loop.
    """
    global _training_active, _training_thread
    if _training_active:
        print("Training is already in progress.")
        return

    _training_active = True

    # Open browser to relevant tutorials
    urls = [
        "https://www.youtube.com/results?search_query=davinci+resolve+color+grading+tutorial",
        "https://www.youtube.com/results?search_query=cinematic+video+editing+tips"
    ]
    print(f"Opening training resources: {urls[0]}")
    webbrowser.open(urls[0])

    _training_thread = threading.Thread(target=_training_loop, daemon=True)
    _training_thread.start()

def stop_video_training():
    global _training_active
    if not _training_active:
        print("No training session is active.")
        return

    print("Stopping training session...")
    _training_active = False
    # The thread is daemon, it will stop with the process or on next loop check
    print("Training stopped. All learned data saved to database.")

def _training_loop():
    """
    Background loop that 'watches' videos and saves patterns to the database.
    """
    session = database.get_session()
    print("--- AI WATCHING VIDEOS: Learning patterns... ---")

    while _training_active:
        # 1. 'See' the screen
        context = vision.analyze_frame()

        # 2. Extract knowledge
        if context['brightness'] > 0:
            knowledge = EditingKnowledge(
                category='visual_pattern',
                style_name='observed_video',
                data={
                    "context": context,
                    "timestamp": time.time()
                },
                source='video_stream',
                confidence=0.75
            )
            session.add(knowledge)
            print(f"AI: Learning from visual frame (Brightness: {context['brightness']:.1f}, Color: {context['dominant_color']})")

        # Periodic save
        session.commit()

        # Watch at 0.5 FPS (every 2 seconds)
        time.sleep(2)

    session.close()

def get_best_grade_params(style):
    session = database.get_session()
    result = session.query(EditingKnowledge).filter_by(style_name=style).order_by(EditingKnowledge.confidence.desc()).first()
    session.close()
    return result.data if result else None
