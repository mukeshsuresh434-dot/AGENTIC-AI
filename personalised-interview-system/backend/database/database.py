import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.init_db import Base

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/interview.db")
DB_PATH = os.path.abspath(DB_PATH)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)
