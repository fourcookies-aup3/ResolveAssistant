import database
from database import EditingKnowledge
import time
import threading
import vision
import webbrowser

_training_active = False

def start_video_training():
    global _training_active
    if _training_active: return
    _training_active = True

    topics = ["https://www.youtube.com/results?search_query=advanced+davinci+resolve+workflow"]
    webbrowser.open(topics[0])

    threading.Thread(target=_training_loop, daemon=True).start()

def stop_video_training():
    global _training_active
    _training_active = False

def _training_loop():
    session = database.get_session()
    print("--- PRECISION TRAINING ACTIVE ---")

    while _training_active:
        # High-fidelity capture: Vision + OCR
        context = vision.analyze_frame()
        screen_text = vision.read_text_from_screen()

        # Learn state-action relationships
        knowledge = EditingKnowledge(
            category='high_precision_workflow',
            style_name='advanced_technique',
            data={
                "visual_context": context,
                "detected_labels": screen_text[:500],
                "confidence_score": 0.95
            },
            source='professional_tutorials',
            confidence=0.95
        )
        session.add(knowledge)
        session.commit()

        print(f"AI: Learned high-precision state from screen (Words: {len(screen_text.split())})")
        time.sleep(2)

    session.close()

def get_best_grade_params(style):
    session = database.get_session()
    result = session.query(EditingKnowledge).filter_by(style_name=style).order_by(EditingKnowledge.confidence.desc()).first()
    session.close()
    return result.data if result else None
