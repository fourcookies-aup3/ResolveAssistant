from sqlalchemy import Column, Integer, String, Float, JSON, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import datetime
import os

Base = declarative_base()

class EditingKnowledge(Base):
    __tablename__ = 'editing_knowledge'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    style_name = Column(String)
    data = Column(JSON)
    source = Column(String)
    confidence = Column(Float, default=1.0)

class ObservedAction(Base):
    __tablename__ = 'observed_actions'
    id = Column(Integer, primary_key=True)
    page = Column(String)
    action_type = Column(String)
    details = Column(String)
    visual_context = Column(JSON)
    timestamp = Column(Float)

class ProcessedFile(Base):
    __tablename__ = 'processed_files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)
    status = Column(String) # 'completed', 'failed'
    processed_at = Column(DateTime, default=datetime.datetime.utcnow)

DB_PATH = 'resolve_assistant.db'

engine_args = {
    'connect_args': {'check_same_thread': False},
    'poolclass': StaticPool
}

engine = create_engine(f'sqlite:///{DB_PATH}', **engine_args)
Session = sessionmaker(bind=engine)

def init_db(custom_engine=None):
    global engine, Session
    if custom_engine:
        engine = custom_engine
        Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    print(f"Database initialized.")

def get_session():
    return Session()
