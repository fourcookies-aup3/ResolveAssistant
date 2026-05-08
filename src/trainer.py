import database
from database import EditingKnowledge
import time
import random

def train_from_internet(topic="DaVinci Resolve Color Grading"):
    """
    Simulates searching the internet for tutorials and extracting knowledge.
    In a real implementation, this would use a web scraper or search API.
    """
    print(f"--- Training Mode: Searching internet for '{topic}' ---")
    session = database.get_session()

    # Simulated search results / tutorial findings
    findings = [
        {"style": "cinematic", "data": {"gain": 1.2, "gamma": 0.9, "sat": 1.1}, "info": "Tutorial: High contrast and teal/orange look."},
        {"style": "nature", "data": {"green_boost": 1.15, "exposure": 1.05}, "info": "Guide: Enhancing natural landscapes."},
        {"style": "hd", "data": {"sharpness": 0.5, "detail": 0.3}, "info": "Technical: Optimizing for high-definition clarity."},
        {"style": "colourful", "data": {"saturation": 1.4, "vibrance": 1.2}, "info": "Artistic: Vibrant and punchy colors."}
    ]

    for item in findings:
        print(f"Learning from: {item['info']}")
        knowledge = EditingKnowledge(
            category='color_grade',
            style_name=item['style'],
            data=item['data'],
            source='internet',
            confidence=0.9
        )
        session.add(knowledge)
        time.sleep(1) # Simulate processing time

    session.commit()
    session.close()
    print("Training session complete. Knowledge base updated.")

def get_best_grade_params(style):
    """
    Queries the database for the most confident knowledge on a style.
    """
    session = database.get_session()
    result = session.query(EditingKnowledge).filter_by(style_name=style).order_by(EditingKnowledge.confidence.desc()).first()
    session.close()
    return result.data if result else None
