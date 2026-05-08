from sqlalchemy import Column, Integer, String, Float, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class EditingKnowledge(Base):
    __tablename__ = 'editing_knowledge'
    id = Column(Integer, primary_key=True)
    category = Column(String) # e.g., 'color_grade', 'audio_selection', 'ui_location'
    style_name = Column(String) # e.g., 'cinematic'
    data = Column(JSON) # Store parameters like gain, lift, or file patterns
    source = Column(String) # 'internet', 'observation', 'predefined'
    confidence = Column(Float, default=1.0)

class ObservedAction(Base):
    __tablename__ = 'observed_actions'
    id = Column(Integer, primary_key=True)
    page = Column(String)
    action_type = Column(String) # 'click', 'hotkey', 'type'
    details = Column(String)
    visual_context = Column(JSON) # Brightness, dominant color at the time
    timestamp = Column(Float)

# Set up the database
DB_PATH = 'resolve_assistant.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print(f"Database initialized at {DB_PATH}")

def get_session():
    return Session()
